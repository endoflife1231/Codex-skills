# Source and Codex migration

- **Source bundle:** `content-skills-main`
- **Source path:** `skills/content-linkedin`
- **Integrated pack:** `2026-07-03.1`
- **License status:** See `LICENSE.source.txt` when present.

## Migration notes

Ported from a Claude-oriented content studio. Slash routing became direct `$content-*` skill invocation, brand state moved to `.agents/brand`, and optional parallel agents became project-scoped Codex custom agents.
