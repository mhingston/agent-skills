---
name: exploratory-qa
description: >
  Perform evidence-led exploratory QA of a deployed RAC feature across Jira,
  linked pull requests, service dependencies, authenticated HTTP behaviour,
  runtime telemetry, and backing data. Use for post-deployment validation,
  cross-service smoke testing, regression checks, or deciding whether a failed
  acceptance criterion is a code defect, data issue, permission problem, or
  deployment/configuration gap. Do not use for unit-test-only work, release
  approval, production health claims without a bounded environment and window,
  or unapproved mutation.
compatibility: Requires access to the relevant RAC repositories and, when live testing is requested, RAC CLI, forwarding or an approved endpoint, authentication, Azure DevOps/Jira access as applicable, and bounded telemetry/data access.
metadata:
  execution: direct-cli
  mutation_policy: explicit-confirmation
---

# Exploratory QA

Validate deployed behaviour against the requirement, not merely deployment health or automated test claims. Treat every result as evidence with an explicit environment, timestamp, request, response, and limitation.

## Use when

- a Jira ticket or linked PRs have reached a deployed test environment;
- a user asks whether a feature works, whether regressions were introduced, or why an acceptance criterion fails;
- the behaviour crosses an API, downstream service, database, queue, identity, or deployment boundary;
- a failure needs classification before deciding whether remediation belongs in application code, configuration, data-platform delivery, access governance, or test data.

## Avoid when

- the request is only to run an existing local test suite;
- the target environment is unspecified or production observability is requested without an exact bounded window;
- the task is release approval, merge approval, a human verdict, or a broad performance/security assessment;
- the proposed action would grant access, change schemas/data, deploy, merge, or update Jira without explicit user authorisation.

## Required inputs and gates

Establish before live testing:

1. Jira issue/key and acceptance criteria, including comments and linked work where available.
2. Linked PRs, repositories, merge state, changed contracts, and stated verification.
3. Exact RAC stage (`dev`, `sit`, `uat`, `pre`, or `prd`) and value stream.
4. Service endpoints, deployment versions, dependency order, and current health.
5. Authentication method and the role/audience needed for each protected endpoint.
6. Test data, expected results, and a bounded telemetry window.

If a required input is missing, use repository or platform discovery when safe. Ask only when the missing choice materially changes the test or risk. Never infer production, an identity, a Snowflake role, or a service endpoint from a similar environment.

Use the specialised skills for their domains:

- Jira reader for requirements, comments, and links;
- Azure DevOps CLI for PRs, commits, builds, and work items;
- RAC deployment triage for versions, health, and endpoints;
- RAC local development for `kubefwd` and reversible local forwarding;
- RAC App Insights logs for bounded service telemetry;
- Snowflake CLI for live object, identity, role, and query validation;
- JITPIM skill for local just-in-time access prerequisites when available;
- review for adversarial code/diff review when a code defect is suspected.

If a live test requires JITPIM access to AKS, Key Vault, App Configuration,
Application Insights, or another protected RAC resource, invoke the standalone
`jitpim` skill for the exact environment and domain before continuing. Do not
reproduce JITPIM implementation details in this skill. If that skill is not
installed, use `raccli-access-governance` for the narrowest supported access
request and report the missing JITPIM capability if the local workflow cannot
be verified. Treat JITPIM requests, LaunchAgent reloads, and access grants as
side effects requiring explicit approval.

## Fast path

