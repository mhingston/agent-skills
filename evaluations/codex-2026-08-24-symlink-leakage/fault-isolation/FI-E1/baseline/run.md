# Run record

- Case: `FI-E1`
- Condition: `baseline`
- Prompt: This queue consumer occasionally processes the same message twice. We can make it happen maybe once every 50 runs locally, but nobody knows why. Diagnose the root cause before we touch the implementation.
- Expected routing: `fault-isolation`
- Loaded skills observed in Codex events: `code-research`
- Agent-reported selection (not a native harness event): `code-research`
- Final response:

Research status: **Blocked**

The workspace contains no queue-consumer implementation, tests, configuration, dependency manifests, or Git history—only an untracked `README.md` and skill metadata. There is therefore no evidence from which to distinguish likely causes such as:

- acknowledgement occurring after a side effect;
- visibility timeout expiring during processing;
- retry after a lost acknowledgement;
- concurrent polling or lease renewal failure;
- non-atomic deduplication;
- duplicated message publication.

Please provide or mount the consumer repository, including its queue configuration and relevant tests. A failing-run log containing message ID, delivery attempt, consumer instance, processing timestamps, acknowledgement timestamp, and visibility/lease timing would significantly narrow the diagnosis. I made no implementation changes.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
