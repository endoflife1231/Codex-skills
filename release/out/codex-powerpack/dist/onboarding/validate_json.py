#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument("--schema",required=True); p.add_argument("--document",required=True); a=p.parse_args()
    schema=json.loads(Path(a.schema).read_text()); document=json.loads(Path(a.document).read_text())
    if not isinstance(document,dict): raise SystemExit("ERROR: document is not an object")
    missing=[x for x in schema.get("required",[]) if x not in document]
    if missing: raise SystemExit("ERROR: missing required fields: "+", ".join(missing))
    for key, rule in schema.get("properties",{}).items():
        if key not in document: continue
        value=document[key]
        if "const" in rule and value != rule["const"]: raise SystemExit(f"ERROR: {key} must equal {rule['const']!r}")
        if "enum" in rule and value not in rule["enum"]: raise SystemExit(f"ERROR: {key} is outside its enum")
        expected=rule.get("type")
        types={"string":str,"object":dict,"array":list,"boolean":bool,"integer":int,"number":(int,float)}
        if expected in types and not isinstance(value,types[expected]): raise SystemExit(f"ERROR: {key} has wrong type")
    print(f"OK: {Path(a.document).name} matches {Path(a.schema).name}")
if __name__=="__main__":
    try: main()
    except Exception as exc: raise SystemExit(f"ERROR: schema validation failed: {exc}")
