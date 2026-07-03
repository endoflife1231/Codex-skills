# Quality Evaluation Cases

Use these cases for manual or automated regression testing.

## Case 1 — Preserve qualified claim

Source:

```text
Teams can reduce review time by up to 25%, based on an internal analysis of 42 customers in Q1 2026.
```

Target: Russian, faithful, corporate website.

Must preserve:

- possibility, not guarantee;
- `up to`;
- 25%;
- internal-analysis attribution;
- 42 customers;
- Q1 2026.

## Case 2 — Remove Russian calque

Source:

```text
Мы адресуем ключевые вызовы современного бизнеса и даём вам возможность реализовать свой потенциал.
```

Target: US English, adaptive, B2B homepage.

Expected behavior:

- recover a concrete meaning if context supplies one;
- otherwise avoid inventing a product mechanism;
- do not output `address key challenges` + `realize your potential` as generic filler;
- flag insufficient specificity when review notes are requested.

## Case 3 — Separate voice by language

Input includes a formal Russian voice file and a conversational English voice file.

Expected behavior:

- English follows `VOICE_EN.md`, not a translated version of Russian formality;
- facts and claim boundaries remain shared.

## Case 4 — Campaign diversity

Source line has one strategic promise. Target: Russian campaign mode.

Expected behavior:

- three routes use genuinely different mechanisms;
- no invented proof;
- no three synonym-only variants.

## Case 5 — Negative control

Request:

```text
Translate this passport page exactly for a certified application.
```

Expected behavior:

- skill should not perform creative transcreation;
- recommend exact professional/certified translation requirements.

## Case 6 — Product UI

Source:

```text
Delete workspace? All project data will be permanently removed. This action cannot be undone.
```

Target: Russian product UI.

Must preserve:

- destructive action;
- scope of deletion;
- permanence;
- irreversibility;
- concise UI wording.

## Case 7 — No fake personalization

Request includes a cold sales email but no recipient research.

Expected behavior:

- do not claim to have followed the recipient's work or admired a recent launch;
- write relevance based only on supplied segment context.
