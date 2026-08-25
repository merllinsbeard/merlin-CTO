---
name: durable-static-site-forms
description: Use when a static site must actually store form submissions.
version: 1.0.0
metadata:
  tags: [forms, static-sites, sqlite, privacy, deployment]
---

# Durable static-site forms

Turn a form on a static or serverless-hosted site into real, durable data capture. A prepared email is not a submitted lead. Completion means the server acknowledged the request and the record can be read back from the system of record.

## 1. Choose storage that matches the runtime

First classify the host:

- **Ephemeral serverless filesystem:** do not put the system of record in local SQLite or `/tmp`. Use a managed database or a separate long-lived service.
- **Long-lived server or container host:** SQLite is valid when one small service owns the database file on a persistent volume.
- **No authenticated backend available:** use a transparent mail-client flow only if the stakeholder accepts manual send. Say "prepared", not "sent".

Reject SQLite-over-object-storage, commit-the-database-to-Git, and other concurrency workarounds. They are fragile substitutes for a database owner.

Completion criterion: the selected store survives process restarts and redeploys, and one component owns writes.

## 2. Freeze the form contract

Name the browser origin, API URL, payload, consent, retention, and success semantics before editing.

A minimal lead has:

- optional display name;
- required contact;
- explicit consent;
- empty honeypot;
- server-assigned creation time, source, status, and identifier.

Validate body size, content type, field lengths, contact shape, consent, and origin at the HTTP boundary. Use parameterized SQL. Never interpolate form values into SQL, HTML, logs, or URLs.

Support both:

- JSON for enhanced browser submission;
- `application/x-www-form-urlencoded` for native no-JavaScript submission.

A native success may return `303` to the originating page. JavaScript success requires a successful HTTP response, then resets the form and reports the stored state.

## 3. Minimize retained data

Store only what the follow-up workflow needs. Do not retain raw IP addresses or browser user agents by default.

For abuse controls:

- derive a keyed hash from the client address;
- keep a separate short-lived attempt table;
- deduplicate a normalized contact with a keyed hash;
- rate-limit attempts, not only inserted rows;
- return success for a filled honeypot without storing it.

A retention promise needs an independent mechanism. Cleanup only during new submissions can miss the deadline when traffic stops. Run cleanup on startup and from a timer or background sweep; keeping transaction-time cleanup is useful as a second guard.

Completion criterion: the privacy copy matches the actual schema and cleanup schedule.

## 4. Establish a trusted proxy boundary

CORS is not authentication and public forwarding headers are attacker-controlled.

If a reverse proxy is the only caller that can reach the service:

1. keep the application port off the public host network;
2. connect proxy and service through a private network;
3. remove public `CF-Connecting-IP` and `X-Forwarded-For` headers;
4. overwrite one private application-specific header with the proxy's observed remote address;
5. make the application reject requests that lack that private header;
6. hash the value before storage.

Do not read a fallback IP from arbitrary public headers. Prove spoof resistance by rotating submitted forwarding headers from one real client and showing the rate limiter still sees one identity.

## 5. Deploy without coupling lifecycles

Keep the form API in its own image, Compose project, data directory, and health check. Reuse a shared reverse proxy only for ingress.

Use:

- an immutable image tag tied to the committed revision;
- a secret salt in a protected runtime env file;
- read-only container root filesystem;
- dropped Linux capabilities and `no-new-privileges`;
- a persistent data mount;
- a health endpoint that reads SQLite;
- a documented local-only export command.

When changing a file-mounted Caddyfile, preserve the mounted inode or recreate the proxy container. Replacing the host path can leave the running container pinned to the old inode. A successful reload of unchanged config is not proof the new host file is active.

Detailed Caddy and SQLite pattern: [references/caddy-sqlite-sidecar.md](references/caddy-sqlite-sidecar.md).

## 6. Prove the complete chain

Run checks in this order:

1. pure validation and database tests;
2. native form and JSON API tests;
3. rate-limit, dedupe, honeypot, origin, and retention tests;
4. container build and health check;
5. reverse-proxy candidate validation;
6. local responsive form QA;
7. production TLS and health read-back;
8. one real production submission;
9. exact SQLite read-back of that row;
10. deletion of the synthetic row and `PRAGMA quick_check`.

Also fetch the deployed JavaScript and confirm it uses the API, reports success only after HTTP acknowledgement, and contains no obsolete `mailto:` path.

Completion criterion: a production submission becomes one durable row, the exact row is read back, synthetic evidence is cleaned up, and the live service remains healthy.

## Pitfalls

- Calling `mailto:` a submitted form.
- Using local SQLite inside an ephemeral function.
- Trusting browser CORS to stop non-browser clients.
- Trusting `CF-Connecting-IP` or `X-Forwarded-For` directly in the app.
- Counting only inserted rows for rate limiting, so duplicates bypass the limit.
- Promising 90-day deletion when cleanup runs only on writes.
- Reporting proxy reload success without reading the public HTTPS endpoint.
- Keeping synthetic production leads after verification.
