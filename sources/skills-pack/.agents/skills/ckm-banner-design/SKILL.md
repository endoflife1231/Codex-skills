---
name: ckm-banner-design
description: Design banners for social media, ads, website heroes, campaigns, and print in multiple art directions; adapted from ClaudeKit for Codex.
license: MIT
metadata:
  author: claudekit
  version: 1.0.0
  argument_hint: '[platform] [style] [dimensions]'
  codex_migration: '2026-06-27'
  source_path: skills/.curated/ui-ux/.claude/skills/banner-design/SKILL.md
  source_name: ckm:banner-design
---

# Banner Design — Multi-Format Codex Workflow

Create campaign banners, social covers, ads, website heroes, and print-oriented banner compositions. This workflow does not publish assets or replace approved brand files without explicit user approval.

## Inputs

Ask focused questions in chat only for missing decisions:
- purpose and target platform;
- exact dimensions and safe zones;
- exact headline, supporting text, CTA, and required logos;
- existing brand guidelines/tokens;
- raster, HTML/CSS, SVG, or editable-source expectation;
- number of concepts and final file format.

## Workflow

1. Read `references/banner-sizes-and-styles.md` for platform dimensions and composition constraints.
2. Load `$brand`/`$design-system` when project brand rules exist.
3. Propose two or three materially different art directions and state the trade-offs. Ask for a choice when the direction affects substantial work.
4. Build the composition with `$frontend-ui-engineering` or `$ui-styling` when HTML/CSS is appropriate.
5. Generate required raster backgrounds or illustrations with `$imagegen`. Preserve exact text for the code/layout layer rather than relying on generated image text.
6. Verify contrast, safe zones, crop behavior, responsive scaling, and the exact target dimensions.
7. Use `$browser-testing-with-devtools` or `$playwright` for browser-backed screenshots only when the browser dependency is configured.
8. Save finals under a project path such as `assets/banners/<campaign>/`, using non-destructive versioned names.

## Export guidance

- Prefer browser screenshots for HTML/CSS banner compositions.
- Prefer SVG for deterministic vector artwork.
- Prefer PNG/WebP for raster delivery; preserve an editable source when the user needs future revisions.
- Do not claim pixel-perfect export unless the exact viewport and output dimensions were verified.

## Completion report

List:
- selected art direction;
- dimensions and platform;
- source files and final exported files;
- brand tokens/assets used;
- verification performed and anything not verified.
