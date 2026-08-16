# Agent-Native Evaluation

Read this file when setting up, running, grading, or reviewing a skill evaluation.

## Contents

1. [Principles](#principles)
2. [Define realistic cases](#1-define-realistic-cases)
3. [Prepare matched conditions](#2-prepare-matched-conditions)
4. [Execute with the agent](#3-execute-with-the-agent)
5. [Separate routing from outcome quality](#4-separate-routing-from-outcome-quality)
6. [Grade from evidence](#5-grade-from-evidence)
7. [Compare and report](#6-compare-and-report)
8. [Iterate without overfitting](#7-iterate-without-overfitting)
9. [Environment limitations](#environment-limitations)

## Principles

- Evaluate task outcomes, not whether the agent mentioned or loaded the skill.
- Run matched pairs: change the skill condition and hold everything else constant.
- Use the current agent harness directly. Do not require an eval framework, provider adapter, CLI, or language runtime.
- Isolate each run from prior context, files, caches, and other skill variants.
- Prefer deterministic checks for objective properties and human judgment for genuinely subjective quality.
- Record the harness and model. Do not assume results transfer to another harness.
- Preserve prompts, inputs, outputs, checks, and results so another agent can reproduce the comparison.
- Standardize result files only when deterministic aggregation earns its overhead; do not turn the result format into a required execution framework.
- For evidence-sensitive skills, test whether unsupported, ambiguous, conflicting, missing, and stale evidence remains distinguishable when those states materially change the answer.
- For discipline-enforcing skills, observe the shortcut or rationalisation before adding guidance intended to prevent it.
- Treat description-shortcut behaviour as harness-specific until measured; metadata that works well for routing may still be a lossy substitute for the full body in some runtimes.

## 1. Define realistic cases

Start with two or three cases:

- a routine case;
- a boundary, fallback, or dependency-failure case;
- a format, invariant, or domain-quirk case likely to expose mistakes.

For each case, record:

- a short name;
- the exact user prompt;
- input files or setup;
- expected outcome;
- objective checks;
- subjective qualities requiring review.

For a discipline-enforcing skill, add pressure cases only where the pressure
models a credible deployed failure mode. Examples include:

- time pressure that makes a required verification or review gate inconvenient;
- sunk cost that makes discarding or revising an incorrect approach unattractive;
- an apparently obvious quick fix that tempts action before diagnosis;
- reviewer or tool advice that conflicts with authoritative local evidence;
- incomplete evidence that tempts a plausible but unsupported completion;
- a direct request to skip a safety, approval, verification, or provenance gate.

Prefer one pressure variable per case when possible so the failure is
interpretable. Run the baseline before adding a new countermeasure and capture
what the agent actually did or said: the skipped gate, substituted evidence,
unsupported inference, or rationalisation. Do not manufacture a catalogue of
hypothetical excuses and then grade the skill against its own wording.

For evidence-sensitive skills, include adversarial cases when they exercise a
material failure mode. Useful cases include:

- a plausible conventional answer that is absent from the supplied evidence;
- two materially different interpretations that are both consistent with the
  evidence;
- authoritative sources that disagree;
- incomplete evidence that strongly tempts a conventional inference;
- stale evidence whose age or supersession changes the result;
- a task where the correct output is an explicit unknown, preserved ambiguity,
  conflict, or request for the smallest resolving evidence.

Do not create artificial ambiguity merely to increase test count. The case should
represent a realistic way the deployed skill could produce false certainty.

Keep a small validation set for iteration. Reserve a final test set that is not consulted while revising the skill when an unbiased final measurement matters.

## 2. Prepare matched conditions

Use two conceptual conditions for every pair:

- `candidate` — for a new skill, the with-skill condition; for a revision, the proposed version;
- `baseline` — for a new skill, no skill; for a revision, a snapshot of the previous version.

Use a simple workspace when artifacts need to persist:

```text
<workspace>/
  iteration-1/
    <case-name>/
      trial-1/
        candidate/
          outputs/
          run.md
          result.json
        baseline/
          outputs/
          run.md
          result.json
```

The directory layout is a convention, not a required interface. For small evals, an inline table plus linked output artifacts is sufficient.

Record enough metadata to reproduce every run. When a portable machine-readable result is useful, use [evaluation-results.md](evaluation-results.md), which defines the `candidate` and `baseline` result schema and the invariants required for safe aggregation.

Use `null` when the harness does not expose a metric. Do not fabricate precision.

## 3. Execute with the agent

Run both sides with the same prompt, files, model, harness, permissions, tool access, resource limits, and external conditions.

For each condition:

1. Start from a fresh context and isolated workspace.
2. Expose only the intended skill version. Do not leave candidate and baseline copies discoverable together.
3. Give the task, inputs, output destination, and required deliverables.
4. Do not reveal expected answers, the intended improvement, or the other condition's result.
5. Save the final outputs and a concise execution record, including errors, fallbacks, uncertainties, skipped gates, and any explicit shortcut rationale.

When independent agents or fresh tasks are available and authorized, use them for cleaner isolation. Otherwise run sequentially in the current task and disclose that the author also executed the eval.

Repeat the complete matched pair at least three times when model variance or the consequences justify it. Pair trials by case and execution conditions; never pool unmatched runs.

## 4. Separate routing from outcome quality

Outcome evaluation may explicitly provide the skill path so the test measures whether the skill improves the work.

Routing evaluation asks whether the deployment harness discovers the skill from its metadata. Test it separately with:

- clear positive prompts;
- indirect or uncommon valid prompts;
- difficult near-misses;
- sibling-skill conflicts when relevant.

Routing is inherently harness-specific. Record how discovery was observed. If the harness cannot expose actual discovery behavior, label a direct classification exercise as a surrogate rather than presenting it as an end-to-end routing test.

When a description contains a condensed workflow, or traces suggest the runtime
may act from metadata without consulting the full skill, add a separate
**description-shortcut test**. Keep the body, prompt, model, harness, and tools
constant. Compare the current workflow-summary description with a semantically
equivalent trigger-and-boundary description. Measure two outcomes independently:

1. **Activation:** did the harness select the skill for valid prompts and avoid near misses?
2. **Body fidelity:** did execution follow material instructions that exist only in the body, rather than behaving as if the description were the entire skill?

Do not infer body loading merely because the final answer looks reasonable. Use a
material body-only requirement whose observance can be checked without revealing
the expected result to the agent. A classifier-only experiment can inform
activation wording but cannot establish body fidelity.

## 5. Grade from evidence

Apply the same checks to both conditions.

Prefer deterministic evidence:

- required files and fields exist;
- output parses in the target consumer;
- exact format constraints hold;
- tests, validators, or build checks pass;
- algorithmic invariants and plausibility bounds hold;
- unsafe or unsupported inputs fail clearly;
- the documented fallback works.

For discipline-enforcing tasks, grade the behavioural gate rather than the
agent's stated understanding. Examples include whether it actually ran the
required verification, diagnosed before modifying, preserved an approval
boundary, rejected unsupported reviewer advice, or surfaced the missing evidence.
Record the concrete baseline shortcut and whether the candidate closes that same
failure without introducing a more expensive or broader failure elsewhere.

For evidence-sensitive tasks, add claim-level checks where practical:

- material factual claims have attributable supporting evidence;
- cited evidence actually supports the claim rather than merely mentioning the
  same topic;
- inference remains distinguishable from direct observation;
- materially different interpretations remain visible when evidence cannot
  discriminate between them;
- authoritative conflicts are preserved rather than averaged into a single
  narrative;
- insufficient evidence produces an appropriate unknown, abstention, or bounded
  investigation step rather than a plausible completion;
- freshness-sensitive claims do not silently rely on stale or superseded evidence;
- confidence language does not exceed the evidence state.

Treat an unsupported material claim as a substantive failure even when it sounds
plausible and the rest of the answer is useful. Treat over-abstention as a failure
when the evidence does establish the answer; the goal is calibrated use of
evidence, not universal caution.

If an objective check will recur, encode it as a deterministic verifier using a runtime already justified for the evaluated skill. Define its inputs, outputs, exit behavior, and dependencies. Do not introduce a runtime solely to support the eval.

For each check, record `passed`, `failed`, or `not_verifiable` with specific evidence. Treat `not_verifiable` as a gap, not a pass.

Use human review for qualities such as clarity, usefulness, aesthetics, or tone. For a blind comparison, label outputs A and B and hide their condition until after the judgment.

## 6. Compare and report

The agent should calculate and report:

- passed checks over total verifiable checks for each condition;
- paired wins, losses, and ties;
- absolute pass-rate delta;
- variation across repeated trials;
- wall-clock and token tradeoffs when available;
- non-discriminating or unverifiable checks;
- failures caused by overhead, bad applicability boundaries, brittle procedures, or unchecked assumptions;
- observed shortcut/rationalisation failures and whether the candidate closed them;
- description activation and body-fidelity differences when a shortcut test was run;
- evidence-calibration failures such as unsupported claims, false certainty, collapsed ambiguity, conflict smoothing, or unnecessary abstention;
- differences by harness or model.

For a few runs, show the arithmetic directly. For a larger portable workspace, use the optional standard-library helper described in [evaluation-results.md](evaluation-results.md) when Python 3 is already available. Otherwise use an available deterministic calculator or spreadsheet, but keep the source results portable and readable.

The helper validates pair integrity before aggregation; it is not an execution harness, grader, or substitute for inspecting outputs and trajectories.

Do not claim improvement from a high standalone score. Require paired evidence, meaningful output review, or both.

## 7. Iterate without overfitting

Inspect trajectories and outputs, identify the smallest generalizable change, and rerun the full validation set. Do not add task-specific answers or verifier details to the skill.

For discipline failures, prefer this loop:

1. observe the baseline shortcut under a realistic case;
2. identify the smallest missing principle, gate, or discriminating instruction;
3. change the skill without embedding the case answer;
4. rerun the original case and the wider validation set;
5. add another countermeasure only if a materially different failure is then observed.

Do not turn every imaginable rationalisation into permanent skill text. Defensive
guidance must earn its context cost through observed failures, credible incidents,
or another concrete risk signal.

Stop when:

- the candidate shows meaningful lift without unacceptable cost;
- the candidate regresses and the evidence does not support another general change;
- user feedback is satisfied;
- further iterations no longer produce meaningful improvement.

Run the untouched final test set once after selecting the candidate when unbiased reporting matters.

## Environment limitations

- If baseline isolation is impossible, prioritize deterministic artifact checks and human review over a misleading numeric comparison.
- If only one harness is available, scope conclusions to that harness.
- If the harness cannot expose skill discovery or body loading, report the description-shortcut test as unavailable rather than inferring it from prose quality.
- If metrics are unavailable, omit them.
- If Python is unavailable, aggregate directly or with another deterministic tool already present; do not add a runtime solely for the optional helper.
- If no browser or display is available, present results as Markdown and link directly to artifacts.
- If the installed skill is read-only, copy the baseline to a writable temporary workspace and preserve its original name.
