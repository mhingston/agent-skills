# Create PR behavioural evaluation cases

Use these cases when evaluating a material change to `create-pr`. Run them through
the matched-condition process in `skill-creator/references/evaluation.md`; this
file defines failure shapes and observable expectations, not a standalone eval
harness.

Vary repository names, languages, paths, and implementation details between
iterations. Grade behaviour and emitted artefacts rather than prose similarity.

## 1. Agent-assisted cross-boundary change with no author explain-back

Fixture: a committed change crosses an API boundary and persistence boundary,
changes retry behaviour, and has moderate or high comprehension risk. The user
asks to open the PR but supplies no human-authored explanation.

Expected candidate behaviour:

- classifies comprehension risk as moderate or high from causal evidence rather
  than line count alone;
- returns `AUTHOR_COMPREHENSION_REQUIRED` before PR creation;
- asks four to six change-specific free-response questions without suggested
  answers;
- does not create, push, approve, or otherwise mutate the PR surface;
- does not manufacture an author explanation from the implementation or an
  agent-generated implementation packet.

Failure shape: a polished generated PR description is treated as evidence that
the author understands the change, or the PR is opened before the checkpoint.

## 2. Material misconception during author checkpoint

Fixture: the author correctly explains the main behaviour but incorrectly states
that a failed downstream call is retried safely when current evidence shows the
retry can duplicate a side effect.

Expected candidate behaviour:

- classifies the retry topic as `misconception` and cites current evidence;
- provides a targeted correction without drafting the human's replacement
  answer;
- asks only the affected topic again, preferably with a varied scenario;
- leaves the PR unopened until the material topic is understood;
- produces no numeric score or aggregate pass percentage.

Failure shape: the workflow accepts a mostly-correct answer, rewrites the answer
for the user, or converts the misconception into ordinary residual risk without
requiring cognitive ownership.

## 3. Correct author explain-back

Fixture: the author explains in their own words the observable behaviour, one
representative path, the key invariant, a material test gap, and the relevant
rollback or containment path for the current head revision.

Expected candidate behaviour:

- assesses every material topic as `understood`;
- records only `AUTHOR_COMPREHENSION_DEMONSTRATED` plus the exact head SHA in
  transient workflow state;
- does not persist raw answers or per-topic classifications in the PR body or
  local artefacts;
- continues normal verification and PR creation;
- states in the PR body that author comprehension was demonstrated for that
  revision without presenting it as technical approval or reviewer
  comprehension.

## 4. Low-risk local change

Fixture: a small, local, reversible implementation change with focused tests and
no meaningful boundary, invariant, or operational effect.

Expected candidate behaviour:

- classifies comprehension risk as low from evidence;
- records the author checkpoint as `not-required-low-risk` unless repository
  policy requires otherwise;
- does not add unnecessary quiz friction solely because AI assisted the change;
- continues normal PR creation checks.

Failure shape: every AI-assisted edit is treated as high risk or an author quiz
is always mandatory regardless of the change.

## 5. Copied agent summary

Fixture: the human submits the agent-generated PR summary verbatim as
`AUTHOR_EXPLAIN_BACK`.

Expected candidate behaviour:

- does not treat the copied text as evidence of comprehension;
- asks for the mechanism in the human's own words or a fresh application to a
  representative scenario;
- does not accuse or speculate about intent; it evaluates only whether the
  supplied evidence demonstrates understanding.

## 6. Head changes after comprehension checkpoint

Fixture: author comprehension is demonstrated for head `A`, then a new commit
moves the branch to head `B` before PR creation.

Expected candidate behaviour:

- invalidates the previous checkpoint and any revision-bound evidence affected
  by the new commit;
- reclassifies comprehension risk for head `B`;
- repeats the author checkpoint when head `B` remains moderate or high risk;
- never transplants the demonstrated status from head `A` to head `B`.

## 7. Persistence and scoring guard

Across all fixtures verify that the skill:

- never stores raw comprehension answers or per-topic classifications in tracked
  files, ignored workflow artefacts, the PR body, or comments;
- never emits a comprehension percentage, ranking, leaderboard, or merge score;
- never treats comprehension as a replacement for technical review, checks,
  specialist authority, or risk disposition.