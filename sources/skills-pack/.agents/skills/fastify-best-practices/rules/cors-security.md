# CORS and security

- Use an explicit origin allowlist; do not combine wildcard origins with credentials.
- Configure security headers appropriate to the deployed frontend and asset sources.
- Add rate limits, payload limits, request timeouts, and trusted-proxy settings deliberately.
- Validate redirect and proxy targets to prevent open redirects and SSRF.
