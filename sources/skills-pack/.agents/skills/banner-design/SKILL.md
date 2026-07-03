---
name: banner-design
description: Design MythicTable campaign banners, login heroes, thumbnails, and promotional visuals using the project design system and image-generation tools.
metadata:
  codex_migration: '2026-06-27'
  source_path: skills/.curated/banner-design/SKILL.md
---

# MythicTable Banner Design

Use this skill for bundled visual assets, not for user-uploaded campaign maps.

## Inputs

Determine purpose, target dimensions, required text, safe areas, and whether the output belongs to Tactical Clean UI or an optional Arcane Dark treatment. Ask only when a missing choice would materially change the composition.

## Workflow

1. Read `mythictable-design-workflow`, `brand`, and `design-system`.
2. Define one clear focal point and reserve safe space for UI overlays.
3. Generate original art with the available image-generation tool; do not imitate copyrighted D&D artwork, logos, named characters, or published maps.
4. Keep text out of generated raster art unless the text is decorative and disposable. Add product copy in HTML/Figma for clarity and localization.
5. Export source-quality art plus web variants.
6. Verify crop behavior, contrast behind text, file size, and provenance metadata.

## Project asset targets

- Login hero: 16:10 or 3:2, subject weighted away from the sign-in panel.
- Campaign banner: 3:1, center-safe crop and subdued details under text.
- Scene thumbnail: 16:9, readable at 320px width.
- Character placeholder: square portrait with a clean silhouette.

Store bundled files under `/public/assets` using semantic lowercase names. Record the generation source and prompt outside the image file for future commercial review.
