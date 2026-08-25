---
name: oracle
description: "Oracle second-model review: bundle prompts/files, debug, refactor, design-check."
---

# Oracle (CLI) — best use

Oracle bundles your prompt + selected files into one “one-shot” request so another model can answer with real repo context (API or browser automation). Treat outputs as advisory: verify against the codebase + tests.

## Main use case (browser, GPT‑5.6 Sol Pro)

Default workflow here: `--engine browser` with GPT‑5.6 Sol at the explicit Pro effort tier in ChatGPT. This is the “human in the loop” path: it can take ~10 minutes to ~1 hour; expect a stored session you can reattach to.

Recommended defaults:

- Engine: browser (`--engine browser`)
- Model: current browser Pro alias (`--model gpt-5-pro`), which Oracle 0.18 resolves to the current GPT‑5.6 Sol target. Prefer this alias for the default so the top Pro target follows supported model updates; use `gpt-5.6-sol` only when pinning that exact family is intentional.
- Maximum browser effort: `--browser-thinking-time pro`. `pro` is deliberate and distinct from `heavy`; it selects the top Pro tier exposed by ChatGPT's unified Intelligence picker.
- Model-picker strategy: `--browser-model-strategy select`. Maximum mode is fail-closed: a run must verify the requested model and effort instead of submitting silently at the UI's current setting.
- Research mode: keep `--browser-research off` for normal runs; follow the source policy below.
- Invocation: rely on the configured defaults or restate the current golden path exactly. Explicit CLI/MCP arguments override config; use a different model or picker strategy only when the user explicitly requests that variant.
- Parallelism: up to five concurrent browser tabs per shared profile (`--browser-max-concurrent-tabs 5`) for direct local browser runs. Oracle serializes the short profile/send critical section.
- Remote bridge limit: Oracle 0.18's `createRemoteServer` is intentionally single-flight and returns HTTP 409 `busy` for a second simultaneous remote run. Do not claim remote concurrency from `maxConcurrentTabs`; queue/reattach remote work or run independent Oracle processes directly on the signed-in Mac. Do not remove the bridge guard in-process: `runBrowserMode` is not safely reentrant there.
- Attachments: directories/globs + excludes; avoid secrets. For many text files, add `--browser-bundle-files --browser-bundle-format zip`.

## Source policy: standard web search stays available

Treat standard ChatGPT web search and the dedicated Deep Research workflow as separate capabilities.

- Normal mode (`browser.researchMode=off`) disables only the dedicated Deep Research workflow. It does not make the task closed-book.
- In normal mode, use standard ChatGPT web search when current or external technical facts would improve the answer. Request citations and label web findings separately from attached files and live evidence.
- Write the source instruction positively: “Use standard ChatGPT web search as needed. Treat attached files and verified live evidence as canonical for project-specific facts.”
- Use bundle-only or no-web operation only when the user explicitly requests a closed-book review. Do not infer closed-book mode from “Deep Research off”, “one-shot”, “review”, or the presence of a complete bundle.
- Activate `--browser-research deep` only when the user explicitly requests the dedicated multi-step Deep Research workflow.

## Golden path (fast + reliable)

1. Pick a tight file set (fewest files that still contain the truth).
2. Preview what you’re about to send (`--dry-run` + `--files-report` when needed).
3. Run in normal browser mode for GPT‑5.6 Sol Pro with standard web search available; activate the dedicated Deep Research workflow or API only when explicitly requested.
4. If the run detaches/timeouts: reattach to the stored session (don’t re-run).

## Commands (preferred)

- Show help (once/session):
  - `npx -y @steipete/oracle --help`

- Preview (no tokens):
  - `npx -y @steipete/oracle --dry-run summary -p "<task>" --file "src/**" --file "!**/*.test.*"`
  - `npx -y @steipete/oracle --dry-run full -p "<task>" --file "src/**"`

- Token/cost sanity:
  - `npx -y @steipete/oracle --dry-run summary --files-report -p "<task>" --file "src/**"`

