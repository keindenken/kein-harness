# The Gate Over a Plan

What RALPLAN adds to the artifact the `plan` skill produces. The artifact itself is specified by [that skill's contract](../../plan/references/plan-template.md), which the `plan` invocation already carries; only the overlay is here.

## Statuses

`In Review` and `Approved` join `Draft`, and only this workflow may set them.

- `Draft` before review, after a must-fix verdict, and for a terminal unapproved plan.
- `In Review` only while the complete current review content sits at a fresh official gate.
- `Approved` only after every fresh lane passes the current review-content SHA-256.

`Status reason` additionally carries the current workflow phase and why approval is absent.

## Two hashes

State records the exact artifact SHA-256 and a review-content SHA-256 that excludes only the `Status` and `Status reason` lines.

A status-only transition changes the artifact hash and leaves the review hash stable, so it does not invalidate a review. Every other content change changes the review hash and invalidates every verdict. Hashes are the authority on drift; a transcript is not.

## Evidence Gates under approval

An Evidence Gate may remain in an `Approved` plan only when every expected result stays within the approved outcome, scope, architecture, and acceptance semantics.

If a result would require a new material decision, gather the evidence before approval or leave the plan `Draft` with the gap explicit. An approved plan whose gate can land outside the approved space has moved the decision to execution time, which is the thing approval was supposed to settle.
