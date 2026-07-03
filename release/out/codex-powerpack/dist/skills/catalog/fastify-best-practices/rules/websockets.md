# WebSockets

- Authenticate the handshake and re-check authorization for every mutating event.
- Validate all event payloads with schemas.
- Treat the server as authoritative; use command IDs, base revisions, acknowledgements, and snapshots.
- Bound room membership, event rates, payload sizes, and replay buffers.
- Do not assume a transient socket implies durable delivery.
