# `fsd`: what is still open

The state machine, execute's task parking and the stage-transition hooks landed in 20aa92c..91ef72a (execute run `260919-011818-fsd-u1-u3-u4`, completed after twelve tasks and seven final audits). What follows is what that run left for the skill prose and the live runs, and the risks it accepted instead of closing.

## What the `fsd` SKILL.md must say (story U5)

The mechanism only works if the lead does these, and nothing enforces them:

- Declare the frontmatter hooks, including `PostToolUse` matcher `Bash` → `hook.py post-bash`; the block is in `docs/skills/fsd/260919-hook-probe.md`. Then `claude plugin validate plugin --strict` with it in place, which has not been run on the real plugin.
- Pass `--input <requirements>` to `ocs state ralplan start`; without it the ralplan run cannot link, so execute never can either.
- Validate the interview ledger with `ocs validate interview ledger <path>` while it is still active; a completed ledger never links.
- Run `ocs state execute dispatch` before starting an executor, so the park seal is the pre-dispatch content.
- Run each watched command (`ralplan start`, `execute start`, `validate interview ledger`) as its own Bash call, with an absolute or repository-relative `--input` for execute.
- Never abort another operator's execute run: gap's occupant row prints an abort command, but aborting someone else's work is irreversible and belongs in the decision policy as a parked question.
- After an aborted execute, decide closeout or restart deliberately; gap gives no nudge there, by design.

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