- Startup/perf trace:
  - `npx -y @steipete/oracle --perf-trace --perf-trace-path /tmp/oracle-perf.json --dry-run summary -p "<task>" --file "src/**"`
  - Use when CLI startup or time-to-first-output feels slow; inspect `first-output` and `exit`.

- Browser run (main path; long-running is normal):
  - `oracle --engine browser --model gpt-5-pro --browser-thinking-time pro --browser-model-strategy select --browser-research off --browser-max-concurrent-tabs 5 --browser-bundle-files --browser-bundle-format zip -p "<task>" --file "src/**"`
  - **Robust default flag set:** explicit model/effort/research controls plus bundled ZIP attachments. Common failure modes and fixes:
    1. `Thinking time: option not found`, `status=unavailable`, or `verified=no` → treat the run as unverified maximum; inspect the saved session/log and fix the signed-in account or current picker flow instead of falling back silently.
    2. `Attachments did not finish uploading before timeout` (especially with a big/`>50KB` file or 3+ files) → keep `--browser-bundle-files --browser-bundle-format zip` (one ZIP upload instead of N).
    3. `Chrome window closed before oracle finished` → keep the automation browser/runtime available and reattach to the stored session instead of duplicating the run.
  - Run in the background (`run_in_background`) since it takes ~10–60 min; you'll be notified on completion. On error, check the run log, fix the flag, re-run with a fresh `--slug` (a stuck session shows `error` in `oracle status`).

- Manual paste fallback (assemble bundle, copy to clipboard):
  - `npx -y @steipete/oracle --render --copy -p "<task>" --file "src/**"`
  - Note: `--copy` is a hidden alias for `--copy-markdown`.

## Attaching files (`--file`)

`--file` accepts files, directories, and globs. You can pass it multiple times; entries can be comma-separated.

- Include:
  - `--file "src/**"` (directory glob)
  - `--file src/index.ts` (literal file)
  - `--file docs --file README.md` (literal directory + file)

- Exclude (prefix with `!`):
  - `--file "src/**" --file "!src/**/*.test.ts" --file "!**/*.snap"`

- Defaults (important behavior from the implementation):
  - Default-ignored dirs: `node_modules`, `dist`, `coverage`, `.git`, `.turbo`, `.next`, `build`, `tmp` (skipped unless you explicitly pass them as literal dirs/files).
  - Honors `.gitignore` when expanding globs.
  - Does not follow symlinks (glob expansion uses `followSymbolicLinks: false`).
  - Dotfiles are filtered unless you explicitly opt in with a pattern that includes a dot-segment (e.g. `--file ".github/**"`).
  - Default cap: files > 1 MB are rejected unless you raise `ORACLE_MAX_FILE_SIZE_BYTES` or `maxFileSizeBytes` in `~/.oracle/config.json`.

## Budget + observability

- Target: keep total input under ~196k tokens.
- Use `--files-report` (and/or `--dry-run json`) to spot the token hogs before spending.
- Use `--perf-trace` / `ORACLE_PERF_TRACE=1` for startup and first-output timing. Traces redact prompts, tokens, keys, cookies, and inline cookie payloads; detached API children write a session-suffixed sidecar trace.
- If you need hidden/advanced knobs: `npx -y @steipete/oracle --help --verbose`.

## Engines (API vs browser)

- Auto-pick: uses `api` when `OPENAI_API_KEY` is set, otherwise `browser`.
- Browser engine supports GPT + Gemini only; use `--engine api` for Claude/Grok/Codex or multi-model runs.
- Direct local browser runs share a bounded five-tab lease. Remote-bridge runs remain single-flight in Oracle 0.18. More tabs are not automatically better: account throttling and UI instability remain the limiting factors.
- **API runs require explicit user consent** before starting because they incur usage costs.
- Browser attachments:
  - `--browser-attachments auto|never|always` (auto pastes inline up to ~60k chars then uploads).
  - Add `--browser-bundle-files --browser-bundle-format zip` to upload many text files as one ZIP while preserving file names.
- Remote browser host (signed-in machine runs automation):
  - Host: `oracle serve --host 0.0.0.0 --port 9473 --token <secret>`
  - Client: `oracle --engine browser --remote-host <host:port> --remote-token <secret> -p "<task>" --file "src/**"`

