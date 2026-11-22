"""Offline regression tests: no GitHub account or cloud credentials required."""
import json
from pathlib import Path
import re
import subprocess
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

import audit_repos as audit

ROOT = Path(__file__).resolve().parent.parent
REPO = {
    "name": "demo", "full_name": "devarent/demo", "html_url": "https://github.com/devarent/demo",
    "description": "A | table\nwith <markup>", "language": None, "license": None,
    "default_branch": "main", "size": 1, "open_issues_count": 0, "fork": False,
}


def result(code=0, stdout="{}", stderr=""):
    return subprocess.CompletedProcess([], code, stdout=stdout, stderr=stderr)


class ApiTests(unittest.TestCase):
    @patch.object(audit.subprocess, "run")
    def test_paginated_records(self, run):
        run.return_value = result(stdout='{"name":"first"}\n{"name":"second"}\n')
        self.assertEqual(audit.api("users/demo/repos", paginate=True),
                         [{"name": "first"}, {"name": "second"}])
        self.assertIn("--paginate", run.call_args.args[0])
        self.assertNotIn("--slurp", run.call_args.args[0])

    @patch.object(audit.subprocess, "run")
    def test_empty_account(self, run):
        run.return_value = result(stdout="")
        self.assertEqual(audit.api("users/demo/repos", paginate=True), [])

    @patch.object(audit.subprocess, "run")
    def test_confirmed_404_is_absent(self, run):
        run.return_value = result(1, '{"status":"404"}', "not found")
        self.assertIsNone(audit.api("path", optional=True))
        with self.assertRaises(audit.ApiError):
            audit.api("path")

    @patch.object(audit.subprocess, "run")
    def test_auth_rate_limit_server_and_network_errors_are_not_missing(self, run):
        for code in (401, 403, 429, 500):
            run.return_value = result(1, json.dumps({"status": code}), "API failed")
            with self.subTest(status=code), self.assertRaises(audit.ApiError):
                audit.api("path", optional=True)
        run.return_value = result(1, "", "network error")
        with self.assertRaises(audit.ApiError):
            audit.api("path", optional=True)

    @patch.object(audit.subprocess, "run")
    def test_invalid_json(self, run):
        run.return_value = result(stdout="not JSON")
        with self.assertRaises(audit.ApiError):
            audit.api("path")


class InspectionTests(unittest.TestCase):
    @patch.object(audit, "api")
    def test_license_variants_and_only_workflow_files(self, api):
        api.side_effect = [
            {"name": "Readme.md"},
            [{"name": n, "type": "file"} for n in ("LICENSE.md", "licence.txt", ".gitignore")],
            [{"name": "ci.yml", "type": "file"}, {"name": "checks.yaml", "type": "file"},
             {"name": "README.md", "type": "file"}, {"name": "fake.yml", "type": "dir"}],
        ]
        row = audit.inspect(REPO)
        self.assertEqual(row["license_files"], ["LICENSE.md", "licence.txt"])
        self.assertEqual(row["workflow_files"], ["checks.yaml", "ci.yml"])
        self.assertIsNone(row["license_spdx"])
        self.assertTrue(row["gitignore"])
        self.assertEqual(row["readme"], "Readme.md")
        self.assertEqual(row["errors"], [])

    @patch.object(audit, "api", return_value=None)
    def test_missing_files(self, api):
        row = audit.inspect(REPO)
        self.assertEqual(row["workflow_files"], [])
        self.assertEqual(row["license_files"], [])
        self.assertIsNone(row["readme"])
        self.assertFalse(row["gitignore"])

    @patch.object(audit, "api", side_effect=audit.ApiError("rate limited"))
    def test_errors_remain_unknown(self, api):
        row = audit.inspect(REPO)
        self.assertEqual(len(row["errors"]), 3)
        self.assertNotIn("workflow_files", row)
        self.assertNotIn("license_files", row)
        text = audit.render({"owner": "demo", "fetched_at": "today", "repositories": [row]})
        self.assertIn("unknown | unknown | unknown | unknown | 3", text)

    def test_markdown_escaping(self):
        self.assertEqual(audit.cell(REPO["description"]), "A \\| table with &lt;markup&gt;")


class RepositoryTests(unittest.TestCase):
    def test_snapshot_and_generated_atlas_match(self):
        snapshot = json.loads((ROOT / "docs/REPO-ATLAS.json").read_text())
        rows = snapshot["repositories"]
        self.assertTrue(rows)
        names = [r["name"] for r in rows]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(names, sorted(names, key=str.lower))
        for row in rows:
            self.assertEqual(row["errors"], [], row["name"])
        self.assertEqual(audit.render(snapshot), (ROOT / "docs/REPO-ATLAS.md").read_text())

    def test_maintenance_document_links_exist(self):
        # Check file targets in maintenance docs only; not external URLs or anchors.
        for name in ("README.md", "CONTRIBUTING.md", "docs/REPO-ATLAS.md", "docs/AUDIT-2026-11-22.md",
                     "docs/CODE-AUDIT-2026-11-22.md", "docs/CODE-AUDIT-DATA.md", "docs/audit-patches/README.md",
                     "docs/TERRAFORM-CI-FOLLOWUP.md", "gcp/README.md", "gcp/examples/service_account/README.md"):
            path = ROOT / name
            for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
                # Markdown allows angle-bracket destinations containing spaces.
                url = urlsplit(link[1:-1] if link.startswith('<') and link.endswith('>') else link)
                if url.scheme or url.netloc or not url.path:
                    continue
                with self.subTest(file=name, link=link):
                    self.assertTrue((path.parent / unquote(url.path)).exists())

    def test_hcl_source_visible_and_sensitive_files_ignored(self):
        for path, ignored in (("example/new.hcl", False), ("example/.tflint.hcl", False),
                              ("example/tests/mock.tftest.hcl", False),
                              ("example/.terraform.lock.hcl", True), ("example/secret.tfvars", True),
                              ("example/state.tfstate", True), ("example/plan.tfplan", True)):
            with self.subTest(path=path):
                status = subprocess.run(["git", "check-ignore", "--no-index", "-q", path], cwd=ROOT).returncode
                self.assertIn(status, (0, 1))
                self.assertEqual(status == 0, ignored)


if __name__ == "__main__":
    unittest.main()
