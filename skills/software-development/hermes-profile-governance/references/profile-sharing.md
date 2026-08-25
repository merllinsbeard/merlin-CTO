# Hermes profile sharing

Use this reference when a user asks to share, clone, export, publish, or fully reproduce a Hermes profile.

## Choose the artifact first

- **Profile Distribution** is the publishable artifact. It should contain portable behavior: `SOUL.md`, selected runtime configuration, materialized `skills/`, plugins, MCP configuration, and explicitly owned automation.
- **Profile export/import** is a personal backup or same-owner migration. It is not a safe publishing format: profile state, private memory, sessions, logs, caches, and machine-local runtime entries are separate concerns.

Do not call a profile "fully shared" until the target has the identity, behavior, required integrations, and a verified clean install. Credentials, user memory, project access, and external knowledge stores remain separate dependencies.

## Distribution gate

Before packaging a profile:

1. Inventory the profile root and classify every top-level path as portable behavior, user data, runtime state, secret, or machine-local infrastructure.
2. Resolve every skill symlink. Hermes distribution installation rejects symlinks (`_reject_distribution_symlinks` in `hermes_cli/profile_distribution.py`); copy the target directory contents into the distribution and preserve license files.
3. Use an explicit `distribution_owned` allowlist for the intended payload. Include `SOUL.md`, `config.yaml`, `skills`, `plugins`, and only the automation/MCP paths actually intended for recipients.
4. Remove absolute paths, local usernames, private project paths, provider credentials, bot tokens, and private memory from portable config. Replace them with documented environment requirements or recipient-local configuration.
5. Install into a fresh profile and verify the expected skill index, config behavior, plugin loading, and one representative chat/tool workflow.

## Backup gate

Use export only after inspecting the live profile for sockets, FIFOs, caches, multi-gigabyte home/workspace directories, and symlinked skill trees. A live gateway socket is runtime state, not profile content. A large profile home is evidence that export is the wrong sharing boundary, not a reason to publish the archive.

For an export failure, preserve the exact error and classify it as either a profile-content boundary problem or a local setup problem. Never turn a single failed run into a blanket claim that Hermes cannot export profiles; inspect the current implementation and upstream first.

## Reproduction evidence from the CTO profile

The CTO profile had 93 skill symlink entries: 48 vendor-local, 24 shared default-profile, 10 from another profile, and 11 from a Hermes release. Its profile home was 6.7 GB. Running the native export attempted to traverse runtime/profile content and failed on `gateway.sock`; therefore a materialized, curated distribution was the validated path for sharing behavior, while the uncurated export was not.

The installed Hermes tree was checked against `origin/main`; no relevant export or distribution fix was present in the inspected commits. Recheck upstream before repeating this conclusion after an upgrade.

## What must stay external

Keep these outside a public distribution unless the user explicitly requests a private same-owner migration and the transport is controlled:

- OAuth/API credentials and `.env` files;
- `USER.md`, `MEMORY.md`, sessions, logs, state databases, and gateway runtime state;
- OpenViking credentials and private indexes;
- GitHub/Docker/rclone credentials and project registry;
- repository working trees, production directories, and deployment receipts.

A recipient needs a separate setup contract for those dependencies. Treat a successful install as proof of packaging only, not proof of the full external workflow.
