#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
status=0

if command -v python3 >/dev/null 2>&1; then
  echo "[ok] python3: $(python3 --version 2>/dev/null)"
else
  echo "[warn] python3 not found"
  status=1
fi

if [ -f "$ROOT/dist/verify/validate_dist.py" ]; then
  if python3 "$ROOT/dist/verify/validate_dist.py"; then
    echo "[ok] dist validation passed"
  else
    echo "[warn] dist validation failed"
    status=1
  fi
else
  echo "[warn] dist validator missing"
  status=1
fi

if [ -d "$ROOT/sources/skills-pack/.agents/skills" ]; then
  echo "[ok] source skill base present"
else
  echo "[info] skills-pack source is not bundled (normal for release archives)"
fi

if [ -d "$ROOT/dist/skills/catalog" ] && [ -f "$ROOT/dist/skills/catalog/caveman/SKILL.md" ]; then
  echo "[ok] published skill catalog is installable"
else
  echo "[warn] published skill catalog missing"
  status=1
fi

if [ -f "$ROOT/dist/integrations/codebase-memory/adapter.json" ] && \
   [ -x "$ROOT/dist/integrations/codebase-memory/install.sh" ]; then
  echo "[ok] Codebase Memory MCP adapter present"
else
  echo "[warn] Codebase Memory MCP adapter incomplete"
  status=1
fi

if [ -x "$ROOT/dist/onboarding/adapt-project.sh" ] && \
   [ -f "$ROOT/dist/onboarding/schemas/adaptation-plan.schema.json" ]; then
  echo "[ok] project adaptation onboarding present"
else
  echo "[warn] project adaptation onboarding incomplete"
  status=1
fi

if command -v codex >/dev/null 2>&1; then
  echo "[ok] codex available for schema-bound AI analysis"
else
  echo "[info] codex exec unavailable; onboarding will use deterministic guided fallback"
fi

if command -v graphify >/dev/null 2>&1; then
  echo "[ok] optional graphify CLI available"
else
  echo "[info] optional graphify CLI absent; Graphify plans require dependency setup before apply"
fi

exit "$status"
