---
name: cli-agent-first
description: Use when choosing direct, subagent, or coding CLI execution.
version: 1.0.0
author: Merlin
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [orchestration, delegation, cli-agents]
    related_skills: [codex, claude-code, opencode, cto-subagent-development, writing-for-agents]
---

# CLI agent first

Choose one owner for the next change. Hermes CTO keeps the outcome, architecture, boundaries, and acceptance.

## Choose the owner

1. Continue in the current session when it already owns the task and workspace.
2. Use direct execution for a small bounded change.
3. Use `cto-subagent-development` for independent read-only research or isolated work.
4. Use `codex` for connected implementation, security-sensitive work, or expensive failures.
5. Use `claude-code` or `opencode` when the user names that writer or its runtime is already configured.
6. Give each mutable worktree exactly one writer.

Done when one owner and one write boundary are explicit.

## Write the order

Load `writing-for-agents`. Give the writer the outcome, repository, settled decisions, constraints, non-goals, allowed mutations, proof command, and required report. Do not delegate product or architecture choices that the CTO can settle first.

Done when a fresh writer can execute without conversation history.

## Review and accept

Treat writer summaries as claims. Read the complete diff, run the named checks, inspect user-facing behavior, and repair every finding before acceptance. Use an independent reviewer for security, money, irreversible work, failed attempts, large diffs, or release paths.

Done when every acceptance criterion has direct evidence and no unresolved defect remains.

## Pitfalls

- Two writers in one worktree.
- A prompt that omits repository ownership or external-action boundaries.
- Accepting a summary instead of the artifact.
- Naming a CLI or skill that is not installed.
