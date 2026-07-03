# Codebase Memory MCP upstream audit

Date: 2026-07-03  
Audited tree: `sources/codebase-memory-mcp-main/`  
Upstream: <https://github.com/DeusData/codebase-memory-mcp>  
Declared release: `0.8.1` (`server.json`)  
Provenance: local source snapshot; no embedded `.git`, commit therefore unverified.

## Verdict

The project is suitable as an optional, project-scoped Codex integration. Reuse the
MCP stdio server and its explicit `cli` tools. Do not invoke its broad upstream
`install`, `update`, or `uninstall` commands from Powerpack: those commands detect
many host clients and may modify user-level MCP configs, instruction files, skills,
and hooks.

## SAFE TO REUSE

- MIT-licensed first-party source and the released static executable.
- Stdio MCP mode: running the executable without a subcommand.
- Read/query tools and explicit `cli` calls, including `index_repository`,
  `index_status`, `search_graph`, `query_graph`, `trace_path`, `search_code`,
  `get_code_snippet`, `get_architecture`, and `detect_changes`.
- `CBM_CACHE_DIR` to isolate databases and configuration inside a target project.
- `--version` and `--help` for health checks.
- Release archives after platform selection and SHA-256 verification.
- Source builds through `scripts/build.sh` when a suitable C/C++ toolchain exists.

## NEEDS ADAPTATION

- Codex config: upstream targets `~/.codex/config.toml`; Powerpack must merge a
  managed project section into `<target>/.codex/config.toml` instead.
- Cache: upstream defaults to `~/.cache/codebase-memory-mcp`; Powerpack must set
  `CBM_CACHE_DIR=<target>/.codex-powerpack/cache/codebase-memory` in MCP config.
- Indexing: call `cli index_repository` explicitly and keep watcher/auto-index off
  unless the user selects it.
- Release installation: pin a version, download an archive and checksum manifest
  separately, verify SHA-256, then copy only the expected binary.
- Instructions: merge a small sentinel-delimited block into project `AGENTS.md`.
- Update/uninstall: operate only on files recorded in Powerpack state.

## DO NOT EXECUTE DIRECTLY

- Root `install.sh`: downloads `latest`, then runs the binary's broad `install -y`.
- `codebase-memory-mcp install`: auto-detects multiple clients and can modify
  user-level Codex/Claude/Gemini/OpenCode/editor configs, skills, instructions,
  and SessionStart/PreToolUse hooks.
- `codebase-memory-mcp update`: downloads and replaces its executable, then
  refreshes agent configuration.
- `codebase-memory-mcp uninstall`: removes configuration across detected clients;
  it is wider than a single Powerpack target.
- `scripts/install-git-hooks.sh` and any repository-development hook setup.
- Any `curl | sh` or `wget | bash` path.

## OPTIONAL

- UI build and local HTTP UI on port 9749. It must remain off by default.
- Auto-index and background watcher. They are useful for active codebases but are
  not required for a valid install.
- Committed `.codebase-memory/graph.db.zst` team artifact. Powerpack does not create
  or commit it automatically.
- Source build when a verified release binary cannot be used.

## UNSUPPORTED OR UNCLEAR

- Exact upstream commit: unavailable because the supplied snapshot has no `.git`.
- Windows project installer parity in this Bash-based Powerpack release. The
  upstream has Windows binaries, but this integration's orchestrator targets
  Linux/macOS shells and WSL/Codespaces.
- Offline installation without either a supplied executable or a previously
  downloaded managed executable.

## Technical findings

- License: MIT for the project. The source vendors permissively licensed parsers,
  libraries and Nomic model data; upstream details them in `THIRD_PARTY.md`.
- Version: `0.8.1` in `server.json`.
- Binary: `codebase-memory-mcp`; static release variants are documented for Linux
  amd64/arm64, macOS amd64/arm64 and Windows amd64.
- Build: C/C++ via `Makefile.cbm` and `scripts/build.sh`; optional React UI build.
- Storage: SQLite/index/config under `CBM_CACHE_DIR`, otherwise
  `~/.cache/codebase-memory-mcp`.
- MCP transport: stdio.
- UI: optional local HTTP server, default port 9749.
- Network: normal MCP/query/index operation is local. Upstream installer/update and
  update checks contact GitHub. Powerpack installation may contact the pinned
  GitHub release only to obtain a binary and checksum manifest.
- Hooks: upstream supports Claude PreToolUse and several SessionStart hooks;
  Powerpack installs none of them.
- Writes: index, ADR management, project deletion, config mutation and upstream
  install/update/uninstall are write-capable. Powerpack exposes indexing but keeps
  broad host mutation outside its managed workflow.
- Removal: Powerpack removes its MCP/AGENTS managed blocks and executable; cache is
  retained unless `--clear-cache` is explicit.
- Health: `--version`, TOML parsing, executable checksum, `cli index_status`, and an
  MCP initialize probe are suitable checks.

## Secret and noise policy

Powerpack supplies an ignore file excluding VCS data, dependencies, build output,
caches, `.env*`, private keys, credential/secrets patterns and common key files.
The integration must never inspect these files merely to decide whether to index.
