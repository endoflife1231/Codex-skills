#!/usr/bin/env bash
set -euo pipefail

status=0
TARGET="${1:-.}"
TARGET="$(cd "$TARGET" && pwd -P)"

if command -v python3 >/dev/null 2>&1; then
  echo "[ok] python3: $(python3 --version 2>/dev/null)"
else
  echo "[warn] python3 not found"
  status=1
fi

if command -v graphify >/dev/null 2>&1; then
  echo "[ok] graphify: $(graphify --version 2>/dev/null || echo 'present')"
else
  echo "[warn] graphify CLI not found on PATH"
  status=1
fi

if [ -f "$TARGET/.codex-powerpack/state/graphify.json" ]; then
  echo "[ok] managed Graphify state present"
else
  echo "[warn] managed Graphify state missing"
  status=1
fi

if [ -f "$TARGET/graphify-out/graph.json" ]; then
  echo "[ok] graphify-out/graph.json present"
else
  echo "[info] graphify-out/graph.json not present yet"
fi

if [ -f "$TARGET/graphify-out/.graphify_python" ]; then
  echo "[ok] graphify-out/.graphify_python present"
else
  echo "[info] graphify-out/.graphify_python not present yet"
fi

if [ -f "$TARGET/.codex/hooks.json" ]; then
  if grep -q graphify "$TARGET/.codex/hooks.json"; then
    echo "[warn] Graphify hook detected; Powerpack does not require or manage it"
  else
    echo "[info] unrelated Codex hooks file exists"
  fi
fi

exit "$status"
