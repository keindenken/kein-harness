---
name: ralplan
description: Use when an implementation plan needs evidence-grounded architecture and quality consensus before it is trusted for execution.
---

# RALPLAN

## Overview

RALPLAN turns one canonical implementation plan into a reviewable decision artifact. Planner owns plan prose; the lead owns workflow state; a fresh Architect and fresh Critic independently decide whether the complete current plan is safe and specific enough to approve.

This skill ends with an approved plan or an explicit unapproved state. It grants no execution authority and does not route to another skill.

## Required Files

Read these when their stage begins:

- [references/state-schema.md](references/state-schema.md) before creating or resuming a run.
- [references/plan-template.md](references/plan-template.md) before assigning the canonical artifact to Planner.
- [references/review-contract.md](references/review-contract.md) before assembling either official review package.

Use `ocs state ralplan --help` for validation, reconciliation, and atomic checkpoint commands.

Dispatch `kein:planner`, `kein:architect`, and `kein:critic` with the Agent tool, one new agent per call, supplying the complete stage-specific package. Never continue an existing agent for an official round: a fresh agent is what keeps a reviewer blind to earlier history.

## Workflow

1. Resolve the task, repository, canonical plan path, and run directory before dispatch. Default the plan to `<ocs state-dir plans>/<slug>.md` and the run directory to `<ocs state-dir runs/ralplan>/<YYMMDD-HHMMSS>-<slug>/`; follow the project's own convention instead when it already has one for plan artifacts. Preserve the original requirements by path and hash when possible; otherwise store a prompt-safe summary and its hash.
2. On resume, run `reconcile`. Treat its `required_action` as the exact next action; never infer continuity from conversation alone.
3. For a new artifact, Planner is the first writer: do not create a scaffold. Assign Planner the canonical path, template contract, requirements, repository root, and current consolidated findings, with writes limited to that planning artifact and source, test, configuration, generated-file, and Git changes prohibited. Planner creates or revises the artifact directly; the lead does not copy plan prose from a message. Checkpoint only after Planner has produced a valid Draft artifact and the lead has computed both hashes.
4. Validate the artifact. The lead may edit only workflow-owned `Status` and `Status reason` metadata. Set `In Review`, refresh both recorded hashes, checkpoint, and assemble two separate packages from the review contract.
5. Dispatch a fresh Architect and fresh Critic under their native read-only boundaries. They are blind to each other, previous rounds, claimed fixes, and expected outcomes. Each receives the complete current plan and the same review-content plan hash. Either lane's `MUST_FIX` blocks approval.
6. If blocked, set Draft with a concrete reason, persist consolidated falsifiable findings, clear both verdicts, and ask Planner to revise the same artifact. Any review-content change invalidates both prior verdicts. Advance the round only when a new official pair is dispatched.
7. If both lanes return `PASS` for the same review hash, set Approved and explain the approval and any bounded Evidence Gates in `Status reason`. Confirm the review hash did not change, checkpoint the Approved state, then compact it to the completed receipt.

Fresh official reviewers are mandatory after every review-content revision. A previous reviewer may perform a targeted closure check when a subtle or high-risk correction needs confirmation; that check can block but cannot approve or replace either fresh lane.

## Evidence and Decisions

Resolve a load-bearing empirical fact before approval when its result could change scope, architecture, acceptance semantics, or safety. When every expected result already maps to an approved in-scope branch, keep it as a bounded Evidence Gate; an unexpected result is a stop boundary for replanning.

Ask the user immediately only when an answer is necessary for the next approval or materially changes a review. Record useful non-blocking questions in the plan and continue.

Around five unsuccessful official rounds is a diagnostic trigger, not a maximum. Reassess whether the problem needs user authority, missing evidence, a bounded conditional plan, or an explicit Draft handoff. Do not manufacture approval from repetition.

When the same defect class recurs against the same contract, revisit the contract or underlying design instead of polishing the same prose again. Evidence gathering does not authorize production implementation or scope expansion.

## Quick Reference

| Situation | Required action |
|---|---|
| Plan body changed | Clear both verdicts; fresh dual review |
| Only status metadata changed | Refresh artifact hash; review hash remains stable |
| One lane returns `MUST_FIX` | Consolidate findings; return to Planner |
| Both fresh lanes pass one review hash | Mark Approved and checkpoint |
| Unexpected Evidence Gate result | Stop and replan |
| Pause or context loss | Checkpoint; resume through `reconcile` |

## Common Mistakes

- **Lead rewrites Planner output:** assign one artifact and let Planner revise it.
- **Review history leaks into a fresh lane:** package only current inputs listed in the review contract.
- **One passing lane is treated as consensus:** both independent lanes must pass the same review hash.
- **Full review prose becomes permanent state:** persist only compact verdicts and actionable findings.
- **A stale verdict survives plan drift:** hashes are authority; invalidate before continuing.
- **A hard retry cap forces a bad terminal state:** use the around-five reassessment without weakening approval.
