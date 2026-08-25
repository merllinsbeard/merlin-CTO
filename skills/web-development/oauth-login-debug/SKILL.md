---
name: oauth-login-debug
description: "Debug live OAuth/OIDC login failures via probes."
---

# OAuth Login Debug

Live login failures (provider error page, `state` rejected, redirect back to login, origin errors) are protocol-level: fix them with live probes and the actual library source, not by guessing from docs.

## Loop

1. **Reproduce against the live site first.** Capture the exact outgoing authorization request. Headless Playwright with a request listener is the reliable way:

   ```js
   page.on("request", (r) => { if (r.url().includes(PROVIDER_HOST)) log(r.url()); });
   // open login page, click the sign-in button, waitForURL(/provider|error/)
   ```

   Log every query param's **presence and length** (`redirect_uri`, `scope`, `state`, `nonce`, `code_challenge`). The failing param is usually visible by shape, not by name.

2. **Read the bundled library, not the docs.** What the framework actually sends lives in `node_modules` inside the *deployed* image or local checkout. Auth.js example: `@auth/core/lib/actions/signin/authorization-url.js` (what goes into the URL), `.../callback/oauth/checks.js` (create/use/decode of state/pkce/nonce), `.../callback/index.js` and `oauth/callback.js` (callback validation). Grep for the provider config (`checks:`, `issuer`, `authorization`) to find the site's provider file, then trace from there.

3. **Probe the live provider for the real limit.** Providers enforce undocumented constraints. Find them empirically with a curl sweep against the real authorization endpoint, classifying the response body:

   ```bash
   for len in 64 128 200 255 256 257 300; do
     body=$(curl -sS "https://<auth-endpoint>?client_id=$CID&redirect_uri=$URI&response_type=code&scope=openid+profile&state=$(head -c $len /dev/zero | tr '\0' 'a')")
     printf '%s %s %s\n' "$len" "${#body}" "$(printf '%s' "$body" | head -c 40)"
   done
   ```

   Error bodies are typically a short distinct page; success is the full login UI. A binary sweep pins the exact boundary. Keep `client_id`/`redirect_uri` real so the probe reaches the same validation.

4. **Fix at the root.** If the framework's payload exceeds a provider limit, reconfigure the framework (drop a check, shorten the payload) — never fork the library. Verify the fix keeps equivalent protection: dropping OIDC `state` is compensated by PKCE `code_verifier` (HttpOnly cookie) + `nonce` claim verification, which holds when no redirect-proxy flow is used.

5. **Prove it end-to-end.** Run the repo's own browser e2e with its OIDC fixture if one exists (full login included); otherwise script the same Playwright repro against a staging/local stack. Unit tests that pin the provider `checks` array must be updated in the same commit.

## Pitfalls

- **Deployed revision ≠ repo HEAD.** Read the running container's image label/revision (`docker inspect --format '{{index .Config.Labels "org.opencontainers.image.revision"}}'`) and compare with `origin/main`. Fixes are not live until the new revision is deployed, and the live bug may already be fixed on main — check branch history before re-fixing.
- **Auth.js specifics:** with `checks: [..., "state", ...]` the `state` parameter is an **encrypted JWE (~430+ chars)**, far longer than a random nonce. Dropping `"state"` from `checks` is behaviorally clean: `checks.state.create` returns without emitting the param, `useCookie` short-circuits on the callback, and `oauth4webapi.validateAuthResponse` receives `undefined` and skips state validation. But `create` throws if `origin` data is passed without the check (redirect-proxy flow) — keep that in mind. Also check `AUTH_URL`/`trustHost`: a missing public origin makes Auth.js emit `http://` internal redirect URIs and `origin_forbidden` errors, which can stack with the provider error.
- **Provider docs understate limits.** Telegram documents `state` as a random string with no length cap; the real cap had to be measured. Trust the probe over the docs for boundary values.
- **Don't conclude from the unit layer alone.** `state` was green in the test suite while production login was broken; only a live repro exposed it.

## References

- `references/telegram-oidc-quirks.md` — Telegram OIDC endpoint facts, the measured `state` limit, and the Auth.js JWE-state fix.
