# Forced-choice comparison — plan-A vs plan-B, phase-49

| Dimension | Choice | Confidence |
|---|---|---|
| Scope fidelity | **B** | medium |
| Decision completeness | **B** | medium |
| Executability | **B** | medium |
| Gate proportionality | **B** | high |
| Handoff readability | **B** | high |
| **Overall** | **B** | medium |

## 1. Scope fidelity

**Choice: B. Confidence: medium.**

For B:

- The kickoff routes `reorder-indicator-look` by its backlog row, whose shape is **자리·길이·굵기·파랑** — place, length, weight, blue (`base/docs/post-loop-backlog.md:176`, kickoff line 32). B's S49-2 asks the owner for exactly that set plus U9(E): "Place, extent, weight, blue, and keep/change of the visual-count claim" (`plan-B.md:144`, and the slice table at `plan-B.md:44`). A's mid-phase table reduces the item to two rows — U49-1 *weight* and U49-2 *length rule* (`plan-A.md:1124-1125`) — and S49-2's "Owner input" names only those two (`plan-A.md:448`). Place and blue leave the plan without being ruled out anywhere.
- The kickoff records the spacing mark's cardinality as a **direction already given**, not a question: "one `-` mark per edge instead of two icons" (kickoff line 34; the backlog row spells the same as received, `base/docs/post-loop-backlog.md:178`, including the Figma 12–13 px × 2 px × 1 px outline reference). B implements it as a recorded direction and says so — "Mark CARDINALITY here is a recorded owner direction, not a plan invention and not a live-pass field" (`plan-B.md:154`), with cardinality excluded from U49-4 (`plan-B.md:515`) and carried to the panel with the Figma reference numbers (`plan-B.md:146`). A re-opens it as a choice, U49-5a, whose candidate (1) is "two double-headed arrows per edge *(shipped)*" (`plan-A.md:1128`), and whose deferral default is "shipped mark" (`plan-A.md:490`). That default silently reverses the owner's stated direction — the exact defect A itself identifies and avoids for `padding-glyph` (`plan-A.md:500`).

For A:

- The larger scope expansion is B's. C49-4 adds a fourth declared KIND to the layer contract, moving five hand-written closed sets, two production restatements, the spec KIND table, and four gate universes (`plan-B.md:156`, `plan-B.md:162-176`). Nothing in the kickoff authorises a KIND-vocabulary change; it follows from B's reading of the mark direction rather than from a ruling. B labels the ownership generalisation as its own inference (`plan-B.md:154`) and gives it a revert exit (`plan-B.md:304`), but A's path keeps the mark change inside `SPACING_GLYPH_PATHS` and `figureFor` (`plan-A.md:476-478`) and therefore reaches the kickoff's bundle without enlarging a closed contract. A's out-of-scope section is also the more complete of the two, naming multi-select drag and the C48-1 re-litigation that B's one-line list omits (`plan-A.md:1193-1204` vs `plan-B.md:50`).
- Process note against both: the kickoff requires "unanimous approval of the CURRENT text" (kickoff line 51). B's own status records two REVISE verdicts and four open findings (`plan-B.md:3`); A's records that r5 "no review lane has read it" (`plan-A.md:9`). Neither satisfies the clause; A's current text is the one no lane has read.

## 2. Decision completeness

**Choice: B. Confidence: medium.**

For B:

- Every decision B parks is parked with a named question and a named consequence: U49-2…U49-6 each say what the answer changes (`plan-B.md:513-517`), and the one decision B makes beyond the owner's words is flagged for rejection in place — "The generalisation is named as an inference so an owner can reject it without reopening the whole contract" (`plan-B.md:154`).
- B closes the decision A leaves open. The hardest unmade question in this bundle is what happens to the per-root glyph obligations when the mark stops being per-root; B enumerates G44-5 universe B's five legs and disposes of each — two survive, the family-kind pin moves, the size-term leg and the inhabitation pair retire with named replacements and their own RED mutations (`plan-B.md:178-191`) — and names two further homes (`plan-B.md:186-189`) that no leg-by-leg reading reaches.

For A:

- A's decision surface is broader where it is present: D49-0's painter table is established from source with each anchor uniqueness-checked (`plan-A.md:63-73`), and it produces the structural reason for choosing (b) that B reaches only rhetorically — three of four painters are module-private, so a gallery costs three exported writers (`plan-A.md:116`). A also decides the reopen option set in advance rather than leaving "return to the owner" as an intent (`plan-A.md:352`).

Against A on this dimension: the spacing reveal half — the expensive half by A's own account — is handed to the executor undecided: "A *reveal* change moves when nodes exist at all and therefore does touch that spec's subject set. Grep the e2e for the strip and apron roles before writing the lands list" (`plan-A.md:486`). That is an architecture decision deferred to implementation time with no label.

