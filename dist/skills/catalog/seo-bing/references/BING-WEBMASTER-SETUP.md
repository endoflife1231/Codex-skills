# Bing Webmaster Tools and IndexNow setup for Codex

The `$seo-bing` skill is already installed. It uses bundled scripts under `.agents/vendor/claude-seo/scripts/` and reads credentials from the environment that launches Codex.

Required variables are documented in [the central Codex integration guide](../../../CODEX_INTEGRATIONS.md). For IndexNow, publish the key file at the declared `INDEXNOW_KEY_LOCATION` and run the skill's verification workflow before submitting URLs. URL submission is an external side effect and always requires explicit approval.
