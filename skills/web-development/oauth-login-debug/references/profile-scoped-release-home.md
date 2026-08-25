# Profile-scoped agent HOME during release operations

Use when an otherwise configured production release fails inside a Hermes or
other profile-scoped agent process because subprocesses inherit a different
`HOME` from the human operator shell.

## Symptom split

Do not collapse `release host command failed` into one diagnosis. Read the
transaction stage and live state:

- running container revision unchanged + new offsite backup evidence present +
  candidate images absent locally -> backup passed, image pull failed;
- encrypted archive without its evidence receipt -> local backup completed but
  offsite publication failed;
- exact images present but old containers remain -> inspect migration/index or
  topology-start stages next.

Always read back the current production revision before retrying. A fail-closed
release can complete one safe effect while leaving production untouched.

## Validated repair

A profile can replace `$HOME`, hiding the operator's configured Docker and
rclone files. Pass their paths only to the release process:

```bash
DOCKER_CONFIG=/home/<operator>/.docker \
RCLONE_CONFIG=/home/<operator>/.config/rclone/rclone.conf \
RELEASE_MANIFEST="$manifest" \
PREDEPLOY_VERDICT="$verdict" \
RELEASE_RECEIPT="$receipt" \
make prod-deploy
```

Rules:

1. Verify both config paths exist with private permissions; never print their
   contents or credential values.
2. Probe offsite storage read-only before retrying. Distinguish missing config,
   offline backend, and transfer failure.
3. Do not copy operator credentials into the application `.env`, alter the app
   config fingerprint, or disable backup/pull gates.
4. Reuse only the exact unexpired predeploy verdict and a not-yet-created receipt
   path. If expired, regenerate the verdict through the normal facade.
5. After success, verify the immutable receipt, exact container revisions,
   service health, public endpoints, and the original browser behavior.

Capture the durable lesson as explicit operator config provenance—not as a
negative claim that Docker, rclone, Tailscale, or the release facade is broken.
