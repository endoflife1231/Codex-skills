#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/common.sh"

TARGET=""; SCOPE=project; BINARY=""; BACKUP=false; DRY_RUN=false; UI=false
while (($#)); do
  case "$1" in
    --target) TARGET="${2:?}"; shift 2;;
    --scope) SCOPE="${2:?}"; shift 2;;
    --binary) BINARY="${2:?}"; shift 2;;
    --backup) BACKUP=true; shift;;
    --dry-run) DRY_RUN=true; shift;;
    --ui) UI=true; shift;;
    *) die "unknown configure option: $1";;
  esac
done
[[ -n "$TARGET" ]] || die "--target is required"
[[ "$SCOPE" == project || "$SCOPE" == user ]] || die "--scope must be project or user"
resolve_layout "$TARGET" "$SCOPE"
BINARY="${BINARY:-$BIN_PATH}"
args=(upsert --config "$CONFIG_PATH" --binary "$BINARY" --cache "$CACHE_DIR")
$UI && args+=(--ui)
$BACKUP && args+=(--backup)
$DRY_RUN && args+=(--dry-run)
python3 "$HERE/config_tool.py" "${args[@]}"

agent_args=(upsert --file "$AGENTS_PATH" --fragment "$HERE/AGENTS.fragment.md")
$BACKUP && agent_args+=(--backup)
$DRY_RUN && agent_args+=(--dry-run)
python3 "$HERE/managed_text.py" "${agent_args[@]}"

ignore_args=(upsert --target "$TARGET/.cbmignore" --rules "$HERE/default.ignore")
$DRY_RUN && ignore_args+=(--dry-run)
python3 "$HERE/ignore_tool.py" "${ignore_args[@]}"
