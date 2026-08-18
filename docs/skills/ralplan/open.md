# `ralplan`: what is still open

Observed during the e3-v3 fixture round in `descvi/kein-e3v3`, with the harness pinned at `fb55678`. Nothing here has been acted on: the instrument is fixed for the length of that run, so any change waits for it to finish.

## The lead checkpoints a state the workflow does not name

A blocked round produces three `Status reason` writes and two checkpoints:

| | `Status` | phase in the reason | checkpoint | prescribed by |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `Draft` | `revising` | — | step 6 |
| 2 | `Draft` | `drafted` | `DRAFT_CHECKPOINT_OK` | nothing |
| 3 | `In Review` | `reviewing` | `CHECKPOINT_OK` | step 4 |

Row 2 is in no step. Step 3's "compute both hashes and checkpoint only once it has" governs a first draft returned by the `plan` skill, and the same step says revisions are this workflow's own and do not run `plan` again. `state-schema.md` ties phase `drafted` to the first durable checkpoint at round 0, which this is not.

It is not obviously waste, which is why it is recorded rather than deleted. Between "Planner returned a revision" and "lanes dispatched" there is a real state, and with no checkpoint in it a crashed run resumes through `reconcile` reading phase `revising` against an already-revised artifact — and sends the revision back to Planner. The lead invented a state because the workflow is missing one.

Decide which way: name the post-revision state in step 6 and let it checkpoint, or state that a revision checkpoints only on dispatch and accept the re-revision on resume.

## `Status reason` is being written as a round summary

`plan-gate.md` asks it for two things: the current workflow phase, and why approval is absent. Row 3 above instead re-narrated the round — which findings were consolidated, which lane had returned `PASS` before the revision, what the content change invalidated, and the full 64-character review hash.

That content already has a home. Step 6 persists consolidated findings into state, and `state-schema.md` gives each one `claim`, `evidence`, `impact`, and `required_correction`. Writing it into the artifact as well costs an `Edit` against a large plan file three times a round, and leaves a later reader two copies that can disagree.

Nothing is invalidated by it — both lines are excluded from the review hash by design. The cost is tokens and duplication, not correctness.

## The `Draft` / `In Review` flip itself is correct

Recorded because it looks like the wasteful part and is not. `plan-gate.md` permits `In Review` "only while the complete current review content sits at a fresh official gate", so a plan being revised cannot stay in it. Two status transitions per blocked round is what those definitions require, and collapsing them would mean a plan is `In Review` while no lane is reading it.
