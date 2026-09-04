# Execution ledger — plan-B.md (phase-49)

Lead's reading: seven stories (S49-0, S49-1, S49-2, S49-3, S49-4, S49-5, S49-R), `plan-B.md:197–333`. Every citation below is `plan-B.md:<line>` unless a `base/` path is given.

---

## S49-0 — close the records before source work

**scope** — Given, and unusually complete (`203`): `docs/e3/tracker.md` (the v3 CLOSE section and its deferred-archiving paragraph); `.omc/plans/ralplan-e3-v3-direct-manipulation.md`; `.omc/plans/ralplan-phase-42-resize-handles.md`; `.omc/archive/260901-e3-v3/`; `.omc/archive/README.md`; every tracked file returned by the two-target `git grep` at `103`; `docs/e3/phase-49-owner-pass-record.md`; `scripts/check-owner-pass-record.mjs`; the `verify` job in `.github/workflows/ci.yml`.
Inferred by me: the *content* of the phase-48 tracker section. The plan says "the same idiom as phase-47" (`232`) and names the story ids S48-0a/0b/1/2/3/4/5 (`205`), which routes to `base/docs/e3/tracker.md` rather than to the plan; the per-story text itself is mine to write.
Inferred by me: the field vocabulary of `scripts/check-owner-pass-record.mjs` for four of the five families — see `invented` #1.

**completion_condition** — The two v3 plan paths (`ralplan-e3-v3-direct-manipulation.md`, `ralplan-phase-42-resize-handles.md`) exist only under `.omc/archive/260901-e3-v3/`, with zero references to their old paths anywhere in the indexed tree *or* the non-ignored working tree, `.omc/plans` and `.omc/archive` included; the other three files in `.omc/plans/` have not moved and no second v3 archive directory exists (`232`). `docs/e3/tracker.md` gains a phase-48 routing note plus a per-story record for S48-0a…S48-5, and its deferred-archiving paragraph no longer names `260817-e3-v3` or the "34 references" count, amended in the same commit as the move (`205`, `207`, `232`). `.omc/archive/README.md` gains a `260901-e3-v3/` row (`205`, `109`). `docs/e3/phase-49-owner-pass-record.md` exists with all five families at `status: pending`; `scripts/check-owner-pass-record.mjs` exists with a `--selftest` covering three failure shapes; both are wired into the CI `verify` job as two separate steps in the order and shape at `224–227` (`219`, `221`, `232`). The commit message and the tracker record name the 168 code anchors (136 + 32) the move removes from the citation gate's scan roots, with the regeneration command at `212–215` re-run rather than the number carried (`209`, `232`). `node scripts/check-citation-anchors.mjs`, `node scripts/check-owner-pass-record.mjs --selftest`, and `node scripts/check-owner-pass-record.mjs` all exit zero (`232`).

**verification_path**
- `git grep --untracked -n -E '\.omc/plans/(ralplan-e3-v3-direct-manipulation|ralplan-phase-42-resize-handles)\.md' -- .` prints nothing (`105`, `338`).
- `git ls-files .omc/archive/260901-e3-v3/` lists the two moved plans beside phase-43/44/45/47 and `spike-handles/`; `ls -d .omc/archive/260817-e3-v3` still reports no such path (`232`).
- RED control 1: with the targets moved on disk and unstaged, plant one old-path reference *inside a moved destination*; the `--untracked` scan must name file and line while plain `git grep` names nothing; restore byte-identically (`234`, `338`).
- RED control 2: the pre-existing old-path reference in `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` must be named by the scan before it is updated (`234`, `338`).
- Validator RED: delete a required field from a `recorded` family section; the validator exits non-zero naming family and field (`234`, `342`).
- `node scripts/check-citation-anchors.mjs --selftest` and the gate itself exit zero; manual section-link review of every changed markdown target, because `.md` anchors are skipped at `base/scripts/check-citation-anchors.mjs` (`111`, `347`).
- EG49-1's five censuses re-run immediately before editing (`356`).

**invented**
1. **The validator's field vocabulary for S49-2, S49-3, S49-5 and S49-R.** The plan specifies the required fields for exactly one family: "for S49-4 those fields include outer width, outer height, computed fill, outline width, and outline colour in both themes, plus the explicitly held delay" (`219`). G49-4 then states the general list — "routes, themes, orientations, selected alternatives, rejected alternatives, measured values, and held questions" (`342`) — but the script is required to be "a hardcoded field vocabulary rather than a count" (`219`), so a concrete per-family list has to exist in code and only one exists on the page. I would set S49-2 = {routes, themes, place, extent, weight, blue, readout-form}, S49-3 = {routes, themes, radius, selected width, hover width, hover-vs-selection relation}, S49-5 = {routes, themes, orientations, figure, dimensions}, S49-R = {routes, values tried, keep-or-split, chosen value}, drawn from `144–148` and `513–517`. This is my construction, not the plan's.
2. **The per-story text of the phase-48 tracker section.** "Compact per-story record" and "linking to the phase-48 plan and close handoff rather than duplicating their substance" (`205`) fixes the shape but not what each of the seven rows says. I would take each row's one-line claim from the phase-48 close handoff.
3. **The archive destination is a plan-level override of the owner's own instruction.** The kickoff (`base/docs/handoff/260903-phase-49-kickoff.md:22`) and the tracker both name `.omc/archive/260817-e3-v3/`; the plan rejects that as stale and rules `260901-e3-v3/` (`32`, `107`), then edits the tracker to say so while deliberately leaving the kickoff untouched (`207`). The evidence is sound — I confirmed `.omc/archive/260817-e3-v3/` is absent and `260901-e3-v3/` holds the phase-43/44/45/47 set — but "owner approval of this plan is the ruling" is claimed only for D49-1 (`28`), never for D49-2's destination. Overwriting an owner-written instruction sentence is a decision I would want signed, not inferred.
4. **Whether the record + validator + CI wiring belongs in this story at all.** The plan bundles a docs/archive move with a new gate script and a CI change under one SMALL label (`42`, `219`). Nothing in the plan makes them one unit; I am choosing to keep them together only because the plan's sequencing sentence (`503`) needs the record to exist before the live session.

