# S48-0a — Rulings and the PRE-CODE half of the doc sweep (docs only)

Read `docs/prompt/worker-brief.md` first; it binds you (no git; no spawning writers/reviewers; anchor edits by content and assert each applied once; report reversals loudly; restore by `cp` backup, never `git checkout --`).

**Plan:** `.omc/plans/ralplan-phase-48-handle-admission.md` (REVISION 5b). Read §0, §1, §2.5, §2.6, §3.2, §3.4, §3.6, §3.7, §3.8, §3.9, §3.10, §4 (S48-0a's row and done-when), §9. Your story is **S48-0a exactly as §4 states it**: every ruling and prose correction that is a DOC statement landed; every anchor into text S48-1 will delete or rewrite RETIRED (never re-pointed — S48-1 owns re-points, because the citation gate resolves against the working tree at commit time and the new symbols do not exist yet); citation gate GREEN. **No code, no measurement.**

## What to write, and where

1. **`docs/post-loop-backlog.md`, the B-Q5 row** — append the phase-48 planning outcome: the model being replaced (C48-1 one-liner), the parent rulings disposed (ralplan-42 §3.12 five clauses per §3.2; the "single number" docblock ruling DISCHARGED not reversed; R42-D1 REVERSED as a priced acceptance per §3.9 C48-3; the 2026-08-27 clip ruling honoured at straight edges with the arc rescue in the renderer per §3.7), the three owner questions U48-1/U48-2/U48-8 with the plan's defaults, and the pointer to the plan + spike. Keep the row's existing history; append, do not rewrite.
2. **`docs/architecture.md`, the handle section** — a transitional note (this is pre-code): the admission model is being replaced in phase-48, what replaces it (one paragraph), and that the section is rewritten in the code commit. Do not describe the new symbols as existing.
3. **`.omc/plans/ralplan-phase-42-resize-handles.md` §3.12** and **`.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` §8** — a dated retirement note at the top of each section pointing at phase-48's disposition (the same shape ralplan-46 used for B-Q5's excision). History stays; a note is added.
4. **`docs/known-issues.md`** — only if a KI row cites the admission model or its constants by anchor; retire per rule 5 below.
5. **`packages/descvi/test/extractor/run.test.ts`** — its handle-lab docblock names `order-walk.ts` as a sibling source file (§2.5 item 3). Correct the prose ONLY if the edit is comment-only and the file is otherwise untouched; it is outside the citation gate, so nothing forces it — but the plan puts it in the prose sweep by name. Report exactly what you changed.
6. **Anchor retirement (the mechanical half).** Enumerate FROM SOURCE, not from the plan: run
   `grep -rnoE '`[^`]*handle-geometry\.ts#[^`]+`' docs .omc/plans .omc/specs .omc/research e2e packages/descvi/src/react packages/descvi/src/vite scripts`
   and, for each anchor, decide from §3.10 whether its target text is DELETED or REWRITTEN by S48-1. Every such anchor in a file you own (docs, .omc/plans, .omc/specs, .omc/research) is RETIRED: delete the citation if the sentence no longer needs it, or convert it to `git show f411977:packages/descvi/src/react/overlay/canvas/handle-geometry.ts` + a quoted phrase (the gate treats `git show <sha>:path` as a record, not a pin). **Anchors in `e2e/`, `packages/**`, `scripts/` are S48-1's — list them in your report, do not touch them.** The phase-48 plan's OWN anchors into deleted text are also S48-1's (§2.6) — leave them and list them. Anchors whose target text SURVIVES (e.g. `HANDLE_CHIP_PX`, `RESIZE_STRIP_Z`, `buildEffectiveClip`, `fitsInClip`, `centredOn`) stay.
7. **§2.5 items 1 and 2** (the two `spacing-affordance-geometry.ts` docblocks) are attached to symbols S48-1 rewrites — they are S48-1's; do NOT edit them. Record them in your report as S48-1 sites.

## Gates you run

- `node scripts/check-citation-anchors.mjs` — GREEN at the end, AND shown RED once on this tree: plant one bad anchor in a doc you own, run, paste the RED line, restore by inverse edit (not git), run again GREEN. Paste both runs.
- `git diff --stat` at the end — paste it. It must show only files you own plus, at most, `run.test.ts`. If anything else appears, revert it by inverse edit and say so.
- Do NOT run `pnpm gates`, `pnpm test`, or any dev server. Do not touch `:3000`/`:3001`/`:7331`.

## Report (your final message; printed text reaches nobody)

≤60 lines: files changed with one line each; the retired-anchor list (file → anchor → retired how); the S48-1 handover list (anchors and prose sites you deliberately left); both citation-gate runs pasted; the diff stat; every place you disagreed with this brief or the plan, loudly. Leave every change uncommitted — the lead commits.
