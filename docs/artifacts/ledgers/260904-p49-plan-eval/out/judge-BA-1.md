# Forced-choice comparison — plan-A vs plan-B (read order: B then A)

| Dimension | Choice | Confidence |
|---|---|---|
| 1. Scope fidelity | **B** | medium |
| 2. Decision completeness | **B** | medium |
| 3. Executability | **B** | medium |
| 4. Gate proportionality | **B** | high |
| 5. Handoff readability | **B** | high |
| Overall | **B** | medium-high |

## 1. Scope fidelity — B

**For B.**

The kickoff routes each parked item to its backlog row as "the source of truth", each of which "carries its measured facts and the owner's words as received" (kickoff:31, 43). The `spacing-affordance-mark` row records both the direction and its reference geometry: *"변마다 아이콘 두 개가 아니라 `-` 자국 하나 — Figma의 것은 가로 12–13px, 세로 2px, 1px 외곽선"* (`base/docs/post-loop-backlog.md:178`). plan-B carries both halves into the owner pass — the 12–13 px × 2 px × 1 px outline is exposed and labelled on the panel and captured in both themes (plan-B.md:146) — and rules cardinality out of the pass because the kickoff already settles it (plan-B.md:154, 515). plan-A never states those measured dimensions anywhere, and instead re-asks the settled half: `U49-5a` offers *"(1) two double-headed arrows per edge (shipped) / (2) one `-` mark per edge"* as an owner choice (plan-A.md:1128), which puts a recorded owner direction back on the table as an open candidate.

plan-B declines to edit the kickoff: *"`docs/handoff/260903-phase-49-kickoff.md` repeats the same stale destination and is **not** edited: it is a dated record"* (plan-B.md:207). plan-A states the opposite — *"the lead has corrected the kickoff doc"* (plan-A.md:10) — against `base/docs/README.md:57`, which rules `docs/handoff/*` point-in-time records "deliberately **not** rewritten". plan-A cites that same rule twice as binding elsewhere (plan-A.md:177, 563), so this is an internal inconsistency, not a disagreement with the repo.

The kickoff also names the U3 rider as owner-stated: *"the owner wants to try several values"* (kickoff:36). plan-B takes it conditionally as S49-R with a preview-before-split discipline (plan-B.md:48, 320). plan-A recommends NO and records the row struck (plan-A.md:1107, 1131) — legitimate if the ruling it cites is real, but it removes the one item the kickoff attributes directly to the owner's own words.

**For A.** plan-A answers the kickoff's constraint sentence — *"descvi cannot edit its own indicator with descvi. The surface has to sit outside that boundary. The plan states where"* (kickoff:28) — more exactly than plan-B does. D49-0 settles reachability per furniture family from source, showing that exactly one of the four subjects has an exported painter and the other three are module-private (plan-A.md:67–71, 77), which is what disqualifies the gallery structurally rather than on cost. plan-B's §2.1 establishes the same boundary only at layer level (plan-B.md:58–60) and never asks which painters are callable.

## 2. Decision completeness — B

**For B.**

plan-A leaves the central mechanism of S49-4 unmade. It treats one-`-`-per-edge as a figure swap: *"the mark half is nearly free … a change to `SPACING_GLYPH_PATHS` and `figureFor`"* (plan-A.md:478) and concludes *"A mark change keeps the `<svg>`, so the obligation is untouched"* (plan-A.md:482). The source says otherwise: a glyph is appended per operable root at `base/packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts:140`, aprons are iterated separately at line 267, and the module's own docblock states *"the strip and the aprons are one band split by the ceiling"* (line 317). One edge therefore carries several glyphs today, so "one mark per edge" is an ownership change, not a path swap. plan-B makes that decision explicitly, names the ownership unit, and flags the one part of it that is an inference so the owner can reject it in isolation (plan-B.md:154, 156).

plan-B also decides in advance what happens if the story that would inhabit the new vocabulary never runs: S49-1 commit (c) is a single revert unit and S49-4's stop branch reverts it, with "leave it standing" explicitly ruled out as a plan amendment rather than executor discretion (plan-B.md:252, 304, 493). plan-A's equivalent situation — S49-4 possibly having no gate at all to move — is named but not resolved: *"If S49-1 did not land that witness, S49-4 has no gate to relax and no gate to show RED — and that, not the mark change, is what would have to block the story"* (plan-A.md:488).

