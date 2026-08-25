# Telegram OIDC `id` claim shape (2026-08-22 production incident)

The official docs show `id` as a JSON number, but the real production callback delivered it in a form a strict `typeof value === "number"` parser rejects — a numeric string. The token was otherwise valid (signature, issuer, audience, nonce all verified); only the claims parser killed the callback.

## Shipped fix (`web/lib/auth/telegram-oidc.ts`, PR #27)

Normalize at the parser boundary instead of rejecting:

- pass numbers through;
- accept canonical digit-only strings `^[0-9]+$` (no sign, whitespace, exponent, or separators) so the parsed value is exactly what was signed;
- keep `Number.isSafeInteger(value) && value > 0`;
- reject everything else with the same error as before.

Both forms canonicalize to the same session identity string, so identity continuity holds.

## Test shape

The old test `["non-numeric id", { id: "123456789" }]` expecting rejection was *encoding the bug* — flipped it. New regression suite:

- accept production form: `id: "123456789"` → identity `telegram:<sub>:123456789`;
- reject near-misses: `""`, `"+123"`, `"-123"`, `" 123 "`, `"1e8"`, `"abc"`, `0`, `-123`, `123.5`.

Object-valued `id` is not testable via `SignJWT` (functions don't clone); it can't survive JSON serialization into a JWT anyway — don't add it.

## Symptom signature in Auth.js logs

```
[auth][error] OAuthProfileParseError: Read more at https://errors.authjs.dev#oauthprofileparseerror
[auth][cause]: TelegramOidcError: Telegram id claim must be a positive integer
[auth][error] InvalidCheck: pkceCodeVerifier value could not be parsed.
```

The `[auth][cause]:` line carries the real error; the `InvalidCheck` that follows is a cascade artifact — the callback died before consuming the PKCE cookie. Corroborating DB state: no new Web identity created, no internal assertion processed, active grant and bot profile already exist. Retrying login or clearing browser cache does not help until the parser ships.
