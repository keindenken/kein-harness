# `plan`: what is still open

Measurements are in this directory; the surveys they were read against are in `docs/research/`. Cases are in `dev/eval/cases/`.

## The two graders that have never separated anything

**`records-the-open-question` is 5/5 against 4/5 the wrong way round.** The control arm records the non-blocking question in every replicate and never writes the heading. `vocabulary-open-questions` separates the arms 5/5 against 0/5 on the heading alone. So the skill teaches the section and not the behaviour, and the behaviour was already there. Either the grader is asking for something everyone does, or `## Open Questions` is worth keeping only as a place to put what a planner would have written anyway. Not yet decided.

**`no-pre-written-implementation` is 0/5 on both sides.** Nobody follows it, including the arm that carries the rule. Counting Python blocks that contain a loop, a `try`, or a transaction gives twelve to one against the skill, so the rule does move behaviour — the grader cannot see that because it also catches the backfill routine written as prose, which both arms do.

The reason not to delete the rule: its point is code that cannot be known until it is implemented, which goes stale between planning and building. Neither fixture has a place where that is true. `plan-evidence-gate` invites the violation with a batched resumable backfill, and there is one conventional way to write that, so pre-writing it costs a reader nothing. **Measuring this needs a fixture where the plan genuinely cannot know the code.** That fixture does not exist yet and is the blocking item.

## The four that pass in both arms

`plan-file-written`, `sequences-the-irreversible-step`, `stops-at-the-artifact`, and — in the first evidence-gate run — `records-the-open-question`. Deletion evidence has accumulated across runs. Before deleting any of them, check whether the fixture invites the failure at all: `sequences-the-irreversible-step` may be inert because the requirements document names the corruption hazard outright, which makes it hard to miss rather than easy to get right.

## `plan-no-unknown` has not been measured on the current instrument

Everything on that case predates the tightened gate criterion, the `path: PLAN.md` declaration, the judge move off the fast tier, and the correction to the graders that had been telling judges to look in a working directory. Its five graders returned `inert` sixty times out of sixty across three runs, and the one signal ever found there came from isolating a single sentence rather than from the rule set. It should be re-run before anything is concluded from those nulls.

## What the ranking keeps catching that the graders do not

Twice now the ranking has separated the arms on an axis the per-assertion graders reported almost nothing on, and both times the grader was what needed fixing rather than the reading. Worth watching whether that keeps happening: it would mean pass/fail thresholds are systematically the weaker instrument, not that these two graders happened to be wrong.
