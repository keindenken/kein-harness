# Fix round 4 — S48-5's closure findings (all prose/strengthening; no behaviour change)

Read `docs/prompt/worker-brief.md`; no git; restore by `cp`; assert each edit once. Tree: 294add7 + uncommitted S48-5. **Do not touch `src/app/sandbox/resize-flex-col/page.tsx`** (the owner's own smoke fixture, uncommitted, not ours).

## J1 — `e2e/resize-handles.spec.ts` (OWNER: S48-3 lane) — CG-1, CG-2, CG-8, CG-9, CG-10, CG-11, CG-13
- CG-1: clause 2's docblock — "(2a) a CORNER root is wholly inside — that is the whole job of the sandwich, and removing the clamp fires here" and "D48-7(iii) puts the rescue in the renderer…" → rewrite to the shipped scope (2a = outside by at most half its side, like 2b); the sandwich text goes to past tense with the (i) ruling and date.
- CG-2: the file docblock's reason 4 ("The renderer's corner SANDWICH … U48-11 measures it") → "rendered == derived is now an ASSERTION (U48-11) only a compositor can make".
- CG-8: retitle the U48-11 row to what it asserts (identity under D48-7 (i)) — this changes a golden title: regenerate via `pnpm test:e2e:update-identities` LAST and paste the traced diff (one rename, net 0).
- CG-9/CG-10: lift the `placement === "free"` fences on the rect-for-rect `rendered == derived` leg and on clause 4's anchor envelope and `boundsViolations`' corner legs — under (i) they hold at EVERY fixture; drive one RED (a 3 px corner translate in a `cp`-restored copy) and paste which rows fire now.
- CG-11: the ruling-skip label applies to `nw` at the rounded corner only (0.863 > HIT_SNAP_PX); the other three (0.500) are unaskable under the snap floor — label them so.
- CG-13: pin the unaskable count (42) as an assertion, not only a print.
Runs: scoped `resize-handles.spec.ts`; then the golden regeneration (full run) once; paste the summary. Ports are free (the lead's server is down).

## J2 — docblocks (OWNER: S48-1 lane) — CG-6, CG-15
- `docs/architecture.md` and `use-resize-handles.ts`: "consumed by the ORACLES alone" → "no caller at all; kept as the stated definition of the effective clip (plan §3.10)".
- `handle-geometry.ts`: `fitsInClip`'s note must not claim G48-5's containment leg is stated against it (that leg uses the spec's own `clipRectOvershoot`); say it is kept beside `buildEffectiveClip` as the pure predicate over that clip, with no caller.
Runs: citation gate, lint.

## J3 — plan + handoff (OWNER: the lead) — CG-3, CG-4, CG-5, CG-7, CG-16, CG-14 note
Decision table D48-7 → (i) with the withdrawal; §9 U48-11 pins 73/38 and "became a gate"; §3.7 preamble, §4 S48-1 done-when (S48-5 amendment), §5 G48-5's U48-11 sentence, §7 consequences → (i); handoff §1 (strike the clamp clause; state block includes S48-5); CG-14 note (the `git show 294add7` record dies if history is rewritten — do not squash phase-48).
