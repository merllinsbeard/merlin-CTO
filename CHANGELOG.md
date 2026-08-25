# Changelog

## 1.0.4 - 2026-08-25

Runtime craft: Postgres, pytest, observability, defensive review, and frontend rules.

- Ten skills: `observability-and-instrumentation`, `database-schema-designer`, `supabase-postgres-best-practices`, `python-best-practices`, `python-testing-patterns`, `security-review`, `vercel-react-best-practices`, `react-best-practices`, `vue-best-practices`, `tailwind-v4`
- `SOUL.md` and `/ask-merlin` name them
- Installed pack is now 117 materialized skills

## 1.0.3 - 2026-08-25

Ask-merlin router and the live-needed skill pack land on the night README.

- `/ask-merlin` routes the whole merlin-cto skill tree when the user asks which skill or flow
- Ten live-needed skills: profile, Desktop, Kanban, OAuth, `setup-ts-deep-modules`, `codebase-capability-map`
- Installed pack is now 107 materialized skills
- Public plates and the quiet reel from 1.0.2 stay first on the homepage

## 1.0.2 - 2026-08-25

Public plates and a short reel.

- `docs/media/overview.png`, `what.png`, `how.png`, `different.png`, `night.png`
- `docs/media/reel.mp4`: same plates, stations fill, sun breathes
- README uses the plates instead of Mermaid

The installed profile payload was still 96 skills.

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
