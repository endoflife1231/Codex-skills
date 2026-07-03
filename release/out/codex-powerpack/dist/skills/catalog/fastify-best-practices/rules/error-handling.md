# Error handling

- Use a central error handler that distinguishes validation, authentication, authorization, conflict, not-found, and internal failures.
- Return stable machine-readable error codes without exposing stack traces or secrets.
- Log unexpected errors once with request context.
- Convert database constraint errors into domain-safe responses.
