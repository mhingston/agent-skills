# GitHub Copilot

Capability status: **no documented native hosted programmatic-tool-calling runtime equivalent; use capability-based fallbacks**

Last verified: 2026-07-19

Canonical sources:

- Copilot CLI overview: <https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview>
- Copilot CLI command reference: <https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference>
- Agent skills: <https://docs.github.com/en/copilot/concepts/agents/about-agent-skills>
- Copilot plugins: <https://docs.github.com/en/copilot/concepts/agents/about-plugins>
- Fleet and subagents: <https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet>
- Copilot SDK: <https://github.com/github/copilot-sdk>

## When to read this reference

Read this when applying the skill in GitHub Copilot CLI, Copilot cloud agent, IDE agent mode, or an application embedded with the Copilot SDK.

Do not require the Copilot SDK merely to use this skill. The skill is directly usable by Copilot products that support Agent Skills. The SDK is only one optional route for applications that deliberately embed the Copilot agent runtime.

## Capability finding

The official Copilot documentation reviewed on 2026-07-19 describes:

- ordinary agent tool use;
- shell, read, write, URL, and MCP tools;
- Agent Skills containing instructions, scripts, and resources;
- custom agents and parallel subagents;
- hooks and plugins;
- a programmatic CLI prompt interface;
- the Copilot SDK as an embedded agent runtime.

It does not document an OpenAI- or Anthropic-style hosted runtime where model-generated code can invoke arbitrary allowlisted agent or MCP tools repeatedly inside one model turn while keeping intermediate results outside model context.

Do not claim native feature parity unless newer official documentation establishes it.

## Route selection without the SDK

Use this decision order.

### 1. Local script for shell-accessible operations

Use a small script when every required operation is available through:

- existing project commands;
- safe local libraries already present in the repository;
- authenticated command-line tools;
- documented HTTP APIs that the environment is allowed to access.

This is the closest no-SDK fallback for deterministic fan-out, filtering, aggregation, and validation.

The script must:

- have explicit parameters and structured output;
- cap item count, concurrency, retries, and duration;
- use safe argument handling rather than shell interpolation;
- keep credentials outside generated source;
- avoid writes unless separately approved;
- preserve source identifiers and partial failures;
- be removed after use unless it is intentionally added as a reusable skill or project script.

This route uses Copilot's normal shell tool. It is not native programmatic tool calling and does not reduce model calls when the script itself must repeatedly invoke Copilot.

### 2. Direct calls for MCP-only or harness-only tools

A local process cannot call an arbitrary Copilot or MCP tool merely because the agent can see it.

When the required operation exists only in the agent tool layer:

- use direct calls with an explicit call budget;
- batch requests only if the tool natively supports batching;
- reduce results between calls where the harness permits;
- preserve approval boundaries and citations;
- stop rather than creating an undeclared dependency on the SDK.

For a one-off or low-volume workflow, this is usually the correct route.

### 3. Purpose-built composite MCP tool for recurring workflows

For a stable, repeated, high-volume deterministic stage, create or adopt a narrow MCP tool that performs the bounded fan-out and reduction behind one tool call.

Examples:

- `fetch_issue_summaries(issue_numbers, concurrency)`;
- `compare_inventory(skus)`;
- `validate_repositories(repositories, checks)`.

Prefer a domain-specific composite tool over a generic `execute_code` or `invoke_any_tool` interface.

The MCP server should own:

- credentials and authorization;
- concurrency, retries, rate limiting, and timeouts;
- strict input and output schemas;
- idempotency and duplicate suppression;
- provenance and partial-failure reporting.

This introduces an MCP server dependency, but not a Copilot SDK dependency. Copilot CLI can configure MCP servers directly, and a Copilot plugin can package the skill together with MCP configuration when distribution justifies it.

A composite MCP tool is a prebuilt operation, not model-generated arbitrary code over other tools. Document that difference.

### 4. Subagents for parallel semantic work

Use Copilot custom agents, the `task` tool, or fleet execution when independent subtasks require model judgment or separate context windows.

This is suitable for parallel research, codebase exploration, or independent reviews. It is not a token-saving substitute for deterministic programmatic calling because each subagent can make its own model calls and consume additional AI credits.

Require:

- disjoint subtask boundaries;
- bounded concurrency and depth;
- a small evidence-bearing report from each worker;
- deterministic aggregation where possible;
- explicit accounting for extra model calls and cost.

### 5. Copilot SDK for embedded applications only

Use the Copilot SDK when the user is building an application that intentionally embeds Copilot's agent runtime and accepts that dependency.

The SDK exposes the Copilot CLI engine through language bindings and JSON-RPC. It can define tools, skills, agents, hooks, MCP servers, permissions, and sessions, but its documented agent loop remains an iterative model-tool-model loop rather than the hosted in-turn program runtimes described by OpenAI and Anthropic.

Do not select the SDK merely to run this skill in Copilot CLI, cloud agent, or IDE agent mode.

## Programmatic CLI mode is not the same feature

Copilot CLI supports non-interactive prompting through `copilot -p` or `copilot --prompt`. This makes the CLI callable from scripts, but each invocation runs an agent task. It does not turn arbitrary Copilot tools into functions callable by generated code inside one model turn.

Avoid recursively invoking `copilot -p` for deterministic fan-out. That approach increases model calls and cost and weakens result and permission control. Use it only when each independent item genuinely needs model judgment and a subagent or batch job is unavailable.

## Skills, scripts, and plugins

Agent Skills are the default distribution format for this guidance. A skill may include scripts and references, so users can adopt the decision procedure without any SDK.

Add a bundled script only when one deterministic operation recurs across tasks and can remain portable. Do not bundle a generic orchestration runtime merely to imitate a missing harness feature.

Use a Copilot plugin only when the package needs to distribute additional components such as:

- a composite MCP server configuration;
- hooks enforcing validation or logging;
- custom agents for semantic fan-out;
- the skill itself as one installable unit.

Keep the standalone skill independently useful.

## Permissions

Copilot CLI supports allow and deny rules for shell, read, write, URL, and MCP tools.

- grant only the command, URL, path, or MCP operation required;
- prefer exact or narrow patterns over `--allow-all-tools`;
- deny destructive commands explicitly where practical;
- keep writes and external side effects approval-gated;
- do not pass secrets in prompts or generated scripts;
- validate local script arguments and outputs;
- preserve MCP server authorization independently of Copilot permissions.

## Recommended fallback report

When native programmatic calling is unavailable, report:

```text
Native programmatic runtime: unavailable or undocumented
Selected fallback: local script | direct calls | composite MCP tool | subagents
Why this route is valid: ...
Why the SDK is not required: ...
Semantic or approval boundary retained by direct calls: ...
Extra dependency, if any: ...
Feature differences from native programmatic calling: ...
```

## Review checklist

- [ ] Current official Copilot documentation was checked for native capability changes.
- [ ] The skill remains usable without the Copilot SDK.
- [ ] A local script is used only for shell-, library-, or API-accessible operations.
- [ ] MCP-only tools are not falsely treated as callable from local code.
- [ ] A composite MCP tool is proposed only for a recurring stable operation.
- [ ] Subagents are reserved for semantic work and their model cost is acknowledged.
- [ ] `copilot -p` is not used as fake low-cost programmatic fan-out.
- [ ] Shell and MCP permissions are narrowly scoped.
- [ ] Writes and irreversible actions retain explicit approval.
- [ ] The chosen fallback's differences from native programmatic calling are documented.