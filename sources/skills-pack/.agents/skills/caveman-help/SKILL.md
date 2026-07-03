---
name: caveman-help
description: >-
  Explain the installed Caveman suite, activation levels, related skills, optional hooks, and safe usage. Trigger on $caveman-help or questions about how Caveman works in this Codex pack.
metadata:
  source: JuliusBrussee/caveman
  license: MIT
  codex_migration: '2026-06-27'
---

# Caveman Help

Return a concise guide based on this installed package, not on assumptions about upstream Claude/Gemini integrations.

## Available skills

- `$caveman` — concise response mode for the current conversation.
- `$caveman-commit` — compact Conventional Commit message only.
- `$caveman-review` — compact one-line review findings.
- `$caveman-compress` — safely compress a natural-language file with backup and validation.
- `$caveman-stats` — compare original and compressed files using deterministic size metrics and rough token estimates.
- `$caveman-setup` — optionally install native project-local Codex hooks for cross-session persistence.
- `$cavecrew` — choose compact Codex subagents for locate/edit/review work.

## Custom agents

- `cavecrew_investigator` — read-only code locator.
- `cavecrew_builder` — bounded one/two-file implementation worker.
- `cavecrew_reviewer` — compact diff reviewer.

## Activation

Use `$caveman` and optionally say `lite`, `full`, `ultra`, `wenyan-lite`, `wenyan-full`, or `wenyan-ultra`. Say `stop caveman` or `normal mode` to deactivate in the current conversation.

Hooks are **not installed by default**. This prevents a dropped-in skill pack from silently changing every response or adding unreviewed project hooks. Use `$caveman-setup` only when persistent behavior is desired.

## Dependencies

Core skills require no external package. Compression helpers require Python 3. Optional hooks require Python 3 and a trusted project `.codex/` layer. No Anthropic API key or Claude CLI is used by this migration.
