# Runtime agent validation reference

Read this reference only when an ontology or semantic model is intended to
validate or govern proposed tool calls, intermediate results, or resulting state
inside a live agent workflow.

The ontology supplies governed meaning and logical consequences. It does not
execute tools, grant authority, enforce transactions, or make side effects safe
by itself. Enforcement occurs only when an authoritative runtime boundary
consumes validation results and fails closed where required.

## Keep validation and enforcement layers distinct

Do not treat all checks as equivalent:

1. **Structural validation** — validate tool names, required fields, datatypes,
   serialisation, and protocol shape with typed contracts such as JSON Schema,
   OpenAPI, Protobuf, Pydantic, Zod, or equivalent mechanisms.
2. **Ontology reasoning** — derive classifications, relationships,
   equivalences, incompatibilities, and other logical consequences from accepted
   assertions and axioms. RDFS and OWL normally use open-world semantics.
3. **Operational semantic validation** — check required properties, datatypes,
   cardinalities, closed value sets, relationship shapes, and cross-property
   conditions with SHACL or an equivalent validation mechanism.
4. **Policy and authority enforcement** — determine whether the actor may
   perform the action under current permissions, approvals, and mutable policy
   through an authoritative policy boundary.
5. **Transactional enforcement** — protect uniqueness, idempotency,
   concurrency, balances, and irreversible state transitions at the application,
   database, ledger, or side-effecting tool boundary.
6. **Postcondition verification** — read authoritative resulting state and
   compare observed effects with the accepted proposal and expected effects.

An ontology may explain why a proposal or result conflicts with governed domain
meaning. It must not be assumed to prevent the action unless the runtime boundary
uses that result to block execution.

## Use a proposal–validate–commit–verify workflow

For every side-effecting action governed by semantic checks:

1. **Propose** — produce a typed action proposal without performing irreversible
   effects.
2. **Validate structure** — validate tool identity, parameters, types, required
   fields, and protocol shape.
3. **Resolve semantic context** — resolve referenced entities, source identities,
   current state, evidence revisions, and applicable ontology, mapping, rule, and
   policy versions.
4. **Evaluate meaning** — run required inference, SHACL or equivalent constraints,
   and expected-effect checks.
5. **Evaluate authority** — check permissions, approval requirements, policy,
   risk, and reversibility through the designated enforcement boundary.
6. **Commit** — execute the action only after every mandatory gate passes. Prefer
   dry-run, staged, idempotent, or reversible mechanisms where available.
7. **Verify** — read back authoritative state and validate actual effects against
   expected postconditions.
8. **Contain or escalate** — when verification fails, stop dependent work and
   invoke the defined rollback, compensation, containment, or human-escalation
   path.

Do not execute first and use ontology validation only as retrospective logging.
Do not require all agents to be side-effect free; instead separate proposal from
execution and place material effects behind explicit validation and authority
gates.

## Pin the runtime context

A validation result is meaningful only for the exact context evaluated. Record:

- action and proposal identifier;
- actor or agent identity and delegated authority;
- tool and tool-schema version;
- ontology or vocabulary version;
- SHACL or constraint-set version;
- semantic conversion and identifier-mapping rule versions;
- policy version and approval state;
- source and current-state revisions or observation times;
- validator implementations and versions;
- risk level, reversibility, and required gates.

Mark the result stale and revalidate when any pinned input changes before commit.
Do not combine validation evidence from different revisions.

## Return an explicit validation outcome

Use a runtime-validation status distinct from assertion status, competency-test
status, or publication-readiness status:

- `pass` — every mandatory check ran and passed for the pinned context;
- `reject` — one or more applicable rules were violated;
- `indeterminate` — required identity, evidence, state, or meaning could not be
  resolved sufficiently;
- `unavailable` — a mandatory validator or authoritative enforcement boundary
  could not run.

A result should identify:

```yaml
validation_result:
  proposal_id: ACT-001
  status: indeterminate
  risk: high
  pinned_context:
    source_revision: <sha>
    ontology_version: <version>
    constraint_version: <version>
    mapping_rule_versions: [MAP-001@2]
    policy_version: <version>
    tool_schema_version: <version>
  checks:
    structural: pass
    semantic_reasoning: pass
    operational_constraints: indeterminate
    authority: not-run
    transactional_preconditions: not-run
  violations: []
  unresolved:
    - Customer identity cannot be reconciled with the payment recipient.
  evidence: []
  retryable: false
  required_next_action: human-review
```

Do not collapse missing evidence into `reject`, and do not convert
`indeterminate` into `pass` through model confidence.

## Fail closed proportionately

Apply the policy selected for the action's risk and reversibility:

- any `reject` from a mandatory gate blocks execution;
- `indeterminate` or `unavailable` blocks irreversible, externally visible,
  security-sensitive, financially material, compliance-relevant, or otherwise
  high-risk actions;
- a low-risk fallback is allowed only when an explicit current policy permits it,
  defines the degraded behaviour, and records the exception;
