---
name: iterative-runner
description: 'Run a bounded implement-test-debug loop in the current Codex session until explicit completion criteria pass or a documented stop condition is reached. Use for retry-until-green, flaky-test isolation, TDD repair loops, and multi-attempt implementation work. Triggers on: loop until done, keep trying, retry until pass, TDD loop, iterate until tests pass.'
metadata:
  codex_migration: '2026-06-27'
  source_path: skills/.curated/claude-main/.claude/skills/iterative-runner/SKILL.md
  migration_note: Rewritten for Codex as a bounded in-session workflow; recursive legacy agent invocation was removed.
---

# Iterative Runner

Use a **bounded, evidence-driven loop inside the current Codex session**. Do not start an unbounded background process, recursively launch another coding agent, or claim the work will continue after the current session ends.

## When to Use

- A failing test, type check, linter, or build needs several diagnose/fix/verify passes.
- The user explicitly asks to keep iterating until a measurable condition is satisfied.
- A TDD task benefits from repeated red → green → refactor cycles.
- A flaky or environment-sensitive failure needs controlled reproduction attempts.

For a single obvious edit, use the relevant domain skill directly instead of adding a loop.

## Required Inputs

Before the first iteration, record:

1. **Goal** — the behavior or artifact to produce.
2. **Verification command(s)** — exact tests, checks, or observable assertions.
3. **Maximum iterations** — default to 8 unless the task justifies another finite limit.
4. **Stop conditions** — secrets/credentials required, destructive action, external approval, missing dependency, repeated identical failure, or no new evidence.

## Loop

For iteration `1..N`:

1. Reproduce or run the narrowest relevant verification.
2. Capture the concrete failure signal: exit code, failing assertion, stack trace, diff, log line, or measured output.
3. Form one testable hypothesis. Do not batch unrelated speculative fixes.
4. Make the smallest change that can test the hypothesis.
5. Re-run the narrow check, then the broader affected suite when it passes.
6. Record what changed and what evidence was gained.
7. Stop immediately when all completion criteria pass.

If two consecutive iterations produce no new evidence, pause and change the diagnostic approach rather than repeating the same edit.

## TDD Variant

1. Add or identify a failing test that captures the required behavior.
2. Confirm it fails for the expected reason.
3. Implement the smallest behavior change.
4. Run the focused test until green within the iteration limit.
5. Refactor without changing behavior.
6. Run the broader relevant suite.

## Completion Report

Report one of these outcomes:

- **Completed** — list the passing verification commands and key changes.
- **Blocked** — state the exact blocker, evidence, attempted approaches, and the next safe action.
- **Iteration limit reached** — summarize remaining failures and the most likely next hypothesis.

Never emit a synthetic completion marker in place of real verification evidence.
