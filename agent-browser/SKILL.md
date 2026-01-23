---
name: agent-browser
description: Automates real browser interactions for web testing, form filling, screenshots/PDF export, and lightweight data extraction using the agent-browser CLI.
license: Apache-2.0
compatibility: >
  Requires Node.js + npm and the agent-browser CLI installed. For best reliability,
  install the bundled Chromium (`agent-browser install`) or connect to an existing browser via CDP.
allowed-tools: Bash(agent-browser:*)
metadata:
  docs: https://agent-browser.dev/
  vendor: vercel-labs
---

## When to use this skill

Use `agent-browser` when you need to:
- Navigate websites and interact with real UI elements (click/type/fill/select)
- Validate end-to-end flows (login, checkout, onboarding)
- Take screenshots or export PDFs
- Extract small amounts of structured information from pages
- Run reliable “agentic browsing” via **Snapshot + Refs** (stable element references)

Avoid for:
- Large-scale crawling (prefer dedicated crawlers)
- Heavy OCR (prefer native text extraction; screenshot only when needed)

---

## Installation / setup (if not installed)

```bash
npm install -g agent-browser
agent-browser install  # Download Chromium
````

Notes:

* If Chromium download is blocked in your environment, connect to an existing browser via CDP (see CDP section below).
* Use `--headed` when you need to visually observe the browser.

---

## Core concept: Snapshot + Refs (recommended)

1. Open a page:

```bash
agent-browser open https://example.com
```

2. Take a snapshot to get stable element refs (`@e1`, `@e2`, …):

```bash
agent-browser snapshot -i
# or JSON for machine parsing:
agent-browser snapshot -i --json
```

3. Interact using refs:

```bash
agent-browser click @e2
agent-browser fill @e3 "test@example.com"
agent-browser get text @e1
```

4. Re-snapshot after any major UI change (navigation, modal, dynamic load):

```bash
agent-browser snapshot -i
```

Why this matters:

* Refs are far less brittle than CSS/text selectors.
* Keeps the agent grounded in the current page structure.

---

## Selector strategy (best → worst)

1. **Refs from snapshot:** `@e12`
2. **Semantic locators:** `find role|label|text|placeholder|testid ...`
3. **CSS selectors:** `#id`, `.class`, `[data-testid="..."]`
4. **Text/XPath:** only as a last resort

---

## Reliability checklist

* Snapshot first, then act by `@e…` refs.
* Re-snapshot after navigation / DOM changes.
* Use `wait` on meaningful signals (URL/text/load/element) instead of arbitrary sleeps.
* If an action fails, snapshot again and re-check the ref.

---

## Common recipes

### Login flow (robust)

```bash
agent-browser open https://site.com/login
agent-browser snapshot -i --json
agent-browser fill @e2 "me@domain.com"
agent-browser fill @e3 "correct horse battery staple"
agent-browser click @e4
agent-browser wait --url "**/dashboard"
```

### Extract content

```bash
agent-browser get text @e10
agent-browser get attr @e10 href
agent-browser get count "text=Result"
```

### Screenshot/PDF

```bash
agent-browser screenshot page.png --full
agent-browser pdf page.pdf
```

---

## Sessions (isolated state)

Run multiple isolated sessions in parallel:

```bash
agent-browser --session agent1 open https://site-a.com
agent-browser --session agent2 open https://site-b.com
```

---

## CDP mode (connect to an existing browser)

If you already have a Chrome/Chromium instance running with remote debugging:

```bash
agent-browser connect 9222
# or
agent-browser --cdp 9222 snapshot -i
```

---

## Full command reference

See:

* `references/REFERENCE.md` (CLI surface area)
* `references/STREAMING.md` (WebSocket streaming protocol)

````

---

## `agent-browser/references/REFERENCE.md`

