---
name: remote-machine-access
description: "Use for native SSH work across Macs and remote hosts."
---

# Remote Machine Access

Operate a user-owned machine through its existing SSH trust path while keeping the requested effect native to the target application. Prefer direct host and application interfaces over GUI imitation.

## Scope

Use this skill when work crosses machine boundaries: running a command on another host, opening live remote files in a local editor, checking a service on a Mac from Linux, or coordinating an application on one machine with files on another.

For native desktop clicking, accessibility trees, or pixel input, use `computer-use`. This skill owns the SSH topology, native CLI route, and end-to-end verification.

## Workflow

1. **Name both legs.** Identify the machine executing the application and the machine owning the data. State the requested effect in those terms before acting.
2. **Resolve existing trust.** Inspect the configured SSH alias rather than inventing an address, user, key, or port. Use `ssh -G <alias>` for effective non-secret routing fields and `ssh -o BatchMode=yes -o ConnectTimeout=<seconds> <alias> <probe>` for reachability.
3. **Discover the native interface.** On the application host, locate the app-provided CLI or automation interface and read its live `--help`. Prefer that interface over simulated typing or clicks.
4. **Preflight from the application host.** If the application will reach a second machine, verify that exact second hop and every requested target path from the application host. A first-hop success proves only the first hop.
5. **Apply one minimal action.** Use live remote paths when the user asked to edit live state. Do not create local copies unless copying is the requested outcome.
6. **Read back the effect.** Verify the exact application state: window or tab names, workspace identity, remote connection process, or another native state query. A zero exit code from a launcher proves invocation, not that the user can see the requested result.
7. **Report topology and boundary.** Say which machine owns the files, which machine runs the app, whether changes are live, and what verification observed.

## Guardrails

- Reuse configured aliases and keys; never print private key material, tokens, passwords, or full secret-bearing configuration.
- Keep SSH probes non-interactive. Stop rather than guessing credentials or opening an authentication prompt.
- Do not mutate SSH configuration when an existing route works.
- Do not bring a desktop window to the foreground unless the user asked to see it or the native interface requires it and the effect is expected.
- Verify file reachability without dumping private file contents unless their contents are needed for the task.
- Keep editor workspaces on one remote authority. Mixed local and remote arguments can produce ambiguous workspace behavior.

## Completion criteria

The task is complete only when:

- every requested target resolved on the correct machine;
- the native application accepted the action;
- an independent readback shows the requested files, window, workspace, or service state;
- the report distinguishes live remote state from copied local state.

## References

- For opening several live server files in one Zed window on macOS, including the validated sequential CLI pattern and verification probes, read [`references/zed-ssh-workspaces.md`](references/zed-ssh-workspaces.md).
