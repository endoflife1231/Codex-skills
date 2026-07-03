# Codex runtime notes

## Capability levels

1. HTML/CSS/JavaScript prototypes and decks use the repository's existing toolchain and need no Huashu-specific install.
2. Screenshot, PDF, PPTX, and image-processing helpers require Node dependencies declared in the skill-local `package.json`.
3. `scripts/verify.py` uses the Python Playwright package plus its Chromium runtime; prefer an already configured `$playwright` or browser workflow when available.
4. MP4/GIF and audio pipelines also require `ffmpeg` and `ffprobe` on `PATH`.
5. Narration through Doubao is optional and requires user-provided credentials. Never print, copy, or commit them.

## Preflight

Before invoking a helper, inspect the script, then check the exact executable and package it needs. If dependencies are missing, explain the capability that is unavailable and ask before installing anything.

If the user approves a skill-local install, run `npm ci` inside `.agents/skills/huashu-design`. The resulting `node_modules/` is local runtime state and must remain ignored by Git.

Do not assume that the Node `playwright` dependency also installs Python Playwright. If `verify.py` is the chosen verifier, check `python3 -c 'import playwright'` and ask before installing the Python package or browser runtime.

For FFmpeg workflows, verify both commands:

```bash
command -v ffmpeg
command -v ffprobe
```

Do not claim an export succeeded unless the output exists and its media metadata was inspected.

## Portable paths

Resolve scripts relative to `.agents/skills/huashu-design/`. Do not use upstream `.agents/skills/huashu-design` placeholders. Codex may start below the repository root, so derive the root with `git rev-parse --show-toplevel` when a stable project path is required.

## Audio policy

No stock BGM/SFX is bundled in this pack. Use project-owned audio, user-provided files, or clearly licensed sources. Record the source and license in the project deliverable when audio ships.
