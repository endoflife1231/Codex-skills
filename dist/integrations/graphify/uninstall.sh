#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; ROOT="$(cd "$HERE/../../.." && pwd)"; TARGET="."; CLEAR=false
while (($#)); do case "$1" in --target) TARGET="${2:?}"; shift 2;; --clear-output) CLEAR=true; shift;; *) echo "ERROR: unknown Graphify uninstall option: $1" >&2; exit 2;; esac; done
args=(uninstall --root "$ROOT" --target "$TARGET"); $CLEAR && args+=(--clear-output)
python3 "$HERE/manage.py" "${args[@]}"
echo "OK: managed Graphify adapter removed; graph output preserved unless explicitly cleared"
