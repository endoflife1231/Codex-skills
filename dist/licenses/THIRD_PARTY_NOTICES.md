# Third-Party Notices

This assembled Codex Powerpack distribution is built from a mix of imported upstream material and first-party Codex-native adaptation.

This notice file is a distribution-level guide, not a replacement for per-source or per-skill notices that already exist inside imported source trees.

## Sources included in the assembled distribution

### `sources/skills-pack`

- Role: primary base for the skill layer and existing Codex-native patterns
- License status: mixed, per-skill
- Notes:
  - individual skill directories retain local license files where available
  - redistribution must follow the per-skill notices already preserved in the source pack
  - this distribution publishes a registry over the pack rather than flattening all skills into one new single-license layer

### `sources/claude-overlay`

- Role: reference-only migration and policy source
- Upstream: `Piebald-AI/claude-code-system-prompts`
- License: MIT
- Local license file: `sources/claude-overlay/LICENSE`
- Notes:
  - only adapted policy fragments and references are used
  - raw Claude-specific system prompt behavior is not shipped as a direct always-on layer

### `sources/subagents`

- Role: role-source material for Codex-native agent migration
- Upstream: `VoltAgent/awesome-claude-code-subagents`
- License: MIT
- Local license file: `sources/subagents/LICENSE`
- Notes:
  - subagents are not redistributed as raw Claude-format agents in the dist layer
  - only adapted role concepts and curated behavior are used

### `sources/graphify`

- Role: optional Graphify adapter and integration input
- Upstream: `safishamsi/graphify`
- License: MIT
- Local license file: `sources/graphify/LICENSE`
- Notes:
  - Graphify remains optional
  - the distribution ships an adapter layer, not Graphify binaries or package installers

### `sources/project-rules`

- Role: first-party Codex-native rules source
- License: first-party

### `sources/codebase-memory-mcp-main`

- Role: optional project-scoped code intelligence MCP integration
- Upstream: `DeusData/codebase-memory-mcp`
- Declared version: `0.8.1`
- Commit: unverified local snapshot (the supplied tree has no `.git` metadata)
- License: MIT
- Preserved license: `dist/licenses/source-licenses/codebase-memory-mcp-LICENSE`
- Included files: Powerpack adapter, generated Skill wrapper, AGENTS fragment,
  configuration template, ignore rules, and lifecycle scripts
- Upstream source modifications: none
- Binary: obtained separately from a pinned upstream release or supplied locally;
  it is not committed into this distribution
- Checksums: installation requires a match against the separately downloaded
  upstream `checksums.txt`; policy lives in the integration's `checksums.json`
- Vendored dependencies and model data retain upstream notices in
  `sources/codebase-memory-mcp-main/THIRD_PARTY.md`

## Distribution policy

- Imported material is adapted selectively rather than copied wholesale.
- Host-specific, unsafe, or optional behavior is kept out of the default core whenever possible.
- The final distribution should not be interpreted as a single-license monolith.
- Optional integrations are published as adapters or references unless they are safe and product-appropriate as defaults.

## Current adaptation depth

- `claude-overlay` has been adapted into published core references rather than shipped as raw system-prompt overlays.
- `subagents` have been adapted into canonical Codex-native agent roles plus agent-reference material.
- `skills-pack` remains the primary published skill base, classified through local registries and profiles.

## Practical redistribution guidance

- Review per-source and per-skill notices before republishing outside your own workspace.
- Treat `dist/` as an assembled distribution with mixed provenance rather than as wholly first-party authored content.
- If you publish a derivative build, keep this notice file together with the source-specific notices it refers to.
