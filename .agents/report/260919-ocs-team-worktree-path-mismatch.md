# `ocs team --worktree <path>` cannot attach a worker when the coordinator pane lives in a different worktree

Date: 2026-09-19. Reporter: a Claude Code lead session in the descvi repository. Reproduced twice in a row, then diagnosed by hand.

## Versions

- kein plugin: `/Users/kein/Documents/workspace/dev/kein-harness/main/plugin` at `5b5961e` (the last commit to touch `libexec/ocs-team` is `2da9b80`; `libexec/ocs-team` has no uncommitted changes).
- orca CLI `1.4.205`, codex-cli `0.154.0`, macOS (Darwin 25.6.0).

## Setup

- The coordinator is a Claude Code session whose Orca pane is in the main worktree `/Users/kein/Documents/workspace/dev/descvi/repo`.
- The target is a linked worktree of the same repository, `/Users/kein/Documents/workspace/dev/worktree/repo/ki54-boundary`, on branch `fix/ki-54-residual-and-overlay-boundary`. Orca knows it: `orca terminal create --worktree path:<it>` succeeded.
- Goal: run two execute runs in parallel, one per worktree, each with a codex Executor (`/execute --executor codex`).

## Command

```sh
cd /Users/kein/Documents/workspace/dev/worktree/repo/ki54-boundary
ocs team codex --agent executor \
  --worktree /Users/kein/Documents/workspace/dev/worktree/repo/ki54-boundary \
  --task-file <package.md>
```

`ocs team ... --check` on the same arguments passed every precondition and printed the launch, so the check does not cover this failure.

## Observed

Both attempts printed the same thing and exited 0:

```
ocs team: the worker started but could not be attached to a dispatch.
  terminal=term_… left open for inspection.
```

- The worker terminal was up. codex had reached its idle TUI prompt ("Ask Codex to do anything", 0 in / 0 out), so the `tui-idle` wait passed.
- No task was ever delivered to the worker.
- The Orca task stayed in `ready` with no dispatch.
- The run dir (`.agents/kein/runs/team/<stamp>-executor/`) held only `command.txt`, `role.md` and `spec.txt`. It had no `run=/task=/dispatch=` line.

## Root cause (measured)

Re-running the one step that `ocs-team` silences (`worker-start ... --json 2>/dev/null`) by hand, from the target worktree, against the stranded task and terminal:

```sh
orca orchestration worker-start --task task_ac4d06b08f74 --terminal term_162085e2-… --json
```

```
"code": "terminal_worktree_mismatch",
"message": "Terminal term_162085e2-… does not belong to worktree efd9325a-…::/Users/kein/Documents/workspace/dev/descvi/repo. …"
```

- The Run and Task that `ocs team` creates carry the coordinator pane's identity. In `task-list`, `created_by_process_incarnation` names `…/Users/kein/Documents/workspace/dev/descvi/repo…`, which is the pane's worktree. Neither `$PWD` nor `--worktree` changes it.
- The worker terminal, correctly, is created in the target worktree: `orca terminal create --worktree "path:$worktree"`.
- Orca then refuses to bind a terminal from one worktree to a Run/Task homed in another.
- `cd`-ing into the target worktree before running `ocs team` does not help, because the identity comes from the pane, not the process cwd.

Consequence: `ocs team --worktree <path>` works only when `<path>` is the coordinator pane's own worktree, which is the default and needs no flag. That defeats the documented purpose of the path form, a lead driving lanes in several existing worktrees.

It is unverified whether `--worktree new` hits the same refusal. It also creates the terminal in a worktree other than the pane's, so it likely does. Worth one probe.

## Why it was hard to see

1. The `worker-start` stderr goes to `/dev/null`, so the one line naming the cause (`terminal_worktree_mismatch`) never reaches the caller. The printed message ("the worker started but could not be attached") reads like a transient Orca hiccup and invites a blind retry. I retried once, and that stranded a second terminal and a second `ready` task.
2. The command exits 0 on this path. The `fail()` helper exits 1, but the lead's `| tail` pipeline reported 0, and the lanes reference says a nonzero exit is what marks a lane as not run. Check whether this branch actually returns nonzero.
3. `--check` does not test the pane-worktree vs target-worktree relation, so it green-lights a launch that cannot bind.
4. Cleanup is manual on every failure:
   - `orca terminal close --terminal <h>`
   - `orca orchestration task-update --id <task> --status failed`
   - The Run is left behind; I found no delete for it.

