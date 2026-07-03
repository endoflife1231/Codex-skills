# Careful Execution

This reference adapts the strongest useful safety guidance from Claude-derived material into Codex-native terms.

## Default mindset

- local, reversible actions are normal engineering work
- destructive, externally visible, or hard-to-reverse actions require a higher bar
- when scope is unclear, match the action to the narrowest confirmed user intent

## Actions that deserve explicit pause

- deleting files, branches, or local work
- force-push, reset, or history rewrite
- changing external systems, CI, permissions, or infrastructure
- publishing code, comments, messages, or artifacts to shared systems
- rotating secrets or changing auth-related configuration

## Better behavior when blocked

- investigate root cause instead of forcing past safety controls
- do not treat destructive shortcuts as the default fix
- preserve unexpected user state until it is understood
