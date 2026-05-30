---
name: "search-eureka-sessions"
description: "Find Eureka sessions using natural language queries with filters for time, flags, pins, status, topics, and parent-child relationships"
alwaysAllow: ["Bash", "Read", "Glob", "Grep"]
---

# Search Eureka Sessions

Search and find Eureka sessions (COS sessions, task sessions, and sub-agents) using natural language.

## How Sessions Are Stored

Eureka sessions live in two directories under the workspace root (`~/.eureka/workspaces/{workspaceId}/`):

- **`cos-sessions/{id}/session.jsonl`** — Top-level COS (Chief of Staff) sessions. These are the main conversation threads the user sees.
- **`sessions/{id}/session.jsonl`** — Task sessions and sub-agent sessions spawned by COS sessions.

Each `session.jsonl` is JSONL format. **Line 1** is the `SessionHeader` (JSON metadata). Lines 2+ are messages.

### Session ID Format
`YYMMDD-adjective-noun` (e.g., `260525-early-inlet`). The date prefix is the creation date.

### Session Header Fields (Line 1)

| Field | Description |
|-------|-------------|
| `id` | Session ID |
| `type` | `cos`, `task`, `runner`, or `sub-agent` |
| `name` | Session title/name (often AI-generated summary) |
| `createdAt` | Unix timestamp (ms) |
| `lastUsedAt` | Unix timestamp (ms) |
| `isFlagged` | Boolean — user starred/flagged |
| `isPinned` | Boolean — pinned to top |
| `todoState` | Workflow status: `todo`, `in-progress`, `needs-review`, `done`, `cancelled` |
| `parentSessionId` | Parent session ID (for task/sub-agent) |
| `engine` | Agent engine: `claude`, `codex`, `copilot` |
| `model` | LLM model used |
| `source` | Origin: `app`, `discord`, `telegram`, `slack`, `teams`, `cli`, `api`, `office` |
| `messageCount` | Total messages |
| `userMessageCount` | User messages only |
| `preview` | First ~150 chars of first user message |
| `workingDirectory` | Working directory path |
| `tokenUsage` | `{inputTokens, outputTokens, totalTokens, costUsd}` |
| `hiddenFromList` | Boolean — hidden/internal sessions |

### Session Hierarchy
```
COS Session (cos-sessions/)
  └── Task Session (sessions/, parentSessionId → COS)
      └── Sub-Agent (sessions/, parentSessionId → Task)
```

## How to Search

### Step 1: Determine the workspace root

**Do NOT hardcode the workspace path.** Derive it at runtime so the skill is portable.

The skill always runs from somewhere inside `...\.eureka\workspaces\{workspaceId}\...`. The workspace root is the `...\.eureka\workspaces\{workspaceId}` directory — i.e. the one that contains the `sessions/` and `cos-sessions/` subfolders. Walk up from the current working directory until you find a directory containing both `sessions` and `cos-sessions` (or matches the `.eureka/workspaces/<id>` pattern):

```python
import os

def find_workspace_root(start=None):
    d = os.path.abspath(start or os.getcwd())
    while True:
        # workspace root contains the sessions store
        if os.path.isdir(os.path.join(d, "sessions")) or os.path.isdir(os.path.join(d, "cos-sessions")):
            # confirm it's under .eureka/workspaces
            parent = os.path.basename(os.path.dirname(d))
            if parent == "workspaces":
                return d
        nd = os.path.dirname(d)
        if nd == d:  # reached filesystem root
            raise RuntimeError("Could not locate Eureka workspace root from " + os.getcwd())
        d = nd

WS_ROOT = find_workspace_root()
```

### Step 2: Collect session headers

Read **only line 1** from each `session.jsonl` to get metadata.

**CRITICAL — Windows compatibility:**
- Always use `python3` (not inline python via `-c` which breaks on Windows batch shells).
- Always write Python scripts to a temp file first, then execute.
- Always open files with `encoding='utf-8'` — sessions contain Chinese and other non-ASCII text.
- Use `os.path.join()` or raw strings for Windows paths.
- Use Python's `tempfile` or a known safe temp directory (`os.environ.get('TEMP', '/tmp')`).

Use this pattern:

```python
import json, os, glob

# WS_ROOT comes from find_workspace_root() in Step 1 — do not hardcode it.
headers = []

for pattern in [
    os.path.join(WS_ROOT, "cos-sessions", "*", "session.jsonl"),
    os.path.join(WS_ROOT, "sessions", "*", "session.jsonl"),
]:
    for fp in glob.glob(pattern):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line:
                    headers.append(json.loads(first_line))
        except Exception:
            pass
```

