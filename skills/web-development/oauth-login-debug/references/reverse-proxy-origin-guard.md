# False 403 after successful OAuth behind a reverse proxy

Use when OAuth/OIDC callback succeeds, session-bound reads work, but the first browser mutation (for example, `POST /api/conversations`) redirects to a generic forbidden page.

## Diagnostic split

Do not treat all 403s as grant failures. Prove the layers separately:

1. **Session:** an authenticated read such as `/api/auth/session` or `/v1/me` succeeds.
2. **Registry/backend:** the identity has an active grant and backend reads return 200.
3. **Web mutation:** capture the exact browser request and response before it reaches the backend.

If backend logs contain the successful reads but no corresponding POST, the denial is in middleware/route protection, not the access registry.

## Exact browser probe

Use real Chromium, not curl alone. An empty same-origin POST can legitimately omit `Origin` while still sending a public `Referer`:

```text
POST /api/conversations
Origin: null
Referer: https://public.example/
```

Behind a reverse proxy, framework `request.url` may be internal (`http://0.0.0.0:3000/...`). Comparing the public Referer against that internal origin creates a false 403.

For an authenticated automated probe, generate a short-lived session through the application's own JWT encoder and production secret without printing either value; set the HttpOnly cookie in a fresh browser context; perform the mutation; and immediately delete any test object created. Log only status, error code, `Origin`, and `Referer`.

## Safe repair

Use the explicitly configured public application origin (for Auth.js deployments, normally `AUTH_URL`) as the canonical expected origin. Preserve fail-closed behavior:

- matching `Origin` -> allow;
- absent `Origin` + matching `Referer` -> allow;
- foreign `Origin` or `Referer` -> reject;
- absent `Origin` and absent `Referer` -> reject;
- malformed configured public URL -> reject;
- if no public URL is configured in local development, fall back to `request.url`.

Do not trust arbitrary `X-Forwarded-*` headers as the primary repair. An explicit public URL has a narrower trust boundary.

## Proof ladder

1. Regression test with public configured origin, internal request URL, and public Referer (RED before the fix, GREEN after).
2. Tests for matching Origin, foreign Referer, originless+refererless rejection, and malformed public URL.
3. Build production bundle.
4. Start that already-built bundle with the public URL supplied only at runtime. Verify:
   - public Referer -> reaches auth layer (typically 401 without a session), not origin-forbidden;
   - foreign Referer -> 403 origin-forbidden.
5. After deploy, repeat the authenticated real-browser mutation and verify the backend received it.

A green OAuth callback, health check, or authenticated GET does not prove this path. The slice closes only when the first real browser mutation succeeds.