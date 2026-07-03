# Implementation Plan

Generated: 2026-06-28

Status: planning only. No build, migration, or source mutation has started yet.

## Planning Assumptions

- `sources/skills-pack` is the base of the final distribution.
- `caveman` is treated as an embedded capability already present inside `skills-pack`, not as a blocking missing source.
- `project-rules` may be created as a first-party Codex-native source if it improves product quality and packaging clarity.
- `subagents` will not be copied raw. They will be selectively migrated into real Codex agents and routed through Codex-compatible instructions.
- `unverified` provenance is acceptable unless it directly affects licensing, reproducibility, or runtime safety.

## Target Structure

```text
build/
├── source-manifest.json
└── reports/
    ├── source-inventory.md
    └── implementation-plan.md

dist/
├── core/
│   ├── AGENTS.base.md
│   └── references/
├── agents/
│   ├── registry.json
│   └── codex/
├── skills/
│   ├── registry.json
│   └── bundles/
├── integrations/
│   └── graphify/
├── profiles/
├── install/
├── verify/
├── docs/
├── manifests/
└── licenses/

release/
└── codex-powerpack-<version>.zip
```

## Source Mapping

### `sources/skills-pack`

- Role: primary base.
- Keep:
  - existing `.agents/skills`
  - existing `.codex/agents`
  - validation/indexing/notices patterns
  - Caveman integration already present
- Adapt:
  - narrow or refactor broad AGENTS fragments into `dist/core`
  - filter unsafe examples from default-facing docs
  - split product output into reusable registries and profiles
- Exclude from core:
  - any skill that is platform-locked, redundant, legacy, or unsafe-by-default

### `sources/subagents`

- Role: migration source for Codex-native subagents.
- Keep as source material only.
- Migrate selectively:
  - map chosen Claude markdown agents into Codex TOML agents
  - rewrite tool assumptions, triggers, and write permissions for Codex
  - collapse overlaps into one working implementation per role
- Exclude:
  - raw Claude frontmatter files
  - plugin marketplace flows
  - installer scripts and direct plugin instructions

### `sources/claude-overlay`

- Role: reference source only.
- Keep:
  - migration heuristics
  - safety language
  - decomposition patterns
- Exclude:
  - raw always-on prompt text
  - Claude-specific tool or model claims
  - destructive shell examples in user-facing core docs

### `sources/graphify`

- Role: optional integration.
- Keep:
  - verified package metadata
  - install/update/run concepts
  - Codex-specific skill guidance as reference material
- Adapt:
  - convert to a local wrapper under `dist/integrations/graphify`
  - add runtime checks before any command is suggested
  - make hooks opt-in only
- Exclude:
  - `curl | sh`
  - unverified host-specific assumptions
  - anything that would make Graphify mandatory for the core pack

### `sources/project-rules`

- Role: first-party source to create if needed.
- Proposed use:
  - hold Codex-native project rules and migration-safe reference material
  - provide a clean home for content that should not live inside imported upstream folders

### Embedded `caveman`

- Role: existing capability already present in `skills-pack`.
- Plan:
  - keep as a distinct family of skills and policies in the final distribution
  - expose explicit enable/disable policy through profiles and docs

## Selected Agents

The final distribution should ship a small Codex-native agent set with clear scope and non-overlapping roles.

Selected base agents:

- `explorer`
- `planner`
- `implementer`
- `debugger`
- `reviewer`
- `tester`
- `security-reviewer`
- `architect`

Additional optional agents to keep if they integrate cleanly:

- `performance-auditor`
- `design-asset-producer`
- `manual-edit-applier`

Source strategy:

- Reuse the strongest existing Codex-native agents from `skills-pack` where they already match the role.
- Fill missing roles from `subagents` through migration.
- Resolve collisions by choosing one canonical Codex name and mapping any imported role text into that implementation.

Canonical collision policy:

- Keep Codex naming with hyphenated public IDs where possible for new distributed agents.
- Preserve existing working `skills-pack` behavior internally if needed, but expose only one public agent per role.
- `code_reviewer` and `code-reviewer` become one canonical `reviewer` or `code-reviewer` path in the final dist.
- `security_auditor` and `security-auditor` become one canonical `security-reviewer` path in the final dist.

## Excluded Agents

Exclude from the default distribution:

- bulk language-specialist agents from `subagents`
- business/product/research agents that are not clearly tied to Codex development workflows
- any imported agent that requires Claude-only tools, plugin marketplace behavior, or ambiguous write access
- duplicate reviewers, testers, and security agents that do not materially improve the final pack

These can remain as future expansion material, but not in the first clean release.

## Selected Skills

Default skill strategy:

- inherit the current `skills-pack` as the base skill corpus
- keep Caveman family as first-class but configurable
- add one Graphify wrapper skill later
- keep migrated subagent behavior in agents, not as duplicated skills unless a workflow truly belongs in the skill layer

Selection policy:

- keep high-value general engineering skills already present in `skills-pack`
- keep validated design/development/review/test workflows
- prefer one canonical skill per workflow category
- demote legacy, host-specific, or redundant material into references instead of active registered skills

