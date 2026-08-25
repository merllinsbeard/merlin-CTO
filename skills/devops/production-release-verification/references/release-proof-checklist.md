# Release proof checklist

Use this as a compact evidence contract. Replace placeholders with values from live command output; never fill counts from memory.

## Identity

- `source_revision`: exact merged commit
- `artifact_digest`: immutable image or artifact digest
- `manifest`: exact manifest consumed by deploy
- `receipt`: private release receipt naming the same identity

## Candidate gates

- [ ] unit/integration: exact `N/N`, exit 0
- [ ] browser/product: exact `N/N`, exit 0
- [ ] typecheck/lint: passed
- [ ] security/container/topology: passed
- [ ] recovery/rollback: passed, or explicit external gate
- [ ] evidence signed and signature verified

## Deployment read-back

- [ ] deploy command consumed the exact manifest
- [ ] running image/revision equals `source_revision` / `artifact_digest`
- [ ] service health and deployment record read back successfully

## Acceptance

- [ ] capability A canary passed with detached evidence
- [ ] capability B canary passed with detached evidence
- [ ] combined scenario passed against the running service
- [ ] persistence/reload, ownership, cleanup, accounting, and failure paths checked when in scope

## Reporting

Use these labels exactly: `merged`, `released`, `deployed`, `live-accepted`.

If any box is open, report the highest reached label and name the next gate. Close the issue only when its acceptance contract is live-accepted.
