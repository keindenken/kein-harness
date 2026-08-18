# `ralplan`: what is still open

Observed during the e3-v3 fixture round in `descvi/kein-e3v3`, with the harness pinned at `fb55678`. Nothing here has been acted on: the instrument is fixed for the length of that run, so any change waits for it to finish.

## A fresh lane is not blind, and the artifact contract is why

`review-contract.md` requires each lane package to contain "the complete current canonical plan", and one paragraph later requires that "a fresh reviewer receives no previous finding, verdict, reviewer identity, revision note, change summary, claimed fix, closure result, or expected outcome."

`plan-gate.md` requires the artifact to carry a `Status reason` saying why approval is absent. Round 5 of the fixture run opened with this one:

> Round-4 findings were addressed by Planner revision and every round-4 verdict (including the architect PASS) invalidated by the content change.

That is a previous verdict, a revision note, a change summary, and a claimed fix — four of the eight forbidden items — delivered to a fresh Architect and Critic inside the artifact the contract mandates including. Nothing in either file excludes the status lines from the package.

The code already knows those lines are not review content: `review_text()` strips both by line prefix before hashing, which is what makes a status-only edit leave the review hash stable. The strip exists for the hash and was never extended to the package.

This is not a cost question. Blind lanes are the whole mechanism the consensus gate rests on, and after the first round they have not been blind.

## The post-revision checkpoint is required by the state machine

An earlier version of this file recorded that checkpoint as a state the lead invented because no workflow step names it. That was wrong, and the correction is the interesting part.

`validate_transition` refuses to open `In Review` while the previous state carries unresolved findings, and step 6 requires those findings to be persisted. So `Draft(revising, findings) -> In Review` is rejected outright, and the run has to pass through a `Draft` checkpoint that clears them. Clearing them is itself gated: a same-hash `Draft` that drops its findings is rejected too.

Together those two rules say **findings may only be dropped by actually changing the plan**, and the checkpoint in the middle of the round is where that is enforced. It is the mechanism that makes a `MUST_FIX` unskippable. The prose not mentioning it is a documentation gap; the call is doing real work.

## `Status` carries two facts and can only express one

`plan-gate.md` gives `Draft` three meanings: before review, after a must-fix verdict, and for a terminal unapproved plan. A reader who opens the artifact cannot tell an abandoned plan from one whose Planner is mid-revision, and the field flips twice within about half an hour of wall clock on a live round.

The alternative reading is that `Status` should answer only "is a gate running over this artifact" — `Draft` when no run is open, `In Review` for the length of a run including its revisions, `Approved` when it passed. `phase` already exists and already carries `revising` / `drafted` / `reviewing`, so the sub-state has a home that is not the artifact header.

The mechanism does not object. What the state machine actually protects is the findings-and-hash invariant above, which it happens to express on `plan.status`; expressing it on `phase` would preserve it exactly while freeing `Status` to mean one thing. That is the change to weigh, not the flip itself.

## The two-field header is not the only shape

The incumbent artifacts in `descvi` use a single free-form line — `Status: APPROVED — two-vendor unanimous consensus, 2026-08-17` — rather than a fixed token plus a separate `Status reason`, and that is the preferred style here.

`validate_plan_text` currently rejects it twice over: it requires exactly one `Status:` whose stripped value is exactly `Draft`, `In Review`, or `Approved`, and separately requires a non-empty `Status reason`. Accepting `Status: <state> — <free text>` and dropping the second field is a small parser change, and `review_text()` already strips by line prefix, so one merged line stays out of the review hash without any further work.

Note that merging the fields does not fix the blindness leak above. That one is fixed by stripping the status lines from the lane package, and the two changes are independent.
