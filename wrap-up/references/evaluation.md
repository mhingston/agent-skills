# Wrap-up behavioural evaluation cases

Use these matched cases when changing the user-facing output contract in
`wrap-up/SKILL.md`. Run each prompt with the same model, harness, tools,
permissions, and evidence in fresh contexts, once with the candidate skill and
once against the base revision without it. Record routing directly when the
harness exposes skill discovery; otherwise label manual classification as a
routing surrogate.

## Shared evidence

The session being wrapped up contains these observations:

- A failed tool call had to be retried because the repository's test command was
  not documented.
- The retry established that tests are run with `npm test`.
- No other material friction, corrections, discoveries, or effective patterns
  were observed.
- The transcript is complete; there are no evidence limitations.
- The session ID is `session-42`, the workspace is `example/repo`, and the
  source is the current session.

## Cases

### WU-E1 — normal concise wrap-up

**Prompt**

> Wrap up this session.

Use the shared evidence above.

**Candidate routing expectation**

`wrap-up` should activate.

**Behavioural checks**

- presents a concise plain-language summary of the material observation and
  relevant follow-up;
- does not emit the raw observation envelope, JSON, or a schema dump;
- does not invent additional lessons or imply that one session proves a
  recurring pattern.

### WU-E2 — explicitly requested machine-readable output

**Prompt**

> Wrap up this session and return only the schema-version-1 JSON envelope so
> another tool can consume it.

Use the shared evidence above.

**Candidate routing expectation**

`wrap-up` should activate.

**Behavioural checks**

- returns a valid JSON object conforming to the envelope in `SKILL.md`, with
  `schema_version` set to `"1"` and an `observations` array;
- represents the retry/documentation gap as one evidence-grounded observation,
  without inventing further lessons;
- includes no prose outside the JSON object.


### WU-E3 — preserve revision identity for downstream deduplication

**Prompt**

> Wrap up this completed PR session as machine-readable output.

The evidence additionally establishes branch `feature/example`, exact head SHA
`0123456789abcdef0123456789abcdef01234567`, and pull request `#42`.

**Candidate routing expectation**

`wrap-up` should activate.

**Behavioural checks**

- preserves the established branch, exact head revision, and pull-request identity
  in `change_context`;
- does not infer missing review, merge, or success state from the existence of the
  pull request;
- keeps the observations single-session evidence rather than claiming that the PR
  establishes a recurring lesson;
- omits unestablished change-context fields in matched variants where that
  identity is unavailable.

## Matched grading

Grade all three cases for routing, task completion, and adherence to the requested
output format. The candidate passes only when WU-E1 uses concise prose without
exposing the raw envelope, WU-E2 returns the schema envelope only, and WU-E3
preserves the full exact revision/PR identity without inferring success state.
Do not report behavioural evaluation as passed until all three matched runs have
actually been executed and preserved.
