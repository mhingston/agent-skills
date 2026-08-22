# ACP harnesses

Use this reference when the workflow needs repository-capable coding workers over
Agent Client Protocol (ACP).

## Compatibility model

Mastra is the ACP **client**. `@mastra/acp` starts a configured ACP **agent**
process and communicates with it over standard input/output.

The compatibility boundary is therefore the protocol, not a maintained shortlist:
if an executable correctly implements ACP over stdio, Mastra can configure it by
command and arguments. Named harnesses below are examples and discovery aids, not
an allowlist.

## Discover a worker

Resolve the worker in this order:

1. explicit user choice;
2. existing repository/project configuration;
3. an already-installed local ACP executable or adapter consistent with the
   user's constraints;
4. the current ACP Registry;
5. one concise clarification when the choice still materially changes the task.

Do not reinstall a CLI unnecessarily. Do not switch a user from subscription or
local-login authentication to provider API billing without explicit consent.

The current registry is available at:

- `https://agentclientprotocol.com/get-started/registry`
- `https://cdn.agentclientprotocol.com/registry/v1/latest/registry.json`

Query the registry rather than copying its full contents into this skill. It is a
moving catalogue.

## Documented examples

As of 2026-08-22, current Mastra ACP documentation explicitly uses Claude Code,
Amp, and Codex as examples. Mastra's ACP launch announcement also names Cursor
and Gemini CLI. The ACP Registry contains those plus many more agents, currently
including GitHub Copilot, OpenCode, pi ACP, Auggie CLI, Cline, Qwen Code, Kimi
CLI, goose, Junie, and others.

Do not infer that an agent absent from Mastra's prose examples is unsupported.
Protocol compatibility and the current executable/adapter are the relevant test.

### Claude Code / Claude Agent

A common ACP bridge is:

```ts
command: "npx",
args: ["-y", "@agentclientprotocol/claude-agent-acp"],
```

Prefer a locally installed bridge when the project already has one, especially in
corporate environments where spawn-time `npx` resolution may hit a different npm
registry configuration.

Use the user's existing Claude authentication where the bridge supports it. Do
not introduce an Anthropic API key merely because ACP is in use.

### Codex

A common adapter is:

```ts
command: "npx",
args: ["-y", "@agentclientprotocol/codex-acp"],
```

Prefer the existing Codex/ChatGPT local login when supported. Do not introduce an
OpenAI API key unless the user chooses API authentication.

### Cursor

Cursor is present in the ACP Registry and has supported native ACP operation.
Detect the installed CLI and consult its current documentation/registry metadata
rather than hard-coding a historical executable name when the project does not
already define one.

### Gemini CLI

Gemini CLI is present in the ACP Registry and has supported native ACP mode. Use
the installed CLI's current ACP invocation and the user's existing Gemini
configuration/authentication.

### Amp and other registry agents

Amp is now named directly in Mastra's current ACP docs. Resolve its current
installation/command from the ACP Registry or installed configuration.

Use the same rule for GitHub Copilot, OpenCode, pi ACP, or another registered
agent: obtain current distribution and invocation data rather than embedding a
stale command here unless the project already pins one.

### Custom ACP executable

When the user provides another ACP-compatible command, configure that command and
arguments directly. Ask for command/args only when they cannot be inferred from
repository configuration, an installed executable, or registry metadata.

## Authentication

Authentication belongs to the worker/harness, not Mastra's workflow graph.

- Prefer existing local login/subscription/enterprise authentication.
- Preserve the user's configured credential provider and environment.
- Report a missing auth prerequisite; do not silently switch billing modes.
- Distinguish credential failure from network/organization-verification failure.
- Do not persist secrets into generated workflow JSON or run receipts.

## Sessions and workflow state

Mastra's `AcpAgent` can persist its ACP process/session across calls. That may be
useful for conversational continuity, but dynamic workflow correctness should not
depend on hidden session state.

Prefer explicit graph inputs, repository state, and persisted workflow artifacts.
Choose fresh/isolated worker sessions where role isolation, reproducibility, or
independent review matters. Enable session persistence only when it is an
intentional part of the design.

## Permissions

ACP agents may request permissions for file or command operations.

- Preserve a project-provided `onPermissionRequest` policy.
- Prefer allow-once/non-persistent choices when unattended policy is otherwise
  unspecified.
- Reject or stop when there is no recognizable safe option.
- Never silently grant global/permanent permission.
- Never weaken the user's sandbox, filesystem scope, network rules, or CLI policy
  merely to make the workflow run.

Mastra's default permission behaviour can select the first option returned by an
ACP agent. Do not rely on that default when permission consequences matter;
configure explicit policy.

## Selection note for generated workflows

A planner may select only from worker IDs that have already been registered and
allowed by deterministic policy. Planner output must never manufacture a command,
package, credential, model provider, or new ACP registration.
