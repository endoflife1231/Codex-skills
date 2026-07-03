#!/usr/bin/env python3
"""Deep static validation for the 2026-07-03 Codex skill-pack integration."""
from __future__ import annotations

import ast
import json
import os
import re
import sys
import tomllib
from pathlib import Path

import yaml

PROJECT = Path(__file__).resolve().parents[2]
AGENTS = PROJECT / ".agents"
SKILLS = AGENTS / "skills"
MANIFEST = json.loads((AGENTS / "INTEGRATION_MANIFEST.json").read_text("utf-8"))
NEW = set(MANIFEST["new_skills"])
REGISTERED = {p.parent.name for p in SKILLS.glob("*/SKILL.md")}
ERRORS: list[str] = []
STATS: dict[str, int] = {}


def fail(message: str) -> None:
    ERRORS.append(message)


def imported_files(*suffixes: str):
    allowed = set(suffixes)
    for name in sorted(NEW):
        for path in (SKILLS / name).rglob("*"):
            if path.is_file() and (not allowed or path.suffix.lower() in allowed):
                yield path


# Registration, counts, and metadata.
if len(REGISTERED) != MANIFEST["total_skills"]:
    fail(f"expected {MANIFEST['total_skills']} registered skills, found {len(REGISTERED)}")
missing = sorted(NEW - REGISTERED)
if missing:
    fail(f"missing imported skills: {missing}")
if len(list((PROJECT / ".codex" / "agents").glob("*.toml"))) != MANIFEST["total_custom_agents"]:
    fail("custom-agent count does not match manifest")

for name in sorted(REGISTERED):
    skill = SKILLS / name / "SKILL.md"
    text = skill.read_text("utf-8", errors="replace")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not match:
        fail(f"{name}: missing YAML frontmatter")
        continue
    try:
        data = yaml.safe_load(match.group(1)) or {}
    except Exception as exc:
        fail(f"{name}: invalid frontmatter: {exc}")
        continue
    if data.get("name") != name:
        fail(f"{name}: frontmatter name is {data.get('name')!r}")
    if not str(data.get("description", "")).strip():
        fail(f"{name}: empty description")
    openai_yaml = SKILLS / name / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        fail(f"{name}: missing agents/openai.yaml")

# Parse machine-readable and executable text formats.
counts = {"python": 0, "json": 0, "yaml": 0, "toml": 0}
for path in PROJECT.rglob("*"):
    if not path.is_file():
        continue
    try:
        if path.suffix == ".py":
            ast.parse(path.read_text("utf-8")); counts["python"] += 1
        elif path.suffix == ".json":
            json.loads(path.read_text("utf-8")); counts["json"] += 1
        elif path.suffix in {".yaml", ".yml"}:
            yaml.safe_load(path.read_text("utf-8")); counts["yaml"] += 1
        elif path.suffix == ".toml":
            tomllib.loads(path.read_text("utf-8")); counts["toml"] += 1
    except Exception as exc:
        fail(f"{path.relative_to(PROJECT)}: parse failure: {exc}")
STATS.update(counts)

# No active source-platform instructions in imported behavior files.
legacy = re.compile(
    r"\.claude/|CLAUDE\.md|Claude Code|claude code|allowed-tools|\bTask tool\b|"
    r"^/content\b|^/seo\b|^/humanizer\b|~/\.claude|\.claude-plugin",
    re.M,
)
legacy_hits = 0
for path in imported_files(".md", ".yaml", ".yml", ".json", ".toml", ".py", ".sh", ".ps1"):
    if path.name.startswith("LICENSE") or path.name == "SOURCE.md":
        continue
    text = path.read_text("utf-8", errors="replace")
    if legacy.search(text):
        legacy_hits += 1
        fail(f"{path.relative_to(PROJECT)}: active source-platform marker remains")
STATS["legacy_marker_files"] = legacy_hits

# Validate local Markdown links in imported content and shared marketing registry.
link_re = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
link_checked = 0
link_roots = [SKILLS / name for name in NEW] + [AGENTS / "vendor" / "marketingskills", AGENTS / "CODEX_INTEGRATIONS.md"]
for base in link_roots:
    paths = [base] if base.is_file() else list(base.rglob("*.md"))
    for path in paths:
        for raw in link_re.findall(path.read_text("utf-8", errors="replace")):
            target = raw.strip().split()[0].strip("<>").split("#", 1)[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
                continue
            if any(char in target for char in "{}<>$"):
                continue
            if target in {"url", "link", "path/to/component", "path/to/another", "figmaUrl?node-id=X-Y"}:
                continue
            if target.startswith(("/", "around:", "SOUTH,")):
                continue
            link_checked += 1
            destination = PROJECT / target if target.startswith(".agents/") else path.parent / target
            if not destination.resolve().exists():
                fail(f"{path.relative_to(PROJECT)}: broken local link {raw!r}")
STATS["local_links"] = link_checked

# Direct skill references must resolve. Ignore shell variables and documented placeholders.
ignore_tokens = {"skill-name", "text", "id", "offset", "len", "mes", "off", "rep", "word"}
ref_re = re.compile(r"(?<![\w$])\$([a-z][a-z0-9-]{1,60})\b")
ref_checked = 0
ref_files = list(imported_files(".md", ".yaml", ".yml", ".json", ".toml")) + list((PROJECT / ".codex" / "agents").glob("*.toml"))
for path in ref_files:
    text = path.read_text("utf-8", errors="replace")
    for token in ref_re.findall(text):
        if token in ignore_tokens:
            continue
        ref_checked += 1
        if token not in REGISTERED:
            fail(f"{path.relative_to(PROJECT)}: references unregistered ${token}")
STATS["skill_references"] = ref_checked

# Credentialed/live integrations are explicit-only.
explicit = {
    "seo-ahrefs", "seo-bing", "seo-dataforseo", "seo-firecrawl", "seo-image-gen",
    "seo-profound", "seo-seranking", "seo-unlighthouse", "ru-textovod",
}
for name in explicit:
    path = SKILLS / name / "agents" / "openai.yaml"
    data = yaml.safe_load(path.read_text("utf-8")) or {}
    if data.get("policy", {}).get("allow_implicit_invocation") is not False:
        fail(f"{name}: live integration must be explicit-only")

# Core shared assets and Codex-native setup docs.
for relative in (
    ".agents/CODEX_INTEGRATIONS.md",
    ".agents/vendor/claude-seo/scripts",
    ".agents/vendor/marketingskills/tools/REGISTRY.md",
    ".agents/vendor/content-skills",
    ".agents/brand/README.md",
):
    if not (PROJECT / relative).exists():
        fail(f"missing required shared resource: {relative}")

if ERRORS:
    for item in ERRORS:
        print(f"ERROR: {item}")
    print(f"FAILED: {len(ERRORS)} integration validation error(s)")
    raise SystemExit(1)

print(
    "OK: deep integration validation passed — "
    f"{len(REGISTERED)} skills, {MANIFEST['total_custom_agents']} custom agents, "
    f"{STATS['local_links']} local links, {STATS['skill_references']} skill references"
)
print(json.dumps(STATS, sort_keys=True))
