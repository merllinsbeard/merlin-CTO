---
name: public-hermes-profile-distribution
description: Publish portable Hermes profiles publicly with proof.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, profiles, distribution, github, sanitization, security]
    related_skills: [hermes-profile-governance, hermes-profile-skills, writing-for-agents]
---

# Public Hermes profile distribution

Use this skill when turning a personal Hermes profile into a public profile another person can install. Treat the result as a distribution artifact, not as a copy of the operator's home directory.

## Artifact boundary

Publish only the portable behavior layer:

- identity and operating rules that do not name the original owner;
- portable runtime configuration and explicit provider requirements;
- materialized profile-local skills with their `references/`, `templates/`, and `scripts/`;
- distribution metadata, license/attribution, and verification scripts.

Exclude personal memory, session history, OpenViking indexes, project paths, production procedures, credentials, OAuth state, message tokens, caches, databases, backups, and runtime sockets. Keep application-specific integrations out unless they are deliberately generalized and separately documented.

## Workflow

### 1. Inspect and define the boundary

Inventory the source profile's prompts, config, skills, symlinks, gitlinks, ignored files, untracked files, memory, and external references. Separate reusable behavior from owner-specific state before copying anything. For every repository, provider, path, channel, contact, or operational procedure, decide whether it is public contract, generic example, or private material; private material is removed rather than renamed cosmetically.

### 2. Materialize the distribution

Copy every selected skill directory into the distribution tree, including support files. A source-profile symlink is not portable when its target lives outside the published tree. Remove runtime caches and ensure the manifest's skill count equals the committed materialized tree.

### 3. Build fail-closed proofs

The committed-tree verifier must reject forbidden path classes, symlinks/gitlinks, personal identifiers, missing required files, malformed manifests, and unexpected skill counts. Empty scan output is not proof of success: missing input, malformed input, or a failed probe must return non-zero. Run gitleaks against the commit history and inspect the committed tree, not only the working tree.

### 4. Create the first public commit

Before the first push, require:

- one clean root commit (`git rev-list --count HEAD == 1`);
- clean status and `git diff --cached --check`;
- no forbidden paths or mode `160000` entries in `git ls-tree -r HEAD`;
- successful full verifier, gitleaks, and isolated install smoke.

Set visibility explicitly with `gh repo create ... --public`. Read GitHub back and assert public visibility, expected default branch, license, and topics. Compare local `HEAD` to `git ls-remote origin refs/heads/main`, then inspect the remote recursive tree for the same boundary invariants.

### 5. Prove the consumer path

A repository page or successful push is not an installation proof. Clone the public URL into a fresh directory, compare the clone's `HEAD` to the published SHA, rerun the committed-tree verifier and gitleaks, and run the smoke installer from that clone. Then exercise the exact user path:

```bash
hermes profile install github.com/<owner>/<repo> --alias
hermes profile show <alias>
hermes profile info <alias>
```

Use a disposable profile name for the smoke. Assert its metadata and selected skill count, then delete it and verify cleanup by listing profiles. Do not report success from installer stdout alone.

## Release blockers

- A gitlink or symlink depends on the publisher's filesystem.
- Public config contains a real project, channel, contact, token, memory, or production path.
- A verifier passes when its input is absent, malformed, or empty.
- A manifest claims skills are included while the tree contains only links or a partial subset.
- Only a local install was tested; the public GitHub URL was not installed.
- The published root commit is rewritten after push. Add a corrective commit instead.

Record untested boundaries separately. A successful install proves packaging and loading, not model authorization, live messaging, or application-specific deployment.

## References

The detailed packaging boundary, proof sequence, and release-blocker checklist are also stored at `hermes-profile-governance/references/public-hermes-profile-distribution.md` for the governance umbrella.

## Completion criteria

The skill is complete only when the public tree, remote identity, fresh-clone checks, exact GitHub URL install, and disposable-profile cleanup have all been verified with real command output.
