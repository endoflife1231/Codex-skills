# Third-party notices

This pack was migrated from the user-provided archive. Per-skill license files are preserved where available; for skills without a local license file, the nearest source-repository license was copied as `LICENSE.source.txt`.

## agent-skills-main.zip

Imported workflow skills and custom-agent instructions are derived from the user-provided `agent-skills-main.zip` project.

- Copyright: © 2025 Addy Osmani
- License: MIT
- Canonical license copy: `.agents/licenses/agent-skills-MIT.txt`
- A `LICENSE.source.txt` copy is also present in every imported skill directory.

The Codex migration changes repository paths, project-instruction filenames, MCP configuration, invocation syntax, and subagent orchestration while retaining the substantive engineering guidance.


## caveman-main.zip

Caveman communication/compression workflows and Cavecrew agent concepts are derived from the user-provided `caveman-main.zip`.

- Copyright: Copyright (c) 2026 Julius Brussee
- License: MIT
- Canonical license copy: `.agents/licenses/caveman-MIT.txt`
- A `LICENSE.source.txt` copy is present in every imported Caveman skill directory.

Codex migration removes Anthropic/Claude runtime dependencies, replaces Claude session-log accounting with transparent file metrics, converts agents to project-scoped Codex TOML, narrows auto-triggers, and makes native Codex hooks explicitly opt-in.

## huashu-design-master

HTML prototype, presentation, motion, narration, critique, helper-script, component, and showcase material is derived from the user-provided `huashu-design-master` project.

- Copyright: Copyright (c) 2026 alchaincyf (花叔 · 花生)
- License: MIT
- Canonical license copy: `.agents/licenses/huashu-design-MIT.txt`
- Skill-local license: `.agents/skills/huashu-design/LICENSE.source.txt`

The Codex migration replaces provider-specific tool names with capability-based steps, enforces explicit subagent permission, adds dependency preflight, normalizes local paths, and excludes bundled MP3/BGM/SFX files whose reuse rights were not documented clearly enough for this pack.

## impeccable-main

Impeccable skill instructions, references, detector/live scripts, and two custom-agent profiles are derived from the user-provided `impeccable-main` project.

- Author: Paul Bakaus
- License: Apache License 2.0
- Canonical license copy: `.agents/licenses/impeccable-Apache-2.0.txt`
- Skill-local license: `.agents/skills/impeccable/LICENSE.source.txt`

The Codex migration keeps one repo-local `$impeccable` skill, converts nested agent profiles to project-scoped Codex agents, narrows implicit routing to product UI, limits pinning to `.agents/skills`, removes Claude as an automatic live-copy provider, removes approval/sandbox bypass, and leaves the design hook opt-in.

## taste-skill-main

Frontend design, image-direction, brand-kit, redesign, motion, style-mode, and Stitch guidance is derived from the user-provided `taste-skill-main` project.

- Copyright: Copyright (c) 2026 Leonxlnx
- License: MIT
- Canonical license copy: `.agents/licenses/taste-skill-MIT.txt`
- Skill-local license: `.agents/skills/design-taste-frontend/LICENSE.source.txt`

Thirteen upstream skills were deduplicated into one registered `$design-taste-frontend` workflow with mode-specific references. The legacy v1 and `full-output-enforcement` skills are excluded. Absolute aesthetic bans were demoted behind project identity, user intent, accessibility, and verified dependencies.


## Integrated writing, marketing, content and SEO sources (2026-07-03)

The following user-provided source bundles were integrated and adapted for Codex. Canonical license copies are stored in `.agents/licenses/`; source-local copies are stored in imported skill directories where a repository license was supplied.

- **claude-seo-main** — MIT, Copyright (c) 2026 agricidaniel.
- **content-skills-main** — MIT, Copyright (c) 2026 Vstorm.
- **humanizer-main** — MIT, Copyright (c) 2025 Siqi Chen.
- **humanizer-ru-main** — MIT, Copyright (c) 2026 Sergey Starikov; NOTICE preserved for the blader/humanizer adaptation.
- **marketingskills-main** — MIT, Copyright (c) 2025 Corey Haines.
- **ru-text-main** — MIT, Copyright (c) 2026 Arseniy Kamyshev.
- **claude-skills-main** — no repository-level license file was present in the supplied archive. Files are retained as user-directed private integration with explicit provenance; no broader redistribution permission is asserted by this pack.
- **bilingual-transcreator** — user-provided custom work; no license file was present.

Migration changes invocation syntax, state paths, shared runtime paths, agent manifests, tool assumptions and external-action guardrails while preserving the substantive workflows.
