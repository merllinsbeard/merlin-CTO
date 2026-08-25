# Worktree overlap checklist

Use this before editing when multiple coding agents are active.

## Inspect

- Repository root and origin
- `git worktree list --porcelain`
- For every worktree: branch, `git status --short --branch`, latest commit, `git diff --stat`
- Active agent/editor processes and their worktree paths
- Remote state and open PRs when credentials are available

## Decide ownership

| Surface | Current writer | Evidence | Action |
|---|---|---|---|
| Implementation files | one agent | dirty diff / active task | hand requirements to owner |
| Independent research | separate agent | disjoint paths | allow parallel work |
| Shared integration boundary | orchestrator | agreed design | serialize review and merge |

## Handoff template

> Owner: `<agent/worktree/branch>`
>
> Files/surface: `<paths or subsystem>`
>
> Required behavior: `<acceptance criteria>`
>
> Do not: create a competing implementation or cherry-pick partial edits.
>
> Finish gate: review complete diff, run `<focused tests>`, then `<broader checks>`.

## Report template

`<owner>` owns `<surface>`. `<requirements>` are waiting there. Next gate: `<review/test/push>`. No second implementation is being merged.
