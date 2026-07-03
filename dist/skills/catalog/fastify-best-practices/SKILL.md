---
name: fastify-best-practices
description: Guides production Fastify v5 backend and REST API development with TypeScript or JavaScript. Use for Fastify plugins, routes, JSON Schema validation, error handling, authentication, CORS/security, logging, performance, database integration, WebSockets.
license: MIT
metadata:
  source: adapted-for-codex-from-mcollina-skills
  tags: fastify, nodejs, typescript, backend, api, server, http
  codex_migration: '2026-06-27'
  source_path: skills/.curated/fastify-best-practices/SKILL.md
---

# Fastify Best Practices

Use this skill for general Fastify implementation and review. For project-specific decisions, also load `mythictable-fastify-api` and `mythictable-project-architecture`.

## Default workflow

1. Confirm the installed Fastify major version and plugin compatibility.
2. Model each domain as a focused Fastify plugin.
3. Define request and response schemas before handlers.
4. Keep authorization and domain invariants on the server.
5. Test routes with `fastify.inject()` and test startup/shutdown separately.
6. Add structured logging, health checks, and graceful shutdown before deployment.

## Rule index

- `rules/plugins.md` — encapsulation and plugin boundaries
- `rules/routes.md` — route organization and thin handlers
- `rules/schemas.md` — validation and serialization
- `rules/error-handling.md` — typed operational errors
- `rules/hooks.md` — lifecycle hooks
- `rules/authentication.md` — authentication and authorization
- `rules/testing.md` — `inject()` and integration tests
- `rules/performance.md` — event-loop and schema performance
- `rules/logging.md` — Pino and request context
- `rules/typescript.md` — TypeScript patterns
- `rules/decorators.md` — typed decorators
- `rules/content-type.md` — parsers and upload boundaries
- `rules/serialization.md` — response contracts
- `rules/cors-security.md` — CORS, headers, and abuse controls
- `rules/websockets.md` — realtime boundaries
- `rules/database.md` — lifecycle and transactions
- `rules/configuration.md` — validated environment configuration
- `rules/deployment.md` — production lifecycle
- `rules/http-proxy.md` — proxying safety

## Core principles

- Prefer encapsulated plugins over global mutable state.
- Treat schemas as executable contracts.
- Keep handlers orchestration-focused; move domain logic into services.
- Prefer official Fastify plugins and verify their Fastify compatibility range.
- Do not block the event loop with image processing, large JSON transforms, or synchronous filesystem work.
- Never trust client-supplied identity, role, revision, ownership, or visibility claims.
