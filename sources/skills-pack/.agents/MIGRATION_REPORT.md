# Migration Report

Pack version: **2026-06-27.2**

## Combined pack

- Previous registered skills: **117**
- `agent-skills-main.zip` source skills inspected: **24**
- Directly migrated source skills: **23**
- Source meta-skill replaced by Codex-native lifecycle skill: **1**
- Registered skills in the updated pack: **141**
- Source personas converted to project-scoped Codex custom agents: **4**

## Codex-specific changes

- All imported skills moved to `.agents/skills/<name>/SKILL.md`.
- Frontmatter descriptions shortened and trigger scope clarified to improve implicit matching in a large pack.
- `skills/...` paths migrated to `.agents/skills/...`.
- Claude-specific `CLAUDE.md` guidance migrated to Codex `AGENTS.md` and nested override semantics.
- Claude/Gemini slash commands migrated into `$skill-name` invocation and `$engineering-delivery-lifecycle` orchestration.
- Chrome DevTools setup migrated from `.mcp.json` to Codex `codex mcp add` / `.codex/config.toml` syntax, with isolated-profile and missing-dependency safeguards.
- Four Markdown personas converted to `.codex/agents/*.toml`; review agents are read-only.
- Shared source references copied into the relevant skill directories for progressive disclosure.
- MIT license and provenance preserved.

## Deliberately excluded

- `.claude-plugin/`, `.claude/commands/`, `.gemini/commands/`, root `commands/`, hooks, marketplace manifests, and CI tests specific to the source repository.
- The source `using-agent-skills` skill as a separate registered skill, because it conflicts with the existing `$skill-router`. Its useful routing and lifecycle content was merged instead.
- Automatic MCP installation, credentials, deployment, pushing, or other external side effects.

The original pack's earlier deduplication and migration report is superseded by this combined report; the original provenance remains recorded in `.agents/SKILLS_INDEX.json`.


# Caveman integration — 2026-06-27.3

Source: user-provided `caveman-main.zip` (`JuliusBrussee/caveman`, MIT).

## Added

- Skills: `caveman`, `caveman-commit`, `caveman-review`, `caveman-compress`, `caveman-stats`, `caveman-help`, `caveman-setup`, `cavecrew`.
- Custom agents: `cavecrew_investigator`, `cavecrew_builder`, `cavecrew_reviewer`.
- Optional native Codex hook installer/handler under `$caveman-setup`.

## Adapted

- Slash-command wording → Codex `$skill-name` invocation.
- Claude agent Markdown → project `.codex/agents/*.toml`.
- Anthropic/Claude-powered compression → current-session Codex candidate editing plus deterministic local safety/validation scripts.
- Claude session-log statistics → deterministic original/compressed file metrics with explicitly approximate token estimate.
- Persistent Claude hooks → optional native Codex `SessionStart`/`UserPromptSubmit` hooks, not installed by default.
- Broad commit/review auto-triggers → explicit terse-output triggers to avoid conflicts with existing pack skills.

## Excluded

- Claude plugin/marketplace manifests, Gemini/OpenCode/OpenClaw installers, statusline scripts, npm installer, benchmarks/evals, generated website assets, and Claude-specific uninstaller.
- Upstream recursive model calls and unstable transcript scraping.

# Design workflow integration — 2026-06-28.1

Sources: user-provided `huashu-design-master` (MIT), `impeccable-main` (Apache-2.0), and `taste-skill-main` (MIT).

## Added

- Registered skills: `huashu-design`, `impeccable`, and `design-taste-frontend`.
- Project custom agents: `impeccable_asset_producer` and `impeccable_manual_edit_applier`.
- Huashu references, helper scripts, reusable HTML/React stage assets, and showcase references.
- Impeccable command references, local detector, live-iteration scripts, optional hook manager, and Codex asset workflow.
- Taste modes for core marketing frontend, redesign, image-to-code, web/mobile image direction, brand kits, minimalist/brutalist/high-end styles, GSAP motion, and Google Stitch.

## Deduplicated and adapted

