#!/usr/bin/env python3
from __future__ import annotations
import json, os, shutil, subprocess, tempfile
from pathlib import Path
import jsonschema

ROOT=Path(__file__).resolve().parents[1]; ONBOARD=ROOT/"dist/onboarding"
def run(*args,ok=True,env=None):
    cp=subprocess.run([str(x) for x in args],cwd=ROOT,text=True,capture_output=True,env=env)
    if ok and cp.returncode: raise AssertionError(f"{args}\n{cp.stdout}\n{cp.stderr}")
    if not ok and cp.returncode==0: raise AssertionError(f"expected failure: {args}")
    return cp
def write_case(root:Path,case):
    for rel,text in case.get("files",{}).items():
        p=root/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,"utf-8")
    gen=case.get("generate")
    if gen:
        prefix=gen.get("prefix","src/file")
        for i in range(gen["count"]):
            p=root/f"{prefix}{i}{gen['extension']}"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text("# fixture\n","utf-8")
def fake_cbm(path:Path):
    path.write_text("#!/usr/bin/env bash\nif [[ ${1:-} == --version ]]; then echo 'codebase-memory-mcp 0.8.1'; fi\nif [[ ${1:-} == cli ]]; then echo '{\"status\":\"indexed\"}'; fi\nexit 0\n","utf-8"); path.chmod(0o755)
def main():
    cases=json.loads((ROOT/"tests/fixtures/onboarding/cases.json").read_text())
    schemas={name:json.loads((ONBOARD/"schemas"/name).read_text()) for name in ["project-facts.schema.json","project-analysis.schema.json","adaptation-plan.schema.json","adaptation-state.schema.json"]}
    with tempfile.TemporaryDirectory(prefix="powerpack-onboarding-") as td:
        base=Path(td)
        for case in cases:
            target=base/case["name"]; target.mkdir(); write_case(target,case)
            original_agents=(target/"AGENTS.md").read_text() if (target/"AGENTS.md").exists() else None
            run(ONBOARD/"adapt-project.sh","--target",target,"--mode","analyze-only","--with-codebase-memory","auto","--with-graphify","auto")
            facts=json.loads((target/".codex-powerpack/analysis/project-facts.json").read_text())
            plan=json.loads((target/".codex-powerpack/generated/adaptation-plan.json").read_text())
            analysis=json.loads((target/".codex-powerpack/analysis/project-analysis.json").read_text())
            jsonschema.validate(facts,schemas["project-facts.schema.json"])
            jsonschema.validate(analysis,schemas["project-analysis.schema.json"])
            jsonschema.validate(plan,schemas["adaptation-plan.schema.json"])
            exp=case["expect"]
            assert plan["integrations"]["codebase-memory"]["decision"]==exp["codebase-memory"],case["name"]
            assert plan["integrations"]["graphify"]["decision"]==exp["graphify"],case["name"]
            selected={x["id"] for x in plan["skills"]["always_on"]+plan["skills"]["selected"]}
            assert {"caveman","caveman-compress","caveman-review","caveman-stats"}<=selected
            assert len(plan["always_on"]["live_language"]["skills"])>=8
            assert len(selected)<253
            for skill in exp.get("skills",[]): assert skill in selected,(case["name"],skill,selected)
            assert len(plan["agents"]["selected"]) in {4,8}
            if exp.get("secret_risk"): assert any("secret-pattern" in x for x in facts["risks"])
            if exp.get("existing_mcp"): assert exp["existing_mcp"] in facts["existing_codex"]["mcp_servers"]
            if original_agents is not None: assert (target/"AGENTS.md").read_text()==original_agents

        # Lifecycle: plan, exact apply, idempotent reanalysis, verification and rollback.
        target=base/"lifecycle"; target.mkdir(); (target/"main.py").write_text("print('ok')\n"); (target/"AGENTS.md").write_text("USER RULE\n")
        binary=base/"cbm"; fake_cbm(binary)
        run(ONBOARD/"adapt-project.sh","--target",target,"--mode","guided","--apply","--non-interactive","--with-graphify","no","--codebase-memory-binary",binary)
        assert "USER RULE" in (target/"AGENTS.md").read_text()
        run(ONBOARD/"verify-adaptation.sh","--target",target)
        state=json.loads((target/".codex-powerpack/state/adaptation-state.json").read_text())
        jsonschema.validate(state,schemas["adaptation-state.schema.json"])
        run(ONBOARD/"adapt-project.sh","--target",target,"--mode","guided","--force-rescan","--with-graphify","no")
        assert (target/".codex-powerpack/generated/adaptation-diff.json").exists()
        run(ONBOARD/"rollback.sh","--target",target)
        assert (target/"AGENTS.md").read_text()=="USER RULE\n"
        assert not (target/".agents").exists()

        # Graphify apply uses the safe wrapper: no upstream installer and no hook.
        graph=base/"graph-lifecycle"; graph.mkdir(); (graph/"README.md").write_text("docs\n")
        for i in range(21): (graph/f"doc{i}.md").write_text("doc\n")
        fakebin=base/"bin"; fakebin.mkdir(); graphify=fakebin/"graphify"
        graphify.write_text("#!/usr/bin/env bash\n[[ ${1:-} == --version ]] && echo 'graphify fixture'\nexit 0\n"); graphify.chmod(0o755)
        env=os.environ.copy(); env["PATH"]=str(fakebin)+os.pathsep+env["PATH"]
        run(ONBOARD/"adapt-project.sh","--target",graph,"--mode","guided","--apply","--non-interactive","--with-codebase-memory","no","--with-graphify","yes",env=env)
        assert (graph/".codex-powerpack/state/graphify.json").exists()
        assert not (graph/".codex/hooks.json").exists()
        run(ONBOARD/"rollback.sh","--target",graph,env=env)
        assert not (graph/".agents").exists()

        # Fail-safe flags and plan integrity.
        waiver=base/"waiver"; waiver.mkdir(); (waiver/"README.md").write_text("docs")
        run(ONBOARD/"adapt-project.sh","--target",waiver,"--mode","analyze-only","--without-project-intelligence",ok=False)
        integrity=base/"integrity"; integrity.mkdir(); (integrity/"main.py").write_text("x=1")
        run(ONBOARD/"adapt-project.sh","--target",integrity,"--mode","analyze-only")
        plan=integrity/".codex-powerpack/generated/adaptation-plan.json"; plan.write_text(plan.read_text()+" ")
        run(ONBOARD/"apply-plan.sh","--target",integrity,"--plan",plan,"--yes","--dry-run",ok=False)
        auto=base/"auto-no-network"; auto.mkdir(); (auto/"main.py").write_text("x=1")
        run(ONBOARD/"adapt-project.sh","--target",auto,"--mode","auto","--with-graphify","no",ok=False)
        assert not (auto/".codex/config.toml").exists()
    print(f"OK: onboarding fixtures and lifecycle passed ({len(cases)} fixtures)")
if __name__=="__main__": main()
