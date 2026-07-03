# Content types and uploads

- Accept only required content types and enforce body/file limits.
- Stream uploads when possible; validate MIME type using content inspection, not filename alone.
- Sanitize filenames, generate server-side storage keys, and strip image metadata.
- Never parse unbounded or attacker-controlled payloads synchronously.
