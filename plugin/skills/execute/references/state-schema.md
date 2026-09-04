# Execute State Schema

Store state at `<run-root>/<YYMMDD-HHMMSS>-<slug>/state.json`, where the run root is `ocs state-dir runs/execute`.

Active, blocked, and interrupted states retain run identity, input identity, canonical worktree and Git common directory, baseline and observed fingerprints, the serial task ledger, current task and round, latest verification, unresolved findings, final-audit facts, and the exact next action. They never store transcripts, raw logs, or agent handles.

A finding carries `reviewer_role`, `claim`, `evidence`, `impact`, `required_correction`, `severity` (`critical`, `important`, `minor`), `confidence` (`high`, `medium`, `low`), and `blocks` — `null`, a verbatim clause of the task's `completion_condition` (whitespace and case folded), or text prefixed `regression: ` or `instruction: `. A finding carried on an accepted task may add `carried_because`; a `critical` one must. A verdict is `PASS`, `REVISE`, or `BLOCK`, and at acceptance it is checked against the findings of the same `reviewer_role`: `BLOCK` needs one that cites, `REVISE` needs at least one and none that cite, `PASS` needs none.

A finding recorded before `blocks` existed stands where it stood, unchanged, until something is accepted over it; acceptance, the final audit and the receipt require the field, and any finding written new carries it.

`unresolved_findings` on an accepted task is what that task carries — findings with `blocks: null` a `REVISE` lane returned and the lead chose not to promote. A finding that cites cannot be retained by an accepted task, by a final audit, or by completion. The same rule holds for the run-level list.

Every state carries a zero-based monotonic `revision`. Each candidate increments the revision observed in the current checkpoint; a stale candidate is rejected after the canonical-worktree lock is acquired.

**Write `"auto"` for anything derived rather than decided, and `checkpoint` fills it in.** It accepts the sentinel for `revision`, for `worktree.observed`, for `worktree.baseline` on the first checkpoint only, and for any `worktree_fingerprint` or `final_fingerprint` wherever it appears — the latest verification, each task's verification and acceptance, every verdict, and the final audit. All of them are computed from the predecessor and the worktree, which the checkpoint reads anyway in order to check what was written; asking for them creates one way to be wrong per field and no way to be right that those two sources do not already determine.

`"auto"` for `worktree.baseline` after the run has started is an error rather than a re-derivation, because the baseline is what drift is measured against.

Each fingerprint contains `head`, `index_sha256`, `tracked_diff_sha256`, `untracked_sha256`, and the combined `fingerprint`. It changes for HEAD, staged, unstaged, and untracked content changes, except for untracked paths under `.agents/kein/runs/`. That exclusion is what keeps the fingerprint measurable: the run ledger lives inside the worktree, so a checkpoint writing its own `state.json` would otherwise change the untracked set it had just recorded and every following `reconcile` would report drift over work nobody did. Deliverables elsewhere under `.agents/kein/` — plans among them — stay in the fingerprint.

Completed receipts retain only input reference/hash, worktree root/final fingerprint, accepted task summaries — each with the `carried_findings` its task carried — final verification, fresh independent final-audit PASS facts, and the run-level `carried_findings`. Both carried lists are exact projections of the checkpointed state; a receipt that drops one is refused, because the receipt is what the next reader inherits. Aborted receipts retain identity, worktree root, time, and stop reason.

Use:

```text
ocs state execute validate <state.json>
ocs state execute reconcile <state.json>
ocs state execute check-worktree <run-root> <worktree>
ocs state execute start --run-root <runs/execute> --slug <slug> --kind plan --input <path> --worktree <path> --tasks <tasks.json>
ocs state execute checkpoint <state.json> <candidate.json>
ocs state execute amend <state.json> --reason <text> [--summary <text>]
```

`start` writes a run's first checkpoint from its parts rather than from a hand-authored candidate. It names the run directory — `<run-root>/<YYMMDD-HHMMSS>-<slug>/state.json`, printed, and what every later checkpoint takes as its positional — reads the canonical root and Git common directory out of `--worktree`, hashes `--input` or `--summary` for the input identity, and opens the ledger from `--tasks`: a JSON array whose entries carry `id`, `title`, `scope`, `completion_condition`, `verification_path` and `rationale` and nothing else. The five remaining fields on each task are a run's opening position and are filled in. Pass a `state.json` path instead of `--run-root` with `--slug` when the directory already exists. Nothing needs creating first; a checkpoint makes its own parent directory.

`checkpoint` promotes a hand-authored candidate and stays the escape hatch for a state nothing else builds.

`amend` moves the run's input identity in place. A plan is edited while its run is live whenever an owner ruling or a factual correction lands in it, and that is a change to the input, not a new run: `amend` re-reads a plan input from its path (or takes `--summary` for a brief), refuses an unchanged input, and appends `{at, reason, from, to}` to `input.amendments`, which the completed receipt carries. A candidate that moves the hash without that entry is still refused, and `reconcile` names `amend` as the exit when it finds the input changed. Amend between tasks; a plan edit is a worktree change like any other, and inside a review round it moves the fingerprint the round was reviewed at.

`checkpoint` validates transitions, input identity, current worktree fingerprint, and single-run exclusivity before an atomic same-directory replace. `reconcile` never promotes partial work; drift requires inspection and fresh verification before selecting a continuation.
