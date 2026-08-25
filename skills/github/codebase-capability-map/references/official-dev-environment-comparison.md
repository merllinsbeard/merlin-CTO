# Official developer-environment comparison: Hermes Agent ↔ OpenAI Codex

> Evidence bank from the official-source comparison performed on 2026-08-03. Revalidate pricing, model names, app/CLI versions, and feature availability before reusing it as a current report.

This is a worked reference for comparisons where the deliverable must distinguish documented behavior, implementation evidence, surfaces, scope, defaults, and limits. It is not a replacement for the linked live docs.

## 1. Evidence protocol

Use this order:

1. Canonical first-party docs (HTML URL retained in the final report).
2. Official release/changelog pages for dates and product versions.
3. Official source/tests for implementation details or when docs are ambiguous.
4. A local checkout only as a pinned snapshot: record tag, commit, commit date, and dirty/untracked state.

For each claim record:

```text
capability | surface | scope/isolation | default | limit | evidence URL/path | version/date | status
```

Use these status labels:

- `DOCUMENTED`: explicitly stated in first-party documentation.
- `IMPLEMENTED`: verified in source/tests, even if the docs are terse.
- `INFERRED`: reasoned from multiple facts; label it instead of presenting it as a product guarantee.
- `UNKNOWN`: not resolved. Never turn a failed scraper/search into a negative feature claim.

OpenAI Codex documentation is surface-conditional. Preserve separate rows for `app`, `web`, `CLI`, and `IDE`; a `<ContentModeSwitch>` page may make a feature available on one surface and explicitly unavailable on another.

## 2. Retrieval fallback that worked

When `web_extract` was rate-limited, the official developer docs exposed Markdown variants by appending `.md` to the canonical page URL. Fetch the Markdown into `/tmp`, then inspect it with `read_file`; cite the canonical HTML page in the result.

Examples:

```text
https://developers.openai.com/codex/projects
https://developers.openai.com/codex/projects.md
https://developers.openai.com/codex/environments/cloud-environment
https://developers.openai.com/codex/environments/cloud-environment.md
```

For exact GitHub release metadata, use the official repository API endpoint and print only public fields:

```text
https://api.github.com/repos/openai/codex/releases/tags/rust-v0.146.0
https://api.github.com/repos/NousResearch/hermes-agent/releases/tags/v2026.7.30
```

This avoids guessing a version from a search snippet. If a Markdown URL returns 404, keep the canonical HTML page and use `web_extract` or the local checkout; 404 is not evidence that the feature is absent.

## 3. Hermes Agent — evidence and boundaries

### Version anchor used in the comparison

- Official release: **Hermes Agent v0.19.1**, tag `v2026.7.30`, published `2026-07-30T23:45:37Z`: <https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.30>
- Local pinned checkout reported `version = "0.19.1"`; tag description was `v2026.7.30-610-gd0b87dad7`; HEAD commit `d0b87dad77944c669b453385bb797d53fa33c4f7`, dated `2026-08-02T12:35:50-07:00`.
- Treat the checkout as a snapshot, not automatically as the released tag. Record the divergence when reporting implementation facts.

### Projects / named multi-folder workspaces

- Official CLI reference: <https://hermes-agent.nousresearch.com/docs/reference/cli-commands>
- Desktop: <https://hermes-agent.nousresearch.com/docs/user-guide/desktop>
- Tools reference: <https://hermes-agent.nousresearch.com/docs/reference/tools-reference>
- Source anchors from the pinned checkout: `hermes_cli/projects_db.py`, `hermes_cli/projects_cmd.py`, `tools/project_tools.py`, `apps/desktop/src/store/projects.ts`.

Verified model:

- `hermes project` manages human-named projects that span multiple folders/repos: `create`, `list`, `show`, `add-folder`, `remove-folder`, `rename`, `set-primary`, `use`, `archive`, `restore`, `bind-board`.
- State is per profile in `$HERMES_HOME/projects.db`; the schema has `projects` and `project_folders`, with a designated primary path.
- A project groups desktop sessions by folder membership. The primary folder anchors the session workspace and the Kanban repo/branch convention when a board is bound.
- The desktop `project` toolset exposes `project_list`, `project_create`, and `project_switch`; source describes it as GUI-session-only. The CLI can still manage project records.
- Desktop repository discovery is separately configurable (`repo_scan_enabled`, roots, excludes). Do not confuse auto-discovered repo groups with explicit named Projects.

