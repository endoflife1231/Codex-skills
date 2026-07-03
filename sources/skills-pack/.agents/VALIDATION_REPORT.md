# Validation report — Codex Skills Pack 2026-07-03.1

Validation was executed against the integrated directory before packaging.

## Pack inventory

- Registered skills: **252**
- `agents/openai.yaml` files: **252**
- Project custom agents: **33**
- Added unique skills: **100**
- Added custom agents: **24**
- Files: **3,095**
- Symlinks: **0**
- Approximate unpacked size: **24 MB**

## Structural validation

Command:

```bash
python3 .agents/tools/validate_pack.py
```

Result:

```text
OK: 252 skills and 33 custom agents validated
```

The validator checks canonical skill registration, unique frontmatter names, metadata, required project files, agent manifests, selected workflow assets, integrated vendor resources, collision decisions, and expected final counts.

## Deep integration validation

Command:

```bash
python3 .agents/tools/validate_integration.py
```

Result:

```text
OK: deep integration validation passed — 252 skills, 33 custom agents, 636 local links, 787 skill references
```

Deep checks include:

- all imported skills listed in the integration manifest exist;
- all registered skills have `SKILL.md` and `agents/openai.yaml`;
- JSON, YAML, TOML, and Python parsing;
- no active `.claude/`, `CLAUDE.md`, Claude Code, legacy slash-command, or Claude tool markers in imported behavior files;
- imported Markdown local links resolve;
- direct `$skill-name` references resolve to registered skills;
- live integrations are explicit-only;
- shared SEO, marketing, content, brand, and integration resources exist.

## Syntax validation

Successfully parsed or checked:

- Python files: **170**
- JSON files: **77**
- YAML files: **266**
- TOML files: **34**
- Bash files with `bash -n`: **12**
- JavaScript files with `node --check`: **83**

The environment used Python 3.13.5 and Node.js 22.16.0.

## Link and reference validation

- Imported/local Markdown links checked: **636**
- Broken checked links: **0**
- Direct skill references checked: **787**
- Unregistered direct skill references: **0**
- Concrete shared vendor/script paths checked separately; only documented future project-state files such as `.agents/media-list.md` and `.agents/brand/.setup-draft.json` were absent by design.

## Claude-to-Codex residue scan

Imported active behavior files were scanned for:

- `.claude/` and `~/.claude`;
- `CLAUDE.md`;
- `Claude Code`;
- `allowed-tools` and `Task tool`;
- legacy `/seo`, `/content`, and `/humanizer` invocation lines;
- Claude plugin manifests.

Result: **0 files with active legacy markers**. Legal/source provenance files are excluded from this behavioral scan so upstream attribution is not rewritten.

## Routing smoke tests

The following queries were checked with `.agents/tools/find_skill.py`:

| Query | Top result |
|---|---|
| `сделай живой перевод лендинга с русского на английский` | `$bilingual-transcreator` |
| `полный SEO аудит сайта` | `$seo-audit` |
| `напиши LinkedIn пост в голосе бренда` | `$content-linkedin` |
| `отредактируй русский AI текст` | `$humanizer-ru` / `$ru-editor` |
| `создай маркетинговую стратегию запуска SaaS` | `$marketing-plan`, followed by `$launch` |

## Security and side effects

- No symlinks are present.
- No real PEM private key payload was found; one documented service-account JSON placeholder contains `BEGIN PRIVATE KEY` with ellipses.
- The pack does not automatically install dependencies, configure MCP servers, create credentials, publish content, submit URLs, send outreach, buy ads, or mutate external systems.
- Credentialed/live integrations are explicit-only and must preflight network, credentials, quota/cost, and approval.
- Rewritten MCP setup uses `codex mcp`; active instructions do not mutate another platform's settings.

## Runtime limitations

The validation environment did not contain the Codex CLI or user credentials. Therefore:

- real Codex discovery/UI loading was not exercised;
- MCP servers were not installed or called;
- paid/vendor APIs were not called;
- real websites were not crawled;
- model-quality eval cases were not executed inside an authenticated Codex session.

The Nanobanana validator correctly reported `codex_cli: false` and `nanobanana_mcp: false` while confirming Node and `npx` were present. This is an expected capability-gated failure, not a pack error.

After installation in a real project, run both validators and restart Codex before testing explicit skills and optional integrations.
