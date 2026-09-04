# Forced-choice comparison — plan-A vs plan-B (read order: B, then A)

## 1. Scope fidelity

**Choice: B. Confidence: medium.**

For B:

- The kickoff records the spacing direction as already given by the owner: `docs/post-loop-backlog.md:178` (quoted in kickoff:34) says *"변마다 아이콘 두 개가 아니라 `-` 자국 하나"* — one mark per edge instead of two icons per edge. B treats that as settled and says so: `plan-B.md:154` ("Mark CARDINALITY here is a recorded owner direction, not a plan invention and not a live-pass field"), and `plan-B.md:515` explicitly removes cardinality from the owner question. A puts the shipped form back on the ballot as candidate (1) at `plan-A.md:1128` — *"(1) two double-headed arrows per edge (shipped) / (2) one `-` mark per edge"* — which asks the owner to re-decide a direction the kickoff carries as received.
- The kickoff's process ruling at kickoff:51 is unambiguous: **"codex is excluded by the owner's standing ruling of 2026-09-02 — consensus is the Claude lanes' alone."** `plan-A.md:9` records codex as a review lane in four of five rounds, and `plan-A.md:10` states the lead *"has corrected the kickoff doc"* to reverse the exclusion. Editing the owner's own ruling document is the sharpest form of deciding something the owner reserved; the kickoff's own opening (kickoff:3) says the plan cites the inputs, not this doc. B keeps consensus to an architect and a critic (`plan-B.md:3`).
- The kickoff calls the U3 threshold an *"Optional rider, same surface, owner-stated"* with *"the owner wants to try several values"* (kickoff:36). B keeps it as a conditional rider that previews values and only splits on a recorded ruling (`plan-B.md:48`, `plan-B.md:320`). A records it as **"RULED NO BY THE OWNER"** and strikes the row entirely (`plan-A.md:1107`, `plan-A.md:1131`), removing the trial the owner asked for.

For A (the reason that cuts the other way, and it is not small):

- `base/docs/README.md:57` states that `docs/handoff/*` and archived plans under `.omc/archive/` *"are point-in-time records and are deliberately **not** rewritten."* B's S49-0 done-when at `plan-B.md:232` requires *"zero references across the tracked tree AND the non-ignored working tree, including `.omc/plans` and `.omc/archive`"*, and `plan-B.md:42` says *"every tracked reference updated."* Measured on `base/`, the great majority of the two targets' referring files sit in `.omc/archive/260818-phase-42-consensus/` (28 files), `.omc/archive/260901-e3-v3/` (3) and `.omc/archive/260819-phase-43-consensus/` (2) — so B's completion condition cannot be met without rewriting exactly the records the repo forbids rewriting. A names the convention and scopes the rewrite to live documents (`plan-A.md:177`, `plan-A.md:563`), and its six-file live census (`plan-A.md:213-222`) reproduces on `base/` file-for-file.

## 2. Decision completeness

**Choice: A. Confidence: medium.**

For A:

- A carries a labelled register of what it did *not* settle: `plan-A.md:1216-1232` gives fifteen `U-n` rows, each with "how it was checked" and "what would settle it", including negatives flagged as negatives (`plan-A.md:1225`: *"the claim is a NEGATIVE — that no gate fires — which is the shape of claim most likely to be wrong"*). Nothing in B plays this role for source-read claims; B's Open Questions (`plan-B.md:505-517`) cover owner values only.
- A decides a class of mechanism questions B never reaches. B's C49-1 (`plan-B.md:117-119`) says `OverlayShell` owns `comparisonActive`, a panel owns the controls, and the painters accept profile slices — but never says how a profile change reaches painters that are effect-driven with explicit dependency arrays. A measured that this is the blocking fact (`plan-A.md:276`: *"mutating a module-level record triggers no pass AT ALL, because no dependency changed"*) and rules the re-render channel, the `[`/`]` binding, its capture-phase text-entry guard, the IME failure mode, and the fallback key (`plan-A.md:278-288`), plus the `ImportMetaEnv` widening a typecheck will otherwise fail on (`plan-A.md:403`). B's S49-1 worker must invent all of it. B also never confronts that reaching for a panel control extinguishes the hover ring and ends the drag — the very transience problem three of its four subjects have; `plan-B.md:28` records only *"compares one live preset at a time"* as the cost.
- A's deferral semantics are decided rather than assumed: `plan-A.md:168` (a deferred row ships its gate move at the shipped value and is recorded as `DEFERRED — SHIPPED VALUE STANDS`), and `plan-A.md:500` rules that `padding-glyph`'s deferral default is *change*, not status quo, because a direction already exists.

For B:

