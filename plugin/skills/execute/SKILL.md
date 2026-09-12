---
name: execute
description: Use when a bounded code change or executable implementation plan should be carried through implementation, verification, independent review, correction, and final audit.
argument-hint: "[plan path or task brief] [--reviewer claude|codex] [--executor claude|codex]"
---

# Execute

## Overview

Execute is a lead-owned code-development convergence loop. It advances serial tasks through focused implementation, fresh self-verification, independent review, correction, blind re-review, and a whole-change final audit. Approval status is not the entry gate; executability is.

It does not invoke RALPLAN.

## At entry

Read from this working directory when the skill loaded; `ocs state-dir` answers relative to it.

- `command -v ocs` → !`command -v ocs || echo "NOTHING ON PATH — no state command will run"`
- `ocs state-dir runs/execute` → !`ocs state-dir runs/execute 2>&1`

!`ocs state execute --help 2>&1`

## References

- Read [state-schema.md](references/state-schema.md) before creating or resuming state.
- Read [task-ledger-template.md](references/task-ledger-template.md) before normalizing input.
- Read [review-contract.md](references/review-contract.md) before review, closure check, or final audit.
- Read [lanes.md](references/lanes.md) only when the invocation names a vendor for a lane — `--reviewer claude,codex` for review, `--executor codex` for the implementation itself.
- Read [split.md](references/split.md) only when a task of this run is to be authored in another worktree while this run continues.
- Run `ocs state execute --help` for checkpoint and reconciliation commands.

## Entry and Resume

1. Resolve the canonical Git worktree and run root, the latter from `ocs state-dir runs/execute`. Resume or explicitly stop any occupying nonterminal run. The ledger is serial in this worktree: every normalized task keeps its place in it through acceptance. Another worktree is another run, and a task of this run may be authored there and brought back when its turn comes; `split.md` has the shape.
2. On resume, run `reconcile` and follow its exact next action. An input it reports changed is amended with its reason when the change was authorized, and blocked when it was not; a run does not restart because its plan moved. A transcript or old agent handle never proves completion; fingerprint drift requires inspection and fresh evidence.
3. Apply the executability gate. Approved, Draft, and unapproved plans and bounded briefs are eligible when outcome, scope, ordering, completion conditions, and verification paths require no invented material decision. Otherwise checkpoint `blocked`, and ask the one question that would unblock it when there is one.
4. Normalize mechanically and open the run with `start` before dispatch. An unexpected Evidence Gate result blocks before dependent production work.

## Task Loop

1. Dispatch one focused `kein:executor` with one task, its scope, completion condition, repository instructions, and verification path. Keep later tasks pending; no second write-capable task runs in this worktree.
2. Apply repository testing policy first, then explicit input RED, test-first, or TDD requirements. If both are silent, Execute does not require strict TDD, but verification remains mandatory.
3. After every implementation or correction, capture fresh Executor self-verification and the exact worktree fingerprint. Self-verification is not approval.
4. Select at least one independent reviewer by risk and evidence question. Complementary read-only lanes may run concurrently when their dispatches share one message. Wait for all selected lanes, then issue one consolidated correction brief containing every `BLOCK` finding.
5. On `BLOCK`, choose the original or a fresh Executor, start a correction round, clear stale evidence, correct, and verify again.
6. After correction, dispatch at least one newly spawned blind reviewer over the complete current result. Exclude earlier findings, verdicts, identities, correction notes, claimed fixes, closure results, and desired outcomes. A previous reviewer cannot approve the correction; its separate closure check can block but cannot approve.
7. Accept only when current-round verification and a fresh independent `PASS` or `REVISE` bind to the same task, round, and fingerprint. A `REVISE` lane's findings are dispositioned at acceptance — fixed before it with the verification path re-run and no fresh lane, promoted to an appended task, or carried on this one with a reason where the review contract requires it — and then written into the checkpoint with the acceptance. Then advance serially.

## Finalization

1. After all tasks pass and before final audit, `kein:code-simplifier` is there for a behaviour-preserving pass over the changed code, where the tasks left something the final reviewers would otherwise have to read past. Any simplifier write requires regression verification.
2. Dispatch fresh final reviewers over the complete post-simplification tree and final evidence. Any later mutation invalidates final approval; repeat the affected verification and final audit or restore and verify the audited tree.
3. Collapse state to a compact receipt and report accepted tasks, changed locations, final evidence, and residual risk. Do not create another durable report by default.
