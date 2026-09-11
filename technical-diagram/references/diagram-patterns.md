# Technical diagram patterns

Choose the smallest pattern that communicates the mechanism. A pattern is a
composition aid, not a semantic substitute: preserve the actual system behaviour
and omit unsupported edges.

## 1. Linear request or data flow

Use when one request, event, or record moves through a small number of stages.

```text
actor → entry point → processing/service → store/tool → outcome
```

Good for:

- request/response paths;
- ingestion pipelines;
- model/tool calls;
- simple event processing;
- authentication handshakes at a high level.

Design notes:

- left-to-right is the default;
- number steps only when order is not obvious;
- put response flow on a separate return path when it matters;
- collapse implementation detail inside one service if it does not alter the
  story.

## 2. Primary path with fallback

Use when the normal route is simple but resilience or graceful degradation is a
material part of the explanation.

```text
primary path  ─────────────────────────→ outcome
       │
       └──── failure / miss / timeout → fallback ─→ outcome
```

Good for:

- cache miss → database;
- model failure → backup model/cached answer/human;
- circuit breaker → degraded path;
- retry then dead-letter or manual handling.

Design notes:

- keep the happy path visually dominant;
- move fallback into a lower lane or secondary grouped region;
- use dashed connectors for conditional/failure routing;
- show where the fallback rejoins the useful outcome;
- distinguish retry from fallback rather than drawing both as generic loops.

## 3. Cluster or sharded service

Use when one logical capability is implemented by several peer nodes.

```text
          logical cluster
      ┌────────────────────┐
input → node A   node B   node C
      └────────────────────┘
```

Good for:

- distributed caches;
- stateless service replicas;
- worker pools;
- partitions/shards;
- replicated data services.

Design notes:

- draw the cluster boundary once;
- state the routing rule that makes the peers meaningful: shard key, hash,
  partition, round-robin, leader/follower, etc.;
- do not use a triangle merely because there are three nodes;
- if replication matters, show replica relationships distinctly from shard
  ownership;
- if a failed node causes rebalancing, add a separate resiliency lane rather than
  cluttering the normal cluster view.

## 4. Hub and fan-out

Use when one coordinator sends work to multiple independent capabilities.

```text
             → service A
coordinator  → service B
             → service C
```

Good for:

- orchestration;
- search across data sources;
- notifications to channels;
- parallel analysis stages;
- API aggregation.

Design notes:

- align peer targets vertically;
- use one clean fan-out rail where possible;
- show join/aggregation explicitly if results must converge;
- label sequential dependencies separately from true parallel fan-out.

## 5. Publish/subscribe or queue

Use when producer and consumer are intentionally decoupled through messaging.

```text
producer → topic / queue → consumer(s)
```

Good for:

- event-driven architecture;
- job queues;
- asynchronous workflows;
- stream processing.

Design notes:

- make the broker/queue a first-class object;
- show one-to-many consumers without implying direct producer calls;
- add retry/dead-letter as a secondary lane only if material;
- distinguish queue semantics from pub/sub when the difference matters;
- do not imply delivery guarantees that the source does not establish.

## 6. State or lifecycle progression

Use when the core mental model is movement between named states rather than
movement between services.

```text
created → active → suspended → closed
             ↘ recovery ↗
```

Good for:

- order lifecycle;
- workflow status;
- authentication/token states;
- deployment/release states;
- agent-run lifecycle.

Design notes:

- put state names inside nodes and transition verbs beside arrows;
- use a loop only for a real repeatable transition;
- highlight terminal states;
- split into multiple rows if a state machine becomes visually cyclic and hard to
  trace.

## 7. Before / after

Use when the user needs to understand a change, refactor, optimisation, or design
trade-off.

```text
BEFORE                         AFTER
old path                       new path
problem callout                consequence callout
```

Good for:

- architecture migrations;
- performance improvements;
- removal of coupling;
- introducing a queue/cache/gateway;
- policy or ownership changes.

Design notes:

- keep both halves structurally comparable;
- visually highlight only the changed dimension;
- use one concise consequence per side;
- do not redraw unchanged context differently merely to make the after picture
  look cleaner.

## 8. Layered architecture overview

Use when responsibility boundaries matter more than runtime sequence.

```text
clients
────────────
application / API
────────────
domain / services
────────────
data / infrastructure
```

Good for:

- service responsibility maps;
- platform layers;
- trust boundaries;
- high-level deployment architecture.

Design notes:

- use broad horizontal or vertical bands;
- keep arrows sparse and only show relationships that matter to the question;
- avoid turning the visual into a complete dependency graph;
- if runtime order is actually the user's question, switch to a flow pattern.

## 9. Control plane / data plane

Use when one path configures or governs another runtime path.

```text
control plane  ─ ─ ─→ config/policy
                         ↓
data plane     request → runtime components → outcome
```

Good for:

- model routing configuration;
- service mesh/control planes;
- deployment management;
- feature flagging;
- policy distribution.

Design notes:

- separate planes spatially;
- use dashed connectors for configuration/control when appropriate;
- keep the runtime/data path visually stronger;
- do not imply the control plane is in the per-request path unless it really is.

## 10. Boundary crossing

Use when security, tenancy, network, ownership, or deployment boundaries are the
important part of the story.

```text
[boundary A] → gateway/interface → [boundary B]
```

Good for:

- trust zones;
- third-party integrations;
- cross-account/cloud calls;
- tenant isolation;
- frontend/backend boundaries.

Design notes:

- label the boundary itself, not just the components inside it;
- show the interface where policy/validation occurs;
- avoid decorative dashed boxes with no semantic meaning;
- use colour sparingly so the boundary remains visible without overwhelming the
  flow.

## 11. Decision split

Use when one deterministic or policy decision creates two or three materially
different routes.

```text
input → decision
          ├─ condition A → path A
          └─ condition B → path B
```

Good for:

- routing;
- eligibility;
- cache hit/miss when both branches deserve equal emphasis;
- feature gating;
- classification outcomes.

Design notes:

- put the condition on the branch, not inside a paragraph in the decision node;
- keep branches visually symmetric when neither is the default;
- use the primary+fallback pattern instead if one route is overwhelmingly normal
  and the other exists only for resilience.

## 12. Feedback loop

Use when output changes future input or configuration.

```text
observe → evaluate → update → execute
   ↑                         │
   └─────────────────────────┘
```

Good for:

- adaptive systems;
- monitoring/remediation;
- model evaluation and promotion;
- autoscaling;
- optimisation loops.

Design notes:

- show what state or policy is updated;
- label the frequency or trigger only when established and relevant;
- distinguish a real closed loop from a one-off reporting path.

## Combining patterns

Combine at most two patterns on one canvas by default. Examples:

- cluster + primary/fallback for distributed cache behaviour;
- linear flow + boundary crossing for an external API integration;
- hub/fan-out + join for parallel analysis;
- lifecycle + fallback for recovery states.

When a third pattern seems necessary, ask whether the visual is trying to explain
more than one message. Splitting usually produces a stronger artifact.

## Pattern selection heuristic

Choose based on the question the visual answers:

| Reader question | Pattern |
| --- | --- |
| What happens in order? | Linear flow |
| What happens when the normal path fails? | Primary + fallback |
| How is one logical service spread across nodes? | Cluster/sharded service |
| How does work spread to peers? | Hub + fan-out |
| How are producers and consumers decoupled? | Queue/pub-sub |
| How does an entity move between states? | Lifecycle |
| What changed? | Before/after |
| Who owns which responsibility? | Layered architecture |
| What configures what runs? | Control plane/data plane |
| Where is the important boundary crossed? | Boundary crossing |
| Which route is chosen and why? | Decision split |
| How does output influence future behaviour? | Feedback loop |

If none fits cleanly, state the one-message thesis again before inventing a custom
layout. Often the source material needs abstraction rather than a new visual
notation.
