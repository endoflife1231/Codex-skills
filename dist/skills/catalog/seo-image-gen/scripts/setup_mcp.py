#!/usr/bin/env python3
"""Configure the optional nanobanana MCP server for Codex.

This script delegates configuration to the official `codex mcp add` command.
It never writes repository files. The supplied key is persisted by Codex's MCP
configuration mechanism, so use a dedicated key and rotate it when needed.
"""
from __future__ import annotations

import argparse
import getpass
import shutil
import subprocess
import sys

SERVER = "nanobanana-mcp"
PACKAGE = "@ycse/nanobanana-mcp@1.1.1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--remove", action="store_true", help="Remove the Codex MCP entry")
    parser.add_argument("--key", help="Google AI API key; omit to enter it securely")
    args = parser.parse_args()

    if not shutil.which("codex"):
        print("codex CLI is not available. See ../references/CODEX-SETUP.md", file=sys.stderr)
        return 2
    if args.remove:
        return subprocess.call(["codex", "mcp", "remove", SERVER])
    if not shutil.which("npx"):
        print("npx is required for the MCP server.", file=sys.stderr)
        return 2

    key = args.key or getpass.getpass("GOOGLE_AI_API_KEY: ")
    if not key:
        print("No key provided.", file=sys.stderr)
        return 2

    # Remove first so repeated setup is deterministic. Ignore a missing entry.
    subprocess.run(["codex", "mcp", "remove", SERVER], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cmd = [
        "codex", "mcp", "add", SERVER,
        "--env", f"GOOGLE_AI_API_KEY={key}",
        "--", "npx", "-y", PACKAGE,
    ]
    completed = subprocess.run(cmd, check=False)
    if completed.returncode == 0:
        print(f"Configured {SERVER}. Verify with: codex mcp get {SERVER}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
