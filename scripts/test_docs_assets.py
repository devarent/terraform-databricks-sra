"""Offline regression tests for generated documentation asset checks."""
import json
from pathlib import Path
import tempfile
import unittest

from check_docs_assets import check_assets

ROOT = Path(__file__).resolve().parent.parent


class DocsAssetsTests(unittest.TestCase):
    def inspect(self, html, assets=(), page='index.html'):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / page
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html)
            for asset in assets:
                p = root / asset
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('asset')
            return check_assets(root, '/sra/')

    def test_missing_build_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = check_assets(Path(tmp), '/sra/')
            self.assertTrue(result['errors'])
            self.assertEqual(result['html_files'], 0)

    def test_existing_absolute_and_relative_assets(self):
        result = self.inspect('<script src="/sra/app.js"></script><img src="../../img/logo.svg">',
                              ('app.js', 'img/logo.svg'), 'docs/page/index.html')
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['local_references'], 2)

    def test_original_favicon_mispath_is_detected(self):
        result = self.inspect('<link rel="icon" href="/sra/repo/docs/src/icon.png">', ('img/icon.svg',))
        self.assertEqual(len(result['errors']), 1)
        self.assertIn('missing local asset', result['errors'][0])

    def test_external_and_data_assets_are_not_fetched(self):
        result = self.inspect('<img src="https://example.invalid/a.png"><img src="//example.invalid/b.png"><img src="data:image/png;base64,AAAA">')
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['local_references'], 0)

    def test_traversal_is_rejected(self):
        result = self.inspect('<script src="/sra/%2e%2e/outside.js"></script>')
        self.assertIn('escapes build', result['errors'][0])

    def test_query_fragment_and_percent_encoding(self):
        result = self.inspect('<link rel="stylesheet" href="/sra/my%20style.css?v=1#x">', ('my style.css',))
        self.assertEqual(result['errors'], [])

    def test_wrong_base_url_and_invalid_base_config(self):
        result = self.inspect('<img src="/other/logo.svg">')
        self.assertIn('outside configured base URL', result['errors'][0])
        with self.assertRaises(ValueError):
            check_assets(Path('.'), 'sra')

    def test_preload_included_but_navigation_links_excluded(self):
        result = self.inspect('<link rel="preload" as="font" href="/sra/font.woff2"><a href="/sra/not-checked/">Page</a>')
        self.assertEqual(result['local_references'], 1)
        self.assertEqual(len(result['errors']), 1)

    def test_docs_runtime_and_favicon_contract(self):
        package = json.loads((ROOT / 'docs/sra/package.json').read_text())
        self.assertEqual(package['engines']['node'], '>=20.0')
        self.assertEqual(package['packageManager'], 'yarn@1.22.22')
        lock = (ROOT / 'docs/sra/yarn.lock').read_text()
        self.assertNotIn('https://registry.yarnpkg.com/', lock)
        self.assertIn('https://registry.npmjs.org/', lock)
        config = (ROOT / 'docs/sra/docusaurus.config.ts').read_text()
        self.assertIn("favicon: 'img/primary-icon-orange-cloud-security.svg'", config)
        self.assertTrue((ROOT / 'docs/sra/static/img/primary-icon-orange-cloud-security.svg').is_file())


if __name__ == '__main__':
    unittest.main()