**IMPORTANT:** Always write the Python script to a `.py` file first, then run it:
```bash
cat > "$TEMP/search_sessions.py" << 'PYEOF'
# ... script content ...
PYEOF
python3 "$TEMP/search_sessions.py"
```

**NEVER use `python3 -c "..."` or `python3 << 'EOF'`** — these break on Windows due to batch shell escaping.

### Step 3: Filter and match

Parse the user's natural language query into filters:

**Topic/keyword search** — Match against `name` and `preview` fields (case-insensitive). For deeper search, read message content from JSONL lines 2+.

**Time range** — Parse relative dates ("last week", "yesterday", "May 2026") and compare against `createdAt` or `lastUsedAt` timestamps.

**Flags/pins** — Filter by `isFlagged: true` or `isPinned: true`.

**Status** — Filter by `todoState` values: `todo`, `in-progress`, `needs-review`, `done`, `cancelled`.

**Session type** — Filter by `type`: `cos` (main conversations), `task` (background tasks), `sub-agent`, `runner` (scheduled).

**Parent-child** — Use `parentSessionId` to find sub-agents of a task, or tasks spawned by a COS session.

**Engine/model** — Filter by `engine` or `model` fields.

**Source** — Filter by `source` field (app, teams, slack, etc.).

**Cost/usage** — Sort or filter by `tokenUsage.costUsd` or `tokenUsage.totalTokens`.

### Step 4: Rank results

Rank results by a combined relevance score:
1. **Keyword match strength** — exact match in name > partial match in name > match in preview > match in message content
2. **Recency** — more recently used sessions score higher
3. **Message count / engagement** — sessions with more messages may be more substantive

### Step 5: Present results

**CRITICAL — Clickable session links:**
Use the `task://` protocol to make session names clickable. In markdown output, format links as:
```
[Session Name](task://session-id)
```
This creates a clickable link that navigates directly to the session in Eureka.

**For top results (top 1-3 by relevance)**, show rich detail with snippets:

```markdown
1. [Session Name](task://session-id)
   `type` · `engine` · `model` · updated YYYY-MM-DD
   Summary: Brief description of what happened in the session based on name/preview.
   Match: Show the matched keyword context — which fields matched and relevant snippets.
```

**For remaining results**, show a compact list:

```markdown
1. [Session Name](task://session-id)
   Summary: one-line based on preview/name
```

**For deep content matches**, also show message snippet context:
- When a keyword was found inside message bodies (not just name/preview), show the surrounding context with the match highlighted in backticks or bold.

Always show results in the user's timezone (Asia/Shanghai).

## Deep Content Search

When the user's query doesn't match well against session names/previews, or when they ask for deeper search, read message content:

```python
# Read messages from a session (skip header line 0)
with open(session_jsonl_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i == 0: continue  # skip header
        msg = json.loads(line)
        content = msg.get("content", "")
        if isinstance(content, str) and keyword.lower() in content.lower():
            # Found a match — extract surrounding context for snippet
            idx = content.lower().index(keyword.lower())
            snippet = content[max(0, idx-80):idx+len(keyword)+80]
            # ... collect this match
```

Only do deep search when metadata search returns few results, or the user explicitly asks.

## Example Queries and How to Handle Them

| User Query | Filters to Apply |
|------------|-----------------|
| "find my Kusto sessions" | keyword "Kusto" in `name` or `preview` |
| "flagged sessions from last week" | `isFlagged: true` + `createdAt` in last 7 days |
| "sessions about Copilot Lumina that are done" | keyword "Copilot Lumina" + `todoState: "done"` |
| "which sessions have sub-agents?" | task sessions where other sessions have matching `parentSessionId` |
| "most expensive sessions" | sort by `tokenUsage.costUsd` descending |
| "pinned sessions" | `isPinned: true` |
| "sessions from Teams" | `source: "teams"` |
| "what was I working on yesterday?" | `lastUsedAt` within yesterday's date range |

## Notes

- Always show results in the user's timezone (Asia/Shanghai).
- Hidden sessions (`hiddenFromList: true`) should be excluded by default unless explicitly requested.
- When the user asks for "sessions", search both COS sessions and task sessions. Mention the type in results.
- Sub-agents are typically not shown unless the user asks about them or asks about a specific task's children.
- Session names can be in English or Chinese — support both in keyword matching.
- Use case-insensitive matching for keywords.
- **Always use `encoding='utf-8'`** when reading any session file.
- **Never use `python3 -c`** — always write a `.py` file first.
- **Always use `task://session-id`** links for session references in output.
