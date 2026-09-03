# Revision brief — round 2 → round 3 (phase-48 plan)

Round 2 ran a PRIMED closure audit (`CA-n`) against `revision-r1.md` and a FRESH unprimed reviewer (`F-n`) on REVISION 1. Both returned REVISE. Round 1's findings were false facts (shape, order, price); round 2's are smaller and of a different kind — an ambiguous coordinate, an unstated measure, a gate leg voided by a later ruling, a denominator, one cell computed with the ramp off. The trend is converging; this is the last text round before the lead decides whether a third buys anything. Closure verdicts on the R1 items: R1, R2, R5, R6, R7, R9, R10, R11 CLOSED; R3, R4, R8, R12 PARTIAL. This brief is the ONE consolidated list; lead rulings are marked. Produce **REVISION 2** in place, for a reader who has seen none of this. Same limits as before. Re-run the citation gate and paste it.

---

## Q1 — C48-1b gives the four band rects IN COORDINATES (F-1) — **LEAD RULING**

"Running the whole edge" admits `[0, L]` and `[−5, L+5]`; the lab's capsule reaches 5 px past each vertex and a reader following §2.0's provenance takes the second. Under `[−5, w+5]` the `w` handle at 220×10 owns **zero** area — criterion 1 fails outright. **Ruling: bands span exactly `[0, L]` along their edge** (no overreach past the vertex; the corner squares own the vertex zone), thickness 10 centred on the edge line. Write the four rects as closed-form coordinates in C48-1b, and say which reading every RUN-P number used.

## Q2 — U48-8's arithmetic is wrong in the direction that changes the owner's menu (F-4, CA-10, CA-11, F-6, CA-4) — **LEAD RULING**

Fresh review measured at 220×10, sweeping a FIXED corner under the ruled order `n,e,s,w`: inscribed radius of `w` = **2.50 for every corner ≤ 4**, 2.00 at 6, 1.00 at 8. The cap is `bandPx / 2`, because `n` and `s` (tested first) own the band's entire inward half at a 10 px short side — at that height n's and s's straddle zones cover the whole interior. Shrinking the corner is **not** a lever under the ruled order; with order `w,e,n,s` and corner 2 the radius reaches 4.00. So "reaching 4 needs a corner ≤ 2, at which criterion 2 collapses" is a false reason for a true conclusion. Also: diagonal share is aspect-invariant (CA-10 re-ran: corner 2 → 12.9 %, 4 → 42.6 %, 5 → 61.8 %, 6 → 81.2 %, 8 → 100 % at both 100×100 and 220×10) — say so, and quote the number at the size the claim is about.

**Must achieve:**
1. Restate U48-8 on the corrected arithmetic: under C48-1 as ruled, criterion-1 purchase at short side 10 is capped at `bandPx/2` = 2.5 for any corner and is 1.0 at the owner's corner 8; the corner is not the lever. List the REAL levers with each priced at **220×10 and 10×220**: band thickness (`bandPx`), strip precedence/geometry (a fixed order favours one aspect ratio and hurts the other; anything size-dependent is a predicate P48-1 forbids — say so), the floor itself, and a fallback below some short side. The plan still does not choose; the owner does. Keep the steelman (strips carry no paint).
2. **Define the purchase measure** in §2.7's header: the exact geometric largest inscribed disc inside the handle's OWNED region (distance to the region boundary and to every earlier region), not a lattice sample; if a lattice is used anywhere, say it under-reports by up to one step and print the step. Two lanes got 1.00 vs 0.75 at 220×10 from the same area (17.25 px²) — the difference is the measure, and the floor comparison sits on it.
3. Fix the ramp-off cell: 220×22 under C48-1a's ramp is corner 8.27 → **133.88 px², r 4.75** (plan prints 138.9 / 5.0, which is corner 8 flat). State that the instrument applies the ramp inside 20 < min(w,h) < 80, and re-check every RUN-P row whose subject sits in that interval.

