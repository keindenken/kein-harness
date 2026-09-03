# Planner brief — phase-48 (B-Q5): replace the resize-handle admission model

Read `docs/prompt/worker-brief.md` first and obey it: you own this brief and nothing else; no git; no spawning anything that writes or reviews; report reversals loudly; anchor by content, never by line number.

## Your deliverable

ONE file: `.omc/plans/ralplan-phase-48-handle-admission.md` — a RALPLAN-DR consensus-planning draft, **round 0, status "DRAFT — NOT REVIEWED, NOT APPROVED"**. English. It will be reviewed by an architect lane (which probes behaviour) and a critic lane (which attacks structure and falsifiability) IN PARALLEL on your text, so write it for a reader who has none of this brief in context. Your final message to the lead is a ≤40-line summary: the decisions you took, every place you disagreed with this brief (loudly), and every ⚠ UNVERIFIED fact the plan leans on.

Format reference: `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` §0 (RALPLAN-DR summary: 3–5 principles, decision drivers, real decisions with ≥2 options each and why the loser lost), its evidence labels (**READ** / **RUN-P** / **INHERITED** / **⚠ UNVERIFIED**), its per-story gate table with a **RED-when** per gate, and its ADR section. Do not copy its content; copy its discipline. Every contract, decision, gate and story gets a numbered id (`C48-n`, `D48-n`, `G48-n`, `S48-n`) so a per-commit brief can cite it verbatim.

**Planning does not mutate source.** Do not edit anything under `packages/`, `src/`, `e2e/`, `docs/`. You MAY run read-only probes (node scripts in the scratchpad, `pnpm vitest run <file>`, `node --experimental-strip-types` against copies placed OUTSIDE the repo). Do NOT start or kill any dev server: `:3000` (pid 5804, `pnpm dev`) belongs to a prior lane, `:3001`/`:7331` may belong to the owner's own `descvi:dev`. Do NOT run `pnpm gates` or `pnpm test:e2e`.

Run `node scripts/check-citation-anchors.mjs` before you finish — `.omc/plans` is in its scan roots — and paste the result. A `file.ts:NNN` pin is banned in every spelling; write `` `path#<exact unique source text>` ``.

## The one-line scope

Phase-48 was inherited as "tune the constants of the admission rule". The measurement spike (this branch, commits `5f7ebef..f411977`) turned it into **"replace the admission model"**: the E/W strips vanishing below ~39 px is an artefact of the shipped admission MODEL (pairwise 20 px hit-centre separation + corner-first walk), not a property of small elements. Closed-form boundary: `hypot(w/2, 6) < 20 → w < 38.16`.

## The owner's spec (DECIDED 2026-09-01, tentative pending real use) — the plan implements THIS

Verbatim from the owner: 「좁음 20 이하 + 꼭짓점 8 / 넓음 80 + 꼭짓점 16 / 걸침, 경사를 몰고 가는 쪽 = 짧은쪽, 변 띠 두께 10」.

Structure = excalidraw-desktop's (read from source at `e1bb9ff8`, transcribed in `src/app/sandbox/handle-lab/policies.ts#export function cornerFirstBandRegions`): four corner hit squares CENTRED on the box vertices, tested first; then one band per side running the WHOLE edge; **no size predicate anywhere**, no pairwise separation clause, no admission walk — all eight regions always exist and a region that is entirely eaten by corners simply never wins a hit test. descvi's own numbers on that structure:
- corner hit square side = linear ramp on `min(w, h)`: `≤20 → 8 px`, `≥80 → 16 px`, clamped, linear between (`src/app/sandbox/handle-lab/candidate.ts#export function rampCornerAt`, `#export function effectiveCornerSize`, driver `'min'`).
- side band FULL thickness 10 px, **straddle** placement (centreline ON the edge, 5 in / 5 out) — `candidate.ts#export function bandCentreOffset`.
- The complete constants object: `src/app/sandbox/handle-lab/owner-spec.ts#export const OWNER_SPEC: CandidateConstants = {`.

