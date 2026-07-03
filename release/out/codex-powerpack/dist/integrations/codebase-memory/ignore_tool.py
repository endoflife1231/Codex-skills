#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path

BEGIN = "# CODEX-POWERPACK:BEGIN codebase-memory"
END = "# CODEX-POWERPACK:END codebase-memory"

def strip(text: str) -> str:
    start = text.find(BEGIN)
    if start < 0: return text.rstrip()
    end = text.find(END, start)
    if end < 0: raise ValueError("incomplete managed .cbmignore block")
    return (text[:start].rstrip() + "\n" + text[end + len(END):].lstrip()).rstrip()

p = argparse.ArgumentParser()
p.add_argument("action", choices=["upsert", "remove"])
p.add_argument("--target", required=True)
p.add_argument("--rules")
p.add_argument("--dry-run", action="store_true")
a = p.parse_args()
path = Path(a.target)
text = strip(path.read_text("utf-8") if path.exists() else "")
if a.action == "upsert":
    rules = Path(a.rules).read_text("utf-8").strip()
    text = text + ("\n\n" if text else "") + BEGIN + "\n" + rules + "\n" + END
text = text.rstrip() + ("\n" if text else "")
if a.dry_run: print(text, end="")
elif text: path.write_text(text, "utf-8")
elif path.exists(): path.unlink()
