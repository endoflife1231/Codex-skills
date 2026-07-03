# ПРОМПТ №1 — интеграция `codebase-memory-mcp-main` в мой Codex Powerpack

Ты работаешь как ведущий инженер по сборке, интеграции MCP, безопасности и Codex-native tooling.

Твоя задача: интегрировать локально предоставленный проект `codebase-memory-mcp-main` в мой уже собранный дистрибутив Codex Powerpack.

Это не новый дистрибутив с нуля. Это доработка существующего дистрибутива.

---

## 0. Что уже есть в моём дистрибутиве

Сначала найди реальный корень дистрибутива.

Не предполагай путь вслепую. Корнем дистрибутива считается каталог, внутри которого есть:

```text
dist/skills/registry.json
dist/agents/registry.json
dist/core/AGENTS.base.md
dist/profiles/minimal.yaml
dist/profiles/standard.yaml
dist/profiles/full.yaml
```

В моём текущем архиве уже есть:

```text
dist/skills/registry.json
dist/agents/registry.json
dist/core/AGENTS.base.md
dist/integrations/graphify/adapter.json
dist/profiles/minimal.yaml
dist/profiles/standard.yaml
dist/profiles/full.yaml
dist/install/install.sh
dist/install/update.sh
dist/install/uninstall.sh
dist/verify/validate_dist.py
dist/verify/doctor.sh
dist/licenses/THIRD_PARTY_NOTICES.md
dist/manifests/
```

Также уже есть 8 базовых Codex-агентов:

```text
explorer
planner
implementer
debugger
reviewer
tester
security-reviewer
architect
```

И большой Skill registry примерно на 252 Skills.

Текущий `dist/install/install.sh` может быть только проверочным stub-скриптом. Не считай его полноценным установщиком. Если он только запускает validate и печатает слои — его нужно аккуратно расширить до реального установщика, не ломая текущую проверку.

---

## 1. Источник для интеграции

Я положу исходник сюда:

```text
sources/codebase-memory-mcp-main/
```

Если каталог называется иначе, но явно содержит Codebase Memory MCP, сначала найди его по README, лицензии, manifest-файлам и исходникам.

Не редактируй исходник в `sources/codebase-memory-mcp-main/`.

Работай только в:

```text
dist/integrations/codebase-memory/
dist/skills/
dist/core/
dist/profiles/
dist/install/
dist/verify/
dist/docs/
dist/licenses/
dist/manifests/
build/reports/
tests/
```

---

## 2. Главная цель

После интеграции мой дистрибутив должен уметь устанавливать Codebase Memory MCP в любой проект как локальный project-scoped MCP-инструмент для Codex.

Желаемый пользовательский сценарий:

```bash
bash dist/install/install.sh \
  --target /workspaces/my-project \
  --profile standard \
  --with-codebase-memory
```

Или через будущий onboarding:

```bash
bash dist/onboarding/adapt-project.sh \
  --target /workspaces/my-project \
  --mode guided
```

После установки в конкретный проект должно появиться:

```text
<target>/.codex/config.toml
<target>/.codex-powerpack/
<target>/.codex-powerpack/tools/
<target>/.codex-powerpack/cache/codebase-memory/
<target>/.codex-powerpack/state/
```

Не нужен внешний сервер в интернете. MCP-сервер должен запускаться локально внутри проекта, Codespace или локальной машины.

---

## 3. Что такое Codebase Memory MCP в этой интеграции

Codebase Memory MCP должен быть основным инструментом для понимания кода:

- поиск функций, классов, методов и символов;
- анализ импортов;
- анализ вызовов;
- impact analysis;
- работа с git diff;
- поиск архитектурных связей;
- быстрый обзор структуры кода;
- помощь Codex перед изменением файлов.

Он не должен заменять чтение реальных исходников.

Правило:

```text
MCP помогает найти и понять связи.
Исходный код, тесты и реальные файлы остаются источником истины.
```

---

## 4. Важные ограничения безопасности

### 4.1. Не запускай upstream installer вслепую

Не выполняй автоматически в моём дистрибутиве:

```bash
codebase-memory-mcp install
```

или любые upstream install-команды до аудита.

Сначала изучи, что именно upstream installer меняет:

