#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

CAVEMAN=["caveman","caveman-compress","caveman-review","caveman-stats"]
LIVE=["bilingual-transcreator","humanizer","humanizer-ru","ru-editor","ru-text","ru-textovod","en-ru-translator-adv","copy-editing","writing-guidelines","brand","copywriting","impeccable"]

def item(identifier, reason, confidence=1.0, always=False, required=False, **extra):
    return {"id":identifier,"confidence":confidence,"always_on":always,"required":required,"reasons":[reason],**extra}

def decide_integration(facts, analysis, cbm_override, graph_override, without):
    src=facts["source_file_count"]; docs=facts["documentation_file_count"]; media=facts["binary_or_media_count"]
    cbm = src>=30 or facts["monorepo"] or len(facts["services"])>1
    graph = docs>=20 or media>0 or (src==0 and docs>0)
    if src>0 and not cbm and not graph: cbm=True
    if not cbm and not graph: graph=True
    if cbm_override != "auto": cbm=cbm_override=="yes"
    if graph_override != "auto": graph=graph_override=="yes"
    if without: cbm=graph=False
    if not without and not (cbm or graph): raise ValueError("selection would leave project without project intelligence")
    return {
      "codebase-memory":{"decision":"enable" if cbm else "disable","confidence":.95 if cbm and src>=30 else .78,"reasons":[f"source files: {src}",f"monorepo: {facts['monorepo']}"]},
      "graphify":{"decision":"enable" if graph else "disable","confidence":.92 if graph and docs>=20 else .76,"reasons":[f"documentation files: {docs}",f"media files: {media}"],"external_dependency":"graphify CLI"},
      "at_least_one_required":not without,"explicit_waiver":without
    }

