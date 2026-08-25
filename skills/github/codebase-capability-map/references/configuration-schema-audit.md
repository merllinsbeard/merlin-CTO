# Configuration/schema audit reference

Use this reference when the capability question is about a plugin, app, or repository whose behavior is driven by persisted configuration (JSON, YAML, frontmatter, database rows, or UI state).

## Evidence ladder

Prefer evidence in this order:

1. Runtime schema/parser and defaults.
2. Behavior code that consumes each field.
3. Serialization/migration code and persistence boundaries.
4. Tests and fixtures that assert the public shape.
5. UI labels and README examples.

Treat UI text and README examples as discoverability aids, not proof of accepted keys, enum values, defaults, or current behavior.

## Four-layer model

Record every field in one of these layers:

- **Global persisted settings**: vault/application data applied as inherited defaults.
- **Local overrides**: board/view/document configuration stored with the object, often sparse.
- **Operational state**: last-used file, current filter, collapsed panels, manual pins, access timestamps.
- **Compatibility-only fields**: legacy keys accepted for migration but no longer written.

Do not mix these layers in a proposed profile. In particular, a transient `lastFilter` is not the same as a canonical saved view, and a global layout default is not a local frontmatter override.

## Reusable audit sequence

1. Pin the exact release or commit and confirm the source tree is clean/read-only before exploration.
2. Locate the canonical schema/default object, then extract every key, type, enum, range, and default.
3. Trace the parser and serializer. Check whether sparse overrides are resolved against defaults and whether hand-authored YAML/object input differs from the form written back by the application.
4. Locate migration code and classify old fields as active, read-only compatibility, migrated, or retired/stripped.
5. Trace behavior end-to-end: input scope → parsing/normalization → matching/routing → derived board/model → filters/sort/group/layout → writeback.
6. Inspect tests and fixtures for exact IDs, paths, query syntax, and edge cases; use them as evidence, not as an excuse to assume an untracked fixture is part of the release.
7. Build a capability matrix with columns for key, accepted values, default, persistence layer, behavioral effect, and evidence path/line.
8. Propose a minimal profile by keeping semantic fields that define the workflow, adding only high-value ergonomics, and leaving decorative or stateful fields out.
9. Explicitly list non-capabilities and non-enforced prose rules. A saved filter is not an automatic default view; a displayed column is not a limit on card count.
10. Verify the exact configuration with the project parser or focused tests when dependencies are ready. If execution is blocked by setup, report that as verification status and never claim a passing test.

## Profile-design heuristics

For a personal task/inbox board, prefer one routing dimension (usually explicit tags), a bounded scope, archive/someday exclusions, one property grammar, a readable property display, and a small number of named saved views. Avoid enabling grouping, manual ordering, debug display, and persistent last-state fields until the workflow actually needs them.

When a board has fixed custom columns plus synthetic `uncategorized`/`done` columns, configure only the custom columns; verify reserved IDs before proposing frontmatter. Preserve stable column IDs rather than relying on labels because manual state and collapsed-column state often key off IDs.

For query syntax, verify whether commas mean OR within a group and whitespace means AND across groups. Do not infer this from a natural-language saved-view name.

## Reporting standard

Cite source paths and line ranges for schema/defaults, persistence, and behavior. Label claims as implemented, compatibility-only, inferred, or unknown. Include the exact copyable config separately from the inventory, and state whether any files were changed. If a targeted test was attempted, report its real outcome and the blocker instead of substituting static parsing as test evidence.
