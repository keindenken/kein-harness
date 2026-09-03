# Fresh unprimed review — round 3 (phase-48 plan, REVISION 2)

Read `docs/prompt/worker-brief.md` first; it binds you. Then `.omc/artifacts/phase48-plan/review-common.md` (what the phase is, the limits, the bar, the report format). You are READ-ONLY on the repo. Read-only probes are encouraged and expected: this project's plans have repeatedly reached unanimous text approval and then had facts falsified by the first run, so a finding that comes from running something outranks one that comes from reading.

**You are deliberately UNPRIMED.** You have not been given any previous round's findings and you must not go looking for them — every other file under `.omc/artifacts/phase48-plan/` except `review-common.md` and this file is off-limits. Read the CURRENT text of `.omc/plans/ralplan-phase-48-handle-admission.md` as a whole, as a fresh senior reviewer would, and find what such a reviewer would find — **including what prior rounds missed**. The plan's status line and §9 tell you what has been reviewed; treat that as history, never as your scope.

Where to point your instruments (not exhaustive — the point of this lane is what is NOT on it):

- Write your OWN implementation of the model from the plan's contract clauses ALONE (C48-1a…e and any coordinates it gives), then reproduce the three RUN-P numbers the design leans on hardest. If your implementation and the plan disagree, the contract is ambiguous or the number is wrong — either is must-fix; say which readings produce which numbers.
- Every gate `G48-n`: is its RED-when reachable by a fixture the plan names; does the gate live in `pnpm gates` (a `run:` step under `verify` in `.github/workflows/ci.yml`) or `pnpm test:e2e`, and does the plan say which; does the row have a named file/home a story lands.
- The story ladder and the one code commit: with `tsconfig.json` including `src/**` and `pnpm typecheck` running root `tsc --noEmit`, is every done-when satisfiable at the commit it belongs to?
- The DOM path (`use-resize-handles.ts`, `OverlayShell.tsx`): does what the plan says the DOM delivers match what the DOM does — z, stacking contexts, clipping, append order?
- The owner questions in §9: is each one stated on arithmetic you can reproduce, and are the levers offered the real ones?

Report per `review-common.md` format, findings prefixed `H-n`, must-fix separated from worth-considering, each with what you did to check it. Verdict line first: `APPROVE` or `REVISE`; a conditional approve is REVISE.
