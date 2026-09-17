# Auditing an existing skill

Use this reference when reviewing or improving an existing skill package. Run
mechanical checks before spending semantic-review capacity, then use model
judgement only for questions static analysis cannot establish reliably.

## 1. Run deterministic preflight

Resolve the bundled script from the installed `skill-creator` package and pass the
target skill directory:

```bash
python3 scripts/audit-skill.py <target-skill-dir> --pretty
```

The script emits deterministic JSON describing:

- canonical top-level frontmatter keys and required fields;
- duplicate or unknown top-level frontmatter keys;
- frontmatter-name versus directory-name mismatch;
- `SKILL.md` line count against a configurable review threshold;
- package-local resources referenced by Markdown or common `scripts/`,
  `references/`, and `assets/` paths;
- missing resources, absolute machine-specific paths, and references that escape
  the skill package.

Use `--max-lines 0` when the target repository has no applicable line threshold.
Use `--fail-on error` or `--fail-on warning` only when a caller needs the findings
to become an exit-code gate; the default keeps findings in the report without
turning an audit into an execution failure.

Treat this output as static package evidence. A clean report does not establish
that the skill triggers correctly, that a conditional reference is loaded when
needed, that a script is deterministic under external state, or that the skill
improves task behaviour.

## 2. Spend semantic review on judgement

After repairing mechanical errors, inspect the parts that require contextual
reasoning:

1. **Instructions versus mechanics** — identify repeated transformations,
   extraction, counting, formatting, validation, or other stable operations that
   should become parameterized scripts rather than being reconstructed by the
   model.
2. **Instructions versus enforcement** — for consequential `do` or `do not`
   rules, ask whether a hook, permission boundary, policy engine, CI gate, schema,
   tool contract, or other independent control can enforce the invariant. Keep
   model guidance for judgement; do not describe prose compliance as enforcement.
3. **Discovery cost** — ask whether the skill genuinely needs eager discovery in
   the target harness or can be found through user invocation, catalogue search,
   ranking, or another lazy mechanism. Measure routing and task behaviour rather
   than adopting a catalogue-wide invocation default.
4. **Runtime side effects** — make hooks, permission changes, model or effort
   selection, environment changes, session-persistent state, background work, and
   similar effects explicit and bounded when a runtime supports them. Keep these
   in adapters or runtime configuration rather than adding runtime-specific
   top-level fields to the canonical skill.
5. **Reference boundaries** — check that the parent instructions contain enough
   recognition context to load conditional material at the right time and that
   the boundary can be exercised in a real harness when it matters.
6. **Rule weight** — remove duplicated, generic, or hypothetical defensive prose
   that has no evidenced failure, invariant, or boundary to protect. Do not trade
   away a real exception or recovery rule merely to reduce tokens.

## 3. Keep runtime heuristics evidence-bound

Do not copy runtime-specific limits or frontmatter fields into the canonical skill
contract merely because one harness currently exposes them. Claims about
invocation controls, hook lifetime, cache effects, compaction thresholds, context
forking, model selection, or description limits should be verified against the
current target runtime and represented in its adapter or documentation when they
are material.

Likewise, do not call a script "fully deterministic" solely because it is code.
Network responses, clocks, randomness, mutable files, environment differences,
concurrency, and external services can still make a script nondeterministic. Aim
for deterministic and idempotent behaviour where practical, declare external
inputs, and test consequential edge cases.

## 4. Continue with behavioural evaluation

Static preflight should make semantic review cheaper; it must not replace matched
behavioural evaluation. When the proposed revision changes behaviour materially,
return to the `skill-creator` evaluation workflow and compare the candidate with
the previous skill under the same task, harness, model, environment, and verifier.
