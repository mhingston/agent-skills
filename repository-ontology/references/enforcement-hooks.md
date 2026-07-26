# Optional repository enforcement hooks

Read this reference only when an accepted repository ontology or typed concept
model will be operationalised to detect semantic drift or gate code changes.
The bundled scripts are optional companion tooling; they are not required for
ordinary assessment, establishment, evolution, or formal validation.

## Preconditions

Do not create blocking hooks until all of these are true:

1. A named consumer and concrete enforcement use case exist.
2. The relevant concepts, identifiers, relationships, and source mappings are
   accepted and versioned.
3. Each blocking rule is backed by a `confirmed` assertion or authoritative
   source, not model confidence or observed frequency.
4. A deterministic extractor can observe the required repository facts.
5. A human or governance owner can review rules, decisions, baselines, and
   waivers.
6. The actual Git, CI, or agent-completion boundary can consume the result and
   fail closed where required.

If these conditions are absent, report candidate tensions or semantic gaps
instead of introducing enforcement.

## Keep ontology, constraints, and enforcement distinct

Maintain separate artefacts for:

- the ontology or meaning model;
- repository-to-semantic mappings and extractor configuration;
- executable closed-world constraints;
- mutable decisions and waivers;
- observed repository facts;
- hook reports and baselines;
- the Git or CI boundary that enforces exit codes.

The ontology explains governed meaning. The constraint profile states which
closed checks are executable. The guard evaluates them. The surrounding hook or
CI job blocks the change.

Do not embed volatile extraction logic as timeless ontology truth. Do not hide
blocking interpretation inside a prompt.

## Classify every proposed check

Before implementing a hook, classify it as one of:

- **structural validation** — malformed profile, duplicate IDs, dangling
  references, or invalid rule shape;
- **ontology reasoning** — derived classification or semantic consequence;
- **operational semantic constraint** — closed relationship, mapping, value, or
  cardinality requirement;
- **architectural or organisational policy** — mutable allowed or forbidden
  dependency and ownership rules;
- **transactional invariant** — uniqueness, concurrency, balance, or state
  transition enforced by the application or database;
- **advisory heuristic** — an uncertain signal requiring investigation.

Use the least powerful authoritative mechanism that satisfies the requirement.
The bundled guard is suitable for structural checks, bounded repository
relationships, mappings, and decision pairing. It is not a substitute for
runtime policy services, databases, compilers, or transaction boundaries.

## Blocking eligibility

A finding may block only when:

- the rule uses an implemented deterministic rule kind;
- its assertion status is `confirmed`;
- `enforcement` is explicitly `block`;
- all mandatory extractor inputs and pinned context are available;
- the rule owner has accepted its false-positive and maintenance cost;
- the finding is not covered by a valid exact baseline entry or waiver.

Treat statuses as follows:

| Assertion status | Hook treatment |
| --- | --- |
| `confirmed` | May block when an explicit executable rule says so. |
| `observed` | Advisory unless independently confirmed as an operational contract. |
| `inferred` | Advisory only. |
| `disputed` | Advisory and escalate for resolution. |
| `deprecated` | Normally advisory; block only through a separate confirmed prohibition. |

A profile that marks an unconfirmed rule as blocking is structurally invalid.
This prevents generated or inferred assertions from silently becoming policy.

## Hook classes

Use distinct hook purposes rather than one opaque semantic score:

### Structural

Block on invalid operational artefacts, including duplicate semantic IDs,
unsupported rule kinds, malformed status values, duplicate project mappings,
or missing required rule fields.

### Conformance

Evaluate observed repository relationships and mappings against confirmed
constraints. Examples include forbidden project dependencies, required event
relationships, or governed files with no unique component mapping.

### Semantic decision

Compare the current constraint profile with a known base revision. Require an
accepted decision for material component or rule additions, removals, and
semantic modifications.

### Tension

Report uncertain or incomplete observations without blocking: unmapped external
project references, ambiguous source identities, possible vocabulary drift, or
unsupported extractor scope.

A combined hook blocks only on mandatory structural, conformance, or decision
findings. Advisory tensions remain visible in the same report.

## Proposal–validate–commit use

For a code change governed by hooks:

