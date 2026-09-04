# Forced-choice comparison: plan-A vs plan-B (phase-49)

| Dimension | Winner | Confidence |
|---|---|---|
| 1. Scope fidelity | **B** | medium |
| 2. Decision completeness | **A** | medium |
| 3. Executability | **B** | medium |
| 4. Gate proportionality | **B** | high |
| 5. Handoff readability | **B** | high |
| **Overall** | **B** | medium |

## 1. Scope fidelity — B

**For B.** The kickoff records `spacing-affordance-mark`'s mark count as an owner direction already given, not a question: `base/docs/handoff/260903-phase-49-kickoff.md:34` — "one `-` mark per edge instead of two icons" — and the backlog row it points at carries the same words plus the measured reference (`base/docs/post-loop-backlog.md:178`: "변마다 아이콘 두 개가 아니라 `-` 자국 하나 — Figma의 것은 가로 12–13px, 세로 2px, 1px 외곽선"). B implements exactly that split: cardinality is treated as recorded direction (`plan-B.md:154`, `plan-B.md:515` — "Mark cardinality is NOT part of this question"), while the fields the owner did *not* settle — reveal trigger, outer dimensions, fill, outline — go to the live pass, and B carries the 12–13 px × 2 px / 1 px outline reference into the owner pass as a labelled comparison input (`plan-B.md:146`). A does the opposite: `plan-A.md:1128` puts "(1) two double-headed arrows per edge *(shipped)* / (2) one `-` mark per edge" to the owner as U49-5a, re-asking a decision the kickoff records as taken, and A never mentions the Figma dimensions or the outline anywhere (zero hits for `12–13` and for `outline` in plan-A.md), so the pass it schedules cannot judge the values the row actually names.

Second, B measures a fact the kickoff's inputs assert and both plans could have got wrong. `base/packages/descvi/src/react/overlay/canvas/reorder-paint.ts:141` is `const gap = Math.abs(anchorEdge - neighbourEdge);` feeding line 142's clamp, so the band collapses at *exact contact only* and is positive under overlap. B states the docblock/arithmetic disagreement and refuses to route it (`plan-B.md:81`), then measures the separation sign before the owner is asked (`plan-B.md:375`). A carries the kickoff's framing forward unmeasured — `plan-A.md:444` says the clamp is "on the gap" and treats gap-0 as the whole degenerate story.

**For A.** A discharges the kickoff's explicit instruction at `base/…kickoff.md:47` (say whether phase-47's routed items (ii) and (iii) ride) with its own section and a stated reason per item, `plan-A.md:57`; B discharges it in one clause inside a boundaries paragraph (`plan-B.md:50`). A also handles `padding-glyph` more faithfully than B on the deferral direction: `plan-A.md:500` makes the deferral default *execute the standing G48-8 direction*, noting that treating silence as "keep the arrow" would reverse an owner input — B's S49-5 has no equivalent (`plan-B.md:306-318`).

**Counterweight against B, named.** B lands new contract vocabulary the owner never asked for — the `delegated-mark` kind into five hand-written closed sets and the spec KIND table (`plan-B.md:156`, `plan-B.md:252`) — plus a press-scoped selection-shield handoff (`plan-B.md:251`) that exists only to serve the *optional* rider. Both are labelled as inferences with named revert units (`plan-B.md:304`, `plan-B.md:493`), which is why this does not flip the dimension; had they been silent it would.

## 2. Decision completeness — A

**For A.** A closes the mechanism decisions an executor would otherwise have to invent. The re-render channel is diagnosed from source and ruled: mutating a module-level record fires no paint pass because the effects carry explicit dependency arrays, so the override bumps the existing remeasure `tick` (`plan-A.md:276`). The key is then enumerated against every keydown owner in the overlay and ruled to bare `[`/`]` with a text-entry guard copied from a named line, plus a decided fallback to `F2`/`F3` if the IME kills the channel (`plan-A.md:278`, `plan-A.md:288`). The grepped artefact is pinned to an exact literal, `descvi-look-override`, after measuring that esbuild mangles the identifier (`plan-A.md:302`, `plan-A.md:304`), and the ambient-declaration blocker is decided in advance (`plan-A.md:403`: add `readonly DEV: boolean`, do *not* reach for `vite/client`). Each of those is a decision B leaves to the worker: B says only that controls "change the real ring-layer node without a rebuild" and are "keyboard reachable" (`plan-B.md:244`), and never states that the profile must enter the hooks' dependency arrays — the exact defect A measured.

A also gives every owner row a stated deferral default (`plan-A.md:294` C49-6, and per-story at `plan-A.md:448`, `472`, `490`, `500`), so "the owner defers" has a defined shipped outcome. B has stop branches but no per-row default.

