---
name: caveman-commit
description: >-
  Generate an explicitly requested terse Conventional Commit message with a precise subject and only necessary rationale. Trigger on $caveman-commit or requests for a very short commit message; do not replace the general Git workflow or run git commit.
metadata:
  source: JuliusBrussee/caveman
  license: MIT
  codex_migration: '2026-06-27'
---

# Caveman Commit

Generate a commit message only. Do not stage, commit, amend, push, or change files.

## Subject

```text
<type>(<scope>): <imperative summary>
```

- Allowed types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, `revert`.
- Scope is optional and should match project convention.
- Use imperative mood: `add`, `fix`, `remove`.
- Prefer at most 50 characters; hard cap 72.
- No trailing period.
- Match repository capitalization conventions.

## Body

Omit the body when the subject explains the change. Include it only for:

- non-obvious rationale;
- breaking changes;
- security fixes;
- data/schema migrations;
- rollback/revert context;
- required issue references.

Wrap at 72 characters. Explain **why**, not a diff summary. Use trailers such as `Closes #42` only when grounded in the task or repository context.

## Output

Return one copy-ready code block. Do not add an explanation before or after it unless important information is missing.

## Boundaries

Do not invent issue numbers, breaking-change details, attribution trailers, or verification claims. If the staged diff is unavailable, derive only from files/context actually inspected and state the uncertainty outside the message.
