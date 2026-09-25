---
name: ralplan
description: Use when an implementation plan needs evidence-grounded architecture and quality consensus before it is trusted for execution.
argument-hint: "[what to plan] [--reviewer claude|codex] [--planner codex] [--primed] [--max-rounds <n>]"
---

# RALPLAN

## Overview

RALPLAN is the `/plan` skill under a consensus gate. Planner owns plan prose; the lead owns workflow state; a fresh Architect and fresh Critic independently decide whether the complete current plan is safe and specific enough to approve.

Use it when that gate could actually return `BLOCK` — the architecture is contested, an independent reader would plausibly disagree, or a wrong plan is expensive to discover later. A gate that cannot fail is ceremony, and its rounds are the expensive part; `/plan` alone produces the same artifact without them.

This skill ends with an approved plan or an explicit unapproved state. It grants no execution authority, and the only skill it runs is `/plan`.

## At entry

Read from this working directory when the skill loaded; `ocs state-dir` answers relative to it.

- `command -v ocs` → !`command -v ocs || echo "NOTHING ON PATH — no transition command will run"`
- `ocs state-dir plans` → !`ocs state-dir plans 2>&1`
- `ocs state-dir runs/ralplan` → !`ocs state-dir runs/ralplan 2>&1`

!`ocs state ralplan --help 2>&1`

## Required Files

Read each before the point its line names:

- [state-schema.md](references/state-schema.md) before creating or resuming a run.
- [plan-gate.md](references/plan-gate.md) before setting a status or computing a hash. The artifact's own contract arrives with the `/plan` invocation; this covers only what the gate adds to it.
- [review-contract.md](references/review-contract.md) before assembling each official review package.
- [lanes.md](references/lanes.md) only when the invocation names a vendor for a lane — `--reviewer codex`, `--reviewer claude,codex`, `--planner codex`.

## Workflow

Each transition builds its own state; do not hand-author one unless no command names the shape you need.

Entry and resume:

1. Resolve the task, repository, and canonical plan path before dispatch. Default the plan to `<ocs state-dir plans>/<slug>.md`; follow the project's own convention instead when it already has one for plan artifacts.
2. On resume, run `reconcile`. Treat its `required_action` as the exact next action; never infer continuity from conversation alone.
3. For a new artifact, **run the `/plan` skill**, passing `--planner` through when the invocation carries it. It owns first-draft production, from the canonical path through Planner's dispatch boundaries, and returns a valid `Draft`. Compute both hashes and checkpoint only once it has. Revisions are this workflow's own and happen when a round blocks, not by running `/plan` again.

Each round, until the plan is approved or the run ends unapproved:

4. Validate the artifact. The lead may edit only the workflow-owned `Status` line. Set it to the bare `Status: In Review`, open the round, and assemble one separate package per lane from the review contract.
5. Dispatch a fresh Architect and fresh Critic under their native read-only boundaries. They are blind to each other, previous rounds, claimed fixes, and expected outcomes. Each receives the plan's path and the same review-content plan hash. A lane's `BLOCK` blocks approval until the ground it named is answered.
6. If a blocking ground is standing, `block` with the round's consolidated findings and ask Planner to revise the same artifact. Checkpoint when the round resolves, not when a lane returns. Any review-content change invalidates every prior verdict. Advance the round only when a new official lane set is dispatched. Under `--max-rounds`, a ground still standing at the last allowed round ends the run instead: set `Status: Draft`, then `block`, which records the run blocked; report the standing findings and stop unapproved.
7. Otherwise approve, and a round that returned findings can still be that round. A `REVISE` finding reaches approval without a round: carry it as it stands, or, after `approve`, have Planner correct it in the text, leaving the `Status` line alone, read the diff yourself, and then record it with `fix`. A recorded fix cannot be taken back, so a diff you would not approve goes back to Planner before `fix`, not after. A `BLOCK` reaches approval only with a deferral recorded against the ground it named, and its `Caught by` belongs in the plan's pre-mortem before the approval, not after. Set `Status: Approved — <who agreed, and when>` in one line; what the approval stands over and its deferrals live in state and the receipt, and bounded Evidence Gates in the plan body, not in that line. Checkpoint the Approved state, then compact it to the completed receipt.

Fresh official reviewers are mandatory after every review-content revision, except that a run started with `--primed` may send a `BLOCK` correction back to the reviewer that raised it, primed with the `round-<n>-plan.md` and `round-<n>-findings.json` that `block` left beside the run, and count its verdict. A blocking lane that raised nothing that round still gets a fresh lane.

## Dispatch

Dispatch `kein:planner`, `kein:architect`, and `kein:critic` with the Agent tool, one new agent per call, supplying the complete package the review contract defines for it. Never continue an existing agent for an official round: a fresh agent is what keeps a reviewer blind to earlier history. `--primed` is the one exception, and only for the reviewer whose `BLOCK` the correction answers. Planner's first dispatch is not one of these — the `/plan` skill owns the first draft and dispatches Planner itself.

An invocation may name another vendor for a review lane, or `--planner codex` for Planner, whose revisions then resume the codex worker that wrote the draft rather than dispatching `kein:planner`. Without such a flag every lane is native, and the rest of this section is the whole story.

Put the blind lanes in one message: they then run concurrently, and neither can have seen the other's response, so the contract's blindness between them holds by construction rather than by the lead's care.

## Evidence and Decisions

Resolve a load-bearing empirical fact before approval when its result could change scope, architecture, acceptance semantics, or safety. When every expected result already maps to an approved in-scope branch, keep it as a bounded Evidence Gate; an unexpected result is a stop boundary for replanning.

Ask the user immediately only when an answer is necessary for the next approval or materially changes a review. Record useful non-blocking questions in the plan and continue.

Without `--max-rounds`, around five unsuccessful official rounds is a diagnostic trigger, not a maximum, and it re-arms rather than being spent: a decision to continue covers the next five rounds, not the rest of the run. Reassess whether the problem needs user authority, missing evidence, a bounded conditional plan, or an explicit Draft handoff. Do not manufacture approval from repetition.

When the same defect class recurs against the same contract, revisit the contract or underlying design instead of polishing the same prose again. Evidence gathering does not authorize production implementation or scope expansion.
