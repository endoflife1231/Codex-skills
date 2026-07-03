# Codebase Memory MCP integration

This adapter installs a pinned Codebase Memory executable into a project-owned
Powerpack directory and registers it as a stdio MCP server for Codex. It never
runs the upstream broad installer and installs no hooks.

## Layout

- Binary: `<target>/.codex-powerpack/tools/codebase-memory-mcp`
- Cache/index: `<target>/.codex-powerpack/cache/codebase-memory/`
- State: `<target>/.codex-powerpack/state/codebase-memory.json`
- MCP config: `<target>/.codex/config.toml`
- Rules: a managed block in `<target>/AGENTS.md`

## Commands

```bash
bash dist/integrations/codebase-memory/install.sh --target /path/to/project --backup
bash dist/integrations/codebase-memory/index.sh --target /path/to/project
bash dist/integrations/codebase-memory/doctor.sh --target /path/to/project
bash dist/integrations/codebase-memory/uninstall.sh --target /path/to/project
```

Use `--binary /verified/local/codebase-memory-mcp` for offline installation.
Downloaded release archives are accepted only when their SHA-256 matches the
separately downloaded pinned `checksums.txt`. UI is opt-in with `--ui`; no detached
watcher is started by this integration.

Codebase Memory is the fast structural map for source code. Graphify remains the
better route for broad documentation, PDF/image knowledge and visual maps. When
both exist, query only the relevant backend and resolve disagreements against the
actual files and tests.
