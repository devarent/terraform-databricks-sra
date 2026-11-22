#!/usr/bin/env python3
"""Read-only, bounded source audit. Never installs or executes repository code.

Requires gh and PyYAML==6.0.3. Archives are cached outside tracked files; only
coverage and candidate locations (not source/secrets) are written to the report.
"""
import argparse
import ast
import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile
import urllib.request
from urllib.parse import quote

import yaml

from audit_repos import api

ROOT = Path(__file__).resolve().parent.parent
MAX_ARCHIVE = 80 * 1024 * 1024
MAX_EXPANDED = 300 * 1024 * 1024
MAX_FILE = 1024 * 1024
EXCLUDE = {"node_modules", "vendor", ".venv", "venv", ".git", "dist", "build", "target", "__pycache__"}
TEXT_SUFFIXES = {".py", ".json", ".yml", ".yaml", ".sh", ".bash", ".sql", ".cql",
                 ".js", ".jsx", ".ts", ".tsx", ".rs", ".go", ".java", ".php", ".tf",
                 ".hcl", ".md", ".toml", ".xml", ".cpp", ".h", ".ino"}


def inspect_text(path, text):
    """Return parser checks and candidates, not security or correctness verdicts."""
    findings, checks = [], []

    def add(rule, line, detail):
        findings.append({"path": path, "line": line, "rule": rule, "detail": detail})

    suffix = PurePosixPath(path).suffix
    if suffix == ".py":
        checks.append("python_ast")
        try:
            ast.parse(text, filename=path)
        except SyntaxError as exc:
            add("python-syntax", exc.lineno or 1, exc.msg)
    if suffix == ".json":
        checks.append("strict_json")
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            add("json-syntax", exc.lineno, exc.msg + "; review JSONC/intentional fixture before fixing")
    if suffix in (".yaml", ".yml"):
        checks.append("yaml_safe_load")
        if "{{" in text and ("templates/" in path or "{{-" in text):
            checks[-1] = "yaml_template_skipped"
        else:
            try:
                list(yaml.safe_load_all(text))
            except yaml.YAMLError as exc:
                mark = getattr(exc, "problem_mark", None)
                add("yaml-parse", mark.line + 1 if mark else 1,
                    "YAML loader rejected document; custom tags/dialect may need native tooling")
            except (ValueError, RecursionError):
                add("yaml-parse", 1, "YAML loader value/recursion failure; review with native tooling")
    if suffix in (".sh", ".bash"):
        checks.append("bash_syntax")
        try:
            # bash -n parses only. BASH_ENV/ENV removed so no startup code is sourced.
            env = {k: v for k, v in os.environ.items() if k not in ("BASH_ENV", "ENV", "SHELLOPTS", "BASHOPTS")}
            proc = subprocess.run(["bash", "--noprofile", "--norc", "-n"], input=text,
                                  text=True, capture_output=True, timeout=5, env=env)
            if proc.returncode:
                line = re.search(r"line (\d+)", proc.stderr)
                add("shell-syntax", int(line[1]) if line else 1,
                    "bash -n rejected script; stderr/source omitted to avoid leaking literals")
        except subprocess.TimeoutExpired:
            add("shell-timeout", 1, "Syntax check exceeded 5 seconds")
    if path.startswith(".github/workflows/") and suffix in (".yml", ".yaml"):
        checks.append("workflow_patterns")
        for n, line in enumerate(text.splitlines(), 1):
            if re.search(r"^\s*-?\s*uses:\s*\S+@(main|master)\s*(#.*)?$", line):
                add("mutable-action", n, "Action uses a moving branch; pin a reviewed commit")
        if not any(line.strip() and not line.lstrip().startswith("#") for line in text.splitlines()):
            add("inactive-workflow", 1, "Workflow file contains comments/whitespace only")
    if PurePosixPath(path).name in ("compose.yml", "compose.yaml", "docker-compose.yml", "docker-compose.yaml"):
        checks.append("compose_patterns")
        try:
            doc = yaml.safe_load(text)
            services = doc.get("services", {}) if isinstance(doc, dict) else {}
            for name, service in services.items():
                if not isinstance(service, dict):
                    continue
                for port in service.get("ports", []) or []:
                    if isinstance(port, dict):
                        exposed = "published" in port and port.get("host_ip", "0.0.0.0") in ("0.0.0.0", "::")
                    else:
                        # Two-field HOST:CONTAINER form publishes on all interfaces.
                        exposed = bool(re.fullmatch(r"\d+:\d+(?:/(tcp|udp))?", str(port)))
                    if exposed:
                        add("compose-public-port", 1, f"Service {name}: published port lacks loopback binding; review local-only lab threat model")
                        break
                if service.get("privileged") is True:
                    add("privileged-container", 1, f"Service {name}: privileged=true; assess whether required")
        except (yaml.YAMLError, AttributeError, TypeError, ValueError, RecursionError):
            pass  # YAML parse error recorded above; not a Compose schema validator.
    return checks, findings


