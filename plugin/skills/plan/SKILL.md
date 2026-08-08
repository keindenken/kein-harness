---
name: plan
description: Use when an implementation plan should be written as a durable artifact without a consensus review gate.
---

# Plan

## Overview

Plan produces one canonical implementation plan from a single Planner pass and stops. It is the primitive RALPLAN adds a consensus gate to, and its output is RALPLAN's first-round artifact: the same file, at the same path, under the same contract.

It runs no review, grants no execution authority, and routes to no other skill.

## When RALPLAN instead

Use RALPLAN when a review gate could actually return `MUST_FIX` — the architecture is contested, an independent reader would plausibly disagree, or a wrong plan is expensive to discover later. A gate that cannot fail is ceremony, and its rounds are the expensive part.

The choice is not final in either direction. The artifact is the same one, so a plan written here enters RALPLAN later without being rewritten.

## Required Files

Read [plan-template.md](../ralplan/references/plan-template.md) before dispatching Planner. RALPLAN owns that file because there is exactly one contract for this artifact, and a second copy would drift from it and break promotion.

Ignore its `In Review` status, its two-hash scheme, and its verdict invalidation rules. All three serve a review gate, and this skill has none.

## Workflow

1. Resolve the task, the repository, and the canonical plan path. Default to `<ocs state-dir plans>/<slug>.md`; follow the project's own convention instead when it has one for plan artifacts.
2. Dispatch one fresh `kein:planner` with the Agent tool and `run_in_background: false`, supplying the canonical path, the template contract, the requirements, and the repository root. Limit its writes to that artifact and prohibit source, test, configuration, generated-file, and Git changes.
3. Planner is the first writer. Do not create a scaffold, and do not copy plan prose out of its message — it writes the file itself.
4. Validate the artifact against the template. The lead may edit only `Status` and `Status reason`.
5. Leave `Status: Draft`, record in `Status reason` that no review gate was run, then report the path and stop.

## Keep no state

No run directory, no ledger, no hashes. A single pass has nothing to reconcile, and both artifact hashes exist to invalidate reviews that never happen here; RALPLAN computes them if it takes the artifact. Every other workflow in this harness keeps state, so the absence here is a decision rather than an omission.

## The status reason is the whole safety property

A plan written here is indistinguishable from a reviewed one by its path, its template, and its prose. `Status reason` is the only place that difference is recorded, so a reason that omits it produces an artifact that reads as gated and was not. Execute accepts unapproved plans by design, which makes this a fact downstream work needs rather than a formality.
