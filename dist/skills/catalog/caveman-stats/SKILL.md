---
name: caveman-stats
description: >-
  Compare an original text file with a Caveman-compressed version and report deterministic byte, character, and word savings plus a clearly labeled rough token estimate. Trigger only on $caveman-stats or an explicit compression-statistics request.
metadata:
  source: JuliusBrussee/caveman
  license: MIT
  codex_migration: '2026-06-27'
---

# Caveman Stats

Measure a concrete original/compressed file pair:

```bash
python3 .agents/skills/caveman-stats/scripts/stats.py "<original>" "<compressed>"
```

Report bytes, characters, words, and percentage reduction. The script's token field is only `ceil(characters / 4)` and must be labeled a rough estimate, not actual Codex tokenizer output or billing data.

When used after `$caveman-compress`, compare the `backup` and final source paths returned by the compression workflow.

## Migration note

The upstream `caveman-stats` parsed Claude Code session logs. Codex transcript format is not a stable public hook interface, so this migration deliberately avoids claiming exact session-token savings. Do not scrape private or unstable transcript files unless the user explicitly supplies one and understands the limitation.
