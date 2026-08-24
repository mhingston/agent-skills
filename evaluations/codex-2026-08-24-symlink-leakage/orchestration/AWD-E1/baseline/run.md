# Run record

- Case: `AWD-E1`
- Condition: `baseline`
- Prompt: Design a durable review-and-remediation agent workflow. I need the state machine, authority boundaries, typed handoffs, retry semantics, resumability, independent verification, and failure recovery. Do not choose or implement an orchestration runtime yet.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `plan`
- Final response:

## Plan status: Conditional

The workflow design is runtime-neutral and ready to prototype. It remains conditional on three human-owned policy decisions: what constitutes an approval-required risk, who may accept residual risk, and the retention policy for prompts, evidence, and receipts.

Repository constraints used as governing evidence:

- `E1`: Evidence, explanation, automated checks, and policy thresholds are not approval or human judgment. [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-96t1q4u2/repo/README.md)
- `E2`: Review artifacts and verdicts bind to an exact revision.
- `E3`: Automation may enforce a recorded verdict but may not invent one.
- `E4`: Repository-local workflow artifacts belong under `.agent-artifacts/<branch>/<workflow>/<revision>/`, provided that location is safely ignored.

## 1. Outcome contract

The workflow accepts one immutable review target and produces either:

1. an independently verified, policy-compliant remediation result;
2. a human decision packet for unresolved risk or authority;
3. a durable blocked/cancelled/failure result that can be resumed or diagnosed without reconstructing hidden agent memory.

Requirements:

- `R1` — Deterministic orchestration owns state transitions; agents submit typed proposals and claims.
- `R2` — Reviewer, remediator, and verifier have distinct authority.
- `R3` — Every material artifact binds to the exact target revision and accepted contract.
- `R4` — Retries are bounded, classified, and idempotent.
- `R5` — Every externally visible transition is durably checkpointed and resumable.
- `R6` — No remediation is accepted from self-reported completion alone.
- `R7` — Approval, residual-risk acceptance, scope expansion, and contract changes remain human-owned.
- `R8` — Process death, stale work, duplicate delivery, ambiguous external effects, and verification regressions have explicit recovery paths.

Non-goals:

- Selecting an orchestration framework, queue, database, model vendor, or deployment topology.
- Letting agents approve, merge, deploy, revise requirements, or accept risk.
- Treating repeated model sampling as independent verification.
- Designing repository-specific review criteria before inspecting the target repository.

Core invariants:

- `I1`: One authoritative workflow record exists for each run.
- `I2`: Accepted evidence always names its target revision, contract version, producer identity, and provenance.
- `I3`: A changed revision invalidates all prior revision-sensitive review and verification results.
- `I4`: No actor reviews or verifies its own material output.
- `I5`: An effect is never repeated merely because its acknowledgement was lost.
- `I6`: Resumption rebuilds context from durable state; conversation history is never authoritative.
- `I7`: Terminal status does not imply approval unless a valid human verdict receipt exists.

## 2. Authority model

| Actor | May do | Must not do |
|---|---|---|
| Coordinator | Validate handoffs, apply transition rules, issue leases, enforce budgets, persist receipts | Interpret evidence as human approval; author remediation |
| Reviewer | Inspect the bound target; report falsifiable findings and coverage limits | Modify the target; accept risk; approve or merge |
| Triage/policy component | Deterministically classify findings using approved policy | Lower severity through model judgment; dismiss findings without evidence |
| Remediator | Modify only the accepted scope; run permitted checks; return evidence | Change the accepted contract; suppress findings; approve its own work |
| Independent verifier | Reproduce findings, inspect the remediation, run independent checks, report residual risk | Repair the work being verified; accept residual risk |
| Human owner | Approve scope or contract changes, waive/accept risk, resolve policy questions, cancel | Delegate accountability implicitly through silence |
| Effect executor | Perform separately authorized external effects and return receipts | Decide whether the effect is appropriate |
| Recovery operator | Break stale leases, reconcile ambiguous effects, resume or terminate runs | Alter historical receipts or fabricate completion evidence |

Separation must be based on execution identity and context isolation, not merely different prompts. At minimum, the verifier receives the original contract, review findings, resulting diff, and verification criteria—but not the remediator’s persuasive narrative as an authority source.

## 3. Authoritative state machine

