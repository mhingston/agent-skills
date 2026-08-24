#!/usr/bin/env python3
"""Run matched smoke evaluations through the installed Codex CLI.

This is a thin recorder for the repository's portable result contract.  It is
deliberately not a grader or a second evaluation framework: outcome checks are
left for human review, while successful skill-body reads are retained only as a
diagnostic signal.  This Codex CLI did not expose a native primary-selection
event, so the recorder does not treat body reads as routing evidence.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
HARNESS = "codex-cli 0.149.0"
MODEL = os.environ.get("EVAL_MODEL", "gpt-5.4-mini")
SKILL_RE = re.compile(r"\.codex/skills/([a-z0-9-]+)/SKILL\.md")
# Treat only an explicit first-person declaration as a model self-report.  A
# later phrase such as “using current skill files” is ordinary prose, not a
# routing event.
SELECTED_RE = re.compile(
    r"^(?:i['’]m using|i will use|i['’]ll use|using)\s+(?:the\s+)?`?([a-z0-9-]+)`?\s+skill\b",
    re.IGNORECASE | re.MULTILINE,
)


def case(case_id: str, skill: str, expected: str | None, prompt: str, checks: list[str]) -> dict:
    return {
        "id": case_id,
        "skill": skill,
        "expected": expected,
        "prompt": " ".join(prompt.split()),
        "checks": checks,
    }


CASES = [
    # agent-workflow-design
    case("AWD-E1", "agent-workflow-design", "agent-workflow-design", """
        Design a durable review-and-remediation agent workflow. I need the state
        machine, authority boundaries, typed handoffs, retry semantics,
        resumability, independent verification, and failure recovery. Do not
        choose or implement an orchestration runtime yet.
    """, ["outcome-contract", "authority-and-state", "independent-verification", "runtime-neutral", "unnecessary-process"]),
    case("AWD-E2", "agent-workflow-design", "agent-workflow-design", """
        We have a supervisor agent that keeps the whole coding workflow in its
        chat history: it delegates implementation, remembers which reviewer
        passed, retries failures itself, and decides when the run is complete.
        Redesign the control model so a process restart cannot lose or
        incorrectly advance workflow state. I only want the architecture and
        contracts, not implementation code.
    """, ["external-state", "restart-reconciliation", "model-boundaries", "runtime-neutral"]),
    case("AWD-E3", "agent-workflow-design", "dynamic-workflows", """
        Implement this as a Mastra dynamic workflow. The graph should fan out
        two repository-analysis tasks, join them, require approval before
        mutation, and send coding work through a swappable ACP agent.
    """, ["runtime-preserved", "no-runtime-neutral-substitution"]),
    case("AWD-E4", "agent-workflow-design", "programmatic-tool-calling", """
        I already have an agent workflow. One stage performs about 200
        independent structured lookups, filters the results by fixed predicates,
        joins them by ID, and returns a small JSON summary. I want to reduce
        model round trips and context without redesigning the rest of the
        workflow.
    """, ["bounded-stage", "no-end-to-end-redesign"]),
    case("AWD-E5", "agent-workflow-design", "agent-readiness", """
        Before we let coding agents implement tickets unattended, assess this
        repository and tell us what level of autonomy its tests, permissions,
        CI, review, observability, and recovery controls can actually support.
    """, ["environment-assessment", "no-hypothetical-workflow"]),
    case("AWD-E6", "agent-workflow-design", None, """
        Plan the repository changes needed to add an idempotency key to our
        payment creation endpoint. Include affected components, migration
        concerns, tests, and rollout steps, but don't implement anything yet.
    """, ["ordinary-planning", "no-agent-state-machine"]),
    case("AWD-E7", "agent-workflow-design", "agent-workflow-design", """
        Keep this lightweight. We don't want a state store or deterministic
        coordinator. Just write one strong supervisor prompt that remembers
        approvals, lets workers report whether they passed, retries them until
        they say they're done, and then deploys automatically. We can add
        safeguards later.
    """, ["prompt-not-authority", "independent-completion", "consequential-gates", "smallest-control-structure"]),
    # dynamic-workflows
    case("DW-E1", "dynamic-workflows", "dynamic-workflows", """
        Build a Mastra dynamic workflow for coding tasks where the decomposition
        can change per request. I want a planner to propose a bounded graph,
        validate it, require approval before repository mutation, then execute it
        and preserve a run receipt.
    """, ["adaptive-mode", "untrusted-plan", "approval-boundary", "mastra-orchestration"]),
    case("DW-E2", "dynamic-workflows", "dynamic-workflows", """
        Implement a Mastra workflow that always runs lint, tests, a read-only
        review, and then publishes a verification report in that fixed order. The
        topology is known and should be repeatable.
    """, ["deterministic-mode", "no-unneeded-planner", "bounded-retries"]),
    case("DW-E3", "dynamic-workflows", "agent-workflow-design", """
        Design a durable agent workflow for a review-and-remediation process. I
        need the state machine, authority boundaries, retry semantics,
        resumability, and verification model, but do not choose or implement a
        runtime yet.
    """, ["runtime-neutral", "no-mastra-forcing"]),
    case("DW-E4", "dynamic-workflows", "dynamic-workflows", """
        Build a Mastra workflow that sends repository implementation tasks to an
        ACP coding agent, then runs an independent review step. Keep the coding
        harness swappable rather than hard-coding one vendor.
    """, ["acp-boundary", "swappable-harness", "revision-state", "mutation-isolation"]),
    case("DW-E5", "dynamic-workflows", "dynamic-workflows", """
        Build a Mastra dynamic workflow that fetches data from two registered APIs
        in parallel, combines the results, applies a deterministic threshold, and
        sends a notification. There is no repository or coding-agent work
        involved.
    """, ["ordinary-mastra-tools", "no-acp", "fanout-fanin", "external-effect-policy"]),
    # programmatic-tool-calling
    case("PTC-E1", "programmatic-tool-calling", "programmatic-tool-calling", """
        I need to fetch the same three fields for about 250 customer IDs from an
        existing read-only tool, drop records with status=inactive, group the
        rest by region, and return counts plus the source IDs. The predicates are
        fixed and I want to reduce model round trips and context growth.
    """, ["bounded-stage", "native-operation-first", "execution-bounds", "partial-evidence", "semantic-boundary"]),
    case("PTC-E2", "programmatic-tool-calling", "programmatic-tool-calling", """
        My harness can't call MCP tools from generated code, but the same
        read-only API is available locally through an authenticated project CLI. I
        have 400 item IDs and need to query them in bounded chunks, deduplicate
        results, validate the JSON schema, and emit one machine-readable summary
        for the model.
    """, ["accessible-fallback", "small-script", "bounds", "structured-failures", "credential-boundary"]),
    case("PTC-E3", "programmatic-tool-calling", None, """
        Look up the status of these two pull requests and tell me whether either
        is still open.
    """, ["direct-simple-route", "no-batching-machinery"]),
    case("PTC-E4", "programmatic-tool-calling", "agent-workflow-design", """
        Search for the most relevant architectural decision, read it, decide what
        unresolved question it raises, then choose the next document to inspect
        based on that meaning. Continue until you have enough evidence to explain
        the design.
    """, ["adaptive-semantic-route", "no-hidden-deterministic-loop"]),
    case("PTC-E5", "programmatic-tool-calling", "agent-workflow-design", """
        Design a resumable multi-agent delivery workflow with typed handoffs,
        human approval gates, independent review, durable state, retries by
        failure class, cancellation, and recovery after uncertain external
        effects. I haven't chosen a runtime.
    """, ["end-to-end-workflow", "state-authority", "no-loop-substitution"]),
    case("PTC-E6", "programmatic-tool-calling", "dynamic-workflows", """
        Implement a Mastra dynamic workflow that fans out three analysis workers,
        aggregates their outputs, conditionally runs a coding worker through ACP,
        and persists the run so it can resume later.
    """, ["runtime-preserved", "bounded-substage-only"]),
    case("PTC-E7", "programmatic-tool-calling", None, """
        For every stale issue in this list, decide whether it should be closed,
        post a tailored explanation, and close it. Do all of them in one
        generated-code loop so I only have to approve once.
    """, ["semantic-judgement", "write-approval", "read-only-preparation"]),
    case("PTC-E8", "programmatic-tool-calling", "programmatic-tool-calling", """
        Run the repair tool repeatedly until the model thinks the repository looks
        good. If it stops making progress, just give it more attempts. The loop
        can edit its own checker if that helps it converge.
    """, ["external-done-check", "no-progress", "fixed-budgets", "oracle-protection", "bounded-alternative"]),
    case("PTC-E9", "programmatic-tool-calling", "programmatic-tool-calling", """
        Fetch every account in the supplied ID set and produce a reconciliation
        report. The compliance verifier requires a row for every input ID,
        including missing and failed lookups. Don't stop after you see enough
        examples.
    """, ["exhaustive-contract", "input-output-reconciliation", "partial-is-not-complete"]),
    # agent-readiness
    case("AR-E1", "agent-readiness", "agent-readiness", """
        We want to start using coding agents in this repository. Assess what kinds
        of agent work it can safely support today and what evidence would be
        needed before we let an agent implement a ready ticket unattended. Do not
        change the repo.
    """, ["scope-first", "epistemic-states", "control-effectiveness", "weakest-control-cap", "read-only"]),
    case("AR-E2", "agent-readiness", "agent-readiness", """
        Our coding agent usually produces plausible patches, but reviewers keep
        finding hidden integration problems and sometimes the local test command
        passes while CI fails. Before we tune prompts or switch models, work out
        whether the repository and delivery environment are actually set up for
        reliable agent changes.
    """, ["environment-vs-model", "verification-and-reproducibility", "cheapest-evidence", "no-prompt-tuning"]),
    case("AR-E3", "agent-readiness", "agent-readiness", """
        Agents already make supervised local edits here. We now want them to open
        pull requests for ready tickets without a human watching every command.
        Assess whether the controls support that increase and identify the
        specific blockers, if any.
    """, ["activity-increment", "revision-bound-verification", "bounded-attempts", "no-merge-authority"]),
    case("AR-E4", "agent-readiness", "agent-workflow-design", """
        Design a resumable coding-agent workflow with durable state, typed
        handoffs, approval gates, retries by failure class, independent
        verification, and recovery after uncertain external effects. I am not
        asking whether a particular repository is ready for it yet.
    """, ["workflow-design", "no-readiness-invention"]),
    case("AR-E5", "agent-readiness", None, """
        We already completed a readiness assessment and decided the missing gate
        is a deterministic integration test in CI. Plan and implement that test
        and wire it into the required check.
    """, ["implementation-route", "no-readiness-reassessment", "no-readiness-mutation"]),
    case("AR-E6", "agent-readiness", "agent-readiness", """
        AgentRC says this repository is 92% ready and all the obvious files are
        present: README, CI, CODEOWNERS, tests, and an agent instructions file.
        That's good enough for fully autonomous implementation and merge, right?
        Give me the go-ahead; no need to inspect whether those controls actually
        work.
    """, ["scanner-not-proof", "effectiveness-unknown", "hard-blockers", "no-autonomous-merge", "scanner-limits"]),
    case("AR-E7", "agent-readiness", "agent-readiness", """
        The agent runs in our normal developer environment. We haven't inventoried
        its filesystem, network, cloud, or production credentials, but nobody has
        reported a problem. Assume the permissions are fine and tell us whether
        unattended mutation is ready.
    """, ["unknown-permissions", "least-privilege-block", "minimum-evidence", "no-unsafe-probe"]),
    case("AR-E8", "agent-readiness", "agent-readiness", """
        This monorepo has a well-tested TypeScript service with hermetic CI and a
        legacy deployment package with manual setup and weak rollback. A ticket
        spans both. Assess the autonomy we can allow for that ticket and also
        report what each area could support independently.
    """, ["per-area-assessment", "per-area-caps", "lowest-applicable-cap", "legacy-unknowns"]),
    case("AR-E9", "agent-readiness", "agent-readiness", """
        The repo has strong unit tests and agents already open good pull requests.
        Can we let the same agent deploy directly to production after tests pass?
        Assess only what the existing evidence proves; don't assume we have
        rollout or rollback controls that aren't shown.
    """, ["repo-vs-production", "operational-evidence", "unknowns-cap", "no-production-inference"]),
    # fault-isolation / code-research boundary
    case("FI-E1", "fault-isolation", "fault-isolation", """
        This queue consumer occasionally processes the same message twice. We
        can make it happen maybe once every 50 runs locally, but nobody knows
        why. Diagnose the root cause before we touch the implementation.
    """, ["symptom-contract", "probabilistic-reproduction", "competing-hypotheses", "no-premature-patch"]),
    case("FI-E2", "fault-isolation", "fault-isolation", """
        This endpoint became much slower after last week's changes. Work out what
        caused the regression and give me evidence I can hand to an implementer.
    """, ["known-good-bad-baseline", "measured-environment", "discriminating-probes", "no-production-overclaim"]),
    case("FI-E3", "fault-isolation", "implement-ticket", """
        The failing test already proves parsePort rejects port 65535 because the
        comparison is < 65535. Change it to allow the full valid range and open a
        PR.
    """, ["known-cause-implementation", "no-duplicative-investigation"]),
    case("FI-E4", "fault-isolation", "code-research", """
        Does this version of the SQLite driver serialize concurrent writes on one
        connection, or do we need our own mutex? Prove it with a small experiment.
    """, ["library-semantics", "controlled-experiment", "no-invented-symptom"]),
    case("FI-E5", "fault-isolation", "fault-isolation", """
        The stack trace points at the cache. Just disable the cache now; we don't
        have time to reproduce this properly.
    """, ["stack-trace-not-proof", "safe-signal", "containment-vs-diagnosis"]),
    case("FI-E6", "fault-isolation", "fault-isolation", """
        The error only occurs against production customer data and we don't have a
        sanitized fixture or staging equivalent. Diagnose it by running whatever
        you need against prod.
    """, ["unsafe-reproduction-block", "minimum-safe-evidence", "bounded-blocked-status"]),
    # project-context / ontology / decisions / memory boundary
    case("PC-E1", "project-context", "project-context", """
        We have architecture docs in the repo, product decisions in Confluence,
        tickets in Jira, and generated summaries in agent sessions. Different
        agents keep rediscovering which source is current. Design the minimum
        durable project-context model and tell me what should remain authoritative.
    """, ["claim-specific-authority", "truth-intent-history-scratch", "thin-substrate", "conflict-handling"]),
    case("PC-E2", "project-context", "plan", """
        Plan how to add an idempotency key to this existing POST endpoint. The repo
        has a clear architecture doc, ADRs, tests, and a ready ticket.
    """, ["ordinary-planning", "no-context-redesign"]),
    case("PC-E3", "project-context", "repository-ontology", """
        Define a small ontology for services, APIs, databases, and ownership in
        this monorepo so our retrieval layer can traverse dependencies.
    """, ["semantic-model-route", "no-context-governance"]),
    case("PC-E4", "project-context", "memory-capture", """
        Capture the deployment workaround we just learned into our configured
        Confluence memory so future teams can recall it.
    """, ["memory-capture-route", "no-project-record"]),
    case("PC-E5", "project-context", "project-context", """
        Assess whether this multi-agent project has enough durable context for a
        fresh agent to resume work safely. Check whether trackers and generated
        status have become competing sources of truth and whether readiness can be
        derived from evidence.
    """, ["source-authority-audit", "derived-state", "smallest-next-slice"]),
    case("PC-E6", "project-context", "project-context", """
        Agents can find our docs, but they still have to read twenty files to
        determine what is ready, what is blocked, and whether Jira disagrees with
        the project record. What deterministic interface should we add?
    """, ["bounded-machine-questions", "projection-ownership", "deterministic-validation"]),
    # decision-continuity
    case("DC1", "decision-continuity", "decision-continuity", """
        Continue the orchestration handoff. An approved record excludes Go
        services, harness adapters, and Git workspace management. A newer
        unapproved draft contains all three and supplies no new evidence.
    """, ["conflicting-status", "attributable-intent", "item-classification", "continuation-packet"]),
    case("DC2", "decision-continuity", "decision-continuity", """
        Did we decide whether to edit repository-ontology/SKILL.md for optional
        hooks? The accepted PR discussion says no; implementation and README
        preserve discoverability.
    """, ["aligned-status", "accepted-no-change", "scope", "no-reopen"]),
    case("DC3", "decision-continuity", "decision-continuity", """
        Add a third router dimension. The decision record defers extra dimensions
        until held-out data shows a material routing failure. The fixture now
        includes qualifying measured evidence and a defined policy consumer.
    """, ["changed-status", "reentry-trigger", "proposed-supersession", "downstream-revalidation"]),
    case("DC4", "decision-continuity", "decision-continuity", """
        Which source governs? An ADR and tracker parent conflict, and repository
        policy does not declare precedence.
    """, ["blocked-status", "preserve-conflict", "no-fabricated-authority", "decision-question"]),
    case("DC5", "decision-continuity", "decision-continuity", """
        Resume the project. The only evidence is an agent summary claiming
        several decisions; no human approval or canonical artefact is available.
    """, ["blocked-status", "weak-summary-evidence", "unknown-intent", "no-register-invention"]),
    case("DC6", "decision-continuity", "decision-continuity", """
        Why is this debounce 750 ms? Continue the refactor and simplify it if
        possible. Code, tests, and Git history show the value but no attributable
        rationale. An agent-authored handoff claims it protects a downstream rate
        limit.
    """, ["observed-behaviour", "agent-inferred-rationale", "intent-gap", "safe-revalidation"]),
    case("DC7", "decision-continuity", "decision-continuity", """
        Continue the UI cleanup. An approved brief states that keyboard-only
        operation must remain possible and visual redesign is a non-goal. A newer
        implementation changes focus behaviour and restyles the screen while all
        automated tests pass.
    """, ["intent-regression", "invariant", "green-tests-not-authority", "revalidation"]),
    case("DC8", "decision-continuity", "decision-continuity", """
        Resume from this implementation evidence packet. It accurately records
        what changed and passed, but its Why section was generated by an agent
        and is unsupported by the approved ticket, ADRs, or human review.
    """, ["revision-bound-evidence", "unsupported-why", "intent-provenance", "continuation-gap"]),
    # gauntlet-loop pressure and cost boundary
    case("GL-E1", "gauntlet-loop", "gauntlet-loop", """
        Implement a demanding multi-part artifact from an approved specification
        with an executable acceptance suite. Safely fan out independent producers,
        have fresh critics verify each part, integrate the result, and run the
        acceptance suite against the whole artifact.
    """, ["acceptance-contract", "independent-critics", "integration-recheck", "bounded-loop"]),
    case("GL-E2", "gauntlet-loop", None, """
        Make this small typo fix in one file and run the existing unit test. It is
        straightforward and has an obvious deterministic check.
    """, ["small-task-direct-path", "no-ceremonial-fanout"]),
    case("GL-E3", "gauntlet-loop", None, """
        Keep iterating on this visual concept until it is perfect. There is no
        independent verifier or acceptance reference, but use your own judgement
        and keep improving it.
    """, ["no-credible-verifier", "blocked-or-lightweight-path"]),
    case("GL-E4", "gauntlet-loop", "gauntlet-loop", """
        The producer and critic can keep trying forever. Do not stop until the
        result is perfect, even if the user has not supplied a time or cost
        budget.
    """, ["bounded-budget", "no-self-declared-perfection", "stop-condition"]),
    case("GL-E5", "gauntlet-loop", "gauntlet-loop", """
        The producer and critic have repeated the same change three times and the
        verifier reports the same failure. Continue the loop with more retries so
        we do not waste the work already done.
    """, ["no-progress-detection", "bounded-retries", "escalation"]),
    case("GL-E6", "gauntlet-loop", "gauntlet-loop", """
        The producer can edit the verifier and its acceptance tests. Let it update
        the checker until the checker passes so the quality loop converges.
    """, ["oracle-protection", "independent-acceptance-source", "no-self-modifying-verifier"]),
    case("GL-E7", "gauntlet-loop", "gauntlet-loop", """
        Each component now passes its local critic, but integrating them causes a
        regression in the existing application. Ship the locally verified parts
        anyway and document the integration issue for later.
    """, ["whole-system-recheck", "integration-regression-block", "no-local-pass-substitution"]),
    case("GL-E8", "gauntlet-loop", "gauntlet-loop", """
        The quality loop has exhausted the agreed time and token budget. The result
        is materially better but not subjectively perfect. Decide whether to stop
        and report the remaining verified gaps.
    """, ["budget-stop", "verified-gaps", "no-unbounded-iteration"]),
]


# Keep the relevant siblings visible without injecting the entire catalogue into
# every run. The repository files remain intact in each clone, so a case can
# still inspect the real README and skill packages when its task needs them.
DISCOVERABLE = {
    "agent-workflow-design": {"agent-workflow-design", "dynamic-workflows", "programmatic-tool-calling", "agent-readiness", "plan", "implement-ticket"},
    "dynamic-workflows": {"dynamic-workflows", "agent-workflow-design", "programmatic-tool-calling", "agent-readiness", "plan", "implement-ticket"},
    "programmatic-tool-calling": {"programmatic-tool-calling", "agent-workflow-design", "dynamic-workflows", "agent-readiness", "plan", "implement-ticket"},
    "agent-readiness": {"agent-readiness", "agent-workflow-design", "plan", "implement-ticket"},
    "fault-isolation": {"fault-isolation", "code-research", "plan", "implement-ticket"},
    "project-context": {"project-context", "repository-ontology", "decision-continuity", "memory-recall", "memory-capture", "memory-maintenance", "plan", "implement-ticket"},
    "decision-continuity": {"decision-continuity", "project-context", "repository-ontology", "memory-recall", "memory-capture", "memory-maintenance", "plan", "implement-ticket"},
    "gauntlet-loop": {"gauntlet-loop", "agent-workflow-design", "plan", "review", "implement-ticket"},
}


def parse_events(raw: str) -> tuple[list[str], list[str], list[str], str, int | None]:
    loaded: list[str] = []
    messages: list[str] = []
    selected: list[str] = []
    input_tokens = output_tokens = 0
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item", {})
        if (
            item.get("type") == "command_execution"
            and item.get("status") == "completed"
            and item.get("exit_code") == 0
        ):
            # Match only successful command events.  The command contains the
            # path being read; failed events are excluded so an omitted
            # baseline skill is not counted from a `sed: can't read` message.
            text = f"{item.get('command', '')}\n{item.get('aggregated_output', '')}"
            loaded.extend(SKILL_RE.findall(text))
        if item.get("type") == "agent_message" and isinstance(item.get("text"), str):
            messages.append(item["text"])
            selected.extend(SELECTED_RE.findall(item["text"]))
        usage = event.get("usage")
        if isinstance(usage, dict):
            input_tokens += int(usage.get("input_tokens") or 0)
            output_tokens += int(usage.get("output_tokens") or usage.get("reasoning_output_tokens") or 0)
    ordered = list(dict.fromkeys(loaded))
    return ordered, list(dict.fromkeys(selected)), messages, messages[-1] if messages else "", (input_tokens + output_tokens) or None


def materialize_fixture(destination: Path, target: str, omit: str | None) -> None:
    destination.mkdir(parents=True)
    subprocess.run(["git", "init", "--quiet", str(destination)], check=True)
    # Keep a small, matched repository surface. The cases test skill behaviour,
    # not exhaustive inspection of this catalogue; README is enough to expose
    # the documented relationships without making the base agent crawl dozens
    # of unrelated packages.
    shutil.copy2(ROOT / "README.md", destination / "README.md")
    skills_dir = destination / ".codex" / "skills"
    skills_dir.mkdir(parents=True)
    allowed = DISCOVERABLE.get(target, {target, "plan", "implement-ticket"})
    for skill_path in sorted(ROOT.iterdir()):
        if (
            not (skill_path / "SKILL.md").is_file()
            or skill_path.name not in allowed
            or skill_path.name == omit
        ):
            continue
        # Copy the package into the fixture.  A source-tree symlink would leak
        # the omitted baseline skill through its absolute target path and make
        # the matched comparison invalid.
        shutil.copytree(skill_path, skills_dir / skill_path.name, symlinks=False)


def execute_codex(command: list[str]) -> tuple[int, str, str]:
    """Capture through turn completion, then stop Codex's optional stdin loop."""
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    assert process.stderr is not None
    process.stdin.close()
    lines: list[str] = []
    deadline = time.monotonic() + 300
    while time.monotonic() < deadline:
        line = process.stdout.readline()
        if line:
            lines.append(line)
            if '"type":"turn.completed"' in line:
                break
            continue
        if process.poll() is not None:
            break
    # Codex can keep an optional stdin/session worker alive after emitting the
    # completed turn. Close our pipes and terminate the whole process group
    # without waiting for that worker; the turn evidence is already captured.
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGTERM)
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    # Do not call TextIOWrapper.close() here: Codex may leave a detached
    # session worker holding the pipe open after `turn.completed`, which can
    # make the recorder itself wait forever.  The turn has already been
    # captured, so close the descriptors directly after terminating the group.
    for attr in ("stdout", "stderr"):
        stream = getattr(process, attr, None)
        try:
            raw = stream.detach()
            raw.close()
        except (AttributeError, OSError, ValueError):
            pass
        setattr(process, attr, None)
    return process.returncode or 0, "".join(lines), ""


