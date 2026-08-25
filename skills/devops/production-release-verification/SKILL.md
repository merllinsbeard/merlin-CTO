---
name: production-release-verification
description: Verify immutable production releases.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [release, production, immutable-artifacts, canary, verification]
    related_skills: [principle-prove-it-works, unlazy, github-issue-to-pr]
---

# Production release verification

Use this skill when a change must move from merged source to a production artifact and a verified user-visible result. It exists to prevent the most common false finish: treating a green build, a merged PR, or a successful deploy command as proof that production serves the intended behavior.

## The release state machine

Keep these states separate in every report and issue thread:

- **merged** — source revision is in the protected integration branch.
- **released** — an immutable artifact was built, signed or attested, and its digest was verified.
- **deployed** — production is running that exact artifact; read back the running revision.
- **live-accepted** — the required user scenario passed against the running deployment.

A later state implies the earlier ones only when the same immutable revision and artifact identity are carried through. Never collapse the four labels into “done”.

## Procedure

1. **Freeze identity.** Record the source revision, image digest or artifact ID, manifest path, and release receipt path. Use the same identity for every later command.
2. **Run the complete candidate gate.** Include unit and integration tests, browser tests, typecheck/lint, security scans, container/topology checks, recovery, and rollback proof where the repository defines them. Record exact counts and exit status in durable evidence.
3. **Repair findings at the root.** If a gate exposes a real defect, fix the class of defect, merge the fix, and rebuild. The old artifact is invalid even if its source is now corrected.
4. **Publish evidence.** Sign or attest the release evidence and verify the signature. Create a private receipt that names the exact artifact and all acceptance gates.
5. **Deploy the exact manifest.** Run the repository’s native deploy facade with explicit manifest, predeploy verdict, receipt, and environment. Then read back running image/revision, service health, and the deployment record.
6. **Canary sequentially.** Keep gated capabilities disabled by default. Enable one capability, run its detached production canary and inspect logs/metrics; restore or continue only after it passes. Repeat for the next capability, then run the combined acceptance scenario.
7. **Verify the real user path.** Exercise the exact scenario named by the issue, not only health checks or API status. Confirm persistence/reload, ownership, cleanup, accounting, and failure behavior when they are part of the contract.
8. **Close the loop.** Comment the issue with revision, digest, evidence, and the highest verified state. Close it only when the acceptance criteria are live-accepted. If deployment stopped at an earlier state, say so plainly and leave the issue open.

## Registry and receipt preconditions

Before a release build pushes to a registry, validate the active credential’s package-write permission and authenticate the container client explicitly. A denied push is a release precondition failure, not a reason to claim that a local build is an immutable release. Keep credentials out of logs and durable summaries.

## Evidence standard

Prefer deterministic scripts and repository-native release gates over prose. A valid handoff names:

- immutable source revision;
- artifact/image digest;
- signed evidence and verification result;
- exact test counts and skipped suites;
- running production revision after deploy;
- canary and live-acceptance results;
- rollback outcome or explicit remaining gate.

For a compact reusable checklist and receipt fields, see [`references/release-proof-checklist.md`](references/release-proof-checklist.md).

## Pitfalls

- Calling a signed candidate “deployed” before reading the running revision.
- Calling a deployed service “accepted” because healthcheck and CI are green.
- Reusing an artifact built before the final root-cause fix.
- Enabling multiple risky capabilities together before individual canaries pass.
- Closing the issue at merge or release when the user contract requires live production verification.
- Reporting exact counts from memory instead of the test runner’s output.

## Verification

The skill is applied correctly when the final report contains the four state labels, one immutable identity, direct evidence for each claimed transition, and an explicit next gate for any state not reached.
