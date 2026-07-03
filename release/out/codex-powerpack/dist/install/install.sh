#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET=""; PROFILE=standard; DRY_RUN=false; BACKUP=false; FORCE=false
CBM_CHOICE=profile; CBM_SCOPE=project; CBM_AUTO=auto; CBM_UI=false; CBM_BINARY=""
VERBOSE=false
usage() { echo "Usage: $0 --target PATH [--profile minimal|standard|full] [--with-codebase-memory|--without-codebase-memory] [options]"; }
while (($#)); do case "$1" in
  --target) TARGET="${2:?}"; shift 2;; --profile) PROFILE="${2:?}"; shift 2;;
  --with-codebase-memory) CBM_CHOICE=on; shift;; --without-codebase-memory) CBM_CHOICE=off; shift;;
  --codebase-memory-mode) CBM_SCOPE="${2:?}"; shift 2;; --codebase-memory-auto-index) CBM_AUTO="${2:?}"; shift 2;;
  --codebase-memory-ui) CBM_UI=true; shift;; --codebase-memory-binary) CBM_BINARY="${2:?}"; shift 2;;
  --codebase-memory-clear-cache) shift;; --dry-run) DRY_RUN=true; shift;; --backup) BACKUP=true; shift;;
  --force) FORCE=true; shift;; --non-interactive) shift;; --verbose) VERBOSE=true; shift;;
  --help|-h) usage; exit 0;; *) echo "ERROR: unknown option: $1" >&2; exit 2;; esac; done
[[ -n "$TARGET" ]] || { usage >&2; exit 2; }
[[ "$PROFILE" == minimal || "$PROFILE" == standard || "$PROFILE" == full ]] || { echo "ERROR: invalid profile" >&2; exit 2; }
$VERBOSE && set -x
python3 "$ROOT/dist/verify/validate_dist.py"
args=(install --root "$ROOT" --target "$TARGET" --profile "$PROFILE")
$DRY_RUN && args+=(--dry-run); $BACKUP && args+=(--backup); $FORCE && args+=(--force)
python3 "$ROOT/dist/install/project_files.py" "${args[@]}"

enable_cbm=false
[[ "$CBM_CHOICE" == on ]] && enable_cbm=true
[[ "$CBM_CHOICE" == profile && "$PROFILE" != minimal ]] && enable_cbm=true
if $enable_cbm; then
  cbm=(--target "$TARGET" --scope "$CBM_SCOPE" --auto-index "$CBM_AUTO")
  $CBM_UI && cbm+=(--ui); $DRY_RUN && cbm+=(--dry-run); $BACKUP && cbm+=(--backup); $FORCE && cbm+=(--force)
  [[ -n "$CBM_BINARY" ]] && cbm+=(--binary "$CBM_BINARY")
  "$ROOT/dist/integrations/codebase-memory/install.sh" "${cbm[@]}"
fi
echo "OK: Codex Powerpack profile '$PROFILE' installed into $TARGET"
