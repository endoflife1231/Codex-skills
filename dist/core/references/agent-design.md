# Agent Design

The final agent layer should be small, clear, and Codex-native.

## Target base roles

- explorer
- planner
- implementer
- debugger
- reviewer
- tester
- security-reviewer
- architect

## Default write policy

Read-only by default:

- explorer
- planner
- reviewer
- security-reviewer

Write-enabled when needed:

- implementer
- debugger
- tester
- architect

## Migration principles

- Use existing Codex-native agents from `skills-pack` where they already fit.
- Use `subagents` only as role-source material.
- Do not ship overlapping agents that do the same job with different names.
- Preserve parent-session orchestration instead of hiding logic in nested autonomous behavior.

## Reporting expectations

Every agent should have a compact report shape:

- scope reviewed or changed
- key findings or decisions
- unresolved risks
- verification performed
- recommended next step, if any

## Review agents

Review-style agents should focus on:

- correctness
- safety
- behavioral regressions
- missing validation

They should avoid becoming general-purpose implementers unless the user explicitly asks for that behavior.
