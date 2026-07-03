# Codex integration setup

The skills in this pack are already installed at project scope. This guide only configures optional live data sources and MCP servers.

## Safety and scope

- Never store API keys inside `.agents/`, committed files, prompts, reports, or examples.
- Prefer a dedicated low-privilege key and rotate it if it is exposed.
- `codex mcp add` writes MCP configuration to Codex configuration. Review the resulting entry with `codex mcp list` and `codex mcp get <name>`.
- Package versions below are pinned to the versions supplied by the source bundles. Verify current vendor documentation before changing versions.
- Paid APIs, crawls, submissions, publishing, and advertising remain approval-gated.

## MCP integrations

Run these from a trusted terminal, not from an untrusted repository script. Replace placeholders locally; do not commit the commands with real secrets.

### Ahrefs

```bash
codex mcp add ahrefs \
  --env AHREFS_API_TOKEN='<token>' \
  -- npx --yes --package=@ahrefs/mcp@0.0.11 mcp
```

Verify with `codex mcp get ahrefs`, then invoke `$seo-ahrefs`.

### Firecrawl

```bash
codex mcp add firecrawl-mcp \
  --env FIRECRAWL_API_KEY='<fc-key>' \
  -- npx -y firecrawl-mcp@3.11.0
```

Verify with `codex mcp get firecrawl-mcp`, then invoke `$seo-firecrawl`.

### DataForSEO

The field configuration shipped with this pack is at `.agents/vendor/claude-seo/extensions/dataforseo/field-config.json`.

```bash
codex mcp add dataforseo \
  --env DATAFORSEO_USERNAME='<login>' \
  --env DATAFORSEO_PASSWORD='<password>' \
  --env FIELD_CONFIG_PATH="$(pwd)/.agents/vendor/claude-seo/extensions/dataforseo/field-config.json" \
  -- npx -y dataforseo-mcp-server@2.8.10
```

Verify with `codex mcp get dataforseo`, then invoke `$seo-dataforseo`.

### Nanobanana / Gemini image generation

```bash
codex mcp add nanobanana-mcp \
  --env GOOGLE_AI_API_KEY='<key>' \
  -- npx -y @ycse/nanobanana-mcp@1.1.1
```

Verify with `codex mcp get nanobanana-mcp`, then invoke `$seo-image-gen`.

## Environment-variable integrations

Export these in the environment that launches Codex, or use your operating system's secret manager. Do not add them to repository files.

| Skill | Variables |
|---|---|
| `$seo-bing` | `BING_WEBMASTER_API_KEY`; for IndexNow also `INDEXNOW_KEY`, `INDEXNOW_KEY_LOCATION` |
| `$seo-profound` | `PROFOUND_API_KEY` |
| `$seo-seranking` | `SERANKING_API_KEY` |
| `$ru-textovod` | `TEXTOVOD_EMAIL`, `TEXTOVOD_API_KEY` |

Example for the current shell:

```bash
export SERANKING_API_KEY='<key>'
codex
```

## Local tools without API keys

`$seo-unlighthouse` uses local Node tooling. Check availability without mutating the pack:

```bash
node --version
npx --yes --package=unlighthouse@0.13.5 unlighthouse-ci --help
```

## Removal and rotation

```bash
codex mcp list
codex mcp remove <server-name>
```

Re-add an MCP server to rotate its secret. Restart or reload Codex after configuration changes if tools are not visible in the current session.