### Context files

- <https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files>

Verified behavior in the pinned docs/source:

- Project-context precedence is `.hermes.md`/`HERMES.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`; only one project context type is loaded per session (first match), while `SOUL.md` is independent identity context.
- `AGENTS.md` is loaded at startup and nested context is discovered progressively as relevant paths are touched; nested files are security-scanned.
- Prompt-injection scanning and head/tail truncation apply before injection. The cap can be explicit via `context_file_max_chars` or model-window-scaled (documented floor 20,000 and ceiling 500,000); progressive per-file hints are capped at 8,000 characters.
- A context file is not a sandbox or a permission boundary; it is prompt guidance.

### Kanban / dispatcher

- <https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban>
- CLI section: <https://hermes-agent.nousresearch.com/docs/reference/cli-commands#hermes-kanban>

Verified model:

- Durable SQLite-backed task board; multiple named boards can represent projects/repos/domains.
- Kanban is deliberately different from `delegate_task`: it is a durable queue/state machine with named profile workers, comments, dependencies, retries, human blocking/unblocking, and an audit trail.
- Worker workspaces are `scratch` (ephemeral), `dir:<absolute-path>` (trusted shared local directory), or `worktree` (preserved Git worktree). Scratch artifacts must be declared to survive cleanup; worktrees are preserved.
- Dispatcher ticks every 60 seconds by default, reclaims stale/crashed claims, promotes ready tasks, atomically claims, and spawns the assigned profile. It runs inside the gateway by default (`kanban.dispatch_in_gateway: true`).
- Boards are the hard isolation boundary; tenants are a soft namespace inside a board. The Kanban DB is root-anchored/shared across profiles, unlike Projects, which are per-profile.
- Attachment uploads are capped at 25 MB in the documented workflow.

### Profiles

- <https://hermes-agent.nousresearch.com/docs/user-guide/profiles>

A profile has its own Hermes home, config, `.env`, `SOUL.md`, memory, sessions, skills, cron jobs, state DB, aliases, and gateway process. Important boundary: a profile is **not** a filesystem sandbox. With the default local terminal backend the agent still has the host user's filesystem access; use `terminal.cwd` and/or a sandbox backend for execution isolation.

### Delegation

- <https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation>

- `delegate_task` starts a child with a fresh conversation, isolated context, inherited enabled tools, and a separate terminal session; only the child's final summary returns to the parent.
- Batch default: 3 concurrent children; configurable through `delegation.max_concurrent_children` / `DELEGATION_MAX_CONCURRENT_CHILDREN`, with no hard ceiling in the documented implementation. Oversized batches error rather than silently truncate.
- Leaf children cannot use `delegate_task`, `clarify`, `memory`, `send_message`, or `cronjob`; orchestrator children can spawn within `max_spawn_depth`.
- Delegation background completion is persisted in the active profile's state DB before delivery, but it is still an in-process/parent-owned workflow. Use Kanban or cron for durable queue/schedule semantics.

### Git worktrees

- <https://hermes-agent.nousresearch.com/docs/user-guide/git-worktrees>
- CLI reference: <https://hermes-agent.nousresearch.com/docs/reference/cli-commands>

`hermes --worktree` / `hermes chat --worktree` creates an isolated Git worktree for a run. Desktop also has a native worktree lane/new-branch flow. Keep the distinction explicit: the worktree is repository isolation, not profile isolation; local non-Git directories do not get Git worktree semantics.

### Skills

- <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills>
- <https://hermes-agent.nousresearch.com/docs/reference/skills-catalog>

Hermes skills are `SKILL.md` knowledge/procedure packages with progressive disclosure, profile-scoped installation/state, platform/tool requirements, and optional external directories. Bundled skills are seeded per profile by default; profiles may opt out. A skill being present does not mean its prerequisites or optional tools are installed.

### ACP / IDE

- <https://hermes-agent.nousresearch.com/docs/user-guide/features/acp>

`hermes acp` exposes Hermes over stdio ACP/JSON-RPC to ACP-compatible editors/hosts. The curated `hermes-acp` set includes file, terminal/process, web/browser, memory, todo, session search, skills, `execute_code`, `delegate_task`, and vision. Messaging delivery and cron management are intentionally excluded from ACP editor UX. ACP reuses Hermes identity, provider, memory, skills, and state; it is a transport/host integration, not a separate agent product.

