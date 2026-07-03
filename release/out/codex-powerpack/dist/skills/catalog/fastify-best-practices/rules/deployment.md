# Deployment

- Listen on `0.0.0.0` inside containers and expose only through the intended reverse proxy/private network.
- Implement readiness and liveness endpoints with meaningful dependency checks.
- Handle SIGTERM/SIGINT: stop accepting work, drain sockets, close Fastify, then close database/storage resources.
- Run migrations as an explicit deployment step and back up persistent volumes.
