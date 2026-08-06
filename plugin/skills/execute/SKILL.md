---
name: execute
description: Use when a bounded code change or executable implementation plan should be carried through implementation, verification, independent review, correction, and final audit.
---

# Execute

## Overview

Execute is a lead-owned code-development convergence loop. It advances serial tasks through focused implementation, fresh self-verification, independent review, correction, blind re-review, and a whole-change final audit. Approval status is not the entry gate; executability is.

It neither invokes RALPLAN nor grants commit, push, pull-request, deployment, or release authority.

## References

- Read [state-schema.md](references/state-schema.md) before creating or resuming state.
- Read [task-ledger-template.md](references/task-ledger-template.md) before normalizing input.
- Read [review-contract.md](references/review-contract.md) before review, closure check, or final audit.
- Read [lanes.md](references/lanes.md) only when the invocation names a vendor for a lane.
- Run `ocs state execute --help` for checkpoint and reconciliation commands.

An invocation may name another vendor for a lane — `--reviewer claude,codex` for review, `--executor codex` for the implementation itself. Read [lanes.md](references/lanes.md) before dispatching whenever it does. Without such a flag every lane is native, and the rest of this section is the whole story.

Pass `run_in_background: false` on every Agent tool Executor and reviewer dispatch. A backgrounded subagent's final message never reaches the lead — only an idle notification does — so a lane whose deliverable is a judgement rather than a file returns nothing at all, and a lead waiting on all selected lanes waits forever. Reviewers deliver verdicts, so for them this is what makes the round observable. Complementary read-only lanes still run concurrently when their dispatches share one message.

## Entry and Resume

1. Resolve the canonical Git worktree and run root, the latter from `ocs state-dir runs/execute`. Resume or explicitly stop any occupying nonterminal run. Distinct worktrees host only genuinely distinct runs: every normalized task remains in this run's serial ledger through acceptance and cannot be extracted to another worktree for concurrency.
2. On resume, run `reconcile` and follow its exact next action. A transcript or old agent handle never proves completion; fingerprint drift requires inspection and fresh evidence.
3. Apply the executability gate. Approved, Draft, and unapproved plans and bounded briefs are eligible when outcome, scope, ordering, completion conditions, and verification paths require no invented material decision. Otherwise checkpoint `blocked`.
4. Normalize mechanically and checkpoint before dispatch. An unexpected Evidence Gate result blocks before dependent production work.

## Task Loop

1. Dispatch one focused `kein:executor` with one task, its scope, completion condition, repository instructions, and verification path. Keep later tasks pending; no second write-capable task may run elsewhere as a deadline workaround.
2. Apply repository testing policy first, then explicit input RED, test-first, or TDD requirements. If both are silent, Execute does not require strict TDD, but verification remains mandatory.
3. After every implementation or correction, capture fresh Executor self-verification and the exact worktree fingerprint. Self-verification is not approval.
4. Select at least one independent reviewer by risk and evidence question. Complementary read-only lanes may run concurrently. Wait for all selected lanes, then issue one consolidated correction brief containing every blocker.
5. On `MUST_FIX`, choose the original or a fresh Executor, start a correction round, clear stale evidence, correct, and verify again.
6. After correction, dispatch at least one newly spawned blind reviewer over the complete current result. Exclude earlier findings, verdicts, identities, correction notes, claimed fixes, closure results, and desired outcomes. A previous reviewer cannot approve the correction; its separate closure check can block but cannot approve.
7. Accept only when current-round verification and a fresh independent `PASS` bind to the same task, round, and fingerprint. Then checkpoint and advance serially.

## Finalization

1. After all tasks pass, run `kein:code-simplifier` only for a concrete avoidable-complexity candidate and immediately before final audit. Any simplifier write requires regression verification.
2. Dispatch fresh final reviewers over the complete post-simplification tree and final evidence. Any later mutation invalidates final approval; repeat the affected verification and final audit or restore and verify the audited tree.
3. Collapse state to a compact receipt and report accepted tasks, changed locations, final evidence, and residual risk. Do not create another durable report by default.

## Quick Reference

| Situation | Action |
|---|---|
| Unapproved but executable | Start |
| Material decision missing | Block and ask one necessary question |
| Reviewer still running | Wait and consolidate the round |
| Correction | Fresh verification and new blind review |
| Prior reviewer offers closure | Non-approving closure check only |
| Post-audit edit | Invalidate and repeat the gate |

## Red Flags

- Next writer starts before acceptance.
- Executor tests count as approval.
- Findings arrive piecemeal to the Executor.
- Existing reviewer approves its correction.
- Stale evidence survives a changed fingerprint.
- Task commit is required without user authority.

Any red flag stops advancement until its gate is restored.