Against B: B ships with four review findings unresolved by its own status line, one of them substantive — C49-4's enumerated home list omits `SPACING_GLYPH_CONTROL_KIND` (`plan-B.md:3`), which is the sole production writer of the kind at `base/packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts:103,118`. The damage is contained because B instructs the executor to re-derive the list by grep rather than read the list (`plan-B.md:170`), and that command does return the missed line.

## 3. Executability

**Choice: B. Confidence: medium.**

For B:

- Each story carries the same six fields — Purpose, Affected locations, Required behavior, Dependencies, Done when, Stop/failure behavior (`plan-B.md:199-236` for S49-0). A worker can start S49-3 from `plan-B.md:274-286` alone: five files, four acceptance claims, two named RED mutations, one stop rule.
- The one LARGE story is split into three independently revertible commits with the revert consequence of each stated — (a) profile and seams, (b) the press-scoped shield handoff, (c) the uninhabited vocabulary landing, with EG49-5 required before (c) and only before (c) (`plan-B.md:248-254`). The risk table then reuses those units as the rollback (`plan-B.md:491,493`).

For A:

- A's S49-1 is the opposite shape: one story lands the override reader, the per-family records, wiring in four painter modules, the keyboard bump, the ring's spatial A/B, the `vite-env.d.ts` widening, a new gate script with two Vite builds, and a widening of another gate's witness list (`plan-A.md:395-425`). Its "Done when" (`plan-A.md:423`) is testable but is not one round's work, and it has no internal commit boundaries.
- A's story text also depends on §6 to be implementable: S49-1a's Lands are only correct if the four field spellings match G49-5's greps, which A states as a trap in the story itself — an executor who nests the fields "satisfies the contract, moves no pixel, passes every witness, and leaves the gate permanently at `homes=0`" (`plan-A.md:366`) — and the adjacent rule forbids writing the retired literal in a comment (`plan-A.md:367`). A gate that constrains the shape of a legal refactor is a question the worker has to resolve by reading a 583-line gate section.

For A, and it is real: A's per-story lands are anchored to exact source lines that were uniqueness-checked, and S49-P is a bounded pre-story with an abort condition and three named executable fallbacks (`plan-A.md:340-352`), which is the one thing B has no equivalent of — B's D49-1 stop is "stop and reopen D49-1" with no option set (`plan-B.md:258`).

## 4. Gate proportionality

**Choice: B. Confidence: high.**

For B:

- Size. B's whole gate apparatus is `plan-B.md:334-350` (nine gates as one table, 17 lines) plus the five evidence gates at `plan-B.md:351-399`. A's §6 runs `plan-A.md:515-1097` — **583 lines, 47% of the plan**, 74.7 KB. G49-2 alone occupies `plan-A.md:537-707` (171 lines) and what it guards is a two-file `git mv` plus 11 pointer rewrites across 6 files (`plan-A.md:313-315`). G49-5 occupies `plan-A.md:976-1081` (106 lines) to guard a five-field constants record.
- Each B gate names a mutation and a failure action in its own row, and the ones that matter are tied to the story that changes their subject: G49-1's O1/O2 split names the RED for each oracle and the exact reason a rewritten oracle stops asserting anything (`plan-B.md:339`); G49-5's mutation list is twelve named mutations against the mark contract (`plan-B.md:343`); EG49-5 carries a mandatory positive control so a zero census is the tree's answer and not the probe's (`plan-B.md:395`).

For A:

- A's gates are the stronger instruments where they exist. They are committed scripts, not prose, each with an exit-status verdict, a missing-root precondition, and a `--selftest` wired into `.github/workflows/ci.yml` (`plan-A.md:519-527`), and each was demonstrated GREEN and planted-RED from the committed file (`plan-A.md:587-604`). B has one gate whose RED-when is not a mutation of itself — G49-7 "repository gates", whose RED-when reads "The new focused RED demonstrations establish that phase gates can fail" (`plan-B.md:345`), which is a statement about other gates.

The dimension asks whether the gates are larger than the thing they guard. A's are, by a wide margin, and A concedes the coupling cost in the stories that must obey them (`plan-A.md:366`, `plan-A.md:421`).

## 5. Handoff readability

**Choice: B. Confidence: high.**

For B:

- The story ladder is uniform and self-contained, and the fields a worker needs are in fixed positions (`plan-B.md:199-332`). Where a story depends on something upstream it says which unit and when: "EG49-2 precedes (a) and (b); EG49-5 precedes (c)" (`plan-B.md:254`).
- Text addressed to reviewers is quarantined into the status paragraph (`plan-B.md:3`) and the pre-mortem (`plan-B.md:401-443`), not interleaved with instructions.

For A:

