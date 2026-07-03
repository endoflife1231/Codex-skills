# Authentication and authorization

- Store sessions in secure, HttpOnly, SameSite cookies for browser applications.
- Rotate or invalidate sessions on credential/security changes.
- Authorization must check server-side campaign membership, role, ownership, and resource visibility.
- Protect state-changing cookie-authenticated routes against CSRF.
- Rate-limit login, invite-code, and abuse-prone endpoints.
