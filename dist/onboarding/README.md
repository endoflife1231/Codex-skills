# Project adaptation onboarding

Onboarding turns a project scan into an explainable, reviewable and reversible
Powerpack installation. Decisions and mutations are deliberately separate.

```text
scan facts → schema-bound analysis → component selection → hashed plan
                                                    ↓ explicit approval
                                    backup → apply → verify → state/rollback
```

## Modes

- `guided` (default): scan and create a plan; apply only with `--apply` and user
  confirmation. `--non-interactive --apply` is itself the explicit approval.
- `auto`: applies only when confidence meets the threshold and no manual-review
  finding exists. Hooks, watchers, deploys, migrations and implicit network downloads
  remain disabled; supply a verified Codebase Memory binary when needed.
- `manual`: creates a reviewable plan using explicit profile/integration choices;
  it does not apply without `--apply`.
- `analyze-only`: writes facts, analysis and generated plans under
  `.codex-powerpack/` but does not modify project configuration.

When `codex exec` supports schema output, it may produce `project-analysis.json`.
If unavailable or invalid, onboarding uses a clearly marked deterministic fallback.
It never parses free-form model prose as configuration.

## Always-on policy

Caveman and the curated RU/EN live-language group are installed in every plan.
Caveman controls concise final presentation without hiding errors or evidence;
live-language affects prose but never code or machine formats.

At least one intelligence layer is required. Codebase Memory is selected for code,
symbols, calls, diffs and impact. Graphify is selected for documentation/media and
visual semantic maps. Mixed projects can use both. An explicit
`--without-project-intelligence --force` waiver is recorded in the plan.

## Generated and state files

- `.codex-powerpack/analysis/`: deterministic facts and bounded analysis
- `.codex-powerpack/generated/`: selections, plan, SHA-256 and generated rules
- `.codex-powerpack/state/adaptation-state.json`: applied state
- `.codex-powerpack/backups/adaptation-*`: pre-apply snapshots

## Commands

```bash
# Plan only
bash dist/onboarding/adapt-project.sh --target /path/project --mode guided

# Review adaptation-plan.md, then apply
bash dist/onboarding/adapt-project.sh --target /path/project --mode guided --apply

# Repeat analysis after the project changes
bash dist/onboarding/adapt-project.sh --target /path/project --mode guided --force-rescan

# Restore the exact pre-apply snapshot
bash dist/onboarding/rollback.sh --target /path/project
```

Graphify remains an external optional dependency. If selected and its CLI is absent,
apply stops before backup or project mutation. Codebase Memory uses the managed,
checksum-verified project-scoped integration.