- missing authority never degrades to inferred authority;
- human approval supplements but does not silently replace mandatory technical or
  transactional controls.

When no risk policy exists, treat mandatory `indeterminate` and `unavailable`
results as blocking.

## Model expected and observed effects separately

A valid proposal does not prove successful execution. Record:

- preconditions evaluated before commit;
- expected effects and invariants;
- authoritative observations after execution;
- postcondition checks;
- partial, delayed, duplicate, or unexpected effects;
- rollback, compensation, containment, and escalation outcomes.

Example:

```yaml
action_validation:
  proposal_id: ACT-REFUND-001
  action: IssueRefund
  proposal:
    order: order.123
    amount: 25.00
    currency: GBP
    recipient: customer.456
  preconditions:
    - order is refundable
    - no accepted refund already covers this amount
    - recipient is the entitled customer
  expected_effects:
    - refund.refersTo = order.123
    - refund.recipient = customer.456
    - order.refundedAmount increases by 25.00
  observed_effects: []
  validation:
    structural: pass
    semantic_reasoning: pass
    operational_constraints: pass
    authority: pass
    transactional_preconditions: pass
    postconditions: not-run
```

Use the authoritative application or ledger to enforce duplicate-refund,
uniqueness, balance, and idempotency rules. Do not model those guarantees as OWL
reasoning alone.

## Respect open-world reasoning behaviour

Do not interpret ontology inference as closed-world validation:

- absence of a fact normally means unknown, not false;
- an OWL functional property may cause two values to be inferred as the same
  individual instead of being rejected as duplicates;
- disjointness may make assertions inconsistent but does not itself prevent a
  tool call;
- domain and range axioms can infer unexpected class membership;
- transitive and bridge properties can propagate relationships beyond the
  directly asserted scope.

For every identity-sensitive, functional, inverse-functional, disjoint,
transitive, or bridge axiom, probe for:

- unintended `sameAs` or identity merging;
- unexpected class membership through domain or range;
- cross-domain relationship propagation;
- inferred ownership, authority, or eligibility;
- contradictions hidden by incomplete evidence;
- cardinality restrictions resolved through identity collapse.

Use SHACL, schemas, application checks, or transactional controls when the
requirement is to reject invalid operational data rather than derive logical
consequences.

## Control repair and retry loops

When validation fails and an agent is allowed to revise the proposal:

- return the specific violated rule, unresolved evidence, and source authority;
- provide only the information needed to produce a corrected proposal;
- preserve each proposal and result for comparison and audit;
- set explicit attempt, token, time, and cost budgets;
- detect materially equivalent repeated proposals, not only identical text;
- prevent the agent from weakening, removing, bypassing, or reinterpreting the
  validator or policy;
- stop immediately when required evidence, authority, or enforcement capability
  is unavailable;
- escalate when the same violation recurs, the budget is exhausted, or correction
  requires a canonical semantic or policy decision.

A failed validation is not permission to search indefinitely for a technically
passing representation that defeats the rule's intent.

Use a state model equivalent to:

```text
PROPOSED
  -> STRUCTURALLY_INVALID -> REVISE | STOP
  -> SEMANTICALLY_INVALID -> REVISE | ESCALATE
  -> INDETERMINATE -> GATHER_EVIDENCE | ESCALATE | STOP
  -> UNAUTHORISED -> STOP
  -> VALIDATED -> COMMIT
  -> COMMITTED -> VERIFY
  -> POSTCONDITION_FAILED -> CONTAIN | ROLLBACK | ESCALATE
  -> VERIFIED
```

Persist the current state, attempt count, budgets, pinned context, and validator
results. Do not treat workflow state as evidence that the action is valid.

## Test the complete enforcement path

Test more than the ontology or validator in isolation:

- valid, invalid, missing, disputed, and stale inputs;
- unknown and aliased identities;
- duplicate and concurrent proposals;
- actions that become stale between validation and commit;
- validator and policy-service unavailability;
- attempts to bypass or weaken checks;
- authority changes during the loop;
- partial and delayed side effects;
- rollback and compensation failures;
- repeated semantically equivalent proposals;
- unintended reasoner inferences;
- human escalation and resumption.

For each test, verify the actual enforcement boundary blocks, permits, or
escalates as specified. A validator returning `reject` is not sufficient evidence
if the tool can still execute.

## Stop conditions

Stop or escalate when:

- the action cannot be separated into proposal and controlled execution;
- a mandatory structural, semantic, policy, or transactional check cannot run;
- source identity, current state, or authority cannot be resolved;
- the runtime cannot pin and preserve the evaluated context;
- the side-effecting boundary cannot consume and enforce the validation result;
- postconditions cannot be observed for a material action;
- rollback, compensation, or containment is required but unavailable;
- the repair loop exceeds its defined budget;
- passing validation would require weakening canonical semantics or policy.

Report the smallest missing enforcement capability, evidence item, authority
decision, or source correction needed to resume.