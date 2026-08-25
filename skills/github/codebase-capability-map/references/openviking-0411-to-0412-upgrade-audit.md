# OpenViking v0.4.11 → v0.4.12: upgrade-audit reference

Session-specific evidence bank for a read-only tag-to-tag audit. Upstream repository: `volcengine/OpenViking`.

## Exact source points

- v0.4.11: tag `v0.4.11`, commit `49ca3cdfe8336cd9f54a4c7d391b5846cb3f88f6`.
- v0.4.12: tag `v0.4.12`, commit `c1d38eb47ff2ebf9ff4cee46756728893fd8caf3`.
- Verify both checkouts with `git status --short`, `git rev-parse HEAD`, `git ls-files`, and `git show HEAD:path`; do not trust a stale/untracked working-tree file as tag evidence.

## Findings

### Agent Evolution is a deployment-level default change

v0.4.12 adds `AgentEvolutionConfig` and `ServerConfig.agent_evolution` in `openviking/server/config.py`; `enabled` defaults to `false`. The HTTP-server setting is instance-wide. A disabled commit removes `cases`, `trajectories`, and `experiences` from the effective memory policy; existing memories remain readable/searchable. Session-level `memory_policy` remains an allow-list below the global switch.

Relevant sources:

- `openviking/server/config.py:84-109,267-295`
- `openviking/session/session.py:113-150,1734-1753,2130-2164`
- `openviking/session/compressor_v3.py:301-374`
- `docs/design/agent-evolution-global-switch-design.md:1-112`
- `docs/en/guides/01-configuration.md:1451-1479`

For a deployment that must preserve pre-upgrade production, explicitly set:

```json
{"server": {"agent_evolution": {"enabled": true}}}
```

Per-user legacy `agent_evolution` values are parse-only and ignored. Archive metadata stores the commit-time decision; older archives without the snapshot preserve historical enabled behavior during recovery.

### The `tasks` visibility issue persists upstream

`openviking/storage/internal_names.py` still includes `"tasks"` in `STORAGE_INTERNAL_ENTRY_NAMES` in v0.4.12, and `openviking/storage/viking_fs.py` uses that set for directory visibility filtering. Compare the file byte-for-byte across the two tags before and after applying a downstream patch. If the deployment intentionally exposes task records, reapply the local patch after package installation and verify the imported constant plus an actual list/tree request.

### MCP and Bot dependency boundaries

v0.4.12 changes the root dependency to `mcp>=1.27,<2` and the `[bot]` extra to `mcp>=1,<2`; retaining an operational `mcp<2` constraint is compatible and defensive. `[local-embed]` remains `llama-cpp-python>=0.3.0`.

`ov compile` is a Bot-backed HTTP workflow: the Rust CLI posts to `/bot/v1/compile`, and the OpenViking Bot proxy returns 503 when Bot is disabled. The command requires a reachable VikingBot deployment; the bundled topology needs `openviking[bot]` and server `--with-bot` (or equivalent `server.with_bot=true`). Do not add `[bot]` merely for ordinary OpenViking/CLI/session use.

Relevant sources:

- `pyproject.toml:88,143-178,195-209`
- `crates/ov_cli/src/main.rs:1018-1048`
- `crates/ov_cli/src/commands/compile.rs:30-35`
- `openviking/server/routers/bot.py:57-64,175-244`
- `openviking/server/bootstrap.py:165-171,249-313`
- `docs/en/api/24-vikingbot.md:1-3,138-160`

### Legacy code-navigation surfaces were removed

Between the tags, the old `/api/v1/code/{outline,search,expand}` router, old code AST helpers, and their REST/MCP tests are deleted. Verify consumers with a tracked-tree search for `code_outline|code_search|code_expand|/api/v1/code`; absence in the newer tag is evidence of removal, not proof of a replacement. Known active Ansible/scripts callers were absent in the audited deployment, but external MCP/OpenCode/Codex clients require a separate check.

### Compatibility and migration scope

No dedicated 0.4.11→0.4.12 data migration command was identified. Existing memory files remain readable; the Agent Evolution queue payload stays unchanged and the commit decision is stored in archive metadata. The historical `admin migrate` flow is for older legacy 0.3.x agent/session namespaces, not a routine 0.4.11→0.4.12 upgrade.

If VikingBot uses the old `agents.commit_keep_recent_count`, v0.4.12 accepts it for config compatibility but does not automatically translate a physical-message count into the newer Turn-aware settings. Review `commit_keep_recent_turn_count`, `commit_retained_message_token_budget`, and `commit_min_raw_tail_steps` explicitly.

## Minimal post-install probes

```bash
python -c 'import openviking; print(openviking.__version__)'
python -c 'from openviking.storage.internal_names import STORAGE_INTERNAL_ENTRY_NAMES; assert "tasks" not in STORAGE_INTERNAL_ENTRY_NAMES'
openviking-server doctor
ov health
```

Then exercise, on staging, an existing-memory read/search, a session commit, task visibility, and `ov compile` only if `[bot]` and Bot proxy were intentionally enabled. Keep a config/workspace backup before restart; do not infer downgrade safety from a successful upgrade.
