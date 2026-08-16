# Planning Depth and Concern Routing

Use this reference for Standard or Critical work. Apply only the sections whose triggers are present.

## Contents

1. Select depth
2. Bound inspection
3. Route material concerns
4. Plan uncertainty retirement
5. Choose transition patterns
6. Construct useful slices
7. Design verification and recovery

## 1. Select depth

Choose the deepest profile indicated by any material axis. Do not average a high-risk concern away.

| Axis | Focused | Standard | Critical |
| --- | --- | --- | --- |
| Reach | One local responsibility | Several collaborating components | Multiple systems, teams, consumers, or environments |
| Uncertainty | Existing pattern and requirement are clear | Some behaviour or integration must be confirmed | Core requirement, mechanism, or ownership is unresolved |
| Impact | Failure is local and visible | Failure affects a workflow or service | Failure risks data, security, compliance, availability, or public compatibility |
| Reversibility | Simple revert | Coordinated rollback or feature gate | Irreversible mutation, long migration, or external commitment |
| Verification | Fast deterministic checks already exist | New integration or runtime checks are needed | Correctness is hard to observe or recovery is unproven |

Increase depth when repository context is weak, even if the requested change sounds small. Reduce prose, not evidence, for Focused work.

For Critical work, require:

- a named human decision owner for policy or product choices;
- an explicit decision gate for each consequential human-owned choice, including the evidence to review and the dependent work it blocks;
- at least one credible alternative for consequential design decisions;
- explicit intermediate states and gates;
- failure, recovery, rollback, telemetry, and post-change checks;
- an investigation plan instead of speculative implementation wherever a high-impact unknown remains.

Do not introduce phase approvals merely because work is Critical. A gate exists to settle a real decision, not to certify that a document phase happened.

## 2. Bound inspection

Start from the requested behaviour and follow actual dependencies outward:

1. Locate the user-visible or system-visible entry point.
2. Identify maintained durable context that claims to describe the relevant product intent, architecture, ownership, repository conventions, or prior decisions.
3. Trace the normal path to the authoritative rule or state.
4. Trace failure, retry, and cancellation paths.
5. Find tests and executable repository checks for those paths.
6. Identify callers, consumers, schemas, configuration, and deployment units that constrain compatibility.
7. Inspect history only when current evidence does not explain a consequential design choice.

Use durable context to seed the trace, not to terminate it. Record a freshness signal when available and revalidate claims that can materially affect scope, design, safety, compatibility, or verification. When durable context and current authoritative evidence disagree, preserve both observations and treat the discrepancy as drift, an unresolved decision, or a source-authority problem rather than silently selecting whichever is more convenient.

Expand inspection when a newly found boundary can change scope, sequencing, or verification. Stop when additional evidence would only add descriptive detail.

Treat these as evidence-quality warnings:

- documentation and implementation disagree;
- a durable architecture, product, convention, or decision artefact has no usable freshness signal where drift would matter;
- tests assert behaviour different from the issue;
- generated files have an unknown source of truth;
- the apparent interface has undeclared external consumers;
- a migration or rollout command is mentioned but not available;
- the repository lacks a deterministic check for a claimed invariant;
- required state exists only in an inaccessible environment.

## 3. Route material concerns

Include a concern when its trigger is present. Omit it otherwise; do not create a ceremonial section.

