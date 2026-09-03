# Fresh unprimed review — round 4 (phase-48 plan, REVISION 3)

Read `docs/prompt/worker-brief.md` first; it binds you. Then `.omc/artifacts/phase48-plan/review-common.md` (what the phase is, the limits, the bar, the report format). You are READ-ONLY on the repo, including `.omc/spikes/`. Read-only probes are encouraged and expected.

**You are deliberately UNPRIMED.** You have not been given any previous round's findings and you must not go looking for them — every other file under `.omc/artifacts/phase48-plan/` except `review-common.md` and this file is off-limits. Read the CURRENT text of `.omc/plans/ralplan-phase-48-handle-admission.md` as a whole, as a fresh senior reviewer would, and find what such a reviewer would find — **including what prior rounds missed**. The plan's status line and §9 are history, never your scope.

The plan now cites a reference instrument at `.omc/spikes/phase48-model/`. Three things to do with it, in this order:

1. **Run it** — `node .omc/spikes/phase48-model/tables.mjs` (or whatever its README says) — and diff its output against every number in the plan. A number in the plan that the script does not print, or that it prints differently, is must-fix.
2. **Write your OWN implementation** of the model from the plan's contract clauses ALONE (C48-1a–f and the §2.0 rect table, the membership convention, `cornerOrder`/`stripOrder`), then compare it with `model.mjs` on the plan's fixtures. Where they disagree, either the contract admits two readings (say which produce which numbers) or the reference model departs from the contract — both are must-fix.
3. Only then read the plan's numbers as claims.

Also point your instruments at: every gate `G48-n` (is its RED-when reachable by a named fixture; is it in `pnpm gates` via a `run:` step under `verify` in `.github/workflows/ci.yml`, or in `pnpm test:e2e`; does it have a home file a story lands); the story ladder against `tsconfig.json` (`src/**` included) and `package.json`'s `typecheck` (root `tsc --noEmit` plus per-package); the DOM path (`use-resize-handles.ts`, `OverlayShell.tsx`, the z ladder across `spacing-affordance-geometry.ts`, `reorder-paint.ts`, `use-spacing-drag.ts`); and every owner question in §9 (is it stated on arithmetic you reproduced, and are the levers offered the real ones).

Report per `review-common.md` format, findings prefixed `J-n`, must-fix separated from worth-considering, each with what you did to check it. Verdict line first: `APPROVE` or `REVISE`; a conditional approve is REVISE.
