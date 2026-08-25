---
name: ask-cto
description: "Use only when the user asks which skill or flow."
version: 1.4.0
author: Merlin, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [routing, cto]
    related_skills: [how-to-talk, writing-for-agents, cli-agent-first]
---

# Ask CTO

You don't remember every skill, so ask.

Load this skill only when the human explicitly asks which skill, flow, or mode to use. If they already named a skill, or they asked you to do the work, do not load this file.

A **flow** is a path through the skills in this profile. Most work travels one **main flow**. **Modes** from `SOUL.md` decide who writes. Everything else is an on-ramp or standalone.

`SOUL.md` is the source of truth for modes, ownership, and the skill lists. This file names the path. It does not add a fifth mode.

`ask-matt` covers the Matt Pocock family only.

## Who writes

Pick one mode before the main flow. Done: one mode is named.

- **Direct.** This session investigates, decides, edits, and proves. Use it when the files are in reach and a separate writer does not help.
- **Subagents.** Independent research or several reviews of one large diff. Load `cto-subagent-development`. Write each child order through `writing-for-agents`. `delegate_task` is the tool inside this mode.
- **Kanban.** The work must survive a restart, cross profiles, wait on blockers, or move through a ticket graph. This profile is the implementer.
- **Coding CLI.** Linear implementation. Load `cli-agent-first`. This profile keeps the goal, the spec, and acceptance. The CLI is the **writer**.

**One writer per worktree.** Parallel research is fine. Parallel writes are not.

If the choice is "me or a writer", load `cli-agent-first` first.

## The main flow: idea → ship

The route most work travels.

1. **Sharpen.** Working directory present: tell the human to type `/grill-with-docs`. No working directory: load `grill-me`. Done: the idea is sharp enough to spec, or the next step is a prototype.
2. **Branch: does a question need a runnable answer?** Detour through `prototype` or `spike`. A prototype lives in its own directory: tell the human to type `/handoff` out and back. Done: one question has a throwaway answer. Do not merge the experiment into the product path.
3. **Branch: is this a multi-session build?**
   - **Yes.** Load `to-spec`, then `to-tickets`. Each ticket is a vertical slice with `blocked_by` edges. Then run one ticket at a time through `implement` or `implement-spec`. Fresh context per ticket.
   - **No.** Load `implement` or `implement-spec` in this window.

   Either way, load `blast-radius` before a non-trivial edit. Prefer `ponytail` and `principle-laziness-protocol` for the smallest native change. Split large work with `principle-sequence-verifiable-units`. If the run keeps stopping short, load `unlazy`. Close with `principle-prove-it-works`. Written code is not done. Done: every acceptance criterion has a test, live output, diff, file, URL, or service state.

Keep steps 1-3 (grill, spec, tickets) in one window. Do not implement inside the spec step.

If the window is filling before tickets exist, read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md). Load `principle-guard-the-context-window`.

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Something is broken.** Load `diagnosing-bugs` when there is no tight loop yet. Load `systematic-debugging` when the loop already fails. Then `principle-fix-root-causes`. A red test as the lock: `tdd`. The human explicitly asked for TDD: tell them to type `/tdd-bug-fix`.
- **Incoming bugs and raw requests.** Load `triage`. Do not triage tickets that `to-tickets` already wrote.
- **Fog: too big for one session, the way is not visible.** Tell the human to type `/wayfinder`. Wayfinder produces decisions, not code. When the map clears, merge at `to-spec`.
- **How does this run?** Load `how`. **Why was it shaped this way?** Load `why`. **Wiki and Mermaid of what exists?** Load `code-wiki`. Do not load two of these for the same question.

## Codebase health

- Tell the human to type `/improve-codebase-architecture` to scan live code for deepening. A chosen candidate enters the main flow at `/grill-with-docs`.
- Load `codebase-design` to design the chosen module.

## Vocabulary underneath

- `principle-model-the-domain` and `domain-modeling`: stateful language, overloaded words, branching rules.
- `codebase-design`: deep module, seam, interface.
- `principle-type-system-discipline`, `principle-boundary-discipline`, `principle-separate-before-serializing-shared-state`: illegal states, validation edges, shared writers.
- `setup-ts-deep-modules`: TypeScript package boundaries.
- `codebase-capability-map`: what the platform can actually do. Skip if it is not installed.

Reach for these when the words or the seams are the problem. Let the flow above pull them in otherwise.

## Review and release

Pick one review skill for one artifact.

- Local diff against spec or standards: `code-review`.
- Pre-commit pass: `requesting-code-review`.
- GitHub pull request: `github-code-review`.
- Kanban review lane: `sdlc-review`.
- Costly or failed work: add `oracle`.
- Merged vs released vs deployed vs live-accepted: `production-release-verification`. Green CI is not live-accepted.

## GitHub

- Auth or `gh` login: `github-auth`.
- Create or triage issues: `github-issues`.
- Issue to a verified PR: `github-issue-to-pr`.
- Branch, commit, open, CI, merge: `github-pr-workflow`.
- Clone, remotes, releases: `github-repo-management`.
- Several coding agents already overlap: `concurrent-coding-agent-coordination`.

## Frontend and product

- New UI: `design-taste-frontend`, then a writer through `cli-agent-first`.
- Existing UI: `redesign-existing-projects`.
- Quality gaps: `frontend-premium-audit`.
- Live exploratory QA: `dogfood`. File defects, then return to the main flow.
- Promise versus live copy: `product-surface-review`.

## Writers and infra

`cli-agent-first` names the writer. This distribution ships `codex`, `claude-code`, and `opencode`. Use `cursor-agent` or `grok` only if installed. A missing CLI is a named gap.

- Containers: `docker-management`.
- Recurring lesson: `principle-encode-lessons-in-structure`. Put it in code, types, tests, or a skill.

## Phase boundaries

A **phase** ends when this chunk of work is done: the grilling, the spec, one ticket, the review. At the boundary, pick from [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md). Mid-phase, continue or split leftover isolated work with `delegate_task`.

## Standalone

Off the main flow.

- `research`: cited investigation that should leave a file. Feed that file into `/grill-with-docs`.
- `resolving-merge-conflicts`: already mid-merge or rebase. It never runs `--abort`.
- `hermes-agent`: Hermes setup or diagnosis. Official docs first.
- `remote-machine-access`: Mac or remote host over SSH.
- `wizard`: steps only a human can click.
- `wait-what-bro`: the last answer did not land.
- `writing-for-agents`: any text another agent will execute.
- Tell the human to type `/ask-matt` only for the Matt Pocock family.
- Tell the human to type `/handoff` when a new harness, directory, or colleague needs a portable file.
- Tell the human to type `/to-questionnaire` when the missing facts live in someone else's head.

## Ownership

Inspect live project state and repository instructions before the first write.

Owned by the current user: full cycle is allowed. Shared, client, or unclear: read, local implementation, and tests. External git mutations need explicit permission.

Name skills by their frontmatter `name`. Write `to-spec`, not `mattpocock/to-spec`.

If a named skill is not installed, say so. Do not invent a cousin.
