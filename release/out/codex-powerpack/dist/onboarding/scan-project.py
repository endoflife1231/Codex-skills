#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import tomllib
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "vendor", ".venv", "venv", "dist", "build", "coverage", ".next", "target", "__pycache__", ".cache", ".codex-powerpack", ".agents", ".codex"}
SECRET_PATTERNS = [".env", ".env.*", "*.pem", "*.key", "*.p12", "*.pfx", "credentials*", "secrets*", "id_rsa*"]
SOURCE_EXT = {
    ".py": "Python", ".pyi": "Python", ".js": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".go": "Go", ".rs": "Rust",
    ".java": "Java", ".kt": "Kotlin", ".kts": "Kotlin", ".cs": "C#",
    ".c": "C", ".h": "C/C++", ".cc": "C++", ".cpp": "C++", ".hpp": "C++",
    ".php": "PHP", ".rb": "Ruby", ".swift": "Swift", ".dart": "Dart",
    ".vue": "Vue", ".svelte": "Svelte", ".sol": "Solidity", ".ex": "Elixir", ".exs": "Elixir"
}
DOC_EXT = {".md", ".mdx", ".rst", ".txt", ".adoc", ".pdf"}
MEDIA_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".mp4", ".mov", ".mp3", ".wav"}
MANIFEST_NAMES = {
    "package.json", "pnpm-workspace.yaml", "yarn.lock", "package-lock.json", "bun.lock", "bun.lockb",
    "pyproject.toml", "requirements.txt", "poetry.lock", "uv.lock", "Pipfile", "go.mod", "Cargo.toml",
    "pom.xml", "build.gradle", "build.gradle.kts", "composer.json", "Gemfile", "Dockerfile",
    "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml", "Makefile", "justfile",
    "Taskfile.yml", "tsconfig.json", "angular.json", "alembic.ini", "manage.py", "pytest.ini"
}


def secret(name: str) -> bool:
    low = name.lower()
    return any(fnmatch.fnmatch(low, pat.lower()) for pat in SECRET_PATTERNS)


def uniq(values):
    return sorted({str(x) for x in values if x})


def safe_json(path: Path) -> dict:
    if path.stat().st_size > 1_048_576: return {}
    try: return json.loads(path.read_text("utf-8"))
    except Exception: return {}


def safe_toml(path: Path) -> dict:
    if path.stat().st_size > 1_048_576: return {}
    try: return tomllib.loads(path.read_text("utf-8"))
    except Exception: return {}


def add_script_commands(commands: dict[str, list[str]], scripts: dict) -> None:
    # Commands are inventory-only untrusted strings; onboarding never executes them automatically.
    mapping = {"build": "build", "lint": "lint", "typecheck": "typecheck", "test": "test", "e2e": "e2e", "dev": "dev"}
    for key, dest in mapping.items():
        if key in scripts and isinstance(scripts[key], str): commands[dest].append(f"package-script:{key}")


