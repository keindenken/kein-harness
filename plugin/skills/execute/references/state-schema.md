# Execute State Schema

Store state at `<run-root>/<YYMMDD-HHMMSS>-<slug>/state.json`, where the run root is `ocs state-dir runs/execute`.

Active, blocked, and interrupted states retain run identity, input identity, canonical worktree and Git common directory, baseline and observed fingerprints, the serial task ledger, current task and round, latest verification, unresolved findings, final-audit facts, and the exact next action. They never store transcripts, raw logs, or agent handles.

Every state carries a zero-based monotonic `revision`. Each candidate increments the revision observed in the current checkpoint; a stale candidate is rejected after the canonical-worktree lock is acquired.

**Write `"auto"` for anything derived rather than decided, and `checkpoint` fills it in.** It accepts the sentinel for `revision`, for `worktree.observed`, for `worktree.baseline` on the first checkpoint only, and for any `worktree_fingerprint` or `final_fingerprint` wherever it appears — the latest verification, each task's verification and acceptance, every verdict, and the final audit. All of them are computed from the predecessor and the worktree, which the checkpoint reads anyway in order to check what was written; asking for them creates one way to be wrong per field and no way to be right that those two sources do not already determine.

`"auto"` for `worktree.baseline` after the run has started is an error rather than a re-derivation, because the baseline is what drift is measured against.

Each fingerprint contains `head`, `index_sha256`, `tracked_diff_sha256`, `untracked_sha256`, and the combined `fingerprint`. It changes for HEAD, staged, unstaged, and untracked content changes, except for untracked paths under `.agents/kein/runs/`. That exclusion is what keeps the fingerprint measurable: the run ledger lives inside the worktree, so a checkpoint writing its own `state.json` would otherwise change the untracked set it had just recorded and every following `reconcile` would report drift over work nobody did. Deliverables elsewhere under `.agents/kein/` — plans among them — stay in the fingerprint.

Completed receipts retain only input reference/hash, worktree root/final fingerprint, accepted task summaries, final verification, and fresh independent final-audit PASS facts. Aborted receipts retain identity, worktree root, time, and stop reason.

Use:

```text
ocs state execute validate <state.json>
ocs state execute reconcile <state.json>
ocs state execute check-worktree <run-root> <worktree>
ocs state execute checkpoint <state.json> <candidate.json>
```

`checkpoint` validates transitions, input identity, current worktree fingerprint, and single-run exclusivity before an atomic same-directory replace. `reconcile` never promotes partial work; drift requires inspection and fresh verification before selecting a continuation.
