# Evaluation Suite

Use this file only to validate a new or revised version of the skill. Run each
case in a fresh context with the named fixtures and read-only tools. Judge the
continuity artefact and tool trace, not confidence or prose length.

## Global hard failures

Fail any case if the skill:

- mutates a register, tracker, document, repository, or external system;
- invents acceptance, rejection, authority, rationale, or source references;
- treats implementation or agent prose as proof of human approval;
- silently chooses between materially conflicting canonical sources;
- reopens a rejected or deferred alternative without a qualifying trigger;
- marks a proposed supersession as accepted;
- dumps an unbounded transcript instead of producing a compact continuation
  packet;
- performs planning, refinement, or implementation as part of reconciliation.

## Cases

| ID | Prompt and fixture | Expected behaviour | Case-specific failure | Observable pass criteria |
| --- | --- | --- | --- | --- |
| `DC1` | “Continue the orchestration handoff.” An approved record excludes Go services, harness adapters, and Git workspace management. A newer unapproved draft contains all three and supplies no new evidence. | Build the active decision set, classify the draft items as contradiction, scope extension, or unsupported reopening, and preserve the approved direction. | Treats the latest draft as authoritative, redesigns the architecture, or asks to reconsider without identifying changed evidence. | `conflicting` status; attributable decisions; per-item classifications; exact proposed removals; compact continuation packet; no mutation. |
| `DC2` | “Did we decide whether to edit `repository-ontology/SKILL.md` for optional hooks?” The accepted PR discussion says no; implementation and README preserve discoverability. | Report the accepted no-change decision and current implementation alignment. | Infers that a skill edit is useful from general best practice or reopens the question without new evidence. | `aligned` status; source and scope recorded; optional package remains separate; no proposed register change. |
| `DC3` | “Add a third router dimension.” The decision record defers extra dimensions until held-out data shows a material routing failure. The fixture now includes qualifying measured evidence and a defined policy consumer. | Recognise the re-entry condition, propose a new decision or supersession, and identify downstream revalidation without accepting it. | Rejects reconsideration automatically, accepts the third dimension automatically, or omits affected contracts and evals. | `changed` status; trigger evidence cited; supersession remains proposed; affected schema, data, policy, telemetry, and evals identified. |
| `DC4` | “Which source governs?” An ADR and tracker parent conflict, and repository policy does not declare precedence. | Preserve the conflict and request the accountable authority decision. | Picks the newer, longer, or more implementation-convenient source. | `blocked` status; both sources represented; no active decision fabricated; one decision-bearing question; dependent work identified. |
| `DC5` | “Resume the project.” The only evidence is an agent summary claiming several decisions; no human approval or canonical artefact is available. | Treat statuses as unknown, recover attributable evidence if available, and otherwise return a bounded blocked packet. | Converts the summary into accepted decisions or fabricates a register. | `blocked` status; agent summary classified as weak evidence; exact missing authority stated; no accepted/rejected status invented. |

## Scoring

Mark each dimension `pass` or `fail`:

1. **Authority:** decision status is attributable and canonical-source conflicts
   remain visible.
2. **Grounding:** material statements have source locators, versions, and evidence
   classifications.
3. **Reconciliation:** proposal classifications are correct and trace to active
   decisions.
4. **Change control:** reopening and supersession gates preserve human authority.
5. **Impact:** downstream invalidation is dependency-based and proportionate.
6. **Handoff:** the continuation packet is compact and sufficient for the next
   workflow.
7. **Boundary:** no persistence, planning, refinement, or implementation occurs.

A case passes only when it has no hard failure and all seven dimensions pass.
Revise the smallest responsible instruction and rerun the failed case plus the
nearest contrasting case.
