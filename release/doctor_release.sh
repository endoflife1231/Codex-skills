#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
status=0

if command -v zip >/dev/null 2>&1; then
  echo "[ok] zip available"
else
  echo "[warn] zip not found"
  status=1
fi

if python3 "$ROOT/dist/verify/validate_dist.py"; then
  echo "[ok] dist validation passed"
else
  echo "[warn] dist validation failed"
  status=1
fi

exit "$status"
