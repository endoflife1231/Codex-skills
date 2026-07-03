#!/usr/bin/env python3
"""Validate local prerequisites and the Codex nanobanana MCP entry."""
from __future__ import annotations

import json
import shutil
import subprocess


def check_command(name: str) -> bool:
    return shutil.which(name) is not None


def main() -> int:
    checks = {
        "codex_cli": check_command("codex"),
        "node": check_command("node"),
        "npx": check_command("npx"),
        "nanobanana_mcp": False,
    }
    if checks["codex_cli"]:
        result = subprocess.run(
            ["codex", "mcp", "get", "nanobanana-mcp"],
            capture_output=True, text=True, check=False,
        )
        checks["nanobanana_mcp"] = result.returncode == 0
    print(json.dumps(checks, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
