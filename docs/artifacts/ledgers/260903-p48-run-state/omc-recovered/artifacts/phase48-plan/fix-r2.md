# Fix round 2 — consolidated from the verification round (architect VA-n, critic VC-n) + the owner's rulings

Read `docs/prompt/worker-brief.md`; it binds you (no git; restore by `cp`; assert each edit applied once; report reversals loudly). The tree carries the whole uncommitted code commit. Each item names its OWNER; touch only your items' files; run only your own files' tests (no full runs — the lead runs the final gates over a quiesced tree).

## G1 — Re-impose pass: no detach under a live gesture (OWNER: S48-1 lane) — VA-2, VC-5

`use-resize-handles.ts#    if (beforeCount !== wanted.size) {`: the body re-appends every surviving node (`appendChild` on an attached node = detach + reattach, which releases pointer capture), and the claim "no gesture can be in flight" is not established — `axes` is re-derived per pass and `placeFurniture` is the per-pointermove pass. **Must achieve:** the re-impose runs only when no drag / pointer capture is in flight (gate it on the hook's existing drag-in-flight state or lease; if a gesture is live, defer to the next idle pass); replace the size proxy `beforeCount !== wanted.size` with a real "set or order changed" test (compare the current child order with the wanted order) or record the trace VC-5 made in a comment; and re-run `pnpm typecheck`. Report the exact lines.

## G2 — Unit oracle: U48-8 (a) applied, and the DOM-order row (OWNER: S48-2 lane) — owner ruling, VA-3, VA-4

- **U48-8 → (a), owner-ruled 2026-09-02:** below short side 18 criterion 1 is an EXISTENCE claim. Retire the ten `it.fails` rows; the `describe` becomes `G48-1 / U48-8 (a) — h ∈ 8..17: existence + pinned T5 intervals (owner-ruled 2026-09-02, provisional on the live pass)`, keeping the two normal rows (T5 `[lower, upper]` pinned; all eight own something). The floor leg stays over `h ∈ 18..22`. Run the file: it must be green with no `it.fails` left; show the T5 pin still fires on a value drift (a `bandPx` flip).
- **VA-3 — a jsdom row asserting DOM append order** in `resize-handle-layer.test.tsx`: children of the handle host in document order equal `["se","sw","ne","nw","w","s","e","n"]` (reverse `cornerOrder` then reverse `stripOrder`) on a both-axes subject; and, exercising G1's pass, after a writability flip that removes and re-adds a strip the order is restored. RED-when: drop either `.reverse()` in production (drive it on a `cp`-restored copy and paste). This is the package-side gate F1 lacked.

## G3 — e2e bookkeeping and corpus (OWNER: S48-3 lane) — VC-1, VC-3, VC-4, VC-2

- **VC-1 (must):** `e2e/resize-handles.spec.ts`'s retirement docblock gains the line for `acceptance 4c — small AND flush`: *rewritten into G48-5's clause 2/3 (containment → 2a/2b/2c against the effective clip, `hitIsSelf` → witness presses), all three fixtures kept* — so the commit body enumerates every deleted row.
- **VC-3 / VC-4:** add `220×10` and `220×8` to `FIXTURE_SIZES` in `e2e/handle-derivation.test.ts` (and mirror in S48-2's `LEG_B_FIXTURES` if the two lists are meant to match — say whether they are); name the distinct sizes so the corpus-count pin is honest (`expect(corpus.length).toBe(N)` with N derived, not padded). Re-run the file.
- **VC-2:** one sentence in `e2e/handle-derivation.ts`'s docblock: the interval leg shares the certified-sweep ALGORITHM with production (regions and emptiness are independent; the sweep is not), so a sweep defect is caught by G48-5's DOM presses, not by G48-4c.

## G4 — Plan (OWNER: the lead)

§5 G48-4b's RED-when: the constants flip must be applied to ONE derivation (VA-5); §3.3/§5 note VC-2's coverage boundary. Already applied: U48-1/2/8 rulings.

## After the fixes (lead)

Quiesce (no lane writing; `git status` + mtimes stable), publish an md5 census, run `pnpm gates` and `pnpm test:e2e` ONCE each, then a closure audit on G1–G3, then the commit.
