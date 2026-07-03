#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/common.sh"

TARGET=""; SCOPE=project; AUTO_INDEX=auto; UI=false; DRY_RUN=false; BACKUP=false
FORCE=false; SUPPLIED_BINARY="${CBM_POWERPACK_BINARY:-}"
usage() { echo "Usage: $0 --target PATH [--scope project|user] [--auto-index on|off|auto] [--ui] [--binary PATH] [--dry-run] [--backup] [--force]"; }
while (($#)); do
  case "$1" in
    --target) TARGET="${2:?}"; shift 2;;
    --scope) SCOPE="${2:?}"; shift 2;;
    --auto-index) AUTO_INDEX="${2:?}"; shift 2;;
    --ui) UI=true; shift;;
    --binary) SUPPLIED_BINARY="${2:?}"; shift 2;;
    --dry-run) DRY_RUN=true; shift;;
    --backup) BACKUP=true; shift;;
    --force) FORCE=true; shift;;
    --help|-h) usage; exit 0;;
    *) die "unknown install option: $1";;
  esac
done
[[ -n "$TARGET" ]] || die "--target is required"
[[ "$SCOPE" == project || "$SCOPE" == user ]] || die "invalid --scope: $SCOPE"
[[ "$AUTO_INDEX" == on || "$AUTO_INDEX" == off || "$AUTO_INDEX" == auto ]] || die "invalid --auto-index: $AUTO_INDEX"
resolve_layout "$TARGET" "$SCOPE"

if $DRY_RUN; then
  echo "DRY-RUN: install codebase-memory $VERSION"
  echo "  binary: $BIN_PATH"
  echo "  config: $CONFIG_PATH"
  echo "  cache:  $CACHE_DIR"
  "$HERE/configure.sh" --target "$TARGET" --scope "$SCOPE" --binary "$BIN_PATH" --dry-run >/dev/null
  exit 0
fi

mkdir -p "$TOOLS_DIR" "$CACHE_DIR" "$STATE_DIR"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

install_from_file() {
  local src="$1"
  [[ -f "$src" ]] || die "binary not found: $src"
  cp "$src" "$BIN_PATH"
  chmod 0755 "$BIN_PATH"
}

if [[ -n "$SUPPLIED_BINARY" ]]; then
  install_from_file "$SUPPLIED_BINARY"
elif [[ -x "$DIST_ROOT/sources/codebase-memory-mcp-main/build/c/codebase-memory-mcp" ]]; then
  install_from_file "$DIST_ROOT/sources/codebase-memory-mcp-main/build/c/codebase-memory-mcp"
elif [[ -x "$BIN_PATH" && "$FORCE" == false ]]; then
  ok "reusing managed binary $BIN_PATH"
else
  os="$(uname -s | tr '[:upper:]' '[:lower:]')"
  case "$os" in linux|darwin) ;; *) die "unsupported OS: $os";; esac
  case "$(uname -m)" in x86_64|amd64) arch=amd64;; arm64|aarch64) arch=arm64;; *) die "unsupported architecture: $(uname -m)";; esac
  key="$os-$arch"
  IFS=$'\t' read -r archive pinned_expected < <(python3 -c 'import json,sys; x=json.load(open(sys.argv[1]))[sys.argv[2]][sys.argv[3]]; print(x["name"]+"\t"+x["sha256"])' "$HERE/checksums.json" "$($UI && echo ui_artifacts || echo artifacts)" "$key")
  base="${CBM_POWERPACK_RELEASE_BASE_URL:-https://github.com/DeusData/codebase-memory-mcp/releases/download/v$VERSION}"
  fetch() { if command -v curl >/dev/null; then curl -fL --retry 2 -o "$2" "$1"; elif command -v wget >/dev/null; then wget -O "$2" "$1"; else die "curl or wget required"; fi; }
  fetch "$base/checksums.txt" "$tmp/checksums.txt"
  fetch "$base/$archive" "$tmp/$archive"
  expected="$(awk -v name="$archive" '$2==name || $2=="*"name {print $1}' "$tmp/checksums.txt" | head -n1)"
  [[ "$expected" =~ ^[0-9a-fA-F]{64}$ ]] || die "no trusted checksum for $archive"
  [[ "${expected,,}" == "${pinned_expected,,}" ]] || die "upstream checksum manifest differs from pinned checksum for $archive"
  actual="$(sha256_file "$tmp/$archive")"
  [[ "${actual,,}" == "${expected,,}" ]] || die "checksum mismatch for $archive"
  tar -tzf "$tmp/$archive" | awk '/^\// || /(^|\/)\.\.($|\/)/ { bad=1 } END { exit bad }' || die "unsafe archive paths"
  tar -xzf "$tmp/$archive" -C "$tmp/extracted" 2>/dev/null || { mkdir -p "$tmp/extracted"; tar -xzf "$tmp/$archive" -C "$tmp/extracted"; }
  found="$(find "$tmp/extracted" -type f -name codebase-memory-mcp -print -quit)"
  [[ -n "$found" ]] || die "archive did not contain codebase-memory-mcp"
  install_from_file "$found"
fi

"$BIN_PATH" --version >/dev/null 2>&1 || die "installed binary cannot run"
cfg=(--target "$TARGET" --scope "$SCOPE" --binary "$BIN_PATH")
$BACKUP && cfg+=(--backup)
$UI && cfg+=(--ui)
"$HERE/configure.sh" "${cfg[@]}"

resolved_auto="$AUTO_INDEX"
if [[ "$AUTO_INDEX" == auto ]]; then
  file_count="$(python3 - "$TARGET" <<'PY'
import os, sys
skip_dirs={'.git','node_modules','vendor','.venv','venv','dist','build','target','__pycache__','.cache'}
secret_suffixes=('.pem','.key','.p12','.pfx')
count=0
for base, dirs, files in os.walk(sys.argv[1]):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for name in files:
        low=name.lower()
        if low == '.env' or low.startswith('.env.') or low.startswith(('credentials','secrets','id_rsa')) or low.endswith(secret_suffixes):
            continue
        count += 1
        if count > 50000: break
    if count > 50000: break
print(count)
PY
)"
  if (( file_count > 0 && file_count <= 50000 )); then resolved_auto=on; else resolved_auto=off; fi
fi
if [[ "$resolved_auto" == on ]]; then
  CBM_CACHE_DIR="$CACHE_DIR" "$BIN_PATH" config set auto_index true >/dev/null
else
  CBM_CACHE_DIR="$CACHE_DIR" "$BIN_PATH" config set auto_index false >/dev/null
fi
backup_json="$(python3 - "$CONFIG_PATH" "$AGENTS_PATH" <<'PY'
import glob, json, sys
print(json.dumps(sorted(glob.glob(sys.argv[1]+'.powerpack-backup-*') + glob.glob(sys.argv[2]+'.powerpack-backup-*'))))
PY
)"
write_state "$AUTO_INDEX" "$UI" "$SCOPE" "$backup_json"
if [[ "$AUTO_INDEX" == on ]]; then "$HERE/index.sh" --target "$TARGET" --scope "$SCOPE"; fi
"$HERE/verify.sh" --target "$TARGET" --scope "$SCOPE"
