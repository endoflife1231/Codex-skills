# Orchestration Reference

This reference adapts the useful orchestration ideas from Claude-style meta-agents into Codex-native guidance.

## Parent session stays in control

- the parent session decides when a specialist agent is worth using
- the parent session defines scope, success criteria, and limits
- the parent session merges outputs into one coherent result for the user

## When to use specialist agents

- when a role is clearly narrower than the parent task
- when read-only review benefits from separation
- when a debugging, testing, or security pass needs a different lens

## When not to use them

- when the task is small and direct
- when multiple agents would duplicate the same work
- when the handoff cost is larger than the likely gain

## Good outputs

Every agent report should be easy for the parent session to merge:

- scope covered
- evidence or files examined
- findings or decisions
- unresolved risks
- recommended next step
