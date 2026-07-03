---
name: design-taste-frontend
description: Design or redesign distinctive production landing pages, portfolios, campaigns, editorial sites, and brand-led frontend experiences without generic AI aesthetics. Use for marketing-oriented web design, art direction, image-first website workflows, premium visual systems, or an explicitly requested minimalist, brutalist, high-end, GSAP, mobile-concept, brand-kit, or Google Stitch mode. Prefer impeccable for dashboards and existing product UI audits, and huashu-design for HTML prototypes, decks, animation, or narrated media.
---

# Design Taste Frontend

Build production-quality brand and marketing interfaces with a deliberate visual concept, real hierarchy, and implementation discipline. This skill consolidates the strongest non-legacy Taste modes behind one router so the large pack exposes one clear trigger instead of many overlapping skills.

## When to use and boundaries

- Use for landing pages, portfolios, campaigns, editorial pages, brand sites, and visually led frontend redesigns.
- Use `$impeccable` for dashboards, tools, settings, forms, onboarding, product UI, accessibility audits, and targeted production hardening.
- Use `$huashu-design` for high-fidelity prototypes, HTML presentations, motion pieces, video/GIF export, or narrated explainers.
- Use `$imagegen` directly for a standalone raster asset that does not require a frontend art-direction workflow.
- Do not apply a named visual style merely because it exists. The brief and existing brand context control the choice.

## Workflow

1. Inspect the brief, repository, design system, representative components, assets, and content.
2. State a one-line design read: audience, desired feeling, visual lane, and what must be avoided.
3. Choose one primary mode from the routing table. Combine a second mode only when it supplies a distinct capability rather than another competing aesthetic.
4. Define a compact system: typography, palette, spacing, grid, surfaces, imagery, interaction, and responsive behavior.
5. Implement with the existing stack. Verify dependencies before importing libraries; do not silently replace the framework or design system.
6. Use real content and realistic states. Preserve identity and functionality during redesigns.
7. Test keyboard access, contrast, reduced motion, responsive breakpoints, overflow, loading/error/empty states, and relevant project checks.
8. Compare the result against the design read and remove generic filler before delivery.

## Mode routing

Read only the selected reference:

- **Core marketing/frontend direction**: `references/core-upstream.md`. Default for landing pages, portfolios, campaigns, and broad brand-led redesigns.
- **Existing marketing-site redesign**: `references/redesign.md`. Audit first and preserve functional behavior.
- **Image-first website to code**: `references/image-to-code.md`. Use when the user wants generated visual references followed by implementation.
- **Website reference images only**: `references/imagegen-web.md`.
- **Mobile screen concepts only**: `references/imagegen-mobile.md`.
- **Brand-kit boards and identity worlds**: `references/brandkit.md`.
- **Industrial brutalism**: `references/industrial-brutalist.md`, only when requested or strongly justified by the brief.
- **Editorial minimalism**: `references/minimalist.md`, only when requested or justified.
- **High-end expressive visual mode**: `references/high-end-visual.md`. Treat exact fonts and effects as suggestions, never assumed installed assets.
- **GSAP-heavy motion direction**: `references/gsap-motion.md`. Use deterministic choices derived from the brief; never pretend to execute code that was not run.
- **Google Stitch DESIGN.md output**: `references/stitch.md`, only when Stitch is the requested target.

The legacy v1 skill and `full-output-enforcement` were intentionally excluded. They duplicate the current workflow and conflict with Codex response, context, and completion controls.

## Image generation

- When a selected mode requires raster generation or image editing, explicitly use `$imagegen` and follow its tool workflow.
- Obtain user approval at the decision points required by the selected mode; do not generate a large batch before the direction is settled.
- Keep UI text, controls, logos, charts, and layout chrome semantic whenever code can render them cleanly.
- Generate or source production assets at their intended aspect ratio and sufficient resolution. Do not ship tiny crops from a full-page mock.
- Never imitate a living designer's exact style. Translate references into high-level attributes such as hierarchy, restraint, geometry, material, or rhythm.

## Design discipline

- Avoid the default AI attractors: purple gradients, gratuitous glass, repeated rounded cards, floating decorative pills, fake metrics, generic testimonials, and uniform section rhythm.
- Do not ban a font, icon library, gradient, or component pattern categorically when the project already uses it well. Context and identity preservation win over upstream absolutism.
- Prefer a small number of strong compositional decisions over dense decoration.
- Keep headings readable on a small laptop, preserve meaningful whitespace, and prevent hero content from falling below the first viewport without intent.
- Use motion to explain hierarchy or state. Respect `prefers-reduced-motion` and avoid expensive scroll effects on constrained devices.
- Do not install or import GSAP, icon packs, fonts, component systems, or image libraries until the repository confirms them or the user approves installation.

## Redesign rule

For an existing site, inventory what must remain: information architecture, URLs, copy, analytics hooks, accessibility semantics, component contracts, and brand assets. Make targeted changes unless the user explicitly authorizes a larger redesign. Validate that behavior remains intact.

## Delivery

Ship working code or the explicitly requested visual artifact. Report the selected mode, files changed, checks run, and any generated or externally sourced assets. Do not return an aesthetic manifesto in place of implementation.