### Cron

- <https://hermes-agent.nousresearch.com/docs/user-guide/features/cron>

- One-shot and recurring jobs, pause/resume/edit/trigger/remove, attached skills, platform/file delivery, fresh agent sessions, and no-agent script-only jobs.
- Gateway scheduler ticks every 60 seconds. Model resolution is job pin → `cron.model` → global default; the default drift guard can fail closed when a global provider/model changes.
- Jobs default detached from a repository: no `AGENTS.md`/`CLAUDE.md`/`.cursorrules` and gateway-start working directory. An absolute `workdir` opts into project context and tool cwd; `workdir` jobs serialize on a scheduler tick because cwd is process-global.
- Cron runs cannot recursively create more cron jobs.

### Sessions

- <https://hermes-agent.nousresearch.com/docs/user-guide/sessions>

Every surface stores sessions in the profile's SQLite state DB with FTS5 search, full role/tool history, titles, model/config, token counts, timestamps, and lineage metadata. CLI can resume by ID/title/most recent and restore recorded working directory (or suppress with `--no-restore-cwd`); compression reduces active context but is not a privacy delete.

### OpenAI Codex provider vs Codex skill/runtime

- Provider docs: <https://hermes-agent.nousresearch.com/docs/integrations/providers>
- Bundled skill docs: <https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex>
- Runtime docs: <https://hermes-agent.nousresearch.com/docs/user-guide/features/codex-app-server-runtime>

Keep three things separate:

1. `model.provider: openai-codex`: Hermes inference provider using device-code ChatGPT/Codex OAuth, stored in Hermes' auth store; existing Codex CLI installation is not required. Hermes can import existing CLI credentials when present.
2. Bundled `autonomous-ai-agents/codex` skill, version `1.0.1`: a procedure that invokes the standalone Codex CLI through Hermes `terminal`; requires Codex CLI, a Git repository, and a PTY. It documents `codex exec`, sandbox flags, PR review, and manual Git worktree fan-out.
3. Codex App-Server Runtime: a separate runtime path that hands turns to a local Codex app-server process; do not use its requirements to describe the ordinary `openai-codex` provider.

## 4. OpenAI Codex — evidence and boundaries

### Version/date anchors

- Stable CLI release verified through the official release API: `rust-v0.146.0`, published `2026-07-29T01:42:51Z`: <https://github.com/openai/codex/releases/tag/rust-v0.146.0>
- Release listing also showed later alpha/pre-release builds; never label those as the stable CLI without checking the release tag/channel.
- Changelog: <https://developers.openai.com/codex/changelog>. The July 23, 2026 entry documents multi-folder local projects and identifies Codex CLI 0.145.0 in the adjacent July 21 entry; use the changelog rather than inferring the app version from the CLI version.
- App announcement: <https://openai.com/index/introducing-the-codex-app>

### CLI / app / IDE

- CLI: <https://developers.openai.com/codex/cli>
- Desktop app: <https://developers.openai.com/codex/app>
- IDE: <https://developers.openai.com/codex/ide>

CLI is a local terminal agent whose project is the start directory or `--cd/-C`; it does not expose the ChatGPT Projects view. The IDE extension treats the open folder/workspace as the project; multi-root workspaces select a workspace root and do not expose the ChatGPT Projects view. The desktop app is the surface with Projects/sidebar, parallel threads, built-in Git/review, skills, worktrees, cloud/local modes, and automations.

### Projects, folders, and threads

- <https://developers.openai.com/codex/projects>

Desktop local Projects can connect one or more folders. The July 2026 documentation/changelog says the **primary folder** controls new chats, Git operations, and automatic discovery of `AGENTS.md`, skills, and `config.toml`; secondary folders remain available for search/read/edit. A ChatGPT web Project is file/source context and has no direct local-folder access. CLI and IDE use their launch/open workspace instead of the Projects view.

Do not equate a named Project, a thread, a workspace root, and a sandbox: they organize/contextualize work at different scopes.

### Cloud environment

- <https://developers.openai.com/codex/environments/cloud-environment>

