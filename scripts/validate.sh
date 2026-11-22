#!/usr/bin/env bash
# Offline maintenance checks. No cloud changes, credentials or provider downloads.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
"${PYTHON:-python3}" -m unittest discover -s scripts -p 'test_*.py' -v
bash -n scripts/audit-repos.sh scripts/validate.sh
git diff --check
# Include newly staged files, which an unstaged diff cannot inspect.
git diff --cached --check
if command -v terraform >/dev/null 2>&1; then
  terraform fmt -check -recursive
else
  echo 'SKIP: terraform fmt (Terraform is not installed).'
fi
echo 'NOT RUN: terraform init/validate/test, TFLint, security scanners, docs build, live deployment tests.'
echo 'Offline maintenance checks passed; this is not a deployment or security certification.'
