#!/usr/bin/env bash
set -euo pipefail

if ! command -v graphify >/dev/null 2>&1; then
  echo "[graphify-adapter] graphify CLI is not installed or not on PATH." >&2
  exit 1
fi

if [ "$#" -lt 1 ]; then
  echo "Usage: ./run.sh <path-or-url> [graphify args...]" >&2
  exit 1
fi

TARGET="$1"
shift || true

echo "[graphify-adapter] Building or refreshing graph for: $TARGET"
graphify "$TARGET" "$@"
