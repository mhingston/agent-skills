# Human control and judgement preservation

Use this reference when a workflow contains a consequential human gate or when
automation removes recurring work that may also be maintaining human capability.

The objective is not to keep humans busy or to slow automation. Remove mechanical
friction freely. Preserve human involvement only where the operating model still
depends on judgement, understanding, accountability, or recovery capability that
would otherwise become weaker or ceremonial.

## Test whether a human gate is substantive

A human checkpoint is a real control only when all material conditions hold:

1. **Authority** — the person or role is actually authorised to decide, redirect,
   stop, or accept the relevant residual risk.
2. **Evidence** — the decision packet contains current, attributable evidence and
   makes material uncertainty visible.
3. **Understanding** — the person can form a proportionate causal model of the
   behaviour, failure mode, or trade-off they are responsible for; polished model
   prose is not itself evidence of comprehension.
4. **Agency** — disagreeing, requesting more evidence, redirecting, or stopping is
   operationally possible and does not merely rubber-stamp a decision already made
   by the workflow.

Do not add an approval step when deterministic policy can decide the matter safely.
Conversely, do not call a passive acknowledgement or click-through approval
"human in the loop" when the workflow has removed the information, time, authority,
or understanding needed to exercise judgement.

## Check capability displacement

Before automating a recurring human activity, ask:

- what part is mechanical execution versus judgement-bearing practice;
- what causal, domain, operational, or trade-off knowledge people currently gain
  through doing it;
- whether another owner can independently reason about representative cases;
- whether the future operating model still expects humans to supervise, diagnose,
  recover, or handle novel exceptions in this area;
- what knowledge-transfer path disappears if the work is fully delegated.

Do not infer displacement merely because AI performed the work. Strong contracts,
verification, observability, containment, and reconstructability can make detailed
implementation familiarity unnecessary. Preserve practice only when losing it
would weaken a consequential human control the system still relies on.

## Select the smallest active mechanism

Prefer the least costly mechanism that exercises the capability actually needed.

| Need | Useful mechanism |
| --- | --- |
| Mechanical, reversible work with a strong oracle | No human friction; automate it |
| Human value or trade-off judgement | Have the human state criteria or constraints before seeing the model's preferred option |
| Material ambiguity | Surface competing interpretations and the smallest deciding evidence or accountable choice |
| Consequential change with comprehension risk | Scenario-based explain-back in the human's own words |
| Unexpected evidence that contradicts the working model | Stop the retry/fix loop long enough to restate the hypothesis or frame |
| Knowledge concentrated in one owner | Pairing, second-owner walkthrough, or transfer scenario |
| Rare exception handling still depends on human skill | Sampled representative cases, simulation, incident/recovery drills, or bounded rotation |
| Consequential or irreversible effect | Separate proposal from commit and keep commit authority independently governed |

Do not require all mechanisms. A workflow should be able to justify why a
particular control remains necessary and retire it when evidence shows the
capability is no longer required or the mechanism has become ceremony.

## Treat surprise as information

When an observation materially contradicts the current causal model, repeated
equivalent retries can reduce learning while increasing activity. For
consequential work, define a no-progress or surprise transition that requires one
of:

- new discriminating evidence;
- a changed hypothesis or problem frame;
- an accountable decision;
- a safe stop or escalation.

Do not make every failure a meeting or human interrupt. Use this only when the
next automated action would otherwise repeat the same unsupported model of the
problem.

## Preserve capability without preserving obsolete work

Useful options include:

- automate context assembly, evidence gathering, deterministic validation, and
  repetitive execution while leaving the consequential decision explicit;
- sample a small proportion of representative cases rather than requiring manual
  handling of every case;
- move practice to simulations or drills when production work is too costly or
  risky as a training surface;
- require active explanation only at boundaries where causal understanding is
  part of the control contract;
- deliberately widen ownership when one person's tacit model is a substitution
  risk.

The goal is retained human control proportional to consequence, not maximum
manual participation.
