#!/usr/bin/env python3
"""Offline HCL syntax and local-module contract checks, NOT terraform validate.

No provider downloads, credentials, cloud access or Terraform execution. Reads
Git-listed .tf/.hcl sources only (including untracked non-ignored source files).
Checks local module paths, required/unsupported inputs and simple module output
references. Does not evaluate expressions, remote modules, resources or providers.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import subprocess
import sys

try:
    import hcl2
    from hcl2.utils import SerializationOptions
except ImportError:
    hcl2 = None

ROOT = Path(__file__).resolve().parent.parent
META_ARGS = {'source', 'version', 'providers', 'count', 'for_each', 'depends_on'}


def git_sources(root):
    paths = subprocess.check_output(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z', '--', '*.tf', '*.hcl'],
        cwd=root, text=True,
    ).split('\0')
    return sorted({Path(p) for p in paths if p and Path(p).suffix in ('.tf', '.hcl')})


def blocks(document, kind):
    return {name: body for group in document.get(kind, []) for name, body in group.items()}


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


def check_sources(root, paths):
    root = root.resolve()
    documents, issues = {}, []
    summary = {'files': len(paths), 'parsed': 0, 'local_modules_checked': 0, 'remote_or_dynamic_modules_skipped': 0}

    def issue(path, rule, detail):
        issues.append({'path': str(path), 'rule': rule, 'detail': detail})

    for path in paths:
        resolved = root / path
        if resolved.is_symlink() or not resolved.resolve().is_relative_to(root):
            issue(path, 'unsafe-path', 'Source must be a regular file inside the checkout')
            continue
        try:
            documents[path] = hcl2.loads(resolved.read_text(), serialization_options=SerializationOptions(
                strip_string_quotes=True, explicit_blocks=False, with_comments=False))
            summary['parsed'] += 1
        except Exception as exc:
            # Avoid echoing possibly sensitive source literals from parser exceptions.
            issue(path, 'hcl-parser', f'{type(exc).__name__}; confirm with Terraform before changing semantics')
    by_dir = defaultdict(dict)
    for path, doc in documents.items():
        if path.suffix == '.tf':
            by_dir[path.parent][path] = doc

    for directory, files in by_dir.items():
        for kind in ('variable', 'output', 'module'):
            seen = set()
            for path, doc in files.items():
                for group in doc.get(kind, []):
                    for name in group:
                        if name in seen:
                            issue(path, 'duplicate-declaration', f'Duplicate {kind} {name} in module directory')
                        seen.add(name)
        local_outputs = {}
        for path, doc in files.items():
            for name, call in blocks(doc, 'module').items():
                source = call.get('source', '')
                if not isinstance(source, str) or not source.startswith(('./', '../')) or '${' in source:
                    summary['remote_or_dynamic_modules_skipped'] += 1
                    continue
                target = (root / directory / source).resolve()
                if not target.is_relative_to(root):
                    issue(path, 'module-outside-checkout', f'Module {name} points outside checkout')
                    continue
                child_files = by_dir.get(target.relative_to(root))
                if not child_files:
                    issue(path, 'missing-local-module', f'Module {name} has no parsed .tf source at its local target')
                    continue
                summary['local_modules_checked'] += 1
                variables = {k: v for child in child_files.values() for k, v in blocks(child, 'variable').items()}
                local_outputs[name] = {k for child in child_files.values() for k in blocks(child, 'output')}
                for arg in sorted(set(call) - set(variables) - META_ARGS):
                    issue(path, 'unsupported-module-input', f'Module {name} does not declare input {arg}')
                for arg in sorted(k for k, v in variables.items() if 'default' not in v and k not in call):
                    issue(path, 'missing-module-input', f'Module {name} requires input {arg}')
        # Simple expressions only, not plain string literals or dynamic module indexes.
        for path, doc in files.items():
            references = set()
            for value in strings(doc):
                for expression in re.findall(r'(?<!\$)\$\{([^{}]*)\}', value):
                    for name, output in re.findall(r'\bmodule\.([\w-]+)(?:\[\d+\])?\.([\w-]+)', expression):
                        if name in local_outputs and output not in local_outputs[name]:
                            references.add((name, output))
            for name, output in sorted(references):
                issue(path, 'unknown-module-output', f'Module {name} does not export {output}')
    return summary | {'issues': issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Print redacted diagnostic JSON')
    args = parser.parse_args()
    if hcl2 is None:
        print('Missing parser: install scripts/requirements-terraform-checks.txt', file=sys.stderr)
        return 2
    result = check_sources(ROOT, git_sources(ROOT))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"HCL: {result['parsed']}/{result['files']} files parsed; {result['local_modules_checked']} local module calls checked.")
        for finding in result['issues']:
            print(f"{finding['path']}: {finding['rule']}: {finding['detail']}")
        print('Not run: provider/schema validation, expression evaluation, fmt, plan, apply, runtime tests.')
    return 1 if result['issues'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
