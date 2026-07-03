# Source Inventory

Generated: 2026-06-28

Scope: inventory only. No files under `sources/` were modified, no hooks were executed, and no build/integration work was started.

Update note (2026-07-03):

- `sources/skills-pack` has since been refreshed to the newer `2026-07-03.1` pack expansion.
- Current source-pack state is now 252 skills and 33 Codex custom agents.
- The 152/9 counts below remain part of the original phase-1 inventory snapshot.

## Executive Summary

- Present sources: `claude-overlay`, `graphify`, `skills-pack`, `subagents`.
- Missing expected sources from the master prompt: `sources/caveman`, `sources/project-rules`.
- `caveman` is already represented inside `sources/skills-pack` as integrated Codex skills; this is usable, but standalone provenance is currently absent.
- Planning assumption for the next phases: treat `caveman` as embedded in `skills-pack`, and allow `project-rules` to be authored as a first-party Codex-native source if needed.
- Nested source directories do not contain local `.git` directories, so commit/tag and origin can only be confirmed where a local manifest or package metadata explicitly states them.
- Current base pack status:
  - `skills-pack`: 152 skills, 9 Codex custom agents.
  - `subagents`: 154 Claude-style subagents across 10 categories.
- No exact duplicate skill names were found across the scanned source layouts.
- Two normalized agent-name collisions were found:
  - `code_reviewer` vs `code-reviewer`
  - `security_auditor` vs `security-auditor`

## Structure Snapshot

Expected by `codex_powerpack_docs/prompts/MASTER_PROMPT_FOR_CODEX.md`:

```text
sources/
├── claude-overlay/
├── subagents/
├── skills-pack/
├── caveman/
├── graphify/
└── project-rules/
```

Actual during phase 1:

```text
sources/
├── claude-overlay/
├── graphify/
├── skills-pack/
├── subagents/
└── source-manifest.json
```

Missing during phase 1: `sources/caveman`, `sources/project-rules`.

Current workspace note:

- `sources/project-rules` has since been created as a first-party Codex-native source for later phases.

## Source Details

### 1. `sources/claude-overlay`

- Purpose: Claude-oriented overlay of system prompts, tool descriptions, migration guides, and reference materials.
- Local verification:
  - Files: 530
  - Local VCS metadata: absent
  - License: MIT via [LICENSE](/workspaces/Codex-skills/sources/claude-overlay/LICENSE)
  - Likely upstream: `Piebald-AI/claude-code-system-prompts`, inferred from links embedded in [CHANGELOG.md](/workspaces/Codex-skills/sources/claude-overlay/CHANGELOG.md)
- Formats:
  - Mostly `*.md`
  - One JS utility: [updatePrompts.js](/workspaces/Codex-skills/sources/claude-overlay/tools/updatePrompts.js)
- Executables: none detected.
- Hooks: none detected.
- Dependencies: none declared locally.
- Risks:
  - Very large prompt corpus. Examples:
    - [CHANGELOG.md](/workspaces/Codex-skills/sources/claude-overlay/CHANGELOG.md)
    - [skill-model-migration-guide.md](/workspaces/Codex-skills/sources/claude-overlay/system-prompts/skill-model-migration-guide.md)
  - Claude-specific tool vocabulary and model assumptions would conflict with a clean Codex core if imported directly.
  - Prompt text contains destructive-command examples such as `rm -rf` and `git reset --hard`; safe as documentation, unsafe if copied without filtering.
- Possible use:
  - Reference-only source for migration wording, safety framing, and decomposition patterns.
  - Not suitable as direct always-on policy in current form.
- Redistribution:
  - MIT appears permissive, but notices must be preserved.

### 2. `sources/subagents`