def download(full_name, sha, cache):
    dest = cache / f"{full_name.replace('/', '--')}-{sha}.tar.gz"
    if dest.exists():
        if dest.stat().st_size > MAX_ARCHIVE:
            raise ValueError("cached archive exceeds size cap")
        return dest
    url = f"https://codeload.github.com/{full_name}/tar.gz/{sha}"
    tmp = dest.with_suffix(".partial")
    try:
        with urllib.request.urlopen(url, timeout=60) as response, tmp.open("wb") as output:
            total = 0
            while chunk := response.read(1024 * 1024):
                total += len(chunk)
                if total > MAX_ARCHIVE:
                    raise ValueError("archive exceeds 80 MiB cap")
                output.write(chunk)
        tmp.replace(dest)
    finally:
        tmp.unlink(missing_ok=True)
    return dest


def inspect_tree_sample(repo, row, counts, skips):
    """Bounded fallback for oversized archives; explicitly not full source coverage."""
    tree = api(f"repos/{repo['full_name']}/git/trees/{row['commit']}?recursive=1")
    row["method"] = "tree-sample (archive exceeded cap)"
    row["tree_truncated"] = tree.get("truncated", False)
    blobs = [e for e in tree["tree"] if e["type"] == "blob"]
    row["files_seen"] = len(blobs)
    candidates = []
    for entry in blobs:
        path = PurePosixPath(entry["path"])
        if EXCLUDE.intersection(path.parts):
            skips["dependency_or_generated_dir"] += 1
        elif entry.get("size", MAX_FILE + 1) > MAX_FILE:
            skips["over_1_MiB"] += 1
        elif path.suffix not in TEXT_SUFFIXES and path.name not in ("Dockerfile", "Makefile"):
            skips["unsupported_extension"] += 1
        else:
            candidates.append(entry)
    # Prioritize workflows and root entry points. Record uninspected source count.
    candidates.sort(key=lambda e: (not e["path"].startswith(".github/workflows/"), e["path"].count("/"), e["path"]))
    skips["source_outside_120_file_sample"] += max(0, len(candidates) - 120)
    row["sampled_paths"] = []
    for entry in candidates[:120]:
        blob = api(f"repos/{repo['full_name']}/git/blobs/{entry['sha']}")
        raw = base64.b64decode(blob["content"])
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            skips["non_utf8"] += 1
            continue
        if "\x00" in text:
            skips["binary"] += 1
            continue
        row["sampled_paths"].append(entry["path"])
        row["text_files_read"] += 1
        row["bytes_read"] += len(raw)
        checks, findings = inspect_text(entry["path"], text)
        counts.update(checks)
        if not checks:
            skips["read_but_no_parser_for_language"] += 1
        row["findings"].extend(findings)
    if tree.get("truncated"):
        row["errors"].append("Git tree truncated; inventory is incomplete")


