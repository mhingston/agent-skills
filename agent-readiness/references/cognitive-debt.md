# Cognitive debt

Use this diagnostic when agent-generated change volume, weak ownership, rapid
parallel delivery, or inherited code may have outpaced human understanding of a
material area. The concern is not whether every line is memorised. It is whether
people who remain accountable for the system retain enough theory to reason about
change, failure, and recovery.

Treat cognitive debt as distinct from technical debt and specification/intent
debt:

- **technical debt** is a known implementation or design compromise;
- **specification/intent debt** is missing or ambiguous authoritative purpose,
  constraints, or expected behaviour;
- **cognitive debt** is degraded human understanding of how or why a material
  area works, even when the code, tests, or documentation appear healthy.

Do not infer cognitive debt from code volume, AI authorship, documentation count,
or the absence of hand-written implementation. Demonstrable human understanding
and retained decision authority matter more than who typed the code.

## Human-theory probe

For the area and target activity, ask whether an accountable engineer can explain,
with evidence rather than confidence alone:

- what problem the area solves and why it is shaped this way;
- the important domain, state, data, concurrency, permission, compatibility, and
  operational invariants;
- assumptions that must remain true across dependencies and boundaries;
- likely failure modes, blast-radius boundaries, and recovery expectations;
- which behaviours are governed intent versus incidental implementation;
- how they would investigate behaviour that automated checks or telemetry do not
  immediately explain;
- where to escalate when product, architecture, security, data, or operational
  judgement is required.

Prefer lightweight demonstrations over documentation-volume proxies: a focused
walkthrough, incident explanation, change-impact analysis, architecture review, or
teach-back against a representative scenario can provide stronger evidence than a
large corpus nobody can reliably apply.

## Interpret by consequence and containment

Use complexity and consequence as triage dimensions, not as a universal numeric
score. Higher complexity increases the effort required to rebuild a useful mental
model; higher consequence increases the cost of discovering misunderstanding
through failure. Record the evidence and decision directly instead of multiplying
arbitrary numbers into a maturity score.

Assess cognitive debt at meaningful ownership and architectural boundaries. Weak
human understanding in a replaceable, well-contained adapter with strong
contracts, observability, and recovery is different from the same gap in core
business rules, security boundaries, shared data ownership, or production
orchestration.

A cognitive gap becomes an autonomy gate only when it materially weakens the
human control required for the target activity—for example, reviewers cannot
reason about change impact, incidents cannot be diagnosed safely, recovery
requires unexplained assumptions, or consequential judgement would effectively be
delegated to the model. Do not globally downgrade unrelated areas.

Strong independent controls can reduce the consequence of limited implementation
familiarity, but do not pretend they create human understanding. Keep the two
claims separate.

## Accept debt explicitly when appropriate

Some cognitive debt can be a rational trade-off. When the operating model accepts
it, record:

- the affected area and target activity;
- what understanding is intentionally deferred or fragile;
- the accountable human owner or decision authority;
- why the boundary and consequence make acceptance reasonable;
- compensating contracts, tests, observability, rollback, or isolation;
- a trigger for repayment or reassessment, such as ownership change, repeated
  incidents, broader reuse, increased autonomy, or expansion of blast radius;
- observable completion evidence for repayment.

Avoid vague promises to "document it later". Prefer the smallest durable action
that rebuilds the missing theory: capture a governing invariant or rationale,
perform a focused walkthrough or teach-back, add a diagnostic/contract seam,
resolve ownership, or reconstruct a critical decision from authoritative evidence.

For implementation-replaceability concerns, pair this diagnostic with
[specification reconstructability](specification-reconstructability.md). The two
questions are related but different: reconstructability asks whether intended
behaviour survives replacement; cognitive debt asks whether accountable humans
retain enough theory to own the system safely.

## Sources

This diagnostic adapts the distinction and risk framing from:

- [The Cost of Cognitive Debt](https://ljtn.github.io/epiq/blog/cost-of-cognitive-debt.html),
  especially the idea that degraded human understanding has a real cost that
  varies with system complexity and consequence;
- Margaret-Anne Storey, [From Technical Debt to Cognitive and Intent Debt](https://doi.org/10.1145/3807966),
  which frames cognitive debt as erosion of shared understanding and highlights
  practices that rebuild team mental models.

The skill deliberately does not adopt a single Cost of Cognitive Debt score.
Agent-readiness already uses evidence-backed gates and area-specific autonomy caps,
which preserve the useful mechanism without turning an imprecise heuristic into a
readiness metric.
