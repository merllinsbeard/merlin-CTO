# Telegram OIDC quirks (oauth.telegram.org)

Verified live 2026-08-22 against `https://oauth.telegram.org`.

## Endpoints (from official discovery)

- discovery: `https://oauth.telegram.org/.well-known/openid-configuration`
- authorization: `https://oauth.telegram.org/auth`
- token: `https://oauth.telegram.org/token`
- JWKS: `https://oauth.telegram.org/.well-known/jwks.json`
- Supported: `response_type=code` only, PKCE `plain`/`S256`, `client_secret_basic`/`client_secret_post`, algs `RS256` `ES256` `EdDSA` `ES256K` (docs: `EdDSA`/`ES256K` incompatible with `profile`/`phone` scopes).
- Scopes: `openid`, `profile`, `phone`, `telegram:bot_access`. No UserInfo endpoint, no revocation, no refresh token; `id_token` TTL 3600s.
- Allowed origins/redirect URIs are registered via `@BotFather mini app → bot → Login Widget` (docs still say "Bot Settings → Web Login" — outdated).

## Hard limit: `state` ≤ 256 characters

Telegram's docs describe `state` as "a random string" with no length cap. Reality, measured by sweeping lengths against the live `/auth` endpoint:

| `state` length | response |
|---|---|
| ≤ 256 | full login UI page (~7–12 KB) |
| ≥ 257 | 14-byte plaintext body: `state too long` |

The error page is rendered by Telegram as bare Times-like text, so in a browser it looks like an empty white page with "state too long" in the corner.

## Auth.js (`next-auth@5.0.0-beta.32` / `@auth/core@0.41.3`) state encoding

With `checks: ["pkce", "state", "nonce"]` (the OIDC default), Auth.js sets `state` to an **encrypted JWE** (`A256CBC-HS512`, payload `{origin, random}`, salt `encodedState`) — measured **~435 chars** with a 64-char secret, ~540 with origin data. This exceeds Telegram's 256 cap, so every sign-in failed with `state too long`. Repro: real Playwright click-through against production captured the exact 435-char state in the redirect.

## The fix (shipped pattern)

Remove `"state"` from the provider `checks` (`["pkce", "nonce"]`). Behaviorally clean in this Auth.js version:

- `authorization-url.js` → `checks.state.create()` returns `undefined` when the provider has no `"state"` check, so no `state` param and no state cookie. It throws `InvalidCheck` only if `origin` data was passed (redirect-proxy flows) — verify none is used.
- Callback: `checks.state.use()` is `useCookie("state")`, which short-circuits when the check is absent; `oauth4webapi.validateAuthResponse` gets `undefined` expectedState and skips validation.

Protection equivalence: CSRF/replay stay covered by one-time `code_verifier` (PKCE S256, HttpOnly sealed cookie) + `nonce` claim verified against the sealed nonce cookie, plus full `id_token` verification (JWKS signature, `iss`, `aud`, `exp`). Only acceptable when the provider has no redirect-proxy flow and state carried no product data.

Tests/docs to update in the same commit: any unit test pinning `checks` and any docs listing the flow's checks.

## Related Auth.js deployment gotcha (stacking bug)

Without `AUTH_URL` (or `trustHost` + correct forwarded headers), Auth.js builds redirect URIs from the internal request URL: observed `redirect_uri=http://0.0.0.0:3000/...` style `http://` origins and `{"error":"origin_forbidden"}` on `/api/auth/signin`. Fix: set `AUTH_URL=<public https origin>` in the web container env. Check the **deployed** image revision against `origin/main` — the running stack may predate both fixes.

## Repro script shape

```js
// playwright: capture the outgoing provider request
page.on("request", (r) => {
  if (r.url().includes("oauth.telegram.org")) {
    const u = new URL(r.url());
    console.log(JSON.stringify({
      redirect_uri: u.searchParams.get("redirect_uri"),
      state_length: (u.searchParams.get("state") ?? "").length,
      has_nonce: u.searchParams.has("nonce"),
    }));
  }
});
```