```text
NEW
  → TARGET_BOUND
  → REVIEWING
  → REVIEW_READY
      ├─ no actionable findings → VERIFYING
      ├─ actionable findings    → REMEDIATION_PLANNED
      ├─ human decision needed  → AWAITING_DECISION
      └─ invalid target         → BLOCKED

REMEDIATION_PLANNED
  → REMEDIATING
  → REMEDIATION_READY
  → VERIFYING
      ├─ accepted                       → READY_FOR_HUMAN_VERDICT
      ├─ correctable findings remain    → REMEDIATION_PLANNED
      ├─ contract/scope conflict        → AWAITING_DECISION
      ├─ target became stale            → SUPERSEDED
      └─ retry/recovery exhausted       → BLOCKED

READY_FOR_HUMAN_VERDICT
  ├─ approved       → COMPLETED
  ├─ changes wanted → REMEDIATION_PLANNED
  ├─ rejected       → REJECTED
  └─ target changed → SUPERSEDED
```

Cross-cutting states:

- `PAUSED`: deliberately quiescent with no active lease.
- `RECOVERING`: reconciling a worker loss or uncertain effect.
- `CANCELLING`: cancellation requested; active work is being stopped.
- `CANCELLED`: terminal cancellation with retained evidence.
- `EXPIRED`: a wait, approval, or target-binding validity window elapsed.
- `BLOCKED`: cannot safely progress without new evidence, authority, or capability.
- `SUPERSEDED`: another target revision or decision replaced this run.
- `FAILED`: internal invariant or unrecoverable system failure—not an ordinary review rejection.

Every transition requires:

```text
expected_state + expected_workflow_version
actor_identity + actor_authority
command_id
validated input artifact references
transition result
durable event/receipt
```

Use compare-and-swap or equivalent optimistic concurrency. A worker never writes the next workflow state directly; it submits a handoff that the coordinator validates and applies.

## 4. Durable record model

```typescript
type WorkflowRecord = {
  workflowId: WorkflowId
  version: number
  state: WorkflowState
  target: TargetBinding
  contract: ContractSnapshot
  policyVersion: string
  instructionSetVersion: string
  activeLease?: Lease
  iteration: number
  budgets: BudgetState
  artifactRefs: ArtifactRef[]
  findingLedger: FindingRecord[]
  decisionRefs: DecisionReceipt[]
  effectRefs: EffectReceipt[]
  lastTransition: TransitionReceipt
  createdAt: Timestamp
  updatedAt: Timestamp
}
```

`TargetBinding` contains repository identity, base revision, exact reviewed revision, working-tree digest if applicable, and relevant dependency/configuration fingerprints.

Store large prompts, logs, diffs, and tool output as immutable artifacts referenced by digest. Keep only compact, redacted summaries in model context.

## 5. Typed handoffs

All handoffs share an envelope:

```typescript
type Handoff<TKind, TPayload> = {
  schemaVersion: string
  handoffId: UUID
  workflowId: WorkflowId
  kind: TKind
  producer: {
    role: Role
    executionId: string
    modelOrToolVersion?: string
  }
  target: TargetBinding
  contractVersion: string
  workflowVersionRead: number
  attempt: number
  createdAt: Timestamp
  payload: TPayload
  evidence: EvidenceRef[]
  uncertainty: Uncertainty[]
  contentDigest: Digest
}
```

Principal payloads:

```typescript
type ReviewReport = {
  coverage: ReviewCoverage
  findings: Finding[]
  checksRun: CheckResult[]
  limitations: Limitation[]
  recommendation: "verify_clean" | "remediate" | "human_decision" | "blocked"
}

type Finding = {
  findingId: StableId
  ruleOrRequirementRefs: string[]
  location: RevisionBoundLocation[]
  claim: string
  severity: Severity
  consequence: string
  reproduction?: Reproduction
  falsificationAttempts: EvidenceRef[]
  confidenceBasis: string
  remediationConstraint?: string
}

type RemediationTask = {
  taskId: StableId
  acceptedFindingIds: StableId[]
  allowedScope: ResourceScope
  forbiddenEffects: Capability[]
  requiredChecks: CheckSpecification[]
  completionContract: CompletionCriterion[]
}

type RemediationResult = {
  taskId: StableId
  resultRevision: RevisionId
  changeDigest: Digest
  findingDisposition: FindingDisposition[]
  checksRun: CheckResult[]
  residualConcerns: ResidualConcern[]
  effectReceipts: EffectReceipt[]
}

type VerificationReport = {
  verifiedRevision: RevisionId
  independence: IndependenceAttestation
  findingResults: VerifiedFindingResult[]
  regressionChecks: CheckResult[]
  policyChecks: CheckResult[]
  coverageGaps: Limitation[]
  verdict:
    | "accepted_technically"
    | "remediation_required"
    | "human_decision"
    | "blocked"
}
```

