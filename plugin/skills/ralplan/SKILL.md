---
name: ralplan
description: Use when an implementation plan needs evidence-grounded architecture and quality consensus before it is trusted for execution.
---

# RALPLAN

## Overview

RALPLAN is the `/plan` skill under a consensus gate. Planner owns plan prose; the lead owns workflow state; a fresh Architect and fresh Critic independently decide whether the complete current plan is safe and specific enough to approve.

Use it when that gate could actually return `MUST_FIX` — the architecture is contested, an independent reader would plausibly disagree, or a wrong plan is expensive to discover later. A gate that cannot fail is ceremony, and its rounds are the expensive part; `/plan` alone produces the same artifact without them.

This skill ends with an approved plan or an explicit unapproved state. It grants no execution authority, and the only skill it runs is `/plan`.

## Required Files

Read each before the point its line names:

- [state-schema.md](references/state-schema.md) before creating or resuming a run.
- [plan-gate.md](references/plan-gate.md) before setting a status or computing a hash. The artifact's own contract arrives with the `plan` invocation; this covers only what the gate adds to it.
- [review-contract.md](references/review-contract.md) before assembling each official review package.
- [lanes.md](references/lanes.md) only when the invocation names a vendor for a review lane — `--architect codex`, `--critic claude,codex`.

## Workflow

Use `ocs state ralplan --help` for the transition commands — `start`, `open`, `block`, `revised`, `approve`, `complete` — plus validation and reconciliation. Each transition builds its own state; do not hand-author one unless no command names the shape you need.

1. Resolve the task, repository, canonical plan path, and run directory before dispatch. Default the plan to `<ocs state-dir plans>/<slug>.md` and the run directory to `<ocs state-dir runs/ralplan>/<YYMMDD-HHMMSS>-<slug>/`; follow the project's own convention instead when it already has one for plan artifacts.
2. On resume, run `reconcile`. Treat its `required_action` as the exact next action; never infer continuity from conversation alone.
3. For a new artifact, **run the `/plan` skill.** It owns first-draft production, from the canonical path through Planner's dispatch boundaries, and returns a valid `Draft`. Compute both hashes and checkpoint only once it has. Revisions are this workflow's own and happen in step 6, not by running `plan` again.
4. Validate the artifact. The lead may edit only workflow-owned `Status` and `Status reason` metadata. Set `In Review`, refresh both recorded hashes, checkpoint, and assemble one separate package per lane from the review contract.
5. Dispatch a fresh Architect and fresh Critic under their native read-only boundaries. They are blind to each other, previous rounds, claimed fixes, and expected outcomes. Each receives the complete current plan and the same review-content plan hash. Any lane's `MUST_FIX` blocks approval.
6. If blocked, set Draft with a concrete reason, persist consolidated falsifiable findings, clear every verdict, and ask Planner to revise the same artifact. Checkpoint when the round resolves, not when a lane returns. Any review-content change invalidates every prior verdict. Advance the round only when a new official lane set is dispatched.
7. If every lane returns `PASS` for the same review hash, set Approved and explain the approval and any bounded Evidence Gates in `Status reason`. Confirm the review hash did not change, checkpoint the Approved state, then compact it to the completed receipt.

Fresh official reviewers are mandatory after every review-content revision. A previous reviewer may perform a targeted closure check when a subtle or high-risk correction needs confirmation; that check can block but cannot approve or replace a fresh lane.

## Dispatch

Dispatch `kein:planner`, `kein:architect`, and `kein:critic` with the Agent tool, one new agent per call, supplying the complete package the review contract defines for it. Never continue an existing agent for an official round: a fresh agent is what keeps a reviewer blind to earlier history. Planner's first dispatch is not one of these — the `plan` skill owns the first draft and dispatches Planner itself.

An invocation may name another vendor for a review lane. Without such a flag every lane is native, and the rest of this section is the whole story.

Put the blind lanes in one message: they then run concurrently, and neither can have seen the other's response, so the contract's blindness between them holds by construction rather than by the lead's care.

## Evidence and Decisions

Resolve a load-bearing empirical fact before approval when its result could change scope, architecture, acceptance semantics, or safety. When every expected result already maps to an approved in-scope branch, keep it as a bounded Evidence Gate; an unexpected result is a stop boundary for replanning.

Ask the user immediately only when an answer is necessary for the next approval or materially changes a review. Record useful non-blocking questions in the plan and continue.

Around five unsuccessful official rounds is a diagnostic trigger, not a maximum, and it re-arms rather than being spent: a decision to continue covers the next five rounds, not the rest of the run. Reassess whether the problem needs user authority, missing evidence, a bounded conditional plan, or an explicit Draft handoff. Do not manufacture approval from repetition.

When the same defect class recurs against the same contract, revisit the contract or underlying design instead of polishing the same prose again. Evidence gathering does not authorize production implementation or scope expansion.