```md
# agent-browser CLI reference

This is a compact, agent-friendly reference to the `agent-browser` CLI.

## Core navigation & interaction

```bash
agent-browser open <url>                 # Navigate (aliases: goto, navigate)
agent-browser click <sel>                # Click element
agent-browser dblclick <sel>             # Double-click
agent-browser fill <sel> <text>          # Clear and fill
agent-browser type <sel> <text>          # Type into element
agent-browser press <key>                # Press key (alias: key)
agent-browser hover <sel>                # Hover element
agent-browser select <sel> <val>         # Select dropdown option
agent-browser check <sel>                # Check checkbox
agent-browser uncheck <sel>              # Uncheck checkbox
agent-browser scroll <dir> [px]          # Scroll (up/down/left/right)
agent-browser eval <js>                  # Run JavaScript
agent-browser close                      # Close browser
````

## Snapshots (refs)

```bash
agent-browser snapshot                   # Full accessibility tree
agent-browser snapshot -i                # Interactive/actionable only (recommended)
agent-browser snapshot -c                # Compact output
agent-browser snapshot -d 3              # Depth limit
agent-browser snapshot -s "#main"        # Scope to CSS selector
agent-browser snapshot --json            # Machine-readable output
```

Refs look like `@e1`, `@e2`, ... and are the preferred selectors for actions.

## Get page / element info

```bash
agent-browser get text <sel>             # Text content
agent-browser get html <sel>             # innerHTML
agent-browser get value <sel>            # Input value
agent-browser get attr <sel> <attr>      # Attribute value
agent-browser get title                  # Page title
agent-browser get url                    # Current URL
agent-browser get count <sel>            # Count matches
agent-browser get box <sel>              # Bounding box
```

## State checks

```bash
agent-browser is visible <sel>
agent-browser is enabled <sel>
agent-browser is checked <sel>
```

## Semantic element finding (stable-ish)

Actions include `click`, `fill`, `check`, `hover`, `text`.

```bash
agent-browser find role <role> <action> [value]
agent-browser find text <text> <action>
agent-browser find label <label> <action> [value]
agent-browser find placeholder <ph> <action> [value]
agent-browser find testid <id> <action> [value]
agent-browser find first <sel> <action> [value]
agent-browser find nth <n> <sel> <action> [value]
```

## Wait

Prefer waits over sleeps.

```bash
agent-browser wait <selector>            # Wait for element
agent-browser wait <ms>                  # Wait for time
agent-browser wait --text "Welcome"      # Wait for text
agent-browser wait --url "**/dash"       # Wait for URL glob
agent-browser wait --load networkidle    # Wait for load state
agent-browser wait --fn "condition"      # Wait for JS predicate
```

## Screenshots & PDF

```bash
agent-browser screenshot                 # base64 PNG to stdout
agent-browser screenshot page.png
agent-browser screenshot page.png --full
agent-browser pdf page.pdf
```

## Mouse

```bash
agent-browser mouse move <x> <y>
agent-browser mouse down [button]
agent-browser mouse up [button]
agent-browser mouse wheel <dy> [dx]
```

## Tabs & frames

```bash
agent-browser tab
agent-browser tab new [url]
agent-browser tab <n>
agent-browser tab close [n]
agent-browser frame <sel>
agent-browser frame main
```

## Cookies & storage

```bash
agent-browser cookies
agent-browser cookies set <name> <val>
agent-browser cookies clear

agent-browser storage local
agent-browser storage local <key>
agent-browser storage local set <k> <v>
agent-browser storage local clear

agent-browser storage session            # sessionStorage variants
```

## Network (routing / inspection)

```bash
agent-browser network route <url-glob>
agent-browser network route <url-glob> --abort
agent-browser network route <url-glob> --body <json>
agent-browser network unroute [url-glob]
agent-browser network requests
```

## Debug / tooling

```bash
agent-browser trace start [path]
agent-browser trace stop [path]
agent-browser console
agent-browser errors
agent-browser highlight <sel>
agent-browser state save <path>
agent-browser state load <path>
```

## Navigation helpers

```bash
agent-browser back
agent-browser forward
agent-browser reload
```

## Sessions (isolated state)

```bash
agent-browser --session <name> <command>
AGENT_BROWSER_SESSION=<name> agent-browser <command>

agent-browser session list
agent-browser session
```

