# The Gate Over a Plan

What RALPLAN adds to the artifact the `/plan` skill produces. The artifact itself is specified by [that skill's contract](../../plan/references/plan-template.md), which the `/plan` invocation already carries; only the overlay is here.

## Statuses

`In Review` and `Approved` join `Draft`, and only this workflow may set them.

- `Draft` while no gate is open over the artifact: before the first round, and for a terminal unapproved plan.
- `In Review` for the length of an open run, including while Planner is revising between rounds.
- `Approved` after every blocking lane has returned a verdict on the review-content SHA-256 it read with no blocking ground left standing. That hash is the current one unless a `fix` has since moved it (see Two hashes).

The field answers one question — is a gate running over this artifact — so a reader who opens the plan cold gets that answer without reconstructing the round history.

That question is not "did every lane find nothing". An approved plan may stand over findings: a `REVISE` item, which is real and does not make execution unsafe, and a `BLOCK` item whose ground the lead overruled and deferred. Both are recorded against the run and survive into the completed receipt, and a deferred one additionally owes the plan's pre-mortem the `Caught by` it named. A `REVISE` item corrected after approval leaves that list and is recorded as a fix instead. What `Approved` asserts is that nothing blocking is standing unanswered, which is a smaller claim than the status used to make and the only one the gate ever established.

Where a run is *inside* a round is `phase`, which lives in state rather than in artifact prose, and it is what the transition rules are enforced on.

A lane reads this file, so while a gate is open the line says nothing about the run. `In Review` is the bare word, and the validator refuses a reason on it; the round, the verdicts and the revisions are in state. `Approved` carries one line saying who agreed and when. `Draft` may carry a reason, which the `/plan` skill writes for a standalone plan.

## What the body may not narrate

The plan cites anything outside itself and must — a prior phase's ruling, a decision id, an owner's judgement are what bind the work. It does not narrate its own drafts: which round found what, what an earlier revision claimed, which sentence was corrected, what a reviewer will say about a clause. The corrected fact is the whole of what a reader can act on.

A fresh lane reads this artifact from its path, and [review-contract.md](review-contract.md) forbids the lane every previous finding, verdict, revision note and change summary — so a body that narrates its own corrections hands the lane all four back inside the text it is required to read. That is the mechanism, and it is what would license dropping this rule: it holds only while a lane reads the body.

## Two hashes

State records the exact artifact SHA-256 and a review-content SHA-256 that excludes only the `Status` line.

A status-only transition changes the artifact hash and leaves the review hash stable, so it does not invalidate a review. Every other content change changes the review hash and invalidates every verdict, with one exception: a `fix` after approval moves the review hash and keeps the verdicts, bound to the hash the lanes read, and records the move. Hashes are the authority on drift; a transcript is not.

## Evidence Gates under approval

An Evidence Gate may remain in an `Approved` plan only when every expected result stays within the approved outcome, scope, architecture, and acceptance semantics.

If a result would require a new material decision, gather the evidence before approval or leave the plan `Draft` with the gap explicit. An approved plan whose gate can land outside the approved space has moved the decision to execution time, which is the thing approval was supposed to settle.
