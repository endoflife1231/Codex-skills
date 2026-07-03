#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"
TARGET=""; MODE=guided; PROFILE=auto; DRY_RUN=false; APPLY=false; CBM=auto; GRAPH=auto
CAVEMAN=yes; LIVE=yes; WITHOUT_INTEL=false; THRESHOLD=.7; NON_INTERACTIVE=false; FORCE_RESCAN=false; REUSE=false; VERBOSE=false; FORCE=false; CBM_BINARY=""
usage() { echo "Usage: $0 --target PATH [--mode guided|auto|manual|analyze-only] [--apply] [options]"; }
while (($#)); do case "$1" in
  --target) TARGET="${2:?}"; shift 2;; --mode) MODE="${2:?}"; shift 2;; --dry-run) DRY_RUN=true; shift;; --apply) APPLY=true; shift;;
  --profile) PROFILE="${2:?}"; shift 2;; --with-codebase-memory) CBM="${2:?}"; shift 2;; --with-graphify) GRAPH="${2:?}"; shift 2;;
  --with-caveman) CAVEMAN="${2:?}"; shift 2;; --with-live-language) LIVE="${2:?}"; shift 2;; --without-project-intelligence) WITHOUT_INTEL=true; shift;;
  --confidence-threshold) THRESHOLD="${2:?}"; shift 2;; --non-interactive) NON_INTERACTIVE=true; shift;; --force-rescan) FORCE_RESCAN=true; shift;; --reuse-analysis) REUSE=true; shift;;
  --verbose) VERBOSE=true; shift;; --force) FORCE=true; shift;; --codebase-memory-binary) CBM_BINARY="${2:?}"; shift 2;; --help|-h) usage; exit 0;; *) echo "ERROR: unknown option: $1" >&2; exit 2;; esac; done
[[ -n "$TARGET" ]] || { usage >&2; exit 2; }; [[ -d "$TARGET" ]] || { echo "ERROR: target is not a directory" >&2; exit 2; }
[[ "$MODE" =~ ^(guided|auto|manual|analyze-only)$ ]] || { echo "ERROR: invalid mode" >&2; exit 2; }
[[ "$PROFILE" =~ ^(auto|minimal|standard|full)$ ]] || { echo "ERROR: invalid profile" >&2; exit 2; }
[[ "$CBM" =~ ^(auto|yes|no)$ && "$GRAPH" =~ ^(auto|yes|no)$ ]] || { echo "ERROR: integration choices must be auto|yes|no" >&2; exit 2; }
[[ "$CAVEMAN" == yes && "$LIVE" == yes ]] || { echo "ERROR: Caveman and live-language are required" >&2; exit 2; }
$WITHOUT_INTEL && ! $FORCE && { echo "ERROR: --without-project-intelligence requires --force as explicit confirmation" >&2; exit 2; }
$VERBOSE && set -x
TARGET="$(cd "$TARGET" && pwd -P)"; ANALYSIS="$TARGET/.codex-powerpack/analysis"; GENERATED="$TARGET/.codex-powerpack/generated"; mkdir -p "$ANALYSIS" "$GENERATED"
FACTS="$ANALYSIS/project-facts.json"; AI="$ANALYSIS/project-analysis.json"; OLD_PLAN=""
if [[ -f "$GENERATED/adaptation-plan.json" ]]; then OLD_PLAN="$(mktemp)"; cp "$GENERATED/adaptation-plan.json" "$OLD_PLAN"; fi
if $FORCE_RESCAN || [[ ! -f "$FACTS" ]] || ! $REUSE; then python3 "$HERE/scan-project.py" --target "$TARGET" --output "$FACTS" >/dev/null; fi
python3 "$HERE/validate_json.py" --schema "$HERE/schemas/project-facts.schema.json" --document "$FACTS" >/dev/null
if ! $REUSE || [[ ! -f "$AI" ]]; then "$HERE/analyze-project.sh" --target "$TARGET" --facts "$FACTS" --output "$AI"; fi
select_args=(--root "$ROOT" --target "$TARGET" --facts "$FACTS" --analysis "$AI" --mode "$MODE" --profile "$PROFILE" --with-codebase-memory "$CBM" --with-graphify "$GRAPH" --confidence-threshold "$THRESHOLD" --output-dir "$GENERATED")
$WITHOUT_INTEL && select_args+=(--without-project-intelligence)
python3 "$HERE/select-components.py" "${select_args[@]}" >/dev/null
python3 "$HERE/validate_json.py" --schema "$HERE/schemas/adaptation-plan.schema.json" --document "$GENERATED/adaptation-plan.json" >/dev/null
python3 "$HERE/generate-project-rules.py" --plan "$GENERATED/adaptation-plan.json" --output-dir "$GENERATED" >/dev/null
if [[ -n "$OLD_PLAN" ]]; then python3 "$HERE/compare_plans.py" --old "$OLD_PLAN" --new "$GENERATED/adaptation-plan.json" --output "$GENERATED/adaptation-diff.json"; rm -f "$OLD_PLAN"; fi
echo "Plan: $GENERATED/adaptation-plan.md"
if [[ "$MODE" == analyze-only ]] || { [[ "$MODE" == guided || "$MODE" == manual ]] && ! $APPLY; }; then echo "No project configuration was applied."; exit 0; fi
confidence_ok="$(python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); print("yes" if p["confidence"]>=float(sys.argv[2]) and not p["skills"]["manual_review"] else "no")' "$GENERATED/adaptation-plan.json" "$THRESHOLD")"
if [[ "$confidence_ok" != yes && "$FORCE" != true ]]; then echo "ERROR: plan needs manual review; rerun guided or pass --force after review" >&2; exit 1; fi
if [[ "$MODE" == guided && "$NON_INTERACTIVE" != true ]]; then read -r -p "Apply this reviewed plan? [y/N] " answer; [[ "$answer" =~ ^[Yy]$ ]] || { echo "Cancelled."; exit 0; }; fi
apply_args=(--target "$TARGET" --plan "$GENERATED/adaptation-plan.json" --yes)
$DRY_RUN && apply_args+=(--dry-run); $FORCE && apply_args+=(--force); [[ -n "$CBM_BINARY" ]] && apply_args+=(--codebase-memory-binary "$CBM_BINARY")
"$HERE/apply-plan.sh" "${apply_args[@]}"