- Purpose: large catalog of Claude Code subagent definitions.
- Local verification:
  - Files: 189
  - Local VCS metadata: absent
  - License: MIT via [LICENSE](/workspaces/Codex-skills/sources/subagents/LICENSE)
  - Upstream URL appears in [README.md](/workspaces/Codex-skills/sources/subagents/README.md): `https://github.com/VoltAgent/awesome-claude-code-subagents`
- Formats:
  - Markdown agent definitions under `categories/*/*.md`
  - Plugin metadata under `.claude-plugin/`
  - One installer shell script: [install-agents.sh](/workspaces/Codex-skills/sources/subagents/install-agents.sh)
- Executables:
  - No executable bit detected in this checkout, but [install-agents.sh](/workspaces/Codex-skills/sources/subagents/install-agents.sh) is clearly an installer flow.
- Hooks: none detected.
- Dependencies: none declared locally.
- Counts:
  - 154 subagents total
  - 10 categories
- Risks:
  - Source format is Claude frontmatter, not Codex TOML agent format. See [CLAUDE.md](/workspaces/Codex-skills/sources/subagents/CLAUDE.md).
  - Many agent templates assume Claude tool names and permission semantics.
  - The catalog is too broad for blind inclusion; there is heavy topical overlap with existing `skills-pack` skills and agents.
  - README includes plugin and `curl`-based installation guidance that should not be transplanted into a Codex-first pack.
- Possible use:
  - Selective adaptation of a small curated Codex-native agent set.
  - Source text for role descriptions, completion criteria, and category taxonomy.
- Redistribution:
  - MIT appears permissive, but notices must be preserved.

### 3. `sources/skills-pack`

- Purpose: current integrated Codex skills pack and agent bundle. This is the strongest candidate for the final distribution base.
- Local verification:
  - Files: 1947
  - Local VCS metadata: absent
  - Root license file: not present
  - Version string from local docs: `2026-06-28.1`
  - README: [README.md](/workspaces/Codex-skills/sources/skills-pack/README.md)
- Formats:
  - Skills and references: markdown
  - Agent configs: TOML and YAML
  - Helper scripts: Python, JS/CJS/MJS
  - Assets: SVG, PNG
- Counts:
  - 152 skills under `.agents/skills/`
  - 9 Codex custom agents under `.codex/agents/`
- Executables detected:
  - [fetch_images.py](/workspaces/Codex-skills/sources/skills-pack/.agents/skills/huashu-design/scripts/fetch_images.py)
  - [verify.py](/workspaces/Codex-skills/sources/skills-pack/.agents/skills/huashu-design/scripts/verify.py)
- Hooks:
  - [caveman_hook.py](/workspaces/Codex-skills/sources/skills-pack/.agents/skills/caveman-setup/scripts/caveman_hook.py)
  - Hook-install guidance also exists in the Caveman setup skill.
- Dependencies surfaced from local files:
  - [huashu-design/package.json](/workspaces/Codex-skills/sources/skills-pack/.agents/skills/huashu-design/package.json)
  - `requirements.txt` files inside `ckm-ui-styling` and `ui-styling`
- Risks:
  - Licensing is mixed and per-skill; no root-level pack license governs everything uniformly.
  - Some skills contain examples of destructive or platform-specific shell usage and must be routed carefully.
  - Because Caveman and several design/review workflows are already integrated here, adding more sources without curation could create redundant or conflicting skills.
- Possible use:
  - Primary base for the eventual Codex Powerpack.
  - Reuse existing validators, indices, notices, and Codex-native agent structure.
- Redistribution:
  - Must follow per-skill notices inside `.agents/licenses/` and individual skill folders.

### 4. `sources/caveman`

- Status: missing.
- Master-prompt expectation: standalone source.
- Actual situation: Caveman already exists as integrated skills inside `skills-pack`, including `caveman`, `caveman-setup`, `caveman-review`, `caveman-compress`, `caveman-commit`, `caveman-help`, `caveman-stats`, and `cavecrew`.
- Risk:
  - Standalone provenance cannot be re-verified from a dedicated source folder during this pass.
