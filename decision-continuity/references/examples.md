# Decision Continuity Examples

Use these examples to calibrate classification and boundaries. They are not
templates to copy without inspecting the actual workstream.

## Example 1: Unsupported reopening in an orchestration handoff

### Prior evidence

An approved design record states:

- use agents and agent skills as the primary primitives;
- use SQLite for durable task, run, lease, and event state;
- do not add harness adapters;
- do not manage Git workspaces;
- do not introduce a Go service merely because an earlier prototype used Go.

### Current proposal

A new handoff proposes a Go coordinator service with harness-driver interfaces
and workspace lifecycle management. It gives no new operational evidence.

### Expected reconciliation

```yaml
continuity_status: conflicting
proposal_reconciliation:
  - proposal: Add a Go coordinator service.
    classification: unsupported-reopening
    related_decisions:
      - DEC-ORCH-003
    required_action: Remove the component or present materially new evidence for explicit reconsideration.
  - proposal: Add harness-driver interfaces.
    classification: contradiction
    related_decisions:
      - DEC-ORCH-004
    required_action: Preserve the accepted no-adapter boundary.
  - proposal: Manage Git workspaces.
    classification: scope-extension
    related_decisions:
      - DEC-ORCH-005
    required_action: Exclude from the handoff.
```

The skill must not redesign the system. It identifies the drift and returns a
continuation packet that preserves the accepted primitives.

## Example 2: Compatible refinement of ontology enforcement

### Prior evidence

The accepted direction keeps deterministic enforcement tooling optional and
self-contained beside the repository-ontology skill. The canonical `SKILL.md`
does not need to change merely to advertise the optional tooling.

### Current proposal

Add another deterministic extractor inside the existing enforcement package and
extend its tests. Leave the canonical skill unchanged.

### Expected reconciliation

- Additional extractor: `compatible-refinement`.
- Canonical skill change: not proposed.
- Existing responsibility boundary: preserved.
- Continuity status: `aligned`.

A proposal to edit `SKILL.md` only for discoverability would be an
`unsupported-reopening` unless new evidence showed that users could not find or
operate the optional package through its existing README.

## Example 3: Valid re-entry for a deferred router dimension

### Prior evidence

The first router version deliberately supports two classification dimensions.
Additional dimensions are deferred until representative evaluation data shows
that they improve routing decisions enough to justify greater complexity.

### New evidence

A labelled evaluation set now shows a repeated failure mode that the two
dimensions cannot separate. A third dimension reduces the measured error on a
held-out set and has a defined consumer in the routing policy.

### Expected reconciliation

- Re-entry condition: satisfied.
- Third dimension: `supersession-proposed` or `new-decision-required`, depending
  on the original record.
- Existing first-version decision: remains accepted until the accountable human
  approves the change.
- Downstream revalidation: classifier schema, training data, router contract,
  thresholds, telemetry, and evaluation fixtures.

## Example 4: Implementation differs from the decision record

### Prior evidence

An ADR says retries are disabled for a non-idempotent operation.

### Current repository

The implementation retries the operation three times.

### Expected reconciliation

The code is evidence of current behaviour, not evidence that the ADR was
superseded. Report a conflict between recorded direction and implementation.
Require investigation of change history and accountable intent before deciding
whether to fix the code or supersede the ADR.
