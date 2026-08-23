# Behavioural Evaluation in CI

Use this reference when a repository wants skill or agent-instruction changes to
receive behavioural regression coverage in continuous integration.

The goal is to run the same real harness used in deployment against a changed
skill and an exact baseline. Static package validation, linting, schema checks,
or a model-free classifier are useful controls but are not behavioural evals.

## 1. Select affected skills deterministically

Compute changed paths from the pull request merge base or other exact base
revision. Map a change to a top-level skill when it modifies that skill's
`SKILL.md`, `references/`, `scripts/`, `assets/`, generated adapter input, or
other material behaviour-affecting resource.

Do not trigger a model run merely because a catalogue README or unrelated
repository file changed. When several skills changed, run each affected suite or
an explicitly defined integration suite when their interaction is the behaviour
under test.

Record the exact base revision, candidate revision, selected skill paths, and the
rule that selected them. Do not rely on an agent to decide which of its own
changes require evaluation.

## 2. Materialize an exact baseline

For an existing skill, evaluate the candidate against the exact skill package at
the selected base revision. For a new skill, use the no-skill condition or the
nearest existing capability only when that is the declared comparison.

Do not compare against a remembered prompt, copied summary, or current checkout
whose content may already include candidate changes. Keep candidate and baseline
packages isolated so the harness cannot discover both.

## 3. Execute in a real harness

Pin or record, as applicable:

- harness and version;
- model and model profile;
- system or repository instruction bundle;
- tool and permission surface;
- test inputs and workspace fixture revision;
- evaluator or deterministic verifier version;
- attempt, token, time, and cost bounds.

Run matched candidate and baseline conditions from fresh contexts. Use the same
cases and external conditions for both sides. Prefer the actual deployment
harness when the claim is about production behaviour. A surrogate classification
or static prompt inspection may supplement this run but cannot replace it.

At minimum include a routine case, a boundary or near-miss case, and a known
failure-prone case when those behaviours exist. Include validated `eval_seed`
regressions that belong to the affected skill.

## 4. Publish evidence, not a green badge

For every matched pair retain enough evidence to inspect what happened:

- case identity;
- candidate and baseline package revisions;
- harness/model identity;
- verifiable checks and results;
- final output or stable artifact reference;
- material trajectory failure or shortcut category when relevant;
- tokens, duration, and cost when exposed;
- `not_verifiable` fields rather than invented values.

Use the portable result contract in `evaluation-results.md` when deterministic
aggregation earns its overhead. A CI summary should link or point to the raw
results used to derive any aggregate.

Never report `PASS` merely because the harness launched successfully or the
skill package validated. If the behavioural harness, credentials, baseline,
verifier, or required fixture is unavailable, report `NOT_RUN` or `BLOCKED` with
the missing prerequisite.

## 5. Introduce blocking gates conservatively

Start a new behavioural suite as advisory until enough runs show that its cases,
verifiers, latency, and variance are stable enough to distinguish regressions
from noise. Promote a check to blocking only with an explicit repository policy
covering:

- which changes require the gate;
- minimum cases or repeated trials where variance matters;
- success and regression thresholds;
- treatment of `not_verifiable`, infrastructure failure, and flaky cases;
- token, duration, or cost regression policy;
- waiver authority and expiry when waivers are permitted.

Do not silently convert an advisory metric into merge policy. A higher-cost
candidate may be correct when it buys materially stronger evidence or behaviour;
use paired functional and efficiency evidence rather than a cost-only threshold.

## 6. Turn validated escapes into regression cases

A production incident, escaped defect, unsafe action, or repeatedly missed
behaviour may enter the affected skill's evaluation suite before it justifies a
durable instruction change when all of these are true:

- the failure is tied to an exact run, revision, or other stable evidence unit;
- the relevant failure mechanism is supported rather than guessed from temporal
  proximity;
- the behaviour can be reproduced or represented by a faithful fixture;
- an independent verifier can distinguish the failure from the desired outcome;
- secrets, personal data, and task-specific answer keys can be removed.

Preserve the historical reproduction when exact fidelity matters, and normally
add a sibling or near-miss case so the skill cannot simply memorize the incident.
The regression case does not prove which skill change should fix it.

## 7. Separate pull-request and portability coverage

A fast pull-request suite should exercise the affected skill in one pinned
reference harness when that gives useful signal. Broader portability testing
across multiple harnesses or models can run on a schedule or before a release when
its cost and latency would make every pull request impractical.

Do not generalize a passing result from one harness to all harnesses. Record the
scope of every conclusion.

## 8. Avoid placebo CI

Do not create a workflow named `behavioural-evals` that only checks filenames,
validates Markdown, or confirms an evaluation specification exists. Those checks
may be useful admission controls, but they must be named and reported as static or
configuration validation.

When the repository cannot run a credentialled real harness, keep the behavioural
contract executable elsewhere and report that the behavioural run is unavailable.
An explicit unexecuted contract is stronger evidence than a misleading green
check.