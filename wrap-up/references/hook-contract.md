# Wrap-up lifecycle hook contract

Read this reference only when automatic lifecycle capture is being considered or
installed.

## Purpose

The hook exists to make a completed session discoverable to a later `wrap-up`
run. It is not the reflection engine itself and it must not silently promote one
session into durable instructions.

Keep the lifecycle adapter deterministic and thin:

```text
SessionEnd
    -> queue receipt(session id, transcript path, cwd, harness, reason)

next SessionStart in same workspace
    -> add model-visible context describing oldest pending receipt

wrap-up succeeds
    -> acknowledge receipt
```

## Why not use Stop as the default

`Stop` fires at the end of ordinary agent turns, not only when an interactive
session is truly finished. A mandatory wrap-up `Stop` hook therefore risks an
extra model turn on routine replies or repeated blocking loops.

Use `SessionEnd` as the lifecycle signal. Because supported harnesses treat
`SessionEnd` as advisory and do not let its output steer the already-ending
agent, queue the receipt and surface it on the next `SessionStart` rather than
launching a recursive or detached agent process.

A product-specific integration may choose a stronger end-of-task signal when the
runtime exposes one with reliable semantics. Do not generalise such a signal into
the canonical skill without version-checked evidence.

## Receipt schema

The bundled helper writes only:

```json
{
  "schema_version": "1",
  "session_id": "...",
  "transcript_path": "...",
  "cwd": "...",
  "harness": "claude-code | codex",
  "hook_event_name": "SessionEnd",
  "reason": "...",
  "queued_at": "..."
}
```

Do not copy transcript contents into hook state. The wrap-up skill reads the
transcript from the harness-owned path when it later processes the receipt.

The state directory is selected in this order:

1. `AGENT_SKILLS_WRAP_UP_STATE_DIR`;
2. `%LOCALAPPDATA%/agent-skills/wrap-up` on Windows;
3. `$XDG_STATE_HOME/agent-skills/wrap-up` when configured;
4. `~/.local/state/agent-skills/wrap-up`.

Workspace directories use a hash of the canonical working directory so unrelated
repositories do not consume each other's pending receipts.

## Installation contract

The installer is preview-first. Without `--apply` it reports the target config,
copied hook path, and handlers it would add.

With `--apply` it may:

- create the harness hook directory;
- copy the deterministic lifecycle helper into that directory;
- create a missing JSON hook/settings file;
- add one `SessionStart` and one `SessionEnd` command handler when equivalent
  wrap-up handlers are not already present.

It must not:

- delete, reorder, or replace unrelated hook groups;
- repair malformed JSON by guessing the operator's intent;
- toggle managed policy or hook trust;
- disable another hook;
- enable a globally disabled hook subsystem without explicit operator intent;
- write transcript contents into the hook configuration or receipt.

Repeated installation must not duplicate handlers. Updating the bundled helper
may refresh the copied helper while preserving the existing configuration.

## Failure semantics

`SessionEnd` capture should fail visibly when required identity or transcript path
is absent. Do not manufacture a receipt that cannot later be resolved.

`SessionStart` should remain advisory. If a pending record is malformed, leave it
in place and continue rather than deleting evidence. If the model ignores the
reminder, the receipt remains pending for a later session.

Acknowledge a receipt only after `wrap-up` has produced a usable observation
packet. Missing or unreadable transcripts remain pending so the loss is visible.

## Security and privacy

- Store transcript references, not transcript copies.
- Treat transcript paths and session IDs as local operational metadata.
- Do not upload hook state or observations to a remote system unless the user has
  configured and authorised that destination.
- Preserve harness workspace trust and managed-hook policy.
- Hook installation is a configuration mutation; preview and approval are part of
  the contract, not optional UX polish.