- `.codex/config.toml`;
- `AGENTS.md`;
- Skills;
- hooks;
- пользовательский home;
- глобальные настройки;
- MCP-конфигурации других клиентов;
- индексы;
- бинарники;
- базы данных;
- shell-profile;
- network calls.

Если нужно протестировать upstream installer, делай это только в изолированной временной fixture-директории с отдельными `HOME`, `CODEX_HOME`, `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`.

### 4.2. Не используй `curl | sh`

Запрещено:

```bash
curl URL | sh
wget -O- URL | bash
```

Разрешённый процесс:

1. скачать файл;
2. проверить источник;
3. проверить платформу;
4. проверить SHA256;
5. распаковать;
6. проверить ожидаемый бинарный файл;
7. установить в управляемый каталог.

### 4.3. Не перезаписывай пользовательские настройки

Нельзя целиком заменять:

```text
.codex/config.toml
~/.codex/config.toml
AGENTS.md
.codex/AGENTS.md
```

Нужно:

- делать backup;
- использовать управляемые блоки;
- использовать TOML-aware merge;
- не создавать дубликаты MCP-серверов;
- сохранять пользовательский текст.

### 4.4. Не индексируй секреты

Исключай:

```text
.env
.env.*
*.pem
*.key
credentials*
secrets*
id_rsa*
```

Можно отметить факт наличия секретных файлов, но нельзя читать или индексировать их содержимое.

---

## 5. Этап 1 — аудит upstream

Сначала изучи:

```text
sources/codebase-memory-mcp-main/
```

Создай отчёт:

```text
build/reports/codebase-memory-audit.md
```

В отчёте укажи:

```text
SAFE TO REUSE
NEEDS ADAPTATION
DO NOT EXECUTE DIRECTLY
OPTIONAL
UNSUPPORTED OR UNCLEAR
```

Проверь:

- лицензию;
- README;
- release process;
- способ сборки;
- способ установки;
- имя бинарного файла;
- доступные CLI-команды;
- MCP server mode;
- supported OS;
- supported architectures;
- поддерживает ли один static binary;
- где хранится SQLite/index/cache;
- есть ли UI;
- есть ли watcher;
- есть ли auto-index;
- есть ли hooks;
- есть ли инструменты записи;
- какие network calls есть;
- какие shell-скрипты есть;
- какие файлы Codex он меняет;
- как удалить всё корректно;
- как проверить версию;
- как проверить работоспособность.

Не начинай реализацию, пока аудит не готов.

---

## 6. Этап 2 — новый модуль интеграции

Создай:

```text
dist/integrations/codebase-memory/
├── adapter.json
├── install.sh
├── configure.sh
├── index.sh
├── update.sh
├── verify.sh
├── doctor.sh
├── uninstall.sh
├── restore-tools.sh
├── AGENTS.fragment.md
├── config.template.toml
├── default.ignore
├── checksums.json
├── VERSION
└── README.md
```

Если текущий стиль дистрибутива использует более простые скрипты, всё равно создай эти роли или их прямые эквиваленты.

---

## 7. `adapter.json`

Создай реальный adapter manifest.

Минимальная структура:

```json
{
  "id": "codebase-memory",
  "name": "Codebase Memory MCP",
  "type": "mcp",
  "optional": true,
  "recommended": true,
  "source": "sources/codebase-memory-mcp-main",
  "upstream_url": "",
  "upstream_commit": "",
  "upstream_version": "",
  "license": "",
  "mcp_server_name": "codebase-memory",
  "default_scope": "project",
  "default_enabled": true,
  "default_auto_index": "auto",
  "default_ui": false,
  "managed_tool_dir": ".codex-powerpack/tools",
  "managed_cache_dir": ".codex-powerpack/cache/codebase-memory",
  "managed_state_dir": ".codex-powerpack/state",
  "profiles": {
    "minimal": "optional",
    "standard": "enabled",
    "full": "enabled"
  },
  "routing": {
    "use_for": [
      "code symbol search",
      "call graph",
      "imports",
      "dependency tracing",
      "impact analysis",
      "git diff analysis",
      "architecture of code"
    ],
    "do_not_use_for": [
      "PDF analysis",
      "image analysis",
      "broad documentation knowledge graph",
      "visual project maps"
    ]
  },
  "conflicts": [],
  "coexists_with": [
    "graphify",
    "caveman"
  ]
}
```

