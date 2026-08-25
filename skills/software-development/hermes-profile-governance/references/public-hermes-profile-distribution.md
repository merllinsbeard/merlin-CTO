# Public Hermes profile distribution

Use this runbook when turning a personal Hermes profile into a public profile another person can install.

## Artifact boundary

Publish only the portable behavior layer:

- identity and operating rules that do not name the original owner;
- profile runtime config with provider-neutral or explicitly documented defaults;
- materialized profile-local skills, including each skill's `references/`, `templates/`, and `scripts/`;
- distribution metadata, license/attribution, and verification scripts.

Keep out personal memory, session history, OpenViking indexes, project paths, production runbooks, credentials, OAuth state, message tokens, caches, databases, backups, and runtime sockets. A public profile is a reusable behavior artifact, not a copy of the operator's home directory.

## Pre-push proof

1. Start from a clean source tree and inventory symlinks, gitlinks, ignored files, and untracked files.
2. Materialize every skill into the distribution tree. A symlink that works in the source profile but points outside the published tree is not portable.
3. Run a fail-closed committed-tree verifier. It should reject forbidden path classes, symlinks/gitlinks, personal identifiers, missing required files, and unexpected skill counts. Do not make a verifier pass merely because a scan returned empty output.
4. Run `gitleaks` against the commit history and scan the committed tree, not only the working tree.
5. Create one clean root commit before the first push. Verify `git rev-list --count HEAD == 1`, `git status --porcelain` is empty, and `git diff --cached --check` is clean.
6. For a public repository, set visibility explicitly with `gh repo create ... --public`. Read the repository back and assert `visibility == PUBLIC`, the expected default branch, and the expected license/topics.
7. Compare local `HEAD` with `git ls-remote origin refs/heads/main`; then inspect the remote recursive tree and reject forbidden paths or mode `160000` entries.

## Post-push proof

A repository page is not an installation proof. Clone the public URL into a fresh directory, compare its `HEAD` with the published SHA, rerun the committed-tree verifier and gitleaks, and run the smoke installer from that clone. Then exercise the exact user path:

```bash
hermes profile install github.com/<owner>/<repo> --alias
hermes profile show <alias>
hermes profile info <alias>
```

Use a disposable profile name for the smoke and delete it after the assertions pass. Verify cleanup by listing profiles; do not report success from installer stdout alone.

## Release blockers

- A gitlink or symlink depends on the publisher's filesystem.
- Public config contains a real project, channel, contact, token, memory, or production path.
- A scanner/verifier exits successfully when its input is absent, malformed, or empty.
- A manifest claims skills are included while the tree contains only links or a partial subset.
- Only a local install was proven; the public GitHub URL was not installed.
- The published root commit is rewritten after push. Add a corrective commit instead.

Record what was not tested separately. A successful install proves packaging and loading, not model authorization, live messaging, or application-specific deployment.
