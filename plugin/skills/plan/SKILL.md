---
name: plan
description: Use when an implementation plan should be written as a durable, reviewable artifact.
---

# Plan

## Overview

Plan produces one canonical implementation plan artifact. Planner writes it; the lead resolves where it goes, bounds what Planner may touch, and checks the result against its contract.

## Required Files

Read [plan-template.md](references/plan-template.md) before dispatching Planner.

## Workflow

1. Resolve the task, the repository, and the canonical plan path. Default to `<ocs state-dir plans>/<slug>.md`; follow the project's own convention instead when it has one for plan artifacts. Preserve the requirements by path and hash when possible; otherwise keep a prompt-safe summary and its hash.
2. Dispatch one fresh `kein:planner` with the Agent tool and `run_in_background: false`, supplying the canonical path, the template contract, the requirements, and the repository root. Limit its writes to that artifact; prohibit source, test, configuration, generated-file, and Git changes.
3. Planner is the first writer. Do not create a scaffold, and do not copy plan prose out of its message — it writes the file itself.
4. Validate the artifact against the template, then report its path.

## Evidence and Decisions

Resolve a load-bearing empirical fact when its result could change scope, architecture, acceptance semantics, or safety. Where every expected result already maps to an in-scope branch, record it as a bounded Evidence Gate instead of resolving it now.

Ask the user immediately only when an answer materially changes the plan. Record useful non-blocking questions in the plan and continue.

When the same defect class recurs against the same contract, revisit the contract or the underlying design rather than polishing the same prose again.
