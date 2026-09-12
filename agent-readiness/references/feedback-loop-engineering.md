# Feedback loop engineering

Use this reference when recurring agent friction, review findings, CI failures,
repository drift, or production evidence may indicate that the engineering system
itself needs to change. The goal is not to add more agent ceremony. It is to make
future runs operate in a better environment by converting repeated evidence into
small, durable, verified improvements.

Treat feedback-loop capability as evidence about the operating environment, not as
an independent maturity score. A repository does not become agent-ready merely by
having maintenance agents, scheduled audits, dashboards, or retrospective reports.
The important question is whether relevant signals lead to appropriately owned
corrective work and whether that work measurably reduces the problem it was meant
to address.

## Three loop levels

Distinguish three useful levels of feedback.

### Inner loop — one change

The inner loop detects problems in the change currently being made. Typical
signals include:

- compilation, static analysis, linting, and formatting;
- focused and broader tests;
- independent review;
- exact-revision CI gates;
- agent-operable product or system feedback.

Its job is to falsify an incorrect change before it is accepted. This loop is often
part of the direct autonomy gate for bounded implementation because it establishes
whether one run can detect that its work is wrong.

### Middle loop — the project across changes

The middle loop looks across multiple runs, pull requests, CI histories, or the
repository's changing state. It seeks patterns that no single task has enough
context to see, including:

- repeated agent retries or confusion around the same operation;
- recurring review comments;
- repeated or flaky CI failures;
- stale or contradictory documentation;
- architectural, dependency, test, or complexity drift;
- repeated manual workarounds;
- recurring verification gaps;
- conventions that are repeatedly discovered too late.

Its output should normally be ordinary corrective work for the existing delivery
pipeline: improve a tool, add or strengthen a deterministic check, clarify an
authoritative contract, repair documentation, remove a repeated setup hazard, or
otherwise change the project so later runs do not pay the same cost again.

Do not treat one observation as a durable project rule. When longitudinal learning
or codification qualification is needed and a dedicated `session-lessons` workflow
is available, route recurrence analysis there rather than duplicating its evidence
thresholds. `agent-readiness` should consume the resulting evidence to judge
whether the operating environment supports the requested activity.

### Outer loop — the running system and business outcome

The outer loop observes what happens after delivery. Relevant signals can include:

- production errors, incidents, saturation, or latency;
- deployment and rollback evidence;
- product or business measures with an explicit causal interpretation;
- security or compliance events;
- post-deployment verification tied to the released revision.

This loop matters most when the target activity includes production-affecting
actions. A repository can support bounded local implementation without a rich
outer loop, but governed operational autonomy cannot be inferred from local checks
alone.

## Do not require every loop universally

The three-loop model is a diagnostic, not a universal checklist.

- A documentation-only change may need little beyond a strong inner loop.
- Repeated project friction can make a middle-loop capability valuable without
  making its absence an autonomy blocker by itself.
- Production actions require credible runtime verification and recovery evidence,
  but ordinary local work does not automatically require business telemetry.

Treat a missing loop as a **Gate** only when the selected policy or target activity
requires the capability, or when repeated unresolved evidence demonstrates that an
existing required control is ineffective. Otherwise classify it as an
**Improvement** or **Informational** finding according to consequence.

The existence of a maintenance loop must never raise the autonomy cap by itself.
Only stronger underlying controls and evidence may do that.

## Signal-to-correction discipline

For a project-level loop, preserve this chain:

1. **Observe a stable signal.** Keep the source and identity of the evidence: run,
   task, revision, PR, CI job, repository state, incident, or telemetry window.
2. **Interpret what the signal can establish.** Repeated retries may indicate tool
   friction; repeated review comments may indicate late enforcement; stale docs
   indicate drift. Do not jump directly from correlation to root cause.
3. **Qualify recurrence and scope.** Deduplicate correlated observations and seek
   evidence across independent contexts before codifying a general rule, except
   where a severe incident justifies immediate regression coverage.
