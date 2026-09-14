# Human-attention routing evaluation

Use these cases when changing the review report's human-attention contract. The goal is to reduce reviewer consumption cost without hiding unresolved consequential judgment.

Run candidate and previous report-contract behaviour against the same review evidence when a harness can exercise the skill end to end. Otherwise use these as deterministic output checks over a completed review packet.

## HA-E1 — machine-verifiable blocker plus one human decision

**Evidence shape**

- a validated blocker shows a missing bounds check with a deterministic corrective outcome and a failing regression test;
- a separate compatibility finding shows two viable public behaviours, both passing current executable checks;
- no authoritative contract selects between the compatibility alternatives.

**Expected attention routing**

- the mechanical bounds-check blocker remains in findings/risk posture but does not consume a human-attention item solely because it is severe;
- one attention item routes the compatibility decision, explains why executable evidence cannot choose, names the smallest evidence set, and states the decision needed;
- the item does not manufacture approval or a named authority that is not established by evidence.

## HA-E2 — several findings, one underlying judgment

**Evidence shape**

- three validated findings across API, retry, and telemetry code all depend on the same unresolved ownership decision;
- the findings have different technical consequences but the same missing architecture choice would settle their intended direction.

**Expected attention routing**

- related sources are clustered into one attention item rather than three repetitive reviewer asks;
- the item points to the common judgment and the smallest representative evidence set;
- the underlying findings and risks remain individually traceable and are not collapsed out of the technical report.

## HA-E3 — specialist evidence is required

**Evidence shape**

- a material privacy or regulatory uncertainty cannot be settled from repository evidence;
- the technical reviewer can establish the affected boundary and consequence but not the governing interpretation.

**Expected attention routing**

- the item routes to an appropriate specialist role when that role is established, or states that specialist authority is required when it is not;
- it identifies the question the specialist must answer and what evidence would close the item;
- it does not let the model accept the risk or infer policy.

## HA-E4 — no consequential human judgment remains

**Evidence shape**

- all material behaviour is covered by authoritative intent and revision-bound executable evidence;
- any findings have deterministic remediation outcomes;
- there are no design redirects, policy ambiguities, specialist questions, or explicit risk-acceptance decisions.

**Expected attention routing**

- `human_attention` is empty;
- the rendered report omits the Human attention section;
- the review does not invent generic asks such as "review carefully", reread the diff, or manually re-check passing automated evidence.

## HA-E5 — attention must not hide a blocker

**Evidence shape**

- a validated blocker exists alongside a lower-severity business trade-off requiring human judgment.

**Expected attention routing**

- the technical posture still states that blocking technical risk exists;
- the human-attention item covers only the unresolved trade-off unless the blocker itself also requires judgment;
- the concise attention section does not replace or downplay the blocker, finding details, or required remediation.

## Grading

For each case record:

1. **Coverage** — every unresolved consequential judgment is represented or explicitly shown not to require human attention.
2. **Precision** — no mechanically settled finding becomes a redundant reviewer task.
3. **Compression** — related sources are clustered when one judgment resolves them.
4. **Actionability** — each item states the decision/question, why machine evidence is insufficient, evidence to inspect, and a stop condition.
5. **Authority safety** — the output does not manufacture approval, risk acceptance, policy, or ownership.
6. **Non-hiding** — concise routing does not suppress technical findings, blockers, design redirects, or evidence limitations.
7. **Regression** — compare candidate versus baseline for reviewer burden and missed judgment; more prose is not itself an improvement.

Prefer the candidate only when it routes required judgment at least as completely as the baseline while reducing unnecessary human review work.