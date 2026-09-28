# `fsd`: what is still open

The state machine, execute's task parking and the stage-transition hooks landed in 20aa92c..91ef72a (execute run `260919-011818-fsd-u1-u3-u4`, completed after twelve tasks and seven final audits). What follows is what that run left for the skill prose and the live runs, and the risks it accepted instead of closing.

## Accepted residual risk

Each of these fails open (a missing link, so no hook fires) or needs someone to act against the flow deliberately:

- post-bash does not recognise backslash-continued commands, `$(...)` nesting, here-strings, `env`/`time` prefixes, or a start whose stdout is redirected.
- Whether `PostToolUse` fires for a Bash call that exits nonzero is unmeasured.
- The fsd state file has no lock; a concurrent write can drop a link.
- `guard` checks nothing on a completed execute receipt; close's AGENTS.md hash is the backstop.
- A hand-authored checkpoint can still open a span on paused→active with a made-up hash.
- Occupant lookup reads `<worktree>/.agents/kein/runs` and ignores `KEIN_STATE_ROOT` or a subdirectory `CLAUDE_PROJECT_DIR`.
- fsd states written before `resolved_reference` existed are no longer writable; runs are temporary.
- Interview's `output_path` and its completed `requirements_path` are assumed equal.
- execute: a `parked → parked` checkpoint can rewrite the park record; the reference's wording about the seal on `parked → pending` is looser than the code; a root-scoped task's `scope_fingerprint` starts covering untracked files for runs in flight; parking a reopened `accepted → correcting` task means undoing its accepted content.
- `continue` commits its successor before it commits the slice it is closing; a process killed between those two commits leaves both active -- the slice never marked `completed`, and its already-minted successor orphaned alongside it, with no `continued` on either to say they were ever meant to link. Nothing here repairs that automatically: `checkpoint` refuses to write `continued` onto the unclosed slice by hand, so the only recovery is `continue`'s own row-12 refusal (`a nonterminal fsd run already exists`) naming the orphan's own path on the next `continue` attempt, followed by aborting it and continuing again (closeout.md's own continue branch).

## Deferred measurement

Not an accepted risk, but a thing no run has yet exercised, so nothing here has been checked against a real one:

- No live chained run (`ocs state fsd continue`) has gone end to end yet. Its first real use should measure: whether the lead actually continues rather than closes when acceptance criteria remain; whether ralplan's own planner uses the remaining criteria and earlier slices' receipts that `gap`'s chained action hands it; whether a later slice's plan lands at a path of its own rather than overwriting an earlier one; whether ralplan's review lanes approve a slice plan that deliberately covers only part of the acceptance criteria, since the first slice's own action carries no remaining-criteria suffix to say so; whether the lead passes `gap`'s multi-line action as the whole `/kein:ralplan` argument rather than only its first line, and which path it then gives `ocs state ralplan start --input`; and whether the requirements' acceptance criteria stayed unedited across slices, since `AC<n>` ids are positional.

## The hooks do not see a run started in a worktree

In the 260926 slice-chain run the lead moved the flow into a linked git worktree with Claude Code's EnterWorktree, then started the fsd run there. `post-skill` did not enter `ralplan` and `post-bash` did not link the ralplan or execute runs, so the lead entered and attached every stage by hand, and the Stop hook never blocked. The same run also found that a worktree-isolated session refuses Bash commands it cannot prove stay in the worktree (pipelines, `$VAR` expansion, heredocs), so every step had to be a plain command.

It happened again on 2026-09-28 in a descvi run (`260928-210336-e3-v4-remaining`, EnterWorktree then `/kein:fsd`), and there it cost more: that lead did not attach ralplan while it was live, so once ralplan completed `attach` refused it as no longer live, `stages.ralplan.resolved_reference` stayed null, and `attach … execute` then refused too, because `_expected_execute_plan_reference` has no completed ralplan link to read the plan from. A missed link at one stage takes the next stage's link down with it.

Measured on 2026-09-28 with a headless session in a scratch repository whose `PostToolUse` and `Stop` hooks logged their environment: after EnterWorktree, the hook process's `CLAUDE_PROJECT_DIR` still names the checkout the session was launched in, while the payload's `cwd` and the hook's own working directory name the worktree. The lead's Bash has no `CLAUDE_PROJECT_DIR` at all, before or after, so `ocs state-dir` in Bash falls through to the git top level of its `cwd` and writes the run under the worktree. `hook.py`'s `_state_dir_root` and `_reference_dir` take `CLAUDE_PROJECT_DIR` first, so the hook searches the launch checkout's `runs/fsd`, finds nothing nonterminal there, and allows silently. The hook's docstring says it mirrors `ocs state-dir`, and it does line for line, but the two run with different environments, so they resolve different roots.

Not yet decided: whether the hook should take the payload `cwd`'s git top level before `CLAUDE_PROJECT_DIR` (which matches where Bash's `ocs` writes), or search both; whether `ocs-state-dir`, `prompt-layers.py`, `agent-layers.sh` and `ocs-doctor`, which also read `CLAUDE_PROJECT_DIR`, have the same split; and whether `attach` should accept a completed ralplan run whose plan matches, so one missed link does not strand execute. Landing the resolution fix also turns the Stop guard on, mid-run, for any fsd run already live in a worktree, whose unlinked stages would then read as a gap on every turn end.

**Reopen when** that fix is taken up; the probe is a scratch repository, a linked worktree, and a `--settings` file whose hooks append `$CLAUDE_PROJECT_DIR`, the payload `cwd` and `pwd` to a log.

## What would reopen the design

The run went through three association designs before this one held: inference after the fact, then a strict-only rule that lost the flow's own runs, then linking at creation. If a live run (U6) shows the flow's own stage run going unlinked on the ordinary path, the first thing to check is whether the lead followed the U5 list above, and the second is post-bash's spelling coverage, before touching the belonging rule.
