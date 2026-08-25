# Acceptance gates

## G1. Portable distribution

- [x] The repository contains a valid Hermes `distribution.yaml`, portable `config.yaml`, public `SOUL.md`, materialized skills, and installation documentation.
  CHECK: `python scripts/verify_distribution.py .`
  EXPECT: exit 0 and `distribution verification: PASS`
  EVIDENCE: verifier passes with 117 materialized skills.

## G2. Public-data boundary

- [x] The committed tree contains no credentials, sessions, memories, personal paths, private project identifiers, runtime databases, caches, sockets, or symlinks.
  CHECK: `python scripts/verify_public_tree.py .`
  EXPECT: exit 0 and `public tree verification: PASS`
  EVIDENCE: re-run against the positioning commit before release.

## G3. Secret scan

- [x] Gitleaks reports no findings in the committed history.
  CHECK: `gitleaks git --no-banner --redact=100 .`
  EXPECT: exit 0
  EVIDENCE: re-run against the positioning commit before release.

## G4. Clean installation

- [x] Hermes installs the distribution into a disposable named profile and recognizes the resulting profile.
  CHECK: `scripts/smoke_install.sh`
  EXPECT: exit 0 and `isolated install smoke: PASS`
  EVIDENCE: smoke installs 117 skills, rejects maintainer-only paths, and removes the profile.

## G5. Agent behavior

- [x] The installed profile answers as a CTO for its current user, names its repository safety boundary, and does not claim the publisher's identity, memory, repositories, or infrastructure.
  EVIDENCE: live model response stated all four boundaries and required real execution evidence.

## G6. Public GitHub publication

- [x] `merllinsbeard/merlin-CTO` is public and its default branch is `main`.
  CHECK: `gh api repos/merllinsbeard/merlin-CTO --jq '{visibility,default_branch,homepage}'`
  EXPECT: public, main, homepage points at the latest release
  EVIDENCE: live API read on 2026-08-25. Homepage and release are set with this drop.

## G7. CI and receipt

- [ ] Every push and tag runs distribution verification, public-tree verification, and gitleaks. The GitHub Release for `v1.0.0` carries a receipt for commit, tree, skill count, and verifier output.
  CHECK: `python scripts/write_release_receipt.py --check <receipt>` and the Actions run on that SHA
  EXPECT: receipt PASS, workflow conclusion success
  EVIDENCE: pending push
