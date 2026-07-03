#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

SNAPSHOT_PATHS=["AGENTS.md",".codex",".agents",".cbmignore",".codex-powerpack/tools",".codex-powerpack/cache",".codex-powerpack/state",".codex-powerpack/core"]

def run(cmd, **kw):
    cp=subprocess.run([str(x) for x in cmd],text=True,**kw)
    if cp.returncode: raise RuntimeError(f"command failed ({cp.returncode}): {' '.join(map(str,cmd))}")
    return cp

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def snapshot(target:Path, backup:Path):
    entries=[]; backup.mkdir(parents=True,exist_ok=False)
    for rel in SNAPSHOT_PATHS:
        src=target/rel; dst=backup/rel
        row={"path":rel,"existed":src.exists(),"type":"directory" if src.is_dir() else "file"}
        if src.exists():
            dst.parent.mkdir(parents=True,exist_ok=True)
            shutil.copytree(src,dst) if src.is_dir() else shutil.copy2(src,dst)
        entries.append(row)
    manifest=backup/"backup-manifest.json"; manifest.write_text(json.dumps({"schema_version":1,"entries":entries},indent=2)+"\n","utf-8")
    return manifest

def restore(target:Path, backup:Path):
    manifest=json.loads((backup/"backup-manifest.json").read_text())
    # deepest paths first prevents parent restoration from being overwritten later
    for row in sorted(manifest["entries"],key=lambda x:x["path"].count("/"),reverse=True):
        rel=row["path"]; current=target/rel; saved=backup/rel
        if current.exists(): shutil.rmtree(current) if current.is_dir() else current.unlink()
        if row["existed"]:
            current.parent.mkdir(parents=True,exist_ok=True)
            shutil.copytree(saved,current) if saved.is_dir() else shutil.copy2(saved,current)

def main():
    p=argparse.ArgumentParser(); p.add_argument("--root",required=True); p.add_argument("--target",required=True); p.add_argument("--plan",required=True); p.add_argument("--yes",action="store_true"); p.add_argument("--force",action="store_true"); p.add_argument("--dry-run",action="store_true"); p.add_argument("--codebase-memory-binary"); a=p.parse_args()
    root=Path(a.root).resolve(); target=Path(a.target).resolve(); plan_path=Path(a.plan).resolve(); plan=json.loads(plan_path.read_text())
    run([sys.executable,root/"dist/onboarding/validate_json.py","--schema",root/"dist/onboarding/schemas/adaptation-plan.schema.json","--document",plan_path],capture_output=True)
    if Path(plan["project_root"]).resolve()!=target: raise SystemExit("ERROR: plan target mismatch")
    sum_path=plan_path.with_name("adaptation-plan.sha256")
    expected=sum_path.read_text().split()[0] if sum_path.exists() else ""
    if not expected or digest(plan_path)!=expected: raise SystemExit("ERROR: plan hash mismatch")
    if not a.yes and not plan.get("approved",False): raise SystemExit("ERROR: plan is not approved; pass --yes only after reviewing it")
    # Fresh deterministic scan; generated Powerpack state is excluded from the fingerprint.
    cp=run([sys.executable,root/"dist/onboarding/scan-project.py","--target",target,"--stdout"],capture_output=True)
    fresh=json.loads(cp.stdout)
    if fresh["project_fingerprint"]!=plan["project_fingerprint"] and not a.force: raise SystemExit("ERROR: project changed after analysis; rescan or use --force after review")
    integrations=plan["integrations"]
    if integrations["graphify"]["decision"]=="enable" and not shutil.which("graphify"): raise SystemExit("ERROR: Graphify selected but graphify CLI is unavailable; install it safely or revise the plan")
    if plan.get("mode")=="auto" and integrations["codebase-memory"]["decision"]=="enable" and not a.codebase_memory_binary and not (target/".codex-powerpack/tools/codebase-memory-mcp").is_file():
        raise SystemExit("ERROR: auto mode refuses an implicit network download; supply --codebase-memory-binary or apply the plan in guided mode")
    if a.dry_run:
        print(json.dumps({"plan_sha256":expected,"operations":plan["operations"],"preflight":"ok"},indent=2)); return
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup=target/".codex-powerpack/backups"/f"adaptation-{stamp}"; manifest=snapshot(target,backup)
    state_path=target/".codex-powerpack/state/adaptation-state.json"
    try:
        run([sys.executable,root/"dist/install/project_files.py","install","--root",root,"--target",target,"--plan",plan_path,"--backup"]+(["--force"] if a.force else []))
        generated=target/".codex-powerpack/generated/AGENTS.project.generated.md"
        run([sys.executable,root/"dist/onboarding/generate-project-rules.py","--plan",plan_path,"--output-dir",generated.parent])
        run([sys.executable,root/"dist/onboarding/managed_rules.py","merge","--target",target/"AGENTS.md","--generated",generated])
        if integrations["codebase-memory"]["decision"]=="enable":
            cmd=[root/"dist/integrations/codebase-memory/install.sh","--target",target,"--scope","project","--auto-index","auto","--backup"]
            if a.codebase_memory_binary: cmd += ["--binary",a.codebase_memory_binary]
            run(cmd)
        if integrations["graphify"]["decision"]=="enable": run([root/"dist/integrations/graphify/install.sh","--target",target])
        selected_skills=[x["id"] for x in plan["skills"]["always_on"]+plan["skills"]["selected"]]
        selected_agents=[x["id"] for x in plan["agents"]["selected"]]
        state={"schema_version":1,"project_root":str(target),"plan_path":str(plan_path),"plan_sha256":expected,"applied_at":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),"status":"applied","managed_files":[str(target/"AGENTS.md"),str(target/".agents/skills"),str(target/".codex/agents")],"backup_root":str(backup),"backup_manifest":str(manifest),"selected_skills":selected_skills,"selected_agents":selected_agents,"integrations":integrations,"verification":{"status":"pending"}}
        state_path.parent.mkdir(parents=True,exist_ok=True); state_path.write_text(json.dumps(state,indent=2)+"\n","utf-8")
        run([root/"dist/onboarding/verify-adaptation.sh","--target",target,"--plan",plan_path])
        state=json.loads(state_path.read_text()); state["status"]="verified"; state["verification"]={"status":"passed","verified_at":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}; state_path.write_text(json.dumps(state,indent=2)+"\n","utf-8")
    except BaseException:
        restore(target,backup)
        raise
    print(f"OK: adaptation applied and verified: {state_path}")

if __name__=="__main__":
    try: main()
    except Exception as exc: raise SystemExit(f"ERROR: {exc}")
