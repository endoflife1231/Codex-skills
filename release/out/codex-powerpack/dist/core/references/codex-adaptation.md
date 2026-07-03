# Codex Adaptation Notes

This distribution intentionally adapts upstream material instead of importing it wholesale.

## Claude-derived material

Use Claude-derived sources for:

- safety framing
- careful execution patterns
- review heuristics
- orchestration ideas
- migration references

Do not copy directly into the always-on core:

- Claude-only tool names
- Claude slash-command assumptions
- Claude plugin workflows
- model-specific claims
- long system prompt bodies

## Subagent migration

Subagents from `sources/subagents` are source material, not production-ready Codex agents.

Migration rules:

- keep the role intent
- rewrite the trigger for Codex tasks
- rewrite permissions in Codex-native terms
- narrow write access wherever possible
- remove marketplace or Claude-only installation assumptions
- merge overlaps into one canonical agent per role

## Quality filter

When choosing what to keep:

- prefer reusable engineering behavior over platform branding
- prefer clear completion criteria over verbose persona text
- prefer one strong implementation over multiple near-duplicates
- move long or risky material into references instead of core

## Core split

Use this rough split during implementation:

- `dist/core`: short universal policy
- `dist/core/references`: long-form migration, safety, and packaging notes
- `dist/agents`: Codex-native role definitions
- `dist/skills`: registered workflow knowledge
