# Forced choice, plan-A vs plan-B, phase-49

| Dimension | Winner | Confidence |
|---|---|---|
| 1. Scope fidelity | B | medium |
| 2. Decision completeness | A | medium |
| 3. Executability | A | medium |
| 4. Gate proportionality | B | high |
| 5. Handoff readability | B | high |
| **Overall** | **B** | medium |

## 1. Scope fidelity — B

**For B.** The kickoff makes each backlog row the source of truth for its parked decision (kickoff:31, kickoff:43). The `spacing-affordance-mark` row (`base/docs/post-loop-backlog.md:178`) carries two things as received: *"변마다 아이콘 두 개가 아니라 `-` 자국 하나 — Figma의 것은 가로 12–13px, 세로 2px, 1px 외곽선"*. B carries both into the pass — cardinality as a recorded owner direction rather than a live-pass field (plan-B.md:154), and the reference dimensions as labelled comparison inputs (plan-B.md:146, plan-B.md:515). B also refuses to edit the kickoff, on the ground that it is a dated record and the plan is the executable authority (plan-B.md:207), which matches this repo's own rule at `base/docs/README.md:57`.

**For B, second.** B treats the cardinality change as an ownership question rather than a path swap and names the one thing it inferred beyond the owner's words — generalising "per edge" to one mark per `SpacingAffordance` — so the owner can reject that alone (plan-B.md:154). Source supports the reading: `base/packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts:107,120,300` gives every strip **and every apron** its own glyph, and `spacing-affordance-geometry.ts:311` records one apron per padding edge — i.e. two icons on one edge, literally the shape the owner asked to reduce.

**Against B / for A.** A scopes S0's rewrite correctly and B does not. A rules the frozen-record namespaces out of the rewrite list (plan-A.md:177, plan-A.md:209) and publishes a census of 11 pointers across 6 files (plan-A.md:213-222). I reproduced it exactly on `base/`: `docs/architecture.md`, `docs/known-issues.md`, `docs/e3/tracker.md`, `.omc/plans/ralplan-phase-46-…`, `.omc/research/phase48-strip-band-pricing.md`, `.omc/archive/README.md`. B instead sizes the work at "90 occurrences across 47 tracked files" (plan-B.md:103) — also reproducible — and makes zero references "across the tracked tree … including `.omc/plans` and `.omc/archive`" a done-when (plan-B.md:232). 41 of those 47 files are `docs/handoff/**` or `.omc/archive/**`, which `base/docs/README.md:57` says are *"point-in-time records and are deliberately not rewritten"*. B never names that convention as a bound, and contradicts itself at plan-B.md:217 where it does invoke the immutable-record semantics for anchors.

**The offsetting A defect.** A reduces the same spacing item to a path swap — *"one `-` per edge instead of two icons (a change to `SPACING_GLYPH_PATHS` and `figureFor`)"* (plan-A.md:478) — and never mentions the 12–13 px × 2 px × 1 px outline reference anywhere in 38,000 words (`grep` for `12–13`/`outline` in plan-A.md returns nothing). Its gate note that *"A mark change keeps the `<svg>`, so the obligation is untouched"* (plan-A.md:482) is true only under the reading that leaves cardinality alone. A also amends the owner's kickoff document (plan-A.md:10) — a document whose own line 3 declares it the record of the ruling.

Net: A is more faithful on S0, B on the parked visual item that is the phase's substance and on the record-editing rule. B.

## 2. Decision completeness — A

**For A.** A closes the fidelity question its own form creates and B leaves open. A's second reason for (b) is that a comparison mechanism reached by the pointer destroys the subject — the hover ring dies, the drag ends (plan-A.md:118) — and it answers that with two named mechanisms: a keyboard channel on the existing remeasure `tick`, and a spatial A/B for the one persistent subject (plan-A.md:128). B chooses the same form and its cost line concedes *"compares one live preset at a time"* (plan-B.md:28), but nothing in B says how the owner judges a hover ring or a live reorder indicator while reaching for a toolbar panel. B's S49-3 asks for exactly that comparison (plan-B.md:145) without the mechanism.

