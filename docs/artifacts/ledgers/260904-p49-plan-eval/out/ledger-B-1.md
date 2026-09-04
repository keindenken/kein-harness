# Execution ledger — plan-B.md (phase-49)

Lead's note on the unit of measure: `plan-B.md` is 517 lines and 133,893 bytes — a mean of **259 characters per line**, roughly three screen lines each. Every `reading_cost` below is a source-line count; multiply by about three for what a worker actually reads.

---

## S49-0 — close the records before source work

**title.** v3.5 close housekeeping: tracker phase-48 section, two v3 plan moves, owner-pass record + validator + CI wiring.

**scope** — *given*, and given unusually precisely, at `plan-B.md:203`: `docs/e3/tracker.md` (the v3 CLOSE section and its deferred-archiving paragraph); `.omc/plans/ralplan-e3-v3-direct-manipulation.md`; `.omc/plans/ralplan-phase-42-resize-handles.md`; `.omc/archive/260901-e3-v3/`; `.omc/archive/README.md`; every tracked file returned by the two-target `git grep` in §2.5 (`plan-B.md:103` measures 47 files / 90 occurrences); new `docs/e3/phase-49-owner-pass-record.md`; new `scripts/check-owner-pass-record.mjs`; the `verify` job in `.github/workflows/ci.yml`.

*Inferred by me*: the tracker's phase-48 section must match "the same idiom as phase-47" (`plan-B.md:232`) — the idiom itself is not in the plan and the worker has to read `base/docs/e3/tracker.md` to find it.

**completion_condition.** Move exactly the two D49-2 files into the already-existing `.omc/archive/260901-e3-v3/` (`plan-B.md:31`), leaving `open-questions.md`, `ralplan-phase-46-…` and `ralplan-phase-48-…` in `.omc/plans/`; rewrite every path reference so that the `--untracked` closure scan of `plan-B.md:105` prints nothing over both the index and the non-ignored working tree; amend the tracker's deferred-archiving paragraph in the *same commit* so it no longer names `260817-e3-v3` or the stale 34-reference count (`plan-B.md:207`, `232`); add the missing `260901-e3-v3/` row to `.omc/archive/README.md` (`plan-B.md:109`); add a phase-48 routing note plus per-story record for S48-0a/0b/1/2/3/4/5; create the owner-pass record with all five families `status: pending`; create `scripts/check-owner-pass-record.mjs` with a hardcoded field vocabulary and a `--selftest` covering three failure shapes; wire **two** steps into the CI `verify` job (`plan-B.md:221-228`); record in the commit message that the moved plans' 168 code anchors leave `SCAN_ROOTS` (`plan-B.md:209`, `217`). Verified by `node scripts/check-citation-anchors.mjs`, `node scripts/check-owner-pass-record.mjs --selftest` and `node scripts/check-owner-pass-record.mjs` all exiting zero, with the citation gate's green explicitly not read as evidence about anything now in `.omc/archive/` (`plan-B.md:232`).

**verification_path.**
- `plan-B.md:356` (EG49-1) — seven commands run in one sitting: the four `-- .` censuses with `git grep -o` (never `-c`), plus `ls -d .omc/archive/260817-e3-v3 2>/dev/null || echo ABSENT`, `git ls-files .omc/archive/260901-e3-v3/`, `git grep -o '\.omc/archive/260901-e3-v3' -- . | wc -l`, and the README `comm -23` row check at `plan-B.md:109`.
- `plan-B.md:105`, `338` (G49-0) — closure scan `git grep --untracked -n -E '\.omc/plans/(ralplan-e3-v3-direct-manipulation|ralplan-phase-42-resize-handles)\.md' -- .` prints nothing; two RED controls at `plan-B.md:234`: (1) plant an old-path reference inside a moved-but-unstaged destination and confirm `--untracked` names it while plain `git grep` names nothing, (2) confirm the pre-existing old-path reference in `ralplan-phase-46-ring-furniture-restyle.md` is named before it is fixed.
- `plan-B.md:211-216` — the anchor-count loop, re-run immediately before the move.
- `plan-B.md:342` (G49-4) — validator RED by deleting a required field from a `recorded` section; `--selftest` covers that shape plus a `recorded`-with-no-fields flip plus an out-of-set status.
- `plan-B.md:232` — final: `pnpm gates` picks up both new `run:` steps.

**invented.**
1. **The validator's field vocabulary for four of five families.** `plan-B.md:219` enumerates required fields for S49-4 only ("outer width, outer height, computed fill, outline width, and outline colour in both themes, plus the explicitly held delay"). `plan-B.md:342` gives a generic list ("routes, themes, orientations, selected alternatives, rejected alternatives, measured values, and held questions"). I derived S49-2/S49-3/S49-5/S49-R's required fields from the "Owner ruling recorded" column of C49-3 (`plan-B.md:144-148`) — place/extent/weight/blue/visual-count-claim; radius/selected width/hover width/hover-vs-selection relation; pad figure + dimensions; keep-or-split + value. That derivation is mine; a different reader could ship a thinner vocabulary and still pass every stated check.
2. **The record's on-disk syntax.** `plan-B.md:219` says each section "declar[es] `status: pending` or `status: recorded`" but never says whether that is YAML front-matter per section, a markdown table cell, or a literal line. The validator's parser depends entirely on this and nothing constrains it.
3. **Commit boundaries inside S49-0.** `plan-B.md:207`/`232` fix one boundary (tracker amendment rides with the move). Whether the tracker phase-48 section, the owner-pass record + validator, and the CI wiring are one commit or three is unstated, while `plan-B.md:503` requires an exit-zero `pnpm test:e2e` per tracked commit tree — so the count is a real cost decision. I chose three (see `one_round`).
4. **`base/docs/e3/tracker.md`'s phase-47 idiom.** "the same idiom as phase-47" (`plan-B.md:232`) is a pointer out of the plan; the shape of the record — heading depth, per-story row format, what a "routing note" contains — is mine.

**would_ask.** None that block. The four items above are all decidable by a competent worker from repository evidence, and the plan's stop rule at `plan-B.md:236` and EG49-1's alternate path at `plan-B.md:358` cover the two ways this story can go wrong (an unresolvable reference; a `260817-e3-v3/` that has since appeared).

**one_round: split** — into three.
- Files in scope: 5 named documents + ~47 reference-carrying tracked files (`plan-B.md:103`) + 2 new files + `.github/workflows/ci.yml` ≈ **55**.
- Distinct acceptance claims in the done-when (`plan-B.md:232`): **12** (zero old-path refs across index *and* working tree; new paths exist; one v3 directory; retained three unmoved; tracker paragraph amended in the move commit; README row; tracker phase-48 section; record exists with five `pending`; coverage change recorded with count and command; commit message names the scan-root exit; CI carries both steps; three commands exit zero).
- Gates to implement and drive RED: **2** (G49-0's two arms, G49-4's validator RED) plus a `--selftest` covering three shapes.
- Evidence gates to run: **1** (EG49-1, seven commands).
- Split: **(0a)** the archive move + 47-file reference rewrite + tracker paragraph amendment + README row, gated by G49-0's two RED controls; **(0b)** the tracker phase-48 section (pure prose, no gate); **(0c)** `check-owner-pass-record.mjs` + the record + `--selftest` + the two CI steps, gated by G49-4. (0a) alone is a full sitting: 47 files of hand-checked markdown links, with the plan explicitly forbidding a green citation gate from standing in for that review (`plan-B.md:111`, `236`).

