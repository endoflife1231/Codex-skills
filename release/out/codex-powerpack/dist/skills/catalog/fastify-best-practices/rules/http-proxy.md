# HTTP proxying

- Proxy only to allowlisted destinations.
- Strip hop-by-hop and sensitive inbound headers unless explicitly required.
- Set connect/read timeouts and maximum response sizes.
- Do not expose internal services or user-controlled URLs through a generic proxy endpoint.
