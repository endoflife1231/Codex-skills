---
name: caveman-compress
description: >-
  Safely compress a natural-language Markdown or text file into concise Caveman prose using the current Codex session, with preflight checks, an out-of-tree backup, candidate validation, and atomic apply. Trigger only on $caveman-compress or an explicit request to compress a memory/instruction file.
metadata:
  source: JuliusBrussee/caveman
  license: MIT
  codex_migration: '2026-06-27'
---

# Caveman Compress

Compress natural-language prose while preserving technical content and recoverability. This Codex migration does **not** call Anthropic, Claude CLI, or another model: Codex performs the rewrite in the current session, while bundled scripts handle only deterministic safety checks, backups, validation, and atomic replacement.

## Supported targets

Natural-language `.md`, `.markdown`, `.txt`, `.rst`, `.typ`, `.typst`, or `.tex` files. Refuse code/config files, credential-like paths, files over 2 MiB, and already generated backups.

## Workflow

1. Inspect the target and explain that successful apply will overwrite it while preserving a backup.
2. From the repository root, prepare a safe candidate:

   ```bash
   python3 .agents/skills/caveman-compress/scripts/workflow.py prepare "<file>"
   ```

   Record the returned `candidate`, `backup`, and `meta` paths.
3. Read the original and edit **only the candidate**. Compress prose by removing filler, repeated context, weak hedging, and redundant connective language.
4. Preserve exactly:
   - YAML frontmatter;
   - headings and their order;
   - fenced code blocks;
   - inline code;
   - URLs;
   - commands, file paths, identifiers, numbers, requirements, warnings, and ordering constraints.
5. Validate:

   ```bash
   python3 .agents/skills/caveman-compress/scripts/workflow.py validate "<meta>"
   ```

6. Fix candidate-only validation errors. Warnings require review but may be acceptable when intentional.
7. Before applying, show the user the backup path and a concise size/change summary. Apply only when the user explicitly requested the overwrite or confirms it:

   ```bash
   python3 .agents/skills/caveman-compress/scripts/workflow.py apply "<meta>"
   ```

8. If needed, restore:

   ```bash
   python3 .agents/skills/caveman-compress/scripts/workflow.py restore "<meta>"
   ```

## Compression rules

- Keep every instruction, exception, acceptance criterion, decision, and dependency.
- Prefer bullets and compact sentences where structure improves clarity.
- Never compress destructive-operation sequencing into ambiguous fragments.
- Do not alter code or exact strings merely to save tokens.
- Never process secrets, credentials, private keys, `.env` files, or content the user is not permitted to transform.

Backups/candidates live under `.codex/caveman-backups/`, which this pack adds to `.codex/.gitignore`.