## Q3 — §3.12 clause 3 is FALSIFIED by C48-1, not strengthened (F-2) — **LEAD RULING**

A strip's geometric centre lies ON its edge line, which the perpendicular bands (tested first, higher z under D48-8) own: at 220×10 `e`/`w` centres resolve to `n`; at 100×1 to `ne`/`nw`/`n`; at 1×1 everything resolves to `nw`. G48-5's clause-3 row is RED by construction on `1×100`, `100×1`, `1×1` and the owner's own 220×10. **Ruling:** clause 3 is re-keyed to a WITNESS point the handle owns — a point returned by `resolveHandleAt` for that handle (e.g. the centre of its largest inscribed disc, which Q2 already computes) — and the disposition row says "changes shape", not "strengthens". State the witness rule in C48-1 so both oracles derive the same point.

## Q4 — The lab repoint joins the one commit (F-3) — **LEAD RULING**

`tsconfig.json` includes `src/**`, `pnpm typecheck` runs `tsc --noEmit` at the root, and the lab imports the symbols §3.10 deletes (`policies.ts` imports `admitHandles`; `handle-lab.tsx` imports `HANDLE_ADMISSION_ORDER`, `HANDLE_HIT_PX`, `STRIP_EDGE_COVERAGE_MIN`, `STRIP_HIT_BAND_PX`; `order-walk.ts` imports the module). S48-1's done-when "typecheck green" is unsatisfiable with S48-4 landing after. The same coupling argument D48-4 makes for S48-2 applies. **Ruling:** the lab repoint/deletion (`order-walk.ts` delete, `policies.ts` repoint, `handle-lab.tsx` / `candidate-lab.tsx` / `policy-lab.tsx` edits) moves INTO the code commit; S48-4 keeps only the artifact check, `pnpm gates`, `pnpm test:e2e` and the `descvi:dev` smoke. Update §3.4, §3.6, §4 and the done-when lists consistently.

## Q5 — D48-8's z values must be DERIVED from `stripOrder`, not written a second time (F-5) — **LEAD RULING**

