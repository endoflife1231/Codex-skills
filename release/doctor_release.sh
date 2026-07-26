#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
status=0
for cmd in python3 zip; do
  if command -v "$cmd" >/dev/null 2>&1; then echo "[ok] $cmd available"; else echo "[error] $cmd missing"; status=1; fi
done
python3 "$ROOT/dist/verify/validate_dist.py" || status=1
for file in README.md README.ru.md LICENSE THIRD_PARTY_NOTICES.md OPEN_SOURCE_AUDIT.md VERSION; do
  [[ -s "$ROOT/$file" ]] || { echo "[error] missing $file"; status=1; }
done
exit "$status"
