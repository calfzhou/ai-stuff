---
name: worktree
description: Create a git worktree and launch a new Eureka task session rooted in it, so the UI (branch indicator, clickable file paths) reflects the worktree correctly. Use when the user wants to work in a git worktree.
alwaysAllow:
  - Bash
  - mcp__eureka-self__create_task
  - mcp__eureka-self__get_task
  - mcp__eureka-self__send_message
---

**STOP. Read this entire skill before doing ANYTHING.**

You are a worktree setup tool. You MUST complete ALL 5 steps below in order, then stop. Do not skip any step. Do not stop after step 2.

**If you start analyzing code, reading source files, exploring the repo, or working on the user's task: you have failed. Stop and restart from step 1.**

# Steps

## 1. Resolve repo and refs

The user may specify a repo path in their prompt (takes priority). Otherwise, check if the current working directory is a git repo:

```bash
git -C "<path>" rev-parse --show-toplevel
git -C "<path>" symbolic-ref refs/remotes/origin/HEAD 2>/dev/null
```

If neither works, ask the user which repo to use. Fall back to `main` if default branch detection fails.

The user may specify a branch name — use it as-is. Otherwise generate a short kebab-case name from the task description (3-5 words). Do NOT hardcode any branch naming prefix.

## 2. Create the worktree

The worktree MUST be created INSIDE the repo, under `<repo>/.worktrees/`. Never create it as a sibling of the repo or anywhere else.

The folder name uses only the **last segment** of the branch name (after the final `/`). Example: branch `users/zhouji/2606-fix-login` → folder `<repo>/.worktrees/2606-fix-login`.

```bash
BRANCH="<full branch name>"
LEAF="${BRANCH##*/}"

git -C "<repo>" fetch origin 2>/dev/null
mkdir -p "<repo>/.worktrees"
grep -qxF '.worktrees' "<repo>/.git/info/exclude" 2>/dev/null || echo '.worktrees' >> "<repo>/.git/info/exclude"
git -C "<repo>" worktree add -b "$BRANCH" "<repo>/.worktrees/$LEAF" "origin/<base_ref>"
```

**WRONG examples (never do these):**
- `C:\Users\zhouji\Workspace\o365\MyRepo-some-feature` (sibling of repo)
- `C:\Users\zhouji\Workspace\worktrees\some-feature` (random location)

**CORRECT example:**
- `C:\Users\zhouji\Workspace\o365\MyRepo\.worktrees\some-feature` (inside repo)

## 3. Create the Eureka task — DO NOT SKIP THIS STEP

Get current task's engine and model via `mcp__eureka-self__get_task` (task ID is in the Eureka Task Context section of the system prompt). Then call `create_task`:

```
mcp__eureka-self__create_task({
  name: "<short descriptive name>",
  working_dir: "<repo>/.worktrees/<leaf>",
  workspace_id: "<current_workspace_id>",
  agent_engine: "<same engine>",
  model: "<same model>"
})
```

**IMPORTANT:** Only pass `name`, `working_dir`, `workspace_id`, `agent_engine`, and `model`. Do NOT pass a `worktree` parameter — that is a different feature. Just set `working_dir` to the worktree path.

This step is mandatory. The whole point of this skill is to create a task rooted in the worktree.

## 4. Forward the user's prompt (only if there are actual requirements)

Strip worktree-related phrases from the user's prompt: "use worktree", "in a worktree", "/worktree", "[skill:worktree]", "help create a git worktree", repo path specs, branch name specs, base ref specs. Look at what remains.

- If there are **remaining requirements** after stripping, forward them:

```
mcp__eureka-self__send_message({
  agent_id: "<new_task_id>",
  text: "You are already in a git worktree on branch '<branch>' (based on '<base_ref>'). Do NOT create another worktree. Work on the following requirements:\n\n<remaining requirements>"
})
```

- If **nothing remains** (the user only asked to create a worktree), skip this step.

`send_message` accepts the task ID directly — it routes to the Main agent.

## 5. Report back and STOP

Tell the user: task name, branch, base ref, worktree path, whether requirements were forwarded. Then STOP.

# Rules

- **You MUST complete steps 1 through 5.** Do not stop after creating the worktree — you must also create the task (step 3).
- **NEVER pass a `worktree` parameter to `create_task`** — just use `working_dir`.
- **Worktree path MUST be `<repo>/.worktrees/<leaf>`** — never outside the repo.
- **NEVER call `spawn_sub_agent` or `list_sub_agents`** — creates extra tabs.
- **NEVER call Glob, Grep, Read, or Agent tools** — you don't need them.
- **NEVER analyze code or work on the user's requirements** — forward them.
- If branch exists → ask user for a different name.
- If worktree path exists → ask user how to proceed.
- If fetch fails → warn but continue from local refs.
