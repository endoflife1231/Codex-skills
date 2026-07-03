# Install Layer

The installer is a project-scoped orchestrator. It validates the distribution,
installs the selected profile's real Skill directories and Codex agent files,
merges the managed core block into `AGENTS.md`, records state, and optionally
installs Codebase Memory MCP.

```bash
bash dist/install/install.sh \
  --target /workspaces/my-project \
  --profile standard \
  --with-codebase-memory
```

Standard and full profiles enable Codebase Memory by default; minimal leaves it
optional. Use `--without-codebase-memory` to opt out, or
`--codebase-memory-binary /path/to/verified/binary` for an offline install.

Updates reuse the same managed paths and preserve user text. Uninstall removes
only files and blocks recorded by Powerpack; Codebase Memory cache is retained
unless `--clear-cache` is explicit.

For project-aware selection instead of a static profile, use:

```bash
bash dist/onboarding/adapt-project.sh --target /path/to/project --mode guided
```