**For A.** plan-A decides several executor-level things plan-B leaves blank. It rules the re-render channel and the exact keybinding with a named fallback and a copied text-entry guard (plan-A.md:276–288, 397), and it names the ambient type edit that would otherwise be found by a failing typecheck (plan-A.md:403). plan-B's control surface requirement is only *"is keyboard reachable"* (plan-B.md:244) with no key, no guard, and no statement about what happens when reaching for a control ends the gesture being compared.

## 3. Executability — B

**For B.**

Every plan-B story has the same five headings — Affected locations, Required behavior, Dependencies, Done when, Stop/failure behavior — filled at the file level (plan-B.md:199–236 for S49-0, 238–258 for S49-1, and the same shape through S49-R at 320–332). The LARGE story is split into three independently revertible commits with an ordering condition each (plan-B.md:248–252), so a worker can start and finish (a) without owning (b) or (c).

plan-A's S49-1 is one round that bundles the override reader, per-family records, four painter modules, the spatial A/B indexing, a committed gate script, its CI wiring and an ambient type declaration (plan-A.md:395–421), and its done-when requires *"each of the §7 candidate values renders in the live canvas"* (plan-A.md:423) — values the owner has not supplied at that point in the order (plan-A.md:39). A worker cannot close that story in one round without asking.

**For A.** S49-P is the one thing in either plan that a worker could run tomorrow with an unambiguous outcome: five ordered legs, an abort condition, and three named executable fallbacks if it aborts, including the "park the surface" floor (plan-A.md:344–354). plan-B's nearest equivalent, EG49-2, ends in *"If a difference is an intentional prerequisite for expressing a candidate, separate it into the later ruled story"* (plan-B.md:368), which is a judgement, not a branch.

## 4. Gate proportionality — B

**For B.**

plan-A's gate section runs from plan-A.md:515 to plan-A.md:1096 — roughly 580 lines, 47% of the document — for a phase whose deliverable code change is a constants record, one override reader, four painter parameterisations and four value edits. G49-2 alone occupies plan-A.md:531–706, about 175 lines with four pasted transcripts, to guard `git mv` of two files (plan-A.md:313). Its own selftest fixture is bigger than the change: four plants, four controls, three verdicts, run under two shells (plan-A.md:616–657), plus two further broken-copy transcripts (plan-A.md:662–693). By plan-A's own accounting the four scripts add two full Vite builds to every local `pnpm gates` run from S49-1 onward (plan-A.md:421) — a permanent tax on the repo for a phase-scoped instrument.

plan-B's gate table is plan-B.md:336–347 (nine gates, one line each, every one carrying a named RED-when and a failure action) plus Evidence Gates at plan-B.md:351–399 — about 65 lines total, guarding a LARGE story and five promotions. Its one new repo script, `check-owner-pass-record.mjs`, is specified in one paragraph with its failure shapes and its two CI steps (plan-B.md:219–228), and it guards a thing every story writes to.

**For A.** plan-A's gates are the only ones in either plan that have been *shown* to fail rather than asserted able to: G49-3 planted-RED on a raised constant and GREEN on the lowered one, which executes the one-sidedness rather than claiming it (plan-A.md:734–743, 796–801), and G49-5's real-tree run reports four RED fields that are exactly the defect S49-1a exists to fix (plan-A.md:1009–1018). plan-B's gates all name a RED-when and none has been run.

## 5. Handoff readability — B

**For B.**

plan-A's first 39 lines are addressed entirely to reviewers, not workers: revision lineage r0→r5, lane verdicts, a "twelve things that reverse the inputs" list, and a table of which gates are RED on the tree today and why that is correct (plan-A.md:5–38). A worker looking for what to do meets none of it. The same fact is then restated across the document — the `dist/` reversal appears at plan-A.md:28, 298, 846, 1180 and 1229, in five different registers. Forward references are load-bearing: the threshold interval is deliberately stated *only* in U49-B, so S49-6's done-when cannot be read without jumping (plan-A.md:506, 508); the anchor count has "exactly one home" in D49-4 and is refused everywhere else (plan-A.md:24, 1208).

