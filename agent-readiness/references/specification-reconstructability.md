# Specification reconstructability

Use this diagnostic only when the requested operating model deliberately makes
implementation replaceable—for example, agents may substantially regenerate or
replace bounded implementation with little implementation-level review—or when
code-only tacit knowledge is already a suspected reliability problem.

The objective is not to make code disposable. It is to test whether the intended
behaviour that higher autonomy depends on exists independently enough of the
current implementation to survive replacement.

## Counterfactual probe

Ask:

> If this implementation were replaced, which material behaviour could not be
> reconstructed without reading the old code?

Inspect the smallest evidence set that could answer that question. Check whether
authoritative intent and independent verification preserve, where material:

- externally observable behaviour, boundary cases, and failure semantics;
- business, state, concurrency, permission, and compatibility invariants;
- interface, schema, and existing-data obligations;
- performance, capacity, resource, security, privacy, and operational constraints;
- recovery, rollback, and other externally significant lifecycle behaviour.

Prefer independent oracles: accepted requirements, contracts, schemas, property or
conformance tests, externally governed policy, operational thresholds, and other
sources whose expected result is not merely copied from the current algorithm.
Characterization tests can preserve observed legacy behaviour, but do not by
themselves establish that the behaviour is approved intent.

## Pair with operational reconstructability when familiarity is replaceable

Behavioural reconstructability does not prove that an unfamiliar implementation
can be operated safely. When the operating model accepts that responders may not
remember the implementation, also use
[operational reconstructability](operational-reconstructability.md).

Ask the related but distinct counterfactual:

> If the pager fired and nobody remembered this implementation, could an
> accountable responder establish what the deployed system is doing, bound the
> impact, contain it, and verify recovery from trustworthy evidence?

Runtime evidence can strongly establish what happened under observed conditions;
it does not by itself establish what should have happened. Reconcile observed
behaviour against the authoritative intent and independent oracles assessed here.
Do not convert stable production behaviour into a requirement merely because it
is observable.

## Pair with theory reconstructability when needed

Behavioural and operational reconstructability do not prove that accountable
humans retain the theory needed to own the system. When agent-generated change
volume, weak ownership, rapid parallel delivery, or inherited code may have
outpaced human understanding, also use the
[cognitive-debt diagnostic](cognitive-debt.md).

Ask the related but distinct counterfactual:

> If the current maintainers were unavailable, could an accountable engineer
> reconstruct why the material behaviours, constraints, and boundaries exist from
> authoritative evidence and operational signals without treating the current
> implementation as self-justifying?

Do not require implementation trivia to survive in human memory. Focus on the
purpose, governing invariants, important assumptions, failure/blast-radius
boundaries, decision authority, and diagnostic model required for the target
activity. A system can be behaviourally and operationally reconstructable yet
still carry material cognitive debt if nobody can safely reason about change or
failure; conversely, strong human understanding does not replace missing
independent specifications, verification, or runtime evidence.

## Interpret gaps conservatively

Classify a material behaviour found only in implementation as observed current
behaviour, not automatically as a requirement. Determine whether it is governed
intent, accidental behaviour, an implementation choice, or genuinely unknown
before recommending that it be preserved.

Treat missing reconstructability as tacit-knowledge or specification debt. It is
not automatically a readiness failure: connect it to the requested activity and
only lower an autonomy cap when losing or hallucinating that behaviour would make
the proposed operating model unsafe or unreliable.

Prefer the smallest durable remediation that closes the material gap, such as:

- capture the governing invariant or quality attribute in an authoritative source;
- add an independent contract, property, conformance, performance, or recovery
  check;
- make an unresolved product or architecture choice explicitly human-owned;
- preserve a legacy behaviour as characterization evidence until its authority is
  resolved.

Do not require literal repository deletion/regeneration, exhaustive documentation,
tool-stack-independent specifications, or conversion of incidental implementation
details into requirements. Stop when further reconstruction analysis is unlikely
to change the autonomy decision or remediation order.