Owner's two acceptance criteria, already made falsifiable in the lab (`owner-spec.ts`): **(1) narrow** — at short side 10 px (220×10) all eight handles are grabbable somewhere, and a press aimed at a vertex (aim disc radius = `POINTER_DRAG_THRESHOLD_PX` = 4) lands on the DIAGONAL handle ≥ 80 % of the time; **(2) wide** — at 100×100 the same diagonal share ≥ 80 %. Measured at the owner's numbers: PASS — 220×10 all eight (E/W minimum width 46); diagonal share 100.0 % (788/788). Known RED configurations for these gates: corner 10 px at narrow fails criterion 1; corner 5 px gives 61.4 % diagonal share. Carry these RED configs into the gates — a gate that has not been shown RED has not been built.

**Explicitly OUT of scope (owner ruling):** the tied candidates (outside placement; excalidraw-style ㄱ/ㄴ bracket corners) — memo only, decided by real use; band 8-vs-10 — a designer's call, ship 10. Do not reopen either; record them as follow-ups in the ADR.

## What the lab measured that the plan must carry (all RUN-P in the lab; cite the research docs)

- Straddle vs outside against the SHIPPED spacing affordances (`packages/descvi/src/react/overlay/canvas/spacing-affordance-geometry.ts`, `placeSpacingAffordances`): padding-handle overlap with resize surfaces is 15.1 % today, **51.7 % under straddle**, 12.7 % under outside; the increase is entirely the band; gap strips 0.0 % on padded containers (`src/app/sandbox/handle-lab/spacing-overlap.ts`, research `.omc/research/phase48-bq5-corner-placement.md` and the B-Q5 backlog row at `f411977`). The owner chose straddle knowing this. The plan must therefore RULE how a straddling band and a padding handle resolve a shared pixel (z-order / hit priority / node identity) and gate it — this is a risk that needs a MECHANISM, not a sentence.
- Corner placement: centring the corner square on the vertex costs 0.000 px against the shipped `placeHandle` in the free regime (research `phase48-bq5-corner-placement.md`). `translateIntoRect` fires only in the CLIPPED regime — the plan must say what the new model does under `EffectiveClip` (frame edge, rounded frame corner) because ralplan-42 §3.12's clause "inside the EFFECTIVE clip" and its fixtures (1×100 flush, 1×1 at a rounded corner) survive the model change.
- Ramp safety: worst-case margin is at size 50 (the MIDDLE of the ramp), not at an endpoint; band 8 fails at sizes 1–9; straddle needs `band > corner` perpendicular extent for no-limit reach, outside needs `band > corner/2`.
- Prior art (`.omc/research/phase48-prior-art-small-element-policy.md`): none of moveable / interact.js / tldraw / excalidraw refuses a handle by pairwise separation; excalidraw desktop has NO size predicate and identical geometry at 220×15/20/40/120. This is the argument for deleting the separation clause rather than tuning it.

## Blast radius (READ by the lead from live source at f411977 — re-read every one yourself)

