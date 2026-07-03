#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from detect import detect_file_type, should_compress
from validate import validate

SENSITIVE_BASENAME = re.compile(
    r"(?ix)^(\.env(\..+)?|\.netrc|credentials(\..+)?|secrets?(\..+)?|passwords?(\..+)?|"
    r"id_(rsa|dsa|ecdsa|ed25519)(\.pub)?|authorized_keys|known_hosts|"
    r".*\.(pem|key|p12|pfx|crt|cer|jks|keystore|asc|gpg))$"
)
SENSITIVE_COMPONENTS = {'.ssh', '.aws', '.gnupg', '.kube', '.docker'}
SENSITIVE_TOKENS = ('secret', 'credential', 'password', 'passwd', 'apikey', 'accesskey', 'privatekey')


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def repo_root(start: Path) -> Path:
    try:
        out = subprocess.check_output(['git', '-C', str(start), 'rev-parse', '--show-toplevel'], text=True, stderr=subprocess.DEVNULL).strip()
        if out:
            return Path(out).resolve()
    except Exception:
        pass
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent
    for p in (cur, *cur.parents):
        if (p / '.git').exists() or (p / '.agents').exists():
            return p
    return cur


def sensitive(path: Path) -> bool:
    if SENSITIVE_BASENAME.match(path.name):
        return True
    lowered = {p.lower() for p in path.parts}
    if lowered & SENSITIVE_COMPONENTS:
        return True
    compact = re.sub(r'[_\-\s.]', '', path.name.lower())
    return any(t in compact for t in SENSITIVE_TOKENS)


def safe_json(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def prepare(source: Path) -> int:
    source = source.expanduser().resolve()
    if not source.exists() or not source.is_file():
        raise SystemExit(f'not a file: {source}')
    if sensitive(source):
        raise SystemExit('refused: path appears to contain secrets or credentials')
    if not should_compress(source):
        raise SystemExit(f'refused: detected {detect_file_type(source)}, not natural-language text')
    if source.stat().st_size > 2 * 1024 * 1024:
        raise SystemExit('refused: file exceeds 2 MiB safety limit')

    root = repo_root(source.parent)
    rel = str(source.relative_to(root)) if source.is_relative_to(root) else source.name
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    key = hashlib.sha256(str(source).encode()).hexdigest()[:12]
    run_dir = root / '.codex' / 'caveman-backups' / key / stamp
    run_dir.mkdir(parents=True, exist_ok=False)
    backup = run_dir / f'{source.name}.original'
    candidate = run_dir / f'{source.name}.candidate'
    meta = run_dir / 'meta.json'
    shutil.copy2(source, backup)
    shutil.copy2(source, candidate)
    meta.write_text(json.dumps({
        'source': str(source),
        'relative_source': rel,
        'original_sha256': sha256(source),
        'backup': str(backup),
        'candidate': str(candidate),
        'created_utc': stamp,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    safe_json({'status': 'prepared', 'source': str(source), 'backup': str(backup), 'candidate': str(candidate), 'meta': str(meta)})
    return 0


def load_meta(meta_path: Path) -> dict:
    data = json.loads(meta_path.read_text('utf-8'))
    for k in ('source', 'original_sha256', 'backup', 'candidate'):
        if not isinstance(data.get(k), str) or not data[k]:
            raise SystemExit(f'invalid meta: missing {k}')
    return data


def validate_cmd(meta_path: Path) -> int:
    data = load_meta(meta_path.resolve())
    backup = Path(data['backup'])
    candidate = Path(data['candidate'])
    if not backup.exists() or not candidate.exists():
        raise SystemExit('backup or candidate missing')
    res = validate(backup, candidate)
    safe_json({'valid': res.is_valid, 'errors': res.errors, 'warnings': res.warnings,
               'original_bytes': backup.stat().st_size, 'candidate_bytes': candidate.stat().st_size})
    return 0 if res.is_valid else 2


def apply_cmd(meta_path: Path) -> int:
    data = load_meta(meta_path.resolve())
    source = Path(data['source'])
    backup = Path(data['backup'])
    candidate = Path(data['candidate'])
    if sha256(source) != data['original_sha256']:
        raise SystemExit('refused: source changed after prepare; start a new compression run')
    res = validate(backup, candidate)
    if not res.is_valid:
        safe_json({'status': 'refused', 'errors': res.errors, 'warnings': res.warnings})
        return 2
    fd, tmp_name = tempfile.mkstemp(prefix=source.name + '.', suffix='.tmp', dir=str(source.parent))
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        shutil.copy2(candidate, tmp)
        os.replace(tmp, source)
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass
    safe_json({'status': 'applied', 'source': str(source), 'backup': str(backup),
               'before_bytes': backup.stat().st_size, 'after_bytes': source.stat().st_size,
               'warnings': res.warnings})
    return 0


def restore(meta_path: Path) -> int:
    data = load_meta(meta_path.resolve())
    source = Path(data['source'])
    backup = Path(data['backup'])
    if not backup.exists():
        raise SystemExit('backup missing')
    shutil.copy2(backup, source)
    safe_json({'status': 'restored', 'source': str(source), 'backup': str(backup)})
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description='Safe local workflow helper for $caveman-compress')
    sub = p.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('prepare'); a.add_argument('source', type=Path)
    for name in ('validate', 'apply', 'restore'):
        q = sub.add_parser(name); q.add_argument('meta', type=Path)
    ns = p.parse_args()
    if ns.cmd == 'prepare': return prepare(ns.source)
    if ns.cmd == 'validate': return validate_cmd(ns.meta)
    if ns.cmd == 'apply': return apply_cmd(ns.meta)
    if ns.cmd == 'restore': return restore(ns.meta)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