**reading_cost: ~68 lines** (≈ 200 screen lines). Sections: header/status `1-4` (4); D49-2 rows `30-32` (3); §1 scope row `42` (1); §2.5 `101-111` (11); S49-0 `199-236` (38); gate rows G49-0/G49-4/G49-7/G49-9 `338, 342, 345, 347` (4); EG49-1 `353-360` (8); risk rows `497-498` (2); sequencing `503` (1). A worker can skip §2.1–§2.4, all of §3 except G49-4's subject, and every other story.

---

## S49-1 — build the real comparison surface without moving a pixel by default

**title.** `OverlayComparisonProfile`, painter injection seams, toolbar toggle and panel; press-scoped shield threshold handoff; uninhabited `delegated-mark` vocabulary landing.

**scope** — *given* at `plan-B.md:242`, and it is the longest affected-locations list in the plan: new `packages/descvi/src/react/overlay/comparison/**`; `OverlayShell.tsx`; `toolbar/OverlayToolbar.tsx`; painter modules under `canvas/` including `use-canvas-selection-shield.ts`; focused tests under `overlay/__tests__/` (`canvas-selection-shield-travel.test.tsx`, `resize-handle-layer.test.tsx`) and `packages/descvi/test/reorder/`; the five hand-written closed-kind-set homes enumerated at `plan-B.md:164-168`; the two closed-set restatement homes in `use-resize-handles.ts` (`plan-B.md:172`); the spec KIND table; `delegated-mark` arms in `e2e/resize-handles.spec.ts`, `e2e/spacing-gesture.spec.ts`, `e2e/multi-select-shield.spec.ts`, `e2e/reorder-drag.spec.ts`; `e2e/fixtures/expected-identities.json` **only if** a collected row is added.

*Inferred by me*: which painter modules are "applicable". §2.2 (`plan-B.md:81-85`) implies `reorder-paint.ts`, `use-selection-rings.ts`, `use-spacing-affordances.ts`, `use-reorder-drag.ts` and `pointer-thresholds.ts`, and `plan-B.md:83` explicitly excludes `handle-geometry.ts`/`DEFAULT_HANDLE_GEOMETRY` from override. That exclusion is stated; the positive list is not.

**completion_condition.** Land one named `OverlayComparisonProfile` and one exported `SHIPPED_OVERLAY_PROFILE` in a new module, holding inputs only and creating no DOM (`plan-B.md:117`), with four independently resettable families; thread the applicable slice into the existing painters as a defaulted parameter so that with comparison inactive **and** after Reset the inline styles, geometry, hit targets, layer ownership and gesture behaviour are byte-equivalent to the pre-seam tree (`plan-B.md:119`, `244`, `366`); add the toolbar toggle and a chrome panel outside `#dsh-screen` and `#dsh-ring-layer` that labels Baseline/Candidate, displays every active value, is keyboard reachable, uses bilingual labels, persists across route navigation within an overlay session, and resets in one action; add a press-scoped handoff giving `use-canvas-selection-shield.ts` an effective threshold for the press reorder classification just saw, resolving to `POINTER_DRAG_THRESHOLD_PX` for every unclassified press (`plan-B.md:246`, `251`); add `delegated-mark` to the four-value closed set in all five hand-written homes and both restatement homes and the spec KIND table, plus positive-obligation arms at G42-7, G44-5 B2, G46-3 and the spacing dispatch, with the **production population empty** and every arm exercised on plants (`plan-B.md:123`, `246`). Nothing under `src/app/**` and nothing in `.descvi/screens.json` changes (`plan-B.md:256`). Landed as three independently revertible commits (a)/(b)/(c) in that order (`plan-B.md:250-252`), each recording exit-zero `pnpm test:e2e`.

**verification_path.**
- `plan-B.md:362-370` (EG49-2) — capture fixed pre-change DOM/style/geometry expectations per family *before* the seam lands; re-run after, comparison inactive and after Reset; confirm the `delegated-mark` production population is empty. Precedes (a) and (b) (`plan-B.md:254`).
- `plan-B.md:390-399` (EG49-5) — `pnpm exec playwright test e2e/resize-handles.spec.ts --project=design-view` with a task-scoped probe reading `scene.operable` filtered on `family === "spacing"` for the G42-7 and G46-2/G46-3 scenes; **mandatory instrument control**: the same probe against the padded G48-6b scene must return non-zero. Required before (c) and only before (c).
- `plan-B.md:339` (G49-1 / oracle O1) — change one shipped-profile value while leaving fixed expectations untouched; the family's baseline row must fail.
- `plan-B.md:340` (G49-2) — disconnect one profile prop at a hook/painter boundary; the control row stays interactive but the real node fails to change; shell integration test observes one node identity before/after with no second family node.
- `plan-B.md:341` (G49-3) — alias the candidate to the shipped object and mutate it; default and reset rows must fail. `node scripts/check-handle-constants.mjs --selftest` and `… .mjs` exit zero.
- `plan-B.md:256` — the shield's five existing release cases and the reorder mute row stay green with the handoff resolving to the shared constant; each new `delegated-mark` arm demonstrated RED on a plant with the three C49-4 mutations (`plan-B.md:195`); a real `descvi:dev` smoke changes each family once on a shipped route and Reset restores it.

