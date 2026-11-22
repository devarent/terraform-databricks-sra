#!/usr/bin/env bash
# Read-only public repository audit; --write refreshes the local atlas + JSON.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/audit_repos.py" "$@"
