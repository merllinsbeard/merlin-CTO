# Development playbook

End-to-end route from a request to a verified result. Open this file when the human asks for the whole process. For a single request, stay in `SKILL.md` or use one recipe.

Two independent axes:

- Orchestration: Direct, Subagents, Kanban, Cron, Coding CLI.
- Execution: this session's native tools, or one coding writer named by `cli-agent-first`.

Do not mix the axes. A Kanban ticket can still be executed by a coding CLI. A Cron job cannot ask a follow-up.

## Intake

1. Read the request once. Name the outcome in one sentence.
2. Inspect live project state: `hermes project` if projects exist, repository `AGENTS.md` / `SOUL.md` / tracker rules, `git status`, branch, worktrees, and ownership.
3. Live Git, files, CI, the running service, and official docs beat memory and old reports.
4. If `openviking` is installed, search it before asking the human to repeat a durable fact. Direct sources still win.
5. Classify ownership before any mutation:
   - Owned by the current user: full cycle is allowed.
   - Shared, client, or unclear: read, local implementation, and tests only. External git mutations need explicit permission.
6. Choose the contract: orchestration lane, execution owner, supporting skills, verification contract.

Done: ownership, lane, owner, and proof are named. No file has been changed yet.

## Decide before building

This is the default path for new behaviour. Skip it only for a one-session reversible fix whose outcome is already named.

1. If the idea is still fuzzy and a repo is present, tell the human to type `/grill-with-docs`.
2. If there is no working directory, load `grill-me`.
3. If the effort cannot fit one session and the decisions are not yet deliverables, tell the human to type `/wayfinder`. After the map is clear, return here.
4. If a question needs a runnable answer before a design can be honest, load `prototype` or `spike`. Keep the experiment throwaway.
5. Stateful or branching rules: load `principle-model-the-domain` and `domain-modeling` before designing modules.
6. Module shape: load `codebase-design`. `/improve-codebase-architecture` is a separate user-invoked survey of a live tree, not the start of a new module.
7. Write agent-facing design notes through `writing-for-agents`.
8. Stop. Wait for the human to agree the design, or in an autonomous session record the assumed design and continue only when that assumption is reversible.
9. Only then load `to-spec`.

Done: the design is agreed or explicitly assumed, and the next artifact is a spec or a one-session change.

## Specify and split

1. Load `to-spec`. The spec must include checkable acceptance criteria.
2. Load `to-tickets`. Each ticket is a vertical slice with `blocked_by` edges.
3. Keep grilling, spec, and tickets in one context window when possible. If the window is filling, load `principle-guard-the-context-window` and split at a phase boundary with `/handoff`.
4. Incoming bugs and raw requests go through `triage`. Tickets produced by `to-tickets` are already agent-ready. Do not triage them.
5. If `to-goal` is installed and the human wants one paste-ready Goal prompt, load it only after the spec and tickets exist.

Done: every ticket can be executed from its own text, and blocking edges are explicit.

## Orchestrate the build

Pick the lane from `SKILL.md`. The lane can change between tickets. It cannot change mid-ticket.

- One-session change: Direct. This session loads `implement` or `implement-spec`.
- Isolated research or isolated file sets: Subagents via `cto-subagent-development`.
- Durable ticket graph: Kanban via `ticket-campaign-execution`.
- Recurring watch or digest: Cron via `cronjob`.
- Linear implementation or costly failure: Coding CLI via `cli-agent-first`.

Invariants for every lane:

- One writer per worktree.
- Parent or this session owns decisions, credentials, release authority, and the final claim.
- Child summaries are claims. Read the diff and run the named check before accepting.
- Reversible work proceeds. Ask only on a true external blocker or an irreversible action outside owned repositories.
- A Cron prompt is self-contained. It does not see this chat.

Done: every in-flight ticket has one owner and one mutable workspace.

## Change the code

1. Load `blast-radius` before a non-trivial edit.
2. Prefer `ponytail` and `principle-laziness-protocol`: the smallest native change that closes the root cause.
3. Load `principle-fix-root-causes`. Do not patch the symptom.
4. Load `tdd` when a red test is the cleanest defect boundary, or when the ticket says so. An explicit TDD request is `/tdd-bug-fix`.
5. Type, boundary, and shared-state rules live in `principle-type-system-discipline`, `principle-boundary-discipline`, and `principle-separate-before-serializing-shared-state`.
6. Delete dead code.
7. Large work goes through `principle-sequence-verifiable-units` and, when the run keeps stopping at 80 percent, `unlazy`.

Done: the diff matches the ticket, and dead code from the change is gone.

## Review

Choose one review skill. Do not stack them on the same artifact.

- Local diff against spec or standards: `code-review`.
- Pre-commit pass: `requesting-code-review`.
- GitHub pull request: `github-code-review`.
- Unpushed local branch, if `branch-review-before-push` is installed: that skill.
- Kanban review lane: `sdlc-review`.
- Costly, irreversible, or failed work: add `oracle` as a second model.

Fix findings at the root. Re-run the affected checks. Do not open a second formal review unless the first review required it.

Done: every finding is fixed or explicitly deferred, and the affected checks pass.

## Merge, release, deploy, accept

Keep the states separate. Load `production-release-verification` as soon as the change must leave the working tree.

1. **implemented.** Local proof exists.
2. **merged.** The revision is on the protected integration branch. Use `github-pr-workflow` or `github-issue-to-pr`.
3. **released.** An immutable artifact exists and its digest was verified.
4. **deployed.** Production is running that exact artifact. Read the running revision back.
5. **live-accepted.** The exact user scenario passed against that running revision.

Green CI, a health check, or a successful deploy command is not live-accepted.

Shared or unclear repositories stop at a reviewable local diff unless the current user gave explicit permission.

## Explain and record

- How the system works: `how`.
- Why it was shaped this way: `why`.
- Onboarding wiki: `code-wiki`.
- A lesson that will recur: `principle-encode-lessons-in-structure`. Put it in code, types, tests, or a skill. Do not leave it as a reminder.
- Session transfer: tell the human to type `/handoff`.
- Human-facing prose: `how-to-talk`, then `unslop`. If the last answer did not land, load `wait-what-bro`.
- Durable facts, if `openviking` is installed: `viking_remember` for one fact in one layer. Do not copy the same fact into local memory.

## Hermes itself

For Hermes configuration, load `hermes-agent`. Source order: official docs, then live config and CLI, then current `origin/main`, then GitHub issues. A native capability beats a local workaround.

If Desktop routes the wrong chat or tab and `hermes-desktop-debugging` is installed, load that skill. Do not treat a Desktop click as one button handler.

Do not create an internal Hermes fork, patch, worktree, or branch unless the current user explicitly authorized that code change.

## Phase hygiene

Stay in one phase until its proof exists. Then either continue with the next recipe or tell the human to type `/handoff`.

Do not carry an unfinished grill into implementation. Do not carry an unfinished implementation into release language.
