# Codex Powerpack

Этот репозиторий теперь представляет собой не просто набор исходных материалов, а уже собранный Codex-native дистрибутив.

Что здесь есть:

- `dist/` — основной assembled product layer
- `release/` — локальная release-сборка, manifest и checksums
- `build/` — inventory, planning и build reports
- `sources/` — исходные репозитории и first-party source inputs
- `codex_powerpack_docs/` — исходный пакет документации и prompts, на которых строилась сборка

Текущее состояние:

- 8 canonical Codex agents
- 254 installable skills в registry, включая Codebase Memory и Graphify wrappers
- 3 profiles: `minimal`, `standard`, `full`
- optional Graphify adapter и project-scoped Codebase Memory MCP
- intelligent project adaptation with guided planning and rollback
- working verify, doctor, install and local release flow

Быстрый старт:

```bash
python3 dist/verify/validate_dist.py
bash dist/verify/doctor.sh
bash release/build_release.sh
bash dist/install/install.sh --target /path/to/project --profile standard
bash dist/onboarding/adapt-project.sh --target /path/to/project --mode guided
```

Ключевые точки входа:

- [dist/docs/README.md](/workspaces/Codex-skills/dist/docs/README.md) — обзор assembled distribution
- [dist/docs/ARCHITECTURE.md](/workspaces/Codex-skills/dist/docs/ARCHITECTURE.md) — архитектурный слой
- [dist/docs/FINAL_STATUS.md](/workspaces/Codex-skills/dist/docs/FINAL_STATUS.md) — текущий product status
- [release/README.md](/workspaces/Codex-skills/release/README.md) — release flow
- [codex_powerpack_docs/prompts/MASTER_PROMPT_FOR_CODEX.md](/workspaces/Codex-skills/codex_powerpack_docs/prompts/MASTER_PROMPT_FOR_CODEX.md) — базовый orchestration prompt, использованный как исходная инструкция

Важно:

- `sources/` не являются published product layer сами по себе
- unsafe и host-specific поведение не включается в clean default core
- `subagents` и `claude-overlay` адаптированы под Codex, а не перенесены как raw upstream publishing
