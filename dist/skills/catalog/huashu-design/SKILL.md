---
name: huashu-design
description: Create high-fidelity HTML prototypes, interactive demos, slide decks, motion pieces, narrated explainers, and visual design explorations. Use for HTML-based visual artifacts, app or iOS prototypes, editable HTML presentations, animation-to-video workflows, design-direction comparisons, and expert visual critique. Prefer design-taste-frontend for production marketing pages and impeccable for existing product UI audits. Media export and narration require optional local dependencies.
---

# Huashu Design

Create polished visual artifacts with HTML as the production medium. Adopt the relevant role—product designer, prototyper, presentation designer, motion designer, or critic—rather than treating every request as a generic web page.

## When to use and boundaries

- Use this skill for prototypes, interactive demos, HTML decks, motion, explainers, and multiple visual directions.
- Use `$design-taste-frontend` for a production landing page, portfolio, campaign, or image-first marketing build.
- Use `$impeccable` for an existing product interface, dashboard, form, settings surface, accessibility audit, or targeted production polish.
- Do not use this skill for ordinary HTML maintenance or backend work.
- Do not spawn subagents unless the user explicitly requests delegation or parallel agents. When they do not, produce independent variants sequentially from the same written brief.

## Core rules

1. Verify unstable facts before designing around them. Browse current primary sources for named products, events, versions, people, or specifications; record only facts the design actually needs.
2. Start from existing context. Inspect project styles, assets, brand rules, representative screens, and real content before inventing a new visual system.
3. Surface assumptions briefly before committing to an expensive direction. Ask only for information that materially changes the artifact.
4. Prefer several genuinely different visual directions over superficial color swaps when exploration is requested.
5. Use honest placeholders when a required asset cannot be sourced legally or reliably. Never fabricate official logos, product imagery, citations, or UI states.
6. Avoid generic AI-design tells: gratuitous gradients, glass cards everywhere, filler metrics, decorative pills, repetitive card grids, weak hierarchy, fake testimonials, and motion without narrative purpose.
7. Keep semantic content and controls in HTML/CSS/SVG. Use raster assets only where imagery or texture is intrinsically raster.
8. Preserve accessibility, reduced motion, keyboard operation, responsive behavior, and readable contrast.

## Workflow

1. Classify the deliverable: prototype, deck, motion piece, narrated explainer, design exploration, or critique.
2. Inspect existing context and verify unstable product facts.
3. Write a compact design brief covering audience, task, content, tone, format, dimensions, constraints, assets, and acceptance checks.
4. Select the narrow reference route below. Read only the files needed for the deliverable.
5. For ambiguous visual direction, create three structurally distinct directions from the same brief. If subagents were explicitly requested, they may work independently; otherwise create the variants sequentially without borrowing visual decisions between them.
6. Implement the selected direction with real content and working interaction.
7. Verify interaction, responsive layout, overflow, accessibility, console errors, and any export pipeline.
8. Report the artifact paths, verification performed, optional dependencies used, and remaining placeholders.

## Reference routing

Read these only when relevant:

- General workflow and context: `references/workflow.md`, `references/design-context.md`, `references/content-guidelines.md`.
- Visual-direction exploration: `references/design-styles.md`, `references/brand-asset-protocol.md`, `references/tweaks-system.md`.
- React and reusable frames: `references/react-setup.md` and `assets/*.jsx`.
- Slide decks and editable PPTX: `references/slide-decks.md`, `references/editable-pptx.md`.
- Motion and cinematic work: `references/animations.md`, `references/animation-best-practices.md`, `references/animation-pitfalls.md`, `references/cinematic-patterns.md`, `references/scene-templates.md`.
- Launch films and narrated explainers: `references/launch-film-director-notes.md`, `references/voiceover-pipeline.md`, `references/audio-design-rules.md`.
- Video/GIF export: `references/video-export.md`.
- Expert review: `references/critique-guide.md`, `references/verification.md`.
- Example galleries: `assets/showcases/INDEX.md`. Treat examples as inspiration, not templates to clone.
- Multi-perspective case study: `references/multi-perspective-parallel-case-study.md`. Its upstream agent syntax is illustrative only; follow the subagent boundary above.

## Runtime and assets

- Reuse the frames, stage components, deck shell, and animation helpers under `assets/` before recreating them.
- The bundled showcase PNG/HTML files are reference assets, not mandatory output dependencies.
- Bundled music and sound files were deliberately excluded. Source audio per project with clear usage rights and attribution.
- Core HTML/CSS/JS work needs no installation.
- Export, screenshot, PPTX, or image-processing scripts may need Node packages from this skill's `package.json`; video/audio scripts may additionally need FFmpeg. Read `references/runtime-codex.md` before running them.
- Never install packages, download media, call paid APIs, or use voice credentials without the user's approval.

## Verification

- Prefer an available browser workflow for real click and viewport checks.
- Run `python3 .agents/skills/huashu-design/scripts/verify.py <artifact>` when applicable.
- For video, inspect duration, resolution, frame rate, audio presence, and representative frames.
- For decks, verify every slide at the target aspect ratio and confirm editable export when requested.
- For prototypes, test the primary flow, keyboard access, empty/error states, and narrow-screen behavior.

## Delivery

Return the finished artifact, not only a design description. Keep generated source editable, identify optional runtime requirements, and state exactly what was and was not verified.
