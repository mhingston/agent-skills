# Flow constraints for automation discovery

Use this reference only when an automation candidate is intended to improve a
recurring end-to-end engineering or delivery outcome and there is enough evidence
to reason about where work waits, queues, reworks, or blocks.

Do not turn ordinary reminder, evidence-capture, attention, or coordination
automations into process-measurement exercises merely because they have a
sequence of steps.

## Define the protected flow

Name the externally meaningful outcome and its boundary before optimising a
stage. Examples include:

- ticket ready -> merge-ready pull request;
- pull request opened -> merged change;
- alert fired -> verified recovery;
- dependency update detected -> safely released remediation.

Then identify the meaningful stages or handoffs and, where evidence exists:

- active work time;
- elapsed or waiting time;
- queue age and work in progress;
- rework, rejection, or repeat attempts;
- arrival and completion rates;
- scarce human or system authority;
- intentional waits such as change windows or external SLAs.

Do not invent timing or queue data. Distinguish observed evidence from inference,
and state when the current constraint cannot be established confidently.

## Identify the current constraint

The current constraint is the stage, handoff, policy, capacity limit, quality
problem, or decision boundary that most credibly limits improvement of the
protected end-to-end outcome.

The longest wait is a useful clue, not an automatic answer. A stage may appear
slow because work arrives in bursts, upstream quality creates rework, a deliberate
approval protects a consequential decision, or downstream capacity is already
saturated.

Prefer a bounded hypothesis such as:

> Review queue age is the best-supported current constraint for ticket-to-merge
> lead time because implementation time is short and stable, while most elapsed
> time accumulates before first review. This would be weakened if the queue is
> mostly intentional release-window waiting or if review rework originates from
> poor ticket quality upstream.

## Select an intervention

Prefer the smallest automation that can improve the current constraint without
removing required human accountability or merely increasing arrival pressure on a
later stage.

For a candidate intended to improve flow, record:

- protected end-to-end outcome;
- current constraint and evidence strength;
- local stage the automation changes;
- expected local effect;
- expected end-to-end effect;
- likely upstream/downstream displacement risk;
- evidence that would falsify the hypothesis;
- pilot metrics and stop/reassess conditions.

A locally faster stage is not automatically valuable. If coding throughput rises
while review wait, WIP, rework, or release delay rises enough to absorb the gain,
the intervention did not establish an end-to-end improvement.

## Respect ownership boundaries

This lens chooses **where an automation opportunity is worth testing**. It does
not design a multi-agent state machine, define detailed runtime orchestration, or
approve an automation's side effects.

Route agent coordination, durable state, handoff, retry, authority, and recovery
design to `agent-workflow-design` when those become the primary problem. Route a
running automation back to `automation-reviewer` after a pilot so observed
system-flow impact and constraint migration can be evaluated from run evidence.

## Behavioural regression cases

### AM-F1 — faster coding is not the current constraint

Evidence shows ticket-ready to merge-ready averages 31 hours: 4 hours active
implementation, 22 hours waiting for review, 2 hours review, and 3 hours CI/merge.
A proposal suggests adding a coding agent expected to halve implementation time.

Expected behaviour:

- protect ticket-ready -> merge-ready as the outcome;
- identify review wait as the stronger current constraint hypothesis;
- do not prioritise the coding agent merely because its local speedup is easy to
  automate;
- recommend a bounded intervention or investigation around review flow first,
  unless other evidence changes the diagnosis.

### AM-F2 — ambiguous timing must stay ambiguous

Only anecdotal claims say review is slow; no representative timestamps, queue
history, or rework evidence are available.

Expected behaviour:

- report the constraint as unknown rather than manufacturing a bottleneck;
- propose the smallest measurement needed if the answer would change priority;
- continue to evaluate non-flow automation opportunities from evidence that does
  exist.

### AM-F3 — intentional waiting is not automatically waste

Most elapsed time occurs at a production approval gate that is required by policy
and exercised only in a fixed weekly release window.

Expected behaviour:

- distinguish intentional governed waiting from an automatable queue;
- do not recommend bypassing or weakening human authority;
- consider adjacent preparation, evidence assembly, or scheduling friction only
  where those can improve the protected outcome without changing the policy.

### AM-F4 — unrelated automation should not acquire flow ceremony

The task is to design a read-only reminder for stale personal follow-ups across
email and tickets.

Expected behaviour:

- use the normal `audit-me` responsibility, evidence, state, and pilot model;
- do not require ticket-to-merge timing, WIP, queue, or flow-constraint analysis;
- omit the flow hypothesis when it does not materially apply.

## Source provenance

The flow-constraint lens is informed by LeadDev's promoted partner article
"The engineer's guide to building a software factory". Transfer the mechanism —
optimise a bounded end-to-end outcome at its current constraint and re-measure —
not the article's product-specific topology, customer claims, or a requirement to
build a generic software-factory platform.
