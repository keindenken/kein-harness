# Forced-choice comparison — plan-A vs plan-B (read order: B, then A)

## 1. Scope fidelity — **B**, confidence **high**

For B:

- The kickoff's spacing row is a **recorded direction, not an open question**: "one `-` mark per edge instead of two icons" (kickoff:34), and `docs/post-loop-backlog.md:178` carries the measured Figma reference (가로 12–13px, 세로 2px, 1px 외곽선). B treats cardinality as settled and confirms rather than asks (plan-B.md:154, plan-B.md:515: "Mark cardinality is NOT part of this question"), and carries the 12–13 px × 2 px × 1 px outline into the pass as a labelled comparison input (plan-B.md:146). A re-opens it: U49-5a offers "(1) two double-headed arrows per edge *(shipped)* / (2) one `-` mark per edge" as an owner choice (plan-A.md:1128), and the backlog's measured dimensions appear nowhere in plan-A.
- The kickoff is a dated record and says the plan cites the inputs, not this doc (kickoff:3). B refuses to edit it and carries the correction in the executable authority instead (plan-B.md:207). A states the opposite: "the owner reversed that on 2026-09-04 … **and the lead has corrected the kickoff doc**" (plan-A.md:10), i.e. it rewrote the owner's dated scope record and reversed the kickoff's process ruling that "codex is excluded by the owner's standing ruling of 2026-09-02" (kickoff:51), then ran codex lanes on that basis (plan-A.md:9).
- The kickoff holds the ~1 s delay explicitly (kickoff:34); both hold it (plan-B.md:302, plan-A.md:480), so this is a tie, but B additionally records it as a named unanswered question rather than only an omission (plan-B.md:515).

For A: `padding-glyph` arrives already directed — "the pad strip's arrow-up-to-line → a plain directional bar" (kickoff:35). A reads that as confirmation and makes the *deferral default a change* (plan-A.md:500); B re-opens it as an owner ruling to be taken live ("Should padding use the plain directional bar…", plan-B.md:516), which treats a ruled item as pending. On this one row A is the more faithful reading.

## 2. Decision completeness — **B**, confidence **medium**

For B:

- B decides the mechanism the spacing direction actually needs and labels the one thing it inferred: ownership generalised from "per edge" to one mark per `SpacingAffordance`, "named as an inference so an owner can reject it without reopening the whole contract" (plan-B.md:154), with the fourth kind `delegated-mark`, its positive obligation, and its five hand-written homes enumerated (plan-B.md:162–176).
- B pre-decides both branches of its unmeasured facts rather than leaving them to the executor: EG49-5's census decides whether G42-7's delegated arm is coverage or planted-only, and both outcomes are written (plan-B.md:300, plan-B.md:390–399); EG49-3 branches the overlap arm to a synthetic unit row if no shipped route carries one (plan-B.md:377). It also decides the exit if the promotion never happens — revert S49-1 commit (c) as one unit (plan-B.md:304, plan-B.md:493).

Against A, the same subject is a **silent assumption**: "the mark half is nearly free (a change to `SPACING_GLYPH_PATHS` and `figureFor`)" (plan-A.md:478) and "A mark change keeps the `<svg>`, so the obligation is untouched" (plan-A.md:482). In `base/`, `createAffordanceNode` appends a glyph to **every** root (`use-spacing-affordances.ts:140`) and an affordance owns a strip plus aprons — "two aprons for a gap band … one for a padding edge" (`spacing-affordance-geometry.ts:311`). A figure swap therefore yields *two* `-` marks per padding edge, not one; the change A calls free is the ownership change B specifies. No A contract, story or gate names it.

For A: A leaves fewer *execution-time* decisions to the runner in one respect B does not touch at all — the switch channel. A enumerates the overlay's keydown owners, rules the bare `[`/`]` keys, makes the text-entry guard and `event.isComposing` a contract, and pre-decides the function-key fallback (plan-A.md:276–288). B says only "is keyboard reachable" (plan-B.md:244), which is a decision handed to the executor.

## 3. Executability — **B**, confidence **medium**

For B:

- Every story carries the same six fields — Purpose, Affected locations, Required behavior, Dependencies, Done when, Stop/failure behavior (plan-B.md:199–236 for S49-0, repeated at 238–332) — and the affected-location lists are file-level and self-contained (e.g. plan-B.md:292 names each spacing writer and each gate leg the story moves).
- A's S49-4 cannot be finished as written: its done-when says "no gate pins the glyph's `d` today, so the gate this story must show RED is the override witness S49-1 lands … If S49-1 did not land that witness, S49-4 has no gate to relax and no gate to show RED — **and that … is what would have to block the story**" (plan-A.md:488). Worse, its own gate claim is false against `base/`: `e2e/spacing-gesture.spec.ts:720` asserts an svg descendant on every operable spacing root and the F10 row (`e2e/spacing-gesture.spec.ts:835`) pins that presence and its computed `display`, so a one-mark-per-edge change goes RED there. B names both and disposes of them (plan-B.md:184, plan-B.md:189).

For A: A's S49-1a is the best-sized story in either plan — one file, one refactor, an explicit "every existing assertion passes unedited" completion condition with the four witness files named, and a stated weak leg (plan-A.md:360–389). Nothing in B is that cleanly bounded; B's S49-1 is LARGE and bundles the profile, the painter seams, a press-scoped shield handoff and a four-kind vocabulary landing across five hand-written sets into one story with three commit units (plan-B.md:248–252). A's per-row deferral default (C49-6, plan-A.md:294) also lets a value story land when the owner is unavailable, which B has no equivalent of.

