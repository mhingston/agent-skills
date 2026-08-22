#!/usr/bin/env python3
"""Behavioural tests for the wrap-up lifecycle hook and installer."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LIFECYCLE = SCRIPT_DIR / "lifecycle-hook.py"
INSTALLER = SCRIPT_DIR / "install-hook.py"


class WrapUpHookTests(unittest.TestCase):
    def run_python(
        self,
        script: Path,
        *args: str,
        stdin: dict | None = None,
        env: dict[str, str] | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            input=(json.dumps(stdin) if stdin is not None else None),
            text=True,
            capture_output=True,
            env=env,
            check=check,
        )

    def test_lifecycle_queue_remind_and_acknowledge(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "repo"
            workspace.mkdir()
            transcript = root / "ended-session.jsonl"
            transcript.write_text("{}\n", encoding="utf-8")
            state = root / "state"
            env = os.environ.copy()
            env["AGENT_SKILLS_WRAP_UP_STATE_DIR"] = str(state)

            ended = self.run_python(
                LIFECYCLE,
                "session-end",
                "--harness",
                "codex",
                stdin={
                    "hook_event_name": "SessionEnd",
                    "session_id": "ended-123",
                    "transcript_path": str(transcript),
                    "cwd": str(workspace),
                    "reason": "user_exit",
                },
                env=env,
            )
            self.assertEqual(ended.stdout, "")
            receipts = list(state.glob("*/*.json"))
            self.assertEqual(len(receipts), 1)
            receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
            self.assertEqual(receipt["session_id"], "ended-123")
            self.assertEqual(receipt["transcript_path"], str(transcript))
            self.assertNotIn("transcript", {key for key in receipt if key != "transcript_path"})

            reminder = self.run_python(
                LIFECYCLE,
                "session-start",
                "--harness",
                "codex",
                stdin={
                    "hook_event_name": "SessionStart",
                    "session_id": "new-456",
                    "cwd": str(workspace),
                },
                env=env,
            )
            self.assertIn("pending wrap-up", reminder.stdout)
            self.assertIn("ended-123", reminder.stdout)
            self.assertIn(str(transcript), reminder.stdout)

            self.run_python(
                LIFECYCLE,
                "ack",
                "--session-id",
                "ended-123",
                "--cwd",
                str(workspace),
                env=env,
            )
            self.assertFalse(receipts[0].exists())

            empty = self.run_python(
                LIFECYCLE,
                "session-start",
                "--harness",
                "codex",
                stdin={
                    "hook_event_name": "SessionStart",
                    "session_id": "new-789",
                    "cwd": str(workspace),
                },
                env=env,
            )
            self.assertEqual(empty.stdout, "")

    def test_installer_preview_does_not_mutate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "repo"
            repo.mkdir()
            preview = self.run_python(
                INSTALLER,
                "--harness",
                "claude-code",
                "--scope",
                "project",
                "--repo-root",
                str(repo),
            )
            result = json.loads(preview.stdout)
            self.assertEqual(result["mode"], "preview")
            self.assertTrue(result["config_changed"])
            self.assertCountEqual(result["added_handlers"], ["SessionStart", "SessionEnd"])
            self.assertFalse((repo / ".claude").exists())

    def test_installer_preserves_existing_hooks_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "repo"
            config_path = repo / ".claude" / "settings.json"
            config_path.parent.mkdir(parents=True)
            existing = {
                "permissions": {"allow": ["Read"]},
                "hooks": {
                    "PostToolUse": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "echo existing",
                                    "timeout": 4,
                                }
                            ]
                        }
                    ]
                },
            }
            config_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")

            first = self.run_python(
                INSTALLER,
                "--harness",
                "claude-code",
                "--scope",
                "project",
                "--repo-root",
                str(repo),
                "--apply",
            )
            first_result = json.loads(first.stdout)
            self.assertTrue(first_result["config_changed"])
            merged = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(merged["permissions"], existing["permissions"])
            self.assertEqual(merged["hooks"]["PostToolUse"], existing["hooks"]["PostToolUse"])
            self.assertEqual(len(merged["hooks"]["SessionStart"]), 1)
            self.assertEqual(len(merged["hooks"]["SessionEnd"]), 1)
            copied_hook = repo / ".claude" / "hooks" / "agent-skills-wrap-up.py"
            self.assertTrue(copied_hook.exists())

            before_config = config_path.read_bytes()
            before_hook = copied_hook.read_bytes()
            second = self.run_python(
                INSTALLER,
                "--harness",
                "claude-code",
                "--scope",
                "project",
                "--repo-root",
                str(repo),
                "--apply",
            )
            second_result = json.loads(second.stdout)
            self.assertFalse(second_result["config_changed"])
            self.assertFalse(second_result["hook_changed"])
            self.assertEqual(second_result["added_handlers"], [])
            self.assertEqual(config_path.read_bytes(), before_config)
            self.assertEqual(copied_hook.read_bytes(), before_hook)

    def test_codex_installer_preserves_hooks_and_warns_about_inline_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "repo"
            codex = repo / ".codex"
            codex.mkdir(parents=True)
            hooks_path = codex / "hooks.json"
            existing = {
                "description": "existing",
                "hooks": {
                    "Stop": [
                        {
                            "hooks": [
                                {"type": "command", "command": "echo stop", "timeout": 1}
                            ]
                        }
                    ]
                },
            }
            hooks_path.write_text(json.dumps(existing), encoding="utf-8")
            (codex / "config.toml").write_text("[hooks]\n", encoding="utf-8")

            applied = self.run_python(
                INSTALLER,
                "--harness",
                "codex",
                "--scope",
                "project",
                "--repo-root",
                str(repo),
                "--apply",
            )
            result = json.loads(applied.stdout)
            merged = json.loads(hooks_path.read_text(encoding="utf-8"))
            self.assertEqual(merged["description"], "existing")
            self.assertEqual(merged["hooks"]["Stop"], existing["hooks"]["Stop"])
            self.assertEqual(len(merged["hooks"]["SessionStart"]), 1)
            self.assertEqual(len(merged["hooks"]["SessionEnd"]), 1)
            self.assertTrue(any("inline hooks" in note for note in result["notes"]))

    def test_installer_refuses_malformed_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "repo"
            config = repo / ".claude" / "settings.json"
            config.parent.mkdir(parents=True)
            config.write_text("{not-json", encoding="utf-8")

            failed = self.run_python(
                INSTALLER,
                "--harness",
                "claude-code",
                "--scope",
                "project",
                "--repo-root",
                str(repo),
                "--apply",
                check=False,
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("refusing to modify malformed JSON", failed.stderr)
            self.assertEqual(config.read_text(encoding="utf-8"), "{not-json")


if __name__ == "__main__":
    unittest.main()
