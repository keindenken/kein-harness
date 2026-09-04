# Forced-choice comparison, plan-A vs plan-B

Reading order: `plan-A.md` first, then `plan-B.md`. Both read in full.

## 1. Scope fidelity — **A**, confidence medium

| | |
|---|---|
| Choice | A |
| Confidence | medium |

**For A.**

- The kickoff's line 47 instructs the plan to say explicitly whether it takes phase-47's routed (ii) and (iii) as riders. `plan-A.md:57` discharges it as its own section and gives a reason per item. `plan-B.md:50` also declines both, so this is not decisive on its own — but A additionally names the item the kickoff held back: the ~1 s Figma-style delay stays out at `plan-A.md:480`, and `padding-glyph` executes the standing owner direction rather than being re-asked as a decision at `plan-A.md:500`, which matches kickoff line 35's framing of that item as already directed.
- A's out-of-scope section (`plan-A.md:1193`–`1204`) enumerates every item the kickoff named at line 38 — v4/marquee, the L1 MCP server, the KI-19/49/50 family, KI-47, phase-48 residuals — plus multi-select drag, and each carries the reason it is out rather than a bare listing.

**Against A, for B.**

- A unilaterally reverses one of the owner's process rulings. Kickoff line 51 records codex as excluded by the owner's standing ruling of 2026-09-02; `plan-A.md:10` asserts the owner reversed it on 2026-09-04 and that "the lead has corrected the kickoff doc", and `plan-A.md:9` then counts codex lanes as consensus participants across five rounds. `base/docs/handoff/260903-phase-49-kickoff.md:51` still carries the exclusion. B's lanes are a fresh architect and a fresh critic only (`plan-B.md:3`), which is what the kickoff as written permits.
- A also re-asks something the kickoff records as already directed: `plan-A.md:1128` offers "two double-headed arrows per edge *(shipped)*" as candidate (1) for the spacing mark, while kickoff line 34 records the direction as "one `-` mark per edge instead of two icons". B rules cardinality out of the live pass for exactly that reason at `plan-B.md:154` and `plan-B.md:515`, and flags its own "per edge → per `SpacingAffordance`" generalisation as a named inference an owner may reject — the better handling of the owner-reserved boundary.

**Decisive against B.** Two additions B makes that the owner did not rule in, one of them overriding a documented repository convention:

- `plan-B.md:232` sets S49-0's completion at "The two old paths have zero references across the tracked tree AND the non-ignored working tree, including `.omc/plans` and `.omc/archive`", and `plan-B.md:338` (G49-0) makes that zero the GREEN condition over `-- .`. Measured on `base/`: the two targets carry 90 occurrences across 47 files, and **41 of those 47 files are under `.omc/archive/**`**. `base/docs/README.md:57` states that archived plans "are point-in-time records and are deliberately **not** rewritten". B's own text acknowledges the archive's record semantics at `plan-B.md:217` — but only about citation-gate coverage, never about the rewrite its done-when orders. So B's S49-0 either cannot reach green or reaches it by breaking a convention the repo documents. A scopes to enumerated roots that drop `.omc/archive/**` contents and `docs/handoff/**` for precisely this reason (`plan-A.md:177`, `plan-A.md:563`), and its 11-pointers-across-6-files census reproduces exactly on `base/`.
- B converts one of the four visual decisions into a contract-vocabulary migration: the `delegated-mark` kind lands in five hand-written closed sets, two production restatements and the spec KIND table, with positive-obligation arms added to G42-7, G44-5 B2, G46-2 and G46-3 (`plan-B.md:123`, `plan-B.md:162`), and S49-4 then retires two G44-5 universe-B legs and the F10 row (`plan-B.md:183`, `plan-B.md:189`). The kickoff's line 34 asks for a mark change on a comparison surface. B names its exit honestly (the revert unit at `plan-B.md:304`), which is why this is a fidelity finding and not a disqualification — but it is scope the owner did not rule in, on gates the kickoff's line 38 residual clause did not open.

## 2. Decision completeness — **A**, confidence high

| | |
|---|---|
| Choice | A |
| Confidence | high |

**For A.**

