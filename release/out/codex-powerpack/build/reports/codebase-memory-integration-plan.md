# Codebase Memory MCP integration plan

1. Preserve the supplied upstream snapshot under `sources/codebase-memory-mcp-main`.
2. Add a project-scoped adapter with pinned metadata and safe routing rules.
3. Add managed install/configure/index/update/verify/doctor/uninstall/restore roles.
4. Add a generated integration Skill and a short managed AGENTS fragment.
5. Register Codebase Memory beside Graphify and expose profile policies.
6. Turn the distribution installer into an idempotent project orchestrator while
   retaining distribution validation and dry-run support.
7. Add license/notices, state receipts, fixtures, integration tests and validators.
8. Run clean/repeat/uninstall/dry-run/conflict/checksum/restore tests, distribution
   doctor, and release build; record exact results.

Prompt 2 onboarding/adaptation is explicitly out of scope for this pass.
