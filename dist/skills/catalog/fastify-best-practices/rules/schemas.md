# Schemas

- Define body, params, querystring, headers, and response schemas.
- Prefer a single source of truth that produces runtime schemas and TypeScript types.
- Set `additionalProperties: false` for security-sensitive payloads unless extensibility is deliberate.
- Reuse schemas with stable IDs; do not compile new dynamic schemas per request.
