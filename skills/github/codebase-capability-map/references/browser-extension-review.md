# Browser-extension review evidence checklist

Use this when evaluating an OSS browser extension that connects to an agent runtime.

## Evidence to collect

- Candidate release/tag/date, installation/update path, and whether it is alpha, unpacked, store-distributed, or signed.
- Manifest permissions and host permissions, especially `debugger`, `tabs`, `scripting`, `cookies`, `nativeMessaging`, `downloads`, and broad `http/https/file` access.
- Security/privacy docs: token storage, page-context boundaries, prompt-injection handling, sensitive-page restrictions, approval gates, and persistence of raw page data.
- Live platform compatibility: exact protocol method names, gateway routes, feature flags, and whether the feature is enabled by default in the installed release.
- Real verification output: test count, build/lint/check status, and dependency audit. Keep runtime dependency exposure separate from dev-only packaging vulnerabilities.
- Open issues that change the deployment decision: session identity, stale runs, remote auth, control ownership, and model/runtime compatibility.

## Decision rubric

- **Adopt:** materially improves an uncovered workflow; permissions and update path are acceptable; live compatibility is proved.
- **Isolated pilot:** useful but new, broad, or operationally overlapping. Use a separate browser profile and scoped local token; start Chat-only/read-only.
- **Watch:** current stack already covers the capability, or the candidate is alpha/manual-install with unresolved ownership issues.
- **Reject:** unacceptable permissions, licensing, data boundary, or no credible maintenance path.

## Hermes-specific comparison

- Browser Harness owns ordinary interactive web work in `NeuromancerChrome`; Cua Driver owns native Mac GUI. Do not add a browser extension to the owner's everyday Chrome for a casual test.
- A candidate that uses `chrome.debugger` may create a second control lane. Check for debugger/CDP contention and exact tab/session ownership before enabling live control.
- Do not install a companion plugin or enable a controller feature in production until the gateway protocol and feature flag are verified against the installed Hermes release.
- A clean unit-test suite is evidence of implementation discipline, not evidence that the extension is the right operational surface.
