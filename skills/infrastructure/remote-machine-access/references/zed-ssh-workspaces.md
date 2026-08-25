# Zed SSH Workspaces

Use this recipe when Zed runs on one machine and the files live on another SSH host. It keeps one remote workspace and opens live files rather than copies.

## Preconditions

- The application machine is reachable through an existing SSH alias.
- From that machine, the data host is reachable non-interactively.
- Zed is installed and its bundled CLI responds to `--help`.
- Every requested path is readable from the Zed machine through the same SSH authority.

## Preflight

From the orchestrating host, verify the first hop. Then run the second-hop checks on the Zed machine:

```bash
ssh -G <data-host-alias>
ssh -o BatchMode=yes -o ConnectTimeout=8 <data-host-alias> \
  'for p in <absolute-paths>; do test -r "$p" || exit 1; done'
```

On macOS, a standard Zed installation exposes:

```bash
/Applications/Zed.app/Contents/MacOS/cli --help
```

Use the discovered path when the installation differs.

## Open several remote files in one window

Zed accepts remote targets in this form:

```text
ssh://[user@]host:/absolute/path
```

Create the workspace with the first file, then add each remaining file sequentially:

```bash
ZED=/Applications/Zed.app/Contents/MacOS/cli
"$ZED" -n "ssh://<user>@<host>:/absolute/path/first.md"
"$ZED" -a "ssh://<user>@<host>:/absolute/path/second.md"
"$ZED" -a "ssh://<user>@<host>:/absolute/path/third.md"
```

This sequential `-n` then `-a` pattern is the validated multi-file route. It keeps all targets on one remote authority and avoids the ambiguity of passing several remote URLs in one launcher invocation.

## Verify the visible result

On macOS, query Zed's window names without changing file contents:

```bash
osascript -e 'tell application "System Events" to tell process "Zed" to get name of every window'
```

The result must name every requested file in the same window. Also confirm that Zed owns a live SSH remote-server connection:

```bash
pgrep -lf 'ssh.*zed|zed.*remote|remote_server'
```

A successful launcher exit without this readback is incomplete.

## Report

State that Zed runs on the application machine, the files remain on the data host, and edits are live over SSH. Do not call them local copies.
