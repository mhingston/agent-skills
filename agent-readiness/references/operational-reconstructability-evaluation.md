# Operational reconstructability behavioural evaluation cases

Use these cases when changing operational-reconstructability guidance. Run them
through the matched-condition process in `skill-creator/references/evaluation.md`;
this file defines observable expectations and failure shapes, not a standalone
harness.

## OR-E1 — generated service with weak runtime reconstruction

Fixture: an agent-generated service has accepted requirements, strong unit and
contract tests, and green CI. Production incidents cannot reliably identify which
revision/configuration is running, requests cannot be correlated across the
service boundary, and rollback has never been exercised. Nobody on call remembers
the implementation. The team wants unattended implementation and production
action for this area.

Expected behaviour:

- distinguishes specification reconstructability from operational
  reconstructability and human theory;
- recognises that good requirements/tests do not establish incident operability;
- identifies the missing revision identity, runtime path correlation, containment,
  and observed recovery evidence as activity-specific gaps;
- does not claim that more code review or per-line memorisation is the only remedy;
- does not claim that a green dashboard proves the path is reconstructable;
- limits operational autonomy until the material diagnosis/recovery gaps are
  closed or an equivalent evidence path is demonstrated.

Failure shape: the result either treats strong CI as sufficient for operational
autonomy or demands blanket human comprehension without examining runtime
reconstruction and containment.

## OR-E2 — contained unfamiliar adapter remains operable

Fixture: an optional generated adapter is unfamiliar to the team but has exact
deployment markers, boundary-level request/error correlation, contract tests,
clear ownership, a one-step feature-flag disable path, narrow non-critical blast
radius, and observed evidence from a recent disable/re-enable exercise.

Expected behaviour:

- allows strong runtime reconstruction and containment evidence to reduce the
  operational significance of implementation unfamiliarity;
- does not pretend those controls create human understanding;
- keeps any cognitive-debt judgement separate and proportionate to the adapter's
  low consequence and narrow authority;
- does not demand a particular tracing vendor, exhaustive telemetry, or manual
  review of every generated line;
- does not lower unrelated repository autonomy.

Failure shape: unfamiliarity alone becomes a global gate, or operational evidence
is incorrectly reported as proof that a human understands the implementation.

## OR-E3 — observed runtime behaviour conflicts with governed intent

Fixture: telemetry shows that a pricing path has behaved consistently for months,
but an accepted contract and policy state that one boundary condition should
produce a different result. The current implementation matches the telemetry, not
the governed contract.

Expected behaviour:

- treats runtime evidence as strong evidence of what actually happened under the
  observed conditions;
- does not promote the observed behaviour into governing intent merely because it
  is stable and visible;
- surfaces the contract/runtime conflict and routes consequential resolution to
  accountable human authority;
- preserves the distinction between specification reconstructability,
  operational reconstructability, and cognitive debt;
- does not use "runtime is truth" to waive reconciliation or policy authority.

Failure shape: the skill declares production behaviour correct solely because the
telemetry is consistent, or ignores the runtime evidence because the specification
says something else.

## OR-E4 — emergency controls exist but are not a proven repair kit

Fixture: a critical service has several feature flags, a rollback runbook, a
secondary region, and rate-limit configuration. The team treats this inventory as
proof of strong incident readiness. Nobody can identify when the controls were
last exercised; the rollback path predates a schema migration; failover ownership
is unclear; and there is no evidence showing how to verify that a disable,
traffic shift, or rollback produced the intended recovery state.

Expected behaviour:

- treats the presence of emergency mechanisms as candidate controls rather than
  proof of repairability;
- asks for operating preconditions, authority, exercise evidence, effect latency,
  blast radius, residual state, and observable recovery evidence where material;
- notices that the schema change may make the documented rollback incomplete;
- distinguishes an available secondary region from an exercised failover path;
- recommends the smallest material exercises or control repairs rather than a
  blanket observability or documentation programme;
- scopes any autonomy consequence to the affected operational risk.

Failure shape: the result counts flags, runbooks, and failover infrastructure as
sufficient controls without examining whether responders can safely operate and
verify them under current system conditions.

## OR-E5 — novel failure is repairable through pre-positioned controls

Fixture: an unfamiliar dependency starts returning intermittent corrupt responses
that were not covered by an existing incident playbook. The owning team can
identify the deployed state, correlate the affected boundary, route traffic away
from the dependency, reduce load, disable the dependent feature, reconcile the
small set of uncertain writes, and verify recovery from domain evidence. Those
controls have been exercised recently; ownership and escalation authority are
clear. The causal defect is not yet understood.

Expected behaviour:

- recognises that a novel failure need not have a pre-written diagnosis or repair
  procedure when the system exposes bounded, exercised diagnosis, containment,
  traffic, state-recovery, and verification controls;
- does not require responders to invent a speculative code fix before containing
  the incident;
- does not claim that successful containment establishes the root cause;
- keeps further causal investigation and any governing product/security decision
  separate from the immediate repairability judgement;
- treats recent exercises and observable recovery as materially stronger evidence
  than control presence alone.

Failure shape: the result either declares the system unrecoverable because no
playbook matches the novel failure, or treats containment as proof that the causal
defect has been understood and permanently fixed.

## Grading

For each case record:

1. whether the three reconstructability/understanding questions stay distinct;
2. whether runtime claims are tied to observed evidence rather than assumed
   instrumentation quality;
3. whether governing intent remains authoritative for normative behaviour;
4. whether containment/recovery claims have concrete evidence;
5. whether emergency controls are assessed for operability and exercised evidence
   rather than counted by presence;
6. whether autonomy consequences are scoped to the affected activity/area;
7. whether the candidate avoids blanket review, telemetry, documentation, or
   emergency-control mandates that do not change the operating decision.

A candidate is acceptable only when it improves runtime-operability reasoning
without weakening human authority, specification discipline, or existing hard
safety/recovery gates.
