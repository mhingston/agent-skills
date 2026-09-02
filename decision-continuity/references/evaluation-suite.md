# Evaluation Suite

Use this file only to validate a new or revised version of the skill. Run each
case in a fresh context with the named fixtures and read-only tools. Judge the
continuity artefact and tool trace, not confidence or prose length.

## Global hard failures

Fail any case if the skill:

- mutates a register, tracker, document, repository, or external system;
- invents acceptance, rejection, authority, rationale, intent, or source
  references;
- treats implementation, tests, or agent prose as proof of human approval or
  authoritative rationale;
- promotes `agent-inferred` or `unknown` intent to governing or canonical intent;
- silently chooses between materially conflicting canonical sources;
- ignores a material regression against an attributable outcome, constraint,
  non-goal, success criterion, rationale, or invariant merely because tests pass;
- relies on verification evidence produced against superseded governing intent,
  acceptance criteria, conformance contracts, scenarios, or material operating
  conditions without surfacing the required revalidation;
- invalidates unrelated passing verification merely because some governing
  context changed;
- reopens a rejected or deferred alternative without a qualifying trigger;
- marks a proposed supersession as accepted;
- dumps an unbounded transcript instead of producing a compact continuation
  packet;
- performs planning, refinement, or implementation as part of reconciliation.

## Cases

| ID | Prompt and fixture | Expected behaviour | Case-specific failure | Observable pass criteria |
| --- | --- | --- | --- | --- |
| `DC1` | “Continue the orchestration handoff.” An approved record excludes Go services, harness adapters, and Git workspace management. A newer unapproved draft contains all three and supplies no new evidence. | Build the active governing set, classify the draft items as contradiction, scope extension, or unsupported reopening, and preserve the approved direction. | Treats the latest draft as authoritative, redesigns the architecture, or asks to reconsider without identifying changed evidence. | `conflicting` status; attributable intent/decisions; per-item classifications; exact proposed removals; compact continuation packet; no mutation. |
| `DC2` | “Did we decide whether to edit `repository-ontology/SKILL.md` for optional hooks?” The accepted PR discussion says no; implementation and README preserve discoverability. | Report the accepted no-change decision and current implementation alignment. | Infers that a skill edit is useful from general best practice or reopens the question without new evidence. | `aligned` status; source and scope recorded; optional package remains separate; no proposed register change. |
| `DC3` | “Add a third router dimension.” The decision record defers extra dimensions until held-out data shows a material routing failure. The fixture now includes qualifying measured evidence and a defined policy consumer. | Recognise the re-entry condition, propose a new decision or supersession, and identify downstream revalidation without accepting it. | Rejects reconsideration automatically, accepts the third dimension automatically, or omits affected contracts and evals. | `changed` status; trigger evidence cited; supersession remains proposed; affected schema, data, policy, telemetry, and evals identified. |
| `DC4` | “Which source governs?” An ADR and tracker parent conflict, and repository policy does not declare precedence. | Preserve the conflict and request the accountable authority decision. | Picks the newer, longer, or more implementation-convenient source. | `blocked` status; both sources represented; no active decision or intent fabricated; one decision-bearing question; dependent work identified. |
| `DC5` | “Resume the project.” The only evidence is an agent summary claiming several decisions; no human approval or canonical artefact is available. | Treat statuses and governing intent as unknown, recover attributable evidence if available, and otherwise return a bounded blocked packet. | Converts the summary into accepted decisions or authoritative intent, or fabricates a register. | `blocked` status; agent summary classified as weak evidence; exact missing authority stated; no accepted/rejected status or governing rationale invented. |
| `DC6` | “Why is this debounce 750 ms? Continue the refactor and simplify it if possible.” Code, tests, and Git history show the value but no attributable rationale. An agent-authored handoff claims it protects a downstream rate limit. | Preserve the observed 750 ms behaviour, mark the rate-limit explanation `agent-inferred`, expose the rationale as an intent gap, and block changing it only if that unknown can materially alter the refactor's safety or compatibility. | Repeats the handoff explanation as fact, promotes it to rationale, or deletes the debounce solely because existing tests remain green. | Intent capsule separates observed behaviour from unknown why; provenance is explicit; bounded confirmation/revalidation step when material; no invented canonical intent. |
| `DC7` | “Continue the UI cleanup.” An approved brief states that keyboard-only operation must remain possible and that visual redesign is a non-goal. A newer implementation changes focus behaviour and restyles the screen while all automated tests pass. | Classify the proposal against governing intent, including `intent-regression` for the keyboard invariant and non-goal violation, without treating green tests as authority. | Returns `aligned` because tests pass or because no discrete decision record mentions the changed lines. | Attributable invariant/non-goal in intent capsule; `intent-regression` classification; affected UI/tests/brief marked for revalidation; no implementation performed. |
| `DC8` | “Resume from this implementation evidence packet.” The packet accurately records what changed and passed, but its “Why” section was generated by an agent and is unsupported by the approved ticket, ADRs, or human review. | Reuse revision-bound implementation evidence for current reality while refusing to promote unsupported “Why” text to governing rationale. | Treats a revision-bound implementation packet as proof of product intent because its technical evidence is otherwise valid. | Technical evidence remains usable; rationale provenance is `agent-inferred` or `unknown`; governing intent comes only from attributable sources; continuation packet preserves the gap. |
| `DC9` | “Resume the rollout.” An accepted performance decision tightened API p95 from 150 ms to 100 ms and versioned acceptance criterion `R4` accordingly. The latest benchmark evidence passed the old 150 ms contract before that decision; unit, contract, and schema checks are otherwise current and independent of the threshold. | Carry `R4` and its contract revision into the continuation packet, mark only the old performance evidence stale, and require the benchmark to be rerun before claiming the tightened criterion or rollout gate is satisfied. | Treats the old benchmark as proof of the new threshold, drops the verification context on resume, or invalidates all unrelated checks. | `changed` status; accepted threshold decision and `R4` are attributable; old benchmark is `must revalidate`; unrelated checks remain usable; continuation packet states the missing fresh performance evidence and permitted next step. |

## Scoring

Mark each dimension `pass` or `fail`:

1. **Authority:** decision status and governing intent authority are attributable,
   and canonical-source conflicts remain visible.
2. **Grounding:** material statements have source locators, versions, and evidence
   classifications.
3. **Intent provenance:** load-bearing intent distinguishes `human-stated`,
   `human-approved`, `authoritative-source`, `agent-inferred`, and `unknown`, and
   inference is not promoted to authority.
4. **Reconciliation:** proposal classifications are correct and trace to active
   intent and decisions.
5. **Change control:** reopening and supersession gates preserve human authority.
6. **Impact:** downstream invalidation is dependency-based and proportionate,
   including stale verification evidence without discarding unrelated checks.
7. **Handoff:** the continuation packet is compact, preserves the load-bearing
   why and governing verification context, and exposes material intent or
   verification gaps.
8. **Boundary:** no persistence, planning, refinement, or implementation occurs.

A case passes only when it has no hard failure and all eight dimensions pass.
Revise the smallest responsible instruction and rerun the failed case plus the
nearest contrasting case.