## 4. Gate proportionality — **B**, confidence **medium**

For B:

- B's whole gate table — nine gates, each with claim, RED-when, command and failure action — is **14 lines** (plan-B.md:336–347), plus five evidence gates in ~48 lines (plan-B.md:351–399), guarding a LARGE surface story and four promotions. The one new machine gate it authors is sized to its subject: a field validator for a docs record, plus two CI steps (plan-B.md:219–228).
- A's §6 runs from plan-A.md:515 to plan-A.md:1096 — roughly **580 of 1232 lines, 47% of the plan**. G49-2 alone is plan-A.md:537–706 (~170 lines, of which ~120 are pasted transcripts) to guard a two-file `git mv` plus 11 pointer rewrites in six files (plan-A.md:315). G49-5 is plan-A.md:976–1080 (~105 lines) to guard a five-field constants record created by one story in one file (plan-A.md:364). G49-2's leg (c) also guards more than any story changes: it validates markdown fragments across the whole citation corpus (plan-A.md:566), while S49-0 changes six files.

For A: on the first conjunct — "can each fail for a named reason" — A is clearly stronger. All four gates are committed scripts with exit-status verdicts, missing-root preconditions, demonstrated planted REDs, and `--selftest`s that are themselves shown RED from scope-reduced copies (plan-A.md:519–527, plan-A.md:770–789, plan-A.md:926–942). B's G49-1/G49-2/G49-3/G49-5 remain prose obligations with no runner once the phase closes — exactly the "gate nobody watches" hazard the kickoff raises (kickoff:8) and which B only answers for its one validator.

## 5. Handoff readability — **B**, confidence **high**

For B: 517 lines against A's 1232, with a worker path that is one story section long — S49-0's Affected locations, Required behavior and Done when are contiguous at plan-B.md:203–232, and the one forward reference (§2.5's census) is a single named section.

Against A: a worker starting S49-0 must read the Lands list (plan-A.md:310–330), then D49-4 for the census and its two reversals (plan-A.md:174–226), then G49-2's 170 lines for the command and its allow-list predicate. Much of the surrounding text is addressed to reviewers, not workers — "A reviewer should read these first" (plan-A.md:25), "Read the two RED lines against each other" (plan-A.md:695), "READ THE FOUR `ok` LINES AT THE BOTTOM OF THAT RUN" (plan-A.md:791) — and the revision archaeology (r0/r1'/r2'/r3'/r4'/r5) repeats the same findings in the status block, in the contracts, in the gates, in §9's PM-10 row and again in §11 (plan-A.md:5–37, 1189, 1210–1214).

For A: A's repetition is not free of value to a worker in one place — the RED-direction table (plan-A.md:825–834) tells an executor exactly which mutation to try per field, which B never spells out per field.

## Overall — **B**, confidence **high**

B answers the kickoff's rulings with less re-opening, decides the one thing the spacing direction actually requires, sizes its gates to the changes they guard, and is readable at one story per sitting. A's central weakness is not length but that its largest investment (four gate scripts, ~580 lines) sits on the two cheapest subjects in the bundle — a docs move and a constants refactor — while the one subject that needed architecture, the spacing mark, is asserted free on a reading `base/` contradicts.

**What A does better and B should take.** A's gates are files, not paragraphs: committed scripts with exit-status verdicts, missing-subject preconditions, and `--selftest` steps wired into the CI verify job so their RED is re-proved on every push rather than remembered from a transcript (plan-A.md:519–527, plan-A.md:1190). B has exactly one gate in that shape (`check-owner-pass-record.mjs`, plan-B.md:219–228) and leaves G49-1, G49-2, G49-3 and G49-5 as prose that any executor will re-implement. B should also take A's two owner-facing mechanisms: the five-column mid-phase table with the shipped value present as a candidate and a per-row `Defer?` cell (plan-A.md:1122–1131, plan-A.md:166), and C49-6's rule that a deferred row still ships its contract and gate move (plan-A.md:294) — B's promotion sequence stalls entirely if a ruling does not arrive. Finally, B's "keyboard reachable" (plan-B.md:244) should absorb A's keybinding analysis: the key space is occupied, `[` opens a Tailwind arbitrary value, and both OverlayShell keydown listeners are capture-phase (plan-A.md:282).

## Framing

Sentences that tell the reader how to weigh or feel rather than stating a fact or an instruction to act.

**plan-A**

- plan-A.md:25 — "A reviewer should read these first, because each is a place where the input and the tree disagreed and the tree won."
- plan-A.md:23 — "Three of the four are RED on the tree right now and every one of those REDs is the gate working. A gate that were GREEN today would be a gate with no subject."
- plan-A.md:508 — "A conclusion that survives its own reason being wrong is the most expensive kind of correct there is."
- plan-A.md:1074 — "The elided rows are the point, not a saving: the crippled copy's mechanism is perfect and its reach is three fields."
- plan-A.md:791 — "READ THE FOUR `ok` LINES AT THE BOTTOM OF THAT RUN."

**plan-B**

- plan-B.md:11 — "Compare the mechanism that actually paints. A facsimile is not evidence about imperative furniture."
- plan-B.md:12 — "The shipped default is a gate subject, not a convenient preset."
- plan-B.md:36 — "The price is a small permanent comparison control in the existing toolbar and sequential A/B viewing, which is lower risk than preserving a second renderer."
- plan-B.md:3 — "What remains before code is written is not a decision but an observation schedule."
- plan-B.md:217 — "Naming it is what keeps it from being coverage loss wearing a cleanup label."
