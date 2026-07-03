---
name: cavecrew
description: >-
  Route an explicitly requested compact subagent workflow among cavecrew_investigator, cavecrew_builder, and cavecrew_reviewer to save parent-context space. Trigger on $cavecrew, use cavecrew, delegate compactly, or an explicit request for compressed subagent output.
metadata:
  source: JuliusBrussee/caveman
  license: MIT
  codex_migration: '2026-06-27'
---

# Cavecrew

Cavecrew provides three project-scoped Codex custom agents whose result contracts are intentionally terse. Use only when the user invokes `$cavecrew`, names one of the agents, or explicitly asks for compact delegation. Keep orchestration in the parent Codex session.

## Choose an agent

| Task | Agent |
|---|---|
| Locate definitions, callers, uses, tests, or directory structure | `cavecrew_investigator` |
| Make an obvious surgical edit in one or two existing files | `cavecrew_builder` |
| Review a diff, branch, or file and return findings only | `cavecrew_reviewer` |

Prefer built-in `explorer` when broad explanation or architecture commentary is needed. Prefer built-in `worker` or the parent session for new features, three-plus-file changes, cross-cutting refactors, or work that needs command-heavy verification. Prefer `code_reviewer` for a thorough multi-axis report.

## Output contracts

`cavecrew_investigator`:

```text
path:line — `symbol` — short note
totals: ...
```

`cavecrew_builder`:

```text
path:line-range — change.
verified: evidence.
```

It may return `too-big`, `needs-confirm`, `ambiguous`, or `regressed` instead of editing.

`cavecrew_reviewer`:

```text
path:line: severity: problem. fix.
totals: ...
```

## Common flows

- **Locate → edit → review:** investigator, parent selects bounded sites, builder, reviewer.
- **Parallel locate:** spawn two or three investigators with non-overlapping questions, then merge results.
- **Known one-file edit:** builder directly.

## Boundaries

- `$cavecrew` counts as an explicit request to use these custom agents, but the parent still decides the minimum necessary fan-out.
- Do not recursively delegate from a Cavecrew agent.
- Do not use builder for destructive changes, credential work, deployment, or unclear scope.
- Use normal complete prose for security warnings and irreversible actions.
