# Run record

- Case: `GL-E8`
- Condition: `candidate`
- Prompt: The quality loop has exhausted the agreed time and token budget. The result is materially better but not subjectively perfect. Decide whether to stop and report the remaining verified gaps.
- Expected routing: `gauntlet-loop`
- Loaded skills observed in Codex events: `gauntlet-loop`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Stop.

Status: `Exhausted`—the agreed time and token limits are binding, and subjective perfection is not a valid reason to extend the loop.

Report:

- The exact best-known candidate evaluated.
- Each remaining mandatory criterion as `fail` or `unverified`, with current evidence.
- Any advisory or subjective polish gaps separately.
- Verification limitations, including stale or non-independent evidence.
- The smallest concrete next action required for each mandatory gap.

Do not claim `Verified` unless every mandatory criterion passed for that exact candidate. No further iteration should occur without a newly authorized budget.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
