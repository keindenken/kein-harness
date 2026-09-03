# Fresh unprimed review — round 2 (phase-48 plan, REVISION 1)

Read `docs/prompt/worker-brief.md` first; it binds you. Then `.omc/artifacts/phase48-plan/review-common.md` (what the phase is, the limits, the bar, the report format). You are READ-ONLY on the repo. Read-only probes are encouraged and expected: this project's plans have repeatedly reached unanimous text approval and then had facts falsified by the first run, so a finding that comes from running something outranks one that comes from reading.

**You are deliberately UNPRIMED.** You have not been given any previous round's findings and you must not go looking for them (`.omc/artifacts/phase48-plan/revision-r1.md`, `architect-r1.md`, `critic-r1.md`, `closure-r2.md` are off-limits — reading them would make you a second closure audit, and the lead already has one). Read the CURRENT text of `.omc/plans/ralplan-phase-48-handle-admission.md` as a whole, as a fresh senior reviewer would, and find what such a reviewer would find — **including what prior rounds missed**. The plan's own status line and §9 tell you what has been reviewed; treat that as history, never as your scope.

Where to point your instruments (not an exhaustive list — the point of this lane is what is NOT on it):

- Every number the plan calls RUN-P: pick the three the design leans on hardest and reproduce them from f411977 sources copied OUTSIDE the repo. If one does not reproduce, that is must-fix.
- Every contract clause `C48-n`: could two executors write different code from it? Name the two readings.
- Every gate `G48-n`: run its RED-when in your head against the fixtures the plan names — is there a fixture that reaches it? Is the gate in `pnpm gates` (a `run:` step under `verify` in `.github/workflows/ci.yml`) or in `pnpm test:e2e`, and does the plan say which?
- Every ruling that reverses or discharges a written parent ruling (ralplan-42 §3.12, R42-D1, the "single number" docblock): is the reason one a later reader can defeat, and does the plan sweep every prose site whose CAUSE the ruling moved?
- The DOM path in `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts` and `OverlayShell.tsx`: does what the plan says the DOM delivers match what the DOM does?
- The owner's ruled numbers are out of scope to reopen — but whether the plan's gates can tell the owner something about them is in scope.

Report per `review-common.md` format, findings prefixed `F-n`, must-fix separated from worth-considering, each with what you did to check it. Verdict line first: `APPROVE` or `REVISE`; a conditional approve is REVISE.
