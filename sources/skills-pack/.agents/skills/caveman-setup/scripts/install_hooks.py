#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil, subprocess
from datetime import datetime, timezone
from pathlib import Path

COMMAND = 'python3 "$(git rev-parse --show-toplevel)/.agents/skills/caveman-setup/scripts/caveman_hook.py"'
MODES = ('off','lite','full','ultra','wenyan-lite','wenyan-full','wenyan-ultra')


def repo_root(start: Path) -> Path:
    try:
        out = subprocess.check_output(['git','-C',str(start),'rev-parse','--show-toplevel'], text=True, stderr=subprocess.DEVNULL).strip()
        if out: return Path(out).resolve()
    except Exception: pass
    for p in (start.resolve(), *start.resolve().parents):
        if (p/'.agents').exists() or (p/'.git').exists(): return p
    return start.resolve()


def load(path: Path) -> dict:
    if not path.exists(): return {'hooks': {}}
    data = json.loads(path.read_text('utf-8'))
    if not isinstance(data, dict): raise SystemExit('hooks.json root must be an object')
    if not isinstance(data.get('hooks', {}), dict): raise SystemExit('hooks must be an object')
    data.setdefault('hooks', {})
    return data


def handler():
    return {'type':'command','command':COMMAND,'timeout':5,'statusMessage':'Loading optional Caveman mode'}


def group(event: str):
    g = {'hooks':[handler()]}
    if event == 'SessionStart': g['matcher'] = 'startup|resume|clear|compact'
    return g


def is_ours(g: object) -> bool:
    return isinstance(g, dict) and any(isinstance(h, dict) and 'caveman_hook.py' in str(h.get('command','')) for h in g.get('hooks',[]))


def updated(data: dict, remove: bool) -> dict:
    hooks = data.setdefault('hooks', {})
    for event in ('SessionStart','UserPromptSubmit'):
        current = hooks.get(event, [])
        if not isinstance(current, list): raise SystemExit(f'{event} must be a list')
        current = [g for g in current if not is_ours(g)]
        if not remove: current.append(group(event))
        if current: hooks[event] = current
        else: hooks.pop(event, None)
    return data


def backup(path: Path, root: Path) -> None:
    if not path.exists(): return
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    dst = root/'.codex'/'.caveman-backups'/f'hooks-{stamp}.json'
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dst)


def ensure_ignore(root: Path) -> None:
    p = root/'.codex'/'.gitignore'
    lines = p.read_text('utf-8').splitlines() if p.exists() else []
    for item in ('.caveman-state.json','caveman-backups/','.caveman-backups/'):
        if item not in lines: lines.append(item)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines).rstrip()+'\n','utf-8')


def main() -> int:
    p = argparse.ArgumentParser(description='Install/remove optional project-local Codex Caveman hooks')
    p.add_argument('--repo', type=Path, default=Path.cwd())
    p.add_argument('--mode', choices=MODES, default='full')
    p.add_argument('--no-auto-activate', action='store_true')
    p.add_argument('--remove', action='store_true')
    p.add_argument('--apply', action='store_true', help='write changes; without this flag only print preview')
    ns = p.parse_args()
    root = repo_root(ns.repo)
    hooks_path = root/'.codex'/'hooks.json'
    data = updated(load(hooks_path), ns.remove)
    config = {'default_mode': ns.mode, 'auto_activate': not ns.no_auto_activate}
    print(json.dumps({'repo':str(root),'action':'remove' if ns.remove else 'install','hooks':data,
                      'config':None if ns.remove else config,'will_write':ns.apply}, ensure_ascii=False, indent=2))
    if not ns.apply: return 0
    hooks_path.parent.mkdir(parents=True, exist_ok=True)
    backup(hooks_path, root)
    hooks_path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n','utf-8')
    config_path = root/'.codex'/'caveman.json'
    if ns.remove:
        try: config_path.unlink()
        except FileNotFoundError: pass
        try: (root/'.codex'/'.caveman-state.json').unlink()
        except FileNotFoundError: pass
    else:
        config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2)+'\n','utf-8')
    ensure_ignore(root)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
