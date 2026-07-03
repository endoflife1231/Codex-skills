<!-- CODEX-POWERPACK:BEGIN codebase-memory -->
Use Codebase Memory MCP first for code symbols, calls, imports, dependencies,
impact analysis, architecture, and git-diff exploration. Its index is a map, not
the source of truth: read the real files before editing and trust source plus tests
when results disagree. Refresh the index after substantial changes. Never index
secrets, and never substitute MCP output for running relevant tests.
<!-- CODEX-POWERPACK:END codebase-memory -->
