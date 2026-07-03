---
name: seo-bing
description: Bing Webmaster Tools + IndexNow extension. Microsoft Copilot citations are fed by the Bing index; this
  skill makes Bing visibility, link data, and IndexNow URL submission first-class.
metadata:
  version: 2.2.0
---

# seo-bing

## Codex portability rules

- Invoke this workflow with the `$skill-name` shown by Codex; legacy `$seo ...` examples below are mapped to the corresponding `$seo-*` skill.
- Shared Python helpers live under `.agents/vendor/claude-seo/scripts/`. Run only the helper required for the current task.
- Check network access, Python dependencies, credentials, paid API budget, browser/MCP availability, and user approval before external calls. Never fabricate live SEO data.
- Codex custom SEO agents live in `.codex/agents/seo_*.toml`. Spawn them only when the user explicitly requests subagents or parallel analysis; otherwise execute the same checks inline and sequentially.
- Treat source-provided dates, thresholds, platform behavior, and API capabilities as claims to verify against current primary documentation when material.


The non-Google indexing surface. Google still rejects IndexNow (per
Gary Illyes, multiple SOTR episodes 2024-2025), so this skill is
specifically for **Bing/Yandex/Seznam/Naver indexing** and
**Microsoft Copilot AI citation** (which pulls from the Bing index).

## Prerequisites

- Export the required credentials as described in `references/BING-WEBMASTER-SETUP.md`.
- A Bing Webmaster Tools API key.
- Optional: an IndexNow host key (32+ chars) published at the URL
  declared as `INDEXNOW_KEY_LOCATION`.

## Routing

| Command | Underlying script |
|---|---|
| `$seo-bing links <url>` | `python3 .agents/vendor/claude-seo/scripts/bing_webmaster.py links <url>` |
| `$seo-bing compare <urlA> <urlB>` | `python3 .agents/vendor/claude-seo/scripts/bing_webmaster.py compare <urlA> <urlB>` |
| `$seo-bing submit <url>` (single URL) | `python3 .agents/vendor/claude-seo/scripts/indexnow_submit.py --host ... --urls <url>` |
| `$seo-bing submit-batch <file>` | `python3 .agents/vendor/claude-seo/scripts/indexnow_submit.py --urls-file <file>` |
| `$seo-bing verify-indexnow` | `python3 .agents/vendor/claude-seo/scripts/indexnow_submit.py --verify-only` |

## When this skill applies

- The user is publishing new pages and wants Microsoft Copilot
  citation eligibility (Bing index ingestion).
- The user wants to nudge Bing/Yandex/Seznam/Naver indexing for fresh
  URLs.
- The user is doing competitor backlink analysis and wants Bing's
  unique link data (Bing tracks links Google's API doesn't surface).

## Cross-skill delegation

- For Google indexing (very different model — sitemap-driven, no
  IndexNow), use `seo-google indexing`.
- For multi-source backlink confidence weighting, fall back to
  `seo-backlinks` which already integrates Bing + Moz + CC.