Заполни поля реальными данными после аудита.

---

## 8. `install.sh`

Скрипт должен:

1. принимать `--target`;
2. принимать `--scope project|user`, но project должен быть по умолчанию;
3. принимать `--auto-index on|off|auto`;
4. принимать `--ui`;
5. принимать `--dry-run`;
6. принимать `--backup`;
7. принимать `--force`;
8. определять ОС и архитектуру;
9. выбирать правильный binary/release/build;
10. проверять SHA256;
11. устанавливать бинарник в управляемый каталог проекта;
12. не менять `.codex/config.toml` напрямую без `configure.sh`;
13. создавать state manifest;
14. вызывать `verify.sh`.

Project mode по умолчанию:

```text
<target>/.codex-powerpack/tools/
<target>/.codex-powerpack/cache/codebase-memory/
<target>/.codex-powerpack/state/
<target>/.codex/config.toml
```

User mode сделать опциональным и не использовать по умолчанию.

---

## 9. `configure.sh`

Скрипт должен безопасно добавить MCP-конфигурацию для Codex.

Целевой файл в project mode:

```text
<target>/.codex/config.toml
```

Требования:

- создать `.codex/`, если её нет;
- создать config, если его нет;
- сохранить существующие настройки;
- не удалить другие MCP;
- не дублировать `[mcp_servers.codebase-memory]`;
- обновлять только управляемый блок/секцию;
- делать backup;
- проверять TOML настоящим TOML-парсером;
- при конфликте создать `.new` и показать diff;
- записать изменения в state manifest.

Не угадывай TOML-формат Codex. Посмотри текущую документацию/примеры в проекте или исходнике, затем используй подтверждённый формат.

Если точный формат MCP для Codex не подтверждён локально, создай понятный TODO/blocked report и не делай фальшивую интеграцию.

---

## 10. `index.sh`

Скрипт должен:

- запускать первичную индексацию проекта;
- уметь incremental update;
- уметь force rebuild;
- использовать exclude/ignore rules;
- не читать секреты;
- не индексировать зависимости и build output;
- сохранять лог;
- не падать без объяснения на неподдерживаемых языках;
- не запускаться автоматически в dry-run;
- не включать watcher без явного флага.

Исключения по умолчанию:

```text
.git/
node_modules/
vendor/
.venv/
venv/
dist/
build/
coverage/
.next/
target/
__pycache__/
.cache/
tmp/
temp/
.env
.env.*
*.pem
*.key
```

---

## 11. `doctor.sh` и `verify.sh`

`doctor.sh` должен давать понятный диагноз:

```text
OK
WARNING
ERROR
SUGGESTED FIX
```

Проверять:

- бинарник есть;
- версия совпадает;
- SHA256 совпадает;
- права запуска есть;
- `.codex/config.toml` валиден;
- MCP-секция есть;
- путь к binary существует;
- cache dir доступен;
- индекс создан или объяснено, почему нет;
- auto-index policy понятна;
- Graphify не конфликтует;
- Caveman не конфликтует;
- Codespaces restore готов.

`verify.sh` должен быть пригоден для CI и возвращать ненулевой exit code при критических ошибках.

---

## 12. `uninstall.sh`

Удаление должно быть точным.

Удалить:

- управляемую MCP-запись;
- управляемый binary;
- управляемый AGENTS-блок;
- управляемые generated files;
- restore-script, если он управляемый.

По умолчанию не удалять индекс/кэш без явного флага.

Добавь флаг:

```bash
--clear-cache
```

Нельзя удалять чужие файлы по wildcard.

---

## 13. `AGENTS.fragment.md`

Создай короткий фрагмент для управляемого блока:

```markdown
<!-- CODEX-POWERPACK:BEGIN codebase-memory -->
...
<!-- CODEX-POWERPACK:END codebase-memory -->
```

Смысл:

- использовать Codebase Memory MCP для первичного исследования кода;
- использовать для символов, вызовов, импортов, зависимостей, impact analysis, git diff;
- не считать индекс абсолютной истиной;
- перед редактированием читать реальные файлы;
- после крупных изменений обновлять индекс;
- при конфликте верить исходному коду и тестам;
- не читать секреты;
- не использовать MCP вместо проверки тестами.