1. Extract acceptance criteria into observable behaviours and non-goals.
2. Trace each behaviour through its runtime path: caller → API → downstream services → persistence/data source → response.
3. Confirm deployed versions include the relevant merged changes and that dependencies are available in a safe order.
4. Establish or reuse forwarding without killing existing processes. Record the exact hostnames and ports; cluster-internal DNS is not directly reachable without forwarding.
5. Run a compact matrix:
   - one representative positive case per changed behaviour;
   - one boundary/validation case per changed input;
   - one no-data or unknown-identifier case;
   - one representative existing-behaviour regression case;
   - pagination, ordering, limits, authentication, and error propagation where relevant.
   - for flag- or configuration-dependent behaviour, one case for each meaningful flag variant and one case with the feature path disabled where safe.
   - for every state-writing case, use a unique synthetic identifier or explicit case/version key; reuse a key only when overwrite behaviour is itself under test.
   - declare retention and cleanup before the first write. If cleanup is unavailable, record the residual synthetic data and ensure every case remains individually readable.
6. Capture status code, response shape, important fields, latency where useful, and correlation/request identifiers. Do not print tokens, cookies, personal data, or secrets.
7. Correlate surprising responses across request telemetry, dependencies, exceptions, deployed role/version, and the backing data object.
8. Stop when each criterion is supported or has a concrete blocker. Do not add speculative tests or “fix” a verifier to obtain a pass.

For the repeatable authenticated variant-testing procedure, read
[authenticated-variant-testing.md](references/authenticated-variant-testing.md).

## Authenticated variant testing

Use this procedure when the acceptance criterion depends on a runtime flag,
business attribute, configuration value, or environment-specific branch.

1. Resolve the exact stage, value stream, service endpoint, deployed version,
   client application, target application, required audience, and read-only
   request path.
2. Discover a small set of valid test identifiers through an authorised,
   bounded search or a documented fixture. Select cases using the returned
   business attribute; do not guess identifiers or infer a flag from a similar
   record.
3. Obtain a token only after explicit user approval for the exact client,
   target, stage, and value stream. Use it only in the immediate request. Do
   not print, persist, log, or echo it; take extra care with tools that copy
   tokens to a clipboard.
4. Project responses to non-sensitive evidence: status, correlation ID,
   response shape, changed fields, relevant labels/text, and latency where
   useful. Do not dump full payloads containing personal or operational data.
5. Run the smallest useful matrix: enabled/positive variant, enabled/negative
   variant, disabled or real-provider path when safe, unknown identifier, and
   wrong-environment or not-yet-deployed case when relevant.
6. Assert both the base response and the changed field. A `200` proves neither
   that the intended configuration was active nor that the downstream source
   was correct; verify those separately when the distinction matters.
7. Report candidate-selection evidence, exact request shape without secrets,
   expected versus observed result, deployment/version evidence, and every
   unverified variant.

If a backing data query masks or withholds identifiers, do not try to bypass the
masking. Use the owning service's authorised search endpoint to obtain bounded
candidate identifiers, or report the data-access limitation.

## Forwarding services without ingress

When a service has no public ingress, use a local forwarding path rather than
requesting or creating an ingress:

- prefer an existing healthy `raccli kubefwd <stage>` session when the test
  needs several cluster services or service-name resolution;
- use an exact `kubectl port-forward` when only one deployment/service needs
  direct Swagger or API access;
- check local port ownership first, preserve unrelated forwarding processes,
  and use the exact stage, namespace, workload, and port mapping;
- verify the forwarded endpoint with `/healthz`, `/readyz`, or Swagger before
  testing the feature;
- remember that port-forwarding changes routing only; it does not bypass the
  API's authentication, authorisation, or downstream calls from the pod.

For the direct port-forward and Swagger fallback, read
[no-ingress-forwarding.md](references/no-ingress-forwarding.md).

## Test design rules

Prefer stable, non-destructive, bounded requests. Use real read-only data only when its sensitivity and scope are appropriate. When a feature enriches an existing result, test both the base result and the enrichment field; a successful base response does not prove the enrichment path.

For optional filters, test omitted, paired, partial, invalid, boundary, and over-limit values. For lookup/enrichment features, test a known identifier, an unknown identifier, duplicate-source precedence where applicable, and the exact expected title/value. For pagination, verify stable ordering, cursor pairing, page bounds, and no accidental duplicates across pages.

