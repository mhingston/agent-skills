---
name: plan
description: Create evidence-grounded, non-mutating implementation and investigation plans for software-engineering work. Use when asked to plan, design, scope, decompose, sequence, or hand off a repository change; assess how an issue or specification should be implemented before code is touched; or cover code, tests, interfaces, migrations, operations, deployment, and rollback in an executable plan. Do not use to implement the change itself.
---

# Plan Software Work

Produce a plan another engineer or agent can execute without rediscovering material context. Treat the plan as a testable hypothesis about the work, not a guarantee about an implementation that has not happened.

## Boundaries

- Inspect repositories, task systems, documentation, history, configuration, and available tooling with read-only actions.
- Do not edit files, install dependencies, create branches, commit, deploy, send messages, or otherwise change repository or external state. Do not run commands expected to create build artifacts unless the user separately authorizes diagnostics.
- Do not drift from planning into implementation, even when the implementation appears trivial. End with a handoff.
- Do not infer the system from filenames, the task description, or one nearby implementation alone.
- Respect repository instructions and permission boundaries. Record unavailable evidence instead of bypassing access controls.
- When the primary task is to reconcile a resumed proposal against prior accepted, rejected, deferred, or superseded decisions rather than plan a repository change, use a decision-continuity workflow when available.

## Evidence discipline

Classify material statements:

- **Observed (`E#`)**: directly supported by repository content, tool output, authoritative documentation, or the user. Cite a stable locator such as a path and symbol, document section, issue field, or command result.
- **Inferred (`I#`)**: a reasoned interpretation of one or more observations. Name the supporting evidence and what could falsify the inference.
- **Assumed (`A#`)**: an unverified premise used to keep planning. State its consequence and when the executor must revalidate it.
- **Open (`Q#`)**: an unresolved question, missing permission, or human-owned decision.

Never present an inference or assumption as observed fact. Prefer authoritative, current, repository-local evidence; explain conflicts and provenance. Use exact paths, symbols, interfaces, commands, and versions only when inspected. Do not invent line numbers, signatures, tests, metrics, schedules, or effort estimates.

For a proposed new artifact, label its name or location as a design decision or inference grounded in observed repository conventions.

## Choose planning depth

Scale depth to the greatest of change size, uncertainty, impact, irreversibility, and weakness of available verification:

| Profile | Typical conditions | Expected treatment |
| --- | --- | --- |
| Focused | Local, familiar, reversible, strong existing checks | Targeted evidence, compact outcome contract, one to three slices |
| Standard | Several components or moderate uncertainty/risk | Current-flow analysis, explicit decisions and dependencies, staged verification |
| Critical | Public contracts, data migration, security, production operations, broad coupling, or costly rollback | Alternatives, transition states, failure model, gates, telemetry, rollout and rollback |

Read [planning-depth.md](references/planning-depth.md) for Standard or Critical work, or when deciding whether a concern is material. Read [agentic-systems.md](references/agentic-systems.md) when models select tools, control loops, delegate work, pause and resume, or initiate consequential external effects. Read [schema-and-ontology-changes.md](references/schema-and-ontology-changes.md) when a machine-readable schema, ontology, taxonomy, controlled vocabulary, or generated domain model is material. Read [examples.md](references/examples.md) only when calibration would improve the plan. Read [evaluation-suite.md](references/evaluation-suite.md) only when validating or revising this skill.

## Workflow

### 1. Parse the request and authority

Extract the requested outcome, supplied acceptance criteria, constraints, explicit exclusions, and referenced sources. Determine which instructions are authoritative when task text, repository documentation, code, tests, and operational configuration disagree. Surface unresolved conflicts.

For resumed work, identify the prior plan, handoff, parent item, ADR, decision register, or explicit human decision that governs continuation. Preserve accepted constraints and rejected alternatives unless materially new evidence supports an explicit reconsideration or supersession proposal. Do not treat the newest draft or implementation as authoritative merely because it is current.

Inventory the tools and permissions needed to inspect relevant evidence. Use available read-only tools directly; report missing access when it limits the plan.

### 2. Establish the current state

Inspect the smallest sufficient evidence set, expanding only when findings justify it:

- applicable repository instructions and relevant architecture or domain documentation;
- manifests, configuration, and the relevant directory and dependency structure;
- current entry points, call paths, data flows, interfaces, state ownership, and failure paths;
- nearby implementations and reusable conventions;
- tests, fixtures, schemas, validation scripts, CI gates, and documented run commands;
- deployment, observability, migration, compatibility, and rollback mechanisms when relevant;
- history or issue context when the reason for the current design affects the change.

Record the evidence that changes the plan. Note dirty or divergent state, stale documents, missing tests, inaccessible systems, and contradictions. Stop gathering context when additional inspection is unlikely to change scope, design, ordering, risk, or verification.

When a machine-readable schema, ontology, taxonomy, controlled vocabulary, or generated domain model is material, identify its authoritative source, derived artifacts, consumers, versioning policy, and validation chain. Distinguish schema validity, instance conformance, vocabulary integrity, generated-artifact consistency, consumer compatibility, and formal semantic consistency; do not treat one validator as evidence for every layer.

