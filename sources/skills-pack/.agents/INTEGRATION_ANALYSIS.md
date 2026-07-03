# Integration analysis — Codex Skills Pack 2026-07-03.1

## Scope

Two user-provided archives were analyzed:

1. `codex skills(2).zip` — the existing Codex pack.
2. `skills for update and integration.zip` — source skills to integrate and port.

The work was performed as a merge into the existing pack, not as a replacement. Existing skill names, custom agents, routing rules, provenance metadata, and safety constraints were preserved unless a documented conflict required a change.

## Input inventory

### Existing Codex pack

- 152 registered skills under `.agents/skills/`.
- 9 project custom agents under `.codex/agents/`.
- Existing `AGENTS.md`, skill index, router, validator, migration report, and third-party notices.

### Integration archive

| Source root | `SKILL.md` files | Source agent Markdown files | Notes |
|---|---:|---:|---|
| `bilingual-transcreator` | 1 | 0 | Portable RU↔EN transcreation workflow |
| `claude-seo-main` | 33 | 20 | 18 unique core SEO agents plus 2 duplicate extension mirrors |
| `claude-skills-main` | 4 | 0 | Translation, Russian editorial, Textovod, ASCII editing |
| `content-skills-main` | 15 | 6 | Content studio, brand voice, social, blog, visual workflows |
| `humanizer-main` | 1 | 0 | English anti-slop and humanization |
| `humanizer-ru-main` | 1 | 0 | Russian voice passport and humanization |
| `marketingskills-main` | 46 | 0 | Marketing strategy and execution suite |
| `ru-text-main` | 2 | 0 | Two byte-identical registrations of the same skill |
| **Total** | **103** | **26** | 100 unique skill behaviors after exact deduplication |

## Conflict analysis

### Exact duplicates

Three registrations were byte-identical and were registered once:

- root and nested copies of `ru-text`;
- core and extension copies of `seo-dataforseo`;
- core and extension copies of `seo-image-gen`.

Unique extension scripts, references, field configurations, and setup documentation were retained even when the duplicate skill registration was removed.

### Distinct skills with the same name

Two collisions contained materially different workflows and were preserved under different Codex names:

| Source collision | Integrated names | Decision |
|---|---|---|
| two `seo-audit` skills | `$seo-audit`, `$marketing-seo-audit` | Keep the deep specialist/crawl suite under the canonical name; retain the lighter marketing audit under a qualified name |
| two `content-strategy` skills | `$content-strategy`, `$content-editorial-strategy` | Keep broad marketing content strategy canonical; qualify the brand-led editorial workflow |

No distinct behavior was discarded because of a name collision.

## Claude-to-Codex portability findings

The source bundles contained several patterns that could not be copied safely or functionally as-is:

1. Slash commands such as `/seo ...`, `/content ...`, and `/humanizer-ru`.
2. Skills and settings stored under `~/.claude/`.
3. JSON MCP configuration written to `.claude/settings.json`.
4. Claude Markdown agents and model labels such as `sonnet`.
5. Automatic assumptions about Claude task/subagent tools.
6. Source-root-relative scripts and tool registries that would break after copying individual skills.
7. Large monolithic humanizer files that would consume excessive context whenever activated.
8. Installers that copied files into another platform and wrote credentials automatically.
9. Hooks, marketplace manifests, release tooling, CI files, and promotional assets unrelated to skill behavior.

## Codex-native integration architecture

### Registered skills

The final pack contains **252 skills**:

- 152 existing skills;
- 46 new marketing and growth skills;
- 31 new SEO and search-visibility skills;
- 15 new content-studio skills;
- 8 new writing, localization, and editorial skills.

Every registered skill has:

- a canonical `.agents/skills/<name>/SKILL.md`;
- unique frontmatter `name`;
- a non-empty routing `description`;
- `.agents/skills/<name>/agents/openai.yaml`;
- source/provenance notes;
- source license copies when supplied.

### Shared vendor resources

Shared files were centralized instead of duplicated across skills:

