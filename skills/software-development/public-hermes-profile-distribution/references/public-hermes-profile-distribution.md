# Public Hermes profile distribution runbook

## Boundary

Publish only portable identity, operating rules, explicit runtime requirements, materialized skills, attribution, and verification scripts. Exclude personal memory, session history, OpenViking indexes, project paths, production procedures, credentials, OAuth state, message tokens, caches, databases, backups, and sockets.

## Pre-push gates

- materialize every selected skill and all support files; no external symlinks;
- verify the committed tree fail-closed: forbidden paths, personal identifiers, symlinks, gitlinks, missing files, malformed manifests, and unexpected skill counts fail;
- run gitleaks against history and the committed tree;
- create one clean root commit before first push; check `git status --porcelain`, `git diff --cached --check`, and `git rev-list --count HEAD`;
- create the public repository explicitly and read back visibility, default branch, license, and topics;
- compare local `HEAD` with `git ls-remote origin refs/heads/main` and inspect the remote recursive tree.

## Consumer proof

Clone the public URL into a fresh directory, compare its `HEAD` to the published SHA, rerun verification and gitleaks, then exercise:

```bash
hermes profile install github.com/<owner>/<repo> --alias
hermes profile show <alias>
hermes profile info <alias>
```

Use a disposable smoke profile, assert its metadata and skill set, delete it, and verify cleanup by listing profiles. Installer stdout alone is not proof.

## Blockers

Stop publication for a gitlink or external symlink, private state in public config, fail-open verification, a partial materialized skill set, a local-only install proof, or an attempt to rewrite the root commit after push. Add a corrective commit after publication instead.

A passing install proves packaging and loading only. Report model authorization, live messaging, and application deployment as separate boundaries unless exercised.
