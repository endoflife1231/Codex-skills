#!/usr/bin/env bash
set -euo pipefail

CBM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_ROOT="$(cd "$CBM_DIR/../../.." && pwd)"
VERSION="$(tr -d '[:space:]' < "$CBM_DIR/VERSION")"

die() { echo "ERROR: $*" >&2; exit 1; }
warn() { echo "WARNING: $*" >&2; }
ok() { echo "OK: $*"; }

absolute_dir() {
  local path="$1"
  mkdir -p "$path"
  (cd "$path" && pwd -P)
}

resolve_layout() {
  local target="$1" scope="${2:-project}"
  TARGET="$(absolute_dir "$target")"
  if [[ "$scope" == "user" ]]; then
    POWERPACK_HOME="${CODEX_POWERPACK_HOME:-$HOME/.codex-powerpack}"
    CONFIG_PATH="${CODEX_HOME:-$HOME/.codex}/config.toml"
    AGENTS_PATH="${CODEX_HOME:-$HOME/.codex}/AGENTS.md"
  else
    POWERPACK_HOME="$TARGET/.codex-powerpack"
    CONFIG_PATH="$TARGET/.codex/config.toml"
    AGENTS_PATH="$TARGET/AGENTS.md"
  fi
  TOOLS_DIR="$POWERPACK_HOME/tools"
  CACHE_DIR="$POWERPACK_HOME/cache/codebase-memory"
  STATE_DIR="$POWERPACK_HOME/state"
  STATE_PATH="$STATE_DIR/codebase-memory.json"
  BIN_PATH="$TOOLS_DIR/codebase-memory-mcp"
}

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | awk '{print $1}';
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | awk '{print $1}';
  else die "sha256sum or shasum is required"; fi
}

write_state() {
  local auto_index="$1" ui="$2" scope="$3" backup_json="${4:-[]}"
  mkdir -p "$STATE_DIR"
  python3 - "$STATE_PATH" "$VERSION" "$BIN_PATH" "$(sha256_file "$BIN_PATH")" \
    "$scope" "$CONFIG_PATH" "$CACHE_DIR" "$auto_index" "$ui" "$AGENTS_PATH" "$TARGET/.cbmignore" "$backup_json" <<'PY'
import json, sys
from datetime import datetime, timezone
from pathlib import Path
p, version, binary, sha, scope, config, cache, auto, ui, agents, ignore, backups = sys.argv[1:]
data = {
  "schema_version": 1,
  "integration": "codebase-memory",
  "enabled": True,
  "version": version,
  "commit": "f0c9be1-release; local-source-snapshot-unverified",
  "binary_path": binary,
  "binary_sha256": sha,
  "mcp_scope": scope,
  "mcp_config_path": config,
  "mcp_server_name": "codebase-memory",
  "cache_path": cache,
  "index_path": cache,
  "auto_index": auto,
  "ui_enabled": ui == "true",
  "managed_files": [binary, config, agents, ignore],
  "managed_config_keys": ["mcp_servers.codebase-memory"],
  "backup_paths": json.loads(backups),
  "installed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
}
Path(p).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY
}
