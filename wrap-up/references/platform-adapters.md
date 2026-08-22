# Platform adapters

Read this reference only when detecting, previewing, installing, or debugging an
automatic wrap-up lifecycle hook.

These mappings were checked against the official product documentation on
**2026-08-22**. Hook APIs change quickly; re-check the canonical documentation
before changing event names, paths, trust semantics, output handling, command
forms, or timeout assumptions.

## Claude Code

Canonical documentation:

- <https://code.claude.com/docs/en/hooks>
- <https://code.claude.com/docs/en/hooks-guide>

Relevant current behaviour:

- user settings: `~/.claude/settings.json`;
- shared project settings: `.claude/settings.json`;
- local project settings: `.claude/settings.local.json`;
- plugin hooks may also live in a plugin's `hooks/hooks.json`;
- `SessionStart` runs when a session begins or resumes;
- `SessionEnd` runs when the session terminates;
- command-hook stdout on `SessionStart` can add context to Claude;
- `SessionEnd` has no decision control, so its output cannot keep the ending
  session alive or steer that same agent;
- command hooks support exec form via `command` plus `args`, avoiding shell
  tokenisation and providing a cross-platform way to invoke the copied Python
  helper;
- project hooks remain subject to workspace trust and managed policy;
- `/hooks` shows the effective hook set and source.

The bundled installer uses `.claude/settings.json` for project scope and
`~/.claude/settings.json` for user scope. It composes with existing `hooks`
entries rather than replacing the settings document and emits the helper command
in exec form.

Do not create a standalone `.claude/hooks.json`; Claude Code currently expects
project/user hooks under the `hooks` key in the corresponding settings file.

## Codex

Canonical documentation:

- <https://developers.openai.com/codex/hooks>
- <https://developers.openai.com/codex/config-reference>

Relevant current behaviour:

- user hooks may live in `~/.codex/hooks.json` or inline in
  `~/.codex/config.toml`;
- project hooks may live in `<repo>/.codex/hooks.json` or inline in
  `<repo>/.codex/config.toml`;
- matching hooks from multiple active files are composed;
- `SessionStart` command stdout is added as model-visible developer context;
- `SessionEnd` runs for the main thread only and remains advisory;
- `SessionEnd` runs synchronously, defaults to a short timeout, and currently
  supports at most a few seconds, so it is unsuitable for launching a blocking
  reflection agent;
- command handlers are the currently supported executable hook type;
- command handlers support a Windows-specific `commandWindows` override;
- non-managed hooks must be reviewed/trusted before they run;
- `/hooks` is the inspection and trust surface;
- managed policy may ignore project/user hooks.

The bundled installer deliberately uses `hooks.json` rather than editing TOML.
It emits a POSIX `command` plus `commandWindows` from the same argument vector so
paths with spaces are quoted according to the target shell. If the same Codex
config layer already contains inline `[hooks]`, Codex may merge both and warn. In
that situation prefer an operator-reviewed consolidation rather than silently
rewriting TOML.

## Adapter selection

When harness identity is explicit, use it. Otherwise infer conservatively from
active process/config evidence and ask only when the wrong choice would mutate a
different product's configuration.

Default to project scope for repository-specific learning. Use user scope only
when the operator explicitly wants the wrap-up lifecycle across projects.

Installation is not activation. After writing configuration, surface the
harness-specific trust or policy step that remains instead of claiming the hook
is active merely because the file exists.