Planned skill buckets:

- Core engineering
- Review, testing, and security
- Design and frontend
- Delivery and deployment
- Caveman
- Optional integrations
- References-only migrated material

## Conflict Resolution

### Agent collisions

- Resolve by one canonical Codex-native agent per role.
- Migrate the best content, not both artifacts.

### Skill duplication

- If two skills solve the same problem, keep the higher-quality Codex-native one.
- Move secondary guidance into references or merge it into the surviving skill.

### Claude-derived instruction conflicts

- Never copy raw Claude tool lists or command triggers into Codex core.
- Keep useful reasoning patterns, remove host-specific claims.

### Unsafe examples

- Filter dangerous commands out of default docs and always-on instructions.
- Keep them only as guarded reference content when they are educational and clearly marked.

## AGENTS.md Strategy

The final product should not rely on one giant root instruction file.

Plan:

- `dist/core/AGENTS.base.md`
  - short, Codex-native, always-on policy
  - research before edit
  - minimal diff
  - verify against real code
  - run relevant tests
  - mark unverified claims explicitly when still relevant
  - controlled write permissions
  - safe external actions
- `dist/core/references/`
  - longer optional guidance
  - migration notes
  - safety references
  - platform integration notes
- `dist/agents/` and `dist/skills/`
  - hold specialized instructions instead of bloating root AGENTS

Result:

- short root guidance
- deep instructions only when the chosen skill or agent requires them

## Caveman Policy

Keep Caveman as a separate capability family.

Policy:

- main agent default: Lite behavior only when the user asks for compactness or a profile enables it
- final answer compression: configurable, never forced globally
- `tester`, `reviewer`, `debugger`, `security-reviewer`: preserve technical detail and findings; no aggressive compression
- commands, files, line refs, risks, and failures must survive compression
- hooks stay opt-in and never auto-enabled

## Graphify Adapter

Planned output:

```text
dist/integrations/graphify/
├── install.sh
├── run.sh
├── update.sh
├── doctor.sh
├── uninstall.sh
├── adapter.json
└── default.graphifyignore
```

Adapter policy:

- optional only
- core distribution works without Graphify
- every script performs preflight checks
- no `curl | sh`
- no auto-hook execution
- no guessed commands beyond what local source confirms
- Codespaces-safe rebuild path included

Planned validation points:

- Python availability
- package entrypoint availability
- writable output directory
- optional extras declared but not silently installed
- hook installation requires explicit user trust

## Codespaces

Codespaces support should be first-class but minimal.

Plan:

- avoid machine-global assumptions
- keep install flows repo-local where possible
- add doctor checks for common Codespaces gaps:
  - missing Python tools
  - missing Node for selected skills
  - missing browser/runtime dependencies
  - missing executable bits on helper scripts
- ensure Graphify and optional hooks degrade gracefully in ephemeral environments

## Licenses

License plan:

- preserve upstream notices for each reused source
- keep `skills-pack` as mixed-license content with per-skill notices
- keep `claude-overlay`, `subagents`, and `graphify` notices separate
- add a final consolidated notices manifest in `dist/licenses/` and `dist/manifests/`
- do not treat the final dist as a single-license artifact unless every included component supports that claim

Quality threshold:

- only include source-derived content that has a known local license file or an already-documented license in the current pack
- where provenance is imperfect but the license is locally present, proceed and document it

## Test Matrix

### Structure validation

- directory layout matches the target structure
- registries exist and parse
- no source files under `sources/` changed

### Agent validation

- all distributed agents parse in Codex-native format
- read-only agents have no write tools
- migrated agent names are collision-free

### Skill validation

- every registered skill resolves to a real directory
- every skill has license metadata and source mapping
- duplicate workflow skills are either merged or excluded

### Safety validation

- no default docs include `curl | sh`
- no auto-enabled hooks
- no raw Claude-only tool instructions in core policy

### Integration validation

- Graphify wrapper works when installed
- Graphify absence does not break the pack
- Caveman flags behave as documented

### Packaging validation

- manifests and notices are present
- profile files load
- release zip is reproducible enough for local rebuild checks

## Execution Order

1. Author `project-rules` source if the core/reference split needs a clean first-party home.
2. Build `dist/core` from `skills-pack` plus filtered first-party rules.
3. Curate and migrate the small Codex-native agent set from `skills-pack` and `subagents`.
4. Normalize collisions and publish one canonical registry.
5. Add Graphify adapter and wrapper skill as optional integration.
6. Generate profiles, manifests, notices, and verification tooling.
7. Produce the release artifact only after validation passes.

## Decision Summary

- `unverified` provenance is not a blocker unless it harms license clarity, reproducibility, or runtime safety.
- `skills-pack` is the foundation.
- `caveman` stays, but as embedded capability.
- `project-rules` can and likely should be authored as first-party support material.
- `subagents` are worth using, but only after Codex migration and deduplication.
- Claude-derived and unsafe material will be filtered instead of copied verbatim.
