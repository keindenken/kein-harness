# Closure audit — round 5 (phase-48 plan, REVISION 4)

Read `docs/prompt/worker-brief.md` first; it binds you. Then `.omc/artifacts/phase48-plan/review-common.md` (limits, bar, report format). You are READ-ONLY on the repo, including `.omc/spikes/`. Running `node .omc/spikes/phase48-model/tables.mjs` and `selftest.mjs` is read-only and expected.

**You are PRIMED, on purpose.** Read the round-4 revision brief `.omc/artifacts/phase48-plan/revision-r4.md` (six Y-items) — then the CURRENT text of `.omc/plans/ralplan-phase-48-handle-admission.md` (REVISION 4) and the spike. Per-Y-item verdict: **CLOSED / PARTIAL / NOT CLOSED / REWORDED-ONLY** (the last is the one the lead most wants).

Specifically:
- **Y1**: read the new purchase/witness instrument. Is the interval actually certified (1-Lipschitz argument correct for the clearance function as implemented — check the clearance function's definition, not the comment)? Is the witness deterministic (best grid point, stated tie-break)? Do G48-1 and the flush rows assert against the interval with the stated bound? Does the convergence selftest go RED when you widen the reported interval or move the witness? Re-run the corpus and confirm the max `upper − lower` the plan prints.
- **Y2**: is the flush-pair measurement a S48-0 deliverable with a stated instrument, and is the escape "stop and report to the owner" rather than an out-of-scope candidate? If the plan ran it during planning, reproduce the number.
- **Y3**: G48-4b/4c homes and the `run:` claim consistent across §1, §3.3, §4, §5; G48-9 has a `min(w,h) < 35` fixture and the constructibility condition.
- **Y4–Y6**: each item's must-achieve, with REWORDED-ONLY in mind.

Run `tables.mjs`, diff against the embedded block, and confirm no number outside the block or the declared exception classes. Then **new defects introduced by the revision** and the id-resolution check.

Report per `review-common.md` format, findings prefixed `CD-n`. Verdict line first: `APPROVE` only if every Y-item is CLOSED and no new must-fix exists; otherwise `REVISE`. If you APPROVE, say explicitly that you approve the CURRENT TEXT AS A WHOLE, not only the Y-items.
