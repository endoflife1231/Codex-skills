#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path


def metrics(path: Path) -> dict:
    text = path.read_text('utf-8', errors='replace')
    chars = len(text)
    return {
        'path': str(path.resolve()),
        'bytes': path.stat().st_size,
        'characters': chars,
        'words': len(text.split()),
        'estimated_tokens': math.ceil(chars / 4),
    }


def main() -> int:
    p = argparse.ArgumentParser(description='Compare original and compressed text files')
    p.add_argument('original', type=Path)
    p.add_argument('compressed', type=Path)
    ns = p.parse_args()
    a, b = metrics(ns.original), metrics(ns.compressed)
    def pct(before, after):
        return round((before - after) * 100 / before, 2) if before else 0.0
    out = {
        'original': a,
        'compressed': b,
        'savings_percent': {
            'bytes': pct(a['bytes'], b['bytes']),
            'characters': pct(a['characters'], b['characters']),
            'words': pct(a['words'], b['words']),
            'estimated_tokens': pct(a['estimated_tokens'], b['estimated_tokens']),
        },
        'note': 'estimated_tokens uses ceil(characters/4); this is not Codex billing or exact tokenizer data',
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
