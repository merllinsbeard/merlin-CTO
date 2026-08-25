# Profile compliance audit probes

This reference captures a validated way to compare a spoken or written profile specification with the live Hermes profile. Keep session-specific names out of the main skill; use these patterns as probes.

## Requirement matrix

Build one row per criterion with these columns:

| Criterion | Prompt evidence | Runtime evidence | Skill evidence | Verdict | Repair |
|---|---|---|---|---|---|

Do not calculate a coverage percentage. A single conflict in assignment, repository authority, or review policy can dominate many implemented wording checks.

## Prompt file inventory

Check the live profile root and its memory directory:

- `<profile>/SOUL.md`
- `<profile>/AGENTS.md`
- `<profile>/profile.yaml`
- `<profile>/USER.md` when present
- `<profile>/memories/USER.md`
- `<profile>/memories/MEMORY.md`

The root `USER.md` may contain only routing metadata while the real durable user profile lives under `memories/`. Missing a root `MEMORY.md` is not evidence that memory is absent.

## Safe runtime probes

Use selected config reads rather than printing the whole configuration:

```bash
hermes --profile <name> config get model --json
hermes --profile <name> config get fallback_providers --json
hermes --profile <name> config get agent --json
hermes --profile <name> config get delegation --json
hermes --profile <name> config get kanban --json
hermes --profile <name> config get skills --json
hermes --profile <name> config get toolsets --json
hermes --profile <name> config get moa --json
```

Useful native readbacks:

```bash
hermes profile list
hermes --profile <name> status
hermes --profile <name> gateway status
```

Use native Project and Kanban tools for their live state. For a claimed remote-machine route, use the existing SSH alias with `BatchMode=yes` and a bounded timeout, then verify the target's native interface.

## Skill resolution probe

Extract every backticked or explicitly named skill from AGENTS, USER, MEMORY, and SOUL. For each name:

1. Find the exact name in `skills_list`.
2. Run `skill_view(name)`.
3. Read the behavior-bearing section.
4. Follow any linked reference that controls the disputed path.

Report exact-name failures. Example: a collection of frontend design skills does not satisfy an AGENTS rule that invokes a missing `taste` router.

## Conflict patterns

### Assignment conflict

Prompt says the profile handles autonomous Kanban tasks, while `profile.yaml` describes it as manual-only or tells the dispatcher to assign another profile. The tools may work when called manually, but automatic routing is still CONFLICT.

### Model-routing conflict

AGENTS maps simple and complex work to one set of models, while the loaded writer-routing skill maps the same classes to different CLI harnesses. Inspect the actual delegation config too. A delegation model is not automatically a CLI writer.

### Review-policy conflict

AGENTS requires one formal review, while an execution skill mandates per-task spec review, quality review, and a final integration review. Prompt precedence does not make the skill healthy. Mark CONFLICT and repair the skill or stop invoking it.

### Bot-mode interaction conflict

AGENTS forbids questions in Bot mode, while spec or ticket skills require user approval. The autonomous path needs an explicit non-interactive branch. Do not assume the higher-level rule will reliably erase every lower-level prompt.

### Authority conflict

SOUL says the profile owns all technical work, while the repository registry names only a subset. Unlisted repositories remain restricted. Mark PARTIAL unless a later ownership rule intentionally chose that behavior.

### Capability versus proof

Installed skills, configured messaging, and an available Kanban tool prove components. They do not prove a full voice-to-spec-to-tickets-to-delivery cycle. If the pilot was deferred or no exact user-flow evidence exists, mark the full path UNVERIFIED.

## Repair order

1. Resolve profile assignment and repository authority.
2. Define the mode selector: direct execution, CLI writer, native subagents, or Kanban campaign.
3. Align model routing between AGENTS, delegation config, and writer skills.
4. Remove review-policy and Bot-mode conflicts from invoked skills.
5. Add missing exact-name routers.
6. Verify the full workflow once, then record only stable routing and ownership facts.
