# Assembled context quality

Use this diagnostic when an agent-readiness decision materially depends on the
context packet assembled for a task from repository instructions, retrieval,
tickets, documentation, memory, generated summaries, external systems, or other
sources.

The purpose is to evaluate whether the **context actually handed to the agent is
fit for the target activity**. It is not a replacement for project knowledge
management, retrieval architecture, repository ontology, or the rest of the
agent-readiness assessment.

## Boundary: source quality is not packet quality

Separate these questions:

1. **Does the knowledge exist?** If important intent, constraints, decisions, or
   operational facts live only in people's heads, diagnose the capture or
   project-context problem.
2. **May the agent access it?** Missing authorization or unsafe access is a
   permissions/security problem.
3. **Can the system retrieve it?** Retrieval failure, poor indexing, or missing
   routing is an upstream context-delivery problem.
4. **Is the assembled packet fit for this task?** Only after relevant information
   can be captured, accessed, and retrieved should this diagnostic judge the
   quality of the resulting context.

Do not mark an upstream absence as a context-quality success merely because the
packet is concise. Conversely, do not require one universal context mechanism when
different repositories can assemble fit-for-task context safely in different
ways.

When the packet is dynamic, record enough identity to reproduce the assessment:
target task, relevant source revisions or freshness, retrieval/configuration
version when material, and harness/model version when behaviour is being compared.

## Five properties

Use the CAFE(S) properties as a shared diagnostic vocabulary, not as five weighted
scores.

### Clarity

Ask whether the intended meaning resolves consistently for a competent agent.

Inspect for:

- ambiguous objectives, terms, pronouns, scope, or precedence;
- conflicting instructions with no authority or conflict-resolution rule;
- repository-wide guidance whose applicability to the current area is unclear;
- implicit exceptions or legacy alternatives that look equally valid;
- compressed context that omits distinctions needed to choose safely.

A clarity problem matters when reasonable interpretations would lead to materially
different actions. Do not demand exhaustive prose where code, schemas, tests, or
other authoritative artifacts already resolve the ambiguity.

### Actionability

Ask whether the agent can proceed safely and know when to stop.

Inspect whether the packet contains or resolves:

- the bounded outcome;
- material constraints, invariants, dependencies, and non-goals;
- completion evidence or a falsifiable definition of done;
- authority boundaries and allowed effects;
- stop, retry, and escalation conditions for unresolved decisions or failures.

Do not let the agent invent a convenient definition of done merely to keep moving.
A vague ambition can be useful product intent while still being insufficient for
bounded autonomous implementation.

### Fidelity

Ask whether the material context is true enough to rely on for this task.

Inspect:

- source authority and provenance;
- freshness relative to the repository, deployment, schema, policy, or decision;
- internal consistency and explicit handling of contradictions;
- whether generated summaries preserve uncertainty rather than laundering guesses
  into facts;
- whether retrieved examples or prevalent code patterns are being mistaken for
  approved forward policy;
- whether superseded guidance remains in the packet without being marked as such.

Fidelity is task-relative. A stale historical explanation may be acceptable
background while the same stale value used as a current deployment constraint
would be unsafe.

### Efficiency

Ask whether the packet gives material information enough attention.

Inspect:

- irrelevant repository-wide instructions delivered to every task;
- duplicated guidance, verbose summaries, or repeated source copies;
- large retrieval results where one decisive constraint is buried among low-value
  material;
- obsolete or competing alternatives that remain visible after authority is known;
- context placed globally even though it applies only to one file, component, or
  workflow;
- context expansion that increases token cost and cognitive competition without
  improving decisions.

Prefer **context locality**: broadly applicable guidance belongs at broad scope;
specialized guidance should be delivered close to the area or task that needs it.
The same text can be useful when scoped locally and harmful when injected into
unrelated sessions.

Prefer removal, scoping, indexing, or on-demand retrieval before adding another
global summary. When practical, validate consequential efficiency changes with
representative tasks or an ablation that keeps the task, model, and harness
otherwise comparable.

Efficiency is not merely cost optimization. Excess context can become a
correctness problem when critical information competes unsuccessfully for model
attention. Do not, however, lower autonomy solely because a packet is longer than
an arbitrary token threshold.

### Security

Ask whether every source should be present and how the agent is allowed to
interpret it.

Inspect:

- minimum-necessary access and data exposure;
- secrets, personal data, regulated data, or other content the target activity
  does not require;
- trust labels or equivalent boundaries between authoritative instructions and
  untrusted data;
- prompt-injection exposure in tickets, email, web content, pull requests, logs,
  retrieved documents, and tool output;
- whether untrusted content can redefine policy, authority, tool permissions, or
  completion criteria;
- whether redaction, sandboxing, least privilege, and output controls match the
  possible blast radius.

Treat external or user-controlled content as evidence/data unless an authorized
policy explicitly makes it instructional. Never infer instruction authority from
the fact that content was retrieved into the context window.

## Readiness implications

Map context-quality findings back to the existing readiness dimensions and target
activity rather than creating a separate maturity score.

- **Clarity, actionability, or fidelity** can become a Gate when the ambiguity,
  missing completion contract, or stale/contradictory context prevents safe
  execution of the named activity.
- **Efficiency** is normally an Improvement, but can become a Gate when evidence
  shows that context pollution or placement reliably hides a material constraint
  required for the target activity.
- **Security** can directly Gate access or autonomous action when untrusted content,
  excessive data exposure, or instruction/data confusion creates unacceptable
  blast radius.
- Strong context quality never compensates for missing verification, isolation,
  least privilege, human authority, reconciliation, or recovery.
- Do not raise an autonomy cap merely because a packet scores or appears strong on
  these properties.

When the target activity is low consequence and the packet's weakness cannot
materially change the outcome, record the issue as Improvement or Informational
rather than manufacturing a universal gate.

## Evaluation

For consequential context changes, prefer behavioural evidence over prose review
alone.

A useful comparison keeps the task and relevant environment stable while varying
the context mechanism or packet. Record:

- exact task and expected invariants;
- model/harness and material configuration;
- source/context versions;
- completion correctness and violated invariants;
- unnecessary tool calls, retries, or clarification caused by the packet;
- whether critical facts were missed or untrusted text was followed as policy.

Retain representative failures as regression fixtures when the context mechanism is
used repeatedly. Do not optimize for token count alone; the objective is the
smallest packet that preserves the information needed for safe and correct work.

## Source

This diagnostic adapts the CAFE(S) framework from Brian Houck, Max
Kanat-Alexander, Eirini Kalliamvakou, Margaret-Anne Storey, and Nicole Forsgren,
[CAFE(S): Your Agent Is Only as Good as Its Context](https://getdx.com/research/cafe-s-your-agent-is-only-as-good-as-its-context/),
24 September 2026.

The transferable mechanism is evaluating **assembled task context** across Clarity,
Actionability, Fidelity, Efficiency, and Security after knowledge capture, access,
and retrieval are possible. This skill deliberately does not adopt CAFE(S) as a
numeric measurement system and does not treat high-quality context as sufficient
evidence for autonomy.
