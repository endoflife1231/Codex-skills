# Serialization

- Define response schemas for every sensitive endpoint.
- Serialize role-specific DTOs; do not send hidden fields and rely on client-side hiding.
- Keep dates, IDs, decimals, and nullable values consistent across APIs.
- Avoid returning raw ORM rows.
