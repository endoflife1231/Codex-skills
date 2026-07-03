---
name: codebase-memory
description: Use the project-scoped Codebase Memory MCP to explore symbols, imports, calls, architecture, diffs, and change impact before editing code.
---

# Codebase Memory

Use this Skill when a task requires understanding a non-trivial codebase: locate
symbols, follow calls or imports, inspect architectural boundaries, assess a git
diff, or estimate change impact. Start with the narrowest relevant MCP query.

The index is navigation help, never final authority. Read every real source file
you intend to change, confirm important claims against code and tests, and refresh
the index after substantial edits.

Use Graphify instead for broad documentation graphs, PDFs, images, semantic maps,
or mixed non-code corpora. If both integrations are installed, avoid asking both
the same question without a reason.

Do not use Codebase Memory to read secrets, replace test execution, or justify a
change solely from stale index output. If results look incomplete, check index
status, run the managed index command, then fall back to direct source inspection.
