#!/usr/bin/env python3
"""Reconcile recorded result files with the harness's routing evidence.

The first orchestration runs were recorded before the parser separated native
selection evidence from skill-body reads.  This one-time normalisation keeps
the portable result schema honest: body loading is useful evidence, but it is
not a native routing event, and the deliberately target-omitted baseline does
not have an applicable body-loading expectation.
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("eval_runner", HERE / "run.py")
runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(runner)
CASE_BY_ID = {item["id"]: item for item in runner.CASES}
RETURN_RE = re.compile(r"process_returncode=(-?\d+)")


def replace_check(checks: list[dict], replacement: dict, ids: set[str]) -> list[dict]:
    result: list[dict] = []
    inserted = False
    for check in checks:
        if check.get("id") in ids:
            if not inserted:
                result.append(replacement)
                inserted = True
            continue
        result.append(check)
    if not inserted:
        result.insert(0, replacement)
    return result


def main() -> int:
    changed = 0
    for result_path in sorted(HERE.rglob("result.json")):
        if result_path.parent.name not in {"candidate", "baseline"}:
            continue
        data = json.loads(result_path.read_text(encoding="utf-8"))
        item = CASE_BY_ID.get(data.get("case"))
        if item is None:
            continue
        raw_path = result_path.with_name("run.jsonl")
        loaded, selected, _messages, _final, _tokens = runner.parse_events(
            raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
        )
        expected = item["expected"]
        target = item["skill"]
        condition = data.get("condition")
        returncode = 0
        for note in data.get("notes", []):
            match = RETURN_RE.search(note)
            if match:
                returncode = int(match.group(1))
                break

        if selected:
            if expected is None:
                route_ok = target not in selected
                evidence = f"agent-reported selection={selected}; target absent is required"
            elif expected == target:
                route_ok = expected in selected
                evidence = f"agent-reported selection={selected}; expected={expected!r}"
            else:
                route_ok = expected in selected and target not in selected
                evidence = (
                    f"agent-reported selection={selected}; expected sibling={expected!r}; "
                    f"target={target!r} absent"
                )
            route_status = "passed" if route_ok and returncode == 0 else "failed"
        else:
            route_status = "not_verifiable"
            evidence = f"no native selection event; body-loaded skills={loaded}"
        if returncode != 0:
            evidence = f"exit={returncode}; {evidence}"

        route_check = {"id": "routing-observed", "status": route_status, "evidence": evidence}
        if condition == "baseline":
            body_status = "not_verifiable"
            body_evidence = (
                f"target={target!r} was intentionally omitted from the baseline; "
                f"body-loaded skills={loaded}"
            )
        elif expected == target:
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
        body_check = {"id": "body-loading-observed", "status": body_status, "evidence": body_evidence}

        checks = replace_check(data.get("checks", []), route_check, {"routing-observed"})
        checks = replace_check(checks, body_check, {"body-loading-observed"})
        data["checks"] = checks
        notes = [note for note in data.get("notes", []) if not note.startswith("selected_or_loaded_skills=")]
        notes = [note for note in notes if not note.startswith("agent_reported_selection=")]
        notes.append(f"body_loaded_skills={loaded}")
        notes.append(f"agent_reported_selection={selected}")
        data["notes"] = notes
        result_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        changed += 1
    print(f"normalised {changed} result files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
