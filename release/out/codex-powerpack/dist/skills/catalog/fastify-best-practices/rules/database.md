# Database

- Create one managed pool per process and close it during shutdown.
- Use transactions for state changes that must update current state and append an event atomically.
- Keep transaction scopes short and define conflict behavior.
- Enforce uniqueness/idempotency in the database where correctness depends on it.