- Recommendation:
  - Treat Caveman as already absorbed into `skills-pack` unless a separate source is later supplied.

### 5. `sources/graphify`

- Purpose: knowledge-graph tooling, install/update flows, and host-specific skill generation.
- Local verification:
  - Files: 644
  - Local VCS metadata: absent
  - License: MIT via [LICENSE](/workspaces/Codex-skills/sources/graphify/LICENSE)
  - Confirmed source URL from local metadata:
    - [sources/source-manifest.json](/workspaces/Codex-skills/sources/source-manifest.json)
    - [pyproject.toml](/workspaces/Codex-skills/sources/graphify/pyproject.toml)
  - Confirmed commit from local metadata:
    - `0c628fa38f2027f1e204935bceae1b9859474ef1`
- Formats:
  - Python package
  - Markdown docs and generated skill docs
  - YAML workflows
  - TOML/lock metadata
- Dependencies:
  - Core dependencies declared in [pyproject.toml](/workspaces/Codex-skills/sources/graphify/pyproject.toml)
  - Python `>=3.10`
  - `networkx`, `numpy`, `rapidfuzz`, many `tree-sitter-*` packages
  - Optional extras for `mcp`, `video`, `openai`, `anthropic`, `gemini`, `postgres`, `terraform`, `dm`, and others
- Hooks and automation:
  - [`.pre-commit-config.yaml`](/workspaces/Codex-skills/sources/graphify/.pre-commit-config.yaml)
  - Graphify docs and skill docs mention `/hooks` and installation flows
- Risks:
  - [README.md](/workspaces/Codex-skills/sources/graphify/README.md) recommends `curl | sh` for `uv`, which conflicts with the master-prompt safety rule.
  - The repository ships many host-specific skill variants and installation commands; these need exact Codex filtering.
  - Commands like `graphify install --platform codex` must be validated against real local behavior before any build step depends on them.
- Possible use:
  - Optional Graphify integration with explicit install/update/doctor/uninstall wrappers.
  - Dedicated Graphify skill wrapper and adapter files later in implementation.
- Redistribution:
  - MIT appears permissive, but bundled/generated dependency trees require separate care.

### 6. `sources/project-rules`

- Status:
  - Missing during phase 1 inventory
  - Present now as a first-party source for later phases
- Purpose:
  - clean Codex-native project rules
  - authored migration-safe policy text
  - stable source for core rules that should not live inside imported upstream material
- Current files:
  - [README.md](/workspaces/Codex-skills/sources/project-rules/README.md)
  - [AGENTS.base.source.md](/workspaces/Codex-skills/sources/project-rules/AGENTS.base.source.md)
  - [migration-policy.md](/workspaces/Codex-skills/sources/project-rules/references/migration-policy.md)
- Current interpretation:
  - This source is now the first-party home for clean Codex-native policy and migration support text.

## Duplicate Skills

Exact duplicate skill names were not found across the current source layouts.

Notes:

- `skills-pack` holds real Codex `SKILL.md` directories.
- `graphify` contains many host-specific `skill-*.md` documents, but they are platform variants of Graphify guidance, not duplicate installed skills in this workspace yet.

## Agent Name Collisions

Normalized collisions found:

1. `code_reviewer` vs `code-reviewer`
   - [code_reviewer.toml](/workspaces/Codex-skills/sources/skills-pack/.codex/agents/code_reviewer.toml)
   - [code-reviewer.md](/workspaces/Codex-skills/sources/subagents/categories/04-quality-security/code-reviewer.md)

2. `security_auditor` vs `security-auditor`
   - [security_auditor.toml](/workspaces/Codex-skills/sources/skills-pack/.codex/agents/security_auditor.toml)
   - [security-auditor.md](/workspaces/Codex-skills/sources/subagents/categories/04-quality-security/security-auditor.md)

Implication:

- A future merged distribution should not install both under near-identical names without explicit rename or precedence policy.

## Instruction and Format Conflicts

### Claude vs Codex agent format

- `subagents` uses Claude markdown frontmatter and Claude tool names.
- `skills-pack` already uses native Codex TOML agents.
- Mixing them directly would create invalid or ambiguous agent registration behavior.

### Slash commands vs Codex skill invocation

- Graphify docs are written around `/graphify` and host-specific install helpers.
- Codex pack routing should use Codex-native skills plus `AGENTS.md`, not raw imported slash-command assumptions.

### Oversized permanent prompts

- `claude-overlay` contains many very long prompt files that are useful as references but inappropriate for a short always-on core.

## Missing Tool / Environment References

Observed references that cannot be assumed to be available in the final pack:

- `uv`, `pipx`, and several optional Python extras in Graphify.
- Claude plugin marketplace flows in `subagents`.
- Hook-driven behavior referenced by Graphify and Caveman setup.
- Platform-specific browser, video, and shell tooling in some existing `skills-pack` skills.

These are not blockers, but they must be gated behind explicit runtime checks and optional integration paths.

## Dangerous Commands and Safety Flags

Examples detected in documentation or helper scripts:

- `curl | sh` in [graphify/README.md](/workspaces/Codex-skills/sources/graphify/README.md)
- `git reset --hard` examples inside Claude-overlay prompt material
- `rm -rf` examples inside some prompt/reference files
- PowerShell bypass example in [screenshot/SKILL.md](/workspaces/Codex-skills/sources/skills-pack/.agents/skills/screenshot/SKILL.md)

Current assessment:

- These detections are not proof of unsafe implementation by themselves.
- They are strong signals that any migration must filter source text and refuse blind carry-over of shell snippets into default instructions.

## Long Prompt / Large Instruction Files

Largest notable files worth treating as references instead of core:

- [claude-overlay/CHANGELOG.md](/workspaces/Codex-skills/sources/claude-overlay/CHANGELOG.md)
- [claude-overlay/README.md](/workspaces/Codex-skills/sources/claude-overlay/README.md)
- [claude-overlay/system-prompts/skill-model-migration-guide.md](/workspaces/Codex-skills/sources/claude-overlay/system-prompts/skill-model-migration-guide.md)
- [graphify/CHANGELOG.md](/workspaces/Codex-skills/sources/graphify/CHANGELOG.md)
- [skills-pack/.agents/skills/design-taste-frontend/references/core-upstream.md](/workspaces/Codex-skills/sources/skills-pack/.agents/skills/design-taste-frontend/references/core-upstream.md)
- [skills-pack/.agents/skills/impeccable/reference/live.md](/workspaces/Codex-skills/sources/skills-pack/.agents/skills/impeccable/reference/live.md)

## Readiness Verdict

Inventory phase is complete enough to proceed to the planning phase later, with these constraints:

- `skills-pack` should be treated as the primary integration base.
- `subagents` should be selectively adapted, not bulk-imported.
- `claude-overlay` should remain a reference source, not a raw always-on instruction source.
- `graphify` is promising but must be integrated as optional and validated against exact local commands.
- Missing standalone `caveman` and `project-rules` sources must be acknowledged in the plan.

## Created Artifacts

- [build/source-manifest.json](/workspaces/Codex-skills/build/source-manifest.json)
- [build/reports/source-inventory.md](/workspaces/Codex-skills/build/reports/source-inventory.md)

## 2026-07-03 Codebase Memory source addition

- `sources/codebase-memory-mcp-main` is present as an unchanged local upstream snapshot.
- Declared version: 0.8.1; license: MIT; commit: unverified because local `.git` is absent.
- Its broad upstream installer and hooks are not executed by Powerpack.
- The published form is a project-scoped adapter with isolated cache, managed Codex TOML,
  release checksum verification, explicit indexing, state tracking and exact uninstall.
