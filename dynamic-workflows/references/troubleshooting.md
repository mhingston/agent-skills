# Mastra / ACP troubleshooting

Use this reference only after a concrete integration failure or when installed
behaviour contradicts the current Mastra documentation.

The observations below came from the original prototype and are deliberately
kept out of active instructions because they are version-specific. Re-verify the
installed packages/source before applying them.

## Historical verified baseline

A local end-to-end combination verified on 2026-08-21 was:

- `@mastra/core@1.61.0`
- `@mastra/acp@0.4.0`
- `@mastra/libsql@1.21.1`
- `@agentclientprotocol/claude-agent-acp@0.70.0`

It successfully exercised local subscription authentication, read and write.
Treat this only as evidence that the combination worked then, not a recommended
pin or proof that newer versions behave identically.

## Bare `AcpAgent` registration failure

With `@mastra/acp@0.4.0` + `@mastra/core@1.61.0`, registering a bare `AcpAgent`
directly under `new Mastra({ agents: { ... } })` was observed to fail at
construction with calls to full-`Agent` internals such as:

```text
TypeError: mastraAgent.__setLogger is not a function
```

Further no-op shimming then exposed another internal method call. Do not patch a
chain of private methods.

At that version, the working no-supervisor route for a dynamic workflow was to
register `createACPTool()` under Mastra `tools` and reference the tool ID from the
graph. `AcpAgent` also worked when used in its documented subagent role under a
real model-backed Mastra `Agent`.

**Before using this workaround now:** inspect the installed `Mastra` agent
registration implementation and current docs. If direct lightweight/subagent
registration is supported by the installed release, prefer the current supported
path and delete obsolete workaround code.

## `npx -y` and corporate npm registries

Spawn-time resolution such as:

```text
npx -y @agentclientprotocol/claude-agent-acp
```

may resolve packages using registry configuration visible from the spawned
process/cwd. In a corporate environment this can fail with a registry 403 even
when ACP and Claude auth are healthy.

If this occurs, prefer installing the adapter as a project dependency and invoke
its local executable/entry point deterministically. Diagnose registry resolution
before changing credentials or ACP settings.

## ACP SDK major versions

The Mastra ACP package and a particular ACP adapter may depend on different major
versions of the ACP SDK. Because ACP communicates across a process/wire boundary,
separate nested SDK copies are not automatically a defect.

Do not force package-manager deduplication merely to make SDK majors match. Check
protocol compatibility and actual runtime behaviour first.

## Claude organization verification vs credentials

A Claude Code/Enterprise login can be locally valid while an ACP-spawned process
still fails because organization verification requires network access during a
query.

Before concluding that a token is stale/revoked, test outbound access from the
**actual process environment** launching the ACP agent. Historically relevant
hosts included:

- `api.anthropic.com`
- `claude.ai`
- `console.anthropic.com`

A nested agent/tool sandbox, CI runner, container, proxy, or corporate allowlist
may be the blocker even when the user's normal terminal works.

Do not redirect `CLAUDE_CONFIG_DIR` to an empty directory as a generic fix. That
can create a different authentication failure by hiding state needed by the
existing login.

## Generic `Internal error`

`claude-agent-acp` has historically surfaced some failures through a generic
message such as:

```text
RequestError: Internal error
```

When this happens, inspect the structured error payload (`error.data`, including
fields such as `details`) in addition to `error.message` and the stack. The
structured field has contained the actionable underlying organization/network
failure when the top-level message did not.

Do not diagnose from the generic message alone.

## `EMFILE` settings watcher noise

A `Settings watcher error ... EMFILE: too many open files, watch` line observed in
Claude ACP stderr was not, by itself, evidence that the ACP query failed. The
watcher error could be logged and swallowed while the real session failure lived
elsewhere in structured error data.

Treat it as a separate resource symptom unless evidence binds it causally to the
failed request. Do not let a vivid stderr line displace the actual error payload.

## `getAvailableModels()`

For the tested Claude bridge, an empty result from `getAvailableModels()` did not
necessarily mean authentication failed. Validate with an actual supported call
or the adapter's current documented health signal before treating an empty model
list as fatal.

## Debug order

When an ACP-backed dynamic workflow fails:

1. capture the exact package versions and worker command/args;
2. identify whether failure occurred before process spawn, ACP initialize,
   session creation, prompt execution, permission handling, or workflow mapping;
3. inspect structured error data and worker stderr without assuming the loudest
   message is causal;
4. verify executable/package resolution;
5. verify auth and then network/organization checks from the same process context;
6. compare behaviour with current installed docs/types/source;
7. reduce to a direct minimal ACP call before blaming the dynamic workflow;
8. separately validate the Mastra graph/schema when live worker execution is
   blocked.

Record a new workaround in durable guidance only after the failure mechanism is
reproduced and version-scoped.
