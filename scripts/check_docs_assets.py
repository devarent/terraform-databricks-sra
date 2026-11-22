#!/usr/bin/env python3
"""Check local HTML asset references in a Docusaurus build; never fetch URLs.

Checks script/img src and stylesheet/icon/preload href. Not a browser, link/anchor
crawler, srcset parser, CSS url() parser or client-side JavaScript runtime test.
"""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag in ('script', 'img') and attrs.get('src'):
            self.urls.append(attrs['src'])
        if tag == 'link' and attrs.get('href'):
            rel = set(attrs.get('rel', '').lower().split())
            if rel.intersection({'icon', 'stylesheet'}) or (
                'preload' in rel and attrs.get('as') in ('image', 'script', 'style', 'font')
            ):
                self.urls.append(attrs['href'])


def check_assets(build_dir, base_url):
    if not base_url.startswith('/') or not base_url.endswith('/'):
        raise ValueError('base URL must begin and end with /')
    root = build_dir.resolve()
    files = sorted(root.rglob('*.html')) if root.is_dir() else []
    if not files:
        return {'html_files': 0, 'local_references': 0, 'errors': ['No built HTML files; run yarn build first']}
    errors, count = [], 0
    for page in files:
        parser = Assets()
        parser.feed(page.read_text(encoding='utf-8'))
        for raw in parser.urls:
            parsed = urlsplit(raw)
            # External/data resources are outside this offline smoke check.
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            count += 1
            path = unquote(parsed.path)
            if path.startswith('/'):
                if not path.startswith(base_url):
                    errors.append(f'{page.relative_to(root)}: asset outside configured base URL: {path}')
                    continue
                target = root / path[len(base_url):]
            else:
                target = page.parent / path
            target = target.resolve()
            if not target.is_relative_to(root):
                errors.append(f'{page.relative_to(root)}: asset escapes build directory')
            elif not target.is_file():
                errors.append(f'{page.relative_to(root)}: missing local asset: {path}')
    return {'html_files': len(files), 'local_references': count, 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, default=Path('docs/sra/build'))
    parser.add_argument('--base-url', default='/terraform-databricks-sra/')
    args = parser.parse_args()
    try:
        result = check_assets(args.build_dir, args.base_url)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Docs assets: {result['html_files']} HTML files, {result['local_references']} local references, {len(result['errors'])} errors")
    for error in result['errors']:
        print(error)
    return int(bool(result['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
