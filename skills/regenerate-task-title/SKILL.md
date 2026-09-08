---
name: Regenerate Eureka Task Title
description: >-
  Rewrite low-quality Eureka task titles from full conversation context and
  update them directly through the local gateway bridge (no copy-paste). The
  user names the specific task(s) - by slug, "Copy Path" folder path, or
  "Copy Link" eureka:// link - and this skill refines those titles only. It
  never searches, lists, or picks tasks on the user's behalf.
alwaysAllow:
  - bash
  - read
  - grep
---

# Regenerate Eureka Task Title

Eureka's built-in auto-title only sees the first ~500 characters of the first
user message, and manual regeneration only sees the last 3 user messages
(truncated). Titles therefore latch onto one tiny fragment instead of the
task's actual scope. This skill fixes the titles of tasks the user explicitly
names: read the REAL conversation, synthesize a retrieval-friendly title, and
write it back through the local gateway bridge so the UI updates instantly
(no restart, no paste).

Scope rule: the user provides the task(s). Do NOT search, list, browse, or
suggest tasks, and never infer which task the user "probably" means from a
vague description. If the user cannot name a task precisely, ask them to copy
its path or link from the task's context menu ("Copy Path" / "Copy Link") and
stop there.

## Input: how the user names tasks

Accept any of these, one or many, mixed freely:

1. Task slug directly, e.g. `260903-pure-valley` (shape: 6 digits, dash,
   lowercase words; appears bare in the user's message).
2. Session folder path from the task context menu "Copy Path", e.g.
   `%USERPROFILE%\.eureka\workspaces\<wsId>\sessions\<taskId>` (the folder
   basename is the task id; if the path ends in `session.jsonl`, take the
   parent folder name).
3. Deep link from "Copy Link", e.g.
   `eureka://workspaces/<wsId>/sessions/<taskId>` - also accept it wrapped in
   a markdown or HTML anchor (`[title](eureka://...)` /
   `<a href="eureka://...">title</a>`); extract the last `sessions/<id>`
   segment.

Extraction is mechanical: match `eureka://workspaces/[^/\s"']+/sessions/([^/"'\s>)]+)`
for links, take the basename (or parent of `session.jsonl`) for paths, and
match `[0-9]{6}-[a-z0-9-]+` tokens for bare slugs. A link or path may point at
a sub-agent or a cos session by mistake; the verification step below filters
those out - never rename anything that is not a root task.

## Connection (local gateway bridge)

The desktop app runs an authenticated HTTP bridge on `http://127.0.0.1:8788`.
The device token lives in `%USERPROFILE%\.eureka\bridge-devices.json`
(`devices[*].token`). Never print, log, or echo the token; load it inside the
script and keep it in memory only.

```python
import json, os, urllib.request

with open(os.path.expanduser("~/.eureka/bridge-devices.json")) as f:
    token = json.load(f)["devices"][0]["token"]

def call(method, path, payload=None):
    # Content-Type must stay text/plain: the bridge treats application/json
    # as a CORS-preflight trigger and rejects preflights on loopback.
    req = urllib.request.Request(
        f"http://127.0.0.1:8788{path}",
        data=json.dumps(payload).encode() if payload is not None else None,
        method=method,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "text/plain"},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())
```

Responses are envelopes: `{"ok": bool, "version": str, "data": ...}` - work
with `data`. If port 8788 refuses connection, the app may run as a numbered
instance: probe `8789`..`8795` with an authenticated `GET /api/tasks` and use
the first port that answers 200.

Endpoints:

- `GET /api/tasks` -> `data.tasks[]`: `id`, `title`, `preview`, `status`,
  `messageCount`, `updatedAt` (epoch ms), `workspaceId`, `isPinned`,
  `isFlagged`. Already filtered to real tasks (no sub-agents, no schedule
  jobs, no cos sessions). Use it ONLY to verify the user-named ids and to
  read current titles - never to choose tasks. `workspaceId` + `id` also
  build the task's deep link (see step 5).

Task deep link: `eureka://workspaces/{workspaceId}/sessions/{taskId}` - the
same URL the task context menu's "Copy Link" produces. Render every task you
mention in chat as a markdown link `[title](eureka://...)` so the user can
jump straight to it from the conversation.
- `GET /api/tasks/{id}/messages?limit=20` -> `data.session.messages[]` plus
  `data.pageInfo`. Wire quirk: the role is in the `type` field
  (`user`/`assistant`/`tool`), not `role`. Older pages: pass
  `before={pageInfo.startCursor}`.
- `PATCH /api/tasks/{id}` with body `{"title": "New title"}` -> renames via
  the same in-process path the desktop UI uses (memory + disk + live UI
  event). Safe on running tasks; auto-title never fires again after the first
  user message, so the rename sticks.

## Workflow

1. Collect identifiers. Extract every task id from the user's message using
   the input rules above. If none resolve, ask for a path or link per task;
   do not guess and do not search.
2. Verify. One `GET /api/tasks` call. Every provided id must appear in
   `tasks[]`; report any that do not ("not a root task - sub-agent or cos
   session?") and continue with the valid ones. The same response supplies
   each task's current `title` (for the proposal table) and all sibling
   titles (for uniqueness checks).
3. Context. Per task, build a digest:
   - the FIRST user message, untruncated (this states the original goal);
   - the last 6-10 user messages (this shows how the task evolved);
   - the most recent final assistant message, trimmed to ~1000 chars;
   - `preview`, `status`, and `messageCount` from the list entry.
   Use `limit=1` reads plus `before`-pagination to walk back to older user
   messages without pulling tool spam. Skip assistant thinking blocks.
4. Generate one title per task with the rules below.
5. Propose. Present a table: task (deep link), current title, proposed
   title. For more than one task this confirmation is mandatory. For a single
   task, still show the proposal; apply immediately only if the user
   pre-authorized it.
6. Apply. `PATCH` each confirmed task sequentially (a ~150 ms pause between
   calls is plenty). Report per-task success/failure with the final title and
   the task's deep link, so the user can jump to it and eyeball the result.
7. If the user wants a record of a multi-task run, write a small markdown
   summary into a timestamped folder `regenerate-task-title_YYYYMMDD_HHMMSS/` in the
   working directory, with each task's deep link included. Do not create
   files for single renames.

## Title quality rules

The goal is RETRIEVAL: the user scans a sidebar weeks later and must recognize
the task. Optimize for that, not for brevity at any cost.

1. Whole-task scope. The title states what the task IS about overall, never
   one fragment of the first message. If the conversation drifted, title the
   dominant theme across the entire conversation; mention the current phase
   only when it disambiguates (e.g. "... - review fixes").
2. Name the concrete object. Include the repo, product, feature, document, or
   person when known ("Eureka title generation", not "Analyze code").
3. Language. Match the dominant language of the USER's own messages (ignore
   assistant language). Chinese conversation -> Chinese title, etc.
4. Shape. 4-10 words; at most ~48 Latin characters or ~22 CJK characters;
   verb-first when natural in that language. Plain text: no quotes, no
   markdown, no trailing period, no "Task:" prefix.
5. Unique. Check proposals against all other current titles in the workspace;
   if two tasks would collide, add the distinguishing qualifier (module,
   branch, date, person).
6. Honest. Only use facts present in the conversation. If a task is genuinely
   trivial, a short plain title is correct - do not inflate it.
7. Bad -> good calibration: a one-word or copy-of-first-five-words title is
   almost always wrong; a title that could describe ten different tasks is
   wrong; a title that uniquely identifies this work and fits on one sidebar
   line is right.

## Fallback (bridge unreachable)

If the app is not running (or the bridge cannot be reached), titles can be
edited on disk directly: each task's title is the `"name"` field in the FIRST
line of `<session folder>\session.jsonl` - the folder the user's "Copy Path"
already points at. Rewrite only that JSON field on line 1, preserving
everything else. This is safe ONLY while the app is closed (the running app
keeps all titles in memory and will overwrite the file), and the change
appears after the next app start. Prefer the bridge; use the fallback only on
request or when the app is down.

## Safety

- Never rename without showing old -> new for each task.
- Never touch or even propose tasks the user did not name, no matter how bad
  their titles look.
- Never print the bridge token; never send it anywhere except the loopback
  bridge.
- Renames are ordinary metadata writes (the same as the user renaming in the
  UI) - no backup ceremony needed, but report every change made.