**would_ask**
- Which fields must each of S49-2, S49-3, S49-5 and S49-R declare when `recorded`? (`219` gives only S49-4.)
- Does the owner accept `260901-e3-v3/` as the destination and accept that S49-0 rewrites the tracker sentence they wrote? (`32`, `107`, `207` vs kickoff `:22`.)
- `221` asserts `check-v3-registers.mjs` is "the one audit gate in `.github/workflows/ci.yml` with no selftest step". It is not: `base/.github/workflows/ci.yml:169` (KI register), `:176` (V3 registers), `:179` (session migration) and `:187` (extract outcome) all lack one. The prescription at `224–227` is unaffected, but the plan's own status paragraph already recorded this as an unfixed finding (`3`) and the false sentence is still on the page. Confirm the two-step shape is still wanted.

**one_round** — **split.** Files in scope: 4 named files + 2 moves + 1 destination dir + 1 README + 1 CI workflow + "every tracked file returned by the two-target grep", which §2.5 measures at **47 tracked files / 90 occurrences** (`103`). Distinct acceptance claims in the done-when at `232`: I count 13 (zero old refs in two universes; new paths exist; one v3 directory; retained files unmoved; tracker paragraph amended in the same commit; README row; phase-48 section; record with five `pending`; coverage loss recorded with count and command; commit message names the anchor loss; both CI steps present; `pnpm gates` runs both; three commands exit zero). Gates the story must implement and drive RED: 1 new gate (G49-4) with 3 selftest shapes plus 1 file-level RED, plus 2 closure-scan RED controls (`234`). Evidence gates to run: 1 (EG49-1, five commands, `356`).
Split I would take: **S49-0a** = the archive move + reference rewrite + tracker amendment + README row + closure-scan RED controls; **S49-0b** = the phase-48 tracker section; **S49-0c** = the owner-pass record, its validator, its `--selftest`, and the two CI steps. 0c is a new gate script with its own RED obligations and shares no file with 0a; bundling them means a validator defect blocks a 47-file reference rewrite.

**reading_cost** — ~118 lines. S49-0 (`199–237`, 39) + §2.5 measured blast radius (`101–112`, 12) + the D49-2 and destination rows of the options table (`30–32`, 3) + §1 scope row (`42`, 1) + EG49-1 (`353–361`, 9) + gates G49-0, G49-4, G49-9 (`338`, `342`, `347`, 3) + the risk rows on markdown targets and the closure scan (`497–498`, 2) + the sequencing paragraph (`503`, 1). Realistically also the status paragraph (`3`) and §0 options table (`23–37`) before an executor trusts the destination override: +18.

---

## S49-1 — build the real comparison surface without moving a pixel by default

**scope** — Given at `242`, broad: new modules under `packages/descvi/src/react/overlay/comparison/`; `OverlayShell.tsx`; `toolbar/OverlayToolbar.tsx`; "applicable painter modules under `.../canvas/`" including `use-canvas-selection-shield.ts`; focused tests under `.../overlay/__tests__/` (`canvas-selection-shield-travel.test.tsx`, `resize-handle-layer.test.tsx`) and `packages/descvi/test/reorder/`; the five closed-kind-set homes enumerated at `164–168`; the two closed-set restatement homes at `172`; the spec KIND table (`174`); `delegated-mark` arms in `e2e/resize-handles.spec.ts`, `e2e/spacing-gesture.spec.ts`, `e2e/multi-select-shield.spec.ts`, `e2e/reorder-drag.spec.ts`; `e2e/fixtures/expected-identities.json` only if a collected row is added.
Inferred by me: which files under `comparison/` exist and what they are called (`117` names the two exported symbols, not the modules). "Applicable painter modules" (`242`) resolves to four by way of §2.2's table (`79–88`): `reorder-paint.ts`, `use-selection-rings.ts`, `use-spacing-affordances.ts`, `use-reorder-drag.ts` — my resolution, not the plan's list.

**completion_condition** — One `OverlayComparisonProfile` type and one `SHIPPED_OVERLAY_PROFILE` value exist under `packages/descvi/src/react/overlay/comparison/`, with four independently resettable families (reorder paint/readout, selection/hover rings, spacing marks/reveal, reorder threshold), containing inputs only and creating no DOM (`117`). The existing painters remain the only DOM writers, accept their profile slice, default to the shipped profile, and emit byte-equivalent inline styles and geometry when comparison is inactive (`119`). A toolbar toggle opens a chrome panel outside `#dsh-screen` and `#dsh-ring-layer`, labels Baseline and Candidate, displays every active value, is keyboard reachable, uses bilingual labels, survives route navigation within the overlay session, and resets in one action; nothing is written to source, storage, sidecar or manifest (`117`, `244`). The story lands as three independently revertible commits (`250–252`): (a) profile + seams + surface, pixel-neutral; (b) the press-scoped shield handoff resolving to `POINTER_DRAG_THRESHOLD_PX` for every press reorder did not classify, gesture-neutral; (c) the `delegated-mark` vocabulary added to the five closed sets, both restatement homes, the spec KIND table and four positive-obligation arms, with the production population **uninhabited** and every new arm exercised on plants (`123`, `246`). No `src/app/**` or `.descvi/screens.json` content changes (`256`).

**verification_path**
- Focused Vitest: profile defaults/reset/immutability; shell+toolbar visibility, keyboard access, state retention, reset; direct-DOM tests that each family reads the candidate profile (`256`, `349`).
- G49-1 O1: fixed pre-seam expectations per family, compared with comparison inactive and after Reset (`339`, `366`). RED-when: change one shipped-profile value while leaving the expectations untouched — the family row must fail (`339`).
- G49-2 RED-when: disconnect one profile prop at a hook/painter boundary; the control stays interactive but the real node fails (`340`).
- G49-3: `node scripts/check-handle-constants.mjs --selftest` and the gate; RED-when: alias candidate state to the shipped object and mutate it (`341`).
- The shield's five existing release cases and the reorder mute row stay green with the handoff resolving to the shared constant (`256`, `366`).
- Each of the three C49-4 mutations (cloned mark, removed mark, flipped operability) shown RED against a plant, including at G42-7 Universe B (`195`, `343`).
- EG49-2 before (a) and (b); EG49-5 before (c) (`254`), EG49-5 run as `pnpm exec playwright test e2e/resize-handles.spec.ts --project=design-view` with the mandatory non-zero control on the padded G48-6b scene (`394–395`).
- `pnpm test:e2e` exit zero on each of the three commit trees (`248`); a real `descvi:dev` smoke changing each family once and resetting (`256`).

