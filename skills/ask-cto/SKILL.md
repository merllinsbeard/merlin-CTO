---
name: ask-cto
description: Route engineering work to the right CTO flow.
disable-model-invocation: true
version: 1.1.0
author: Merlin, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [routing, orchestration, cto]
    related_skills: [cli-agent-first, writing-for-agents, how-to-talk]
---

# Ask CTO

This profile's single public interface. It names a route. It does not do the work.

Every answer must contain this contract, in this order:

1. Orchestration lane
2. Execution owner
3. Supporting skills
4. Verification contract

Then either stop, or start the named route.

## Answer shape

Write the contract as four labeled lines, then one next action. Do not write an essay.

```
Lane: Direct
Owner: this session
Skills: blast-radius → principle-fix-root-causes → principle-prove-it-works
Proof: pytest tests/billing/test_proration.py is green after the change
Next: load those skills and edit
```

If the next step is user-invoked, `Next` is the exact `/name` and this session waits.

## When to use

- The human typed `/ask-cto`.
- The human asks which flow or skills to use.
- The request sits on more than one skill family.

If the human already named a skill, load that skill. Do not reroute it.

`ask-matt` covers the Matt Pocock family only. It is not this profile's router.

## How to answer

1. Inspect live project state, repository instructions, worktrees, and ownership before choosing.
2. Live Git, files, CI, the running service, and official docs beat memory and old reports.
3. Pick one lane, one owner, the smallest supporting set, and a checkable proof.
4. Name skills by their frontmatter `name` only. Write `to-spec`, never `mattpocock/to-spec`.
5. User-invoked skills cannot be fired from here. Tell the human to type them: `/grill-with-docs`, `/wayfinder`, `/handoff`, `/improve-codebase-architecture`, `/to-questionnaire`, `/tdd-bug-fix`, `/ask-matt`.
6. Load model-invoked skills with `skill_view`.
7. If a skill named in this router is not installed, say so and pick the closest installed substitute. Do not invent a cousin.
8. After the portable rules, open [references/installed-extras.md](references/installed-extras.md) and apply any extra whose skill is actually installed.
9. Open the other reference files only when this file is not enough.

## Default architecture path

For any new behaviour, domain language, or system shape, this is the default. It is not one option among many.

1. Repo present: tell the human to type `/grill-with-docs`. No repo: load `grill-me`.
2. Wait until the design is agreed. In an autonomous session, write the assumed design down and continue only if that assumption is reversible.
3. Load `to-spec`. Then load `to-tickets`.
4. Only then pick a build recipe.

Do not start `to-spec` from a fuzzy idea. Do not start `implement` from a conversation. A one-session reversible fix may skip this path.

Huge foggy effort goes to `/wayfinder` first. Wayfinder produces decisions, not code. After the map is clear, return to step 3.

## Orchestration lane

Choose one:

- **Direct.** Small reversible change. Files already in reach. This session investigates, edits, and proves the result.
- **Subagents.** Independent read-only research or isolated file sets. Load `cto-subagent-development`. Write child orders through `writing-for-agents`. One writer per worktree. `delegate_task` is a tool inside this lane, not a fifth lane.
- **Kanban.** Work must survive a restart, cross profiles, wait on blockers, or move through a ticket graph. This profile is the implementer. Load `ticket-campaign-execution` for the graph. Load `sdlc-review` only in the review lane.
- **Cron.** The work is a recurring watch, digest, or heartbeat with no human in the loop. Use the `cronjob` tool. A scheduled job gets a self-contained prompt. It cannot ask questions later.
- **Coding CLI.** Linear implementation, UI, browser proof, or a costly failure. Load `cli-agent-first`. This profile keeps the outcome, decisions, and acceptance. The CLI is the writer.

If two lanes fit, pick the cheaper one that still finishes with evidence. Cron wins over "I will remember to check." Kanban wins over a chat that must survive `/new`.

## Execution owner

After the lane is named, name the owner:

- Direct lane: this Hermes session.
- Subagent lane: named children. The parent keeps acceptance.
- Kanban lane: the assigned worker on the card.
- Cron lane: the scheduled job. This session only creates or updates the job.
- Coding CLI lane: one installed writer chosen by `cli-agent-first`. This distribution ships `codex`, `claude-code`, and `opencode`. If `cursor-agent` or `grok` is installed, `cli-agent-first` may name them. Do not name a writer that is not installed.

Never give two writers one mutable worktree.

## Supporting skills

Load `how-to-talk` before any human-facing text. Load `writing-for-agents` before any agent-facing text. Load `unslop` before sending prose to a human.

Then add only the family the request needs. Resolve overlaps with the collision rules below. Use [references/routing-map.md](references/routing-map.md) when the family is still unclear.

## Collision rules

Pick one skill per family. Details live in the routing map.

**Understand.** Runtime and placement: `how`. Motivation and history: `why`. Wiki and Mermaid: `code-wiki`. Cited investigation: `research`. Inventory: `codebase-inspection`. Architecture picture: `software-architecture-visualization`.

**Build.** One-session ticket: `implement`. Spec without tickets: `implement-spec`. Ticket graph: `ticket-campaign-execution`. Red test as the lock: `tdd`. Explicit TDD request: `/tdd-bug-fix`. Prefer `tdd` over `test-driven-development`.

**Review.** Before a non-trivial edit: `blast-radius`. Local diff: `code-review`. Pre-commit: `requesting-code-review`. GitHub PR: `github-code-review`. Kanban review lane: `sdlc-review`. Second model: `oracle`. Production: `production-release-verification`.

**Frontend.** New UI: `design-taste-frontend`. Existing UI: `redesign-existing-projects`. Gaps: `frontend-premium-audit`. Live QA: `dogfood`. Copy vs product: `product-surface-review`.

Do not load two understand skills for the same question. Do not stack two review skills on the same artifact.

## Phase boundaries

Stay in this session while the phase is the same: one recipe, one worktree, one proof.

Start a new phase, or tell the human to type `/handoff`, when any of these is true:

- the next artifact is a different kind (grill notes → spec → tickets → implementation → review → release)
- the context window is filling and the next work is independent
- a new directory, harness, or worktree is required
- a user-invoked skill must run before this session can continue

Do not compact away an unsettled design. Do not continue implementation in the same breath as a spec.

## Verification contract

Name the proof before work starts. Written code is not done.

A result is complete only with real evidence: tests, live output, a diff, a file, a URL, or service state.

Keep these states separate: implemented, merged, released, deployed, live-accepted.

Stop only when the named proof exists, or on a named external blocker.

## After the route is named

1. Load the named model-invoked skills.
2. If the next step is user-invoked, tell the human the exact `/name` and wait.
3. Execute the route until the verification contract has evidence.
4. Delete dead code. Prefer the smallest native fix.

## References

- Whole lifecycle: [references/development-playbook.md](references/development-playbook.md)
- Request type to skills: [references/routing-map.md](references/routing-map.md)
- Executable recipes: [references/recipes.md](references/recipes.md)
- Extra skills, if installed: [references/installed-extras.md](references/installed-extras.md)

## Pitfalls

- Using `ask-matt` as the profile router.
- Naming a skill by folder path.
- Starting two writers in one worktree.
- Opening `to-spec` before the design is agreed.
- Collapsing merged, released, deployed, and live-accepted.
- Loading the catalog instead of one route.
- Pretending an uninstalled writer or extra skill ran.

## Verification

Done: the answer contains the four contract fields in the labeled shape, every named skill exists in this profile or is marked missing, user-invoked next steps are written as `/name`, and work either waits on that invocation or continues until the named proof exists.
