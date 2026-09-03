# Closure audit — round 3 (phase-48 plan, REVISION 2)

Read `docs/prompt/worker-brief.md` first; it binds you. Then `.omc/artifacts/phase48-plan/review-common.md` (limits, bar, report format). You are READ-ONLY on the repo. Read-only probes are encouraged.

**You are PRIMED, on purpose.** Read the round-2 revision brief `.omc/artifacts/phase48-plan/revision-r2.md` — eleven Q-items — and then the CURRENT text of `.omc/plans/ralplan-phase-48-handle-admission.md` (REVISION 2). Give a per-Q-item verdict: **CLOSED / PARTIAL / NOT CLOSED / REWORDED-ONLY** — the last is the one the lead most wants from you: a sentence that changed while the defect it names survived (a measure "defined" by a name with no formula; a floor "stated" as a requirement; a lever listed without its 220×10 AND 10×220 price; a gate leg dropped from one row and quietly re-attached to another; a ruling whose reason is the old one with new words).

For each Q-item: verdict, the section(s) where it is answered, and where a probe was required (Q2's inscribed-disc measure and the ramp-interior re-check, Q7's per-fixture floors, Q10's `bandPx > cornerNarrowPx` row) whether the plan shows the probe OUTPUT and whether you re-ran it (re-copy sources from f411977; never trust a stale copy; the scratch trees under `/private/tmp/claude-501/.../scratchpad/p48/` and `/private/tmp/arch48/` exist from earlier lanes).

Then: **new defects introduced by the revision** — anything the rewrite broke that REVISION 1 had right (dangling ids, a gate that lost its RED-when, a done-when list that no longer matches its story's Lands column, a number that changed without provenance). Check every id referenced resolves to a defined item.

Report per `review-common.md` format, findings prefixed `CB-n`. Verdict line first: `APPROVE` only if every Q-item is CLOSED and no new must-fix exists; otherwise `REVISE`.
