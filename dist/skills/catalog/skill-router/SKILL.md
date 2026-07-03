---
name: skill-router
description: Select the best local skill for a task and locate omitted skills in this large pack. Use when no exact skill was named or the right workflow is unclear.
metadata:
  author: local-migration
  codex_migration: '2026-06-27'
---

# Skill Router

Use this skill before substantial work when the user did not name an exact skill or when multiple skills could apply.

## Workflow

1. From the repository root, run:
   ```bash
   python3 .agents/tools/find_skill.py "<task description>" --top 8
   ```
2. Review the returned names and descriptions in `.agents/SKILLS_INDEX.md`.
3. Open only the selected `.agents/skills/<name>/SKILL.md` and the references it explicitly requires.
4. Follow that workflow. Combine skills only when their scopes are complementary.
5. Prefer the narrowest skill that fully covers the task. Use complementary skills in sequence; do not stack semantically duplicate review/security workflows without a reason.
6. For an explicit end-to-end feature or release workflow, use `$engineering-delivery-lifecycle`.
7. Verify external prerequisites (CLI, credentials, MCP servers, network access) before relying on them.

## Explicit invocation

Use `$skill-name` in Codex IDE/CLI to request a known skill directly. The router is a discovery fallback, not a replacement for the selected skill.


## Engineering lifecycle shortcuts

- Unclear underlying need: `$interview-me`; rough idea with multiple directions: `$idea-refine`.
- Substantial new behavior: `$spec-driven-development` → `$planning-and-task-breakdown` → `$incremental-implementation`.
- Failure: `$debugging-and-error-recovery`; test-first change: `$test-driven-development`.
- Pre-merge: `$code-review-and-quality`; production launch: `$shipping-and-launch`.
- Full explicitly requested workflow: `$engineering-delivery-lifecycle`.

The imported `using-agent-skills` meta-skill was not registered separately because it duplicated this router and imposed overly rigid “always invoke” behavior. Its useful lifecycle mapping is incorporated here and in `$engineering-delivery-lifecycle`.

## Communication and compact delegation shortcuts

- Explicit token-efficient replies: `$caveman`; compact commit text: `$caveman-commit`; compact review comments: `$caveman-review`.
- Safe prose-file compression: `$caveman-compress`; deterministic comparison: `$caveman-stats`.
- Opt-in cross-session Caveman hooks: `$caveman-setup` (never auto-install).
- Explicit compact subagents for locate / bounded edit / review: `$cavecrew`.

Do not select Caveman skills merely because the user asked for ordinary code, commits, or review. Their distinguishing requirement is explicit compression/terse output.
