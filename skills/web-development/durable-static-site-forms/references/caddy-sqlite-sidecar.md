# Caddy and SQLite sidecar pattern

This reference records a validated pattern for a static frontend that submits to a small SQLite service on a long-lived Docker host.

## Topology

```text
static site (HTTPS)
  -> public Caddy vhost
  -> private Docker network
  -> one lead API container
  -> bind-mounted SQLite database
```

The API container publishes no host port. Caddy and the service share one external Docker network. Keep the API Compose project, data directory, image tag, and lifecycle separate from unrelated applications.

## Proxy boundary

Use an application-specific header. The proxy overwrites it; the application never trusts public forwarding headers.

```caddyfile
api.example.com {
  encode zstd gzip

  handle /healthz {
    reverse_proxy lead-api:8080
  }

  handle /v1/leads {
    reverse_proxy lead-api:8080 {
      header_up -CF-Connecting-IP
      header_up -X-Forwarded-For
      header_up X-Lead-Client-IP {remote_host}
    }
  }

  handle {
    respond "Not found" 404
  }
}
```

The service must reject a lead request without `X-Lead-Client-IP`. It hashes that value with a runtime secret before rate-limit or dedupe storage.

Prove the boundary live: send six requests from one machine while rotating fake `CF-Connecting-IP`, `X-Forwarded-For`, and `X-Lead-Client-IP` values. The sixth request must still return `429`, and the five rows must contain one distinct IP hash.

## SQLite ownership

Use one writer service and a persistent host directory:

```yaml
services:
  api:
    image: ${LEADS_IMAGE:?set LEADS_IMAGE}
    read_only: true
    volumes:
      - ./data:/data
    networks:
      - edge
    cap_drop: [ALL]
    security_opt: [no-new-privileges:true]

networks:
  edge:
    external: true
```

Initialize SQLite with WAL mode, `busy_timeout`, parameterized statements, and explicit transactions for rate-limit check plus insert. Keep attempts in a separate table so duplicate contacts cannot bypass the rate limit.

A practical schema stores:

- random lead ID;
- creation timestamp;
- optional name;
- contact and classified contact kind;
- keyed contact hash;
- source and status;
- keyed IP hash.

Do not store raw IP or user agent unless a documented requirement needs them.

## Retention

Delete expired rows through three independent opportunities:

1. process startup;
2. each insert transaction;
3. hourly timer or background sweep.

The third path is required for an honest maximum-retention promise when traffic stops.

## File-mounted Caddy configuration

A bind mount of one file can remain attached to the old inode when deployment replaces the host path. Symptoms:

- the host file contains the new vhost;
- `caddy reload` says the config is unchanged;
- the new TLS hostname still fails.

Safe choices:

- update the existing file in place, preserving its inode, then reload;
- or replace the file and explicitly recreate the proxy container so it remounts the path.

Validate a candidate before either action. Afterward, verify the new HTTPS endpoint, certificate subject, and pre-existing vhosts.

## Production proof

1. Read the deployed form action and JavaScript asset.
2. Submit a synthetic lead through the public hostname.
3. Read the exact SQLite row locally.
4. Assert contact kind, source, status, and fixed hash lengths.
5. Delete only synthetic rows and their attempt records.
6. Run `PRAGMA quick_check`.
7. Read container image, running state, and health.

Do not leave synthetic PII in the database.
