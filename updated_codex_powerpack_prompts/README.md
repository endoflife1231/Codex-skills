# Updated Codex Powerpack prompts

Файлы:

1. `PROMPT_1_integrate_codebase_memory_mcp.md` — интеграция `codebase-memory-mcp-main` в текущий Codex Powerpack.
2. `PROMPT_2_project_adaptation_onboarding.md` — автоматическая адаптация дистрибутива под конкретный проект.

Оба промпта адаптированы под текущую структуру твоего архива:

- `dist/skills/registry.json`
- `dist/agents/registry.json`
- `dist/core/AGENTS.base.md`
- `dist/integrations/graphify/adapter.json`
- `dist/profiles/minimal.yaml`
- `dist/profiles/standard.yaml`
- `dist/profiles/full.yaml`
- `dist/install/install.sh`
- `dist/verify/validate_dist.py`

Ключевые обновления:

- Caveman всегда устанавливается.
- Live-language RU/EN Skills всегда устанавливаются.
- В каждом проекте должен быть Codebase Memory MCP, Graphify или оба.
- Выбор Codebase Memory/Graphify зависит от сложности и типа проекта.
- Система не ставит все Skills подряд, кроме always-on групп.
- `install.sh` должен быть доработан из проверочного stub в настоящий orchestrator.
