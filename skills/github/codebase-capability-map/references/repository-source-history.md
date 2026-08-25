# Repository source-history and API-name provenance

Use this reference when an audit asks whether a capability was implemented, planned, renamed, removed, or only documented.

## Evidence ladder

1. **Current implementation:** exact identifier search in source and tests; inspect schemas/registries, dispatch handlers, lifecycle methods, and transport registrations.
2. **Current documentation:** inspect the canonical docs page/source file, but keep documentation claims separate from implementation facts.
3. **History:** identify the first introducing commit by path, inspect its parent and child snapshots, then inspect later deletion/rename diffs. For GitHub, use the commits-by-path API and raw-at-commit URLs when a full clone is unavailable.
4. **Classification:**
   - `implemented`: registration plus handler/transport evidence;
   - `documented-only`: docs mention it, source does not register it;
   - `introduced`: a source diff adds the identifier, with commit/date;
   - `removed`: an earlier source snapshot contains it and a later diff deletes or renames it;
   - `not found`: exact search is clean across the explicitly inspected source/history scope.

## Reliable probes

```text
# Avoid substring false positives; quote the literal name.
git log --all --oneline -S'"tool_name"' -- .

# Enumerate a provider's actual surface.
search schemas -> get_tool_schemas/registry -> handle_tool_call/dispatch

# Enumerate an MCP surface.
@mcp.tool registration -> function name -> endpoint -> docs tool table
```

Use word-boundary searches for names such as `viking_recall`; `openviking_recall` or an internal variable named `_recall_tool_names` is not proof of a public tool. Do not call a related API a rename without a deletion/addition diff or explicit migration note. A docs-only commit that says a tool is available is evidence of a claim, not proof that the target project implements it.

## Transport/namespace check

Provider wrappers often prefix names (`viking_search`) while native MCP tools are unprefixed (`search`, `recall`). Trace automatic/lifecycle recall separately from explicit tool calls. Confirm the actual HTTP path (`/mcp` versus REST endpoints) before saying a capability is exposed through MCP.

## Citation shape

For concise reports use one row per finding: `finding → current source/docs link with line → introducing/removal commit → interpretation`. Include the inspection scope for negative findings. Prefer canonical GitHub blob links with line anchors, raw-at-commit links for historical snapshots, and commit URLs for dates and diffs.

## Validated OpenViking/Hermes pattern

In the examined case, OpenViking's Hermes integration docs mentioned `viking_recall`, but Hermes source registered six other `viking_*` tools and implemented automatic recall via REST `prefetch()`. OpenViking's native MCP endpoint independently introduced the unprefixed `recall` tool later. The correct conclusion was documentation drift/unimplemented wrapper name—not an assumed rename or removal.