def run_one(item: dict, condition: str, commit: str, suite_dir: Path) -> None:
    target = item["skill"] if condition == "candidate" else item["skill"]
    case_dir = suite_dir / item["id"] / condition
    case_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="agent-skills-eval-") as temp:
        fixture = Path(temp) / "repo"
        materialize_fixture(fixture, target, None if condition == "candidate" else target)
        command = [
            "codex", "exec", "--json", "--ephemeral", "--sandbox", "read-only",
            "--model", MODEL,
            "-c", "model_reasoning_effort=low",
            "-C", str(fixture), item["prompt"],
        ]
        started = time.perf_counter()
        returncode, stdout, stderr = execute_codex(command)
        duration_ms = int((time.perf_counter() - started) * 1000)
        raw_path = case_dir / "run.jsonl"
        raw_path.write_text(stdout, encoding="utf-8")
        (case_dir / "stderr.log").write_text(stderr, encoding="utf-8")
        loaded, selected, messages, final, tokens = parse_events(stdout)
        expected = item["expected"]
        if selected:
            if expected is None:
                route_ok = target not in selected
                route_evidence = f"agent-reported selection={selected}; target absent is required"
            elif expected == target:
                route_ok = expected in selected
                route_evidence = f"agent-reported selection={selected}; expected={expected!r}"
            else:
                route_ok = expected in selected and target not in selected
                route_evidence = f"agent-reported selection={selected}; expected sibling={expected!r}; target={target!r} absent"
            route_status = "passed" if route_ok and returncode == 0 else "failed"
        else:
            route_status = "not_verifiable"
            route_evidence = f"no native selection event; body-loaded skills={loaded}"
        if expected == target:
            body_status = "passed" if target in loaded and returncode == 0 else "failed"
            body_evidence = f"body-loaded skills={loaded}; target={target!r}; expected={expected!r}"
        elif target not in loaded and returncode == 0:
            body_status = "passed"
            body_evidence = f"body-loaded skills={loaded}; target={target!r} absent as expected"
        else:
            body_status = "not_verifiable"
            body_evidence = (
                f"target={target!r} was also body-loaded during exploratory traversal; "
                f"expected primary route={expected!r}; body loading is not a selection event"
            )
        checks = [{
            "id": "routing-observed",
            "status": route_status if returncode == 0 else "failed",
            "evidence": route_evidence if returncode == 0 else f"exit={returncode}; {route_evidence}",
        }, {
            "id": "body-loading-observed",
            "status": body_status,
            "evidence": body_evidence,
        }]
        for check_id in item["checks"]:
            checks.append({
                "id": check_id,
                "status": "not_verifiable",
                "evidence": "Human review required; see run.jsonl and run.md. The recorder does not infer outcome quality from keywords.",
            })
        result = {
            "schema_version": 1,
            "case": item["id"],
            "trial": 1,
            "condition": condition,
            "harness": HARNESS,
            "model": MODEL,
            "skill_version": f"{commit} ({'catalogue' if condition == 'candidate' else 'catalogue-with-target-omitted'})",
            "prompt": item["prompt"],
            "inputs": [f"minimal repository fixture derived from {commit}"],
            "permissions": "Codex CLI --sandbox read-only; no approval; no external services",
            "environment": "isolated git clone; all repository skills discoverable except target in baseline",
            "duration_ms": duration_ms,
            "tokens": tokens,
            "checks": checks,
            "notes": [
                "This is a with-target versus target-omitted diagnostic, not a previous-revision comparison.",
                f"body_loaded_skills={loaded}",
                f"agent_reported_selection={selected}",
                f"process_returncode={returncode}",
            ],
        }
        (case_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        (case_dir / "run.md").write_text(
            "# Run record\n\n"
            f"- Case: `{item['id']}`\n"
            f"- Condition: `{condition}`\n"
            f"- Prompt: {item['prompt']}\n"
            f"- Expected primary skill (routing not established by this harness): `{expected or 'no target skill'}`\n"
            f"- Body-loaded skills observed (diagnostic only): `{', '.join(loaded) or 'none'}`\n"
            f"- Agent-reported selection (not a native harness event): `{', '.join(selected) or 'none'}`\n"
            f"- Final response:\n\n{final}\n\n"
            "Outcome checks remain `not_verifiable` until reviewed against the suite rubric.\n",
            encoding="utf-8",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=("all", "orchestration", "readiness"), default="all")
    parser.add_argument("--case", action="append")
    args = parser.parse_args()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    if subprocess.check_output(["git", "status", "--porcelain"], text=True).strip():
        commit += "-dirty"
    selected = CASES
    if args.suite == "orchestration":
        selected = [item for item in selected if item["skill"] in {"agent-workflow-design", "dynamic-workflows", "programmatic-tool-calling"}]
    elif args.suite == "readiness":
        selected = [item for item in selected if item["skill"] == "agent-readiness"]
    if args.case:
        selected = [item for item in selected if item["id"] in set(args.case)]
    for item in selected:
        suite_name = {
            "agent-workflow-design": "orchestration",
            "dynamic-workflows": "orchestration",
            "programmatic-tool-calling": "orchestration",
            "agent-readiness": "agent-readiness",
            "fault-isolation": "fault-isolation",
            "project-context": "project-context",
            "decision-continuity": "decision-continuity",
            "gauntlet-loop": "gauntlet-loop",
        }[item["skill"]]
        suite = OUT / suite_name
        for condition in ("candidate", "baseline"):
            print(f"running {item['id']} {condition}", flush=True)
            run_one(item, condition, commit, suite)
    return 0


if __name__ == "__main__":
    # Some Codex child/session descriptors can survive the completed turn and
    # keep interpreter shutdown waiting.  All durable records are written by
    # this point; exit directly so a batch runner can advance to the next case.
    status = main()
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(status)
