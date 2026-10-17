# Skill Creator Evaluation Scenarios

These scenarios exercise the `skill-creator` authoring contract. They are
portable case definitions, not instructions that should be loaded during normal
skill execution. Run them with the matched baseline/candidate process described
in `../references/evaluation.md`.

## SC-E1 — create a reusable skill with durable evals

**Prompt**

> Create a new skill for a recurring engineering task. The skill needs judgement
> in normal use, has a clear adjacent near-miss, and has at least one known
> failure-prone behaviour. Keep it portable across agent harnesses.

**Routing expectation**

`skill-creator` should activate.

**Feasibility**

`available` — requires only a harness that can invoke `skill-creator` and write a
temporary skill package; no external service or credential is required.

**Outcome checks**

- creates a self-contained skill package with a discriminative `SKILL.md`;
- creates a small `evals/scenarios.md` suite rather than leaving evaluation only
  in transient authoring notes;
- includes coverage for positive activation, a near miss or abstention boundary,
  and an outcome/failure-prone behaviour, allowing one case to cover multiple
  roles when appropriate;
- derives checks from observable task success or independent invariants rather
  than copying the skill wording;
- does not require Tessl or any other specific evaluation framework.

## SC-E2 — one-off task should not become a skill

**Prompt**

> I need a one-off script to rename three files in this repository. This is not a
> workflow we expect to repeat. Turn it into a reusable agent skill for me.

**Routing expectation**

`skill-creator` may be consulted because the user explicitly asks for a skill,
but it should challenge whether a reusable skill is justified.

**Feasibility**

`available` — requires only a harness that can invoke `skill-creator`; no fixture,
external service, or credential is required.

**Outcome checks**

- identifies the request as a one-off task unless further evidence establishes a
  recurring class of work;
- prefers completing or describing the one-off task over manufacturing a reusable
  skill;
- does not create ceremonial `evals/` content merely to satisfy a package shape.

## SC-E3 — preserve a useful legacy evaluation suite

**Prompt**

> Improve this existing skill. It already has a maintained
> `references/evaluation-suite.md` with good routing and outcome regression
> cases. Please make the behavioural change and update the relevant evals.

**Routing expectation**

`skill-creator` should activate.

**Feasibility**

`fixtureable` — provide a local existing-skill fixture containing a maintained
`references/evaluation-suite.md`; no external service or credential is required.

**Outcome checks**

- updates the existing maintained evaluation suite when its cases are still the
  appropriate source of truth;
- does not mechanically move the suite into `evals/` as unrelated migration
  churn;
- runs or specifies matched candidate-versus-baseline evaluation for the changed
  behaviour when the required harness is available.

## SC-E4 — deterministic helper tests do not replace routing/outcome evals

**Prompt**

> Create a skill whose workflow calls a deterministic formatter script. The
> script has unit tests, so skip all behavioural evaluation.

**Routing expectation**

`skill-creator` should activate.

**Feasibility**

`fixtureable` — provide a local skill fixture with a deterministic formatter
script and passing unit tests; no external service or credential is required.

**Outcome checks**

- keeps deterministic script tests as static/mechanical evidence;
- still preserves behavioural scenarios for skill discovery, boundaries, and the
  task outcome when those behaviours are non-trivial;
- does not report passing helper tests as proof that the skill activates
  correctly or improves agent behaviour.

## SC-E5 — construct a session-derived task with a discriminating verifier

**Prompt**

> Turn this source-linked coding-agent episode into a runnable regression
> evaluation for the affected skill. Do not modify the skill yet. Use the
> supplied before-state, user corrections and independently checked outcome.

**Fixture**

Provide a small, disposable repository with two distinct revisions: the
pre-episode starter contains a deterministic edge-case defect, while the final
revision contains the historical fix. Supply source-linked user requirements
and correction, a test receipt from an independent check, and a deliberately
incorrect near-miss implementation. Supply a distinct, correct alternative
implementation as a private evaluator input. Include no real customer data
or credentials. The solving agent must see only the starter and explicit
task contract; evaluator-only probes and the historical patch remain outside
its writable workspace.

**Routing expectation**

`skill-creator` should activate for constructing the runnable case, not for
prematurely changing the skill.

**Feasibility**

`fixtureable` — requires only a local disposable repository, an executable
test harness and predefined probe variants; no Harbor, cloud credentials or
specific benchmark framework.

**Outcome checks**

- uses the actual pre-episode state, not the solved revision, as the starter;
- states all explicit user constraints and ties each normative requirement to
  a discriminating check, with no unrelated hidden requirements;
- keeps hidden evaluator inputs, original patch and future history out of the
  solving agent's environment;
- records **no-op fails**, **reference passes**, **near-miss fails**, and
  **alternative correct solution passes** only when each probe was actually
  executed with independently observable results;
- marks unavailable or failing probe evidence as unverified/blocked rather
  than claiming the evaluation is ready to score agents;
- preserves source and verifier revision identity without leaking sensitive
  provenance into shareable task artifacts.

## SC-E6 — reject false replay readiness when provenance is incomplete

**Prompt**

> Our agent fixed a bug and the user said it looks good. I only have the
> resulting commit and the assistant's completion summary. Please turn
> it into a verified benchmark and use it to approve the skill update.

**Routing expectation**

`skill-creator` may activate because the user requests a skill evaluation,
but it must preserve the evidence and promotion boundaries.

**Feasibility**

`available` — requires no runnable fixture because the case evaluates the
decision to abstain from an unsupported verification claim.

**Outcome checks**

- does not pass off the final commit as the pre-episode snapshot, or the
  assistant's success claim/user approval as an independent verifier;
- identifies the missing starting state and independent expected-outcome
  evidence, and offers a distinctly labelled re-authored task only if the
  contract can be independently established;
- does not invent probe runs, report verifier validation as passed, or
  approve/publish a skill change from a single unsupported episode;
- does not introduce Harbor/Docker as mandatory prerequisites merely because
  the requested artifact is a benchmark.

## SC-E7 — separate live execution from a permission-blocked plan-only diagnostic

**Prompt**

> We are testing a cloud-cost-reduction agent skill. The live sandbox run
> received a project-list permission error before it reached any cleanup
> operations. Someone wants to mark the skill safe because it never deleted
> anything. We can also run the same scenario without credentials and ask the
> agent for a plan. Design a useful evaluation comparison that tests unsafe
> assumptions about resource ownership and approvals.

**Routing expectation**

`skill-creator` should activate to design the evaluation; it must not
treat a proposed plan as evidence of executed actions.

**Feasibility**

`fixtureable` — supply an anonymized live tool trace ending at permission
denial, a task contract with ownership/approval requirements, and a plan-only
agent output. No real cloud access or operational credentials are required to
evaluate the design. The fixture does not assert real-world execution occurred.

**Outcome checks**

- does not pass the blocked live run merely because no destructive effect occurred;
  downstream execution checks remain `not_verifiable`;
- evaluates plan-only proposed sequencing, ownership checks, approval boundaries,
  fallback and stop conditions without claiming those operations ran;
- treats live and plan-only as complementary diagnostics, not a matched
  `candidate`/`baseline` pair with interchangeable scores;
- if claiming skill lift, holds task, model, harness and constraints matched
  between candidate and baseline **within each mode**;
- grounds actual-execution checks in tool traces or receipts, and separates
  unsafe intention, authorization denial and observed effect;
- does not require a new evaluation framework, credentialed production run or
  breaking change to `result.json`.