For write matrices, preserve the nested response or document shape used by the contract when reading back state; do not use a projection that changes the shape under test. Assertions must distinguish missing, `null`, `false`, `0`, empty strings, and empty arrays or objects. Do not use fallback or coalescing operators that treat valid `false` or `0` values as missing.

If a verification helper reports a failure, preserve the initial evidence, validate the helper's projection and parsing semantics, and retain both the original and corrected outcomes before classifying product behaviour.

Treat authentication separately from application behaviour:

- `401`/`403` proves an access boundary response, not feature correctness;
- a token is used only for the immediate bounded request and is never persisted or echoed;
- a user grant does not prove a deployed application identity has the same access;
- an application `200` with an empty or null result still requires downstream/data verification.

## Failure classification

Classify only from evidence:

| Evidence | Likely class | Next check |
|---|---|---|
| Route is absent or response shape contradicts merged code | wrong version, route, or deployment | deployed version, Swagger, commit/image evidence |
| Request is rejected before downstream telemetry | API validation/auth/contract defect | request binding, roles, status and response detail |
| Downstream call is absent | routing, feature wiring, or short-circuit | API dependency telemetry and configuration |
| Downstream returns success but data is empty/null | data, filter, source precedence, or mapping issue | exact query/object and response payload |
| Downstream exception names missing/unauthorised object | effective identity, manifest/grant, or provisioning issue | live role/object metadata and deployment manifest |
| Correct object exists but columns/shape differ | schema contract drift | data-platform source/model/schema and query |
| Base path passes while new field fails | incomplete feature path | enrichment provider and backing data path |
| Existing path fails while changed path passes | regression or environment dependency | before/after contract, logs, and sibling service behaviour |

Do not label an issue “application bug” until configuration, identity, object existence, environment, and data availability have been checked. Do not label it “permissions” when the repository proves the object is not provisioned or the query targets the wrong layer.

## Data-platform and schema checks

When a Snowflake error or empty result is involved, inspect the authoritative data-platform checkout before changing application code. Follow this order:

1. dbt source YAML for source database/schema/table names;
2. `dbt_project.yml` and environment/database/schema macros;
3. model SQL for `source`, `ref`, aliases, filters, and materialisation;
4. model schema YAML and tests;
5. Snowflake DDL and grant scripts;
6. live `INFORMATION_SCHEMA`, session identity, and a small read-only query.

Distinguish raw/source objects (`DATALAKE_<env>_SRC`) from integrated objects (`RACDATA_<env>_INT`). A manifest entry may grant access but does not create a missing database/schema/table; platform provisioning and application access are separate dependencies.

## Reporting

Lead with the outcome: `PASS`, `FAIL`, `PARTIAL`, or `BLOCKED`. Include:

- exact ticket, environment, services, deployment versions, and test window;
- a compact matrix of criterion, request, expected result, observed result, and status;
- regression cases run and their evidence;
- failure classification with the strongest supporting telemetry/data evidence;
- limitations and unverified paths;
- the smallest safe next action and owner boundary.

Separate observed facts, inferences, recommendations, and decisions requiring human judgement. Never claim a feature is working from deployment health alone, and never claim a test ran without command/response evidence.

## Remediation and mutation boundaries

Diagnostics, read-only queries, local forwarding, and test requests are allowed within the stated scope. Creating a branch, editing code/configuration, committing, pushing, or opening a PR requires the user to have requested remediation. Access grants, Snowflake DDL/DML, Jira updates, deployment, merge, rollback, restart, or persistent logging require explicit confirmation immediately before the action and exact target confirmation.

For a suspected code/configuration defect:

1. preserve unrelated work and establish the exact base revision;
2. make the narrowest change at the owning layer;
3. add or update a regression test when practical;
4. run focused automated checks and re-run the failing live case after deployment;
5. review the complete diff and publish a behaviour-first PR with evidence and limitations;
6. do not merge, approve, deploy, or update the tracker unless separately authorised.
