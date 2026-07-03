#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, tomllib
from pathlib import Path

BLOCKS=["core","generated-project-profile","caveman","live-language","project-intelligence"]
def main():
    p=argparse.ArgumentParser(); p.add_argument("--root",required=True); p.add_argument("--target",required=True); p.add_argument("--plan",required=True); a=p.parse_args(); root=Path(a.root); target=Path(a.target); plan=json.loads(Path(a.plan).read_text()); errors=[]; warnings=[]
    sreg={x["name"]:x for x in json.loads((root/"dist/skills/registry.json").read_text())["skills"]}; areg={x["name"]:x for x in json.loads((root/"dist/agents/registry.json").read_text())["agents"]}
    skills=[x["id"] for x in plan["skills"]["always_on"]+plan["skills"]["selected"]]
    for name in skills:
        if name not in sreg: errors.append(f"unknown selected Skill: {name}"); continue
        if not (target/".agents/skills"/name/"SKILL.md").is_file(): errors.append(f"installed Skill missing SKILL.md: {name}")
    for required in ["caveman","caveman-compress","caveman-review","caveman-stats"]:
        if required not in skills: errors.append(f"always-on Caveman Skill missing: {required}")
    live=plan["always_on"]["live_language"]["skills"]
    if not live or any(x not in skills for x in live): errors.append("live-language-core incomplete")
    for row in plan["agents"]["selected"]:
        name=row["id"]; path=target/".codex/agents"/f"{name}.toml"
        if name not in areg or not path.is_file(): errors.append(f"selected agent missing: {name}"); continue
        data=tomllib.loads(path.read_text()); actual=data.get("sandbox_mode")=="workspace-write"
        if actual != bool(row.get("write_access")): errors.append(f"agent write access differs from plan: {name}")
    agents_md=target/"AGENTS.md"; text=agents_md.read_text("utf-8") if agents_md.exists() else ""
    for name in BLOCKS:
        if text.count(f"<!-- CODEX-POWERPACK:BEGIN {name} -->")!=1 or text.count(f"<!-- CODEX-POWERPACK:END {name} -->")!=1: errors.append(f"managed AGENTS block invalid: {name}")
    config=target/".codex/config.toml"
    if config.exists():
        try: tomllib.loads(config.read_text())
        except Exception as exc: errors.append(f"invalid Codex TOML: {exc}")
    integrations=plan["integrations"]; enabled=[x for x in ["codebase-memory","graphify"] if integrations[x]["decision"]=="enable"]
    if integrations["at_least_one_required"] and not enabled: errors.append("no project-intelligence integration enabled")
    if "codebase-memory" in enabled and not (target/".codex-powerpack/state/codebase-memory.json").is_file(): errors.append("Codebase Memory state missing")
    if "graphify" in enabled and not (target/".codex-powerpack/state/graphify.json").is_file(): errors.append("Graphify managed state missing")
    if "graphify" in enabled and not (target/"graphify-out/graph.json").is_file(): warnings.append("Graphify configured; graph has not been built explicitly yet")
    state=target/".codex-powerpack/state/adaptation-state.json"
    if not state.is_file(): errors.append("adaptation state missing")
    else:
        data=json.loads(state.read_text())
        if not Path(data.get("backup_manifest","")).is_file(): errors.append("backup manifest missing")
    result={"status":"error" if errors else "ok","errors":errors,"warnings":warnings,"selected_skills":len(skills),"selected_agents":len(plan["agents"]["selected"]),"enabled_integrations":enabled}
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if errors: raise SystemExit(1)
if __name__=="__main__": main()
