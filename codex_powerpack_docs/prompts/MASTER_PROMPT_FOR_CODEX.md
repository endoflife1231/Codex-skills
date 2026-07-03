# Мастер-промпт: сборка Codex Powerpack

Ты работаешь как ведущий инженер по интеграции и сборке.

## Цель

Собрать единый переносимый дистрибутив для Codex из локально предоставленных исходников.

Он должен объединить:

1. адаптированные агентные правила;
2. субагентов;
3. пользовательский Skill-пак;
4. Caveman;
5. Graphify;
6. профили;
7. install/update/uninstall;
8. verify/doctor;
9. Codespaces support;
10. лицензии и manifests;
11. документацию;
12. воспроизводимый ZIP-релиз.

## Источники

```text
sources/
├── claude-overlay/
├── subagents/
├── skills-pack/
├── caveman/
├── graphify/
└── project-rules/
```

Если источник отсутствует, не выдумывай содержимое. Отметь `missing` и продолжай с доступными частями.

## Жёсткие правила

- Не утверждай, что переносишь интеллект другой модели.
- Сначала изучи реальные файлы.
- Не угадывай формат Codex.
- Не угадывай команды Graphify.
- Не запускай непроверенные hooks.
- Не используй `curl | sh`.
- Не перезаписывай пользовательские файлы.
- Не складывай все инструкции в один AGENTS.md.
- Не включай всех агентов и Skills без отбора.
- Не давай всем агентам запись.
- Не включай исходник без проверки лицензии.
- Не меняй папки `sources/`.
- Работай в `build/`, `dist/`, `release/`.
- Используй точные версии и hashes.
- Перед опасным действием покажи план.

## Этап 1. Инвентаризация

Создай:

```text
build/reports/source-inventory.md
build/source-manifest.json
```

Для каждого источника укажи:

- путь;
- назначение;
- URL;
- commit/tag;
- лицензию;
- форматы;
- исполняемые файлы;
- hooks;
- зависимости;
- риски;
- возможное использование;
- ограничения перераспространения.

Найди:

- дубликаты Skills;
- совпадения имён агентов;
- конфликтующие инструкции;
- ссылки на отсутствующие инструменты;
- длинные постоянные промпты;
- опасные команды.

Не начинай реализацию до завершения отчёта.

## Этап 2. План

Создай:

```text
build/reports/implementation-plan.md
```

Включи:

- целевую структуру;
- mapping каждого источника;
- выбранных и исключённых агентов;
- выбранные Skills;
- конфликты;
- стратегию AGENTS.md;
- Caveman policy;
- Graphify adapter;
- Codespaces;
- лицензии;
- тестовую матрицу.

## Этап 3. Core policy

Раздели инструкции на:

- короткий core;
- references;
- Skills;
- инструкции агентов;
- удаляемые специфичные части.

Создай:

```text
dist/core/AGENTS.base.md
dist/core/references/
```

Core должен требовать:

- исследование перед изменением;
- минимальный diff;
- проверку реального кода;
- запуск тестов;
- фиксацию непроверенного;
- контроль write-доступа;
- безопасную работу.

## Этап 4. Субагенты

Создай агентов в фактически поддерживаемом формате Codex.

Минимум:

- explorer;
- planner;
- implementer;
- debugger;
- reviewer;
- tester;
- security-reviewer;
- architect.

Для каждого определи:

- назначение;
- триггер;
- чтение;
- запись;
- инструменты;
- формат отчёта;
- критерии завершения;
- Caveman policy;
- Graphify policy;
- источник и лицензию.

Explorer, Planner, Reviewer и Security Reviewer по умолчанию не редактируют проект.

## Этап 5. Skills

Создай:

```text
dist/skills/registry.json
```

Для каждого Skill:

- имя;
- описание;
- источник;
- профиль;
- зависимости;
- конфликты;
- лицензия;
- hash.

При конфликте не перезаписывай молча.

## Этап 6. Caveman

Подключи Caveman как отдельный Skill.

Политика:

- главный агент: Lite;
- финальный ответ: configurable;
- Tester, Reviewer, Debugger, Security Reviewer: без агрессивного сжатия;
- команды, ошибки, файлы, строки и риски сохранять.

Добавь флаги включения и отключения.

## Этап 7. Graphify

Сначала изучи реальный исходник.

Определи:

- точную установку;
- зависимости;
- команды;
- выходные файлы;
- hooks;
- конфигурацию;
- обновление;
- удаление;
- лицензию.

Создай:

```text
dist/integrations/graphify/
├── install.sh
├── run.sh
├── update.sh
├── doctor.sh
├── uninstall.sh
├── adapter.json
└── default.graphifyignore
```

Также создай Skill-обёртку.

Правила:

- Graphify помогает навигации;
- вывод подтверждается реальным кодом;
- проверяется актуальность;
- интеграция опциональна;
- отсутствие Graphify не ломает core;
- hooks требуют явного согласия;
- предусмотрен Codespaces rebuild.

## Этап 8. Профили

Создай:

```text
dist/profiles/minimal.yaml
dist/profiles/standard.yaml
dist/profiles/full.yaml
```

Minimal:

- core;
- explorer;
- planner;
- reviewer;
- tester;
- основные Skills;
- Caveman;
- Graphify optional.

Standard:

- Minimal;
- implementer;
- debugger;
- architect;
- security reviewer;
- расширенные Skills;
- Graphify default, только если совместим.

Full:

- все проверенные компоненты;
- не включать непроверенные.

## Этап 9. Установщик

Создай:

```text
dist/install.sh
dist/update.sh
dist/uninstall.sh
dist/verify.sh
dist/doctor.sh
```

Требования:

- `set -Eeuo pipefail`;
- safe quoting;
- dry-run;
- backup;
- idempotency;
- управляемые блоки AGENTS.md;
- state manifest;
- точный uninstall;
- понятные ошибки;
- non-interactive;
- verbose;
- логирование без секретов.

Поддержи:

```text
--target
--profile
--mode
--with-graphify
--without-graphify
--with-caveman
--without-caveman
--dry-run
--backup
--force
--non-interactive
--verbose
```

## Этап 10. Codespaces

Не перезаписывай `.devcontainer.json`.

Создай:

```text
dist/templates/devcontainer-snippet.json
dist/scripts/restore-tools.sh
```

Покажи пользователю точный ручной способ подключения.

## Этап 11. Лицензии

Создай:

```text
dist/licenses/THIRD_PARTY_NOTICES.md
dist/licenses/source-licenses/
```

Не включай компонент, если право перераспространения не подтверждено.

## Этап 12. Тесты

Проверь:

- clean install;
- existing AGENTS.md;
- repeated install;
- update;
- uninstall;
- profiles;
- with/without Graphify;
- with/without Caveman;
- missing dependencies;
- conflicts;
- state manifest;
- backup restore;
- Codespaces restore.

Создай:

```text
build/reports/test-report.md
```

## Этап 13. Релиз

После успешных тестов создай:

```text
release/codex-powerpack-X.Y.Z.zip
release/codex-powerpack-X.Y.Z.sha256
release/codex-powerpack-X.Y.Z-manifest.json
release/codex-powerpack-X.Y.Z-test-report.md
```

Не включай:

- `.git`;
- `.env`;
- секреты;
- caches;
- временные файлы;
- непроверенные hooks;
- исходники без разрешения на перераспространение.

## Итоговый отчёт

Укажи:

- что включено;
- что исключено;
- причины исключения;
- тесты;
- оставшиеся риски;
- команду установки;
- команду проверки;
- команду удаления;
- путь к архиву.
