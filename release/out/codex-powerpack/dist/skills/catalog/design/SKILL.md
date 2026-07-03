---
name: design
description: Route broad visual-design work across brand, design systems, UI styling, logos, presentations, banners, icons, and social assets.
metadata:
  codex_migration: '2026-06-27'
  source_path: skills/.curated/design/SKILL.md
---

# Design Router

Route broad visual-design work to the narrowest registered Codex skill. Do not load every design skill at once.

## Routing

| Need | Skill or local resource |
|---|---|
| Brand voice, palette, guidelines, asset rules | `$brand` or `$ckm-brand` |
| Tokens, semantic colors, spacing, typography | `$design-system` or `$ckm-design-system` |
| Production UI implementation | `$frontend-ui-engineering`, `$ui-styling`, or `$ckm-ui-styling` |
| Existing product UI audit, polish, accessibility, or live iteration | `$impeccable` |
| Brand-led landing page, portfolio, campaign, or premium marketing frontend | `$design-taste-frontend` |
| High-fidelity HTML prototype, interactive demo, deck, motion piece, or narrated explainer | `$huashu-design` |
| Raster image, illustration, texture, hero art | `$imagegen` |
| Multi-format campaign banner | `$ckm-banner-design` or `$banner-design` |
| HTML presentation / pitch deck | `$ckm-slides` |
| Broad UX research and pattern lookup | `$ui-ux-pro-max` |
| Browser screenshot or visual verification | `$browser-testing-with-devtools` or `$playwright` |
| Logo, CIP, or icon exploration using bundled datasets | the `scripts/` and `references/` directories in this skill |

## Workflow

1. Clarify the asset type, audience, destination, dimensions, exact text, brand constraints, editable format, and acceptance criteria.
2. Read only the selected sub-skill and the references needed for the chosen asset.
3. Reuse repository brand tokens and assets before inventing new ones.
4. For generated raster art, use `$imagegen`; never assume an unregistered Gemini helper or external image CLI exists.
5. For HTML/CSS output, implement with a UI skill and verify at the target viewport with a configured browser skill.
6. Save project-bound assets inside the workspace, use non-destructive filenames, and report exact paths.
7. Ask for approval before replacing existing approved brand assets or publishing externally.

## Bundled local utilities

Resolve paths from this skill directory. Typical commands:

```bash
# Search logo datasets
python3 .agents/skills/design/scripts/logo/search.py "minimal technology" --domain style

# Generate deterministic SVG/logo variants from local inputs
python3 .agents/skills/design/scripts/logo/generate.py --help

# Explore CIP deliverables
python3 .agents/skills/design/scripts/cip/search.py --help

# Generate icon variants
python3 .agents/skills/design/scripts/icon/generate.py --help
```

Inspect a script's `--help` and source before running it. Do not assume dependencies, API keys, or browser/MCP servers are present.

## Selection rules

- Prefer a narrow skill when the user already named the asset type.
- Keep the three extended design workflows separate: Impeccable owns production product UI, Design Taste owns brand/marketing frontend, and Huashu owns HTML visual artifacts and media.
- Do not randomly choose between design workflows; choose based on format and acceptance criteria.
- Use `$imagegen` for raster visuals, not placeholder HTML pretending to be an image.
- Use code-native SVG/HTML/CSS for deterministic vector or interface artifacts when that better matches the repository.
