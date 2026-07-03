# Project adaptation onboarding audit

Date: 2026-07-03

## Current distribution

- Distribution root confirmed by all six required registry/core/profile files.
- Skills before onboarding integration wrappers: 253 unique entries; every entry had a release-bundled install source.
- Final published registry after adding the safe Graphify wrapper: 254 Skills.
- Agents: 8 canonical Codex TOML definitions.
- Caveman: all 8 family Skills present; the required 4 are in every profile.
- Live language: all 12 preferred RU/EN/editorial Skills are present.
- Codebase Memory: complete project-scoped adapter, verified release path and lifecycle tests.
- Graphify: adapter exists, but the external `graphify` CLI is not bundled and must be
  treated as a checked dependency rather than silently installed.
- Current profile installer is real and stateful, but it installs static profiles; it
  needs an exact-selection input for onboarding plans.

## Runtime capabilities

- Python 3.12 is available.
- `codex exec` is not available in this workspace. AI analysis must therefore use a
  visible deterministic fallback and mark its analysis method/confidence honestly.
- JSON Schema files can be validated structurally with Python; optional `jsonschema`
  may be used when present but cannot be a hard runtime dependency.

## Risks to control

- Project documentation is untrusted input and must never become executable commands.
- Scanner must collect metadata without opening secret files or traversing dependencies.
- Guided planning must not call installers or mutate user configuration.
- Apply must consume a hashed plan, recheck the project fingerprint, preflight external
  tools, snapshot affected user paths, and make no new selection decisions.
- Graphify recommendations must not create a false successful install when its CLI is
  absent.
- Existing Skills, agents, AGENTS blocks and MCP sections must be preserved or backed up.
- Architect and tester currently have write-capable TOML sandboxes; selection must expose
  this instead of describing them as read-only.

## Design decision

Implement four explicit artifacts and phases:

1. `project-facts.json`: deterministic scanner output.
2. `project-analysis.json`: schema-bound Codex output when available, otherwise marked
   deterministic fallback.
3. `adaptation-plan.json` plus SHA-256: the only input accepted by apply.
4. `adaptation-state.json`: managed paths, backups, plan hash, verification and rollback.

Analyze-only and guided-without-apply may write only under `.codex-powerpack/analysis`
and `.codex-powerpack/generated`; they do not modify project instructions, Codex config,
Skills, agents, hooks, source files or dependencies.