plan-B keeps one story per heading with its file list inline, so S49-4's worker gets every location in one place (plan-B.md:292) without a forward jump.

**For A.** plan-B's own status paragraph is reviewer-facing and self-contradicting: it declares the consensus gate discharged and U49-1 answered, then closes with *"Not executable until the owner approves D49-1"* (plan-B.md:3), which the Open Questions section flatly contradicts (plan-B.md:509). A worker reading only the top of plan-B would conclude the plan is blocked.

## Overall — B, medium-high confidence

plan-B wins on every dimension, but not by the same margin on each: the readability and gate-proportionality gaps are large and structural, while scope fidelity and decision completeness are close and could flip if plan-A's two claimed owner rulings of 2026-09-04 (plan-A.md:10, 1104, 1107, 1116) are genuine and plan-B's `delegated-mark` vocabulary is judged as scope the owner did not authorise.

**What the winner should take from plan-A.** The reachability table. D49-0 (plan-A.md:65–79) establishes per family which painter can be called from outside React, that the ring's look is three inline literals with nothing to parametrise until they are named, and that hover and selection agree on a 6 px radius by two independent literals that nothing would notice diverging. plan-B threads a profile into "the existing painters" (plan-B.md:117) without ever asking whether each painter can receive one, and its §2.2 readiness column records the ring literals as a fact (plan-B.md:82) without making the naming its own story the way S49-1a does (plan-A.md:360–369). plan-A's per-field RED-direction table is the second thing worth taking: it names, per field, the mutation that goes RED *and the one that does not* — the reorder thickness bound is one-sided, so lowering it leaves the suite green, and the hover width is a `toContain` that passes on `'11.5px'` (plan-A.md:825–834). plan-B's RED-when cells name mutations without direction, and "a mutation that swaps selected and hover widths is RED" (plan-B.md:284) is exactly the kind of claim plan-A measured and found half-true. Finally, plan-A's C49-6 deferral discipline — every owner row's shipped value is one of the offered candidates, so "keep what we have" costs one cell and a deferral costs a row rather than the phase (plan-A.md:166, 168, 294) — is a cleaner answer to owner unavailability than plan-B's "a family may not be promoted while its section reads `pending`" (plan-B.md:342).

## Framing

Observation only, not scored.

**plan-A**

| Line | Sentence |
|---|---|
| plan-A.md:23 | "**Three of the four are RED on the tree right now and every one of those REDs is the gate working.** A gate that were GREEN today would be a gate with no subject." — tells the reader how to feel about a red gate before stating what it guards. |
| plan-A.md:25 | "A reviewer should read these first, because each is a place where the input and the tree disagreed and the tree won." — a reading order addressed to a reviewer, hoisted above the plan's own content. |
| plan-A.md:508 | "**A conclusion that survives its own reason being wrong is the most expensive kind of correct there is**, and a claim that the duplication is gone while it is still there is worse than the duplication." — an epigram doing the work of the measurement it replaces. |
| plan-A.md:524 | "**A reconstruction is not a demonstration** — that is the whole lesson of rounds 1 through 3." — a rubric ending, telling a reviewer what to look for in the four gate sections that follow. |
| plan-A.md:1074 | "**The elided rows are the point, not a saving**: they are all `ok`." — instructs the reader how to read an elision rather than showing the rows. |

**plan-B**

| Line | Sentence |
|---|---|
| plan-B.md:11 | "**Compare the mechanism that actually paints.** A facsimile is not evidence about imperative furniture." — a principle hoisted above D49-1, which is the decision it is an argument inside. |
| plan-B.md:12 | "**The shipped default is a gate subject, not a convenient preset.**" — an adjective ("convenient") carrying the case against the option it rejects. |
| plan-B.md:36 | "The price is a small permanent comparison control in the existing toolbar and sequential A/B viewing, which is lower risk than preserving a second renderer." — "small" and "lower risk" are the argument, unmeasured. |
| plan-B.md:154 | "**The generalisation is named as an inference so an owner can reject it without reopening the whole contract**" — tells the reader how to weigh a decision the same paragraph is making. |
| plan-B.md:217 | "Naming it is what keeps it from being coverage loss wearing a cleanup label" — a figure of speech standing in for the disposition of the 168 anchors. |
