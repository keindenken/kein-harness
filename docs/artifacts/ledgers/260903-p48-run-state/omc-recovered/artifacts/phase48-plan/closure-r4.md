# Closure audit — round 4 (phase-48 plan, REVISION 3)

Read `docs/prompt/worker-brief.md` first; it binds you. Then `.omc/artifacts/phase48-plan/review-common.md` (limits, bar, report format). You are READ-ONLY on the repo, including `.omc/spikes/`. Read-only probes are encouraged; running `node .omc/spikes/phase48-model/tables.mjs` is read-only and expected.

**You are PRIMED, on purpose.** Read the round-3 revision brief `.omc/artifacts/phase48-plan/revision-r3.md` — eight Z-items — then the CURRENT text of `.omc/plans/ralplan-phase-48-handle-admission.md` (REVISION 3) and the spike `.omc/spikes/phase48-model/` it now cites. Give a per-Z-item verdict: **CLOSED / PARTIAL / NOT CLOSED / REWORDED-ONLY** — the last is the one the lead most wants: a sentence that changed while the defect survived (a "definition" that is a name; a table "regenerated" with one cell still hand-typed; a convention stated in one clause and contradicted by the instrument; a gate leg moved to another row without a RED-when).

Specifically for Z1: run `tables.mjs`, then diff its output against every number in the plan — a number in the plan that is not in the output, or an output the plan misquotes, is must-fix. Read `model.mjs` against C48-1's clauses and say whether it implements the contract AS WRITTEN (membership convention, `cornerOrder`, `stripOrder`, ramp, witness degenerate value, purchase measure, criterion-2 measure) — a model that silently differs from the contract makes every table a measurement of something else.

For Z4: confirm from source that `RESIZE_STRIP_Z`/`RESIZE_CORNER_Z` are now KEEP in §3.10, that no story deletes them, and that G48-9's DOM row has a fixture where two strips overlap and a RED-when.

Then: **new defects introduced by the revision**, and the id-resolution check (every id referenced resolves; retired ids are noted).

Report per `review-common.md` format, findings prefixed `CC-n`. Verdict line first: `APPROVE` only if every Z-item is CLOSED and no new must-fix exists; otherwise `REVISE`.
