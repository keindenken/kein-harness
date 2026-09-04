# RALPLAN — phase-49: the comparison surface, the four parked visual decisions, and the v3.5 close

## Status

- **Revision:** r5 — ⚠ **a HARDENING pass on r4', and NOT a sixth text round.** Both round-5 lanes judged the r4' text fit to hand to the owner; the closure audit's words were *"fit to hand to the owner, and the loop should not run again"*. So r5 applies `.omc/artifacts/phase49-plan/revision-brief-r5-hardening.md` and nothing else — no new decision, no new story, no re-opened option, no new gate. **Its headline is a defect in the SELFTESTS rather than in the text**: each `--selftest` drove its script through the ARGUMENT path, which replaces the very object the plan calls the gate, so a copy with six of seven witnesses deleted, or two of five fields deleted, or the archive index dropped from the root set, or the heading-slug branch disabled, ran its own selftest GREEN. On every CI push those selftests would have re-proved the scan MECHANISM and never the SCOPE. All four now assert their own enumeration and were shown RED from a broken copy that reduces it. Everything before this bullet stands on r4' — four revisions on r0, applying the round-4 adjudication recorded in `.omc/artifacts/phase49-plan/revision-brief-r4.md` (which stands on `revision-brief-r3.md`, on `r2`, on `r1`). ⚠ **The lead pre-committed r4' as the LAST full text round**: past that point the remaining defects are the kind text rounds cannot produce — which is why r4' spent itself making the gates things a MACHINE runs after this session ends, and why r5 spends itself on the one thing r4' could not check about them.
  ⚠ **r3' WAS A DESIGN CHANGE AND r4' FINISHES IT; A READER WHO TREATS EITHER AS A TEXT REPAIR WILL MISREAD §6.** Three rounds running, every must-fix belonged to one class — PM-10, *a gate believed because it returned zero, that returned zero because it never looked at its subject* — on the same two contracts. The cause was that the gates were authored as **shell snippets inside prose**: prose cannot be run, so each round's reviewers executed a *reconstruction* and found a new way the reconstruction differed from what would actually run. **G49-2, G49-3, G49-4 and — as of r4' — G49-5 are committed scripts** — `scripts/gate-g49-2-archive-pointers.sh`, `scripts/gate-g49-3-look-witnesses.sh`, `scripts/gate-g49-4-override-leak.sh`, `scripts/gate-g49-5-one-home.sh` — each with `set -eu`, positional scan roots, a missing-root precondition, an **exit-status verdict** and a **`--selftest` that stages its own plant**. The plan states what prose is good for: each gate's RED-when, its allow-list predicate, and what claim goes unguarded if the gate cannot be written. The script's job is being runnable; the plan's job is saying what it must prove.
  ⚠ **AND r3' STOPPED ONE WORD SHORT OF A RULE THIS REPO ALREADY HAD, WHICH IS WHAT r4' FIXES.** All three scripts were UNTRACKED (`git ls-files scripts/ | grep g49` → empty), named in no story's Lands, and run by nothing in `.github/workflows/ci.yml` — while `AGENTS.md` states that the gate set IS that job and that **a gate nobody watches has already stopped being one**. Their RED proofs were one-off manual plants recorded in a plan that gets archived, so after phase-49 closed nothing would have shown they can fail. At r4' **all FOUR scripts carry a `--selftest` that stages its own plant** — the idiom already sitting in that job under a step named *"proves the gate can fail"* — **and landing them, selftests included, into the verify job is an explicit item in S49-0's and S49-1's Lands**, with G49-4's second Vite build priced in §6 rather than discovered in CI. **The fourth script is G49-5**, which r3' left as a prose description of a scan, in the revision whose whole thesis was that a gate living in prose gets re-implemented by every reader.
- **Mode:** DELIBERATE (four owner-owned visual decisions plus a docs migration; pre-mortem is §9, expanded verification is §6).
- **Lanes that read this text:** **r0** — architect (Claude, probing) APPROVE-WITH-CONDITIONS, critic (Claude) REJECT, codex REJECT; all three in parallel on the r0 text. **r1'** — a closure audit (primed, holding the r1 item list) `0 NOT CLOSED / 3 PARTIAL / 0 REWORDED-ONLY`, an unprimed fresh review APPROVE-WITH-CONDITIONS, and codex REJECT; all three in parallel on the r1' text. **r2'** — a closure audit (primed, holding the r2 item list) which ran G49-2's final command verbatim and reproduced this plan's pasted transcript file-for-file, an unprimed fresh review, and codex; all three in parallel on the r2' text. **r3'** — a primed closure audit returned **ALL CLOSED** on R23…R28, all six substantive and none reworded-only; both Claude lanes ran the three committed scripts and reproduced this plan's pasted transcripts **row for row, under `sh` and `zsh` alike**; the `dist/` reversal was verified to have propagated completely; codex moved from REJECT to APPROVE-WITH-CONDITIONS. **What running them exposed is round 4's item list, and it is mostly about the gates' OWNERSHIP rather than their logic.** **r4'** — a primed closure audit and codex, in parallel on the r4' text; **both judged it fit for the owner** and neither reopened a decision, an option set, a driver or the owner table. **Both independently found the same defect and it is the one r5 exists for**: the selftests prove scan mechanics and not that the production enumerations still cover every claimed subject, so a later edit can remove a witness, a field or an archive-index root and keep a green selftest. **r5** — the hardening pass itself; no review lane has read it.
  ⚠ **The codex lanes are in scope.** `docs/handoff/260903-phase-49-kickoff.md` originally recorded codex as excluded by a ruling of 2026-09-02; **the owner reversed that on 2026-09-04 ("codex 투입 가능") and the lead has corrected the kickoff doc.** A reader who finds the older sentence quoted anywhere downstream is reading a superseded ruling, not a scope contradiction.
- **Approval state:** _(lead fills)_
- **Branch:** `phase-49-omc`, forked from `feat/phase-49-comparison-surface` @ `9473225`, itself forked from the phase-48 head rather than from `main`.
- **Gates run on this text at r5:** `node scripts/check-citation-anchors.mjs` → GREEN, 0 violations. **All FOUR gate scripts were invoked BY PATH**, each in GREEN and in a planted RED, each precondition shown firing, and each `--selftest` shown GREEN *and* shown RED from a deliberately broken copy — see the demonstration records inside each gate. ⚠ **AT r5 THE BROKEN COPY REDUCES THE GATE'S SCOPE, WHICH IS WHAT r4''s BROKEN COPIES DID NOT DO.** r4' broke a pattern or an exclusion — a mechanism — and all four selftests survived a scope cut untouched. The r5 copies delete six of G49-3's seven witnesses, two of G49-5's five fields, G49-2's archive-index root, G49-2's heading-slug branch, and `dist` from G49-4's bundle set; **each of those five copies now reports RED and names what was lost.**
  ⚠ **REAL-TREE STATE AND STAGED-DEMONSTRATION STATE ARE DIFFERENT THINGS, AND r3' PUBLISHED ONE SENTENCE THAT CONFLATED THEM.** It said all three gates were run "each in GREEN", which is true of the staged states and false of the tree an executor will run them on — a reader who runs them against that sentence concludes the scripts are broken. Per gate, on THIS working tree, before any story has landed:

  | gate | real-tree state today | why that is the CORRECT reading | where its GREEN was shown |
  |---|---|---|---|
  | G49-2 | **RED, exit 1** — 6 live-pointer rows, **legs (b) and (c) silent** | leg (a) IS S49-0's rewrite list; it is a POST-move gate | `--selftest`'s clean fixture, and the post-move sandbox |
  | G49-3 | **GREEN, exit 0** — 7 witness files, 87 tests | nothing has moved yet | on the real tree |
  | G49-4 | **RED, exit 1 at leg 0** — no override reader exists in source | S49-1 is what creates the subject | with a guarded reader planted, both bundles built |
  | G49-5 | **RED, exit 1** — 4 of 5 fields have no home | that IS D49-0's fact 2, and the reason S49-1a exists | `--selftest`'s fixture; and its 5th row is GREEN on the real tree today |

  **Three of the four are RED on the tree right now and every one of those REDs is the gate working.** A gate that were GREEN today would be a gate with no subject.
  ⚠ **The checked-anchor COUNT is deliberately not repeated here.** r0 carried three different numbers for one measurement in three sections (600 / 599 / 556). The count has exactly one home — **D49-4**, written beside the command that produces it and beside the tree it was measured on — and S49-0 re-derives it immediately before the move rather than trusting any written figure. **A number that appears in more than one place has, by construction, more than one truth**, and this one moves every time the plan is edited.
- ⚠ **TWELVE things in this plan reverse the inputs it was written from, every one of them from source or from a run, every one flagged in place.** A reviewer should read these first, because each is a place where the input and the tree disagreed and the tree won. ⚠ **Item 3 is a reversal OF THIS PLAN'S OWN PREVIOUS REVERSAL** — it stood for two revisions and it was wrong:
  1. **D49-4** — the archiving destination (`260901-e3-v3`, which exists) and the "240 references" framing. *(from r0)*
  2. **U49-B** — the arming-threshold rider's price, and its reachable box, which is narrower than **both** framings the item arrived with. r0's own table offered two values (5 px, 6 px) that the suite rejects on arrival. **The interval itself is stated in U49-B and nowhere else, this line included** — see S49-6. *(from r0; the lower end closed at r2', the last duplicate removed at r3')*
  3. ⚠ **G49-4 / C49-8 — THE `dist/` CLAIM IS FALSE AND IS REVERSED AT r3'.** r1' asserted, and r2' repeated in four places, that `pnpm build` produces a bundle with *no overlay in it* because `vite.config.mts` mounts the plugin `overlay: false`. **Measured at r3' by running `pnpm build` and grepping the emitted bundle: the overlay IS in `dist/`.** `overlay: false` is a **runtime branch**, not a build exclusion — `packages/descvi/src/vite/bootstrap-entry.ts#import DescviOverlay, { type ManifestMap } from '../react/DescviOverlay';` is an unconditional module-scope import and the flag only chooses which tree the bootstrap renders, so Rollup keeps the whole overlay graph. Reproduce: `grep -RIlF -e dsh-selection-ring -e data-dsh-ring-key -e pad-x dist/` → all three present in `dist/assets/index-*.js`. **What r1' actually measured was an identifier grep, which esbuild mangles away in every bundle** (reversal 5), so its zero in `dist/` said nothing about `dist/`. **Consequence: `dist/` is a subject, and the bundle `vite.config.mts`'s own docblock calls "the deliverable" would have been left unguarded.** G49-4 now builds and scans **both** bundles. *(from r1'; reversed at r3')*
  4. **D49-4's census query** — the `^\./…` anchoring the exclusions arrived with is inert under the grep on this machine, which returns the whole `.omc/archive/**` history as live pointers. **Do not restore the anchored form.** *(from r1')*
  5. **G49-4's grepped artefact is a STRING LITERAL, NEW AT r2', and it is now MEASURED rather than reasoned.** There is no `minify` key in `vite.config.mts`, `descvi.vite.config.mts` or `packages/descvi/src/vite/`, so the design-view build takes Vite's esbuild default with identifier mangling. **Run at r2': a planted identifier `readDescviLookOverrideProbe` was mangled to `vM` and is ungreppable; the planted literal `"descvi-look-override"` survives verbatim.** A gate that greps for the reader's NAME returns the same zero with and without the leak. *(from r1'; the gate's evidence is inside G49-4)*
  6. **D49-4's census PUBLISHES A COUNT COLUMN ITS OWN COMMAND CANNOT PRODUCE, NEW AT r2'.** `grep -rlnE` — `-l` suppresses `-n` and prints filenames only. The live referrers r2' listed were right **as scoped** (nine then, eleven since r4' widened the roots — item 11); the instrument beside them could not regenerate one of the per-file numbers. One command per claim, each labelled, is the replacement.
  7. **The census query's ROOTS were wrong, NEW AT r2' AND FOUND BY RUNNING IT.** Rooted at `.`, it sweeps `.omc/artifacts/**` — the gitignored review-apparatus tree — and returned **the review artefacts of this planning round as live pointers to repair**. ⚠ **No count is given, and that is the point twice over**: the population grows with every lane this round spawns, so r2' wrote "four" and the next measurement found five. The roots are now enumerated (`docs .omc/plans .omc/specs .omc/research packages e2e scripts src`), which drops the untracked namespaces the same way `docs/handoff/**` and `.omc/archive/**` are dropped. This is instance 5 of §9's `PM-10` class and it was found by the only thing that finds them: running the command.
  8. ⚠ **THE ARCHIVE GATE WAS VACUOUS UNDER THIS MACHINE'S SHELL, NEW AT r3' AND FOUND BY RUNNING IT UNDER BOTH SHELLS.** r2' wrote the scan roots as `ROOTS="docs …"` and expanded them unquoted. **zsh does not word-split an unquoted scalar**, so both legs received ONE eight-word argument, emitted a warning to *stderr* and zero rows to *stdout* — and zero rows satisfied the stated verdict **vacuously, on a tree carrying five live pointers**. Under `sh` the same block returned the correct five. The roots are now a **positional list** (`set -- docs .omc/plans …` then `"$@"`), which reads identically under both shells, and the demonstration below runs the committed script under `sh` **and** `zsh` and pastes both. *(from r2')*
  9. ⚠ **THE LEAK GATE'S PRECONDITION CERTIFIED A CHUNK THAT CANNOT HOLD ITS SUBJECT, NEW AT r3'.** `find dist-designview -name '*.js' -size +0c -print -quit` returns the **first** match, which on this tree is `dist-designview/assets/page-BUv_gJ87.js`, a per-page chunk. Of the 32 emitted `.js` files exactly one carries the overlay (`grep -RIl 'dsh-ring-layer' dist-designview/` → `dist-designview/assets/index-CAq1jD4i.js`). So a build that emitted page chunks while dropping the overlay entry passed that precondition and then grepped clean. ⚠ **Both chunk names are content hashes and move on the next source edit** — they are pasted as the record of one measurement, never as something to compare against; the two commands regenerate them. **The precondition now asserts an overlay MARKER**, and G49-4's leg-1 RED is demonstrated against a staged bundle that has the page chunks and not the entry. *(from r2')*
  10. ⚠ **THE REVISION BRIEF'S OWN NUMBER WAS WRONG AND THIS PLAN'S MEASUREMENT REVERSES IT — SAID HERE RATHER THAN LEFT AS A QUIET CORRECTION.** Revision brief r3 stated the dogfood corpus carries **275** arbitrary-value classes. r3' measured **251 occurrences / 39 distinct / 155 `className` attributes** and published the pipeline that produces each; the round-4 audit re-ran it and confirmed **the plan is right and the brief was wrong**. r3' then used its own number without saying it had overruled its instructions, which is the half that needed fixing: **a correction that is not announced is indistinguishable from a transcription error.** Reproduce: `grep -rIoh 'className="[^"]*"' --include='*.tsx' src/app | grep -o '[a-zA-Z0-9:/_.-]*\[[^]]*\]' | wc -l` for the 251, the same pipeline through `sort -u | wc -l` for the 39. *(from revision brief r3; reversed at r3', flagged at r4')*
  11. ⚠ **THE POINTER CENSUS WAS RIGHT AS SCOPED AND THE SCOPE WAS WRONG — 9 ACROSS 5 BECOMES 11 ACROSS 6 AT r4'.** `.omc/archive/README.md` — the archive's INDEX, not an archived plan — asserts in its own table that one plan is *"APPROVED and live at"* and another *"execution-ready at"* the two paths S49-0 moves. It was outside the census's roots and behind G49-2's `--exclude-dir=archive`, **and the exclusion's justification was imported from a rule that does not cover it**: `docs/README.md` exempts archived plans as point-in-time RECORDS, and an index asserting where plans live is not a record. It is exactly the file an archiving pass exists to rewrite. The exclusion is now narrowed to the archive's CONTENTS. *(from r0's census framing; reversed at r4')*
  12. ⚠ **THE SPATIAL A/B AS r3' SPECIFIED IT COULD NOT RENDER TWO VALUES, AND THAT FALSIFIES A LEAD RULING RATHER THAN A PLANNER INVENTION.** `use-selection-rings.ts` states in its own docblock that its style writer is *"THE ONE RING STYLE WRITER — the primary's shipped static node and every pooled secondary go through this and nothing else"*. One writer, one merged record, one value: two selected siblings at two candidate widths was not renderable as written. The mechanism is replaced (D49-1) and the ruling it serves — that pure-temporal comparison forces comparison from memory — still stands. *(from R6's adopted synthesis; reversed at r4')*

