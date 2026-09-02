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