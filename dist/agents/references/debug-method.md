# Debug Method

This reference captures the strongest debugging patterns adapted from the upstream debugging specialist material.

## Evidence first

- start from failing tests, logs, stack traces, or concrete symptoms
- separate observed facts from guesses
- reproduce or tightly characterize the failure before changing code

## Root-cause loop

1. isolate the failing path
2. form a small hypothesis
3. test it with the cheapest useful check
4. keep only evidence-backed causes
5. validate the fix against the original symptom

## Scope control

- do not widen the fix before proving it is necessary
- check nearby regressions after the fix
- if the root cause is still uncertain, report that honestly instead of forcing a story
