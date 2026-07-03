# Logging

- Use Fastify/Pino structured logs rather than `console.log`.
- Include request ID, user ID when safe, campaign/session IDs, command ID, and outcome.
- Redact cookies, authorization headers, passwords, tokens, private notes, and secrets.
- Avoid duplicate logging of the same error at several layers.
