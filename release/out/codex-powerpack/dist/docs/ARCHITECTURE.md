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

## Source strategy

- `skills-pack` is the primary product base
- `subagents` provide role ideas, not final agent files
- `claude-overlay` provides migration-safe patterns and references
- `graphify` is optional and adapter-based
- `codebase-memory-mcp` remains unchanged under `sources/`; the published adapter
  owns binary verification, project config, isolated cache, state, and removal
- `project-rules` holds first-party Codex-native policy

## Quality strategy

- one canonical role per agent job
- one clean default core
- host-specific and unsafe behavior remains opt-in
- upstream material is adapted, not dumped into the product unchanged
