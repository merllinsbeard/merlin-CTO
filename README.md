# Merlin CTO

A portable Hermes Agent profile for software architecture, implementation, code review, infrastructure, and autonomous engineering work.

The profile ships without its author's memory, sessions, credentials, project registry, or machine-specific paths. Each installation starts with an independent user and local memory.

## Requirements

- Hermes Agent 0.20.5 or newer
- an authenticated `openai-codex` provider with access to `gpt-5.6-sol`
- Git for repository work
- optional coding CLIs used by individual skills

## Install from GitHub

```bash
hermes profile install github.com/merllinsbeard/merlin-CTO --name merlin-cto --alias
```

Inspect the installed profile:

```bash
hermes profile show merlin-cto
merlin-cto doctor
```

Start it inside a project:

```bash
cd /path/to/repository
merlin-cto chat
```

If the model is unavailable on your account, select one you can use:

```bash
hermes -p merlin-cto model
```

Provider credentials are local user data. They are never included in this repository.

## Memory boundary

The distribution uses Hermes local memory by default. It does not include OpenViking configuration, `USER.md`, `MEMORY.md`, sessions, databases, Telegram history, or project data.

To connect a separate memory provider, configure it after installation. Do not reuse another person's memory namespace or credentials.

## Telegram

Telegram is optional and requires a bot token owned by the person installing the profile:

```bash
hermes -p merlin-cto gateway setup
hermes -p merlin-cto gateway install
```

## Updating

```bash
hermes profile update merlin-cto
```

User-owned memory, sessions, credentials, logs, and local workspace data remain untouched during a distribution update.

## Repository contents

- `SOUL.md`: stable CTO behavior and operating rules
- `config.yaml`: portable default model, delegation, memory, and approval settings
- `skills/`: materialized engineering skills with no filesystem symlinks
- `distribution.yaml`: Hermes distribution manifest
- `scripts/`: deterministic publication and installation checks
- `tools/`: maintainer tooling

## Verification

```bash
python scripts/verify_distribution.py .
python scripts/verify_public_tree.py .
gitleaks git --log-opts=-1 --no-banner --redact=100 .
scripts/smoke_install.sh
```

## License

Repository-authored files are MIT licensed. Bundled third-party skills retain their original licenses and attribution. See `THIRD_PARTY_NOTICES.md`.
