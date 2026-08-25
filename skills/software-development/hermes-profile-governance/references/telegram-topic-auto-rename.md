# Telegram topic auto-rename diagnosis

Use this reference when a Hermes profile generates internal session titles but Telegram topic names stay unchanged.

## Model the path as four gates

A successful rename requires all four gates. Do not stop after checking the config flag.

1. **Allowed.** Resolve `platforms.telegram.extra.disable_topic_auto_rename`. `false` permits renaming. Use `hermes config get` and `hermes config set`; do not hand-edit YAML.
2. **Activated.** Multi-session DM topic mode must be enabled for the chat and user in the profile's canonical `state.db`. The table is opt-in and may not exist until `/topic` activation.
3. **Bound.** The Telegram `(chat_id, thread_id)` must point to the Hermes session whose generated title will be applied.
4. **Applied.** Telegram must accept `editForumTopic` for that exact chat and thread.

A running gateway or an internal `sessions.title` proves none of gates 2 through 4.

## Profile-safe inspection

Resolve all paths from `$HERMES_HOME`. Named profiles do not use the default `~/.hermes/state.db`.

Check the canonical flag:

```bash
hermes config get platforms.telegram.extra.disable_topic_auto_rename
```

Inspect only the relevant rows in `state.db`:

```sql
SELECT chat_id, user_id, enabled,
       has_topics_enabled, allows_users_to_create_topics
FROM telegram_dm_topic_mode
WHERE chat_id = ?;

SELECT chat_id, thread_id, session_id, managed_mode
FROM telegram_dm_topic_bindings
WHERE chat_id = ? AND thread_id = ?;
```

Also read the current session row and routing entry. Confirm that `chat_id`, `thread_id`, `session_key`, and `session_id` agree across them.

## Activation and repair

Prefer Hermes' native `/topic` activation flow when a user is present. It checks BotFather capabilities, enables topic mode, and creates the system topic.

For an explicit headless operator task:

1. Call Telegram `getMe` with the profile's token without printing the token.
2. Require `HTTP 200`, `ok: true`, `has_topics_enabled: true`, and `allows_users_to_create_topics: true`.
3. Inspect the live `SessionDB` method signatures. If available, call `enable_telegram_topic_mode(...)` and `bind_telegram_topic(...)`. Prefer these native methods over direct SQL because they own schema migration and invariants.
4. Bind only the current chat, thread, user, session key, and session ID. Do not infer IDs from memory.
5. Read the mode and binding back from `state.db`.

If Telegram topics are disabled, stop at the real human-only BotFather setting. Do not create database state that claims the feature is active.

## End-to-end proof

Use the generated session title as the topic name and call `editForumTopic` for the exact current thread. A valid completion record contains:

- resolved config value `false`;
- topic-mode row with `enabled = 1`;
- binding row pointing to the current session;
- Telegram response `HTTP 200`, `ok: true`, `result: true`;
- gateway still running.

Telegram has no general read endpoint for arbitrary private-topic metadata. The successful write response is the external proof; the mode and binding readbacks prove that future auto-title events can reach the same path.

## Semantics to report

Hermes renames a new ad-hoc DM topic after its first completed exchange, when the auto-title pipeline creates the session title. Existing topics are not backfilled. If the user asked to fix the current topic too, rename that one explicitly and distinguish the manual repair from future automatic behavior.

Topics declared under `extra.dm_topics` are operator-managed and intentionally keep their configured names. Do not diagnose their preserved names as an auto-rename failure.
