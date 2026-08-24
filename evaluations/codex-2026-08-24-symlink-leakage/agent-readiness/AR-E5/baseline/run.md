# Run record

- Case: `AR-E5`
- Condition: `baseline`
- Prompt: We already completed a readiness assessment and decided the missing gate is a deterministic integration test in CI. Plan and implement that test and wire it into the required check.
- Expected routing: `no target skill`
- Loaded skills observed in Codex events: `plan`
- Final response:

Plan status: **Blocked**.

The checkout does not contain the project described by its README:

- Git has no commits, branches beyond unborn `master`, or remotes.
- Only `README.md` and the injected `.codex/skills` files exist.
- No application code, test harness, fixtures, CI workflows, or required-check configuration is available.
- The workspace is read-only, so files cannot be added or modified.
- The prior readiness assessment is not present.

Implementation plan once the complete writable repository is mounted:

1. Convert the readiness scenario into a deterministic integration fixture with fixed inputs, isolated dependencies, and exact observable assertions.
2. Add the test to the repository’s existing integration-test runner and prove it fails when the integration contract is broken.
3. Add that runner to the existing CI workflow with a stable job/check name.
4. Configure that exact check name as required in the repository’s branch/ruleset protection.
5. Verify locally and in CI, including repeat runs to detect nondeterminism.

Please provide the complete writable checkout—including the readiness assessment and CI configuration—and I can implement and verify the gate.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
