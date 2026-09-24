# Code-modernization behavioural evaluation

Use matched runs when changing `code-modernization` triggering, applicability,
certificate semantics, promotion policy, pilot behaviour, or scale gates. Compare
the candidate against no skill or the previous version under the same model,
harness, repository/project fixture, evidence, and verifier.

Grade routing and outcome behaviour separately. Static validation does not
establish behavioural lift.

## Positive trigger cases

### 1. Cross-language transform with thin legacy tests

**Prompt shape:** A critical COBOL service is being rewritten in Java. The user
wants behaviour preserved, but the original tests cannot run against the Java
implementation and current test coverage is thin.

**Expected behaviour:**

- trigger `code-modernization`;
- classify the work as a transform, not a generic rewrite;
- reconstruct and disposition current behaviour before implementation;
- propose differential/replay evidence, golden/representative fixtures, persistence
  or wire compatibility where relevant, and parallel/staging evidence;
- identify thin tests as a certificate gap rather than assuming parity is
  unprovable;
- define a representative end-to-end pilot before scale.

**Failure:** Treat the Java rewrite as ordinary planning, or declare existing test
suite parity to be the only acceptable oracle even though it cannot run on the
target stack.

### 2. Broad runtime uplift

**Prompt shape:** A large monorepo must move from an end-of-support runtime to the
new supported version while normal development continues.

**Expected behaviour:**

- classify the work as an uplift;
- define target runtime/package constraints and compatibility evidence;
- inspect dependency direction and identify a safe partitioning strategy;
- define freeze/coexistence rules and anti-regression CI for completed partitions
  when appropriate;
- account for reconciliation and review capacity rather than maximizing parallel
  agent count.

**Failure:** Treat each package bump as independent without a programme-level
compatibility or regression boundary.

### 3. Reimagine with changed business behaviour

**Prompt shape:** A legacy claims system is being replaced and stakeholders also
want to change eligibility rules and the customer workflow.

**Expected behaviour:**

- classify changed areas as reimagine;
- require an authoritative behavioural specification and explicit decisions for
  changed/dropped behaviour;
- retain differential checks only for behaviours marked preserve;
- derive certificate evidence from the target specification rather than blindly
  treating the old system as truth.

**Failure:** Force full parity with the old system or let the modernization agent
invent new business rules.

### 4. Pilot passes technically but review capacity collapses

**Setup:** The pilot meets its certificate. Scaling from one to eight concurrent
workers causes review/integration WIP to grow while verified completion stays
flat.

**Expected behaviour:**

- acknowledge that the pilot established useful technical evidence;
- refuse to equate more generated candidates with higher end-to-end throughput;
- reduce admission/concurrency or batch size until verification capacity supports
  scale;
- preserve certificate and human-owned promotion requirements.

**Failure:** Weaken review/certificate gates or recommend more workers because
generation is locally fast.

### 5. Recurring pilot defect

**Setup:** Three pilot slices repeatedly mishandle the same date-normalization edge
case and SMEs manually correct each patch.

**Expected behaviour:**

- classify the repeated issue as a workflow/context/certificate failure;
- improve the owning rule, fixture, oracle, or worker context;
- preserve the escaped case as a regression fixture when valid;
- rerun a representative case before scaling.

**Failure:** Accept manual SME correction as the intended scaled operating model.

### 6. In-place uplift with live development

**Prompt shape:** The system cannot be taken offline and a separate long-lived
modernization branch would drift rapidly from active development.

**Expected behaviour:**

- consider dependency-aware in-place partitions;
- define how a partition becomes frozen/modernized without blocking unrelated
  development;
- add or require compatibility/anti-regression gates for completed partitions;
- make integration ownership and rollback/recovery explicit.

**Failure:** Recommend a repository-wide freeze by default or parallel mutation
without compatibility controls.

## Negative / adjacent-routing cases

### 7. One small dependency bump

**Prompt shape:** Upgrade one library from 4.2 to 4.3, fix the one deprecated API,
and update its focused tests.

**Expected behaviour:** Route to ordinary planning/implementation rather than
starting a modernization programme.

**Failure:** Produce target/certificate/promotion/pilot machinery for a small
bounded change whose existing workflow already owns the outcome.

### 8. Current-system explanation only

**Prompt shape:** "Walk me through how the payment service currently persists a
payment and publishes the settlement event."

**Expected behaviour:** Route primarily to `codebase-walkthrough`.

**Failure:** Invent a modernization target or promotion policy when no
modernization has been requested.

### 9. Agent workflow design only

**Prompt shape:** "Design the state machine, worker handoffs, retries, permissions,
and resumability for our migration agents. The target and verification policy are
already approved."

**Expected behaviour:** Route primarily to `agent-workflow-design`.

**Failure:** Reopen accepted product/modernization decisions merely because the
workflow is agentic.

### 10. One patch review

**Prompt shape:** "Review this PR that ports the serializer to the new runtime."

**Expected behaviour:** Route to the review lifecycle for the exact change.

**Failure:** Replace revision-specific technical review with a programme-level
modernization assessment.

## Adversarial evidence cases

### 11. Observable legacy bug

**Setup:** Differential replay shows the old system returns an incorrect tax value
for one edge case. Product authority confirms the target should fix it.

**Expected behaviour:**

- keep old behaviour as observed evidence;
- mark the behaviour `change` with its authority;
- adapt parity checks so the approved difference is expected;
- do not force the target to reproduce the known bug.

**Failure:** Treat any old/new difference as an automatic regression.

### 12. High model confidence, missing evidence

**Setup:** The worker reports 99% confidence and all self-authored tests pass, but
required replay and persistence round-trip evidence was not run.

**Expected behaviour:**

- keep the certificate incomplete;
- do not promote based on confidence or producer-owned tests;
- report the missing evidence or environment blocker.

**Failure:** Treat confidence as equivalent to independent verification.

### 13. Existing tests pass but external compatibility breaks

**Setup:** All unit tests pass, but the target changes a wire format consumed by an
external service.

**Expected behaviour:**

- fail or block the applicable certificate condition;
- surface the interface/consumer compatibility requirement;
- do not let local green tests override the externally protected contract.

**Failure:** Declare the modernization slice correct because local CI is green.

### 14. Uncertain target-runtime behaviour

**Prompt shape:** A certificate depends on whether a new runtime retries a
particular network operation, but documentation and current code are inconclusive.

**Expected behaviour:**

- keep the claim unknown;
- route the narrow falsifiable question to `code-research` or another bounded
  experiment;
- feed the result back into the modernization certificate.

**Failure:** Guess the runtime semantics or broaden the experiment into a full
modernization execution.

## Success criteria

A strong candidate should improve the rate at which the agent:

- distinguishes uplift, transform, and reimagine;
- separates current behaviour from authoritative target intent;
- creates independent, revision-bound certificate conditions rather than one
  vague score;
- chooses type-appropriate oracles such as differential/replay evidence;
- keeps certificate evidence separate from approval authority;
- excludes model confidence from promotion authority;
- proves the real promotion path on a representative pilot before scale;
- fixes recurring failures in the owning workflow/oracle/context;
- constrains concurrency by verification and accountable-review capacity;
- routes ordinary changes, walkthroughs, workflow design, experiments, and
  revision-specific reviews to their existing owners.

Do not claim behavioural lift from static validation or green CI alone.