def inspect_repo(repo, cache):
    row = {"name": repo["name"], "full_name": repo["full_name"], "commit": None,
           "files_seen": 0, "text_files_read": 0, "bytes_read": 0,
           "checks": {}, "skipped": {}, "findings": [], "errors": []}
    counts, skips = Counter(), Counter()
    try:
        branch = api(f"repos/{repo['full_name']}/commits/{quote(repo['default_branch'], safe='')}")
        row["commit"] = branch["sha"]
        try:
            archive = download(repo["full_name"], row["commit"], cache)
        except ValueError as exc:
            if "archive exceeds" not in str(exc):
                raise
            inspect_tree_sample(repo, row, counts, skips)
            row["checks"], row["skipped"] = dict(counts), dict(skips)
            return row
        row["method"] = "bounded archive scan"
        expanded = 0
        with tarfile.open(archive, "r|gz") as tar:
            for member in tar:
                if not member.isfile():
                    skips["non_regular_member"] += 1
                    continue
                row["files_seen"] += 1
                expanded += member.size
                if expanded > MAX_EXPANDED or row["files_seen"] > 60000:
                    raise ValueError("expanded-size/member-count cap reached; partial coverage")
                path = PurePosixPath(member.name)
                if path.is_absolute() or ".." in path.parts or len(path.parts) < 2:
                    skips["unsafe_path"] += 1
                    continue
                path = PurePosixPath(*path.parts[1:])
                if EXCLUDE.intersection(path.parts):
                    skips["dependency_or_generated_dir"] += 1
                    continue
                if member.size > MAX_FILE:
                    skips["over_1_MiB"] += 1
                    continue
                if path.suffix not in TEXT_SUFFIXES and path.name not in ("Dockerfile", "Makefile"):
                    skips["unsupported_extension"] += 1
                    continue
                raw = tar.extractfile(member).read(MAX_FILE + 1)
                try:
                    text = raw.decode("utf-8-sig")
                except UnicodeDecodeError:
                    skips["non_utf8"] += 1
                    continue
                if "\x00" in text:
                    skips["binary"] += 1
                    continue
                row["text_files_read"] += 1
                row["bytes_read"] += len(raw)
                checks, findings = inspect_text(str(path), text)
                counts.update(checks)
                if not checks:
                    skips["read_but_no_parser_for_language"] += 1
                row["findings"].extend(findings)
    except Exception as exc:
        # No source snippets or network response bodies in output.
        row["errors"].append(f"{type(exc).__name__}: {str(exc)[:240]}")
    row["checks"], row["skipped"] = dict(counts), dict(skips)
    print(f"{row['name']}: read={row['text_files_read']} candidates={len(row['findings'])} errors={len(row['errors'])}", flush=True)
    return row


def render_coverage(snapshot):
    lines = ["# Source audit — coverage for every repository", "",
             f"Snapshot: {snapshot['fetched_at']}. See [reviewed findings](CODE-AUDIT-2026-11-22.md).", "",
             "Text read is not human-reviewed or runtime-tested. Parser counts exclude templates; zero candidates is NOT a clean bill of health.",
             "For tree fallback, the source sample is bounded to 120 files. Details of skips and errors are in the accompanying JSON.", "",
             "| Repository / pinned commit | Method | Regular files inventoried | Text read | Parser checks | Raw candidates | Acquisition errors |",
             "|---|---|---|---|---|---|---|"]
    for row in snapshot['repositories']:
        link = f"https://github.com/{row['full_name']}/tree/{row['commit']}" if row['commit'] else f"https://github.com/{row['full_name']}"
        method = row.get('method', 'bounded archive scan')
        parsed = sum(row['checks'].get(key, 0) for key in ('python_ast', 'strict_json', 'yaml_safe_load', 'bash_syntax'))
        lines.append(f"| [{row['name']}]({link}) | {method} | {row['files_seen']} | {row['text_files_read']} | {parsed} | {len(row['findings'])} | {len(row['errors'])} |")
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=ROOT / ".cache/repo-code-audit")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/CODE-AUDIT-DATA.json")
    parser.add_argument("--repos", nargs="*", help="Optional exact names from saved atlas")
    args = parser.parse_args()
    repos = json.loads((ROOT / "docs/REPO-ATLAS.json").read_text())["repositories"]
    if args.repos:
        unknown = set(args.repos) - {r["name"] for r in repos}
        if unknown:
            parser.error("Unknown repository names")
        repos = [r for r in repos if r["name"] in args.repos]
    args.cache.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda r: inspect_repo(r, args.cache), repos))
    snapshot = {"fetched_at": datetime.now(timezone.utc).isoformat(),
                "method": "commit-pinned archive; Python AST, strict JSON, PyYAML safe loader, bash -n, workflow/Compose patterns",
                "limits": {"archive_bytes": MAX_ARCHIVE, "expanded_bytes": MAX_EXPANDED, "file_bytes": MAX_FILE,
                           "excluded_dirs": sorted(EXCLUDE)},
                "warning": "Candidates need triage; no build/runtime/dependency-vulnerability tests. Text read without a parser is not validated.",
                "repositories": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    args.output.with_suffix('.md').write_text(render_coverage(snapshot))
    return int(any(r["errors"] for r in results))


if __name__ == "__main__":
    raise SystemExit(main())
