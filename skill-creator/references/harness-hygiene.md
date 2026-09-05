# Harness Hygiene

Use this reference when the user wants to shrink, simplify, de-duplicate, or reduce
the context cost of an existing skill package or bounded set of independently
installable skills **without intentionally changing behaviour**.

The contract is semantic preservation, not minimum word count. A smaller package
is better only when every material trigger, boundary, invariant, procedure,
recovery path, and output contract still applies in the same circumstances.

## Boundaries

- Treat behaviour change, trigger change, renamed APIs, new policy, or changed
  authority as ordinary skill revision, not hygiene.
- Keep every skill independently installable. Do not eliminate duplication by
  creating runtime dependencies on repository-level shared folders, sibling
  skills, or agent definitions.
- Do not remove guidance merely because a particular model usually knows it.
  Remove it only when it is generic advice that does not encode package-specific
  behaviour and its absence is safe across the target harnesses.
- Do not move material behind a reference unless the parent retains a concrete
  load trigger and the reference boundary can be evaluated when behaviour matters.
- Do not treat static validation or a smaller token count as proof that behaviour
  was preserved.

## 1. Establish the preservation baseline

Before editing, inventory the target package and record:

- public name, description, positive triggers, near misses, and arguments;
- required workflow steps and ordering constraints;
- authority, mutation, approval, and safety boundaries;
- invariants, checks, fallback and stop conditions;
- scripts, references, assets, and every pointer that makes them reachable;
- existing behavioural evaluation cases and important historical regressions;
- line or word count as a cost signal, never as the acceptance oracle.

For several skills, treat each package boundary separately. Cross-package
similarity is evidence for a possible authoring convention, not permission to make
one skill depend on another at runtime.

## 2. Apply the keep/delete test

For each instruction ask:

> If this instruction disappeared, could a conforming agent reasonably behave
> differently on an in-scope task or boundary case?

Keep it when the answer is yes or uncertain. Candidate reductions fall into five
classes.

### Duplicate

Remove a repeated rule when one authoritative statement remains reachable in the
same package and with the same applicability. Do not de-duplicate across package
boundaries by introducing shared runtime content.

### Generic advice

Remove prose such as generic quality exhortations only when it adds no concrete
constraint, decision rule, recovery action, or package-specific interpretation.
A repository convention like `uv run pytest`, an authority boundary, or an exact
size/latency rule is not generic advice.

### Verbose restatement

Collapse multiple sentences that encode one decision into the shortest wording
that preserves its conditions and consequences. Do not compress away exceptions,
provenance, status distinctions, or stop rules.

### Progressive disclosure

Move detail to `references/` only when it is conditional or specialist enough to
earn an extra read. Keep the recognition rule in `SKILL.md` and state exactly
when to load the reference. Prefer a little duplication over a hidden dependency
whose load condition is ambiguous.

### Dead artifact

Delete a script, reference, or asset only after proving that no surviving package
instruction or supported workflow requires it. Search references and inspect
callers; an unreferenced file may still be an intentional user-facing asset, so
uncertainty means flag rather than delete.

## 3. Preserve the semantic map

Maintain a compact old-to-new map for every material reduction:

| Previous behaviour | New home | Preservation evidence |
| --- | --- | --- |
| `<rule or step>` | `<file/section>` | `<why semantics are unchanged>` |

A deleted item needs an explicit reason such as `duplicate of ...` or `generic
non-behavioural advice`. If a material rule has no new home and is not proven
non-behavioural, restore it.

## 4. Verify the candidate

Run static package validation and resolve every remaining relative link. Then
check:

- public name, trigger boundaries, arguments, and output contract are unchanged;
- each old material step, rule, invariant, exception, and recovery path remains;
- moved references have explicit load triggers from the parent;
- scripts and assets still have live callers or an intentional user-facing role;
- no new cross-package runtime dependency was introduced;
- the final package remains within the repository context-budget policy.

When the cleanup moves material behind references or removes instructions that
could plausibly affect decisions, run matched behavioural evaluation against the
pre-clean version when a real harness is available. Include at least:

1. a routine case that should behave identically;
2. a boundary/fallback case that depends on retained constraints;
3. a case that specifically requires any newly disclosed reference.

Prefer exact task outcomes and revision/package diffs over judging whether the
agent used the same wording or reasoning. If no real harness is available, state
that semantic preservation is supported by static inspection only.

## 5. Report the result

Report:

- files changed;
- approximate lines or words before and after;
- material rules moved, merged, or deleted and their disposition;
- references/assets proven live or removed;
- static validation performed;
- behavioural comparison performed, or the missing harness prerequisite;
- any item left unchanged because preservation was uncertain.

Do not claim behavioural equivalence solely from reduced size, valid Markdown,
valid frontmatter, or green package validation.