| Concern | Include when | Inspect | Plan explicitly |
| --- | --- | --- | --- |
| Product shape | A user-facing workflow, interaction, or product choice can materially change architecture, interfaces, or persistent state | Current journey and behaviour, authoritative product requirements, maintained product context, existing interaction patterns, user evidence, analytics or acceptance signals | User/problem outcome; observable product success evidence or the human-owned metric decision still required; whether a cheap representative sketch/prototype is needed to retire interaction uncertainty before architecture |
| Architecture | Responsibilities, ownership, or dependencies change | Current boundaries, maintained architecture context and ADRs, dependency direction, authoritative rules, nearby patterns | Knowledge ownership, permitted dependencies, change locality, rejected alternatives, and any durable-context conflict that must be resolved |
| Implementation topology | Standard or Critical work where component boundaries, interfaces, or call/data paths are consequential to execution | Existing files and symbols, type and interface definitions, entry points, callers, data/control flow, repository placement conventions | Expected components or files, key types/interfaces, important call/data paths, and ownership boundaries at the minimum detail needed to align execution; exact new signatures only when they are contract-critical and evidence supports constraining them |
| Interfaces | A caller, API, event, command, library, or file format can observe the change | Definitions, consumers, error semantics, versioning, generated clients | Inputs, outputs, invariants, idempotency, ordering, errors, compatibility |
| Data | Persistent shape, meaning, ownership, retention, or volume changes | Schemas, migrations, data access, constraints, backup and restore, representative scale | Expand/backfill/switch/contract stages, integrity checks, recovery, ownership |
| Compatibility | Old and new producers or consumers may coexist | Supported versions, deployment order, serialization, feature negotiation | Compatibility window, adapters or fallback, removal criteria |
| Security and privacy | Trust boundaries, identity, authorization, secrets, personal data, or dependencies change | Threat assumptions, permission checks, secret handling, audit requirements, scanners | Least privilege, deny cases, abuse cases, redaction, security verification, approval |
| Concurrency and failure | Work is asynchronous, retried, distributed, cancellable, or partially applied | State transitions, transaction boundaries, retry policy, deduplication, recovery jobs | Atomicity, idempotency, ordering, timeouts, reconciliation, poison or partial state |
| Operability | Behaviour runs in a service, job, infrastructure, or production workflow | Logs, metrics, traces, alerts, dashboards, runbooks, service objectives | Success/failure signals, thresholds, ownership, diagnosis and recovery path |
| Performance and scale | Latency, throughput, resource use, or cost is a requirement or plausible regression | Baselines, representative loads, bottlenecks, budgets, profiling tools | Measurement method, workload, acceptance threshold, regression gate |
| Testing | Always, scaled to observable risk | Existing test layers, fixtures, commands, flakiness, CI gates | Requirement-to-check mapping, negative and boundary cases, expected signals |
| Documentation | Users, operators, integrators, or maintainers need new non-obvious knowledge | Existing canonical docs, generated docs, examples, runbooks, decision records | Exact audience, source of truth, changed semantics, ownership |
| Deployment | More than a local library edit, or release order matters | Pipeline, environments, flags, health checks, approvals, artifact promotion | Sequence, gate, abort condition, post-deploy check |
| Rollback and recovery | Failure cannot be corrected by a simple code revert | Data compatibility, old artifacts, backups, feature gates, recovery commands | Trigger, authority, exact recoverable state, data reconciliation, validation |

Do not equate mentioning a concern with solving it. Each included concern must change a step, decision, check, or gate.

When **Product shape** is triggered, resolve interaction uncertainty before architecture wherever different plausible journeys would change system boundaries, interfaces, or state. Treat supplied mockups and prototypes as evidence, not authority. If no representative interaction exists and a cheap prototype could retire material uncertainty, plan it as a bounded investigation with an explicit decision rule; the non-mutating planning workflow must not create that prototype itself. Never invent product success thresholds: use observed targets, ask the accountable human when the metric is decision-bearing, or record the missing target as Open.

For Standard or Critical work, record **Implementation topology** only after the relevant product shape and architecture decisions are sufficiently settled. Use the minimum precision needed to align execution: expected components/files, key types or interfaces, important call/data paths, and ownership boundaries. Existing exact signatures can be Observed; proposed locations or signatures are design decisions and must be labelled as such. Do not freeze method-level detail merely to make a plan look complete.

When a human-owned choice blocks dependent work, express it as one explicit decision gate with owner, decision, evidence, blocked dependencies, and evidence-backed state. Gate only the work that truly depends on that choice. Do not substitute a generic “approve requirements/design/tasks” checkpoint for a missing product, architecture, security, migration, rollout, or compatibility decision.

## 4. Plan uncertainty retirement

Use one of four treatments:

| Unknown | Treatment |
| --- | --- |
| Answer exists in accessible evidence | Inspect it before planning dependent work |
| Answer can be learned with a safe, bounded check | Add an investigation step and decision rule |
| Answer is a product, policy, risk, or ownership choice | Ask the responsible human and gate only the dependent work |
| Answer has low impact and is reversible | State an assumption and revalidate before use |

Write an investigation step as a falsifiable experiment:

- **Question:** one decision the evidence must enable.
- **Method:** the cheapest safe inspection, measurement, prototype, or dry run.
- **Bound:** scope, data set, environment, attempts, or timebox chosen by the repository or user.
- **Evidence:** artifact or signal to retain.
- **Decision rule:** how evidence selects a branch.
- **Disposition:** discard experimental code, retain a production-shaped slice, or request a human decision.

Do not let a prototype silently become production code. Do not plan dependent implementation before the gate it relies on.

## 5. Choose transition patterns

Use the smallest transition that preserves a valid intermediate state.

### Local behaviour change

1. Add or identify an executable check that fails for the missing behaviour.
2. Change the owning responsibility without broad cleanup.
3. Run focused deterministic checks, then the relevant wider gate.
4. Update canonical documentation if observable semantics changed.

### Behaviour-preserving refactor

1. Establish characterization or contract coverage.
2. Apply one structural transformation while preserving behaviour.
3. Verify behaviour and the intended structural improvement.
4. Add the new behaviour in a separate slice.

### Interface evolution

1. Add a compatible version, field, or adapter.
2. prove old and new consumers can coexist.
3. migrate producers or consumers in an explicit order.
4. observe use of the old path.
5. remove compatibility only after the exit criterion is met.

### Persistent-data migration

1. Expand storage with additive schema changes.
2. make new writes safe while the old representation remains usable.
3. backfill idempotently with progress and integrity evidence.
4. compare or shadow reads before changing authority.
5. switch reads behind a reversible gate.
6. stop old writes only after the rollback window closes.
7. contract old storage in a later, separately approved slice.

Adapt the sequence to the system; do not prescribe dual writes when transactions, change capture, or a one-shot offline migration is safer.

### Dependency or infrastructure replacement

1. Establish the behaviour, service-level, security, and cost criteria.
2. isolate provider-specific behaviour if it is currently leaked.
3. prove the candidate with representative failure and load cases.
4. introduce it behind a reversible routing boundary.
5. compare old and new signals.
6. cut over gradually with abort conditions.
7. remove the old path only after operational acceptance.

## 6. Construct useful slices

Prefer a slice boundary when it creates one of:

- a testable behaviour;
- a retired high-impact uncertainty;
- a stable interface for dependent work;
- a reversible migration state;
- an operational gate or recovery capability;
- removable temporary compatibility with a clear exit criterion.

Avoid a slice boundary that creates only:

- an empty layer or unused abstraction;
- setup with no consuming outcome;
- documentation detached from the changed behaviour;
- a test task separated from the behaviour it verifies;
- a mechanical file-by-file checklist;
- a state that cannot build, deploy, or roll back.

Represent dependencies explicitly. Parallel execution is safe only when slices do not share mutable state, have stable contracts, and have a planned integration gate. Do not promise parallelism merely because steps appear in separate files.

## 7. Design verification and recovery

For each `R#` and invariant, ask:

1. What incorrect implementation could still look plausible?
2. Which deterministic check would reject it?
3. At what narrowest layer can that check run?
4. Which wider check detects integration regressions?
5. What production signal confirms the assumption under real conditions?
6. If the signal fails, what state is recoverable and who acts?

State an expected signal, not only a command. Examples include:

- a targeted test fails before the change and passes after it;
- a schema validator accepts both rollout versions;
- a type checker reports no new diagnostics;
- an invariant query reports zero mismatches;
- a canary metric remains within an existing service objective;
- a rollback restores the prior read path without losing writes.

Use manual review for product meaning, visual quality, usability, or policy intent after deterministic checks have established what they can. Never use “looks correct” as the sole completion check for machine-verifiable behaviour.
