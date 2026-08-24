# Run record

- Case: `AWD-E1`
- Condition: `baseline`
- Prompt: Design a durable review-and-remediation agent workflow. I need the state machine, authority boundaries, typed handoffs, retry semantics, resumability, independent verification, and failure recovery. Do not choose or implement an orchestration runtime yet.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `plan, agent-workflow-design`
- Agent-reported selection (not a native harness event): `none`
- Final response:

**Plan Status**
Ready. The workflow can be specified independently of any orchestration runtime.

**Outcome Contract**
`R1` Define a durable review-and-remediation agent workflow that can:
- review a bounded target artifact or change,
- produce a typed assessment,
- request or perform remediation,
- independently verify the result,
- resume after interruption without duplicating work,
- fail safely when authority is missing or evidence is insufficient.

`R2` Preserve strict authority boundaries:
- agents can recommend, transform, and verify only within their delegated scope,
- human approval is required for consequential decisions,
- no agent may silently upgrade its own authority,
- review evidence is not approval and verification is not policy acceptance.

`R3` Use typed handoffs between stages so each stage receives only the minimum required facts, identifiers, and constraints.

`R4` Support retry, pause/resume, and partial recovery without losing provenance or re-running completed work blindly.

`R5` Require independent verification before declaring remediation complete.

`R6` Provide explicit failure recovery paths for:
- missing context,
- rejected remediation,
- verification failure,
- conflicting evidence,
- interrupted execution,
- expired or superseded instructions.

Non-goals:
- choosing a runtime,
- implementing code,
- defining repo-specific file formats beyond the workflow contract,
- making policy decisions that belong to humans.

**Current-State Evidence**
- `E1` [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-n9_uihky/repo/README.md) defines this repository as a catalogue of reusable Agent Skills and orchestrating agent definitions, which means a workflow design should be portable and not runtime-tied.
- `E2` [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-n9_uihky/repo/README.md) explicitly distinguishes public skills from workflow-internal modules and states that internal modules fail closed without exact orchestration context.
- `E3` [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-n9_uihky/repo/README.md) states that evidence is not approval, explanation is not proof, and model-generated rationale is not human judgement.
- `E4` [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-n9_uihky/repo/README.md) lists adjacent capabilities for review, implementation, decision continuity, and observability, which implies the workflow should separate those responsibilities rather than merge them.

No repo-local `agent-workflow-design/SKILL.md` file was present at the checked path, so I’m treating that capability as unavailable evidence rather than assuming its details.

**Approach and Decisions**
The design should use a small deterministic state machine with bounded model judgement inside specific states, not as the controller of the whole process.

Selected design:
- one workflow instance represents one bounded target, one revision stream, and one authority context,
- state transitions are explicit and serializable,
- all stage outputs are typed envelopes with provenance,
- remediation and verification are separate roles,
- restart resumes from the last committed state, not from conversational memory.

Decision boundaries:
- `D1` Human-owned acceptance is required whenever remediation changes public behavior, security posture, data shape, or rollback characteristics.
- `D2` Independent verification is mandatory for completion, and must not reuse the same reasoning path that generated the remediation.
- `D3` If instructions conflict or authority is ambiguous, the workflow blocks and surfaces the conflict instead of guessing.

Responsibility/interface map:
- `Coordinator`: owns the state machine, persistence, idempotency, and transition guards; consumes typed task envelopes; produces next-state envelopes and execution receipts.
- `Reviewer`: owns defect finding, constraint extraction, and remediation recommendation; consumes target evidence and policy context; produces review findings, confidence, and remediation scope.
- `Remediator`: owns bounded changes inside delegated scope; consumes approved or allowed remediation intent; produces a change proposal or applied patch summary.
- `Verifier`: owns independent checks and falsification; consumes the change summary plus original requirements; produces pass/fail evidence and residual-risk notes.
- `Human`: owns approval of consequential choices, policy exceptions, and escalation outcomes; consumes summarized options and evidence; produces explicit decisions.

**State Machine**
Use a compact, recoverable state machine:

1. `INIT`
- Load workflow record, target identity, revision identity, policy context, and last checkpoint.
- Validate that the target is still current and that authority is still valid.

