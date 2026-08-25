# Read-only cross-source reconciliation

Use when someone asks to regain orientation across several days of work without making changes.

## Source precedence

1. Current canonical task register / project source of truth.
2. Live repository state and current Kanban cards.
3. Recent meeting transcripts and agent sessions.
4. Older hubs, contours, and planning documents — treat as historical until reconciled.

## Method

- Start explicitly in read-only mode: do not switch boards, change cards, archive items, commit, push, or deploy.
- Parallelize independent reconnaissance by source: Kanban graph, message/voice archive, sessions/knowledge base, and repository state.
- For Kanban, distinguish **active execution lanes**, **intentional owner gates**, **external blockers**, **superseded audit trails**, and **structurally invalid DAGs**. A `done` status is insufficient: inspect review verdicts and missing remediation children.
- For voice notes, check the actual delivery surface before declaring absence. A voice message sent to an agent bot may be present as an agent-session transcript or audio cache rather than in a general Telegram collector.
- Validate substantial claims against current Git status, branch/upstream relationship, and test evidence. Report uncommitted or local-only work as a preservation risk, not as a confirmed loss.
- End with a compact map: current source of truth, live next gate per project, blockers that require an owner/external party, and stale duplicates that should not be resumed.

## Pitfalls

- Do not conflate `blocked` with unfinished engineering: some blocks intentionally preserve an owner decision before external side effects.
- Do not resume old cards merely because they are `todo`; migrations between boards commonly leave historical chains behind.
- Do not treat an old project hub as authoritative when a newer task register or acceptance run conflicts with it.
- Do not mutate the board during an orientation pass. Propose cleanup only after the map is accepted.
