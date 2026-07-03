#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"
ERRORS: list[str] = []


def require(path: Path, label: str) -> None:
    if not path.exists():
        ERRORS.append(f"missing {label}: {path.relative_to(ROOT)}")


require(DIST / "core" / "AGENTS.base.md", "core base")
for rel in [
    "core/references/README.md",
    "core/references/codex-adaptation.md",
    "core/references/safe-integrations.md",
    "core/references/agent-design.md",
    "core/references/source-policy-map.md",
    "core/references/communication-style.md",
    "core/references/editing-discipline.md",
    "core/references/tool-selection.md",
    "agents/registry.json",
    "skills/registry.json",
    "profiles/minimal.yaml",
    "profiles/standard.yaml",
    "profiles/full.yaml",
    "integrations/graphify/adapter.json",
    "integrations/codebase-memory/adapter.json",
    "integrations/codebase-memory/install.sh",
    "integrations/codebase-memory/configure.sh",
    "integrations/codebase-memory/index.sh",
    "integrations/codebase-memory/update.sh",
    "integrations/codebase-memory/verify.sh",
    "integrations/codebase-memory/doctor.sh",
    "integrations/codebase-memory/uninstall.sh",
    "integrations/codebase-memory/restore-tools.sh",
    "integrations/codebase-memory/AGENTS.fragment.md",
    "integrations/codebase-memory/checksums.json",
    "integrations/registry.json",
    "skills/generated/codebase-memory/SKILL.md",
    "templates/devcontainer-codebase-memory-snippet.json",
    "onboarding/adapt-project.sh",
    "onboarding/scan-project.py",
    "onboarding/analyze-project.sh",
    "onboarding/select-components.py",
    "onboarding/validate_json.py",
    "onboarding/generate-project-rules.py",
    "onboarding/apply-plan.sh",
    "onboarding/verify-adaptation.sh",
    "onboarding/rollback.sh",
    "onboarding/schemas/project-facts.schema.json",
    "onboarding/schemas/project-analysis.schema.json",
    "onboarding/schemas/adaptation-plan.schema.json",
    "onboarding/schemas/adaptation-state.schema.json",
    "onboarding/rules/detection-rules.yaml",
    "onboarding/rules/selection-rules.yaml",
    "onboarding/rules/always-on.yaml",
    "onboarding/rules/conflicts.yaml",
    "onboarding/rules/safety-rules.yaml",
    "onboarding/README.md",
    "docs/PROJECT_ADAPTATION.md",
    "verify/doctor.sh",
    "verify/README.md",
    "install/install.sh",
    "install/update.sh",
    "install/uninstall.sh",
    "docs/README.md",
    "docs/ARCHITECTURE.md",
    "docs/FINAL_STATUS.md",
    "licenses/THIRD_PARTY_NOTICES.md",
    "manifests/build-state.json",
    "manifests/profile-summary.json",
    "manifests/source-summary.json",
    "manifests/distribution-summary.json",
    "manifests/onboarding-summary.json",
]:
    require(DIST / rel, rel)

agent_registry_path = DIST / "agents" / "registry.json"
skill_registry_path = DIST / "skills" / "registry.json"
build_state_path = DIST / "manifests" / "build-state.json"

agent_count = 0
skill_count = 0

if agent_registry_path.exists():
    agent_registry = json.loads(agent_registry_path.read_text("utf-8"))
    agents = agent_registry.get("agents", [])
    agent_count = len(agents)
    for agent in agents:
        name = agent.get("name")
        path = ROOT / agent.get("path", "")
        if not path.exists():
            ERRORS.append(f"agent registry path missing for {name}: {path.relative_to(ROOT)}")
            continue
        try:
            parsed = tomllib.loads(path.read_text("utf-8"))
        except Exception as exc:
            ERRORS.append(f"{path.relative_to(ROOT)} TOML: {exc}")
            continue
        if parsed.get("name") != name:
            ERRORS.append(f"{path.relative_to(ROOT)} name mismatch: {parsed.get('name')} != {name}")
        writes = agent.get("writes")
        mode = parsed.get("sandbox_mode")
        if writes and mode != "workspace-write":
            ERRORS.append(f"{name}: expected workspace-write, got {mode}")
        if writes is False and mode != "read-only":
            ERRORS.append(f"{name}: expected read-only, got {mode}")

if skill_registry_path.exists():
    skill_registry = json.loads(skill_registry_path.read_text("utf-8"))
    skills = skill_registry.get("skills", [])
    skill_count = len(skills)
    seen: set[str] = set()
    for skill in skills:
        name = skill.get("name")
        if not isinstance(name, str) or not name:
            ERRORS.append("skill registry contains invalid name")
            continue
        if name in seen:
            ERRORS.append(f"duplicate skill in registry: {name}")
        seen.add(name)
        source = ROOT / skill.get("source", "")
        if (ROOT / "sources").exists() and not source.exists():
            ERRORS.append(f"skill source missing for {name}: {source.relative_to(ROOT)}")
        install_source = ROOT / skill.get("install_source", "")
        if not install_source.is_dir():
            ERRORS.append(f"skill install source missing for {name}: {install_source.relative_to(ROOT)}")
        elif not (install_source / "SKILL.md").is_file():
            ERRORS.append(f"skill install source has no SKILL.md for {name}")
        else:
            expected_hash = skill.get("hashes", {}).get("skill_md_sha256")
            actual_hash = hashlib.sha256((install_source / "SKILL.md").read_bytes()).hexdigest()
            if expected_hash != actual_hash:
                ERRORS.append(f"skill hash mismatch for {name}")

