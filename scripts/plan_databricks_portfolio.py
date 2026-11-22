#!/usr/bin/env python3
"""Generate a public catalogue, a fork DRY-RUN manifest and web import data.

GitHub GET requests only. No fork/create/push/delete/deploy operations. This tool
never claims that public-name availability implies permission or fork eligibility.
Python stdlib + authenticated gh; reuses the metadata audit's paginated reader.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from audit_repos import ApiError, api, cell

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/portfolio"
SOURCE = "databricks"
TARGET = "devarent"
PRIORITY = {
    "terraform-databricks-sra": "P1", "terraform-provider-databricks": "P1",
    "terraform-databricks-examples": "P1", "cli": "P1", "setup-cli": "P1",
    "databricks-sdk-py": "P1", "databricks-sql-python": "P1", "databricks-sql-nodejs": "P1",
    "app-templates": "P1", "appkit": "P1", "devhub": "P1", "databricks-agent-skills": "P1",
    "zerobus-sdk": "P2", "sdk-js": "P2", "databricks-ai-bridge": "P2",
    "bundle-examples": "P2", "mlops-stacks": "P2", "dbt-databricks": "P2",
    "databricks-sdk-go": "P2", "databricks-sdk-java": "P2", "databricks-jdbc": "P2",
}


def metadata(repo):
    return {key: repo.get(key) for key in (
        "id", "name", "full_name", "html_url", "description", "language", "topics",
        "archived", "fork", "default_branch", "size", "pushed_at"
    )} | {"license_spdx": (repo.get("license") or {}).get("spdx_id")}


def category(repo):
    """Navigation heuristic, not a dependency/runtime classifier."""
    name = repo["name"].lower()
    if "terraform" in name or any(x in name for x in ("cluster-api", "k8s", "container", "docker", "operator")):
        return "Infrastructure / deployment"
    if any(x in name for x in ("sdk", "sql-", "jdbc", "connector", "sqlalchemy", "dbt-")):
        return "SDK / data connector"
    if any(x in name for x in ("appkit", "app-templates", "devhub", "vscode", "responsive-docs")):
        return "Web / developer experience"
    if any(x in name for x in ("ml", "agent", "genai", "automl", "quantum", "genie", "optim")):
        return "AI / ML"
    if any(x in name for x in ("spark", "iceberg", "delta", "table", "data", "postgres", "pg-")):
        return "Data / analytics"
    if any(x in name for x in ("cli", "bazel", "build", "rules", "brew", "style", "ide-")):
        return "Tooling / build"
    return "Other / manual classification"


def plan_entry(repo, destinations, fork_details):
    names = {r["name"].casefold(): r for r in destinations}
    existing = names.get(repo["name"].casefold())
    # Compare IDs/full names from actual API details, not repository descriptions.
    matching = [f for f in fork_details if (f.get("parent_full_name") or "").casefold() == repo["full_name"].casefold()]
    network = [f for f in fork_details if (f.get("source_full_name") or "").casefold() == repo["full_name"].casefold()]
    flags = []
    if repo["archived"]:
        flags.append("archived: reference-only by default")
    if repo["license_spdx"] in (None, "NOASSERTION"):
        flags.append("license terms need manual review; SPDX unknown is not permission")
    if repo["fork"]:
        flags.append("source is itself a fork: inspect root network and upstream attribution")
    if (repo["size"] or 0) >= 100 * 1024:
        flags.append("large GitHub size estimate (>=100 MiB); inspect before copying")
    if matching:
        action = "reuse_existing_fork"
    elif existing:
        action = "resolve_name_collision"
    elif network:
        action = "review_existing_fork_network"
    elif repo["archived"]:
        action = "catalog_only_archived"
    else:
        action = "review_before_fork"
    if existing:
        flags.append("destination name already exists publicly; never overwrite or delete")
    return repo | {
        "category": category(repo),
        "integration_priority": "P3-reference" if repo["archived"] else PRIORITY.get(repo["name"], "P3-review"),
        "priority_basis": "curated relevance to SRA/web/data integration; not a quality rating",
        "proposed_destination": f"{TARGET}/{repo['name']}",
        "public_name_collision": existing["full_name"] if existing else None,
        "confirmed_parent_matches": [f["full_name"] for f in matching],
        "known_root_network_matches": [f["full_name"] for f in network],
        "action": action,
        "review_flags": flags,
        "execution_allowed": False,
        "fork_eligibility": "not verified: private name collisions, source fork-network policy and account permissions require preflight",
    }


def build_snapshot(sources, destinations, fork_details, fetched_at):
    sources = sorted(sources, key=lambda r: r["name"].casefold())
    destinations = sorted(destinations, key=lambda r: r["name"].casefold())
    return {
        "schema_version": 1, "fetched_at": fetched_at, "mode": "dry-run-only",
        "source_owner": SOURCE, "destination_owner": TARGET,
        "scope": "Public repositories only, all REST API pages. No source audit or runtime validation of Databricks repositories.",
        "safety": {"remote_writes": False, "code_copied": False, "private_repositories_checked": False,
                   "licenses_approved": False, "dependencies_installed": False},
        "source_count": len(sources), "destination_count": len(destinations),
        "source_repositories": [plan_entry(r, destinations, fork_details) for r in sources],
        "destination_repositories": destinations,
        "destination_fork_details": fork_details,
    }


def web_catalog(snapshot):
    items = []
    for group, key in (("upstream", "source_repositories"), ("owned", "destination_repositories")):
        for r in snapshot[key]:
            items.append({
                "id": r["full_name"], "github_id": r["id"], "name": r["name"],
                "owner": r["full_name"].split("/")[0], "source_kind": group,
                "url": r["html_url"], "description": r["description"], "language": r["language"],
                "license_spdx": r["license_spdx"], "archived": r["archived"], "fork": r["fork"],
                "category": r.get("category", category(r)), "size_kb": r["size"],
                "integration_priority": r.get("integration_priority"),
                "verification": "metadata_only",
            })
    return {"schema_version": 1, "fetched_at": snapshot["fetched_at"], "items": items}


def render_catalog(snapshot):
    rows = snapshot["source_repositories"]
    licenses = Counter(r["license_spdx"] or "not detected" for r in rows)
    lines = [f"# Databricks — {len(rows)} public repositories", "",
             f"Snapshot UTC: {snapshot['fetched_at']}. Source: `GET /orgs/databricks/repos?type=public&per_page=100` with pagination.", "",
             "This catalogue is **separate from devarent ownership**. It does not copy code or certify code quality/security.",
             "See [integration plan](WEB-INTEGRATION-PLAN.md), [fork dry-run](FORK-DRY-RUN.md), [manifest](DATABRICKS-MANIFEST.json) and [web import data](WEB-CATALOG.json).", "",
             f"- Public destinations observed: **{snapshot['destination_count']}** (listed separately in the JSON manifest; original [devarent atlas](../REPO-ATLAS.md) retained).",
             f"- Archived: **{sum(r['archived'] for r in rows)}**. Forks of other repositories: **{sum(r['fork'] for r in rows)}**.",
             "- License classification: " + "; ".join(f"{cell(k)}: {v}" for k, v in sorted(licenses.items())) + ".",
             "- P1: review first for SRA/web integration; P2: optional use-case integrations; P3: reference/review only. These are recommendations, not installations.",
             "- Category is a name-based navigation heuristic; language is GitHub primary language, not all languages present.",
             "- `NOASSERTION` / missing SPDX require reading actual terms; a known SPDX is not a full licensing approval.", "",
             "| Repository | Description | Language | SPDX | Archived | Fork | Category | Priority | GitHub KB |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| [{r['name']}]({r['html_url']}) | {cell(r['description'])} | {cell(r['language'])} | {cell(r['license_spdx'])} | {r['archived']} | {r['fork']} | {r['category']} | {r['integration_priority']} | {r['size']} |")
    return "\n".join(lines) + "\n"


def render_dry_run(snapshot):
    rows = snapshot["source_repositories"]
    counts = Counter(r["action"] for r in rows)
    lines = ["# Fork plan — DRY RUN ONLY", "", f"Snapshot: {snapshot['fetched_at']}.", "",
             "**No forks created, no pushes, no remote repository edits. Every entry has `execution_allowed: false`.**", "",
             "Decisions: " + "; ".join(f"`{k}`: {v}" for k, v in sorted(counts.items())) + ".", "",
             "## Preflight before any future execution", "",
             "1. Review source LICENSE/NOTICE, fork-network root, account permissions and GitHub policy. Do not replace custom/Other licenses with MIT.",
             "2. This inventory reads public destinations only. An apparently free name can still collide with a private repo; verify privately through authenticated GitHub tooling, never by posting credentials in chat.",
             "3. Existing forks should normally be reused. Never overwrite, rename or delete an existing repo to make a bulk operation succeed.",
             "4. A source that is itself a fork may share a root network with a destination under a different name. Such roots have NOT all been resolved; public-name checks alone cannot prove fork eligibility.",
             "5. Archived projects are catalogue-only by default; inspect modern replacements. Do not enable inherited Actions, webhooks, Pages, secrets or deployments automatically.",
             "6. Review large history/LFS/submodules and preservation of attribution. GitHub size is an estimate, not download/storage accounting.",
             "7. Authorize a small reviewed batch in a separate appropriate workflow/session; recheck collisions immediately before changes and record outcomes. This tool deliberately has NO execute option.", "",
             "## Per-repository decisions", "",
             "Names below are proposals, not confirmed available destinations. Flags are review gates, not automatic refusals or legal advice.", "",
             "| Source | Proposed destination | Public collision | Existing direct-parent fork | Action | Review flags |",
             "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| [{r['full_name']}]({r['html_url']}) | {r['proposed_destination']} | {cell(r['public_name_collision'])} | {cell(', '.join(r['confirmed_parent_matches']) or None)} | `{r['action']}` | {cell('; '.join(r['review_flags']) or 'Manual preflight still required')} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="GET fresh metadata; overwrite local outputs only")
    args = parser.parse_args()
    path = OUT / "DATABRICKS-MANIFEST.json"
    try:
        if args.refresh:
            raw_source = api("orgs/databricks/repos?type=public&per_page=100", paginate=True)
            raw_dest = api("users/devarent/repos?type=owner&per_page=100", paginate=True)
            details = []
            for r in raw_dest:
                if r["fork"]:
                    detail = api(f"repos/{r['full_name']}")
                    details.append({"full_name": detail["full_name"],
                                    "parent_full_name": (detail.get("parent") or {}).get("full_name"),
                                    "source_full_name": (detail.get("source") or {}).get("full_name")})
            snapshot = build_snapshot([metadata(r) for r in raw_source], [metadata(r) for r in raw_dest],
                                      details, datetime.now(timezone.utc).isoformat())
        else:
            snapshot = json.loads(path.read_text())
    except (ApiError, OSError, ValueError) as exc:
        print(f"Planning failed; existing outputs left unchanged: {exc}", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = {
        "DATABRICKS-MANIFEST.json": json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        "WEB-CATALOG.json": json.dumps(web_catalog(snapshot), ensure_ascii=False, indent=2) + "\n",
        "DATABRICKS-CATALOG.md": render_catalog(snapshot),
        "FORK-DRY-RUN.md": render_dry_run(snapshot),
    }
    for name, content in outputs.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"DRY RUN: {snapshot['source_count']} upstream + {snapshot['destination_count']} owned public repos. Remote writes: 0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
