#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; source "$HERE/common.sh"
TARGET=""; SCOPE=project; FORCE=false; WATCH=false; DRY_RUN=false
while (($#)); do case "$1" in
  --target) TARGET="${2:?}"; shift 2;; --scope) SCOPE="${2:?}"; shift 2;;
  --force|--rebuild) FORCE=true; shift;; --watch) WATCH=true; shift;; --dry-run) DRY_RUN=true; shift;;
  --incremental) shift;; *) die "unknown index option: $1";; esac; done
[[ -n "$TARGET" ]] || die "--target is required"; resolve_layout "$TARGET" "$SCOPE"
[[ -x "$BIN_PATH" ]] || die "managed binary missing: $BIN_PATH"
mkdir -p "$CACHE_DIR" "$STATE_DIR/logs"
python3 "$HERE/ignore_tool.py" upsert --target "$TARGET/.cbmignore" --rules "$HERE/default.ignore"
$WATCH && warn "watcher is managed by the MCP process; no detached watcher is started by Powerpack"
cmd=("$BIN_PATH" cli index_repository --repo_path "$TARGET")
$FORCE && cmd+=(--force true)
if $DRY_RUN; then printf 'DRY-RUN:'; printf ' %q' "${cmd[@]}"; echo; exit 0; fi
CBM_CACHE_DIR="$CACHE_DIR" "${cmd[@]}" 2>&1 | tee "$STATE_DIR/logs/codebase-memory-index.log"
