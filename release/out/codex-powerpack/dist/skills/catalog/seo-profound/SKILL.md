---
name: seo-profound
description: Profound LLM citation tracker (extension). Time-series brand citation rates across ChatGPT, Perplexity,
  and other LLMs. Pairs with seo-seranking for triangulated AI visibility coverage.
metadata:
  version: 2.2.0
---

# seo-profound

## Codex portability rules

- Invoke this workflow with the `$skill-name` shown by Codex; legacy `$seo ...` examples below are mapped to the corresponding `$seo-*` skill.
- Shared Python helpers live under `.agents/vendor/claude-seo/scripts/`. Run only the helper required for the current task.
- Check network access, Python dependencies, credentials, paid API budget, browser/MCP availability, and user approval before external calls. Never fabricate live SEO data.
- Codex custom SEO agents live in `.codex/agents/seo_*.toml`. Spawn them only when the user explicitly requests subagents or parallel analysis; otherwise execute the same checks inline and sequentially.
- Treat source-provided dates, thresholds, platform behavior, and API capabilities as claims to verify against current primary documentation when material.


Profound is purpose-built for LLM brand-mention tracking. While
SE Ranking samples prompts on demand, Profound continuously polls and
publishes time-series so trend deltas (week-over-week, month-over-month)
are first-class.

## Prerequisites

- Export `PROFOUND_API_KEY` as described in `references/PROFOUND-SETUP.md`.
- Profound API key.
- Before any tool call, confirm `PROFOUND_API_KEY` exists in the current process environment without printing it.

## Routing

| Command | Purpose |
|---|---|
| `$seo-profound citations <brand>` | Current citation rate per LLM + 30-day trend |
| `$seo-profound prompts <brand>` | Top prompts that surface (or fail to surface) the brand |
| `$seo-profound competitors <brand>` | Brands cited alongside `brand` for the same prompts |
| `$seo-profound alerts <brand>` | Spike/drop alerts vs. 7-day baseline |

## Output conventions

- Cite Profound on every metric: "Profound (live, confidence 0.90)".
- Profound covers ChatGPT + Perplexity natively; for Gemini / AI
  Overviews / AI Mode coverage, defer to `seo-seranking`.
- For Google AI Overviews citation rate, also cross-reference
  `seo-dataforseo` AI visibility tools when available.

## Cross-skill delegation

- For end-to-end AI search audit (passage citability + brand mentions + platform-specific tuning), hand back to `seo-geo`.
- For prompt-set design + AI Cleanup pattern detection in cited content, fall back to `seo-content`.
