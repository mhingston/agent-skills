# Authenticated variant testing

Use this reference for deployed API behaviour that changes according to a flag,
business attribute, configuration value, or environment.

## Inputs

Record these before making a protected request:

- ticket and acceptance criteria;
- exact stage and value stream;
- service and endpoint;
- deployed version or commit evidence;
- approved client application and target application;
- required role/audience;
- bounded search criterion or approved fixture;
- variant field and expected response difference.

## Candidate discovery

Prefer a read-only search endpoint owned by the service under test or its
authoritative dependency. Keep the search bounded with a real non-sensitive
criterion and a small result limit. For each candidate, record only the
identifier and the business attribute needed to select the test case.

Do not use an unconstrained production or test-data scan. Do not manufacture a
policy/customer/claim identifier. If a direct warehouse query returns masked
identifiers, use the authorised application search path or report that the
identifier cannot be materialised.

## Token handling

Token acquisition is a governed step, even when the command is technically
read-only. Require explicit approval for the exact target before running the
RAC access-token command:

```text
raccli access token <value-stream> <stage> <client-app> <target-app>
```

Use the resulting token only in the immediate bounded request. Keep it in
process memory or an ephemeral shell variable, never in a file, command log,
response, screenshot, or final report. Some RAC CLI versions copy the token to
the clipboard; clear or overwrite that clipboard state after use according to
local policy.

## Request matrix

Run only the cases justified by the acceptance criteria:

| Case | Selection | Expected evidence |
|---|---|---|
| Positive variant | Known record with the flag/attribute enabled | Changed response field uses enabled behaviour |
| Negative variant | Known record with the flag/attribute disabled | Changed response field uses disabled behaviour |
| Provider/config boundary | Feature disabled, real provider selected, or configuration absent | Mock/alternate path is not used, or the documented fallback is observed |
| Unknown identifier | Bounded nonexistent identifier | Documented `404`, empty result, or validation response; no false positive |
| Environment boundary | Same request against a stage without the deployed change | Version skew or unchanged behaviour is recorded, not treated as a feature result |

Avoid mutating endpoints unless the user explicitly authorises the exact test
data and rollback. Prefer response assertions over snapshots of full payloads.

## Evidence and assertions

For each request capture:

- server timestamp and stage;
- endpoint and non-sensitive request parameters;
- HTTP status and correlation/request ID;
- deployed service version;
- selected business attribute;
- changed response fields or stable text fragments;
- expected result and pass/fail status;
- limitations, especially unverified configuration or dependency state.

Separate these claims:

1. The endpoint returned the expected variant.
2. The selected record had the expected business attribute.
3. The intended runtime flag/configuration was active.
4. The dependency and data source were healthy and authoritative.

Only claim each one when its evidence supports it. A successful response can
support the first claim while leaving the latter claims unverified.
