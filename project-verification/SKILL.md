---
name: project-verification
description: Establish or refresh a repository-local, agent-readable verification capability that explains how to launch the real product, health-check it, drive user-visible behaviour, capture evidence, verify side effects, and clean up safely. Use when a repository lacks a dependable executable verification path for coding agents or when an existing verification skill/harness has drifted. Do not use for verifying one specific change, diagnosing one concrete failure, or running release approval.
compatibility: Requires read access to the repository. Executable proof requires a safe local or test environment capable of running the relevant product surface without production credentials or uncontrolled external side effects.
---

# Project Verification

Create or maintain a durable verification capability that another agent can read cold and use to prove real product behaviour.

The output is not a test plan for one ticket and not a release verdict. It is repository-local infrastructure for repeatedly answering: **how do I start this product, know I am driving the right instance, exercise behaviour through a real external surface, capture evidence, and clean up what I created?**

## Boundaries

- Preserve existing repository and harness conventions. Do not introduce a new browser runner, test framework, container stack, or agent runtime when an adequate route already exists.
- Do not modify product behaviour merely to make verification easier unless the user separately asks for that implementation work.
- Do not use production credentials, customer data, destructive infrastructure, or uncontrolled external effects to obtain proof.
- A passing unit test, page load, HTTP 200, process start, or model assertion is not by itself proof of user-visible behaviour.
- Prefer real public/user surfaces over internal setters or test-only backdoors. Mocks are acceptable only at an already explicit external boundary and must not replace the behaviour being claimed.
- Never kill processes by broad name or delete shared state. Clean up only instances and scratch state created by the verification run.
- Verification evidence is not approval, release readiness, or product intent.

## Route adjacent work

Use another capability when the primary outcome is:

- verifying acceptance criteria for one implementation: use the implementation workflow and its per-change verification map;
- diagnosing why a concrete bug, regression, flake, or slowdown occurs: use `fault-isolation`;
- testing an uncertain runtime/library/compatibility claim experimentally: use `code-research`;
- running bounded end-to-end acceptance against one deployed or preview revision: use the `qa` agent;
- assessing whether the repository is ready for agent autonomy: use `agent-readiness` and treat missing project verification as one possible remediation finding.

These are routing boundaries, not runtime dependencies. This skill must remain independently installable.

## Choose a mode

Use **establish** when no dependable repository-local verification capability exists.

Use **refresh** when a maintained verification skill, harness guide, feature map, or equivalent already exists and may have drifted.

In both modes, preserve the strongest existing executable mechanisms and make the smallest durable change.

## 1. Interview the repository

Inspect the repository before asking the user for information that can be discovered. Establish:

- **surface** — what users or clients actually touch: web UI, mobile app, desktop app, CLI/TUI, API/service, library, worker, or another externally observable surface;
- **run** — the authoritative local/test startup path, required dependencies, ports, configuration, seed state, and readiness signal;
- **drive** — the existing programmatic route that can exercise the surface: browser/e2e runner, CLI/PTY harness, HTTP client, mobile automation, contract runner, or repository-specific helper;
- **observe** — screenshots, terminal transcripts, responses, logs, traces, files, database state, messages, exit codes, or other evidence that can establish outcomes and side effects;
- **isolate** — how runs avoid corrupting developer sessions or one another: ports, profiles, data directories, fixtures, namespaces, test tenants, disposable processes, or equivalent boundaries;
- **clean up** — how to stop exactly what was started and remove only run-owned scratch state;
- **current verification assets** — tests, scripts, docs, CI commands, existing agent skills, harness adapters, and feature inventories worth reusing.

Treat filenames and README claims as leads until reconciled with executable configuration or code. If the checkout cannot start or the relevant surface is unavailable, report the precise blocker rather than inventing instructions.

## 2. Resolve the repository-local package location

Prefer an already established repository convention for project-local Agent Skills or verification instructions. Keep the generated package portable: canonical instructions must not depend on Cursor-, Claude-, Codex-, or another harness-specific syntax when the underlying action can be described generically.

If no project-local skill location exists, choose the smallest explicit location consistent with repository guidance. Record the choice as a new convention rather than pretending it was observed. Do not create duplicate harness-specific copies; adapters may translate the canonical package when needed.

The verifier name should be specific to the project or primary surface, for example `verify-api`, `verify-cli`, or `verify-web-app`, rather than a generic `verify` when several products share the repository.

## 3. Define the executable verification contract

The maintained verifier must contain concrete, repository-grounded instructions for:

### Launch

- exact command or bounded procedure;
- prerequisites and safe configuration;
- readiness signal;
- how the verifier records the instance it owns;
- teardown for that exact instance.

