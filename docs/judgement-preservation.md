# Judgement-preserving automation

This document explains the repository-wide judgement-preservation principle in
`AGENTS.md` and the responsibility boundary in `README.md`. It is rationale and
design guidance for maintainers and operators, not a shared runtime dependency for
portable skills.

## The question before removing friction

Automation should remove mechanical work aggressively. The extra question is:

> What else is this activity doing, and will the future operating model still
> depend on that function?

Some recurring work is only waste. Some also builds causal understanding,
practical judgement, shared context, accountability, or recovery skill. When that
secondary function is still required, preserve it deliberately instead of
assuming a human approval step at the end is equivalent.

This is especially important when automation compresses implementation faster
than planning, verification, integration, and accountable decision-making. Output
can increase while human capability, shared understanding, or fallback competence
quietly declines.

## Systems-thinking lenses

These are diagnostic lenses, not maturity scores.

### Shifting the burden

A reinforcing pattern can form:

```text
hard work -> delegate to automation -> less human practice
          -> weaker human capability -> delegation becomes more necessary
```

The automation may be genuinely effective. The risk appears only when humans are
still expected to supervise novel cases, diagnose failure, or recover the system
after the practice that built those abilities has disappeared.

### Success to the successful

If the faster path receives more work, it also receives more opportunities to
improve while the slower human path receives fewer repetitions. Allocation can
therefore widen the apparent capability gap and make further allocation to
automation look increasingly obvious.

Do not counter this by forcing arbitrary manual work. Preserve only practice that
maintains a capability the operating model still needs.

### Stocks and flows

Throughput, changes merged, and tasks completed are flows. Human understanding,
distributed expertise, trust, and recovery competence are slower-moving stocks.
Optimising the visible flow can deplete the stock without showing up immediately
in delivery metrics.

Assess both when the automation changes who encounters, reasons about, and learns
from representative cases.

### Requisite variety

The human fallback is most valuable for rare, ambiguous, and novel disturbances.
If automation removes routine exposure, ask whether the remaining human control
still has enough practiced repertoire to handle the wider variety of situations
for which it remains accountable.

## Liberal-arts lenses

### Technique is not practical judgement

Procedures, skills, and rules can encode repeatable technique. They do not remove
the need for practical judgement where particulars, competing goods, uncertainty,
or consequences matter.

For this repository, the implication is simple:

> A skill may codify technique without claiming to exhaust the judgement required
> to apply it.

Some workflows should terminate deterministically. Others should deliberately
arrive at a well-framed human decision with evidence and authority intact.

### Tacit and situated knowledge

Not all useful knowledge becomes equivalent when written down. Some capability is
formed by repeated exposure to real situations, corrective feedback, and
participation in diagnosis or recovery.

Context capture, memory, ontologies, and documentation remain valuable, but their
presence is not proof that an accountable person can apply the knowledge to a new
case.

### Reflection in action

Unexpected evidence can be a learning event. If the workflow immediately converts
every surprise into another automated retry, it may preserve activity while
preventing the problem frame from being reconsidered.

For consequential work, repeated no-progress or contradictory evidence should
sometimes trigger a hypothesis update, a new discriminating observation, or an
accountable decision before execution continues.

## Prefer active over ceremonial friction

Useful controls exercise the capability they are intended to preserve. Examples:

- criteria or constraints stated before a model recommendation;
- competing interpretations surfaced before choosing;
- scenario-based explain-back for consequential changes;
- second-owner walkthroughs where knowledge concentration matters;
- sampled manual cases, simulations, or recovery drills;
- separation of proposal from consequential commit;
- a surprise/no-progress interrupt before repeating an unsupported approach.

A passive acknowledgement, copied model summary, or approval checkbox is not
evidence of understanding or judgement.

The default remains: **no extra friction when no material human capability or
decision responsibility is being displaced.**
