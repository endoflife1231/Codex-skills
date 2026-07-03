#!/usr/bin/env python3
from __future__ import annotations
import argparse, re
from pathlib import Path

NAMES=["generated-project-profile","caveman","live-language","project-intelligence"]
def remove(text,name):
    pattern=re.compile(rf"(?:\n\n)?<!-- CODEX-POWERPACK:BEGIN {re.escape(name)} -->.*?<!-- CODEX-POWERPACK:END {re.escape(name)} -->\n?",re.S)
    return pattern.sub("",text).rstrip()
def extract(text,name):
    m=re.search(rf"<!-- CODEX-POWERPACK:BEGIN {re.escape(name)} -->.*?<!-- CODEX-POWERPACK:END {re.escape(name)} -->",text,re.S)
    if not m: raise ValueError(f"generated block missing: {name}")
    return m.group(0)
def main():
    p=argparse.ArgumentParser(); p.add_argument("action",choices=["merge","remove","check"]); p.add_argument("--target",required=True); p.add_argument("--generated"); a=p.parse_args(); path=Path(a.target); text=path.read_text("utf-8") if path.exists() else ""
    if a.action=="check":
        bad=[n for n in NAMES if text.count(f"<!-- CODEX-POWERPACK:BEGIN {n} -->")!=1 or text.count(f"<!-- CODEX-POWERPACK:END {n} -->")!=1]
        if bad: raise SystemExit("ERROR: missing or duplicate blocks: "+", ".join(bad))
        print("OK: generated project rule blocks valid"); return
    for n in NAMES: text=remove(text,n)
    if a.action=="merge":
        if not a.generated: p.error("merge requires --generated")
        generated=Path(a.generated).read_text("utf-8"); blocks=[extract(generated,n) for n in NAMES]
        text=text.rstrip()+("\n\n" if text.strip() else "")+"\n\n".join(blocks)+"\n"
    elif text: text=text.rstrip()+"\n"
    if text.strip(): path.write_text(text,"utf-8")
    elif path.exists(): path.unlink()
if __name__=="__main__": main()