**Execution order.** S49-0 → **S49-P (the live-switch spike — an abort gate, not a task)** → S49-1a → S49-1 → **[owner gate, §7's table]** → S49-2 / S49-3 / S49-4 / S49-5 (each: contract-and-gate commit, then value commit, per C49-5) → S49-6 only if U49-B is answered yes. Every story before the gate executes without the owner; every story after it has a shipped-value default (C49-6), so a deferral costs a row and not the phase.

## 1. Principles

1. **The deliverable of this phase is a JUDGEMENT INSTRUMENT, and only then the four values it produces.** Three items (`reorder-indicator-look`, `selection-ring-treatment`, `spacing-affordance-mark`) have each been through a live pass and each stopped at the same place; a fourth (`padding-glyph`) arrived the same way at phase-48's G48-8 pass. `docs/open-design-questions.md#⚠ **이것이 "아직 안 봤다"가 아니라는 것이 이 항목의 요점입니다.**` states the diagnosis: the owner looked, and what they could not see was alternatives. A phase that ships a fifth single value stops in the same place, so the surface is the thing that must be right.
2. **The surface compares REAL renderings or it compares nothing.** A mock-up of a 2 px line beside a 3 px line answers a question about lines, not about this indicator in this canvas. Every candidate form is judged by whether it reaches the same drawing code the product reaches — which is why the imperative-furniture boundary (principle 3) is the axis and not a footnote.
3. **descvi cannot edit its own furniture with descvi, and the plan says where the boundary is rather than discovering it mid-story.** The furniture is painted imperatively into the ring layer and React does not reconcile it. Any surface that assumes the overlay is an ordinary React screen is already wrong.
4. **A LOOK change is a contract change.** `.omc/specs/v3-layout-panel-visual-spec.md#⚠ **Both are CONTRACT changes, not CSS changes.**` and the S46-1/S46-2 split that discharged it are the shipped precedent: where a gate asserts the look, the contract moves FIRST, in its own commit, with no red window in between. This phase inherits that discipline verbatim for the glyph and for anything else a gate pins.
5. **The comparison machinery is scaffolding and must be provably absent from what ships.** A parameterisation that survives into the production path turns one shipped value into two, and the second one is the one nobody re-reads. The mechanism that prevents it is a gate, not a convention (G49-4).

## 2. Decision drivers

- **D-A — Fidelity of the comparison to the shipped rendering.** The owner's decision is only as good as the pixels they judged. This driver dominates D49-1 and is the reason the cheapest option is not automatically the chosen one.
- **D-B — Gate blast radius per iteration.** The surface will be edited many times (four items × several candidate values × at least one revision round). Any form whose every edit re-pins gate assertions taxes the whole phase, not one story. This is what prices option (c) out.
- **D-C — The phase must not stall on the owner.** The owner's picks land mid-phase by construction. Everything before the pick must execute without them, everything after must be specified with the value as a parameter, and every item must have a stated fallback so a deferral costs one row and not the phase.

## 2a. What phase-49 does NOT take from the routed list

`docs/e3/tracker.md#**What the next phase should take.**` routes three items forward from phase-47. **Phase-49 takes none of them, and says so rather than leaving it to inference.** (i) is already done there. (ii) — the `boundary`/`selection-change` vocabulary decision — is a terminal-vocabulary question with no visual component; it does not ride a comparison surface and stays routed. (iii) — a gate for *a mechanism the codebase already documented, imported into a context where its sign flips* — is a cross-cutting gate-design problem whose cost is unbounded relative to this phase's bundle; it stays routed. Neither is a rider.

## 3. Decisions

### D49-0 — the ground fact every other decision stands on: WHERE the furniture is drawn, and how much of it is reachable from outside

Established from source (each anchor verified to occur exactly once in its file with `grep -c -F`):

| Furniture | Module | Painter | Reachable from outside the React tree? |
|---|---|---|---|
| Reorder indicator | `packages/descvi/src/react/overlay/canvas/reorder-paint.ts` | `packages/descvi/src/react/overlay/canvas/reorder-paint.ts#export function paintReorderOverlay(layer: HTMLElement, state: ReorderPaintState, isDark: boolean): void {` | **YES** — exported, takes the layer as an argument |
| Selection ring | `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts` | `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#function applyRingStyle(node: HTMLElement, box: RingBox, color: string): void {` | **NO** — module-private; the only export is the hook |
| Hover ring | same file, **a separate code path** | inline writes in the hook's first layout effect | **NO** |
| Spacing strips + glyphs | `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts` | `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts#function createSpacingGlyph(doc: Document, figure: keyof typeof SPACING_GLYPH_PATHS, id: string): SVGElement {` | **NO** |
| Resize chip (phase-48) | `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts` | `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts#function applyHandleStyle(` | **NO** |

All five write **imperatively into `#dsh-ring-layer`** — React renders the container and nothing inside it, stated in the source itself at `packages/descvi/src/react/overlay/OverlayShell.tsx#Imperatively populated by useSelectionRings; React owns this node and nothing inside it.` — and the reorder painter resolves the layer by id at paint time (`packages/descvi/src/react/overlay/canvas/use-reorder-drag.ts#const node = doc.getElementById("dsh-ring-layer");`), entirely outside reconciliation.

**Three facts this table settles that the brief's framing did not have:**

1. **Exactly ONE of the four parked items has a painter callable from outside the overlay.** The reorder indicator does; the ring, the spacing glyph and the pad glyph do not. Any surface that is "a screen that draws the furniture itself" therefore reaches 1/4 of this phase's subjects unless the phase exports three private style writers — which is the leak D49-2 must prevent, not create.
2. **The ring's look is not in constants at all — it is INLINE LITERALS**, three of them: the selection border at `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#2.5px solid ${color}`, the selection radius at `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#node.style.borderRadius = "6px";`, and the hover ring's own separate `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#1.5px solid ${shades.light}`. **There is nothing to parametrise until they are named.** That is a story of its own (S49-1a), not a line in another story.
3. **Hover and selection do NOT share a code path**, which is precisely what backlog direction (c) — *"Figma는 hover 링이 selection 링보다 크다"* — asks about. Today they differ on three axes already (width 1.5 vs 2.5, shade `light` vs `deep`, z 39 vs 40) and agree on radius 6 px by two independent literals. **A "hover larger than selection" experiment that changes one of those two 6s and not the other produces a bug that looks like a design.** C49-3 exists for this.

### D49-1 — the FORM of the comparison surface

**Options** (the three `docs/open-design-questions.md#**무엇이 비교 표면이 되어야 하는가.**` names).

**(a) A static gallery screen** rendering several values side by side.

| | |
|---|---|
| Can show | The reorder indicator's real painter, called directly with a synthetic `ReorderPaintState`. Several thicknesses at once, in one screenshot. |
| Cannot show | The ring, the spacing glyph or the pad glyph **without exporting three private writers** (D49-0). Real canvas context — a real selected element with a real ring group, real neighbours, real gaps. **And it cannot show the two facts the `reorder-indicator-look` row says the decision needs**: the gap-0 collapse (`packages/descvi/src/react/overlay/canvas/reorder-paint.ts#const thickness = Math.max(0, Math.min(REORDER_INDICATOR_THICKNESS_PX, gap));` — a synthetic state can be *told* gap is 0, but the owner's question is whether the collapse is acceptable *when it happens to them*), and the "16 px tick on short items" read, which is a property of `/shop/member-list`'s real 7-member row against `/lab/tests/reorder-flow`'s real vertical 5. |
| Gate cost | Low if it lives under `src/app/**` (dogfood, out of the deliverable). |
| Lives in | `src/app/**`. |

**(b) A dev-only runtime override on the overlay** — the live canvas, values switched without a rebuild.

| | |
|---|---|
| Can show | All four items, in real canvas context, on any screen in the corpus including the two `reorder-indicator-look` names. The gap-0 collapse and the short-item tick happen for real. The hover-vs-selection size relation is observable by moving the pointer, which is the only way that relation exists at all. |
| Cannot show | Two values *simultaneously* in one viewport. |
| Gate cost | Moderate and bounded: the constants get named (S49-1a), which touches source under `packages/**` and is gated; the override itself must be provably absent from production (G49-4). |
| Lives in | `packages/**` — deliverable, gated. |

**(c) Promote `lab/tests/**` fixtures to comparison duty.**

| | |
|---|---|
| Can show | Nothing new. |
| Cost | Two mechanisms, both measured. **(1)** `packages/descvi/test/host-pristine-src.test.ts#const ALLOWED_AUTHOR_FILES = new Set(['page.tsx', 'spec.ts']);` is an allow-list over BASENAMES applied recursively to the three namespaces at `packages/descvi/test/host-pristine-src.test.ts#const AUTHOR_NAMESPACES = ['lab/challenge', 'lab/tests', 'shop'] as const;` — so a comparison screen there may carry no helper module at any depth. **(2)** The re-pin cost is not a fixture count and not a `screens.json` snapshot. ⚠ **THE FIGURE THIS PARAGRAPH USED TO LEAD WITH — "69 assertions" — IS CARRIED FROM PHASE-47 AND WAS NEVER RECOMPUTED ON THIS TREE, so it is replaced by the MECHANISM plus the command that regenerates it, per this plan's own rule that a number with no live instrument beside it is a claim nobody can check:** the count is whatever `pnpm vitest run packages/descvi/test/gate packages/descvi/test/extractor/run.test.ts` reports as failing after a screen is added, and it is large for a structural reason that does not move — ten gate files under `packages/descvi/test/gate/` collect subjects by a filesystem scan rooted at `packages/descvi/test/helpers/insert-composition.ts#export function corpusScanRoot(repoRoot: string): string {` and pin **whole-corpus census totals as bare literals** (e.g. `packages/descvi/test/gate/insert-span.test.ts#expect(sites.length).toBe(784);`), with an eleventh file, `packages/descvi/test/extractor/run.test.ts`, carrying a hand-written `GOLDEN_IDS` list plus a byte-identity check of `.descvi/screens.json`. Two screens moved a large batch of those numbers at phase-47 — the phase-47 record says 69 — **because the pins are over every oid in the corpus**, and that mechanism is what prices option (c), not the particular integer. |

> ⚠ **AND THE SAME MEASUREMENT REMOVES THAT COST FROM (a) AND (b), WHICH IS WORTH SAYING BECAUSE THE KICKOFF DOC LEAVES IT LOOMING OVER ALL THREE.** The 11 census files pin the corpus under `src/app/**`. **A pure furniture-look change touches no screen, so none of them moves for S49-2…S49-6.** They enter this phase's risk only if it ADDS a screen — which only (a) does, and which (b) does not. If a surface ever does need helper modules beside a page, the precedent is `src/app/sandbox/**`, which is deliberately outside `AUTHOR_NAMESPACES` and is where `handle-lab` legally carries sibling `.tsx` files.
>
> **(c) IS INVALIDATED, AND NOT ON COST.** It is invalidated because **it is not an answer to the question.** `lab/tests/**` fixtures supply *subjects* — which element, in which layout — and the parked items are questions about *values*. A promoted fixture screen shows the same single shipped value the owner has already seen, on one more element. It would still be true after (c) shipped that the owner has never seen two thicknesses. **And the subjects it would supply already exist**: the `reorder-indicator-look` row names `/shop/member-list` and `/lab/tests/reorder-flow` as the pair the decision needs, and both are in the corpus today. So (c) pays phase-47's re-pin price to obtain something the phase already has and something the phase does not need. Cost is the second reason, not the first.

**CHOSEN: (b).**

**Reason — the STRUCTURAL one, which is the strongest and which r0 buried in a table cell.** **Three of the four subjects have no callable painter** (D49-0's table, fact 1). (a) therefore buys **one-quarter coverage at the price of exporting three module-private style writers** — `applyRingStyle`, the hover path's inline writes, and `createSpacingGlyph` — into a screen that is not the product. That is to say: **(a) manufactures the very leak D49-2 exists to prevent**, and it manufactures it in source rather than in a bundle, where no grep-the-bundle gate can even see it. This reason turns on nothing about how a person judges, so it survives whatever U49-A answers, and it survives the re-specification of G49-4 (revision-brief r1's item R1, and r2's item R17) that removed the leak gate's ability to speak for anything else.

**Second reason, and it cuts both ways — say so rather than leaning on it.** Three of the four subjects only exist while a gesture is in flight, and a gesture cannot be placed side by side with itself: the reorder indicator is painted during a drag and cleared on release (`packages/descvi/src/react/overlay/canvas/reorder-paint.ts#export function clearReorderPaint`); the spacing strips appear on pointer-in and the new direction the `spacing-affordance-mark` row asks for is *specifically about when they appear*; the hover ring exists only under a pointer, and there is exactly one pointer. A gallery that shows three of any of these at once has shown the owner something that can never happen. ⚠ **But transience is only half an argument, because it cuts against (b) too**: under (b) the owner still switches a value by reaching for a control, and reaching for a control moves the pointer, which extinguishes the hover ring and ends the drag. r0 used transience to kill (a) and never answered it for (b). **The answers are two mechanisms, both now required rather than hoped for:** the override's re-render channel is a KEYBOARD binding, not a pointer control (see the amended C49-2 and S49-1), and the persistent subject gets a spatial comparison instead of a temporal one (next paragraph).

> ⚠ **AND HERE IS THE ONE THING IN THIS DECISION THAT WAS NOT RENDERABLE AS r3' WROTE IT — FOUND BY codex, VERIFIED FROM SOURCE, AND IT FALSIFIES A LEAD RULING RATHER THAN A PLANNER INVENTION.** `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts# * THE ONE RING STYLE WRITER — the primary's shipped static node and every pooled secondary go through this and nothing else (plan §3.6, DR45-4's named cost paid down).` — one writer, fed one merged record, writing one value. **Two selected siblings at two candidate widths is not something that specification can paint.** The ruling it serves is not withdrawn: R6 adopted the architect's synthesis because the objection was real — a purely temporal comparison forces the owner to compare across a gap in time and a pointer trip, which is comparison from memory, the instrument that already failed three live passes. **What went unchecked was whether the chosen mechanism could paint two values at once.**
>
> **THE MECHANISM, REPLACED — the third option, which keeps one writer.** The pooled ring nodes are already KEYED: `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#export const RING_POOL_KEY_ATTR = "data-dsh-ring-key";`, set at `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#function createPooledRingNode(doc: Document, key: string): HTMLElement {` and read back off the node at `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#    const key = node.getAttribute(RING_POOL_KEY_ATTR);`, keyed by ELEMENT and deliberately not by oid. **So the ring's override record carries a candidate LIST, and the one writer indexes it by that key.** One reader, one record, one writer, one leak surface, one gate — **only the SHAPE of the override's value changes**, from a scalar to a list.
>
> ⚠ **TWO SOURCE CORRECTIONS TO THAT MECHANISM, BECAUSE THE ADJUDICATION STATED IT ONE STEP LOOSER THAN THE SOURCE SUPPORTS AND AN EXECUTOR WOULD HIT BOTH.** (1) **The writer does NOT receive the key today** — `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#function applyRingStyle(node: HTMLElement, box: RingBox, color: string): void {` takes a node, a box and a colour; the key lives on the node as an attribute. S49-1 either passes the member identity as a fourth argument at both call sites or reads it back off the node — the first is cleaner and the second needs no signature change, and **either way the docblock's own warning applies: `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts# * ⚠ TWO CALLERS, and the structural gate counts them.` A fork of this writer is what the gate exists to catch, and the whole point of indexing is that there is no fork.** (2) **The PRIMARY ring carries no pool key at all** — the attribute is set only by `createPooledRingNode`, so the primary's static node needs an identity of its own (a sentinel) or the list indexes from the secondaries alone. Neither is hard; both are the kind of thing a story discovers at 2am if the plan does not say it.
>
> **AND THE FALLBACK IS DECIDED HERE, NOT MID-STORY.** If S49-P shows the indexing does not reach the pooled path cleanly, **drop the spatial A/B, take the ring temporally like the other three, and record in the story that the architect's objection to pure-temporal comparison goes UNANSWERED.** That is honest, it costs one row, and it is strictly better than a sentence describing a rendering the renderer cannot produce.

**The shape of the surface: temporal where the subject is transient, SPATIAL where it is persistent.** **The selection ring is persistent** — it survives the pointer leaving, which is exactly what distinguishes it from the other three. So the plan does not force it through a temporal comparison it does not need. Where the subject permits it, S49-1 ALSO stages a **spatial A/B: two selected siblings at two candidate values in one viewport**, rendered by the ONE ring style writer indexing a candidate list by the pool key each node already carries (the box above), on the shipped multi-select pool (`packages/descvi/src/react/overlay/__tests__/selection-ring-pool.test.tsx` is the pool's own witness). This is the synthesis, not a hedge: (b) is the substrate for all four items; the ring additionally gets the side-by-side that (a) was wanted for, without exporting a single private writer. **S49-3 takes the ring decision on the spatial staging; S49-2, S49-4 and S49-5 take theirs temporally.** The gap-0 collapse and the 16 px tick, the two facts the `reorder-indicator-look` row says the decision turns on, are why S49-2 stays temporal: both are consequences of a real layout, and reproducing a real layout inside a gallery is the canvas with extra steps and a second renderer to keep honest.

**What (b) costs, stated rather than discovered.** The ring's values must be named before they can be switched (S49-1a) — this is real source work under `packages/**`, and it is work the `selection-ring-treatment` row needs done whatever surface wins, because *"굵기에 스위트 스팟이 있으니 값을 흔들어 찾는다"* is not performable against a literal in a template string.

### D49-2 — how alternatives are parametrised

**Options.**

- **(i) A value-set module the surface iterates over.** Natural for a gallery; under (b) there is nothing to iterate — the canvas shows one state.
- **(ii) A dev-only override, resolved ONCE per paint pass from a single reader, guarded by `import.meta.env.DEV`.** The candidate values live in the same record as the shipped defaults, so the shipped value stays one literal in one place.
- **(iii) Duplicate the renderer for the comparison path.** **INVALIDATED**, and by this repo's own history rather than on taste: phase-48 needed *three* agreement gates (G48-4a/4b/4c) to hold three implementations of one model together, and that was for a model with an exact oracle. A second furniture renderer has no oracle at all — its whole purpose is to look different — so nothing could ever hold it to the first. The owner would then be judging the copy.

**CHOSEN: (ii), shaped by the precedent already in the tree.**

`packages/descvi/src/react/overlay/canvas/handle-geometry.ts#chipPx: HANDLE_CHIP_PX,` shows the pattern C48-1 established: a **constants record** (`DEFAULT_HANDLE_GEOMETRY`) that every consumer reads and that G48-4a asserts as source text. D49-2 extends that pattern to the look family rather than inventing a second one — one record per furniture family, the shipped value as the record's default, candidates as named siblings.

**Reason — from D49-0's own fact 2, which makes the choice nearly free rather than merely correct.** **The ring has no constants at all today; its look is three inline literals.** So *naming them is unavoidable whatever surface wins* — (a) would need them named to feed a gallery, (c) would need them named to vary anything, and the `selection-ring-treatment` row's own words (*"굵기에 스위트 스팟이 있으니 값을 흔들어 찾는다"*) are not performable against a literal inside a template string. **Once the record exists because it had to, the defaulted override is the zero-marginal-cost option**: it adds one reader and no second store of values. That is a cost argument that does not borrow anything from a gate.

**Secondary, and stated with its dependency named.** Single-source-of-truth and no-leak are the same requirement seen twice, and a record with a defaulted override satisfies both with one mechanism. ⚠ **The no-leak half of this is only as good as G49-4, and G49-4 as r0 wrote it could not go RED** (see the re-specification in §6). ✅ **At r3' that gate is a COMMITTED SCRIPT and has been shown RED from the file in three independent ways** — leg 0 on the real tree (no reader in source), leg 2 with a guard-free plant in place and the matching bundle file named, and leg 1 against a bundle carrying page chunks and no overlay entry — **plus GREEN with the guarded reader, across BOTH emitted bundles. The demonstration record is inside G49-4.** So this half of the reason is now a proof about the INSTRUMENT. What it is still not is a proof about the phase's own override, which does not exist yet: G49-4 has been shown able to see a leak, and S49-1 is what puts the real subject in front of it. What remains unconditional either way: any design where candidate values live somewhere other than beside the default eventually disagrees with it, and the disagreement is invisible — which is exactly what an untestable second renderer (option iii) institutionalises.

**The mechanism, precisely, so an executor does not guess:**
1. Each family exposes a constants record (reorder: extend `reorder-paint.ts`; ring: **create one, S49-1a**; spacing glyph: the `SPACING_GLYPH_PATHS` record already is one; pad glyph: same record).
2. Exactly one module reads an override and merges it over the defaults. It is the ONLY module that mentions the override, and its body is inside `if (import.meta.env.DEV)`.
3. Every painter takes its constants from the merged record, never from a bare literal — which is only possible after S49-1a names the ring's three literals.
4. **The leak gate is G49-4** and it greps the production bundle, not the source.

### D49-3 — the mid-phase owner gate

The owner's picks land after S49-1 and before S49-2…S49-5. The phase is shaped so that no story waits on a decision it could have been given as a parameter.

**Before the pick, executing unblocked:** S49-0 (docs), S49-1a (naming the ring literals — a pure refactor, no pixel moves, gate-checkable as such), S49-1 (the surface), and each later story's **gate and contract moves**, which under principle 4 have to land first anyway.

**The artefact the owner returns** is the U49 table in §7, filled. ⚠ **It has FIVE columns — `#`, *item*, *candidates*, *chosen*, *defer?* — and the owner fills the two right-hand ones.** r0 described it as three columns, which is not the table §7 prints, and a plan that miscounts its own owner artefact is a plan whose executor will not recognise the artefact when it arrives.

⚠ **The rows must be able to express the outcomes the stories already plan for, and r0's could not.** S49-4 explicitly plans for "take the mark, defer the reveal", and r0 gave that a **single** row with **one** `Defer?` cell — an outcome the story is designed around and the artefact cannot record. It is now two rows (U49-5a / U49-5b). Likewise U49-4's candidates were a slash-separated sentence that does not parse into pairs; they are now numbered triples. **A row that cannot express a planned outcome is how a deferral gets recorded as a decision.**

It is a table and not prose because a prose ruling is what produced `docs/e3/tracker.md`'s W×H-readout misroute, where a scope sentence was read as a binding owner ruling the owner did not remember making.

**Every row's shipped default is one of the candidates offered.** This is not a formality: it makes *"the value we have is the right one"* an available answer that costs the owner one cell, rather than an answer they can only give by rejecting the exercise.

**Fallback if the owner defers a row.** The item stays at its shipped value; the story ships **its contract and gate move only**, with the value unchanged; the plan row is marked `DEFERRED — SHIPPED VALUE STANDS`; and the backlog row is updated to *"compared, kept"* rather than closed. ⚠ **A deferred row must not be recorded as a closed decision** — that is how an unexamined value acquires the authority of a ruling.

**What does NOT block on the owner at all:** `padding-glyph`. The backlog row already carries a decided direction (*"pad 스트립의 글리프를 방향에 맞춘 얇은 일자 바로 교체(가로 변엔 `-`, 세로 변엔 `l`)"*), given by the owner at phase-48's G48-8 pass. It rides the surface for confirmation, not for a decision, and S49-5 can execute on the standing direction if the owner defers.

### D49-4 — S0's archiving scope

> ⚠ **THIS DECISION REVERSES BOTH THE KICKOFF AND THE TRACKER, FROM SOURCE, AND THE REVERSAL IS THE DECISION.** The archiving this phase was told to perform **has already largely happened**, at `8db53ad` (2026-09-01), *"docs(omc): archive the shipped v3 initiative and the closed spikes, with every inbound pointer moved in the same commit"*. It moved the phase-43/44/45/47 ralplans plus three spike trees and the phase-23/38 material, **and it moved 64 pointers across 15 files in the same commit, verified by query**. Two consequences follow and neither is optional.
>
> 1. **The destination is `.omc/archive/260901-e3-v3/`, which EXISTS, not `.omc/archive/260817-e3-v3/`, which does not.** `260817-e3-v3` is the tracker's 2026-08-24 prose written before the move happened; the only `260817` directory on disk is `.omc/archive/260817-e3-v3-consensus/` and it holds the v3 consensus round briefs, not plans. Creating `260817-e3-v3` would split one initiative's archive across two directories on the strength of a stale sentence. **Reproduce: `ls .omc/archive | grep e3-v3`.**
> 2. **The "240 references" framing is the wrong instrument for the remaining work.** The figure is real — `grep -c '.omc/plans/ralplan-' -- . ':!.omc/plans'` sums to **242 occurrences across 154 tracked files at `9473225`** (the brief's 240/153 was measured at `cc6f631`, before the kickoff doc landed) — but it counts every reference to every ralplan ever written, the overwhelming majority of which sit in `docs/handoff/**` and `.omc/archive/**`, are **already** pointing at pre-archive paths, and are **never rewritten** by `docs/README.md#They are point-in-time records and are deliberately **not** rewritten`. Treating 242 as the work item would rewrite exactly the documents the repo's own convention forbids rewriting.

**The pointer census — 11 live pointers across 6 files.** This is the authoritative census for S49-0's rewrite list; **it is a claim about six files that are NOT the allow-listed ones**, and G49-2 works from a PREDICATE rather than from this count (see R14 below and G49-2 itself).

> ⚠ **IT WAS 9 ACROSS 5 UNTIL r4', THE CENSUS WAS CORRECT AS SCOPED, AND THE SCOPE WAS WRONG — WHICH IS THE MORE EXPENSIVE OF THE TWO WAYS TO BE WRONG.** `.omc/archive/README.md` carries **two** live pointers at the moved paths: its own table says one plan is *"APPROVED and live at `.omc/plans/ralplan-e3-v3-direct-manipulation.md`"* and another is *"execution-ready at `.omc/plans/ralplan-phase-42-resize-handles.md`"*. It sat outside the census roots and behind G49-2's `--exclude-dir=archive` on both legs, **and the exclusion's justification was imported from a rule that does not cover it.** `docs/README.md#They are point-in-time records and are deliberately **not** rewritten` exempts ARCHIVED PLANS, as point-in-time records. **This file is not an archived plan and not a record — it is a live INDEX asserting where plans are.** A move invalidates it by construction; it is precisely the file an archiving pass exists to rewrite. The exclusion is therefore narrowed to the archive's CONTENTS, with the index named as a scan root of its own, and the plan does not get to leave a gate asserting *"the move left no live pointer at a moved path"* while two survive in the file that indexes the destination.
>
> ⚠ **AND IT IS ALREADY STALE BEFORE PHASE-49 TOUCHES ANYTHING: it has no `260901-e3-v3/` row at all** (`grep -c '260901' .omc/archive/README.md` → 0) although that directory exists and holds four archived ralplans plus a spike tree. So S49-0 does not merely repair two pointers there; it adds the row the 2026-09-01 pass never wrote.

**Two commands, one per claim, each labelled — because r1' published one command for two claims and it could produce neither.** The published form was `grep -rlnE …`, and **`-l` suppresses `-n`**: it prints filenames only, so the per-file count column beside it could not be regenerated by the instrument printed under it. Confirm for yourself with `grep -rlnE 'ralplan-phase-42-resize-handles\.md' --include='*.md' docs`, which prints bare paths.

```
# THE ROOTS, shared by both commands and by G49-2. Enumerated, not `.` — see the roots reversal below.
# The archive's INDEX is a root; the archive's CONTENTS are not. Written as a positional list here
# for the same reason the script uses one: an unquoted scalar is ONE argument under zsh.
set -- docs .omc/plans .omc/specs .omc/research packages e2e scripts src .omc/archive/README.md

# CLAIM 1 — WHICH FILES carry a pointer (the rewrite list). File list, no counts.
# ⚠ NO `--include` LIST, NEW AT r4'. It was inert on this tree (the census is identical with and
# without it) but it is a blind spot with no upside: this repo puts plan paths in `.json`, `.mts` and
# spec files, and a four-extension allow-list is a filter nobody would notice going stale.
grep -rIlE '\.omc/plans/ralplan-(e3-v3-direct-manipulation|phase-42-resize-handles)\.md' \
  --exclude-dir=node_modules --exclude-dir=archive --exclude-dir=handoff "$@"

# CLAIM 2 — HOW MANY pointers each file carries (the column in the table below). Occurrences, not lines.
grep -rIoE '\.omc/plans/ralplan-(e3-v3-direct-manipulation|phase-42-resize-handles)\.md' \
  --exclude-dir=node_modules --exclude-dir=archive --exclude-dir=handoff "$@" \
  | cut -d: -f1 | sort | uniq -c | sort -rn
```

⚠ **TWO REVERSALS LIVE IN THIS QUERY AND THE EXECUTOR MUST NOT RESTORE EITHER SPELLING.**

1. **The `^\./…` exclusions.** The form this query arrived in anchored them as `grep -v '^\./docs/handoff'` and `grep -v '^\./\.omc/archive'`. Whether `grep -r .` emits a `./` prefix is implementation-dependent — the shim on this machine (`ugrep 7.8.4`, `grep --version`) emits **no** prefix, which makes both filters silently inert and returns the entire `.omc/archive/**` history as live pointers. They are now `--exclude-dir=` on an enumerated root set, which is prefix-agnostic by construction.
2. **The root `.`, NEW AT r2' AND FOUND BY RUNNING THE QUERY RATHER THAN BY READING IT.** Rooted at `.`, this census sweeps `.omc/artifacts/**` — gitignored at `.gitignore`'s `.omc/artifacts/` line, i.e. ephemeral scratch, not repo content — and on this tree it returned **the review artefacts of this planning round** (revision briefs and `ask/codex-*.md` transcripts) as live pointers awaiting repair. ⚠ **No count, deliberately: r2' wrote "four" and the next measurement found five, because the population grows with every lane the round spawns** — the same defect as the row below, one namespace over. Rewriting them would be rewriting the review of the plan that orders the rewrite. **This is instance 5 of `PM-10`, and instance 4's lesson applied one namespace over: the measuring apparatus is inside the measured population.** Enumerated roots drop it for the same reason they drop `docs/handoff/**` and `.omc/archive/**`.

**Output of CLAIM 2 on the r4' working tree** — the two right-hand columns are the reading, not the command's output:

| file | pointers | disposition |
|---|---|---|
| `docs/e3/tracker.md` | 5 | REWRITE |
| `.omc/archive/README.md` | 2 | **REWRITE — the archive INDEX, new at r4'. Not a record; a live table asserting where two plans ARE.** Also gains the missing `260901-e3-v3/` row in the same edit. |
| `docs/architecture.md` | 1 | REWRITE |
| `docs/known-issues.md` | 1 | REWRITE |
| `.omc/research/phase48-strip-band-pricing.md` | 1 | REWRITE (this same decision keeps the file live) |
| `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` | 1 | REWRITE (this same decision keeps the file live) |
| `.omc/plans/ralplan-phase-42-resize-handles.md` | *(unstated — same reason as the row below)* | self-references — they move WITH the file, and are not rewrites. **ALLOW-LISTED (G49-2), not counted in the 11.** |
| `.omc/plans/ralplan-phase-49-comparison-surface.md` | *(unstated — see below)* | this plan's own text. **ALLOW-LISTED (G49-2), not counted in the 11.** |

⚠ **THIS PLAN'S OWN ROW HAS NO NUMBER IN IT, AND THE OMISSION IS THE POINT — instance 4 of `PM-10`, in its purest form.** r1' said this file contributes **2**. The closure audit measured **3**. The lead measured **4**. **All three were right, at three different moments**, because every revision that discusses the archiving adds another mention of the archived paths — and this revision added more. Writing `3` here would reproduce the defect on a one-round delay; writing `4` would too. **The measuring document is part of the measured population**, exactly as the anchor count in this same decision is a function of the tree, and it gets the same treatment: no figure, a predicate instead. G49-2 tests *which file a row came from*, never *how many rows there are*.

⚠ **THE INSTRUMENT FINDING, AND IT IS THE ONE WORTH CARRYING OUT OF THIS SECTION.** Four independent enumerations of this same set produced four different answers (7/4, 8/4, 9/6, 11 occurrences/7 files) before the census settled it at 9/5 — **and r4' moved it again, to 11 across 6, when the archive INDEX entered the root set** (U-9 carries that correction). They did not differ on the facts. **Every enumeration that reached for a `git grep … ':!.omc/plans'` pathspec was blind to the phase-46 pointer BY CONSTRUCTION: the exclusion that hides the plans being MOVED also hides the plan doing the POINTING.** That is the identical shape as the one-sided `toBeLessThanOrEqual(2)` bound in S49-2 — an instrument whose blind spot is exactly aligned with its subject, so it returns the answer you expected and nothing tells you it never looked. **Do not re-introduce the `':!.omc/plans'` exclusion when regenerating this count.** Drop `.omc/archive/**` and `docs/handoff/**` (frozen-record namespaces) and `.omc/artifacts/**` (gitignored scratch), which is what the enumerated `ROOTS` above do, and nothing else. ⚠ **This is instance 1 of the class `PM-10` names, and by r2' there are five of them; §9 carries the full list. It is worth knowing that this section diagnosed the shape correctly and then produced instance 4 nine lines above and instance 5 inside its own published command.**

**CLAIM 3 — what else remains, measured, and it is a DIFFERENT claim about DIFFERENT files.** This one is about the five plans and two specs that STAY, not about the two that move, and it exists only to show that the consumption test's residue is small. Excluding the historical namespaces, their live inbound references are single-digit per file. Reproduce with:

```
grep -rIo --exclude-dir=node_modules --exclude-dir=plans --exclude-dir=archive --exclude-dir=handoff --exclude-dir=.git --exclude-dir=artifacts \
  '\.omc/\(plans\|specs\)/[A-Za-z0-9._-]*' docs packages e2e scripts .omc src | sort | uniq -c | sort -rn
```

**Options.**

- **(A) Move everything the 2026-09-01 pass deliberately kept, now that its reason has expired.** `8db53ad`'s own commit message names the reason: *"WHAT DELIBERATELY STAYS, because phase-48 stands on it: `ralplan-phase-42` …, `ralplan-phase-46` …, `ralplan-e3-v3-direct-manipulation` …, `v3-layout-panel-visual-spec` and the phase-46/48 B-Q5 measurements."* Phase-48 has shipped, so on a literal reading all five become movable. **Against it, decisively:** phase-49 itself consumes `.omc/specs/v3-layout-panel-visual-spec.md` §5.5 and §5.11 as binding contract, and `packages/descvi/src/react/overlay/panel/SizingSection.tsx`, `layout-refusal-messages.ts` and `spacing-refusal-messages.ts` cite it from PRODUCT SOURCE. Archiving a document that a live phase and three shipped source files consume freezes a text that is still being read as current — the exact failure `.omc/archive/README.md`'s frozen-record contract exists to prevent.
- **(B) Move the two clearly-dead v3 plans and nothing else.** `ralplan-e3-v3-direct-manipulation.md` (the v3 ladder, complete, `check-v3-registers.mjs` GREEN with zero `deferred-v3` residue) and `ralplan-phase-42-resize-handles.md` (phase-42 shipped; its §3.12 clause 1 was the ruling phase-48 had to declare a reversal of, and phase-48 declared it). Live referrers: **11 pointers across 6 files** — the census is below and it is the list S49-0 works from; G49-2 works from a predicate and from no number at all. Everything else stays.
- **(C) Move nothing; write only the tracker record.** Cheapest and defensible on the grounds that nothing is broken, but it leaves the tracker's archiving deferral open for a third phase and the deferral has now survived two closes.

**CHOSEN: (B), with one addition — the tracker's stale deferral paragraph is REPLACED, not left standing.**

**Reason (the strongest available, not the first).** The archiving deferral was never about tidiness; the tracker says what it was about — *"phase-46/47 planning still consumes the parent plan and the visual spec; moving the files now buys nothing and breaks every path."* That is a **consumption test**, and it is the test that should decide each file, one file at a time. Applied now it separates the five cleanly: the v3 ladder and phase-42 have no live consumer (their live referrers are all backward-looking records in `docs/`, which is what an archive pointer is FOR); the visual spec, the phase-46 plan and the phase-48 plan each have at least one consumer that is not a record — this very plan for the spec, `.omc/research/phase48-strip-band-pricing.md` for phase-46, and three *source* files under `packages/descvi/src/react/overlay/` plus a test for phase-48. Option (A) fails the test it inherited; option (C) declines to apply it. And the tracker paragraph must be replaced rather than merely satisfied, because a satisfied deferral that still reads as open is how this item survived phase-47 and phase-48 untouched.

**Consequence stated up front, in `8db53ad`'s own idiom — and THIS IS THE ONE HOME FOR THE ANCHOR COUNT.** The citation gate excludes `.omc/archive/**`, so moving two large plans drops the gate's checked-anchor count.

```
node scripts/check-citation-anchors.mjs      # leg (b): "N citation(s) checked, 0 violation(s)"
```

| tree | leg (b) count |
|---|---|
| `9473225`, r0 plan text present | **600** |
| `9473225` working tree, **r1' plan text present** | **610** — this revision cites ten more anchors than r0 did |
| `9473225` working tree, **r3' plan text present** | **636** (`scanned 342 files`, 0 violations) — r3' adds the C49-2 keybinding anchors and the two bootstrap/build anchors behind the `dist/` reversal |

⚠ **THE COUNT IS A FUNCTION OF THE TREE, WHICH IS PRECISELY WHY IT GETS ONE HOME AND A COMMAND.** r0 stated it in three places with three values — 600 in the status block, 599 in §11, 556 here — and 556 was measured before this plan file existed, by a command that no longer produces it, while S49-0 was told to compare against it. **Nowhere else in this plan states an anchor count.** ⚠ **AND NEITHER NUMBER IN THE TABLE ABOVE IS THE ONE S49-0 COMPARES AGAINST**: this plan file will be edited again before S49-0 runs, and every edit moves the count. **S49-0 re-derives the pre-move number immediately before the `git mv`, in the same working tree**, records both it and the post-move number in the commit message, and treats the table above as a record of two past measurements rather than as a target.

**What S0 does NOT move, each with its pin:**

| File | Stays because |
|---|---|
| `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` | §8 carries phase-48's inheritance; `.omc/research/phase48-strip-band-pricing.md` and `docs/known-issues.md` consume it. Archive it when phase-48 is archived, as one set. |
| `.omc/plans/ralplan-phase-48-handle-admission.md` | Cited from PRODUCT SOURCE (`packages/descvi/src/react/overlay/canvas/handle-geometry.ts`) and from tests. Moving it edits shipped source for a docs reason. |
| `.omc/plans/open-questions.md` | Cross-phase living register; `8db53ad` already ruled it stays and gave the reason (*"Archiving it would have frozen the one file built not to freeze"*). Not re-opened. |
| `.omc/specs/v3-layout-panel-visual-spec.md` | Consumed by THIS phase (§5.5, §5.11) and by three product source files. |
| `.omc/specs/interaction-ontology.md` | Consumed by `scripts/check-v3-registers.mjs`, i.e. by a running gate. |
| `.omc/research/phase46-*`, `.omc/research/phase48-*`, `.omc/spikes/phase48-model/` | The re-runnable probes behind phase-46/48's measurements; they move with the phase-48 set, not with v3. |

## 4. Contracts

Each is one sentence an executor can implement without guessing.

- **C49-1 — One record per furniture family.** Every look value a phase-49 story can change is a named field of exactly one exported constants record for its family, and no painter reads a bare literal for such a value.
- **C49-2 — One override reader, and it MAY participate in the re-anchor path.** Exactly one module in `packages/descvi/src/react/overlay/` mentions the comparison override, its whole body sits inside `import.meta.env.DEV`, and every painter receives already-merged constants rather than consulting the override itself.
  ⚠ **AMENDED AT r1' — the r0 wording forbade the one thing that makes the surface work.** Both ring paints and the spacing pass are effect-driven with explicit dependency arrays: `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#}, [placeSelectionRing, reanchorRef, stateMap, deviceMode, dim, collapsed, dark, tick]);` and its spacing twin `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts#}, [placeAffordances, reanchorRef, stateMap, deviceMode, dim, collapsed, dark, tick]);`. **The good news is that the constants are read INSIDE the pass, so nothing caches them — U-2's caching fear is unfounded. The bad news is that mutating a module-level record triggers no pass AT ALL**, because no dependency changed. Only the reorder indicator repaints unaided, since `paintReorderOverlay` runs per `pointermove`. **So the override needs a re-render channel, and the channel is the existing remeasure `tick`** — it already sits in every one of those dependency arrays and in the hover path's. C49-2 therefore PERMITS the override reader to bump `tick` (or to expose a callback the shell binds to it); what it still forbids is a painter consulting the override directly. ⚠ **The bump must be reachable from the KEYBOARD**: reaching for a pointer control to switch a value extinguishes the hover ring and ends the drag — it destroys the subject being compared (D49-1's second reason).

  ⚠ **AND THE KEY IS NAMED HERE, AT r2', BECAUSE THE KEY SPACE IS OCCUPIED AND "a keyboard binding" IS NOT A SPECIFICATION AN EXECUTOR CAN SAFELY FILL IN.** The overlay's keydown owners were enumerated from source. **Escape** terminates the reorder drag (`packages/descvi/src/react/overlay/canvas/use-reorder-drag.ts#      if (e instanceof KeyboardEvent && e.key === "Escape") terminate("escape");`), ends the reorder mute, cancels the spacing-drag popup (`packages/descvi/src/react/overlay/canvas/use-spacing-drag.ts#      if (live === null || e.key !== "Escape") return;`) and deselects at the canvas shield. **Enter** commits the spacing popup and every panel field. **Cmd/Ctrl+Z** is undo (`packages/descvi/src/react/overlay/OverlayShell.tsx#      if (!(event.metaKey || event.ctrlKey) || event.shiftKey || event.key.toLowerCase() !== "z") return;`). **And the worst of them: a BARE Meta or Control keydown re-targets the hover preview deepest↔parent** — `packages/descvi/src/react/overlay/canvas/use-canvas-hover-ring.ts#      if (e.key !== "Meta" && e.key !== "Control") return;`, whose own docblock states the mechanism at `packages/descvi/src/react/overlay/canvas/use-canvas-hover-ring.ts# * The modifier is tracked on mousemove AND via document keydown/keyup of Meta/Control, so pressing/releasing Cmd with the pointer stationary re-evaluates the preview against the last pointer target.`. **That one does not extinguish the comparison subject; it silently CHANGES it** — the owner would be comparing two values on two different elements and nothing on screen would say so. **That is worse than losing the subject, and it disqualifies every modified binding, not only Cmd+Z.**

  **RULED: the channel is the bare, unmodified `[` and `]` keys** — previous candidate / next candidate — **and the ruling now ships with a text-entry guard as CONTRACT, because the key is NOT free.** ⚠ **One document-capture listener does fire on every keydown and was checked rather than assumed**: `packages/descvi/src/react/overlay/OverlayShell.tsx#    const advance = () => { canvasOwnershipGenerationRef.current += 1; };` bumps a generation counter, but its only consumer is the deferred focus-restore ticket (`packages/descvi/src/react/overlay/OverlayShell.tsx#    if (canvasOwnershipGenerationRef.current !== ticket.generation) return;`), which stales a stage-refocus and touches no gesture. **A candidate switch is therefore free of it.**

  ⚠ **AND HERE IS WHAT r2' GOT WRONG, REVERSED AT r3': `[` IS OCCUPIED, AND THE PLAN'S OWN RISK REGISTER RECORDED THE HAZARD BACKWARDS.** r2' ruled the brackets free on `grep -rn 'key === "\[\|key === "\]\|BracketLeft\|BracketRight' packages/descvi/src src e2e` → empty. **That grep measures handlers that COMPARE `e.key` to a bracket. The real consumer is TEXT ENTRY.** `packages/descvi/src/react/overlay/panel/ClassNameChipEditor.tsx#              // A space commits the pending token UNLESS it is inside an unbalanced bracket/quote (an arbitrary value being typed) — tokenize decides.` reasons explicitly about an unbalanced bracket because `[` opens a Tailwind arbitrary value, and the dogfood corpus is full of them — **251 arbitrary-value token occurrences, 39 distinct, across 155 `className` attributes** (`grep -rIoh 'className="[^"]*"' --include='*.tsx' src/app | grep -o '[a-zA-Z0-9:/_.-]*\[[^]]*\]' | wc -l`, and the same pipeline through `sort -u | wc -l`). **And both of OverlayShell's document keydown listeners are registered with `{ capture: true }`** — `packages/descvi/src/react/overlay/OverlayShell.tsx#    document.addEventListener("keydown", advance, { capture: true });` and `packages/descvi/src/react/overlay/OverlayShell.tsx#    document.addEventListener("keydown", onKeyDown, { capture: true });` — so a capture-phase bracket handler takes the character **before the field ever sees it**. Typing `w-[200px]` into the className chip editor would eat the `[`, and would also fire a candidate switch nobody asked for.

  **CONTRACT (not a review note): the switch handler carries the repo's own established text-entry guard, copied rather than invented.** The line to copy is `packages/descvi/src/react/overlay/OverlayShell.tsx#      if (active.closest("input, textarea, select, [contenteditable], [role=\"textbox\"]") !== null) return;`, inside the undo handler's own keydown listener.

  ⚠ **AND THE ANCHOR MATTERS HERE MORE THAN ANYWHERE ELSE IN THIS PLAN, BECAUSE r2' AND r3' BOTH POINTED IT AT A COMMENT THAT ARGUES THE OPPOSITE.** The citation used to be `packages/descvi/src/react/overlay/OverlayShell.tsx#  // A text-entry guard mirroring the sibling`, which resolves to `focusStageIfOwned`'s docblock — a passage whose own sentence says a text-entry guard mirroring the sibling *"was actually BUILT and rejected"*, on a cost table about focus restoration that has nothing to do with a candidate switch. **The claim was true and the pointer was wrong**: the undo handler does carry the guard, but the plan never anchored the line that carries it, and the citation gate stayed GREEN the whole time because the cited text is unique. **An executor who opened that anchor read an argument against the contract they had just been told to implement.** This is `AGENTS.md`'s named failure verbatim — *confirming a line is there is not confirming it is the one that runs* — and the repair is to cite the guard itself. The rejected-guard docblock is still worth reading, but as a different claim: it is why the FOCUS-RESTORE path does not carry one, and it is cited for that and only that at `packages/descvi/src/react/overlay/OverlayShell.tsx#  // A text-entry guard mirroring the sibling`. **Plus `event.isComposing`**, which every panel field in this tree already honours (`packages/descvi/src/react/overlay/panel/ClassNameChipEditor.tsx#                  if (e.nativeEvent.isComposing) return;` is one of two in that file alone) and whose gate precedent is `packages/descvi/src/react/overlay/__tests__/ime-composition-guard.test.tsx#describe("instrument control — jsdom can produce both spellings of the composition flag", () => {`.

  ⚠ **AND THE IME HALF IS NOT A COURTESY — IT IS THE CHANNEL BEING DEAD IN THIS PROJECT'S PRIMARY INPUT MODE.** Under an active Korean IME the `e.key` for the physical bracket key is not `"["` at all, so the switch simply does not fire. S49-P leg (5) tests this with the IME **on** as well as off, and if the guard is judged fragile the fallback is decided here and not mid-story: **bind a non-printable key instead** — `F2` / `F3`, which no text field consumes and which `grep -rn 'key === "F2"\|key === "F3"' packages/descvi/src src e2e` finds no handler for. ⚠ **That is a NEGATIVE with no positive control available** — nothing in the tree binds a function key, so the grep cannot be shown able to return non-zero for these two; read it as "no binding found", exactly as U-15 now reads for the brackets. S49-P's result chooses between the guarded bracket and the function key; the plan does not leave "a keyboard binding" as the specification.
- **C49-3 — Hover and selection are ONE parameter set with two members, never two unrelated literals.** Any value that both rings carry (today: `borderRadius`, written twice as `6px`) is a single field consumed by both writers, so that a change to one cannot silently fail to reach the other; values that legitimately differ (width, shade, z) are two named fields of the same record, not two literals in two functions.
  ⚠ **THIS IS A COUPLING CONTRACT, NOT A LOOK GUARANTEE, and the difference is visible on screen.** The hover ring's radius applies to a box **inflated 2 px per side**; the selection ring's applies to the element's exact box. **So one shared radius field renders as two apparent curvatures.** C49-3 guarantees the two radii cannot silently diverge — which is a real defect today, since nothing would notice. It does not guarantee they look identical. If the owner wants them to LOOK the same, that is a second field (a hover-radius offset), decided on the surface like any other candidate, not a bug in this one.
- **C49-4 — The shipped default is the record's default.** The value that ships is written in exactly one place and is the value a production build reads with no override present; a candidate value never becomes the default by being left selected.
- **C49-5 — A LOOK change moves its gate first, in its own commit — AND IT BINDS THE FINAL VALUE COMMIT ONLY.** Where a gate asserts the look being changed, the contract and gate amendment land in a commit with no pixel change, and the look lands in a commit with no gate edit — the S46-1/S46-2 split, applied per item. There is never a commit in which a gate asserts the old look on the new rendering.
  ⚠ **WHICH REGIME THE PHASE IS IN — ruled here, once, so an executor does not have to guess it mid-loop.** Driver D-B prices out any form whose every edit re-pins gate assertions; this contract mandates a contract-first split per look change on families whose look IS pinned. **Both cannot govern the candidate-trying loop, and that loop is the phase's whole point.** The rule: **a candidate tried on the override is UNGATED, and C49-5 does not apply to it.** Trying 3 px, then 4 px, then 3 px again on the live surface is not a look change — nothing is committed, no default has moved, and every gate still asserts the shipped value truthfully because the shipped value is still what it asserts. **C49-5 binds the FINAL value commit**: the one that changes a record's default after the owner's table is filled. That one splits, contract-first, in its own commit. This is the single reconciliation of D-B and C49-5, and it is stated here rather than in a story because an executor reads the contracts before the story they are about to run.
- **C49-6 — A deferred item ships its gate move and its shipped value.** Owner deferral changes what value ships, never whether the story lands.
- **C49-7 — Phase-49 does not disturb C48-1.** The corner chip stays `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts#const chipPx = Math.min(HANDLE_CHIP_PX, cornerSizeFor(box, DEFAULT_HANDLE_GEOMETRY));` painted on the vertex, and no root is translated. ⚠ **The one place this phase can break it without touching phase-48 code**: the chip's border is `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts#1.5px solid ${deep}` and takes the SAME `deep` shade as the selection ring, which spec §5.5 binds and which, after S46-2, is the only group colour on a handle at all. A `selection-ring-treatment` change that alters the `deep` shade — as opposed to the ring's width or radius — moves the chip border's contrast with it, including the two light-mode ratios §5.5 records as marginal. **Width and radius changes to the ring do not touch the chip; a shade change does.** A story that proposes a shade change owes §5.5 a re-measurement on its own probe; the width and radius candidates in §7 are chosen so that this phase does not have to.
- **C49-8 — The comparison surface is not shipped UI, and the artefacts that prove it are named rather than called "production".** ⚠ **descvi ships as source** — `packages/descvi/package.json`'s `build` is an `echo` no-op, so there is no published descvi bundle at all. What the repo emits is **two** Vite bundles over the same `src/app/**`: `pnpm descvi:build` → `dist-designview/` (design-view, overlay on) and `pnpm build` → `dist/` (the plain prototype view).

  ⚠ **BOTH ARE SUBJECTS, AND THIS REVERSES WHAT r1' AND r2' SAID — MEASURED AT r3' BY BUILDING `dist/` AND GREPPING IT.** The plan asserted through two revisions that `dist/` *"contains no overlay to leak into"* because `vite.config.mts` mounts the plugin `overlay: false`. **It does contain the overlay.** `overlay: false` is a **runtime branch**: `packages/descvi/src/vite/bootstrap-entry.ts#import DescviOverlay, { type ManifestMap } from '../react/DescviOverlay';` is an unconditional module-scope import and the flag only selects which tree the generated bootstrap renders, so Rollup keeps the whole overlay graph. Reproduce: `grep -RIlF -e dsh-selection-ring -e data-dsh-ring-key -e pad-x dist/` → all three overlay-only strings present in `dist/assets/index-*.js`. **What r1' actually measured was an identifier grep, and esbuild mangles identifiers in every bundle** — so its zero in `dist/` was the mangling, not the absence, and the conclusion drawn from it was `PM-10` one level up. **The contract therefore names both bundles, and G49-4 builds and scans both.** Restricting the gate to `dist-designview/` would have left the bundle `vite.config.mts`'s own docblock calls *"the deliverable"* unguarded.

  The contract is therefore: no code path reachable without `import.meta.env.DEV` mentions the override, and the override's **string literal** is absent from `dist-designview/` **and** from `dist/`, proven by G49-4 against both directories rather than argued from a guard's presence in source.

  ⚠ **THE GREPPED ARTEFACT IS A STRING LITERAL, NOT AN IDENTIFIER, AND THIS IS THE CONTRACT'S OPERATIVE CLAUSE RATHER THAN A GATE DETAIL — MEASURED AT r2'.** There is **no `minify` key** in `vite.config.mts`, in `descvi.vite.config.mts` or anywhere under `packages/descvi/src/vite/`, so the design-view build takes Vite's esbuild default, which mangles every non-exported identifier. **Run on this tree: a planted reader named `readDescviLookOverrideProbe` came out of the bundle as `vM` and `grep -RIl 'readDescviLookOverrideProbe' dist-designview/` found nothing; the same plant's literal `"descvi-look-override"` survived byte-for-byte.** A gate that greps for the reader's NAME therefore returns the identical zero with and without the leak — the `PM-10` shape, one level down from the bundle mistake r1' fixed. **So C49-8 obliges the override reader to CARRY a stable string literal, and at r3' the literal is NAMED rather than shaped: it is exactly `descvi-look-override`**, a `localStorage` / `window` key, and G49-4 greps that byte string. **The name of the module, the hook or the field is not the artefact and must not be greppable in place of it.**

  ⚠ **"A STRING OF THE SHAPE `descvi-look-override`" IS NOT A PIN, AND THAT WAS THE DEEPEST HOLE IN r2' — CLOSED AT r3'.** r2' bound *identifier vs literal* and left *which literal* free. Nothing anywhere asserted the string occurred in source at all. **So if S49-1's executor writes `descviLookOverride`, or `descvi:look-override`, or assembles the key from a template, G49-4 is GREEN forever having never looked at its subject** — and the harm this phase exists to prevent (a candidate value shipping as if it were decided) lands unwatched. **The closure is G49-4's leg 0: the literal must occur in EXACTLY ONE file under `packages/descvi/src/react/overlay/`.** C49-2's single-reader rule already makes that a one-site claim, so the leg costs nothing and it is what ties source and bundle to the same string. **Before S49-1 lands the reader, leg 0 is RED by construction — there is no subject yet — and that is the correct reading, not a false alarm.**

## 5. Stories

### S49-0 — the v3.5 close (docs only)

**Lands.**
- `docs/e3/tracker.md` — the missing **phase-48 section**, in the shape phase-45/46/47 already use: a heading of the form *"### phase-48 — v3.5 B-Q5, the resize-handle admission model replaced by C48-1 — SHIPPED …"*, a `Plan:` routing line to `.omc/plans/ralplan-phase-48-handle-admission.md`, a one-paragraph *What shipped*, and the per-story record **S48-0a / S48-0b / S48-1 / S48-2 / S48-3 / S48-4 / S48-5**. ⚠ **The substance does NOT move here** — it stays in the plan, the commit messages and `docs/handoff/260902-phase-48-close.md`, per the close's own rule (*"This file carries only what is not already in the plan, the commit messages or the backlog"*). This section is a routing note plus the story ledger. It records that S48-5 exists because a live pass overturned D48-7 (iii) on the spot, because that is a per-story fact the plan's pre-execution text cannot carry.
- `docs/e3/tracker.md` — the v3 CLOSE section's archiving paragraph, **replaced** (see D49-4) by a dated closure recording what moved, what stayed and the consumption test that decided each.
- `git mv .omc/plans/ralplan-e3-v3-direct-manipulation.md .omc/plans/ralplan-phase-42-resize-handles.md .omc/archive/260901-e3-v3/`
- `.omc/archive/README.md` — **the archive's INDEX, two edits in the same commit.** (i) The two rows asserting that a plan is *"APPROVED and live at"* / *"execution-ready at"* a moved path are rewritten to the archived paths. (ii) **The missing `260901-e3-v3/` row is added**, in the table's existing shape, naming the four ralplans and the spike tree that directory already holds — it has had no row since the 2026-09-01 pass created it. ⚠ **This file is NOT exempt as a frozen record and the plan says why where an executor will read it:** `docs/README.md#They are point-in-time records and are deliberately **not** rewritten` exempts archived PLANS; an index that asserts where plans are is the opposite of a point-in-time record, and it is the one file whose whole job the move invalidates.
- **The 11 live pointers across 6 files** — `docs/e3/tracker.md` (5), `.omc/archive/README.md` (2), `docs/architecture.md` (1), `docs/known-issues.md` (1), `.omc/research/phase48-strip-band-pricing.md` (1), `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` (1) — rewritten **in the same commit** as the `git mv`. This is `8db53ad`'s rule, and the debt it names (three pointers dead since an earlier pass) is what happens when they are not. ⚠ **THREE of the six live in `.omc/`, not `docs/`** — `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md`, `.omc/research/phase48-strip-band-pricing.md` and `.omc/archive/README.md` — **and each of the two enumerations that undercounted was blind to one of them**: a `':!.omc/plans'`-shaped pathspec cannot see the phase-46 plan, and `--exclude-dir=archive` could not see the archive INDEX until r4' narrowed it to the archive's CONTENTS. D49-4's instrument finding. The rewrite list is D49-4's census table and nothing shorter. **The moved files' self-references travel with them and are not rewrites, and this plan's own mentions stay — both by G49-2's allow-list PREDICATE, which is a test on which file a row came from and states no count for either.** ⚠ **Do not "fix" this by writing down how many mentions this plan carries: the number was 2 at r1', 3 at the closure audit and 4 at r2', all three correct, and the next edit moves it again (PM-10 instance 4).**

- ⚠ **`scripts/gate-g49-2-archive-pointers.sh` IS COMMITTED BY THIS STORY AND WIRED INTO CI, AND THAT IS AN ITEM IN THE LANDS LIST RATHER THAN AN ASSUMPTION.** r3' wrote the script, ran it, and left it untracked, named in no story and run by nothing in `.github/workflows/ci.yml` — which `AGENTS.md` calls the gate set. Two steps go into that job's `verify:` steps, beside the two audit gates that already use this exact idiom (`Audit gate — citation anchors selftest (proves the gate can fail)` and the gate step under it), placed after `Lint` and before `Build`:

  ```
      - name: Audit gate — phase-49 archive pointers selftest (proves the gate can fail)
        run: sh scripts/gate-g49-2-archive-pointers.sh --selftest
      - name: Audit gate — phase-49 archive pointers (G49-2)
        run: sh scripts/gate-g49-2-archive-pointers.sh
  ```

  ⚠ **THE BLOCK IS PASTEABLE AS WRITTEN AND THAT IS DELIBERATE — 6-SPACE `- name:`, 8-SPACE `run:`, matching every step already in that job, and `Audit gate — ` as the prefix all four of this phase's steps use** (r4' indented these 2/4 and split the prefix between two spellings; both resolved at wiring time and neither should have to). ⚠ **AND EVERY `run:` IS A SINGLE-LINE SCALAR, WHICH IS A HARD REQUIREMENT RATHER THAN A HOUSE STYLE:** `scripts/gates.mjs` parses this job with a deliberately narrow line scan and **treats a block scalar (`run: |`) as a parse error** — its own docblock says it should fail loudly and be extended rather than guess. A multi-line step here breaks `pnpm gates` for the whole repo, not just for this gate.

  **The selftest step is not decoration**: it stages its own fixture — a live pointer at a moved path, the same pointer inside the archive INDEX, a dangling archive citation, a dead fragment, and four silent controls — and asserts all three verdicts **and the gate's own scope**, so the gate is proven able to fail on every CI run rather than in one planning session's transcript. Cost: both steps together are well under a second (measured at r5: the gate's three legs over nine roots run in **0.56 s** wall on this machine, the selftest in **0.08 s**).

  ⚠ **AND `pnpm gates` PARSES THIS SAME JOB, SO THESE TWO STEPS JOIN THE COMMAND AN EXECUTOR ACTUALLY TYPES — WHICH `AGENTS.md` MANDATES PER COMMIT.** The plan prices CI in three places and had priced the local loop in none. For G49-2, G49-3 and G49-5 the local addition is noise (**0.56 s + 2.9 s + 0.34 s** wall at r5, plus **0.08 s + 2.2 s + 0.50 s** for their selftests). **G49-4 is the one that is not noise, and S49-1 states it where its executor meets it.**

**Done when.** `node scripts/check-citation-anchors.mjs` (G49-1) is GREEN **and `sh scripts/gate-g49-2-archive-pointers.sh` exits 0, and `sh scripts/gate-g49-2-archive-pointers.sh --selftest` exits 0, and both steps are in `.github/workflows/ci.yml`'s verify job** — ⚠ **it exits 1 before the move, with leg (a) printing the rewrite list, so a run that is still RED after the commit means a pointer was missed and not that the gate is noisy**; `pnpm gates` green; `git diff --exit-code .descvi/screens.json` clean (S49-0 touches no source, so an artifact diff here is a defect and not a deliverable).

**Owner input needed.** None. S49-0 is the one story that executes before the mid-phase gate and it does not wait on anything.

### S49-P — the live-switch spike (a numbered PRE-STORY with an abort condition, not a register entry)

> ⚠ **r0 called this "the highest-value pre-execution check in the phase" and then scheduled nobody to run it.** A check that lives only in an UNVERIFIED register is a check nobody owns; it becomes a story here so that it has a runner, a moment, and a stated consequence for failing.

**When.** After S49-0, **before S49-1a**. Nothing downstream of D49-1 is safe to build until it passes.

**Scope — deliberately one of everything, so a failure is attributable.** ONE constant (the reorder indicator's thickness, because it is the only family whose painter is already callable and already repaints per `pointermove` — the cheapest possible subject), ONE override, ONE drag, in a running `pnpm descvi:dev`.

**What it must show, in order.**
1. With the override set, the value the live canvas paints is the override's value, **without a reload**.
2. The value can be switched **from the keyboard, mid-gesture, on the bare `[` / `]` keys C49-2 names**, and the newly-painted value appears on the same gesture (C49-2's amended `tick` channel — this is the leg the architect's probe says nothing currently provides). ⚠ **The key is not the spike's to choose.** C49-2 enumerates the overlay's keydown owners and rules `[` / `]` free; the spike CONFIRMS that in a browser. If the spike wants a different key it must re-run that enumeration and say why, in writing, before using it.
3. Switching does **not** extinguish the subject: the drag survives, and on the ring family the hover ring survives a switch.
4. ⚠ **Switching does not CHANGE the subject either, which is a distinct failure and the one that hides.** With the pointer stationary over an element, pressing the switch key must leave the hover preview on the same node. A bare **Meta or Control** press re-targets it deepest↔parent (C49-2's citation), so a binding that reaches the modifier state at all makes the owner compare two values on two different elements with nothing on screen saying so. The spike checks this explicitly, on the ring family, by reading the previewed node's oid before and after.

5. ⚠ **TEXT ENTRY SURVIVES THE BINDING — NEW AT r3', AND IT IS THE LEG THE `[` RULING WAS MISSING.** With the className chip editor focused, type `w-[200px]` and confirm **the text lands intact and no candidate switch fires**. Both of OverlayShell's document keydown listeners are `{ capture: true }`, so an unguarded bracket handler eats the `[` before the field sees it, and the dogfood corpus carries 251 arbitrary-value token occurrences that need one (C49-2). **Run it with the IME ON as well as off**: under an active Korean IME the `e.key` for that physical key is not `"["` at all, so the switch channel is simply dead in the input mode this project is built to support, and that is a different failure from the guard misfiring. `packages/descvi/src/react/overlay/__tests__/ime-composition-guard.test.tsx#describe("instrument control — jsdom can produce both spellings of the composition flag", () => {` is the precedent for how this repo proves the jsdom half; the browser half is this leg's.

**ABORT CONDITION — stated before any code lands, because it reopens a decision and not just a story.** If (1) fails, or if (2) can only be achieved by a pointer control, or if (3) shows that switching kills the subject being judged, **or if (4) shows that the only free key changes the subject**, then **D49-1 REOPENS**: (b) has lost the property it was chosen for and the phase returns to the owner with the spike's result before S49-1a is written. ⚠ **AND A REOPENED D49-1 MUST NAME WHAT THE OWNER WOULD BE CHOOSING BETWEEN, BECAUSE ON r3''s TEXT THE OPTION SET WAS EMPTY.** (a) is disqualified structurally (three of four painters are module-private) and (c) is INVALIDATED as not an answer to the question, so "the phase returns to the owner" pointed at a table with no surviving row — and "an owner conversation" is an intent, not a mechanism. **The three candidates a reopened D49-1 actually offers, stated now so the conversation has a shape:** **(b′)** keep the live override and accept a RELOAD per candidate — the surface survives, the mid-gesture property does not, and the owner judges the transient three from memory again, which is the instrument that already failed; **(a′)** take (a) for the reorder indicator ALONE — it is the one family with a callable painter, so a gallery costs no export there, and the other three items park with their backlog rows updated to *"surface attempted, blocked"*; **(z)** park the whole comparison surface and ship S49-0 + S49-1a + S49-5's standing direction, which is PM-6's floor and is a real outcome rather than a failure. **All three are worse than (b) and all three are executable**, which is the property a reopened decision needs and the property r3' left it without.

⚠ **LEG (5) IS THE ONE THAT DOES NOT ABORT, AND SAYING SO IS WHAT KEEPS IT FROM BEING SKIPPED.** A leg whose only outcome is "stop the phase" gets run defensively; leg (5) has a cheap, already-decided branch — if the guarded bracket loses text or the IME kills the channel, **the binding moves to the function key C49-2 names**, the spike re-runs legs (2)(3)(4) on it, and nothing about D49-1 is reopened. What leg (5) must NOT do is pass by not being run: the value it protects is a text field the owner will be typing in *while* comparing candidates.

**Lands.** Nothing permanent. The spike's diff is discarded; its OUTPUT is a recorded result — which of (1)(2)(3) held, on which screen, at which commit — and that result is what S49-1 is written against.

**Owner input.** None to run it. Owner input becomes necessary only if it aborts.

### S49-1a — name the ring's look values (pure refactor, no pixel moves)

**Why it is its own story.** D49-0 fact 2: the ring has no constants. Until it does, nothing about `selection-ring-treatment` can be parametrised, gated or compared.

**Lands.** `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts` — a constants record carrying selection width, selection radius, hover width, hover inflation and the two z values; `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#function applyRingStyle(node: HTMLElement, box: RingBox, color: string): void {` and the hover path both read it. **C49-3 applies here**: the radius becomes ONE field consumed twice.

- ⚠ **THE FOUR FIELD SPELLINGS ARE PART OF THIS STORY'S LANDS, NOT A GATE DETAIL — `selectionWidthPx`, `selectionRadiusPx`, `hoverWidthPx`, `hoverInflatePx`, EACH A FLAT KEY OF THE RECORD.** C49-1 requires only *"a named field of exactly one exported constants record"*, and G49-5 greps those four exact spellings (§6's home-form column). **So an executor who nests them — `selection: { widthPx: 2.5 }` — satisfies the contract, moves no pixel, passes every witness, and leaves the gate permanently at `homes=0` for four of its five rows.** The gate would be RED on a correct refactor and the only repair a reader would find is to edit the gate. **The spellings are the contract here; if a later story wants a different shape, it moves §6's column in the same commit (C49-5's discipline, applied to a gate rather than to a look).**
- ⚠ **AND THE BARE LEG READS COMMENTS, SO THE DOCBLOCK THIS REFACTOR WANTS TO WRITE IS THE ONE THING IT MUST NOT.** G49-5's bare legs are `grep -F` over the whole overlay tree with no comment stripping, so a line explaining the retired literal — *the* natural thing to write beside a "we used to write `borderRadius = "6px"` twice" refactor — turns its field's row RED, and in a repo this comment-dense the only repair left is to delete the explanation. **Describe the retired value ("the two independent 6 px radius writes"), never spell its literal form.** One sentence, so it is not discovered by a gate failing on a comment.

- ⚠ **G49-6 LANDS HERE, AND THAT IS WHERE IT BELONGED ALL ALONG — IT HAD NO OWNER FOR FOUR REVISIONS.** G49-6 is the unit assertion that the two rings' radius comes from ONE field: mutate the field, assert BOTH computed radii moved. **This story is what creates that field**, so this is the only story in the phase where the assertion is both writable and meaningful — before it, there is no field; after it, the coupling is already load-bearing and an assertion added later is a claim about code nobody re-read. It is C49-3's only mechanism, and C49-3 states a defect that exists TODAY, before any experiment: two independent `6px` literals that nothing would notice diverging.
- ⚠ **`scripts/gate-g49-3-look-witnesses.sh` AND `scripts/gate-g49-5-one-home.sh` ARE COMMITTED BY THIS STORY AND WIRED INTO CI.** Both are the instruments this story's own claim rests on — G49-3 that no pixel moved, G49-5 that the record it creates has exactly one home per field — and neither was tracked or scheduled before r4'. Four steps go into `.github/workflows/ci.yml`'s `verify:` job, each gate preceded by its `--selftest`, in the shape the two audit gates already there use:

  ```
      - name: Audit gate — phase-49 one-home selftest (proves the gate can fail)
        run: sh scripts/gate-g49-5-one-home.sh --selftest
      - name: Audit gate — phase-49 one home per look field (G49-5)
        run: sh scripts/gate-g49-5-one-home.sh
      - name: Audit gate — phase-49 look witnesses selftest (proves the gate can fail)
        run: sh scripts/gate-g49-3-look-witnesses.sh --selftest
      - name: Audit gate — phase-49 look witnesses (G49-3)
        run: sh scripts/gate-g49-3-look-witnesses.sh
  ```

  **Same two properties as S49-0's block and for the same two reasons**: 6/8 indentation and the `Audit gate — ` prefix so it pastes rather than gets adapted, and every `run:` a single-line scalar because `scripts/gates.mjs` treats a block scalar as a parse error. **These four steps also enter `pnpm gates`** — measured at r5, they add **2.9 s + 0.34 s** for the two gates and **2.2 s + 0.50 s** for their selftests to every local run.

  ⚠ **G49-3 DUPLICATES WORK CI ALREADY DOES AND IS STILL WORTH ITS SECONDS**, and the plan says so rather than letting a reviewer discover it: its seven witnesses run inside `Test (per-package)` too. What the separate step buys is the WITNESS LIST as a named object — a renamed witness turns this step RED at its precondition (exit 2) instead of quietly shrinking the set some other step happens to cover. Measured cost: **2.9 s wall** for the seven files on this machine at r5 (3.67 s at r4'; vitest's own reported duration was 2.18 s), and the runner is ~4.8× slower on vitest per this job's own measured note, so budget ~20 s. G49-5's own cost is a handful of greps.

**Done when.** Every existing assertion passes **unedited** — in particular `packages/descvi/src/react/overlay/__tests__/OverlayShell-selection-set.test.tsx#border: '2.5px solid rgb(234, 88, 12)',`, `packages/descvi/src/react/overlay/__tests__/OverlayShell-selection-set.test.tsx#borderRadius: '6px',`, the hover width rows in `OverlayShell-canvas-hover.test.tsx`, and **the five geometry rows in `OverlayShell-hover-channels.test.tsx`** (which r0 did not name anywhere). **A gate edit in this commit is a defect**, exactly as at S46-1.

⚠ **ONE LEG OF THAT SENTENCE IS WEAKER THAN THE SENTENCE, AND IT IS THE HOVER WIDTH SPECIFICALLY.** The hover-width assertions are `toContain` substring tests — `packages/descvi/src/react/overlay/__tests__/OverlayShell-canvas-hover.test.tsx#    // to rgb(). Solid, thin (1.5px).` — the two `expect(border).toContain('1.5px')` rows it heads (the anchor is on the comment because the assertion text occurs twice in the file), which pass on `'11.5px'`. That is not this phase's defect and no U49-4 candidate triple produces such a value, **but "every assertion passes unedited" is the entire proof that this refactor moved nothing**, and a substring test cannot carry that. S49-1a either reads the hover width back exactly or records, in its commit message, that this leg is weaker than the others. It does not silently lean on it. ⚠ **The other three fields are exact and need no such note**: the selection border and radius are an exact `toEqual` over a style map, and the hover INFLATION is pinned arithmetically by `OverlayShell-hover-channels.test.tsx`'s `ring.style.top` rows.

**Owner input.** None.

### S49-1 — the comparison surface

**Lands.** The override reader (C49-2), the per-family records (C49-1), the wiring in the four painter modules, and the **keyboard bump** on the remeasure `tick` that gives the override a re-render channel (C49-2 as amended; S49-P has already proved it works). Under `packages/**`, so deliverable and gated.

⚠ **THE SWITCH HANDLER'S TEXT-ENTRY GUARD IS PART OF THIS STORY'S LANDS, NOT A REVIEW NOTE (C49-2, new at r3').** Both of OverlayShell's document keydown listeners are `{ capture: true }`, and `[` opens a Tailwind arbitrary value that the dogfood corpus uses 251 times, so an unguarded bracket handler eats the character before the className chip editor sees it. The handler returns early on `event.isComposing` and on `active.closest("input, textarea, select, [contenteditable], [role=\"textbox\"]")`, copied from the guard line itself, `packages/descvi/src/react/overlay/OverlayShell.tsx#      if (active.closest("input, textarea, select, [contenteditable], [role=\"textbox\"]") !== null) return;` — **not** from the `focusStageIfOwned` docblock, which records a differently-scoped guard being REJECTED (C49-2). **If S49-P leg (5) shows the guard fragile or the IME kills the channel, this story lands the function-key binding instead** — that branch is decided in C49-2 and is not the executor's to invent.

⚠ **AND THE OVERRIDE'S KEY IS A NAMED LITERAL, NOT A SHAPE.** It is exactly `descvi-look-override`, written once, in one module under `packages/descvi/src/react/overlay/`, and **not** assembled from a template or a constant that a bundler could split. G49-4's leg 0 asserts precisely that, and it is what makes legs 1 and 2 measurements rather than rituals.

⚠ **AND A WITNESS SETS THE OVERRIDE THROUGH THE READER'S EXPORTED SETTER — NEVER BY WRITING THE KEY AGAIN (C49-2, new at r4').** `__tests__` sits UNDER `packages/descvi/src/react/overlay/`, which is leg 0's root, so the moment a test names the literal the count is 2 and G49-4 goes RED for a reason that has nothing to do with a leak — **on the very story that lands the subject.** The obvious workaround, spelling the key differently in the test, is precisely the hole leg 0 exists to close. Two things close it instead: **leg 0 excludes `__tests__`** (measured at r4': without the exclusion, a one-line witness naming the key turns the gate RED — the demonstration is in G49-4), and **the reader exports a setter that the witness calls**, so a witness never has a reason to write the literal at all. ⚠ **Note also what leg 0 is and is not, because its own justification used to overstate it: C49-2's single-reader rule is a claim about MODULES, and the leg's predicate is over FILES.** They coincide here only because one module is one file; a module split would need the leg re-expressed, and the plan says so rather than leaving a reader to assume the two are the same claim.

⚠ **AND ONE AMBIENT DECLARATION, named here so it is not discovered by a failing typecheck.** `import.meta.env.DEV` **is not typed in this package.** `packages/descvi/src/vite-env.d.ts` declares an `ImportMetaEnv` with exactly one member and its docblock says the narrowing is deliberate — referencing `vite/client` instead would turn a `@ts-expect-error` in `preview-css-compiler-host.ts` into an unused-directive error, because the root `tsc --noEmit` leg reaches both files in one compilation. **So S49-1 adds `readonly DEV: boolean` to that existing interface and does NOT reach for `vite/client`.** Reversing that file's docblocked decision to save one line would break the typecheck in a file this phase never touches.

**⚠ It also stages the SPATIAL A/B for the one persistent subject (D49-1) — and the MECHANISM is specified, because r3''s was not renderable.** The selection ring survives the pointer leaving, so it does not need a temporal comparison and should not be forced through one. S49-1 therefore additionally supports **two selected siblings rendering at two candidate values in one viewport**, and it does so **without a second writer**: the ring's override record carries a candidate LIST, and `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#function applyRingStyle(node: HTMLElement, box: RingBox, color: string): void {` — the single writer both paths already go through — indexes that list by the member identity. **Two source facts an executor must have, both verified at r4' and both absent from r3''s sentence:** the writer takes no key today, so the identity arrives either as a fourth argument at its two call sites or is read back off the node (`packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#    const key = node.getAttribute(RING_POOL_KEY_ATTR);` does exactly that already); and **the PRIMARY ring node carries no pool key at all** — `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#function createPooledRingNode(doc: Document, key: string): HTMLElement {` sets it only on secondaries — so the primary needs a sentinel identity or the list indexes from the secondaries alone. ⚠ **What must NOT happen is a second style writer**: the docblock's own warning (`packages/descvi/src/react/overlay/canvas/use-selection-rings.ts# * ⚠ TWO CALLERS, and the structural gate counts them.`) is a gate, and a fork is what it counts. **If S49-P shows the indexing does not reach the pooled path cleanly, this story drops the spatial A/B, takes the ring temporally like the other three, and records that the architect's objection to pure-temporal comparison goes UNANSWERED** — a decision already made in D49-1, not one for the executor. **The other three families stay temporal**; they have no persistent state to stage.

- ⚠ **THE OVERRIDE WITNESSES ARE ADDED TO `set --` IN `scripts/gate-g49-3-look-witnesses.sh`, AND THE `COVERAGE` STRING IS FLIPPED IN THE SAME COMMIT.** The gate's heading promises both modes and its committed witness list is the DEFAULT column alone — seven files, none of which can witness an override that does not exist yet. After this story lands, a run that says GREEN would be asserting the default half under a name claiming both: **true as a statement, unreachable as the scenario it names.** So this story's diff includes new witnesses for the override column of §6's table (one per family: the ring radius through both computed radii, the hover inflation against an unmoved selection box, the reorder band's cross-axis extent, and — the phase's FIRST assertion on the glyph — the emitted `d`), their addition to the positional list, and the one-line edit that makes the exit-0 message say what it actually ran. **The plan's own rule is that the witness list IS the gate**; a widened claim with an unwidened list is the failure that rule exists to prevent.
- ⚠ **`scripts/gate-g49-4-override-leak.sh` IS COMMITTED BY THIS STORY AND WIRED INTO CI, AND ITS PRICE IS STATED HERE RATHER THAN DISCOVERED IN A 35-MINUTE JOB.** Two steps, at the END of the verify job's gate block (after `Build`, because the gate makes its own bundles and a preceding `Build` is not its subject):

  ```
      - name: Audit gate — phase-49 override leak selftest (proves the gate can fail)
        run: sh scripts/gate-g49-4-override-leak.sh --selftest
      - name: Audit gate — phase-49 override leak (G49-4)
        run: sh scripts/gate-g49-4-override-leak.sh
  ```

  **6/8 indentation, the `Audit gate — ` prefix, and each `run:` a single-line scalar**, for the reasons S49-0's block states — the last of those is hard: `scripts/gates.mjs` treats a block scalar in this job as a parse error.

  **The price, measured at r4' rather than estimated:** the gate's own `pnpm descvi:build` + `pnpm build` pair took **4.80 s and 4.66 s** wall on two consecutive full runs on this machine, and `verify:` already carries one `pnpm build` of its own, so the added term is one extra `pnpm build` plus one `pnpm descvi:build`. Against a job whose two vitest suites are ~20 of its 35 minutes this is noise — **but it is noise that was worth measuring, because the alternative was a reviewer asking the question in CI.** ⚠ **The `--selftest` step runs NO build at all** (it drives every leg against a fixture bundle it stages, in **0.09 s** measured at r5), which is exactly why it can be the step that proves the gate can fail without doubling the gate's cost.

  ⚠ **AND THE PRICE THE PLAN DID NOT STATE UNTIL r5 IS THE LOCAL ONE, WHICH IS THE COMMAND AN EXECUTOR ACTUALLY TYPES.** `pnpm gates` parses this same `verify` job, and `AGENTS.md` mandates it per commit — so **from S49-1's commit onward every local gate run gains two full Vite builds** (this gate's own `pnpm descvi:build` + `pnpm build`, on top of the `Build` step already in the job), measured at r4' at **4.80 s and 4.66 s** wall for the pair. Against CI's 35-minute job that is noise; against a local edit-run loop it is the difference an executor will feel, and it is worth knowing it is the price of the gate rather than a regression. ⚠ **Before S49-1 lands, `pnpm gates` pays none of it, because the step is not in the job yet** — this story is what puts it there, in the same commit as the reader it guards. **The two Vite builds arrive with this story and with no story before it.**

**Done when.** With no override present the rendering is byte-for-byte what shipped **across every family the phase touches, spacing and padding included** (G49-3's witness table, every assertion green and unedited, **with the override witnesses now in the list**); with an override present each of the §7 candidate values renders in the live canvas and switches from the keyboard mid-gesture; the ring's spatial A/B renders two values at once; `sh scripts/gate-g49-4-override-leak.sh` is GREEN **across both `dist-designview/` and `dist/`** — including its leg-0 source pin, which is what proves the gate is looking at the literal S49-1 actually wrote — and has been shown RED with the guard removed, with the RED output in the commit message.

**Gates it adds.** G49-4. **Gates it WIDENS: G49-3** — see the Lands item below; **G49-5** — the four ring fields it enumerates acquire their homes here and at S49-1a, and the gate goes from four RED rows to none.

**Owner input.** U49-A on the plan; nothing at execution time.

### S49-2 — `reorder-indicator-look` (U49-1 weight, U49-2 length rule)

**Lands.** `packages/descvi/src/react/overlay/canvas/reorder-paint.ts` — `packages/descvi/src/react/overlay/canvas/reorder-paint.ts#export const REORDER_INDICATOR_THICKNESS_PX = 2;` and the cross-axis extent rule at `packages/descvi/src/react/overlay/canvas/reorder-paint.ts#const crossMin = Math.min(...order.map(`.

> **⚠ THE GATE'S OWN DOCBLOCK IS MISLEADING HERE, AND A PLAN THAT BELIEVED IT WOULD HAVE UNDER-SCOPED THIS STORY.** `packages/descvi/test/reorder/reorder-paint-geometry.test.ts#⚠ **THE PROPERTY IS ASSERTED, NEVER THE PIXELS.**` says *"a change to the thickness or the offset that KEEPS the property is green"* — **and the file it sits in contradicts it.** Measured against the assertions rather than against the prose:
>
> | Change | RED at |
> |---|---|
> | Thickness **raised** (2 → 3 or 4) | three rows, all in `reorder-paint-geometry.test.ts`: `packages/descvi/test/reorder/reorder-paint-geometry.test.ts#expect(row.right - row.left, "thin across the MAIN axis").toBeLessThanOrEqual(2);`, its column twin, and `packages/descvi/test/reorder/reorder-paint-geometry.test.ts#expect(wrongAxis.right - wrongAxis.left, "the axis decides which way the band is thin").toBeLessThanOrEqual(2);` |
> | Thickness **lowered** to 1 | nothing — the bound is one-sided |
> | **Length rule** changed (members' extent → parent's extent) | `packages/descvi/test/reorder/reorder-paint-geometry.test.ts#expect(row.bottom).toBe(24);`, `packages/descvi/test/reorder/reorder-paint-geometry.test.ts#expect(col.right).toBe(70);`, and the painted arm's `packages/descvi/src/react/overlay/__tests__/reorder-paint.test.tsx#expect(node.style.width).toBe("60px");` |
> | Colour, border-radius, edge offset | nothing |
>
> **So C49-5's contract-first split DOES apply to S49-2** for U49-1-upward and for U49-2, and the gate move is the `toBeLessThanOrEqual(2)` bound and the three extent literals. `e2e/reorder-drag.spec.ts` reads the indicator only for presence and visibility and asserts no dimension, so the e2e tree is not in this story's lands list. ⚠ **The asymmetry is the trap**: a plan that tested its scoping by lowering the thickness would have observed a green suite and concluded the look is ungated. Raise it.

**Observation, not a gate: the gap-0 collapse.** `packages/descvi/src/react/overlay/canvas/reorder-paint.ts#const thickness = Math.max(0, Math.min(REORDER_INDICATOR_THICKNESS_PX, gap));` clamps the band to the gap, so at gap 0 nothing is drawn and the `n / N` readout carries the position alone. **A larger weight does not change this** — the clamp is on the gap, not on the constant — and the owner should be shown a gap-0 parent at each candidate weight so they judge the collapse once rather than re-discovering it per value.

**Done when (the G49-7 obligation, which is per-story as of r4' rather than a numbered gate nobody scheduled).** The contract commit lands with no pixel moved; the value commit edits no gate; and **after the value lands, the amended gate is re-run and shown RED on this story's named mutation — the thickness RAISED, or the extent literals moved — with that RED output recorded beside the value commit.** A story that cannot produce one has shipped scaffolding and does not close.

**Owner input.** U49-1, U49-2. Default if deferred: 2 px, members' cross-axis extent. Also carries U49-C's observation question.

### S49-3 — `selection-ring-treatment` (U49-3 radius, U49-4 width and the hover relation)

**Lands.** The record from S49-1a.

**Gate move comes FIRST (C49-5) — for the FINAL value commit; the candidates tried on the override are ungated (C49-5's regime rule).** Unlike S49-2, this look **is** asserted, in **four** places:

1. the selection border and radius in `packages/descvi/src/react/overlay/__tests__/OverlayShell-selection-set.test.tsx`;
2. the hover width in `packages/descvi/src/react/overlay/__tests__/OverlayShell-canvas-hover.test.tsx`;
3. ⚠ **`packages/descvi/src/react/overlay/__tests__/OverlayShell-hover-channels.test.tsx`, which r0 omitted from this list and from G49-3's command alike — but it pins the INFLATION, not the width, and r1' conflated the two.** Its geometry rows are `ring.style.top` reads against stubbed rects (`packages/descvi/src/react/overlay/__tests__/OverlayShell-hover-channels.test.tsx#    // Canvas hover on reg-conn → its row highlights, ring anchors conn.` — the `expect(ring.style.top).toBe('8px')` row it heads, against a stub whose top is 10 on a stubbed top of 10), so they move when the 2-px-per-side inflation moves and stay put when the width does. **This story routes the hover-vs-selection change to the HOVER side** (the e2e trap below forces it there), and **U49-4's triples move the inflation on two of four candidates**, so this file is squarely in the value commit's path — and r0 would have shipped a gate that reported green having never run it;
3a. ⚠ **and the hover WIDTH is a different file with a weaker assertion.** `packages/descvi/src/react/overlay/__tests__/OverlayShell-canvas-hover.test.tsx#    // to rgb(). Solid, thin (1.5px).` — the two `expect(border).toContain('1.5px')` rows it heads (the anchor is on the comment because the assertion text occurs twice in the file). A **substring** test is what they are, and it is RED on every value U49-4 offers, so the story is covered — but it is not an exact pin and the contract commit must not be checked against it alone. See G49-3's per-field table;
4. and — **for a shade change only** — the chip border in `packages/descvi/src/react/overlay/__tests__/resize-handle-layer.test.tsx#keeps the 1.5px group-coloured border`.

The contract commit re-expresses those assertions against the named constants **with the values unchanged and no pixel moved**; the value commit edits no gate. **RED direction for this family is either way** (the radius and both widths are exact pins, not one-sided bounds) — see G49-3's per-field table.

**The ring takes its decision on the SPATIAL staging, not on a temporal switch** (D49-1): two pooled siblings at two candidate widths in one viewport. It is the only one of the four items whose subject survives the pointer moving away, and the only one for which side-by-side is available at all.

**⚠ The hover-larger-than-selection candidate is a relation, not a number.** Today hover is 1.5 px at z 39 *inside* a box inflated 2 px per side, and selection is 2.5 px at z 40 on the element's exact box. Inverting the *size* relation while leaving the *weight* relation alone gives the owner something Figma does not have. The candidate must be specified as the pair, which is what U49-4's rows do.

> **⚠ AND THERE IS AN E2E TRAP ON EXACTLY THE HALF THAT LOOKS FREE.** The obvious way to make hover read larger is to shrink or inflate the SELECTION ring's box. `e2e/multi-select-shield.spec.ts` compares the selection ring's `boundingBox()` to the element's box under `Math.round` with **no tolerance** — `e2e/multi-select-shield.spec.ts#expect(round(await page.locator("#dsh-selection-ring").boundingBox())).toEqual(round(await boxOf(page, ROW_A)));` — and the multi-member row does the same for every pooled ring. **A one-pixel inflation of the selection ring is RED there**, and because that is a Playwright spec, a title edit while repairing it also moves `e2e/fixtures/expected-identities.json`. The hover ring carries the inflation today precisely because the selection ring may not. **So the relation must be changed on the HOVER side.** Other e2e box comparisons (`selection-consistency`, `resize-handle-shield`, `alignment-write`) carry ±1–2 tolerances and would not have caught this; the one with no tolerance is the one that decides.

**Done when (the G49-7 obligation).** The contract commit re-expresses the four assertion sites against the named constants with no pixel moved; the value commit edits no gate; **the amended gate is then shown RED on this story's named mutation — the radius or a width moved in either direction, both being exact pins — with that RED output recorded beside the value commit.** ⚠ **G49-6 must be GREEN throughout**: a width change that silently decoupled the two radii would pass every row in this story's list.

**Owner input.** U49-3, U49-4. Default if deferred: radius 6, selection 2.5 / hover 1.5. **No candidate in §7 changes the `deep` shade** (C49-7, PM-8).

### S49-4 — `spacing-affordance-mark` (U49-5a mark, U49-5b reveal — TWO rows, see D49-3)

**Lands.** `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts` — the figure routing at `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts#function figureFor(kind: SpacingAffordanceKind, axis: "row" | "column", edge: SpacingEdge | undefined): keyof typeof SPACING_GLYPH_PATHS {`, the path record, and the reveal predicate.

**⚠ The reveal half is the expensive half and the mark half is nearly free.** The backlog row asks for two things: one `-` per edge instead of two icons (a change to `SPACING_GLYPH_PATHS` and `figureFor`), and *reveal when the pointer is inside the object* (a change to when affordances are placed at all, which is `use-spacing-affordances.ts`'s placement pass and touches the hit model, not the paint). **They are separately deferrable, and at r1' the owner table SPLITS them into U49-5a (mark) and U49-5b (reveal) so the artefact can record what this story already plans for.** r0 kept them as one row with one `Defer?` cell because the owner asked for them as one direction — which made "take the mark, defer the reveal", the story's own stated outcome, unrecordable. If the owner takes the mark and defers the reveal, the story ships the mark.

**What is NOT in this story.** The ~1 s Figma-style delay — the row holds it explicitly until the owner has seen the rest, and this plan does not put it on the table.

**Gates.** `e2e/spacing-gesture.spec.ts` asserts the C46-1 `glyph-conditional` obligation — that a declaring node has an `svg` descendant and hides below the published size term — **not the path data**. A mark change keeps the `<svg>`, so the obligation is untouched.

> **⚠ ONE THING IN THIS FAMILY IS EXPENSIVE AND IT IS NOT THE MARK: the 8 px hide threshold.** `e2e/spacing-gesture.spec.ts#C9's GLYPH LEG IS DOM PRESENCE, AND BELOW 8 px THE GLYPH IS PRESENT BUT NOT PAINTED` pins `display` against a **bare literal 8 that no production symbol feeds**, and the test's own TITLE names "8 px". So changing `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts#const SPACING_GLYPH_PX = 8;` is red twice over: the row fails, and repairing the row edits a Playwright title, which changes the identity tuple in `e2e/fixtures/expected-identities.json` and requires both a regeneration and a HAND review of that golden's `distribution` object, which regeneration deliberately refuses to overwrite. **A one-`-`-per-edge mark is a smaller figure than two arrows and the temptation to shrink the threshold with it is exactly the trap.** Keep `SPACING_GLYPH_PX` at 8 unless the owner asks otherwise, and if they do, price it as its own row.

A *reveal* change moves when nodes exist at all and therefore does touch that spec's subject set. Grep the e2e for the strip and apron roles before writing the lands list (PM-5).

**Done when (the G49-7 obligation).** ⚠ **This story is the one where the obligation is hardest to discharge and saying so is the point:** no gate pins the glyph's `d` today, so the gate this story must show RED is **the override witness S49-1 lands** (G49-3's spacing/padding row), on a mutation of the emitted `d`. If S49-1 did not land that witness, S49-4 has no gate to relax and no gate to show RED — **and that, not the mark change, is what would have to block the story.**

**Owner input.** U49-5a and U49-5b, answered independently. Default if deferred, per row: shipped mark; shipped reveal.

### S49-5 — `padding-glyph` (U49-6)

**Lands.** One entry in `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts#"pad-x": "M4 4v8M12 8H6.5M8.75 5.75 6.5 8l2.25 2.25",` and its vertical twin `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts#"pad-y": "M4 4h8M8 12V6.5M5.75 8.75 8 6.5l2.25 2.25",`.

> **⚠ MEASURED: the path strings occur NOWHERE outside their own module.** Reproduce: `grep -rIn -e 'M4 4v8' -e 'SPACING_GLYPH_PATHS' e2e packages src | grep -v use-spacing-affordances` returns nothing. **So the phase-46 §5.11 discipline applies to this item vacuously — there is no gate asserting the glyph, so no contract moves first** — and the plan says so explicitly rather than performing a contract-first split against an empty set. What remains binding is the C46-1 obligation the new figure must keep: it is still an `<svg>` with a path, still hidden below `SPACING_GLYPH_PX`, still declared `glyph-conditional`.

**Done when (the G49-7 obligation, discharged in the one form available here).** There is no gate on the path strings, so there is no gate to move and none to relax — the plan says this rather than performing a contract-first split against an empty set. What this story owes instead is the same evidence in the only place it exists: **the override witness on the emitted `d` (G49-3's spacing/padding row) shown RED on the old figure and GREEN on the new**, plus the C46-1 obligation confirmed intact — still an `<svg>` with a path, still hidden below `SPACING_GLYPH_PX`, still declared `glyph-conditional`.

**Owner input.** U49-6, and it is confirmation rather than a decision — the direction is standing from the G48-8 pass. Default if deferred: **execute the standing direction** (a plain directional bar), not the shipped arrow. ⚠ **This is the one row whose deferral default is CHANGE rather than status quo**, because a decision was already given; treating silence as "keep the arrow" would reverse an owner input.

### S49-6 — *optional rider, NOT recommended (U49-B)*: the reorder arming threshold (phase-47 U3)

**Lands.** `packages/descvi/src/react/overlay/canvas/pointer-thresholds.ts`, three hard pins, one regime tripwire, G47-3's diagonal control, two e2e sub-threshold rows — **and two hand-added pins for the stale-green copies enumerated under U49-B, which land FIRST.** A story that changes the value before those two copies are tied to the symbol has broken a phase-48 owner ruling with a green suite.

**Done when.** The two new pins exist and have been shown RED by editing the constant; the chosen value ships; G47-3 has been shown RED at a value it should reject; **the value is inside the reachable box, which is derived once in U49-B and stated nowhere else.** Its consequence is what this story needs: **3 px is the only alternative to the shipped 4** that S49-6 can take without also re-pricing G47-3. A story that wants an upward value is a **G47-3 re-pricing story** and must be brought as one.

⚠ **THE INTERVAL HAS ONE HOME — U49-B — AND THIS SENTENCE IS THE PLAN'S OWN ONE-HOME RULE APPLIED TO THE PLAN.** r1' stated the box in four places, in two different spellings, and only U49-B's was right. **r2' fixed the spelling in all four and then claimed the interval "now appears once" while still stating it in four places** — which is the more expensive half, because a reader who trusts a one-home claim stops checking. **r3' makes the claim true rather than restating it: the interval is derived and written in U49-B alone, and every other mention — the status block, here, and §7 — points there instead of repeating a number.** The box is closed from below by `packages/descvi/src/react/overlay/__tests__/spacing-affordance-geometry.test.ts#⚠ THE FIXTURE's FLOOR-REGIME SUBJECTS ARE PINNED TO THE FLOOR's ACTUAL VALUE, never to the literal 4`'s below-floor subject at 2 px and by the sub-threshold leg in `e2e/reorder-drag.spec.ts`. The conclusion drawn from it — one alternative value — was right in all four places, on a reason that was false in three of them. **A conclusion that survives its own reason being wrong is the most expensive kind of correct there is**, and a claim that the duplication is gone while it is still there is worse than the duplication: the first costs a reader one check, the second costs them the habit of checking.

**⚠ It is one constant for five gestures.** There is no "reorder-only" threshold today. If the owner wants reorder to arm differently from resize, that is a *split*, not a value change, and it is a different story from this one.

**Owner input.** U49-7. Default if deferred (**the recommended path**): 4 px, and the item stays in `docs/handoff/260831-phase-47-close.md` §2 as still-owned rather than silently closed.


## 6. Gates

Every gate below is runnable by someone who is not its author, and every one names the mutation that turns it RED. A gate whose RED-when cannot be staged is scaffolding and does not ship.

⚠ **THE GATES THIS PHASE AUTHORS ARE COMMITTED SCRIPTS AS OF r3', AND THERE ARE FOUR OF THEM AS OF r4'.** `scripts/gate-g49-2-archive-pointers.sh`, `scripts/gate-g49-3-look-witnesses.sh`, `scripts/gate-g49-4-override-leak.sh` and — new at r4' — `scripts/gate-g49-5-one-home.sh`. **A gate written as a shell snippet inside prose cannot be run, so every round its reviewers executed a reconstruction and found a new way the reconstruction differed from what would actually run** — three rounds spent discovering properties of `sh` that a file on disk surfaces on its first invocation. G49-5 was the last gate still living in prose, in the revision whose whole thesis was that prose gates get re-implemented by every reader; it is a file now. **SIX rules bind all four scripts as of r5, and each of them is a finding rather than a preference:**

1. **`#!/bin/sh` with `set -eu`, and no unquoted expansion of a multi-word scalar anywhere.** Scan roots and witness lists are POSITIONAL (`set -- a b c` then `"$@"`), which reads identically under `sh` and `zsh`. r2''s `ROOTS="…"` did not, and the zsh reading made a gate vacuous on a tree carrying five live pointers.
2. **Every gate ends in an EXIT-STATUS verdict.** A gate that prints its findings and exits 0 is not a gate: zero rows from a broken invocation reads exactly like zero rows from a clean tree. r2''s G49-2 had no verdict at all.
3. **A missing scan root is a FAILURE, not an empty result** — the `scripts/check-citation-anchors.mjs#MISSING SCAN ROOT — the corpus is not what this gate was configured to check: ${missingRoots.length}` idiom, reused rather than reinvented. **Each script's precondition is demonstrated firing below**, because a precondition that cannot fail is not one.
4. **Each is demonstrated by INVOKING THE COMMITTED FILE**, GREEN and planted-RED, with the transcript pasted. **A reconstruction is not a demonstration** — that is the whole lesson of rounds 1 through 3.
5. ⚠ **EACH CARRIES A `--selftest` THAT STAGES ITS OWN PLANT, AND EACH LANDS IN A STORY AND IN `.github/workflows/ci.yml` — NEW AT r4', AND IT IS THE RULE THIS REPO ALREADY HAD.** `scripts/check-citation-anchors.mjs --selftest` sits in that job under a step named *"proves the gate can fail"*, and `check-handle-constants.mjs` beside it does the same. r3' shipped three scripts with neither: untracked, in nobody's Lands, run by nothing — and their RED proofs were manual plants recorded in a plan that gets archived. **After phase-49 closed, nothing would have shown any of them can fail.** A demonstration pasted into a plan proves a gate could fail ONCE, on one tree, in one session; a selftest in CI proves it on every push, which is the difference between a gate and a story about a gate. Where each lands: **G49-2 → S49-0**; **G49-3 and G49-5 → S49-1a**; **G49-4 → S49-1**, which also widens G49-3's witness list.
   ⚠ **AND THE SELFTESTS THEMSELVES WERE SHOWN ABLE TO FAIL**, because a selftest that cannot go RED is the same defect one level up: each was re-run from a deliberately broken COPY of its own script and reported the specific assertion that stopped holding. Those transcripts are inside the gates, beside the GREEN ones.
   ⚠ **AND AT r4' THAT PROOF WAS ABOUT MECHANISM AND NOT ABOUT SCOPE, WHICH IS r5's WHOLE ITEM AND THE SIXTH RULE THIS LIST NOW CARRIES.** Every fixture case in every selftest drives its script through the ARGUMENT path — witness files on the command line, a fixture overlay root, fixture bundle directories — **and that path REPLACES the very object this plan calls the gate.** So a copy of G49-3 with six of its seven witnesses deleted, a copy of G49-5 with two of its five fields deleted, a copy of G49-2 with the archive-index root dropped or the heading-slug branch replaced by `false`, and a copy of G49-4 with `dist` dropped from the bundle set **all ran their own selftests GREEN**: on every CI push those steps re-proved the scan mechanism and never the reach. codex's sentence for it is worth keeping — *self-tests prove individual scan mechanics but do not prove that their production enumerations still cover every claimed subject.* **Rule 6, adopted from codex's own synthesis: keep the explicit lists, and make every list REMOVAL a selftest failure.** Each selftest now asserts its own enumeration against a separately written expectation — G49-3 the exact seven-file default list plus one required witness per furniture family, G49-5 the exact five-field manifest plus a staged RED per enumerated field on both legs, G49-2 a planted pointer inside its archive INDEX and a control that resolves only by heading slug, G49-4 the two-bundle default scan set — **and all five broken copies above now report RED and name what was lost.** The transcripts are inside the gates. **This landed WITH the scripts, in the same commit: a selftest added later is a selftest nobody was ever blocked by.**

**And the honest outcome if one of them could not be made to fail on its own planted RED is that the gate does not ship and the plan names the claim that then goes unguarded.** Each of the three carries that sentence. At r3' all three produced a real RED from the committed file, so none of them takes that exit.

### G49-1 — the archiving move leaves no live pointer at a moved path (check 1 of 2)

**Run.** `node scripts/check-citation-anchors.mjs` — must stay GREEN.
**⚠ This gate is NOT sufficient on its own and the plan says so where an executor will read it.** Leg (b) checks anchor uniqueness inside the target file; for a `.md` target the anchor is treated as a section link and **the target's existence is not checked at all**. Moving a `.md` file therefore does not turn this gate red. That is the whole reason G49-2 exists.
**RED-when.** Introduce an anchor citation into a `.ts` file whose text does not occur there, or a bare line pin into `packages/descvi/src/vite/plugin.ts`. Demonstrate before believing green.

### G49-2 — the archiving move leaves no live pointer at a moved path (check 2 of 2, the one that can actually see it)

> ⚠ **THIS GATE IS A COMMITTED SCRIPT AT r3', AND THAT IS THE ROUND'S ESCALATION RATHER THAN A TIDY-UP. Read this before editing anything back into prose.**
>
> Three rounds running, every must-fix on this gate was the same class (`PM-10`), and the cause was structural: **the gate was authored as a shell snippet inside prose.** Prose cannot be run, so each round's reviewers executed a *reconstruction* and found a new way the reconstruction differed from what would actually run. Three rounds were spent discovering properties of `sh` that a file on disk surfaces on its first invocation. **The gate is now `scripts/gate-g49-2-archive-pointers.sh`**; the plan states what prose is good for — the predicate, the RED-when, and what goes unguarded if the gate cannot be written.
>
> **What the previous forms could not do, in order, so nobody restores one:**
> - **r1' leg (a) named an allow-listed row its own query removes**, and its count-based GREEN then tolerated a genuine live pointer as the missing archive row.
> - **r1' leg (b) was RED on arrival and its plant lived in this file** — `[A-Za-z0-9._/-]*` with no required extension swallowed a sentence-final period, a prose ellipsis and pasted `grep -n` context. A gate cannot hold its own plant.
> - **r2' was VACUOUS UNDER THIS MACHINE'S SHELL.** `ROOTS="docs …"` expanded unquoted is ONE argument under zsh, which does not word-split unquoted scalars; both legs emitted a warning to *stderr* and zero rows to *stdout* on a tree carrying five live pointers, and **zero rows satisfied the stated verdict vacuously**. Under `sh` the same block returned the correct five.
> - **r2' had no exit-status verdict at all.** It printed rows and returned whatever the last `grep` returned, so zero rows from a broken invocation read exactly like zero rows from a clean tree. That is `ND-1`, and it is the reason every gate in this phase now ends in an exit status.

**Run.** `sh scripts/gate-g49-2-archive-pointers.sh`, from the repo root.

**The verdict is the EXIT STATUS**, not the rows: `0` GREEN, `1` RED (a row survived the predicate), `2` RED (a scan root is missing). **A missing scan root is a FAILURE, not an empty result** — the idiom is `scripts/check-citation-anchors.mjs#MISSING SCAN ROOT — the corpus is not what this gate was configured to check: ${missingRoots.length}`, reused rather than reinvented.

**GREEN is a PREDICATE, never a count.** Both legs apply the same test: *every row this leg produced came from a file in the allow-list set*. The set is three **basenames** — this plan, and the two files being moved — so the predicate reads the same before and after the `git mv`, and neither a plant, a transcript nor a future revision's tenth discussion of the archiving moves a number the gate compares against. This plan must name both source paths for S49-0's `git mv` line to be executable; the two moved files' self-references travel *with* them and rewriting a document's references to itself is not a pointer repair.

**THERE ARE THREE LEGS AS OF r4', AND LEG (c) IS THE ONE THE PLANNING BRIEF ASKED FOR IN ITS FIRST PARAGRAPH AND NOBODY CLOSED FOR FOUR ROUNDS.**
- **(a)** a live pointer at a moved path, in a file that is not allow-listed;
- **(b)** a dangling `.omc/archive/*.md` citation, from a file that is not allow-listed;
- **(c)** ⚠ **a markdown citation whose FRAGMENT matches neither a TEXT ANCHOR nor a HEADING SLUG in its target** — that is the whole claim, and it is narrower than "the fragment resolves"; the paragraph below states the false negative it buys. codex reported this gap in rounds 2, 3 and 4 and it was closed in none of them: an existing target with a fragment naming no section passes leg (b), and `scripts/check-citation-anchors.mjs` skips markdown fragments **by design** — its own docblock says a heading slug is not a literal string in the file, so uniqueness-checking one would report every correct section link as a violation. That exclusion is right and its cost is this leg's subject. **A requirement restated every round and closed by nobody is not something the lanes are missing; it is a near-miss that kept being accepted.**

**Four things in the script are load-bearing and each replaces a way an earlier form could not work.**
- **The roots are a POSITIONAL LIST** (`set -- docs .omc/plans …` then `"$@"`), which reads identically under `sh` and `zsh`. This is the r2' vacuity, fixed at the only place it can be fixed.
- **`\.md\b` on leg (b), and no `-h`.** The required extension drops the period, the ellipsis and the `README.md-41-` context; keeping the citing file is what lets the allow-list — a test on *which file a row came from* — apply at all.
- **`--exclude-dir=archive` AND `--exclude-dir=handoff` on EVERY leg — but the archive's INDEX is a scan root of its own (r4').** The frozen-record rule (`docs/README.md#They are point-in-time records and are deliberately **not** rewritten`) exempts point-in-time RECORDS: a dangling archive citation inside `docs/handoff/**` would be permanently RED with no legal repair, a gate whose only fix is to break a documented convention. **`.omc/archive/README.md` is not a record.** It is the index, it asserts where two plans ARE, the move makes it wrong, and it was invisible to both legs until r4' — the exclusion was carrying a justification that did not cover it. Naming the file on the command line scans it even though `--exclude-dir=archive` drops the directory around it: the flag governs directories the walk descends into, not paths given as arguments (verified on this machine's `ugrep 7.8.4` shim, and it is GNU grep's documented behaviour too).
- ⚠ **NO `--include` LIST ON LEG (a), NEW AT r4'.** It was inert — the census is byte-identical with and without it — but it was a blind spot leg (b) never had: this repo puts plan paths in `.json`, `.mts` and spec files, and the bare-basename citation form (five occurrences inside one of the moved plans) is unmatched by the regex entirely. **A filter that is doing nothing today and would silently do the wrong thing tomorrow is worth deleting while it is still free.**

**LEG (c) VALIDATES *TEXT-ANCHOR-OR-HEADING-SLUG* CITATIONS, AND THE CLAIM IS WRITTEN IN THOSE WORDS BECAUSE IT IS NARROWER THAN "THE FRAGMENT RESOLVES".** A fragment passes if **either** spelling this repo actually uses is satisfied: the fragment occurs as literal text **anywhere in the target file** (the dominant form here — the citation quotes the sentence it means), **or** it equals the GitHub slug of one of the target's headings (the web's own form, which the citation gate's docblock names as its reason for skipping markdown). **Both halves are needed: substring-only leaves the slug form RED, slug-only leaves the quoted-sentence form RED.**

⚠ **THE DELIBERATE FALSE NEGATIVE, STATED AS A CONTROL RATHER THAN LEFT FOR A REVIEWER TO FIND.** The text half is `grep -qF` over the whole target, not a heading test. So **a citation whose section was renamed, merged or deleted still passes as long as the quoted words survive anywhere in the file** — in another section, in a code fence, in a table of contents. The real defect this leg caught was caught because a punctuation transposition destroyed the byte match; **had the heading merely moved, the leg would have been silent.** And short fragments (`#KI-45`, `#B-Q5`) are effectively unguarded, because any occurrence of those characters passes. The leg's claim is therefore *this citation's text still exists in this file*, never *this citation still points at a section*. **Migrating to true heading-slug validation is OUT OF SCOPE for a named reason and not by omission: it would require repairing this repo's existing quoted-sentence citation corpus, which is the dominant form here — a corpus edit, not a gate edit.**

⚠ **AND NO FIGURE IS PUBLISHED FOR EITHER HALF, ONLY THE RECIPE THAT REGENERATES IT** — the figure moves with every revision of this file, and r4' published one (17 of 23) that reproduced under no scoping any later lane could construct. To measure either half, copy the script and replace one branch's condition with `false`, then count its rows on the live corpus:

```
# how many live citations a HEADING-ONLY rule would be RED on — disable the substring branch
#   (`if grep -qF -e "$frag" "$target"; then` → `if false; then`) in a COPY, then:
sh /path/to/copy.sh | grep -c '^DEAD FRAGMENT'
# how many a SUBSTRING-ONLY rule would be RED on — disable the slug branch the same way.
```

**On the r5 text that reads 14 and 1**, which is the conclusion this leg ships on and it is robust under every scoping both round-5 lanes tried: **a heading-only rule could never have been switched on** (it is the r1' leg-(b) defect exactly — an instrument RED on a clean tree, whose repair is to edit the corpus rather than the instrument), **and substring-only leaves exactly one live citation RED**, so neither half can be dropped.

⚠ **And the allow-list does NOT exempt leg (c).** The exemption exists because a document's references to itself and to the paths it is ordering moved are legitimate; a fragment that names nothing has no such excuse in any file — **least of all in this one, where the first dead fragment leg (c) found was living.**

⚠ **DO NOT re-derive leg (a) with a `git grep … ':!.omc/plans'` pathspec.** It is the query four separate enumerations reached for and it is blind by construction — see D49-4's instrument finding. Both `.omc/`-resident live pointers, and every allow-listed file, are invisible to it.

**DEMONSTRATION — THE COMMITTED FILE, INVOKED BY PATH, AT r4'.** ⚠ **The real tree was never planted in and holds no plant now**: every plant below is staged by the script's own `--selftest` inside a `mktemp -d` fixture it removes on exit, which is the r4' replacement for a manual plant somebody has to remember to undo. The one thing that IS on the real tree is a genuine defect leg (c) found, and it is repaired in this revision rather than pasted as a plant.

**STATE 1 — the real working tree, BEFORE the move. RED by construction, and leg (a) IS the rewrite list.**

```
$ sh scripts/gate-g49-2-archive-pointers.sh
--- (a) a live pointer at a moved path, in a file that is not allow-listed ---
LIVE POINTER docs/architecture.md
LIVE POINTER docs/e3/tracker.md
LIVE POINTER docs/known-issues.md
LIVE POINTER .omc/plans/ralplan-phase-46-ring-furniture-restyle.md
LIVE POINTER .omc/research/phase48-strip-band-pricing.md
LIVE POINTER .omc/archive/README.md
--- (b) a dangling .omc/archive/*.md citation, from a file that is not allow-listed ---
--- (c) a markdown citation whose fragment resolves to nothing (the allow-list does NOT exempt this leg) ---
DEAD FRAGMENT **⚠ 이것이 "아직 안 봤다"가 아니라는 것이 이 항목의 요점입니다.**  in docs/open-design-questions.md  <- cited from .omc/plans/ralplan-phase-49-comparison-surface.md
G49-2: RED (7 row(s) survived the allow-list predicate)
$ echo $?
1
```

**TWO THINGS IN THAT OUTPUT ARE FINDINGS AND NOT DEMONSTRATIONS.**

1. ⚠ **`LIVE POINTER .omc/archive/README.md` is the row four rounds could not see** — the archive INDEX, hidden by an exclusion whose justification covers archived plans and not the table that says where they are. It is the sixth file in S49-0's rewrite list.
2. ⚠ **`DEAD FRAGMENT …` IS A REAL DEFECT IN THIS PLAN, FOUND BY LEG (c) ON ITS FIRST RUN, AND IT IS THE BEST ARGUMENT FOR THE LEG THERE IS.** §1's principle 1 cited `docs/open-design-questions.md` at a fragment reading `**⚠ 이것이 …**` while the source reads `⚠ **이것이 …**` — the warning sign and the bold markers transposed. **The citation gate was GREEN on it the whole time and always would have been**, because it skips markdown fragments by design. The citation is corrected in this revision, which is why the row is gone from the runs below. *(A four-round-old dead pointer, in the plan's first principle, found in the first second of the leg's existence.)*

⚠ **SO A READER RE-RUNNING THIS TODAY GETS SIX ROWS, NOT SEVEN, AND THAT DIFFERENCE IS THE REPAIR RATHER THAN A TRANSCRIPT ERROR.** The STATE 1 block is the run that FOUND the fragment; the citation was fixed in this same revision, so leg (c) is now silent and legs (a)+(b) contribute the six-file rewrite list alone. **That output IS the rewrite list**, and it agrees file-for-file with D49-4's census — including the archive index, which the census gained in the same round for the same reason. ⚠ **Note what does NOT appear in it: the two moved files' own self-references and this plan's own mentions**, which the predicate removes without anyone having to know how many there are.

**STATE 2 — `--selftest`: the gate staging its own plants, GREEN.** Three rows it must produce, three CONTROLS it must stay silent on, and all three verdicts:

```
$ sh scripts/gate-g49-2-archive-pointers.sh --selftest
SELFTEST ok   [clean fixture] exit 0
SELFTEST ok   [planted — four rows, four controls silent] exit 1
SELFTEST ok   [row present] LIVE POINTER docs/pointer-plant.md
SELFTEST ok   [row present] LIVE POINTER .omc/archive/README.md
SELFTEST ok   [row present] DANGLING .omc/archive/260901-e3-v3/nothing-here.md
SELFTEST ok   [row present] DEAD FRAGMENT
SELFTEST ok   [control silent] .omc/plans/ralplan-phase-49-comparison-surface.md
SELFTEST ok   [control silent] docs/handoff/frozen.md
SELFTEST ok   [control silent] docs/fragment-control.md
SELFTEST ok   [control silent] docs/slug-control.md
SELFTEST ok   [missing scan root] exit 2
G49-2 --selftest: GREEN (the gate produced all three verdicts and every control stayed silent)
$ echo $?
0
```

**What the four controls prove, and they are the half a gate cannot be trusted without** — a gate that passed everything would look identical to one that filters correctly. **CONTROL 1**: the same live pointer written into an allow-listed plan, silent — the predicate is doing work. **CONTROL 2**: the same dangling archive citation written into `docs/handoff/`, silent — the frozen-record exclusion, shown working rather than asserted. **CONTROL 3**: a fragment that resolves by TEXT, silent — leg (c) is not simply reporting every citation it can see. ⚠ **CONTROL 4, NEW AT r5 AND IT IS SCOPE RATHER THAN MECHANISM**: a fragment that resolves ONLY by heading slug (the fixture target's sole heading is `# Target`, whose slug `target` does not occur as text in the file), silent — **so disabling the slug branch turns this control into a row, which is what makes the slug half of the rule something the selftest can lose.** And `[clean fixture] exit 0` is this gate's GREEN: the same script, on a corpus with none of the four defects in it, which is the state S49-0 must leave the real tree in.

⚠ **AND THE SECOND `LIVE POINTER` ROW IS SCOPE TOO.** The fixture plants the moved-path pointer inside its own `.omc/archive/README.md` and asserts that row by name, because the archive INDEX is a scan root of its own precisely to defeat `--exclude-dir=archive` — the blind spot round 4 spent a CRITICAL finding on. Drop that root from `set --` and the selftest is RED at a named row instead of quietly narrowing.

⚠ **THE PLANTS ARE ASSEMBLED IN THE SCRIPT, NEVER SPELLED — because `scripts/` is one of this gate's own scan roots.** A plant written out in full inside the file would be a live row on every run: that is the r1' failure (*"a gate cannot hold its own plant"*) reproduced inside the very file that records it, and it was observed on the first draft of this script before the strings were split. The plan keeps the same discipline: **the plants are described by their SHAPE here and appear whole only in the transcript**, which the allow-list makes structurally invisible to legs (a) and (b).

**STATE 3 — the same two runs under `zsh`, because the shell is precisely what r2' got wrong.**

```
$ zsh scripts/gate-g49-2-archive-pointers.sh --selftest
SELFTEST ok   [clean fixture] exit 0
SELFTEST ok   [planted — four rows, four controls silent] exit 1
SELFTEST ok   [row present] LIVE POINTER docs/pointer-plant.md
SELFTEST ok   [row present] LIVE POINTER .omc/archive/README.md
SELFTEST ok   [row present] DANGLING .omc/archive/260901-e3-v3/nothing-here.md
SELFTEST ok   [row present] DEAD FRAGMENT
SELFTEST ok   [control silent] .omc/plans/ralplan-phase-49-comparison-surface.md
SELFTEST ok   [control silent] docs/handoff/frozen.md
SELFTEST ok   [control silent] docs/fragment-control.md
SELFTEST ok   [control silent] docs/slug-control.md
SELFTEST ok   [missing scan root] exit 2
G49-2 --selftest: GREEN (the gate produced all three verdicts and every control stayed silent)
```

Identical, line for line, and the real-tree run under `zsh` reproduces the `sh` run the same way — **STATE 1's seven rows at r4', six at r5, leg (c) silent since the fragment was repaired.** **The r2' block did not.**

**STATE 4 — THE SELFTEST ITSELF SHOWN ABLE TO FAIL, AND AT r5 THE BREAK IS A SCOPE CUT RATHER THAN A PATTERN CUT.** A selftest that cannot go RED is the same defect one level up — and r4''s copy broke leg (c)'s *pattern*, which is a mechanism, so it never asked whether the selftest would notice the gate's REACH shrinking. It would not have. Two copies, each deleting exactly one thing this gate's scope is made of:

```
$ sh /…/g2-archive-index-root-removed.sh --selftest   # a COPY with .omc/archive/README.md dropped from `set --`
SELFTEST ok   [clean fixture] exit 0
SELFTEST ok   [planted — four rows, four controls silent] exit 1
SELFTEST ok   [row present] LIVE POINTER docs/pointer-plant.md
SELFTEST FAIL [row missing] LIVE POINTER .omc/archive/README.md
SELFTEST ok   [row present] DANGLING .omc/archive/260901-e3-v3/nothing-here.md
SELFTEST ok   [row present] DEAD FRAGMENT
SELFTEST ok   [control silent] .omc/plans/ralplan-phase-49-comparison-surface.md
SELFTEST ok   [control silent] docs/handoff/frozen.md
SELFTEST ok   [control silent] docs/fragment-control.md
SELFTEST ok   [control silent] docs/slug-control.md
SELFTEST ok   [missing scan root] exit 2
G49-2 --selftest: RED (1 assertion(s) failed — the gate cannot be trusted)
$ echo $?
1

$ sh /…/g2-slug-branch-disabled.sh --selftest          # a COPY with the heading-slug branch replaced by `if false`
SELFTEST ok   [clean fixture] exit 0
SELFTEST ok   [planted — four rows, four controls silent] exit 1
SELFTEST ok   [row present] LIVE POINTER docs/pointer-plant.md
SELFTEST ok   [row present] LIVE POINTER .omc/archive/README.md
SELFTEST ok   [row present] DANGLING .omc/archive/260901-e3-v3/nothing-here.md
SELFTEST ok   [row present] DEAD FRAGMENT
SELFTEST ok   [control silent] .omc/plans/ralplan-phase-49-comparison-surface.md
SELFTEST ok   [control silent] docs/handoff/frozen.md
SELFTEST ok   [control silent] docs/fragment-control.md
SELFTEST FAIL [control leaked] docs/slug-control.md appears in the output
SELFTEST ok   [missing scan root] exit 2
G49-2 --selftest: RED (1 assertion(s) failed — the gate cannot be trusted)
$ echo $?
1
```

**Read the two RED lines against each other.** The first is a row that must be there and is not — the gate stopped looking at a namespace. The second is a control that must be silent and is not — the gate stopped accepting a citation form it is supposed to accept, which is the same defect pointing the other way. **A copy with leg (c)'s pattern disabled is still RED too** (`SELFTEST FAIL [row missing] DEAD FRAGMENT`, the r4' proof), so the mechanism half did not have to be given up to get the scope half.

⚠ **NOTE WHAT IS NOT IN ANY OF THESE TRANSCRIPTS: A LINE READING `exit=N`.** Every block r3' pasted ended in one, and **no script in this phase emits it** — it was a transcription habit, and at G49-4 it is worse than cosmetic, because `cmd ; echo "exit=$?"` is the disarming pattern that was instance (1) of the `PM-10` class. Where an exit status is shown here it is a separate `echo $?` command, which is a real thing a reader can type and get the same answer.
**RED-when, for an executor re-running this after the move.** ⚠ **It is `--selftest`, and that is the whole point of r4' — there is nothing left to stage by hand.** Run `sh scripts/gate-g49-2-archive-pointers.sh --selftest`; it creates the four plants and the four controls in a temp fixture, asserts all three verdicts AND the gate's own scope, and removes the fixture on exit, so a runner cannot forget to undo a plant and cannot leave one behind for the next lane to find. Both that output and the post-move gate run go in S49-0's commit message. ⚠ **The plant path must NEVER be written into this plan as an INSTRUCTION** — r1' told the runner to plant a specific archive filename, and writing that filename down *is* the plant, so the plant shipped and the gate was permanently RED on it; r2' then repeated the filename inside the very sentence forbidding it (`ND-6`). **The plants are described by their SHAPE here and appear whole only in a transcript**, which the allow-list makes structurally invisible to legs (a) and (b).

⚠ **AND YES, THE SELFTEST TRANSCRIPT ABOVE CONTAINS A DANGLING ARCHIVE PATH. That is deliberate and it is safe for exactly one reason, which is the reason this gate was rebuilt:** the allow-list predicate makes this file's own mentions structurally invisible to legs (a) and (b). If a later revision ever removes this plan from `ALLOW`, this transcript becomes RED — and that is correct: the exemption and the text that needs it live and die together. ⚠ **Leg (c) has no such exemption, so the transcripts above are written in a row FORM that carries no backticked citation** — the row prints its fragment and its target as bare text. A transcript that pasted a dead citation in citation form would be a plant leg (c) could see, and the leg would be right.

⚠ **One thing this gate deliberately does NOT assert: a row count as a GREEN condition.** r1' required leg (a) to equal a census figure that included a count of this document's own mentions, which moves every revision. **A gate whose GREEN is a number it must be edited to keep true is not a gate.** What replaces it is the demonstration above: the instrument shown producing a non-zero on a subject it was pointed at, and a silent control beside it.

**If this gate could not be written**, the claim that would go unguarded is S49-0's whole deliverable: that the `git mv` left no live pointer at a moved path. G49-1 cannot substitute — for a `.md` target it treats the anchor as a section link and never checks the target's existence, so moving a `.md` file does not turn it red. **Leg (c) CAN be written and was, so the fragment claim is guarded rather than named as a hole** — which is the answer round 4 asked for and rounds 2 and 3 did not get. What stays unguarded, stated rather than left to inference: **a dead fragment inside `docs/handoff/**` or `.omc/archive/*/`**, excluded from all three legs because the repair those namespaces would need is an edit their own convention forbids.

**Why two checks.** This is `8db53ad`'s own method (*"rewritten and then verified BY QUERY rather than by list"*) restated as a gate. A list is what produced the three pointers that had been dead since an earlier archiving pass.

### G49-3 — with no override present, the rendering is what shipped — AND with an override present it is what the override says

**Run.** `sh scripts/gate-g49-3-look-witnesses.sh`, from the repo root — every existing look assertion, **unedited**, at S49-1a and S49-1.

**The verdict is the EXIT STATUS**: `0` GREEN, `1` RED (vitest's own failure — a look assertion moved), `2` RED (a witness file is missing). ⚠ **The witness list IS the gate, which is why it is a committed file and not a command line.** Handing vitest a witness that no longer exists must be a FAILURE and never an empty result: a run that matched nothing is the exact shape of a gate reporting green having never executed its subject, and this gate's whole history is one file having been left off a command.

**DEMONSTRATION — THE COMMITTED FILE, INVOKED BY PATH, AT r4'.**

**GREEN, the real working tree.** ⚠ **Read the trailing clause: the exit-0 message now says WHAT IT RAN, which is r4''s repair of a heading that promised two modes over a witness list carrying one.**

```
$ sh scripts/gate-g49-3-look-witnesses.sh
 ✓ |descvi| src/react/overlay/__tests__/OverlayShell-canvas-hover.test.tsx (16 tests) 611ms

 Test Files  7 passed (7)
      Tests  87 passed (87)
   Duration  2.18s (transform 707ms, setup 0ms, collect 3.72s, tests 1.82s, environment 3.35s, prepare 377ms)

G49-3: GREEN (7 witness file(s) ran and every look assertion held — default-mode witnesses only; the override column is not in this list yet (S49-1))
$ echo $?
0
```

**PLANTED-RED, the real working tree** — the constant **raised**, per the RED-when table below, in `packages/descvi/src/react/overlay/canvas/reorder-paint.ts` (2 → 3). The file was restored from a snapshot taken after the work began — never with a checkout — and its SHA-256 re-checked (`c27bad03…485`, identical):

```
$ sh scripts/gate-g49-3-look-witnesses.sh
⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯
 FAIL |descvi|  test/reorder/reorder-paint-geometry.test.ts > G47-6 — the indicator's rect is a band in the DESTINATION gap, across the main axis > PERPENDICULAR — a row band is thin on x and spans the members' cross extent; a column band is the transpose
AssertionError: thin across the MAIN axis: expected 3 to be less than or equal to 2
 Test Files  1 failed | 6 passed (7)
      Tests  1 failed | 86 passed (87)
G49-3: RED (a look assertion moved — default-mode witnesses only; the override column is not in this list yet (S49-1))
$ echo $?
1
```

⚠ **MEASURED CORRECTION TO THIS PLAN'S OWN RED-WHEN TABLE — MADE AT r3', AND AT r4' IT IS FINALLY IN THE TABLE.** The table said raising the thickness fails "three rows". **Three `toBeLessThanOrEqual(2)` rows exist, but all three sit in ONE `it()`** — `packages/descvi/test/reorder/reorder-paint-geometry.test.ts#  it("PERPENDICULAR — a row band is thin on x and spans the members' cross extent; a column band is the transpose", () => {` — and vitest aborts a test at its first failed assertion, so the run reports **one** failing test and never evaluates the other two. The rows are three; the independent witnesses are one. ⚠ **r3' wrote that correction in prose and left "three rows fail" standing in the table two paragraphs below — which is the row an executor actually reads.** The plan's own rule is to propagate a correction through the whole output rather than through the paragraph being edited; the table row now carries the measurement.

**`--selftest`, which is what makes this gate provable after phase-49 closes.** The seven real witnesses cannot be planted without touching product source, so the selftest stages its own: two fixture tests under `packages/descvi/test/`, where the package's vitest `include` globs will actually collect them (a fixture in `$TMPDIR` is not awkward, it is INVISIBLE — vitest treats CLI paths as filters over the files its config already collects). It removes them on exit.

```
$ sh scripts/gate-g49-3-look-witnesses.sh --selftest
SELFTEST ok   [default list size] the no-argument path runs 7 witness file(s)
SELFTEST ok   [family covered] selection ring (width + radius) — packages/descvi/src/react/overlay/__tests__/OverlayShell-selection-set.test.tsx
SELFTEST ok   [family covered] selection ring (pooled secondaries) — packages/descvi/src/react/overlay/__tests__/selection-ring-pool.test.tsx
SELFTEST ok   [family covered] hover ring — WIDTH — packages/descvi/src/react/overlay/__tests__/OverlayShell-canvas-hover.test.tsx
SELFTEST ok   [family covered] hover ring — INFLATION — packages/descvi/src/react/overlay/__tests__/OverlayShell-hover-channels.test.tsx
SELFTEST ok   [family covered] reorder indicator (paint) — packages/descvi/src/react/overlay/__tests__/reorder-paint.test.tsx
SELFTEST ok   [family covered] reorder indicator (geometry) — packages/descvi/test/reorder/reorder-paint-geometry.test.ts
SELFTEST ok   [family covered] spacing / padding (placement) — packages/descvi/src/react/overlay/__tests__/spacing-affordance-geometry.test.ts
SELFTEST ok   [a witness whose assertion holds] exit 0
SELFTEST ok   [a witness whose assertion moved] exit 1
SELFTEST ok   [one holding and one moved — a single failure is still RED] exit 1
SELFTEST ok   [a missing witness is a FAILURE, not an empty result] exit 2
G49-3 --selftest: GREEN (the default witness list is the one this gate claims, and the gate produced all three verdicts on staged witnesses)
$ echo $?
0
```

**The last line before the verdict is the precondition, shown firing** — a renamed or deleted witness is exit 2 and never an empty pass, which is the shape of a gate reporting green having never executed its subject. **The mixed run above it is the one worth reading twice**: one holding and one moved is RED, so a widened witness list cannot be diluted by the files that still pass.

⚠ **AND THE FIRST EIGHT LINES ARE r5's ITEM, BECAUSE THE FOUR FIXTURE CASES BELOW THEM COULD NOT SEE A NARROWING.** Every fixture case drives the ARGUMENT path, which replaces the list this gate calls itself — so **a copy with six of the seven witnesses deleted ran this selftest GREEN.** The list is now written once, above both branches, and the selftest asserts its exact size plus one required witness per furniture family. The proof:

```
$ sh /…/g3-six-witnesses-deleted.sh --selftest   # a COPY with six of the seven default witnesses deleted
SELFTEST FAIL [default list size] expected 7 default witness file(s), got 1 — a witness was added or removed without this assertion moving with it
SELFTEST ok   [family covered] selection ring (width + radius) — packages/descvi/src/react/overlay/__tests__/OverlayShell-selection-set.test.tsx
SELFTEST FAIL [family UNCOVERED] selection ring (pooled secondaries) — the default list no longer contains packages/descvi/src/react/overlay/__tests__/selection-ring-pool.test.tsx
SELFTEST FAIL [family UNCOVERED] hover ring — WIDTH — the default list no longer contains packages/descvi/src/react/overlay/__tests__/OverlayShell-canvas-hover.test.tsx
SELFTEST FAIL [family UNCOVERED] hover ring — INFLATION — the default list no longer contains packages/descvi/src/react/overlay/__tests__/OverlayShell-hover-channels.test.tsx
SELFTEST FAIL [family UNCOVERED] reorder indicator (paint) — the default list no longer contains packages/descvi/src/react/overlay/__tests__/reorder-paint.test.tsx
SELFTEST FAIL [family UNCOVERED] reorder indicator (geometry) — the default list no longer contains packages/descvi/test/reorder/reorder-paint-geometry.test.ts
SELFTEST FAIL [family UNCOVERED] spacing / padding (placement) — the default list no longer contains packages/descvi/src/react/overlay/__tests__/spacing-affordance-geometry.test.ts
SELFTEST ok   [a witness whose assertion holds] exit 0
SELFTEST ok   [a witness whose assertion moved] exit 1
SELFTEST ok   [one holding and one moved — a single failure is still RED] exit 1
SELFTEST ok   [a missing witness is a FAILURE, not an empty result] exit 2
G49-3 --selftest: RED (7 assertion(s) failed — the gate cannot be trusted)
$ echo $?
1
```

⚠ **READ THE FOUR `ok` LINES AT THE BOTTOM OF THAT RUN.** All four verdicts still hold on the crippled copy, which is exactly why the r4' selftest was GREEN on it: **the mechanism is intact and the gate is looking at one seventh of its subject.** The failing rows name the families that lost their cover rather than reporting an off-by-one, because "the count moved" is not a finding an executor can act on.

**AND THE ONE-SIDEDNESS WAS RUN AS A CONTROL, not asserted** — the same constant **lowered** to 1, on the real tree:

```
$ sh scripts/gate-g49-3-look-witnesses.sh
 Test Files  7 passed (7)
G49-3: GREEN (7 witness file(s) ran and every look assertion held — …)
$ echo $?
0
```

**That GREEN is the finding.** The bound is one-sided, and a lane that tested its scoping by lowering the value would have observed a clean suite and concluded the look is ungated. This is the trap S49-2 documents; here it is executed.

**If this gate could not be written**, the claim that would go unguarded is the one S49-1a exists to make: that naming the ring's three inline literals moved no pixel.

⚠ **`OverlayShell-hover-channels.test.tsx` was missing from r0's command AND from S49-3's contract-move list, and it is the file the S49-3 value commit actually moves.** It pins the hover ring's geometry in five rows, and S49-3's own e2e ruling routes the hover-vs-selection change to the **hover** side — so the one file the change lands on was the one file the gate never ran. A gate that reports green having never executed its subject is worse than no gate, because it also supplies a reason to stop looking. `spacing-affordance-geometry` and `reorder-paint` are here for the same reason from the other direction — see the witness set.

**The witness set must cover every family the phase touches — and r0's "byte-for-byte what shipped" was narrower than its own sentence.** It omitted the spacing/padding output entirely, which is two of the four parked items. An identity claim is only as wide as the witnesses carrying it, so the set is stated per family and per mode:

⚠ **THE HOVER ROW IS SPLIT AT r2', BECAUSE r1' NAMED A WITNESS THAT CANNOT WITNESS WHAT THE ROW CLAIMED.** `OverlayShell-hover-channels.test.tsx` contains **no border and no width assertion at all**: its six `border|width` lines are stub-rect INPUTS (`stubRect(desc, { top: 200, left: 10, width: 100, height: 20 })`) and its geometry rows pin `ring.style.top` — `packages/descvi/src/react/overlay/__tests__/OverlayShell-hover-channels.test.tsx#    // Canvas hover on reg-conn → its row highlights, ring anchors conn.` — the `expect(ring.style.top).toBe('8px')` row it heads, against a stub whose top is 10 against a stubbed top of 10 **is the 2-px-per-side INFLATION witness, and it is a good one**. It says nothing about width. The only hover-width pins in the tree are the two `toContain('1.5px')` rows in `OverlayShell-canvas-hover.test.tsx`. **One file witnesses the inflation; a different file witnesses the width; neither witnesses both.**

| family / field | default witness (no override) | override witness |
|---|---|---|
| selection ring — width and radius | `OverlayShell-selection-set.test.tsx` (an exact `toEqual` over a pinned style map: `packages/descvi/src/react/overlay/__tests__/OverlayShell-selection-set.test.tsx#      border: '2.5px solid rgb(234, 88, 12)',` and `packages/descvi/src/react/overlay/__tests__/OverlayShell-selection-set.test.tsx#      borderRadius: '6px',`), `selection-ring-pool.test.tsx` | real-renderer: override the radius field, assert BOTH computed radii moved (this is G49-6) |
| **hover ring — INFLATION** | **`OverlayShell-hover-channels.test.tsx`**, the `ring.style.top` rows. RED in **either** direction — the inflation is arithmetic on an exact pin. | real-renderer: override the inflation, assert the hover box moved and the SELECTION box did not |
| **hover ring — WIDTH** | **`OverlayShell-canvas-hover.test.tsx`**, `packages/descvi/src/react/overlay/__tests__/OverlayShell-canvas-hover.test.tsx#    // to rgb(). Solid, thin (1.5px).` — the two `expect(border).toContain('1.5px')` rows it heads (the anchor is on the comment because the assertion text occurs twice in the file). ⚠ **SUBSTRING-LIMITED: RED on any value that is not a superstring of `1.5`** — `'11.5px'` passes. This is the one-sidedness revision-brief r1's item R9 asked to be surfaced, on a second field. | real-renderer: override hover width, assert the border read back **exactly**, not by substring |
| reorder indicator | `reorder-paint-geometry.test.ts`, `reorder-paint.test.tsx` | real-renderer: override thickness, assert the painted band's cross-axis extent moved |
| spacing / padding glyph | ⚠ **NO DEFAULT WITNESS EXISTS FOR THE FIGURE, and that is a fact this plan states twice and must not contradict a third time.** `spacing-affordance-geometry.test.ts` is a strips-and-bands suite with **no glyph, `svg`, `path` or `d` assertion in it** — it witnesses WHERE affordances are placed, never WHAT is drawn in them, which is the same fact S49-5 states from the other side ("the path strings occur NOWHERE outside their own module"). It is in the run list as the PLACEMENT witness. The figure's only default constraint is the C46-1 `<svg>`-presence obligation in `e2e/spacing-gesture.spec.ts`, which is satisfied by any path. | real-renderer: override the figure routing, assert the emitted `d` changed and the `<svg>` survived. **This is the phase's FIRST assertion on the glyph's `d`** — and it is why S49-5 can ship without a contract-first split (there is no gate to move) while S49-1 still owes the `d` a witness. |

**Both modes run against the REAL renderer**, not against a helper that re-implements the merge — a witness that reads the record back has proved the record, not the paint.

**RED-when — THE DIRECTION IS NAMED PER FIELD, because half of these bounds are one-sided.** r0 said "change one field's default; the suite must fail", which is false for the reorder thickness in the only direction an executor is likely to try first. That is the same trap S49-2 documents at length and r0 then failed to propagate into the gate an executor actually runs:

| field | mutation that goes RED | mutation that does NOT |
|---|---|---|
| reorder indicator thickness | **RAISE it** (2 → 3). ⚠ **The run reports ONE failing test, not three.** Three `toBeLessThanOrEqual(2)` rows exist and all three sit in one `it()`, which vitest aborts at the first failure — measured, not read. An executor expecting three failures and seeing one must not conclude the gate half-worked. | **lowering to 1 — the bound is one-sided and the suite stays GREEN** |
| reorder length rule | either direction: three extent literals are exact | — |
| selection ring radius | **either direction** — pinned by an exact `borderRadius: '6px'` | — |
| selection ring width | **either direction** — an exact `toEqual` over a style map containing `border: '2.5px solid …'`. **No caveat: this row is not substring-limited and r1' wrongly attached one to it.** | — |
| **hover ring INFLATION** | **either direction** — `OverlayShell-hover-channels.test.tsx`'s `ring.style.top` rows are exact | — |
| **hover ring WIDTH** | **any value that is not a superstring of `1.5`** — `OverlayShell-canvas-hover.test.tsx` asserts by `toContain`, so `'11.5px'` is GREEN | **widening to `11.5px`, and any other value containing `1.5`.** No §7 candidate triple produces one, so the phase is not exposed — but the gate's reach stops here and S49-1a may not lean on this row to prove a refactor moved nothing (U-13) |
| spacing glyph figure | changing the emitted `d` — the override witness must assert the `d`, since no gate pins the path strings today (S49-5) | — |

**A mutation whose direction is not named above has not been demonstrated.** **This is the whole point of S49-1a being a separate commit**: if the refactor could move a value without a gate noticing, the refactor is not a refactor.

### G49-4 — the comparison machinery is absent from EVERY bundle this repo emits

> ⚠ **THIS GATE IS A COMMITTED SCRIPT AT r3' — `scripts/gate-g49-4-override-leak.sh`. Four earlier forms could not go RED, each for a different reason, and every one of them was found by RUNNING rather than by reading. Read the list before editing anything back.**
>
> **(1) r0: the shell always exited 0.** `pnpm build && grep … ; echo "exit=$?"` reports the exit status of `echo`'s predecessor into a variable nobody tests; the pipeline's own status is discarded by the `;`. The command could not fail a runner.
> **(2) r0/r1': the subject was argued, not named.** "Production" describes nothing this repo emits — `packages/descvi/package.json`'s build is an `echo` no-op.
> **(3) r1': `[ -d dist-designview ]` proves a DIRECTORY, not a bundle.** A stale directory, a partial write or a bare `mkdir` passes it and then greps nothing.
> **(4) r1'/r2': the grep aimed at an IDENTIFIER, which esbuild mangles.** There is no `minify` key in `vite.config.mts`, `descvi.vite.config.mts` or `packages/descvi/src/vite/`, so both builds take Vite's esbuild default. **Re-measured at r3': a planted `readLookOverride` came out of the bundle as `yM` and `grep -RIl 'readLookOverride' dist-designview/` found nothing, while the literal `descvi-look-override` survived byte-for-byte** — `ction yM(){return globalThis["descvi-look-override"]??null}`. A gate greping the reader's name returns the identical zero with and without the leak.
> **(5) r2': the precondition certified a chunk that cannot hold the subject.** `find dist-designview -name '*.js' -size +0c -print -quit` returns the **first** match — a per-page chunk. A build that emitted page chunks while dropping the overlay entry passed it and grepped clean.
> **(6) r1'/r2': `dist/` was excused on a claim that is FALSE — see C49-8's reversal.** `overlay: false` is a runtime branch, not a build exclusion; the overlay is in `dist/`. Scanning only `dist-designview/` left the bundle `vite.config.mts` calls "the deliverable" unguarded.

**Run.** `sh scripts/gate-g49-4-override-leak.sh`, from the repo root, with no arguments — the gate then builds **both** bundles itself, because a stale directory greps clean for the same reason an empty one does. Arguments name bundle directories to inspect instead, with no build; that path exists so leg 1 can be shown RED, and so `--selftest` can drive every leg against a staged fixture without a build at all.

⚠ **LEG 0 RUNS BEFORE THE BUILDS AS OF r4', AND THE OLD ORDER WAS SPENDING TWO FULL VITE BUILDS TO REACH AN ANSWER THAT NEEDED NONE.** Leg 0 is a grep over source. On every tree before S49-1 lands — which is every tree this plan is reviewed on — it is the leg that decides, so evaluating it after both builds meant building twice and then exiting on a source check. Measured after the hoist: **0.019 s** to the leg-0 RED on the real tree, against 4.7–4.8 s of builds it no longer pays for.

**The verdict is the EXIT STATUS**: `0` GREEN, `1` RED, `2` RED (precondition). ⚠ **Nothing in this gate captures a status into a variable and prints it. There is no `echo "exit=$?"` anywhere in it and adding one back disarms it.**

**Three legs, and leg 0 is the one r2' did not have.**

| leg | asserts | why it exists |
|---|---|---|
| **0 — SOURCE PIN**, before any build | the literal `descvi-look-override` occurs in **exactly one** file under `packages/descvi/src/react/overlay/`, **excluding `__tests__/`** | ⚠ **Without it the gate greps the bundle for a string nothing in source ever writes.** C49-8 obliged the reader to carry "a literal of the *shape*" — and a shape is not a pin. If S49-1's executor writes `descviLookOverride`, or splits the key across a template, legs 1 and 2 are GREEN forever having never looked at their subject. C49-2's single-reader contract already makes this a one-site claim, so the leg is free and it ties source and bundle to the same bytes. ⚠ **THE `__tests__` EXCLUSION IS NOT TIDINESS AND WITHOUT IT THIS LEG TURNS A UNIT TEST INTO A GATE FAILURE.** `__tests__/` sits under this same root, so the moment S49-1's executor writes a witness naming the key — which this repo's doctrine actively pushes them toward — the count is 2 and the gate is RED on the very story that lands the subject, for a reason unrelated to a leak. The workaround an executor reaches for is to spell the key differently in the test, **which is precisely the hole this leg exists to close.** Measured at r4': with the exclusion removed, a one-line witness turns the selftest's GREEN case RED, naming both files. A witness sets the override through the reader's exported SETTER (C49-2), so it never needs the literal. ⚠ **And one precision the earlier justification did not have: the single-reader contract is a claim about MODULES and this predicate is over FILES.** They coincide only because one module is one file here; a module split needs the leg re-expressed. |
| **1 — BUNDLE PIN**, per bundle | some emitted file carries the overlay marker `dsh-ring-layer` | replaces `[ -d ]` and replaces `find … -print -quit`. Asserts the thing the grep is supposed to be searching, rather than that *some* JavaScript exists. |
| **2 — THE LEAK**, per bundle | the literal is absent | the actual claim. `grep` exits non-zero when it finds nothing, which is the GREEN outcome, so the sense is inverted explicitly inside the script rather than by a bare `!` a later edit can drop. |

**The bundles, both of them, by name:** `dist-designview/` (`pnpm descvi:build`, `descvi.vite.config.mts`, `descvi.vite.config.mts#outDir: path.resolve(__dirname, 'dist-designview'),`) and `dist/` (`pnpm build`, `vite.config.mts`). ⚠ **`dist/` is a subject and r1'/r2' said it was not — C49-8 carries the reversal and the reproducing command.**

**DEMONSTRATION — THE COMMITTED FILE, INVOKED BY PATH, AT r4'.** The override does not exist yet, so the subject was staged the way S49-1 will land it: a reader in a scratch module under the overlay tree, imported and called from `applyRingStyle`. Both plant edits were undone afterwards — the scratch module deleted and `use-selection-rings.ts` restored from a snapshot taken after the work began, never with a checkout, its SHA-256 re-checked (`b418a73d…f5c`, identical) — and both bundles were rebuilt clean at the end, verified by `grep -rIlF -e descvi-look-override dist dist-designview` returning nothing.

**STATE A — the real tree today, no plant: leg 0 RED, before any build runs.**
```
$ sh scripts/gate-g49-4-override-leak.sh
--- leg 0 — the override literal is written in exactly ONE file under packages/descvi/src/react/overlay, excluding __tests__ ---
G49-4: RED (leg 0 — the literal 'descvi-look-override' occurs in 0 file(s) under packages/descvi/src/react/overlay, expected exactly 1)
$ echo $?
1
```
**That run took 0.019 s.** Before the r4' hoist it took two full Vite builds to print the same line.

**STATE B — GREEN: the reader planted WITH its `import.meta.env.DEV` guard, both bundles built by the gate.**
```
$ sh scripts/gate-g49-4-override-leak.sh
--- leg 0 — the override literal is written in exactly ONE file under packages/descvi/src/react/overlay, excluding __tests__ ---
SOURCE packages/descvi/src/react/overlay/zz-scratch-look-override.ts
--- build — a stale directory is not a bundle, so the gate makes its own ---
--- leg 1 [dist-designview] — the bundle carries the OVERLAY, not merely some JavaScript ---
OVERLAY CHUNK dist-designview/assets/index-SHnNOBEb.js
--- leg 2 [dist-designview] — the override literal is absent from the bundle ---
--- leg 1 [dist] — the bundle carries the OVERLAY, not merely some JavaScript ---
OVERLAY CHUNK dist/assets/index-CGHIq9Uf.js
--- leg 2 [dist] — the override literal is absent from the bundle ---
G49-4: GREEN (one source reader; every bundle carries the overlay and none carries the override literal)
$ echo $?
0
```
⚠ **Read leg 1 of that run twice: `dist` has an overlay chunk.** That single line is the `dist/` reversal, on the tree, in the gate's own output. ⚠ **And the whole run — both builds included — cost 4.80 s wall** (`time` on this machine; a second full run measured 4.66 s). That is the number S49-1's CI wiring is priced with, measured rather than deferred to whoever notices the job got slower. **Both chunk names are content hashes and move on the next source edit**; they are a record of one measurement, never something to compare against.

**STATE C — PLANTED-RED: the same reader with the `DEV` guard REMOVED.**
```
$ sh scripts/gate-g49-4-override-leak.sh
--- leg 0 — the override literal is written in exactly ONE file under packages/descvi/src/react/overlay, excluding __tests__ ---
SOURCE packages/descvi/src/react/overlay/zz-scratch-look-override.ts
--- build — a stale directory is not a bundle, so the gate makes its own ---
--- leg 1 [dist-designview] — the bundle carries the OVERLAY, not merely some JavaScript ---
OVERLAY CHUNK dist-designview/assets/index-B2TzzUph.js
--- leg 2 [dist-designview] — the override literal is absent from the bundle ---
LEAKED dist-designview/assets/index-B2TzzUph.js
G49-4: RED (leg 2 — the comparison override shipped in dist-designview)
$ echo $?
1
```
**The same unguarded build leaks into `dist/` too**, measured by pointing the gate at that directory in the no-build mode: `LEAKED dist/assets/index-Clyb4hXB.js`, `G49-4: RED (leg 2 — the comparison override shipped in dist)`. **That is the second half of the `dist/` reversal and the reason both bundles are scanned.**

**STATE D — `--selftest`: every leg driven against a staged fixture, WITH NO BUILD.** This is what makes the gate provable on every CI run at grep cost instead of at two-Vite-build cost.
```
$ sh scripts/gate-g49-4-override-leak.sh --selftest
SELFTEST ok   [default bundle set] a no-argument run scans both bundles: dist-designview dist
SELFTEST ok   [leg 0 — no reader in source at all] exit 1
SELFTEST ok   [GREEN — one reader, a __tests__ witness that does not count, a clean bundle] exit 0
SELFTEST ok   [control silent] the __tests__ witness was not counted as a source home
SELFTEST ok   [leg 2 — the literal shipped in the bundle] exit 1
SELFTEST ok   [leg 1 — a bundle of page chunks with no overlay entry] exit 1
SELFTEST ok   [a missing bundle directory is a FAILURE, not an empty result] exit 2
SELFTEST ok   [leg 0 — two source homes for one literal] exit 1
SELFTEST ok   [a missing overlay source root is a FAILURE] exit 2
G49-4 --selftest: GREEN (both bundles are in the default scan set, every leg produced its verdict, and the __tests__ control stayed silent)
$ echo $?
0
```
⚠ **THE FIRST LINE IS r5's ITEM AND IT IS THE `dist/` REVERSAL IN ITS ONLY EXECUTABLE FORM.** Every case under it names its bundle directories on the command line — the ARGUMENT path — which replaces the default set entirely, so **a copy with `dist` deleted from that set ran this selftest GREEN while the gate no longer looked at the bundle `vite.config.mts`'s own docblock calls "the deliverable".** The reversal was prose in four places and an argument nowhere. It is an assertion now:

```
$ sh /…/g4-dist-dropped-from-scope.sh --selftest   # a COPY with `dist` deleted from the default bundle set
SELFTEST FAIL [default bundle set] expected 'dist-designview dist' (2), got 'dist-designview' (1) — this repo emits TWO bundles and both are subjects (C49-8's r3' reversal)
SELFTEST ok   [leg 0 — no reader in source at all] exit 1
SELFTEST ok   [GREEN — one reader, a __tests__ witness that does not count, a clean bundle] exit 0
SELFTEST ok   [control silent] the __tests__ witness was not counted as a source home
SELFTEST ok   [leg 2 — the literal shipped in the bundle] exit 1
SELFTEST ok   [leg 1 — a bundle of page chunks with no overlay entry] exit 1
SELFTEST ok   [a missing bundle directory is a FAILURE, not an empty result] exit 2
SELFTEST ok   [leg 0 — two source homes for one literal] exit 1
SELFTEST ok   [a missing overlay source root is a FAILURE] exit 2
G49-4 --selftest: RED (1 assertion(s) failed — the gate cannot be trusted)
$ echo $?
1
```

**Line 6 of the GREEN run is r2''s precondition defect, staged permanently**: a fixture bundle carrying page chunks and no overlay entry: `find … -name '*.js' -size +0c -print -quit` would certify it and then grep clean, and leg 1 refuses it.

**STATE E — THE SELFTEST SHOWN ABLE TO FAIL, and it is the R35 measurement rather than a formality.** The script was copied with the `__tests__` exclusion deleted — the single change R35 rules is load-bearing — and the copy re-run:
```
$ sh /…/g4-no-exclusion.sh --selftest      # a COPY with --exclude-dir=__tests__ removed
SELFTEST ok   [default bundle set] a no-argument run scans both bundles: dist-designview dist
SELFTEST ok   [leg 0 — no reader in source at all] exit 1
SELFTEST FAIL [GREEN — one reader, a __tests__ witness that does not count, a clean bundle] expected exit 0, got 1
    | --- leg 0 — the override literal is written in exactly ONE file under packages/descvi/src/react/overlay, excluding __tests__ ---
    | SOURCE packages/descvi/src/react/overlay/__tests__/look-override.test.ts
    | SOURCE packages/descvi/src/react/overlay/look-override.ts
    | G49-4: RED (leg 0 — the literal 'descvi-look-override' occurs in 2 file(s) under packages/descvi/src/react/overlay, expected exactly 1)
SELFTEST FAIL [control leaked] the __tests__ witness was counted as a source home
SELFTEST ok   [leg 2 — the literal shipped in the bundle] exit 1
SELFTEST ok   [leg 1 — a bundle of page chunks with no overlay entry] exit 1
SELFTEST FAIL [a missing bundle directory is a FAILURE, not an empty result] expected exit 2, got 1
    | --- leg 0 — the override literal is written in exactly ONE file under packages/descvi/src/react/overlay, excluding __tests__ ---
    | SOURCE packages/descvi/src/react/overlay/__tests__/look-override.test.ts
    | SOURCE packages/descvi/src/react/overlay/look-override.ts
    | G49-4: RED (leg 0 — the literal 'descvi-look-override' occurs in 2 file(s) under packages/descvi/src/react/overlay, expected exactly 1)
SELFTEST ok   [leg 0 — two source homes for one literal] exit 1
SELFTEST ok   [a missing overlay source root is a FAILURE] exit 2
G49-4 --selftest: RED (3 assertion(s) failed — the gate cannot be trusted)
$ echo $?
1
```
**Those three failures are exactly the future R35 describes**: a one-line witness naming the key makes the gate RED on the story that lands the subject, and it also swallows an unrelated precondition, because leg 0 now fails before the bundle check is ever reached.

**RED-when, for an executor.** Delete the `import.meta.env.DEV` guard around the override reader and re-run; the literal must be found. **The RED-leg output, showing the matching file, goes in S49-1's commit message.** Only then is the GREEN leg evidence.

**If this gate could not be written**, the claim that would go unguarded is principle 5 and C49-8 together: that the comparison machinery is provably absent from what ships. Nothing else in the phase measures a bundle, and a guard in source is a claim about what a bundler will do rather than a record of what it did.

### G49-5 — the shipped value has exactly one home

> ⚠ **THIS GATE HAD NO OWNER, NO MOMENT, NO LANDING COMMIT AND NO RUNNABLE COMMAND FOR FOUR REVISIONS — AND ITS ACCEPTANCE WAS SELF-SEALING.** Its Run was *"a field-aware scan over the overlay tree"*: a description, not a command, **in the revision whose whole thesis is that a gate living in prose gets re-implemented by every reader.** And it *"enumerates the fields it covers rather than claiming the family"* with **no field list anywhere in the plan**, so any omitted field was out of scope by construction and the gate could not go RED for the omission. That is the same defect the plan diagnoses for S49-P and then committed here. **At r4' it is `scripts/gate-g49-5-one-home.sh`, it lands in S49-1a, and its five fields are enumerated in the script and below.**

**Run.** `sh scripts/gate-g49-5-one-home.sh`, from the repo root. **The verdict is the EXIT STATUS**: `0` GREEN, `1` RED (a field row failed), `2` RED (the scan root is missing).

**Two legs PER FIELD, because one is not enough and the obvious precedent supplies neither.**

| leg | asserts | why |
|---|---|---|
| **home** | the field's assignment form occurs **exactly once** under `packages/descvi/src/react/overlay/`, excluding `__tests__` | the "one home" claim itself |
| **bare** | the literal form the refactor is supposed to have ELIMINATED occurs **zero** times | ⚠ **without it the gate cannot tell "one home" from "no home".** `packages/descvi/src/react/overlay/__tests__/resize-drag-machine.test.ts#expect(countExports("export const POINTER_DRAG_THRESHOLD_PX = 4;")).toBe(1);` is a census over `export const` DECLARATIONS, and four of the five values here are a record FIELD or a bare literal inside a template string — neither is an `export const`, so a declaration census over them returns 1 by finding nothing twice |

**THE FIELDS IT COVERS, WHICH IS ITS ENTIRE REACH:**

| field | home form | bare form it forbids | state on this tree |
|---|---|---|---|
| selection ring width | `selectionWidthPx:` | `2.5px solid` | **RED** — 0 homes, 1 bare |
| selection ring radius | `selectionRadiusPx:` | `borderRadius = "6px"` | **RED** — 0 homes, **2 bare** (that IS C49-3's defect, counted) |
| hover ring width | `hoverWidthPx:` | `1.5px solid ${shades.light}` | **RED** — 0 homes, 1 bare |
| hover ring inflation | `hoverInflatePx:` | `r.width + 4` | **RED** — 0 homes, 1 bare |
| reorder indicator thickness | `export const REORDER_INDICATOR_THICKNESS_PX =` | *(none — the declaration IS the home, and this is the one row the `countExports` precedent does transfer to)* | **GREEN** — 1 home |

⚠ **TWO CONTRACTS THIS TABLE ENCODES THAT NO CONTRACT STATED UNTIL r5, BOTH BINDING ON S49-1a's EXECUTOR.** *(1)* **The home column is four exact key spellings, so the field shape is contract**: nesting them (`selection: { widthPx: 2.5 }`) satisfies C49-1's wording and leaves four of these five rows at `homes=0` forever — S49-1a's Lands names the four spellings for that reason. *(2)* **The bare column is `grep -F` over the whole tree, comments included**, so a docblock explaining the retired literal turns its own row RED; describe the retired value, never spell it.

⚠ **THE HOVER-WIDTH ROW IS SPELLED WITH ITS COLOUR EXPRESSION AND THAT IS NOT PEDANTRY — IT WAS MEASURED BEFORE THE ROW SHIPPED.** The bare string `1.5px solid` occurs **twice** under that root: the hover ring, and the phase-48 resize chip's border, which takes the group `deep` shade. **A row matching the shorter string would be permanently RED on a value C49-7 forbids this phase to touch** — a gate whose only repair is to break an owner ruling, which is the r1' leg-(b) shape in a new family. The first draft of this script had exactly that row; the two-line grep that found it is the reason it does not ship.

⚠ **WHAT IT DELIBERATELY DOES NOT COVER, NAMED RATHER THAN LEFT TO THE HEADING:** the **spacing and pad glyph figures**. Their record (`SPACING_GLYPH_PATHS`) already exists and its entries ARE the values, so "one home" is true of them by construction and there is no second form to hunt. What those two need is a witness on the emitted `d`, which is G49-3's override column and S49-1's obligation — **not this gate**. A field with no row here is a field this gate does not cover, and that sentence is only honest with a list beside it.

**DEMONSTRATION — THE COMMITTED FILE, INVOKED BY PATH, AT r4'.**

**The real working tree, RED by construction** — and the fifth row is what shows the instrument can pass a row rather than failing everything it is pointed at:
```
$ sh scripts/gate-g49-5-one-home.sh
--- one home per parametrised field, under packages/descvi/src/react/overlay (excluding __tests__) ---
FIELD RED selection-ring-width  homes=0 (want 1)  bare=1 (want 0)
FIELD RED selection-ring-radius  homes=0 (want 1)  bare=2 (want 0)
FIELD RED hover-ring-width  homes=0 (want 1)  bare=1 (want 0)
FIELD RED hover-ring-inflation  homes=0 (want 1)  bare=1 (want 0)
FIELD OK  reorder-indicator-thickness  homes=1 (want 1)  bare=n/a (want 0)
G49-5: RED (4 field(s) do not have exactly one home)
$ echo $?
1
```
**Those four REDs are D49-0's fact 2, executed.** The ring has no constants; its look is inline literals; `bare=2` on the radius is the two independent `6px` writes C49-3 exists to couple. **S49-1a is the story that turns this GREEN, which is why the gate lands there.**

**`--selftest`** — a fixture record, both RED mutations, the `__tests__` control, and the precondition:
```
$ sh scripts/gate-g49-5-one-home.sh --selftest
SELFTEST ok   [field manifest] the gate enumerates exactly: selection-ring-width selection-ring-radius hover-ring-width hover-ring-inflation reorder-indicator-thickness
SELFTEST ok   [no record at all — every field has zero homes] exit 1
SELFTEST ok   [GREEN — one home per field, no bare literal anywhere] exit 0
SELFTEST ok   [GREEN — a __tests__ witness naming a field and a bare literal changes nothing] exit 0
SELFTEST ok   [home leg RED — a second assignment of selection-ring-width] exit 1
SELFTEST ok   [row named] home leg / selection-ring-width — the failing row is selection-ring-width
SELFTEST ok   [bare leg RED — the retired literal re-introduced for selection-ring-width] exit 1
SELFTEST ok   [row named] bare leg / selection-ring-width — the failing row is selection-ring-width
SELFTEST ok   [home leg RED — a second assignment of selection-ring-radius] exit 1
SELFTEST ok   [row named] home leg / selection-ring-radius — the failing row is selection-ring-radius
SELFTEST ok   [bare leg RED — the retired literal re-introduced for selection-ring-radius] exit 1
SELFTEST ok   [row named] bare leg / selection-ring-radius — the failing row is selection-ring-radius
SELFTEST ok   [home leg RED — a second assignment of hover-ring-width] exit 1
SELFTEST ok   [row named] home leg / hover-ring-width — the failing row is hover-ring-width
SELFTEST ok   [bare leg RED — the retired literal re-introduced for hover-ring-width] exit 1
SELFTEST ok   [row named] bare leg / hover-ring-width — the failing row is hover-ring-width
SELFTEST ok   [home leg RED — a second assignment of hover-ring-inflation] exit 1
SELFTEST ok   [row named] home leg / hover-ring-inflation — the failing row is hover-ring-inflation
SELFTEST ok   [bare leg RED — the retired literal re-introduced for hover-ring-inflation] exit 1
SELFTEST ok   [row named] bare leg / hover-ring-inflation — the failing row is hover-ring-inflation
SELFTEST ok   [home leg RED — a second assignment of reorder-indicator-thickness] exit 1
SELFTEST ok   [row named] home leg / reorder-indicator-thickness — the failing row is reorder-indicator-thickness
SELFTEST ok   [bare leg n/a] reorder-indicator-thickness — the declaration IS the home, so there is no bare form to forbid
SELFTEST ok   [GREEN again once every plant is removed] exit 0
SELFTEST ok   [a missing scan root is a FAILURE, not an empty result] exit 2
G49-5 --selftest: GREEN (both legs produced a RED per field, and the __tests__ control stayed silent)
$ echo $?
0
```
**Both RED-when mutations are in there as staged plants rather than as instructions**: a second assignment of the field in a second record literal (the home leg), and the bare literal re-introduced in a painter beside the record read (the bare leg). The GREEN either side of them is the control — **the fixture returns to 0 when the plants are removed, so the RED is attributable to the plant and not to the fixture.** Identical output under `zsh`.

⚠ **AND r5 IS WHY THERE ARE NOW TEN OF THOSE PLANTS RATHER THAN TWO: THE PLANTS ARE DRIVEN FROM `FIELDS` ITSELF, SO AN ENUMERATED FIELD CANNOT BE UNTESTED — AND THE FIRST LINE IS WHAT STOPS `FIELDS` SHRINKING UNDER THEM.** A loop over the list can never notice a deletion; a manifest written a second time can. **A copy with two of the five fields deleted ran the r4' selftest GREEN**, which is a gate covering three fields under a heading claiming five. The proof:

```
$ sh /…/g5-two-fields-deleted.sh --selftest   # a COPY with the two hover rows deleted from FIELDS
SELFTEST FAIL [field manifest] the enumeration moved without this assertion moving with it
    | expected: selection-ring-width selection-ring-radius hover-ring-width hover-ring-inflation reorder-indicator-thickness
    | actual:   selection-ring-width selection-ring-radius reorder-indicator-thickness
SELFTEST ok   [no record at all — every field has zero homes] exit 1
SELFTEST ok   [GREEN — one home per field, no bare literal anywhere] exit 0
SELFTEST ok   [GREEN — a __tests__ witness naming a field and a bare literal changes nothing] exit 0
… every remaining field's home and bare plant still RED, still named …
SELFTEST ok   [GREEN again once every plant is removed] exit 0
SELFTEST ok   [a missing scan root is a FAILURE, not an empty result] exit 2
G49-5 --selftest: RED (1 assertion(s) failed — the gate cannot be trusted)
$ echo $?
1
```

**The elided rows are the point, not a saving**: they are all `ok`. The crippled copy's mechanism is perfect and its reach is three fields — which is exactly the state the r4' selftest could not distinguish from the shipped one.

**RED-when, for an executor.** Run `--selftest`. For a field-specific check on the real tree after S49-1a: add a second assignment of that field anywhere under the overlay tree and confirm its row alone goes RED.

**What it catches that G49-4 does not.** G49-4 proves the override does not ship. G49-5 proves the DEFAULT was not quietly duplicated — the failure mode where production and the surface agree today and drift on the next edit.

**If this gate could not be written**, the claim that would go unguarded is C49-1 and C49-4 together: that every look value has one home and that the shipped default is the record's default. It CAN be written and is, for the five fields above; for the two glyph figures it is not written, and the sentence above says so.

### G49-6 — hover and selection share what they are supposed to share

**Run.** A unit assertion that the two rings' radius comes from one field: mutate the field and assert BOTH computed radii moved.
**RED-when.** Re-introduce a second literal for either ring's radius; the mutation moves one ring and not the other, and the row fails.
**Why it is a gate and not a review note.** C49-3. Today the equality holds by coincidence of two literals — G49-5 counts them, `bare=2` — and nothing in the repo would notice if it stopped, which is a defect that exists before any experiment does.

⚠ **IT LANDS IN S49-1a, AND FOR FOUR REVISIONS IT LANDED NOWHERE.** No story's Lands or "Gates it adds" named it. **S49-1a is the only story where the assertion is both writable and meaningful**: before it there is no field to assert on, and after it the coupling is already load-bearing, so an assertion added later is a claim about code nobody re-read. It is a vitest assertion in the ring witness file rather than a shell script — **the distinction is not arbitrary**: G49-2/3/4/5 are scans and orchestration, which is what a shell gate is good for, and this one needs a rendered ring, which is what the witness suite already provides.

### G49-7 — the look change did not silently relax its own gate

⚠ **IT IS NOT A NUMBERED GATE ANY MORE, AND THAT IS THE POINT RATHER THAN A DEMOTION.** As a numbered gate it had no owner, no moment and no landing commit for four revisions — the same defect it exists to prevent, committed by the mechanism meant to prevent it. **A gate nobody schedules is a habit with a number on it**, and the plan already records that a standing RED-first resolution is exactly what failed in phase-47, three times.

**So it becomes a PER-STORY OBLIGATION, in the done-when of each value story (S49-2, S49-3, S49-4, S49-5, and S49-6 if it is taken):** after the value lands, re-run the gate that was amended in that story's contract commit, **demonstrate it RED on the mutation that story names**, and record the RED output beside the value commit. A story that cannot produce one has shipped scaffolding, and the story does not close.

**Why the obligation is stronger than the numbered gate was.** It has a runner (the story's executor), a moment (immediately after the value lands), an artefact (the RED transcript in the commit message) and a consequence (the story does not close) — four things the numbered gate had none of. **The register keeps its number only as a cross-reference**, so a reader who meets `G49-7` elsewhere in this plan is sent here.

## 7. Owner questions

Two kinds, kept apart because they are answered at different moments. **U49-A…** are answered on the PLAN, before execution. **U49-1…U49-6** are the mid-phase table (D49-3) and are answered ON THE SURFACE, after S49-1 lands.

### Answered on the plan

- **U49-A — Is (b), the dev-only runtime override on the live overlay, the surface the owner wants? ✅ RULED (b) BY THE OWNER, 2026-09-04.** The recommendation below was taken as written; D49-1 is closed and the option set does not reopen except through S49-P's abort, which remains the only path back.

  *(the question as it stood, kept because the reasoning is what S49-P tests)* Is (b) the surface the owner wants? ⚠ **This is the one question the plan cannot answer for them, because the plan's argument for (b) rests on a claim about how the owner judges** — that switching values under a live gesture beats seeing three renderings at once. **Recommendation: (b).** Cost of (b): the ring's three inline literals get named (real source work, gated); the override needs a leak gate. Cost of choosing (a) instead: three of the four items become unreachable without exporting private writers, and the two facts `reorder-indicator-look` says it needs are not observable. Cost of choosing (c): phase-47's re-pin price for subjects that already exist.
- **U49-B — Does the optional phase-47 U3 rider (the reorder arming threshold) ride this phase? ✅ RULED NO BY THE OWNER, 2026-09-04 — the recommendation below was taken.** S49-6 does not run; the threshold stays 4 px; the item stays owner-owned in `docs/handoff/260831-phase-47-close.md` §2 rather than being silently closed, and U49-7 drops out of the mid-phase table.** ⚠ **RECOMMENDATION: NO — and this REVERSES the framing the item arrives with.** `docs/handoff/260831-phase-47-close.md#G47-3 already pins that the reorder boundary moves with the constant, so testing is one line under a watching gate.` reads as "cheap". **Measured, it is the most expensive item in the bundle**, and for a reason the phase-47 sentence could not see: the constant is **not reorder's**. It is `packages/descvi/src/react/overlay/canvas/pointer-thresholds.ts#export const POINTER_DRAG_THRESHOLD_PX = 4;`, consumed by five gestures — resize, Shift aspect-lock, the phase-45 shield's travel guard, the spacing drag, and the reorder arm — and the two spacing render floors are declared as aliases of it. Changing it moves:
  - three hard pins, one of which is a **source-text census**: `packages/descvi/src/react/overlay/__tests__/resize-drag-machine.test.ts#expect(countExports("export const POINTER_DRAG_THRESHOLD_PX = 4;")).toBe(1);`, plus `packages/descvi/src/react/overlay/__tests__/resize-drag-wiring.test.tsx#expect(POINTER_DRAG_THRESHOLD_PX).toBe(4);` and a boundary row pinned to literals **on purpose** so it cannot move with the constant;
  - a regime tripwire that constrains the new value to roughly `[3, 6]` (`packages/descvi/src/react/overlay/__tests__/spacing-affordance-geometry.test.ts#⚠ THE FIXTURE's FLOOR-REGIME SUBJECTS ARE PINNED TO THE FLOOR's ACTUAL VALUE, never to the literal 4`);
  - G47-3's own diagonal control, RED above 4.243 (`packages/descvi/test/reorder/reorder-drag-machine.test.ts#expect(Math.hypot(3, 3) >= POINTER_DRAG_THRESHOLD_PX).toBe(true);`);
  - two e2e sub-threshold rows that arm if the value drops;
  - and ⚠ **two copies of `4` that no gate ties to the symbol and that therefore go STALE-GREEN rather than red** — `packages/descvi/src/react/overlay/__tests__/handle-geometry.test.ts#const PURCHASE_FLOOR_PX = 4;` and a `4 px floor` literal in `e2e/resize-handles.spec.ts`. Phase-48's owner ruling locked `cornerNarrowPx / 2 == POINTER_DRAG_THRESHOLD_PX`; moving the threshold breaks that identity **with no gate firing**, and G48-4a's constants checker does not cover this file.
  - and, for completeness of the blast radius rather than as a cost: **three dogfood files import the symbol** — `src/app/sandbox/handle-lab/handle-lab.tsx`, `src/app/sandbox/handle-lab/candidate-lab.tsx`, `src/app/sandbox/handle-lab/owner-spec.ts`. `src/app/**` is out of the deliverable scope (AGENTS.md), so they are not a reason not to do it; they are three more places a reader will find the old number and they were absent from r0's enumeration.

  **So the honest price is: a shared five-gesture constant, a value box that the diagonal control closes at 4.243 from above and the regime tripwire closes at ~3 from below — i.e. `[3, 4.243]`, ONE alternative value — and two hand-added pins before anything is safe to change.** ⚠ **The `[3, 6]` framing above is the tripwire's box alone and is NOT the reachable box**; the diagonal control binds first. r0 carried `[3, 6]` into the owner table and offered 5 px and 6 px, both of which are RED on arrival. That is not a rider on a look phase; it is a small phase. Cost of taking it anyway: the above, plus the risk that a threshold change is judged in the same live pass as four look changes and the owner cannot attribute what they felt to which. Cost of leaving it: it returns to `docs/handoff/260831-phase-47-close.md` §2 still owned — **which is where it already is**, so leaving it loses nothing that is not already lost. **If the owner wants it anyway, take it as S49-6 and take the two stale-green pins with it; do not take it without them.**
- **U49-C — Does phase-47's U9 option (E) — whether the `n / N` readout should stop claiming to be a visual count — ride S49-2? ✅ RULED BY THE OWNER, 2026-09-04: the OBSERVATION SHEET, not a story.** The recommendation below was taken; if the driving answer is "yes, change it", it becomes a follow-up backlog row rather than shipping in this phase.** It is stalled behind this same surface (`docs/handoff/260831-phase-47-close.md#(E) is a form decision stalled behind the same comparison surface.`) and it is a question about the *same gesture* the owner will be driving to judge the indicator. **Recommendation: put it on the S49-2 observation sheet as a question to answer while driving, not as a story.** Cost of a story: the readout's text is a contract with its own gate. Cost of the observation sheet: if the answer is "yes, change it", it becomes a follow-up row rather than shipping this phase.

### The mid-phase table (D49-3) — the owner fills the two right-hand columns

**Five columns. The owner fills `Chosen` and `Defer?`; every other cell is already filled in.**

| # | Item | Candidates (the shipped value is one of them) | Chosen | Defer? |
|---|---|---|---|---|
| U49-1 | Reorder indicator — **weight** | (1) 2 px *(shipped)* / (2) 3 px / (3) 4 px | | |
| U49-2 | Reorder indicator — **length rule** | (1) members' cross-axis extent *(shipped — the 16 px-tick read on short items)* / (2) the parent's cross-axis extent / (3) the extent plus a fixed overhang | | |
| U49-3 | Selection ring — **radius** | (1) 6 px *(shipped)* / (2) 4 px / (3) 0 px (backlog direction (a), drop the rounding) | | |
| U49-4 | Selection ring — **width, AND the hover relation, as ONE choice** | ⚠ **Each candidate is a numbered TRIPLE `(selection px, hover px, hover inflation px)`, because the relation is not a number and a slash-list of loose values does not parse into pairs.** (1) `(2.5, 1.5, 2)` *(shipped: hover thinner, on a box inflated 2 px per side)* / (2) `(2, 2, 2)` — equal weight, size relation unchanged / (3) `(2.5, 2.5, 4)` — **hover reads LARGER** (backlog direction (c), the Figma relation), achieved on the HOVER side only / (4) `(2.5, 1.5, 4)` — hover larger in size, still lighter in weight | | |
| U49-5a | Spacing affordance — **the MARK** | (1) two double-headed arrows per edge *(shipped)* / (2) one `-` mark per edge | | |
| U49-5b | Spacing affordance — **the REVEAL** | (1) revealed on strip hover *(shipped)* / (2) revealed when the pointer is inside the object | | |
| U49-6 | Pad glyph | (1) arrow-up-to-line *(shipped)* / (2) a plain directional bar (`-` on horizontal edges, `l` on vertical) — **the standing direction from the G48-8 pass** | | |
| ~~U49-7~~ | ⚠ **DROPPED — U49-B was ruled NO by the owner on 2026-09-04, so this row is not asked.** The row is struck rather than deleted because its derivation is the record of why the rider is expensive. ~~Arming threshold — **shared by five gestures, not reorder's own** | (1) 4 px *(shipped, ratified for resize)* / (2) 3 px. ⚠ **NO UPWARD VALUE IS ON THIS TABLE — see the box below.** | | |

⚠ **U49-5a and U49-5b are two rows because S49-4 plans for exactly the outcome one row cannot record.** The mark is nearly free (a change to `SPACING_GLYPH_PATHS` and `figureFor`); the reveal is the expensive half (it moves when affordances are placed at all, which touches the hit model). "Take the mark, defer the reveal" is a likely and legitimate answer, and it needs two `Defer?` cells to exist.

> ⚠ **U49-7's REACHABLE BOX IS DERIVED IN U49-B AND NOT RESTATED HERE — see the one-home note in S49-6.** What this table needs from it: r0 offered 5 px and 6 px, **both RED on arrival** before anyone measures anything, so the owner was being offered two cells that could not be filled. **3 px is the only genuine alternative to the shipped 4.** Any upward value is not a candidate on this table at all — it is a **G47-3 re-pricing story**, i.e. a decision to move the diagonal control's own assertion, and it must be brought as one rather than smuggled in as a value.
>
> **This makes U49-B's NO recommendation stronger, not weaker.** The rider was already the most expensive item in the bundle; it now also has a candidate set of two, one of which is the status quo. **Keep the NO.**

⚠ **U49-2's candidates are not free-form.** "Length = the members' cross-axis extent" is what produces the 16 px tick the backlog row flags; the parent's extent is the alternative that makes the line read as a column divider. The owner should judge these on `/shop/member-list`'s 7-member row **and** `/lab/tests/reorder-flow`'s vertical five — the row names both, and the point of naming both is that a rule can look right on one and wrong on the other.

## 8. ADR

**Decision.** Build the comparison surface as a **dev-only runtime override on the live overlay** (D49-1 (b)), parametrised by **per-family constants records with a single `import.meta.env.DEV`-guarded override reader** (D49-2 (ii)), gated by **four committed gate scripts that land in stories and run in CI with their own `--selftest`s** (§6's rule 5), of which the leak gate greps a STRING LITERAL in BOTH bundles this repo emits — `dist-designview/` and `dist/`** (G49-4 — the bundle because a guard in source is a claim about what a bundler will do; the literal because esbuild mangles every identifier and a name-grep returns the same zero either way; **both bundles because `overlay: false` is a runtime branch and `dist/` carries the overlay, which r1' and r2' had wrong**; and with a source-pin leg, because a bundle grep for a string nothing in source writes is GREEN forever). Take the four parked visual decisions on that surface behind a **mid-phase owner table with per-row deferral** (D49-3), and discharge the v3.5 close as S0 by **moving two dead v3 plans into the archive directory that already exists**, replacing the tracker's now-stale deferral, and **repairing the archive INDEX — which asserts both plans are live at the paths the move invalidates, and which has no row for the destination directory at all** (D49-4).

**Drivers.** D-A fidelity of the comparison to the shipped rendering; D-B gate blast radius per iteration; D-C the phase must not stall on the owner.

**Alternatives considered.**
- *A static gallery screen* (D49-1 (a)) — reaches one of four painters, and buying the other three means exporting three module-private writers, which is the leak D49-2 exists to prevent; also cannot render a transient affordance side by side with itself. **The side-by-side it WAS wanted for is delivered instead by staging the persistent subject — the selection ring — in the multi-select pool, at no export cost.**
- *Promoting `lab/tests/**` fixtures* (D49-1 (c)) — supplies subjects, not values; the subjects it would supply already exist; pays phase-47's corpus-census re-pin price (D49-1 (c) carries the regenerating command rather than a carried-forward integer).
- *A duplicated renderer for the comparison path* (D49-2 (iii)) — no oracle can hold two furniture renderers together, so the owner would be judging the copy.
- *Archive everything `8db53ad` deliberately kept* (D49-4 (A)) — freezes documents that this plan and three product source files still consume.
- *Archive nothing* (D49-4 (C)) — leaves a deferral that has already survived two phase closes.

**Why chosen.** **Structurally: three of the four subjects have no callable painter**, so a gallery reaches one item in four and only by exporting three module-private style writers — i.e. by manufacturing in source the very leak the phase exists to prevent. That reason turns on no claim about how a person judges and survives every gate re-specification in this revision. **Then, on the form of the comparison:** three of the four subjects exist only while a gesture is in flight and there is one pointer, so their comparison is temporal; **the selection ring is persistent, so its comparison is spatial** — two pooled siblings at two candidate values in one viewport, which the shipped multi-select pool already supports. Temporal where the subject vanishes, spatial where it does not; both on the live overlay, so neither needs a second renderer. Everything else follows: parametrised constants need a re-render channel (the existing remeasure `tick`, bumped from the bare `[` / `]` keys, because reaching for a pointer control extinguishes the subject and every modifier and every obvious key is already taken — Escape terminates the drag, Enter commits, Cmd+Z undoes, and a bare Meta or Control silently re-targets the hover preview, which changes the subject rather than losing it) and a leak proof against the one bundle that actually contains the overlay; and a mid-phase owner gate needs a table with defaults so a deferral costs a row and not the phase. S0's scope follows from the consumption test the tracker's own deferral sentence states, applied per file instead of per era.

**Consequences.**
- The ring's look becomes named constants (S49-1a) — a permanent improvement the `selection-ring-treatment` row needs whatever surface had won.
- Hover and selection stop being two unrelated literal sets (C49-3); this is a behavioural contract change, not only a refactor.
- The overlay gains a dev-only code path. Its absence from **both** emitted bundles is now something the repo asserts, which is a gate that must be kept alive.
- ⚠ **The phase now ships FOUR GATE SCRIPTS as deliverables, each with a `--selftest`, each landing in a named story and each wired into `.github/workflows/ci.yml`'s verify job** — `scripts/gate-g49-2-archive-pointers.sh` (S49-0), `scripts/gate-g49-3-look-witnesses.sh` and `scripts/gate-g49-5-one-home.sh` (S49-1a), `scripts/gate-g49-4-override-leak.sh` (S49-1). ⚠ **The CI half is the half r3' left out, and without it the escalation was decorative**: three untracked scripts whose only RED proof lived in a plan that gets archived. That is a consequence of r3''s escalation finished at r4', and it is permanent: three consecutive review rounds proved that a gate written as prose is re-implemented by every reader, and three consecutive rounds of `PM-10` on two contracts is what the cost of that looked like. **They are repo scripts and inherit the repo's obligations** — a later phase that renames a witness or a scan root must move the script with it, which is exactly the failure the missing-root preconditions turn RED instead of silent.
- ⚠ **The candidate-switch keybinding carries a text-entry guard as contract (C49-2), not as polish.** `[` is not a free key: it opens a Tailwind arbitrary value, the corpus is full of them, and OverlayShell's keydown listeners are capture-phase. The guard is copied from the repo's own undo handler, `event.isComposing` is included, and S49-P leg (5) tests it with the IME on — under which the bracket channel may be dead outright, in which case the binding moves to a function key.
- The citation gate's checked-anchor count drops when two plans move into the excluded archive (D49-4's stated consequence).
- ⚠ **Phase-49 does not close the parked items by itself** — it closes them only if the owner fills the table. A deferred row leaves a backlog row alive with a better record than it had.

**Follow-ups.**
- Phase-47 routed items (ii) and (iii) stay routed (§2a).
- KI-47 stays unrouted and needs fresh owner input.
- U9 option (E) becomes a follow-up row unless the observation sheet answers it (U49-C).
- Archiving `ralplan-phase-46-*`, `ralplan-phase-48-*`, `.omc/specs/v3-layout-panel-visual-spec.md`, `.omc/research/phase46-*`, `.omc/research/phase48-*` and `.omc/spikes/phase48-model/` as one set, when their consumers are gone.
- The two ungated fixture lists phase-48 named (`LEG_B_FIXTURES` vs `FIXTURE_SIZES`) remain bound by nothing; not this phase's.

## 9. Risks

Each is paired with a MECHANISM — something that would have to be in place, not an intention.

⚠ **THE ROWS ARE `PM-n`, NOT `Rn`, AND THE RENAME AT r2' IS NOT COSMETIC.** `R1`, `R5`, `R8`, `R9`, `R10` are also item ids in the revision briefs this plan was written from, meaning something else entirely — and both spellings appeared in this file, pointing at both registers, with nothing to tell them apart. S49-3's shade note and S49-4's e2e-grep note now read `(C49-7, PM-8)` and `(PM-5)`; where the text means a brief item it says so in words ("revision-brief r1's item R1").

| # | Risk | Mechanism |
|---|---|---|
| PM-1 | **The override leaks into the shipped overlay** and a candidate value ships as if it were decided. | `scripts/gate-g49-4-override-leak.sh` greps **a string literal** in `dist-designview/` **and in `dist/`** — ⚠ **both, because r3' measured that `overlay: false` is a runtime branch and the overlay IS in `dist/`; excusing it would have left the bundle the config calls "the deliverable" unguarded** — behind an **overlay-MARKER precondition** (a directory is not a bundle, and neither is the first `.js` a `find` happens to meet), and behind a **source pin** that the literal occurs in exactly one overlay module, without which the bundle grep hunts a string nothing in source writes. The script's own non-zero exit is the failure and there is no `echo "exit=$?"` to swallow it. **All four states RUN from the committed file at r3' and re-run at r4' after the leg-0 hoist and the `__tests__` exclusion, output pasted in the gate — plus a `--selftest` that drives every leg against a staged fixture with NO build, and which was itself shown RED from a broken copy.** A guard present in source proves nothing about what a bundler emitted; a grep over a directory that never held the subject proves less than that; and a grep for an identifier esbuild has renamed to `vM` proves nothing at all. |
| PM-2 | **The ring refactor (S49-1a) moves a pixel while claiming not to.** A "pure rename" that changes `6px` to a constant initialised to `6` is exactly the shape of change that is believed rather than checked. | S49-1a lands with the S46-1 property: every value identical, no pixel moved, and it is verified by the same computed-style assertions that already watch the ring — not by review. The commit that names the constants edits no gate. |
| PM-3 | **Hover and selection drift apart** because the two 6 px radii are two literals, and an experiment changes one. | C49-3 makes the shared value a single field. The risk is real *today*, before any experiment: the mechanism is the refactor, not vigilance. |
| PM-4 | **A look change turns a gate RED and the story quietly relaxes the gate to match.** | C49-5's split: the contract commit contains no pixel change and the look commit contains no gate edit, so a relaxation cannot hide inside a restyle. This is `.omc/specs/v3-layout-panel-visual-spec.md#⚠ **Both are CONTRACT changes, not CSS changes.**`'s discipline and the S46-1/S46-2 precedent, not a new rule. |
| PM-5 | **The story's "lands" list misses an e2e spec that asserts the old look by PROPERTY rather than by symbol.** Phase-48 shipped this exact defect three times. | Every story's lands list is built by grepping the e2e tree for the numeric property (`2.5px`, `6px`, the glyph `d` strings), not only for the identifier — and the grep's non-zero baseline is recorded before the change, so a post-change zero is evidence rather than a misspelling. |
| PM-6 | **The owner defers everything** and the phase ships only a surface. | Every story ships its contract and gate move regardless (C49-6), and `padding-glyph` executes on a standing direction rather than a pending one. The floor is: the ring's values are named, hover and selection are one parameter set, the pad glyph is fixed, and the v3.5 close is done. |
| PM-7 | **The mid-phase gate stalls the phase** because the owner is not available when S49-1 lands. | Order: S49-0 and S49-1a and every contract/gate move are placed BEFORE the gate; the pick only unblocks the value half of S49-2…S49-5. |
| PM-8 | **A ring `deep`-shade change silently re-prices the chip border's contrast** (§5.5's two marginal light-mode ratios) and phase-48's C48-1 is disturbed from outside. | C49-7 states the coupling and §7's candidates avoid shade changes; a story that wants one owes §5.5 a re-measurement on the probe §5.5 names. |
| PM-9 | **Two verification lanes mutate one tree** during the RED demonstrations this plan requires, and one lane reads the other's mid-mutation state. | Disjoint files or separate worktrees, per phase-48's own §4 record. Also: `:7331` is a fixed-port singleton — an `EADDRINUSE` during a live pass is concurrency, never code. |
| PM-10 | ⚠ **THE PHASE'S OWN SIGNATURE FAILURE, AND THE ROW EXISTS BECAUSE THE PLAN KEPT COMMITTING IT. A gate is believed because it returned zero, and it returned zero because it never looked at its subject.** Planning produced **eleven instances across three rounds**. ⚠ **They are NOT all in gates, and r2' overclaimed by saying they were** — (4) and (5) are in D49-4's table and census command, neither of which is a gate; the point survives without the overclaim and is weaker with it. Read the list rather than the sentence: **(1)** the `':!.omc/plans'` pathspec that hid the phase-46 pointer — *the exclusion that hides the plans being MOVED also hides the plan doing the POINTING*; **(2)** the `^\./…` exclusions, inert under this machine's `ugrep`, so an archive filter silently filtered nothing; **(3)** the leak grep aimed at `dist/` **on a reason that was itself false** — see (11); **(4)** *the measuring document is part of the measured population* — a pinned count of a path inside a file that gains an occurrence every time it discusses the count (2, then 3, then 4, all correct); **(5)** the same census rooted at `.`, sweeping the gitignored `.omc/artifacts/**` and returning this planning round's own review transcripts as pointers to repair; **(6)** the leak grep aimed at an IDENTIFIER, which esbuild mangles in every build — re-measured at r3': the planted `readLookOverride` became `yM`; **(7)** G49-2 leg (b)'s character class, which had no required extension and so was RED on a clean tree, on ten rows, two of them the plan's own prose; **(8)** ⚠ **the archive gate VACUOUS under this machine's zsh** — an unquoted multi-word scalar arrives as one argument, both legs warn to stderr and print nothing, and zero rows satisfied the verdict on a tree carrying five live pointers; **(9)** ⚠ **the leak gate's precondition certifying a per-page chunk** — `find … -print -quit` returns the FIRST match, which provably cannot hold the override; **(10)** ⚠ **the deepest one: NOTHING TIED THE LEAK GATE'S SUBJECT TO SOURCE.** C49-8 obliged a literal *of a shape*; no leg asserted the string occurred in source at all, so a differently-spelled key would have left the gate GREEN forever having never looked at anything; **(11)** ⚠ **`overlay: false` read as a build exclusion when it is a runtime branch** — the overlay IS in `dist/`, so the bundle the config calls "the deliverable" was excused from the gate on a false premise, and the measurement that excused it was instance (6) wearing a different hat. ⚠ **(12) NEW AT r4' — THE ARCHIVE GATE'S EXCLUSION CARRIED A JUSTIFICATION THAT DID NOT COVER WHAT IT EXCLUDED.** `--exclude-dir=archive` was defended by `docs/README.md`'s frozen-RECORD rule; the archive's INDEX is not a record, it is a live table asserting where two plans are, and it held two live pointers at the moved paths that four rounds of census could not see. **The two-sided control was run: without the exclusion the regex finds them; with it, silence** — a filter returning zero because it never looked. ⚠ **(13) NEW AT r4' — A DEAD MARKDOWN FRAGMENT SURVIVED FOUR ROUNDS IN §1's FIRST PRINCIPLE, UNDER A GREEN CITATION GATE.** The plan cited a heading with the warning sign and the bold markers transposed; `check-citation-anchors.mjs` skips markdown fragments by design and always would have been GREEN on it. **It was found in the first second of G49-2's new leg (c) existing** — which is the whole argument for the leg, and the reason "the second check exists" had been a true sentence about a check that could not see this class. **Note what (4)–(13) share and (1)–(3) do not: they were found by RUNNING, not by reading.** Four rounds of careful reading produced four wrong answers to instance (1) alone. | **Three mechanisms, and the third is the one that ends the recurrence.** *(i)* Every zero in this phase is paired with a **staged non-zero on the same instrument**, plus a silent CONTROL where a filter is doing work. *(ii)* **A gate is not specified until its FINAL command has been run in both states and the output pasted beside it.** *(iii)* ⚠ **AND AT r3' THAT STOPPED BEING ENOUGH, SO THE GATES BECAME FILES.** Instances (7)–(9) all survived a lane that read the command carefully and died on the first execution, and (8) died only when the same text was run under a second shell. **A gate that lives in prose is re-implemented by every reader; a gate that lives in `scripts/` is the same bytes every time.** §6's four script rules are what that costs. **A count is never a GREEN condition where the plan is inside the population — use a path predicate (G49-2's `ALLOW`) so no number appears at all.** |
| PM-12 | ⚠ **A GATE THIS PHASE AUTHORS STOPS BEING RUN THE DAY THE PHASE CLOSES.** The scripts were untracked, in no story's Lands and in no CI job for a whole revision, with their only RED proofs pasted into a plan that gets archived — which is `AGENTS.md`'s *"a gate nobody watches has already stopped being one"*, committed by the revision that escalated to scripts precisely to stop committing it. | Each script lands in a NAMED story (G49-2 → S49-0, G49-3 + G49-5 → S49-1a, G49-4 → S49-1) and goes into `.github/workflows/ci.yml`'s verify job **paired with its own `--selftest`**, in the shape the two audit gates already there use. The selftest is the load-bearing half: it stages its own plant on every run, so "this gate can fail" is re-proved by the machine rather than remembered from a transcript. Costs measured rather than estimated, in CI **and in `pnpm gates`, which parses the same job and is what an executor types** — G49-4's two builds at 4.66–4.80 s, G49-3's seven witnesses at 2.9 s wall, G49-5 at 0.34 s, G49-2's three legs at 0.56 s, and every selftest at well under a second except G49-3's 2.2 s. |
| PM-11 | **The owner's answer cannot be recorded in the artefact the plan asked for**, so it gets recorded as prose and a deferral acquires the authority of a decision. | §7's table is the artefact, it has five columns (D49-3 states the count), and every outcome a story plans for has a row that can hold it — U49-5 split into 5a/5b for "take the mark, defer the reveal", U49-4's candidates written as numbered triples so a relation is one cell. A story whose planned outcome has no row is a defect found in review, not in the owner's reply. |

## 10. Out of scope

Named so that nobody pulls them in by inference:

- **v4 absolute positioning and the marquee decision.** `docs/e3/tracker.md#- **Marquee → stays deferred-v4.**` settles them together at v4 planning; awarding the stage-background drag slot now pre-empts that.
- **The L1 MCP server.** Owner-excluded from this phase's candidate set.
- **The KI-19/49/50 staleness family.** Owner-excluded with no destination; `docs/known-issues.md` records the exclusion rather than a replacement phase, and inventing one reverses an owner condition.
- **KI-47** (the selection ring's COLOUR going stale after a theme toggle). Adjacent to `selection-ring-treatment` and deliberately not merged into it: this phase asks about the ring's FORM. KI-47 is unrouted and needs fresh owner input — `docs/handoff/260831-phase-47-close.md#**Adding it back by lead inference reverses an owner condition; it needs fresh owner input.**`.
- **Phase-48's residuals** other than the tracker record S0 writes — see `docs/handoff/260902-phase-48-close.md` §"3. Residuals, named".
- **Phase-47 routed items (ii) and (iii)** — see §2a.
- **Multi-select drag.** Owner framing on the record as a UX improvement worth having, not a parity obligation; it competes on priority and is not in this bundle.
- **Re-litigating phase-48's C48-1.** The corner-chip admission model is settled and this phase must not disturb it (see C49-7).

## 11. ⚠ UNVERIFIED register

Planning did not run the app (owner note: planning does not verify e2e mechanics). Everything below was checked against an artefact — source text, a test file, a commit, a directory listing — and **not** against a running `descvi:dev`. What WAS run: `node scripts/check-citation-anchors.mjs` (GREEN, 0 violations — **the checked-anchor count lives in D49-4 and nowhere else**, including here; r0 stated it in three places with three different values) and `grep -c -F` uniqueness checks on every anchor cited above.

⚠ **AND AT r3', SIX THINGS THAT ARE NO LONGER IN THIS REGISTER BECAUSE THEY WERE EXECUTED — every one of them by invoking a COMMITTED SCRIPT rather than a pasted command.** *(i)* **G49-2**, GREEN in a post-move scratch copy, planted-RED with two live plants and **two silent controls**, run under `sh` **and** `zsh` with identical output, and its missing-root precondition shown firing. *(ii)* **G49-3**, run for the first time in this plan's history: GREEN, planted-RED on the raised thickness, **GREEN again on the lowered one** (the one-sided bound, executed rather than asserted), and its missing-witness precondition shown firing. *(iii)* **G49-4** in four states — leg 0 RED on the real tree, GREEN with a guarded reader, leg 2 RED with the guard removed, leg 1 RED against a staged bundle carrying page chunks and no overlay entry. *(iv)* **`pnpm descvi:build` was run by this lane**, which the r2' closure audit could not do; `dist-designview/`'s overlay chunk rebuilt byte-identically, so the freshness claim no longer rests on mtimes. *(v)* **`pnpm build` was run**, and it is what falsified the `dist/` claim (C49-8's reversal). *(vi)* **The esbuild mangling measurement** the whole of C49-8 turns on, re-measured. **The outputs are pasted inside the gates, not summarised here**, because a gate's evidence belongs beside the gate.

⚠ **AND AT r4', FIVE MORE — every one of them by invoking a committed file, and three of them are FINDINGS rather than confirmations.** *(vii)* **All four scripts were re-run after r4''s edits**, in GREEN and in planted-RED, each precondition firing. *(viii)* **Each `--selftest` was run AND was shown RED from a deliberately broken copy of its own script** — a selftest that cannot fail is the same defect one level up, and the G49-4 copy with the `__tests__` exclusion removed is simultaneously the measurement behind that exclusion. ⚠ **AT r4' ALL FOUR OF THOSE COPIES BROKE A MECHANISM, AND ALL FOUR SELFTESTS SURVIVED A SCOPE CUT UNTOUCHED — CORRECTED AT r5**, where a fifth family of copies deletes six of G49-3's seven witnesses, two of G49-5's five fields, G49-2's archive-index root, G49-2's heading-slug branch and `dist` from G49-4's bundle set, and **every one of the five reports RED and names what was lost** (§6, rule 6). *(ix)* **G49-2's new leg (c) found a dead markdown fragment in this plan's own §1**, which is repaired here; the resolution rule was measured against all live `.md#` citations first, by disabling one branch at a time in a copy and counting the rows — ⚠ **r4' published that measurement as "17 of 23" and no scoping reproduces it; r5 replaces the figure with the command, in §6's leg-(c) paragraph.** The conclusion is unchanged and is robust under every scoping tried: a heading-only rule could not have been switched on, and substring-only leaves one live citation RED, so both halves ship. *(x)* **The archive INDEX was read and its two live pointers verified**, along with the absence of any `260901-e3-v3/` row. *(xi)* **G49-4's build cost was timed** — 4.80 s and 4.66 s wall for both bundles on two consecutive runs — which is what S49-1's CI wiring is priced with. Everything else in this section remains read, not run.

**What changed in this register at r1' and r2', and by what.** At **r1'** the architect's lane re-checked six of r0's ⚠ entries against source: **U-2 settled, and the answer is better than the fear** — see C49-2's amendment (the constants are read inside the paint pass, so nothing caches them; the real problem is the opposite one, that a module-level mutation triggers no pass at all); **U-11 settled, and the answer is that r0 was wrong** — see G49-4. At **r2'** the unprimed lane and this revision settled three more from source or by execution: **U-13 is upgraded from a footnote to a gate row** (G49-3's per-field table now splits hover width from hover inflation, because the two live in different files and only one of them is an exact pin); **U-9's number is corrected**; and **U-15 is added** for the key-space enumeration behind C49-2's `[` / `]` ruling. At **r3'** two entries changed by execution and one by being read from the other end: **U-11's answer is reversed again** — `dist/` DOES carry the overlay, so it is a subject (C49-8); **U-15's hazard was recorded BACKWARDS and is corrected** — the bracket is not free in source, and the consumer is text entry rather than the browser; and **G49-2/3/4 left the "read, not run" category entirely** by becoming scripts that were invoked. At **r4'** the register changed by execution again: **U-9's count is corrected upward** (the archive index), and **a new class of claim entered the register and left it in the same round** — that a markdown fragment citation resolves, which nothing in this repo checked and G49-2 leg (c) now does. The rest stand as written; being read by a second lane is not the same as being executed, and the entries below say which instrument would settle each.

| # | Claim | How it was checked | What would settle it |
|---|---|---|---|
| U-1 | The furniture is painted imperatively into `#dsh-ring-layer` and React reconciles none of it. | Source: the `ref=` container nodes in `OverlayShell.tsx`, the `appendChild`/`createElement` sites in four modules, and the source's own statement of the contract. | Nothing — this one is a property of the source and is as verified as it can be. Listed because every downstream decision leans on it. |
| U-2 | A dev-only override can switch look constants **live**, without a reload, in `descvi:dev`. | ✅ **PARTLY SETTLED FROM SOURCE at r1', and the answer inverted the fear.** The caching half is disproved: both ring paints and the spacing pass read their constants INSIDE the pass, so nothing caches at module init or at mount. The half that is real is the opposite one: **mutating a module-level record fires no pass at all**, because the effects have explicit dependency arrays and no dependency changed — only `paintReorderOverlay` repaints unaided, per `pointermove`. C49-2 is amended to give the override a `tick` channel. | **S49-P**, now a numbered pre-story with an abort condition rather than a register entry. It must still show that the `tick` bump repaints MID-GESTURE from the keyboard and does not extinguish the subject — those are runtime facts no source read settles. |
| U-3 | Switching values under a live gesture is a better judgement instrument for the owner than a side-by-side gallery. | An argument from the transience of the affordances, plus the record that three live passes each stopped at the same place. **It is a claim about how a person judges and no artefact can settle it.** | U49-A. |
| U-4 | The reorder indicator's thickness bound is one-sided (raising is RED at 3 rows, lowering is green). | Read from the three `toBeLessThanOrEqual(2)` assertions. Not executed. | `pnpm vitest run packages/descvi/test/reorder/reorder-paint-geometry.test.ts` with the constant raised. |
| U-5 | The spacing glyph path strings occur nowhere outside their module, so a mark change moves no gate. | `grep -rIn -e 'M4 4v8' -e 'SPACING_GLYPH_PATHS' e2e packages src \| grep -v use-spacing-affordances` → empty. ⚠ **A zero from a grep is only evidence once the grep has been shown to find something**; this one was shown non-zero against `use-spacing-affordances.ts` before the exclusion was applied. | Executing the suites after the change. |
| U-6 | The selection ring's box is pinned to the element's box with NO tolerance in `e2e/multi-select-shield.spec.ts`, so a 1 px inflation is RED. | Read from the `round(...)` `toEqual` rows. **Not executed** — planning does not run e2e. | `pnpm test:e2e e2e/multi-select-shield.spec.ts` with the ring inflated. |
| U-7 | `SPACING_GLYPH_PX` is pinned by a bare literal 8 in a Playwright title, so changing it forces an `expected-identities.json` regeneration plus a hand `distribution` review. | Read from the F10 row and the identity-oracle reporter. Not executed. | Changing the constant and running `pnpm test:e2e`. |
| U-8 | The arming threshold has two stale-green copies (`PURCHASE_FLOOR_PX` and the `4 px floor` literal) that no gate ties to the symbol. | Read from both files plus the absence of coverage in `scripts/check-handle-constants.mjs`. **Not executed, and the claim is a NEGATIVE** — that no gate fires — which is the shape of claim most likely to be wrong. | Change `POINTER_DRAG_THRESHOLD_PX` and run the full suite; the two files must stay green while others go red. **Do this before believing U49-B.** |
| U-9 | Moving two plans into `.omc/archive/260901-e3-v3/` breaks nothing, because the **11** live pointers across 6 files are the whole live set. ⚠ **It was 9 across 5 until r4' and the census was right AS SCOPED — the scope was wrong.** The archive's own INDEX carried two of them, outside the roots and behind an exclusion whose justification covers archived plans rather than the table that says where plans are. | D49-4's CLAIM 1 and CLAIM 2 commands over the enumerated `ROOTS`, excluding the historical and gitignored namespaces. ⚠ **r1' wrote "7" here against a census that said 9 two sections above — corrected at r2'; the count moved again at r4' when the roots gained `.omc/archive/README.md`.** ⚠ **The root set remains a judgement, and r4' is the proof that the judgement can be wrong**: it undercounted for four revisions because a live index sat one directory outside it. If another live document lives outside `docs .omc/plans .omc/specs .omc/research packages e2e scripts src .omc/archive/README.md`, this undercounts again — **and the way that gets found is by asking what a file DOES, not what namespace it is in.** What is no longer a judgement is the other direction — rooting at `.` OVERcounted, by sweeping the gitignored `.omc/artifacts/**` (PM-10 instance 5). | G49-2's demonstration, which is now RUN: the instrument was shown producing a non-zero on a planted subject inside `.omc/plans/`, the exact namespace every prior enumeration was blind to. |
| U-15 | ⚠ **THIS ROW RECORDED ITS HAZARD IN THE WRONG DIRECTION AT r2', AND A HAZARD NOTED BACKWARDS READS AS A HAZARD HANDLED — CORRECTED AT r3'.** r2' worried that a key *free in source* might be swallowed by the browser. **The key is not free in source.** The grep that ruled `[` and `]` free measured handlers that COMPARE `e.key` to a bracket; the real consumer is **text entry** — `[` opens a Tailwind arbitrary value, the dogfood corpus carries 251 such token occurrences, and both of OverlayShell's document keydown listeners are `{ capture: true }`, so a capture-phase bracket handler takes the character before the field sees it. The surviving claim is narrower: **the overlay's keydown OWNERS are Escape, Enter, Cmd/Ctrl+Z and a bare Meta or Control** (which re-targets the hover preview), and no handler compares a key to a bracket. | Source: every `keydown` listener under `packages/descvi/src/react/overlay/`, plus `grep -rn 'key === "\[\|key === "\]\|BracketLeft\|BracketRight' packages/descvi/src src e2e` → empty. ⚠ **That grep is a NEGATIVE with no positive control** — nothing in the tree binds a bracket, so it cannot be shown able to return non-zero for these keys. Read it as "no handler compares a key to a bracket", which is all it measures, and never as "the key is free". The text-entry consumer was found by reading the CHIP EDITOR rather than by grepping for key comparisons, which is the instrument the r2' reading did not have. | **S49-P legs (2), (4) and the new (5)**: press the switch key mid-drag in a running `descvi:dev` and confirm the drag survives, the value changes, and the hover preview stays on the same node — **then type `w-[200px]` into the className chip editor, with the IME on and off, and confirm the text lands intact and no switch fires.** If the guard is fragile the binding moves to the function key C49-2 names. |
| U-10 | The gap-0 collapse and the 16 px short-item tick are the two facts the indicator decision turns on. | Taken from the backlog row, which records them as already measured by phase-47. **Not re-measured here.** | The live pass at S49-2. |
| U-11 | ~~`pnpm build`'s `dist/` contains no overlay, so it is not a witness and G49-4 need not scan it.~~ | ❌ **DISPROVED BY RUNNING THE BUILD at r3' — and this reverses r1''s own reversal, which stood for two revisions.** r1' read `vite.config.mts#descviDesignView({ repoRoot: __dirname, overlay: false })` and that config's docblock (`vite.config.mts#This is the deliverable: clean pages + router, NO overlay. It shares the SAME`) and concluded there was no overlay in `dist/` to leak into. **The docblock describes what the page RENDERS, not what the bundle CONTAINS.** `overlay: false` is a runtime branch: `packages/descvi/src/vite/bootstrap-entry.ts#import DescviOverlay, { type ManifestMap } from '../react/DescviOverlay';` is an unconditional module-scope import and the flag only selects which tree the generated bootstrap mounts, so Rollup keeps the whole overlay graph. ⚠ **And the measurement that appeared to confirm r1' was instance (6) of `PM-10`: an identifier grep, mangled away in every bundle.** A zero that means "esbuild renamed it" was read as "the code is not here". | **SETTLED BY EXECUTION at r3'.** `pnpm build` was run by a write-capable lane; `grep -RIlF -e dsh-selection-ring -e data-dsh-ring-key -e pad-x dist/` returns `dist/assets/index-*.js` for all three, and with an unguarded reader planted the literal leaks into `dist/` as well as `dist-designview/`. **G49-4 now builds and scans both bundles**, and its GREEN transcript shows an `OVERLAY CHUNK` line for each. |
| U-12 | `import.meta.env.DEV` is **not typed in this package**, so C49-2's guard does not compile until the ambient declaration is widened. | Source: `packages/descvi/src/vite-env.d.ts` declares `ImportMetaEnv` with exactly one member (`VITE_DESCVI_DEV_TOKEN`) and its docblock explains that the narrowing is DELIBERATE — pulling `vite/client` in turns a `@ts-expect-error` in `preview-css-compiler-host.ts` into an unused-directive error, because the root `tsc --noEmit` leg reaches both files in one compilation. | Nothing to settle — it is a fact of the file. **It belongs in S49-1's lands list**, which it now is, rather than in an executor's discovery halfway through a typecheck. The fix is to add `readonly DEV: boolean` to the existing interface, NOT to reference `vite/client`. |
| U-13 | The **HOVER** ring's width assertions are **substring** tests, so a wider value could pass one of them. ⚠ **The SELECTION ring's are not, and r1' said otherwise.** | Source: `packages/descvi/src/react/overlay/__tests__/OverlayShell-canvas-hover.test.tsx#    // to rgb(). Solid, thin (1.5px).` — the two `expect(border).toContain('1.5px')` rows it heads (the anchor is on the comment because the assertion text occurs twice in the file) matches inside `'11.5px'`; the selection side is an exact `toEqual` over a pinned style map (`packages/descvi/src/react/overlay/__tests__/OverlayShell-selection-set.test.tsx#      border: '2.5px solid rgb(234, 88, 12)',`) and needs no caveat at all. **Not this phase's defect and not on this phase's candidate list** — no U49-4 triple produces a value with `1.5` as a substring of a longer number. | It matters because **S49-1a's "every assertion passes unedited" leans on these assertions to prove the refactor moved nothing.** A `toContain` cannot carry that weight alone. S49-1a should read the computed style back exactly for the width fields, or accept that this one leg is weaker than the sentence around it. |
| U-14 | C49-3/G49-6's shared radius field yields **two apparent curvatures**, not one. | Source: the hover ring's radius applies to a box inflated 2 px per side, so the same numeric radius renders at a different visual curvature on the two rings. | Nothing — it is geometry. **It is recorded so that C49-3's single-field contract is not read as a LOOK guarantee it is not making.** C49-3 guarantees the two radii cannot silently diverge; it does not guarantee they look the same, and if the owner wants them to look the same that is a second field (a hover-radius offset), not a bug in this one. |
