# Reviewing system-flow impact and constraint migration

Use this reference when an automation claims to improve a recurring end-to-end
engineering or delivery outcome rather than only the quality, cost, or usefulness
of its own local result.

The purpose is to distinguish a genuine system improvement from a local speedup
that moved waiting, work in progress, rework, or human load elsewhere. A visible
constraint is not automatically waste: some constraints intentionally preserve
judgement, knowledge transfer, accountability, or risk containment.

## Reconstruct the flow claim

Identify:

- the protected end-to-end outcome and boundary;
- the local stage changed by the automation;
- the pre-pilot constraint hypothesis, if one existed;
- expected local and end-to-end effects;
- upstream and downstream stages likely to absorb extra throughput;
- policy, approval, quality, or release boundaries that must remain intact.

If the original automation had no explicit flow hypothesis, reconstruct only what
the evidence supports. Do not manufacture a baseline after the fact.

## Compare system evidence

Prefer representative before/after or contemporaneous evidence where available,
such as:

- end-to-end elapsed or lead time;
- active versus waiting time by stage;
- queue age and work in progress;
- arrival and completion rates;
- rework, rejection, retry, or reopen rate;
- human touch time or interruption burden;
- completion/acceptance rate;
- release or recovery latency.

Use only metrics that are meaningful for the protected outcome. Do not require a
universal dashboard or treat any one metric as sufficient. Treat PRs opened,
commits or lines generated, agent tasks completed, specifications or tickets
produced, model calls, and worker completions as production/activity indicators
unless evidence connects them to the protected end-to-end outcome.

Separate:

1. **Local effect** — did the automated stage become faster, cheaper, more
   reliable, or require less human effort?
2. **End-to-end effect** — did the protected outcome materially improve?
3. **Constraint movement** — where does the flow now accumulate waiting, WIP,
   rework, or scarce decision capacity?

A successful local effect with no credible end-to-end improvement is not a failed
automation by definition, but it does not justify claiming system-level success.
Optimise verified outcomes, not generated output: increased production establishes
system-level improvement only when accepted end-to-end outcomes improve without an
offsetting increase in WIP, rework, verification load, or required sense-making.
It may have created useful capacity, shifted the next constraint, or simply moved
cost elsewhere.

## Diagnose constraint migration

Evidence for migration can include:

- a downstream queue growing as the automated stage emits work faster;
- reviewers, approvers, release windows, test environments, or deployment systems
  becoming the new dominant wait;
- increased rework because upstream speed reduced preparation or quality;
- reduced human touch time locally but increased interruption or recovery work
  elsewhere;
- stable end-to-end time despite a large local cycle-time improvement.

Do not assume every new queue is caused by the automation. Check changes in
arrival rate, demand mix, staffing, policy, tooling, incidents, release cadence,
and measurement definitions before attributing causality.

## Classify the constraint before optimising it

When a human decision or review stage becomes the dominant wait, determine what
function it is serving before recommending that it be removed, automated, or made
faster. Use evidence to distinguish among at least these cases:

- **wasteful queue** — delay is mostly scheduling, handoff, duplicate checking, or
  missing preparation and adds little decision value;
- **capacity constraint** — the stage performs necessary work, but demand exceeds
  available capacity or work arrives in a form that creates avoidable effort;
- **protective or sense-making constraint** — the stage materially creates shared
  understanding, catches consequential design or risk issues, distributes
  ownership, or provides accountable human judgement that should not be silently
  traded for throughput.

A stage can combine these properties. Do not call review protective merely because
it is human, and do not call it waste merely because it is slow. Look for evidence
such as material design changes, defects prevented, risk dispositions, explain-back
or knowledge-transfer outcomes, concentration of system understanding, and whether
the same function could be preserved with better preparation or a narrower gate.

When a protective function is real, optimise around it first: improve plan quality,
evidence assembly, review routing, batch size, scheduling, or deterministic checks
that remove mechanical work. Change or remove the human boundary only when the
accountable owner explicitly accepts the resulting loss or an alternative control
preserves the required function.

## Choose the next action

Prefer the smallest evidence-backed response:

- **retain** when the end-to-end outcome improved and no material adverse shift is
  visible;
