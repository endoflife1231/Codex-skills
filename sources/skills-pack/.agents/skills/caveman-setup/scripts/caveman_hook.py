#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

ALLOWED = {'off','lite','full','ultra','wenyan-lite','wenyan-full','wenyan-ultra'}


def root_from(cwd: str) -> Path:
    start = Path(cwd or os.getcwd()).resolve()
    try:
        out = subprocess.check_output(['git','-C',str(start),'rev-parse','--show-toplevel'], text=True, stderr=subprocess.DEVNULL).strip()
        if out: return Path(out)
    except Exception: pass
    for p in (start, *start.parents):
        if (p/'.agents').exists() or (p/'.git').exists(): return p
    return start


def read_json(path: Path, default: dict) -> dict:
    try:
        if path.is_symlink() or path.stat().st_size > 65536: return default
        data = json.loads(path.read_text('utf-8'))
        return data if isinstance(data, dict) else default
    except Exception:
        return default


def atomic_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.is_symlink(): return
    fd, tmp = tempfile.mkstemp(prefix=path.name+'.', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2); f.write('\n')
        os.replace(tmp, path)
    finally:
        try: os.unlink(tmp)
        except FileNotFoundError: pass


def context(mode: str) -> str:
    level = mode if mode in ALLOWED else 'full'
    base = ('CAVEMAN MODE ACTIVE ('+level+'). Keep user language. Remove filler and repeated context. '
            'Preserve exact code, commands, identifiers, paths, numbers, constraints, warnings, and evidence. '
            'Use normal complete prose for security, destructive actions, migrations, or ambiguity. '
            'Do not alter code style. User can say stop caveman or normal mode.')
    if level == 'lite': return base + ' Use concise complete sentences.'
    if level == 'ultra': return base + ' Use shortest unambiguous fragments; no invented abbreviations.'
    if level.startswith('wenyan'): return base + ' Use requested classical-Chinese register only where it remains clear.'
    return base + ' Fragments are allowed when unambiguous.'


def emit(event: str, text: str) -> None:
    print(json.dumps({'hookSpecificOutput': {'hookEventName': event, 'additionalContext': text}}, ensure_ascii=False))


def requested_mode(prompt: str):
    low = prompt.lower().strip()
    if re.search(r'\b(stop|disable|deactivate|turn off)\b.*\bcaveman\b|\bcaveman\b.*\b(stop|disable|deactivate|turn off)\b|\bnormal mode\b', low):
        return 'off'
    if '$caveman' not in low and 'caveman mode' not in low and 'talk like caveman' not in low:
        return None
    for mode in ('wenyan-ultra','wenyan-full','wenyan-lite','ultra','full','lite'):
        if mode in low: return mode
    return 'full'


def main() -> int:
    try: data = json.load(sys.stdin)
    except Exception: return 0
    event = data.get('hook_event_name')
    root = root_from(data.get('cwd',''))
    config = read_json(root/'.codex'/'caveman.json', {'default_mode':'off','auto_activate':False})
    default = config.get('default_mode','off')
    if default not in ALLOWED: default = 'off'
    state_path = root/'.codex'/'.caveman-state.json'
    state = read_json(state_path, {})
    active = state.get('active_mode') if state.get('active_mode') in ALLOWED else None

    if event == 'SessionStart':
        if config.get('auto_activate') and default != 'off':
            active = default
            atomic_json(state_path, {'active_mode': active})
        if active and active != 'off': emit('SessionStart', context(active))
        return 0

    if event == 'UserPromptSubmit':
        req = requested_mode(str(data.get('prompt','')))
        if req == 'off':
            try: state_path.unlink()
            except FileNotFoundError: pass
            return 0
        if req:
            active = req
            atomic_json(state_path, {'active_mode': active})
        if active and active != 'off': emit('UserPromptSubmit', context(active))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
