# Safe profile-local skill overrides

Use this when a profile audit finds that an invoked skill contradicts the profile and must change only for that profile.

## Resolve ownership before writing

An entry under `<profile>/skills/` may be a symlink. Before editing, resolve it and classify the target:

| Target | Safe action |
|---|---|
| Real directory inside the active profile | Patch through `skill_manage` when curator-managed |
| Profile-local vendor checkout | Patch only with explicit user direction; expect a vendor diff and update conflicts |
| Shared Hermes release, bundled catalog, external directory, hub install, pinned skill, or another profile | Do not patch |

If `skill_manage` says the skill is outside the trusted directory or cannot find a symlinked skill, do not retry the same patch. Inspect the resolved target and choose a profile-local replacement.

## Preferred replacement pattern

1. Create one class-level profile skill with `skill_manage`; do not create a one-incident skill.
2. Put the corrected workflow in that skill. Keep session evidence in `references/`.
3. Change AGENTS routing to the replacement's exact skill name.
4. Disable the inherited conflicting skill in the profile's `skills.disabled` list.
5. Verify with `hermes --profile <name> skills list --enabled-only`: the replacement appears and the inherited name does not.
6. Verify the shared release or external source has no diff.

This is better than relying on AGENTS precedence over a contradictory skill. The bad instructions disappear from the active profile instead of remaining available to model invocation.

## Profile assignment metadata

When the repair changes which Kanban work a profile may receive, update the orchestrator-facing description with the native command rather than only editing YAML:

```bash
hermes profile describe <profile> --text '<exact routing description>'
hermes profile describe <profile>
```

The second command is the required readback. Keep sticky-default ownership separate from technical-card eligibility: a profile can remain non-default while accepting explicitly routed root and child cards.

## Verification matrix

Programmatically assert the repaired behavior across all affected layers:

- AGENTS contains the mode selector and no stale rule.
- Profile description allows the intended assignment.
- Exact skill names resolve and are enabled.
- Contradictory inherited skills are disabled.
- Delegation model, effort, and concurrency match the prompt.
- Bot-mode planning paths contain no approval stop.
- Shared release and other profiles remain unchanged.

A successful write is not enough. Finish only when every assertion passes against live files and native CLI readbacks.