### 3. Define the outcome contract

Assign identifiers to material requirements (`R#`) and state:

- intended user or system outcome;
- in-scope behaviour and affected consumers;
- non-goals and excluded cleanup;
- constraints and quality attributes;
- prior decisions and rejected or deferred alternatives that materially constrain this plan;
- invariants that must remain true;
- observable completion criteria.

Describe behaviour before choosing components. Avoid architecture-first planning and speculative generality.

### 4. Retire material uncertainty

Rank unknowns by impact, lateness cost, and reversibility. First inspect evidence that is safely available. Ask a targeted question only when the answer could materially change the outcome, scope, architecture, safety, compatibility, acceptance criteria, or an expensive-to-reverse decision.

Otherwise proceed with an explicit assumption and a revalidation point. For a blocking unknown, produce a bounded investigation step containing:

1. the decision or question;
2. the cheapest safe investigation;
3. required evidence and decision rule;
4. scope or attempt bound;
5. resulting branch in the plan.

Do not disguise “investigate” as an implementation step. If evidence cannot yet support an implementation sequence, return an investigation plan and mark the implementation plan Blocked.

Before finalizing a material requirement or design decision, run a challenge pass: clarify ambiguous terms, expose assumptions, seek counterexamples, test consequences and credible alternatives, and state what evidence would change the conclusion. Ask the user only about resulting gaps that could materially change the plan; record the remainder as explicit assumptions or investigation steps.

### 5. Select the design and transition path

For each consequential decision, compare credible alternatives against current constraints, complexity, coupling, compatibility, security, operability, testability, migration cost, and reversibility. Do not force alternatives for a routine local change.

Do not silently reopen a rejected or deferred alternative. Require materially new evidence, a changed constraint or outcome, a falsified assumption, an elapsed review condition, or an explicit accountable-human request. Record any resulting change of direction as proposed until approved, and identify which dependent artefacts require revalidation.

Describe the chosen responsibilities, knowledge ownership, interfaces, data and control flow, invariants, side effects, failures, concurrency, and compatibility only to the depth relevant to the task. Prefer:

- simple boundaries that hide volatile knowledge;
- one authoritative owner for each rule or state;
- small end-to-end slices over horizontal layers;
- preparatory refactoring separated from behavioural change;
- additive or reversible transition states before destructive cleanup;
- explicit integration and removal of temporary compatibility code.

For Standard or Critical plans, create a compact **responsibility and interface map** before sequencing slices when multiple components, files, services, schemas, or modules must coordinate. Record only boundaries that materially constrain implementation:

- the unit or artifact and its single relevant responsibility;
- what it consumes and from whom;
- what it produces and for whom;
- the stable interface, schema, event, type, command, or state transition joining them;
- whether that contract is observed, inferred, assumed, or newly proposed.

Existing contracts must be evidenced. Proposed contracts are design decisions, not observations. Keep the map at the behavioural/interface level unless exact symbols were inspected and are stable enough to matter. Its purpose is to prevent later slices from silently inventing incompatible names, types, payloads, ownership, or sequencing assumptions.

Each intermediate state must be coherent, verifiable, and safe to stop at.

Measure progress by retired uncertainty, valid intermediate states, and verified outcomes—not by step count, tool calls, files changed, commits, or elapsed agent activity.

### 6. Design verification before sequencing work

Map every requirement and invariant to evidence that would falsify an incorrect implementation. Prefer deterministic checks before inferential or subjective review:

1. schema, parser, or migration validation;
2. compilation and type checking;
3. formatting, linting, static analysis, and security scanning;
4. focused unit, contract, and property tests;
5. integration and end-to-end tests;
6. targeted runtime, telemetry, performance, recovery, and post-deployment checks;
7. manual or semantic review only for properties that executable checks cannot establish.

Define falsifiable behavioural checks before implementation where practical, but do not prescribe test-first or RED/GREEN sequencing as an end in itself. Prefer test-first evidence when it materially strengthens the oracle—for example reproducing a defect, characterizing risky existing behaviour, or preserving a human-approved scenario. Require expected values to come from the requirement, invariant, fixture, contract, or another independent oracle rather than duplicating the production algorithm. Where the repository already provides bounded mutation testing and the risk warrants its cost, consider it as evidence of regression sensitivity; do not add a mutation framework merely to satisfy the plan. Do not prescribe a test type that cannot observe the behaviour, and do not invent a command; cite the discovered command or mark the missing verification route as Open. Treat a script name and its invocation syntax as separate evidence: do not infer a package manager, build runner, or flags from a manifest entry alone.

### 7. Build dependency-aware slices

Order work by prerequisite and risk retirement. Make each step independently understandable and worth verifying. A step must include:

- **Outcome**: the state it creates;
- **Basis**: linked `R#`, `E#`, `I#`, and `A#` identifiers;
- **Why**: why it is needed now;
- **Affects**: evidenced files, symbols, interfaces, data, consumers, or operational surfaces;
- **Work**: the change in behavioural and structural terms, without writing implementation code;
- **Dependencies**: prior steps, decisions, permissions, or external readiness;
- **Consumes**: when another slice supplies a material dependency, the exact behavioural/interface contract this slice relies on;
- **Produces**: when a later slice depends on this one, the behavioural/interface contract this slice establishes;
- **Verify**: exact discovered checks and expected observable signals;
- **End state**: what remains working, deployable, reversible, or intentionally temporary;
- **Replan if**: evidence that invalidates this slice or a dependent assumption.

