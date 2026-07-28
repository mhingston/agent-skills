---
name: agent-readiness
description: Assess how safely and effectively coding agents can operate in a repository, codebase area, or engineering workflow. Use before introducing coding agents, increasing autonomy, enabling parallel agent work, or diagnosing why agent changes are unreliable. Determine the highest supported autonomy from evidence about specifications, repository context, reproducibility, verification, architecture, tooling, security, review, observability, recovery, and delivery controls. Read-only by default; do not implement remediations or treat a scanner score as proof of readiness.
---

# Assess Agent Readiness

Determine what agent-assisted activities the current engineering environment can
support reliably. Treat readiness as a property of the complete system around the
model—not the presence of an AI tool, instructions file, test command, or maturity
score.

The objective is not maximum autonomy. Recommend only the autonomy that the
available controls can supervise, and identify the smallest evidence-backed
improvements that would make a more ambitious operating model safe and useful.

## Boundaries

- Inspect repositories, documentation, history, configuration, CI, operational
  artefacts, and available tooling with read-only actions.
- Do not edit files, install dependencies, generate instruction files, create
  reports in the repository, change policies, or enable agent access.
- Do not execute repository-controlled code, hooks, builds, tests, package
  installers, or external scanners without explicit authorisation and an
  appropriate isolation boundary.
- Do not recommend autonomous merge, deployment, production access, secret
  access, or policy changes merely because lower-risk development checks pass.
- Do not infer effectiveness from artefact presence. A test script, README,
  CODEOWNERS file, CI workflow, AI instruction file, or observability dependency
  is evidence to inspect, not proof that the control works.
- Do not turn a readiness assessment into an implementation plan. Recommend
  remediation outcomes and verification evidence; route a requested change to a
  planning or implementation workflow separately.
- Respect repository, organisational, legal, security, privacy, and human
  accountability boundaries. Record missing access rather than bypassing it.

## Route adjacent work

Use this skill for the operating environment and its supported agent autonomy.
Use another workflow when the primary task is:

- planning one repository change: use a software-planning workflow;
- making a selected work item agent-ready: use a refinement workflow;
- establishing a semantic model: use a repository-ontology workflow;
- reviewing a particular patch: use a technical-review workflow;
- designing a durable agent state machine: use an agent-workflow-design workflow
  when available;
- measuring only AgentRC criteria or generating its HTML dashboard: use the
  AgentRC-specific assessment workflow when available.

An AgentRC result may be one evidence source for this assessment, but it does not
replace this skill's effectiveness, autonomy, security, or human-control analysis.

## Evidence discipline

Classify material statements:

- **Observed (`E#`)**: directly supported by inspected repository content, tool
  output, authoritative documentation, policy, or user evidence. Cite a stable
  locator such as a path, symbol, workflow, check, policy section, or command
  result.
- **Inferred (`I#`)**: a reasoned interpretation of observations. Name the
  supporting evidence and what could falsify the inference.
- **Unknown (`U#`)**: missing, inaccessible, stale, contradictory, or untested
  evidence that prevents a confident conclusion.
- **Required (`P#`)**: a policy or operating-model requirement against which the
  environment is being assessed. State its source and whether it is mandatory or
  a proposed default.

Do not convert an unknown into a failure unless the selected policy requires
fail-closed treatment. Do not convert absence of evidence into evidence of
absence. Make contradictions and provenance visible.

## 1. Define the assessment contract

Establish:

- repository, workspace, service, subsystem, or monorepo area in scope;
- intended users and accountable owners;
- target agent activities;
- requested or current operating model;
- relevant organisational policy and risk tolerance;
- environments and data classifications involved;
- evidence sources and access limitations;
- whether the result is a baseline, adoption gate, autonomy-increase gate,
  incident follow-up, or periodic reassessment.

Assess target activities separately when their risks differ. Typical activities
include:

1. read-only explanation and investigation;
2. planning and work-item refinement;
3. supervised local code edits;
4. bounded implementation of one ready task;
5. pull-request creation;
6. parallel agent implementation;
7. dependency, schema, infrastructure, or security changes;
8. deployment or other production-affecting actions.

Do not assume that support for one activity implies support for the next.

When no policy is supplied, propose a conservative assessment policy and mark it
`P#` rather than presenting it as an organisational rule. Prefer explicit
pass/fail gates over arbitrary weighted scoring.

