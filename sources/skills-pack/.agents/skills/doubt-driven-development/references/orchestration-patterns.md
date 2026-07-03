# Codex Orchestration Patterns

Use these patterns when a task benefits from skills or project-scoped custom agents. Keep orchestration in the parent Codex session, keep delegation shallow, and preserve user checkpoints around consequential actions.

## Available primitives in this pack

- **Skills:** `.agents/skills/<name>/SKILL.md`, invoked explicitly as `$skill-name` or selected from their descriptions.
- **Project instructions:** root `AGENTS.md` plus narrower nested instruction files.
- **Custom agents:** `.codex/agents/*.toml`; this pack includes `code_reviewer`, `security_auditor`, `test_engineer`, and `web_performance_auditor`.
- **Parent session:** owns the plan, approvals, edits, and final synthesis.

A custom agent is not a hidden workflow engine. It is a focused, usually read-only perspective that reports back to the parent.

## Pattern 1: Direct skill execution

Use one narrow skill in the parent session when one workflow fully covers the task.

```text
User request → $debugging-and-error-recovery → reproduce → fix → verify → report
```

Best for:
- one artifact or one failure mode;
- tasks that require editing in the main workspace;
- work where delegation adds no independent evidence.

Do not spawn a subagent merely to rename, format, or run a deterministic command.

## Pattern 2: One specialist custom agent

Use one custom agent when a fresh, isolated perspective is valuable and the output can be a report.

```text
Parent Codex session
  ├─ provides exact artifact, scope, and question
  └─ spawns code_reviewer (read-only)
        └─ returns findings with evidence
Parent validates findings and decides what to change
```

Good matches:
- `code_reviewer` for correctness, maintainability, and architecture;
- `security_auditor` for trust boundaries, auth, secrets, and exploit paths;
- `test_engineer` for regression coverage and test strategy;
- `web_performance_auditor` for browser-backed performance evidence.

The parent must verify findings against the actual repository before applying them.

## Pattern 3: Flat parallel fan-out with parent merge

Use parallel specialists only when their scopes are independent enough to avoid duplicated work.

```text
                         ┌─ code_reviewer ───────┐
Known diff or release ───┼─ security_auditor ────┼─ parent deduplicates → GO/NO-GO
                         └─ test_engineer ────────┘
```

Required conditions:
1. Each agent receives the same immutable artifact or clearly separated scope.
2. Each agent has a distinct question.
3. Agents do not recursively spawn more reviewers.
4. The parent waits for all reports, checks evidence, removes duplicates, and resolves contradictions.
5. A critical correctness, security, or data-loss finding blocks a GO decision by default.

Suggested prompt:

```text
Spawn `code_reviewer`, `security_auditor`, and `test_engineer` in parallel.
Give each the current diff and its domain-specific question. Keep them read-only.
Wait for all reports, validate cited files/lines, deduplicate findings, and produce
one GO/NO-GO decision with required fixes and a rollback plan.
```

## Pattern 4: Human-checkpoint lifecycle

For a large feature or migration, combine skills sequentially while the parent and user retain decision points.

```text
$interview-me or $idea-refine
  → $spec-driven-development
  → $planning-and-task-breakdown
  → $incremental-implementation + domain skill
  → $test-driven-development / $debugging-and-error-recovery
  → $code-review-and-quality
  → $shipping-and-launch
```

Use `$engineering-delivery-lifecycle` as the map, not as permission to execute every phase automatically. Skip phases that add no value. Require explicit approval before deploy, publish, push, destructive migration, or external-system changes.

## Pattern 5: Competing-hypothesis debugging

When several plausible root causes fit sparse evidence, use independent investigators and let the parent maintain the evidence board.

Example:

```text
Problem: checkout occasionally hangs for ~30 seconds.

Spawn three read-only investigations:
- code_reviewer: race conditions, blocking calls, concurrency ordering;
- security_auditor: auth/session paths and synchronous external calls;
- test_engineer: experiments that discriminate among hypotheses.

Each report must include: hypothesis, supporting evidence, disconfirming evidence,
and the smallest next experiment. The parent compares reports and runs the most
discriminating experiment before choosing a fix.
```

Do not invent direct agent-to-agent messaging. The parent session is the coordination and reconciliation layer.

## Pattern 6: Fresh-context adversarial review

For `$doubt-driven-development`, pass only:
- the artifact;
- the contract;
- an adversarial issues-only prompt.

Do not pass the parent's claim or long session narrative. This reduces anchoring. Use a read-only specialist when available; otherwise perform a clearly labeled degraded self-review.

## Anti-patterns

### Router agent with no domain value

Bad:

```text
user → meta-router agent → reviewer → router summary → user
```

Use `$skill-router`, the local index, or the parent session instead. Extra paraphrasing loses evidence and hides cost.

### Reviewer recursively spawning reviewers

A specialist should report what additional audit is needed; the parent decides whether to spawn it. Keep the delegation tree flat unless the user explicitly requests a deeper experiment and the configured Codex limits permit it.

### Sequential mega-agent

Do not delegate an entire spec → plan → build → test → ship pipeline to one subagent. It removes user checkpoints and compounds context loss. Keep implementation and approvals in the parent.

### Duplicate lenses

Do not run several nearly identical review skills or agents just to increase apparent confidence. Choose distinct lenses and define the question for each.

### Unverified synthesis

Never merge agent reports by majority vote. Check cited files, commands, and evidence. A confident hallucinated finding is still wrong.

## Decision flow

```text
Can one narrow skill handle the task?
├─ Yes → run it in the parent session.
└─ No  → Is an independent report useful?
         ├─ No → combine complementary skills sequentially.
         └─ Yes → Is one specialist enough?
                  ├─ Yes → spawn one custom agent.
                  └─ No  → fan out flat with distinct scopes; parent merges.
```

## Completion checklist

- [ ] Selected skills/agents are registered in this pack.
- [ ] Delegated scope excludes secrets and unrelated context.
- [ ] Write permissions are no broader than required.
- [ ] External side effects still require user approval.
- [ ] Parent validated evidence and commands.
- [ ] Final report distinguishes verified facts, inferences, and unrun checks.