1. **Propose** the code and any explicit ontology, mapping, decision, or waiver
   changes.
2. **Pin context** to the profile version, source revision, extractor version,
   base revision, and relevant policy artefacts.
3. **Extract observations** deterministically from the repository.
4. **Validate structure** before evaluating semantic rules.
5. **Evaluate constraints** and separate blocking results from advisory findings.
6. **Enforce at the boundary** by consuming the exit code in pre-commit,
   pre-push, CI, or an agent completion gate.
7. **Remediate or escalate** without weakening the validator or inventing
   authority.
8. **Preserve the report** when it is material to review or audit.

Re-run validation when any pinned input changes.

## Brownfield adoption

Do not make an established repository unusable by blocking every historical
violation immediately. Use an exact-finding ratchet:

- record reviewed existing finding fingerprints at an exact ontology version;
- keep baseline findings visible but non-blocking;
- block new, changed, or expanded violations;
- refuse stale baselines after the ontology version changes;
- remove baseline entries when the underlying violation is repaired.

A baseline acknowledges existing debt. It does not confirm that the violating
relationship is semantically correct.

## Decisions and waivers

Keep permanent semantic evolution and temporary exceptions distinct.

An accepted decision should identify:

- a stable decision ID and status;
- affected semantic IDs;
- covered change kinds;
- rationale, owner, and review evidence outside the guard when required.

A waiver should identify:

- one exact finding fingerprint;
- a reason;
- an approver;
- an expiry date;
- a related decision or remediation plan when available.

Do not use inline comments, broad path bypasses, model-generated approvals, or
non-expiring wildcard waivers as escape hatches.

## Outcomes and exit semantics

Keep runtime-validation status distinct from assertion status:

- `pass` — no mandatory blocking finding remains;
- `reject` — a mandatory rule was violated;
- `indeterminate` — required identity, evidence, or comparison context was
  insufficient;
- `unavailable` — a mandatory extractor or source could not run.

Recommended process exits:

- `0` for `pass`, even when advisory findings exist;
- `1` for blocking `reject`, `indeterminate`, or `unavailable`;
- `2` for invalid invocation or unreadable required configuration.

Do not convert `indeterminate` into `pass` using model confidence.

## Agent behaviour

An agent may:

- run the guard;
- inspect evidence and finding fingerprints;
- repair code or mappings;
- propose an ontology evolution or decision;
- request an authorised, time-bounded waiver;
- explain unresolved tensions.

An agent must not:

- mark its own inference as confirmed;
- weaken, remove, or reinterpret a blocking rule merely to pass;
- generate an approval or waiver on behalf of a human;
- edit the baseline to absorb a new violation without explicit review;
- claim enforcement succeeded when the authoritative boundary did not run.

## Output when hooks are requested

Return only the operational artefacts required by the named boundary:

1. the accepted ontology version and source revision;
2. the bounded consumer and enforcement boundary;
3. the executable constraint profile and schema version;
4. extractor identities, versions, inputs, and unavailable coverage;
5. blocking and advisory rule classifications with owners and evidence;
6. semantic-decision, baseline, and waiver paths and governance;
7. the exact local, CI, or agent-completion command;
8. validation results, fixtures, and remaining limitations;
9. the smallest next increment rather than speculative additional rules.

Do not make hook artefacts part of the ordinary repository-ontology output when
operational enforcement was not requested or warranted.

## Stop conditions

Stop or remain advisory when:

- the repository fact cannot be extracted deterministically;
- source identity or authority is unresolved;
- the accepted model does not define the required relationship precisely;
- blocking would depend on natural-language interpretation by an LLM;
- no owner can maintain the rule;
- the boundary cannot consume and enforce the result;
- a transaction or runtime invariant belongs in an application or database;
- passing would require weakening confirmed semantics or inventing authority.

Report the smallest missing model decision, source correction, extractor,
review, or enforcement capability needed to proceed.

## Bundled implementation

The optional standard-library Python implementation is documented in
[`../README.md`](../README.md) and lives at
[`../scripts/ontology-guard.py`](../scripts/ontology-guard.py). Its current
closed rule kinds and wire contracts are defined by the JSON schemas under
`../assets/`.
