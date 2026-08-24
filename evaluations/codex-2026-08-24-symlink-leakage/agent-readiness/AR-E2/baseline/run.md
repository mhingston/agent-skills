# Run record

- Case: `AR-E2`
- Condition: `baseline`
- Prompt: Our coding agent usually produces plausible patches, but reviewers keep finding hidden integration problems and sometimes the local test command passes while CI fails. Before we tune prompts or switch models, work out whether the repository and delivery environment are actually set up for reliable agent changes.
- Expected routing: `agent-readiness`
- Loaded skills observed in Codex events: `none`
- Final response:

The repository is not currently set up for reliable agent changes. More precisely, this checkout is not an assessable delivery repository, so changing prompts or models would be premature.

The highest safe autonomy here is read-only analysis. Automated code changes should be blocked until the repository substrate exists.

Key evidence:

- Git has no commits or valid `HEAD`.
- Nothing is tracked. Even [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-le4w4hi7/repo/README.md:1) is untracked.
- There is no application source, test suite, build definition, dependency manifest, lockfile, toolchain pin, container definition, or CI configuration.
- There is no `AGENTS.md` or equivalent repository-specific operating guidance.
- There is no canonical local command corresponding to CI.
- The README describes an expected catalogue structure—such as `agents/` and `<skill-name>/SKILL.md`—but that structure is absent from this checkout.
- The three `.codex/skills` entries are absolute symlinks into `/home/mark/Projects/agent-skills`. They are machine-specific, untracked, and non-portable.
- The documented `.agent-artifacts` convention requires that directory to be ignored, but no `.gitignore` or matching ignore rule exists.
- This execution environment is read-only and network-restricted. It cannot represent an agent expected to edit files, restore remote dependencies, or exercise hosted integrations.

This means the reported “local tests pass, CI fails” problem cannot be investigated from the supplied checkout. There is neither a local test command nor CI whose behavior can be compared. The likely immediate problem is one of these:

1. The wrong or incomplete repository was supplied.
2. Repository bootstrap and CI configuration exist elsewhere but were omitted.
3. The team relies on undocumented developer-machine state.
4. The delivery environment is assembled dynamically without a revision-bound, reproducible contract.

Before tuning the agent, establish these minimum gates:

- A real, committed baseline with source and tests.
- One canonical verification entry point, such as `make verify` or `./scripts/ci`, used unchanged both locally and in CI.
- Pinned runtime and dependency versions, with committed lockfiles.
- A clean-checkout bootstrap test in an environment matching CI.
- Explicit CI definitions checked into the repository.
- Tests for integration boundaries—not merely isolated unit behavior—including database/schema, generated artifacts, packaging, configuration, and external-service contracts as applicable.
- Repository guidance describing architecture, permitted change boundaries, required commands, generated files, secrets policy, and completion criteria.
- A pre-handoff gate that runs from the exact candidate revision and records command, environment, exit status, and tested commit SHA.
- CI that rejects dirty generated output, missing migrations, lockfile drift, platform assumptions, and test selection differences.
- Portable skill/tool configuration rather than absolute links to one developer’s filesystem.

The acceptance test for readiness should be simple: clone the exact revision into a clean CI-equivalent environment, run one documented bootstrap command and one documented verification command, and obtain the same result locally and in CI without undeclared files, credentials, caches, or global tools.

Until that passes, reviewer-found integration defects are primarily a repository and delivery-system signal—not strong evidence that the model or prompt is the bottleneck.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