def main():
    p=argparse.ArgumentParser(); p.add_argument("--root",required=True); p.add_argument("--target",required=True); p.add_argument("--facts",required=True); p.add_argument("--analysis",required=True); p.add_argument("--mode",choices=["guided","auto","manual","analyze-only"],default="guided"); p.add_argument("--profile",choices=["auto","minimal","standard","full"],default="auto"); p.add_argument("--with-codebase-memory",choices=["auto","yes","no"],default="auto"); p.add_argument("--with-graphify",choices=["auto","yes","no"],default="auto"); p.add_argument("--without-project-intelligence",action="store_true"); p.add_argument("--confidence-threshold",type=float,default=.7); p.add_argument("--output-dir"); a=p.parse_args()
    root=Path(a.root).resolve(); target=Path(a.target).resolve(); facts=json.loads(Path(a.facts).read_text()); analysis=json.loads(Path(a.analysis).read_text())
    sreg=json.loads((root/"dist/skills/registry.json").read_text())["skills"]; areg=json.loads((root/"dist/agents/registry.json").read_text())["agents"]
    skills={x["name"]:x for x in sreg}; agents={x["name"]:x for x in areg}
    missing=[x for x in CAVEMAN+LIVE if x not in skills]
    if "caveman" in missing: raise ValueError("critical always-on Skill caveman is missing")
    warnings=[f"preferred always-on Skill missing: {x}" for x in missing]
    always_ids=[x for x in CAVEMAN+LIVE if x in skills]
    always=[item(x,"required always-on group",1,True,True,group="caveman" if x in CAVEMAN else "live-language-core") for x in always_ids]
    recommended={x["id"]:x for x in analysis.get("recommended_skills",[]) if x.get("id") in skills and x.get("id") not in always_ids}
    unknown_recs=[x.get("id") for x in analysis.get("recommended_skills",[]) if x.get("id") not in skills]
    warnings += [f"analysis recommended unknown Skill: {x}" for x in unknown_recs]
    if a.profile=="full": candidates={x["name"]:{"id":x["name"],"confidence":1,"reasons":["explicit full profile"]} for x in sreg if x["name"] not in always_ids}
    else: candidates=recommended
    cutoff=max(a.confidence_threshold,.85 if a.profile=="minimal" else 0)
    selected=[]; optional=[]; rejected=[]; manual=[]; conflicted=[]; selected_ids=set(always_ids)
    for ident, rec in sorted(candidates.items()):
        conf=float(rec.get("confidence",0)); row=item(ident,(rec.get("reasons") or ["matched project evidence"])[0],conf)
        conflicts=[x for x in skills[ident].get("conflicts",[]) if x in selected_ids]
        if conflicts: row["conflicts"]=conflicts; conflicted.append(row); continue
        if conf>=cutoff: selected.append(row); selected_ids.add(ident)
        elif conf>=.55: optional.append(row)
        else: rejected.append(row)
    if analysis.get("confidence",0)<a.confidence_threshold:
        manual.append(item("project-analysis","analysis confidence is below threshold",analysis.get("confidence",0)))

    rec_agents={x["id"]:x for x in analysis.get("recommended_agents",[]) if x.get("id") in agents}
    base=["explorer","planner","reviewer","tester"]
    if a.profile=="full": chosen=list(agents)
    elif a.profile=="minimal" or facts["source_file_count"]<30: chosen=base
    else: chosen=base+[x for x in ["implementer","debugger","security-reviewer","architect"] if x in rec_agents]
    chosen=list(dict.fromkeys(x for x in chosen if x in agents))
    agent_selected=[]
    for ident in chosen:
        reg=agents[ident]; writes=bool(reg.get("writes")); risk="write-capable" if writes else "read-only"
        agent_selected.append(item(ident,"project size and workflow role",.9,write_access=writes,risk=risk,role=reg.get("role")))
    agent_optional=[item(x,"available but not selected",.5,write_access=bool(agents[x].get("writes"))) for x in agents if x not in chosen]
    integrations=decide_integration(facts,analysis,a.with_codebase_memory,a.with_graphify,a.without_project_intelligence)
    if integrations["graphify"]["decision"]=="enable": warnings.append("Graphify apply requires an existing graphify CLI; no unsafe bootstrap is performed")

    out=Path(a.output_dir) if a.output_dir else target/".codex-powerpack/generated"; out.mkdir(parents=True,exist_ok=True)
    skill_selection={"always_on":always,"selected":selected,"optional":optional,"rejected":rejected,"conflicted":conflicted,"manual_review":manual,"warnings":warnings}
    agent_selection={"selected":agent_selected,"optional":agent_optional,"rejected":[]}
    (out/"skill-selection.json").write_text(json.dumps(skill_selection,indent=2,ensure_ascii=False)+"\n","utf-8")
    (out/"agent-selection.json").write_text(json.dumps(agent_selection,indent=2,ensure_ascii=False)+"\n","utf-8")
    (out/"integration-selection.json").write_text(json.dumps(integrations,indent=2,ensure_ascii=False)+"\n","utf-8")
    resolved_profile=a.profile if a.profile!="auto" else ("minimal" if facts["source_file_count"]<30 else "standard")
    now=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    plan={
      "schema_version":1,"plan_id":"pending","created_at":now,"project_root":str(target),"project_fingerprint":facts["project_fingerprint"],
      "mode":a.mode,"profile":a.profile,"resolved_profile":resolved_profile,"confidence":analysis.get("confidence",0),"analysis_method":analysis.get("analysis_method","unknown"),
      "project_summary":analysis.get("project_summary",""),"detected_stack":{"languages":facts["languages"],"frameworks":facts["frameworks"],"databases":facts["databases"],"testing":facts["testing"],"containers":facts["containers"],"infrastructure":facts["infrastructure"]},
      "always_on":{"caveman":{"enabled":True,"skills":[x for x in always_ids if x in CAVEMAN]},"live_language":{"enabled":True,"skills":[x for x in always_ids if x in LIVE]}},
      "skills":skill_selection,"agents":agent_selection,"integrations":integrations,
      "operations":[{"action":"install-selected-skills","target":".agents/skills"},{"action":"install-selected-agents","target":".codex/agents"},{"action":"merge-managed-rules","target":"AGENTS.md"}]+([{"action":"install-codebase-memory","target":".codex/config.toml"}] if integrations["codebase-memory"]["decision"]=="enable" else [])+([{"action":"configure-graphify","target":"project"}] if integrations["graphify"]["decision"]=="enable" else []),
      "verification":["validate selected Skills and agents","validate managed AGENTS blocks","validate Codex TOML","verify enabled project intelligence","validate adaptation state"],
      "risks":facts["risks"]+warnings+[x["risk"]+": "+x["id"] for x in agent_selected if x["write_access"]],
      "questions":analysis.get("questions_requiring_user_decision",[])+(["Analysis confidence is below threshold; review selections manually."] if manual else []),
      "approved":a.mode=="auto" and not manual
    }
    canonical=json.dumps({**plan,"plan_id":"pending"},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode(); plan["plan_id"]=hashlib.sha256(canonical).hexdigest()[:16]
    plan_path=out/"adaptation-plan.json"; plan_path.write_text(json.dumps(plan,indent=2,ensure_ascii=False)+"\n","utf-8")
    digest=hashlib.sha256(plan_path.read_bytes()).hexdigest(); (out/"adaptation-plan.sha256").write_text(digest+"  adaptation-plan.json\n","utf-8")
    lines=["# Codex Powerpack adaptation plan","",f"- Project: `{target}`",f"- Mode: `{a.mode}`",f"- Profile: `{a.profile}` → `{resolved_profile}`",f"- Analysis: `{plan['analysis_method']}`; confidence `{plan['confidence']:.2f}`","", "## Detected stack", "", ", ".join(sum(plan["detected_stack"].values(),[])) or "No confirmed stack", "", "## Always on", "", "- Caveman: "+", ".join(plan["always_on"]["caveman"]["skills"]), "- Live language: "+", ".join(plan["always_on"]["live_language"]["skills"]), "", "## Selected Skills", "", ", ".join(x["id"] for x in always+selected), "", "## Selected agents", "", ", ".join(x["id"]+f" ({x['risk']})" for x in agent_selected), "", "## Project intelligence", "", f"- Codebase Memory: {integrations['codebase-memory']['decision']} — {'; '.join(integrations['codebase-memory']['reasons'])}", f"- Graphify: {integrations['graphify']['decision']} — {'; '.join(integrations['graphify']['reasons'])}", "", "## Risks and review", ""]+[f"- {x}" for x in plan["risks"]+plan["questions"]]
    (out/"adaptation-plan.md").write_text("\n".join(lines)+"\n","utf-8")
    print(plan_path)
if __name__=="__main__":
    try: main()
    except Exception as exc: raise SystemExit(f"ERROR: {exc}")
