#!/usr/bin/env python3
"""Reproduce selected reviewed findings against the pinned, cached audit archives.

Run code_audit.py first. This explicitly exercises ONE reviewed ML function and
ONE Pydantic model in isolation, never imports remote modules or unpickles models.
Other probes only parse text or use a local HTTP stub. No cloud/database calls.
Dependencies: requirements-code-audit.txt plus requirements-audit-probes.txt.
"""
import ast
from datetime import datetime, timezone
import difflib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import subprocess
import tarfile
from threading import Thread
from typing import Literal

import pandas as pd
from pydantic import BaseModel, Field, HttpUrl, ValidationError, field_validator
import yaml

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = json.loads((ROOT / "docs/CODE-AUDIT-DATA.json").read_text())
REPOS = {r["name"]: r for r in SNAPSHOT["repositories"]}
RESULTS = []


def source(repo, path):
    sha = REPOS[repo]["commit"]
    archive = ROOT / f".cache/repo-code-audit/devarent--{repo}-{sha}.tar.gz"
    with tarfile.open(archive) as tar:
        for member in tar:
            if member.isfile() and "/".join(member.name.split("/")[1:]) == path:
                return tar.extractfile(member).read().decode("utf-8-sig")
    raise ValueError(f"Missing pinned source {repo}/{path}")


def record(repo, path, result):
    RESULTS.append({"repository": repo, "commit": REPOS[repo]["commit"], "path": path, "result": result})


def patch(repo, path, before, after):
    # Patch payload only; no remote edits. Used solely for reviewed, small fixes.
    directory = ROOT / "docs/audit-patches"
    directory.mkdir(exist_ok=True)
    lines = difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                 fromfile=f"a/{path}", tofile=f"b/{path}")
    diff = "".join(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n"
                   for line in lines)
    (directory / f"{repo}.patch").write_text(diff)
    checkdir = ROOT / ".cache/patch-check" / repo
    target = checkdir / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(before)
    proc = subprocess.run(["git", "apply", "--check", f"--directory={checkdir.relative_to(ROOT)}",
                           str(directory / f"{repo}.patch")], cwd=ROOT, capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(f"Patch applicability check failed: {repo}")


def parse_probes():
    for repo in ("arya123", "uts-ec2-amazon-linux"):
        path = "UTS-EC2-WebHosting/ansible/deploy-static-apache.yml"
        before = source(repo, path)
        try:
            yaml.safe_load(before)
        except yaml.YAMLError:
            pass
        else:
            raise AssertionError("Expected original YAML failure")
        assert before.rstrip().endswith("\nEOF")
        after = before.rstrip()[:-3].rstrip() + "\n"
        assert isinstance(yaml.safe_load(after), list)
        patch(repo, path, before, after)
        record(repo, path, "Original YAML rejected; removing terminal EOF parses; git apply --check passed. Ansible execution not tested.")
    repo, path = "aws-billing-qwen-3-32b", ".vscode/launch.json"
    before = source(repo, path)
    try:
        json.loads(before)
    except json.JSONDecodeError:
        pass
    else:
        raise AssertionError("Expected original JSON failure")
    after = before.replace('"ignoreFailures: true', '"ignoreFailures": true')
    json.loads(after)
    patch(repo, path, before, after)
    record(repo, path, "Original JSON rejected; missing quote fixed and JSON parses; git apply --check passed. Debugger itself not launched.")


def http_probe():
    repo, path = "chromadb-lab", "examples/01_heartbeat.sh"
    before = source(repo, path)
    after = before.replace("curl -sS", "curl -fsS")
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            requests.append(self.path)
            self.send_response(404 if "/v2/" in self.path else 200)
            self.end_headers()
            self.wfile.write(b"{}")

        def log_message(self, *_):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        for script, expected in ((before, ["/api/v2/heartbeat"]),
                                 (after, ["/api/v2/heartbeat", "/api/v1/heartbeat"])):
            requests.clear()
            script = script.replace("localhost:8000", f"127.0.0.1:{server.server_port}")
            proc = subprocess.run(["bash", "--noprofile", "--norc"], input=script, text=True,
                                  capture_output=True, timeout=10,
                                  env={"PATH": "/usr/bin:/bin", "NO_PROXY": "127.0.0.1"})
            assert proc.returncode == 0
            assert requests == expected, requests
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    patch(repo, path, before, after)
    record(repo, path, "Local HTTP stub: original exits 0 on v2 HTTP 404 without trying v1; -f fix calls v1 and succeeds. Patch applicability passed; no Chroma server used.")


def ml_probe():
    repo, path = "ml-pipeline-end-to-end", "inference_deploy.py"
    tree = ast.parse(source(repo, path))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "preprocess_live_traffic")
    module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    namespace = {"pd": pd}
    # Only this small, manually reviewed function: no joblib, saved models or mitigation actions.
    exec(compile(module, path, "exec"), namespace)
    sample = {"protocol_type": "tcp", "service": "ssh", "flag": "SF",
              "src_bytes": 10.0, "dst_bytes": 20.0, "srv_count": 1, "count": 2}
    single = pd.DataFrame([sample])
    batch = pd.DataFrame([{**sample, "service": "http"}, sample])

    class IdentityScaler:
        def transform(self, frame):
            return frame

    preprocess = namespace["preprocess_live_traffic"]
    one = preprocess(single, IdentityScaler(), ["service_ssh"])
    many = preprocess(batch, IdentityScaler(), ["service_ssh"])
    assert int(one.iloc[0, 0]) == 0
    assert int(many.iloc[1, 0]) == 1
    record(repo, path, "Same SSH record: service_ssh=0 alone, =1 in batch with HTTP. Confirms batch-dependent encoding; identity scaler, no model deserialization or training.")


def validation_probe():
    repo, path = "database-labs-demo", "app/main.py"
    before = source(repo, path)
    after = before.replace('@field_validator("name", "category", "notes")',
                           '@field_validator("name", "category", "notes", mode="before")')
    after = after.replace('        return value.strip()',
                          '        return value.strip() if isinstance(value, str) else value')

    def get_model(text):
        tree = ast.parse(text)
        model = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "EngineIn")
        namespace = dict(BaseModel=BaseModel, Field=Field, HttpUrl=HttpUrl,
                         field_validator=field_validator, Literal=Literal)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[model], type_ignores=[])), path, "exec"), namespace)
        return namespace["EngineIn"]

    Original, Fixed = get_model(before), get_model(after)
    payload = {"name": "  ", "category": "  ", "repo_url": "https://example.com"}
    assert Original(**payload).name == ""
    for values in (payload, {**payload, "name": " x "}, {**payload, "name": 123}):
        try:
            Fixed(**values)
        except ValidationError:
            pass
        else:
            raise AssertionError("Expected fixed model to reject invalid input")
    assert Fixed(name=" Redis ", category=" Cache ", repo_url="https://example.com").name == "Redis"
    patch(repo, path, before, after)
    record(repo, path, "Original Pydantic model accepts whitespace-only name/category and emits empty strings. Before-validator rejects blank/one-char/non-string input and trims valid input; patch applies. No production DB touched.")


if __name__ == "__main__":
    parse_probes()
    http_probe()
    ml_probe()
    validation_probe()
    output = {"checked_at": datetime.now(timezone.utc).isoformat(), "probes": RESULTS}
    (ROOT / "docs/CODE-AUDIT-PROBES.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))
