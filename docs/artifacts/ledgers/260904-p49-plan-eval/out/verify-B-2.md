# verify-B-2 — plan-B.md lines 259–517 against `base/`

## 1. Claims

| # | plan line | Claim | Verdict | Evidence |
|---|---|---|---|---|
| 1 | 264 | `packages/descvi/src/react/overlay/canvas/reorder-paint.ts` exists | TRUE | present |
| 2 | 264 | `docs/post-loop-backlog.md`, `.omc/specs/v3-layout-panel-visual-spec.md`, `docs/e3/tracker.md` exist | TRUE | all three present |
| 3 | 262, 276, 290, 308 | Backlog rows `reorder-indicator-look`, `selection-ring-treatment`, `spacing-affordance-mark`, `padding-glyph` exist | TRUE | `docs/post-loop-backlog.md` lines 176, 179, 178, 158 |
| 4 | 270, 375 | The short-item observation is on `/shop/member-list`'s 7-member row, contrasted with `/lab/tests/reorder-flow`'s vertical 5 | TRUE | `docs/post-loop-backlog.md:176` states exactly that |
| 5 | 278 | `use-selection-rings.ts` exists | TRUE | `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts` |
| 6 | 280, 284 | There is a *single* selected-ring style writer covering primary and pooled rings | TRUE | `use-selection-rings.ts:52` `applyRingStyle`, docblock at :46 "THE ONE RING STYLE WRITER — the primary's shipped static node and every pooled secondary go through this and nothing else"; two callers |
| 7 | 280, 284, 514 | A hover ring path exists in addition, at a different width from selection | TRUE | `use-selection-rings.ts:273` `1.5px`, vs `:60` `2.5px` for selection |
| 8 | 286 | KI-47 is a ring *colour*/theme-staleness defect, distinct from ring form | TRUE | `docs/known-issues.md:37` and `:428` — colour retained after theme toggle, `use-selection-rings.ts` + `use-resize-handles.ts` sniff `.dark` in a layout effect |
| 9 | 292 | Anchor `use-spacing-affordances.ts#  root.setAttribute(SPACING_GLYPH_HIDDEN_BELOW_ATTR, String(SPACING_GLYPH_PX));` present verbatim | TRUE | line 120 |
| 10 | 292 | Anchor `use-spacing-affordances.ts#        glyph.style.display = Math.min(rect.width, rect.height) >= SPACING_GLYPH_PX ? "block" : "none";` present verbatim | TRUE | line 300 |
| 11 | 292 | Anchors `e2e/spacing-gesture.spec.ts#is the conditional kind` and `#publishes its size term` present | TRUE | lines 714, 715 |
| 12 | 292 | Anchors `e2e/spacing-gesture.spec.ts#    expect(paintedArm.length, ` and `#    expect(hiddenArm.length, ` present | TRUE | lines 728, 729 |
| 13 | 292 | Anchor `e2e/spacing-gesture.spec.ts#    if (n.glyphKind !== "glyph-conditional") continue;` present | TRUE | line 170, inside `conditionalArmViolations` |
| 14 | 292 | Anchor `e2e/spacing-gesture.spec.ts#  // ── F10 — THE GLYPH's OWN ADMISSION RULE ──` present, and F10 is a per-root glyph-presence row | TRUE | line 835; the row asserts `row.present` per `[data-dsh-spacing]` node and pins `display` on a literal 8 (lines 861–864) |
| 15 | 292 | The conditional-arm checker's population filter has "four clean readings" | UNCHECKABLE | `conditionalArmViolations` is referenced at `e2e/spacing-gesture.spec.ts:167`, `:773` (comment) and `:797`; "four clean readings" is not a countable artefact in the tree as stated |
| 16 | 292 | Anchor `use-resize-handles.ts#the layer is a CHILD of` present | TRUE | line 49 |
| 17 | 292 | Anchor `OverlayShell.tsx#unaffected — it declares` present | TRUE | line 1069 |
| 18 | 292 | `e2e/resize-handles.spec.ts`, `e2e/spacing-gesture.spec.ts`, `packages/descvi/src/react/overlay/__tests__/resize-handle-layer.test.tsx` exist and carry G42-7 Universe B / G44-5 B2 / G46-2+G46-3 | TRUE | `resize-handles.spec.ts:1322`; `spacing-gesture.spec.ts:691` with the `(B2)` legs at :719–721; `resize-handle-layer.test.tsx:607`, `:608` |
| 19 | 294, 298 | The shipped declared-kind set is a closed set that `delegated-mark` is not yet in | TRUE | `use-resize-handles.ts:347` "closed three-value set — `glyph`, `glyph-conditional`, `cursor` — and no fourth without amending that clause" |
| 20 | 298, 419 | The spacing spec row asserts a four-class population present | TRUE | `e2e/spacing-gesture.spec.ts:723` `expect([...seen].sort()).toEqual(["gap/apron","gap/strip","pad/apron","pad/strip"])` |
| 21 | 304 | The `delegated-mark` revert takes the kind out of "all four closed sets" | FALSE | Five hand-written enumerations exist: `resize-handle-layer.test.tsx:473` (`DECLARED_KINDS`), `:623` (the message string `'is not one of glyph | glyph-conditional | cursor'`), `e2e/resize-handles.spec.ts:1419` and `:1442`, `e2e/spacing-gesture.spec.ts:712`. The plan's own lines 473 and 493 say "five" |
| 22 | 324, 326 | `use-reorder-drag.ts`, `use-canvas-selection-shield.ts`, `canvas-selection-shield-travel.test.tsx`, `e2e/multi-select-shield.spec.ts`, `pointer-thresholds.ts`, `e2e/reorder-drag.spec.ts` all exist | TRUE | all present under `packages/descvi/src/react/overlay/canvas/`, `__tests__/`, `e2e/` |
| 23 | 324 | `e2e/reorder-drag.spec.ts` has a row (g) | TRUE | line 589, `test('(g) at N > 1 the excluded drag SAYS SO …')` |
| 24 | 326, 384 | Anchor `use-reorder-drag.ts#    const machine = new ReorderDragMachine({` present | TRUE | line 607 |
| 25 | 326, 384 | Anchor `use-reorder-drag.ts#        if (Math.hypot(point.x - mute.x, point.y - mute.y) < POINTER_DRAG_THRESHOLD_PX) return;` present | TRUE | line 376 |
| 26 | 326, 384 | Anchor `use-canvas-selection-shield.ts#        maxTravelRef.current >= POINTER_DRAG_THRESHOLD_PX` present | TRUE | line 386 |
| 27 | 326, 475 | Reorder has exactly three threshold consumers across two files | TRUE | `use-reorder-drag.ts:376` and `:608`; `use-canvas-selection-shield.ts:386` are the only non-import uses in those two files |
| 28 | 330, 384 | The shared value is 4 px | TRUE | `packages/descvi/src/react/overlay/canvas/pointer-thresholds.ts:43` `export const POINTER_DRAG_THRESHOLD_PX = 4;` |
| 29 | 338 | An old-path reference survives in `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` | TRUE | line 11 cites `.omc/plans/ralplan-e3-v3-direct-manipulation.md` |
| 30 | 341 | `DEFAULT_HANDLE_GEOMETRY` exists and `scripts/check-handle-constants.mjs` supports `--selftest` | TRUE | `handle-geometry.ts:189`; `check-handle-constants.mjs:30`, `:201` |
| 31 | 342, 476 | The CI `verify` job already runs `--selftest` + run as two steps for the citation-anchor and handle-constant gates | TRUE | `.github/workflows/ci.yml:216–219` and `:231–234` |
| 32 | 476 | `check-v3-registers.mjs` is "the one audit gate in that job whose RED nothing in CI ever exercises" | PARTLY | It has no `--selftest` (true), but it is not unique: `scripts/check-ki-register.mjs`, run at `.github/workflows/ci.yml:170` in the same job, also has no selftest and no test anywhere referencing it (only a prose mention inside `check-v3-registers.mjs:4`). `check-extract-outcome.mjs` does have a RED test (`packages/descvi/test/gate/extract-outcome-red.test.ts`) |
| 33 | 344 | `.descvi/screens.json` exists | TRUE | present |
| 34 | 347 | `scripts/check-citation-anchors.mjs` scan roots include `.omc/plans` and exclude `.omc/archive`; the gate excludes `.md` and nothing else | TRUE | `:121` `SCAN_ROOTS = ['docs', …, '.omc/plans', '.omc/specs', '.omc/research']`; `:622` `if (citedPath.endsWith('.md')) continue;` |
| 35 | 347 | The two move targets carry 136 + 32 = 168 code anchors, the extra one over an extension filter being a `.json#` anchor into `e2e/fixtures/expected-identities.json` in the v3 parent plan | TRUE | Re-counted: `ralplan-phase-42-resize-handles.md` 136; `ralplan-e3-v3-direct-manipulation.md` 32 (31 by a `.ts|.tsx|.mjs|.mts` filter); the `.json` anchor is at `ralplan-e3-v3-direct-manipulation.md:891` — `e2e/fixtures/expected-identities.json#  "distribution": {` |
| 36 | 356, 358 | `.omc/archive/260817-e3-v3/` does not exist; `.omc/archive/260901-e3-v3/` does | TRUE | `ls -d .omc/archive/*/` lists `260817-e3-v3-consensus/` and `260901-e3-v3/`, no `260817-e3-v3/` |
| 37 | 356 | `.omc/archive/README.md` has no row for `260901-e3-v3/` | TRUE | the README's folder rows omit exactly `260819-phase-43-consensus/` and `260901-e3-v3/` |
| 38 | 375 | Routes `/shop/order-detail`, `/shop/member-list`, `/lab/tests/reorder-flow` exist | TRUE | `src/app/shop/order-detail/page.tsx`, `src/app/shop/member-list/page.tsx`, `src/app/lab/tests/reorder-flow/page.tsx` |
| 39 | 375 | The `reorder-paint.ts` docblock names `4jpxin` as the case-(b) overlap subject, while its markup is `flex-1` siblings with no gap class and no negative margin | TRUE | `reorder-paint.ts:103`; `src/app/shop/order-detail/page.tsx:197` `className="relative flex flex-col flex-1 items-center"` inside `:192` `className="flex items-start p-[5px]"` |
| 40 | 375 | The thickness clamp is taken on the ABSOLUTE separation, so it reaches zero at contact and nowhere else | TRUE | `reorder-paint.ts:141` `const gap = Math.abs(anchorEdge - neighbourEdge);`, `:142` `Math.max(0, Math.min(REORDER_INDICATOR_THICKNESS_PX, gap))` — at overlap the band is non-zero, contradicting the docblock's "collapses to the boundary midpoint" at `:103` |
| 41 | 375, 377 | The only exact-touch oracle is the unit-level `contiguous` fixture, which asserts the band overlaps neither member; there is no overlap oracle in the repository | TRUE | `packages/descvi/test/reorder/reorder-paint-geometry.test.ts:90–104` ("A GAPLESS PAIR collapses the band … case (a)"); no case-(b)/overlapping-pair row anywhere in that file or in `e2e/reorder-drag.spec.ts` |
| 42 | 393 | G42-7 Universe B and G46-2/G46-3 build their scene from `e2e/resize-handles.spec.ts#async function setFixture(` on the `style-edit` card | TRUE | `setFixture` at `:559`; `SUBJECT_OID = "v002k2"` at `:93–94`; both tests call it (`:1325`, `:1420`) |
| 43 | 393 | G42-7's two population assertions count `handle` and `other`, and neither row reports a spacing node | TRUE | `e2e/resize-handles.spec.ts:1330` `family === "handle" … toBe(8)`, `:1332` `family === "other" … toEqual([])` |
| 44 | 393 | The fixture zeroes padding, and the subject carries a 12 px flex gap | TRUE | `setFixture` writes `padding: "0px"` (`:568`); `src/app/lab/tests/style-edit/page.tsx:36` `className="flex items-center gap-3 …"` (gap-3 = 12 px) |
| 45 | 395 | The G48-6b anchor and `#    const spacingPresent = scene.operable.some((node) => node.family === "spacing");` are present, and the latter sits inside that row | TRUE | test at `:1249`, assertion source at `:1318`, before the next test at `:1322` |
| 46 | 515 | The kickoff records the owner's direction as one `-` mark per edge instead of two icons | TRUE | `docs/handoff/260903-phase-49-kickoff.md:34`; backlog `:178` clause (b) says the same, with the Figma figure 12–13 px × 2 px, 1 px outline |

