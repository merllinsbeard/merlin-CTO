# Recipes

Each recipe is one route. Copy the four contract fields into the answer, then execute. Stop when the proof exists.

## Unknown or underspecified request

- **Lane:** Direct.
- **Owner:** this session.
- **Skills:** `how-to-talk`, then `grill-me` if there is no repo. If a repo is present, tell the human to type `/grill-with-docs`.
- **Proof:** a one-sentence outcome, a named next recipe, and either an agreed design note or a waiting `/grill-with-docs` prompt.
- **Boundary:** do not edit files while the outcome is still unnamed.

## Small reversible fix

- **Lane:** Direct.
- **Owner:** this session.
- **Skills:** `blast-radius`, `principle-fix-root-causes`, `principle-laziness-protocol`, `principle-prove-it-works`.
- **Proof:** the named command or user path is green after the change. The diff is read.
- **Boundary:** shared or unclear repos stay local. No push.

## Hard bug or performance regression

- **Lane:** Direct until the loop is red. Subagents only for independent evidence gathering.
- **Owner:** this session.
- **Skills:** `diagnosing-bugs` if no tight loop exists. `systematic-debugging` if the loop already fails. Then `principle-fix-root-causes`. Add `tdd` when a regression test is the lock.
- **Proof:** one command that was red on this bug is now green, and that command is kept.
- **Boundary:** do not theorise a fix before the loop is red.

## Feature in one session

- **Lane:** Direct, or Coding CLI when UI or editor context helps.
- **Owner:** this session, or one writer from `cli-agent-first`.
- **Skills:** `implement` or `implement-spec`, `blast-radius`, `principle-prove-it-works`. Add `tdd` when behaviour is the acceptance boundary.
- **Proof:** every acceptance criterion has direct evidence from this session.
- **Boundary:** one writer, one worktree.

## Architecture or domain decision

- **Lane:** Direct.
- **Owner:** this session.
- **Skills:** `principle-model-the-domain`, `domain-modeling`, `codebase-design`. If a repo exists, tell the human to type `/grill-with-docs` first.
- **Proof:** a written decision with rejected alternatives, ready for `to-spec`.
- **Boundary:** do not load `to-spec` or `implement` until the design is agreed or explicitly assumed as reversible.

## Research, prototype, or spike

- **Lane:** Subagents for reading. Direct for the experiment.
- **Owner:** research children, then this session for the prototype.
- **Skills:** `research` for a cited file. `prototype` for a design question. `spike` for a technical experiment.
- **Proof:** a cited note or a throwaway program that answers one question.
- **Boundary:** do not merge experiment code into the product path.

## Spec and tickets

- **Lane:** Direct.
- **Owner:** this session.
- **Skills:** `to-spec`, then `to-tickets`. Agent-facing text through `writing-for-agents`.
- **Proof:** a spec with checkable acceptance criteria and tickets with `blocked_by` edges.
- **Boundary:** keep this sequence in one window. Do not implement inside the spec step.

## Large multi-ticket campaign

- **Lane:** Kanban for the graph. Coding CLI per ticket when a writer is needed.
- **Owner:** `ticket-campaign-execution` for the graph. One `cli-agent-first` writer per ticket worktree.
- **Skills:** `to-spec`, `to-tickets`, `ticket-campaign-execution`, `cli-agent-first`, `sdlc-review` on review cards, `unlazy` if the campaign stalls.
- **Proof:** every ticket has evidence, review verdicts are recorded, and leftover worktrees are named.
- **Boundary:** one writer per worktree. Do not mix leftover checkouts.

## Code review, PR, or merge conflict

- **Lane:** Direct.
- **Owner:** this session.
- **Skills:** local diff → `code-review` or `requesting-code-review`. Published PR → `github-code-review`. Conflict already in progress → `resolving-merge-conflicts`.
- **Proof:** findings with location, defect, and smallest repair, or a completed merge/rebase that preserves intent.
- **Boundary:** `resolving-merge-conflicts` never runs `--abort`.

## GitHub issue to verified PR

- **Lane:** Coding CLI when implementation is linear. Direct when the change is small.
- **Owner:** `github-issue-to-pr` plus one writer if needed.
- **Skills:** `github-issue-to-pr`, `github-pr-workflow`, `principle-prove-it-works`.
- **Proof:** PR exists, CI state is reported honestly, and local or CI checks for the change passed.
- **Boundary:** do not claim CI is green without reading the run.

## Frontend, redesign, audit, or dogfood

- **Lane:** Coding CLI for implementation. Direct for audit and QA.
- **Owner:** one `cli-agent-first` writer for edits. This session for `dogfood` and audits.
- **Skills:** new UI → `design-taste-frontend`. Existing UI → `redesign-existing-projects`. Gaps → `frontend-premium-audit`. Live QA → `dogfood`. Copy vs product → `product-surface-review`.
- **Proof:** screenshots or live paths for the named surfaces, plus the failing cases found.
- **Boundary:** do not implement during `dogfood`. File defects, then open a build recipe.

## Infrastructure, Docker, remote host

- **Lane:** Direct.
- **Owner:** this session.
- **Skills:** containers → `docker-management`. SSH hosts → `remote-machine-access`. Hermes itself → `hermes-agent`. Human-only clicks → `wizard`.
- **Proof:** the named host or container state was read back after the change.
- **Boundary:** do not invent credentials. A missing login is a blocker.

## Release and exact user scenario

- **Lane:** Direct.
- **Owner:** this session.
- **Skills:** `production-release-verification`, `principle-prove-it-works`, `unlazy`.
- **Proof:** the same revision is merged, released, deployed, and live-accepted, or the highest reached state is named and the work stays open.
- **Boundary:** health checks do not close a user-facing fix.

## Hermes configuration

- **Lane:** Direct.
- **Owner:** this session.
- **Skills:** `hermes-agent`. Official docs first.
- **Proof:** a live CLI or config read shows the new state.
- **Boundary:** no Hermes source fork or patch without an explicit request for that code change.

## Knowledge, handoff, or a recurring lesson

- **Lane:** Direct.
- **Owner:** this session.
- **Skills:** explain → `how` or `why`. Wiki → `code-wiki`. Recurring lesson → `principle-encode-lessons-in-structure`. Session transfer → human types `/handoff`.
- **Proof:** the artifact exists: explanation with citations, wiki files, a structural change, or a handoff file.
- **Boundary:** do not store a recurring lesson only as a reminder in chat.
