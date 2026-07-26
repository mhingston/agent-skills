# Repository ontology operational tooling

This directory contains an optional deterministic guard for repositories that
have already accepted and operationalised part of their repository ontology.
It is not required for ordinary assessment, glossary, taxonomy, concept-model,
or formal-ontology work.

The guard turns a small, explicit JSON constraint profile into repository-boundary
checks suitable for local Git hooks, CI, and agent task-completion gates. It does
not interpret free-form ontology prose, ask an LLM whether code is architecturally
correct, or convert inferred meaning into blocking policy.

## Safety boundary

A rule can block only when both conditions are explicit:

```json
{
  "assertion_status": "confirmed",
  "enforcement": "block"
}
```

`observed`, `inferred`, `disputed`, and `deprecated` rules may be reported as
advisory findings but cannot be configured as blocking rules. Invalid attempts
to do so are structural errors.

The guard is only a validator. A Git hook, required CI check, or other
authoritative boundary must consume its exit code to enforce the result.

## Included capabilities

The initial implementation supports:

- structural validation of the constraint profile;
- explicit observed relationships for language-agnostic use;
- .NET `ProjectReference` extraction as `dependsOn` relationships; enabling
  this extractor makes its configured project inputs mandatory;
- `forbid-relationship`, `require-relationship`, and `require-mapping` rules;
- a semantic-decision gate for material profile changes;
- exact-finding ratchet baselines for brownfield adoption;
- explicit, approved, expiring waivers;
- stable JSON and human-readable reports.

It intentionally does not attempt to infer domain concepts from arbitrary code,
replace compiler or schema checks, enforce runtime transactions, or prove that
an implementation satisfies every natural-language ontology definition.

## Files

```text
repository-ontology/
  README.md
  SKILL.md
  assets/
    constraint-profile.schema.json
    hook-report.schema.json
    examples/
      ontology-guard.json
      decisions.json
      waivers.json
  references/
    enforcement-hooks.md
  scripts/
    ontology-guard.py
    ontology_guard_extract.py
    ontology_guard_model.py
    ontology_guard_policy.py
    test-ontology-guard.py
```

## Quick start

Copy and adapt the example profile into the repository being governed:

```sh
cp repository-ontology/assets/examples/ontology-guard.json .ontology/guard.json
```

Run all checks:

```sh
python3 repository-ontology/scripts/ontology-guard.py check \
  --repo-root . \
  --profile .ontology/guard.json
```

Emit stable JSON for CI or an agent:

```sh
python3 repository-ontology/scripts/ontology-guard.py check \
  --repo-root . \
  --profile .ontology/guard.json \
  --base origin/main \
  --json \
  --output ontology-hook-report.json
```

Exit codes:

| Code | Meaning |
| --- | --- |
| `0` | No blocking findings. Advisory findings may still be present. |
| `1` | A mandatory check rejected, was indeterminate, or was unavailable. |
| `2` | Invalid invocation or unreadable required input. |

## Constraint profile

The profile records the exact ontology version, governed components, optional
extractors, and executable rules. Blocking constraints must use one of the
closed rule kinds implemented by the guard.

A component may declare:

- a stable semantic `id`;
- a governed `type`;
- an explicit `assertion_status`;
- repository path globs;
- an optional `.csproj` path for dependency extraction.

A relationship rule selects endpoints by exact semantic ID or component type:

```json
{
  "id": "ARCH-001",
  "kind": "forbid-relationship",
  "predicate": "dependsOn",
  "subject_type": "presentation-component",
  "object_type": "database-component",
  "assertion_status": "confirmed",
  "enforcement": "block",
  "severity": "error"
}
```

A path-mapping rule checks that matching repository files resolve to exactly one
governed component:

```json
{
  "id": "MAP-001",
  "kind": "require-mapping",
  "path_glob": "src/**/*.csproj",
  "assertion_status": "confirmed",
  "enforcement": "block",
  "severity": "error"
}
```

See `assets/constraint-profile.schema.json` and the example profile for the
complete supported shape.

## Semantic decision gate

When enabled, the guard compares the current profile with the profile at
`--base`. It treats these as material semantic changes:

- component addition or removal;
- component type, path mapping, project mapping, or assertion-status change;
- rule addition, removal, or modification.

Each change must be covered by an accepted decision whose `affects` and
`change_kinds` match the change. The decision file is deliberately separate
from the ontology and executable rules.

```sh
python3 repository-ontology/scripts/ontology-guard.py check \
  --repo-root . \
  --profile .ontology/guard.json \
  --base origin/main \
  --decisions .ontology/decisions.json
```

## Brownfield ratchet

A baseline records exact finding fingerprints that are accepted temporarily as
pre-existing debt. Baseline findings remain visible but do not block. Any new or
materially different finding receives a different fingerprint and blocks
normally.

Generate a proposed baseline explicitly:

```sh
python3 repository-ontology/scripts/ontology-guard.py baseline \
  --repo-root . \
  --profile .ontology/guard.json \
  --output .ontology/baseline.json
```

Review the generated file before committing it. The guard refuses to use a
baseline whose `ontology_version` or canonical `profile_sha256` differs from the
active operational profile.

## Waivers

Waivers apply to one exact finding fingerprint. A valid waiver requires:

- an ID;
- the finding fingerprint;
- a concrete reason;
- an approving human or authority;
- an ISO date after or equal to the current date.

Expired, malformed, or unapproved waivers do not suppress findings. Avoid broad
rule-level or path-level bypasses because they can conceal future violations.

## Integration

### Pre-commit

Run fast checks locally, normally without the decision gate unless an appropriate
base revision is reliably available:

```sh
#!/bin/sh
exec python3 repository-ontology/scripts/ontology-guard.py check \
  --repo-root . \
  --profile .ontology/guard.json
```

Do not overwrite an existing unmanaged Git hook. Prefer the repository's
existing pre-commit framework when one is present.

### CI

CI is the authoritative enforcement boundary because local hooks are bypassable:

```yaml
- name: Validate repository ontology constraints
  run: |
    python3 repository-ontology/scripts/ontology-guard.py check \
      --repo-root . \
      --profile .ontology/guard.json \
      --base "${{ github.event.pull_request.base.sha }}" \
      --json \
      --output ontology-hook-report.json
```

### Agent task completion

An agent may run the same command before claiming completion. The agent should
return the report and propose remediation, a governed ontology change, or a
human decision. It must not edit the validator, weaken a rule, generate its own
approval, or create a waiver merely to make the task pass.

## Development

Run the bundled tests with Python 3.12 or later:

```sh
python3 repository-ontology/scripts/test-ontology-guard.py
```

The implementation uses only the Python standard library.

## Limitations

- The built-in code extractor currently covers only .NET project references.
- JSON Schema assets document the wire contracts; the script also performs its
  own fail-closed structural validation without requiring a schema library.
- Exact baseline and waiver fingerprints intentionally change when the finding's
  governed identity, relationship, rule, or path evidence changes.
- Baselines can suppress only conformance violations; waivers can suppress only
  exact rejected conformance or semantic-decision findings. Missing extractors,
  stale baselines, malformed profiles, and other unavailable context remain blocking.
- Filesystem and Git observations remain repository evidence, not canonical
  domain truth. Their interpretation is governed by the reviewed profile.
