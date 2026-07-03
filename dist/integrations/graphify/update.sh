#!/usr/bin/env bash
set -euo pipefail

if ! command -v graphify >/dev/null 2>&1; then
  echo "[graphify-adapter] graphify CLI is not installed or not on PATH." >&2
  exit 1
fi

if [ ! -d "graphify-out" ]; then
  echo "[graphify-adapter] graphify-out/ does not exist in the current directory." >&2
  echo "[graphify-adapter] Run the adapter build step first." >&2
  exit 1
fi

echo "[graphify-adapter] Running incremental update..."
graphify update .
