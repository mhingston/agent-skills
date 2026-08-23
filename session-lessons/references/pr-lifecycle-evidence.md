# Pull-request lifecycle evidence

Use revision-bound pull-request history as longitudinal learning evidence only when the lifecycle can connect a validated finding to the exact remediation and fresh re-review that followed it.

## Evidence chain

For each candidate observation, reconstruct this chain when available:

```text
validated review finding
  -> reviewed head revision
  -> remediation diff or commit
  -> fresh re-review of the new revision
  -> finding closed, falsified, or still present
  -> merge outcome
```

Prefer findings with concrete evidence, falsification attempts, and canonical contract references such as `AC-N` / `NG-N` when applicable. Preserve those contract references so repeated failures can be clustered by behavioural contract rather than file or reviewer wording.

## Evidence rules

- A merge is not proof that the original finding was correct or resolved. Require current re-review or other revision-bound evidence that establishes what changed.
- A reviewer suggestion is not itself the lesson. Inspect the eventual remediation and identify the evidenced failure mode or effective pattern independently.
- Multiple review/remediation rounds on one PR are correlated. Count one PR as at most one evidence unit per root cause, even when several comments or commits describe it.
- A finding later falsified is contradictory evidence, not a successful remediation example.
- Preserve exact PR, finding, base/head revision, remediation revision, and re-review references when available. Do not rely on a final PR summary that omits earlier failure evidence.
- Do not turn one merged PR into a new rule automatically. Feed it into the same recurrence, contradiction, coverage, and promotion gates as session evidence.

## Category mapping

High-signal lifecycle evidence commonly maps to existing observation categories:

- repeated must-fix failure -> `Skill Gap`, `Documentation Gap`, or `Friction`;
- recurring effective remediation or verification technique -> `Effective Pattern`;
- repository fact discovered during remediation -> `Discovery`;
- reviewer finding later disproved -> `Contradictory Evidence`.

## Deduplication and independence

Treat review comments, remediation commits, and re-review rounds from the same root cause as one evidence unit. Sibling PRs from one decomposed task may also be correlated when they share the same cause. Preserve that correlation rather than inflating recurrence.

When the same pattern recurs across independent PRs, retain the PR and revision identities needed to show that independence. When PR evidence and session evidence describe the same underlying event, count the event once and keep both sources as corroboration.

## Learning quality bar

A PR-derived observation should normally record:

- repository and PR identity;
- original finding ID and reviewed revision;
- root-cause summary grounded in the finding evidence;
- canonical `contract_refs` when present;
- remediation revision and behavioural change;
- fresh re-review result or other closure evidence;
- merge outcome;
- category and proposed reusable pattern;
- correlation notes and limitations.

Use merge as an outcome only. If closure evidence is absent, keep the observation unverified or in the watchlist rather than presenting the remediation as learned fact.