skill_names = {
    item.get("name") for item in
    (json.loads(skill_registry_path.read_text("utf-8")).get("skills", []) if skill_registry_path.exists() else [])
}

for profile_name, expected_agents in {
    "minimal": 3,
    "standard": 8,
    "full": 8,
}.items():
    profile = DIST / "profiles" / f"{profile_name}.yaml"
    if profile.exists():
        lines = profile.read_text("utf-8").splitlines()
        if not any(line.strip() == "core:" for line in lines):
            ERRORS.append(f"{profile.relative_to(ROOT)} missing core section")
        agent_lines = 0
        in_agents = False
        for line in lines:
            if line.strip() == "agents:":
                in_agents = True
                continue
            if in_agents and line.endswith(":") and not line.startswith("  - "):
                in_agents = False
            if in_agents and line.startswith("  - "):
                agent_lines += 1
        if agent_lines != expected_agents:
            ERRORS.append(f"{profile.relative_to(ROOT)} expected {expected_agents} agents, found {agent_lines}")
        in_skills = False
        profile_skills: list[str] = []
        for line in lines:
            if line.strip() == "skills:":
                in_skills = True
                continue
            if in_skills and line.startswith("  - "):
                profile_skills.append(line[4:])
            elif in_skills and line and not line.startswith(" "):
                in_skills = False
        for name in profile_skills:
            if name not in skill_names:
                ERRORS.append(f"{profile.relative_to(ROOT)} references unknown skill: {name}")
        for required_skill in ("caveman", "caveman-compress", "caveman-review", "caveman-stats"):
            if required_skill not in profile_skills:
                ERRORS.append(f"{profile.relative_to(ROOT)} missing always-on skill: {required_skill}")
        for required_live in ("humanizer", "humanizer-ru", "bilingual-transcreator", "copy-editing"):
            if required_live not in profile_skills:
                ERRORS.append(f"{profile.relative_to(ROOT)} missing live-language Skill: {required_live}")
        profile_text = "\n".join(lines)
        expected_policy = "optional" if profile_name == "minimal" else "enabled"
        if f"  codebase-memory: {expected_policy}" not in profile_text:
            ERRORS.append(f"{profile.relative_to(ROOT)} has wrong codebase-memory policy")

if build_state_path.exists():
    build_state = json.loads(build_state_path.read_text("utf-8"))
    if not isinstance(build_state.get("status"), dict):
        ERRORS.append("build-state.json missing status object")

source_summary_path = DIST / "manifests" / "source-summary.json"
if source_summary_path.exists():
    source_summary = json.loads(source_summary_path.read_text("utf-8"))
    if not isinstance(source_summary.get("policy"), dict):
        ERRORS.append("source-summary.json missing policy object")
    sources = source_summary.get("sources")
    if not isinstance(sources, list) or len(sources) < 5:
        ERRORS.append("source-summary.json missing expected source entries")

profile_summary_path = DIST / "manifests" / "profile-summary.json"
if profile_summary_path.exists():
    profile_summary = json.loads(profile_summary_path.read_text("utf-8"))
    if profile_summary.get("default_recommendation") != "standard":
        ERRORS.append("profile-summary.json default_recommendation should be 'standard'")

distribution_summary_path = DIST / "manifests" / "distribution-summary.json"
if distribution_summary_path.exists():
    distribution_summary = json.loads(distribution_summary_path.read_text("utf-8"))
    if not isinstance(distribution_summary.get("release_readiness"), dict):
        ERRORS.append("distribution-summary.json missing release_readiness object")
    if not isinstance(distribution_summary.get("tier_counts"), dict):
        ERRORS.append("distribution-summary.json missing tier_counts object")

if any(DIST.rglob("__pycache__")):
    ERRORS.append("dist contains __pycache__ artifacts")

integrations_registry = DIST / "integrations" / "registry.json"
if integrations_registry.exists():
    data = json.loads(integrations_registry.read_text("utf-8"))
    ids = {item.get("id") for item in data.get("integrations", [])}
    if ids != {"graphify", "codebase-memory"}:
        ERRORS.append(f"integration registry ids mismatch: {sorted(ids)}")

cbm_adapter = DIST / "integrations" / "codebase-memory" / "adapter.json"
if cbm_adapter.exists():
    adapter = json.loads(cbm_adapter.read_text("utf-8"))
    if adapter.get("default_scope") != "project":
        ERRORS.append("codebase-memory default scope must be project")
    if adapter.get("security", {}).get("upstream_installer_allowed") is not False:
        ERRORS.append("codebase-memory must prohibit the upstream broad installer")

for schema_path in sorted((DIST / "onboarding" / "schemas").glob("*.json")):
    try:
        schema = json.loads(schema_path.read_text("utf-8"))
        if schema.get("type") != "object" or not isinstance(schema.get("required"), list):
            ERRORS.append(f"onboarding schema lacks object/required contract: {schema_path.name}")
    except Exception as exc:
        ERRORS.append(f"invalid onboarding schema {schema_path.name}: {exc}")

always_on_path = DIST / "onboarding" / "rules" / "always-on.yaml"
if always_on_path.exists():
    rules = always_on_path.read_text("utf-8")
    for required in ("caveman", "live_language_core", "project_intelligence", "codebase-memory", "graphify"):
        if required not in rules:
            ERRORS.append(f"always-on rules missing: {required}")

for script in sorted((DIST / "onboarding").glob("*.sh")):
    if not script.stat().st_mode & 0o111:
        ERRORS.append(f"onboarding script is not executable: {script.name}")

if ERRORS:
    print("\n".join(f"ERROR: {e}" for e in ERRORS))
    sys.exit(1)

print(f"OK: dist validated ({agent_count} agents, {skill_count} skills)")
