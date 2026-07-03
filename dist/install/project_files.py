#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

BEGIN = "<!-- CODEX-POWERPACK:BEGIN core -->"
END = "<!-- CODEX-POWERPACK:END core -->"
MARKER = ".codex-powerpack-managed"


def profile_list(path: Path, section: str) -> list[str]:
    values: list[str] = []
    active = False
    for line in path.read_text("utf-8").splitlines():
        if line == f"{section}:":
            active = True
            continue
        if active and line.startswith("  - "):
            values.append(line[4:])
        elif active and line and not line.startswith(" "):
            break
    return values


def strip_block(text: str) -> str:
    start = text.find(BEGIN)
    if start < 0:
        return text.rstrip()
    end = text.find(END, start)
    if end < 0:
        raise ValueError("incomplete managed core block in AGENTS.md")
    return (text[:start].rstrip() + "\n\n" + text[end + len(END):].lstrip()).strip()


def backup(path: Path, root: Path, backups: list[str]) -> None:
    if not path.exists():
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    rel = path.name + f".powerpack-backup-{stamp}"
    dest = root / rel
    n = 1
    while dest.exists():
        dest = root / f"{rel}-{n}"; n += 1
    if path.is_dir(): shutil.copytree(path, dest)
    else: shutil.copy2(path, dest)
    backups.append(str(dest))


def copy_managed(src: Path, dest: Path, force: bool, backup_root: Path, backups: list[str]) -> None:
    if dest.exists():
        managed = (dest / MARKER).exists() if dest.is_dir() else False
        if not managed and not force:
            raise RuntimeError(f"refusing to replace unmanaged path: {dest}")
        if not managed: backup(dest, backup_root, backups)
        shutil.rmtree(dest) if dest.is_dir() else dest.unlink()
    shutil.copytree(src, dest)
    (dest / MARKER).write_text("managed by codex-powerpack\n", "utf-8")


def install(a: argparse.Namespace) -> int:
    root, target = Path(a.root).resolve(), Path(a.target).resolve()
    if a.plan:
        plan = json.loads(Path(a.plan).read_text("utf-8"))
        if Path(plan["project_root"]).resolve() != target:
            raise RuntimeError("plan project_root does not match target")
        skills = [x["id"] for x in plan["skills"]["always_on"] + plan["skills"]["selected"]]
        agents = [x["id"] for x in plan["agents"]["selected"]]
        profile_name = plan.get("resolved_profile", plan.get("profile", "auto"))
    else:
        profile = root / "dist/profiles" / f"{a.profile}.yaml"
        if not profile.exists(): raise RuntimeError(f"unknown profile: {a.profile}")
        skills, agents = profile_list(profile, "skills"), profile_list(profile, "agents")
        profile_name = a.profile
    state_dir = target / ".codex-powerpack/state"
    backup_root = target / ".codex-powerpack/backups"
    backups: list[str] = []
    if a.dry_run:
        print(json.dumps({"profile": profile_name, "skills": skills, "agents": agents}, indent=2)); return 0
    state_dir.mkdir(parents=True, exist_ok=True); backup_root.mkdir(parents=True, exist_ok=True)
    (target / ".agents/skills").mkdir(parents=True, exist_ok=True)
    (target / ".codex/agents").mkdir(parents=True, exist_ok=True)
    managed: list[str] = []
    registry = json.loads((root / "dist/skills/registry.json").read_text("utf-8"))
    by_name = {x["name"]: x for x in registry["skills"]}
    for name in skills:
        item = by_name.get(name)
        if not item: raise RuntimeError(f"profile references unregistered skill: {name}")
        src = root / item["install_source"]
        if not src.is_dir(): raise RuntimeError(f"install source missing for {name}: {src}")
        dest = target / ".agents/skills" / name
        copy_managed(src, dest, a.force, backup_root, backups); managed.append(str(dest))
    areg = json.loads((root / "dist/agents/registry.json").read_text("utf-8"))
    amap = {x["name"]: x for x in areg["agents"]}
    for name in agents:
        src = root / amap[name]["path"]
        dest = target / ".codex/agents" / f"{name}.toml"
        if dest.exists() and not a.force:
            # Reinstall is safe only when recorded in our previous receipt.
            old_state = state_dir / "install-state.json"
            old = json.loads(old_state.read_text()) if old_state.exists() else {}
            if str(dest) not in old.get("managed_files", []):
                raise RuntimeError(f"refusing to replace unmanaged agent: {dest}")
        elif dest.exists() and a.force: backup(dest, backup_root, backups)
        shutil.copy2(src, dest); managed.append(str(dest))
    core_copy = target / ".codex-powerpack/core/AGENTS.base.md"
    core_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "dist/core/AGENTS.base.md", core_copy); managed.append(str(core_copy))
    agents_md = target / "AGENTS.md"
    old = agents_md.read_text("utf-8") if agents_md.exists() else ""
    if a.backup: backup(agents_md, backup_root, backups)
    clean = strip_block(old)
    block = f"{BEGIN}\n" + (root / "dist/core/AGENTS.base.md").read_text("utf-8").strip() + f"\n{END}"
    agents_md.write_text(clean + ("\n\n" if clean else "") + block + "\n", "utf-8")
    managed.append(str(agents_md))
    receipt = {
      "schema_version": 1, "distribution": "codex-powerpack", "profile": profile_name,
      "skills": skills, "agents": agents, "managed_files": managed,
      "backup_paths": backups,
      "installed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    (state_dir / "install-state.json").write_text(json.dumps(receipt, indent=2) + "\n", "utf-8")
    return 0


def uninstall(a: argparse.Namespace) -> int:
    target = Path(a.target).resolve(); state = target / ".codex-powerpack/state/install-state.json"
    if not state.exists(): raise RuntimeError(f"install state missing: {state}")
    data = json.loads(state.read_text("utf-8"))
    if a.dry_run: print("\n".join(data.get("managed_files", []))); return 0
    for name in data.get("skills", []):
        p = target / ".agents/skills" / name
        if (p / MARKER).exists(): shutil.rmtree(p)
    for name in data.get("agents", []):
        p = target / ".codex/agents" / f"{name}.toml"
        if str(p) in data.get("managed_files", []) and p.exists(): p.unlink()
    agents = target / "AGENTS.md"
    if agents.exists():
        clean = strip_block(agents.read_text("utf-8"))
        if clean: agents.write_text(clean + "\n", "utf-8")
        else: agents.unlink()
    core = target / ".codex-powerpack/core"
    if core.exists(): shutil.rmtree(core)
    state.unlink()
    return 0


def main() -> int:
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="action", required=True)
    i = sub.add_parser("install"); i.add_argument("--root", required=True); i.add_argument("--target", required=True); i.add_argument("--profile", default="standard"); i.add_argument("--plan"); i.add_argument("--force", action="store_true"); i.add_argument("--backup", action="store_true"); i.add_argument("--dry-run", action="store_true")
    u = sub.add_parser("uninstall"); u.add_argument("--target", required=True); u.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    try: return install(a) if a.action == "install" else uninstall(a)
    except Exception as exc: print(f"ERROR: {exc}", file=sys.stderr); return 1

if __name__ == "__main__": raise SystemExit(main())
