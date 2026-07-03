# Codex Project Skills

This repository includes a local Codex skills pack in `.agents/skills`.

## Skill selection

- When the user names `$skill-name`, open and follow `.agents/skills/skill-name/SKILL.md`.
- Before substantial work without an explicit skill, match the task against `.agents/SKILLS_INDEX.md`. If the match is unclear, run `python3 .agents/tools/find_skill.py "<task description>" --top 8` and select the narrowest relevant workflow.
- Do not load every skill into context. Read only the selected `SKILL.md` and the references it explicitly requires.
- Skill-relative paths resolve from that skill directory, not from the repository root unless the skill says otherwise.

## Tool and safety rules

- Verify required CLIs, credentials, network access, and MCP servers before using integration-specific steps. Never fabricate tool output.
- Inspect bundled scripts before executing them. Prefer dry runs where available.
- Ask for explicit approval before deployment, publishing, pushing commits, destructive changes, or operations that affect external systems.
- Never print, commit, or copy secrets. Keep generated credentials and local state out of version control.
- Run the project-relevant tests, linters, and type checks after modifications; report anything that could not be run.

## Pack maintenance

- Validate the pack with `python3 .agents/tools/validate_pack.py`.
- The complete catalog is `.agents/SKILLS_INDEX.md`; migration details are `.agents/MIGRATION_REPORT.md`.

## Engineering lifecycle skills

- Use proportionate process: do not force a full interview, specification, or plan for a tiny, explicit, reversible change.
- For unclear intent, use `$interview-me` or `$idea-refine`; for substantial unspecified behavior, use `$spec-driven-development`.
- For multi-step work, prefer `$planning-and-task-breakdown`, `$context-engineering`, and `$incremental-implementation`.
- For failures, use `$debugging-and-error-recovery`; for test-first behavior changes, use `$test-driven-development`.
- For an explicitly requested end-to-end feature or release, use `$engineering-delivery-lifecycle`.
- Broad skills such as `$code-review-and-quality`, `$security-and-hardening`, and `$performance-optimization` complement, rather than replace, narrower framework and repository-specific skills.

## Project custom agents

Project-scoped Codex custom agents are in `.codex/agents/`: `code_reviewer`, `security_auditor`, `test_engineer`, `web_performance_auditor`, `cavecrew_investigator`, `cavecrew_builder`, `cavecrew_reviewer`, `impeccable_asset_producer`, and `impeccable_manual_edit_applier`. Spawn them only when the user explicitly requests subagents or parallel review. Keep orchestration in the parent session and merge their reports there. Impeccable must use its inline parent-session fallback when agent permission is absent.

## Extended design workflows

- Use `$impeccable` for existing production product UI: dashboards, tools, forms, settings, accessibility, UX copy, design audits, hardening, and live browser iteration.
- Use `$design-taste-frontend` for brand-led production frontend: landing pages, portfolios, campaigns, editorial sites, and image-first marketing builds.
- Use `$huashu-design` for HTML-based artifacts: high-fidelity prototypes, interactive demos, decks, motion, video/GIF workflows, and narrated explainers.
- Use `$imagegen` for standalone raster generation/editing and when a selected design workflow explicitly routes image work to it.
- Do not load these three broad design skills together. Choose by deliverable; an explicitly named skill wins.
- Impeccable hooks and Huashu media dependencies are opt-in. Preview hooks and require `/hooks` trust; verify and obtain approval before installing packages, downloading media, or using paid APIs.

## Caveman and Cavecrew

- Use `$caveman` only for an explicit Caveman/token-minimization request; it must not reduce technical correctness, evidence, warnings, or requested artifact quality.
- `$caveman-commit` and `$caveman-review` are narrow output-format skills. Do not let their broad topic words override the normal Git/review workflows.
- `$caveman-compress` must edit a candidate, validate it, preserve a backup, and require explicit overwrite intent before apply. It never calls Anthropic or Claude CLI.
- `$caveman-setup` is opt-in. Never modify `.codex/hooks.json` without preview, explicit approval, and Codex hook trust review.
- Invoking `$cavecrew` is an explicit request to use its compact custom agents. Keep orchestration in the parent session; do not recursively delegate.

## Marketing, SEO, content, and editorial skills

- Use `$product-marketing` to create `.agents/product-marketing.md`; marketing skills should reuse it rather than re-inventing positioning.
- Use `$content` only as a router. Prefer a narrow `$content-*` skill when the deliverable is known. Content-studio brand files live under `.agents/brand/`.
- `$content-strategy` is the broad marketing/SEO strategy skill; `$content-editorial-strategy` is the brand-led content-studio pillar and editorial workflow.
- `$seo-audit` is the deep SEO suite with bundled helpers and optional explicit subagents; `$marketing-seo-audit` is the lighter strategic/manual audit.
- External SEO, ads, analytics, CRM, directory, outreach, image-generation, and publishing integrations require capability, credentials, budget, and approval checks. Missing live data must be marked unavailable, never inferred.
- Use `$bilingual-transcreator` for RU↔EN transcreation, `$humanizer` for English editorial humanization, `$humanizer-ru` for Russian voice restoration, and `$ru-text` for Russian language quality. Keep factual claims intact and never optimize for detector evasion.
- The complete catalog is large enough that Codex may omit some metadata from the initial prompt. Use `.agents/tools/find_skill.py` or an explicit `$skill-name`.

## Imported SEO and content custom agents

The pack includes project agents `seo_*` and `content_*` under `.codex/agents/`. They are optional specialists, not automatic dependencies. Spawn them only when the user explicitly requests subagents/parallel work. Otherwise run the relevant skill inline. Keep orchestration in the parent session, limit fan-out, and merge evidence there.