**invented.**
1. **The profile's field shape for two of four families.** `plan-B.md:117` fully enumerates the spacing slice ("ownership form, outer width, outer height, fill, outline width, outline colour, figure, and reveal trigger") and the threshold slice (one resolved value). The **reorder paint/readout** and **selection/hover ring** slices are named as families and never enumerated. §2.2 (`plan-B.md:81-82`) lists the current values — thickness, edge offset, readout gap, radius, colour, cross extent; selected border, hover border, radius, per-side outset — so I took those as the field set. Nothing in the plan says so, and C49-3's ruling columns (`plan-B.md:144-145`) name a *different*, coarser set ("place, extent, weight, blue"), which does not map onto the constants one-to-one — "place" has no current constant at all.
2. **Where the G44-5 B2 plants live.** `plan-B.md:246` requires every new arm "exercised on planted nodes"; `plan-B.md:158` says G42-7's mutations are "planted at that row rather than only in the spacing spec"; `plan-B.md:123` cites `resize-handle-layer.test.tsx#it("G46-3 glyph arm — its population here is EMPTY after S46-2…` as the precedent. For **G44-5 B2 in `e2e/spacing-gesture.spec.ts`** no host is named. I placed the plant in the spacing spec's existing three-mutant plant harness (`plan-B.md:188` establishes that harness exists there). The plan's own status line records this as an unfixed finding: *"S49-1 does not say where its G44-5 B2 and G42-7 plants live"* (`plan-B.md:3`).
3. **Whether the closed-set edit at `e2e/spacing-gesture.spec.ts` reaches the adjacent family-kind pin.** `plan-B.md:246` tells S49-1 to widen the closed set — one of whose five homes is `e2e/spacing-gesture.spec.ts#expect(["glyph", "glyph-conditional", "cursor"],` (`plan-B.md:166`) — while `plan-B.md:182` reserves the kind pin one line below it (`e2e/spacing-gesture.spec.ts#is the conditional kind`) for S49-4. The two edits sit in the same test body. I ruled that S49-1 touches only the array literal and leaves the pin's string untouched. The plan's status line records the same risk: *"one reading of it would widen leg (i) a story early"* (`plan-B.md:3`).
4. **Modality of candidate persistence across navigation.** `plan-B.md:117` says navigation "**may** retain the candidate during the same overlay session"; `plan-B.md:244` says the surface "persists across route navigation in the current overlay session" as a required behaviour. I read the second as governing and the first as its rationale. A worker reading the first as permissive would ship a surface that resets on navigation — and C49-3's reorder row (`plan-B.md:144`) requires comparing `/shop/member-list` against `/lab/tests/reorder-flow`, which that reading breaks.
5. **Whether the O1 baseline snapshot is a tracked fixture.** `plan-B.md:256`/`366` require "expectations captured before the seam landed" and `plan-B.md:258` rejects any oracle derived from `SHIPPED_OVERLAY_PROFILE`, offering "fixed expectations or an immutable before-state snapshot" as the two legal forms. Which one, and whether the snapshot is committed, is mine. It matters: `plan-B.md:365` says O1 expires at the first promotion, so a committed snapshot needs a stated retirement.
6. **Whether S49-1 adds a collected Playwright row.** `plan-B.md:242` permits `e2e/fixtures/expected-identities.json` to move "only if a collected row is added"; `plan-B.md:95` says to prefer focused package tests plus an explicit smoke. I ruled no collected row in S49-1, which keeps the identity golden clean but leaves the cross-route persistence behaviour (item 4) proven only by the manual smoke.
7. **Keyboard-reachability acceptance.** `plan-B.md:244` requires the panel be "keyboard reachable" and `plan-B.md:256` asks tests to prove "keyboard access". No key, focus order, or escape behaviour is specified; the assertion is mine.

**would_ask.**
- Does S49-1 commit (c)'s closed-set widening at `e2e/spacing-gesture.spec.ts` include or exclude the family-kind pin one line below it (`plan-B.md:166` vs `plan-B.md:182`, `246`)? A wrong answer either strands S49-4 or turns S49-1 into a pixel-moving story.
- Where does the G44-5 B2 plant live (`plan-B.md:246`)?
- Does S49-1 own EG49-3's synthetic-overlap unit row? `plan-B.md:378` says the census "runs early enough that S49-1 knows whether it owes the synthetic overlap row"; `plan-B.md:377` and `349` assign the row to `packages/descvi/test/reorder/reorder-paint-geometry.test.ts` without naming a story; `plan-B.md:270` puts it in S49-2's done-when; and `plan-B.md:254` lists only EG49-2 and EG49-5 as S49-1's dependencies. Three owners, no ruling. Recorded unfixed at `plan-B.md:3`.

