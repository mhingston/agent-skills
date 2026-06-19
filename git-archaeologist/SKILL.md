---
name: git-archaeologist
description: Analyze a repository's git history before reading implementation details. Use git metadata to identify risk areas, ownership patterns, defect hotspots, maintenance health, and investigation priorities. Load when auditing a codebase, onboarding to an unfamiliar repository, assessing technical debt, evaluating team health, or being assigned a large repository with little context.
---

# Git Archaeologist

Analyze a repository's history before reading implementation details. Use Git metadata to identify risk areas, ownership patterns, defect hotspots, maintenance health, and investigation priorities.

## When to Trigger

- User asks for a codebase audit
- User asks where to start in an unfamiliar repository
- User asks for technical debt assessment
- User asks why development is slow
- User asks for onboarding guidance
- Agent is assigned a large repository with little context

## Workflow

### Phase 1: Churn Analysis

Run:

```bash
git log --format=format: --name-only --since="1 year ago" \
  | sort | uniq -c | sort -nr | head -20
```

Goal:

- Identify most frequently modified files
- Detect potential "fear files"
- Flag components with excessive change frequency

Output:

```yaml
high_churn_files:
  - path: src/payment_processor.rb
    churn_rank: 1
    investigation_priority: high
```

### Phase 2: Ownership Analysis

Run:

```bash
git shortlog -sn --no-merges
```

And:

```bash
git shortlog -sn --no-merges --since="6 months ago"
```

Goal:

- Estimate bus factor
- Identify knowledge concentration
- Detect departed key contributors

Output:

```yaml
ownership:
  dominant_author_percentage: 67
  bus_factor_risk: high
  departed_experts:
    - Alice Smith
```

### Phase 3: Defect Hotspot Detection

Run:

```bash
git log -i -E \
  --grep="fix|bug|broken" \
  --name-only \
  --format='' \
  | sort | uniq -c | sort -nr | head -20
```

Goal:

- Identify files repeatedly associated with fixes
- Correlate with churn data

Output:

```yaml
bug_hotspots:
  - src/payment_processor.rb
  - src/subscription_service.rb
```

### Phase 4: Risk Correlation

Cross-reference:

```text
High Churn ∩ High Bug Frequency
```

Classify:

| Condition              | Risk     |
| ---------------------- | -------- |
| High churn + high bugs | Critical |
| High churn only        | Medium   |
| High bugs only         | High     |
| Neither                | Low      |

Output:

```yaml
critical_risk_areas:
  - src/payment_processor.rb
```

### Phase 5: Development Velocity

Run:

```bash
git log --format='%ad' --date=format:'%Y-%m' \
  | sort | uniq -c
```

Analyze:

- Increasing activity
- Declining activity
- Release spikes
- Team disruption indicators

Output:

```yaml
velocity:
  trend: declining
  suspected_event: major contributor departure
```

### Phase 6: Firefighting Detection

Run:

```bash
git log --oneline --since="1 year ago" \
  | grep -iE 'revert|hotfix|emergency|rollback'
```

Goal:

- Detect operational instability
- Estimate deployment confidence

Output:

```yaml
operations:
  hotfix_count: 18
  rollback_count: 6
  stability_assessment: poor
```

## Final Report

### Executive Summary

- Bus factor assessment
- Top risk modules
- Defect concentration areas
- Team health indicators
- Deployment maturity indicators

### Recommended Reading Order

Read files in this priority:

1. High churn + high bug files
2. High churn files
3. Core ownership files
4. Remaining codebase

### Suggested Actions

- Refactor hotspot files
- Add tests around defect clusters
- Reduce ownership concentration
- Investigate recurring rollback causes

## Success Criteria

The agent can answer:

- Which files are most dangerous?
- Which files deserve attention first?
- Who understands the system?
- Is the project healthy?
- Is the team firefighting?
- Where should a new engineer begin?
