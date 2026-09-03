# Revision brief — round 5 → round 6 (phase-48 plan) — FINAL TEXT REVISION

Round 5 ran a PRIMED closure audit (`CD-n`) and a FRESH unprimed reviewer (`L-n`) on REVISION 4. Both REVISE. Both re-ran the instrument (selftest GREEN, tables byte-identical 192/192), both re-confirmed every decision's reasoning or outcome, and the fresh lane's independent implementation reproduced every free-regime table including the `scarcest` names. The remaining defects are narrow: one gate's comparison rule (G48-4b), the instrument's self-controls, one false RUN-P label, one scheduling home, counts, and a withdrawn figure doing live work. **This is the FINAL text revision** — the lead intends round 6 as an approval round, not a finding round. Produce **REVISION 5** in place plus spike changes; same limits; paste the citation gate and the tables diff statement.

## X1 — G48-4b compares INTERVALS FOR OVERLAP, never witnesses for identity (L-1, L-2, CD-2 in part) — **LEAD RULING**

The grid's origin is not in the contract, and two faithful readings (region-anchored vs absolute lattice) disagree on 27.4 % of witnesses over G48-4b's corpus while both stay inside the certified bracket. Fixing that by adding the origin to the contract would leave the gate keyed to a convention forever; fix the CLASS instead: **G48-4b compares (a) the eight REGION rects exactly, over the full corpus, and (b) purchase INTERVALS for OVERLAP (`[lowerA, upperA] ∩ [lowerB, upperB] ≠ ∅`), over a named sub-corpus.** Witness identity is dropped from the gate. `witnessPointFor` stays an export for the DOM rows (G48-5 presses it), and FOR THAT its determinism conventions (region-anchored grid, origin, extent under clip, row-major ascending, strict `>`) become contract text in C48-1h — but no gate compares witnesses across implementations, so a conforming oracle cannot fail on a convention. Correct C48-1h's "only if" sentence accordingly.

**Budget (L-2):** the region legs are rect arithmetic and cheap — full 1…120² corpus. The interval legs are the expensive ones: name the sub-corpus (the §5 fixtures + 1…40 × 1…40 + a seeded random sample of stated size) and MEASURE the runtime of G48-4b's and G48-4c's projected shape (the spike can time its own functions); print it beside the rows and show it fits ci.yml's 35-minute job with the ~4.8× runner factor and the package-suite double-run the workflow itself documents. If it does not fit, shrink the named sub-corpus, not the region legs.

## X2 — The instrument's self-controls (CD-1, CD-2, CD-3, CD-4, L-3) — **LEAD RULING on CD-4**

- **CD-1**: case 3 fires only on the CONJUNCTION of the two tangent-handling halves; both single-half reverts are inert (belt-and-braces). Say exactly that in `model.mjs`, `selftest.mjs` and the status block — the honest statement is "either half alone suffices; case 3 proves the pair cannot both regress", not a single-mutation blame. Round 3 blamed one half, round 4 the other; record that both claims were wrong.
- **CD-2**: add a selftest case that goes RED on a scan-order mutation (a fixture with multiple grid maximisers and a recorded expected witness; reversing the row loop must move it and fail).
- **CD-3**: `gridStepPx` gains its condition in C48-1h (a dyadic step, `1/2^k`, so the grid contains the model's half-integer offsets); drop "the lower bound settles regardless"; note that `0.03` is a legal-looking value that turns G48-1 RED with no model change, which is why the condition is contract text.
- **CD-4 ruling**: emptiness stops being grid-quantised — decide it EXACTLY by rect difference (the owned region is a rect minus earlier rects; emptiness of that is closed form and cheap). `empty` then certifies itself and C48-5's strict inequality has an exact gate. State in C48-1g.
- **L-3**: T12's framing — the bound is ARGUED (1-Lipschitz), the table CONFIRMS only self-consistency; give it the analytic control (a single-rect region whose exact disc is known, asserted inside `[lower, upper]`) or drop the "confirm" wording. The closure lane's empirical Lipschitz check (worst L = 1.000000 over 600k pairs, with a working control) can be cited as evidence, labelled as its instrument.

## X3 — Y2's remaining holes (CD-5, CD-6) — **LEAD RULING on CD-6**

- **CD-5**: the `.descvi/screens.json` claim is false as written (`rect`/`top`/`left`/`width`/`height` all occur — in Korean prose strings). Restate as "no geometry FIELD" with the exact command and the field names searched, and re-label with the command beside it.
- **CD-6**: S48-0 cannot be both the doc-only pre-code story and land a live measurement. **Ruling: split it.** `S48-0a` — docs, plans, specs, anchor retirement (unchanged scope, no code). `S48-0b` — the U48-5 measurement gate: home `.omc/spikes/phase48-model/flush-pairs.mjs` (+ whatever DOM dump or Playwright driver it needs), explicitly using the SPIKE's `handleRegions` (production's does not exist yet — say so), allowed to start a dev server because it runs at EXECUTION time (planning's no-server limit does not bind the executor; the story must still name the owner's live servers as off-limits and use its own port/profile). The code commit is blocked on S48-0b's number; the escape stays "stop and report to the owner". Update the ladder, done-whens and §3.9.

## X4 — Mechanical corrections (CD-7, CD-8, CD-9, CD-10, CD-11, CD-12, L-4, L-5, L-6)

- G48-5's RED-when quotes the certified lower bound **4.19**, not the withdrawn 4.20 (CD-7/L-4).
- §1's counts: **two** new vitest files (`e2e/handle-derivation.test.ts`, `src/app/sandbox/handle-lab/spacing-overlap.test.ts`); G48-4b's home exists and is REWRITTEN; G48-4a takes the citation-gate's two-`run:`-line shape (`--selftest` then the bare run) — say so (CD-8).
- Kill the two `Z6` tokens (an id from a retired brief) — replace with the section reference (CD-9).
- §2.8's shipped baseline row carries its `$` command line like §2.7's blocks (CD-10).
- The two out-of-block decimals: print `0.022097` in U48-13 (not 0.022); reword P48-4's "0.5 px sliver" to avoid a bare decimal or add it to the rhetorical exception class (CD-11).
- §3.0 orders C48-1g before C48-1h (CD-12).
- U48-11: state the asymmetry with U48-5 explicitly — it RECORDS inside the commit and decides nothing, which is why it may stay there (L-5).
- C48-1g's degenerate return shape includes `lower`/`upper` so a ported implementation carries the fields §5's flush rows read (L-6).

---

**Status line for REVISION 5:** name both round-5 lanes and verdicts; state that G48-4b's comparison rule changed (X1) and why that closes the convention class; state that this is the final text revision before the approval round. Final message ≤40 lines: per X-item CLOSED/PARTIAL, loud disagreements, new ⚠ UNVERIFIED, the tables command + diff statement, the measured G48-4b/4c runtime, the citation-gate block.
