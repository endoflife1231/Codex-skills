# Source Policy Map

This file maps source families to their intended place in the final distribution.

## `sources/skills-pack`

Primary base for:

- skills
- existing Codex-native agents
- pack validation patterns
- Caveman integration

Secondary source for:

- core wording that is already Codex-compatible

## `sources/subagents`

Primary source for:

- role ideas
- completion criteria
- useful specialist behaviors

Not a direct source for:

- final agent file format
- default tool permissions
- installation workflow

## `sources/claude-overlay`

Primary source for:

- careful execution patterns
- safety reminders
- review heuristics
- migration references

Not a direct source for:

- always-on Codex core
- raw tool descriptions
- Claude-specific host behavior

## `sources/graphify`

Primary source for:

- optional Graphify integration
- adapter inputs
- verified package metadata

Not a direct source for:

- mandatory core behavior
- unfiltered install commands

## First-party material

First-party authored material may be used for:

- `project-rules`
- cleaned Codex-native core policy
- final registries
- packaging, manifests, and release docs
