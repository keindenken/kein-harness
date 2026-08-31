---
name: plan
description: Use when an implementation plan should be written as a durable, reviewable artifact.
argument-hint: "<what to plan>"
---

# Plan

## Overview

Plan produces one canonical implementation plan artifact. Planner writes it; the lead resolves where it goes, bounds what Planner may touch, and checks the result against its contract.

## Required Files

[plan-template.md](references/plan-template.md) is written to Planner. Hand it over by absolute path — copying it into the brief spends tokens restating a file the lane can open, and a paraphrase of it is a second copy to keep true. Read it yourself before validating what comes back.

## Workflow

1. Resolve the task, the repository, and the canonical plan path.
2. Dispatch one fresh `kein:planner` with the Agent tool, supplying the canonical path, the template's absolute path, the requirements, and the repository root. A lane that cannot open that path — a vendor lane under its own sandbox — gets the file's contents instead, which is what `ocs ask --task-file` assembles.
3. Validate the artifact against the template, then report its path.

## Where the plan goes

Default to `<ocs state-dir plans>/<slug>.md`; follow the project's own convention instead when it has one for plan artifacts. Preserve the requirements by path and hash when possible; otherwise keep a prompt-safe summary and its hash.

## Sizing

Size the planning effort to the work, and say in the brief which size you chose. Work whose approach is already settled wants the artifact and its evidence, not a survey of alternatives; contested work wants the alternatives resolved before anything is written. Size governs how far Planner investigates and how much the body carries. It does not govern what the artifact contains — the template contract holds at every size.

A plan that comes back carrying several unresolved material decisions was sized too small, and one that surveys alternatives nobody was choosing between was sized too large. The size was the lead's call and correcting it is too.

## What Planner may touch

Limit its writes to the plan artifact; prohibit source, test, configuration, generated-file, and Git changes. Ownership of the artifact's body is the template's to state and it states it, so nothing here repeats it — including the `Status` line, which Planner writes as `Draft` and no workflow-run status.

## Evidence and Decisions

Resolve a load-bearing empirical fact when its result could change scope, architecture, acceptance semantics, or safety. Where every expected result already maps to an in-scope branch, record it as a bounded Evidence Gate instead of resolving it now.

Ask the user immediately only when an answer materially changes the plan. Record useful non-blocking questions in the plan and continue.

When the same defect class recurs against the same contract, revisit the contract or the underlying design rather than polishing the same prose again.