Фрагмент не должен быть длинным.

---

## 14. Skill-обёртка

Создай Skill:

```text
dist/skills/generated/codebase-memory/SKILL.md
```

или другое место, если в текущем дистрибутиве уже есть принятый каталог для generated Skills.

Добавь запись в:

```text
dist/skills/registry.json
```

Требования к Skill:

- объясняет, когда использовать MCP;
- объясняет, когда не использовать MCP;
- объясняет маршрутизацию с Graphify;
- объясняет проверку по исходникам;
- объясняет обновление индекса;
- не дублирует весь upstream README;
- имеет `profiles: ["standard", "full"]`;
- имеет `tier: "integration"`;
- имеет dependency на integration `codebase-memory`.

Важно: если фактические Skill-директории в дистрибутиве сейчас не включены и есть только registry, сначала исправь проблему установки Skills в целом. Registry-only Skill нельзя считать установленным.

---

## 15. Общий реестр интеграций

Если нет:

```text
dist/integrations/registry.json
```

создай его.

Добавь две интеграции:

```text
codebase-memory
graphify
```

Для `graphify` используй уже существующий:

```text
dist/integrations/graphify/adapter.json
```

Для `codebase-memory` используй новый adapter.

---

## 16. Обновление профилей

Обнови:

```text
dist/profiles/minimal.yaml
dist/profiles/standard.yaml
dist/profiles/full.yaml
dist/manifests/profile-summary.json
```

Правила:

### Minimal

```text
codebase-memory: optional
graphify: optional
caveman: always
live-language: always
```

### Standard

```text
codebase-memory: enabled
graphify: auto
caveman: always
live-language: always
```

### Full

```text
codebase-memory: enabled
graphify: auto
caveman: always
live-language: always
```

Не включай UI Codebase Memory по умолчанию.

---

## 17. Обновление общего установщика

Обнови:

```text
dist/install/install.sh
dist/install/update.sh
dist/install/uninstall.sh
dist/verify/validate_dist.py
dist/verify/doctor.sh
```

Добавь флаги:

```text
--with-codebase-memory
--without-codebase-memory
--codebase-memory-mode project|user
--codebase-memory-auto-index on|off|auto
--codebase-memory-ui
--codebase-memory-clear-cache
```

Проверь совместимость с:

```text
--target
--profile
--dry-run
--backup
--force
--non-interactive
--verbose
```

Если текущий `install.sh` только проверочный, преврати его в реальный orchestrator:

1. parse args;
2. validate dist;
3. resolve target;
4. select profile;
5. create backup;
6. install core;
7. install selected agents;
8. install selected skills;
9. install always-on caveman;
10. install always-on live-language skills;
11. install integrations;
12. merge AGENTS.md;
13. write state;
14. run verify;
15. print report.

---

## 18. Обязательная совместимость с Caveman

В моём дистрибутиве уже есть Caveman-семейство:

```text
caveman
caveman-commit
caveman-compress
caveman-help
caveman-review
caveman-setup
caveman-stats
cavecrew
```

Codebase Memory должен сосуществовать с Caveman.

Caveman не должен сжимать:

- MCP tool output;
- stack traces;
- security findings;
- test failures;
- file paths;
- line numbers;
- команды;
- unresolved risks.

Caveman может сжимать итоговый пользовательский отчёт.

---

## 19. Совместимость с Graphify

Graphify уже есть как optional integration:

```text
dist/integrations/graphify/adapter.json
```

Не удаляй его.

Создай маршрутизацию:

### Codebase Memory MCP использовать для:

- кода;
- функций;
- классов;
- импортов;
- вызовов;
- API;
- git diff;
- impact analysis;
- архитектурных границ кода.

### Graphify использовать для:

- документации;
- Markdown;
- PDF;
- изображений;
- смысловых связей;
- визуальной карты;
- смешанных проектов.

Если установлены оба:

1. не задавать один и тот же вопрос обоим без причины;
2. не строить оба графа после каждого мелкого изменения;
3. Codebase Memory обновлять чаще;
4. Graphify обновлять реже и по отдельной политике;
5. при конфликте проверять исходные файлы.