```text
.agents/vendor/claude-seo/             # source-namespaced SEO scripts, schemas, data, extensions
.agents/vendor/marketingskills/tools/  # tool and integration registry
.agents/vendor/content-skills/         # content scripts, styles and assets
.agents/brand/                         # project brand context and samples
```

The `claude-seo` directory name remains only as a provenance/vendor namespace. Active instructions use Codex invocation, paths, agents, configuration, and safety semantics.

### Custom agents

Twenty-four unique source agents were converted to Codex TOML:

- 18 SEO specialists in `.codex/agents/seo_*.toml`;
- 6 content specialists in `.codex/agents/content_*.toml`.

Together with the existing 9 agents, the pack contains **33 project custom agents**.

Migration rules:

- removed source model names rather than forcing a non-Codex model;
- converted source paths to `.agents/skills/...` and shared vendor paths;
- converted routing references to registered `$skill-name` calls;
- added non-recursion, capability, evidence, spend, and external-side-effect guardrails;
- kept subagent use explicit-only with an inline parent-session fallback.

## Humanizer redesign

The English and Russian humanizer sources were useful but too large as always-loaded entry files:

- English source: 622 lines;
- Russian source: 1,459 lines.

Both were converted to progressive-disclosure skills:

- compact Codex-native `SKILL.md` for routing and workflow;
- complete upstream pattern catalog preserved under `references/`;
- dictionaries, examples, presets, and voice-passport behavior retained;
- detector-evasion framing rejected in favor of editorial quality, factual integrity, and voice consistency.

## Live integration migration

A single Codex-native setup guide was added at `.agents/CODEX_INTEGRATIONS.md`.

It covers:

- Ahrefs MCP;
- Firecrawl MCP;
- DataForSEO MCP and field configuration;
- Nanobanana/Gemini image MCP;
- Bing Webmaster Tools and IndexNow environment variables;
- Profound and SE Ranking environment variables;
- Textovod credentials;
- local Unlighthouse prerequisites;
- MCP removal and credential rotation.

Source installers that wrote `.claude/settings.json` are not active. Nanobanana setup and validation scripts were rewritten to use `codex mcp` rather than editing another platform's settings.

Credentialed, potentially paid, crawling, submission, or image-generation integrations are marked explicit-only in `agents/openai.yaml`.

## Routing changes

The local router was extended for Russian and English marketing/editorial queries. High-precision intent rules now distinguish, among other cases:

- RU→EN transcreation from EN→RU technical translation;
- Russian humanization from general copy editing;
- deep SEO audit from a lightweight marketing audit;
- LinkedIn brand-voice content from general social strategy;
- marketing planning from launch execution;
- landing-page translation from landing-page visual design.

## Documentation changes

Updated or added:

- `README.md`;
- `AGENTS.md` and `.agents/AGENTS.fragment.md`;
- `.agents/SKILLS_INDEX.md` and `.json`;
- `.agents/CODEX_INTEGRATIONS.md`;
- `.agents/INTEGRATION_MANIFEST.json`;
- `.agents/MIGRATION_REPORT.md`;
- `.agents/THIRD_PARTY_NOTICES.md`;
- `.agents/VALIDATION_REPORT.md`;
- this analysis document.

## Deliberate exclusions

The following distribution/platform artifacts were not activated:

- Claude plugin and marketplace manifests;
- Claude settings writers and uninstallers;
- automatic hook installation;
- source CI/release files and issue templates;
- promotional screenshots and website assets;
- automatic dependency installation;
- automatic credentials, paid calls, publishing, URL submission, outreach, ad spend, or external-system mutation.

These exclusions remove incompatible or unsafe automation, not unique skill behavior.

## Result

- **100 unique skills added.**
- **252 total registered skills.**
- **24 custom agents added.**
- **33 total custom agents.**
- **3 exact duplicate registrations removed.**
- **2 name conflicts resolved without dropping behavior.**
- **0 active Claude-specific markers in imported behavior files.**
- **0 broken checked local links.**

See `.agents/INTEGRATION_MANIFEST.json` for the machine-readable list of all added skills and converted agents.