Five z constants in `use-resize-handles.ts` beside `DEFAULT_HANDLE_GEOMETRY.stripOrder` is a fourth implementation of the order, and no gate binds them (G48-4a is two files, G48-4b is pure, G48-5's centres are not order-discriminating). **Ruling — fix the class, not the instance:** the renderer computes each strip's z FROM the constants record (`z = base + (stripOrder.length − index)`, corners above, all above `SPACING_STRIP_Z`), so the order is written once. Add a unit row asserting z is strictly decreasing along `stripOrder` and strictly above `SPACING_STRIP_Z` (RED-when: reverse `stripOrder`, or raise `SPACING_STRIP_Z`). If you reject derivation, the fallback is a source-text gate binding the five constants to `stripOrder` — say why derivation lost.

## Q6 — `translateIntoRect` has THREE call sites and D48-7(iii) must say what moves (CA-1)

Lead verified: the corner path is a sandwich `translateIntoRect → pushOutOfArcs → translateIntoRect`, plus one strip-path call. §3.10 says "delete both" and "move `pushOutOfArcs`" — inconsistent for one path. **Must achieve:** state what the renderer-side rescue IS (the sandwich, or the arc push alone, or a new clamp written against the layer clip), and give each of the three call sites a disposition consistent with it.

## Q7 — G48-5's floor is a value per fixture, with a RED-when that reaches it (CA-2)

"Each with a stated floor" names a requirement, not a number; the row's own RED-when says clause 5 stays green. **Must achieve:** per inherited fixture (`1×100`, `100×1`, `23×100`, `100×23`, `1×1`, each flush variant, `1×1` at the rounded corner) either a floor value (inscribed radius under Q2's measure, computed) or an explicit *known-unreachable, by ruling* entry, and a RED-when that fires the floor leg (e.g. flip `bandPx` to 4 → the flush strip's inscribed radius drops below the floor).

## Q8 — U48-5's populations and its predicate (CA-3) — **LEAD RULING on definitions**

The shipped docblock uses two populations: **324/628 flush pairs (51.6 %)** and **373** = pairs a 10 px inward apron CROSSES (the "recovers 39 of 373" figure). The plan cites both without reconciling, and its rule "> 50 % of flush pairs losing drill-in ⇒ escalate" already trips under R42-D1's own reasoning if "crossed" = "loses drill-in". They are not the same thing: a flush child loses the 5 px of its border ring under the parent's straddling band, and keeps its interior — unless it is thin enough that nothing is left. **Ruling:** define *loses drill-in* as: with the parent selected (its eight regions present), the child's box minus every parent resize region has no inscribed disc of radius ≥ the Q2 floor; state the population as the 324 flush pairs; set the escalation threshold on THAT measure with its reason; and note the 373 as the crossed population, not the losing one.

## Q9 — Overclaims and voided legs (CA-5, CA-6, F-7)

- "Every RED-when in §5 is a field flip" is false for G48-4a, G48-5, G48-6b, G48-7. Scope it to G48-1/2/3/4b in C48-1d and §6 scenario 4.
- G48-4b's "plus the clipped fixtures" leg cannot go RED under D48-7(iii) — both sides are clip-blind. Drop it from G48-4b; the clipped fixtures live in G48-5's DOM rows.
- G48-3b's RED-when moves the gate's own input (the aim radius), not the product, and its title names paint while `chipPx` is not in the computation. RED-when becomes a `cornerWidePx`/`cornerNarrowPx` flip; rename the row to what it measures.

## Q10 — Gates without a home, and a constraint hiding in a footnote (F-9, F-10, F-8)

- G48-6a's only harness is the lab's `spacing-overlap.ts`, which `packages/**` cannot import. `vitest.config.app.ts` runs `src/**/*.test.ts` in `pnpm gates` (lead verified via `vitest.workspace.ts`) and the extractor ignores `.test.ts` siblings, so a `src/app/sandbox/handle-lab/*.test.ts` file is a valid gate home at zero census cost. Name the file and the story that lands it — the same home serves G48-1/2/3 if they need lab helpers, though C48-1d's export should make them package-side; say which rows live where.
- `bandPx > cornerNarrowPx` is what keeps all eight non-empty at a 10 px short side (band 8 → lowest all-eight short side 9). Promote it from an ADR footnote to a contract clause with a unit row (RED-when: `bandPx` = 8), so the designer's 8-vs-10 call cannot silently falsify criterion 1.
- The e2e's DERIVATION is never corpus-compared (only its constants, via G48-4a). Its region derivation is pure; add a node-side leg that runs it over G48-4b's lattice against `handleRegions` — or state explicitly that the e2e's ~13 fixtures are accepted fixture-coincidence and why.

## Q11 — Smaller corrections (CA-7, CA-8, CA-9, CA-12, F-11)

- §3.11 sits inside §4; §3.4 cites §3.10 where it means §3.11. Fix the order and the reference.
- §3.2 clause 2 routes to G48-5, whose Asserts cell names clauses 3, 4, 5 only. Give clause 2 its row or fold it explicitly.
- G48-1's stated mechanism: the killer is `bandPx ≤ corner` together with the corners meeting (corner 10 / band 12 → nothing empty; corner 8 / band 2 → nothing empty). Say `band ≤ corner`.
- §3.9 rules the floor = 4; G48-1 defers it to U48-8. One register: the floor is RULED at 4 unless the owner moves it, and G48-1 asserts it now (RED at short side ≤ 17 under the ruled order — which is the owner's question made visible, not hidden).
- C48-4: the two layers share the parent `#dsh-ring-layer` (`z-40 … overflow-hidden`), which IS a stacking context and clips; the comparison works because both children live in that one context. Say so, and note that its `overflow-hidden` is what clips the band's outward half at the frame edge (D48-7's straight-edge numbers depend on it).

---

**Status line for REVISION 2:** name both round-2 lanes and their verdicts; say this text answers both and has not yet been read by any lane. Keep the provenance notes for every corrected number.