- Revision-history apparatus dominates the reading path. The status block alone runs `plan-A.md:5-39` and is written to reviewers of earlier drafts: r0/r1'/r2'/r3'/r4'/r5 lane verdicts (`plan-A.md:9`), a twelve-item list of "things in this plan [that] reverse the inputs it was written from" (`plan-A.md:25-37`), and PM-10's thirteen numbered planning-defect instances in a single risk cell (`plan-A.md:1189`). None of it is work for a worker.
- Finding one story's work costs several hops: to run S49-3 a worker reads the story (`plan-A.md:450-472`), C49-5's regime rule for which commits are gated (`plan-A.md:293`), C49-3 and C49-7's couplings (`plan-A.md:289,295`), G49-3's per-field table and G49-6 (`plan-A.md:708+`, `plan-A.md:1082`), G49-7 as a per-story obligation (`plan-A.md:1090`), and the U49-3/U49-4 rows (`plan-A.md:1126-1127`).

For A: A's repetition is at least mostly deliberate and self-policed — the one-home rule for the anchor count and the arming interval keeps two figures from appearing twice (`plan-A.md:24`, `plan-A.md:508`), and B has nothing comparable; B's S49-4 "Affected locations" is a single ~350-word paragraph of forward references (`plan-B.md:292`) that is harder to read than anything of comparable length in A's stories.

## Overall

**Choice: B. Confidence: medium.**

B answers the kickoff's enumerated items more exactly, keeps its decisions and its parkings labelled, and hands a worker a story ladder that can be executed a story at a time. A's failure is one of proportion rather than of care: 47% of its text is a gate section that outweighs what it guards, and its narrative of its own revision history is addressed to reviewers who are gone. The two places B is materially weaker — a KIND-vocabulary expansion the kickoff did not authorise, and four review findings left standing in an approved text — are both labelled, revertible, and cheaper to correct than A's structural asymmetry.

**What A does better and B should take.** A's gates are objects rather than descriptions. Every gate in A is a committed script with an exit-status verdict, a precondition that fails on a missing subject, and a `--selftest` wired into the CI verify job so that "this gate can fail" is re-proved by a machine on every push rather than remembered from a transcript (`plan-A.md:519-527`, `plan-A.md:317-328`). B's G49-4 is the only gate it ships in that form (`plan-B.md:219-228`); everything else in B's table is a claim plus a mutation someone is trusted to perform once. B should convert at least G49-0's closure scan and G49-5's mark-ownership legs into committed scripts with selftests, and adopt A's rule that a gate's RED must be demonstrated from the committed file rather than from a reconstruction — the discipline A arrived at only after three rounds of the same class of defect (`plan-A.md:6`). B should also take A's S49-P: a bounded pre-story that tests the live-switch channel against a stated abort condition with three named executable fallbacks (`plan-A.md:340-352`), which is exactly what B's bare "stop and reopen D49-1" (`plan-B.md:258`) lacks.

## Framing

Observation only; not scored.

### plan-A

| Line | Sentence |
|---|---|
| 23 | "**Three of the four are RED on the tree right now and every one of those REDs is the gate working.** A gate that were GREEN today would be a gate with no subject." — tells the reader how to read four RED gates before they have seen them. |
| 25 | "A reviewer should read these first, because each is a place where the input and the tree disagreed and the tree won." — an instruction about reading order and about whom to believe, hoisted above the twelve items it introduces. |
| 224 | "⚠ **THIS PLAN'S OWN ROW HAS NO NUMBER IN IT, AND THE OMISSION IS THE POINT** — instance 4 of `PM-10`, in its purest form." — an absence re-presented as a virtue. |
| 508 | "**A conclusion that survives its own reason being wrong is the most expensive kind of correct there is**, and a claim that the duplication is gone while it is still there is worse than the duplication." — an aphorism placed where the operative fact (the interval has one home) is the whole instruction. |
| 1092 | "**A gate nobody schedules is a habit with a number on it**" — an adjective-and-metaphor argument standing in for the demotion's actual justification, which follows two lines later. |

### plan-B

| Line | Sentence |
|---|---|
| 3 | "…neither named a blocking ground, so the consensus gate is discharged and this plan stands over four recorded findings rather than over nothing" — tells the reader how to weigh two REVISE verdicts before naming what they were. |
| 11 | "A facsimile is not evidence about imperative furniture." — a principle written as a verdict; the fact it rests on is in §2.1. |
| 36 | "…which is lower risk than preserving a second renderer." — a comparative risk claim with no measurement behind it, closing the options ruling. |
| 154 | "**The generalisation is named as an inference so an owner can reject it without reopening the whole contract**" — tells the reader how to receive the inference rather than stating what the inference is. |
| 217 | "Naming it is what keeps it from being coverage loss wearing a cleanup label" — an image doing the work of the argument that the 168 anchors are deliberately unchecked. |
