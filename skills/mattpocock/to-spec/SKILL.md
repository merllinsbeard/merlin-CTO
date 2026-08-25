---
name: to-spec
description: "Use to publish a conversation-backed spec autonomously."
---

Build and publish a spec from settled conversation context and codebase evidence. Use the decisions already present instead of reopening them.

Resolve the issue tracker and triage labels from the project instructions. In direct mode, a missing setup returns `/setup-matt-pocock-skills` as the next action. In Bot mode, record that missing setup as the external blocker.

## Process

1. Explore the repository when its current state is not already grounded. Use the project's domain glossary and relevant ADRs. Done: the affected behavior, existing test seams and binding decisions are named from live sources.

2. Choose the highest stable test seam for each result, preferring existing seams. Record the choice and rationale in the spec. When evidence leaves a product choice open, record one bounded assumption. Escalate only when that choice controls an irreversible external effect. Done: every result has a test seam or one explicit gap.

3. Write the spec with the template below and publish it to the project issue tracker with `ready-for-agent`. Done: the published body and label are read back from the tracker and match the spec.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A complete numbered list of distinct user-visible behaviors. Each story uses this format:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Cover every behavior in scope once.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
