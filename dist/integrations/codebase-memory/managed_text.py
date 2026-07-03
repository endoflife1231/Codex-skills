#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

BEGIN = "<!-- CODEX-POWERPACK:BEGIN codebase-memory -->"
END = "<!-- CODEX-POWERPACK:END codebase-memory -->"


def strip(text: str) -> str:
    start = text.find(BEGIN)
    if start < 0:
        return text.rstrip() + ("\n" if text else "")
    end = text.find(END, start)
    if end < 0:
        raise ValueError("managed AGENTS block has no end marker")
    end += len(END)
    return (text[:start].rstrip() + "\n\n" + text[end:].lstrip()).strip() + "\n"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["upsert", "remove", "check"])
    p.add_argument("--file", required=True)
    p.add_argument("--fragment")
    p.add_argument("--backup", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    path = Path(a.file)
    old = path.read_text("utf-8") if path.exists() else ""
    if a.action == "check":
        return 0 if BEGIN in old and END in old else 1
    new = strip(old)
    if a.action == "upsert":
        if not a.fragment:
            p.error("upsert requires --fragment")
        fragment = Path(a.fragment).read_text("utf-8").strip()
        new = new.rstrip() + ("\n\n" if new.strip() else "") + fragment + "\n"
    if a.dry_run:
        print(new, end="")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    if a.backup and path.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        shutil.copy2(path, path.with_name(path.name + f".powerpack-backup-{stamp}"))
    if new.strip():
        path.write_text(new, "utf-8")
    elif path.exists():
        path.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