## Suggested fixes (for the harness owner to choose)

- **Surface the error.**
  - Capture `worker-start`'s JSON and print `error.code`/`error.message` on failure instead of discarding stderr.
  - Exit nonzero.
  - Close the terminal and fail the task automatically, unless `--keep` is given.
- **Make the path form actually work.**
  - Either create the Run/Task from a context homed in the target worktree (for example a coordinator terminal created there, then `orchestration run-use`), or pass whatever `--run`/`--worktree` selector `worker-start` accepts so the Run is homed where the worker is.
  - The `worker-start --help` lists `--worktree <selector>` and `--run <run_id>`. Whether either lifts the mismatch is untested.
- **Make `--check` fail early.** If the fix is not possible, compare the pane's worktree (`orca worktree current`, run from the pane's cwd) with the resolved `$worktree` and refuse with the reason before creating anything.
- **Fix the docs.**
  - In `skills/execute/references/lanes.md` and the `ocs team --help` text ("a path uses an existing one"), state the restriction until it is lifted.
  - A lead running parallel execute runs across worktrees currently has no codex Executor for any worktree but its own.

## Workaround used in the session

- The codex Executor runs only in the coordinator's own worktree (track B).
- The other worktree (track A) uses the native `kein:executor`.
- Review lanes stay on codex for both, because `ocs ask` does not go through Orca dispatch and is unaffected.

## Leftovers from this session

- Two terminals, closed: `term_5591815e-…` and `term_162085e2-…`.
- One Orca task marked failed (`task_ac4d06b08f74`). The first attempt's task was not found in the second listing.
- Two Orca Runs remain (one is `run_7fa9ec42f3ea`).
- Two stray run dirs under `ki54-boundary/.agents/kein/runs/team/`: `260919-103100-executor` and `260919-103203-executor`.

## Addendum (same day) — fixed upstream, and one side effect of the live edit

- `f0fe5c4` (2026-09-19 10:39, "a worker in a worktree other than the coordinator pane's now attaches…") landed while this session was running. The next cross-worktree lane in this session will exercise it.
- One more symptom was observed on a same-worktree lane (`run_fe7f8bd2d253`, dispatch `ctx_65055cb7692b`) that was already running when `libexec/ocs-team` was rewritten (mtime 10:38:06).
  - The script printed `ocs-team: line 447: re: command not found`.
  - It also printed "the report exists and the dispatch has not settled".
  - It exited 0 while the dispatch later showed `completed`.
- This is bash reading a script that changed under it, not a defect in either version. The worker itself did signal `worker_done` (`msg_fa623ba7ad5b`).
- Worth knowing because `~/.claude/skills/kein` resolves to this working copy (`kein-harness/main/plugin`). Editing `libexec/*` there changes the running lanes of every other session. A lead reading such output will take it for a harness bug. The same happened with `skills/execute/scripts/state.py` in an earlier session.
- Possible mitigation: have `ocs` exec a copy of the script, or wrap the body in a function called at EOF, so a mid-run edit cannot be read half-way.

## Addendum 2 — two concurrent `ocs team` lanes from one coordinator: the second cannot attach

- After `f0fe5c4`, cross-worktree lanes attach. But two lanes started a couple of seconds apart from the same coordinator pane, both targeting `worktree/repo/ki54-boundary` with disjoint scopes, did not both attach. One ran to completion; the other printed:
  ```
  ocs team: the worker started but could not be attached to a dispatch.
    orca: consumer_fenced worker-start requires the coordinator terminal currently bound to the Task Run. …
    task=task_42c5eaec7a97 marked failed.
    terminal=term_3aebc845-… closed.
  ```
- The new failure path is a clear improvement: it names Orca's reason, fails the task and closes the terminal.
- The cause reads as each `ocs team` creating its own Run and re-binding the coordinator terminal to it (`orchestration run-use`-like), so the second bind fences the first's `worker-start`, or vice versa. `ocs team --help` still says "Run several in the background for several lanes", and `lanes.md` says the command refuses a second worker only when it would carry the same package. Neither holds when the lanes come from one pane.
- Session workaround: one `ocs team` lane at a time per coordinator. A second lane in another worktree also serialises.
