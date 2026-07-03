# Configuration

- Validate environment variables at startup and fail fast on invalid configuration.
- Separate development defaults from production-required secrets.
- Never read arbitrary environment variables throughout domain code; expose a typed config object.
- Document public URLs, trusted proxies, cookie security, database, storage, and upload limits.
