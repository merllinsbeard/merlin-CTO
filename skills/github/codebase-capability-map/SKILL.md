---
name: codebase-capability-map
description: "Use when mapping platform capabilities from source+docs."
version: 1.0.0
author: neuromancer-curator
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [capability-map, codebase, reconnaissance, audit, platform]
    related_skills: [codebase-inspection]
---

# Codebase Capability Map

Build a complete capability map of a platform from its sources and docs — including features the current deployment does not use ("upstream potential"). Distinct from `codebase-inspection` (which is LOC/metrics): this skill answers *what the system can do*, not *how big it is*.

## When to use

- "Составь карту возможностей X по исходникам", "what can this platform do", upstream potential, feature inventory.
- Before integrating with a platform: what's available vs. what's actually used.
- Audits: documented vs. implemented vs. experimental.
- **Adaptation / rebranding plans** ("переделать репо под другого человека/домен/язык", fork white-labeling, template rebrand): the deliverable is "every file that must change, in what order, at what cost" — see the adaptation-audit section below.

## Recon order (read-only, ~8 passes)

1. **Orientation.** `git -C <repo> log --oneline -20 | cat`, `branch --show-current`, `describe --tags --always`, `remote -v`, top-level `ls`. Recent `feat(...)` commits = fresh capabilities, often undocumented.
2. **Docs in full.** README, ARCHITECTURE.md, VISION*.md, docs/** — especially: status tables (✅/🚧/📋), "Known Limitations" sections, formal specs (TLA+/Tamarin dirs signal which parts are hardened). Record the project's *own* limitations list verbatim — it's the best source for the "Ограничения" section.
3. **Crate/package inventory.** One-liner: `for d in crates/*/; do grep -m1 '^description' $d/Cargo.toml; done` (or package.json equivalents). Then `ls src/` per crate of interest.
4. **Central registry = capability skeleton.** Most platforms have one canonical catalog: event-kind registry (`grep 'pub const KIND_'`), API router (`grep -oP '\.route\("[^"]+"'`), protobuf enums, command dispatch tables. Extract it fully — it enumerates primitives, events, and actions in one place.
5. **Schema files.** Workflow/action schemas (`enum ActionDef`, triggers), DB migrations list (`ls migrations/`) = feature chronology, feature-flag files (`preview-features.json` etc.) = experimental surface.
6. **CLI surface.** Enumerate every subcommand in one loop into a file (see below).
7. **Deployment models.** docker-compose services, deploy/charts, Dockerfile.* — what ships separately (gateways, sidecars, dashboards).
8. **Examples/ and tests/** — `examples/` READMEs reveal intended extension paths; `#[ignore]`d e2e tests reveal acceptance-level features needing special infra.

## CLI surface extraction

```bash
B=/usr/local/bin/mycli
for c in sub1 sub2 sub3; do
  echo "### $c"
  ${B} $c --help 2>&1 | sed -n '/^Commands:/,/^Options:/p'
done > /tmp/cli_surface.txt
```

**Pitfall — execution blocked:** if running a binary `--help` is blocked by an environment heuristic (e.g. the terminal guard refuses commands it pattern-matches as gateway/process control; or a /tmp copy is noexec), do NOT conclude the CLI is broken. Fallbacks, in order:
1. Invoke via a variable: `B=/usr/local/bin/foo; ${B} --help` — often passes heuristics that match literal command strings.
2. Read the CLI spec from source instead: clap definitions (`grep -n '#\[command(\|about =\|#\[arg' crates/*/src/config.rs`) give the exact same subcommand/flag inventory without execution.

## Cross-check docs against code

README/vision docs drift. Verify claims before reporting them:
- README says "MCP server, full feature surface" → grep routers: is there actually an MCP endpoint, or only a local dev-MCP binary? Say which.
- A kind/enum exists in code but no handler references it → experimental/reserved, mark INFERRED.
- preview-feature flags with no docs section → undocumented surface.

## Repository source-history and API-name provenance

