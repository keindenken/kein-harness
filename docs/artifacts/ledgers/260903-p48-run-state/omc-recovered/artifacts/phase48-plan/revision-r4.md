# Revision brief — round 4 → round 5 (phase-48 plan)

Round 4 ran a PRIMED closure audit (`CC-n`) against `revision-r3.md` and a FRESH unprimed reviewer (`J-n`) on REVISION 3. Both REVISE. Both ran `tables.mjs` (byte-identical to the embedded block, 165/165), both wrote independent implementations from the contract clauses and reproduced the model, and both verified the 0.46 → 4.18 px² correction from source. **The model is right; the findings are now about the instrument's convergence, gate placement, one false reason, one unstated coupling, and one scheduling error.** Z-closure: Z2, Z3, Z5, Z6, Z8 CLOSED; Z1, Z4, Z7 PARTIAL. Produce **REVISION 4** in place plus the spike changes; same limits (`.omc/spikes/` is yours). Paste the citation gate and the `tables.mjs` diff statement into the status block.

---

## Y1 — The purchase/witness instrument becomes CERTIFIED and DETERMINISTIC (J-1, J-7, CC-5) — **LEAD RULING**

`witnessPointFor` is a seeded hill-climb; the fresh lane showed it reporting 2.119 where its own `clearanceAt` reaches 2.125 (band 16 at 220×10), six under-converged cases in a 504-case sweep (worst 0.029), while §5 asserts G48-1 at `1e-9` and the flush rows fire "upward" on a better re-implementation. A production export whose VALUE keys gates cannot be a search with no bound. **Ruling:**

- The measure stays the exact largest inscribed disc. The INSTRUMENT computes a **certified interval**: clearance is 1-Lipschitz, so on a square grid of step `h` over the owned region's bounding box, `lower = max grid clearance`, `upper = lower + h·√2/2`. `h` is a named constant in the constants record (pick it; 1/32 px gives ±0.022, 1/64 ±0.011). The witness is **the best grid point, ties broken by scan order (row-major, ascending)** — deterministic, so two independent implementations with the same `h` agree exactly, which is what lets the e2e re-derive it without importing (J-7) and G48-4b compare witnesses, not only regions.
- Every gate assertion on purchase uses the interval: G48-1 asserts `lower ≥ floor` (state that band 8's `4.000 − h·√2/2` is what actually gets compared, and what that means for C48-5's fence); the flush rows assert `|recorded − lower| ≤ h·√2/2 + ε`, RED-when in both directions stated.
- `selftest.mjs` gains a convergence case: a region whose exact disc is known in closed form (a single rect), asserting `lower ≤ exact ≤ upper`. Re-run every table; fix 2.119; re-sweep the corpus and print the max `upper − lower` beside T1/T4/T5.
- Drop "no lattice appears anywhere" (§2.7); say instead that every lattice in the plan is declared with its step and its bound (§2.8's `OVERLAP_STEP_PX = 1` included — declare it and its error, J-8).

## Y2 — The flush-pair measurement moves BEFORE the cut, and its escape is honest (J-6) — **LEAD RULING**

U48-5's instrument needs only `handleRegions` and the purchase measure — both exist in the spike today — plus the nested-pair corpus (a DOM read: the 628 `[data-oid]` pairs and their flush relation). S48-2 schedules it inside the irreversible commit and names an escape (`outside placement`) that §8 rules OUT. **Ruling:** the measurement is a S48-0 deliverable (pre-cut). If it can be run during planning from a static corpus (the extractor's artifact or a `pnpm dev` DOM dump — NOT a `descvi:dev` start), run it now and put the number in the plan; if it needs a live overlay, S48-0 runs it and the code commit does not start until it is recorded. The escape is **STOP AND REPORT TO THE OWNER** — the outside-placement candidate is the owner's memo, not the plan's lever; say exactly that.

## Y3 — Gate homes and the `run:` claim (J-5, CC-3) — **LEAD RULING**

