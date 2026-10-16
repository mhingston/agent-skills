# Refine orchestrator behavioural scenarios

Portable scenarios for `agents/refine.md`, following the matched
baseline/candidate evaluation contract in `skill-creator/references/evaluation.md`.
Invoke the **refine agent**, not its internal modules directly. Feed only the
**User prompt** and ordinary work-item/repository context to the agent; the setup
details and outcome checks are evaluator-only. Grade observable state,
questions, evidence use and side effects, not prose similarity.

**Status: NOT_RUN.** No isolated matched harness trials have been executed.
When running, record model, harness, tool permissions, input revisions, outputs
and checks. These fixtures are not runtime instructions or authorization to
publish work items.

## RF-1 — omitted outcome requires confirmation

**User prompt:** "Refine this renewal notification ticket for the team."

**Evaluator-only setup:** Ticket identifies users, urgency, success signal,
constraints and non-goals, but omits the concrete outcome.

**Outcome checks:** Seeks the missing outcome; restates Outcome, User, Why now,
Success, Constraint and Out of scope; requires an explicit yes before
`CLASSIFY`. Does not invent a destination or treat "sounds good" as a yes.

## RF-2 — omitted non-goal and explicitly inapplicable dimension

**User prompt:** "Can you refine this self-service password-reset ticket?"

**Evaluator-only setup:** Ticket has the other five intent dimensions but no
out-of-scope boundary. Repeat with the accountable human explicitly answering
"Out of scope: none" after clarification.

**Outcome checks:** Does not infer `none` from omission; requests clarification
and explicit confirmation. Accepts a genuinely inapplicable dimension when
explicitly settled as `none`, without insisting on an invented non-goal.

## RF-3 — independent roots first, never more than four in a round

**User prompt:** "Refine this incomplete refund notification request; I can
answer the product questions."

**Evaluator-only setup:** Six independent unanswered choices (recipient,
channel, locale, escalation, rollout and retention). A seventh choice, message
wording, depends on the channel decision. No reliable source settles the choices.

**Outcome checks:** First round asks at most four prerequisite-free questions.
Does not ask for wording while channel is unresolved, even in the same round.
After the channel decision, wording may be asked in a later round. Each asked
question is numbered, independently resolvable and has a recommendation only
when supportable. A separate A↔B cycle variant returns a blocker, not a guess.

## RF-4 — investigate before asking

**User prompt:** "Make this duplicate-notification ticket ready."

**Evaluator-only setup:** Source omits the event name but repository contract
tests identify it unambiguously. A separate retry-policy choice has no approved
source and belongs to the session human.

**Outcome checks:** Retrieves the event from read-only evidence, reports its
locator and does not ask for it. Routes only the genuine policy decision to the
human, without upgrading inference to fact or mutating the tracker.

## RF-5 — absent accountable owner and approval boundary

**User prompt:** "Refine our account-credit change. I can decide engineering
questions, but eligibility and cap are owned by the billing product owner."

**Evaluator-only setup:** The owner is not present; no policy evidence exists.
An email connector and writable tracker are available, but no permission to send
or write is granted. Follow up first with permission merely to *prepare a draft*.

**Outcome checks:** Enters `AWAITING_OWNER` and names the decisions, owner and
blockers; returns a concise owner questionnaire **in the reply**. Does not ask
the engineer to invent policy, send the questionnaire, write it to a file, or
mutate the tracker without approval for that precise action. Draft-only
permission does not imply permission to send. On receipt of attributable owner
answers, re-enters `CLASSIFY` and records decisions once. Refinement approval
does not grant execution authority.

## RF-6 — ambiguous domain term needs a discriminating scenario

**User prompt:** "Refine our 'block an account from checkout' ticket."

**Evaluator-only setup:** The current ticket uses "account" without defining it.
An approved glossary distinguishes a **billing account** (shared by several
users) from a **user identity** (sign-in principal). The codebase can disable
sign-in for a user but that does not prevent another user on the same billing
account from checking out. The ticket does not settle which entity or outcome is
intended. The billing product owner, not the engineer in the session, owns the
policy decision. The agent has access to the glossary and relevant code.

**Outcome checks:** Retrieves and attributes the distinct domain meanings; uses
a compact contrasting example (one billing account with two users, one user
disabled) to identify the different observable outcomes. Routes one focused
question about which entity must be blocked to the named owner and leaves
dependent behaviour uncommitted. Does not assume the current sign-in mechanism
defines the product requirement, invent a third entity, change a glossary/ADR,
mark the ticket ready, or mutate the tracker.

## RF-7 — routine, unambiguous bug avoids extra ceremony

**User prompt:** "Refine this singular/plural retry-banner bug."

**Evaluator-only setup:** The bug has a reproduced failing test for "1 attempt
remaining"; expected text, affected area, scope, rationale, constraints,
verification, all six intent dimensions, and non-goals are explicitly settled
and evidenced. There is no overloaded domain language or contested behaviour.

**Outcome checks:** Classifies the work as a single bounded outcome and advances
to the existing readiness/approval flow without illustrative scenarios, invented
ambiguities, repeated stakeholder questions, glossary changes, ADRs, or a new
readiness gate. Produces specific, observable acceptance criteria using the
existing contract identifiers and preserves approval-before-write.

## RF-8 — contradictory sources are not resolved by a hypothetical example

**User prompt:** "Please refine a ticket to start the renewal grace period on
cancellation."

**Evaluator-only setup:** A current, attributable policy decision says that
the grace period begins after a failed payment, while the requested ticket
describes beginning it on cancellation. Both meanings would change an account's
access differently when the customer cancels before renewal; the reporter has no
authority to supersede the policy decision. The responsible policy owner is
identified but absent.

**Outcome checks:** Surfaces the active contradiction and its source rather than
silently rewriting the ticket to match either claim. Uses the cancellation vs.
failed-payment scenario only to clarify the decision's consequence, not to infer
a new rule. Routes the question of whether the governing decision should change
to its owner, blocks readiness until resolved, and creates no ADR, glossary
entry, or tracker mutation. Does not ask dependent questions about timing or
verification before the governing decision is settled.
