#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil
from datetime import datetime, timezone
from pathlib import Path
BEGIN="<!-- CODEX-POWERPACK:BEGIN graphify -->"; END="<!-- CODEX-POWERPACK:END graphify -->"; MARKER=".codex-powerpack-managed"
def strip(text):
    s=text.find(BEGIN)
    if s<0:return text.rstrip()
    e=text.find(END,s)
    if e<0:raise ValueError("incomplete Graphify AGENTS block")
    return (text[:s].rstrip()+"\n\n"+text[e+len(END):].lstrip()).strip()
def main():
    p=argparse.ArgumentParser(); p.add_argument("action",choices=["install","uninstall"]); p.add_argument("--target",required=True); p.add_argument("--root",required=True); p.add_argument("--backup",action="store_true"); p.add_argument("--clear-output",action="store_true"); a=p.parse_args(); target=Path(a.target).resolve(); root=Path(a.root).resolve(); skill=target/".agents/skills/graphify"; agents=target/"AGENTS.md"; state=target/".codex-powerpack/state/graphify.json"
    if a.action=="install":
        if skill.exists() and not (skill/MARKER).exists(): raise SystemExit(f"ERROR: unmanaged Graphify Skill exists: {skill}")
        if skill.exists():shutil.rmtree(skill)
        shutil.copytree(root/"dist/skills/generated/graphify",skill); (skill/MARKER).write_text("managed by codex-powerpack\n")
        old=agents.read_text("utf-8") if agents.exists() else ""
        if a.backup and agents.exists(): shutil.copy2(agents,agents.with_name(agents.name+".graphify-backup"))
        fragment=(root/"dist/integrations/graphify/AGENTS.fragment.md").read_text().strip(); clean=strip(old); agents.write_text(clean+("\n\n" if clean else "")+fragment+"\n","utf-8")
        state.parent.mkdir(parents=True,exist_ok=True); state.write_text(json.dumps({"schema_version":1,"integration":"graphify","enabled":True,"hooks":False,"watcher":False,"skill_path":str(skill),"agents_path":str(agents),"output_path":str(target/"graphify-out"),"installed_at":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},indent=2)+"\n")
    else:
        if (skill/MARKER).exists():shutil.rmtree(skill)
        if agents.exists():
            clean=strip(agents.read_text("utf-8")); agents.write_text(clean+"\n","utf-8") if clean else agents.unlink()
        if state.exists():state.unlink()
        if a.clear_output and (target/"graphify-out").exists():shutil.rmtree(target/"graphify-out")
if __name__=="__main__":main()
