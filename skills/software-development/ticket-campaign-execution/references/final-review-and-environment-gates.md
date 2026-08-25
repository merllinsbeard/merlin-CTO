# Final review and environment gates

Use this reference for the terminal ticket of a tracker campaign, especially when work remains an uncommitted local diff.

## Reconcile lanes before review

The final review target is one observable tree. When independent tickets were implemented in separate worktrees and commits are forbidden:

1. Freeze the accepted source worktree and destination worktree; verify no writer is live in either.
2. Export the accepted source diff to a patch or compare the named files directly.
3. Use one reconciliation writer in the destination tree. For non-overlapping files, verify byte-for-byte equality with the accepted source. For overlapping files, verify both intents in the full diff and run both tickets' named checks.
4. Treat the writer report as advisory. If the writer has written the complete diff but hangs with no child test process, terminate the post-write session and perform acceptance from the actual tree.

Done when every accepted lane is present in one destination tree and the combined checks are green.

## Run one formal review

Freeze the review target as `HEAD + complete working diff + untracked files`; a branch range alone misses uncommitted work. Build a self-contained review bundle from the live spec and ticket bodies.

Run the single formal review as one parallel batch with decorrelated lenses, for example:

- **Standards axis:** repository canon, ADRs, security boundaries, generated contracts, test quality.
- **Spec axis:** every acceptance criterion, out-of-scope boundary, user-visible evidence.

The two outputs are one review event. Repair every hard/spec finding in one writer pass. Do not launch a second formal review after repairs; instead, read the repair diff and repeat every affected named check.

## Review findings that need behavioral proof

String-presence assertions are insufficient for routing, ACL, proxy, and generated-contract claims.

- Render edge/proxy templates with synthetic values and run the real pinned server in an isolated host-free network.
- Use a synthetic upstream that returns unique sentinel bodies.
- Probe a public peer and each permitted private peer.
- Assert both status and absence/presence of sentinel bodies: safe SPA fallback reaches the upstream; technical routes remain denied; private monitoring/internal routes remain reachable.
- Verify cleanup with a trap and avoid live hosts, deployment inventories, and secrets.

For generated APIs, compare runtime media type/body against generated OpenAPI and generated client types. For browser errors, use a red-capable event seam: an HTTP-successful media response does not prove decoder success.

## Distinguish code red from environment red

Read the first failing boundary. A suite that reaches assertions and fails behavior is code red. A suite that cannot create its disposable database/container/network is environment red.

For environment red:

1. Preserve the exact error and passed count.
2. Run independent checks that do not require the blocked resource.
3. Identify only test-owned stale resources; never broaden cleanup to production, volumes, or unrelated networks.
4. If local policy forbids cleanup, keep the final ticket open and record the exact human cleanup/resume criterion. Do not redesign tests or production topology to evade a local exhausted resource pool.
5. After cleanup, rerun the full originally named suite—not only focused tests—before closing.

Environment red is a blocker, not proof of either product failure or success.

## Final closure

Close the final ticket only when:

- all review findings are present in the destination diff;
- every affected focused check is green;
- the full combined gate is green after repairs;
- the proof comment records the orchestrator's commands and factual output;
- commit, push, merge, and deploy remain behind their separate approval gate.
