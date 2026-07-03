#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; source "$HERE/common.sh"
TARGET=""; SCOPE=project
while (($#)); do case "$1" in --target) TARGET="${2:?}"; shift 2;; --scope) SCOPE="${2:?}"; shift 2;; *) die "unknown restore option: $1";; esac; done
[[ -n "$TARGET" ]] || die "--target is required"; resolve_layout "$TARGET" "$SCOPE"
if [[ ! -x "$BIN_PATH" ]]; then
  echo "WARNING: managed binary is missing; restoring pinned release"
  "$HERE/install.sh" --target "$TARGET" --scope "$SCOPE" --auto-index off
  exit 0
fi
if ! python3 "$HERE/config_tool.py" check --config "$CONFIG_PATH" >/dev/null 2>&1; then
  "$HERE/configure.sh" --target "$TARGET" --scope "$SCOPE" --binary "$BIN_PATH" --backup
fi
"$HERE/verify.sh" --target "$TARGET" --scope "$SCOPE"
echo "OK: tools restored; existing index was not rebuilt"