- A decides the mechanism down to the level at which an executor cannot silently choose differently. `plan-A.md:366` makes the four ring field spellings (`selectionWidthPx`, `selectionRadiusPx`, `hoverWidthPx`, `hoverInflatePx`) contract, and says why: a nesting that satisfies the prose contract leaves four gate rows at zero homes forever. `plan-A.md:124` names two source facts the chosen ring mechanism needs — the style writer takes no pool key today, and the primary ring carries no pool key at all — and decides the fallback in the plan rather than in the story.
- A reconciles two of its own rules that would otherwise both govern the same loop. `plan-A.md:293` rules that a candidate tried on the override is ungated and that C49-5's contract-first split binds the final value commit only. Without that ruling, driver D-B and contract C49-5 contradict each other over the phase's central activity, and an executor would have to decide mid-loop.
- Where A cannot decide, it parks with a named question and a default: every row of the owner table at `plan-A.md:1122` carries the shipped value as one of its candidates, and each story states its deferral default (`plan-A.md:448`, `:472`, `:490`, `:500`).

**Against A, for B.**

- B decides one thing A leaves as a workaround. A's re-render channel is a `tick` bump driven from a bare `[`/`]` keybinding, which then requires a text-entry guard, an `isComposing` guard, an IME fallback to a function key, and a spike leg to confirm all of it (`plan-A.md:276`–`288`, `plan-A.md:350`). B threads the profile through React state into the painters (`plan-B.md:117`), so re-render is structural and no key needs to be found or guarded. That is the cleaner decision on a real problem A discovered.

**Decisive against B.** B ships four review findings unclosed and one of them is a hole in a list two stories work from. `plan-B.md:3` records: "C49-4's grep-derived home list omits the four `use-spacing-affordances.ts` hits including `SPACING_GLYPH_CONTROL_KIND`, the sole production writer of the kind". Run on `base/`, `grep -rn --include='*.ts' --include='*.tsx' 'glyph-conditional' packages/descvi/src` returns four hits in `use-spacing-affordances.ts`, including the assignment that writes the kind value. `plan-B.md:170` enumerates "five production sentences beyond the two test files" and lists only the three in `use-resize-handles.ts` and one in `OverlayShell.tsx` — in the same paragraph that says the list must be "DERIVED BY GREP rather than carried" because "an enumeration written once and copied forward is exactly how the two homes below were missed for three review rounds". The plan carried a stale enumeration inside the sentence forbidding it, knew it, and shipped it. `plan-B.md:242` and `plan-B.md:292` route S49-1 and S49-4 from that list. An acknowledged-but-unclosed defect in a working list is worse than a parked question, because nobody is asked about it. Separately, `plan-B.md:221` asserts `check-v3-registers.mjs` is "the one audit gate in `.github/workflows/ci.yml` with no selftest step"; `base/.github/workflows/ci.yml` shows four such gates (KI register consistency :169, V3 register identity :176, session migration :179, extract outcome :187) — a claim B's own status line says is falsified and which the body still carries.

## 3. Executability — **A**, confidence medium

| | |
|---|---|
| Choice | A |
| Confidence | medium |

**For A.**

- A's smallest stories are startable and finishable with no question. S49-1a (`plan-A.md:360`–`391`) names the file, the four field spellings, the exact assertion sites its "every existing assertion passes unedited" claim rests on, and — at `plan-A.md:389` — the one leg of that claim that is weaker than the sentence (`toContain('1.5px')` passes on `'11.5px'`), with the executor told to read the width back exactly or record the weakness in the commit message. That is a bounded, testable completion condition with its own known gap disclosed.
- S49-0's rewrite list is enumerated per file with per-file occurrence counts (`plan-A.md:315`) and its done-when is four named commands and their exit statuses (`plan-A.md:332`), including the note that the gate is RED before the move so a post-commit RED means a missed pointer rather than a noisy gate.

**Against A, for B.**

- B's story template is materially easier to execute against: every story carries Purpose / Affected locations / Required behavior / Dependencies / Done when / Stop-failure (`plan-B.md:199`–`332`), and the Evidence Gates each carry a "Required before" line (`plan-B.md:359`, `:369`, `:378`, `:387`, `:398`) that orders the work. A has no equivalent stop-behavior line per story; it has one abort condition (S49-P) and a risks table.

**Decisive against B.** Three completion conditions a worker cannot finish in one round:

- S49-0's done-when is the unsatisfiable one from dimension 1 (`plan-B.md:232`): zero references including `.omc/archive`, against 41 archived files the repo says are not rewritten. A worker stops and asks.
- S49-4 is labelled SMALL at `plan-B.md:46`, and its Affected-locations paragraph (`plan-B.md:292`) is a single chain naming two production writers, five G44-5 legs across three dispositions, the F10 row, the conditional-arm checker's population filter, two spacing-family kind pins, the delegated arms in three specs, the spec, the owner record, the backlog and the tracker. Its done-when (`plan-B.md:298`) requires five leg dispositions plus eight named RED controls. That is not a SMALL story and the size label will mislead whoever picks it up.
- `plan-B.md:131` and `plan-B.md:503` require an exit-zero `pnpm test:e2e` on every tracked commit tree, documentation commits included. Against the kickoff's record that `main`'s e2e job is red on a flake, a hard per-commit exit-zero bound on the full browser suite is both very expensive and at risk of being unmeetable for reasons the story does not own.

