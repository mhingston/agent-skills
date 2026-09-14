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

## Assess knowledge concentration and dissemination

Retained understanding can still be fragile when it is concentrated in one person
or one review path. For consequential areas, inspect whether enough people at the
relevant ownership boundary can independently reconstruct the theory needed to
change, diagnose, and recover the system.

Do not require broad familiarity with every implementation detail. Scale the
expected distribution of understanding to consequence, blast radius, operational
ownership, and substitution risk. A contained adapter may reasonably have one clear
owner; a shared pricing rule, security boundary, data-ownership rule, migration
mechanism, or production orchestrator may require wider recoverability.

Look for evidence such as:

- only one engineer can explain the governing invariants or failure model;
- reviews repeatedly depend on the same person to detect cross-boundary effects;
- agent-generated changes bypass the human interactions through which design and
  operational context previously spread;
- incident response or change approval stalls when one expert is unavailable;
- nominal co-owners can approve syntax or tests but cannot explain consequences;
- a focused pairing, walkthrough, plan review, explain-back, or rotation materially
  increases independent understanding.

Do not use reviewer count, meeting attendance, documentation volume, or copied
summaries as proof of dissemination. The useful evidence is whether another
accountable person can correctly reason about representative change or failure
scenarios without simply replaying the originating model's explanation.

When concentration is material, prefer the smallest durable dissemination action:
review intent or plans before implementation, pair on a consequential change,
perform a focused walkthrough or teach-back, capture the governing rationale or
invariant, produce a decision-bearing change digest, or deliberately widen
operational ownership. Do not add ceremonies when existing independent
understanding is already proportionate to the risk.

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
requires unexplained assumptions, consequential understanding is concentrated in
an unavailable single expert, or consequential judgement would effectively be
delegated to the model. Do not globally downgrade unrelated areas.

Strong independent controls can reduce the consequence of limited implementation
familiarity, but do not pretend they create human understanding. Keep the two
claims separate.

## Accept debt explicitly when appropriate

Some cognitive debt can be a rational trade-off. When the operating model accepts
it, record:

- the affected area and target activity;
- what understanding is intentionally deferred, fragile, or concentrated;
- the accountable human owner or decision authority;
- why the boundary and consequence make acceptance reasonable;
- compensating contracts, tests, observability, rollback, or isolation;
- a trigger for repayment or reassessment, such as ownership change, repeated
  incidents, broader reuse, increased autonomy, expansion of blast radius, or loss
  of the only person who can reconstruct the area;
- observable completion evidence for repayment.

Avoid vague promises to "document it later". Prefer the smallest durable action
that rebuilds the missing theory: capture a governing invariant or rationale,
perform a focused walkthrough or teach-back, add a diagnostic/contract seam,
resolve ownership, widen understanding at a consequential boundary, or reconstruct
a critical decision from authoritative evidence.

## Pair the three reconstructability questions

For implementation-replaceability concerns, pair this diagnostic with
[specification reconstructability](specification-reconstructability.md) and, when
operation must not depend on author recall,
[operational reconstructability](operational-reconstructability.md).

Keep the questions distinct:

- specification reconstructability asks whether intended behaviour survives
  replacement;
- operational reconstructability asks whether responders can establish actual
  deployed behaviour, impact, containment, and recovery from trustworthy evidence;
- cognitive debt asks whether accountable humans retain enough theory to own the
  consequential decisions safely.

A system can be strong in any two dimensions and weak in the third. Runtime
telemetry does not create governing intent or human understanding; human theory
does not replace independent specifications or runtime evidence; and strong
specifications do not guarantee incident operability.

## Behavioural calibration cases

### CD-C1 — one expert is a consequential understanding bottleneck

Agents generate most changes in a shared authorization service. Tests and policy
checks are strong, but every material review and incident diagnosis depends on one
engineer; the remaining listed owners cannot explain the trust-boundary invariants
or recovery assumptions without asking that engineer or the coding agent.

Expected behaviour:

- identify material knowledge concentration without claiming the code is wrong;
- keep strong automated controls as real compensating evidence without treating
  them as human understanding;
- relate the gap to the consequential authorization boundary rather than the whole
  repository;
- recommend a bounded dissemination mechanism, such as plan review, pairing, or a
  scenario-based teach-back, with evidence that another accountable owner can
  reason independently afterwards.

### CD-C2 — narrow ownership is proportionate

A stateless, contract-tested internal adapter has one clear owner and a documented
fallback. Another engineer can reconstruct its input/output contract and disable
path from repository and runtime evidence, but nobody else remembers its internal
implementation.

Expected behaviour:

- do not manufacture a knowledge-distribution requirement from headcount alone;
- treat the boundary, consequence, independent contract, and recovery evidence as
  relevant to whether concentration matters;
- avoid recommending recurring walkthroughs, rotations, or review ceremony when
  they would not materially improve safe ownership.

## Sources

This diagnostic adapts the distinction and risk framing from:

- [The Cost of Cognitive Debt](https://ljtn.github.io/epiq/blog/cost-of-cognitive-debt.html),
  especially the idea that degraded human understanding has a real cost that
  varies with system complexity and consequence;
- Margaret-Anne Storey, [From Technical Debt to Cognitive and Intent Debt](https://doi.org/10.1145/3807966),
  which frames cognitive debt as erosion of shared understanding and highlights
  practices that rebuild team mental models.

The knowledge-concentration refinement is also informed by Honeycomb's 2026 posts
on the code-review bottleneck and spending more time talking to humans in AI-heavy
engineering teams. The transferable mechanism is that implementation automation
can remove incidental knowledge-transfer paths, so shared understanding may need
explicit but proportionate reinforcement.

The skill deliberately does not adopt a single Cost of Cognitive Debt score.
Agent-readiness already uses evidence-backed gates and area-specific autonomy caps,
which preserve the useful mechanism without turning an imprecise heuristic into a
readiness metric.