4. **Choose the earliest durable correction.** Prefer the cheapest layer that can
   reliably prevent or expose the problem: deterministic tool or API, linter,
   schema, test, verifier, authoritative contract, scoped guidance, or workflow
   change.
5. **Route the correction through normal ownership and delivery.** Maintenance
   analysis does not create product, architecture, security, or policy authority.
   Corrective work should use the same review, verification, and approval gates as
   equivalent human-filed work.
6. **Measure whether recurrence falls.** Compare relevant before/after evidence.
   Reopen or revise the hypothesis when the problem persists.

Repeated feedback often means a rule is enforced too late. When a requirement is
objective and machine-checkable, prefer moving it into a deterministic control
rather than adding more prose that every future agent must remember. Guidance is
appropriate when judgement or context genuinely cannot be encoded mechanically.

## Safe maintenance automation

Introduce project-level maintenance automation progressively.

- Run a new loop manually first and inspect all findings.
- Check for duplicate, stale, already-resolved, or weakly supported work.
- Keep recommendation separate from execution until the signal proves useful.
- Increase automation only for narrow, reversible, well-verified corrections.
- Do not let a maintenance agent change its own authority, evaluation criteria,
  instructions, approval requirements, or autonomy level without the ordinary
  human and repository governance that applies to those changes.
- Do not allow a noisy loop to create unbounded work merely because it runs on a
  schedule.

A maintenance agent that files issues can be useful even when it never edits code.
The important property is reliable signal conversion, not how many lifecycle steps
one agent controls.

## Evidence sources

Useful sources reveal different failure classes:

| Source | What it can reveal | Common mistake |
| --- | --- | --- |
| Agent run logs and structured learning observations | retries, confusion, expensive tool paths, repeated setup friction | treating model self-explanation as causal proof |
| Revision-bound review history | recurring validated defects or conventions enforced during review | counting multiple comments on one root cause as independent evidence |
| CI history | recurring failures, flakes, slow or missing verification seams | assuming every red job is an agent-readiness problem |
| Repository state and history | documentation drift, duplicated policy, architectural or test decay | treating prevalence as authoritative intent |
| Production and incident telemetry | escaped failures, operational weakness, real outcome regressions | inferring causality from an unrelated metric movement |

Interpret the signal explicitly before proposing the correction.

## Loop-health evidence

When a feedback loop itself is material to readiness, inspect evidence such as:

- finding precision or the proportion of findings accepted after human review;
- duplicate and already-resolved finding rate;
- recurring failure frequency before and after the correction;
- proportion of findings that lead to verified corrective work;
- ignored or repeatedly reopened findings;
- time, cost, and human attention consumed by the loop;
- false escalation or unsafe automatic-action rate;
- whether corrections survive later repository or tool changes.

Do not use raw issue count, number of scheduled runs, or amount of generated text as
proof that the loop is healthy.

## Readiness interpretation

Feedback-loop evidence should affect an `agent-readiness` assessment in bounded
ways:

- a strong inner loop can directly support bounded implementation when it can
  falsify the material behaviour being changed;
- repeated unaddressed middle-loop evidence can weaken confidence in repository
  comprehension, verification reliability, tooling, or workflow controls;
- an effective middle loop can be evidence that the project learns from recurring
  failures, but does not compensate for a missing hard safety or correctness gate;
- credible outer-loop verification and exercised recovery are relevant to
  production-action readiness;
- no feedback loop may manufacture policy, human judgement, or authority.

When recommending a feedback-loop improvement, state the signal, interpretation,
smallest durable correction, normal owner or approval path, expected observable
change, and the evidence that will show whether recurrence actually declined.

## Source

This reference adapts the inner/middle/outer-loop framing and maintenance-agent
mechanism from Maria Gorinova and Simon Maple,
[Feedback Loop Engineering: making your project agent-ready](https://tessl.io/blog/feedback-loop-engineering-making-your-project-agent-ready),
4 September 2026.

The transferable mechanism is the project-level learning loop: use recurring
agent, review, CI, repository, and production evidence to improve the environment
future changes encounter. This skill deliberately does not adopt maintenance-agent
count, issue volume, or scheduled automation as a readiness metric.