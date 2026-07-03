# Editing Discipline

This reference adapts the useful editing discipline from Claude-derived tool guidance into Codex-native practice.

## Read before overwrite

- read existing files before replacing or heavily editing them
- prefer targeted edits over full rewrites unless a full replacement is truly the cleanest path
- preserve unrelated user changes and established local conventions

## Proportionate editing

- keep the diff as small as possible while still solving the real problem
- avoid introducing documentation, planning files, or comments unless they materially help the repository
- do not silently broaden scope while editing

## Verification after editing

- after making changes, run the most relevant available verification
- if verification cannot be run, report that clearly instead of implying success
