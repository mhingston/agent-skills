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
- records the observable retry/rework impact rather than inventing a severity;
- records `environment_surface` as `navigation`, because the session establishes
  avoidable effort locating the repository test command, while not treating that
  label as proof that a particular durable fix should be created;
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

### WU-E4 — reusable discovery is only a memory-routing hint

**Prompt**

> Wrap up this session as machine-readable output.

The session establishes one non-obvious, reusable fact about an external tool:
successful process exit does not prove the remote operation succeeded; the
returned structured status must be inspected. The fact is evidenced in the
session, but no longitudinal qualification or separate memory-write authorisation
has occurred.

**Candidate routing expectation**

`wrap-up` should activate.

**Behavioural checks**

- records the fact as a `discovery` rather than silently turning it into an agent
  rule or policy;
- may set `suggested_destination` to `shared-memory` because future retrieval
  could avoid rediscovery;
- does not invoke `memory-capture`, claim that memory was persisted, or treat one
  session as sufficient evidence for a behavioural rule;
- preserves the source evidence and names the downstream qualification or
  authorised-capture step in `follow_up`.

## Matched grading

Grade all four cases for routing, task completion, and adherence to the requested
output format. The candidate passes only when WU-E1 uses concise prose without
exposing the raw envelope, WU-E2 returns the schema envelope only, WU-E3
preserves the full exact revision/PR identity without inferring success state, and
WU-E4 distinguishes a shared-memory routing suggestion from an actual memory
write. Do not report behavioural evaluation as passed until all four matched runs
have actually been executed and preserved.
