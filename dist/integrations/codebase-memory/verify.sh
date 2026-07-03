#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; source "$HERE/common.sh"
TARGET=""; SCOPE=project
while (($#)); do case "$1" in --target) TARGET="${2:?}"; shift 2;; --scope) SCOPE="${2:?}"; shift 2;; *) die "unknown verify option: $1";; esac; done
[[ -n "$TARGET" ]] || die "--target is required"; resolve_layout "$TARGET" "$SCOPE"
[[ -x "$BIN_PATH" ]] || die "binary missing or not executable: $BIN_PATH"
[[ -f "$STATE_PATH" ]] || die "state missing: $STATE_PATH"
python3 "$HERE/config_tool.py" check --config "$CONFIG_PATH"
python3 "$HERE/managed_text.py" check --file "$AGENTS_PATH"
expected="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["binary_sha256"])' "$STATE_PATH")"
actual="$(sha256_file "$BIN_PATH")"; [[ "$actual" == "$expected" ]] || die "binary checksum differs from state"
"$BIN_PATH" --version >/dev/null 2>&1 || die "binary version check failed"
[[ -w "$CACHE_DIR" ]] || die "cache is not writable: $CACHE_DIR"
ok "Codebase Memory integration verified"