**For B.** B's `plan-B.md:3` admits the plan stands over four *unclosed* review findings, one of which is a hole in the very enumeration this dimension would otherwise credit: "C49-4's grep-derived home list omits the four `use-spacing-affordances.ts` hits including `SPACING_GLYPH_CONTROL_KIND`, the sole production writer of the kind." A parked decision with a named question counts as made; a known-incomplete enumeration shipped as complete does not.

**Against A, cited.** A's largest single hole is in its most expensive story: `plan-A.md:478` calls the reveal "the expensive half … which touches the hit model, not the paint" and then designs nothing for it, handing the executor `plan-A.md:486` — "Grep the e2e for the strip and apron roles before writing the lands list." B designs that whole surface (`plan-B.md:152-195`), disposing of five G44-5 legs, the F10 row and the conditional-arm checker by name and schedule.

## 3. Executability — B

**For B.** Every story uses the same six-field template — Purpose / Affected locations / Required behavior / Dependencies / Done when / Stop-failure — with locations given as file paths and anchors, e.g. `plan-B.md:292` for S49-4 and `plan-B.md:242` for S49-1. Dependencies are ordered explicitly (`plan-B.md:254`: "EG49-2 precedes (a) and (b); EG49-5 precedes (c)"), and the LARGE story is pre-split into three independently revertible commits with what each revert costs (`plan-B.md:250-252`). Done-whens are enumerable checks; `plan-B.md:232` for S49-0 is a list a worker can walk without re-reading the plan.

**Decisive for B, from base.** A's S49-0 and S49-1a cannot be finished from plan-A.md plus the starting tree. A asserts four gate scripts are "COMMITTED SCRIPTS" (`plan-A.md:519`) and makes landing them a Lands item (`plan-A.md:317`, `plan-A.md:370`, `plan-A.md:408`) with done-when conditions that require them to exit 0 (`plan-A.md:332`) — but `base/scripts/` contains no `gate-g49-*` file, and plan-A.md contains no script body, only rules (`plan-A.md:521-527`) and pasted transcripts (`plan-A.md:590-620`). A worker must reconstruct four shell gates with `--selftest` harnesses from prose — which is precisely the failure mode A's own §6 preamble says three review rounds were spent on.

**For A.** A's S49-P (`plan-A.md:336-358`) is the better executability device in either plan: a numbered pre-story with five ordered legs, a stated abort condition, and — critically — three named, executable options for a reopened D49-1 ((b′) reload-per-candidate, (a′) gallery for the reorder indicator alone, (z) park the surface), so the abort has a shape. B's equivalent stop is one sentence with no option set: `plan-B.md:258` — "stop and reopen D49-1."

## 4. Gate proportionality — B

**Sizes.** Plan A's §6 runs `plan-A.md:515-1097` — **583 lines of a 1232-line plan, 47% of the document**. G49-2 alone is `plan-A.md:537-707`, **171 lines**, and the change it guards is the two-file `git mv` and six pointer rewrites listed at `plan-A.md:313-315`. Plan B's §5 gate table plus the Evidence Gates run `plan-B.md:334-399`, **66 lines**; adding C49-4 (`plan-B.md:152-195`, 44 lines), which is where B's spacing gate design actually lives, gives ~110 lines against a change set that includes a four-kind contract move across five hand-written homes.

**For B on bite.** B's RED-whens name a mutation and a consequence per row: `plan-B.md:339` gives G49-1 two oracles and, for O2, "restore that family's pre-phase value … a rewrite that left the old value acceptable proves the oracle stopped asserting anything"; `plan-B.md:343` lists duplicate-mark, missing-mark, changed-operability, +1 px dimension, removed outline, swapped paint; `plan-B.md:395` makes EG49-5 carry a mandatory non-zero instrument control so a zero census is the tree's answer and not the probe's.

**For A.** A's gates guard subjects more precisely than B's on one axis B does not cover at all: A demonstrates that G49-1 (the citation gate) *cannot* see its own subject — `plan-A.md:534`, "for a `.md` target the anchor is treated as a section link and the target's existence is not checked at all" — and builds G49-2's leg (c) for it, which found a live dead fragment in A's own §1 (`plan-A.md:609`). B has one weak cell by comparison: G49-7's RED-when at `plan-B.md:345` — "The new focused RED demonstrations establish that phase gates can fail" — is not a RED-when for G49-7 at all.

**One factual defect in B, from base.** `plan-B.md:221` argues its selftest step from "`check-v3-registers.mjs` … is the one audit gate in `.github/workflows/ci.yml` with no selftest step." `base/.github/workflows/ci.yml` has six `Audit gate —` steps (169, 176, 179, 187, 218, 233) and **four** of them have no selftest: KI register, V3 register, session migration, extract outcome. B's own status line flags this as an unclosed finding; the conclusion survives, the stated uniqueness does not.

