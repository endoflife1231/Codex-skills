# Project-scoped Codex custom agents

These project-scoped agents were migrated into the current Codex custom-agent TOML format from the source archives noted below.

- `code_reviewer` — structured five-axis code review.
- `security_auditor` — focused vulnerability and threat-boundary review.
- `test_engineer` — test strategy, coverage gaps, and Prove-It regression tests.
- `web_performance_auditor` — source-level or evidence-backed web performance audit.

Codex only spawns subagents when explicitly asked. Example: “Spawn `code_reviewer`, `security_auditor`, and `test_engineer` in parallel, wait for all results, then merge them into a ship decision.”

The review-oriented agents are read-only. They report findings to the parent session; the parent decides what to change.

## Caveman / Cavecrew additions

- `cavecrew_investigator` — terse read-only code locator.
- `cavecrew_builder` — bounded one/two-file implementation worker.
- `cavecrew_reviewer` — terse findings-only reviewer.

Invoke them explicitly or through `$cavecrew`. Cavecrew agents never recursively delegate.
