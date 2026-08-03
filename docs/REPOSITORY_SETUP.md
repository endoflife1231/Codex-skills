# Repository setup

Recommended GitHub metadata:

- Description: `Open-source Codex agents, skills, profiles, project onboarding, installation and rollback toolkit.`
- Topics: `codex`, `openai-codex`, `agent-skills`, `ai-agents`, `developer-tools`, `automation`, `cli`, `open-source`
- Website: leave empty unless a maintained project page exists

Enable Issues, Discussions, private vulnerability reporting, and GitHub Actions. Use squash merge by default and require the validation workflow on the default branch.

## Release process

1. Update `VERSION`, `CHANGELOG.md`, and `release/release_notes.md`.
2. Run `bash release/build_release.sh`.
3. Verify `release/out/SHA256SUMS`.
4. Push a tag such as `v0.2.3`.
5. The release workflow builds and attaches both archives.