**For A, second.** A names decisions B leaves as executor discretion: the exact key and its text-entry guard, with the key space enumerated from source (plan-A.md:278-286); the exact four field spellings the gate greps (plan-A.md:366); the ambient `import.meta.env.DEV` declaration and why not to reach for `vite/client` (plan-A.md:403); a per-row deferral default including the one row whose default is CHANGE (plan-A.md:500); and a reopen path for D49-1 with three named surviving options rather than "return to the owner" (plan-A.md:352).

**Against A / for B.** B's parked items are better labelled as unmeasured. EG49-3 refuses to assign the reorder degenerate arms to a route by assertion and measures the separation sign first (plan-B.md:375), and EG49-5 makes the layer-wide coverage claim conditional on a census with a mandatory non-zero instrument control (plan-B.md:390-396). A's equivalents sit in an UNVERIFIED register (plan-A.md:1221-1225) with "not executed" beside them and no gate ordering them before the story that depends on them. B also carries four unresolved review findings in the open (plan-B.md:3), which is a demerit for completeness but not a silent one.

## 3. Executability — A

**For A.** A's done-whens are exit statuses and named artefacts: S49-0 closes on `check-citation-anchors.mjs` green **and** two specific script exits **and** both steps present in CI (plan-A.md:332); the value stories close on a recorded RED transcript beside the value commit (plan-A.md:446, plan-A.md:470). B's close on prose lists plus a manual markdown-link review (plan-B.md:232, plan-B.md:236) and an owner live pass.

**For A, second — and it is the decisive one.** B's S49-0 cannot be finished as written. Its done-when requires zero old-path references across the tracked tree including `.omc/archive` (plan-B.md:232) over the 47-file population it measured (plan-B.md:103), 41 of which `base/docs/README.md:57` forbids rewriting. A worker either breaks the convention or stops to ask. A's S49-0 hands the worker a six-row rewrite table (plan-A.md:213-222) that I verified is the correct live set.

**Against A / for B.** Story size favours B. B splits its one LARGE story into three independently revertible commits with stated revert consequences (plan-B.md:250-252) and gives every story the same five-field shape — Affected locations, Required behavior, Dependencies, Done when, Stop/failure. A's S49-1 lands the override reader, per-family records, four painter wirings, the keyboard bump, the text-entry guard, the spatial A/B, a new gate script with a selftest, CI wiring, and a widened witness list in one story (plan-A.md:395-425), with no commit boundaries inside it. B's stop/failure clause per story (e.g. plan-B.md:258, plan-B.md:304) is the thing A has only for the spike.

## 4. Gate proportionality — B

**Size against subject.** A's §6 runs plan-A.md:515-1097 — **583 lines of 1,232, 47% of the plan**. G49-2 alone is plan-A.md:537-707, **171 lines**, and what it guards is `git mv` on two files plus six pointer rewrites (plan-A.md:313-315). G49-5 is plan-A.md:976-1081, **106 lines**, guarding four field spellings introduced by one refactor story (plan-A.md:366). B's whole gate apparatus is plan-B.md:334-349 (a 12-row table, ~16 lines) plus plan-B.md:351-399 (five evidence gates, ~49 lines) — **65 of 518 lines, 13%** — and each row carries a claim, a RED-when, a command, and a failure action.

**Guarding something a story changes.** A concedes G49-3 duplicates work CI already does: *"its seven witnesses run inside `Test (per-package)` too"* (plan-A.md:385), and prices it at 2.9 s locally plus ~20 s in CI for a re-run of assertions already running. A also prices two extra full Vite builds onto every local `pnpm gates` run from S49-1 onward (plan-A.md:421). B's one new script — the owner-pass record validator — guards five owner rulings that otherwise land in no machine-checked artefact (plan-B.md:342), and B's G49-1 O1/O2 split guards a real failure shape (an oracle rewritten in place during promotion, plan-B.md:339).

**For A.** A's gates were actually run, and its r5 pass shows each selftest RED from a copy that *reduces the gate's scope* rather than breaking a pattern (plan-A.md:659-695) — that is a stronger falsifiability proof than any of B's, which are all execution-time promises. And A's PM-12 argument that a gate must land in a named story and in CI or it stops being a gate (plan-A.md:1190) is correct; B adopts the same rule for its one validator (plan-B.md:221) but does not apply the reasoning to anything else.

## 5. Handoff readability — B

