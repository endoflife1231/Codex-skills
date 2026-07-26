# Codex Powerpack

[Русская версия](README.ru.md) · [License](LICENSE) · [Third-party notices](THIRD_PARTY_NOTICES.md)

Codex Powerpack is an open-source, project-scoped distribution of Codex agents, skills, profiles, onboarding, verification, installation, update, uninstall, and rollback tooling.

## Requirements

- Linux, macOS, or Windows through WSL
- Bash
- Python 3.10+
- Codex CLI for normal Codex usage
- Optional: Graphify CLI and Codebase Memory binary for the corresponding integrations

## Quick start

```bash
unzip codex-powerpack-v0.2.1-user.zip
cd codex-powerpack-v0.2.1
./verify.sh
./install.sh --target /path/to/project --profile minimal
```

`minimal` is the safest offline-first profile. For the recommended larger profile:

```bash
./install.sh --target /path/to/project --profile standard --without-codebase-memory
```

Project-aware guided installation:

```bash
./adapt-project.sh --target /path/to/project --mode guided
./adapt-project.sh --target /path/to/project --mode guided --apply
```

Rollback or uninstall:

```bash
./rollback.sh --target /path/to/project
./uninstall.sh --target /path/to/project
```

## Profiles

- `minimal` — small, conservative, offline-first baseline
- `standard` — balanced profile for most engineering projects
- `full` — all license-audited skills included in this distribution

## Package types

- **User release:** only runtime files, user documentation, wrappers, manifests, licenses, and checksums.
- **Repository source:** user release plus maintainership docs, GitHub templates, CI workflows, release tooling, and project metadata.

## Safety and optional integrations

- Guided onboarding creates a reviewable plan before applying changes.
- Rollback restores the pre-apply snapshot.
- Codebase Memory may require an approved network download or a locally supplied verified binary.
- Graphify is optional and is not bootstrapped through unsafe installer pipelines.

## Repository structure

- `dist/` — runtime distribution
- `release/` — package builder and release notes
- `.github/` — validation and release workflows
- `docs/` — repository and maintainer documentation

## Validation

```bash
python3 dist/verify/validate_dist.py
bash dist/verify/doctor.sh
bash release/doctor_release.sh
```

## Documentation

- [Distribution overview](dist/docs/README.md)
- [Architecture](dist/docs/ARCHITECTURE.md)
- [Project adaptation](dist/docs/PROJECT_ADAPTATION.md)
- [Installation](dist/install/README.md)
- [Onboarding](dist/onboarding/README.md)
- [Open-source audit](OPEN_SOURCE_AUDIT.md)
- [Repository setup](docs/REPOSITORY_SETUP.md)

## Open-source status

First-party work is licensed under MIT. Third-party components retain their bundled licenses and notices. Skills are included only when redistribution evidence is preserved. Five unresolved skills remain excluded; see [OPEN_SOURCE_AUDIT.md](OPEN_SOURCE_AUDIT.md).