A's own executability cost is real and should be said: S49-1 (`plan-A.md:393`–`427`) accumulates the override reader, four painter wirings, the keyboard handler and its guard, the spatial A/B indexing, a gate script, CI wiring, a witness-list widening and an ambient type declaration into one story. It is large. But each item names its source fact and its decided fallback, so it is large rather than under-specified.

## 4. Gate proportionality — **B**, confidence medium

| | |
|---|---|
| Choice | B |
| Confidence | medium |

**For B.**

- B's entire gate apparatus is `plan-B.md:336`–`347` (a twelve-line table holding ten gates) plus the Evidence Gates at `plan-B.md:351`–`399` (~49 lines) — roughly 61 lines, for a phase whose source footprint is larger than A's (a new comparison module tree, a toolbar toggle, a panel, painter seams, a shield handoff, and a kind vocabulary). Each row states a claim, a RED-when, a command, and a failure action in one line.
- Several of B's gates are sized to a real failure rather than to a category. G49-1's O1/O2 split (`plan-B.md:339`) exists because the default the gate asserts moves during the phase; its O2 RED-when — "restore that family's pre-phase value; the promoted family's row must fail" — catches an oracle that was rewritten into asserting nothing, which is a specific defect that a single fixed oracle would hide. EG49-5 (`plan-B.md:390`) is a census with a mandatory non-zero instrument control on a scene known to hold the family, so a zero is the tree's answer and not the probe's.

**Against B, for A.**

- Two of B's gates cannot fail for a reason of their own. G49-7's RED-when at `plan-B.md:345` is "The new focused RED demonstrations establish that phase gates can fail" — that is other gates' RED, not this one's. And G49-0's GREEN condition (`plan-B.md:338`) is the archive-scope one that cannot be reached, so the gate's verdict is not a fact about the work.
- A's gates, by contrast, name the RED direction per field rather than per gate. `plan-A.md`'s G49-3 RED-when table records that raising the reorder thickness is RED and lowering it is GREEN because the bound is one-sided, and that the run reports one failing test rather than three because three assertions sit in one `it()`. That per-field precision is genuinely better than any row in B's table.

**Decisive against A.** Size against subject. A's §6 runs `plan-A.md:515`–`1097` — **583 lines**. Inside it, G49-2 is `plan-A.md:537`–`707`, **171 lines**, and what it guards is S49-0's `git mv` of two files plus eleven one-line pointer edits (`plan-A.md:315`). G49-4 is `plan-A.md:837`–`975`, **139 lines**, and what it guards is the absence of one string literal from two bundle directories. Most of that length is not the gate: it is the record of how four prior revisions of the gate were wrong (`plan-A.md:543`–`547`, `:606`–`:611`, `:659`–`:697`), pasted transcripts of the same run under two shells (`plan-A.md:639`–`657`), and a selftest-of-the-selftest layer added at r5. The gates work; they are several times larger than the changes they watch, and the surplus is history rather than instruction.

## 5. Handoff readability — **B**, confidence high

| | |
|---|---|
| Choice | B |
| Confidence | high |

**For B.**

- 517 lines against A's 1232, with a fixed six-field story shape (`plan-B.md:199`–`332`) so a worker who has read one story knows where every field of the next one is. The "Affected locations" line means the file list is found without reading the argument that produced it.
- Forward references are resolved by an ordering line rather than by search: `plan-B.md:503` states the execution order and names the two things that must be upstream of the live session and why, and each Evidence Gate carries an explicit "Required before" (`plan-B.md:359`, `:369`, `:378`, `:387`, `:398`).

**Against B, for A.**

- B has its own unreadable passage, and it is in the story a worker will spend the most time in. `plan-B.md:292` is one sentence-chain of roughly 400 words carrying about fifteen backticked anchors, and it is S49-4's entire Affected-locations field. `plan-B.md:3` is a 250-word reviewer-facing status paragraph that ends by repeating its own last clause. A's story bodies, whatever else is wrong with them, break into headed fields.

