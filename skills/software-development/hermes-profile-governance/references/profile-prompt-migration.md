# Profile prompt migration

Use this when profile behavior was stored in `AGENTS.md` or a shared workspace file and must follow the profile across ordinary, project, Bot Chat, Kanban, and cron sessions.

## Scope model

- `HERMES_HOME` selects the profile. `$HERMES_HOME/SOUL.md`, memory, skills, config, sessions, cron, and gateway state are profile-owned.
- The resolved session cwd selects project context. `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, and Cursor rules are workspace- or repository-owned.
- `$HERMES_HOME/AGENTS.md` has no special profile scope. It loads only when cwd discovery reaches it.
- `agent.system_prompt` is a profile overlay, but a selected `display.personality` replaces it. Verify each execution surface before using it as an invariant.
- A `delegate_task` child is intentionally isolated and receives its own `goal` and `context`; it is not a normal profile session.

## Migration procedure

1. Enumerate every affected profile. Read `SOUL.md`, `AGENTS.md`, `terminal.cwd`, `display.personality`, `agent.system_prompt`, and recent session cwd values.
2. Enumerate all profiles and sessions sharing each cwd. Never call a workspace `AGENTS.md` profile-specific merely because one profile usually starts there.
3. Back up `SOUL.md`, `AGENTS.md`, and `config.yaml` for every profile in one timestamped manifest with hashes.
4. Classify rules before moving them:
   - profile-wide identity and standing instructions → `SOUL.md`;
   - conditional procedures → class-level skills;
   - repository commands and conventions → repository context files;
   - model, provider, paths, quotas, and tool availability → live config or memory.
5. If the user explicitly requests a verbatim merge, stage `SOUL.md + AGENTS.md`, prove the full old text is present, atomically replace `SOUL.md`, then remove the active profile `AGENTS.md`.
6. Change config through `hermes --profile <name> config set`, not hand-edited YAML. Read every key back exactly.
7. Verify each profile independently before advancing:
   - old instructions preserved in the new source;
   - profile `AGENTS.md` absent when removal was requested;
   - `load_soul_md(home_override=<profile-home>)` returns the new file exactly;
   - `build_context_files_prompt(cwd=..., skip_soul=True)` does not reintroduce the old profile rules;
   - `hermes --profile <name> config check` passes;
   - prompt files stay below current truncation limits.
8. Test fresh regular, project, Bot Chat, Kanban, and cron sessions. Existing sessions cache prompt snapshots and are not proof of the new layout.

## Rollback

Restore the exact preimages and config from the manifest. Do not reconstruct prompt text from summaries. Restart or rebuild only the surfaces that already loaded the rejected configuration.
