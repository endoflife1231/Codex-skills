# Plugins

- Register domains as focused plugins and rely on Fastify encapsulation.
- Use `fastify-plugin` only when a decorator or hook must intentionally escape encapsulation.
- Declare plugin dependencies explicitly; avoid order-dependent global mutations.
- Close owned resources in `onClose`.
- Keep route registration, decorators, schemas, and hooks near the owning domain.
