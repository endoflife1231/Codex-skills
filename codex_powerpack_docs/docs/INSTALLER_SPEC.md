# Спецификация установщика

## Файлы

```text
install.sh
update.sh
uninstall.sh
verify.sh
doctor.sh
```

## Требования

- `set -Eeuo pipefail`;
- safe quoting;
- dry-run;
- backup;
- идемпотентность;
- управляемые блоки;
- state manifest;
- точное удаление;
- понятные ошибки;
- отсутствие `curl | sh`;
- отсутствие опасных wildcard;
- режим non-interactive;
- лог действий.

## Параметры

```text
--target PATH
--profile minimal|standard|full
--mode project|user
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

## install.sh

1. Preflight.
2. Инвентаризация существующих файлов.
3. Проверка зависимостей.
4. План изменений.
5. Backup.
6. Копирование компонентов.
7. Merge AGENTS.md.
8. Установка Graphify.
9. State manifest.
10. Verify.

## update.sh

- читает state;
- создаёт backup;
- обновляет управляемые файлы;
- не трогает пользовательские;
- записывает конфликты;
- повторно проверяет систему.

## uninstall.sh

- удаляет только файлы из state;
- удаляет только управляемые блоки;
- не удаляет пользовательские файлы;
- внешние зависимости удаляет только отдельным флагом.

## doctor.sh

Формат:

```text
OK
WARNING
ERROR
SUGGESTED FIX
```
