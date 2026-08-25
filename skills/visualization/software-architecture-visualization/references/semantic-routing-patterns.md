# Semantic routing patterns

This reference captures a validated correction from a multi-view software architecture set. It is an example of form selection, not a reusable project fact sheet.

## Failure pattern

One visual style was applied to every architecture question. A generated retro product poster looked playful and compressed. After the host topology succeeded as an isometric map, that same engineering perspective was copied onto product, OSS, and lifecycle views. The set became consistent but less informative.

The correction was to route each question independently.

## Product: screenshot atlas

Use real browser evidence for every panel:

- employee journey: login, live recording, meeting library, ready meeting;
- visible functions: search, filters, statuses, MP4 playback, seek, subtitles, speaker labels, transcript downloads;
- separate band for operator-only tools such as model dashboards, metrics, alerts, and identity administration.

Pass the screenshots to `image_generate` as references. Require recognizable screens, short callouts, and explicit operator labels so the viewer does not mistake operator tools for product UI.

## Hosts: spatial map

An isometric map works when the question is physical placement. Each machine gets one boundary, address, hardware facts, contained services, and a short reason for the split. Untouched production sits outside the rollout path.

This success does not make isometric form the default for other questions.

## OSS: C4-like component map

Dense generated arrows become ambiguous. A clearer component map uses:

- flat host and network boundaries;
- one card per component with exact version and role;
- separate cards for separate databases;
- numbered interface badges on source and target cards;
- a contract legend with source, destination, and real transport or artifact.

This preserves wiring without drawing lines across cards. Useful contract labels include XMPP brewery, trusted HTTP event, OIDC callback, PgQueuer claim, MP4 manifest, async ASR, direct local GPU call, atomic READY, Range MP4, and transcript.

## Lifecycle: sequence and side rails

Use one lane per actor or processing boundary and move time in one direction. Split paths that differ operationally. In the validated case, ASR went through an authenticated gateway while diarization bypassed it and called a local model directly.

Put two subordinate rails below the main flow:

- identity: two identity inputs merge into one immutable principal, then an access grant and delivery ACL;
- failures: no recorder, bad correlation, and exhausted retries terminate without false success.

## Production method lesson

Every final infographic comes from `image_generate`. Dense text and connection-heavy architecture require shorter labels or several generated views. If generation remains inaccurate, report the blocker instead of switching to programmatic rendering.

## QA checklist

- inspect both full resolution and chat-size rendering;
- read every label and version;
- count panels, components, badges, lanes, and steps;
- trace every contract or arrow;
- verify separate databases and trust boundaries;
- distinguish user and operator views;
- distinguish deployed, target, STOP, and untouched production;
- after a correction, recheck the affected path and the surrounding layout.
