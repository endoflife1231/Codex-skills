#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path


def rec(identifier: str, confidence: float, reasons: list[str], evidence: list[str], required=False, always=False):
    return {"id":identifier,"confidence":confidence,"required":required,"always_on":always,"reasons":reasons,"matched_evidence":evidence,"conflicts":[],"source_registry_entry":identifier}


def analyze(f: dict) -> dict:
    src=f["source_file_count"]; docs=f["documentation_file_count"]; media=f["binary_or_media_count"]
    tech=f["languages"]+f["frameworks"]+f["databases"]+f["orms"]+f["testing"]+f["containers"]+f["infrastructure"]
    if f["monorepo"]: style=["monorepo"]
    elif len(f["services"])>1: style=["multi-service"]
    elif src: style=["modular-codebase" if src>=30 else "small-codebase"]
    else: style=["documentation-or-content"]
    cbm = src>=30 or f["monorepo"] or len(f["services"])>1
    graph = docs>=20 or media>0 or (src==0 and docs>0)
    if not cbm and not graph: cbm = src>0
    if not cbm and not graph: graph = True
    skills=[]
    evidence=[f"languages={','.join(f['languages']) or 'none'}",f"source_files={src}",f"documentation_files={docs}"]
    if src: skills += [rec("source-driven-development",.9,["code project needs source-grounded changes"],evidence),rec("test-driven-development",.82,["verification workflow for code changes"],evidence),rec("debugging-and-error-recovery",.8,["code project benefits from structured debugging"],evidence)]
    if any(x in f["frameworks"] for x in ["React","Next.js","Vue","Nuxt","Angular","Svelte"]):
        skills += [rec("frontend-ui-engineering",.92,["frontend framework detected"],f["frameworks"]),rec("browser-testing-with-devtools",.78,["browser UI detected"],f["frameworks"])]
    if any(x in f["frameworks"] for x in ["React","Next.js"]): skills.append(rec("vercel-react-best-practices",.88,["React-family project detected"],f["frameworks"]))
    if "Fastify" in f["frameworks"]: skills.append(rec("fastify-best-practices",.95,["Fastify dependency detected"],["Fastify"]))
    if any(x in f["frameworks"] for x in ["Express","Fastify","NestJS","FastAPI","Django","Flask"]): skills.append(rec("api-and-interface-design",.84,["backend/API framework detected"],f["frameworks"]))
    if "PostgreSQL" in f["databases"]: skills.append(rec("postgres-best-practices",.94,["PostgreSQL dependency detected"],["PostgreSQL"]))
    if "Drizzle" in f["orms"]: skills.append(rec("drizzle-best-practices",.94,["Drizzle detected"],["Drizzle"]))
    if any(x in f["testing"] for x in ["playwright","cypress"]): skills.append(rec("playwright",.9,["browser test stack detected"],f["testing"]))
    if f["containers"] or f["infrastructure"] or f["ci"]: skills.append(rec("ci-cd-and-automation",.84,["CI/container/infrastructure metadata detected"],f["containers"]+f["infrastructure"]+f["ci"]))
    if docs: skills.append(rec("documentation-and-adrs",.8,["project documentation detected"],[f"documentation_files={docs}"]))
    agents=[rec(x,.9,["baseline project role"],[style[0]]) for x in ["explorer","planner","reviewer","tester"]]
    if src>=30 or f["monorepo"]:
        agents += [rec(x,.82,["non-trivial codebase warrants implementation and specialist roles"],[f"source_files={src}"]) for x in ["implementer","debugger","security-reviewer","architect"]]
    integrations=[]
    if cbm: integrations.append(rec("codebase-memory",.92 if src>=30 else .74,["structural code understanding selected"],[f"source_files={src}",f"monorepo={f['monorepo']}"],required=not graph))
    if graph: integrations.append(rec("graphify",.9 if docs>=20 else .75,["documentation/media graph selected"],[f"documentation_files={docs}",f"media_files={media}"],required=not cbm))
    return {
      "schema_version":1,"analysis_method":"deterministic-fallback",
      "project_summary":f"{style[0]} with {src} source and {docs} documentation files",
      "primary_purpose":", ".join(f["project_type"]) or "unknown project",
      "architecture":{"style":style,"layers":[],"modules":f["source_roots"],"services":f["services"],"data_flow":[],"important_boundaries":f["source_roots"]},
      "confirmed_technologies":sorted(set(tech)),"probable_technologies":[],
      "development_workflow":{**f["commands"],"run":f["commands"].get("dev",[])},
      "always_on":{"caveman":{"decision":"enable","required":True,"selected_skills":[],"policy":{}},"live_language":{"decision":"enable","required":True,"selected_skills":[],"languages":["ru","en"],"policy":{}},"project_intelligence":{"required":True,"selected":[x["id"] for x in integrations]}},
      "recommended_skills":skills,"recommended_agents":agents,"recommended_integrations":integrations,
      "graph_strategy":{"codebase_memory":{"decision":"enable" if cbm else "disable","confidence":.92 if cbm else .85,"reasons":[f"source_file_count={src}"]},"graphify":{"decision":"enable" if graph else "disable","confidence":.9 if graph else .85,"reasons":[f"documentation_file_count={docs}",f"media_count={media}"]}},
      "caveman_policy":{},"live_language_policy":{},"project_rules":[],"nested_rule_scopes":[],
      "unknowns":f["unknowns"],"questions_requiring_user_decision":[],"confidence":.82 if tech else .7
    }


def main():
    p=argparse.ArgumentParser(); p.add_argument("--facts",required=True); p.add_argument("--output",required=True); a=p.parse_args()
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(analyze(json.loads(Path(a.facts).read_text())),indent=2,ensure_ascii=False)+"\n","utf-8")
    print(out)
if __name__=="__main__": main()
