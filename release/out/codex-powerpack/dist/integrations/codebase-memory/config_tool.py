#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

BEGIN = "# CODEX-POWERPACK:BEGIN codebase-memory"
END = "# CODEX-POWERPACK:END codebase-memory"
HEADER = "[mcp_servers.codebase-memory]"


def quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def managed_block(binary: str, cache: str, ui: bool = False) -> str:
    return "\n".join(
        [
            BEGIN,
            HEADER,
            f"command = {quote(binary)}",
            'args = ["--ui=true"]' if ui else "args = []",
            f"env = {{ CBM_CACHE_DIR = {quote(cache)} }}",
            END,
        ]
    )


def strip_block(text: str) -> tuple[str, bool]:
    start = text.find(BEGIN)
    if start < 0:
        return text, False
    end = text.find(END, start)
    if end < 0:
        raise ValueError("managed block start exists without end marker")
    end += len(END)
    while end < len(text) and text[end] in "\r\n":
        end += 1
    prefix = text[:start].rstrip()
    suffix = text[end:].lstrip("\r\n")
    return (prefix + ("\n\n" if prefix and suffix else "") + suffix).rstrip() + ("\n" if prefix or suffix else ""), True


def validate(text: str) -> None:
    tomllib.loads(text)


def backup(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = path.with_name(path.name + f".powerpack-backup-{stamp}")
    shutil.copy2(path, dest)
    return dest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["upsert", "remove", "check"])
    parser.add_argument("--config", required=True)
    parser.add_argument("--binary")
    parser.add_argument("--cache")
    parser.add_argument("--ui", action="store_true")
    parser.add_argument("--backup", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path = Path(args.config)
    original = path.read_text("utf-8") if path.exists() else ""

    try:
        validate(original) if original.strip() else None
        clean, had_managed = strip_block(original)
    except Exception as exc:
        print(f"ERROR: invalid existing TOML or managed block: {exc}", file=sys.stderr)
        return 2

    if args.action == "check":
        if not had_managed or HEADER not in original:
            print("ERROR: managed Codebase Memory MCP section missing", file=sys.stderr)
            return 1
        print("OK: managed Codebase Memory MCP TOML is valid")
        return 0

    if args.action == "remove":
        candidate = clean
    else:
        if not args.binary or not args.cache:
            parser.error("upsert requires --binary and --cache")
        if HEADER in clean:
            candidate = clean.rstrip() + "\n\n" + managed_block(args.binary, args.cache, args.ui) + "\n"
            new_path = path.with_name(path.name + ".new")
            new_path.parent.mkdir(parents=True, exist_ok=True)
            new_path.write_text(candidate, "utf-8")
            print(f"ERROR: unmanaged {HEADER} already exists; candidate written to {new_path}", file=sys.stderr)
            return 3
        candidate = clean.rstrip()
        if candidate:
            candidate += "\n\n"
        candidate += managed_block(args.binary, args.cache, args.ui) + "\n"

    try:
        validate(candidate) if candidate.strip() else None
    except Exception as exc:
        print(f"ERROR: generated TOML is invalid: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(candidate, end="")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    if args.backup:
        made = backup(path)
        if made:
            print(f"BACKUP: {made}")
    path.write_text(candidate, "utf-8")
    print(f"OK: {args.action} {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