## API preflight

- API runs require explicit user consent and cost money.
- Before API runs, check provider readiness without printing secrets:
  - `oracle doctor --providers --models gpt-5.4,claude-4.6-sonnet,gemini-3-pro`
  - `oracle --preflight --models gpt-5.4,gemini-3-pro`
  - `oracle --route --model gpt-5.4`
- If the user wants first-party OpenAI, pass `--provider openai` or `--no-azure`. This prevents exported Azure env/config from hijacking the route:
  - `oracle --provider openai --engine api --model gpt-5.5-pro ...`
- For advisory multi-model panels where partial success is useful, use `--allow-partial --write-output <path>` so successful model files and the `<stem>.oracle.json` manifest are easy to recover:
  - `oracle --models gpt-5.4,claude-4.6-sonnet,gemini-3-pro --allow-partial --write-output /tmp/panel.md -p "<task>"`
- `--timeout 10m` is the normal user-facing API deadline; Oracle derives the HTTP transport timeout unless `--http-timeout` is explicitly set.
- If the exported `OPENAI_API_KEY` is invalid and the user wants their personal OpenAI key, use `$one-password` in one persistent tmux session. Known item: `API Key - OpenAI - Personal`, field `api_key`. Inject only into the single Oracle command; never print the key:
  - `OPENAI_API_KEY="$(op item get 'API Key - OpenAI - Personal' --account my.1password.com --fields label=api_key --reveal)" oracle --provider openai --engine api --model gpt-5.5-pro ...`
- For debugging Oracle itself, prefer the local checkout after pulling `~/Projects/oracle`:
  - `pnpm -C ~/Projects/oracle run build`
  - `node ~/Projects/oracle/dist/scripts/run-cli.js ...`

## Sessions + slugs (don’t lose work)

- Stored under `~/.oracle/sessions` (override with `ORACLE_HOME_DIR`).
- Browser runs save durable files under `~/.oracle/sessions/<id>/artifacts/`, including `transcript.md`, Deep Research reports, and downloaded ChatGPT-generated images when available.
- Runs may detach or take a long time (browser/API + GPT‑5.5 Pro often does). If the CLI times out: don’t re-run; reattach.
  - List: `oracle status --hours 72`
  - Attach: `oracle session <id> --render`
- Use `--slug "<3-5 words>"` to keep session IDs readable.
- Duplicate prompt guard exists; use `--force` only when you truly want a fresh run.
- CLI guardrails: root runs without a prompt exit nonzero; `--dry-run` conflicts with `--render` / `--render-markdown`; Ctrl-C exits foreground API runs with code 130 while browser cleanup/reattach still runs.

## Prompt template (high signal)

Oracle starts with **zero** project knowledge. Assume the model cannot infer your stack, build tooling, conventions, or “obvious” paths. Include:

- Project briefing (stack + build/test commands + platform constraints).
- “Where things live” (key directories, entrypoints, config files, dependency boundaries).
- Exact question + what you tried + the error text (verbatim).
- Constraints (“don’t change X”, “must keep public API”, “perf budget”, etc).
- Source policy: preserve standard web search in normal mode and distinguish web findings from canonical project/live evidence; choose closed-book only on the user's explicit instruction.
- Desired output (“return patch plan + tests”, “list risky assumptions”, “give 3 options with tradeoffs”).

### “Exhaustive prompt” pattern (for later restoration)

When you know this will be a long investigation, write a prompt that can stand alone later:

- Top: 6–30 sentence project briefing + current goal.
- Middle: concrete repro steps + exact errors + what you already tried.
- Bottom: attach _all_ context files needed so a fresh model can fully understand (entrypoints, configs, key modules, docs).

If you need to reproduce the same context later, re-run with the same prompt + `--file …` set (Oracle runs are one-shot; the model doesn’t remember prior runs).

## Safety

- Don’t attach secrets by default (`.env`, key files, auth tokens). Redact aggressively; share only what’s required.
- Prefer “just enough context”: fewer files + better prompt beats whole-repo dumps.
