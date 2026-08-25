# Phase boundaries

A **phase** is a chunk of work inside a session: the grilling, the spec, one ticket, the review. A phase ends when this chunk is done.

The **phase boundary** is the only place this decision belongs. Mid-phase there is no decision: continue, or split leftover isolated work with `delegate_task`.

## The options

| Option | What it does |
| --- | --- |
| **Continue** | Stay in this session. No switch. |
| **New session** | Start clean. Use it when this window is disposable. |
| **`/handoff`** | Write a portable markdown file. The human types this. |
| **`delegate_task`** | Send isolated work to its own window and get a report back. |
| **Kanban** | Put the rest on cards when the work must survive a restart. |

Hermes has no `/clear` or `/compact` from the Cursor map. Do not invent them.

## The tree

Work top to bottom at the boundary. The first yes wins.

**1. Can you continue in this session?** Yes when the next phase needs this phase as a **primary source**, or the next phase still fits. Grill → spec → tickets is the standard yes: the tickets want the reasoning, not a summary of it. Continue costs nothing. Rule it out first.

**2. Is this context disposable?** The exploration, the dead ends, and the decisions will not be needed again. Start a **new session**. Getting this wrong is one-way: you lose the **why**, and rereading the diff does not return it.

**3. Does anything need to travel?** Tell the human to type `/handoff` only when you are swapping harness, moving to a new directory or repo, sending work to a colleague, or forking a side task mid-phase. What `/handoff` buys is a file that travels. If nothing is travelling, skip it.

**4. Can the leftover work run without steering?** Isolated research or a second review of a finished diff: `delegate_task`. Write the child order through `writing-for-agents`. One writer per worktree. Child summaries are claims. Read the diff and run the named check in the parent.

**5. Must this survive `/new` or a restart?** Kanban. This profile stays the implementer.

Otherwise continue. A flattened summary is the last resort, not the first reach.

## Primary and secondary sources

Every move except Continue turns a **primary source** into a **secondary source**. Stay when the next phase needs the session as it happened. Leave when staying costs more than it saves.

These are judgement calls. The value is asking the questions in order, at the boundary, not in the middle of the work.
