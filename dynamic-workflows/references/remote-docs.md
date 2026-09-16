# Current documentation and source precedence

Use this reference before writing version-sensitive Mastra dynamic-workflow or
ACP integration code.

These APIs are changing quickly. Treat remembered API shapes and this skill's
historical examples as lower authority than the user's installed version and
current canonical documentation.

## Source precedence

When a Mastra project already exists:

1. **Installed package docs, types, and source** for the exact project version.
2. **Current official Mastra documentation** when installed material is missing
   or conceptual guidance is needed.
3. **Upstream Mastra package source/changelog** when API behaviour or release
   details need confirmation beyond the docs.
4. **Current ACP documentation/registry** for worker compatibility and
   distribution metadata.
5. **This skill's references** for stable design rules and previously observed
   implementation pitfalls.

When no project/packages exist, start with current official Mastra documentation,
then choose versions together rather than mixing old core and new integration
packages casually.

A current remote page can be ahead of an installed package. Never use a newer
remote example to override the types/source of the version the project actually
runs without deliberately upgrading it.

## Mastra documentation discovery

Start with Mastra's agent-friendly documentation index:

`https://mastra.ai/llms.txt`

Relevant current areas include:

- dynamic workflows: `https://mastra.ai/docs/workflows/dynamic-workflows.md`
- ACP connection guide: `https://mastra.ai/docs/connections/acp`
- `AcpAgent`: `https://mastra.ai/reference/acp/acp-agent.md`
- `createACPTool()`: `https://mastra.ai/reference/acp/create-acp-tool.md`

The ACP integration is distributed as the `@mastra/acp` package. Use the package
name as the implementation boundary when checking installed versions, imports,
types, changelog entries, or release metadata.

Useful upstream locations:

- npm package: `https://www.npmjs.com/package/@mastra/acp`
- Mastra monorepo source: `https://github.com/mastra-ai/mastra/tree/main/agent-sdks/acp`

Prefer the canonical Mastra docs for usage guidance. Use the package/source when
you need version-specific implementation details, exports, changelog history, or
to resolve a discrepancy between prose docs and installed behaviour.

Prefer the Markdown form when available. Use whatever web/HTTP retrieval
capability the current harness provides; do not couple this skill to a particular
vendor-specific fetch tool.

For dynamic definitions, also locate the current definition/reference page from
`llms.txt`. Verify graph entry types, mapping syntax, schemas, persistence and run
lifecycle against the installed/current release rather than reconstructing them
from memory.

## ACP discovery

ACP documentation index:

`https://agentclientprotocol.com/llms.txt`

Registry:

`https://agentclientprotocol.com/get-started/registry`

Machine-readable current registry:

`https://cdn.agentclientprotocol.com/registry/v1/latest/registry.json`

Use the registry when resolving an unfamiliar worker or checking whether a named
coding harness currently exposes an ACP distribution. Do not copy the registry's
full agent list into active instructions.

## Claude Code Workflows as a semantic reference

Claude Code's implementation is a useful reference for the *workflow model*, not
a Mastra API contract:

- documentation index: `https://code.claude.com/docs/llms.txt`
- dynamic workflows: `https://code.claude.com/docs/en/workflows`

Transfer durable semantics such as:

- orchestration held by executable runtime state rather than a lead model's
  context;
- intermediate results retained by the workflow rather than replayed into a
  supervisor conversation;
- explicit fan-out/fan-in and bounded loops;
- generated orchestration inspectable before execution;
- progress, cancellation and resumability as runtime concerns;
- coding workers performing filesystem/shell work while orchestration code
  coordinates them.

Do **not** copy Claude-specific JavaScript APIs, agent caps, permission behaviour,
filesystem paths, or session-resume semantics into a Mastra implementation unless
the user explicitly asks for Claude Code itself.

## Verification record

When a version-sensitive decision materially affects the implementation, record
at least:

- installed package/version or current remote source;
- the relevant API/type/source location;
- the date checked;
- any gap between current remote docs and the installed version;
- whether a workaround is current behaviour or only a historical observation.

This keeps temporary compatibility knowledge from becoming permanent skill law.
