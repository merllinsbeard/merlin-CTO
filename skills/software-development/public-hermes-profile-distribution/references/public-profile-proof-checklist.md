# Public profile proof checklist

Use this checklist after the main skill's workflow has been applied.

## Boundary

The public tree contains only portable identity, operating rules, explicit runtime requirements, materialized skills, attribution, and verification scripts. It contains no personal memory, session history, OpenViking indexes, project paths, credentials, OAuth state, message tokens, caches, databases, backups, or sockets.

## Identity and tree

- local `HEAD` is the intended root commit;
- `git rev-list --count HEAD` is one before the first push;
- `git status --porcelain` is empty;
- `git diff --cached --check` is clean;
- committed tree has no forbidden paths, symlinks, or mode `160000` entries;
- manifest count equals materialized skill count;
- gitleaks scans the history and reports no leaks.

## Remote and consumer proof

- GitHub visibility, default branch, license, and topics were read back;
- local `HEAD` equals `git ls-remote origin refs/heads/main`;
- a fresh clone from the public URL has the same `HEAD`;
- committed-tree verification and gitleaks pass in that clone;
- `hermes profile install github.com/<owner>/<repo> --alias` succeeds;
- `hermes profile show` and `hermes profile info` prove the expected version and skill set;
- the disposable smoke profile is deleted and absent from the final profile listing.

A passing install proves packaging and loading only. Report model authorization, live messaging, and application-specific deployment separately unless they were exercised too.
