---
name: caveman-review
description: >-
  Produce explicitly requested compressed code-review findings as one actionable line per issue. Trigger on $caveman-review or a request for terse paste-ready review comments; do not replace full security, architecture, or general review workflows.
metadata:
  source: JuliusBrussee/caveman
  license: MIT
  codex_migration: '2026-06-27'
---

# Caveman Review

Review only the requested diff, branch, file, or change set. Return findings, not implementation.

## Finding format

```text
path/to/file.ts:42: 🔴 bug: user may be null after `find()`. Guard before `.email`.
```

Severity:

- `🔴 bug` — incorrect behavior, crash, data loss, or exploitable flaw;
- `🟡 risk` — edge case, race, leak, missing guard, or meaningful performance cliff;
- `🔵 nit` — optional style/naming issue; emit only when the user requests thorough review;
- `❓ question` — author intent is required before judging.

Sort findings by file and line. End with compact totals. If no issues are found, say `No issues found.` and identify what was actually reviewed.

## Rules

- Include exact path, line/range, symbol, problem, impact, and concrete fix.
- Remove praise, throat-clearing, and speculative refactors.
- Do not report formatting nits unless they affect meaning or were requested.
- Do not claim tests or runtime behavior were checked unless they were actually checked.
- For security findings or architectural disagreements, use a normal paragraph when one line would omit necessary threat or trade-off detail.

For a comprehensive multi-axis review use `$code-review-and-quality`; for a dedicated security pass use `$security-and-hardening` or the `security_auditor` custom agent.
