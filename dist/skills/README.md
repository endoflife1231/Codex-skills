# Skills Layer

This directory holds the published skill layer for the distribution.

Current shape:

- `registry.json` is the machine-readable catalog derived from the existing `skills-pack` base plus local curation metadata.
- The current registry keeps the full validated skill corpus visible while classifying entries into `core`, `specialized`, `design`, `integration`, `caveman`, and `reference-only`.
- the published corpus contains 254 installable skills: 252 from the updated `skills-pack` plus Codebase Memory and Graphify integration wrappers
- `catalog/` contains the actual release-bundled Skill directories; the registry is not metadata-only

Registry intent:

- keep `skills-pack` as the base instead of rebuilding the skill layer from scratch
- preserve quality by classifying skills instead of activating everything equally
- support profile routing for `minimal`, `standard`, and `full`

Notes:

- conflicts listed in the registry are routing conflicts, not structural errors
- hash values currently cover each skill's `SKILL.md`
- the published distribution already includes working profile manifests; future enrichment is optional metadata work rather than a missing product layer
