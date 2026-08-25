# Acceptance gates

## G1. Portable distribution

- [x] The repository contains a valid Hermes `distribution.yaml`, portable `config.yaml`, public `SOUL.md`, materialized skills, and installation documentation.
  CHECK: `python scripts/verify_distribution.py .`
  EXPECT: exit 0 and `distribution verification: PASS`
  EVIDENCE: verifier passes with 90 materialized skills.

## G2. Public-data boundary

- [x] The committed tree contains no credentials, sessions, memories, personal paths, private project identifiers, runtime databases, caches, sockets, or symlinks.
  CHECK: `python scripts/verify_public_tree.py .`
  EXPECT: exit 0 and `public tree verification: PASS`
  EVIDENCE: public-tree verifier passes across 257 files.

## G3. Secret scan

- [x] Gitleaks reports no findings in the committed history.
  CHECK: `gitleaks git --log-opts=-1 --no-banner --redact=100 .`
  EXPECT: exit 0
  EVIDENCE: fresh-clone history scan covered one commit and 1.38 MB; no leaks found.

## G4. Clean installation

- [x] Hermes installs the distribution into a disposable named profile and recognizes the resulting profile.
  CHECK: `scripts/smoke_install.sh`
  EXPECT: exit 0 and `isolated install smoke: PASS`
  EVIDENCE: smoke installs 90 skills, validates the installed tree, and removes the profile.

## G5. Agent behavior

- [x] The installed profile answers as a CTO for its current user, names its repository safety boundary, and does not claim the publisher's identity, memory, repositories, or infrastructure.
  EVIDENCE: live model response stated all four boundaries and required real execution evidence.

## G6. Clean root commit

- [x] The local repository has one root commit, a clean worktree, and all local gates pass against `HEAD`.
  EVIDENCE: fresh-clone proof passed both verifiers, gitleaks, real profile installation, no-gitlink check, and `git show --check`.

## G7. Public GitHub publication

- [ ] `merllinsbeard/merlin-CTO` is public, its `main` SHA equals local `HEAD`, and the remote committed tree passes the forbidden-path audit.
  EVIDENCE: pending
