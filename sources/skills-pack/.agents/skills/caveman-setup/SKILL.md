---
name: caveman-setup
description: >-
  Optionally install, preview, configure, or remove project-local native Codex hooks that persist Caveman mode across prompts and sessions. Trigger only on $caveman-setup or an explicit request for persistent Caveman behavior; hooks are not enabled by default.
metadata:
  source: JuliusBrussee/caveman
  license: MIT
  codex_migration: '2026-06-27'
---

# Caveman Setup

The base `$caveman` skill works without installation. Use this skill only when the user explicitly wants project-local persistence across prompts or sessions.

## Why opt-in

Codex project hooks execute commands and require trust review. This pack therefore ships the hook implementation but does not modify `.codex/hooks.json` automatically.

## Install safely

1. Preview from the repository root:

   ```bash
   python3 .agents/skills/caveman-setup/scripts/install_hooks.py --mode full
   ```

2. Explain that installation will:
   - merge two native hooks into `.codex/hooks.json` (`SessionStart`, `UserPromptSubmit`);
   - create `.codex/caveman.json`;
   - keep generated state/backups ignored;
   - require the user to review/trust the hook in Codex (`/hooks`) before it runs.
3. Apply only after explicit approval:

   ```bash
   python3 .agents/skills/caveman-setup/scripts/install_hooks.py --mode full --apply
   ```

Modes: `off`, `lite`, `full`, `ultra`, `wenyan-lite`, `wenyan-full`, `wenyan-ultra`.

Use `--no-auto-activate` to install prompt-controlled persistence without activating on every new session.

## Remove

Preview, then apply:

```bash
python3 .agents/skills/caveman-setup/scripts/install_hooks.py --remove
python3 .agents/skills/caveman-setup/scripts/install_hooks.py --remove --apply
```

The installer removes only hook groups whose command references this pack's `caveman_hook.py`; unrelated hooks are preserved. Existing `hooks.json` is backed up under `.codex/.caveman-backups/` before modification.

## Safety

- Inspect both bundled scripts before execution.
- Do not bypass Codex hook trust review.
- Do not install in an untrusted repository.
- The hook never blocks prompts, calls the network, reads secrets, or executes model APIs. It only reads its small config/state files and emits developer context.