---

## 20. Codespaces

Создай:

```text
dist/integrations/codebase-memory/restore-tools.sh
```

Он должен:

- проверять binary;
- восстанавливать binary после rebuild;
- проверять `.codex/config.toml`;
- не дублировать MCP;
- не перестраивать индекс без необходимости;
- выдавать понятный отчёт.

Не перезаписывай `.devcontainer.json`.

Создай snippet:

```text
dist/templates/devcontainer-codebase-memory-snippet.json
```

или добавь в существующий templates-каталог.

---

## 21. Лицензии

Добавь:

```text
dist/licenses/source-licenses/codebase-memory-mcp-LICENSE
```

и запись в:

```text
dist/licenses/THIRD_PARTY_NOTICES.md
```

Укажи:

- название;
- upstream URL;
- commit/tag;
- лицензию;
- включённые файлы;
- изменялись ли исходники;
- ставится ли binary отдельно;
- где хранится checksum.

---

## 22. State manifest

Расширь state manifest.

После установки Codebase Memory сохраняй:

```json
{
  "integration": "codebase-memory",
  "enabled": true,
  "version": "",
  "commit": "",
  "binary_path": "",
  "binary_sha256": "",
  "mcp_scope": "project",
  "mcp_config_path": "",
  "mcp_server_name": "codebase-memory",
  "cache_path": "",
  "index_path": "",
  "auto_index": "auto",
  "ui_enabled": false,
  "managed_files": [],
  "managed_config_keys": [],
  "backup_paths": [],
  "installed_at": ""
}
```

Используй существующую структуру state, если она уже есть.

---

## 23. Тесты

Добавь тесты для:

1. clean install;
2. install over existing `.codex/config.toml`;
3. repeated install;
4. uninstall;
5. uninstall with cache preserved;
6. uninstall with `--clear-cache`;
7. dry-run;
8. unsupported architecture;
9. wrong checksum;
10. missing source;
11. missing network;
12. existing Graphify;
13. no Graphify;
14. existing Caveman Skills;
15. no duplicate AGENTS block;
16. valid TOML after merge;
17. `validate_dist.py`;
18. `doctor.sh`;
19. Codespaces restore;
20. release build.

Создай отчёт:

```text
build/reports/codebase-memory-test-report.md
```

---

## 24. Критерии готовности

Интеграция считается готовой, если:

- создан `dist/integrations/codebase-memory/`;
- добавлен adapter;
- добавлен Skill wrapper;
- обновлены профили;
- обновлён общий installer;
- обновлены verify/doctor;
- добавлены лицензии;
- добавлен state tracking;
- project-scoped MCP-конфигурация работает;
- повторная установка не создаёт дубликаты;
- uninstall точный;
- Graphify не сломан;
- Caveman не сломан;
- тесты прошли;
- итоговый релиз собирается.

---

## 25. Порядок работы

Работай строго так:

1. Найди реальный root дистрибутива.
2. Изучи текущие registry и профили.
3. Изучи текущие install/verify скрипты.
4. Изучи `sources/codebase-memory-mcp-main`.
5. Создай аудит.
6. Создай план интеграции.
7. Реализуй adapter.
8. Реализуй установку.
9. Реализуй configure MCP.
10. Реализуй index/doctor/uninstall.
11. Обнови registry/profiles/manifests.
12. Добавь Skill wrapper.
13. Добавь AGENTS fragment.
14. Добавь лицензии.
15. Добавь тесты.
16. Запусти проверки.
17. Исправь ошибки.
18. Собери релиз.
19. Дай финальный отчёт.

---

## 26. Финальный отчёт

В конце напиши:

- что было найдено в текущем дистрибутиве;
- что найдено в upstream Codebase Memory MCP;
- какие файлы созданы;
- какие файлы изменены;
- какие команды установки теперь доступны;
- где хранится binary;
- где хранится индекс;
- где находится MCP-конфигурация;
- как включить/отключить Codebase Memory;
- как он работает вместе с Graphify;
- как он работает вместе с Caveman;
- какие тесты прошли;
- что осталось вручную проверить;
- точную команду для установки в проект;
- точную команду для удаления из проекта.