## 5. Handoff readability — B

**For B.** 517 lines against A's 1232, and the per-story cost of finding what to do is one section: a worker on S49-3 reads `plan-B.md:274-286` and one row of C49-3 (`plan-B.md:145`). Review history is confined to a single Status paragraph (`plan-B.md:3`).

**For A.** A's revision archaeology is addressed to reviewers, not workers, and it occupies the document's entry point: `plan-A.md:5-13` is the Status block explaining what r3', r4' and r5 each were; `plan-A.md:25-37` is a twelve-item numbered list of "things in this plan that reverse the inputs it was written from," each written as a correction to earlier drafts of itself. A worker starting S49-2 reads none of it and must scroll past all of it. The `dist/` reversal is then restated in at least six places — `plan-A.md:28`, `plan-A.md:146`, `plan-A.md:298`, `plan-A.md:1143`, `plan-A.md:1180`, `plan-A.md:1229` — and A's own rule at `plan-A.md:24` is that "a number that appears in more than one place has, by construction, more than one truth."

**For A.** A's stories carry their traps inline where the worker meets them, which B sometimes defers to a contract section: the e2e no-tolerance trap on the selection ring's bounding box is stated inside S49-3 (`plan-A.md:468`) rather than left for the worker to find, and the `SPACING_GLYPH_PX` identity-golden trap is stated inside S49-4 (`plan-A.md:484`). B's S49-4 (`plan-B.md:288-304`) cannot be executed without reading all 44 lines of C49-4 first.

## Overall — B, medium confidence

B wins four dimensions of five, and the two it wins by the widest margin — proportionality and readability — are the ones that decide whether a plan is usable by someone who did not write it. A's 583-line gate section and its twelve-item reversal preamble are a record of the planning loop rather than an instrument for the phase; four of its gates exist only as prose rules plus transcripts of scripts that are not in the tree and not in the plan.

**What A does better and B should take.** A decides the mechanism, not just the shape. B chooses form (b) and then leaves the executor to discover how a candidate value reaches a painter that React does not re-run: A found from source that the ring and spacing passes have explicit dependency arrays, so a module-level mutation triggers no paint at all (`plan-A.md:276`); enumerated every keydown owner in the overlay, including the bare Meta/Control press that silently *re-targets* the hover preview and would have the owner comparing two values on two different elements (`plan-A.md:278`); pinned the override to an exact string literal after measuring that esbuild mangles the identifier form (`plan-A.md:302`); and pre-decided the `import.meta.env.DEV` ambient declaration a typecheck would otherwise surface mid-story (`plan-A.md:403`). B should also take A's S49-P: a spike with an abort condition whose reopened decision arrives with three named, executable options (`plan-A.md:352`) is strictly better than B's "stop and reopen D49-1."

## Framing

Sentences that tell the reader how to weigh or feel rather than stating a fact or an instruction to act.

**plan-A.md**

- `plan-A.md:23` — "**Three of the four are RED on the tree right now and every one of those REDs is the gate working.** A gate that were GREEN today would be a gate with no subject." (A verdict on how to read the table above it, hoisted over the table.)
- `plan-A.md:24` — "**A number that appears in more than one place has, by construction, more than one truth**" (an aphorism standing in for the argument that the count should have one home.)
- `plan-A.md:508` — "**A conclusion that survives its own reason being wrong is the most expensive kind of correct there is**, and a claim that the duplication is gone while it is still there is worse than the duplication."
- `plan-A.md:1092` — "**A gate nobody schedules is a habit with a number on it**" (an adjective-and-metaphor argument for a demotion the sentence then performs.)
- `plan-A.md:517` — "Every gate below is runnable by someone who is not its author… A gate whose RED-when cannot be staged is scaffolding and does not ship." (A rubric opening that tells a reviewer what to look for in the section.)

**plan-B.md**

- `plan-B.md:11` — "**Compare the mechanism that actually paints.** A facsimile is not evidence about imperative furniture." (The second sentence is a constraint hoisted above the option comparison it belongs to in §0's table.)
- `plan-B.md:12` — "**The shipped default is a gate subject, not a convenient preset.**" ("convenient" is doing the work an argument should.)
- `plan-B.md:36` — "…which is lower risk than preserving a second renderer." (A comparative verdict closing the option ruling, with no stated measure of risk.)
- `plan-B.md:217` — "Naming it is what keeps it from being coverage loss wearing a cleanup label" (a figure of speech telling the reader how to regard the disclosure the paragraph just made.)
- `plan-B.md:349` — "A real `descvi:dev` smoke is mandatory even if all automated checks are green." (Ends the test plan by telling the reader what not to trust rather than by adding a check.)
