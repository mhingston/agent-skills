# AgentReady v2.0 requirement map

**Canonical source:** https://github.com/agentready-org/standard/blob/main/spec/spec.md  
**Published version inspected:** v2.0, October 2026  
**Canonical reader site:** https://www.agentready.org/

This is an assessor's routing summary, not a fork of the normative text. **Check the current spec** for changes to identifiers, obligations, and applicability. Source levels are MUST / SHOULD / MAY; a site's conformance requires the applicable MUSTs. The spec deliberately does not assign a score. Do not substitute scanner ladders from other projects.

## Find — reachability before metadata

| ID | Level | Inspect |
| --- | --- | --- |
| AR-FIND-01 | MUST | Agent/search-crawler access to intended public content at robots and network layers; differentiate deliberate training opt-out |
| AR-FIND-02 | SHOULD | Canonical current first-party source answering the task |
| AR-FIND-03 | SHOULD | Valid sitemap and robots.txt sitemap pointer |
| AR-FIND-04 | MAY | Linked AI Catalog advertising actual agent-facing resources |

## Read — actual answer in fetched content

| ID | Level | Inspect |
| --- | --- | --- |
| AR-READ-01 | MUST | Answer in initial server/prerendered HTML, not accessible only after JS |
| AR-READ-02 | MUST | True 404 or redirect for missing paths; honest 429 with Retry-After when rate-limited |
| AR-READ-03 | SHOULD | Homepage raw HTML with meaningful product/docs/pricing navigation |
| AR-READ-04 | SHOULD | Useful task-answering first-party docs |
| AR-READ-05 | SHOULD | Copyable fenced, language-tagged code examples |
| AR-READ-06 | SHOULD | Actual visible links to discovery resources, not unadvertised files |
| AR-READ-07 | SHOULD | Lean, described and linked llms.txt index |
| AR-READ-08 | SHOULD | JSON-LD with essential facts also visible to text-only readers |
| AR-READ-09 | MAY | Advertised Markdown mirrors after HTML is reliable |
| AR-READ-11 | SHOULD | First-party visible pricing, limits and free tier when applicable |

The specification intentionally retired earlier identifiers and does not define an AR-READ-10 requirement in v2.0. Never manufacture missing IDs. A JS browser screenshot is not evidence of AR-READ-01; a mocked route in source is not proof of deployed 404 behaviour.

## Act — only if agents are meant to complete tasks

| ID | Level | Inspect |
| --- | --- | --- |
| AR-ACT-01 | SHOULD | Authentication agents can complete, documented scopes, OAuth discovery when delegated |
| AR-ACT-02 | SHOULD | First-party machine-readable OpenAPI and reliable API contract |
| AR-ACT-03 | SHOULD | Usable Streamable HTTP MCP, appropriate OAuth for private actions |
| AR-ACT-04 | MAY | Server card if supported by intended MCP hosts; evolving convention |
| AR-ACT-05 | MAY | MCP Apps view when handoff to human UI adds value |
| AR-ACT-06 | SHOULD | Installable documented SDKs/CLI relevant to intended clients |
| AR-ACT-07 | SHOULD | Feature-detected WebMCP on actionable web pages; draft API |
| AR-ACT-08 | MAY | Agent-supported payment path only for a product that actually charges |
| AR-ACT-09 | MAY | NLWeb /ask for suitable content products |
| AR-ACT-10 | MUST | At least one useful MCP server **or CLI** through which an agent can complete intended operations |

The \`AR-ACT-10\` MUST is conditional on **actionability**; it is not required of an informational site. A product API alone, in-page WebMCP alone, or an empty MCP surface is not equivalent to a usable MCP-or-CLI action path.

## Evidence and priority notes

- Label a failed live fetch as a fact about the tested client/location/time; do not generalise to all agent networks without corroboration.
- Distinguish absent file, untested capability, intentionally prohibited access, and actually broken intended task. Respect local bot/security policy and do not presume a spec recommendation authorises changing it.
- Source presence is weaker than end-to-end agent completion. For task success, use an explicitly permitted agent client and sandbox and retain a reversible test record.
- Start remediation with blocked fetches and JS-hidden answers, then false HTTP statuses and missing task-relevant pages; only then justify additional protocols. This is a task-first heuristic, not a score.
- Third-party tools such as is-agentic, Ora and Mintlify score separate interpretations of agent accessibility and may change independently of the specification.

## Source and reuse

AgentReady is an external, evolving specification maintained at the source linked above. Attribute findings to the specific version evaluated; do not describe this package as endorsed by AgentReady. Summaries here are paraphrased for evidence-led assessment and must be checked against the canonical source before making normative claims.