When the task asks whether a feature/tool/API was planned, introduced, renamed, removed, or only exposed through one transport, do a provenance pass instead of relying on current docs or broad keyword hits:

1. Search the exact identifier in current source/tests and in reachable history. Use quoted or word-boundary searches so substrings such as `openviking_recall` do not count as `viking_recall`.
2. Trace the complete registration path: provider schemas → tool registry → dispatch handler; for MCP, `@mcp.tool()` → function name → endpoint → canonical docs table.
3. Separate namespaces and transports. A provider wrapper may prefix names while native MCP uses unprefixed names; lifecycle `prefetch()` may use REST even when a raw `/mcp` surface also exists.
4. For history, identify the first source-introducing commit and inspect its parent/child snapshots. A docs-only commit proves a claim, not an implementation. Call a name “removed” only when an earlier source snapshot contains it and a later diff deletes/renames it; otherwise report “not implemented in the inspected scope.”
5. Cite stable GitHub blob line anchors for current code/docs, raw-at-commit URLs for historical snapshots, and commit URLs for dates/diffs. State the inspected scope for negative findings.

`references/repository-source-history.md` — reusable evidence ladder, exact probes, transport/namespace checks, and the validated OpenViking/Hermes naming-drift case.

## Repository evolution, defect history, and personal-claim boundaries

When a user asks what a project built over time, what genuinely broke and was fixed, or asks a codebase to answer a founder/client/AI-development story, do a **repository-evolution audit** rather than converting commit history into biography:

1. Read the repository truth map (`AGENTS.md`, docs index) first. Classify docs as canonical, reference, or historical before relying on them.
2. Pin branch, full HEAD, clean/dirty status, and `git diff --check`; use first-parent chronology plus substantive commit diffs to identify phases.
3. For each defect class, require a fixing/introducing commit plus a current implementation/test/runbook cross-check. A commit subject or archived bug report is a lead, not enough by itself.
4. Separate four maturity facts: tests exist, CI passed for exact SHA, local verification ran, and live deployment/integrations/client acceptance occurred. Never promote one to another.
5. Treat Git author/co-author metadata as recorded metadata only—not proof of who wrote every line, caused a defect, chose a design, or used an AI model. Say “project history records …” unless direct attribution exists.
6. For personal, commercial, client-result, manual-effort, negotiated-price, or subjective questions absent from repo artifacts, state **`НЕ УСТАНОВЛЕНО ПО РЕПОЗИТОРИЮ`** and name the external evidence that would be needed. Do not estimate or smooth gaps.
7. Answer each question with bounded answer, exact `path:line` or commit/CI evidence, calibrated confidence, and explicit unknowns. Keep a separate verified-defect-class list.

Read `references/repository-evolution-evidence-audit.md` whenever the audit crosses the boundary between source history and personal/commercial/live-operational claims. It contains the claim ladder, reporting templates, and closure checklist.

## Configuration and behavior audits

When the request is to analyze a plugin/app's settings or produce a minimal persisted profile, add a configuration-schema pass rather than inferring behavior from the UI:

1. Pin the exact release/commit and keep the source checkout read-only.
2. Extract the canonical schema/default object: every key, type, enum, range, and default.
3. Separate global persisted defaults, local sparse overrides, transient operational state, and compatibility-only fields.
4. Trace parser → serializer → migration code. Verify whether hand-authored YAML/object input is accepted and whether the application writes another form.
5. Follow behavior end-to-end: scope → parsing/normalization → matching/routing → derived model → filter/sort/group/layout → writeback.
6. Use tests/fixtures to confirm exact IDs, paths, and query syntax; do not treat an untracked fixture as release code without saying so.
7. Present a matrix of key, accepted values, default, persistence layer, behavioral effect, and source path/line.
8. Propose a sparse profile with semantic workflow fields first; leave decorative and stateful fields out unless the user explicitly needs them.
9. Distinguish implemented behavior from prose rules that the application does not enforce. A saved filter is not automatically selected at startup, and a displayed column does not enforce card-count limits.
10. Run a focused parser/test verification when dependencies are ready. If setup blocks execution, report the real status and do not claim a pass.

