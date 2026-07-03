# Codex Powerpack

Current assembled components:

- `core/`: short Codex-native base policy plus references
- `agents/`: curated Codex-native agent layer
- `skills/`: machine-readable registry plus actual installable Skill directories
- `profiles/`: `minimal`, `standard`, and `full` profile definitions
- `integrations/graphify/`: optional Graphify adapter
- `integrations/codebase-memory/`: project-scoped local MCP lifecycle
- `onboarding/`: deterministic scan, schema analysis, selection, hashed plan, apply and rollback
- `verify/`: distribution validation and doctor tooling
- `install/`: real project profile orchestrator with backup, state, update, and exact uninstall
- `manifests/`: build state and profile summary
- `licenses/`: distribution-level notices
- `release/`: local packaging flow with manifest and checksums

Key top-level docs:

- `ARCHITECTURE.md`: layer model and source strategy
- `FINAL_STATUS.md`: current release-ready local state of the assembled distribution
- `PROJECT_ADAPTATION.md`: intelligent project-specific onboarding
- `release/release_notes.md`: current release scope
- `build/reports/`: inventory and implementation planning history

This is an assembled Codex-native distribution with working validation, install helpers, and local release packaging.

It is suitable for product review, local packaging, and further editorial polish without requiring structural rework.
