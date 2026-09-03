# Architect lane — round 1 (phase-48)

Read `.omc/artifacts/phase48-plan/review-common.md` first; it is part of this brief.

**Your instrument is behaviour, not reading.** You review by PROBING: run the shipped module, run the lab's candidate model, diff what the plan asserts against what the code does. A finding that comes from reading only is worth-considering; a finding that comes from a run is must-fix if it breaks a gate or a contract.

Deliverables the lead requires from you, each with the evidence that produced it:

1. **The strongest steelman AGAINST the favoured design** (excalidraw-desktop structure + ramp on `min` + straddle 10). Not a strawman: the best argument a senior interaction engineer would make, with the measurement that would settle it if one exists in the repo.
2. **At least one unresolved tradeoff tension** the plan does not resolve, stated as a tension (two goods that pull apart), with the option the plan should at least name.
3. **A synthesis path** where one exists.
4. **Every principle violation** flagged explicitly — the plan's own principles AND `AGENTS.md`'s.

Probe targets you must actually run (paste commands and numbers):
- **The straddle × padding-handle collision.** The plan must state a hit-priority MECHANISM for a pixel shared by a straddling resize band and a padding handle from `packages/descvi/src/react/overlay/canvas/spacing-affordance-geometry.ts` / its DOM in `use-resize-handles.ts` and wherever the spacing layer mounts. Find the actual DOM stacking / pointer-event path (z-index, layer order, `pointer-events`, `elementFromPoint` usage) from source and say whether the plan's mechanism matches what runs. The lab's overlap number (51.7 % under straddle) is in `src/app/sandbox/handle-lab/spacing-overlap.ts` — re-run or re-derive it, do not quote it.
- **The clipped regime.** `handle-geometry.ts#export function placeHandle` / `translateIntoRect` / `fitsInClip` / `buildEffectiveClip`: what does the plan say a vertex-centred 8–16 px corner square does at a frame edge and at a rounded frame corner, and does the shipped clip machinery still apply? Run the ralplan-42 §3.12 fixtures (1×100 flush, 100×1 flush, 1×1 at a rounded frame corner) through the candidate model — copy `candidate.ts`/`policies.ts`/`handle-geometry.ts` OUTSIDE the repo with `.ts` import suffixes and run via `node --experimental-strip-types`, as the prior lanes did in `/tmp/hlprobe/` (re-copy from f411977; do not trust a stale copy).
- **The owner's two criteria as gates.** `src/app/sandbox/handle-lab/owner-spec.ts#export function checkEightReachable` and `#export function checkCornerAim`: confirm the plan's gate statements reproduce the lab's PASS at the owner's numbers AND go RED at the stated RED configs (corner 10 at narrow; corner 5 → 61.4 %). If the plan's gate is phrased so it cannot reach either RED config, that is must-fix.
- **The chip decision (D48 chip paint vs ramp hit).** `HANDLE_CHIP_PX = 10` paint vs 8 px hit at narrow. Check what `use-resize-handles.ts` actually does with the chip node vs the hit node (are they the same element? does the chip receive pointer events?). The decision's options are only real if the DOM allows them.
- **The unit oracle.** `packages/descvi/src/react/overlay/__tests__/handle-geometry.test.ts` — confirm from source that it re-implements the admission rule (so the plan's "rewrite, don't patch" has a true reason), and check the plan's stated deletion reason against `AGENTS.md`'s two allowed reasons.

Report per `review-common.md`. Prefix findings `A-n`. Model spend: do not escalate.
