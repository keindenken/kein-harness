# Closure audit — round 6 (phase-48 plan, REVISION 5) — APPROVAL ROUND

Read `docs/prompt/worker-brief.md` first; it binds you. Then `.omc/artifacts/phase48-plan/review-common.md` (limits, bar, report format). READ-ONLY on the repo including `.omc/spikes/`; running the spike's scripts is expected.

**You are PRIMED, on purpose.** Read the round-5 revision brief `.omc/artifacts/phase48-plan/revision-r5.md` (four X-items) — then the CURRENT text of `.omc/plans/ralplan-phase-48-handle-admission.md` (REVISION 5) and the spike. Per-X-item verdict: **CLOSED / PARTIAL / NOT CLOSED / REWORDED-ONLY**.

Specifically:
- **X1**: does G48-4b now compare region rects (full corpus) + purchase intervals for OVERLAP (named sub-corpus), with witness identity gone from every gate; are the witness conventions contract text for the export only; is the measured runtime printed and does the budget arithmetic hold against ci.yml's own numbers?
- **X2**: run the selftest; apply the stated mutants yourself (single-half tangent reverts → GREEN as now documented; both → RED; scan-order revert → RED; interval widening/narrowing → RED). Is emptiness now exact rect-difference with a control?
- **X3**: is S48-0a/S48-0b split coherent in the ladder, done-whens and §3.9; is the `.descvi/screens.json` claim restated with the actual command and field names?
- **X4**: each mechanical item.

Run `tables.mjs`, diff against the embedded block, run the numeric audit rule (every decimal outside the block is in a declared exception class), and do the id-resolution check.

**This is an approval round.** If every X-item is CLOSED and no new must-fix exists, your verdict is `APPROVE`, and you must state explicitly that you approve the CURRENT TEXT AS A WHOLE — including sections no X-item touched — not merely the X-items. Anything less (a conditional approve, "approve once…") is REVISE. If you REVISE, separate must-fix from worth-considering as always; a worth-considering list does not block an APPROVE.

Report per `review-common.md` format, findings prefixed `CE-n`. Verdict line first.
