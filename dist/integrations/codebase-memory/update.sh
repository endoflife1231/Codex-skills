#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET=""; SCOPE=project; DRY_RUN=false; UI=false
while (($#)); do case "$1" in
  --target) TARGET="${2:?}"; shift 2;; --scope) SCOPE="${2:?}"; shift 2;;
  --dry-run) DRY_RUN=true; shift;; --ui) UI=true; shift;; *) echo "ERROR: unknown update option: $1" >&2; exit 2;; esac; done
[[ -n "$TARGET" ]] || { echo "ERROR: --target is required" >&2; exit 2; }
args=(--target "$TARGET" --scope "$SCOPE" --auto-index auto --backup --force)
$DRY_RUN && args+=(--dry-run); $UI && args+=(--ui)
"$HERE/install.sh" "${args[@]}"
