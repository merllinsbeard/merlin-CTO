---
name: software-architecture-visualization
description: "Use for fact-grounded software architecture visuals."
version: 1.0.0
metadata:
  tags: [architecture, infographic, screenshots, c4, sequence, visualization]
  related_skills: [baoyu-infographic, image]
---

# Software architecture visualization

Create architecture infographics from repository truth, deployment configuration, accepted decisions, receipts, and live evidence. This skill chooses the visual form and sets the verification bar. Every final infographic must come directly from `image_generate`.

## Production invariant

Use `image_generate` for every final infographic. The returned image file is the deliverable.

HTML, SVG, Mermaid, Graphviz, Canvas, Pillow, ImageMagick, browser rendering, and programmatic overlays do not produce an acceptable infographic. They may not replace, reconstruct, label, or repair the final image. Copying the generated file without changing its pixels is allowed.

If one generated image cannot preserve the required facts, shorten labels, split the content into at most three images, or use `image_generate` in edit mode. If those attempts still fail verification, report the image-generation blocker. There is no deterministic fallback.

Done: the final file has direct `image_generate` provenance and no later rendering or overlay step changed its pixels.

## Ground the system

Inventory every required host, component, interface, address, version, user function, and status before drawing. Keep these states distinct:

- `deployed`: runtime receipt or direct evidence exists;
- `implemented`: current source contains it, deployment unproved;
- `target`: accepted design, not live;
- `STOP`: an external gate blocks rollout.

Strip credentials, tokens, internal identifiers that are not needed for the explanation, and personal data from screenshot crops.

Done: every label and connection has a source, and target state cannot be mistaken for deployed state.

## Route by the question

Do not impose one house diagram style across a set. Choose the visual grammar that exposes the mechanism:

| Question | Primary form | What it must reveal |
|---|---|---|
| What does a person see and do? | Annotated atlas of real screenshots | Real screens, visible states, actions, user-versus-operator boundary |
| What runs on which machine and why? | Isometric or spatial host map | Hosts, hardware, placement, network paths, untouched environments |
| Which open-source components exist and how are they wired? | Flat C4-like container map | Versions, trust/network boundaries, databases, protocols and artifact contracts |
| How does one request or meeting move end to end? | Sequence/data-flow swimlanes | Time, actors, durable state, retries, identity and fail-closed branches |

A shared palette may tie the set together. The layout, perspective, and annotation system should change when the question changes.

Done: each image has one learning objective and a form suited to it.

## Build one image at a time

For each requested view:

1. Save source facts and a compact structured-content file.
2. Select the form from the table above and write a short-label prompt.
3. Call `image_generate` and keep its returned file as the candidate.
4. Inspect the full-resolution pixels and the expected chat/display size.
5. Fix defects only with another `image_generate` call, using edit mode for bounded corrections.

When the user already specified the deliverables, language, or correction, proceed without another style interview. Ask only when the decision changes the information structure.

## Form-specific rules

### Screenshot atlas

- Pass actual screenshots to `image_generate` as references and require recognizable screens.
- Remove secrets and irrelevant browser chrome before supplying a reference.
- Name visible functions only when the screenshot or source proves them.
- Separate employee/customer screens from operator/admin tools.
- Prefer four to eight panels with short callouts over a fictional journey illustration.

### Host map

- One explicit boundary per host or environment.
- Keep exact addresses and hardware only when sourced.
- Put each service inside its real owner boundary.
- Place untouched production outside the rollout path and omit rollout arrows.

### C4-like component map

- Put each component in exactly one owning boundary.
- Show separate databases as separate components.
- Prefer numbered interface badges plus a contract legend when direct arrows would cross cards.
- Label the real transport or artifact: XMPP, HTTP event, OIDC callback, SQL/PgQueuer, MP4 manifest, JSON/TXT/VTT, Range MP4.
- Show trust and internal-network boundaries without decorative false connections.

### Sequence/data-flow

- Time runs in one direction.
- Give each actor or processing boundary its own lane.
- Draw different paths separately. Example: authenticated ASR through a gateway versus direct local diarization.
- Keep identity reconciliation and failures in separate rails beneath the main flow.
- Failure branches terminate visibly and never reconnect to success without a new verified transition.

## Verification

Check the artifact itself, not the prompt or render success:

1. Read every headline, address, version, status stamp, and legend entry.
2. Count screenshots, hosts, components, badges, lanes, and steps.
3. Trace every arrow or numbered contract from source to destination.
4. Find duplicated, missing, or misplaced components.
5. Verify user and operator boundaries, database separation, deployed/target/STOP state, and untouched production.
6. Inspect clipping, overlap, empty areas, Cyrillic corruption, tiny text, and false decorative lines.
7. Re-open after each correction and repeat the affected checks.

Prefer semantic corrections over stylistic retries. If the model keeps corrupting dense text or connections, shorten the labels or split the view into separate generated images. Stop on a real image-generation blocker rather than replacing the model with a renderer.

The session-tested routing and correction pattern live in [`references/semantic-routing-patterns.md`](references/semantic-routing-patterns.md).

## Completion

Done means every requested image is a direct `image_generate` result, the full-resolution artifact was inspected, the expected display size remains readable, all connections were traced, and deployed, implemented, target, STOP, user, and operator boundaries are unambiguous.
