---
name: wrap-up
description: Reflect on one completed or ending agent session and capture only material friction, corrections, discoveries, effective patterns, and skill or documentation gaps as structured observations for later longitudinal analysis. Use when the user asks to wrap up, capture lessons, reflect on a just-completed session, or process a pending lifecycle-hook reminder. Do not directly rewrite skills, agent instructions, memory, or policy from a single session.
compatibility: Optional automatic lifecycle capture requires filesystem access and a supported Claude Code or Codex hooks configuration.
---

# Wrap Up

Turn one completed or ending session into a small, evidence-grounded observation
packet. Capture useful learning without promoting a one-off experience directly
into durable agent behaviour.

This is a **single-session capture** workflow. Longitudinal clustering,
qualification, and promotion belong to a later learning workflow.

## Boundaries

- Treat the session transcript and concrete run artefacts as evidence; do not
  reconstruct missing events from memory or model narration.
- Capture only material observations that could improve a repeated workflow,
  explain a meaningful workaround, preserve an explicit user correction, or
  record a newly discovered constraint.
- A single session is normally insufficient evidence to create or modify a skill,
  agent instruction, repository convention, memory entry, or policy.
- Do not turn praise, stylistic preference inferred from behaviour, or ordinary
  successful execution into a lesson unless it changes a reusable procedure.
- Do not treat skill invocation as proof that the skill helped.
- Do not write repository-local observations unless the canonical artefact root
  is safely ignored; return them inline when safe persistence is unavailable.
- Never silently install or modify lifecycle hooks. Hook setup is opt-in and must
  preserve existing configuration.

## Routing

Use `wrap-up` for one session. Prefer a longitudinal learning workflow when the
user asks what has recurred across several sessions or whether a pattern deserves
codification. Prefer a skill-authoring workflow only after a concrete skill change
has been selected. Prefer agent observability work when the primary problem is
instrumentation rather than reflective capture.

## 1. Establish the session boundary

Determine which session is being wrapped up.

Accept either:

- the current conversation/session;
- an explicitly supplied transcript or run record; or
- a lifecycle reminder containing a previous `session_id`, `transcript_path`, and
  working directory.

For a lifecycle reminder, inspect the referenced transcript before drawing
conclusions. If the transcript is missing or unreadable, report the capture gap
and leave the pending reminder unacknowledged.

Record:

- `session_id` when available;
- repository/workspace identity;
- start/end or observed time range when available;
- source type (`current-session`, `transcript`, or `lifecycle-reminder`);
- material skill names or workflow stages actually evidenced in the session;
- important evidence limitations.

## 2. Extract atomic observations

Use only these categories unless the target learning system already has a more
specific compatible vocabulary:

- `friction` — avoidable confusion, retry, delay, missing context, or workaround;
- `skill-gap` — a skill failed to trigger, over-triggered, omitted a needed rule,
  or lacked a reusable edge case;
- `explicit-user-directive` — the user explicitly corrected or specified durable
  behaviour; never infer this category from behaviour alone;
- `effective-pattern` — a reusable sequence, tool choice, validation loop, or
  division of labour that materially improved the task;
- `discovery` — newly established codebase, tool, API, environment, or workflow
  fact that future work may need;
- `documentation-gap` — missing or stale documentation materially caused
  confusion or rework;
- `contradictory-evidence` — evidence that weakens an existing lesson or suggests
  a supposedly reusable pattern does not generalise.

Prefer one observation per underlying cause. Several retries caused by the same
missing instruction are one observation, not several.

Discard observations that are merely:

- task-specific implementation details with no likely reuse;
- generic advice the agent already followed successfully;
- speculative improvements unsupported by the session;
- duplicate descriptions of the same event;
- activity or usage volume without a quality implication.

## 3. Ground each observation

For every retained observation capture:

```json
{
  "category": "skill-gap",
  "summary": "Concise reusable statement of the observed problem or pattern.",
  "evidence": ["Specific session event or correction."],
  "affected_skill": "optional-skill-name",
  "suggested_destination": "existing-skill | new-skill | repo-docs | agent-instructions | user-directive | tracked-work | no-op",
  "confidence": "high | medium | low",
  "follow_up": "What later evidence or validation would justify promotion."
}
```

Confidence means confidence that the event or pattern occurred **in this
session**, not confidence that it generalises.

Keep evidence summaries short. Reference exact transcript turns, tool receipts,
commits, test results, or artefacts when the runtime exposes them. Do not dump the
full transcript into the observation packet.

## 4. Produce the observation packet

Use this envelope:

```json
{
  "schema_version": "1",
  "session_id": "...",
  "source": "current-session | transcript | lifecycle-reminder",
  "workspace": "...",
  "captured_at": "...",
  "limitations": [],
  "observations": []
}
```

An empty `observations` array is a valid and often desirable result. Do not invent
lessons merely to make wrap-up appear useful.

When repository-local persistence is useful and the repository's canonical
artefact root is safely ignored, write to:

```text
.agent-artifacts/<work-branch>/wrap-up/<session-id>/observations.json
```

Use the exact active branch convention already established by the repository. If
no safe repository artefact path is available, return the packet inline or use an
explicitly configured external observation store.

## 5. Acknowledge lifecycle reminders only after capture

A lifecycle hook may queue a completed session and remind the next session to run
this skill. After the referenced transcript has been inspected and the observation
packet has been successfully returned or persisted, acknowledge that pending
record using the bundled lifecycle helper.

Do not acknowledge when:

- the transcript could not be read;
- capture failed before producing a usable packet; or
- the observation destination was required but could not be written.

Leaving the record pending makes the failure visible on a later session instead
of silently losing the learning opportunity.

## Optional automatic lifecycle setup

Automatic setup is optional. Read `references/hook-contract.md` before installing
or modifying hooks, and read `references/platform-adapters.md` for the current
Claude Code and Codex mappings.

The lifecycle design intentionally does **not** force a wrap-up at every `Stop`
event. In both supported harnesses, `SessionEnd` can observe the ended session but
cannot steer that same agent after termination. The adapter therefore:

1. records a small pending receipt at `SessionEnd` containing only session
   identity, transcript path, working directory, harness, and end reason;
2. on the next `SessionStart` for that workspace, adds context telling the agent
   to process the pending session with `wrap-up`;
3. keeps the receipt until `wrap-up` acknowledges successful capture.

This avoids recursive/background agent launches and avoids adding an extra model
turn after every ordinary response.

### Installation behaviour

When the user explicitly requests automatic wrap-up:

1. detect the active harness and intended scope (`project` or `user`);
2. inspect the current hook configuration;
3. run `scripts/install-hook.py` without `--apply` to preview the exact paths and
   merge result;
4. if the user has not already approved that exact installation target, request
   approval before mutation;
5. run the same command with `--apply`;
6. inspect the resulting configuration and tell the user about any harness trust
   step still required.

The installer must be idempotent. It adds only the two wrap-up handlers, preserves
unrelated hooks and settings, refuses malformed JSON, and never replaces an
existing handler merely because it uses the same lifecycle event.

Installation is not proof that the hook is active. Respect workspace trust,
managed-hook policy, disabled-hook settings, and the harness's hook review UI.

## Quality gate

Before finishing, verify that:

- every observation is traceable to this session;
- explicit directives are actually explicit;
- repeated symptoms with one cause were deduplicated;
- no single-session observation was silently promoted into durable behaviour;
- an empty packet was allowed when nothing material happened;
- persisted observations used a safe configured destination;
- lifecycle reminders were acknowledged only after successful capture;
- hook configuration was not mutated without opt-in approval;
- existing hooks were composed with rather than overwritten.