**one_round: split** — the plan has already split it, and I would dispatch the three commits as three briefs.
- Files in scope: **~20** named at `plan-B.md:242` (5 closed-set homes, 2 restatement homes, 1 spec, 4 e2e specs, ≥4 painter modules, 2 shell/toolbar files, ≥2 new modules, ≥3 test files).
- Distinct acceptance claims in the done-when (`plan-B.md:256`): **9**.
- Gates to implement and drive to a failing state: **5** (G49-1 O1, G49-2, G49-3, G49-5's plant arms, G49-8), plus three named RED mutations per new `delegated-mark` arm across four dispatches (`plan-B.md:195`).
- Evidence gates to run: **2** (EG49-2, EG49-5 — the latter with a mandatory non-zero instrument control on a second scene).
- Split as the plan's own (a)/(b)/(c) (`plan-B.md:250-252`): **(a)** profile + seams + surface, gated by G49-1 O1, G49-2, G49-3 and EG49-2; **(b)** the shield handoff, gated by the five existing release cases and the mute row; **(c)** the vocabulary landing, gated by EG49-5 first and then four planted arms across seven files. (c) alone touches five hand-written closed sets that `plan-B.md:162` insists cannot be derived from one another — that is five independent edits plus two restatements plus a spec table in one review round.

**reading_cost: ~200 lines** (≈ 600 screen lines) — the worst in the plan. Sections: status `1-4` (4); principles + DR49-1/2/3 `9-22` (14); D49-1 rows and "Why form (b) wins" `27-29, 36` (4); §1 rows `42-43, 52` (3); §2.1 `56-61` (6); §2.2 `62-87` (26); §2.3 `89-95` (7); C49-1 `115-123` (9); C49-2 `125-138` (14); **all of C49-4 `152-195` (44)** — unavoidable, because commit (c) writes the arms C49-4 defines; S49-1 `238-258` (21); gate rows `339-343, 346` (6); EG49-2 `362-370` (9); EG49-5 `390-399` (10); pre-mortem S1/S2/S3 `403-422` (20); risk rows `491-493, 495` (4). A worker doing only commit (a) can drop C49-4, EG49-5, and pre-mortem S3 — about 74 lines — and reads ~126.

---

## S49-2 — decide and promote reorder indicator/readout treatment

**title.** Close `reorder-indicator-look` and phase-47 U9 option (E).

**scope** — *partly given, partly inferred*. Given at `plan-B.md:264`: comparison profile/controls; `packages/descvi/src/react/overlay/canvas/reorder-paint.ts`; `docs/post-loop-backlog.md`; `.omc/specs/v3-layout-panel-visual-spec.md`; `docs/e3/tracker.md`.

*Inferred by me*: "reorder geometry and paint tests" and "relevant e2e spec/golden if collected coverage changes" (`plan-B.md:264`) name no paths. From §2.2 (`plan-B.md:81`) I resolved these to `packages/descvi/test/reorder/reorder-paint-geometry.test.ts`, `reorder-paint.test.tsx`, and `e2e/reorder-drag.spec.ts`; the G47-6 owner file is never given a path anywhere in the plan.

**completion_condition.** Run every C49-3 reorder context (`plan-B.md:144`) — the current centre-in-gap line against candidate place/extent/weight/blue on `/shop/member-list` and `/lab/tests/reorder-flow`, the remeasured 16 px short-item tick, the degenerate arm EG49-3 licensed, and the `n / N` readout against an honest non-visual-count form — record the owner's exact ruling and the rejected alternatives in the owner-pass record and the owning backlog row; then execute C49-2's four-step sequence (`plan-B.md:133-136`): record, land fixed expectations RED-capable with `SHIPPED_OVERLAY_PROFILE` unchanged, promote only the ruled fields, then docs. Destination resolution, sibling population, `n / N` counting semantics and the request payload must not move (`plan-B.md:266`); if the owner's ruling changes which destination or members the engine names, stop and re-plan it as behaviour (`plan-B.md:272`).

**verification_path.**
- `plan-B.md:372-379` (EG49-3) — Playwright against `/shop/order-detail`, `/shop/member-list`, `/lab/tests/reorder-flow`; census `anchorEdge - neighbourEdge` with its sign for every adjacent member pair, running `4jpxin` explicitly; branch the collapse arm (exact zero only) and the overlap arm on what the census found.
- `plan-B.md:150` — `pnpm exec playwright test <exact-changed-spec> --project=design-view` for the 16 px remeasurement; expected result is a printed/attached rect record matching the backlog observation for the current arm before any candidate is judged.
- `plan-B.md:270` — G47-6 and painted-node coverage express the new contract with recorded RED mutations; the overlap arm discharged either on a shipped overlapping pair or on a synthetic `DropTable` row, "stated as such and never as a browser-verified overlap".
- `plan-B.md:339` (G49-1 O2) — after promotion, restore the family's pre-phase value in `SHIPPED_OVERLAY_PROFILE`; the promoted row must fail. Reject any O2 rewrite lacking its authorising owner-pass record entry.
- `plan-B.md:131`, `346` — exit-zero `pnpm test:e2e` on the contract-preparation, promotion **and** documentation commit trees; `plan-B.md:344` artifact identity; real `descvi:dev` smoke.

**invented.**
1. **Which file owns G47-6.** `plan-B.md:81` and `144` and `270` all require G47-6 to be amended; no line in the plan gives its path. I located it by grep, not by the plan.
2. **The mapping from ruling vocabulary to code.** C49-3 asks the owner for "place, extent, weight, blue" (`plan-B.md:144`); §2.2 exposes `REORDER_INDICATOR_THICKNESS_PX`, `REORDER_INDICATOR_EDGE_OFFSET_PX`, `REORDER_READOUT_POINTER_GAP_PX`, a 1 px radius literal, a colour literal and a member-union cross extent (`plan-B.md:81`). "Place" corresponds to no existing symbol. I mapped it to the edge offset plus a new side/centre selector; that is an architecture decision the plan does not make.
3. **The synthetic-overlap row's owner** — I assigned it to S49-1 so S49-2's live pass is not blocked on writing a unit test (see S49-1's `would_ask`).
4. **What "U9(E)'s honest sibling-oriented form" is.** `plan-B.md:144` says the panel compares `n / N` "with an honest non-visual-count form"; `plan-B.md:513` restates the question. No candidate string, and the plan explicitly forbids changing what the engine counts. The candidate text is mine.

**would_ask.**
- Who writes the synthetic overlapping `DropTable` row, and against which story's review boundary (`plan-B.md:270`, `349`, `377-378` vs `254`)?
- The plan records at `plan-B.md:81` that `reorder-paint.ts`'s docblock and its arithmetic **disagree** about the overlap case, and rules that "nothing in this phase settles that". EG49-3's unexpected-result clause (`plan-B.md:379`) says a stale case-(b) attribution "is recorded as a finding against `reorder-paint.ts` rather than repaired by this phase". I would ask whether the owner accepts shipping a promotion into a function whose own docblock is known-false, or wants the docblock corrected in this story's docs commit.

**one_round: split** — but only after the owner session; it is not dispatchable before it.
- Files in scope: **~7** (2 given source/spec + 3 doc records + ≥2 inferred test files).
- Distinct acceptance claims in the done-when (`plan-B.md:270`): **8**.
- Gates to implement and drive RED: **2** amended (G47-6, painted-node coverage) plus G49-1's O2 rewrite with its own restore-the-old-value RED.
- Evidence gates to run: **1** (EG49-3, a three-route browser census with a per-pair sign record).
- Split along C49-2's own commit boundaries (`plan-B.md:131-136`): the ruling-record commit is one sitting with the owner; contract-preparation with its REDs is a second; promotion + docs a third. Each needs its own exit-zero `pnpm test:e2e` (`plan-B.md:131`), which alone makes one sitting implausible.

**reading_cost: ~43 lines.** Sections: S49-2 `260-272` (13); C49-2 `125-138` + the measurement note `150` (15); C49-3 reorder row `144` (1); §2.2 reorder rows `81, 85` (2); EG49-3 `372-379` (8); gate rows `339, 342, 344, 346` (4); U49-2 `513` (1). The reorder row at `plan-B.md:81` is a single source line of about 2,400 characters.

---

## S49-3 — decide and promote selection-ring treatment

**title.** Close `selection-ring-treatment` without conflating selected and hover rings or absorbing KI-47.

**scope** — *thinnest in the plan; mostly inferred*. Given at `plan-B.md:278`: comparison profile/controls; `use-selection-rings.ts`; "selection/hover tests"; visual spec; backlog and tracker records — with no path for any test file and no path prefix on the source file.

*Inferred by me*: `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts`; and from `plan-B.md:82` the test owners `selection-ring-pool.test.tsx`, `OverlayShell-selection-indicator.test.tsx`, and unnamed "hover tests". `plan-B.md:145` also names "hover direct-DOM effect" and `use-canvas-hover-ring.ts` is not mentioned anywhere in the plan despite existing in the tree — I added it to scope.

**completion_condition.** Run the selected/hover comparison in both themes on primary and pooled selection with independently adjustable rounding, widths and hover outset, labelling selected 2.5 px against hover 1.5 px and showing whether hover is larger than selection (`plan-B.md:145`, `280`); record the owner ruling on radius, selected width, hover width and the hover-versus-selection size relation; add the currently-absent ring-form clause to the visual spec; promote through **the single `applyRingStyle` path** and the hover effect so primary and pooled rings stay style-identical. KI-47 stays unchanged and routed (`plan-B.md:286`).

**verification_path.**
- `plan-B.md:284` — primary and pooled selected rings style-identical; a mutation that forks the pooled style is RED; a mutation that swaps selected and hover widths is RED.
- `plan-B.md:145` — the §2.2 regeneration command (`plan-B.md:67-75`) re-run to confirm the labelled current values, including the four `hoverRing` extent writes that `plan-B.md:77` says a border-and-radius-only pattern would miss.
- `plan-B.md:339` (G49-1 O2), `plan-B.md:342` (G49-4 — cannot promote while the family reads `pending`), `plan-B.md:346` (exit-zero `pnpm test:e2e` per commit tree), `plan-B.md:344` artifact identity.

**invented.**
1. **Where the ring-form clause goes in the spec.** `plan-B.md:145` calls for "the visual spec's new ring-form clause" and the kickoff's own input note says the ring's form is deliberately absent from §5. No section number is given anywhere. Choosing where a new contract clause lands in `.omc/specs/v3-layout-panel-visual-spec.md` is a contract decision, not an editorial one, and it is mine.
2. **Whether the hover ring's four arithmetic extent writes become a named constant.** `plan-B.md:77` establishes that the 2 px outset is "not a named constant and not a border or radius: it is four arithmetic geometry writes"; `plan-B.md:82` says the seam "must centralise them without changing the off-mode output" — but that centralisation is S49-1's, and whether the *promoted* value ships as a new exported constant or stays inline is unstated. It matters, because `scripts/check-handle-constants.mjs` sets the precedent that shipped geometry constants get cross-checked.
3. **The test files.** Three of the four are named only by informal label (`plan-B.md:278`).

**would_ask.** None blocking. The ambiguities above are cheap to settle in review, and `plan-B.md:286` gives a clean stop rule for the one thing that could pull this story out of scope (any colour/theme refresh request → KI-47).

**one_round: yes**, after the ruling — this is the smallest promotion story in the plan.
- Files in scope: **~7**.
- Distinct acceptance claims in the done-when (`plan-B.md:284`): **5**.
- Gates to implement and drive RED: **2** named mutations (fork the pooled style; swap selected and hover widths), plus G49-1's O2 rewrite.
- Evidence gates to run: **0** — no EG is required before S49-3.
- Caveat: C49-2 still requires the record / contract-preparation / promotion / docs commits to be separate with an exit-zero `pnpm test:e2e` each (`plan-B.md:131-136`). "One sitting" holds only if that is read as four commits in one worker's session rather than four review rounds.

**reading_cost: ~35 lines.** Sections: S49-3 `274-286` (13); C49-2 `125-138` (14); C49-3 ring row `145` (1); §2.2 ring row `82` and the writer note `87` (2); the regeneration command `64-77` (14, of which the worker needs `67-75`); gate rows `339, 342, 346` (3); U49-3 `514` (1). Overlaps heavily with S49-2's read; if the same worker takes both, C49-2 and the gate rows are read once.

---

## S49-4 — decide and promote the spacing mark and reveal policy

**title.** Close the non-delay part of `spacing-affordance-mark`; inhabit `delegated-mark`.

**scope** — *given, and given in more detail than any other story*, at `plan-B.md:292`: comparison profile/controls; `use-spacing-affordances.ts` with the two per-root writers cited by anchor (`root.setAttribute(SPACING_GLYPH_HIDDEN_BELOW_ATTR, …)` and `glyph.style.display = Math.min(rect.width, rect.height) >= SPACING_GLYPH_PX ? …`); any hover/reveal owner module; the S49-1-landed delegated arms in `e2e/resize-handles.spec.ts`, `e2e/spacing-gesture.spec.ts` and `resize-handle-layer.test.tsx`; the three further G44-5 universe-B legs at named anchors; the two further spacing homes (the conditional-arm population filter and the F10 row); the two spacing-family kind pins in `use-resize-handles.ts` and `OverlayShell.tsx`; spacing unit/browser coverage; visual spec; owner-pass record, backlog, tracker.

*Inferred by me*: "any hover/reveal owner module" — the reveal trigger changes from band hover to inside-object hover, and no module is named. `use-canvas-hover-ring.ts` and `use-spacing-affordances.ts`'s own hover path are the candidates; the plan does not choose.

**completion_condition.** Record the owner's ruling on reveal trigger, exact outer width and height, computed fill, outline width and outline colour in both themes, with the delay explicitly left held and no value (`plan-B.md:298`), and cardinality recorded as **CONFIRMED against the kickoff direction rather than chosen** (`plan-B.md:154`, `298`). Then, in one contract-preparation commit: move G44-5 universe B's family-kind pin (i) to `delegated-mark`, retire the size-term leg (ii) and the inhabitation pair (iii) **in the same commit that removes the per-root glyph and its `data-v3-glyph-hidden-below` writer**, each with its named successor and demonstrated RED (`plan-B.md:183-184`, `191`); re-scope the conditional-arm checker's four clean readings as plant-only (`plan-B.md:188`); retire the F10 row with the per-root glyph it describes (`plan-B.md:189`); re-point G46-3, G46-2 and — **only if EG49-5 found a spacing population** — G42-7 Universe B onto the inhabited population (`plan-B.md:294`, `300`). Then promote: exactly one non-operable `data-dsh-spacing-mark` node per `SpacingAffordance`, every strip/apron root still present, operable, same rect and role, declaring `delegated-mark` and publishing `data-v3-mark-owner` (`plan-B.md:156`). Hit rectangles, apron behaviour, gestures and write output unchanged. If the story does not promote at all, its terminal action is to **revert S49-1 commit (c) as one unit** (`plan-B.md:304`).

**verification_path.**
- `plan-B.md:298` — eight recorded RED controls: duplicate-mark, missing-mark, changed-operability, +1 px dimension, removed/altered outline, swapped paint, the replacement reveal leg's wrong-visibility mutation, the replacement inhabitation pair's one-answer-everywhere mutation.
- `plan-B.md:343` (G49-5) — the duplicate/missing/operability trio planted at G42-7 Universe B as well as in the spacing spec, "regardless of what EG49-5 found".
- `plan-B.md:150` — `pnpm exec playwright test <exact-changed-spec> --project=design-view` capturing candidate outer dimensions, computed fill, outline width and outline colour in both themes.
- `plan-B.md:342` (G49-4) — the validator must reject a `recorded` S49-4 section missing outline colour, naming family and field; promotion forbidden while the section reads `pending`.
- `plan-B.md:300`, `346` — exit-zero `pnpm test:e2e` on the contract-preparation, promotion and documentation trees; `plan-B.md:344` artifact identity; G49-1 O2.

**invented.**
1. **Where the mark node is appended.** `plan-B.md:156` fixes the mark's attributes, `pointer-events: none`, and its non-operability, but never its host. `base/.omc/specs/v3-layout-panel-visual-spec.md:62` shows this is safe either way — G46-1's subject is *operable* nodes and unmarked non-hittable children of `#dsh-ring-layer` sit outside the marked universe by construction — but that reasoning is mine, from the spec, not from the plan.
2. **Whether the mark itself carries a marker.** Follows from (1) and the same spec line; the plan is silent.
3. **The reveal owner module** (see scope). Whichever module owns inside-object hover detection has to be found and possibly created; the plan says "any hover/reveal owner module" (`plan-B.md:292`) and lets it stand.
4. **The successor legs' assertion text.** `plan-B.md:191` branches correctly on U49-4 — if size-conditional hiding survives, the term is published by the mark and the leg asserts equality against the mark's visibility and "the affordance's governing dimension". **Which dimension governs a gap band versus a padding edge is not stated**, and it is not the same quantity as `Math.min(rect.width, rect.height)` once ownership moves off the root. That is an acceptance-semantics decision I had to make.
5. **The generalisation from "per edge" to "per `SpacingAffordance`".** `plan-B.md:154` names this as the plan's own inference and invites the owner to reject it — so this is *disclosed*, not hidden, but it is still a material decision a worker inherits rather than derives.

**would_ask.**
- Confirm the C49-4 generalisation before the live pass, since `plan-B.md:154` and `515` both say rejecting it "reopens C49-4 rather than answering U49-4" — i.e. rejection after the pass invalidates the story rather than adjusting it. This is the one question in the plan that is cheaper to ask before the session than after.
- Which module owns inside-object reveal (`plan-B.md:292`)?

**one_round: split** — the plan labels it SMALL, and by its own contents it is not.
- Files in scope: **~14** named at `plan-B.md:292`, several of them touched at three or four separate anchors within the same file.
- Distinct acceptance claims in the done-when (`plan-B.md:298-300`): **13** — five ruling fields recorded in both themes, delay held, cardinality confirmed-not-chosen, exactly-one-mark-per-affordance, every root present/operable/same rect/same role, the four-value contract inhabited in the spec and every hand-written home, fixed LOOK expectations, plus the five-leg disposition itemised individually, plus the EG49-5-conditional G42-7 branch.
- Gates to implement or amend and drive RED: **6 gate rows** (G44-5 universe B, G42-7 Universe B, G46-2, G46-3, the F10 row, the conditional-arm checker) carrying **8 named RED mutations** (`plan-B.md:298`), three of which must additionally be planted at the layer-wide universe (`plan-B.md:343`).
- Evidence gates to run: **1** (EG49-5), which must have run before S49-1 (c) — so by S49-4 it is a read of a recorded result, and the story branches on it (`plan-B.md:300`).
- Split into: **(4a)** the owner ruling record; **(4b)** contract preparation — the five-leg disposition, the two further homes, the re-pointed arms, all eight REDs, default unchanged; **(4c)** promotion — the per-root glyph removal, the mark writer, the kind pins in `use-resize-handles.ts` and `OverlayShell.tsx`; **(4d)** spec and closure docs. (4b) alone is a full sitting: `plan-B.md:183-184` requires two retirements to land *in the same commit as the code removal*, which forces (4b) and (4c) to be jointly designed even though they are separate commits — that coupling is the single hardest thing in this plan to execute correctly, and I would give it a named reviewer up front.

**reading_cost: ~110 lines** (≈ 320 screen lines). Sections: S49-4 `288-304` (17); **all of C49-4 `152-195` (44)**; C49-3 spacing row `146` and the measurement note `150` (2); §2.2 spacing row `84` (1); C49-2 `125-138` (14); EG49-5 `390-399` (10); gate rows `339, 342, 343, 344, 346` (5); pre-mortem S3 `417-422` (6); risk rows `492, 494, 495` (3); U49-4 `515` (1); the S49-1 (c) revert unit `252` (1). C49-4 is unavoidable and is the densest block in the document.

---

## S49-5 — decide and promote the padding glyph

**title.** Close `padding-glyph`: arrow-to-line → plain directional bar.

**scope** — *given, thinly*, at `plan-B.md:310`: comparison profile/controls; `use-spacing-affordances.ts`; spacing browser coverage; visual spec; backlog and tracker records.

*Inferred by me*: the concrete symbol is `SPACING_GLYPH_PATHS` "or its delegated-mark successor" (`plan-B.md:147`); "spacing browser coverage" resolves to `e2e/spacing-gesture.spec.ts`, which the plan never names in this story despite naming it eight times in S49-4.

**completion_condition.** Compare the current pad arrow-to-line against a plain axis-aligned bar in both orientations on pad affordances in `/lab/tests/spacing-nesting` (`plan-B.md:147`, `312`); record the ruling on the final pad figure and its dimensions; change **only** the pad figure path/selection and its fixed visual expectation. If S49-4 promoted delegated ownership, paint the chosen figure on the sole mark keyed to each pad affordance and do **not** restore copies inside the strip or aprons; if it did not, the baseline stays the per-root pad glyph. The gap mark's selected figure, one-mark cardinality, delegated ownership, hit roots and gesture behaviour remain fixed (`plan-B.md:147`, `316`).

**verification_path.**
- `plan-B.md:316` — the gap affordance's figure and cardinality unchanged by this story; pad mark orientation matches the selected edge under whichever ownership form S49-4 ruled; no pad figure duplicated across strip/apron roots; a **swapped-orientation mutation is RED**; focused checks plus `pnpm test:e2e` on every commit tree.
- `plan-B.md:342` (G49-4) — the S49-5 family section must be `recorded` with its fields before promotion.
- `plan-B.md:339` (G49-1 O2), `plan-B.md:344` artifact identity.

**invented.**
1. **The branch resolution.** `plan-B.md:312` makes S49-5's baseline conditional on whether S49-4 promoted — but `plan-B.md:314` lists S49-5's dependency as **S49-1 only**, and `plan-B.md:503` says S49-5 "consumes S49-4's ownership ruling when the delegated form is promoted". So S49-5 is formally independent of S49-4 while being materially dependent on it. I sequenced S49-5 strictly after S49-4's promotion or its stop branch; the plan permits the other reading, in which S49-5 would ship a figure into a per-root glyph that S49-4 then deletes.
2. **The bar's geometry.** `plan-B.md:516` (U49-5) asks for "the plain directional bar, and at what ruled dimensions" — but `plan-B.md:146` already fixes the *mark's* outer dimensions as an S49-4 field (12–13 px × 2 px with a 1 px outline). Whether S49-5's "dimensions" are a second, independent set for the pad figure inside that mark, or the same numbers restated, is unresolved. I read them as the figure's path geometry within S49-4's ruled outer box.
3. **Which spec section moves** (`plan-B.md:147` says "the visual spec move" with no target).

**would_ask.**
- Is S49-5 blocked on S49-4's promotion, or genuinely parallel (`plan-B.md:312` vs `314` vs `503`)? Dispatching both in parallel risks S49-5 editing code S49-4 removes.
- Are U49-5's "ruled dimensions" distinct from U49-4's outer dimensions (`plan-B.md:146` vs `516`)?

**one_round: yes**, after the ruling and after S49-4 resolves.
- Files in scope: **~5**.
- Distinct acceptance claims in the done-when (`plan-B.md:316`): **5**.
- Gates to implement and drive RED: **1** (the swapped-orientation mutation), plus G49-1's O2 rewrite for this family.
- Evidence gates to run: **0**.
- The only thing that would force a split is the branch in item 1 above; resolved, this is one worker, one sitting, one review.

**reading_cost: ~34 lines.** Sections: S49-5 `306-318` (13); C49-3 pad row `147` and the measurement note `150` (2); §2.2 spacing row `84` (1); C49-2 `125-138` (14); gate rows `339, 342, 346` (3); U49-5 `516` (1). If S49-4's outcome must be understood first, add C49-4's `154-156` and `189` (4).

---

## S49-R — compare and, only if ruled, split the reorder arming threshold

**title.** phase-47 U3, conditional rider.

**scope** — *given* at `plan-B.md:324`: comparison profile/controls; `use-reorder-drag.ts`; `use-canvas-selection-shield.ts` and its coverage in `canvas-selection-shield-travel.test.tsx` and `e2e/multi-select-shield.spec.ts`; `pointer-thresholds.ts` **only after a split ruling**; G47-3 tests; `e2e/reorder-drag.spec.ts` row (g); relevant browser coverage; owner-pass record and backlog/tracker record. §2.2 (`plan-B.md:85`) gives all three threshold sites by anchor and gives G47-3's file as `packages/descvi/test/reorder/reorder-drag-machine.test.ts`.

*Inferred by me*: nothing material. This is the best-scoped story in the plan.

**completion_condition.** Resolve one reorder-only preview/default value reaching all three §2.2 sites — the `ReorderDragMachine` constructor, the outside-machine N > 1 mute travel comparison, and the shield's release suppression **press-scoped only**, via the handoff S49-1 (b) landed (`plan-B.md:326`). Demonstrate at least two distinct values, one below and one above the shared 4 px, moving the eligible machine boundary, the mute-refusal onset and the release suppression **together**, with an ordinary sub-threshold click still selecting and a post-threshold N > 1 selection still standing at both values (`plan-B.md:330`). If the owner keeps the shared value, record and stop. If the owner splits, introduce a separately named reorder default and rewrite G47-3, `e2e/reorder-drag.spec.ts` row (g) and the shield's reorder-press rows to bind all three boundaries to it, leaving resize, spacing floors and every shield gesture reorder did not classify on `POINTER_DRAG_THRESHOLD_PX`.

**verification_path.**
- `plan-B.md:381-388` (EG49-4) — hold `POINTER_DRAG_THRESHOLD_PX` fixed; run at two candidate values releasing below, at and above each candidate boundary; run spacing-floor and resize-threshold controls throughout; then **two single-consumer reconnection mutations**, each leaving the machine on the preview value: reconnect the mute comparison to the shared constant (the mute-vs-machine equality row must go RED), then reconnect the shield's press-scoped resolution (the release-suppression row must go RED).
- `plan-B.md:330` — if split, a mutation of the reorder constant moves all three reorder boundaries while spacing floors, resize thresholds and non-reorder shield gestures stay fixed and green.
- `plan-B.md:386` — alternate path: if the shield cannot be reached press-scoped without varying its guard for Shift and N > 1 gestures, **leave U3 routed and remove S49-R** rather than splitting implicitly.
- `plan-B.md:342` (G49-4), `plan-B.md:346` (`pnpm test:e2e` per commit tree).

**invented.** None material. The three sites are given by anchor (`plan-B.md:85`), the failure mode this story exists to catch is named explicitly (`plan-B.md:326`: "a preview below the shared value paints refusal before the trailing click is suppressed, and a preview above it suppresses a click that never travelled far enough to be a drag — and both leave every threshold gate green"), the isolation mutations are specified per consumer, the abandonment condition is stated, and the split's blast radius is enumerated file by file at `plan-B.md:148`. This is the one story where an empty `invented` list is the honest answer.

**would_ask.** None. `plan-B.md:332` covers the one out-of-scope request (changing the general pointer threshold → new owner-approved plan) and `plan-B.md:386` covers the one technical failure.

**one_round: split**, on the branch.
- Files in scope: **~8** if kept (record + backlog + tracker + the preview wiring), **~9** if split.
- Distinct acceptance claims in the done-when (`plan-B.md:330`): **7**.
- Gates to implement and drive RED: **2 isolation mutations** guaranteed, plus, if split, G47-3's source-binding and boundary rows, `e2e/reorder-drag.spec.ts` row (g), `e2e/multi-select-shield.spec.ts` and `canvas-selection-shield-travel.test.tsx` rewritten with fixed behavioural boundary oracles — **5 more**.
- Evidence gates to run: **1** (EG49-4, two candidate values × three release points × three consumers × two reconnection mutations = 20 recorded observations).
- Split: **(Ra)** the EG49-4 evidence run and the ruling record — one sitting; **(Rb)** the split implementation, only if U49-6 says split. The keep branch ends at (Ra) and is genuinely one round.

**reading_cost: ~42 lines.** Sections: S49-R `320-332` (13); C49-3 threshold row `148` (1); §2.2 threshold row `85` (1); D49-3 rows `33-34` (2); EG49-4 `381-388` (8); pre-mortem S5/S6 `431-443` (13); gate rows `342, 346` (2); U49-6 `517` (1); S49-1 (b) `251` (1). Pre-mortem S6 duplicates most of EG49-4; a worker who reads EG49-4 can skip it, taking the real cost to ~29.

---

# Closing

## Dispatch state today

| Story | Dispatch | Reason |
|---|---|---|
| **S49-0** | **Today, no question** | Scope, destination, closure-scan form, both RED controls, the anchor-count command and the exact CI step names are all in the text (`plan-B.md:203-234`). My four invented items are all worker-level derivations from repository evidence. |
| **S49-1** | **Today, with one question** | The blocker is not the architecture — that is settled at `plan-B.md:117-123` — but the boundary of commit (c): whether widening the closed set at `e2e/spacing-gesture.spec.ts` (`plan-B.md:166`, `246`) reaches the family-kind pin one line below it that `plan-B.md:182` reserves for S49-4. Commits (a) and (b) are dispatchable today with no question at all. |
| **S49-2** | **Not until the owner session** | Every shipped value is U49-2 (`plan-B.md:513`). EG49-3's browser census (`plan-B.md:372-379`) *is* dispatchable today and should be, since `plan-B.md:378` says S49-1 needs its answer. |
| **S49-3** | **Not until the owner session** | U49-3 (`plan-B.md:514`). After the ruling, dispatchable with no question. |
| **S49-4** | **Not until the owner session, and one question before it** | U49-4 (`plan-B.md:515`), plus the C49-4 generalisation confirmation, which `plan-B.md:154` says must be asked *before* the pass, not after. |
| **S49-5** | **Not until the owner session, and one question** | U49-5, plus the S49-4 sequencing contradiction (`plan-B.md:312` vs `314` vs `503`). |
| **S49-R** | **Not until the owner session** | U49-6 (`plan-B.md:517`). EG49-4 (`plan-B.md:381-388`) is dispatchable today and produces the evidence the session needs. |

Reading that table as a schedule: three units of work are dispatchable this morning — S49-0, S49-1 (a)+(b), and the two evidence gates EG49-3 and EG49-5 — and everything else queues behind one owner session.

## Material decisions parked for the owner

| Ref | Line | What is parked | Can a worker proceed without it? |
|---|---|---|---|
| U49-1 / D49-1 | `509` | **Answered** — the owner ruled D49-1(b) on 2026-09-04. | Yes. But `plan-B.md:3`'s final sentence still says "Not executable until the owner approves D49-1", contradicting the same paragraph. See the wasted-work section. |
| U49-2 | `513` | Reorder place, extent, weight, blue; keep `n / N` or adopt U9(E). | No for S49-2's promotion. Yes for EG49-3 and for S49-1's reorder profile slice, which ships defaults only. |
| U49-3 | `514` | Selected radius/weight, hover weight, hover-vs-selection extent relation. | No for S49-3. Yes for S49-1. |
| U49-4 | `515` | Spacing reveal trigger, outer width/height, fill, outline width and colour per theme. Delay explicitly **held**, not asked. | No for S49-4's promotion. Yes for S49-1 (c), which lands the vocabulary uninhabited precisely so the candidate is legal before the ruling exists (`plan-B.md:129`). |
| C49-4 generalisation | `154`, `515` | "One `-` mark per edge" generalised to one mark per `SpacingAffordance` — the plan's own inference, disclosed. | **No, and this one is different from the others**: `plan-B.md:515` says an owner who reads it otherwise "reopens C49-4 rather than answering U49-4", so a late rejection invalidates S49-1 (c) as well as S49-4. This should be asked before the session, not in it. |
| U49-5 | `516` | Pad figure and its ruled dimensions. | No for S49-5. |
| U49-6 | `517` | Keep the shared threshold or split reorder, and at what value. | No for S49-R's split branch. Yes for EG49-4 and the preview wiring. |
| The `reorder-paint.ts` docblock/arithmetic conflict | `81`, `379` | The plan records that the docblock's overlap case and the function disagree, rules that "nothing in this phase settles that", and files a stale attribution as a finding rather than a repair. | Yes — but S49-2 promotes into that function, so the owner should be told the docblock will still be false after the phase closes. |
| EG49-1 stop condition | `358` | If `.omc/archive/260817-e3-v3/` has appeared since the plan was written, "two v3 archive directories is an owner-visible question, not an implementer's pick". | Yes today — I verified it is absent in `base/.omc/archive/` (the directory list holds `260817-e3-v3-consensus/` and `260901-e3-v3/`, no `260817-e3-v3/`). |
| EG49-5 result | `396`, `300` | Whether G42-7's delegated arm is ever exercised on a shipped root. | Yes — the plan writes the arm and its plants either way (`plan-B.md:474`) and only the coverage *claim* branches. This is a model of how to park a fact without parking the work. |

## Wasted work a worker would do

1. **`plan-B.md:3` contradicts itself in its own last sentence, and the contradiction points at "do not start".** The paragraph announces "U49-1 is since answered — the owner ruled D49-1(b) on 2026-09-04" and then closes with "Not executable until the owner approves D49-1; S49-2 through S49-R deliberately contain later live-decision checkpoints whose answers must be recorded before any shipped default moves." That closing sentence is also a near-verbatim duplicate of the sentence immediately before it. An executor who reads line 3 top-to-bottom and stops at the last clause concludes the plan is blocked. This is the single highest-cost line in the document and the cheapest to fix.

2. **`plan-B.md:3` is otherwise addressed to reviewers, not executors.** The review hash, the "REVISE, not PASS" disposition, the consensus-gate reasoning, and the four recorded findings are a record of how the plan was approved. Three of the four findings describe defects *still present in the text below* — the plant locations, the leg-(i) widening reading, and the three-owner synthetic-overlap row — which means an executor who skips line 3 as process metadata loses the only warning that those three ambiguities exist, while one who reads it gets a paragraph of consensus bookkeeping to reach them. The findings belong in the stories they affect.

3. **`plan-B.md:221`'s rationale is false against the repository.** It states that `check-v3-registers.mjs` "is the one audit gate in `.github/workflows/ci.yml` with no selftest step". `base/.github/workflows/ci.yml` shows **four** audit gates with no selftest step: KI register consistency (line 169), V3 register identity (line 176), session migration (line 179), and extract outcome (line 187). The *conclusion* — add two steps rather than one — is correct and is independently supported by the two precedents the same paragraph cites (ci.yml:216-218 and 231-233, the latter carrying the "a STEP rather than a flag someone can forget" ruling verbatim). But a worker who checks the claim, as this plan's own culture demands, spends the time and finds it wrong. Line 3 already records this as an unfixed finding.

4. **"Record an exit-zero `pnpm test:e2e` on every commit tree" is restated ten times** — `131`, `136`, `248`, `270`, `298`, `300`, `316`, `346`, `349`, `503`. It is a phase-wide rule stated once at `131` and then re-derived per story. Each restatement is a line a worker reads and cannot act on differently.

5. **C49-4's five-leg disposition is restated four times.** The enumeration lives at `plan-B.md:180-184`, then reappears in S49-4's affected locations (`292`), S49-4's required behaviour (`294`), S49-4's done-when (`298`), pre-mortem S3 (`419-421`) and consequences (`473`). The restatements are not identical — `292` names anchors, `298` names outcomes, `419` names catches — so a worker cannot skip any of them without risking a divergence, and must read all six to be sure they agree. This is the largest reading tax in the plan and it falls on its heaviest story.

6. **G49-6 (`plan-B.md:344`) guards an artifact no story changes.** Three separate lines assert `.descvi/screens.json` cannot move (`43`, `256`, `427`), and D49-1(b) was chosen partly to guarantee it. The gate's RED-when is "a controlled temporary artifact edit" — a mutation manufactured solely to prove a gate can fail about a file the phase does not touch. Defensible as a regression guard against an accidental screen; still, it is a demonstrated RED with no subject, and it is charged to every story via `plan-B.md:270`, `298` and `316`.

7. **Pre-mortem S6 (`plan-B.md:438-443`) restates EG49-4 (`381-388`) with no new content.** Same three consumers, same two reconnection mutations, same press-scope rationale. 13 lines a S49-R worker reads twice.

8. **The §2.2 regeneration command (`plan-B.md:67-75`) plus its 3-line justification (`77`) is read in full by S49-3, which needs two of its twelve constants.** The justification is genuinely load-bearing for the hover-extent case, but it sits in the shared evidence section where every story pays for it.

## One structural observation

The plan is unusually honest about what it does not know — EG49-3, EG49-5, the docblock/arithmetic conflict, the C49-4 generalisation and the terminal-uninhabited-kind exit at `plan-B.md:304` are all cases where it names an unmeasured fact, branches the work on the answer, and refuses to assert coverage it has not earned. That discipline is what makes S49-R's `invented` list legitimately empty and S49-0's nearly so. The cost lands entirely on S49-1 (c) and S49-4, where the same discipline produces a 44-line contract (C49-4) restated across six locations and a "SMALL" story carrying 13 acceptance claims and 8 RED controls. The sizing labels at `plan-B.md:42-48` are wrong for S49-4 specifically: it is the second-largest story in the plan and is labelled SMALL alongside S49-5, which has 5 files and 1 mutation.
