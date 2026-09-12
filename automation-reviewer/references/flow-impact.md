# Reviewing system-flow impact and constraint migration

Use this reference when an automation claims to improve a recurring end-to-end
engineering or delivery outcome rather than only the quality, cost, or usefulness
of its own local result.

The purpose is to distinguish a genuine system improvement from a local speedup
that moved waiting, work in progress, rework, or human load elsewhere.

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
universal dashboard or treat any one metric as sufficient.

Separate:

1. **Local effect** — did the automated stage become faster, cheaper, more
   reliable, or require less human effort?
2. **End-to-end effect** — did the protected outcome materially improve?
3. **Constraint movement** — where does the flow now accumulate waiting, WIP,
   rework, or scarce decision capacity?

A successful local effect with no credible end-to-end improvement is not a failed
automation by definition, but it does not justify claiming system-level success.
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

## Choose the next action

Prefer the smallest evidence-backed response:

- **retain** when the end-to-end outcome improved and no material adverse shift is
  visible;
- **retarget** when the automation exposed or moved the constraint to another
  stage and the next intervention is justified;
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
- do not claim the delivery system became faster;
- identify review capacity/queueing as the strongest new constraint hypothesis;
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

## Source provenance

This mechanism is informed by LeadDev's promoted partner article "The engineer's
guide to building a software factory". The transferable idea is to measure a
bounded end-to-end outcome and re-identify the constraint after each intervention.
Do not import the article's vendor-specific platform model, agent topology, or
customer productivity claims as requirements or evaluation evidence.
