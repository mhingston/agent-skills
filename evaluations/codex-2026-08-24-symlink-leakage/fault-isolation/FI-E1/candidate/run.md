# Run record

- Case: `FI-E1`
- Condition: `candidate`
- Prompt: This queue consumer occasionally processes the same message twice. We can make it happen maybe once every 50 runs locally, but nobody knows why. Diagnose the root cause before we touch the implementation.
- Expected routing: `fault-isolation`
- Loaded skills observed in Codex events: `fault-isolation`
- Agent-reported selection (not a native harness event): `none`
- Final response:

`BLOCKED`

The queue-consumer source and test harness are not present in this workspace. The repository has no commits or remotes and contains only a catalogue README, so there is no runnable symptom signal to investigate.

- Symptom contract: one message is reportedly processed twice in roughly 1 of 50 local runs; expected behavior is exactly-once processing.
- Evidence: `rg --files -uu` found no consumer, queue configuration, tests, logs, or fixtures.
- Unknowns: queue technology, acknowledgment timing, retry/visibility settings, consumer concurrency, and how “processed twice” is measured.
- Competing causes remain untested: broker redelivery, acknowledgment after side effects, visibility/lease expiration, multiple subscriptions, consumer restart, producer duplication, or a misleading test oracle.
- Cleanup: no files or implementation behavior were changed.

Please point me at the queue-consumer repository/worktree—or provide the consumer code, queue configuration, and the local command that exhibits the flake. With that, I can build a repeated-run oracle, minimize the failing schedule, and return an evidence-backed root cause before any fix is made.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
