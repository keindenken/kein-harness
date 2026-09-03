# Closure audit — round 2 (phase-48 plan, REVISION 1)

Read `docs/prompt/worker-brief.md` first; it binds you. Then `.omc/artifacts/phase48-plan/review-common.md` (limits, bar, report format). You are READ-ONLY on the repo. Read-only probes are encouraged.

**You are PRIMED, on purpose.** Read the round-1 revision brief `.omc/artifacts/phase48-plan/revision-r1.md` — twelve R-items, each with a *must achieve* — and then the CURRENT text of `.omc/plans/ralplan-phase-48-handle-admission.md` (REVISION 1). Your job is a per-item verdict on whether each R-item's *must achieve* is met in the current text:

- **CLOSED** — met, and the mechanism/number is in the plan, not promised for later.
- **PARTIAL** — part met; say which part is not.
- **NOT CLOSED** — not met.
- **REWORDED-ONLY** — the sentence changed but the defect the item names is still there. **This is the verdict the lead most wants from you**, because only a lane that saw the previous text can see a finding restated rather than fixed. Look for: a number replaced by a rule with no rule stated; a gate given a RED-when that no fixture in the plan can reach; a "precondition stated" that is not a contract clause; a decision that gained an option but not a price; a probe the brief asked for that is reported as "to be run in S48-n".

For each R-item: verdict, the plan section(s) where it is answered, and — where the brief required a probe (R1's re-derivation under rect + chosen order, R3's arc numbers, R4's flush-pair re-measurement, R6's floor) — whether the plan shows the probe's OUTPUT and whether you re-ran it (do, where it is cheap; the probe trees at `/private/tmp/arch48/` and the lanes' scratchpads exist, but re-copy sources from f411977 and never trust a stale copy).

Then a short section: **new defects introduced by the revision** — anything the rewrite broke that round 0 had right (a cross-reference that now dangles, an id that changed meaning, a gate that lost its RED-when in the rewrite).

Report per `review-common.md` format, findings prefixed `CA-n`. Verdict line first: `APPROVE` only if every R-item is CLOSED and no new must-fix exists; otherwise `REVISE`.