- B makes one material decision A asserts away. `plan-A.md:482` states *"A mark change keeps the `<svg>`, so the obligation is untouched."* On `base/`, `use-spacing-affordances.ts:140` appends a glyph to **every** strip and apron root, and `e2e/spacing-gesture.spec.ts:714-720` pins each operable spacing root to `glyph-conditional`, to a published size term, and to an `svg` descendant. Under the owner's recorded one-mark-per-edge direction those obligations move. B spends C49-4 (`plan-B.md:152-195`) disposing of exactly that: five hand-written closed kind sets, G44-5's five legs with two retirements and named replacements, the F10 row that *breaks* rather than empties (`plan-B.md:189`), and the ordering condition that the vocabulary must land uninhabited before the candidate can legally be shown (`plan-B.md:121`). A leaves that decision unmade and unlabelled.

## 3. Executability

**Choice: B. Confidence: medium.**

For B:

- Every story uses the same six-slot template — Purpose / Affected locations / Required behavior / Dependencies / Done when / Stop-failure — at `plan-B.md:199-332`, so a worker reads one contiguous block. S49-1's three revert units (`plan-B.md:248-252`) give commit boundaries and a per-unit revert consequence, and its done-when (`plan-B.md:256`) is a list of checkable facts ending in *"no `src/app/**` or `.descvi/screens.json` content changes."*
- A's stories require forward reads to be executable at all. `plan-A.md:366` makes four exact key spellings contract, then says the gate that enforces them lives in §6 — the table is at `plan-A.md:999`, 633 lines later. `plan-A.md:506` says S49-6's admissible value *"is derived once in U49-B and stated nowhere else"*, at `plan-A.md:1107`. `plan-A.md:389` weakens its own done-when after stating it: *"ONE LEG OF THAT SENTENCE IS WEAKER THAN THE SENTENCE."*
- Story size: B's largest is S49-1, declared LARGE and split into three landings. A's S49-1 (`plan-A.md:393-427`) lands the override reader, four painter records, painter wiring, the keyboard channel with two guards, the spatial A/B indexing through the pool key, an ambient type declaration, a new gate script with a selftest, CI wiring, and G49-3's witness widening — as one story with no internal boundaries.

For A:

- B's S49-0 is labelled **SMALL** (`plan-B.md:42`) while landing a tracker section, two `git mv`s, a rewrite B itself sizes at *"90 occurrences across 47 tracked files"* (`plan-B.md:103`), an archive README row, a new record file, a new validator script with a three-shape selftest, and two CI steps — and, per §1's finding, its done-when as written cannot be reached. A's S49-0 (`plan-A.md:308-334`) is a six-file rewrite with a done-when a worker can actually satisfy.

## 4. Gate proportionality

**Choice: B. Confidence: high.**

Sizes, measured:

| | gate text | share of plan | what the largest gate guards |
|---|---|---|---|
| A | §6, `plan-A.md:515-1096` = **582 lines** | 47% of 1232 | G49-2, `plan-A.md:537-706` = **170 lines**, guarding a two-file `git mv` plus 11 pointer rewrites |
| B | §5 + Evidence Gates, `plan-B.md:334-399` = **66 lines** | 13% of 517 | G49-0, one table row, guarding the same move |

For B:

- Each of B's nine gates carries a claim, a named RED-when, a command, and a failure action in one row (`plan-B.md:338-347`), and the RED-whens name mutations rather than gesture at them — G49-1's O2 arm at `plan-B.md:339` (*"restore that family's pre-phase value in `SHIPPED_OVERLAY_PROFILE`; the promoted family's row must fail"*) is a real oracle-rot detector in one sentence.
- Where B does author machinery it is sized to its subject: `scripts/check-owner-pass-record.mjs` plus a selftest step and a run step, specified in about fourteen lines (`plan-B.md:219-232`), guarding five ruling records.
- A's G49-5 (`plan-A.md:976-1080` = 105 lines) guards a four-field constants record. A's G49-4 (`plan-A.md:837-974` = 138 lines) guards one override reader. `plan-A.md:419` prices the leak gate at two full Vite builds added to `pnpm gates` on every local commit from S49-1 onward — a gate larger, and per-commit slower, than the single module it watches.

For A:

- A's gates are the only ones in either plan proven able to fail. `plan-A.md:590-604` shows G49-2 RED from the committed file on the real tree; `plan-A.md:773-789` shows a scope-cut copy of G49-3 going RED; and leg (c) found a genuine four-round-old dead citation in the plan's own §1 on its first run (`plan-A.md:609`). Nothing in B's gate table has been executed — `plan-B.md:338-347`'s RED-whens are all obligations placed on the future executor, and G49-7 (`plan-B.md:345`) has no mutation of its own at all, only *"the new focused RED demonstrations establish that phase gates can fail."*

## 5. Handoff readability

**Choice: B. Confidence: high.**

For B:

- A worker's path to one story is short: the ladder at `plan-B.md:199-332` is 134 lines for seven stories, and each names its own contracts by id rather than restating them.
- A's cost to find what to do for one story is dominated by text addressed to reviewers. `plan-A.md:25-37` is a twelve-item register of *"things in this plan [that] reverse the inputs it was written from"*, written for a reader auditing the planning rounds; `plan-A.md:5-14` narrates r0 through r5 lane verdicts before a single decision appears. Each gate opens with a history of its own broken predecessors (`plan-A.md:539-547`, `plan-A.md:840-846`, `plan-A.md:978`).
- Repetition: the `dist/` reversal is stated in full at `plan-A.md:28`, `plan-A.md:298`, `plan-A.md:846`, `plan-A.md:862`, `plan-A.md:1143`, `plan-A.md:1180` and `plan-A.md:1229` — seven homes for one measurement, in a plan whose own rule at `plan-A.md:24` is that *"a number that appears in more than one place has, by construction, more than one truth."*

For A:

- B is not free of the same habit: the `delegated-mark` ordering argument is restated at `plan-B.md:121`, `129`, `246`, `252`, `304`, `473` and `493`, and `plan-B.md:3`'s status paragraph is a 300-word reviewer-facing note carrying four unresolved findings that a worker must read past. A's §7 owner table (`plan-A.md:1122-1131`) is, by contrast, a single self-contained artefact a worker can hand over without explanation — B's equivalent is spread across C49-3's table (`plan-B.md:144-148`) and U49-2…U49-6 (`plan-B.md:513-517`).

## Overall

**Choice: B. Confidence: medium.**

B is the plan a worker can execute. It is 517 lines to A's 1232, its gate apparatus is a seventh the size for the same subjects, its stories are uniform and bounded, and its one deep contract investment — C49-4's disposition of the spacing kind vocabulary — is the phase's real architectural risk, verified correct against `base/use-spacing-affordances.ts:140` and `base/e2e/spacing-gesture.spec.ts:714-720`, and missed entirely by A. A's judgment is better in places, but its deliverable is substantially a record of its own review history, and the two places it departs from the kickoff (codex, and editing the kickoff doc) are departures on process rulings the owner reserved.

**What A does better, and B should take.** Three things. First, the frozen-record scoping: `base/docs/README.md:57` forbids rewriting archived plans and handoffs, and B's S49-0 done-when (`plan-B.md:232`) orders exactly that — B should adopt A's live-pointer predicate (`plan-A.md:177`, `plan-A.md:553`), which tests *which file a row came from* rather than counting rows, and which reproduces on `base/` at six live files. Second, the runtime mechanism: A measured that the ring and spacing painters are effect-driven with dependency arrays, so a profile change alone repaints nothing (`plan-A.md:276`), and ruled a keyboard channel with a capture-phase text-entry guard and an IME fallback (`plan-A.md:278-288`) plus the `ImportMetaEnv` widening (`plan-A.md:403`); B's S49-1 has none of this and its worker will hit all three in the first hour. Third, the falsifiability discipline: A's gates were run, and running them found two real defects nobody had found by reading (`plan-A.md:608`, `plan-A.md:609`). B should demonstrate at least G49-0 and G49-4's REDs before execution rather than deferring every RED to the executor.

## Framing

Sentences that tell the reader how to weigh or feel rather than stating a fact or an instruction to act. Observation only.

### plan-A

- `plan-A.md:23` — "**Three of the four are RED on the tree right now and every one of those REDs is the gate working.** A gate that were GREEN today would be a gate with no subject." (Instructs the reader how to read a result before they have it.)
- `plan-A.md:25` — "A reviewer should read these first, because each is a place where the input and the tree disagreed and the tree won." (Addressed to a reviewer, not a worker; assigns the reading order and the verdict together.)
- `plan-A.md:508` — "**A conclusion that survives its own reason being wrong is the most expensive kind of correct there is**, and a claim that the duplication is gone while it is still there is worse than the duplication: the first costs a reader one check, the second costs them the habit of checking." (Aphorism carrying the weight an argument would.)
- `plan-A.md:803` — "**That GREEN is the finding.**" (Tells the reader what to feel about an output rather than what the output was.)
- `plan-A.md:1074` — "**The elided rows are the point, not a saving**: they are all `ok`." (Pre-empts a reader's inference about omitted evidence.)

### plan-B

- `plan-B.md:11` — "**Compare the mechanism that actually paints.** A facsimile is not evidence about imperative furniture." (A constraint hoisted above the option comparison it belongs to, stated before D49-1 is put.)
- `plan-B.md:12` — "**The shipped default is a gate subject, not a convenient preset.**" (The adjective *convenient* does the work of the argument against the alternative.)
- `plan-B.md:3` — "What remains before code is written is not a decision but an observation schedule." (Tells the reader how to weigh five open evidence gates rather than stating what is open.)
- `plan-B.md:154` — "**The generalisation is named as an inference so an owner can reject it without reopening the whole contract**." (Instructs the reader how to receive the inference, in the same sentence that makes it.)
- `plan-B.md:217` — "Naming it is what keeps it from being coverage loss wearing a cleanup label." (A rubric ending: tells a reviewer what to look for in the commit rather than stating the obligation.)