def scan(root: Path) -> dict:
    root = root.resolve()
    files: list[Path] = []
    risks: list[str] = []
    secret_files = 0
    for base, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not Path(base, d).is_symlink())
        for name in sorted(names):
            p = Path(base, name)
            if p.is_symlink(): continue
            if secret(name): secret_files += 1; continue
            files.append(p)

    fingerprint = hashlib.sha256()
    for p in files:
        rel = p.relative_to(root).as_posix()
        try: st = p.stat()
        except OSError: continue
        fingerprint.update(f"{rel}\0{st.st_size}\0{st.st_mtime_ns}\n".encode())

    languages: list[str] = []; docs = media = source = 0
    manifests: list[str] = []; tree: list[str] = []
    source_roots: set[str] = set(); test_roots: set[str] = set(); doc_roots: set[str] = set(); generated_roots: set[str] = set()
    entry_points: list[str] = []; services: list[str] = []
    for p in files:
        rel = p.relative_to(root); rels = rel.as_posix(); suffix = p.suffix.lower()
        if len(tree) < 1000: tree.append(rels)
        if suffix in SOURCE_EXT:
            source += 1; languages.append(SOURCE_EXT[suffix])
            if rel.parts: source_roots.add(rel.parts[0] if len(rel.parts) > 1 else ".")
        if suffix in DOC_EXT or p.name.lower().startswith("readme"):
            docs += 1; doc_roots.add(rel.parts[0] if len(rel.parts) > 1 else ".")
        if suffix in MEDIA_EXT: media += 1
        low_parts = {x.lower() for x in rel.parts}
        if low_parts & {"test", "tests", "spec", "specs", "__tests__"}: test_roots.add(rel.parts[0])
        if low_parts & {"generated", "gen", "coverage"}: generated_roots.add(rel.parts[0])
        if p.name in MANIFEST_NAMES or re.match(r"^(next|vite|nuxt|vitest|jest|playwright)\.config\.", p.name): manifests.append(rels)
        if p.name in {"main.py", "app.py", "manage.py", "main.go", "main.rs", "index.ts", "index.js", "Program.cs"}: entry_points.append(rels)

    dependencies: list[str] = []; dev_dependencies: list[str] = []; frameworks: list[str] = []
    package_managers: list[str] = []; databases: list[str] = []; orms: list[str] = []
    testing: list[str] = []; linters: list[str] = []; type_checkers: list[str] = []; build_tools: list[str] = []
    ci: list[str] = []; containers: list[str] = []; infra: list[str] = []
    commands = {x: [] for x in ["install", "build", "lint", "typecheck", "test", "e2e", "dev"]}

    package = root / "package.json"
    if package.is_file():
        data = safe_json(package); deps = data.get("dependencies", {}); dev = data.get("devDependencies", {})
        if isinstance(deps, dict): dependencies += deps.keys()
        if isinstance(dev, dict): dev_dependencies += dev.keys()
        add_script_commands(commands, data.get("scripts", {}) if isinstance(data.get("scripts", {}), dict) else {})
        package_managers.append("npm"); commands["install"].append("npm-install")
        all_deps = set(dependencies + dev_dependencies)
        fmap = {"next":"Next.js", "react":"React", "vue":"Vue", "nuxt":"Nuxt", "@angular/core":"Angular", "svelte":"Svelte", "express":"Express", "fastify":"Fastify", "nestjs":"NestJS", "@nestjs/core":"NestJS"}
        frameworks += [v for k,v in fmap.items() if k in all_deps]
        testing += [x for x in ["jest","vitest","playwright","cypress"] if x in all_deps]
        linters += [x for x in ["eslint","biome"] if x in all_deps]
        type_checkers += ["TypeScript" for _ in [0] if "typescript" in all_deps]
        if "prisma" in all_deps or "@prisma/client" in all_deps: orms.append("Prisma")
        if "pg" in all_deps: databases.append("PostgreSQL")
    # Monorepos commonly keep package manifests below apps/ or packages/. Read only
    # bounded JSON manifests, never scripts as executable instructions.
    for nested in [p for p in files if p.name == "package.json" and p != package]:
        data=safe_json(nested); deps=data.get("dependencies",{}); dev=data.get("devDependencies",{})
        if isinstance(deps,dict): dependencies += deps.keys()
        if isinstance(dev,dict): dev_dependencies += dev.keys()
        all_nested=set(deps if isinstance(deps,dict) else [])|set(dev if isinstance(dev,dict) else [])
        fmap={"next":"Next.js","react":"React","vue":"Vue","nuxt":"Nuxt","@angular/core":"Angular","svelte":"Svelte","express":"Express","fastify":"Fastify","@nestjs/core":"NestJS"}
        frameworks += [v for k,v in fmap.items() if k in all_nested]
        testing += [x for x in ["jest","vitest","playwright","cypress"] if x in all_nested]
        if "prisma" in all_nested or "@prisma/client" in all_nested: orms.append("Prisma")
        if "pg" in all_nested: databases.append("PostgreSQL")
    for lock, pm in [("pnpm-lock.yaml","pnpm"),("pnpm-workspace.yaml","pnpm"),("yarn.lock","yarn"),("bun.lock","bun"),("bun.lockb","bun")]:
        if (root/lock).exists(): package_managers.append(pm)

    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        data = safe_toml(pyproject); package_managers.append("python")
        blob = json.dumps(data).lower()
        for token, label in [("django","Django"),("fastapi","FastAPI"),("flask","Flask")]:
            if token in blob: frameworks.append(label)
        for token in ["pytest","ruff","mypy","pyright","poetry"]:
            if token in blob:
                (testing if token=="pytest" else linters if token=="ruff" else type_checkers if token in {"mypy","pyright"} else package_managers).append(token)
        commands["install"].append("python-project-install")
    req = root / "requirements.txt"
    if req.is_file() and req.stat().st_size <= 1_048_576:
        for line in req.read_text("utf-8", errors="ignore").splitlines():
            if line.strip() and not line.lstrip().startswith(('#','-')):
                dependencies.append(re.split(r"[<>=!~\[]", line.strip())[0])
    if (root/"go.mod").is_file(): package_managers.append("go"); commands["build"].append("go-build"); commands["test"].append("go-test")
    cargo = root / "Cargo.toml"
    if cargo.is_file():
        package_managers.append("cargo"); commands["build"].append("cargo-build"); commands["test"].append("cargo-test")
        data=safe_toml(cargo); dependencies += (data.get("dependencies", {}) or {}).keys()
    if (root/"composer.json").is_file(): package_managers.append("composer")
    if (root/"pom.xml").is_file(): build_tools.append("Maven")
    if (root/"build.gradle").is_file() or (root/"build.gradle.kts").is_file(): build_tools.append("Gradle")
    if (root/"Makefile").is_file(): build_tools.append("Make")
    if (root/"Dockerfile").is_file(): containers.append("Docker")
    if any((root/x).is_file() for x in ["docker-compose.yml","docker-compose.yaml","compose.yml","compose.yaml"]): containers.append("Docker Compose")
    if (root/".github/workflows").is_dir(): ci.append("GitHub Actions")
    if (root/".gitlab-ci.yml").is_file(): ci.append("GitLab CI")
    for name,label in [("terraform","Terraform"),("k8s","Kubernetes"),("helm","Helm")]:
        if (root/name).is_dir(): infra.append(label)
    if (root/"prisma/schema.prisma").is_file(): orms.append("Prisma")
    if (root/"alembic.ini").is_file(): orms.append("Alembic")

    all_deps = {x.lower() for x in dependencies + dev_dependencies}
    if any(x in all_deps for x in {"postgres","postgresql","psycopg","psycopg2","pg"}): databases.append("PostgreSQL")
    if any(x in all_deps for x in {"mysql","mysql2","pymysql"}): databases.append("MySQL")
    if any(x in all_deps for x in {"sqlite","sqlite3"}): databases.append("SQLite")

    workspace_markers = [root/"pnpm-workspace.yaml", root/"lerna.json"]
    monorepo = any(x.exists() for x in workspace_markers) or sum(1 for p in root.glob("*/package.json")) >= 2
    for parent in ["apps", "packages", "services"]:
        d=root/parent
        if d.is_dir():
            services += [p.relative_to(root).as_posix() for p in d.iterdir() if p.is_dir()]
    project_type=[]
    if source: project_type.append("code")
    if docs >= max(10, source): project_type.append("documentation-heavy")
    if frameworks: project_type.append("web-application")
    if containers or infra: project_type.append("infrastructure")
    if not source and docs: project_type.append("documentation")
    if monorepo: project_type.append("monorepo")

    existing = {"agents_md": [], "config_toml": [], "skills": [], "agents": [], "mcp_servers": []}
    for candidate in [root/"AGENTS.md", root/".codex/AGENTS.md"]:
        if candidate.is_file(): existing["agents_md"].append(candidate.relative_to(root).as_posix())
    config = root/".codex/config.toml"
    if config.is_file():
        existing["config_toml"].append(".codex/config.toml")
        data=safe_toml(config); existing["mcp_servers"] = sorted((data.get("mcp_servers") or {}).keys()) if isinstance(data.get("mcp_servers"),dict) else []
    for d,key in [(root/".agents/skills","skills"),(root/".codex/agents","agents")]:
        if d.is_dir(): existing[key]=sorted(p.stem if p.is_file() else p.name for p in d.iterdir())
    if secret_files: risks.append(f"{secret_files} secret-pattern file(s) detected by name and excluded without reading")
    if any(commands.values()): risks.append("manifest commands are untrusted inventory and must not be executed automatically")
    if not source and not docs: risks.append("no supported source or documentation files detected")
    unknowns=[]
    if not commands["test"]: unknowns.append("test command not confirmed")
    if not frameworks and source: unknowns.append("framework not confirmed")

    return {
      "schema_version":1, "generated_at":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
      "project_root":str(root), "project_fingerprint":fingerprint.hexdigest(), "git_repository":(root/".git").exists(),
      "project_type":uniq(project_type), "languages":uniq(languages), "frameworks":uniq(frameworks),
      "package_managers":uniq(package_managers), "dependencies":uniq(dependencies), "dev_dependencies":uniq(dev_dependencies),
      "databases":uniq(databases), "orms":uniq(orms), "testing":uniq(testing), "linters":uniq(linters),
      "type_checkers":uniq(type_checkers), "build_tools":uniq(build_tools), "ci":uniq(ci), "containers":uniq(containers),
      "infrastructure":uniq(infra), "entry_points":uniq(entry_points), "source_roots":uniq(source_roots),
      "test_roots":uniq(test_roots), "documentation_roots":uniq(doc_roots), "generated_roots":uniq(generated_roots),
      "source_file_count":source, "total_file_count":len(files), "documentation_file_count":docs,
      "binary_or_media_count":media, "monorepo":monorepo, "services":uniq(services),
      "commands":{k:uniq(v) for k,v in commands.items()}, "existing_codex":existing,
      "manifest_files":uniq(manifests), "tree_summary":tree, "risks":risks, "unknowns":unknowns
    }


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--target", required=True); p.add_argument("--output"); p.add_argument("--stdout", action="store_true")
    a=p.parse_args(); root=Path(a.target)
    if not root.is_dir(): p.error("--target must be an existing directory")
    data=scan(root); text=json.dumps(data,indent=2,ensure_ascii=False)+"\n"
    if a.stdout: print(text,end="")
    else:
        out=Path(a.output) if a.output else root/".codex-powerpack/analysis/project-facts.json"
        out.parent.mkdir(parents=True,exist_ok=True); out.write_text(text,"utf-8"); print(out)
    return 0

if __name__=="__main__": raise SystemExit(main())