**Decisive against A.** Most of A's text is addressed to reviewers, not workers. `plan-A.md:5`–`13` is a revision history of five rounds before any decision appears; `plan-A.md:25`–`37` is a numbered list of twelve reversals of earlier drafts that a worker has no use for; and the pattern recurs inside every section — `plan-A.md:160` ("r0 described it as three columns"), `plan-A.md:224` ("r1' said this file contributes 2. The closure audit measured 3. The lead measured 4"), `plan-A.md:389`, `plan-A.md:745`, `plan-A.md:1189`'s thirteen-instance PM-10 list. To assemble what to do for S49-1a a worker must read the story, D49-0's fact 2 (`plan-A.md:78`), G49-3's per-field table, G49-5's home-form column (`plan-A.md:1024` region) and register row U-13 (`plan-A.md:1231`), because the field spellings, the assertion sites and the weak leg are in four different places.

## Overall — **A**, confidence medium

A wins scope fidelity, decision completeness and executability; B wins gate proportionality and handoff readability. The dimensions A wins are about whether the plan answers the owner's rulings and can be run to a bounded end; the dimensions B wins are about what it costs to read and how much apparatus rides along. A's readability cost is severe but survivable — a worker who invests the reading finds every decision made, every default stated and every fallback pre-decided. B's two hardest defects are not survivable in the same way: S49-0's completion condition orders a rewrite of 41 archived records that `base/docs/README.md:57` forbids, and C49-4's grep-derived home list is missing the sole production writer of the kind it is migrating — a hole B recorded in its own status line and shipped anyway. A worker hits both.

**What the losing plan does better, and the winner should take it.** B's story shape is the thing to import wholesale: Purpose / Affected locations / Required behavior / Dependencies / Done when / Stop-failure, one per story, with an "Affected locations" list that a worker can open without reading the argument that produced it, and a per-story stop rule that says what to do when the story cannot finish rather than leaving it to the risks table. Beyond the shape, three specific mechanisms: the Evidence Gates with "Required before" lines, which give A's S49-P siblings it does not have and would have given A's several unmeasured claims a scheduled runner; the owner-pass record and its field validator (`plan-B.md:219`, `plan-B.md:342`), which makes the owner's ruling itself a machine-checked artifact instead of a table someone remembers to fill — A's D49-3 table has no such check; and G49-1's O1/O2 oracle-authority split (`plan-B.md:339`), which names the moment a baseline oracle stops being evidence, a boundary A handles only implicitly through C49-5's commit discipline. Finally, B's three-way revert-unit decomposition of its LARGE story (`plan-B.md:248`–`252`) is the right treatment for A's S49-1, which currently ships the reader, the keybinding, the spatial A/B and the CI wiring as one unit.

## Framing

Sentences that tell the reader how to weigh or feel rather than stating a fact or an instruction. Observation only.

### plan-A.md

| Line | Quote |
|---|---|
| 23 | "**Three of the four are RED on the tree right now and every one of those REDs is the gate working.** A gate that were GREEN today would be a gate with no subject." |
| 25 | "**A reviewer should read these first, because each is a place where the input and the tree disagreed and the tree won.**" |
| 35 | "**a correction that is not announced is indistinguishable from a transcription error.**" |
| 508 | "**A conclusion that survives its own reason being wrong is the most expensive kind of correct there is**, and a claim that the duplication is gone while it is still there is worse than the duplication: the first costs a reader one check, the second costs them the habit of checking." |
| 695 | "**Read the two RED lines against each other.**" |

Two of these are rubric endings aimed at a reviewer (23, 25); two are aphorisms standing in for the argument they summarise (35, 508); one instructs the reader how to interpret a transcript rather than what to do (695). A sixth of the same kind, not counted: `plan-A.md:5`'s opening insistence that r5 is "a HARDENING pass on r4', and NOT a sixth text round", a constraint about the drafting process hoisted above every problem the document is about.

### plan-B.md

| Line | Quote |
|---|---|
| 3 | "…so the consensus gate is discharged and this plan stands over four recorded findings rather than over nothing" |
| 11 | "A facsimile is not evidence about imperative furniture." |
| 36 | "The price is a small permanent comparison control in the existing toolbar and sequential A/B viewing, which is lower risk than preserving a second renderer." |
| 170 | "an enumeration written once and copied forward is exactly how the two homes below were missed for three review rounds." |
| 217 | "Naming it is what keeps it from being coverage loss wearing a cleanup label" |

Line 3 tells the reader how to read an approval that two lanes returned REVISE on. Line 11 is a principle carrying its conclusion inside its adjective. Line 36 asserts a risk comparison as settled where no measurement is offered. Line 170 is a moral drawn from the plan's own review history, sitting where an instruction belongs. Line 217 tells the reader what the naming is for rather than adding to what is named.
