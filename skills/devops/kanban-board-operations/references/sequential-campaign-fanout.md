# Sequential campaign fan-out

Use when the user wants a multi-card campaign on Kanban (rewrite fleet, sequential delivery, one specialist profile) and the current board is a different product stream.

## Decisions before the first card

- Assignee must exist (`hermes profile list`). Unknown assignees sit in `ready` forever.
- Every child body carries the decisions it depends on. Workers cannot see siblings. A shared canon file is extra, not a substitute.
- Sequential means at most one `ready`/`running` card. `max_in_progress` will otherwise spawn up to the clamp (here: 8).
- Process lives in the skill; a cron prompt that duplicates it becomes a pointer after the skill rewrite. Do not fire live Telegram-delivering crons as proof.

## Board

Create a dedicated board. Do not dump the campaign onto the current product board.

```bash
hermes kanban boards create <slug> --name "..." --description "..."
```

Omit `--switch` unless the user asked to leave the current board. Pass `board=<slug>` on every `kanban_*` call.

## Create order — seal the graph before the dispatcher can claim

Do **not** create a batch of unparented cards (even `initial_status=blocked`) and link them afterwards. `blocked` at create is not a hold: the dispatcher can promote and claim them before `kanban_link` runs.

Working sequence:

1. Write the canon file.
2. Create card 1 with no parent. It may go `ready`/`running` immediately — that is intended.
3. Create each later card with `parents=[previous-id]` already set so it stays `todo` until the parent is `done`.
4. After the last create, prove `running=1` (or `ready=1` if card 1 has not been claimed yet) and `ready=0` for everyone else.

If you must batch-create, every card in the batch except the seed must include its parent id in the same `kanban_create` call. Never leave a window of unparented ready work.

## If the race already happened

`kanban_*` has no reclaim. Use the CLI:

```bash
hermes kanban --board <slug> reclaim <task_id> --reason "..."
hermes kanban --board <slug> list
```

Reclaim releases the claim. Confirm the intended seed is the only `running` card and that children with unfinished parents are `todo`, not `ready`. `kanban_block` only accepts `running`/`ready`; if reclaim already moved a card to `todo`, do not loop on block.

Cards created later as `blocked` with parents already set: `kanban_unblock` correctly returns them to `todo` while any parent is open.

Leave a comment on each reclaimed card: ignore partial writes from the aborted run; re-read the live artifact.

## Verify before walking away

- `hermes kanban --board <slug> stats` shows one active card and the rest `todo`.
- Current product board is unchanged.
- Seed worker has loaded the campaign skills named on the card.
