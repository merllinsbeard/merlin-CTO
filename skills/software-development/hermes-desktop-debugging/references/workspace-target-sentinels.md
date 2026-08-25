# Workspace target sentinels: concrete investigation

## Symptom

From the Projects overview, clicking `+` on Home opens a new session under the previously active project when another chat is already loaded. The UI control identifies Home correctly, but the persisted session receives the project cwd.

This note records source evidence from Hermes Desktop `v0.20.5` and the tracked upstream state inspected during the session. Re-check current source before applying any fix.

## Client/backend placement

The visible Electron client ran on the user's Mac and connected to a Hermes backend on `merlinde`. A CDP probe and process scan on `merlinde` could inspect only the backend machine. The absence of a Desktop renderer there did not describe the Mac client.

Rule: establish the machine boundary before interpreting localhost, process, or filesystem evidence.

## Confirmed call chain

### Project row

`ProjectOverviewRow` sends the project's path:

```ts
onClick={() => onNewSession(project.path)}
```

Home uses `path: null`. A component test confirmed that the Home button calls `onNewSession(null)`. That test stopped too early: it proved the leaf callback, not the session creation request.

### Occupied-chat path

The sidebar action requests a tab when the main chat is occupied:

```ts
startSessionInWorkspace(path, { openTab: true })
```

That branch calls:

```ts
openNewSessionTile('center', { cwd: path, listed: false })
```

The tile creator then resolved cwd with:

```ts
options?.cwd || resolveNewSessionCwd()
```

For Home, `options.cwd` is explicitly `null`. JavaScript treats it as falsy, so the code discards the explicit detached target and resolves the current project instead.

### Fresh-draft path

The non-tile helper had the same class of collapse:

```ts
const explicitTarget = path?.trim()
const target = explicitTarget || resolveNewSessionCwd()
```

An explicit Home target again becomes indistinguishable from an absent target. Fix and test both branches; changing only the tile path leaves the sibling defect.

## Domain model

The route needs at least three states:

| Input | Meaning | Expected boundary behavior |
| --- | --- | --- |
| `undefined` | No explicit target | Resolve project or configured default |
| `null` | Explicit no-workspace target | Create a detached session |
| non-empty string | Explicit workspace | Create in that cwd |

If the backend represents detached state by an omitted `cwd`, convert `null` at the request boundary. Do not convert it before fallback selection.

## Regression matrix

Test the final `session.create` payload:

1. Home `+`, main chat occupied: explicit detached target survives the tab or tile path.
2. Home `+`, no chat occupied: explicit detached target survives the draft path.
3. Project `+`: explicit path reaches `session.create` unchanged after normalization.
4. Generic New Session with no explicit target: project or configured fallback still resolves.
5. A delayed file-browser or cwd update cannot overwrite an explicit detached target before send.

The red assertion should inspect the exact request parameters. A button-level callback assertion is necessary but insufficient.

## Fix shape

Use presence semantics, not truthiness:

```ts
const hasExplicitCwd = options != null && Object.hasOwn(options, 'cwd')
const requestedCwd = hasExplicitCwd ? options.cwd : resolveNewSessionCwd()
```

Then normalize the explicit detached value according to the backend contract. For the draft helper, preserve `path === null` as an explicit branch instead of converting it through optional chaining.

A discriminated union is stronger if this state crosses several layers:

```ts
type WorkspaceTarget =
  | { kind: 'default' }
  | { kind: 'detached' }
  | { kind: 'workspace'; cwd: string }
```

## Verification cautions

- A closed issue describing the same symptom is only a lead. Verify the current expression and tests.
- An available update is not a fix unless the failing expression or regression tests changed.
- A status-bar label or file-browser tree can be stale. Verify persisted session cwd or the creation payload.
- The conversation did not verify a user-facing click-sequence workaround against persisted state. Do not promote one from this note as reliable guidance.
