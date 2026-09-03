# Fresh unprimed review — round 5 (phase-48 plan, REVISION 4)

Read `docs/prompt/worker-brief.md` first; it binds you. Then `.omc/artifacts/phase48-plan/review-common.md` (what the phase is, the limits, the bar, the report format). You are READ-ONLY on the repo, including `.omc/spikes/`. Read-only probes are encouraged and expected.

**You are deliberately UNPRIMED.** You have not been given any previous round's findings and you must not go looking for them — every other file under `.omc/artifacts/phase48-plan/` except `review-common.md` and this file is off-limits. Read the CURRENT text of `.omc/plans/ralplan-phase-48-handle-admission.md` as a whole, as a fresh senior reviewer would, and find what such a reviewer would find — **including what prior rounds missed**. The plan's status line and §9 are history, never your scope.

The plan cites a reference instrument at `.omc/spikes/phase48-model/`. In this order: (1) run `node .omc/spikes/phase48-model/tables.mjs` and `selftest.mjs`; diff the output against every number in the plan; (2) write your OWN implementation of the model from the contract clauses alone (C48-1a–g, the §2.0 rect table, the membership convention, `cornerOrder`/`stripOrder`, the purchase measure and its certified interval as the plan defines them) and compare with `model.mjs` on the plan's fixtures — disagreement means the contract admits two readings or the reference departs from it; (3) only then read the plan's numbers as claims.

Also point your instruments at: every gate `G48-n` (RED-when reachable by a NAMED fixture; home file; whether it runs under an existing `pnpm test` step or a new `run:` line in `.github/workflows/ci.yml`'s `verify` job, and whether the plan says which); the story ladder against `tsconfig.json` + `package.json`'s `typecheck`; what is scheduled BEFORE vs INSIDE the single code commit and whether anything decision-relevant sits inside it; the DOM path (`use-resize-handles.ts`, `OverlayShell.tsx`, the z ladder); and every owner question in §9 (arithmetic reproducible; levers real).

**Your verdict has weight this round:** the lead intends this to be the last text round unless you find a new CLASS of defect. Distinguish clearly between must-fix (the plan would mislead an executor or a gate cannot go RED) and worth-considering. If nothing must-fix survives your probes, say `APPROVE` and say explicitly that you approve the CURRENT TEXT AS A WHOLE.

Report per `review-common.md` format, findings prefixed `L-n`. Verdict line first.
Shell cwd was reset to /Users/kein/Documents/workspace/dev/worktree/kein-harness/instrument
