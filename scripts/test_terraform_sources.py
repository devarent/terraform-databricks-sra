"""Regression coverage for offline Terraform contracts and CI path triggers."""
import json
from pathlib import Path
import tempfile
import unittest

import validate_terraform_sources as checker

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parent.parent


@unittest.skipIf(checker.hcl2 is None, 'Install scripts/requirements-terraform-checks.txt')
class SourceTests(unittest.TestCase):
    def inspect(self, files):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path, text in files.items():
                dest = root / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(text)
            return checker.check_sources(root, [Path(p) for p in files])

    def test_module_contract_valid(self):
        result = self.inspect({
            'main.tf': 'module "child" { source="./child" project="demo" }\noutput "email" { value=module.child.email }',
            'child/main.tf': 'variable "project" {}\noutput "email" { value="demo@example.com" }',
        })
        self.assertEqual(result['issues'], [])
        self.assertEqual(result['local_modules_checked'], 1)

    def test_original_gcp_example_errors_are_detected(self):
        result = self.inspect({
            'main.tf': 'module "child" { source="./child" prefix="demo" }\noutput "email" { value=module.child.service_account }',
            'child/main.tf': 'variable "sa_name" { default="demo" }\noutput "workspace_creator_email" { value="demo@example.com" }',
        })
        self.assertEqual({i['rule'] for i in result['issues']}, {'unsupported-module-input', 'unknown-module-output'})

    def test_required_input_and_meta_arguments(self):
        result = self.inspect({
            'main.tf': 'module "child" { source="./child" count=1 providers={} depends_on=[] }',
            'child/main.tf': 'variable "required" {}\nvariable "optional" { default=null }',
        })
        self.assertEqual([i['rule'] for i in result['issues']], ['missing-module-input'])

    def test_remote_module_explicitly_skipped(self):
        result = self.inspect({'main.tf': 'module "remote" { source="owner/example/aws" version="1.0.0" }'})
        self.assertEqual(result['issues'], [])
        self.assertEqual(result['remote_or_dynamic_modules_skipped'], 1)
        self.assertEqual(result['local_modules_checked'], 0)

    def test_missing_or_external_source_rejected(self):
        for source, expected in (('./missing', 'missing-local-module'), ('../../outside', 'module-outside-checkout')):
            with self.subTest(source=source):
                result = self.inspect({'main.tf': f'module "child" {{ source="{source}" }}'})
                self.assertEqual(result['issues'][0]['rule'], expected)

    def test_duplicate_output_across_files(self):
        result = self.inspect({'a.tf': 'output "x" { value=1 }', 'b.tf': 'output "x" { value=2 }'})
        self.assertEqual(result['issues'][0]['rule'], 'duplicate-declaration')

    def test_parser_errors_do_not_print_source_literals(self):
        result = self.inspect({'broken.tf': 'variable "secret" { default = "DO_NOT_ECHO_SECRET"\ninvalid @@@'})
        self.assertEqual(result['issues'][0]['rule'], 'hcl-parser')
        self.assertNotIn('DO_NOT_ECHO_SECRET', json.dumps(result))

    def test_multiline_conditional_is_valid(self):
        result = self.inspect({'vpc.tf': 'locals {\n x = false ? "" : (\n true\n ? "yes"\n : "no"\n)\n}'})
        self.assertEqual(result['issues'], [])

    def test_plain_literal_is_not_a_module_reference(self):
        result = self.inspect({
            'main.tf': 'module "child" { source="./child" }\noutput "doc" { value="module.child.nonexistent" }',
            'child/main.tf': 'output "email" { value="demo" }',
        })
        self.assertEqual(result['issues'], [])

    def test_checkout_sources_and_gcp_regression(self):
        paths = checker.git_sources(ROOT)
        self.assertIn(Path('gcp/modules/workspace_deployment/vpc.tf'), paths)
        self.assertTrue(all('.cache' not in path.parts for path in paths))
        result = checker.check_sources(ROOT, paths)
        self.assertEqual(result['parsed'], len(paths))
        self.assertGreater(result['local_modules_checked'], 0)
        self.assertEqual(result['issues'], [])


@unittest.skipIf(yaml is None, 'Install scripts/requirements-code-audit.txt')
class WorkflowContractTests(unittest.TestCase):
    def load(self, name):
        # BaseLoader preserves the YAML key "on" instead of interpreting it as a YAML 1.1 boolean.
        return yaml.load((ROOT / '.github/workflows' / name).read_text(), Loader=yaml.BaseLoader)

    def test_cloud_callers_retest_shared_changes(self):
        for name in ('aws-test.yml', 'azure-test.yml', 'aws-customizations-test.yml'):
            doc = self.load(name)
            with self.subTest(workflow=name):
                for event in ('push', 'pull_request'):
                    self.assertIn('.github/workflows/terraform-ruw.yml', doc['on'][event]['paths'])
                    self.assertIn('common/tests/**', doc['on'][event]['paths'])
                self.assertEqual(doc['permissions'], {'contents': 'read'})
                self.assertIn('${{ github.workflow }}', doc['concurrency']['group'])

    def test_cloud_mock_filters_do_not_enable_live_integration(self):
        for name, job in (('aws-test.yml', 'test-aws'), ('azure-test.yml', 'test-azure')):
            inputs = self.load(name)['jobs'][job]['with']
            self.assertEqual(inputs['terraform_validate_enabled'], 'true')
            args = inputs['terraform_test_args'].split()
            self.assertTrue(args)
            self.assertTrue(all(arg.startswith('-filter=tests/mock_plan') for arg in args))
            self.assertNotIn('integration.tftest.hcl', inputs['terraform_test_args'])

    def test_maintenance_covers_hcl_and_installs_parser(self):
        doc = self.load('maintenance-checks.yml')
        for event in ('push', 'pull_request'):
            self.assertIn('**/*.tf', doc['on'][event]['paths'])
            self.assertIn('**/*.hcl', doc['on'][event]['paths'])
            self.assertIn('.github/workflows/**', doc['on'][event]['paths'])
        scripts = '\n'.join(step.get('run', '') for step in doc['jobs']['offline-checks']['steps'])
        self.assertIn('requirements-terraform-checks.txt', scripts)
        self.assertIn('validate_terraform_sources.py', scripts)
        self.assertNotIn('terraform apply', scripts)


if __name__ == '__main__':
    unittest.main()
