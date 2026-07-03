# Routes

- Keep route handlers thin: parse validated input, authorize, call a service, map the result.
- Group routes by domain plugin and prefix at registration time.
- Define explicit status codes and response schemas for success and expected errors.
- Do not embed database transactions or cross-domain policy directly in route handlers.
