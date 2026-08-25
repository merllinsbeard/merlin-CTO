# Repository-evolution and evidence-boundary audit

Use this reference when a user asks a code repository to answer narrative questions such as: what was built, what broke, what was fixed, who did what, whether a client accepted it, or whether a commercial claim is true.

The central rule is **evidence boundary**: distinguish what Git and source can prove from personal, commercial, and live-operational history that normally lives elsewhere.

## Claim classes and allowed conclusions

| Claim class | Strongest repository evidence | Safe conclusion | Do not infer |
|---|---|---|---|
| Current capability | Current source + canonical docs + tests | "Implemented in the inspected HEAD" | That production users exercised it |
| Historical evolution | Introducing/fixing commit plus inspected diff | "Project history records this change/fix" | Why it was originally introduced unless stated |
| Defect class | Fix commit, bug reproduction/test, and current guardrail | "History records a defect class and a remediation" | The exact incident impact or who caused it |
| Historical artifact | Archived task, PR note, audit report | "Historical artifact reports/records …" | That it is current truth or independently verified |
| CI state | Remote CI run tied to exact SHA | "CI passed for SHA …" | Live deployment, DNS/cutover, or client acceptance |
| Personal/commercial/client outcome | Contract, payment proof, CRM export, client communication, or analytics committed to repo | Only state the exact artifact | Discovery story, negotiated price, manual-vs-AI effort, client quote, revenue, adoption, or acceptance when absent |

For unsupported personal/commercial/client questions, answer exactly and plainly: **`НЕ УСТАНОВЛЕНО ПО РЕПОЗИТОРИЮ`**. Name the kind of external artifact that would be needed, without guessing its contents.

## Read-only audit sequence

1. **Read the repository truth map first.** Start with `AGENTS.md`, then any documentation index such as `docs/README.md`. Classify documents into canonical, reference, and historical/non-canonical before treating any prose as evidence.
2. **Pin the inspected state.** Record branch, full `HEAD`, working-tree status, and `git diff --check`. Do not attribute pre-existing changes to the audit.
3. **Build phase chronology.** Use first-parent log plus merge/feature commits to identify high-level stages. Inspect meaningful commit diffs; a commit subject alone is a lead, not complete proof.
4. **Trace each claimed defect.** For every material defect class, pair: (a) a fixing/introducing commit, (b) the changed current implementation or test, and, when applicable, (c) an operational guardrail/runbook. Prefer concrete classes such as auth/session, admin rendering, webhook drift, payment callback, CRM idempotency, notification recovery, or deployment safety over an unbounded bug list.
5. **Separate current from archival testimony.** Historical test reports and task documents can establish that a report once alleged an issue. Prefix their use with `historical artifact` and cross-check later code/history before saying it was fixed or still exists.
6. **Audit attribution separately.** Git author/committer/co-author metadata establish recorded commit metadata only. They do not provide line-level human/model provenance, causation, or a reason a defect occurred. Never write “Claude made error X” unless an authoritative artifact explicitly establishes that attribution; otherwise say “project history records …”.
7. **Verify maturity honestly.** Count/inspect tests and workflows, and fetch the latest CI result for the exact SHA when available. State separately: test code exists; CI passed; local tests were run; live integrations/cutover were verified. These are four different facts.
8. **Answer every requested question.** Give each a bounded answer, one or more exact evidence pointers, calibrated confidence, and explicit unknowns. Do not leave commercial or personal questions blank; mark them as not established.

## Evidence shapes

Use the most durable citation available:

- Current source/docs: `path:line`.
- Historical change: full or short commit SHA plus subject; include the diff only after inspecting it.
- Remote CI: workflow/run identifier, conclusion, timestamp, and exact SHA.
- Historical report: `path:line`, explicitly labeled archival/non-canonical.

A test declaration proves that an intended behavior is tested. It does **not** prove the test ran locally, passed on the inspected SHA, or worked against a live third party. A successful CI run proves the configured workflow passed for its SHA, not that production deployment or external SaaS state is correct.

## Remote metadata and strict read-only discipline

For audits that explicitly prohibit side effects, treat execution itself as evidence-sensitive:

1. Do not run application tests, builds, migrations, Compose startup, deployment scripts, or live third-party actions. Even a nominal test can write caches, alter a database, enqueue work, or contact a configured service. Prefer static source/test inspection, Git plumbing, and read-only remote metadata.
2. If authenticated GitHub access is available, query the PR check rollup and/or check-runs for the exact inspected SHA. Cite the SHA, workflow/check name, conclusion, and timestamp. A successful remote check proves only that configured workflow passed.
3. The GitHub Deployments API proves only what that API records. An empty list or zero records is **not** proof that no host-level deployment, DNS cutover, or release occurred outside GitHub Deployments.
4. Repository visibility proves the repository access setting only. It does not establish whether a user-facing product, domain, demo, or client case is public.
5. When a machine schema requires a precise unknown label, preserve the user's phrase verbatim (for example, `НЕ УСТАНОВЛЕНО ПО КОДУ` rather than silently substituting a broader label). Put bounded unknowns on each question object and emit no prose outside a strict JSON-only contract.

## Defect-class reporting template

For each verified class:

```text
name: concise technical class
what_broke: observed failure mode, scoped to available evidence
fix: concrete remediation now present
proof: fix commit + current source/test/runbook evidence
limits: what the evidence does not establish (incident count, live impact, attribution)
```

Avoid treating a historical issue list as a current defect inventory. It is useful for finding commits and regressions, but only becomes a verified resolved class after a diff/code/test cross-check.

## JSON-oriented deliverable template

For a strict answer contract, retain one object per question:

```json
{
  "question": 1,
  "answer": "bounded claim or НЕ УСТАНОВЛЕНО ПО РЕПОЗИТОРИЮ",
  "evidence": ["docs/project_brief.md:5", "abc1234 subject"],
  "confidence": "Высокая|Средняя|Низкая",
  "unknowns": ["what the repository cannot establish"]
}
```

Keep a separate `verified_defect_classes` list. This prevents a narrative answer from silently converting a historical report, a commit title, or a personal statement into a verified fact.

## Closure checklist

- All question numbers present exactly once.
- Canonical docs and historical artifacts visibly distinguished.
- Attribution language downgraded where no direct proof exists.
- Every claim has `path:line`, commit, or CI evidence; every gap has an unknown.
- Final maturity statement distinguishes repository/CI evidence from live acceptance.
- Audit made no repo changes; final `git status --short` and `git diff --check` are clean.