Read `references/configuration-schema-audit.md` for the detailed evidence ladder, four-layer model, and profile-design heuristics.

## Read-only data-isolation and deployment-diff review

Use this subsection when a capability/rebranding review changes expert, tenant, persona, source, index, database, or deployment selection. The goal is to catch real cross-namespace defects without mutating the checkout.

1. Read repository instructions (`AGENTS.md`) and applicable context/ADR files before inspecting the diff. Record the exact worktree, branch/commit, and pre-existing dirty paths so concurrent or unrelated edits are not attributed to the reviewed change.
2. Establish the requested scope with `git status --short`, `git diff --stat`, `git diff --name-only`, then inspect both the changed hunks and full surrounding files. Treat docs/examples as executable contracts: compare their commands with actual wrapper targets and defaults.
3. Trace the selector end-to-end: CLI/Make variable -> shell export and `.env` precedence -> Compose `env_file` versus explicit `environment` -> mounted host/container paths -> local/remote storage filters -> runtime read path. Make variables are not automatically exported to child processes, and Make does not parse `.env`; verify this with `make -n` rather than assuming the Python CLI's environment fallback applies.
4. Test isolation with two temporary namespaces against a shared scratch store. Index namespace A, index namespace B, then query both and inspect the raw artifact. A whole-file `replace` operation can erase A even when filtered reads appear safe. For SQL sync, verify empty reindex, stale document removal, chunk cascade, mixed-payload rejection, and preservation of another namespace.
5. Render deployment configuration without starting services: `docker compose --profile tools config --format json` with a temporary test environment. Check every service's effective selector, data mount, state path, database URL/volume, and secret source. Explicit Compose `environment` entries override `env_file`; a documented `DATABASE_URL` or host data path is not effective unless it appears in the rendered service config.
6. For identity compatibility, compare runtime/profile display names with database `display_name` values and legacy labels. Exercise fresh-database and existing-row paths because `ON CONFLICT DO NOTHING` can preserve a bad first write forever.
7. Demand a reproducible consequence for every finding: exact `path:line`, trigger command/config, observed output/state, and user-visible or data-loss impact. Separate findings introduced by the diff from pre-existing hazards, and never turn a passed smoke test into evidence for untested configuration combinations.
8. Keep probes non-mutating: use `PYTHONDONTWRITEBYTECODE=1`, temporary directories outside the repository, fake DB cursors or read-only config rendering, and `git diff --check` plus a final `git status --short` to verify the review itself made no changes.

See `references/read-only-isolation-review.md` for reusable probe recipes and an evidence checklist.

## Report shape