- **retarget** when the automation exposed or moved the constraint to another
  stage and the next intervention is justified;
- **protect** when the constrained stage provides a material sense-making,
  accountability, or safety function and the next improvement should reduce
  avoidable work around it rather than erase it;
- **narrow or tune** when increased output is overwhelming downstream capacity;
- **repair quality or context** when faster upstream work creates rework;
- **measure** when missing or incompatible evidence prevents a flow conclusion;
- **pause or roll back** when the automation worsens the protected outcome or
  creates unsafe pressure that cannot be contained by a smaller change.

Do not weaken required human approvals, policy gates, or safety controls merely
because they appear as elapsed time. Improve preparation, evidence assembly,
queueing, or scheduling around them unless an accountable policy owner separately
changes the boundary.

## Behavioural regression cases

### AR-F1 — local speedup, migrated review constraint

Before the pilot, implementation averages 6 hours and first-review wait 4 hours.
After introducing a coding automation, implementation averages 1 hour while
first-review wait rises to 10 hours, WIP rises materially, and ticket-ready to
merge-ready time is flat.

Expected behaviour:

- acknowledge the real local implementation gain;
- treat extra PRs, commits, or agent completions as production/activity evidence,
  not delivery success;
- do not claim the delivery system became faster;
- identify review capacity/queueing as the strongest new constraint hypothesis;
- determine whether the review delay is wasteful, capacity-limited, protective, or
  mixed before recommending automation or removal;
- recommend a bounded next experiment or retargeting action rather than simply
  increasing coding throughput again.

### AR-F2 — genuine end-to-end improvement

A review-assistance automation reduces median first-review wait and total
pull-request lead time across representative work, while rework, reopen rate,
quality gates, and downstream release queues remain stable.

Expected behaviour:

- treat the evidence as supporting an end-to-end improvement;
- preserve the independent review and policy boundaries that remain valuable;
- identify the next constraint only if the evidence supports one rather than
  inventing more optimisation work.

### AR-F3 — changed workload makes the comparison indeterminate

The pilot coincides with a release freeze ending, a large demand spike, and a
change in ticket mix. Local automation metrics improve but pre/post lead-time
samples are not comparable.

Expected behaviour:

- classify the system-flow conclusion as indeterminate;
- retain the local evidence separately;
- propose a representative measurement window or matched comparison rather than
  attributing the observed queue change to the automation.

### AR-F4 — non-flow automation should stay on its own contract

The automation is a weekly stale-commitment reminder whose purpose is omission
prevention, with useful-finding, false-positive, miss, interruption, and cost
evidence.

Expected behaviour:

- evaluate it using its stated outcome and existing automation-review dimensions;
- do not require ticket lead time, WIP, or throughput evidence;
- do not reinterpret every automation as a software-production-line stage.

### AR-F5 — slower review is buying shared understanding

Agent-generated implementation volume doubles. Review becomes the dominant queue,
but representative review evidence shows reviewers frequently correct cross-service
assumptions, make material design changes before merge, and spread operational
knowledge across more than one owner. Incidents and rework remain stable. A proposal
suggests auto-approving all green changes to recover lead time.

Expected behaviour:

- recognise the review queue as a real flow constraint without equating it with
  pure waste;
- identify the evidenced design, knowledge-transfer, and accountability functions;
- reject raw green-check status as proof that those functions are replaceable;
- first consider smaller changes such as reviewing intent earlier, improving
  evidence packets, shrinking change size, routing specialist review, or moving
  objective checks into deterministic controls;
- require explicit evidence and accountable authority before removing a protective
  review function.

## Source provenance

The system-flow mechanism is informed by LeadDev's promoted partner article "The
engineer's guide to building a software factory". The transferable idea is to
measure a bounded end-to-end outcome and re-identify the constraint after each
intervention. Do not import the article's vendor-specific platform model, agent
topology, or customer productivity claims as requirements or evaluation evidence.

The protective-constraint refinement is informed by Honeycomb's 2026 engineering
posts on embracing the code-review bottleneck and safely absorbing much higher
pull-request throughput. The transferable mechanism is that review can be both a
queue and a deliberate sense-making/control surface; do not optimise its elapsed
time without establishing which functions would be lost.