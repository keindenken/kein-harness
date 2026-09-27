# `execute`: what is still open

## The lead reads the clock before every checkpoint

Every verification entry carries `observed_at` and every verdict `reviewed_at`, and `checkpoint` fills fingerprints and the revision from `"auto"` but not these two times. After the 260923 run's ledger carried invented round-minute and future times, the lead of the 260926 slice-chain run ran `date -u` before every checkpoint instead: dozens of calls in one run, noticed and questioned by the user. The value is still only an upper bound for `reviewed_at`, which should be when the lane judged, not when the lead recorded it.

Options, not yet decided: `checkpoint` accepts `"auto"` for `observed_at` and `reviewed_at` and stamps its own clock (removes the calls and the future-time risk; `reviewed_at` stays an upper bound); the lane's response format carries its own time and the lead copies it (exact, but the lane can invent it too); or a single `ocs state execute` step that records the lead's verification run together with its time.

**Reopen when** `checkpoint` is next changed, or a ledger again carries a time nobody read from a clock.

## A completion condition's own wording cannot be corrected inside a run

`state.py` refuses any change to an existing task's `scope` or `completion_condition`, and `amend` moves only the plan. So when measurement falsifies the literal words a condition was ledgered with, the only exit is `blocked`, then abort and a new run. oh-my-claudecode 5.x gave ralph the opposite route: a criterion is replaced or superseded, the original kept verbatim with reason, evidence, authority and time, and every completion claim and approval bound to the criteria revision it was made under.

Deliberated on 2026-09-18 and not added. Every falsified ruling in the archived runs (`docs/artifacts/ledgers/260829-p47-run-state`, `260903-p48-run-state`: eight execute runs) was a plan clause, and the conditions defer to the plan ("DR47-6 lands", "the plan's §4 … text governs"), so `amend` carries the correction. The freeze is also what stops a lead fitting the condition to what got built; omc needed more than a dozen hardening commits to make its route safe.

**Reopen when** a run shows a condition written as literal values rather than a pointer — S48-1a's "20→8 / 80→16 clamped" is the shape — whose wording measurement refutes, and a lane's `blocks` cites that wording so the task cannot accept after the plan is amended.

The neighbouring question is in `docs/closed-threads.md`, "A plan correction ends the run": whether an amendment that touches the condition an already accepted task passed under should unseat that acceptance. That thread closed 2026-09-26 (4a41c57): a task accepted under an earlier revision now keeps the run from completing until a fresh lane re-confirms it against the amended plan. This section's own question — correcting a condition's wording inside a run, rather than what an amendment does to an acceptance already made — is untouched by that closure.
