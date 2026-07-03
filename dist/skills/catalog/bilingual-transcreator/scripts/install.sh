#!/usr/bin/env bash
set -euo pipefail
force=false
[[ "${1:-}" == "--force" ]] && force=true
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/.." && pwd)"
dest="$HOME/.agents/skills/bilingual-transcreator"
mkdir -p "$(dirname "$dest")"
if [[ -e "$dest" && "$force" != true ]]; then
  echo "Refusing to overwrite $dest. Re-run with --force." >&2
  exit 1
fi
rm -rf "$dest"
cp -R "$skill_dir" "$dest"
echo "Installed for Codex: $dest"