**invented**
1. **Whether S49-1 adds a collected Playwright row, and therefore whether it moves the identity golden.** `242` says "browser coverage only where jsdom cannot prove the live context" and `e2e/fixtures/expected-identities.json` "only if a collected row is added"; §2.3 (`95`) says only "should prefer extending a relevant collected spec only if the behavior cannot be proved in focused package tests plus an explicit smoke". The done-when (`256`) requires a real `descvi:dev` smoke but names no browser row. Whoever executes decides, and the decision moves a reviewed golden. I would decide: no new collected row in S49-1; the smoke plus jsdom carry it.
2. **Who owns the synthetic overlapping `DropTable` row.** Three owners are named for the same artifact: EG49-3's alternate path says it is "added to `packages/descvi/test/reorder/reorder-paint-geometry.test.ts`" (`377`); the expanded test plan assigns it to the same file (`349`); S49-2's done-when requires it discharged (`270`); and `378` says "the separation census itself runs early enough that S49-1 knows whether it owes the synthetic overlap row" — while S49-1's dependency line (`254`) names only EG49-2 and EG49-5, never EG49-3. The plan's own status paragraph records this as an unfixed finding (`3`). I would put the row in S49-2 and add EG49-3 to S49-1's dependencies only as a read.
3. **The panel's control set per family.** `117` fixes the spacing slice's fields exactly (ownership form, outer width, outer height, fill, outline width, outline colour, figure, reveal trigger) and nothing else's. For reorder, rings and threshold I must derive the controls from C49-3's "required live comparison" column (`144–148`) — place/extent/weight/blue and readout form; radius/selected width/hover width/hover outset; one numeric value — which is a specification of what the owner must be shown, not of what the panel exposes.
4. **What "bilingual user-facing labels" (`244`) means in practice** — which strings, and whether the existing toolbar has a precedent to copy. The plan names none.
5. **Where the G44-5 B2 and G42-7 plants live.** `123` gives the precedent (`resize-handle-layer.test.tsx`'s uninhabited-`glyph` plant row) and `158` says the G42-7 mutations are "planted at that row rather than only in the spacing spec", but no file/row is named for the B2 plants. Recorded as an open finding at `3` and still open.
6. **Whether commit (c) may proceed if EG49-5's control fails.** `395` makes the non-zero control on the G48-6b padded scene "mandatory", and `396` says a zero at G42-7 counts only after the control returned non-zero — but no branch is written for a control that itself returns zero. I would treat that as a hard stop.

**would_ask**
- Does S49-1 own the synthetic overlap row or does S49-2? (`349` / `377` / `270` / `254`.)
- Is a new collected browser row authorised in S49-1, given it moves `e2e/fixtures/expected-identities.json` by design (`95`, `242`)?
- Which file holds the G44-5 B2 plants (`3`, `123`)?
- `170` states the `glyph-conditional` grep "returns five production sentences beyond the two test files". Run against `base/packages/descvi/src` it returns **eight** production hits, four of them in `use-spacing-affordances.ts` (`:97`, `:99`, `:101`, and `:103`, the `SPACING_GLYPH_CONTROL_KIND = "glyph-conditional"` constant that is the sole production writer of the attribute). The plan's instrument ("dispose of every hit", `170`) self-heals, but its stated count does not match, and the plan never says whether the constant is a closed-set restatement (S49-1) or a spacing-family kind pin (S49-4). I read it as a kind pin → S49-4, and would confirm.

**one_round** — **no; split, and the plan already draws the seam.** Files in scope: I count ≥ 20 named files or file groups at `242`, across production overlay code, four painter modules, three test directories, four e2e specs and one golden. Distinct acceptance claims in the done-when (`256`): 9. Gates the story must implement and drive RED: G49-1 (two RED arms), G49-2, G49-3, G49-5 (three mark mutations planted at two universes) — 4 gates, ≥ 6 RED demonstrations. Evidence gates to run: 2 (EG49-2, EG49-5), plus EG49-3's census if the overlap-row ownership resolves here. The plan itself calls it LARGE (`43`) and prescribes three commit boundaries (`248`).
Split: **(a)** profile + `SHIPPED_OVERLAY_PROFILE` + painter seams + toolbar toggle + panel, gated by EG49-2 and G49-1 O1 / G49-2 / G49-3; **(b)** the press-scoped shield handoff, gated by the shield's five release cases and the reorder mute row; **(c)** the `delegated-mark` vocabulary landing, gated by EG49-5 and the three planted mutations at both universes. (a) is still the largest of the three and is where a second review round is most likely; I would accept it as one worker's sitting only because every seam is pixel-neutral and O1 makes drift visible.

**reading_cost** — ~185 lines. S49-1 (`238–259`, 22) + C49-1 (`115–124`, 10) + C49-2 (`125–139`, 15) + C49-4 (`152–196`, 45) + §2.1 (`56–61`, 6) + §2.2 (`62–88`, 27) + §2.3 (`89–96`, 8) + §2.4 (`97–100`, 4) + DR49-2 (`20`, 1) + §1 scope row (`43`, 1) + gates G49-1/2/3/5/6/8 (`339–346`, 6) + expanded test plan (`349`, 1) + EG49-2 (`362–371`, 10) + EG49-5 (`390–399`, 10) + pre-mortem S1/S2/S3 (`403–422`, 20) + the three relevant risk rows (`491–495`, 5). C49-4 alone is 45 lines and only its vocabulary half is this story's.

---

## S49-2 — decide and promote reorder indicator/readout treatment

**scope** — Given at `264`: comparison profile/controls; `packages/descvi/src/react/overlay/canvas/reorder-paint.ts`; reorder geometry and paint tests; "relevant e2e spec/golden if collected coverage changes"; `docs/post-loop-backlog.md`; `.omc/specs/v3-layout-panel-visual-spec.md`; `docs/e3/tracker.md`. Inferred: which reorder test files — §2.2 names `reorder-paint.test.tsx`, `packages/descvi/test/reorder/reorder-paint-geometry.test.ts` and G47-6 (`81`), so those; and `docs/e3/phase-49-owner-pass-record.md`, which the story's done-when needs but its scope line omits.

**completion_condition** — Every C49-3 reorder context is run live on `/shop/member-list` and `/lab/tests/reorder-flow`; the owner's exact ruling on place, cross-axis extent, weight, blue and U9(E)'s readout form is recorded with the alternatives rejected (`144`, `266`); then, in that order, a contract-preparation commit lands fixed expectations with `SHIPPED_OVERLAY_PROFILE` unchanged and each new leg shown RED by a named mutation and restored byte-identically, and a promotion commit moves only the ruled fields into `SHIPPED_OVERLAY_PROFILE` and `reorder-paint.ts` with no gate-scope change (`131–136`). The live-pass record carries the short-item observation, the exact-contact collapse arm discharged by whichever path EG49-3 licensed, and the overlap arm recorded as the separation *sign* EG49-3 measured — from a shipped overlapping pair if one exists, otherwise at unit level on a synthetic overlapping `DropTable`, stated as such and never as a browser-verified overlap (`270`). Destination resolution, sibling population, `n / N` counting semantics (presentation aside) and the request payload are unchanged (`266`). Reset and comparison-off resolve to the promoted default; G47-6 and painted-node coverage express the new contract with recorded RED mutations (`270`).

**verification_path**
- EG49-3 first: Playwright against `/shop/order-detail`, `/shop/member-list`, `/lab/tests/reorder-flow` reading member rects, indicator rect and readout presence during the live gesture; per adjacent pair record `anchorEdge - neighbourEdge` with its sign, run explicitly on `4jpxin` (`375`).
- G49-1 O2 for the reorder family: after promotion, restore the pre-phase value in `SHIPPED_OVERLAY_PROFILE`; the promoted row must fail (`339`).
- G49-5: the story-specific swapped-width / disconnected-profile / wrong-extent mutations RED before promotion; contract-preparation commit changes no default pixel (`343`).
- G49-4: the S49-2 section of `docs/e3/phase-49-owner-pass-record.md` flips to `recorded` with its fields present; `node scripts/check-owner-pass-record.mjs` exits zero (`342`).
- `pnpm exec playwright test <exact-changed-spec> --project=design-view` for the measurement, then `pnpm test:e2e` exit zero on the contract-preparation, promotion and documentation trees (`150`, `136`); artifact identity via `git diff --exit-code .descvi/screens.json` (`344`); real `descvi:dev` smoke (`270`).

**invented**
1. **Which of two readings of the overlap case the executor may cite as truth.** §2.2 records that `reorder-paint.ts`'s docblock says an overlapping pair collapses the band to the boundary midpoint while the arithmetic (`Math.abs` on the separation, then the clamp) yields a positive thickness up to 2 px, and rules that "nothing in this phase settles that" (`81`). The story must still show the owner *something* on that arm and record it. I read the instruction as: report the pixels the shipped function produces, cite neither half of the prose as a ruling (`376`), and file the docblock's stale case-(b) subject attribution as a finding against `reorder-paint.ts` (`379`). That reading is mine; the plan states the conflict without naming which artifact the executor writes the finding into.
2. **Whether U9(E) is one ruling or two.** `144` bundles "keep/change of the visual-count claim" into the same pass as place/extent/weight/blue, and `513` bundles them into one open question U49-2. The readout form is a text change with its own coverage; the indicator is paint. I would record them as two fields under one section rather than one field.
3. **The synthetic `DropTable` row's ownership** (see S49-1 `invented` #2). If S49-1 did not add it, this story does, and it is not in this story's affected-locations list (`264`).

**would_ask**
- Is EG49-3's census a precondition of S49-1 or of this story? (`254` vs `378`.) A worker dispatched on S49-2 alone may find the census unrun.
- Where does the finding against `reorder-paint.ts`'s stale case-(b) attribution get recorded (`379`)?

**one_round** — **yes, for the post-ruling half only; the story as written is not one sitting.** Files in scope: 7 named + 2 inferred. Distinct acceptance claims in the done-when (`270`): 8. Gates to implement and drive RED: G49-5's reorder mutations and G49-1's O2 rewrite with its restore-the-old-value RED — 2 gates, ≥ 3 REDs, plus G47-6 and painted-node coverage rewritten. Evidence gates: 1 (EG49-3). The blocker is not size but the owner live pass sitting in the middle of the story (`268`, "S49-1 and owner availability"): a worker cannot finish in one sitting because the story contains a synchronous human decision. Split I would take: **S49-2a** = EG49-3 census + live pass + ruling record (no source change); **S49-2b** = contract preparation + promotion + docs, three commits, one review round.

**reading_cost** — ~72 lines. S49-2 (`260–273`, 14) + C49-3 reorder row and its trailing note (`144`, `150`, 2) + §2.2 reorder and threshold rows (`79–88`, 10) + C49-2's promotion sequence (`125–139`, 15) + EG49-3 (`372–380`, 9) + gates G49-1/4/5/6/8 (`339–346`, 5) + U49-2 (`513`, 1) + §1 scope row (`44`, 1) + principle 3 and 4 (`13–14`, 2) + pre-mortem S2 (`410–415`, 6) + the O1/O2 risk row (`499`, 1) + sequencing (`503`, 1).

---

## S49-3 — decide and promote selection-ring treatment

**scope** — Given at `278`, and the thinnest scope line in the plan: "comparison profile/controls; `use-selection-rings.ts`; selection/hover tests; visual spec; backlog and tracker records." Inferred by me: "selection/hover tests" resolves via §2.2 (`82`) to `selection-ring-pool.test.tsx`, `OverlayShell-selection-indicator.test.tsx` and the hover tests; the owner-pass record is again omitted from scope but required by the done-when. I confirmed against `base/packages/descvi/src/react/overlay/canvas/use-selection-rings.ts:268–277` that the hover ring's four extent writes and its 1.5 px border live in that same file, so the one-file scope is correct and `use-canvas-hover-ring.ts` is not implicated.

**completion_condition** — The selected and hover rings are compared on the same target in both themes and on primary plus pooled selection, with independently adjustable rounding, widths and hover outset, labelled so selected 2.5 px is distinguishable from hover 1.5 px and so the hover-larger-than-selection relation is visible (`145`, `280`). The owner's ruling on radius, selected width, hover width and the hover-versus-selection size relation is recorded (`145`); then contract preparation adds the ring-form clause — currently absent from the spec, which is what makes this new scope — with RED controls, and promotion moves the values through the single `applyRingStyle` path and the hover direct-DOM effect (`145`, `280`). Primary and pooled selected rings stay style-identical; KI-47 is untouched and stays routed (`284`, `286`).

**verification_path**
- Focused Vitest: pooled/primary parity; a mutation that forks the pooled style is RED; a mutation that swaps selected and hover widths is RED (`284`).
- G49-1 O2 for the ring family: restore the pre-phase value after promotion; the row must fail (`339`).
- G49-4: the S49-3 record section reads `recorded` with its fields; validator exits zero (`342`).
- The §2.2 `rg` command at `67–75` re-run to regenerate the labelled current values before the pass (`145`).
- `pnpm test:e2e` exit zero on contract-preparation, promotion and documentation trees (`136`); artifact identity; real smoke (`346`, `344`).

**invented**
1. **What the ring-form clause in `.omc/specs/v3-layout-panel-visual-spec.md` says.** The plan establishes that §5 deliberately does not constrain the ring's form (kickoff `:45`; plan `145` calls it "the visual spec's new ring-form clause") but gives no clause text, no section number, and no statement of whether the clause binds hover and selected jointly or separately. Writing a spec clause is a contract act; I am inventing its shape.
2. **Whether "hover larger than selection" is a ruled invariant or a ruled value.** `145` asks the owner for "hover-versus-selection size relation" and the kickoff calls it "test Figma's hover-larger-than-selection relation" (`:33`). If the answer is a relation, the contract asserts an inequality; if it is a value, it asserts two numbers. The RED control differs. I would write it as an inequality plus both values.

**would_ask**
- Should the ring-form clause bind hover and selected in one contract or two, and where in `.omc/specs/v3-layout-panel-visual-spec.md` does it land? (`145`, `280`.)

**one_round** — **yes for the post-ruling half.** Files in scope: 1 production file + 3 test files + spec + 2 record docs = 7. Distinct acceptance claims (`284`): 5. Gates to implement and drive RED: 1 (G49-5's ring arm) with 2 named mutations, plus G49-1's O2 rewrite. Evidence gates: 0 — this is the only decision story with no EG of its own. The same live-pass split applies as S49-2, but the implementation half is genuinely small and I would dispatch it as one story.

**reading_cost** — ~50 lines. S49-3 (`274–287`, 14) + C49-3 ring row (`145`, 1) + §2.2 ring row and the 2.5/1.5 sentence (`82`, `87`, 2) + the regeneration command block (`64–77`, 14) + C49-2 (`125–139`, 15) + gates G49-1/4/5 (`339`, `342`, `343`, 3) + U49-3 (`514`, 1).

---

## S49-4 — decide and promote the spacing mark and reveal policy

**scope** — Given at `292`, the most explicit in the plan, down to individual assertion anchors: comparison profile/controls; `use-spacing-affordances.ts` including the two per-root writers whose removal licenses the retirements; "any hover/reveal owner module"; the delegated arms S49-1 landed in `e2e/resize-handles.spec.ts`, `e2e/spacing-gesture.spec.ts` and `resize-handle-layer.test.tsx`; the three further G44-5 universe-B legs (family-kind pin, size-term leg, inhabitation pair) at their named anchors; the conditional-arm checker's population filter and the F10 row; the two spacing-family kind pins (`use-resize-handles.ts#the layer is a CHILD of`, `OverlayShell.tsx#unaffected — it declares`); spacing unit/browser coverage; visual spec; owner-pass record, backlog, tracker.
Inferred by me: "any hover/reveal owner module" (`292`) — the hatch hover is delegated at the layer inside `use-spacing-affordances.ts` (`base/packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts:315`), so I read this as no additional file. Also inferred: `SPACING_GLYPH_CONTROL_KIND` at `base/.../use-spacing-affordances.ts:103` belongs here rather than in S49-1 (see S49-1 `would_ask`).

**completion_condition** — Candidate and promoted one-mark form are implemented through C49-4: one non-operable visual node per `SpacingAffordance` carrying `data-dsh-spacing-mark={affordance.id}`, `pointer-events: none` and the profile's ruled outer dimensions, fill, outline width and outline colour, while every strip and apron root keeps its rect, hit ownership and gesture role, contains no copied glyph, declares `data-v3-glyph-control="delegated-mark"` and publishes `data-v3-mark-owner={affordance.id}` (`156`). The owner ruling on reveal trigger, exact outer width and height, computed fill, outline width and outline colour in both themes is recorded, the delay explicitly left held with no value, and cardinality recorded as CONFIRMED against the kickoff direction rather than chosen here (`146`, `154`, `298`). In one contract-preparation commit: G44-5 universe B's family-kind pin moves to `delegated-mark` and the closed-set leg widens to four values; the published-size-term leg and the inhabitation pair retire in the same commit that removes the per-root glyph and its `data-v3-glyph-hidden-below` writer, each with a named replacement carrying a demonstrated RED; the conditional-arm checker's four clean readings are re-scoped as plant-only in the promotion commit; F10 retires with the per-root glyph it describes; G46-3 gains the delegated exact-one/non-operable arm and its `glyph-conditional` arm becomes production-uninhabited (`183–193`, `294`). G42-7 Universe B is re-pointed onto real roots only if EG49-5 found a spacing population; otherwise the arm stays planted and the story says so in those words (`294`, `300`). Hit rectangles, apron behavior, gestures and source-write output are unchanged (`294`).

**verification_path**
- EG49-5 (already run in S49-1) decides G42-7's leg (`300`, `390–399`).
- RED controls, all recorded: duplicate-mark, missing-mark, changed-operability (both directions), +1 px outer dimension, removed/altered 1 px outline, swapped fill/outline treatment, the replacement reveal leg's wrong-visibility mutation, and the replacement inhabitation pair's one-answer-everywhere mutation — restored byte-identically before the contract-preparation commit is accepted (`195`, `298`, `343`).
- The three mark mutations planted at G42-7 Universe B as well as in the spacing spec (`343`).
- Live browser record capturing candidate outer dimensions, computed fill, outline width and outline colour in both themes on `/lab/tests/spacing-nesting` (`146`).
- G49-4 validator on the S49-4 section, which is the one family whose required fields the plan actually enumerates (`219`, `342`).
- `pnpm test:e2e` exit zero on the contract-preparation, promotion and documentation trees (`300`).
- If no promotion: revert S49-1 commit (c) as one unit (`304`, `493`).

**invented**
1. **What replaces the retired legs, concretely.** `191` gives the *shape* of both replacements but branches them on an unanswered ruling: "if the owner's U49-4 reveal ruling keeps any size-conditional hiding, the term is published by the mark and the replacement leg asserts the same equality against the MARK's visibility and the affordance's governing dimension; if the ruling drops size-conditional hiding, the replacement is the reveal-trigger assertion the ruling names". Which of the two exists is not knowable before the live pass, so the contract-preparation commit cannot be written ahead of it. That is a decision the owner makes, but the *test design* for each branch is mine.
2. **What "the affordance's governing dimension" is** (`191`) for a gap band versus a padding edge. The retired per-root rule was `Math.min(rect.width, rect.height) >= SPACING_GLYPH_PX` on the root's own rect (`183`). The affordance's rect is not the root's rect, and the plan does not define the substitute.
3. **The generalisation from "per edge" to "one mark per `SpacingAffordance`"** is flagged by the plan itself as its own inference, not owner direction (`154`, `515`) — so a gap band gets one mark the way a padding edge does. I am carrying that inference forward; the plan explicitly invites the owner to reject it, which would reopen C49-4 rather than answer U49-4.
4. **Whether `SPACING_GLYPH_CONTROL_KIND` (`base/.../use-spacing-affordances.ts:103`) changes here or in S49-1.** C49-4's grep-derived home list (`172–176`) omits it; the plan's own status paragraph records the omission as a standing finding (`3`). By the plan's stated rule (a kind *pin* is falsified by promotion, not by vocabulary, `173`) it belongs here.

**would_ask**
- Which reveal branch at `191` should contract preparation be written against — is a stop-and-wait between the ruling and the contract commit acceptable, or should both branches be written and one discarded?
- What is "the affordance's governing dimension" for a gap band (`191`)?
- Does the owner accept the "per edge" → "per `SpacingAffordance`" generalisation (`154`), given the plan flags it as reopenable?

**one_round** — **no; split.** Files in scope: 1 production module (with 2 named writers removed), 4 test/spec files touched at 9 distinct named anchors (`292`), plus visual spec, owner-pass record, backlog and tracker = 9 files, 9 anchors. Distinct acceptance claims in the done-when (`298`, `300`): 12 — the five-field ruling record, cardinality-as-confirmed, exactly-one-mark-per-affordance, root presence/operability/rect/role, four-value kind inhabited in spec and in every hand-written home, LOOK expectations matching the ruling, the five-leg disposition of G44-5 universe B, the eight named RED controls, G42-7's conditional leg, exit-zero on three trees. Gates to implement and drive RED: G49-5 plus the amended G44-5 B2, G46-2, G46-3, G42-7 Universe B and the two successor legs — 6 gate surfaces, **8 distinct RED demonstrations** (`298`). Evidence gates: 1 (EG49-5, run upstream).
This is labelled SMALL at `46` and it is not. Split I would take: **S49-4a** = live pass + ruling record; **S49-4b** = contract preparation — the G44-5 five-leg disposition, the two retirements with their named replacements, the F10 retirement, the conditional-checker re-scoping, all eight REDs — with `SHIPPED_OVERLAY_PROFILE` unchanged; **S49-4c** = promotion + kind pins + spec + docs. 4b alone carries more RED obligations than S49-1 commit (c).

**reading_cost** — ~150 lines. S49-4 (`288–305`, 18) + C49-4 in full (`152–196`, 45) + C49-3 spacing row (`146`, 1) + C49-2 (`125–139`, 15) + DR49-2's transitional-member clause (`20`, 1) + §2.2 spacing row (`84`, 1) + §1 scope row (`46`, 1) + EG49-5 (`390–399`, 10) + gates G49-4/G49-5/G49-8 (`342`, `343`, `346`, 3) + expanded test plan (`349`, 1) + pre-mortem S3 (`417–422`, 6) + risk rows on delegated marks, retirement, and terminal vocabulary (`492–495`, 4) + U49-4 (`515`, 1) + ADR consequence on the vocabulary (`473–474`, 2). C49-4 is unavoidable and is 45 lines of contract for one SMALL-labelled story.

---

## S49-5 — decide and promote the padding glyph

**scope** — Given at `310`: comparison profile/controls; `use-spacing-affordances.ts`; spacing browser coverage; visual spec; backlog and tracker records. Inferred: `SPACING_GLYPH_PATHS` "or its delegated-mark successor" (`147`) is the concrete symbol; the owner-pass record is again omitted from scope but required by G49-4.

**completion_condition** — The current pad arrow-to-line figure is compared with a plain axis-aligned bar in both orientations on pad affordances at `/lab/tests/spacing-nesting`; the owner's ruling on final pad figure and its dimensions is recorded; then only the pad figure path/selection and its fixed visual expectation change (`147`, `312`). If S49-4 promoted delegated ownership, the chosen figure is painted by the single mark keyed to each pad affordance and is not copied into the strip or aprons (`147`, `312`). The gap mark's selected figure, one-mark cardinality, delegated ownership, hit roots and gesture behavior are unchanged by this story (`147`, `316`).

**verification_path**
- A swapped-orientation mutation is RED (`316`).
- No pad figure duplicated across strip/apron roots (`316`).
- G49-5's "wrong glyph orientation" mutation (`343`); G49-1 O2 for this family (`339`).
- `pnpm test:e2e` exit zero on every commit tree; focused spacing browser coverage (`316`).

**invented**
1. **The baseline this story compares against depends on S49-4's outcome, and the plan gives no order.** `147` says "Before an S49-4 promotion the baseline is the per-root pad glyph; if S49-4 promotes delegated ownership, the chosen pad figure is painted by the sole mark", and `314` says S49-5 "may share one owner session with S49-4 but remains independently reviewable and revertible" while `503` sequences S49-5 after S49-4. If S49-4 stops before promotion and reverts S49-1 (c) (`304`), S49-5's implementation target changes underneath it. I would gate S49-5 on S49-4's promotion landing or its revert, whichever happens, and say so in the brief.
2. **Whether "and at what ruled dimensions" (`516`) is a separate field from S49-4's outer width/height.** If the delegated form ships, the pad *mark* dimensions were already ruled in S49-4 and the figure's own dimensions are a different thing. The plan does not disambiguate.

**would_ask**
- Is S49-5 dispatchable before S49-4's promotion or revert is known? (`147`, `314`, `503`.)
- Are the pad figure's ruled dimensions distinct from S49-4's ruled mark dimensions? (`147`, `515`, `516`.)

**one_round** — **yes.** Files in scope: 1 production module + spacing browser coverage + spec + 2 record docs = 5. Distinct acceptance claims (`316`): 5. Gates to implement and drive RED: 1 (the orientation mutation), plus G49-1's O2 rewrite. Evidence gates: 0. Genuinely the smallest story, and the only one I would dispatch as written once its dependency question is answered.

**reading_cost** — ~48 lines. S49-5 (`306–319`, 14) + C49-3 pad row (`147`, 1) + C49-2 (`125–139`, 15) + §2.2 spacing row (`84`, 1) + §1 scope row (`47`, 1) + gates G49-1/5 (`339`, `343`, 2) + U49-5 (`516`, 1) + C49-4's delegated ownership rule if S49-4 promoted (`156`, 1) + sequencing (`503`, 1). If the executor has to determine whether the delegated form shipped, add C49-4 in full (+45).

---

## S49-R — compare and, only if ruled, split reorder arming threshold

**scope** — Given at `324`: comparison profile/controls; `use-reorder-drag.ts`; `use-canvas-selection-shield.ts` and its coverage in `canvas-selection-shield-travel.test.tsx` and `e2e/multi-select-shield.spec.ts`; `pointer-thresholds.ts` **only after a split ruling**; G47-3 tests (`packages/descvi/test/reorder/reorder-drag-machine.test.ts`, per `85`); `e2e/reorder-drag.spec.ts` row (g); relevant browser coverage; owner-pass record and backlog/tracker.

**completion_condition** — One reorder-only runtime preview value resolves to all three sites §2.2 names — `ReorderDragMachine`'s constructor, the outside-machine multi-selection mute comparison, and the selection shield's release suppression through S49-1's press-scoped handoff (`326`). Comparison mode demonstrates at least two distinct values, one below and one above the shared 4 px, moving the eligible machine boundary, the N > 1 mute-refusal onset and the release suppression *together*, without changing the shared symbol, with an ordinary sub-threshold click still selecting and a post-threshold N > 1 selection still standing at both values (`330`). The owner ruling is recorded (`330`). If the owner keeps the shared value: record and stop, only the ruling record moves (`148`, `326`). If the owner splits: a separately named reorder default is introduced; resize, spacing floors and every shield gesture reorder did not classify stay on `POINTER_DRAG_THRESHOLD_PX`; G47-3, `e2e/reorder-drag.spec.ts` row (g) and the shield's reorder-press rows bind all three reorder boundaries to the new value with fixed behavioral boundary oracles (`326`, `148`).

**verification_path**
- EG49-4 first, at two candidate values with release below, at and above each candidate boundary (`384`).
- Two single-consumer reconnection mutations, each leaving the machine on the preview value: reconnecting the mute comparison makes the mute-vs-machine equality row RED; reconnecting the shield's press-scoped resolution makes the release-suppression row RED. Spacing-floor, resize-threshold and non-reorder shield controls stay green under both (`330`, `384`).
- If split: a mutation of the reorder constant moves all three reorder boundaries while spacing floors, resize thresholds and non-reorder shield gestures stay fixed and green (`330`).
- `pnpm test:e2e` exit zero on each commit tree; G49-4 on the S49-R record section (`342`).

**invented**
1. **The mechanism of the press-scoped handoff** is specified by intent, not shape: "gives the shield an effective threshold for the press reorder classification has just seen, and resolves to `POINTER_DRAG_THRESHOLD_PX` for every press reorder did not classify" (`121`, `246`). Whether that is a ref, an event payload, or a value passed at press start is mine — though it lands in S49-1 (b), not here, so it is S49-1's invention that this story inherits.
2. **What "a separately named reorder default" is called and where it lives.** `326` says `pointer-thresholds.ts` moves "only after a split ruling"; the constant's name is not given, and G47-3 currently pins behavior "against the shared symbol" (`85`), so the rewrite has to choose what the gate binds to.
3. **Whether this rider runs at all.** `48` marks it "SMALL, conditional"; `34` says "Chosen conditionally"; EG49-4's alternate path (`386`) says that if the shield cannot be reached press-scoped, "leave U3 routed and remove S49-R rather than splitting implicitly". A lead has to decide whether to hold a worker for it. I would dispatch S49-R's evidence half only after EG49-4 passes.

**would_ask**
- If EG49-4 fails its isolation arm, does removing S49-R also mean reverting S49-1 commit (b)? `252` says reverting (b) "costs only S49-R's rider, which is conditional anyway", but no story is told to do it. The plan writes a revert branch for (c) (`304`, `493`) and writes none for (b).
- What is the reorder-only constant's name and home on a split ruling (`326`)?

**one_round** — **yes if kept, split if ruled.** Files in scope: 5 named + 1 conditional (`pointer-thresholds.ts`) + 2 record docs. Distinct acceptance claims (`330`): 5. Gates to implement and drive RED: G47-3's rewrite plus 2 isolation mutations plus, on a split, 1 constant-mutation control — up to 4 REDs. Evidence gates: 1 (EG49-4, and it is the heaviest of the five: two candidate values × three release points × three consumers). The keep branch is a record commit and is trivially one round; the split branch touches a shared constant and four gate files and is a second story.

**reading_cost** — ~72 lines. S49-R (`320–333`, 14) + C49-3 threshold row (`148`, 1) + §2.2 threshold row (`85`, 1) + EG49-4 (`381–389`, 9) + C49-1's handoff paragraph (`121`, 1) + S49-1's (b) commit (`251`, 1) + C49-2 (`125–139`, 15) + D49-3 options rows (`33–34`, 2) + pre-mortem S5/S6 (`431–443`, 13) + gates G49-4/8 (`342`, `346`, 2) + U49-6 (`517`, 1) + §1 scope row (`48`, 1).

---

## Closing

### Dispatch state today

| Story | Dispatch | Why |
|---|---|---|
| S49-0 | **With one question** | Validator field vocabulary exists for one family only (`219`); the destination override of an owner-written instruction (`207`) wants a signature. Everything else is measured and executable. |
| S49-1 | **Not as written** | Three unrelated changes under one story (`250–252`), ≥ 20 files, 4 gates, 2 evidence gates. Dispatchable as (a)/(b)/(c) once the EG49-3-ownership and plant-location questions are answered. |
| S49-2 | **Evidence half yes, promotion half after the ruling** | Contains a synchronous owner decision mid-story (`268`). EG49-3's placement is ambiguous (`254` vs `378`). |
| S49-3 | **Evidence half yes; promotion half with one question** | Only the spec clause's shape is unspecified (`145`). Smallest risk surface of the four decision stories. |
| S49-4 | **No** | Labelled SMALL (`46`) but carries 8 RED demonstrations, 6 gate surfaces, 9 named anchors and a contract-preparation commit whose *design* branches on an unanswered ruling (`191`). |
| S49-5 | **Yes, after S49-4 resolves** | Its baseline is defined by S49-4's outcome (`147`) and its dependency line does not say so (`314`). |
| S49-R | **Only after EG49-4** | Conditional by construction (`34`, `386`); the keep branch is a record commit, the split branch is a second story. |

### Material decisions parked for the owner

| Decision | Lines | Can a worker proceed without the answer? |
|---|---|---|
| U49-2 — reorder place/extent/weight/blue and the `n / N` readout form | `513`, `144` | Yes up to the live pass; no past it. S49-2's contract-preparation commit cannot be written. |
| U49-3 — ring radius, selected/hover weight, hover-vs-selection relation | `514`, `145` | Same. Additionally the spec's ring-form clause has no draft. |
| U49-4 — spacing reveal trigger, outer dimensions, fill, outline; delay held | `515`, `146` | **No, beyond the live pass — and the branch reaches further than the values.** `191` makes the *identity of the replacement legs* depend on the ruling, so even the test design for S49-4b is unwritable in advance. |
| U49-5 — pad figure and its dimensions | `516`, `147` | Yes up to the pass. |
| U49-6 — keep or split the reorder threshold | `517`, `148` | Yes; the whole rider is conditional on it and EG49-4 runs first. |
| The `SpacingAffordance`-level generalisation of "one mark per edge" | `154`, `515` | Yes for the candidate; an owner rejection reopens C49-4 rather than answering U49-4, which is a plan amendment, not a worker decision. |
| The `260817-e3-v3` → `260901-e3-v3` destination override and the tracker rewrite | `32`, `107`, `207`, kickoff `:22` | Technically yes — the evidence is measured and EG49-1 re-runs it (`358`). But it edits an owner-written instruction, so I would not dispatch it silently. |
| The reorder overlap case: docblock vs arithmetic | `81`, `376`, `379` | Yes — the plan rules that nothing here settles it and that the pass reports pixels, not a reconciliation. But no destination is named for the finding against `reorder-paint.ts`. |
| The spacing reveal delay | `154`, `302`, `515` | Yes; explicitly held and excluded from the shipped profile. |

### Text that would make a worker do wasted work

**Addressed to reviewers rather than executors.**
- `3` — the whole status paragraph: a review hash, a consensus-gate disposition, four unresolved findings, and a self-contradiction. It opens "Nothing blocks execution on this question" (via `509`) and closes "**Not executable until the owner approves D49-1**". A worker reading top-down learns first that the plan is approved and then that it is not executable. The stale sentence should be gone.
- `93` — "The phrase '62 gate failures' appears in no tracked document and is not used as evidence." A rebuttal to a review claim; it tells an executor nothing to do.
- `77` — 11 lines justifying why the §2.2 regeneration command uses a third `rg` alternative scoped to `hoverRing` rather than to any `.style.top` writer. The command at `67–75` is already runnable; the justification is for a critic.
- `105` — the demonstration that `git grep --untracked` can see this very plan file. Correct and load-bearing as a *method*, but it is then restated as an executable control in EG49-1 (`356`) and again as G49-0's RED arm (`338`) and again in the risk table (`498`). One statement plus one control would do.
- `176` — "What does NOT move is [the G49-2 CONTROL row]… rewriting it would be coverage loss." Useful as a guard, but written as a defence of a choice.

**Repeated constraints.**
- The `delegated-mark` kind-set story is stated in full at `46` (§1), `121–123` (C49-1), `146` (C49-3), `152–196` (C49-4), `242`/`246`/`252` (S49-1), `292–304` (S49-4), `419–422` (pre-mortem S3), `473–474` (ADR), and `492–493` (risks) — **nine** passes over the same contract. C49-4 is the authority; the rest re-derive it and a worker cannot tell which restatement is normative.
- "`pnpm test:e2e` exits zero on every commit tree, contract-preparation and documentation trees included" appears at `52`, `131`, `136`, `248`, `300`, `316`, `346` and `503` — **eight** times.
- The five-value/four-value closed-set enumeration appears at `164–168`, `242`, `246`, `294`, `421`, `473` and `493`.
- The instruction to re-derive numbers by re-running rather than by arithmetic appears at `103`, `107`, `209`, `358` and `498`.

**Gates guarding things no story changes.**
- **G49-3** (`341`) claims candidate changes do not mutate `DEFAULT_HANDLE_GEOMETRY`, and runs `check-handle-constants.mjs`. But `83` already rules that the comparison surface "must not override this record in S49-1", `43` puts resize geometry out of S49-1's ships-list, and no story anywhere touches the record. Its RED-when (`341`) is about profile aliasing, not about handle geometry — so the gate's stated subject and its RED control are different things, and the handle-constants half is a standing gate re-run under a new name.
- **G49-6** (`344`) requires re-running the extractor and `git diff --exit-code .descvi/screens.json` on a plan that ships no `src/app/**` change by construction (`43`, `50`, `256`, `427`). Cheap once, but `346`/`503` make the per-commit-tree discipline apply across ~15 commits.
- **G49-1's O1 oracle** (`339`) is written to expire at the first promotion and is stated four times as expiring (`339`, `365`, `256`, `499`). For S49-3, S49-4, S49-5 and S49-R the O1 arm is dead the moment S49-2 promotes, yet each of those stories' done-when still routes through G49-1.

**A factual error a worker would trip on.**
- `221` — "`check-v3-registers.mjs` … is the one audit gate in `.github/workflows/ci.yml` with no selftest step". Four gates lack one: `base/.github/workflows/ci.yml:169`, `:176`, `:179`, `:187`. The plan's own status paragraph already lists this as an unfixed finding (`3`); leaving the sentence in means an executor who checks it finds the plan wrong about the repository at the exact point where it is telling them to follow a precedent.
- `170` — "that command returns five production sentences beyond the two test files". It returns **eight** production hits over `base/packages/descvi/src`; the four in `use-spacing-affordances.ts` (`:97`, `:99`, `:101`, `:103`) are unlisted, and `:103` is `SPACING_GLYPH_CONTROL_KIND`, the only production writer of the attribute. The plan's instrument ("dispose of every hit") recovers, but an executor who trusts the count will believe they have over-collected.