Omit `Consumes` or `Produces` when no material cross-slice contract exists; do not pad local changes with empty interface ceremony. Where the responsibility and interface map exists, these fields must use the same owner, name, schema/type, semantics, and direction. If implementation is intentionally free to choose the exact symbol or file, state the behavioural contract rather than inventing a signature.

Prefer a few meaningful slices over many mechanical actions. Fold scaffolding, documentation, and configuration into the slice whose outcome needs them. Split where a reviewer could accept one outcome and reject another, where risk needs an independent gate, or where a valid intermediate state enables safe handoff.

Before finalizing the slice sequence, run a **cross-slice consistency pass**:

1. For every producer/consumer pair, compare the contract one slice establishes with the contract the dependent slice expects.
2. Check names, types or schemas, state ownership, error semantics, compatibility assumptions, and ordering where those details are material and evidenced.
3. Check that later slices do not refer to an artifact, interface, or invariant no earlier slice creates or the current system already provides.
4. Resolve contradictions against the outcome contract and authoritative evidence; otherwise mark the disagreement Open rather than choosing silently.

A plan that is locally plausible task-by-task but internally inconsistent across interfaces is not Ready.

### 8. Define execution controls and handoff

Require the executor to revalidate material assumptions and repository state before each dependent slice. If a materially equivalent approach fails twice, or reaches a stricter repository or harness limit, stop retrying; capture the attempted hypothesis, evidence, failure, and next decision, then diagnose, replan, or escalate.

Replan when new evidence changes a requirement, crosses an unapproved subsystem or security boundary, introduces a new public contract or data migration, invalidates verification or rollback, or makes an intermediate state unsafe. Do not silently absorb newly discovered scope.

End after delivering the plan. Implementation requires separate authorization and an execution workflow.

## Output contract

Use the smallest form that preserves these semantics:

1. **Plan status** — `Ready`, `Conditional`, or `Blocked`, with the reason.
2. **Outcome contract** — objective, `R#` requirements and completion criteria, scope, non-goals, constraints, and invariants.
3. **Current-state evidence** — a compact ledger of `E#`, `I#`, `A#`, and `Q#` entries with locators and implications.
4. **Approach and decisions** — selected design, relevant alternatives, transition states, continuity status (`new`, `aligned`, `changed`, `conflicting`, or `blocked`), governing decision references when work is resumed, any explicit supersession proposal, and the responsibility/interface map when required by planning depth.
5. **Implementation slices** — ordered steps using the required fields, explicit dependencies, and material producer/consumer contracts.
6. **Verification map** — trace each `R#` and invariant through its slice to deterministic checks and expected signals.
7. **Operational transition** — migration, documentation, observability, deployment, compatibility, recovery, and rollback only where relevant.
8. **Handoff controls** — assumption revalidation, human decisions, blockers, and replanning triggers.

Focused plans may combine sections, but may not omit traceability, evidence, verification, or revalidation. State “not applicable” only when omission could otherwise be mistaken for an oversight.

## Stop and escalate

Return **Ready** when the plan is executable and no unresolved item can materially change it. Return **Conditional** when bounded assumptions remain but safe revalidation points exist. Return **Blocked** when implementation would be speculative or unsafe.

Escalate rather than guess when:

- authoritative sources conflict;
- required evidence or read permission is unavailable;
- product, policy, compliance, security, or data-retention intent needs a human owner;
- a consequential irreversible choice lacks decision criteria;
- no credible deterministic completion check or recovery path exists for high-impact work;
- newly discovered scope exceeds the authorized task.

Ask only the smallest set of decision-bearing questions. For each, explain why it matters, the known options or default if any, and what part of the plan depends on the answer.

## Quality gate

Before returning the plan, verify that:

- every material requirement maps to one or more slices and observable checks;
- every slice cites evidence, explains its necessity and effects, and ends in a valid state;
- every material producer/consumer relationship is internally consistent across the responsibility/interface map and dependent slices;
- no later slice relies on an artifact, interface, schema, or invariant that is neither already evidenced nor produced earlier in the plan;
- facts, inferences, assumptions, and open questions remain distinguishable;
- material requirements and decisions survive the challenge pass, and user questions remain decision-bearing;
- resumed work traces to governing decisions, preserves rejected alternatives, and exposes any proposed supersession or continuity conflict;
- file and interface details are evidenced rather than guessed;
- deterministic verification precedes subjective evaluation;
- relevant failure, compatibility, security, operational, migration, documentation, deployment, and rollback concerns are covered without checklist padding;
- no implementation, mutation, generic placeholder, false precision, or unsupported promise entered the plan.

Planning quality is bounded by the quality of the available domain and repository context, and maintainers are responsible for keeping that context accurate, current, accessible, and internally consistent.
