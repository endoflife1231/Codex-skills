#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$ROOT/dist"
OUTDIR="$ROOT/release/out"
PKGROOT="$OUTDIR/codex-powerpack"
ZIP="$OUTDIR/codex-powerpack.zip"
MANIFEST="$OUTDIR/release-manifest.json"
SUMS="$OUTDIR/SHA256SUMS"

python3 "$DIST/verify/validate_dist.py"

rm -rf "$PKGROOT" "$ZIP" "$MANIFEST" "$SUMS"
mkdir -p "$PKGROOT"

cp -R "$DIST" "$PKGROOT/dist"
cp -R "$ROOT/build" "$PKGROOT/build"

python3 - <<'PY' "$ROOT" "$PKGROOT" "$MANIFEST"
import json, os, sys, hashlib
from datetime import datetime, timezone
from pathlib import Path
root = Path(sys.argv[1])
pkgroot = Path(sys.argv[2])
manifest = Path(sys.argv[3])
files = []
for p in sorted(pkgroot.rglob('*')):
    if p.is_file():
        rel = p.relative_to(pkgroot).as_posix()
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        files.append({'path': rel, 'sha256': sha, 'size': p.stat().st_size})
manifest.write_text(json.dumps({
    'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'package_root': pkgroot.name,
    'file_count': len(files),
    'files': files
}, indent=2) + '\n', encoding='utf-8')
PY

(cd "$OUTDIR" && zip -qr "$(basename "$ZIP")" "$(basename "$PKGROOT")" "$(basename "$MANIFEST")")

python3 - <<'PY' "$ZIP" "$MANIFEST" "$SUMS"
import hashlib, sys
from pathlib import Path
zip_path = Path(sys.argv[1])
manifest = Path(sys.argv[2])
sums = Path(sys.argv[3])
def h(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()
sums.write_text(
    f"{h(zip_path)}  {zip_path.name}\n{h(manifest)}  {manifest.name}\n",
    encoding='utf-8'
)
PY

echo "[release] built: $ZIP"
echo "[release] manifest: $MANIFEST"
echo "[release] checksums: $SUMS"
