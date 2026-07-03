#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("--old",required=True)
p.add_argument("--new",required=True)
p.add_argument("--output",required=True)
a=p.parse_args()
old=json.loads(Path(a.old).read_text())
new=json.loads(Path(a.new).read_text())

def ids(plan,key):
    selected={x["id"] for x in plan[key]["selected"]}
    always={x["id"] for x in plan[key].get("always_on",[])} if key=="skills" else set()
    return selected|always

data={
    "skills_added":sorted(ids(new,"skills")-ids(old,"skills")),
    "skills_removed":sorted(ids(old,"skills")-ids(new,"skills")),
    "agents_added":sorted(ids(new,"agents")-ids(old,"agents")),
    "agents_removed":sorted(ids(old,"agents")-ids(new,"agents")),
    "integrations_before":old["integrations"],
    "integrations_after":new["integrations"]
}
Path(a.output).write_text(json.dumps(data,indent=2)+"\n","utf-8")
