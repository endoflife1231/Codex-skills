---
name: seo-unlighthouse
description: Multi-page Lighthouse audit via the MIT-licensed Unlighthouse CLI. Free-tier alternative to running
  PageSpeed against every URL on a site — no API quota burn, runs locally.
metadata:
  version: 2.2.0
---

# seo-unlighthouse

## Codex portability rules

- Invoke this workflow with the `$skill-name` shown by Codex; legacy `$seo ...` examples below are mapped to the corresponding `$seo-*` skill.
- Shared Python helpers live under `.agents/vendor/claude-seo/scripts/`. Run only the helper required for the current task.
- Check network access, Python dependencies, credentials, paid API budget, browser/MCP availability, and user approval before external calls. Never fabricate live SEO data.
- Codex custom SEO agents live in `.codex/agents/seo_*.toml`. Spawn them only when the user explicitly requests subagents or parallel analysis; otherwise execute the same checks inline and sequentially.
- Treat source-provided dates, thresholds, platform behavior, and API capabilities as claims to verify against current primary documentation when material.


Run Lighthouse against every URL on a site (up to a configurable cap)
and aggregate the results. Useful when:

- PageSpeed Insights' free quota (25k QPD) isn't enough for a large site.
- You want offline / local CWV measurement (CI integration, restricted environments).
- You need a quick site-wide regression check after a deploy.

## Prerequisites

- Complete the Node/browser preflight in `references/UNLIGHTHOUSE-SETUP.md` (no API key needed).
- Node 18+ on `$PATH`.

## Routing

| Command | Effect |
|---|---|
| `$seo-unlighthouse <url>` | Mobile audit, up to 200 routes, JSON+HTML report in a temp dir |
| `$seo-unlighthouse <url> --device desktop` | Desktop form factor |
| `$seo-unlighthouse <url> --max-routes 50 --output-dir ./reports` | Cap + persist |

All flags forward to `.agents/vendor/claude-seo/scripts/unlighthouse_run.py` which handles
url_safety pre-flight and subprocess timeout management.

## Output handling

The wrapper reads `ci-result.json` from the Unlighthouse output dir and
returns it parsed. Aggregate fields:

- `score.performance` (median across audited routes)
- `score.accessibility`, `score.bestPractices`, `score.seo`
- Per-route breakdown is available in `<output_dir>/ci-result.json`

## Cross-skill delegation

- For single-URL field data (CrUX), use `seo-google psi` / `seo-google crux`.
- For LCP subpart decomposition on slow pages, use the
  `.agents/vendor/claude-seo/scripts/lcp_subparts.py` workflow (Phase C).
