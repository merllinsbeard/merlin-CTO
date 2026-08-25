# Installed extras

Apply a row only when `skill_view` or `hermes skills list` shows that name as installed. If it is missing, ignore the row. Do not treat a name here as part of the portable distribution.

These extras never override the four-field contract, the default architecture path, or one writer per worktree.

## Writers and launchers

| If installed | Use when | Instead of |
| --- | --- | --- |
| `cursor-agent` | Linear implementation, UI, browser proof, editor context | `claude-code` or `opencode` for that class of work |
| `grok` | `cli-agent-first` named Grok Build, after a live quota check | Cursor on quota exhaustion for linear work, Codex for high-cost work |
| `blackbox` | The human named Blackbox | any other writer |
| `openhands` | The human named OpenHands | any other writer |
| `antigravity-cli` | The human named Antigravity | any other writer |

`cli-agent-first` still chooses the sibling. These skills are how to launch it. A missing binary or a failed auth check is a named gap.

## Memory and orientation

| If installed | Use when | Do not use it for |
| --- | --- | --- |
| `openviking` | Durable people, projects, facts, indexed docs. Search before asking the human to repeat | Live Git, files, CI, or running services. Those win |
| `dev-project-brief` | A live git brief across machines before a campaign | A substitute for `git status` in the worktree you will edit |
| `claw-collectors` | Telegram, voice memos, or meeting transcripts as source material | Engineering routing |

One fact lives in one layer. If OpenViking stores it, do not also write it to local `MEMORY`.

## Hermes profile and Desktop

| If installed | Use when |
| --- | --- |
| `hermes-desktop-debugging` | Desktop routed the wrong chat, tab, tile, or session |
| `inspecting-hermes-desktop-dom` | You need the live Desktop DOM or CSS over CDP |
| `hermes-profile-skills` | Attach or enable skills on an isolated profile |
| `hermes-profile-governance` | Audit a profile end to end |
| `public-hermes-profile-distribution` | Publish a portable profile with proof |
| `hermes-agent-skill-authoring` | Author an in-repo `SKILL.md` |
| `hermes-bot-profile-design` | Style a Desktop Bot profile or avatar |
| `provider-reasoning-verification` | Check provider reasoning levels and mappings |
| `llm-provider-quota-check` | Probe live key or pool quota before a campaign |

Hermes configuration still starts at `hermes-agent` and official docs.

## Infra, auth, and acceptance

| If installed | Use when | Do not mix with |
| --- | --- | --- |
| `environment-contract-migrations` | Deployed URL, host, port, callback, or env meaning changes | A one-line default edit while old values still live in state |
| `oauth-login-debug` | Live OAuth or OIDC login fails | Guessing from provider docs |
| `private-network-acceptance` | A human must test through an existing VPN | `isolated-web-preview` |
| `isolated-web-preview` | A short public preview of a local web app | VPN-only acceptance |
| `deployment-capacity-audit` | Honest server sizing from repo plus live deploy | A production release claim |
| `repo-sync-mac-server` | Sync a repo between a Mac and a server, then set up the Hermes project | A substitute for `github-pr-workflow` |

## Campaigns and boards

| If installed | Use when | Instead of |
| --- | --- | --- |
| `github-ticket-campaign` | Closing a GitHub issue graph through CLI writers | Generic `ticket-campaign-execution` for that GitHub graph |
| `cli-writer-campaign` | Closing a ticket graph through CLI writer lanes | Ad-hoc writer launches |
| `coding-cli-goal-campaign` | A full issue campaign owned by a coding CLI | A loose pile of `cli-agent-first` launches |
| `frontend-polish-campaign` | Several premium UI tickets in one campaign | One-off `frontend-premium-audit` plus hope |
| `kanban-sequential-campaign` | A sequential Kanban campaign with explicit dependencies | Parallel cards that share a worktree |
| `kanban-board-operations` | Clean, dedupe, or reconcile a crowded board | Ordinary ticket execution |
| `to-goal` | Design is agreed and the human wants one paste-ready Goal prompt | A second spec |
| `repository-hygiene-campaign` | Remove docs, tracker, CI, or git sediment on purpose | A drive-by cleanup inside a feature ticket |

## Git and review extras

| If installed | Use when |
| --- | --- |
| `branch-review-before-push` | Review an unpushed local branch, or triage many local branches, without pushing |
| `repository-integration-triage` | Several worktrees or PRs must land without mixing checkouts |
| `clean-repo-publication` | First public push: sanitize tree and history, then prove it |
| `github-profile-surfaces` | GitHub profile or social surfaces, not product code |
| `codebase-capability-map` | Map platform capabilities from source plus docs |

## Product and spec extras

| If installed | Use when |
| --- | --- |
| `source-backed-product-revision` | Revise product copy or UI from calls or feedback |
| `spec-checklist-audit` | Audit spec or checklist tickets against the live codebase |
| `qualification-specification` | Capacity and reliability qualification specs |
| `graphify` | A question about a codebase that should become a structured graph |
| `delegate-research-fanout` | Several independent read-only research children |

## Visualization extras

The portable set already has `baoyu-infographic`, `excalidraw`, `image`, `visualize`, and `software-architecture-visualization`.

If the request is visual and one of these is installed, prefer the specific extra over a generic `image` call: `ascii-art`, `ascii-video`, `baoyu-comic`, `eli5`, `graphify`, `manim-video`, `p5js`, `pretext`, `text-heavy-infographic-series`, `comfyui`, `brandkit`, `gpt-taste`, `high-end-visual-design`, `imagegen-frontend-web`, `imagegen-frontend-mobile`, `industrial-brutalist-ui`, `minimalist-ui`, `stitch-design-taste`.

Do not open a visualization extra to decorate an engineering answer.

## Do not route unless the human named them

These exist in some profiles and are easy to misfire:

- `grilling`, `loop-me`, `wait-what`, `teach`, `claude-handoff`
- `setup-matt-pocock-skills`, `setup-pre-commit`, `setup-ts-deep-modules`, `git-guardrails-claude-code`
- `writing-beats`, `writing-fragments`, `writing-shape`
- `design-taste-frontend-v1` when `design-taste-frontend` is present
- `full-output-enforcement`, `scaffold-exercises`, `migrate-to-shoehorn`

If the human named one, load it. Do not offer it as the default.
