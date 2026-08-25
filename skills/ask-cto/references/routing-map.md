# Routing map

Map a request to installed frontmatter names. If two skills appear in one row, the first column decides. Do not load the whole row.

## Understand

| Signal | Load | Do not load for this signal |
| --- | --- | --- |
| How does this run, where does it live, which layer owns it | `how` | `why`, `code-wiki` |
| Why was this chosen, what was rejected, what does history say | `why` | `how` |
| Generate a wiki, module docs, Mermaid overview | `code-wiki` | `why` |
| Investigate primary sources and leave a cited file | `research` | `how` as a substitute |
| LOC, languages, inventory | `codebase-inspection` | `code-wiki` |
| Fact-grounded architecture picture | `software-architecture-visualization` | `visualize` unless the human asked for a generic chart |
| Human did not understand the last answer | `wait-what-bro` | a new investigation |

## Orchestration

| Signal | Lane | Owner skill |
| --- | --- | --- |
| Small reversible edit, files in reach | Direct | this session |
| Parallel read-only research or isolated file sets | Subagents | `cto-subagent-development` |
| Must survive restart, cross profiles, blockers, ticket graph | Kanban | `ticket-campaign-execution` |
| Linear implementation, UI, browser proof, costly failure | Coding CLI | `cli-agent-first` |
| Several coding agents already overlap | Coding CLI | `concurrent-coding-agent-coordination` plus `cli-agent-first` |
| Native subagent implementation loop | Subagents | `subagent-driven-development` only when that loop is already the project convention |

`delegate_task` is a tool, not a lane. It belongs to the Subagents lane and to short reasoning inside an already chosen lane. It is not a substitute for Kanban or Coding CLI.

## Plan and architecture

| Signal | Load or tell the human |
| --- | --- |
| Sharpen a plan inside a repo | Human types `/grill-with-docs` |
| Sharpen a plan with no repo | `grill-me` |
| Interview primitive with no wrapper | `grill-me` already covers this. Do not invent `/grilling` unless that skill is installed |
| Huge foggy effort, decisions not deliverables | Human types `/wayfinder`, then `to-spec` |
| Agreed design needs a spec | `to-spec` |
| Spec needs vertical tickets | `to-tickets` |
| Markdown plan, no execution | `plan` |
| Missing facts live in someone else's head | Human types `/to-questionnaire` |
| Stateful language, overloaded terms, ADRs | `principle-model-the-domain`, `domain-modeling` |
| Design a deep module | `codebase-design` |
| Scan live code for deepening | Human types `/improve-codebase-architecture` |
| TypeScript package boundaries | `typescript-best-practices` |
| Throwaway design question | `prototype` |
| Throwaway technical experiment | `spike` |

## Build

| Signal | Load |
| --- | --- |
| One-session feature from a ticket | `implement` |
| Build from a spec without a ticket graph | `implement-spec` |
| Multi-ticket campaign | `ticket-campaign-execution` |
| Red-green for a concrete behaviour | `tdd` |
| Human explicitly asked for TDD on a bug | Human types `/tdd-bug-fix` |
| Official bundled TDD name already in use | prefer `tdd`; do not load `test-driven-development` beside it |
| Smallest change that closes the root | `ponytail`, `principle-laziness-protocol` |
| Long run that stops at 80 percent | `unlazy` |
| Independent verifiable slices | `principle-sequence-verifiable-units` |
| Structural search or rewrite | `ast-grep` |
| Recent diff cleanup | `simplify-code` |

## Defects

| Signal | Load |
| --- | --- |
| Hard bug, flake, regression | `diagnosing-bugs` or `systematic-debugging` |
| Need a tight red loop first | `diagnosing-bugs` |
| Four-phase root-cause pass | `systematic-debugging` |
| Symptom-only patch is tempting | `principle-fix-root-causes` |
| REST or GraphQL failure | `rest-graphql-debug` |
| Node inspector | `node-inspect-debugger` |
| Python debugger | `python-debugpy` |

If both `diagnosing-bugs` and `systematic-debugging` fit, pick `diagnosing-bugs` when the feedback loop is missing, and `systematic-debugging` when the loop already exists.

## Review

| Signal | Load |
| --- | --- |
| What else could this break | `blast-radius` |
| Review a diff against spec and standards | `code-review` |
| Pre-commit local review | `requesting-code-review` |
| Review a GitHub pull request | `github-code-review` |
| Kanban review lane | `sdlc-review` |
| Second-model review | `oracle` |
| In-progress merge or rebase conflict | `resolving-merge-conflicts` |

Do not run `code-review` and `github-code-review` on the same artifact unless one is local and the other is the published PR, and then only once each.

## GitHub and release

| Signal | Load |
| --- | --- |
| Auth, tokens, SSH, `gh` login | `github-auth` |
| Create or triage issues | `github-issues` |
| Issue to a verified PR | `github-issue-to-pr` |
| Branch, commit, open, CI, merge | `github-pr-workflow` |
| Clone, fork, remotes, releases | `github-repo-management` |
| Incoming raw issues | `triage` |
| Merged vs released vs deployed vs live-accepted | `production-release-verification` |

## Frontend and product

| Signal | Load |
| --- | --- |
| New interface that must not look templated | `design-taste-frontend` |
| Upgrade an existing site or app | `redesign-existing-projects` |
| Premium UI gaps | `frontend-premium-audit` |
| Live exploratory QA | `dogfood` |
| Promise versus live copy | `product-surface-review` |
| Image to implementation | `image-to-code` |
| DESIGN.md tokens | `design-md` |
| One-off HTML artifact | `claude-design` |
| Known public design system as HTML | `popular-web-designs` |

## Infrastructure and Hermes

| Signal | Load |
| --- | --- |
| Docker, images, Compose | `docker-management` |
| Mac or remote host over SSH | `remote-machine-access` |
| Hermes setup, config, Desktop | `hermes-agent` |
| Desktop in the background | `computer-use` |
| Temporary public Worker | `cloudflare-temporary-deploy` |
| Static site that must store form posts | `durable-static-site-forms` |
| HAR to HTTP client | `har-derived-api-client` |
| In-page natural-language GUI | `page-agent` |
| Steps only a human can click | `wizard` |

## Communication and knowledge

| Signal | Load |
| --- | --- |
| Any human-facing answer | `how-to-talk`, then `unslop` |
| Human asked for a shorter answer | also `concise` |
| Any agent-facing text | `writing-for-agents` |
| Recurring lesson | `principle-encode-lessons-in-structure` |
| Portable session transfer | Human types `/handoff` |
| Matt Pocock family only, after this router already chose that family | Human types `/ask-matt` |

## Installed writers

This distribution materializes `codex`, `claude-code`, and `opencode`. `cli-agent-first` may mention other writers. Use a writer only after checking that it is installed and authorized. A missing CLI is a named gap, not a pretended run.
