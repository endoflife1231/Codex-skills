#!/usr/bin/env bash
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; source "$HERE/common.sh"
TARGET=""; SCOPE=project; status=0
while (($#)); do case "$1" in --target) TARGET="${2:?}"; shift 2;; --scope) SCOPE="${2:?}"; shift 2;; *) echo "ERROR: unknown option $1"; exit 2;; esac; done
[[ -n "$TARGET" ]] || { echo "ERROR: --target is required"; exit 2; }; resolve_layout "$TARGET" "$SCOPE"
check() { if "$@"; then echo "OK: $*"; else echo "ERROR: $*"; echo "SUGGESTED FIX: rerun the Powerpack installer with --with-codebase-memory"; status=1; fi; }
check test -x "$BIN_PATH"
check test -f "$STATE_PATH"
check python3 "$HERE/config_tool.py" check --config "$CONFIG_PATH"
check python3 "$HERE/managed_text.py" check --file "$AGENTS_PATH"
check test -w "$CACHE_DIR"
if [[ -d "$TARGET/graphify-out" ]]; then echo "OK: Graphify output coexists with Codebase Memory"; else echo "WARNING: Graphify is not detected (optional)"; fi
if grep -q 'caveman' "$AGENTS_PATH" 2>/dev/null; then echo "OK: Caveman policy detected and does not alter MCP output"; else echo "WARNING: Caveman policy not detected (integration remains functional)"; fi
if find "$CACHE_DIR" -type f -name '*.db' -print -quit 2>/dev/null | grep -q .; then echo "OK: index database detected"; else echo "WARNING: no index yet; run index.sh when ready"; fi
exit "$status"
