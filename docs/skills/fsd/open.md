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

## What would reopen the design

The run went through three association designs before this one held: inference after the fact, then a strict-only rule that lost the flow's own runs, then linking at creation. If a live run (U6) shows the flow's own stage run going unlinked on the ordinary path, the first thing to check is whether the lead followed the U5 list above, and the second is post-bash's spelling coverage, before touching the belonging rule.
