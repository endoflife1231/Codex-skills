# Project adaptation onboarding implementation report

Date: 2026-07-03

## Delivered

- Deterministic scanner with dependency/build/secret exclusions and stable project fingerprint.
- Schema-bound Codex analysis contract plus an explicit deterministic fallback when
  `codex exec` is unavailable or fails.
- Explainable Skill, agent and integration selection producing separate selection files.
- Always-on Caveman and 12-Skill RU/EN live-language group.
- Routing between Codebase Memory and Graphify, with at least one required unless an
  explicit forced waiver is recorded.
- Compact generated project rules in five independent managed blocks (core plus four
  generated policy blocks); user text remains outside the blocks.
- JSON/Markdown plan and SHA-256 receipt; apply accepts only that plan and makes no
  component decisions.
- Fresh project fingerprint check, external dependency preflight, pre-apply snapshot,
  idempotent selected-component install, verification state and exact rollback.
- Repeat-analysis diff for Skills, agents and integrations.
- Backward-compatible routing metadata on relevant Skills and all canonical agents.
- Graphify's upstream Codex installer was replaced in the published path by a managed
  Powerpack wrapper because upstream enables a PreToolUse hook. The new path installs
  only a local Skill, AGENTS block and state; hooks/watchers remain off.

## Tests

`python3 tests/test_onboarding.py`: PASS

18 fixture classes passed:

1. small Python;
2. large Python/FastAPI;
3. Next.js + TypeScript;
4. React frontend;
5. Node/Express backend;
6. Next.js + Prisma + PostgreSQL;
7. Go service;
8. Rust CLI;
9. pnpm monorepo;
10. Docker/Kubernetes;
11. documentation-heavy;
12. PDF/images;
13. almost no code;
14. existing AGENTS.md;
15. existing project Skill;
16. existing MCP config;
17. existing Graphify output;
18. secret-pattern files.

The suite also validates all four JSON schemas, guided plan/apply/verify/rollback,
preservation of user rules, repeated analysis diff, explicit intelligence waiver,
plan hash tamper rejection, and Graphify apply/rollback through the hook-free wrapper.

`python3 tests/test_codebase_memory.py`: PASS

`python3 dist/verify/validate_dist.py`: PASS (8 agents, 254 Skills)

## Environment-dependent behavior

- `codex exec` is absent in the current workspace, so tested analysis used the marked
  deterministic fallback. The schema-bound invocation is implemented for environments
  where Codex CLI is available.
- `graphify` CLI is absent. Selection tests cover Graphify routing, while apply correctly
  stops before mutation if Graphify is selected but unavailable.
- Codebase Memory lifecycle is independently covered with both fixture and official
  checksum-verified release tests from prompt 1.

## Safety outcome

No project README command, hook, watcher, deployment, migration or secret content is
executed by onboarding. Analyze-only/guided planning writes only Powerpack analysis and
generated-plan artifacts. User configuration changes begin only in the apply phase after
hash, fingerprint and dependency checks plus backup.

## Release acceptance

- Final release build: PASS.
- Unpacked release validation without `sources/`: PASS.
- Unpacked release analyze-only: PASS.
- Unpacked release guided apply with a supplied local MCP fixture: PASS.
- Unpacked release project verification and rollback restoring original user rules: PASS.
