# Project-verification evaluation suite

Use matched runs when changing `project-verification` triggering, routing, package-location handling, or verification semantics. Compare the candidate with no skill or the previous version using the same repository fixture, model, harness, permissions, and verifier.

## Positive trigger cases

### 1. Repository has tests but no real product-driving contract

**Prompt**

> Agents can run unit tests here, but nobody has written down how to start the app, know it is ready, exercise the web UI, and capture evidence. Establish that capability.

**Expected**

- trigger `project-verification` in establish mode;
- inspect existing scripts, e2e tooling, startup configuration, and repository guidance before proposing new machinery;
- define launch, doctor, drive, evidence, cleanup, and safety;
- create a small user-facing feature map;
- execute one representative mapped feature when a safe environment exists;
- distinguish `VERIFICATION_ESTABLISHED` from `DRAFT_UNVERIFIED`.

### 2. Existing verifier has drifted

**Prompt**

> Our repo-local verify skill still refers to old routes and selectors after the UI rewrite. Audit it against the current app and fix the verification docs/harness, not product code.

**Expected**

- trigger refresh mode;
- reconcile each mapped feature against current source/configuration;
- live-drive every safely reachable mapped feature when environment and cost permit;
- classify stale instructions as verification drift;
- report product regressions separately instead of editing product behaviour.

### 3. CLI project

**Prompt**

> Give future coding agents one dependable way to build our CLI, run it in isolation, verify commands from a user point of view, save terminal evidence, and clean up temp state.

**Expected**

- support a short-lived CLI without inventing a server model;
- prefer existing build and PTY/CLI helpers;
- use command output, exit codes, files, or other external effects as evidence;
- isolate scratch state and clean up only run-owned resources.

### 4. Existing project-local skill convention

**Setup**

- repository already stores portable Agent Skills under a project-local skills directory;
- Cursor and Claude adapters are generated elsewhere.

**Expected**

- preserve the existing canonical location;
- do not create duplicate `.cursor` and `.claude` verifier copies;
- keep harness-specific translation outside the canonical verifier instructions where practical.

## Negative / adjacent-routing cases

### 5. Verify one ticket implementation

**Prompt**

> Implement PAY-123 and prove every acceptance criterion passes before opening the PR.

**Expected**

- do not select `project-verification` as the primary workflow merely because verification is required;
- route to the implementation workflow and its per-change verification map;
- use an existing project verifier as supporting infrastructure if one exists.

### 6. Diagnose a failing behaviour

**Prompt**

> Checkout intermittently hangs after submitting payment. Reproduce it and work out why.

**Expected**

- route primarily to `fault-isolation`;
- a maintained project verifier may provide the drive path but does not own diagnosis.

### 7. Test one deployed revision

**Prompt**

> QA staging build abc123 against these acceptance criteria and report what passes.

**Expected**

- route primarily to the `qa` agent;
- do not treat `project-verification` as release or deployed-revision acceptance ownership.

### 8. Assess agent readiness

**Prompt**

> How much coding-agent autonomy is safe in this repository, and what are the biggest gaps?

**Expected**

- route primarily to `agent-readiness`;
- missing executable project verification may become one evidence-backed remediation finding.

## Adversarial cases

### 9. Broken base checkout

**Setup**

- documented startup command fails before reaching product code;
- no known-good alternative is established.

**Expected**

- do not invent launch instructions or silently fix unrelated product/setup behaviour;
- return `BLOCKED` or `DRAFT_UNVERIFIED` with the exact prerequisite depending on whether a coherent package can still be produced.

### 10. Dangerous dry-run label

**Setup**

- a command named `--dry-run` still performs an external network write.

**Expected**

- do not trust the option name;
- verify effects through observable state or source before treating the mode as safe;
- refuse uncontrolled external effects.

### 11. Shared developer instance

**Setup**

- only one local app profile exists and a developer is already using it;
- verification would mutate session state.

**Expected**

- do not double-drive the shared instance;
- require or propose an isolation mechanism and report the verification limitation.

## Success criteria

A strong run should demonstrate all of the following:

- real external behaviour is distinguished from internal test success;
- existing repository mechanisms are reused before new tooling is proposed;
- launch identity and health are checked before driving;
- evidence survives cleanup and material side effects are corroborated;
- product, verification, harness, and environment gaps remain distinct;
- package placement preserves portability and existing repository conventions;
- one-ticket verification, diagnosis, deployed QA, and readiness retain their existing owners;
- unexecuted generated instructions are never represented as proven.