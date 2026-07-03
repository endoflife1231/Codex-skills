# Review Method

This reference deepens the reviewer role without bloating the main agent file.

## Review order

1. understand intended behavior
2. inspect tests and verification first when available
3. read the changed code and nearby boundaries
4. look for regressions, correctness issues, and missing verification
5. only then spend time on lower-priority cleanup suggestions

## High-value findings

Prioritize:

- broken behavior
- security or data handling issues
- missing tests for risky behavior
- wrong abstraction or hidden coupling
- performance regressions with practical impact

## Low-value noise to avoid

- style-only commentary with no material effect
- speculative redesign without evidence
- duplicate findings phrased differently

## Good reviewer tone

- direct
- specific
- evidence-based
- constructive
