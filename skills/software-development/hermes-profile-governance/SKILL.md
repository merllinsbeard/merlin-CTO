---
name: hermes-profile-governance
description: Audit and maintain Hermes profile behavior end to end.
author: Hermes Curator
version: 1.0.0
metadata:
  hermes:
    tags: [hermes, profiles, prompts, audit, configuration]
    related_skills: [hermes-profile-skills, writing-for-agents]
---

# Hermes profile governance

Treat a Hermes profile as one executable system. Its behavior comes from identity prompts, operational prompts, durable memory, profile metadata, runtime config, installed skills, and live integrations. Reading only one layer does not prove compliance.

## When to use

Use this skill when the user asks whether a profile fully reflects a voice note, specification, role definition, workflow, or prior decision. Also use it before declaring a profile canonical, cloning it, or enabling it for autonomous work.

For attaching skills to an isolated profile, use `hermes-profile-skills`. For writing any prompt or instruction an agent will execute, load `writing-for-agents` before editing.

## Outcome

Produce a criterion-by-criterion audit with direct evidence and one verdict per criterion. Distinguish prompt coverage from runtime proof. A sentence in AGENTS is not proof that the named skill exists, its body agrees, the dispatcher can select the profile, or the integration works.

## Sources and precedence

Inspect live sources in this order:

1. The user's current requirement, preserving direct quotes when wording matters.
2. Later explicit decisions that may supersede an earlier voice note.
3. `SOUL.md` for identity and ownership.
4. `AGENTS.md` for operating rules and routing.
5. `profile.yaml` for discoverability and assignment policy.
6. `memories/USER.md` and `memories/MEMORY.md` for durable preferences, ownership registries, and environment facts.
7. Selected runtime config values through `hermes --profile <name> config get <key> --json`.
8. The live skill index and the bodies of skills that control disputed behavior.
9. Live surfaces such as gateway, messaging, Projects, Kanban, delegation, and remote-machine access.

Live files and runtime beat recalled summaries. A later explicit decision can supersede an earlier quote, but name both rather than silently replacing one.

## Audit workflow

### 1. Build the checklist

Turn the source requirement into atomic criteria. Keep distinct criteria for identity, modes, routing, autonomy, review policy, repository authority, skill triggers, model selection, and external surfaces. Do not merge several requirements into one broad verdict.

### 2. Inventory the profile

Read the live prompt files and profile metadata. Locate the actual memory files under the profile's `memories/` directory rather than assuming they live at profile root. Do not read `.env`, auth files, tokens, or full secret-bearing config.

### 3. Read config selectively

Query only the keys needed for the criterion. Common keys:

- `model`
- `fallback_providers`
- `agent`
- `delegation`
- `kanban`
- `skills`
- `toolsets`
- `moa`

Do not dump the entire config. A configured model alias does not prove it is used by delegation or a CLI writer; inspect the specific subsystem.

### 4. Resolve every skill name

For each skill referenced by SOUL, AGENTS, USER, or MEMORY:

1. Confirm it appears in `skills_list`.
2. Load it with `skill_view`.
3. Read the section governing the criterion.
4. Check supporting references when the main file delegates behavior to them.

A similar vendor pack does not satisfy a missing router name. A dangling skill reference is MISSING.

### 5. Check cross-layer conflicts

Compare the operational prompt with the loaded skill bodies and profile metadata. Common conflicts include:

- AGENTS allows Bot mode while `profile.yaml` tells the dispatcher never to assign the profile.
- AGENTS permits one formal review while an execution skill mandates several reviews.
- AGENTS forbids questions in Bot mode while a planning skill requires user approval.
- The routing table names one writer or model family while the routing skill chooses another.
- The prompt grants repository authority that the ownership registry does not contain.

Higher prompt precedence may prevent some bad behavior, but a contradictory skill remains a maintenance defect. Report it as CONFLICT, not IMPLEMENTED.

### 6. Prove live surfaces

Verify each claimed capability through its native read-only status path. Examples include profile and gateway status, messaging configuration, active Projects, Kanban access, delegation model and concurrency, and remote-host reachability. A configured tool is not a completed end-to-end workflow.

If the full workflow has not been exercised, use UNVERIFIED even when all parts exist.

### 7. Assign verdicts

Use exactly one verdict per criterion:

- `IMPLEMENTED`: prompt and runtime agree, with required skill and live evidence present.
- `PARTIAL`: the mechanism exists but routing, scope, or coverage is incomplete.
- `MISSING`: no implementation or referenced skill exists.
- `CONFLICT`: two live layers prescribe incompatible behavior.
- `SUPERSEDED`: a later explicit decision intentionally replaced the original requirement.
- `UNVERIFIED`: configuration exists but the end-to-end path has not run.

Back each verdict with `file:line`, selected config output, or a native status readback.

## Applying repairs

A pure audit is read-only. When the user asks to fix the profile:

1. Settle conflicts before adding more text.
2. Patch the highest governing layer, usually AGENTS for routing and SOUL for identity.
3. Patch or replace contradictory skills instead of relying on prompt precedence forever.
4. Add missing router skills only when their target skills exist and the router has a stable class-level trigger.
5. Update ownership registries explicitly; never infer repository authority from project names.
6. Re-run the audit and then exercise one complete workflow.

## Pitfalls

- Declaring full coverage because SOUL and AGENTS contain the right words.
- Treating `skills_list` presence as proof that a skill's body agrees with the profile.
- Treating a running gateway as proof of a working messaging flow.
- Calling a profile autonomous while its metadata prevents automatic assignment.
- Treating a later safety restriction as an accidental omission. Mark it SUPERSEDED when the user explicitly chose it later.
- Writing profile repairs during a check-only request.

## Reference

See [`references/profile-compliance-audit.md`](references/profile-compliance-audit.md) for the validated probe matrix and conflict patterns.
