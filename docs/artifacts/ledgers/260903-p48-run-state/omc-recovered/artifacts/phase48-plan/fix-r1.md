# Fix round 1 — the code commit (S48-1 + S48-2 + S48-3), consolidated from S48-3's cross-story findings

Read `docs/prompt/worker-brief.md`; it binds you (no git; restore by `cp`, never `git checkout --`; assert every edit applied once; report reversals loudly). The tree carries all three stories uncommitted. Each item names its OWNER; touch only your items' files.

## F1 — Corner-vs-corner DOM precedence must equal `cornerOrder` (OWNER: S48-1 lane) — **LEAD RULING**

S48-3 measured: corners are appended FORWARD at shared z 43, so the last corner wins a shared pixel (`1×100`: model says `nw`, DOM returns `ne`). The same principle that made strips reverse-append applies: **append corner roots in REVERSE `cornerOrder`** so `cornerOrder[0]` paints last and wins. Also confirm the re-impose pass (your unasked addition) re-orders corners the same way, or scope it to strips and say why. Report the exact lines. `pnpm typecheck` + your port-conformance probe again; do not run e2e.

## F2 — `e2e/resize-handle-shield.spec.ts` (OWNER: S48-3 lane)

10 rows RED: the settle predicate expects the E strip at `element.right` (wholly outward) and one row asserts R42-D1 outright. Rewrite onto C48-1/C48-3: the band straddles (centreline on the edge, 5 in / 5 out), so the settle predicate reads `element.right − bandPx/2` (or, better, derives the expected rect from `e2e/handle-derivation.ts`); the R42-D1 row becomes its C48-3 successor (the band's inward half exists; the shield's purpose — whatever it protected — is re-stated against the straddling geometry, or retired with §3.11 reason 1 if its subject was the outward-only apron). Every deleted row carries an AGENTS.md reason.

## F3 — `e2e/resize-write.spec.ts` G42-6b DRAG-TO-CLAMP (OWNER: S48-3 lane)

RED: asserts handles are SHED as the box shrinks. Under P48-1 nothing is shed. Rewrite the row to what C48-1 promises during the same gesture: all eight roots present at every intermediate size down to the 1 px floor, the gesture completable, and (new, cheap) the corner size following `cornerSizeFor` as the box crosses 80 → 20. Keep the drag mechanics; only the expectation changes. Reason for the removed assertion: reason 1.

## F4 — `e2e/spacing-gesture.spec.ts` G44-6 (PADDING) (OWNER: S48-3 lane) — **LEAD RULING**

RED: the padding drag produces no write because the straddling resize band now owns the pixel the row presses — D48-5's priced consequence landing live. Ruling: the affordance still EXISTS (§2.8: 72.6 % of the pad strip is resize-owned at 100×100 pad 8, so 27 % is not); **re-key the row's press point to the padding strip's OWNED residual** — compute it in the spec from the two geometries (the pad strip rect minus production's resize regions; press the residual's witness / centre), and assert the write lands. Add ONE line to the row's docblock recording that the pre-48 press point is now resize-owned by the suppression rule (§3.5), so the next reader knows why it moved. If the residual is EMPTY for the fixture the row uses, do not fake a press: report it as the live answer to U48-4 and leave the row RED with that reason in its title — the owner must see it (G48-8's padding drag).

## F5 — Golden identities (OWNER: S48-3 lane, LAST)

After F2–F4 and F1 have landed and `npx playwright test` on the four resize/spacing specs is green: regenerate `e2e/fixtures/expected-identities.json` via `pnpm test:e2e:update-identities`, then paste the golden's diff summary (which titles were added/removed and why — each must trace to a row you rewrote or retired). Then the full `pnpm test:e2e` once over a quiesced tree; name every remaining failure against the held pins (`selection-consistency` (c) PROBE-ONLY, `undo-cross-screen` HELD DEFECT PIN) or as NEW.

## F6 — Your G48-5 `domPrecedence` pin (OWNER: S48-3 lane, after F1)

Flip `[...cornerOrder].reverse()` back to `[...cornerOrder, ...stripOrder]` once F1 lands (coordinate: the lead will tell you when S48-1 reports), and show the pin goes RED against the pre-F1 order (a note in the report is enough if you ran it before F1 landed).

## Plan write-backs (OWNER: the lead) — do not touch the plan

§4 Lands columns gain the three e2e files; §3.5/§2.8 record G44-6's live consequence; C48-1c gains the corner reverse-append; U48-11's table.