## CDP mode (connect to existing browser)

```bash
agent-browser connect 9222
agent-browser --cdp 9222 snapshot -i
```

## Common global options (typical)

* `--session <name>` isolate state per session
* `--json` JSON output
* `--full, -f` full-page screenshot
* `--headed` show the browser window
* `--cdp <port>` connect via Chrome DevTools Protocol
* `--debug` verbose/debug output

````

---

## `agent-browser/references/STREAMING.md`

```md
# agent-browser streaming (WebSocket live control)

Streaming provides real-time, bidirectional control of a browser session over WebSockets.
Use it for:
- Live agent control loops (observe → decide → act)
- Human-in-the-loop UIs
- Remote browser visualization/debugging
- Long-running sessions with incremental actions

## Start streaming server

```bash
agent-browser stream
````

Common options:

```bash
agent-browser stream --port 3001
agent-browser stream --headed
agent-browser stream --session my-session
agent-browser stream --cdp 9222
```

The server exposes a WebSocket endpoint (typically `ws://localhost:<port>`).
All messages are JSON.

---

## Client → server messages

### Open / navigate

```json
{ "type": "open", "url": "https://example.com" }
```

### Snapshot

```json
{ "type": "snapshot", "interactive": true, "json": true }
```

Useful snapshot options:

* `interactive`: only actionable elements (recommended)
* `depth`: limit tree depth
* `scope`: CSS selector to scope snapshot
* `compact`: reduce verbosity

### Click

```json
{ "type": "click", "selector": "@e12" }
```

Selectors can be:

* Snapshot refs: `@e12` (best)
* CSS selectors
* Semantic locators (role/label/text/testid), if supported by your server build

### Fill / type

```json
{ "type": "fill", "selector": "@e5", "value": "user@example.com" }
```

```json
{ "type": "type", "selector": "@e6", "value": "hello world" }
```

### Keyboard press

```json
{ "type": "press", "key": "Enter" }
```

Supports modifiers like `Control+A`, `Shift+Tab`.

### Mouse input

```json
{ "type": "mouse", "action": "move", "x": 420, "y": 300 }
```

Typical `action` values:

* `move`
* `down`
* `up`
* `wheel`

### Wait

```json
{ "type": "wait", "url": "**/dashboard" }
```

Other common wait modes:

* `text`
* `selector`
* `load` (e.g. `networkidle`)
* `timeout`
* `fn` (JS predicate)

### Eval (JavaScript)

```json
{ "type": "eval", "expression": "document.title" }
```

### Screenshot / PDF

```json
{ "type": "screenshot", "full": true }
```

```json
{ "type": "pdf" }
```

### Tabs / frames

```json
{ "type": "tab", "action": "new", "url": "https://example.com" }
```

```json
{ "type": "frame", "selector": "iframe#checkout" }
```

### Network routing

```json
{ "type": "network.route", "url": "**/api/**", "abort": true }
```

```json
{ "type": "network.route", "url": "**/config.json", "body": "{\"ok\":true}" }
```

---

## Server → client messages

### Snapshot response

```json
{ "type": "snapshot", "tree": { /* accessibility tree + @e refs */ } }
```

### Navigation

```json
{ "type": "navigation", "url": "https://example.com/dashboard" }
```

### Console events

```json
{ "type": "console", "level": "log", "message": "Hello from page" }
```

### Network events

```json
{ "type": "network.request", "url": "https://api.example.com/data", "method": "GET" }
```

### Errors

```json
{ "type": "error", "message": "Uncaught TypeError" }
```

### Video/screenshot frames (for live preview)

```json
{ "type": "frame", "encoding": "base64", "data": "iVBORw0KGgoAAA..." }
```

---

## Recommended agent streaming loop

1. Connect WebSocket
2. `open` URL
3. `snapshot` (interactive)
4. Act using refs
5. Re-snapshot after navigation/DOM changes
6. Prefer `wait` messages over sleeps

---

## Security notes

* Streaming grants full browser control.
* Avoid exposing the WebSocket port publicly.
* Prefer localhost, VPN, or a secured tunnel.