- G48-4b (`__tests__/`) and G48-4c (`e2e/handle-derivation.test.ts` via `vitest.config.app.ts`) are vitest files reached by the EXISTING `pnpm test` / `pnpm -r --filter './packages/**' test` steps; they are not new `run:` lines and cannot carry `--selftest`. Only G48-4a (a `scripts/` file) is a new `run:` line with `--selftest`. Rewrite §3.3, §1's "four new gate legs", and S48-3's done-when accordingly; a vitest gate's control is a test case that plants the mutant and asserts the assertion fires.
- G48-9 names its fixture with `min(w,h) < 35` — 220×10 (36 px² of strip-shared, corner-free area; closure lane's probe) — and states the constructibility condition (`cornerSizeFor(box) < bandPx`) so the fixture cannot be swapped for a rounder subject on which the gate cannot go RED.

## Y4 — Reasons and couplings the owner reads (J-3, J-4, CC-7)

- §3.8/§3.9 "strip precedence: none". The MINIMUM over G48-1's aspect-symmetric corpus is order-invariant; the PER-FIXTURE value is not (`n,e,s,w`: 220×17 → 3.725, 17×220 → 4.000; `e,n,w,s` swaps them). State that reason; keep the conclusion (first short side meeting the floor at both aspects is 18 under every order — print that sweep in `tables.mjs`).
- The band lever tops out at exactly **4.000** because at narrow sizes the binding handle becomes `nw` with purchase `cornerNarrowPx / 2 = 4 = floor`. **No `bandPx` puts a narrow subject ABOVE the floor while `cornerNarrowPx` is 8.** State the coupling `cornerNarrowPx / 2 == POINTER_DRAG_THRESHOLD_PX` in U48-8 as the real content of the owner's question, with Y1's interval making the zero headroom explicit.
- "≤ 2.50 at any corner size" is over T4's seven-point sweep; either bound it analytically (the strip's owned region is within the outward half-band, width `bandPx/2`, so radius ≤ `bandPx/4`) or say "over T4's sweep".

## Y5 — Numbers and citations (CC-1, CC-2, J-2)

- `tables.mjs` prints the SHIPPED model's overlap row in the §2.8 block (baseline for 15.1 / 7.5-or-7.8 / 7.6) and every price sentence uses ONE baseline; fix `7.5` vs the block's `7.8`.
- `tables.mjs` prints the two G48-1 mechanism rows (corner 10 / band 12; corner 8 / band 2) or G48-1 drops the "T9 companion rows" pointer.
- Selftest case 3 does not go RED on the inequality mutation it names (the cut-point insertion is what fixed the tangent case); correct the `model.mjs` comment and the status block to blame the cut-point logic, and make case 3 a control that fires on removing the cut points — or name honestly what mutation it catches.

## Y6 — Gate contradictions and smaller items (CC-4, CC-6, CC-8, J-10, J-11, J-12)

- G48-5: clause 4's lever ("re-introduce a translate") also fires the flush clause-5 rows; scope the lever to free fixtures or qualify "5 stays green" to the free rows.
- C48-1e cites §3.3 for the writability filter; the filter is §2.2's `axes.width || axes.height` guard. Fix the reference and state that `model.mjs` assumes both axes writable.
- The two `39`s (E/W vanishing threshold vs R42-D1's recovered pairs) — disambiguate.
- §2.2's ladder omits `#dsh-selection-badge` (`z-[41]`) and `#dsh-selection-ring-pool` (no z); add them (both `pointer-events: none`, so the "no free integer between 43 and 44" argument stands).
- `scarcest` column under ties: define the tie-break (hit order) so no gate can key on the name ambiguously.
- G48-2: write the assertion as `=== 100 %` at every shipped fixture (RED-when: `cornerNarrowPx` flip), since `≥ 80 %` cannot fail inside the contract's domain; keep the 80 % floor as the owner's criterion text and say why the gate is stricter.

---

**Status line for REVISION 4:** name both round-4 lanes and verdicts; say the model was reproduced by two independent implementations and what changed in the instrument (Y1); say the flush-pair measurement moved before the cut (Y2). Round 5 runs a primed closure audit and a fresh unprimed reviewer; the lead intends round 5 to be the last text round unless it finds a new CLASS.
