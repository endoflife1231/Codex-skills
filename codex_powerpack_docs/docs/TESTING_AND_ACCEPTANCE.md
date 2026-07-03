# Тестирование и приёмка

## Обязательные сценарии

- чистая установка;
- существующий AGENTS.md;
- существующие агенты;
- существующие Skills;
- повторная установка;
- обновление;
- удаление;
- Minimal;
- Standard;
- Full;
- Graphify включён;
- Graphify отключён;
- Caveman включён;
- Caveman отключён;
- dry-run;
- missing dependency;
- Codespaces rebuild.

## Статические проверки

- shellcheck;
- TOML parser;
- JSON parser;
- YAML parser;
- Markdown links;
- duplicate names;
- permissions;
- hashes;
- secret scan;
- отсутствие `.git`;
- отсутствие caches.

## Критические критерии

- пользовательские файлы не теряются;
- uninstall не удаляет чужие файлы;
- AGENTS.md не дублируется;
- непроверенные hooks не запускаются;
- лицензии присутствуют;
- Graphify не обязателен для работы core;
- Caveman не удаляет критические данные.
