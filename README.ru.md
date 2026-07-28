# Codex Powerpack

[English](README.md) · [Лицензия](LICENSE) · [Сторонние лицензии](THIRD_PARTY_NOTICES.md)

Codex Powerpack — открытый дистрибутив для проектного подключения Codex: agents, skills, профили, адаптация проекта, проверка, установка, обновление, удаление и откат.

## Требования

- Linux, macOS или Windows через WSL
- Bash
- Python 3.10+
- Codex CLI для обычной работы с Codex
- Опционально: Graphify CLI и бинарный файл Codebase Memory

## Быстрый старт

```bash
unzip codex-powerpack-v0.2.2-user.zip
cd codex-powerpack-v0.2.2
./verify.sh
./install.sh --target /path/to/project --profile minimal
```

`minimal` — наиболее безопасный offline-first профиль. Рекомендуемый расширенный вариант:

```bash
./install.sh --target /path/to/project --profile standard --without-codebase-memory
```

Установка с анализом проекта:

```bash
./adapt-project.sh --target /path/to/project --mode guided
./adapt-project.sh --target /path/to/project --mode guided --apply
```

Откат или удаление:

```bash
./rollback.sh --target /path/to/project
./uninstall.sh --target /path/to/project
```

## Профили

- `minimal` — небольшой и консервативный offline-first набор
- `standard` — сбалансированный набор для большинства проектов
- `full` — все навыки, прошедшие проверку лицензий

## Два типа пакетов

- **User release:** только рабочие файлы, пользовательская документация, команды запуска, манифесты, лицензии и checksums.
- **Repository source:** user release плюс документация для сопровождения, GitHub-шаблоны, CI, сборщик релизов и метаданные проекта.

## Безопасность и интеграции

- `guided` сначала создаёт проверяемый план и только потом применяет изменения.
- Rollback восстанавливает состояние проекта до установки.
- Codebase Memory может потребовать разрешённую загрузку либо локальный проверенный бинарный файл.
- Graphify остаётся опциональным и не устанавливается через небезопасные конвейеры.

## Структура репозитория

- `dist/` — рабочий дистрибутив
- `release/` — сборщик и release notes
- `.github/` — CI и выпуск релизов
- `docs/` — документация сопровождающего

## Проверка

```bash
python3 dist/verify/validate_dist.py
bash dist/verify/doctor.sh
bash release/doctor_release.sh
```

## Документация

- [Обзор дистрибутива](dist/docs/README.md)
- [Архитектура](dist/docs/ARCHITECTURE.md)
- [Адаптация проекта](dist/docs/PROJECT_ADAPTATION.md)
- [Установка](dist/install/README.md)
- [Onboarding](dist/onboarding/README.md)
- [Аудит open source](OPEN_SOURCE_AUDIT.md)
- [Настройка репозитория](docs/REPOSITORY_SETUP.md)

## Статус open source

Собственные материалы распространяются по MIT. Сторонние компоненты сохраняют свои лицензии и уведомления. Навыки включаются только при сохранённом подтверждении права распространения. Пять спорных навыков пока исключены; подробности — в [OPEN_SOURCE_AUDIT.md](OPEN_SOURCE_AUDIT.md).