- Three top-level products become exactly three registered skills; Taste's useful variants are progressive-disclosure references rather than competing global triggers.
- Routing boundaries are explicit: Impeccable owns production product UI, Design Taste owns brand/marketing frontend, and Huashu owns HTML prototypes/decks/motion/narration.
- Huashu `WebSearch`, task tracking, absolute source paths, and unconditional parallel-agent wording were converted to Codex capabilities, local skill paths, and explicit-permission agent behavior.
- Huashu optional Node/FFmpeg/voice dependencies now require preflight and approval; core HTML work remains dependency-free.
- Impeccable's nested agent profiles were moved to `.codex/agents/*.toml` with workspace-write defaults and parent-session fallback.
- Impeccable live copy editing no longer auto-selects Claude and no longer launches Codex with approval/sandbox bypass.
- Impeccable no longer self-updates independently through `npx`; upstream changes must be re-integrated and validated as a pack update.
- Missing `PRODUCT.md` triggers initialization for substantial design work but no longer blocks a narrow audit or explicitly scoped fix.
- Impeccable pinning writes only Codex `.agents/skills` shortcuts with supported frontmatter.
- Taste's unconditional bans and quantities are subordinate to the brief, existing identity, accessibility, repository dependencies, and user approval.

## Deliberately excluded

- Taste `design-taste-frontend-v1` (obsolete duplicate) and `full-output-enforcement` (conflicts with Codex context/completion controls).
- Separate global registrations for every Taste style and image mode, which would increase trigger collisions in an already large pack.
- Huashu demos, repository/marketing files, `.env.example`, test prompts, and bundled MP3/BGM/SFX assets.
- Impeccable site, extension, multi-provider installers, Claude plugin manifests, test fixtures, release tooling, and an automatically enabled project hook.
- Automatic dependency installation, credentials, paid API calls, hook trust, external publishing, or subagent spawning.

## Result

- Registered skills: **152** at the end of the first integration phase.
- Project-scoped custom agents: **9** at the end of the first integration phase.
- Design routing, skill index, README/AGENTS guidance, provenance, licenses, and validation coverage updated together.


# Integration report — 2026-07-03.1

## Input bundles analyzed

- `codex skills(2).zip`: 152 registered skills and 9 custom agents.
- `skills for update and integration.zip`: 103 `SKILL.md` files across eight source roots.

## Result

- Added unique registered skills: **100**.
- Final registered skills: **252**.
- Added Codex custom agents: **24** (18 SEO, 6 content).
- Final custom agents: **33**.
- Exact duplicate registrations removed: **3**.
- Distinct name conflicts resolved without dropping behavior: **2**.

## Name decisions

- Claude SEO keeps `$seo-audit`; Marketing Skills audit becomes `$marketing-seo-audit`.
- Marketing Skills keeps `$content-strategy`; Content Studio strategy becomes `$content-editorial-strategy`.
- The root and nested `ru-text` SKILL.md copies were identical and became one `$ru-text`.
- The extension copies of `seo-dataforseo` and `seo-image-gen` were identical to core copies; one skill is registered for each, with extension assets merged where unique.

## Claude-to-Codex migrations

- Slash-command routing changed to `$skill-name` routing.
- `CLAUDE.md`, `.claude/` context fallbacks, Claude tool names, and automatic Claude subagent assumptions were removed or overridden.
- 18 SEO Markdown agents and 6 content Markdown agents were converted into `.codex/agents/*.toml`. Source model names such as `sonnet` were not copied; agents inherit the active Codex model.
- Subagent spawning is explicit-only, matching Codex behavior. Every imported skill has an inline fallback.
- Shared source-root scripts moved under `.agents/vendor/` and all registered instructions use repository-relative paths.
- External integration steps are capability-gated and do not imply configured MCP, credentials, network, browser, account, budget, or authentication.
- Humanizer and Humanizer-RU were converted to compact progressive-disclosure skills; their complete upstream guides remain available as references.

## Files deliberately not activated

- Claude plugin manifests, marketplaces, Claude hooks and installers.
- Automatic hook installation or trust changes.
- Upstream GitHub workflows, issue templates, release tooling and promotional screenshots.
- Automatic package installation, credential setup, paid API calls, ad spend, publishing, URL submission or external mutation.

These omissions do not remove skill behavior; they remove platform-specific distribution/automation that is unsafe or irrelevant inside a repo-scoped Codex pack.

## Post-integration hardening

- Replaced remaining slash-command examples with `$skill-name` syntax across imported skills and custom agents.
- Rewrote optional MCP setup for Codex `config.toml` / `codex mcp`; no Claude settings mutation remains in active setup instructions.
- Added `.agents/CODEX_INTEGRATIONS.md` as the single credential and MCP setup guide.
- Rewrote the Nanobanana setup and validation scripts to call Codex MCP commands instead of editing another platform's settings file.
- Repaired marketing-tool registry links after moving shared assets into `.agents/vendor/`.
- Updated converted subagents to use `.agents/skills/...` paths and Codex skill names.
- Credentialed or potentially paid live-integration skills are marked explicit-only in `agents/openai.yaml`; planning and offline skills remain eligible for implicit routing.