Semantic validation must reject:

- unknown finding dispositions;
- evidence tied to another revision;
- completion claims without required check results;
- widened scope;
- stale workflow versions;
- verifier/remediator identity overlap;
- missing or expired approval receipts;
- “fixed” findings whose original reproduction or independent oracle was not exercised.

Findings keep stable identities across iterations. They are closed only by verifier evidence, human disposition, or explicit supersession—not by omission from a later report.

## 6. Review/remediation loop

1. **Bind target and contract**  
   Freeze the exact revision, requirements, policy version, allowed scope, and human authority map.

2. **Independent review**  
   Reviewer submits findings with reproduction or falsification evidence and explicit coverage gaps.

3. **Deterministic intake**  
   Validate schema, revision binding, duplicates, policy routing, and whether human authority is required.

4. **Create remediation task**  
   Convert accepted findings into a bounded task. The coordinator does not let the remediator reinterpret or silently discard findings.

5. **Remediate**  
   Work under a lease against the bound base. Return a new revision plus check evidence and per-finding dispositions.

6. **Independent verification**  
   A separate execution identity reproduces original failures, tests the accepted contract, examines regressions, and challenges the claimed fix.

7. **Reconcile**  
   Deterministically compare the verifier report with the finding ledger and contract. Either close the technical loop, create another bounded iteration, or request a human decision.

8. **Human verdict**  
   Present unresolved material risks, coverage gaps, contract deviations, and exact-revision evidence. Record an explicit, expiring decision receipt.

## 7. Retry semantics

Classify before retrying:

| Failure class | Retry behavior |
|---|---|
| Transient infrastructure error | Retry the same operation with the same idempotency key, bounded backoff and jitter |
| Model output malformed | One schema-repair attempt using validation errors; then rerun the decision from the checkpoint |
| Invalid semantic proposal | Do not blindly retry; return validation evidence for one revised proposal |
| Policy denial or missing authority | Never retry automatically; route to human or block |
| Stale revision/workflow version | Discard result, rebind or supersede |
| Deterministic check failure | Return to remediation; not an infrastructure retry |
| No progress or repeated equivalent patch | Stop the loop and escalate/replan |
| External outcome unknown | Enter `RECOVERING`; reconcile by idempotency key or observed external state before any repeat |
| Worker loss | Let the lease expire, inspect receipts, then resume from the earliest safe transition |
| Human rejection | Terminal or a newly authorized remediation iteration; never an automatic retry |

Recommended default control rule: after two materially equivalent failed remediation strategies, stop retrying and produce a diagnostic/human-decision packet. Budgets should also cap total iterations, model/tool cost, wall-clock duration, and changed scope. Exact values are deployment policy, not agent choices.

Retries operate on the smallest safe unit. A failed verifier must not cause an already recorded remediation effect to run again.

## 8. Resumability and checkpoints

Checkpoint before:

- issuing a worker lease;
- invoking any consequential effect;
- waiting for a human, timer, or external system;
- changing target revision;
- entering or leaving verification;
- marking any terminal state.

On resume:

1. load the authoritative record;
2. validate its schema and transition history;
3. acquire a versioned lease;
4. re-read the target revision and contract;
5. invalidate stale approvals and revision-sensitive evidence;
6. reconcile effects in `requested`, `started`, or `outcome_unknown`;
7. reconstruct minimal context from immutable artifacts;
8. continue from the earliest safe state.

Lease records need an owner, issued time, expiry, heartbeat, workflow version, and cancellation token. Late results from expired leases are retained diagnostically but cannot advance state.

Pausing must leave no unrecorded effect in flight. If that cannot be established, pause becomes `RECOVERING`, not `PAUSED`.

## 9. Independent verification

Independence requires:

- a separate execution identity from the remediator;
- a fresh context projection;
- independent tool calls and check execution;
- original requirements and finding evidence as the oracle;
- no reliance on remediator-written expected outputs where an external or requirement-derived oracle exists;
- a distinct evaluator version where semantic evaluation is necessary.

