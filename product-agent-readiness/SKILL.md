---
name: product-agent-readiness
description: Assess whether an external AI agent can find, read, and (when intended) act through a public website, documentation site, or product. Use for AgentReady.org Find/Read/Act conformance baselines, agent-facing product-accessibility audits, or evidence-led remediation priorities. Read-only assessment; not coding-agent repository autonomy (agent-readiness), AI search ranking, or implementing fixes.
---

# Assess product agent readiness

Answer: **Can an external agent find authoritative product information, read it without browser-only assumptions, and complete an intended task through a supported interface?**

Use [AgentReady's canonical specification](https://github.com/agentready-org/standard/blob/main/spec/spec.md) as the requirement source, not a scanner grade. The bundled [v2.0 requirement map](references/agentready-v2.md) is a navigational aid, not a substitute for checking the current specification and its status. The reference is dated October 2026; note the version examined.

## Ownership and boundaries

- This skill assesses **the product as encountered by external agents**. For the safety/autonomy of coding agents operating *inside a repository*, use a coding-agent-readiness workflow instead.
- Read-only by default. Do not edit repository files, deploy, alter DNS, change crawler policy, weaken WAF/authentication, register MCP tools, generate credentials, or implement remediations.
- Inspect supplied repository artefacts and reports without executing application-controlled code. A public live assessment may use bounded, non-destructive GET/HEAD requests **only when access and scope permit**. Ask for authorisation before active scanning, authenticated testing, invoking actions, or using third-party scanners; do not evade bot blocks or CAPTCHAs.
- For private, sensitive, regulated, or member-specific content, distinguish **intentional access restriction** from the ability of an authorised agent to access an explicitly permitted surface. This skill never recommends publishing protected content.
- Treat scanner scores, existence of files, framework configuration, screenshots, and vendor claims as leads, not proof of successful agent use. Do not claim AgentReady certification or that this skill is an official validator.
- Preserve human/product ownership of crawler, consent, security, identity, payment, and delegated authority decisions. An agent's ability to act does not grant permission to perform an action.

## 1. Establish the assessment contract

Record the target origin(s), representative user tasks, environment/revision if known, evidence sources, permitted inspection methods, and accountable product owner. Distinguish:
- **Informational**: an agent is intended only to find/read/cite content. \`AR-ACT-*\` is not applicable.
- **Actionable**: an agent is expected to complete specific operations. Identify exact operations, safe test environment, intended identity/delegation, and confirmation/side-effect boundaries.

Do not assume every page or private API is intended for agent access. Scope the assessment to **public or explicitly authorised paths** and state any excluded surfaces. Start with 1–3 realistic tasks (e.g. find an API setup answer, find plan limits, or create a sandbox resource). Stop after enough evidence to discriminate the likely bottleneck; expand only for unresolved material claims.

## 2. Inspect Find → Read → Act in order

Use the IDs and MUST/SHOULD/MAY levels in [references/agentready-v2.md](references/agentready-v2.md). Report each material requirement as **pass, fail, unknown, not applicable**, with a stable evidence locator. Never infer a failure from lack of access alone.

### Find — can agents reach the source?

- Locate first-party canonical content and the routes a user task needs. Inspect public fetchability, \`robots.txt\` groups, sitemap links, redirects, and bot protections, including whether edge challenges affect verified agents.
- Separate training crawler policy from search indexing and user-initiated fetch policy; training opt-out does **not** imply an agent-access failure.
- A permissive \`robots.txt\` does not prove WAF/CDN reachability. If real bot reachability matters, require attributable server/CDN logs or authorised tests from the relevant client; a spoofed User-Agent alone is weak evidence.
- Evaluate optional discovery catalogs only after reachability. Unlinked \`.well-known\` manifests do not prove real discovery.

### Read — does a fetch-only client see the answer?

- Read **raw initial HTTP HTML**, not only a JavaScript-rendered browser view. Check whether the answer, meaningful links, setup details, and applicable pricing/limits exist in visible fetched content.
- Verify truthful status behaviour: missing page returns 404/valid redirect rather than a soft 200; throttling returns 429 with Retry-After, not a challenge masquerading as success. If throttling is not observed, mark its runtime behaviour unknown rather than deliberately inducing load.
- Evaluate relevant first-party docs, language-tagged code examples, linked \`llms.txt\` or other discovery files, JSON-LD plus visible text, and optional markdown mirrors. Do not prioritise metadata over unusable HTML.
- When documentation and observed API behaviour disagree, preserve the conflict instead of choosing the nicer story.

### Act — only if product tasks require it

- Verify the existence **and task coverage** of at least one usable MCP server or CLI as required by \`AR-ACT-10\`. WebMCP, an OpenAPI document, an SDK, or a decorative/empty MCP endpoint alone does **not** satisfy that particular requirement.
- Examine publicly documented discoverability, invocation ergonomics, typed API errors, limits, scopes, and authentication. Check OAuth metadata and delegated flows where relevant. Do not require a public unauthenticated action surface for a private product.
- Treat WebMCP, MCP server cards, MCP Apps, agent payment mechanisms, and NLWeb as conditional recommendations reflecting actual user tasks, supported clients, and source maturity, not blanket requirements.
- For authorised sandbox action testing, establish scope, explicit permission, idempotency/confirmation expectations, bounded side effects and cleanup **before** any invocation. Otherwise assess the contract and mark end-to-end completion unverified.

## 3. Make a supported verdict

The AgentReady specification defines **requirements, not scores**. Do not invent a weighted grade or use a third-party grade as its conformance status.

- **Conforms to inspected vX**: each applicable MUST has direct passing evidence, including \`AR-ACT-10\` if actionability is in scope. Say whether verification is source-only or live; source-only review cannot establish full deployed conformance.
- **Does not conform**: at least one applicable MUST is shown failing in the assessed environment. Give the exact ID and proof.
- **Unverified**: one or more applicable MUSTs remain unknown, disputed, stale, or insufficiently observed, and no conclusive failure was demonstrated. If a failure and unknowns coexist, report failure with the unknowns separately.
- SHOULD/MAY gaps are improvements, not conformity blockers. External scanners can aid inspection, but note their independent scoring systems and version drift.

Prioritise the smallest 1–3 fixes that plausibly remove a measured task blocker. Prefer restoring fetchability, correct HTTP semantics and useful visible answers before adding speculative protocol surfaces. Each proposed fix names an owner/decision, affected requirement(s), a falsifiable post-change verification, and any permission/security prerequisite.

## Output

Give a concise report containing:
1. **Scope**: origin/revision, informational vs actionable, representative tasks, current spec/version/date, assessment mode and coverage limits.
2. **Find / Read / Act**: one or two sentences per stage plus a compact table of material IDs, level, status, evidence URL/path/response/log (or reason for unknown), and effect on the task. Mark Act N/A if informational.
3. **Verdict**: conforms / does not conform / unverified for the tested scope, separate from any scanner score.
4. **Next actions**: at most three ranked, reversible improvements with owner and concrete re-test. State blockers and human decisions, not an auto-generated implementation backlog.

Fast path: supplied task + inspected fetch-only evidence + existing report, with unknowns explicit. Full path: add authorised edge logs and sandbox task execution only when the verdict or remediation order genuinely depends on them. If tools/network/access are unavailable, report a bounded source-only result rather than inventing live observations.
