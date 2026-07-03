#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; ROOT="$(cd "$HERE/../../.." && pwd)"; TARGET="."; DRY_RUN=false; BACKUP=false
while (($#)); do case "$1" in --target) TARGET="${2:?}"; shift 2;; --dry-run) DRY_RUN=true; shift;; --backup) BACKUP=true; shift;; *) echo "ERROR: unknown Graphify option: $1" >&2; exit 2;; esac; done
TARGET="$(cd "$TARGET" && pwd -P)"
command -v graphify >/dev/null 2>&1 || { echo "ERROR: graphify CLI is required; Powerpack does not bootstrap it unsafely" >&2; exit 1; }
$DRY_RUN && { echo "DRY-RUN: install managed Graphify Skill/rules at $TARGET (no hooks)"; exit 0; }
args=(install --root "$ROOT" --target "$TARGET"); $BACKUP && args+=(--backup)
python3 "$HERE/manage.py" "${args[@]}"
echo "OK: Graphify project adapter installed without hooks or watcher"
