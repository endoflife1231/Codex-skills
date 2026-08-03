#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
version = (ROOT / "VERSION").read_text("utf-8").strip()
errors: list[str] = []

required = [
    "README.md", "README.ru.md", "CHANGELOG.md", "CHANGELOG.ru.md",
    "CITATION.cff", "OPEN_SOURCE_AUDIT.md", "release/README.md",
    "release/release_notes.md", "dist/docs/README.md",
]
for rel in required:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing {rel}")
    elif version not in path.read_text("utf-8"):
        errors.append(f"{rel} does not reference current version {version}")

for rel in ["CHANGELOG.md", "CHANGELOG.ru.md"]:
    text = (ROOT / rel).read_text("utf-8")
    match = re.search(
        rf"^## \[{re.escape(version)}\].*?(?=^## \[|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        errors.append(f"{rel} is missing a section for {version}")
        continue
    section = match.group(0)
    if len(re.findall(r"^- \S", section, flags=re.MULTILINE)) == 0:
        errors.append(f"{rel} release section has no Markdown bullet items")
    if any(line.strip() == '"' or line.lstrip().startswith('"- ') for line in section.splitlines()):
        errors.append(f"{rel} release section contains fragmented quoted payload text")

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
