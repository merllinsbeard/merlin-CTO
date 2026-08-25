# Changelog

## Unreleased

- Add `/ask-cto` as a SOUL explainer: which mode and which listed skills fit the request
- Expand `SOUL.md` with when-to-pick notes for modes and skill groups

## 1.0.1 - 2026-08-25

Patch on the first public drop.

- Run gitleaks from `$RUNNER_TEMP` so the binary never lands in the checkout
- Ignore a local `gitleaks` binary
- Manifest version `1.0.1` so `hermes profile info` matches the green tag

The 1.0.0 GitHub Release remains as history. Its Actions run failed on the receipt step for this reason.

## 1.0.0 - 2026-08-25

First public Merlin CTO distribution.

Hermes `profile install` clones the default branch. This release is the SHA and receipt to compare against that branch.

### Profile

- Portable `SOUL.md`, `config.yaml`, and `distribution.yaml` for architecture, implementation, review, and infrastructure work
- Local Hermes memory by default. No publisher memory, sessions, credentials, or project registry
- 96 materialized skills with a closed `related_skills` graph
- Fail-closed `scripts/verify_distribution.py` and `scripts/verify_public_tree.py`
- Isolated `scripts/smoke_install.sh`

### Distribution

- Public repository `merllinsbeard/merlin-CTO`
- README that states why this profile exists, the five work modes, one real request-to-evidence route, and skill provenance
- GitHub Actions on `main` and tags: distribution verifier, public-tree verifier, gitleaks
- `scripts/write_release_receipt.py` for an immutable commit/tree/skill-count receipt
- GitHub Release `v1.0.0` with that receipt attached

### History note

Commits before this release are unsigned. The build host has no GPG or SSH signing key for `merllinsbeard`. Later signed tags can point at new commits. They cannot rewrite the published root.
