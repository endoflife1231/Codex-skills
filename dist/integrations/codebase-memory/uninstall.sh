#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; source "$HERE/common.sh"
TARGET=""; SCOPE=project; CLEAR_CACHE=false; DRY_RUN=false
while (($#)); do case "$1" in
  --target) TARGET="${2:?}"; shift 2;; --scope) SCOPE="${2:?}"; shift 2;;
  --clear-cache) CLEAR_CACHE=true; shift;; --dry-run) DRY_RUN=true; shift;; *) die "unknown uninstall option: $1";; esac; done
[[ -n "$TARGET" ]] || die "--target is required"; resolve_layout "$TARGET" "$SCOPE"
if $DRY_RUN; then
  echo "DRY-RUN: remove managed MCP/AGENTS/.cbmignore blocks, $BIN_PATH and $STATE_PATH"
  $CLEAR_CACHE && echo "DRY-RUN: remove cache $CACHE_DIR"
  exit 0
fi
python3 "$HERE/config_tool.py" remove --config "$CONFIG_PATH" --backup
python3 "$HERE/managed_text.py" remove --file "$AGENTS_PATH" --backup
python3 "$HERE/ignore_tool.py" remove --target "$TARGET/.cbmignore"
rm -f -- "$BIN_PATH" "$STATE_PATH"
if $CLEAR_CACHE; then rm -rf -- "$CACHE_DIR"; else echo "OK: cache preserved at $CACHE_DIR"; fi
ok "Codebase Memory integration removed"
