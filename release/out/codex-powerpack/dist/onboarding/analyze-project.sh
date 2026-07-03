#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
TARGET=""; FACTS=""; OUTPUT=""; FORCE_FALLBACK=false
while (($#)); do case "$1" in
  --target) TARGET="${2:?}"; shift 2;; --facts) FACTS="${2:?}"; shift 2;; --output) OUTPUT="${2:?}"; shift 2;;
  --deterministic) FORCE_FALLBACK=true; shift;; *) echo "ERROR: unknown analysis option: $1" >&2; exit 2;; esac; done
[[ -n "$TARGET" ]] || { echo "ERROR: --target required" >&2; exit 2; }
TARGET="$(cd "$TARGET" && pwd -P)"; FACTS="${FACTS:-$TARGET/.codex-powerpack/analysis/project-facts.json}"; OUTPUT="${OUTPUT:-$TARGET/.codex-powerpack/analysis/project-analysis.json}"
[[ -f "$FACTS" ]] || { echo "ERROR: facts missing: $FACTS" >&2; exit 1; }
mkdir -p "$(dirname "$OUTPUT")"
if command -v codex >/dev/null 2>&1 && ! $FORCE_FALLBACK; then
  request="$TARGET/.codex-powerpack/analysis/codex-analysis-request.md"
  {
    cat "$HERE/prompts/analyze-project.md"
    printf '\nInputs are local files; read only these bounded artifacts:\n- %s\n- %s\n- %s\n- %s\n- %s\n' "$FACTS" "$ROOT/dist/skills/registry.json" "$ROOT/dist/agents/registry.json" "$ROOT/dist/integrations/registry.json" "$HERE/rules/always-on.yaml"
  } > "$request"
  if ! codex exec --sandbox read-only -C "$TARGET" --output-schema "$HERE/schemas/project-analysis.schema.json" -o "$OUTPUT" "$(cat "$request")" || \
     ! python3 "$HERE/validate_json.py" --schema "$HERE/schemas/project-analysis.schema.json" --document "$OUTPUT" >/dev/null; then
    echo "WARNING: codex schema analysis failed; using deterministic fallback" >&2
    python3 "$HERE/analyze_project.py" --facts "$FACTS" --output "$OUTPUT"
  fi
else
  echo "WARNING: codex exec unavailable; using deterministic fallback" >&2
  python3 "$HERE/analyze_project.py" --facts "$FACTS" --output "$OUTPUT"
fi
python3 "$HERE/validate_json.py" --schema "$HERE/schemas/project-analysis.schema.json" --document "$OUTPUT" >/dev/null
