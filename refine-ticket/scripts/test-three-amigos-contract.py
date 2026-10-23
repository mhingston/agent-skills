#!/usr/bin/env python3
"""Static presence guard, not evidence of behavioural agent improvement."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_RULES = {
    "review stage": "## 0b. Three-amigos review",
    "single-context perspectives": "not separate agents",
    "Business lens": "**Business**",
    "Engineering lens": "**Engineering**",
    "QA lens": "**QA**",
    "observed evidence": "`observed`",
    "unconfirmed recommendation": "`recommended`",
    "human-settled authority": "`settled`",
    "no recommendation promotion": "Never promote a `recommended` rule",
    "disagreement escalation": "When lenses disagree",
    "traced examples": "Each published example traces to an",
    "open questions block readiness": "no material unresolved three-amigos question",
}


def missing_contract(skill: str, scenarios: str) -> list[str]:
    missing = [name for name, marker in REQUIRED_RULES.items() if marker not in skill]
    for number in range(5, 9):
        if not re.search(rf"(?m)^## RT-{number} — ", scenarios):
            missing.append(f"RT-{number} behavioural fixture")
    return missing


def main() -> int:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    scenarios = (ROOT / "evals" / "scenarios.md").read_text(encoding="utf-8")
    missing = missing_contract(skill, scenarios)
    if missing:
        for entry in missing:
            print(f"FAIL missing refinement review contract: {entry}")
        return 1
    # Negative controls ensure this check detects the regression it is for.
    assert "review stage" in missing_contract(
        skill.replace("## 0b. Three-amigos review", ""), scenarios
    )
    assert "RT-5 behavioural fixture" in missing_contract(
        skill, scenarios.replace("## RT-5 — ", "## DELETED — ")
    )
    print("PASS refinement review contract presence (behavioural scenarios NOT_RUN)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