2. `INTAKE`
- Capture the review question, scope, constraints, and required outputs.
- Normalize the target into a stable typed reference.

3. `BASELINE_CAPTURE`
- Record the exact evidence base being reviewed.
- Freeze hashes, versions, and any applicable snapshots.

4. `REVIEW`
- Analyze the target against scope and criteria.
- Emit findings, severity, evidence, and confidence.
- If findings are absent, emit a clean bill with residual-risk notes.

5. `TRIAGE`
- Decide whether remediation is required, optional, or prohibited.
- Route to `HUMAN_DECISION`, `REMEDIATE`, or `CLOSE`.

6. `HUMAN_DECISION`
- Present only decision-bearing options.
- Block until explicit human instruction arrives.
- Record decision provenance and scope.

7. `REMEDIATE`
- Apply or draft bounded remediation inside delegated constraints.
- Emit the exact change intent and affected surface.

8. `SELF_CHECK`
- Run local consistency checks on the remediation output.
- Ensure the proposed change matches the requested scope and did not expand silently.

9. `INDEPENDENT_VERIFY`
- Run a separate verifier with the original requirement plus change summary.
- Do not reuse the same internal reasoning trace as remediation.
- Produce pass/fail evidence and any unresolved concerns.

10. `RETRY_GATE`
- If remediation or verification failed, classify the failure as retryable, blocked, or escalatable.
- Retry only when the new attempt can change outcome and the previous failure mode is meaningfully different.

11. `RECOVERY`
- Restore from last committed checkpoint, discard partial transient state, and rehydrate typed context.
- Reconcile any drift between stored state and live target state.

12. `COMPLETE`
- Emit final receipt, outcome, verification evidence, and remaining risks.

13. `BLOCKED`
- Stop when authority, evidence, or environment is insufficient.
- Preserve exact blocker and next required input.

14. `ABORTED`
- Stop only when continuation would be unsafe or semantically invalid.

A useful invariant: every state transition must be explainable from the last persisted checkpoint plus current input, without hidden conversational memory.

**Typed Handoffs**
Use explicit envelopes rather than free-form messages.

`ReviewRequest`
- `workflow_id`
- `target_ref`
- `target_revision`
- `scope`
- `constraints`
- `policy_context`
- `required_outputs`

`ReviewFinding`
- `workflow_id`
- `finding_id`
- `severity`
- `location_ref`
- `evidence_refs`
- `reasoning_summary`
- `confidence`
- `recommended_action`

`RemediationIntent`
- `workflow_id`
- `approved_finding_ids`
- `allowed_surface`
- `change_constraints`
- `acceptance_criteria`
- `rollback_condition`

`ChangeReceipt`
- `workflow_id`
- `change_id`
- `touched_assets`
- `diff_summary`
- `assumptions_used`
- `open_questions`

`VerificationRequest`
- `workflow_id`
- `acceptance_criteria`
- `original_evidence_refs`
- `change_receipt`
- `forbidden_overlap`
- `independent_method_hint`

`VerificationResult`
- `workflow_id`
- `result`
- `checks_run`
- `evidence_refs`
- `residual_risks`
- `blockers`

`Checkpoint`
- `workflow_id`
- `state`
- `cursor`
- `artifact_refs`
- `completed_steps`
- `retry_budget`
- `last_transition_reason`

Typed handoff rules:
- every envelope has a stable workflow and revision identity,
- every envelope lists its source evidence,
- every envelope declares whether it is advisory, executable, or final,
- no stage may depend on undeclared fields,
- no stage may infer missing authority from previous success.

**Retry Semantics**
Use retry policy by failure class, not by generic attempt count.

Retryable:
- transient tool failure,
- temporary missing dependency,
- flaky verifier,
- incomplete but recoverable context sync.

Non-retryable without new evidence:
- remediation violates scope,
- verifier fails for a substantive reason,
- authority is ambiguous,
- target revision changed underfoot,
- the same hypothesis has already failed twice.

Retry rules:
- retry only with a changed hypothesis, changed input, or changed execution path,
- preserve the previous failure record,
- increment attempt count per failure class, not globally,
- stop retrying when the same materially equivalent attempt fails twice,
- escalate to human or block when a retry would merely repeat the same risk.

