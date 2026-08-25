---
name: kanban-board-operations
description: Use when cleaning or reconciling a crowded Kanban board.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kanban, maintenance, reconciliation, integrity]
    category: devops
    requires_toolsets: [kanban]
---

# Kanban Board Operations

Reconcile a crowded or contradictory Kanban board into one truthful delivery path without losing active work or corrupting its task graph. Treat board mutation like a small data migration: **scope first, backup second, mutate third, prove fourth**.

## When to Use

Use when the user asks to clean up, delete, archive, reconcile, deduplicate, or explain a Kanban board; or when multiple task chains describe competing candidates for the same outcome.

This skill is for board state. It does not replace code review, deployment approval, or ordinary task execution.

For a strictly read-only, cross-source orientation pass before any cleanup, read [references/read-only-cross-source-reconciliation.md](references/read-only-cross-source-reconciliation.md).

## Principles

- The live board is evidence, not narrative. Establish task IDs, status, dependencies, runs, and timestamps before calling anything redundant.
- Preserve the smallest chain that can still deliver the current outcome: active implementation, its explicitly planned review/release children, and completed provenance worth retaining.
- Do not infer that an old chain is disposable merely because it is blocked. Confirm it is superseded by a named replacement and has no active worker.
- Prefer native `kanban_*` transitions. If the platform has no bulk-delete endpoint and hard deletion is explicitly requested, use the installed Kanban database kernel's task-deletion helper rather than ad-hoc SQL; take a consistent SQLite backup first.
- Delete leaves before parents. This avoids temporary promotion of descendants and preserves a clean audit of the operation.

## Procedure

### 1. Orient and model the graph

1. Read the current task with `kanban_show()` if dispatched from a board task.
2. List the board with `kanban_list(include_archived=true, limit=200)`.
3. Inspect the candidate live chain and each proposed deletion root with `kanban_show(task_id=...)`.
4. Record a fixed deletion manifest: task IDs, title, current status, why superseded, and the replacement chain that remains.
5. Separate the manifest into:
   - **keep**: current `running` work, its planned child review/release cards, and durable `done` provenance;
   - **remove**: explicitly superseded `todo`/`blocked` cards only;
   - **escalate**: anything `running`, ambiguous, or lacking a replacement authority.

Completion criterion: every removal ID is fixed before mutation; no dynamic query may scoop up newly created work.

### 2. Choose the terminal operation

- **Archive** when the user wants history hidden but recoverable.
- **Hard delete** only when the user explicitly asks to remove clutter or declares the cards disposable.
- Do not use archive as a substitute for delete, or vice versa.
- Do not delete a task with an active run. Stop and surface that it must finish, be cancelled through the supported lifecycle, or be explicitly approved for removal.

### 3. Backup and execute safely

For a hard delete:

1. Re-read every deletion target immediately before mutation. Assert all still exist and are only in approved removable states, normally `todo` or `blocked`.
2. Re-read each keep ID and assert its expected status. This is the guard against deletion-manifest drift.
3. Make a consistent online SQLite backup in the board's `backups/` directory and calculate its SHA-256.
4. Delete only the fixed manifest, leaf-first. Use the Kanban DB kernel's supported `delete_task` helper if native tools lack bulk deletion; do not hand-write table deletes.
5. On an unexpected failure, stop. Do not restore automatically: a restore can overwrite legitimate concurrent updates. Report the backup path and the exact partial state instead.

Read [references/safe-task-deletion.md](references/safe-task-deletion.md) before using the kernel fallback.

### 4. Verify from independent views

After mutation, verify all of the following:

- `kanban_list` count and status distribution match the intended keep set;
- every target ID is absent;
- current active task and planned review/release child remain with the expected links;
- SQLite `integrity_check` returns `ok`;
- `foreign_key_check` is empty;
- no dangling `task_links` and no dependency cycles remain.

Report the number of cards removed, the remaining status counts, the active chain retained, and backup path plus hash. State explicitly that code, production, and worktrees were not changed unless they actually were.

## Pitfalls

- **Deleting by status alone:** a broad `todo`/`blocked` query can erase a card created during cleanup. Use a sealed ID manifest.
- **Breaking a child-first graph:** deleting parents first can transiently unblock descendants or complicate evidence. Work leaves to roots.
- **Calling a raw SQLite mutation a cleanup:** task records have comments, runs, events, notification subscriptions, links, and lifecycle invariants. Use the installed kernel helper, not custom delete SQL.
- **Automatic rollback after a partial deletion:** concurrent board activity makes this destructive. Preserve the backup and stop for a deliberate recovery decision.
- **Deleting completed history reflexively:** old `done` cards may be the only provenance for a release, incident, or decision. Keep bounded completed evidence unless the user explicitly asks to purge it.
- **Confusing board cleanup with cancelling work:** a running worker needs its own lifecycle decision; a database delete is not a safe cancellation mechanism.

## Completion Checklist

- [ ] The deletion or archive scope was explicitly authorized.
- [ ] Every removal ID was inspected and fixed before mutation.
- [ ] No active run was in the removal set.
- [ ] A consistent backup and SHA-256 were recorded before hard deletion.
- [ ] The intended remaining live chain was re-read after mutation.
- [ ] Integrity, foreign-key, dangling-link, and cycle checks passed.
- [ ] The final report distinguishes board mutation from code/deploy/production changes.
