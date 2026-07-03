# Verify Layer

This directory contains verification tools for the Codex Powerpack distribution itself.

Goals:

- validate that the assembled distribution has the expected structure
- catch missing core, agents, skills, profiles, and integration files early
- provide a simple doctor flow for local environment checks

These tools validate the assembled `dist/` tree. They do not mutate `sources/`.

Validation also covers onboarding schemas, always-on rules, installable Skill
sources and executable lifecycle scripts. Verify an adapted project with:

```bash
bash dist/onboarding/verify-adaptation.sh --target /path/to/project
```
