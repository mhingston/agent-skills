# Forwarding services without ingress

Use this reference when the service is cluster-internal and has no public URL.
The goal is local, reversible access for Swagger or bounded API requests. Do
not add or expose an ingress as part of QA.

## Choose the forwarding path

| Need | Path |
|---|---|
| Several cluster services, internal DNS, or a RAC-managed local session | Reuse `raccli kubefwd <stage>` |
| One deployment/service for direct Swagger or API inspection | `kubectl port-forward` |
| A public URL or ingress change | Out of scope; obtain separate platform authorisation |

Before forwarding, resolve the exact stage, namespace, workload/service, target
container port, and an unused local port. Inspect existing processes and local
listeners first. Preserve unrelated sessions and do not kill or replace an
existing forwarding process without explicit approval.

## Direct deployment port-forward

Use the exact namespace and deployment discovered from the service manifest or
platform tooling:

```bash
kubectl port-forward deployment/<service> <local-port>:<container-port> \
  -n <namespace>
```

Keep the command running for the duration of the test. Verify the route before
calling a protected feature:

```text
http://localhost:<local-port>/healthz
http://localhost:<local-port>/readyz
http://localhost:<local-port>/swagger/index.html
```

Use the OpenAPI document or Swagger UI to confirm the route and request shape.
Record the local base URL and forwarding command without including credentials.

## RAC-managed forwarding

Prefer the existing session when multiple service dependencies must resolve
locally:

```bash
raccli kubefwd <stage>
```

For a manifest- or service-scoped session, inspect the current command help and
use the exact service/value-stream pair. Reuse a healthy session where possible;
do not use a kill/restart option just to make the test convenient.

Cluster forwarding is a routing aid, not an authentication bypass. Protected
endpoints still need the approved bearer token or other required credentials,
and the deployed pod still makes its own downstream calls. A healthy local
forward therefore proves only that the local route is available, not that the
application or its dependencies are healthy.

## Evidence and cleanup

Capture:

- stage, namespace, workload, local port, and forwarding method;
- health/readiness or Swagger status;
- protected request status, response fields, and correlation ID;
- whether the service version matches the intended change;
- any dependency or authentication limitation.

Stop only the forwarding process created for the test, and only after all
requests and evidence capture are complete. Do not stop a shared session that
was already running.
