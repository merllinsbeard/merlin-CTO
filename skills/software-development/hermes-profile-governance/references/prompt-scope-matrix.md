# Hermes prompt scope matrix

Use this reference when deciding where a rule belongs or proving which prompt a session actually received. Re-check current official docs and live source before mutation; prompt assembly changes over time.

## Two independent roots

- `HERMES_HOME` selects the profile. It owns `SOUL.md`, config, memory, skills, sessions, cron, and gateway state.
- The resolved working directory selects project context. It controls which `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, or Cursor rules load.

`terminal.cwd` changes the tool and gateway starting directory. It does not turn a file in that directory into a profile-owned prompt.

## Placement rules

| Material | Native home | Scope |
|---|---|---|
| Identity, voice, durable standing instructions | `$HERMES_HOME/SOUL.md` | Profile-wide for normal top-level runs; independent of project cwd |
| Manual session overlay | `agent.system_prompt` in profile config | Profile-scoped only when no `display.personality` is selected; verify each execution surface |
| Project architecture, commands, conventions | Project `.hermes.md` or `AGENTS.md` | Working directory / Git directory chain |
| Reusable workflows and branching procedures | Profile `skills/` | Loaded by trigger, not always injected in full |
| Durable user facts | Profile memory provider | Profile-scoped, not a workflow manual |

A file named `$HERMES_HOME/AGENTS.md` has no special profile status. It loads only when the resolved working directory or its applicable Git chain reaches that file.

## Surface matrix

| Surface | Profile identity | Project context |
|---|---|---|
| CLI / regular Desktop session | Profile `SOUL.md` | Launch or attached session cwd |
| Gateway / canonical Bot Chat | Profile `SOUL.md` | Session cwd, normally derived from `terminal.cwd` |
| Desktop project session | Profile `SOUL.md` | Project cwd |
| Kanban worker | Assignee profile `SOUL.md` | Task workspace pinned through `TERMINAL_CWD` |
| Cron | Profile `SOUL.md` | Only the job's explicit `workdir`; no-workdir jobs skip project context |
| `delegate_task` child | Dedicated child system prompt | Profile context and memory are intentionally skipped in current runtime; pass required rules in `goal` and `context` |

Do not call delegated children "profile sessions". Their isolation is intentional.

## Proof procedure

1. Read `HERMES_HOME`, `terminal.cwd`, session `cwd`, and active personality separately.
2. Enumerate other profiles or sessions that share the same cwd before treating a workspace `AGENTS.md` as profile-specific.
3. Run the live `build_context_files_prompt(cwd=..., skip_soul=True)` or equivalent prompt-builder probe against each relevant cwd.
4. Check unique markers from every candidate context file, not only file existence.
5. Test a fresh session. Existing sessions cache the system prompt and can retain an older file snapshot across gateway restarts.

## Safe migration

1. Read every duplicate prompt file completely and classify each rule by scope.
2. Keep the always-needed profile contract concise in `SOUL.md`.
3. Move detailed campaigns, routing tables, and conditional procedures into class-level skills.
4. Keep repository-specific facts in the repository's context file.
5. Treat environment values and model selections as live config or memory, not prompt prose.
6. Verify fresh regular, project, Bot Chat, Kanban, and cron sessions before removing a duplicate.

Never rename, delete, or move an ambiguous `AGENTS.md` before proving which sessions load it. A shared cwd can make one workspace file silently affect several profiles.