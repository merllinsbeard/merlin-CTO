---
name: cto-subagent-development
description: Use for CTO-native subagent research and implementation.
version: 1.0.1
author: Timofei, Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [delegation, subagents, implementation, research]
    related_skills: [writing-for-agents, cli-agent-first]
---

# CTO subagent development

Use native subagents for independent bounded work. CTO owns decisions, shared state, acceptance and the final claim.

## Route the work

Choose this mode for read-only research across independent areas or implementation tasks isolated by file set or worktree. A connected implementation goes to one CLI writer.

Done: every proposed child can finish without writing the same mutable workspace as another child.

## Run the batch

1. Read the request once and enumerate every task with its acceptance criterion in `todo`. Done: the list accounts for the full requested scope.
2. Resolve repository facts and design choices in the parent. Load `writing-for-agents` with `skill_view(name='writing-for-agents', file_path='SKILL.md')`, then write each child _order_ with the goal, exact context, settled decisions, boundaries, non-goals, allowed paths, proof command and output shape. Done: a child can execute from the order alone.
3. Dispatch independent tasks in parallel, up to the profile limit of six. Give each mutable workspace one writer; serialize shared files or isolate them in worktrees. Done: every running writer has a distinct write boundary.
4. Treat child summaries as claims. Read each changed file or full diff, run the named checks and inspect user-facing behavior. Done: every completed task has direct evidence from the parent.
5. Send a decision-complete follow-up order for each defect. Done: every acceptance criterion is verified or tied to one named external blocker.

## Bot mode

Children execute complete orders rather than interviewing the human. A child that lacks a fact returns the exact gap and leaves that branch unchanged. The parent retrieves repository facts, makes reversible choices and dispatches a corrected order. A Kanban block represents only an external decision that cannot be retrieved or inferred safely.

## Authority

The order grants paths and actions explicitly. By default a child edits its assigned workspace, reports changed files and exact checks, and leaves Git history and external systems unchanged. `git add`, commit, push, merge, release and deploy require that exact authority in the order and must satisfy the repository ownership gate.

## Pitfalls

- Several children editing one workspace. Serialize shared files or create isolated worktrees.
- A child order containing an unsettled product or architecture choice. Resolve it in the parent before dispatch.
- Accepting a summary as completion. Parent-owned evidence closes the task.

## Verification

Done: the combined diff is read, relevant checks pass, workspaces did not collide and every claimed result has parent-owned evidence.
