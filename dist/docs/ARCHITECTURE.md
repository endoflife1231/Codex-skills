# Codex Powerpack Architecture

The assembled distribution is intentionally layered.

## Layer model

- `dist/core/`
  - shortest always-on Codex-native rules
  - progressive references for deeper policy
- `dist/agents/`
  - curated canonical agent layer
  - no raw Claude-format agent publishing
- `dist/skills/`
  - registry plus release-bundled installable Skill catalog
  - profile-driven activation model
- `dist/integrations/`
  - optional integrations: Graphify and project-scoped Codebase Memory MCP
- `dist/verify/` and `dist/install/`
  - product self-checks and local lifecycle tooling
- `dist/onboarding/`
  - deterministic project facts, optional schema-bound Codex analysis, explainable selection
  - immutable hashed plan separated from backup/apply/verify/rollback
- `release/`
  - package generation and release artifacts

## Source and licensing strategy

- The public package contains the installable source form used at runtime.
- First-party core, agents, onboarding, installers, and adapters are MIT licensed.
- Third-party skills remain separate license domains and retain local license files.
- Skills without a preserved license or notice are excluded from public packages.
- Graphify and Codebase Memory remain optional external projects; this repository ships first-party adapters, not relicensed upstream binaries.
- Provenance fields in registries are informational and may reference upstream source bundles that are not embedded in the public archive.

## Quality strategy

- one canonical role per agent job
- one clean default core
- host-specific and unsafe behavior remains opt-in
- upstream material is adapted, not dumped into the product unchanged
