# Profile behavior repairs and exact rollbacks

Use this checklist when a user rejects a profile change, especially when the repair touched prompts, skills, memory, plugins, config, or a live gateway.

## Locate the real owner before editing

Classify the unwanted behavior first:

- **Model-authored prose**: inspect the governing skill and prove its invocation path before adding prompt text.
- **Tool- or adapter-authored UI**: inspect the tool surface. A prompt or writing skill cannot rewrite labels added after generation.
- **Role identity or authority**: `SOUL.md` may own it.
- **Operating sequence or routing**: `AGENTS.md` may own it.
- **Reusable writing or task procedure**: the class-level skill owns it.
- **Runtime enforcement**: a plugin owns it only when enforcement is explicitly required and proportionate.

`SOUL.md` is not a generic high-precedence bucket. Do not move style rules, tool behavior, or troubleshooting policy there merely because it is always loaded.

Prefer one canonical repair. Duplicating the same rule across SOUL, AGENTS, memory, a skill, and a plugin creates conflicts and makes rollback unreliable.

## Before a multi-layer repair

Record a change manifest with:

- every file and its pre-change content or hash;
- every skill and support file to be changed;
- exact memory operations and original entry order;
- plugin directories and config keys;
- any service reload or restart required for activation.

If another session changes a target after the last read, stop and re-read. Decide whether that concurrent change belongs to the rejected campaign before reverting it. Never reconstruct a shared file from memory while another writer is active.

## Exact rollback

1. Stop further activation. Disable a newly enabled plugin before removing it.
2. Reverse the original patch or restore the captured preimage. Do not create a new "cleaned up" version during rollback.
3. Restore memory values and ordering. A remove-then-add operation appends an entry, so restoring text alone may not restore prompt precedence.
4. Remove plugin files through the plugin manager.
5. Read config back. Plugin removal can leave `plugins.disabled` or `plugins.entries.<name>` behind; remove only the keys introduced by the rejected change.
6. Reload the runtime only if the rejected plugin or config was already loaded. Use the native graceful path and verify the new process is healthy.
7. Verify every layer against the manifest: full content or hash, memory order, skill body, plugin inventory, config keys, and live runtime.

## Failure pattern to avoid

Do not react to a writing-style complaint by rewriting SOUL, AGENTS, profile metadata, memory, and a skill while also adding a blocking plugin. First prove why the existing writing skill or its invocation failed. A broad repair before diagnosis is profile-wide scope expansion, not a root-cause fix.