Each retry should carry:
- prior failure class,
- what changed,
- why the new attempt can succeed,
- what evidence will distinguish success from another failure.

**Resumability**
Resume from checkpoints, not from narrative memory.

Resumability requirements:
- persist after every state exit and before any external side effect,
- store the minimum typed context needed to re-enter the next state,
- include artifact identifiers, revision binding, and completed-step markers,
- revalidate that the target revision and authority still match on resume,
- detect supersession and force re-triage if the underlying target changed.

Resume algorithm:
1. load last committed checkpoint,
2. compare stored revision to live revision,
3. if unchanged, continue from recorded state,
4. if changed, branch to `BASELINE_CAPTURE` or `BLOCKED` depending on whether the workflow can safely realign,
5. if checkpoint is incomplete or corrupted, reconstruct from persisted receipts only, otherwise block.

**Independent Verification**
Verification must be isolated from generation.

Independent verification principles:
- verifier gets the requirement and the change receipt, not the original chain of reasoning,
- verifier uses different checks than the remediator whenever possible,
- verifier should prefer deterministic checks first,
- verifier must be able to fail the change even if the remediator believes it is correct,
- verifier reports residual risk rather than inferring success from partial agreement.

Verification hierarchy:
- structural checks,
- contract checks,
- behavioral checks,
- negative checks,
- recovery/rollback checks when relevant.

Completion requires:
- at least one check that could falsify the success claim,
- evidence that the checked artifact matches the claimed revision,
- explicit statement of what was not verified.

**Failure Recovery**
Recovery should be explicit and bounded.

Failure classes and responses:
- `CONTEXT_LOSS`: reload checkpoint, reconstruct typed inputs, resume only if revision still matches.
- `AUTHORITY_FAILURE`: block and request human decision or updated scope.
- `REMEDIATION_FAILURE`: retry only if a new bounded hypothesis exists; otherwise escalate.
- `VERIFICATION_FAILURE`: do not auto-loop remediation; either revise with a new hypothesis or block.
- `SUPERCESSION`: stop current run, create a new revision-bound run, preserve old evidence.
- `PARTIAL_SIDE_EFFECT`: record what changed, confirm rollback feasibility, and decide whether to rollback or continue from a repaired state.
- `INTERNAL_INCONSISTENCY`: stop, mark corrupted, and require fresh intake.

Recovery policy:
- prefer rollback over forward-fixing when the side effect is reversible and rollback is safer,
- prefer continuation over restart when the checkpoint is sound and the target is unchanged,
- never silently skip a failed verifier,
- never reuse a stale approval for a new revision.

**Verification Map**
`R1` through `R6` are satisfied when the workflow produces:
- typed intake with revision binding,
- checkpointed state transitions,
- a review finding or clean review result,
- an explicit remediation decision or block,
- an independent verification result,
- a final receipt with residual risks and provenance.

Falsifiable checks:
- a changed target revision forces revalidation,
- a missing authority record blocks remediation,
- a failed verifier prevents completion,
- a repeated equivalent retry is stopped,
- a resume from checkpoint does not lose completed work,
- a superseded target creates a new run instead of mutating the old one.

**Operational Transition**
Because no runtime is being selected yet, the operational design should stay runtime-neutral:
- persist state in a stable workflow record,
- store typed envelopes as serializable artifacts,
- make checkpoints idempotent,
- log transition reasons and failure classes,
- expose a clear human escalation point,
- retain enough evidence to reconstruct why the workflow stopped or succeeded.

**Handoff Controls**
Revalidation required before each dependent stage:
- target revision,
- authority context,
- checkpoint integrity,
- scope constraints,
- previous failure class.

Open decision gates:
- `D1` whether the remediation is authorized at all when it changes consequential behavior,
- `D2` whether a human wants a revised scope after verification failure,
- `D3` whether a superseded target should spawn a new run or be abandoned.

Replan if:
- the target changes,
- the authority model changes,
- verification cannot be made independent,
- retry loops repeat the same hypothesis,
- recovery would require inventing missing context,
- the workflow needs to cross a new policy boundary.

If you want, I can turn this into one of two next artifacts:
1. a runtime-neutral statechart spec with events, guards, and payload schemas, or
2. an agent contract document with producer/consumer interfaces and failure codes.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
