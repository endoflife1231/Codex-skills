---
name: engineering-delivery-lifecycle
description: Orchestrate an end-to-end engineering change from intent and specification
  through planning, incremental implementation, verification, review, and launch.
  Prefer explicit invocation.
metadata:
  author: Adapted from Addy Osmani agent-skills; Codex migration by OpenAI
  license: MIT
  source_archive: agent-skills-main.zip
  codex_migration: '2026-06-27'
  category: Engineering lifecycle
---

# Engineering Delivery Lifecycle

Use this skill when the user wants a feature, migration, or release handled end to end rather than one isolated coding step. This is an orchestrator: it selects focused skills and does not duplicate their detailed procedures.

## Operating principles

- Scale the process to the task. A tiny, well-specified fix does not need a full product interview or a new specification.
- Surface material assumptions; do not block on low-risk details that can be resolved from repository evidence.
- Keep changes surgical and incremental.
- Do not deploy, publish, push, merge, rotate credentials, or run destructive migrations without explicit approval.
- Verification is evidence: tests, builds, linters, runtime checks, traces, or source citations as appropriate.

## Lifecycle routing

1. **Clarify**
   - Use `$interview-me` when the underlying need, audience, or constraints are genuinely unclear.
   - Use `$idea-refine` when alternatives and trade-offs should be explored before committing.
2. **Specify**
   - Use `$spec-driven-development` for substantial new behavior without an adequate spec.
   - Skip a new spec when acceptance criteria are already explicit or the change is small and reversible.
3. **Plan**
   - Use `$planning-and-task-breakdown` for multi-step or dependency-heavy work.
   - Use `$context-engineering` to load only the relevant instructions, code, tests, and docs.
   - Use `$source-driven-development` for version-sensitive APIs and libraries.
4. **Implement**
   - Use `$incremental-implementation` for vertical slices.
   - Add `$test-driven-development` when tests can define the behavior contract.
   - Add domain skills such as `$frontend-ui-engineering`, `$api-and-interface-design`, or framework-specific skills from the local index.
5. **Recover**
   - On a failure, use `$debugging-and-error-recovery`; do not repeat the same command without changing the hypothesis or code.
6. **Review**
   - Use `$code-review-and-quality` and `$code-simplification` before integration.
   - Add `$security-and-hardening`, `$performance-optimization`, and `$browser-testing-with-devtools` only when their scopes apply.
7. **Ship**
   - Use `$documentation-and-adrs`, `$observability-and-instrumentation`, `$deprecation-and-migration`, `$ci-cd-and-automation`, and `$shipping-and-launch` as needed.
   - Produce a rollback plan for production-bound changes.

## Explicit parallel ship review

When the user explicitly requests a comprehensive ship review, Codex may spawn these project custom agents in parallel:

- `code_reviewer` — correctness, readability, architecture, security, and performance.
- `security_auditor` — vulnerabilities, trust boundaries, auth, secrets, dependencies, and LLM risks.
- `test_engineer` — coverage gaps and missing happy-path, edge, failure, and concurrency tests.

Wait for all reports, deduplicate findings, and produce one `GO` or `NO-GO` decision. Any critical security, correctness, or data-loss finding is a default blocker. Include an executable rollback plan. For a web-only performance audit, explicitly spawn `web_performance_auditor` or use `$performance-optimization` with browser evidence.

## Completion report

Report:

- what was clarified or assumed;
- files and behavior changed;
- tests, build, lint, type checks, and runtime verification performed;
- review findings and remaining risks;
- approvals still required for external or destructive actions.
