#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument("--target",required=True); a=p.parse_args(); target=Path(a.target).resolve(); state_path=target/".codex-powerpack/state/adaptation-state.json"
    if not state_path.exists(): raise SystemExit(f"ERROR: adaptation state missing: {state_path}")
    state=json.loads(state_path.read_text()); backup=Path(state["backup_root"]); manifest=Path(state["backup_manifest"])
    if not manifest.exists(): raise SystemExit(f"ERROR: backup manifest missing: {manifest}")
    data=json.loads(manifest.read_text())
    for row in sorted(data["entries"],key=lambda x:x["path"].count("/"),reverse=True):
        current=target/row["path"]; saved=backup/row["path"]
        if current.exists(): shutil.rmtree(current) if current.is_dir() else current.unlink()
        if row["existed"]:
            current.parent.mkdir(parents=True,exist_ok=True)
            shutil.copytree(saved,current) if saved.is_dir() else shutil.copy2(saved,current)
    marker=backup/"ROLLED_BACK"; marker.write_text("rollback completed\n","utf-8")
    print(f"OK: restored snapshot {backup}")
if __name__=="__main__": main()
