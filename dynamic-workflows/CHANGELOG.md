# Dynamic Workflows Changelog

## 1.0.4 — 2026-11-02

- Specify default run/artifact retention, paused-run expiry, deletion and
  versioned-definition lifetime rules.
- Require pre-persistence redaction of secrets across plans, worker outputs,
  receipts, snapshots, logs and telemetry.
- Define correlated run/step/worker/approval spans and an OpenTelemetry-compatible
  export route using the installed Mastra observability API.
- Normalise CLI, schedule, webhook and chat starts to durable, idempotent run
  identity and the same authority/approval policy.
- Require a minimal durable storage contract while retaining LibSQL as the local
  default.
- Pin reusable steps by version/digest and include their resolved digests in
  workflow definition identity for execution and resume.

## 1.0.3

- Tighten immutable run-definition binding, suspend/resume semantics, cumulative
  budgets and authoritative progress reporting.
