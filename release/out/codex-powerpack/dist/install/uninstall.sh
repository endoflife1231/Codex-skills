#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET=""; CLEAR_CACHE=false; DRY_RUN=false
while (($#)); do case "$1" in --target) TARGET="${2:?}"; shift 2;; --codebase-memory-clear-cache|--clear-cache) CLEAR_CACHE=true; shift;; --dry-run) DRY_RUN=true; shift;; *) echo "ERROR: unknown option: $1" >&2; exit 2;; esac; done
[[ -n "$TARGET" ]] || { echo "ERROR: --target is required" >&2; exit 2; }
cbm_state="$TARGET/.codex-powerpack/state/codebase-memory.json"
if [[ -f "$cbm_state" ]]; then
  args=(--target "$TARGET"); $CLEAR_CACHE && args+=(--clear-cache); $DRY_RUN && args+=(--dry-run)
  "$ROOT/dist/integrations/codebase-memory/uninstall.sh" "${args[@]}"
fi
args=(uninstall --target "$TARGET"); $DRY_RUN && args+=(--dry-run)
python3 "$ROOT/dist/install/project_files.py" "${args[@]}"
echo "OK: managed Codex Powerpack files removed"
