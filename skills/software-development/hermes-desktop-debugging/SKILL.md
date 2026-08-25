---
name: hermes-desktop-debugging
description: Use when Hermes Desktop routes UI actions incorrectly.
---

# Hermes Desktop debugging

Debug the visible Desktop action as a routed state transition, not as one button handler. Hermes Desktop can split one user action across the Electron renderer, shared nanostores, tab or tile controllers, a local or remote gateway, and backend session creation. The same action may take a different path depending on whether a chat is already open.

## Workflow

### 1. Locate the renderer

Identify where the visible Electron client runs and where the agent/backend runs.

- A local Desktop may expose a development CDP port on the same machine.
- A Desktop connected to a remote gateway has at least two machines: the renderer machine and the backend machine.
- Process lists, localhost ports, and filesystem paths describe only the machine where the probe ran.

Completion criterion: every observation is labelled as client-side or backend-side. A missing renderer probe on the backend is not evidence about the client.

### 2. Define the exact transition

Write the user's action as input and expected persisted state:

- control clicked or shortcut pressed;
- current chat occupancy and selected tab or tile;
- selected profile, project scope, workspace, and gateway;
- expected `session.create` parameters and final sidebar placement.

Use persisted session data or the actual creation payload as the truth. A highlighted sidebar row, status label, or file browser can lag or belong to another surface.

Completion criterion: one check can distinguish the reported bug from a cosmetic mismatch.

### 3. Trace the entire call chain

Start at the rendered control and follow every callback to the backend request. Record each transformation of the target value. Search sibling paths for the same action, especially:

- empty main chat versus occupied main chat;
- fresh draft versus new tab or tile;
- center tile versus split tile;
- project row versus Home or detached row;
- local profile versus routed remote agent.

Desktop often has separate creation functions for these branches. A unit test around the button proves only that the first callback fired, not that the backend received the intended target.

Completion criterion: every branch that can handle the user's action reaches an identified `session.create` call or an explicit draft state.

### 4. Preserve sentinel meanings

Treat `null`, `undefined`, and `''` as domain values until the owning type proves otherwise.

Typical workspace routing semantics:

- `null`: explicitly detached or no workspace;
- `undefined`: caller supplied no target, so fallback resolution is allowed;
- `''`: normalized detached cwd at the backend boundary;
- non-empty string: explicit workspace path.

Truthiness fallback such as `value || resolveDefault()` collapses these states. Use a presence check, a discriminated type, or nullish coalescing only when its semantics match the domain. At the backend boundary, verify whether detached state is represented by omitting `cwd` or sending an empty value.

Completion criterion: explicit detached and absent target take different tests and produce different creation parameters.

### 5. Compare source, release, and upstream

Identify the exact client version before assuming a closed issue or later source file applies. Compare the installed revision with the tracked upstream branch at the failing expression. An available update is relevant only if that expression or its tests changed.

Completion criterion: any update recommendation names the commit or diff that removes the failing path. Do not recommend updating by version number alone.

### 6. Build regression tests at the seam

Test the creation payload, not only the button callback. The minimal matrix is:

1. explicit detached target with an occupied chat;
2. explicit detached target with an empty draft;
3. explicit workspace path;
4. absent target using project or configured fallback.

Assert the exact `session.create` parameters and, where tabs are involved, the tile's stored cwd.

Completion criterion: the test goes red on the reported branch and green only when sentinel semantics survive to session creation.

## Source-reading heuristics

- Search the prop name from the leaf control upward until its implementation appears.
- Search the session-creation helper downward to every caller.
- Read comments skeptically. A comment describing explicit-target precedence does not prove the expression implements it.
- Search tests for the final request payload. A nearby component test may leave the broken integration untested.
- When one branch contains a truthiness fallback, search sibling branches for the same pattern before fixing one site.

## Evidence note

A concrete workspace-routing investigation, including the call chain and missing test matrix, lives in `references/workspace-target-sentinels.md`.

## Pitfalls

- Do not relaunch or kill the user's Desktop to obtain a debugging port. Use the existing client if reachable, or an isolated instance with separate state.
- Do not infer session ownership from the file browser alone. It may show the previously focused workspace.
- Do not stop at a closed upstream issue. Verify the current code path and revision.
- Do not encode an unverified click sequence as a reliable workaround. Diagnose the source path or verify the alternative against persisted session state first.