Cloud chats create a container and check out the selected repository at a branch or commit SHA, run setup (and optional maintenance on cache resume), then run the agent and return a diff/answer. The universal image is the default. Setup scripts have internet; agent internet is off by default and can be enabled with limited/unrestricted settings. Environment variables last through setup and agent; secrets are decrypted only for setup and removed before the agent phase. Container state is cached for up to 12 hours. Cloud is remote and cannot directly operate on a local folder.

### Worktrees, subagents, and automations

- Worktrees: <https://developers.openai.com/codex/environments/git-worktrees>
- Modes: <https://developers.openai.com/codex/environments/modes>
- Subagents: <https://developers.openai.com/codex/agent-configuration/subagents>
- Automations: <https://developers.openai.com/codex/automations>

The native worktree/parallel-thread workflow is documented primarily for the desktop app; manual CLI parallelism can still be composed with ordinary Git worktrees. Subagents are child agent threads with explicit configuration and inherited security context; report model/concurrency defaults from the live subagents page rather than guessing a universal limit.

Automations are surface-dependent:

- Desktop local-project schedules can run in the project directory or an isolated worktree; the computer must stay on and the app running.
- Web schedules can use uploaded/connected context but cannot operate directly in a local computer folder and do not retain a local folder/worktree between runs.
- CLI and IDE do not expose the Scheduled management interface; create/manage schedules in web or desktop.
- Unattended tasks use default sandbox settings; start with the narrowest access.

### `AGENTS.md` and skills/plugins

- Instructions: <https://developers.openai.com/codex/agent-configuration/agents-md>
- Skills/plugins: <https://developers.openai.com/codex/skills-and-plugins>

Codex discovers at most one instruction file per directory: global `AGENTS.override.md` or `AGENTS.md`, then project-root-to-cwd files, merged root-down so closer files appear later. The combined default cap is `project_doc_max_bytes = 32 KiB`; fallback filenames are configured explicitly, and `CODEX_HOME` changes the Codex home/profile. Skills are reusable packages (explicitly invoked or available to the agent); plugins bundle skills/connectors. Keep this separate from Hermes' profile-scoped skills and context-file precedence.

### Review and sandbox

- Review: <https://developers.openai.com/codex/code-review>
- Approvals/security: <https://developers.openai.com/codex/agent-approvals-security>
- Modes: <https://developers.openai.com/codex/environments/modes>

`/review` is available in app/CLI/IDE variants with surface-specific scopes. Local app/IDE/CLI reviews report prioritized findings without changing the working tree; the app review pane requires a Git repository and can select among multiple attached repositories. Sandbox/approval behavior is mode/surface-specific; never summarize “Codex sandbox” without naming local vs cloud and the selected approval/network mode.

### ChatGPT Pro included usage and the 20× table

- Pricing: <https://developers.openai.com/codex/pricing>
- Pro plans: <https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers>
- Codex usage with a ChatGPT plan: <https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan>

The pricing page snapshot used for this comparison labelled a **Pro 20x** table as local messages per five-hour window:

| Model | Range shown |
|---|---:|
| GPT-5.6 Sol | 200–2,000 |
| GPT-5.6 Terra | 500–4,000 |
| GPT-5.6 Luna | 5,000–40,000 |
| GPT-5.5 | 300–1,600 |
| GPT-5.4 | 400–2,000 |
| GPT-5.4 mini | 1,200–7,000 |

The same page footnote says local messages and cloud chats share a **five-hour window** and that additional weekly limits may apply. Treat ranges as average/variable usage guidance, not a guaranteed message quota; model, context, tools, and task complexity affect consumption. Re-fetch this table before quoting it because plan names, model names, surfaces, and limits change.

## 5. Final-report checklist

Before publishing a comparison:

- State the observation date and pin both product versions where possible.
- Put an official URL beside every non-trivial row; link the exact release tag for version/date claims.
- Give each feature a surface label (`Hermes desktop`, `Hermes CLI`, `Hermes ACP`, `Hermes gateway`, `Codex app`, `Codex CLI`, `Codex IDE`, `Codex web/cloud`).
- State the isolation boundary: project, profile, session/thread, Git worktree, sandbox/container, or none.
- Distinguish native capability from a documented composition recipe.
- Include limits and negative scope explicitly (for example, “CLI/IDE have no Scheduled management UI”), but only when a first-party source states it.
- Add an `Unknowns / revalidate` section for dynamic billing, model retirement, regional rollouts, release channels, and any page that could not be fetched.
- Redact credentials and tokens; record only that an auth file/provider exists.