- `packages/descvi/src/react/overlay/canvas/handle-geometry.ts` — `HANDLE_ADMISSION_ORDER`, `HANDLE_HIT_PX = 20`, `STRIP_HIT_BAND_PX = 12`, `HANDLE_CHIP_PX = 10`, `STRIP_EDGE_COVERAGE_MIN = 0.9`, `hitSizeFor`, `placeHandle`, `translateIntoRect`, `fitsInClip`, `admitHandles`. The admission walk and the separation clause go; the ramp comes in. The `STRIP_HIT_BAND_PX` docblock records the R42-D1 ruling "band wholly OUTSIDE the border box" — straddle reverses R42-D1 and the plan must say so as a ruling with its reason.
- `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts` — the ONLY production caller of `admitHandles`; also paints `chip.style.width = ${HANDLE_CHIP_PX}px`.
- `packages/descvi/src/react/overlay/__tests__/handle-geometry.test.ts` — a THIRD implementation of the admission rule that already disagrees with `admitHandles` on 2,421 / 14,400 free-regime subjects at shipped constants (measured in `.omc/research/phase46-bq5-admission-measurement.md`). It re-derives the clause being deleted; it must be REWRITTEN as a new oracle, not patched. Deleting tests needs one of the two `AGENTS.md` reasons named in the commit.
- `packages/descvi/src/react/overlay/__tests__/resize-handle-layer.test.tsx` — chip literals `"10px"`.
- `e2e/resize-handles.spec.ts` — hand-copied `const HIT_EXTENT = 20;` / `const STRIP_BAND = 12;` (a FOURTH implementation) plus ~45 bare `file.tsx:NNN` pins. It imports only `@playwright/test`. **Owner's note for planning: "planning에서 e2e는 확인 안 할 가능성이 높으니 크게 고려하지 않아도 될듯"** — the e2e rewrite is a real story with real gates, but do NOT spend the plan's depth re-deriving Playwright mechanics; state the contract (constants come from ONE place, pins become anchors), size the story, and leave the mechanics to execution with an explicit ⚠ UNVERIFIED label.
- `spacing-affordance-geometry.ts` does NOT import handle constants (docblock cross-references only; own `GAP_STRIP_HIT_BAND_PX = 16`) — so the straddle interaction is a runtime hit-priority question, not a constant-sharing one.
- The lab `src/app/sandbox/handle-lab/**` is OUT of deliverable scope (`src/app/**`) and must keep compiling and running after the change (`order-walk.ts#export function walkMatchesShipped` is a live RED check against `admitHandles` — when `admitHandles` is deleted the lab's §1–5 either retire or repoint; decide and say which). Never edit `page.tsx`/`spec.ts` there (re-pins ~66 census assertions).

## Decisions the plan MUST present with options (real decisions, not rubber stamps)

1. **Chip paint vs ramp hit.** `HANDLE_CHIP_PX = 10` paint; the owner ruled the 10×10 chip right on 2026-08-27. Under the ramp the narrow corner HIT is 8 px < paint 10 px. Options at least: (a) ramp the chip with the hit; (b) floor the hit at 10 so hit ≥ paint always (then the owner's "8" is not shipped — say so plainly); (c) accept hit < paint at narrow sizes with a stated reason. Recommend one; the owner rules on approval.
2. **The constant-split reversal.** ralplan-42 §3.12 clause 1 and the `handle-geometry.ts` docblocks bind pairwise separation as an INVARIANT with five clauses; phase-46 planned a three-way split of `HANDLE_HIT_PX`. Under the new model the separation clause disappears, so the split is near-moot — but it is a written ruling and must be ARGUED closed, not silently dropped. Enumerate which of §3.12's five clauses survive (effective clip, root hits, anchor envelope, non-empty floor?) and which die, per clause.
3. **Where the admission-independent geometry lives.** One source of truth for the numbers (module constants in `handle-geometry.ts`) consumed by the unit oracle AND the e2e oracle, vs the status quo of four copies. State the mechanism, not the intent.
4. **Cutover shape.** Transitional (both models behind a flag, migrate fixtures, drop) vs single cut — `AGENTS.md`'s transitional-cutover rule is for artifact/grammar migrations; argue whether it applies here.
5. **Straddle × padding handles** — see above; hit-priority mechanism and its gate.

## Story shape the lead sized (challenge it if source says otherwise)

S48-0 rulings & doc sweep (reversal argument, chip ruling, R42-D1 reversal recorded, ralplan-42/46 cross-refs de-anchored); S48-1 port the `candidate.ts` structure into `handle-geometry.ts` + single caller; S48-2 unit oracle rewrite + the owner's two criteria as RED-able unit gates (RED configs known); S48-3 e2e constants + pins + bare-pin cleanup while the file is open; plus the artifact byte-identity check (`git diff --exit-code .descvi/screens.json`) and a `descvi:dev` smoke as the UI gate. Say which stories can land in parallel and which must not.

## Reading list (open every one before you write; cite what you re-read)

`docs/post-loop-backlog.md` B-Q5 row (search `| B-Q5 |`) · `docs/handoff/260831-phase-47-close.md` · `.omc/plans/ralplan-phase-42-resize-handles.md` §3.12 and its G42-6a/6b rows · `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` §8 (routing) and its "four instruments that measured nothing" note · `.omc/research/phase46-bq5-admission-measurement.md` · `.omc/research/phase48-*.md` (all four) · the lab files named above · `docs/architecture.md` (handle section) · `docs/known-issues.md` (KI-47, KI-53) · `AGENTS.md` verification gates.
