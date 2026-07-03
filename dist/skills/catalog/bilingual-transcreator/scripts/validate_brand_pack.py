#!/usr/bin/env python3
"""Validate that a Bilingual Transcreator brand pack exists and has basic content."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

REQUIRED = {
    "BRAND_CONTEXT.md": ["Audience", "Positioning", "Claim"],
    "VOICE_RU.md": ["голос", "Словарь", "пример"],
    "VOICE_EN.md": ["Voice", "Diction", "example"],
}
GLOSSARY_NAMES = ("GLOSSARY.csv", "GLOSSARY.md")
PLACEHOLDER_MARKERS = (
    "- Brand:",
    "- Бренд:",
    "> \n",
    "- Who is speaking:",
    "- Кто говорит:",
)


def validate_markdown(path: Path, required_terms: list[str]) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if len(text.strip()) < 300:
        errors.append(f"{path.name}: file is too short to guide the skill")
    lowered = text.casefold()
    for term in required_terms:
        if term.casefold() not in lowered:
            errors.append(f"{path.name}: missing expected section or concept: {term}")
    placeholder_hits = sum(marker in text for marker in PLACEHOLDER_MARKERS)
    if placeholder_hits >= 2:
        errors.append(f"{path.name}: appears to contain unfilled template placeholders")
    return errors


def validate_glossary(path: Path) -> list[str]:
    errors: list[str] = []
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        required = {"source_term", "approved_target_term", "status"}
        headers = set(rows[0].keys()) if rows else set()
        missing = required - headers
        if missing:
            errors.append(f"{path.name}: missing columns: {', '.join(sorted(missing))}")
        if not rows:
            errors.append(f"{path.name}: glossary has no entries")
    elif len(path.read_text(encoding="utf-8").strip()) < 80:
        errors.append(f"{path.name}: glossary appears empty")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", nargs="?", default=".", help="Project directory")
    args = parser.parse_args()
    project = Path(args.project).resolve()

    errors: list[str] = []
    for name, terms in REQUIRED.items():
        path = project / name
        if not path.exists():
            errors.append(f"Missing {name}")
        else:
            errors.extend(validate_markdown(path, terms))

    glossary = next((project / name for name in GLOSSARY_NAMES if (project / name).exists()), None)
    if glossary is None:
        errors.append("Missing GLOSSARY.csv or GLOSSARY.md")
    else:
        errors.extend(validate_glossary(glossary))

    if errors:
        print("Brand pack needs attention:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Brand pack passed the structural checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
