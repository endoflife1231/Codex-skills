---
name: ckm-brand
description: Brand voice, visual identity, messaging frameworks, asset management, brand consistency. Activate for branded content, tone of voice, marketing assets, brand compliance, style guides.
metadata:
  author: claudekit
  version: 1.0.0
  argument_hint: '[update|review|create] [args]'
  codex_migration: '2026-06-27'
  source_path: skills/.curated/ui-ux/.claude/skills/brand/SKILL.md
  source_name: ckm:brand
---

# Brand

## Codex compatibility

- Legacy Claude-specific tool names or paths are conceptual; use Codex shell/editor capabilities and the local `.agents/skills` path.


Brand identity, voice, messaging, asset management, and consistency frameworks.

## When to Use

- Brand voice definition and content tone guidance
- Visual identity standards and style guide development
- Messaging framework creation
- Brand consistency review and audit
- Asset organization, naming, and approval
- Color palette management and typography specs

## Quick Start

**Inject brand context into prompts:**
```bash
node .agents/skills/ckm-brand/scripts/inject-brand-context.cjs
node .agents/skills/ckm-brand/scripts/inject-brand-context.cjs --json
```

**Validate an asset:**
```bash
node .agents/skills/ckm-brand/scripts/validate-asset.cjs <asset-path>
```

**Extract/compare colors:**
```bash
node .agents/skills/ckm-brand/scripts/extract-colors.cjs --palette
node .agents/skills/ckm-brand/scripts/extract-colors.cjs <image-path>
```

## Brand Sync Workflow

```bash
# 1. Edit docs/brand-guidelines.md (or invoke `$brand` with an update request)
# 2. Sync to design tokens
node .agents/skills/ckm-brand/scripts/sync-brand-to-tokens.cjs
# 3. Verify
node .agents/skills/ckm-brand/scripts/inject-brand-context.cjs --json | head -20
```

**Files synced:**
- `docs/brand-guidelines.md` → Source of truth
- `assets/design-tokens.json` → Token definitions
- `assets/design-tokens.css` → CSS variables

## Subcommands

| Subcommand | Description | Reference |
|------------|-------------|-----------|
| `update` | Update brand identity and sync to all design systems | `references/update.md` |

## References

| Topic | File |
|-------|------|
| Voice Framework | `references/voice-framework.md` |
| Visual Identity | `references/visual-identity.md` |
| Messaging | `references/messaging-framework.md` |
| Consistency | `references/consistency-checklist.md` |
| Guidelines Template | `references/brand-guideline-template.md` |
| Asset Organization | `references/asset-organization.md` |
| Color Management | `references/color-palette-management.md` |
| Typography | `references/typography-specifications.md` |
| Logo Usage | `references/logo-usage-rules.md` |
| Approval Checklist | `references/approval-checklist.md` |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/inject-brand-context.cjs` | Extract brand context for prompt injection |
| `scripts/sync-brand-to-tokens.cjs` | Sync brand-guidelines.md → design-tokens.json/css |
| `scripts/validate-asset.cjs` | Validate asset naming, size, format |
| `scripts/extract-colors.cjs` | Extract and compare colors against palette |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/brand-guidelines-starter.md` | Complete starter template for new brands |

## Routing

Infer the requested operation from the user message. For an update, read `references/update.md`; otherwise load only the reference matching the requested brand task. Resolve bundled scripts from `.agents/skills/ckm-brand/scripts/`.
