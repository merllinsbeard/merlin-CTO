# Sequential canary and human acceptance

Use this checklist for releases with multiple gated capabilities (for example, Voice and Vision):

1. Keep all capability switches off while the immutable artifact is deployed.
2. Enable exactly one capability for the smallest trusted canary population.
3. Run the automated provider, persistence, replay, accounting, and failure-path checks for that capability.
4. Exercise the exact user-facing path. A health check, API 200, or container health is not acceptance.
5. If human testing is required, stop here and wait for the human result. A message asking the human to test is an open gate, not live acceptance.
6. On failure, disable the capability and record the failed gate. On success, record the exact revision and acceptance evidence.
7. Only then enable the next capability and repeat steps 2–6.
8. Run combined acceptance only after every capability passed independently.

Never enable several risky capabilities together merely because their automated checks passed. The release report must distinguish `deployed`, `canary-deployed`, and `live-accepted`.
