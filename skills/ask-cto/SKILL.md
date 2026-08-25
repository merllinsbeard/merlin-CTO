---
name: ask-cto
description: Route engineering work to the right CTO flow.
disable-model-invocation: true
version: 1.0.0
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

## When to use

- The human typed `/ask-cto`.
- The human asks which flow or skills to use.
- The request sits on more than one skill family.

If the human already named a skill, load that skill. Do not reroute it.

`ask-matt` covers the Matt Pocock family only. It is not this profile's router.

## How to answer

1. Inspect live project state, repository instructions, and ownership before choosing.
2. Pick one lane, one owner, the smallest supporting set, and a checkable proof.
3. Name skills by their frontmatter `name` only. Write `to-spec`, never `mattpocock/to-spec`.
4. User-invoked skills cannot be fired from here. Tell the human to type them: `/grill-with-docs`, `/wayfinder`, `/handoff`, `/improve-codebase-architecture`, `/to-questionnaire`, `/tdd-bug-fix`, `/ask-matt`.
5. Load model-invoked skills with `skill_view`.
6. Open a reference file only when this file is not enough.

## Orchestration lane

Choose one:

- **Direct.** Small reversible change. Files already in reach. This session investigates, edits, and proves the result.
- **Subagents.** Independent read-only research or isolated file sets. Load `cto-subagent-development`. Write child orders through `writing-for-agents`. One writer per worktree.
- **Kanban.** Work must survive a restart, cross profiles, wait on blockers, or move through a ticket graph. This profile is the implementer. Load `ticket-campaign-execution` for the graph. Load `sdlc-review` only in the review lane.
- **Coding CLI.** Linear implementation, UI, browser proof, or a costly failure. Load `cli-agent-first`. This profile keeps the outcome, decisions, and acceptance. The CLI is the writer.

If two lanes fit, pick the cheaper one that still finishes with evidence.

## Execution owner

After the lane is named, name the owner:

- Direct lane: this Hermes session.
- Subagent lane: named children. The parent keeps acceptance.
- Kanban lane: the assigned worker on the card.
- Coding CLI lane: one installed writer chosen by `cli-agent-first`. This distribution ships `codex`, `claude-code`, and `opencode`. Do not name a writer that is not installed.

Never give two writers one mutable worktree.

## Supporting skills

Load `how-to-talk` before any human-facing text. Load `writing-for-agents` before any agent-facing text. Load `unslop` before sending prose to a human.

Then add only the family the request needs. Resolve overlaps with the collision rules below. Use [references/routing-map.md](references/routing-map.md) when the family is still unclear.

## Verification contract

Name the proof before work starts. Written code is not done.

A result is complete only with real evidence: tests, live output, a diff, a file, a URL, or service state.

Keep these states separate: implemented, merged, released, deployed, live-accepted.

Stop only when the named proof exists, or on a named external blocker.

## Collision rules

### Understand

- Runtime behavior, walkthrough, placement: `how`.
- Motivation, rejected alternatives, cited history: `why`.
- Repo overview, module docs, Mermaid wiki: `code-wiki`.
- Primary-source investigation that should leave a cited file: `research`.
- LOC and language inventory: `codebase-inspection`.
- Fact-grounded architecture picture: `software-architecture-visualization`.

Do not load two of these for the same question.

### Plan and architecture

- Sharpen an idea in a repo: tell the human to type `/grill-with-docs`.
- Sharpen an idea with no repo: `grill-me`.
- Huge foggy effort: tell the human to type `/wayfinder`. After the map is clear, load `to-spec`.
- Agreed design to a spec: `to-spec`, then `to-tickets`.
- Markdown plan with no execution: `plan`.
- Stateful domain language: `principle-model-the-domain` and `domain-modeling`.
- Module shape: `codebase-design`.
- Scan a live codebase for deepening: tell the human to type `/improve-codebase-architecture`.
- Throwaway design question: `prototype` or `spike`.

Do not start `to-spec` until the design is agreed. Do not start `implement` until tickets exist, unless the change fits one session.

### Build

- Small reversible fix: Direct + this session + `blast-radius` + `principle-fix-root-causes` + `principle-prove-it-works`.
- Feature in one session: `implement` or `implement-spec`.
- Ticket graph: `ticket-campaign-execution`, plus `cli-agent-first` when writers are needed.
- Explicit TDD request: tell the human to type `/tdd-bug-fix`, or load `tdd` when the red test is the right defect boundary.
- Prefer `tdd` over `test-driven-development`.

### Review and release

- Before a non-trivial edit: `blast-radius`.
- Diff against a spec or standards: `code-review`.
- Pre-commit local review: `requesting-code-review`.
- GitHub PR review: `github-code-review`.
- Kanban review lane: `sdlc-review`.
- Second model: `oracle`.
- Production: `production-release-verification`. Never treat merged, green CI, or a health check as live-accepted.

### Frontend and product

- New UI: `design-taste-frontend`, then implementation through `cli-agent-first`.
- Existing UI upgrade: `redesign-existing-projects`.
- Quality gaps: `frontend-premium-audit`.
- Live exploratory QA: `dogfood`.
- Promise versus live copy: `product-surface-review`.

## After the route is named

1. Load the named model-invoked skills.
2. If the next step is user-invoked, tell the human the exact `/name` and wait.
3. Execute the route until the verification contract has evidence.
4. Delete dead code. Prefer the smallest native fix.

## References

- Whole lifecycle: [references/development-playbook.md](references/development-playbook.md)
- Request type to skills: [references/routing-map.md](references/routing-map.md)
- Executable recipes: [references/recipes.md](references/recipes.md)

## Pitfalls

- Using `ask-matt` as the profile router.
- Naming a skill by folder path.
- Starting two writers in one worktree.
- Collapsing merged, released, deployed, and live-accepted.
- Loading the catalog instead of one route.

## Verification

Done: the answer contains the four contract fields, every named skill exists in this profile, user-invoked next steps are written as `/name`, and work either waits on that invocation or continues until the named proof exists.
