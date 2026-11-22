"""Offline regression tests for the public inventory and non-executing fork planner."""
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

import plan_databricks_portfolio as planner

ROOT = Path(__file__).resolve().parent.parent


def repo(name='sample', owner='databricks', **overrides):
    row = dict(id=1, name=name, full_name=f'{owner}/{name}', html_url=f'https://github.com/{owner}/{name}',
               description='Example | <repo>\ntext', language=None, topics=[], archived=False,
               fork=False, default_branch='main', size=10, pushed_at='2026-11-22T00:00:00Z', license_spdx='MIT')
    return row | overrides


class PlannerTests(unittest.TestCase):
    def test_name_collision_case_insensitive_never_overwrites(self):
        entry = planner.plan_entry(repo('Example'), [repo('example', 'devarent')], [])
        self.assertEqual(entry['action'], 'resolve_name_collision')
        self.assertEqual(entry['public_name_collision'], 'devarent/example')
        self.assertFalse(entry['execution_allowed'])

    def test_existing_direct_fork_under_other_name_is_reused(self):
        fork = {'full_name': 'devarent/renamed', 'parent_full_name': 'databricks/sample', 'source_full_name': 'databricks/sample'}
        entry = planner.plan_entry(repo(), [repo('renamed', 'devarent', fork=True)], [fork])
        self.assertEqual(entry['action'], 'reuse_existing_fork')
        self.assertEqual(entry['confirmed_parent_matches'], ['devarent/renamed'])

    def test_known_root_fork_needs_review_not_duplicate(self):
        fork = {'full_name': 'devarent/other', 'parent_full_name': 'someone/other', 'source_full_name': 'databricks/sample'}
        entry = planner.plan_entry(repo(), [], [fork])
        self.assertEqual(entry['action'], 'review_existing_fork_network')

    def test_unknown_details_do_not_crash_or_confirm_eligibility(self):
        entry = planner.plan_entry(repo(), [], [{'full_name': 'devarent/unknown', 'parent_full_name': None, 'source_full_name': None}])
        self.assertEqual(entry['action'], 'review_before_fork')
        self.assertIn('not verified', entry['fork_eligibility'])
        self.assertFalse(entry['execution_allowed'])

    def test_archive_license_size_and_fork_flags(self):
        entry = planner.plan_entry(repo(archived=True, fork=True, size=102400, license_spdx=None), [], [])
        self.assertEqual(entry['action'], 'catalog_only_archived')
        self.assertEqual(entry['integration_priority'], 'P3-reference')
        self.assertEqual(len(entry['review_flags']), 4)
        self.assertFalse(entry['execution_allowed'])
        custom = planner.plan_entry(repo(license_spdx='NOASSERTION'), [], [])
        self.assertTrue(any('license' in f for f in custom['review_flags']))

    def test_web_same_name_different_owners_preserved(self):
        snapshot = planner.build_snapshot([repo()], [repo(owner='devarent', id=2)], [], 'date')
        items = planner.web_catalog(snapshot)['items']
        self.assertEqual(len({r['id'] for r in items}), 2)
        self.assertEqual({r['source_kind'] for r in items}, {'owned', 'upstream'})
        self.assertTrue(all(r['verification'] == 'metadata_only' for r in items))
        rendered = planner.render_catalog(snapshot)
        self.assertIn('Example \\| &lt;repo&gt; text', rendered)

    @patch.object(planner, 'api')
    def test_api_failure_preserves_existing_outputs(self, api):
        api.side_effect = planner.ApiError('rate limited')
        with tempfile.TemporaryDirectory() as tmp, patch.object(planner, 'OUT', Path(tmp)), patch('sys.argv', ['planner', '--refresh']):
            path = Path(tmp) / 'DATABRICKS-MANIFEST.json'
            path.write_text('original')
            self.assertEqual(planner.main(), 1)
            self.assertEqual(path.read_text(), 'original')
            self.assertEqual(len(list(Path(tmp).iterdir())), 1)

    def test_snapshot_outputs_and_ownership_contract(self):
        out = ROOT / 'docs/portfolio'
        snapshot = json.loads((out / 'DATABRICKS-MANIFEST.json').read_text())
        sources, dest = snapshot['source_repositories'], snapshot['destination_repositories']
        self.assertEqual(len(sources), snapshot['source_count'])
        self.assertEqual(len(dest), snapshot['destination_count'])
        self.assertEqual(len({r['id'] for r in sources}), len(sources))
        self.assertTrue(all(r['full_name'].startswith('databricks/') for r in sources))
        self.assertTrue(all(r['full_name'].startswith('devarent/') for r in dest))
        self.assertTrue(all(r['execution_allowed'] is False for r in sources))
        self.assertFalse(any(snapshot['safety'].values()))
        self.assertEqual(planner.render_catalog(snapshot), (out / 'DATABRICKS-CATALOG.md').read_text())
        self.assertEqual(planner.render_dry_run(snapshot), (out / 'FORK-DRY-RUN.md').read_text())
        actual_web = json.loads((out / 'WEB-CATALOG.json').read_text())
        self.assertEqual(planner.web_catalog(snapshot), actual_web)
        self.assertEqual(len(actual_web['items']), len(sources) + len(dest))
        self.assertEqual(len({r['id'] for r in actual_web['items']}), len(actual_web['items']))
        for item in actual_web['items']:
            self.assertEqual(item['url'], f"https://github.com/{item['id']}")

    def test_document_links_exist(self):
        for path in (ROOT / 'docs/portfolio').glob('*.md'):
            for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
                url = urlsplit(link)
                if url.scheme or url.netloc or not url.path:
                    continue
                with self.subTest(path=path, link=link):
                    self.assertTrue((path.parent / unquote(url.path)).exists())

    def test_execute_flag_is_not_supported(self):
        with patch('sys.argv', ['planner', '--execute']), patch('sys.stderr'), self.assertRaises(SystemExit) as exc:
            planner.main()
        self.assertEqual(exc.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
