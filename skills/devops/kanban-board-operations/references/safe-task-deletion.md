# Safe Kanban Task Deletion

Use this fallback only after the user has explicitly requested hard deletion and the native Kanban tool surface has no bulk-delete operation.

## Preconditions

1. Resolve the exact board database path; do not touch a default/current board by accident.
2. Build a sealed ID list from the already inspected task graph. Never derive targets at delete time with `WHERE status IN (...)`.
3. Assert every target is still present and is in an approved removable state. Reject `running` tasks and inspect their `current_run_id`.
4. Assert named keep IDs still have their expected statuses.
5. Create an online SQLite backup with `Connection.backup()` under `<board>/backups/`, then calculate SHA-256.

## Kernel fallback

Import the installed `hermes_cli.kanban_db` module and open the explicit database with `kanban_db.connect(db_path)`. Delete the sealed IDs in leaf-first order with `kanban_db.delete_task(conn, task_id)`.

Why this helper: it removes task-scoped comments, events, runs, notification subscriptions and graph links, then recalculates readiness. Handwritten multi-table SQL is brittle against schema changes and can leave a board that looks plausible but is semantically damaged.

Do not bundle the deletes in a home-grown transaction that bypasses the helper. If a helper call fails, stop and report the exact ID plus backup location. Do not automatically restore: another worker may have updated the board after the backup.

## Required proof after deletion

Run both the native board view and independent SQLite checks:

- task count/status distribution;
- zero surviving removal IDs;
- retained active/review tasks and expected parent-child chain;
- `PRAGMA integrity_check` equals `ok`;
- `PRAGMA foreign_key_check` has no rows;
- no `task_links` whose parent or child no longer exists;
- no directed cycles in the remaining dependency graph.

Record the backup path and SHA-256 in the completion report. The operation changes board metadata only; call out separately whether code, worktrees, or production were untouched.
