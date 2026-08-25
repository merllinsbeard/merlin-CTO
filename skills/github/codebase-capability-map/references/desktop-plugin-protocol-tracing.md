# Desktop plugin protocol tracing

Use this reference when asked to reconstruct an end-to-end protocol implemented by a Hermes Desktop plugin: an `@mention` handoff, a cross-profile command, a background result, or what the user actually sees.

## Evidence-first trace

1. Pin **both** repositories, not only the plugin: plugin `main` SHA and matching current `hermes-agent` SHA. Record `git ls-remote <repo> refs/heads/main`; cite immutable `blob/<sha>/path#Lx-Ly` anchors.
2. Treat README text, banner comments, and injected SOUL prose as hypotheses. Locate the executable registration (`ctx.register`, command handler, callback) and trace its payload instead. A current plugin may retain old terms or transport claims.
3. Follow the desktop boundary end-to-end:
   - plugin registration and input parsing;
   - core SDK invocation point (e.g. composer middleware chain);
   - resulting core gateway RPC and its session/profile scope;
   - any external CLI/process invocation and its stdout/stderr return path;
   - durable session write and the UI path that observes it (stream, polling, or reopen).
4. Label every edge as **automatic** (code invokes it), **protocol-directed** (LLM is told to invoke it), or **user/tool-runtime dependent**. Do not describe a prompt injection into the active agent as a guaranteed RPC handoff.
5. Separate similarly named background mechanisms. A plugin may tell an agent to run a terminal process with `background=true`; that is not evidence it uses the gateway's `prompt.background` RPC. Find call sites for both.
6. Check self-routing, aliases, unknown handles, code-block exclusions, duplicate mentions, target-chat bootstrap/recovery, target-busy behavior, and connection/list failures.
7. Explicitly establish interrupt semantics: does a message enter a running target turn, queue behind it, create a separate invocation, or lack live interrupt entirely?

## Report model

For a diagram, write two parallel paths:

- **Control/data path:** user input → plugin rewrite → active agent turn → command/RPC → target invocation → stdout/event → relay.
- **Persistence/display path:** session creation/resume → durable message row → stream or polling → source/target chat and roster rendering.

Call out the exact boundary where delivery stops being deterministic (usually active-agent tool choice or a background completion notification). Include the source scope and source commit for each non-obvious arrow.

## Validated example: Hermes Bot Mode, 2026-08-16

Pinned refs: `NousResearch/Hermes-Bot-Mode@5bd60417d6fbb5db5695526b2bce7c0db87478ba`; `NousResearch/hermes-agent@fe0a56ed16bb13122781c3a296c0fe7a79f3895f`.

- `@mention` middleware looks up profiles, excludes code, aliases `@hermes` to `default` where appropriate, rejects self/unknown targets, then **appends an instruction** to the active agent rather than sending a target RPC. Plugin: `plugin.js#L5068-L5153`.
- Core runs that middleware before its ordinary submit handler. Core: `apps/desktop/src/app/chat/composer/index.tsx#L118-L145` and `contrib.ts#L67-L95`.
- The injected protocol directs the agent to launch `hermes -p <target> chat --in ~ -c "Bot Chat" ...` using a background terminal call. That is a distinct profile-scoped CLI invocation whose final answer returns on stdout; it is not plugin-driven `prompt.background`. Plugin: `plugin.js#L5139-L5153`; core `prompt.background` implementation: `tui_gateway/methods_prompt.py#L1134-L1190`.
- `Bot Chat` is created/pinned through profile-scoped `session.create` plus a kickoff `prompt.submit`; the gateway defers the durable row until first prompt. Plugin: `plugin.js#L1910-L2027`; core: `tui_gateway/methods_session.py#L14-L159`.
- Delivery is per invocation and has no live interrupt of a mid-conversation target. README: `README.md#L64-L67`.

The plugin header/README contained stale descriptions of gateway-RPC delivery and `Agent Inbox`; execution in this pin uses CLI plus `Bot Chat`. Report the implementation, mention the divergence as a compatibility/documentation risk, and never silently harmonize the two.
