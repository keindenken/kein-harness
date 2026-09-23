# `fsd`: what is still open

The state machine, execute's task parking and the stage-transition hooks landed in 20aa92c..91ef72a (execute run `260919-011818-fsd-u1-u3-u4`, completed after twelve tasks and seven final audits). What follows is what that run left for the skill prose and the live runs, and the risks it accepted instead of closing.

## What the `fsd` SKILL.md had to say (story U5)

Done in 2d94cb8: the skill text states each of these, and the 2026-09-23 run corrected three of its sentences against the code.

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

## What would reopen the design

The run went through three association designs before this one held: inference after the fact, then a strict-only rule that lost the flow's own runs, then linking at creation. If a live run (U6) shows the flow's own stage run going unlinked on the ordinary path, the first thing to check is whether the lead followed the U5 list above, and the second is post-bash's spelling coverage, before touching the belonging rule.

## Left open by the 2026-09-23 run

Carried in that run's receipt; the run record is `docs/skills/execute/260923-audit-stopping-rule.md`.

- **A waiting lead is not told it may wait.** The mid-stage Stop block tells a lead waiting on another lane to check the lane is alive, but not that it may then end the turn for the lane's notification. Nothing stalls — `stop_hook_active` lets the second stop through — but a literal reader may poll in-turn or read a healthy wait as a reason to exit. The fix moves the block's golden text in `check-fsd-hooks`.
- **A halted run's report invites an answer nothing can accept.** When a structural refusal ends a pause attempt in `halt`, `report` still lists the recorded question with "Answer by re-invoking /kein:fsd", and `answer` then refuses a terminal state.
- **Whether `claude --resume` re-arms frontmatter hooks is unmeasured.** The 2026-09-19 probe measured only a `-c -p` continuation, where they did not fire.
- **`closeout.md` step 4 states `halt`'s refusal as one case.** `halt` is also refused on a run that is not active and on an empty reason; neither is reachable from the step as written, so this is wording.

