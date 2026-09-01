# Execution State for Long-Running Agent Workflows

Read this reference when a workflow can outlive one model context, when active state
changes repeatedly during execution, or when a model contributes to state updates.

The goal is to keep the workflow's **current decision state** compact and explicit
without losing the append-only evidence needed for audit, recovery, or later skill
evolution.

These principles are informed by SKILL.state, *State Management for Long-Horizon
LLM Agents* (arXiv:2608.26263v2), but are expressed here as runtime-neutral design
rules rather than a required framework or storage implementation.

## Separate three kinds of memory

Do not collapse these into one conversation transcript or one ever-growing state
object:

1. **Execution state** — mutable, compact facts and decisions that a future
   transition may depend on in the current run.
2. **Audit/evidence history** — append-only observations, receipts, tool effects,
   rejected transitions, and provenance needed to reconstruct what happened.
3. **Evolution memory** — distilled cross-run learning about how a skill or
   workflow should change; this belongs to authoring/evaluation, not runtime
   execution.

A useful default is:

```text
observations/effects -> append-only evidence
                           |
                           v
                    current execution state
                           |
                           v
                     next decision/transition

across completed runs -> authoring/evolution memory
```

Execution state may point to evidence records rather than duplicating them. Do not
make auditability depend on retaining every prior observation in the active model
context.

## Treat execution state as a projection of history

Execution state is not a transcript summary. Retain information because a future
transition can depend on it, not merely because it happened.

For every material state field ask:

> Which future decision, invariant, recovery path, or transition can depend on this
> field?

If there is no credible answer, keep the information in evidence history rather
than active state.

Prefer the smallest state that remains sufficient for the workflow's future
choices. This is a design target, not a proof that history is irrelevant.

### Know when projection is unsafe

Do not discard historical evidence merely because it is not currently active when:

- the future relevance of an observation cannot yet be determined;
- the workflow is still discovering its state schema or task structure;
- an audit, investigation, provenance requirement, or final output depends on
  historical sequence;
- a later semantic decision may need to reinterpret an earlier observation;
- legal, policy, safety, or incident-response requirements mandate retention.

In those cases keep the authoritative evidence durably and decide separately what
subset belongs in active execution state.

## Bind state to exact external reality

Execution state is a cached decision substrate, not a new authority over the
world. Record the source/revision/version or freshness identity needed to detect
staleness.

When new authoritative evidence conflicts with active state:

1. preserve the prior evidence in history;
2. mark or reject stale derived state;
3. project the new authoritative observation into current state;
4. invalidate downstream approvals, gates, or decisions whose premises changed;
5. continue only from the earliest transition whose evidence is still valid.

Do not let an old statement remain influential merely because it appears many
turns earlier in a transcript.

## Prefer validated patches over model-owned state replacement

When model judgement is useful for deciding how semantic observations affect
state, let the model **propose a typed delta** rather than replacing the whole
state object.

Conceptually:

```text
current_state + validated_patch -> next_state
```

The deterministic coordinator remains the writer of record.

A patch contract should define, when relevant:

- expected current state/schema version;
- fields the model may add or update;
- fields the model may not change;
- explicit deletion semantics rather than omission-as-delete;
- value types, enums, cardinality, and size limits;
- source/evidence references supporting changed fields;
- invariants that must still hold after application;
- transition preconditions affected by the patch.

Apply this sequence:

1. parse the proposed patch against a versioned schema;
2. reject unknown or unauthorized fields;
3. verify types and semantic invariants;
4. check expected-version or equivalent stale-write protection when concurrent or
   resumed execution makes it material;
5. require explicit deletion/tombstone operations for destructive changes;
6. compute the candidate next state without mutating the authoritative store;
7. validate the resulting state and allowed transition set;
8. commit atomically and record a state-update receipt;
9. on failure, leave the prior state unchanged and return concrete violations.

Do not interpret a missing field in model output as permission to erase an
existing value. Do not ask the model to reconstruct unchanged fields that the
coordinator already knows.

## Keep model context bounded deliberately

Build each decision context from:

- the current execution state relevant to that decision;
- the active phase contract and invariants;
- the smallest evidence slice needed to justify or challenge the decision;
- required tool/capability schemas;
- current authority and policy state.

Reference bulky history rather than replaying it. Bounded context is not itself a
quality claim: naive truncation or generic compression may remove semantically
necessary state while matching the same token budget.

When comparing context strategies, separate **token reduction** from **state
quality**.

## Test long-horizon state behaviour

When durable state is a material part of the workflow design, include representative
state-specific evaluation rather than only one restart happy path.

### Horizon scaling

Run the same decision pattern at increasing step counts or event volumes. Check
that:

- active decision context grows slowly or remains bounded;
- state fields remain semantically sufficient;
- correctness does not depend on replaying the full transcript;
- evidence history remains available without becoming default model context.

### Distractor noise

Inject irrelevant but plausible telemetry, comments, or intermediate results.
Check that they are retained only where provenance requires and do not displace or
corrupt decision-relevant state.

### External drift

Change authoritative external state after a checkpoint or earlier observation.
Check that the next authoritative read repairs current state, invalidates stale
dependencies, and prevents old transcript content from winning by repetition.

### State-loss / insufficiency

Remove or fail to project one fact that a later transition genuinely requires.
Check that the workflow blocks, retrieves the missing evidence, or otherwise makes
the insufficiency visible rather than confidently completing from a lossy state.

### Patch corruption

Exercise model proposals that:

- omit unchanged fields;
- attempt unauthorized deletion;
- use the wrong type or schema version;
- overwrite a protected state field;
- arrive against a stale expected version;
- satisfy syntax while violating a semantic invariant.

Require deterministic rejection without partial state mutation.

### Budget-matched comparison

If claiming that structured execution state improves long-horizon quality, compare
against at least one alternative with a roughly comparable active-context budget
when practical. Do not attribute a win to state representation when the actual
difference is simply that one condition received far more usable context.

## Relationship to workflow evidence and skill evolution

Keep the ownership boundary explicit:

```text
current run:
  execution state + evidence history -> workflow decisions

across runs:
  selected failures/outcomes -> session learning / skill evolution memory
```

A runtime state field should not become permanent skill guidance merely because it
was useful once. Conversely, evolution memory should not be injected wholesale
into every task execution. Promote durable behaviour through the normal evidence,
authoring, and matched-evaluation workflow.

## Design checklist

Before accepting a long-running state design, verify that:

- active state has a clear future-decision purpose field by field;
- history needed for audit or reinterpretation survives outside active context;
- authoritative external state can invalidate stale projections;
- model-proposed state changes are patches, not implicit whole-state ownership,
  when deterministic patching is practical;
- omission cannot silently delete state;
- stale, malformed, unauthorized, or semantically invalid patches fail atomically;
- context construction selects current state and evidence deliberately rather than
  replaying history by default;
- long-horizon tests cover horizon, distractors, drift, insufficiency, and patch
  corruption when those failure modes are material.
