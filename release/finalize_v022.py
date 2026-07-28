#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "0.2.1"
NEW = "0.2.2"
DATE = "2026-07-28"


def replace_versions(path: Path) -> None:
    try:
        text = path.read_text("utf-8")
    except (UnicodeDecodeError, OSError):
        return
    updated = text.replace(f"v{OLD}", f"v{NEW}").replace(OLD, NEW)
    if updated != text:
        path.write_text(updated, "utf-8")


def prepend_changelog(path: Path, title: str, section: str) -> None:
    if path.exists():
        text = path.read_text("utf-8")
    else:
        text = title + "\n\n"
    if "## [0.2.2]" in text:
        return
    first_break = text.find("\n\n")
    if first_break < 0:
        text = title + "\n\n" + section + text
    else:
        text = text[: first_break + 2] + section + text[first_break + 2 :]
    path.write_text(text, "utf-8")


def main() -> None:
    (ROOT / "VERSION").write_text(NEW + "\n", "utf-8")

    selected_roots = [
        ROOT / "docs",
        ROOT / "release",
        ROOT / "dist" / "docs",
        ROOT / "dist" / "install",
        ROOT / "dist" / "onboarding",
        ROOT / "dist" / "integrations",
        ROOT / "dist" / "manifests",
        ROOT / "dist" / "licenses",
        ROOT / "dist" / "skills",
        ROOT / "dist" / "agents",
        ROOT / "dist" / "core",
    ]
    root_files = [
        "README.md",
        "README.ru.md",
        "CITATION.cff",
        "OPEN_SOURCE_AUDIT.md",
        "OPEN_SOURCE_AUDIT.ru.md",
        "SECURITY.md",
        "SECURITY.ru.md",
        "SUPPORT.md",
        "SUPPORT.ru.md",
        "CONTRIBUTING.md",
        "CONTRIBUTING.ru.md",
        "CODE_OF_CONDUCT.md",
        "CODE_OF_CONDUCT.ru.md",
        "THIRD_PARTY_NOTICES.md",
        "THIRD_PARTY_NOTICES.ru.md",
    ]
    for name in root_files:
        path = ROOT / name
        if path.is_file():
            replace_versions(path)

    suffixes = {".md", ".json", ".yaml", ".yml", ".cff", ".py", ".sh", ".txt"}
    for base in selected_roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel.startswith("dist/skills/catalog/") or rel.startswith("dist/skills/generated/"):
                continue
            if path.name in {"CHANGELOG.md", "CHANGELOG.ru.md"}:
                continue
            replace_versions(path)

    citation = ROOT / "CITATION.cff"
    if citation.exists():
        text = citation.read_text("utf-8")
        text = re.sub(r"^date-released:.*$", f'date-released: "{DATE}"', text, flags=re.M)
        citation.write_text(text, "utf-8")

    prepend_changelog(
        ROOT / "CHANGELOG.md",
        "# Changelog",
        f"""## [0.2.2] - {DATE}\n\n"
        "- Replaced the failed fragmented-payload deployment with direct repository finalization.\n"
        "- Removed temporary payload, trigger, diagnostic, and one-time workflow files.\n"
        "- Synchronized current release references, citation metadata, manifests, and documentation.\n"
        "- Added automated release-consistency validation.\n"
        "- Rebuilt and validated the user and repository archives before publication.\n\n""",
    )
    prepend_changelog(
        ROOT / "CHANGELOG.ru.md",
        "# История изменений",
        f"""## [0.2.2] — {DATE}\n\n"
        "- Публикация через повреждённый фрагментированный payload заменена прямой финализацией.\n"
        "- Удалены временные части, триггеры, диагностические файлы и одноразовые workflows.\n"
        "- Синхронизированы версия, метаданные цитирования, манифесты и документация.\n"
        "- Добавлена автоматическая проверка согласованности релиза.\n"
        "- Пользовательский и репозиторный архивы пересобраны и проверены.\n\n""",
    )

    (ROOT / "SECURITY.ru.md").write_text(
        "# Политика безопасности\n\n"
        "Не публикуйте сведения об уязвимостях в открытых issues. Используйте приватное сообщение об уязвимости GitHub, когда функция доступна. Укажите затронутую версию, шаги воспроизведения, последствия и возможное исправление. Не прикладывайте секреты, персональные данные или материалы закрытых репозиториев.\n\n"
        "Поддерживаемая версия — последний опубликованный релиз. Исправления для старых веток выпускаются только при отдельном объявлении сопровождающего.\n",
        "utf-8",
    )
    (ROOT / "SUPPORT.ru.md").write_text(
        "# Поддержка\n\n"
        "Для проблем установки, пробелов в документации и запросов функций используйте GitHub Discussions или issues. Укажите операционную систему, версии Python и Codex CLI, выбранный профиль, выполненную команду и полный вывод ошибки без секретов.\n\n"
        "Сообщения об уязвимостях должны отправляться приватно.\n",
        "utf-8",
    )
    (ROOT / "CONTRIBUTING.ru.md").write_text(
        "# Участие в разработке\n\n"
        "1. Создайте отдельную ветку.\n"
        "2. Не добавляйте сторонний компонент без подтверждённой лицензии и уведомления об авторстве.\n"
        "3. Обновляйте английскую и русскую пользовательскую документацию одновременно.\n"
        "4. Перед pull request выполните проверки дистрибутива, окружения и сборки релиза.\n"
        "5. Опишите изменение, риски, проверку и происхождение сторонних материалов.\n",
        "utf-8",
    )
    (ROOT / "CODE_OF_CONDUCT.ru.md").write_text(
        "# Кодекс поведения\n\n"
        "Участники должны общаться профессионально, обсуждать работу, а не личные качества, и не допускать оскорблений, дискриминации, преследования или публикации чужих персональных данных. Сопровождающий вправе удалять материалы и ограничивать участие при нарушении этих правил.\n",
        "utf-8",
    )

    release_notes = ROOT / "release" / "release_notes.md"
    release_notes.write_text(
        f"# Codex Powerpack v{NEW}\n\n"
        "This patch release finalizes the audited 249-skill distribution after the failed temporary payload workflow.\n\n"
        "## Included\n\n"
        "- 8 Codex agents\n- 249 license-audited skills\n"
        "- user and repository ZIP archives\n- SHA-256 checksums and manifests\n"
        "- synchronized English and Russian user documentation\n\n"
        "## Fixes\n\n"
        "- removed corrupted payload fragments and one-time triggers;\n"
        "- synchronized current version references and citation metadata;\n"
        "- added release-consistency validation;\n"
        "- rebuilt and validated both release packages.\n",
        "utf-8",
    )
    (ROOT / "release" / "release_notes.ru.md").write_text(
        f"# Codex Powerpack v{NEW}\n\n"
        "Patch-релиз завершает публикацию проверенного набора из 249 навыков после сбоя временного payload-workflow.\n\n"
        "## Состав\n\n"
        "- 8 Codex-агентов;\n- 249 навыков с проверенными условиями распространения;\n"
        "- пользовательский и репозиторный ZIP-архивы;\n- SHA-256 и манифесты.\n\n"
        "## Исправления\n\n"
        "- удалены повреждённые части payload и одноразовые триггеры;\n"
        "- синхронизированы версия и метаданные;\n"
        "- добавлена проверка согласованности релиза;\n"
        "- оба релизных пакета пересобраны и проверены.\n",
        "utf-8",
    )

    checker = ROOT / "release" / "check_release_consistency.py"
    checker.write_text(
        '''#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
version = (ROOT / "VERSION").read_text("utf-8").strip()
errors: list[str] = []

required = [
    "README.md", "README.ru.md", "CITATION.cff", "OPEN_SOURCE_AUDIT.md",
    "release/README.md", "release/release_notes.md", "dist/docs/README.md",
]
for rel in required:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing {rel}")
    elif version not in path.read_text("utf-8"):
        errors.append(f"{rel} does not reference current version {version}")

for path in (ROOT / "dist" / "manifests").glob("*.json"):
    try:
        data = json.loads(path.read_text("utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)} invalid JSON: {exc}")
        continue
    declared = data.get("version")
    if declared is not None and str(declared) != version:
        errors.append(f"{path.relative_to(ROOT)} version {declared} != {version}")

summary_path = ROOT / "dist" / "manifests" / "distribution-summary.json"
if summary_path.is_file():
    counts = json.loads(summary_path.read_text("utf-8")).get("counts", {})
    for key, value in {"agents": 8, "skills": 249, "excluded_unlicensed_skills": 5}.items():
        if counts.get(key) != value:
            errors.append(f"distribution count {key}={counts.get(key)} != {value}")

for rel in [
    ".release-payload", ".v022-release-trigger", ".v022-diagnose-trigger",
    ".v022-finalize-trigger", "v022-diagnostic.txt",
    ".github/workflows/apply-v022.yml", ".github/workflows/diagnose-v022.yml",
    ".github/workflows/finalize-v022.yml",
]:
    if (ROOT / rel).exists():
        errors.append(f"temporary release artifact remains: {rel}")

if errors:
    for error in errors:
        print(f"[error] {error}")
    raise SystemExit(1)
print(f"[ok] release consistency: v{version}, 8 agents, 249 skills")
''',
        "utf-8",
    )

    (ROOT / ".github" / "workflows" / "validate.yml").write_text(
        '''name: Validate

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Check release consistency
        run: python3 release/check_release_consistency.py
      - name: Validate distribution
        run: python3 dist/verify/validate_dist.py
      - name: Run doctor
        run: bash dist/verify/doctor.sh
      - name: Test package build
        run: bash release/build_release.sh
''',
        "utf-8",
    )

    for rel in [
        ".release-payload",
        ".v022-release-trigger",
        ".v022-diagnose-trigger",
        ".v022-finalize-trigger",
        "v022-diagnostic.txt",
        ".github/workflows/apply-v022.yml",
        ".github/workflows/diagnose-v022.yml",
        ".github/workflows/finalize-v022.yml",
    ]:
        path = ROOT / rel
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()

    print(f"finalized repository metadata for v{NEW}")


if __name__ == "__main__":
    main()
