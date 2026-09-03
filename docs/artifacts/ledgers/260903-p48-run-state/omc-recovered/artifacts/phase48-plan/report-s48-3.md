# S48-3 report (lead's condensed copy)

**Files:** `e2e/resize-handles.spec.ts` (13 rows on C48-1), NEW `e2e/handle-derivation.ts` (the e2e's own derivation + the hand-written constants record — REVERSAL: the record lives here, not in the spec, because the vitest file G48-4c cannot import a Playwright spec; the spec keeps `RAMP_ENDPOINT_NARROW_PX = 8` / `_WIDE_PX = 16` literals and G48-4a checks all three files), NEW `e2e/handle-derivation.test.ts` (G48-4c: 10/10, 13.9 s; leg (a) 14,400, leg (b) 472; 7 planted mutants fire), NEW `scripts/check-handle-constants.mjs` (G48-4a: 12 pairs / 3 files GREEN; `--selftest` 10/10 incl. non-dyadic respelling, absent anchor, missing file, ambiguous anchor; `bandPx 10→12` → RED), `.github/workflows/ci.yml` (two `run:` lines = gates steps 13 and 14), 6 anchor re-points.

**§3.11 retirements:** coverage rows (reason 1); HIT_EXTENT/ADMISSION_ORDER/place/deriveExpected/4b/4c (reason 1); 16–24 window → ramp window `|short − cornerSizeFor| ≤ 0.5`; `STRIP_BAND` 12 → 10 + a new straddle (inward-half) leg; centre-keyed → witness-keyed; identity/z/cursor rows kept.

**Browser gates:** `resize-handles.spec.ts --project=design-view` 13/13. G48-5 = 74 witness presses + 14 clause-2c presses (pinned counts; 32 unaskable slivers skipped at `HIT_SNAP_PX = 0.75` because Chromium's hit region is ~1 px wider than the reported rect). RED shown: G48-9 (forward strip append → `s` wins); G48-6b both legs (SPACING_STRIP_Z 41→44; `zIndex:1` on `#dsh-spacing-layer`); G48-5 clause 3 (centre re-key → fires at 220×10, which was ADDED as a fixture because the plan's RED-when named it while the fixture list lacked it).

**U48-11 measured (pure→rendered certified lower, per handle):** the renderer's clamp can REMOVE purchase — at `1×100` flush left, `nw` and `ne` are clamped onto the same rect and the later one owns nothing (`ne` 0.50 → 0.00); the "rescue only restores" assertion is withdrawn. Table in the full report / the spec's printed output.

**⚠ CROSS-STORY FINDINGS (routed to the fix round):**
1. **Corner-vs-corner DOM precedence is the REVERSE of `cornerOrder`** — corners are appended forward at shared z 43, so the LAST corner wins a shared pixel; at `1×100` the model says `nw`, the DOM returns `ne`. Pinned as `domPrecedence = [...cornerOrder].reverse(), ...stripOrder` in G48-5 pending the production fix.
2. `e2e/resize-handle-shield.spec.ts` — 10 rows RED (its settle predicate expects the E strip at `element.right`, i.e. wholly outward; one row asserts R42-D1 outright). Not in any §4 Lands column.
3. `e2e/resize-write.spec.ts` G42-6b DRAG-TO-CLAMP — RED: asserts handles are SHED as the box shrinks (`Expected < 8, Received 8`) — the degradation P48-1 deletes. Not in §4.
4. `e2e/spacing-gesture.spec.ts` G44-6 (PADDING) — RED: the padding drag produces NO write — the straddling band now owns the pixel the row presses. D48-5's priced consequence, live.
5. `e2e/fixtures/expected-identities.json` RED (13 UNEXPECTED / 11 MISSING from re-titled rows + the drift from 2–4) — deliberately NOT regenerated over real failures.

**Full `pnpm test:e2e` (quiesced, twice):** 170 passed; 14 / 12 failed (the 2-row delta = spacing-gesture rows flipping failed↔skipped, the documented cascade); 12 did not run (solo project suppressed). All failures isolation-attributed to 2–4 plus the two standing held pins (`selection-consistency` (c) PROBE-ONLY, `undo-cross-screen` HELD DEFECT PIN). No KI-53 / G44-8 / unresolved-refresh flake observed.

**Smaller corrections:** `boundsViolations` short-axis chosen by compass (min(w,h) named a correct 1×10 band wrong); the `23×100` free floor's certified lower is 4.1875 (not on the grid) → the floor leg asserts the ruled 4, the two-sided leg keeps 4.19 with bracket + 0.005; both left-flush (T6) and top-flush (inherited) rows kept; `30×30` floor 4.656 cross-checked vs T10.

**Ports:** stale pid 5804 on :3000 killed (another checkout's vite); :3001/:7331 free before and after.
