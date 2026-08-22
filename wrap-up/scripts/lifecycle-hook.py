#!/usr/bin/env python3
"""Queue ended sessions and remind the next session to run wrap-up.

This helper is intentionally deterministic. It never invokes a model and never
reads transcript contents; it stores only the transcript path and session
metadata needed by the wrap-up skill.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_ENV = "AGENT_SKILLS_WRAP_UP_STATE_DIR"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def state_root() -> Path:
    override = os.environ.get(STATE_ENV)
    if override:
        return Path(override).expanduser()
    if os.name == "nt" and os.environ.get("LOCALAPPDATA"):
        return Path(os.environ["LOCALAPPDATA"]) / "agent-skills" / "wrap-up"
    if os.environ.get("XDG_STATE_HOME"):
        return Path(os.environ["XDG_STATE_HOME"]) / "agent-skills" / "wrap-up"
    return Path.home() / ".local" / "state" / "agent-skills" / "wrap-up"


def canonical_cwd(value: str | None) -> str:
    if not value:
        return str(Path.cwd().resolve())
    return str(Path(value).expanduser().resolve())


def workspace_key(cwd: str) -> str:
    return hashlib.sha256(cwd.encode("utf-8")).hexdigest()[:20]


def safe_session_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")
    return cleaned[:120] or "unknown-session"


def workspace_dir(cwd: str) -> Path:
    return state_root() / workspace_key(cwd)


def pending_path(cwd: str, session_id: str) -> Path:
    return workspace_dir(cwd) / f"{safe_session_id(session_id)}.json"


def load_stdin_json() -> dict[str, Any]:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid hook JSON input: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("hook input must be a JSON object")
    return payload


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temp, path)


def queue_session(harness: str) -> int:
    payload = load_stdin_json()
    session_id = str(payload.get("session_id") or "").strip()
    transcript_path = payload.get("transcript_path")
    cwd = canonical_cwd(payload.get("cwd"))

    if not session_id:
        print("wrap-up lifecycle hook: missing session_id", file=sys.stderr)
        return 2
    if not transcript_path:
        print("wrap-up lifecycle hook: missing transcript_path", file=sys.stderr)
        return 2

    record = {
        "schema_version": "1",
        "session_id": session_id,
        "transcript_path": str(transcript_path),
        "cwd": cwd,
        "harness": harness,
        "hook_event_name": payload.get("hook_event_name", "SessionEnd"),
        "reason": payload.get("reason"),
        "queued_at": utc_now(),
    }
    atomic_write_json(pending_path(cwd, session_id), record)
    return 0


def load_pending(cwd: str, current_session_id: str | None = None) -> list[tuple[Path, dict[str, Any]]]:
    directory = workspace_dir(cwd)
    if not directory.exists():
        return []

    records: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(directory.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        if current_session_id and data.get("session_id") == current_session_id:
            continue
        if canonical_cwd(str(data.get("cwd") or cwd)) != cwd:
            continue
        records.append((path, data))

    records.sort(key=lambda item: str(item[1].get("queued_at") or ""))
    return records


def remind_pending(harness: str) -> int:
    payload = load_stdin_json()
    cwd = canonical_cwd(payload.get("cwd"))
    current_session_id = str(payload.get("session_id") or "").strip() or None
    pending = load_pending(cwd, current_session_id)
    if not pending:
        return 0

    path, record = pending[0]
    total = len(pending)
    message = (
        "A previous agent session in this workspace has a pending wrap-up. "
        "Before starting unrelated new work, invoke the `wrap-up` skill against "
        f"session {record.get('session_id')!r} using transcript "
        f"{record.get('transcript_path')!r}. Pending receipt: {str(path)!r}. "
        "After successful capture, acknowledge that session with the wrap-up "
        "lifecycle helper so the reminder is not repeated."
    )
    if total > 1:
        message += f" There are {total - 1} additional pending wrap-ups for this workspace."

    # Plain stdout is model-visible additional context for SessionStart in both
    # Claude Code and Codex, keeping this adapter schema-neutral.
    print(message)
    return 0


def acknowledge(session_id: str, cwd_value: str | None) -> int:
    if cwd_value:
        path = pending_path(canonical_cwd(cwd_value), session_id)
        if path.exists():
            path.unlink()
            return 0
        return 1

    matches = list(state_root().glob(f"*/{safe_session_id(session_id)}.json"))
    if len(matches) == 1:
        matches[0].unlink()
        return 0
    if not matches:
        return 1
    print("multiple pending records matched; pass --cwd to disambiguate", file=sys.stderr)
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    for command in ("session-end", "session-start"):
        child = sub.add_parser(command)
        child.add_argument("--harness", choices=("claude-code", "codex"), required=True)

    ack = sub.add_parser("ack")
    ack.add_argument("--session-id", required=True)
    ack.add_argument("--cwd")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "session-end":
        return queue_session(args.harness)
    if args.command == "session-start":
        return remind_pending(args.harness)
    if args.command == "ack":
        return acknowledge(args.session_id, args.cwd)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
