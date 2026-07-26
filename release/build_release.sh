#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(tr -d '[:space:]' < "$ROOT/VERSION")"
OUT="$ROOT/release/out"
STAGE="$OUT/stage"
USER_ROOT="$STAGE/codex-powerpack-v$VERSION"
REPO_ROOT="$STAGE/codex-skills-v$VERSION"
USER_ZIP="$OUT/codex-powerpack-v$VERSION-user.zip"
REPO_ZIP="$OUT/codex-powerpack-v$VERSION-repository.zip"
USER_MANIFEST="$OUT/user-manifest.json"
REPO_MANIFEST="$OUT/repository-manifest.json"
SUMS="$OUT/SHA256SUMS"

python3 "$ROOT/dist/verify/validate_dist.py"
rm -rf "$OUT"
mkdir -p "$USER_ROOT" "$REPO_ROOT" "$OUT"

for item in README.md README.ru.md LICENSE THIRD_PARTY_NOTICES.md OPEN_SOURCE_AUDIT.md VERSION install.sh update.sh uninstall.sh adapt-project.sh rollback.sh verify.sh; do
  cp -a "$ROOT/$item" "$USER_ROOT/$item"
done
cp -a "$ROOT/dist" "$USER_ROOT/dist"
python3 - "$USER_ROOT/dist" <<'PYPRUNE'
import shutil, sys
from pathlib import Path
root=Path(sys.argv[1])
for p in sorted(root.rglob('*'), reverse=True):
    if p.is_dir() and p.name in {'tests', 'test', 'evals', '__pycache__'}:
        shutil.rmtree(p, ignore_errors=True)
    elif p.is_file() and (p.name.startswith('coverage') and p.suffix=='.json'):
        p.unlink(missing_ok=True)
PYPRUNE

python3 - "$USER_ROOT" "$USER_MANIFEST" <<'PYMANIFEST'
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
root=Path(sys.argv[1]); out=Path(sys.argv[2]); files=[]
for p in sorted(root.rglob('*')):
    if p.is_file():
        files.append({'path':p.relative_to(root).as_posix(),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
out.write_text(json.dumps({'generated_at':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),'package_root':root.name,'file_count':len(files),'files':files},indent=2)+'\n')
PYMANIFEST
cp "$USER_MANIFEST" "$USER_ROOT/MANIFEST.json"
(cd "$STAGE" && zip -qyr "$USER_ZIP" "$(basename "$USER_ROOT")")

python3 - "$ROOT" "$REPO_ROOT" <<'PYCOPY'
import shutil, sys
from pathlib import Path
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
ignore=shutil.ignore_patterns('.git','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','release/out','.DS_Store')
for p in src.iterdir():
    if p.name in {'.git'}: continue
    if p.name=='release':
        shutil.copytree(p,dst/p.name,ignore=shutil.ignore_patterns('out'),dirs_exist_ok=True)
    elif p.is_dir():
        shutil.copytree(p,dst/p.name,ignore=ignore,dirs_exist_ok=True)
    elif p.is_file():
        shutil.copy2(p,dst/p.name)
PYCOPY
mkdir -p "$REPO_ROOT/release/out"
cp "$USER_ZIP" "$USER_MANIFEST" "$REPO_ROOT/release/out/"
python3 - "$REPO_ROOT" "$REPO_MANIFEST" <<'PYMANIFEST'
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
root=Path(sys.argv[1]); out=Path(sys.argv[2]); files=[]
for p in sorted(root.rglob('*')):
    if p.is_file():
        files.append({'path':p.relative_to(root).as_posix(),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
out.write_text(json.dumps({'generated_at':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),'package_root':root.name,'file_count':len(files),'files':files},indent=2)+'\n')
PYMANIFEST
cp "$REPO_MANIFEST" "$REPO_ROOT/release/out/repository-manifest.json"
(cd "$STAGE" && zip -qyr "$REPO_ZIP" "$(basename "$REPO_ROOT")")

python3 - "$USER_ZIP" "$REPO_ZIP" "$USER_MANIFEST" "$REPO_MANIFEST" "$SUMS" <<'PYSUM'
import hashlib, sys
from pathlib import Path
paths=[Path(x) for x in sys.argv[1:-1]]; out=Path(sys.argv[-1])
out.write_text(''.join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in paths))
PYSUM
rm -rf "$STAGE"
printf '[release] %s\n' "$USER_ZIP" "$REPO_ZIP" "$SUMS"
