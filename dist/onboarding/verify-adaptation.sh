#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"
TARGET=""; PLAN=""
while (($#)); do case "$1" in --target) TARGET="${2:?}"; shift 2;; --plan) PLAN="${2:?}"; shift 2;; *) echo "ERROR: unknown verify option: $1" >&2; exit 2;; esac; done
[[ -n "$TARGET" ]] || { echo "ERROR: --target required" >&2; exit 2; }; TARGET="$(cd "$TARGET" && pwd -P)"; PLAN="${PLAN:-$TARGET/.codex-powerpack/generated/adaptation-plan.json}"
python3 "$HERE/verify_adaptation.py" --root "$ROOT" --target "$TARGET" --plan "$PLAN"
python3 "$HERE/validate_json.py" --schema "$HERE/schemas/adaptation-state.schema.json" --document "$TARGET/.codex-powerpack/state/adaptation-state.json" >/dev/null
if python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); raise SystemExit(0 if p["integrations"]["codebase-memory"]["decision"]=="enable" else 1)' "$PLAN"; then "$ROOT/dist/integrations/codebase-memory/verify.sh" --target "$TARGET"; fi
if python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); raise SystemExit(0 if p["integrations"]["graphify"]["decision"]=="enable" else 1)' "$PLAN"; then "$ROOT/dist/integrations/graphify/doctor.sh" "$TARGET"; fi