## 2. Establish the current operating environment

Inspect the smallest sufficient evidence set, expanding when findings could
change the supported autonomy or remediation order.

### Intent and task contracts

Inspect whether work normally provides:

- a bounded observable outcome;
- acceptance criteria and explicit non-goals;
- constraints, invariants, dependencies, and authority;
- testable behavioural or interface contracts;
- escalation routes for unresolved product, architecture, security, data, or
  operational decisions;
- task sizing and decomposition suitable for the proposed execution model.

A prompt is not automatically a durable specification. Determine whether the
behavioural contract survives individual agent runs and whether changes to it are
human-owned and reviewable.

### Repository comprehension and authority

Inspect:

- repository and area-specific instructions;
- architecture, domain, interface, decision, contribution, and operational
  documentation;
- source-of-truth ownership and conflict-resolution rules;
- code structure, dependency direction, public boundaries, generated artefacts,
  and duplicated policy;
- history and rationale available when current structure cannot explain why a
  constraint exists;
- freshness, consistency, discoverability, and applicable scope of instructions.

Ask whether a competent new engineer, using only available authorised evidence,
could discover how the relevant system works, why important constraints exist,
and whom to contact when evidence is insufficient.

### Reproducible development environment

Inspect whether an authorised executor can reproducibly:

- provision the required toolchain and services;
- restore pinned or locked dependencies;
- obtain safe non-production configuration;
- build the relevant scope;
- run focused and full validation;
- reset or recreate the environment after failure;
- distinguish environmental failure from product failure.

A documented command is stronger when CI or a clean environment demonstrates it.
Record platform assumptions, unavailable services, hidden manual setup, flaky
provisioning, mutable external dependencies, and long or unreliable feedback
loops.

### Verification reach and reliability

Inspect what the environment can actually falsify:

- compilation, schema validation, type checking, linting, formatting, and static
  or security analysis;
- unit, contract, property, integration, end-to-end, migration, performance,
  recovery, and post-deployment checks;
- red/green evidence for new behaviour where applicable;
- characterization tests before risky refactoring;
- test selection, zero-test detection, flakiness, runtime, determinism, and
  isolation;
- traceability from requirements and invariants to checks;
- independent human or agent review for properties executable checks cannot
  establish;
- whether required checks are enforced on the exact revision being approved.

Verification reach sets the autonomy ceiling. Passing existing tests is weak
support when those tests cannot observe the proposed behaviour or protect the
relevant failure modes.

### Architecture and change isolation

Inspect whether the relevant code offers:

- coherent module and service boundaries;
- clear state, rule, and data ownership;
- explicit interfaces and failure semantics;
- limited blast radius for ordinary changes;
- independently testable seams;
- additive or reversible migration paths;
- manageable coupling and integration points;
- safe isolation for concurrent writers.

Do not penalise a repository for lacking fashionable architecture. Assess whether
its actual design lets an agent understand, change, verify, review, integrate,
and reverse bounded work without broad hidden consequences.

### Tools and deterministic controls

Inspect:

- discoverable, documented, and narrowly scoped tools;
- structured input and output contracts;
- read/write separation, validation, rate limits, retries, timeouts, and
  idempotency where relevant;
- hooks, policy checks, protected paths, secret scanning, and required gates;
- whether deterministic controls enforce critical rules outside the model;
- whether tool results, failures, and side effects remain observable;
- whether unavailable live data would force the agent to guess.

Instructions can guide behaviour but are not an authorisation boundary. Prefer
computational controls for rules whose violation would be unsafe or expensive.

### Security, permissions, and isolation

Inspect:

- least-privilege filesystem, network, API, cloud, database, and repository
  access;
- separation of development, test, staging, and production credentials;
- sandboxing of repository-controlled code and untrusted content;
- secret handling, redaction, data retention, and prompt-injection exposure;
- isolated workspaces for concurrent writers;
- approval gates for writes, messages, merges, deployments, purchases, and other
  consequential actions;
- revocation, audit, and break-glass procedures.

The possible blast radius must be proportionate to verification and recovery.
Unknown permissions or ambient credentials are blockers for unattended mutation.

### Workflow, ownership, and human control

Inspect whether the operating model defines:

