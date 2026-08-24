# Run record

- Case: `DC1`
- Condition: `baseline`
- Prompt: Continue the orchestration handoff. An approved record excludes Go services, harness adapters, and Git workspace management. A newer unapproved draft contains all three and supplies no new evidence.
- Expected routing: `decision-continuity`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

The continuation should stay with the approved record only:

- Keep the approved scope.
- Exclude Go services.
- Exclude harness adapters.
- Exclude Git workspace management.
- Ignore the newer draft for authority, because it adds no new evidence.

If you want, I can turn that into a clean handoff paragraph or a structured status block.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
