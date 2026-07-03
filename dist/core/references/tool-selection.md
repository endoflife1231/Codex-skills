# Tool Selection

This reference captures a small but important Codex-quality rule: prefer purpose-built tools over generic shell usage when the dedicated option gives a clearer and safer result.

## Guidance

- prefer dedicated search, file-read, validation, and project tools over generic shell commands when they provide a better user experience
- use shell commands when they are the most direct or only practical option
- verify that a dedicated tool cannot reasonably do the job before defaulting to broad shell usage for simple search-and-read tasks

## Why it matters

This keeps workflows:

- clearer
- less error-prone
- easier to review
- easier to explain back to the user

It also helps prevent accidental noisy output and reduces the chance of mixing discovery work with risky command execution.
