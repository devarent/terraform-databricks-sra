"""Offline parser regression tests. Optional dependency: PyYAML from audit requirements."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

try:
    import yaml
except ImportError:
    yaml = None
if yaml is not None:
    import code_audit as audit


@unittest.skipIf(yaml is None, "Install scripts/requirements-code-audit.txt for code-audit tests")
class CodeAuditTests(unittest.TestCase):
    def rules(self, path, text):
        return {f['rule'] for f in audit.inspect_text(path, text)[1]}

    def test_python_parse_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "must-not-exist"
            text = f"open({str(target)!r}, 'w').write('executed')\n"
            self.assertEqual(self.rules('app.py', text), set())
            self.assertFalse(target.exists())
        self.assertEqual(self.rules('app.py', 'def broken(:\n'), {'python-syntax'})

    def test_json_error_location(self):
        _, findings = audit.inspect_text('launch.json', '{\n"ignoreFailures: true\n}')
        self.assertEqual(findings[0]['rule'], 'json-syntax')
        self.assertEqual(findings[0]['line'], 2)
        self.assertEqual(self.rules('package.json', '{"private":true}'), set())

    def test_yaml_literal_eof_rejected(self):
        self.assertEqual(self.rules('playbook.yml', '- hosts: all\nEOF'), {'yaml-parse'})
        self.assertEqual(self.rules('playbook.yml', '- hosts: all\n'), set())

    def test_yaml_unsafe_tags_not_constructed(self):
        self.assertEqual(self.rules('a.yml', '!!python/object/apply:os.system ["echo unsafe"]'), {'yaml-parse'})

    def test_templates_record_skipped_not_validated(self):
        checks, findings = audit.inspect_text('templates/a.yaml', 'value: {{ .Values.x }}')
        self.assertEqual(checks, ['yaml_template_skipped'])
        self.assertEqual(findings, [])

    def test_shell_syntax_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'must-not-exist'
            self.assertEqual(self.rules('a.sh', f'touch "{target}"\n'), set())
            self.assertFalse(target.exists())
        self.assertEqual(self.rules('a.sh', 'if then\n'), {'shell-syntax'})

    def test_compose_loopback_and_public(self):
        loopback = 'services:\n  db:\n    ports: ["127.0.0.1:5432:5432"]\n'
        public = loopback.replace('127.0.0.1:', '')
        self.assertEqual(self.rules('compose.yml', loopback), set())
        self.assertIn('compose-public-port', self.rules('compose.yml', public))
        longform = 'services:\n  db:\n    ports:\n      - target: 5432\n        published: 5432\n        host_ip: 127.0.0.1\n'
        self.assertEqual(self.rules('compose.yml', longform), set())

    def test_workflow_moving_branch(self):
        text = 'jobs:\n  test:\n    steps:\n      - uses: actions/checkout@main\n'
        self.assertIn('mutable-action', self.rules('.github/workflows/a.yml', text))
        self.assertEqual(self.rules('.github/workflows/a.yml', '# disabled\n'), {'inactive-workflow'})

    def test_saved_coverage_consistency(self):
        import json
        root = Path(__file__).resolve().parent.parent
        snapshot = json.loads((root / 'docs/CODE-AUDIT-DATA.json').read_text())
        names = [r['name'] for r in snapshot['repositories']]
        atlas = json.loads((root / 'docs/REPO-ATLAS.json').read_text())
        self.assertEqual(set(names), {r['name'] for r in atlas['repositories']})
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(audit.render_coverage(snapshot), (root / 'docs/CODE-AUDIT-DATA.md').read_text())
        for row in snapshot['repositories']:
            self.assertRegex(row['commit'], r'^[0-9a-f]{40}$')
            self.assertEqual(row['errors'], [], row['name'])

    @patch('code_audit.api')
    def test_tree_sample_bound_and_skip_accounting(self, api):
        import base64
        entries = [{'type': 'blob', 'path': f'file-{i:03}.py', 'size': 5, 'sha': str(i)} for i in range(125)]
        api.side_effect = [{'tree': entries, 'truncated': False}] + [
            {'content': base64.b64encode(b'x = 1').decode()} for _ in range(120)]
        counts, skips = audit.Counter(), audit.Counter()
        row = {'commit': 'a' * 40, 'files_seen': 0, 'text_files_read': 0, 'bytes_read': 0,
               'findings': [], 'errors': []}
        audit.inspect_tree_sample({'full_name': 'example/repo'}, row, counts, skips)
        self.assertEqual(row['text_files_read'], 120)
        self.assertEqual(skips['source_outside_120_file_sample'], 5)
        self.assertEqual(counts['python_ast'], 120)
        self.assertEqual(api.call_count, 121)


if __name__ == '__main__':
    unittest.main()
