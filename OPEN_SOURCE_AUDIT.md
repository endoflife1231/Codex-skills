# Open-source audit

Audit date: 2026-07-26  
Release: 0.2.2

## Policy

A skill may be included when redistribution permission is supported by one of the following:

1. a license file inside the skill directory;
2. a license at the root of the upstream repository that covers the skill;
3. an explicit SPDX/package/README license declaration from the upstream project; or
4. confirmed first-party authorship under this repository's MIT license.

License evidence and attribution must be bundled in the public package. A public GitHub repository without any license declaration is not treated as permission to redistribute.

## Result

- Original skills: 254
- Included skills: 249
- Restored after re-audit: 65
- Excluded skills: 5
- Agents: 8 (none had been removed by the earlier skill audit)

## Restored groups

### High-confidence upstream license files

- **PixiJS:** 26 skills; official repository MIT license, Copyright (c) 2026 PixiJS. Evidence: `dist/licenses/pixijs-MIT.txt`.
- **Addy Osmani agent-skills source:** 7 skills; MIT, Copyright (c) 2025 Addy Osmani. Evidence: `dist/licenses/agent-skills-MIT.txt`.
- **Next Level Builder:** 3 skills; MIT, Copyright (c) 2024 Next Level Builder. Evidence: `dist/licenses/nextlevelbuilder-MIT.txt`.
- **Supabase:** 1 skill; official repository MIT license, Copyright (c) 2026 Supabase. Evidence: `dist/licenses/supabase-MIT.txt`.
- **Vercel:** 3 skills; official repository MIT license, Copyright (c) 2026 Vercel, Inc. Evidence: `dist/licenses/vercel-MIT.txt`.

### First-party local work

- **Local migration/router skills:** 3 skills covered by the root MIT license.

### Medium-confidence explicit MIT declaration

- **BarisSozen/claude:** 22 skills. The upstream README says `License: MIT` and `package.json` declares `"license": "MIT"`, but no standalone license file or copyright notice was present during the audit. Evidence: `dist/licenses/barissozen-MIT-declaration.txt`.

This group is included because the upstream project explicitly identifies MIT as its license. The evidence is weaker than a complete bundled license file and that limitation is retained in the notices.

## Skills still excluded

- `ascii-art-beautifier` — upstream repository found, but no license declaration or license file.
- `en-ru-translator-adv` — upstream repository found, but no license declaration or license file.
- `ru-editor` — upstream repository found, but no license declaration or license file.
- `ru-textovod` — upstream repository found, but no license declaration or license file.
- `bilingual-transcreator` — user-provided custom work; no license or confirmed first-party ownership record.

These five can be restored later if the copyright holder supplies a compatible license or the repository owner confirms authorship and relicensing authority.

## Restored skill names

### PixiJS

- `pixijs`
- `pixijs-accessibility`
- `pixijs-application`
- `pixijs-assets`
- `pixijs-blend-modes`
- `pixijs-color`
- `pixijs-core-concepts`
- `pixijs-create`
- `pixijs-custom-rendering`
- `pixijs-environments`
- `pixijs-events`
- `pixijs-filters`
- `pixijs-html-source`
- `pixijs-math`
- `pixijs-migration-v8`
- `pixijs-performance`
- `pixijs-scene-container`
- `pixijs-scene-core-concepts`
- `pixijs-scene-dom-container`
- `pixijs-scene-gif`
- `pixijs-scene-graphics`
- `pixijs-scene-mesh`
- `pixijs-scene-particle-container`
- `pixijs-scene-sprite`
- `pixijs-scene-text`
- `pixijs-ticker`

### Addy Osmani agent-skills

- `deploy-to-vercel`
- `vercel-cli-with-tokens`
- `vercel-composition-patterns`
- `vercel-optimize`
- `vercel-react-native-skills`
- `vercel-react-view-transitions`
- `writing-guidelines`

### Next Level Builder

- `brand`
- `design-system`
- `ui-ux-pro-max`

### Supabase

- `postgres-best-practices`

### Vercel

- `find-skills`
- `vercel-react-best-practices`
- `web-design-guidelines`

### First-party

- `banner-design`
- `design`
- `skill-router`

### BarisSozen

- `apple-ui-design`
- `code-consistency-validator`
- `code-review-expert`
- `common-pitfalls`
- `defi-expert`
- `defi-mev-battletest`
- `defi-registry-manager`
- `error-logger`
- `full-review`
- `hft-quant-expert`
- `iterative-runner`
- `latency-tracker`
- `liquidity-depth-analyzer`
- `pitfalls-blockchain`
- `pitfalls-drizzle-orm`
- `pitfalls-express-api`
- `pitfalls-react`
- `pitfalls-security`
- `pitfalls-tanstack-query`
- `pitfalls-websocket`
- `skill-auditor`
- `system-integration-validator`