For short-lived CLIs or libraries, launch may mean build/prepare once and then start each drive independently.

### Doctor

Define one cheap, read-only health check that answers whether the intended instance is safe and useful to drive. Check identity as well as liveness when practical: expected build/revision, port/process ownership, profile, auth/test context, or other distinguishing state.

Run doctor before the first drive, after surprising behaviour, and after any relaunch. A healthy process with a wedged user state may still require reset or relaunch.

### Drive

Document the narrowest existing harness recipe that acts through the real external surface. Use stable handles such as routes, commands, accessible labels, protocol contracts, or explicit test IDs rather than coordinates, timing guesses, or fragile traversal.

For every drive specify the stimulus and the observable end state. Do not claim a behaviour from an action that cannot observe its consequence.

### Evidence

Define what proof to capture and where. Evidence should show both the action and resulting state when those are distinct. Verify material side effects independently where practical: written files, database changes, emitted messages, state transitions, or downstream effects.

Keep proof artefacts separate from cleanup state so teardown cannot erase the evidence. Redact secrets and sensitive records.

### Cleanup

Stop only processes or instances created by the run and remove only run-owned temporary state. Failed iterations require cleanup too. Preserve evidence unless the verifier explicitly classifies it as scratch.

### Safety and limitations

Name external effects, unsupported parallelism, inaccessible features, platform requirements, auth/test-data prerequisites, and any surface that cannot currently be verified safely.

## 4. Maintain a small feature map

Create or refresh an index of the major user/client-visible behaviours the verifier knows how to exercise. Start with roughly three to five high-value features rather than attempting an exhaustive product catalogue.

For each feature record:

- what the user/client can do;
- how to reach it from the external surface;
- prerequisites and representative safe data;
- the exact drive recipe or verifier entry point;
- the observable end state that demonstrates success;
- material side effects or secondary evidence;
- known limitations or unreachable conditions.

The feature map is a verification navigation surface, not product requirements. Source it from current routes, commands, public interfaces, tests, and maintained documentation; do not invent promised behaviour.

## 5. Prove the verifier

For **establish**, execute the maintained instructions end to end for at least one representative mapped feature when the environment permits:

1. launch or prepare;
2. doctor;
3. drive through the external surface;
4. capture the named evidence;
5. corroborate material side effects where applicable;
6. clean up;
7. confirm evidence survived cleanup.

A generated verifier that has not been exercised is `DRAFT_UNVERIFIED`, not a proven capability. If safe execution is unavailable, retain the useful package but report exactly what remains unverified.

For **refresh**, reconcile every mapped feature against current source and executable configuration. Then exercise every safely reachable mapped feature live when the environment and cost permit. Classify unreachable features with the concrete missing prerequisite; do not silently count them as covered. If full live coverage is too expensive or unavailable, report the exact coverage achieved rather than claiming the map is current.

Do not fix a discovered product regression inside this skill. Distinguish:

- **verification drift** — instructions, selectors, commands, health checks, or feature-map claims are stale; update the verifier;
- **harness gap** — current product behaviour exists but cannot be driven or observed reliably; update verification-owned helpers when bounded and safe;
- **product gap** — the product no longer behaves as the maintained contract or authoritative requirement says; report it for implementation/triage;
- **environment gap** — access, platform, dependency, data, or isolation prevents responsible verification.

## 6. Keep maintenance bounded

Do not turn refresh into general product QA or opportunistic refactoring. Change only the verification package and helpers it owns. Prefer one coherent correction set over many cosmetic edits.

When repository behaviour has changed intentionally, update the feature map only when authoritative evidence supports the new behaviour. Do not let the current implementation silently redefine product intent.

## Output contract

Return one status:

- `VERIFICATION_ESTABLISHED` — a repository-local verifier exists and its core path was exercised successfully;
- `VERIFICATION_REFRESHED` — the existing verifier was reconciled and the reported live coverage completed;
- `DRAFT_UNVERIFIED` — useful verifier instructions were created or updated but could not be executed safely;
- `BLOCKED` — a prerequisite prevents a coherent verifier from being established or maintained.

Include:

1. **Surface and scope** — product/surface covered and what remains outside scope.
2. **Verifier location** — canonical repository-local package/instructions and any owned helpers.
3. **Contract** — launch, doctor, drive, evidence, cleanup, and safety summary.
4. **Feature coverage** — mapped features and live/source coverage state.
5. **Proof** — exact representative commands/procedures and observed results, or the reason execution was not run.
6. **Drift/gaps** — verification drift, harness gaps, product gaps, and environment gaps kept separate.
7. **Next smallest improvement** — only when a concrete missing capability materially limits verification.

Read [references/evaluation-suite.md](references/evaluation-suite.md) only when evaluating or revising this skill.