# Testing

- Build the app in a function and test it with `fastify.inject()` without opening a port.
- Test schemas, auth failures, permission boundaries, conflicts, and idempotency.
- Use isolated database fixtures and roll back or reset deterministically.
- Separately test real startup, WebSocket integration, and graceful shutdown.