## 2. Totals

- TRUE: 43
- PARTLY: 1
- FALSE: 1
- UNCHECKABLE: 1

## 3. The three most damaging FALSE/PARTLY claims

1. **#21 (plan-B.md:304) — "all four closed sets."** The revert unit for `delegated-mark` is specified by count, and the count is one short of the five hand-written enumerations the tree actually carries (`resize-handle-layer.test.tsx:473` and `:623`, `e2e/resize-handles.spec.ts:1419` and `:1442`, `e2e/spacing-gesture.spec.ts:712`); an executor reverting "four" leaves a live enumeration behind, which is precisely the terminal-uninhabited-member hazard the story exists to close.
2. **#32 (plan-B.md:476) — `check-v3-registers.mjs` as "the one audit gate whose RED nothing in CI ever exercises."** It is not unique — `scripts/check-ki-register.mjs` (`.github/workflows/ci.yml:170`) is in the same state — so a reader who trusts the singular treats a known coverage hole as already enumerated and closed.
3. **#15 (plan-B.md:292) — the "four clean readings" of the conditional-arm population filter.** The number is stated as a fact about the tree that S49-4 must re-scope to plant-only, but nothing in `e2e/spacing-gesture.spec.ts` presents four such readings to count; an executor re-scoping by that number has no way to know when the re-scope is complete.
