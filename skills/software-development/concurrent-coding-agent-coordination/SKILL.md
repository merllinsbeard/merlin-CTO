---
name: concurrent-coding-agent-coordination
description: Use when coding agents overlap; assign one owner.
---

# Concurrent Coding-Agent Coordination

Use when two or more coding agents, IDE sessions, or automation workers operate on the same repository at the same time.

## Core rule

A worktree isolates filesystem writes, not design ownership. Every mutable implementation surface needs one active writer. Parallel work is safe only when writers own disjoint surfaces or independent worktrees with an explicit integration boundary.

## Workflow

1. **Inventory live surfaces.** Inspect worktrees, branches, dirty state, recent commits, and active agent processes before editing. Do not infer that a worktree is idle from its name.
2. **Build ownership.** Compare changed-file sets and identify the current owner of each implementation surface. Treat overlapping files and overlapping architectural responsibility as a collision even when branches are separate.
3. **Stop competing implementation.** If another agent owns the same files, do not create a third branch, mechanically cherry-pick partial edits, or keep editing a second implementation. Hand concrete acceptance criteria to the active owner; let that branch integrate one coherent design.
4. **Keep orthogonal work separate.** Research, evidence, and documentation may proceed independently only when they do not mutate the owned implementation surface. Give them their own branch or worktree.
5. **Integrate after ownership ends.** Review the owner’s complete diff against requirements, run focused tests, then relevant broader checks. Resolve architecture on the owner branch, not through a blind line-by-line merge.
6. **Publish one verified unit.** The result should be one coherent commit/PR for one implementation surface. Handoff names the owner, changed files, requirements, tests, and uncertainty.

## Human-facing explanation

Lead with concrete state, not process jargon:

> “Cursor A owns these Jibri files. Our audio requirements go to A; we do not create a competing branch. After A finishes, we review one diff and run tests.”

If the explanation is not understood, reduce it to: **who owns the files, what is waiting, and what happens next**. Do not dump the inventory unless requested.

## Failure modes

- Separate worktrees are mistaken for permission to edit the same subsystem in parallel.
- A branch name is trusted instead of its actual dirty diff.
- Independent implementations are mechanically merged without choosing an architecture owner.
- A local patch is committed to the wrong feature branch merely because it compiles.
- “Wait for Cursor” is reported without naming the owner, files, requirements, and verification gate.

## Verification checklist

- [ ] Every active worktree and writer is identified.
- [ ] Ownership of overlapping files is explicit.
- [ ] No second writer edits the owned implementation surface.
- [ ] Requirements are handed to the owner concretely.
- [ ] The owner’s complete diff is reviewed after handoff.
- [ ] Focused and broader relevant tests are run.
- [ ] The final message states owner → next gate → expected integration result.

See `references/worktree-overlap-checklist.md` for a compact inspection and handoff template.
