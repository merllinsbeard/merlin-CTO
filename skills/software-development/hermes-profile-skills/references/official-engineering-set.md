# Official Hermes engineering set

Снимать с живого `$HERMES_RELEASE`, не с этой памятки, если дерево разъехалось. Релиз: `hermes --version` → Install directory.

Резолв src для каждого имени: `~/.hermes/skills/<rel>` если есть `SKILL.md`, иначе `$HERMES_RELEASE/skills/<rel>`, иначе `$HERMES_RELEASE/optional-skills/<rel>`.

## Bundled (`$HERMES_RELEASE/skills`)

software-development: dogfood, hermes-agent-skill-authoring, inspecting-hermes-desktop-dom, node-inspect-debugger, plan, python-debugpy, requesting-code-review, simplify-code, spike, systematic-debugging, test-driven-development

github: codebase-inspection, github-auth, github-code-review, github-issue-to-pr, github-issues, github-pr-workflow, github-repo-management

devops: sdlc-review

autonomous-ai-agents: claude-code, computer-use, hermes-agent, merge-reconciler, opencode

Official `codex` и `grok` тоже bundled. В CTO их не линковать, если уже есть profile-local копии.

## Optional (`$HERMES_RELEASE/optional-skills`)

software-development: ast-grep, code-wiki, rest-graphql-debug, subagent-driven-development

devops: docker-management

web-development: cloudflare-temporary-deploy, har-derived-api-client, page-agent

autonomous-ai-agents: antigravity-cli, openhands, blackbox

Не брать из optional как «всю инженерию»: mlops/*, finance/*, creative/*, gaming/*, health/*, blockchain/*, security/web-pentest, honcho.

Не делать `hermes skills repair-official --restore all`.

## Neuromancer extras (не official)

Только inbound symlink, чужой профиль не писать.

Брать под инженерную поставку / kanban / oracle: oracle, kanban-board-operations, kanban-sequential-campaign, branch-review-before-push, codebase-capability-map, clean-repo-publication, repo-sync-mac-server, product-surface-review, spec-checklist-audit, isolated-web-preview.

Не брать ops-флот: hermes-storage-doctor, cron-*, bot-mode, lab-public-*, github-trending-stars, telegram-topic-operations, persona-prompt-editing.
