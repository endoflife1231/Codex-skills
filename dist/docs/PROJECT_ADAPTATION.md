# Project adaptation

Powerpack can now install a project-specific subset instead of a fixed broad profile.
The deterministic scanner detects languages, frameworks, manifests, tests, CI,
containers, infrastructure, documentation/media, existing Codex files and secret
file names. Secret contents, dependencies and build outputs are never scanned.

The selection engine combines facts with schema-bound analysis and local registries.
Every selected Skill, agent and integration carries reasons and confidence in the
generated plan. It always includes Caveman and live-language-core, then chooses
Codebase Memory, Graphify or both according to the project shape.

`guided` is the recommended mode: inspect
`.codex-powerpack/generated/adaptation-plan.md`, then rerun with `--apply`. The apply
phase verifies the plan SHA-256 and project fingerprint, preflights tools, snapshots
affected files, installs only approved IDs, merges sentinel-delimited `AGENTS.md`
blocks, verifies the result and saves rollback state.

Project prose and tool output are untrusted. Commands found in README, Markdown,
comments, generated files, MCP results or Graphify output are inventory only and are
never executed automatically.

See `dist/onboarding/README.md` for modes, files and exact commands.