Verification layers:

1. target and artifact digest validation;
2. schema and policy validation;
3. reproduction of each material finding;
4. focused contract and regression checks;
5. full repository gates appropriate to the change;
6. diff inspection for scope and unintended behavior;
7. injected failure/restart checks for workflow machinery;
8. human review only for policy, product meaning, usability, or risk acceptance.

A “clean” reviewer report still goes through verification: confirm review coverage and independently sample risk-bearing areas. Absence of findings is a claim, not proof.

## 10. Failure recovery matrix

| Failure point | Durable evidence | Recovery |
|---|---|---|
| Before worker invocation | transition and lease intent | Reissue after lease reconciliation |
| Worker running, process dies | lease plus any incremental artifacts | Expire lease; accept only complete digest-valid handoff |
| After patch created, before result recorded | revision/change digest | Discover by operation ID; validate and attach rather than recreate |
| Before external effect | requested receipt | Safe to invoke once |
| During external effect | started/outcome-unknown receipt | Query external system; do not repeat until reconciled |
| After effect, before acknowledgement | idempotency key and external receipt | Recover the existing result |
| Verifier dies | immutable remediation revision | Start a new independent verifier |
| Target changes | old/new target bindings | Mark run `SUPERSEDED`; start or rebind through human-authorized policy |
| Approval expires | decision receipt with expiry | Return to `AWAITING_DECISION` |
| State/history corruption | append-only transition receipts and artifact digests | Quarantine run; reconstruct only through an audited recovery operation |
| Retry budget exhausted | attempt ledger and no-progress evidence | `BLOCKED`, with diagnostic and proposed next decisions |

Never “repair” history in place. Recovery emits new events that explain the correction.

## 11. Required observability

Retain a correlated trajectory:

```text
workflow → iteration → transition → worker execution
         → model decision → tool/effect → evidence artifact
         → verification → human decision
```

Minimum operational signals:

- runs by state and age;
- stale leases;
- retries by failure class;
- no-progress and budget exhaustion;
- policy denials;
- revision-invalidated artifacts;
- ambiguous external effects;
- verification rejection rate;
- reopened findings;
- human wait duration;
- cost and token consumption;
- recovery outcomes.

Prompts and raw tool results should be retained only according to an explicit privacy policy. Auditability does not justify indefinite retention of secrets or personal data.

## 12. Human decision gates

- `D1 — Risk policy`: Which severities, data classes, and change categories require explicit human disposition? Owner: engineering/security governance.
- `D2 — Residual-risk authority`: Which role may accept each class of remaining risk? Owner: accountable delivery leadership.
- `D3 — Retention`: What artifacts may be retained, redacted, encrypted, or deleted, and for how long? Owner: security/privacy.
- `D4 — External effects`: Which operations require approval immediately before invocation? Owner: system/resource owners.

These gates block policy configuration, not the runtime-neutral state-machine and schema design.

## 13. Verification map

| Requirement | Required evidence |
|---|---|
| `R1` | Transition-table tests reject invalid actor/state/action combinations |
| `R2` | Identity-overlap and capability-denial tests |
| `R3` | Stale-revision, digest-mismatch, and supersession tests |
| `R4` | Duplicate delivery, bounded retry, oscillation, and budget tests |
| `R5` | Process termination injected before/after each transition and effect |
| `R6` | Self-reported completion rejected without independent evidence |
| `R7` | Missing, rejected, amended, expired, and superseded approval tests |
| `R8` | Worker-loss, late-result, uncertain-effect, corrupted-artifact, cancel, and recovery tests |
| `I1–I7` | Property-based state-machine tests over generated event sequences |

The strongest acceptance test is replay: given the retained workflow record and immutable artifacts, an independent process must reconstruct why every transition occurred, which authority permitted it, which revision it concerned, and whether repeating any outstanding operation is safe.

## Handoff

The next authorized step should be a runtime-neutral specification package containing:

- versioned state and event schemas;
- transition and authority tables;
- JSON Schema or equivalent handoff contracts;
- retry/error taxonomy;
- recovery decision table;
- conformance scenarios and property-based state-machine model;
- policy placeholders for `D1–D4`.

Only after those contracts pass implementation-independent conformance review should an orchestration runtime be evaluated.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