- who supplies and approves intent;
- who may start, pause, redirect, cancel, or resume work;
- bounded attempts, time, cost, tool use, and no-progress detection;
- independent review and revision-bound approval;
- explicit ownership of architecture, product, security, compliance, data, and
  operational decisions;
- escalation and response expectations;
- rules for stale source material and newly discovered scope;
- separation between evidence, recommendation, approval, and execution.

Humans remain accountable for consequential judgement. A model-generated risk
acceptance, rationale, approval, or completion claim is not a human decision.

### Observability, recovery, and learning

Inspect whether a run can be reconstructed from correlated evidence covering:

- model and instruction versions;
- task and source versions;
- tool calls, handoffs, retries, errors, costs, latency, and termination reason;
- repository or external state before and after consequential actions;
- checks and reviews bound to an exact revision;
- checkpoints, durable state, restart and resume behaviour;
- partial or uncertain side effects and reconciliation;
- rollback or safe-stop procedures;
- outcome feedback and regression fixtures derived from failures.

A chat transcript alone may not prove what acted, what changed, why the run
stopped, or whether the claimed result was independently verified.

### Integration, delivery, and operations

When the target activity reaches beyond a local change, inspect:

- branch protection, required checks, ownership, and integration sequencing;
- conflict detection and coordination for parallel work;
- artefact provenance and supply-chain controls;
- deployment environments, approvals, progressive delivery, health checks,
  rollback, and recovery;
- schema and data migration safety;
- runtime telemetry linked to the change;
- incident handling and production access boundaries.

Do not infer production readiness from repository readiness.

## 3. Use scanners as bounded evidence

A deterministic scanner can accelerate discovery, especially across many
repositories, but its criteria and blind spots must remain visible.

For AgentRC or a similar tool:

- inspect its version, policy, criteria, thresholds, scope, and generated command;
- do not invoke an unpinned `npx`, installer, or downloaded executable merely
  because a wrapper skill suggests it;
- run it only when explicitly authorised and adequately isolated, or consume an
  existing result supplied by the user;
- preserve its raw structured output and tool version;
- map each finding to this skill's evidence dimensions;
- distinguish presence checks from demonstrated effectiveness;
- treat generated maturity levels and weighted scores as tool opinions, not the
  readiness verdict;
- make disabled criteria and policy overrides visible;
- do not hand control to a required custom reporter when the active harness does
  not provide one.

Useful transferable ideas from AgentRC include policy profiles, area-aware
assessment, machine-readable output, drift monitoring, and prioritised
remediation. Its built-in result does not by itself establish specification
quality, test adequacy, least privilege, review independence, recoverability, or
safe autonomous operation.

## 4. Evaluate each readiness dimension

For every applicable dimension, report:

- required control or outcome (`P#`);
- current evidence (`E#`, `I#`, `U#`);
- status: `Supported`, `Partial`, `Unsupported`, or `Unknown`;
- effectiveness, not merely presence;
- risk created by the gap;
- target activities affected;
- cheapest decisive evidence or remediation;
- revalidation check.

Use `Not applicable` only with a reason. Avoid a single percentage by default.
When an organisation mandates scoring, show the weights, thresholds, unknown-data
policy, and sensitivity of the result to those choices.

## 5. Determine supported autonomy

Use these activity-oriented levels as a communication aid, not a universal
maturity ladder:

| Level | Supported operating model |
| --- | --- |
| `A0 — Unsupported mutation` | Evidence is insufficient for agent-authored changes. Limit use to human-controlled discussion or isolated experiments. |
| `A1 — Read-only assistance` | Agents may inspect authorised evidence and produce explanations, investigations, or plans; humans execute consequential actions. |
| `A2 — Supervised edits` | Agents may make bounded changes in an isolated workspace while a human remains in the inner loop and validates every consequential step. |
| `A3 — Bounded implementation` | One ready task may run with explicit budgets, deterministic done checks, independent review, exact-revision gates, and no autonomous merge or deployment. |
| `A4 — Parallel bounded delivery` | Multiple disjoint tasks may execute concurrently with isolated state, explicit dependencies, integration ownership, observability, and conflict controls. |
| `A5 — Governed operational action` | Specific production-affecting actions may occur only within narrowly defined policy, strong approval or automated safety gates, reconciliation, telemetry, and tested recovery. |

