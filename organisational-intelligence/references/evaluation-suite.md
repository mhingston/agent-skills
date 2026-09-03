# Organisational-intelligence evaluation suite

Use matched runs when changing `organisational-intelligence` triggering, evidence
rules, retrieval behaviour, source-authority handling, or decision-brief semantics.
Compare the candidate skill against the previous version using the same model,
harness, connected-source fixture, permissions, and verifier.

The goal is a better decision outcome with calibrated evidence use, not merely
more searching or more citations.

## Core cases

### 1. Undocumented engineering constraint — should hunt tacit traces

Prompt:

> Our deployment script has a 30-second delay that nobody can explain from the
> README or runbook. We have access to GitHub history, engineering chat, incident
> notes, and tickets. Work out why it exists and whether removing it is justified.

Expected behaviour:

- frames the decision as whether the constraint is still necessary rather than
  broadly documenting the deployment system;
- starts from the minimum relevant source and authority map;
- searches not only for the delay itself but for warnings, workarounds, reversals,
  incidents, and exact issue/PR identifiers that could explain it;
- follows promising conversations or reviews far enough to detect later correction
  or reversal;
- distinguishes observed practice and historical rationale from current policy or
  current runtime necessity;
- preserves uncertainty and recommends the smallest resolving experiment when the
  original cause cannot establish present necessity.

Failure signals:

- treats the current README as authoritative merely because it is formal;
- searches only the literal phrase `30 seconds` and concludes from absence;
- promotes one chat message into current architectural truth;
- recommends deleting the delay without current evidence or a bounded test.

### 2. Stale canonical document — should not smooth the contradiction

Prompt:

> The onboarding wiki says service ownership sits with Team A, but recent tickets
> and operational messages repeatedly route incidents to Team B. Tell me who owns
> the service and what we should do about the conflicting records.

Expected behaviour:

- distinguishes documented ownership, operational responsibility, and formal
  authority rather than forcing one global answer;
- records the wiki revision and newer contradictory evidence;
- treats repeated routing or named expertise as evidence of observed practice, not
  automatic formal ownership;
- lowers the stale artefact's authority only for the affected claim/scope rather
  than declaring the whole wiki worthless;
- reports the conflict and identifies the smallest accountable confirmation or
  source repair needed.

Failure signals:

- chooses the newest source automatically;
- chooses the wiki automatically because it is canonical;
- averages the evidence into an invented shared ownership model;
- continues using unrelated unverified statements from the discredited ownership
  section as gap-fillers.

### 3. Important source unavailable — should distinguish not searched from absent

Prompt:

> Reconstruct why a customer-specific billing exception exists. You can search our
> internal docs and tickets, but email with the customer is not connected.

Expected behaviour:

- identifies customer email as a potentially material source for external
  commitments;
- searches the reachable evidence without pretending email was covered;
- labels email as `not searched` or `inaccessible`, not as evidence that no
  commitment exists;
- states how strongly the reachable evidence supports a conclusion without that
  source;
- proposes the smallest recovery action only if the missing source could change the
  decision.

Failure signal:

- says there is no customer commitment because none appears in the searched docs or
  tickets.

### 4. Clear current authoritative answer — should not over-hunt

Prompt:

> Our current approved policy and the live configuration both say refunds over
> £5,000 require Finance approval. I only need to know whether the support team can
> approve one without Finance today.

Expected behaviour:

- answers from the minimum sufficient current authoritative evidence;
- does not launch a broad search for historical exceptions, named experts, or old
  workarounds unless the supplied evidence creates a material reason to doubt the
  rule;
- keeps the result scoped to the current decision.

Failure signal:

- treats tacit-evidence discovery as mandatory ceremony and expands the search even
  though the decision is already sufficiently supported.

### 5. Saturated search — should stop and expose the gap

Prompt:

> We have searched the relevant current docs, tickets, chat threads, and PRs for why
> a legacy integration uses a particular timeout. Two follow-up passes using the
> discovered project names, owners, dates, and issue IDs found no new evidence. We
> still cannot establish the original rationale. What next?

Expected behaviour:

- stops widening retrieval rather than proposing endless query variations;
- reports the rationale as unknown with the searched scope visible;
- distinguishes the absence of evidence from evidence that no rationale existed;
- names the smallest next discriminator, such as a bounded experiment or a precise
  question for an accountable maintainer, when useful.

Failure signal:

- equates search exhaustion with proof that the timeout is unnecessary.
