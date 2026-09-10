# Codebase-walkthrough evaluation suite

Use matched runs when changing `codebase-walkthrough` triggering, routing, evidence handling, or output semantics. Compare the candidate with no skill or the previous version under the same repository fixture, model, tools, and verifier.

## Positive trigger cases

### 1. Onboard to an unfamiliar subsystem

**Prompt**

> I'm new to this service. Walk me through how an incoming order gets validated, persisted, and published to downstream consumers, including where each responsibility lives.

**Expected**

- trigger `codebase-walkthrough`;
- establish concrete entry points, persistence, and message boundaries;
- explain in runtime/data-flow order rather than file order;
- produce a compact ownership/interface map;
- mark unsupported rationale or ownership as inferred/unknown.

### 2. Placement question

**Prompt**

> I need to add validation for this field. Before I change anything, show me which layer currently owns this rule and which callers depend on it.

**Expected**

- trigger `codebase-walkthrough`;
- inspect current ownership, interfaces, and callers;
- answer from observed boundaries rather than generic architecture preference;
- finish with a small preserve / likely change point / verify-before-editing orientation;
- do not drift into a full plan or implementation.

### 3. Cross-service flow

**Prompt**

> How does a completed upload move from the API through storage, the queue, and the worker until the result becomes visible to the client?

**Expected**

- use subsystem or cross-system depth;
- trace state, messages, ordering, and externally visible completion;
- inspect only material paths and stop once the requested outcome is explained;
- disclose unresolved retry/idempotency semantics rather than guessing.

### 4. Small local question

**Prompt**

> How does `TokenBucket.TryAcquire` work and who calls it?

**Expected**

- use focused depth without unnecessary fan-out;
- explain the symbol, state, immediate callers, and important edge behaviour;
- avoid broad repository history or architecture analysis unless evidence makes it necessary.

## Negative / adjacent-routing cases

### 5. Concrete bug diagnosis

**Prompt**

> Requests occasionally get duplicated after a timeout. Reproduce the failure and tell me the root cause.

**Expected**

- route primarily to `fault-isolation`;
- do not use a walkthrough as a substitute for a reproducible symptom signal and causal probes.

### 6. Experimental runtime claim

**Prompt**

> Does this HTTP client retry POST requests after a connection reset in version 8.2? Prove it rather than relying on docs.

**Expected**

- route primarily to `code-research`;
- do not turn `codebase-walkthrough` into an experiment harness.

### 7. Durable context

**Prompt**

> Build a maintained project context record for future agents with source authority, architecture, decisions, and current intent.

**Expected**

- route primarily to `project-context`;
- a walkthrough may supply temporary current-state evidence but does not own the durable substrate.

### 8. Measured learning

**Prompt**

> Teach me this subsystem and quiz me until I can explain it back and transfer the concepts to a new scenario.

**Expected**

- route primarily to `teach-me`;
- do not treat a good explanation as evidence of durable learner understanding.

### 9. Exact PR comprehension

**Prompt**

> For PR #92, explain exactly what changed, the new runtime path, risks, and what I should understand before reviewing it.

**Expected**

- route to the PR-review lifecycle when that exact revision-bound comprehension outcome is requested;
- do not replace the internal `explain-diff` stage with a generic codebase walkthrough.

### 10. Architecture planning

**Prompt**

> Design where our new pricing capability should live and compare two architecture options before implementation.

**Expected**

- route primarily to `plan` with architecture handling as appropriate;
- current-state walkthrough evidence may be useful, but the skill does not own design selection.

## Adversarial evidence cases

### 11. Documentation disagrees with code

**Setup**

- README says requests go directly to a worker;
- current source routes them through a queue and an adapter;
- no evidence establishes whether the README or implementation expresses intended future direction.

**Expected**

- describe current observed runtime flow from code/configuration;
- flag documentation drift/contradiction;
- do not infer intent from either source without authority evidence.

### 12. Misleading folder names

**Setup**

- a folder named `domain/` contains transport DTOs;
- domain rules actually live in a separate package.

**Expected**

- derive ownership from behaviour, interfaces, and callers rather than path names;
- avoid repeating architectural labels that the repository does not substantiate.

### 13. Complex repository with tempting overreach

**Setup**

- target request crosses two services;
- repository contains twelve unrelated services and several shared libraries.

**Expected**

- inspect only dependencies that materially affect the requested flow;
- do not read or summarize the whole monorepo;
- name excluded surfaces and the stop condition.

## Success criteria

A strong run should demonstrate all of the following:

- explanations follow runtime/data flow rather than file order;
- observed behaviour, inferred interpretation, historical rationale, and unknowns stay distinct;
- ownership and placement claims are grounded in real interfaces and consumers;
- simple questions avoid unnecessary orchestration;
- broad questions remain bounded by a representative path and stop condition;
- diagnosis, experimentation, durable context, tutoring, exact-PR explanation, and design retain their existing owners;
- contradictions remain visible instead of being reconciled into a smooth but unsupported story.