Higher is not inherently better. Set an overall cap at the lowest unsupported
control required by the requested activity. Also report per-activity caps when,
for example, documentation work can run at `A3` while schema migrations remain at
`A1` or `A2`.

Apply these hard rules:

- no executable done check means no autonomous implementation loop;
- no safe isolation or least privilege means no unattended mutation;
- no independent, revision-bound verification means no autonomous publication;
- no explicit human authority means no consequential policy or risk decision;
- no observable reconciliation and recovery means no uncertain or operational
  side effect;
- no safe integration model means no parallel writers;
- no credible production verification and rollback means no production action.

Do not average away a hard blocker with strengths in unrelated dimensions.

## 6. Prioritise remediation

Rank improvements by:

1. removal of a hard safety or correctness blocker;
2. increase in verification reach;
3. reduction in blast radius or uncertainty;
4. improvement in reproducibility and feedback speed;
5. reduction of repeated human context reconstruction;
6. support for the requested activity rather than abstract maturity;
7. implementation and maintenance cost;
8. reversibility and evidence available after the change.

Prefer foundational engineering improvements that benefit humans and agents:
reliable tests, reproducible setup, clearer contracts, authoritative
instructions, modular boundaries, least privilege, deterministic gates,
observability, and recovery. Do not recommend adding MCP servers, custom agents,
skills, prompt files, dashboards, or autonomous workflows merely to raise a
readiness score.

For each recommendation state:

- outcome and affected target activity;
- evidence and risk addressed;
- owner or decision authority;
- smallest practical change;
- completion evidence;
- whether it changes the supported autonomy cap;
- dependencies and sequencing;
- important non-goals.

Separate immediate blockers from longer-term enablement. Limit the primary
roadmap to the few changes that materially alter readiness.

## Output contract

Return:

1. **Assessment status** — `Ready`, `Conditional`, `Not ready`, or `Unknown` for
   the named target activity and policy.
2. **Scope and policy** — assessed repository or areas, target activities,
   accountable owners, policy source, evidence window, and limitations.
3. **Supported autonomy** — overall cap, per-activity differences, hard rules
   applied, and why higher levels are unsupported.
4. **Evidence ledger** — compact `E#`, `I#`, `U#`, and `P#` entries with stable
   locators and implications.
5. **Readiness matrix** — each applicable dimension, status, effectiveness,
   affected activities, and decisive missing evidence.
6. **Hard blockers and risks** — ordered by consequence, without averaging them
   into a score.
7. **Prioritised remediation** — smallest sequence that improves the requested
   operating model, with owners and observable completion evidence.
8. **Tool evidence** — optional scanner versions, policies, raw result identity,
   mapped findings, and stated blind spots.
9. **Reassessment contract** — checks, fixtures, incidents, repository changes,
   or time-based triggers that should cause reassessment.
10. **Human decisions** — policy, security, product, architecture, data,
    compliance, or operational choices that automation must not invent.

## Reassessment and drift

Recommend reassessment when material evidence changes, including:

- build, test, CI, deployment, permission, or repository-instruction changes;
- a new agent harness, model family, tool, integration, or autonomy target;
- a major architecture, language, dependency, schema, or platform change;
- repeated agent failure, unsafe behaviour, review escapes, or excessive human
  correction;
- newly available run telemetry or evaluation evidence;
- policy or regulatory changes;
- previously unknown evidence becoming available.

For recurring assessment, compare like with like: pin the policy, target
activities, scanner and harness versions, evidence scope, and unknown-data rules.
A changed score without changed criteria is more meaningful than a score produced
under a different policy.

## Quality gate

Before returning, verify that:

- the assessment names a target activity rather than claiming universal
  readiness;
- every conclusion distinguishes observed evidence, inference, unknowns, and
  policy requirements;
- artefact presence was not mistaken for effectiveness;
- verification reach genuinely supports the proposed autonomy;
- security, least privilege, isolation, human authority, observability, recovery,
  and production boundaries were not diluted by an aggregate score;
- strengths in one area did not hide a hard blocker elsewhere;
- AgentRC or another scanner was treated as bounded evidence with visible policy
  and blind spots;
- recommendations improve the requested operating model and contain observable
  completion evidence;
- no repository or external state was changed;
- uncertainty and unavailable evidence remain explicit.