**Measured.** plan-A.md: 38,523 words, 166 lines carrying ⚠, and **292 references to revision rounds** (`r0`/`r1'`…`r5`). plan-B.md: 18,784 words, 3 ⚠ lines, **0** revision-round references. A worker opening plan-A at S49-1a meets four consecutive paragraphs about what r3' and r4' got wrong (plan-A.md:366-369, plan-A.md:389) before reaching an instruction.

**Addressed to reviewers, not workers.** A's status block is 34 lines of adjudication history and a twelve-item reversal register aimed explicitly at a reviewer — *"A reviewer should read these first"* (plan-A.md:25). Its gate sections carry pasted transcripts with commentary on which transcript rows are findings rather than demonstrations (plan-A.md:606-611). None of that is work.

**For A.** A's cross-references resolve to a single home by construction — the anchor count lives only in D49-4 (plan-A.md:24, plan-A.md:257), the threshold interval only in U49-B (plan-A.md:508) — so a worker who follows a pointer does not find two answers. B repeats less but forward-references more: S49-4's Affected-locations paragraph (plan-B.md:292) is one sentence spanning a dozen gate legs across four files and is unreadable without first reading C49-4 (plan-B.md:152-196), and S49-1's `delegated-mark` landing cannot be understood without EG49-5 (plan-B.md:390) fifty paragraphs later.

## Overall — B, medium confidence

B wins scope fidelity, gate proportionality and handoff readability; A wins decision completeness and executability. The two A wins are narrow and partly self-inflicted — A's executability edge comes from pre-answering micro-questions, but the same plan makes a worker read 583 lines of gate apparatus to land a docs move. The two decisive B wins are structural: a plan where 47% of the text is gates guarding a two-file `git mv` and a dev-only flag has mispriced its own subject, and a plan carrying 292 references to its own review history has stopped being written for the person who executes it.

**What A does better that B should take.** A's S0 scoping is simply correct and B's is not: A separates live pointers from frozen records with the repo's own rule (plan-A.md:177, plan-A.md:209) and hands the worker the exact six-file rewrite list, where B hands over a 47-file population that includes 41 files it must not touch. B should replace its "zero references across the tracked tree" done-when (plan-B.md:232) with A's predicate. B should also take A's D49-0 painter-reachability table (plan-A.md:65-79) — the finding that three of the four subjects have no painter callable from outside the overlay is the strongest single argument either plan makes for form (b), and B argues the same conclusion from a weaker premise (plan-B.md:36). Finally B should take A's pre-answered execution traps: the no-tolerance selection-ring box comparison in `e2e/multi-select-shield.spec.ts` that forces the hover-larger change onto the hover side (plan-A.md:468), and the `SPACING_GLYPH_PX` change that drags a Playwright title and the identity golden with it (plan-A.md:484).

## Framing

Sentences that tell the reader how to weigh or feel rather than stating a fact or an instruction. Observation only.

**plan-A**

- plan-A.md:6 — "⚠ **r3' WAS A DESIGN CHANGE AND r4' FINISHES IT; A READER WHO TREATS EITHER AS A TEXT REPAIR WILL MISREAD §6.**"
- plan-A.md:23 — "**Three of the four are RED on the tree right now and every one of those REDs is the gate working.** A gate that were GREEN today would be a gate with no subject."
- plan-A.md:25 — "A reviewer should read these first, because each is a place where the input and the tree disagreed and the tree won."
- plan-A.md:508 — "**A conclusion that survives its own reason being wrong is the most expensive kind of correct there is**, and a claim that the duplication is gone while it is still there is worse than the duplication."
- plan-A.md:1092 — "**A gate nobody schedules is a habit with a number on it.**"

**plan-B**

- plan-B.md:3 — "the consensus gate is discharged and this plan stands over four recorded findings rather than over nothing."
- plan-B.md:11 — "A facsimile is not evidence about imperative furniture."
- plan-B.md:12 — "**The shipped default is a gate subject, not a convenient preset.**"
- plan-B.md:36 — "The price is a small permanent comparison control in the existing toolbar and sequential A/B viewing, which is lower risk than preserving a second renderer."
- plan-B.md:217 — "Naming it is what keeps it from being coverage loss wearing a cleanup label."
