#!/usr/bin/env python3
"""Preview or install the wrap-up lifecycle hooks for Claude Code or Codex."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

HOOK_BASENAME = "agent-skills-wrap-up.py"
MARKER = HOOK_BASENAME


def repo_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        return Path(result.stdout.strip()).resolve()
    except (OSError, subprocess.CalledProcessError):
        return Path.cwd().resolve()


def locations(harness: str, scope: str, root: Path) -> tuple[Path, Path]:
    home = Path.home()
    if harness == "claude-code":
        base = (root / ".claude") if scope == "project" else (home / ".claude")
        return base / "settings.json", base / "hooks" / HOOK_BASENAME
    if harness == "codex":
        base = (root / ".codex") if scope == "project" else (home / ".codex")
        return base / "hooks.json", base / "hooks" / HOOK_BASENAME
    raise ValueError(harness)


def load_config(path: Path, harness: str) -> dict[str, Any]:
    if not path.exists():
        if harness == "codex":
            return {"description": "Project lifecycle hooks.", "hooks": {}}
        return {"hooks": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"refusing to modify malformed JSON at {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"refusing to modify non-object JSON at {path}")
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise SystemExit(f"refusing to modify {path}: top-level 'hooks' is not an object")
    return data


def shell_command(script_path: Path, action: str, harness: str) -> str:
    # Use the interpreter that performed installation so paths with spaces are safe
    # on POSIX shells and the copied helper does not depend on PATH resolving a
    # different Python.
    parts = [sys.executable, str(script_path), action, "--harness", harness]
    return " ".join(shlex.quote(part) for part in parts)


def handler_exists(groups: Any, action: str) -> bool:
    if not isinstance(groups, list):
        return False
    for group in groups:
        if not isinstance(group, dict):
            continue
        handlers = group.get("hooks")
        if not isinstance(handlers, list):
            continue
        for handler in handlers:
            if not isinstance(handler, dict):
                continue
            command = str(handler.get("command") or "")
            if MARKER in command and action in command:
                return True
    return False


def add_handler(config: dict[str, Any], event: str, action: str, harness: str, script_path: Path) -> bool:
    hooks = config["hooks"]
    groups = hooks.setdefault(event, [])
    if not isinstance(groups, list):
        raise SystemExit(f"refusing to modify hook event {event!r}: expected an array")
    if handler_exists(groups, action):
        return False

    groups.append(
        {
            "hooks": [
                {
                    "type": "command",
                    "command": shell_command(script_path, action, harness),
                    "timeout": 2,
                }
            ]
        }
    )
    return True


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    os.replace(temp, path)


def apply_install(
    config_path: Path,
    hook_path: Path,
    config: dict[str, Any],
    source_hook: Path,
    *,
    config_changed: bool,
    hook_changed: bool,
) -> None:
    if hook_changed:
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_hook, hook_path)
        try:
            hook_path.chmod(hook_path.stat().st_mode | 0o111)
        except OSError:
            pass
    if config_changed:
        atomic_write(config_path, json.dumps(config, indent=2, sort_keys=False) + "\n")


def codex_inline_hook_note(config_path: Path, harness: str) -> str | None:
    if harness != "codex":
        return None
    config_toml = config_path.with_name("config.toml")
    if not config_toml.exists():
        return None
    try:
        text = config_toml.read_text(encoding="utf-8")
    except OSError:
        return f"Could not inspect sibling {config_toml}; review it for inline hooks before applying."
    if "[hooks" in text:
        return (
            f"Sibling {config_toml} appears to contain inline hooks. Codex may merge both sources and warn; "
            "review or consolidate them instead of assuming this installer owns the whole hook layer."
        )
    return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harness", choices=("claude-code", "codex"), required=True)
    parser.add_argument("--scope", choices=("project", "user"), default="project")
    parser.add_argument("--repo-root", help="Project root for project-scoped installation")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the copied helper and merged configuration. Without this flag, preview only.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = repo_root(args.repo_root)
    config_path, hook_path = locations(args.harness, args.scope, root)
    source_hook = Path(__file__).with_name("lifecycle-hook.py")
    if not source_hook.exists():
        raise SystemExit(f"bundled lifecycle helper is missing: {source_hook}")

    config_existed = config_path.exists()
    config = load_config(config_path, args.harness)
    added_start = add_handler(config, "SessionStart", "session-start", args.harness, hook_path)
    added_end = add_handler(config, "SessionEnd", "session-end", args.harness, hook_path)
    source_text = source_hook.read_text(encoding="utf-8")
    hook_changed = not hook_path.exists() or hook_path.read_text(encoding="utf-8") != source_text
    config_changed = added_start or added_end or not config_existed

    summary = {
        "mode": "apply" if args.apply else "preview",
        "harness": args.harness,
        "scope": args.scope,
        "config_path": str(config_path),
        "hook_path": str(hook_path),
        "config_changed": config_changed,
        "hook_changed": hook_changed,
        "added_handlers": [
            event
            for event, added in (("SessionStart", added_start), ("SessionEnd", added_end))
            if added
        ],
        "notes": [],
    }

    if args.harness == "claude-code":
        summary["notes"].append("Verify project/workspace trust and inspect the effective hooks with /hooks.")
        if config.get("disableAllHooks") is True:
            summary["notes"].append("disableAllHooks is true in this settings file; installation will not make hooks active.")
    else:
        summary["notes"].append("Review and trust new or changed non-managed hooks with /hooks before expecting them to run.")
        summary["notes"].append("Managed policy may restrict project or user hooks; installation does not bypass policy.")
        inline_note = codex_inline_hook_note(config_path, args.harness)
        if inline_note:
            summary["notes"].append(inline_note)

    if args.apply:
        apply_install(
            config_path,
            hook_path,
            config,
            source_hook,
            config_changed=config_changed,
            hook_changed=hook_changed,
        )

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
