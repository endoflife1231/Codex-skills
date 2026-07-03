# Codebase Memory MCP integration test report

Date: 2026-07-03

## Automated results

Command: `python3 tests/test_codebase_memory.py`

Result: PASS

Covered scenarios:

1. clean project-scoped install from a supplied executable;
2. merge over an existing valid `.codex/config.toml`;
3. preservation of existing `AGENTS.md` text;
4. repeated/idempotent install without duplicate MCP or AGENTS blocks;
5. state receipt and binary SHA-256 recording;
6. explicit indexing path and log creation;
7. integration doctor;
8. Codespaces-style restore without needless reindex;
9. dry-run without target mutation;
10. unmanaged same-name MCP section conflict and `.new` candidate;
11. valid TOML after managed merge;
12. exact uninstall with user config/text preserved;
13. cache preservation by default;
14. cache deletion only with `--clear-cache`;
15. unsupported architecture rejection before download;
16. wrong/upstream-diverged checksum rejection;
17. missing network failure before MCP configuration;
18. no Graphify present (non-blocking warning);
19. Caveman/live-language Skill and Codex agent deployment through the common installer;
20. common uninstall of only managed project files.

## External release verification

- Official tag `v0.8.1` exists and points at release commit `f0c9be1`.
- Official `checksums.txt` was retrieved separately.
- Linux/macOS standard and UI artifact hashes were pinned in `checksums.json`.
- A real Linux amd64 portable archive was downloaded, matched against both the
  pinned hash and upstream manifest, executed only with `--version`, configured in
  a temporary target, verified, and uninstalled successfully.

## Distribution checks

- `python3 dist/verify/validate_dist.py`: PASS (8 agents, 253 skills)
- `bash dist/verify/doctor.sh`: PASS
- `bash release/doctor_release.sh`: PASS after final rebuild
- unpacked release validation plus minimal install/uninstall without `sources/`: PASS
- Shell syntax checks for all integration/install scripts: PASS

## Intentionally not enabled

- No upstream broad `install`, `update`, or `uninstall` command was executed.
- No upstream hooks were installed.
- UI and watcher remain opt-in.
- Prompt 2 project-onboarding/adaptation was not implemented in this pass.