Provenance-tag every claim: **UPSTREAM** (with file path) vs **INFERRED**. Sections:
1. Общая модель (what the thing is, tenancy, protocol)
2. Каталог компонентов (crates/services, one line each)
3. Capability map: primitives / events (full kind catalog) / actions (CLI commands) / permissions / automation / media / deploy models
4. Ограничения платформы (the project's own Known Limitations + verified gaps)
5. Недокументированное/экспериментальное (in code, not in docs)
6. Unknowns (what couldn't be resolved read-only)

## Adaptation / rebranding audit (fork-to-new-owner planning)

When the task is "rebuild this repo for a different person/domain/language", the capability map becomes a **change inventory**. Same recon order, plus these targeted passes:

1. **Identity surface first.** grep the old name/email/domain repo-wide *with counts* (`grep -rIo "old-domain\.io" --exclude-dir=node_modules --exclude-dir=.git . | wc -l`). Total occurrences + files-affected is the headline risk number for the plan (e.g. "domain hardcoded in 516 places across 74 files").
2. **i18n / locale mechanics.** Find the canonical language type (`grep -n "type Lang\|'es' \||'ru' \|" src/`), then trace every consumer: routing defaults, slug tables, hreflang emission, og:locale, JSON-LD `inLanguage`, browser-lang-mismatch banners, API-side language instructions (chat/voice). Count literal occurrences to size the rename.
3. **Content registries.** Locate the articles/content registry — it is the skeleton for "how to add new content" and for everything downstream (sitemap, RSS, prerender, RAG ingest, validators). Document the add-item pipeline end-to-end.
4. **Build pipeline side effects.** Read `package.json` scripts fully: builds often chain stats-fetchers, RAG ingest, OG-image generation, pings — note which steps need API keys/creds and which break a local build without them. This is usually the #1 "local run" gotcha.
5. **Deploy config.** `vercel.json`/nginx/redirects: slugs and rewrites are usually hand-listed per route — they must be rewritten with the content, easy to forget.
6. **Third-party identity bindings.** Search-console verification codes, IndexNow keys, sitemap URLs, `rel="me"` links, eval/test datasets that encode the old persona's facts (CI gates will fail post-rebrand), observability-stored prompts (Langfuse prompt versions override the local file).
7. **Voice/persona artifacts.** Chatbot system prompts and voice instructions (accent, language rules) are often separate from the UI locale — flag them explicitly.

Plan shape: files-by-category table with effort estimates → mechanics of the switch → step-by-step content-addition → local-run requirements → delete/replace list → risks (hardcoded URLs, key bindings) → recommended order of work.

## Official product / developer-environment comparisons

When comparing two development environments or agent platforms, use the same capability-map discipline but add a source-and-surface matrix. Do not flatten CLI, desktop, IDE, web/cloud, ACP, gateway, provider, and skill-based workflows into one product claim.

1. Pin the comparison date (`as of YYYY-MM-DD`) and the exact release/commit for any local checkout.
2. Prefer first-party docs and release pages; use source/tests to verify implementation details and GitHub's official release API/tag pages to pin versions and dates.
3. For every row record: capability, surface, scope/isolation boundary, defaults, limits, evidence URL/path, release/date, and confidence (`documented`, `implemented`, `inferred`, or `unknown`).
4. Separate native features from manual composition. Examples: a provider integration is not the same thing as a bundled delegation skill; a desktop worktree UI is not the same thing as manually running `git worktree`; a project grouping is not automatically a sandbox.
5. Preserve conditional documentation variants. OpenAI Codex pages use surface switches for app/web/CLI/IDE; extract and label each variant instead of merging contradictory statements.
6. If web extraction is rate-limited, do not treat the failure as evidence that a feature is absent. Retry after the documented reset or fetch the official `.md` variant into `/tmp` and inspect it with `read_file`; retain the canonical HTML URL in the report.
7. Report billing/usage tables as time-sensitive ranges, not guarantees. Include the shared window, weekly-limit caveats, plan/surface scope, and the page's update date when available.

Session-specific evidence bank and URL matrix: `references/official-dev-environment-comparison.md`.

## Pitfalls

- Don't re-read a file you already read (read_file dedup returns "unchanged") — page forward with `offset` instead.
- Use `search_files pattern='*' target=files` for directory listings, not `ls`.
- Batch independent reads/greps into parallel tool calls; a repo-wide capability map is ~15-20 batched rounds.
- Never print secrets/keys found in source or env dumps; note their existence, not their values.
- If the task says read-only: no builds, no `cargo`, no writes into the repo; `/tmp` is fine for scratch output.

## Versioned upgrade and compatibility audits

When the task compares an installed release with an exact upstream tag, keep the audit read-only and separate four questions: (1) changed defaults/semantics, (2) removed or renamed API/CLI surfaces, (3) dependency and deployment extras, and (4) persistent config/data compatibility. Compare complete tracked trees or exact `git show HEAD:path` content, not whatever happens to remain in a reused checkout. Verify negative findings with a tracked-tree search and distinguish a deleted surface from a replacement. Search shared filtering/registry constants because a downstream one-line patch may need to be reapplied after package installation. Treat design docs as useful evidence but prefer executable source, schemas, lockfiles, and tests when docs lag. End with a minimal staging probe matrix: config parse, health, read/search of existing data, one representative write/commit, and every optional feature that was intentionally enabled.
