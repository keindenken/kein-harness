# Execution ledger — plan-A.md

Nine stories are defined: S49-0, S49-P, S49-1a, S49-1, S49-2, S49-3, S49-4, S49-5, S49-6 (`plan-A.md:308–514`). Execution order at `plan-A.md:39`.

One finding governs three of the entries below and is stated once here rather than repeated in each. **The plan cites four gate scripts by path as if they were committed files — `scripts/gate-g49-2-archive-pointers.sh`, `scripts/gate-g49-3-look-witnesses.sh`, `scripts/gate-g49-4-override-leak.sh`, `scripts/gate-g49-5-one-home.sh` (`plan-A.md:6`, `:199`, `:520`, `:590`) — and none of them exists in the tree.** `base/scripts/` holds `check-citation-anchors.mjs`, `check-handle-constants.mjs`, `check-v3-registers.mjs` and nine others; `ls base/scripts/gate-g49*` matches nothing. The plan gives each script's legs, exit codes, allow-list predicate, precondition, selftest assertion names and pasted transcripts, but never a line of its source. So the workers on S49-0, S49-1a and S49-1 must each *write* the gate the plan describes and then reproduce the transcript the plan already published for it. The plan's own thesis — "a gate that lives in prose is re-implemented by every reader; a gate that lives in `scripts/` is the same bytes every time" (`plan-A.md:1189`) — describes exactly the position an executor is put in. This is the largest single block of invented work in the phase, and it is invisible in every story's Lands line, which reads "IS COMMITTED BY THIS STORY" (`plan-A.md:317`, `:369`, `:414`) as though the file were being moved rather than authored.

---

## S49-0 — the v3.5 close (docs only)

**scope.** Given by the plan (`plan-A.md:310–330`):
- `docs/e3/tracker.md` (phase-48 section added; v3 CLOSE archiving paragraph replaced)
- `git mv .omc/plans/ralplan-e3-v3-direct-manipulation.md .omc/plans/ralplan-phase-42-resize-handles.md .omc/archive/260901-e3-v3/`
- `.omc/archive/README.md` (two pointer rewrites + a new `260901-e3-v3/` row)
- `docs/architecture.md`, `docs/known-issues.md`, `.omc/research/phase48-strip-band-pricing.md`, `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` (one pointer each)
- `scripts/gate-g49-2-archive-pointers.sh` (new)
- `.github/workflows/ci.yml` (two steps, `plan-A.md:319–324`)

Inferred: the plan calls the story "docs only" in its heading (`plan-A.md:308`) while its Lands include a shell script and a CI workflow edit. An executor must infer that "docs only" governs the *product* tree, not the diff.

**completion_condition.** After the commit, `node scripts/check-citation-anchors.mjs` is GREEN; `sh scripts/gate-g49-2-archive-pointers.sh` exits 0 and its `--selftest` exits 0; both steps are present in `.github/workflows/ci.yml`'s verify job; `pnpm gates` is green; `git diff --exit-code .descvi/screens.json` is clean. The gate is RED before the move by construction, with leg (a) printing the rewrite list, so a surviving RED means a missed pointer rather than a noisy gate (`plan-A.md:332`). The 11 pointers across 6 files and the `git mv` land in the *same* commit (`plan-A.md:315`), and the pre-move and post-move anchor counts are re-derived in that working tree and recorded in the commit message (`plan-A.md:257`).

**verification_path.**
- `sh scripts/gate-g49-2-archive-pointers.sh` → exit 0; the three legs and their exit semantics at `plan-A.md:231`, `:236–238`; expected pre-move output at `plan-A.md:590–600`.
- `sh scripts/gate-g49-2-archive-pointers.sh --selftest` → exit 0 (`plan-A.md:328`, `:332`).
- `node scripts/check-citation-anchors.mjs` (`plan-A.md:213`, `:248`).
- `pnpm gates`; `git diff --exit-code .descvi/screens.json` (`plan-A.md:332`).

**invented.**
1. **The whole of `gate-g49-2-archive-pointers.sh`.** `plan-A.md:590` shows `$ sh scripts/gate-g49-2-archive-pointers.sh` producing six LIVE POINTER rows; the file is absent from `base/scripts/`. The worker must implement three legs, a positional root list, an allow-list predicate over basenames (`plan-A.md:233`), a missing-root precondition (`plan-A.md:231`), a heading-slug *and* substring fragment resolver for leg (c) (`plan-A.md:238`), and a `--selftest` that stages a fixture with "a live pointer at a moved path, the same pointer inside the archive INDEX, a dangling archive citation, a dead fragment, and four silent controls" and additionally asserts its own scan-root enumeration (`plan-A.md:328`, rule 6 at `:207`). None of that is code the plan supplies.
2. **The content of the phase-48 tracker section.** `plan-A.md:311` fixes the shape — heading form, `Plan:` routing line, one-paragraph *What shipped*, records for S48-0a/0b/1/2/3/4/5 — and then says "the substance does NOT move here". What each of the seven per-story records actually says is left to the worker, who must reconstruct it from `.omc/plans/ralplan-phase-48-handle-admission.md`, the commit messages and `docs/handoff/260902-phase-48-close.md`. Only one record's content is specified (S48-5 exists because a live pass overturned D48-7 (iii)).
3. **The replacement text for the tracker's archiving paragraph.** `plan-A.md:312` specifies only "a dated closure recording what moved, what stayed and the consumption test that decided each".
4. **The `260901-e3-v3/` archive-README row.** `plan-A.md:314` says "in the table's existing shape, naming the four ralplans and the spike tree that directory already holds" — the worker enumerates the directory and writes the row.
5. **Whether the census is still 11/6 at execution time.** The table at `plan-A.md:213–222` is measured "on the r4' working tree"; `plan-A.md:224` and `:315` insist no count may be trusted and that the gate works from a predicate. So the worker re-runs CLAIM 1 (`plan-A.md:197`) and treats the six-file list as advisory. That is a correct instruction, but it means the rewrite list is not actually given.
6. **Which `it()` of the CI verify job the two steps go in, in relation to the four other steps this phase adds.** `plan-A.md:317` says "after `Lint` and before `Build`"; `base/.github/workflows/ci.yml` has `Lint` at line 101 and `Build` at 236 with fifteen audit-gate steps between them. The relative ordering of G49-2's pair against S49-1a's four (`plan-A.md:373–380`) is unstated.

**would_ask.** None for the owner. One for the plan's author: is the executor expected to author the four gate scripts, or is there an artefact tree (`.omc/artifacts/phase49-plan/`) holding them that the branch does not carry? The Lands wording (`plan-A.md:317`) reads as "commit an existing file".

**one_round.** **split.** Files in scope: 8 (six markdown pointer targets incl. two rewritten sections, one new shell script, one workflow). Distinct acceptance claims in the completion condition: 6 (citation gate green, G49-2 exit 0, selftest exit 0, CI steps present, `pnpm gates` green, screens.json clean) plus two commit-message obligations (pre/post anchor counts). Gates the story must implement and drive to a failing state: 1 (G49-2, three legs plus a scope-asserting selftest — itself required to be shown RED from a reduced copy, `plan-A.md:207`). Evidence gates it must run: 4. The docs migration alone is one sitting; authoring a three-leg shell gate with a fragment resolver, a self-staging fixture and a scope-assertion selftest is another. Split as **S49-0a** (the `git mv`, the 11 pointer rewrites, the two tracker sections, the archive-README row — verified by the citation gate and by hand) and **S49-0b** (the gate script, its selftest, the CI wiring — verified by its own RED/GREEN pair). Note the split has a real cost the plan would object to: S49-0a then lands without the gate that is supposed to catch a missed pointer, so S49-0b must run G49-2 against S49-0a's result before either closes.

**reading_cost.** ~319 lines, ~46,500 characters. Sections: §5 S49-0 (308–335, 28 lines), §3 D49-4 (172–269, 98), §6 preamble (515–530, 16), §6 G49-1 (531–536, 6), §6 G49-2 (537–707, 171). G49-2 alone is 171 lines / 23,191 characters — 14% of the plan for one story's one gate, most of it transcripts of runs on a tree the executor does not have.

---

## S49-P — the live-switch spike

**scope.** "Nothing permanent. The spike's diff is discarded" (`plan-A.md:357`). Inferred working scope: a throwaway edit in `packages/descvi/src/react/overlay/canvas/reorder-paint.ts` plus a throwaway override reader and key handler, driven under `pnpm descvi:dev` (`plan-A.md:342`).

**completion_condition.** In a running `pnpm descvi:dev`, with one constant (the reorder indicator thickness), one override and one drag: (1) the live canvas paints the override's value with no reload; (2) the value switches from the bare `[`/`]` keys mid-gesture and the new value appears on the same gesture; (3) switching does not extinguish the subject — the drag survives and the hover ring survives a switch; (4) switching does not change the subject — with the pointer stationary, the previewed node's oid is identical before and after the key press; (5) with the className chip editor focused, typing `w-[200px]` lands intact and fires no candidate switch, tested with the Korean IME on and off (`plan-A.md:344–348`). Legs 1–4 failing reopens D49-1 (`plan-A.md:350`); leg 5 failing moves the binding to `F2`/`F3` and reopens nothing (`plan-A.md:352`).

**verification_path.** Manual, in a browser, against `pnpm descvi:dev`; the oid read for leg (4) (`plan-A.md:347`); the typed string for leg (5) (`plan-A.md:348`). The plan gives no command beyond the dev server and no artefact path for the result. `packages/descvi/src/react/overlay/__tests__/ime-composition-guard.test.tsx` is cited as the precedent for the jsdom half only (`plan-A.md:348`).

**invented.**
1. **The spike must build the mechanism S49-1 is supposed to land, and the plan never says so.** S49-P runs "after S49-0, before S49-1a" (`plan-A.md:340`), while the override reader, the merged-constants wiring and the keyboard bump are all S49-1's Lands (`plan-A.md:395`) and the ring's constants do not exist until S49-1a (`plan-A.md:363`). Leg (1) — "with the override set, the value the live canvas paints is the override's value" — therefore requires a reader that does not exist at that point in the order. The worker invents a disposable one: its storage channel, its merge point in `reorder-paint.ts`, and its `tick` bump.
2. **Leg (3)'s ring half is unrunnable at this point in the order for the same reason.** "on the ring family the hover ring survives a switch" (`plan-A.md:346`) and leg (4)'s "on the ring family" (`plan-A.md:347`) both presuppose a ring override; the story's own scope line says "ONE constant (the reorder indicator's thickness)" (`plan-A.md:342`). The worker must decide whether to widen the spike to the ring — contradicting the scope line — or run legs (3)/(4) on the reorder family and record the ring half as untested.
3. **Where the result is recorded.** `plan-A.md:357` says the output is "a recorded result — which of (1)(2)(3) held, on which screen, at which commit". No file, no section, no owner. It also enumerates only (1)(2)(3) where the story defines five legs.
4. **Which screen.** Not named; `/shop/member-list` and `/lab/tests/reorder-flow` are named for S49-2's owner pass (`plan-A.md:1139`), not here.

**would_ask.** For the plan's author, not the owner: does S49-P's throwaway reader constrain S49-1's, or is S49-1 free to redesign it? The abort condition turns on properties of a mechanism the spike is inventing.

**one_round.** **yes**, with a caveat. Files in scope: 0 permanent, ~3 touched and reverted. Distinct acceptance claims: 5 legs, of which 2 have branch consequences (abort vs. rebind). Gates to implement and drive RED: 0. Evidence gates to run: 0 automated; 5 manual observations. It is one sitting for someone with the dev server running. The caveat is that its abort condition can end the phase (`plan-A.md:350`), so its review round is an owner conversation and not a code review.

**reading_cost.** ~90 lines, ~27,000 characters. Sections: §5 S49-P (336–359, 24), §3 D49-1 (81–131, 51 — the abort condition's option set (b′)/(a′)/(z) is only intelligible against it), §4 C49-2 (275–288, 14 — the key ruling, the capture-phase listeners, the text-entry guard line, the IME fallback), §11 row U-15 (1227, 1).

---

## S49-1a — name the ring's look values

**scope.** Given (`plan-A.md:363–380`): `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts` (a constants record with selection width, selection radius, hover width, hover inflation and two z values; `applyRingStyle` and the hover path both read it); `scripts/gate-g49-3-look-witnesses.sh` and `scripts/gate-g49-5-one-home.sh` (new); `.github/workflows/ci.yml` (four steps). Inferred: G49-6's assertion lands here (`plan-A.md:367`, `:1088`) in "the ring witness file", which is not named — `OverlayShell-selection-set.test.tsx` and `selection-ring-pool.test.tsx` are both candidates (`plan-A.md:815`).

**completion_condition.** A pure refactor: the record exists with the four exact flat key spellings `selectionWidthPx`, `selectionRadiusPx`, `hoverWidthPx`, `hoverInflatePx` (`plan-A.md:365`); no comment anywhere under the overlay tree spells a retired literal, because G49-5's bare legs are `grep -F` with no comment stripping (`plan-A.md:366`, `:999`); every existing assertion passes **unedited**, specifically the `border: '2.5px solid rgb(234, 88, 12)'` and `borderRadius: '6px'` rows in `OverlayShell-selection-set.test.tsx`, the hover width rows in `OverlayShell-canvas-hover.test.tsx`, and the five geometry rows in `OverlayShell-hover-channels.test.tsx`; a gate edit in this commit is a defect (`plan-A.md:386`). G49-5 goes from four RED rows toward none (`plan-A.md:993–997`); G49-6 asserts that mutating the single radius field moves both computed radii (`plan-A.md:1084`).

**verification_path.**
- `sh scripts/gate-g49-3-look-witnesses.sh` → exit 0, seven witness files, 87 tests (`plan-A.md:719–729`); `--selftest` → exit 0 with a per-family `ok` line (`plan-A.md:750–760`).
- `sh scripts/gate-g49-5-one-home.sh` → exit 0; per-field home/bare legs at `plan-A.md:986–997`.
- The G49-6 unit assertion (`plan-A.md:1084`).
- The unedited-assertion claim: the seven witnesses named in G49-3's list (`plan-A.md:751–758`).

**invented.**
1. **Both gate scripts, in full** — see the header note. G49-3 must run seven vitest files by path with a missing-witness precondition returning exit 2 and a selftest that stages two fixture tests *under `packages/descvi/test/`* so the package's vitest `include` globs collect them, and removes them on exit (`plan-A.md:747`), and that additionally asserts the exact seven-file list plus one required witness per furniture family (`plan-A.md:207`). G49-5 must implement two `grep` legs per field over five fields with `__tests__` excluded from the home leg (`plan-A.md:986–987`). Neither file exists.
2. **The record's name, export and module.** C49-1 requires "exactly one exported constants record" (`plan-A.md:274`); D49-2 cites `DEFAULT_HANDLE_GEOMETRY` as the precedent (`plan-A.md:142`). The ring record's identifier is never given. Only the four *field* spellings are contract (`plan-A.md:365`), and G49-5's home leg greps `selectionWidthPx:` etc. — so the record name is free but the keys are not, which is an unusual shape a worker will want confirmed.
3. **The two z values are in the record and in no gate.** `plan-A.md:363` puts "the two z values" in the record; G49-5's field table (`plan-A.md:993–997`) enumerates five fields and z is not among them, and `plan-A.md:999` calls that table "its entire reach". So two of the six named fields ship with no one-home guarantee. Whether that is intentional is not stated.
4. **Which file carries G49-6.** `plan-A.md:1088` says "the ring witness file" and that it must be a vitest assertion rather than a shell gate. Two ring witness files exist in G49-3's list.
5. **The hover-width weakness: the worker picks the remedy.** `plan-A.md:387` — S49-1a "either reads the hover width back exactly or records, in its commit message, that this leg is weaker than the others". Those are materially different outcomes (a new exact assertion vs. a prose caveat), and the plan declines to choose. U-13 (`plan-A.md:1231`) restates the same fork.
6. **What "no pixel moved" is verified against for the hover width.** The two `toContain('1.5px')` rows pass on `'11.5px'` (`plan-A.md:817`, `:832`), so the unedited-assertion claim does not cover that field, and the plan says so — but the story still lists it as part of the done-when (`plan-A.md:386`).

**would_ask.** For the plan's author: are the four field spellings really the contract, or the record name too? A later story that reshapes them must move G49-5's column in the same commit (`plan-A.md:365`), so the answer binds beyond this story. Nothing for the owner.

**one_round.** **split.** Files in scope: 5–6 (one source module, two new shell scripts, one workflow, one or two witness test files for G49-6). Distinct acceptance claims: 5 (record exists with four exact keys; both writers read it; no retired literal in any comment; every existing assertion passes unedited; G49-6 holds). Gates to implement and drive to a failing state: 2 authored (G49-3, G49-5) plus 1 new assertion (G49-6) — and each of the two scripts must be shown RED *and* have its selftest shown RED from a scope-reduced copy (`plan-A.md:207`, `:791`). Evidence gates to run: 4 (two gates, two selftests) plus the existing witness suites. Split as **S49-1a-i** (the refactor + G49-6, verified by the existing witnesses unedited) and **S49-1a-ii** (the two scripts, their selftests, the CI wiring). The plan's own reason for keeping G49-6 here — "before it there is no field; after it the coupling is already load-bearing" (`plan-A.md:1088`) — argues for keeping G49-6 in part i, not against the split.

**reading_cost.** ~315 lines, ~44,000 characters. Sections: §5 S49-1a (360–392, 33), §3 D49-0 (61–80, 20), §4 C49-1 and C49-3 (274, 289–290, 3), §6 preamble (515–530, 16), §6 G49-3 (708–836, 129), §6 G49-5 (976–1081, 106), §6 G49-6 (1082–1089, 8).

---

## S49-1 — the comparison surface

**scope.** Given (`plan-A.md:395–418`): the override reader module (one module under `packages/descvi/src/react/overlay/`, unnamed); the per-family constants records; "the wiring in the four painter modules" — `reorder-paint.ts`, `use-selection-rings.ts`, `use-spacing-affordances.ts`, and the pad glyph entries in the same file (from D49-2's list, `plan-A.md:149`); the keyboard bump on the remeasure `tick` in `OverlayShell.tsx` with the text-entry guard; `packages/descvi/src/vite-env.d.ts` (add `readonly DEV: boolean`); the candidate-list indexing in `applyRingStyle` plus a primary-ring identity; `scripts/gate-g49-4-override-leak.sh` (new); `.github/workflows/ci.yml` (two steps); new override witnesses in at least four test files and the corresponding edit to `gate-g49-3-look-witnesses.sh`'s `set --` list and its `COVERAGE` string (`plan-A.md:413`).

Inferred: which four painter modules — the plan names three files and one shared record; the file the override reader lives in; the file the keyboard handler lives in (`OverlayShell.tsx` is where the existing capture-phase listeners are, `plan-A.md:282`, but the plan never says the handler goes there).

**completion_condition.** With no override present, the rendering is byte-for-byte what shipped across every family the phase touches, spacing and padding included — G49-3's witness table green and unedited *with the override witnesses now in the list*. With an override present, each §7 candidate value renders in the live canvas and switches from the keyboard mid-gesture; the ring's spatial A/B renders two values at once. `sh scripts/gate-g49-4-override-leak.sh` is GREEN across both `dist-designview/` and `dist/`, including leg 0's source pin that the literal `descvi-look-override` occurs in exactly one file under `packages/descvi/src/react/overlay/` excluding `__tests__`, and it has been shown RED with the guard removed, with the RED output in the commit message (`plan-A.md:419`, leg semantics at `:302`, `:304`, `:406`).

**verification_path.**
- `sh scripts/gate-g49-4-override-leak.sh` and `--selftest` (`plan-A.md:416–417`); the gate builds both bundles itself, ~4.80 s + 4.66 s (`plan-A.md:419`).
- `sh scripts/gate-g49-3-look-witnesses.sh` with the widened list (`plan-A.md:413`).
- `grep -RIlF -e dsh-selection-ring -e data-dsh-ring-key -e pad-x dist/` as the reproduction behind the two-bundle rule (`plan-A.md:298`).
- Manual, in `descvi:dev`: candidate rendering, mid-gesture switch, spatial A/B (`plan-A.md:419`).
- `pnpm gates`, which from this commit onward carries two extra Vite builds (`plan-A.md:420`).

**invented.**
1. **`gate-g49-4-override-leak.sh` in full**, including the overlay-MARKER precondition that replaces `find … -print -quit` (`plan-A.md:34`), the two-bundle default scan set, leg 0's `__tests__` exclusion, and a `--selftest` that drives every leg against a staged fixture bundle with no build (`plan-A.md:419`) and asserts its own bundle set (`plan-A.md:207`).
2. **How the override is set and shaped.** `plan-A.md:302` calls `descvi-look-override` "a `localStorage` / `window` key" — two different channels, and the plan chooses neither. The ring's record value is "a candidate LIST" indexed by pool key (`plan-A.md:122`) while the other three families take a scalar; the serialisation of that record is never given, and the worker must design it before the keyboard handler can cycle it.
3. **The `[`/`]` handler's semantics.** "previous candidate / next candidate" (`plan-A.md:280`) over *what* list, per family or globally, and how the current family is selected when four families are overridable at once — unspecified. With a per-family list and one pair of keys, either the phase implicitly compares one family at a time or the keys need a selector the plan never mentions.
4. **The primary ring's identity, explicitly left as a fork.** `plan-A.md:124` and `:404`: the primary node carries no pool key, so "the primary needs a sentinel identity or the list indexes from the secondaries alone". Also whether the member identity arrives as a fourth argument to `applyRingStyle` or is read back off the node — again both offered, neither chosen (`plan-A.md:124`). The plan calls these "the kind of thing a story discovers at 2am if the plan does not say it" and then leaves both to the story.
5. **How the spatial A/B is staged for the owner.** "two selected siblings at two candidate values in one viewport" (`plan-A.md:128`) — which screen, which two siblings, how the owner produces that selection, and which candidate index maps to which sibling are all unstated.
6. **The four new override witnesses.** `plan-A.md:413` names what each must assert (the ring radius through both computed radii; the hover inflation against an unmoved selection box; the reorder band's cross-axis extent; the emitted `d`) but not which files they go in or whether the `d` witness is a new file — and it is "the phase's FIRST assertion on the glyph" (`plan-A.md:819`), i.e. a test with no precedent in the tree.
7. **Where the keyboard handler is registered and at what phase.** The existing listeners are `{ capture: true }` on `document` (`plan-A.md:282`); whether the new one joins them, and how it avoids the generation-counter listener, is inferred from `plan-A.md:280` rather than stated.

**would_ask.** For the plan's author: (a) `localStorage` or `window` for `descvi-look-override`, since G49-4 leg 0 pins the literal to one file and the choice determines whether the value survives a reload; (b) with one `[`/`]` pair and four overridable families, is the surface single-family at a time? Both block the reader's design, not just its implementation. Nothing for the owner — U49-A is ruled (`plan-A.md:1104`).

**one_round.** **no — split.** Files in scope: 10–12 (override reader, four painter/wiring modules, `OverlayShell.tsx`, `vite-env.d.ts`, one new shell script, one workflow, ≥4 witness files, plus an edit to another gate script). Distinct acceptance claims: 6 (default rendering unchanged across all four families; each candidate renders; keyboard switch mid-gesture; spatial A/B renders two values; G49-4 green on both bundles including leg 0; G49-4 shown RED with the guard removed). Gates it must implement and drive to a failing state: 1 authored (G49-4, three legs + selftest + a scope-reduced-copy RED) and 1 widened (G49-3, plus its `COVERAGE` string and its selftest's family expectations). Evidence gates it must run: 4 automated (two gates, two selftests) plus `pnpm gates` and a manual live pass. Split into **S49-1-i** the reader + records + painter wiring + `vite-env.d.ts` (verified by G49-3 unedited, default mode); **S49-1-ii** the keyboard channel and its text-entry/IME guard (verified by S49-P's legs re-run); **S49-1-iii** the ring candidate-list indexing and the spatial A/B (verified by the pooled-ring witness); **S49-1-iv** G49-4 + the four override witnesses + the CI wiring. The plan's ordering constraint survives the split: iv must land in the same commit as i, because leg 0 is RED until the reader exists and the plan requires the gate to arrive "in the same commit as the reader it guards" (`plan-A.md:420`) — which means i and iv are one commit even if they are reviewed as two units.

**reading_cost.** ~440 lines, ~65,000 characters. Sections: §5 S49-1 (393–428, 36), §5 S49-P (336–359, 24 — the story is "written against" its result, `plan-A.md:357`), §3 D49-1 (81–131, 51), §3 D49-2 (132–153, 22), §4 C49-2 (275–288, 14), §4 C49-8 (296–304, 9), §6 preamble (515–530, 16), §6 G49-3 (708–836, 129), §6 G49-4 (837–975, 139). This is a third of the plan for one story.

---

## S49-2 — `reorder-indicator-look`

**scope.** Given (`plan-A.md:431`): `packages/descvi/src/react/overlay/canvas/reorder-paint.ts` — `REORDER_INDICATOR_THICKNESS_PX` and the cross-axis extent rule at `const crossMin = Math.min(...order.map(`. Gate move (`plan-A.md:437–439`): the three `toBeLessThanOrEqual(2)` rows and the three extent literals in `packages/descvi/test/reorder/reorder-paint-geometry.test.ts` and `packages/descvi/src/react/overlay/__tests__/reorder-paint.test.tsx`. Explicitly excluded: the e2e tree — `e2e/reorder-drag.spec.ts` asserts presence and visibility only (`plan-A.md:442`). This is the best-scoped story in the plan.

**completion_condition.** Two commits per C49-5: a contract commit that re-expresses the named assertions with no pixel moved, then a value commit that edits no gate and ships the owner's U49-1/U49-2 answers (default 2 px, members' cross-axis extent). After the value lands, the amended gate is re-run and shown RED on this story's named mutation — the thickness *raised*, or the extent literals moved — with that RED output recorded beside the value commit; a story that cannot produce one has shipped scaffolding and does not close (`plan-A.md:446`, G49-7 at `:1094`).

**verification_path.** `pnpm vitest run packages/descvi/test/reorder/reorder-paint-geometry.test.ts` with the constant raised (`plan-A.md:1221`); the direction table at `plan-A.md:827` (raise → RED, lower to 1 → GREEN, one-sided); the measured correction that a raise reports **one** failing test and not three, because all three rows sit in one `it()` (`plan-A.md:745`, `:827`); `sh scripts/gate-g49-3-look-witnesses.sh` as the umbrella run (`plan-A.md:710`).

**invented.** Very little.
1. **Whether the observation sheet is an artefact.** U49-C is ruled "the OBSERVATION SHEET, not a story" (`plan-A.md:1116`) and S49-2 "carries U49-C's observation question" (`plan-A.md:448`), but no file, format or owner for that sheet is named anywhere in the plan. The worker invents it or drops it.
2. **The gap-0 demonstration.** "the owner should be shown a gap-0 parent at each candidate weight" (`plan-A.md:444`) — which screen has a gap-0 parent is not named.
3. **Whether U49-2 candidate (3), "the extent plus a fixed overhang" (`plan-A.md:1125`), has a specified overhang.** It does not; if the owner picks it, the value is invented at execution time.

**would_ask.** For the owner: what overhang, if U49-2 (3) is chosen. That question only fires on one of three answers, so the story can be dispatched and the question raised conditionally.

**one_round.** **yes.** Files in scope: 3 (one source module, two test files). Distinct acceptance claims: 3 (contract commit moves no pixel; value commit edits no gate; the amended gate shown RED on the named mutation). Gates to implement: 0 authored, 1 amended. Evidence gates to run: 2 (the vitest witnesses, plus the G49-3 wrapper). The two-commit split is a sequencing rule, not a second sitting.

**reading_cost.** ~47 lines, ~9,000 characters. Sections: §5 S49-2 (429–449, 21), §4 C49-5 (292–293, 2), §6 G49-3's RED-when table (823–835, 13), §6 G49-7 (1090–1097, 8), §7 rows U49-1/U49-2 (1124–1125, 2) and `plan-A.md:1139`.

---

## S49-3 — `selection-ring-treatment`

**scope.** Given (`plan-A.md:452`): "the record from S49-1a", i.e. `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts`. Gate move across four assertion sites (`plan-A.md:456–460`): `OverlayShell-selection-set.test.tsx` (selection border and radius), `OverlayShell-canvas-hover.test.tsx` (hover width, `toContain`-limited), `OverlayShell-hover-channels.test.tsx` (the inflation, five `ring.style.top` rows), and — for a shade change only — `resize-handle-layer.test.tsx`. Constraint on scope rather than a file: the hover-vs-selection relation must be changed on the **hover** side, because `e2e/multi-select-shield.spec.ts` compares the selection ring's bounding box to the element's box under `Math.round` with no tolerance (`plan-A.md:464`).

**completion_condition.** Contract commit re-expresses the four assertion sites against the named constants with no pixel moved; value commit edits no gate and ships U49-3/U49-4 (default: radius 6, selection 2.5 / hover 1.5); the amended gate is then shown RED on a radius or width moved in either direction — both are exact pins — with the RED output recorded beside the value commit; G49-6 is GREEN throughout, since a width change that silently decoupled the two radii would pass every row in the list (`plan-A.md:472–473`). No candidate changes the `deep` shade, so C49-7's chip-border coupling is not exercised (`plan-A.md:295`, `:474`).

**verification_path.** The four assertion files above; `sh scripts/gate-g49-3-look-witnesses.sh` (`plan-A.md:710`); the per-field RED direction table (`plan-A.md:829–832`); G49-6's mutate-the-field assertion (`plan-A.md:1084`); `pnpm test:e2e e2e/multi-select-shield.spec.ts` with the ring inflated is what would settle U-6, which is read and not executed (`plan-A.md:1223`).

**invented.**
1. **Whether the value commit re-pins the inflation rows.** U49-4 candidates (3) `(2.5, 2.5, 4)` and (4) `(2.5, 1.5, 4)` move the hover inflation from 2 to 4 px (`plan-A.md:1127`), and `OverlayShell-hover-channels.test.tsx`'s rows are exact arithmetic on that inflation (`plan-A.md:816`, `:831`). The plan's rule is that the contract commit re-expresses assertions "against the named constants" (`plan-A.md:471`) — so if those five rows are rewritten to compute from `hoverInflatePx`, the value commit edits no gate; if they are left as literals, the value commit must edit them, which C49-5 forbids. The plan states the rule and never says which of the two the executor is to do for these particular rows.
2. **The spatial A/B's operating procedure.** "two pooled siblings at two candidate widths in one viewport" (`plan-A.md:462`) — the mechanism is S49-1's, but which screen and which pair of siblings the owner judges on is named for no story.
3. **Whether U-6 gets executed here.** `plan-A.md:1223` flags the no-tolerance e2e comparison as read-and-not-executed and says `pnpm test:e2e e2e/multi-select-shield.spec.ts` with the ring inflated would settle it. No story's done-when requires that run, and this is the story whose change is routed away from the selection side precisely because of it.

**would_ask.** For the plan's author: are the `ring.style.top` rows re-expressed as arithmetic over `hoverInflatePx` in the contract commit? A worker who guesses wrong produces exactly the C49-5 violation the phase's fourth principle exists to prevent.

**one_round.** **yes**, for the contract-plus-value pair, but only if S49-1a and S49-1 have both landed. Files in scope: 5 (the record plus four test files). Distinct acceptance claims: 4 (contract commit moves no pixel across four sites; value commit edits no gate; amended gate RED in either direction; G49-6 green throughout). Gates to implement: 0 authored, 1 amended (four sites), 1 that must stay green (G49-6). Evidence gates to run: 3 (G49-3, G49-6, and the named RED). The e2e trap is a constraint on the design, not extra work.

**reading_cost.** ~70 lines, ~17,000 characters. Sections: §5 S49-3 (450–473, 24), §4 C49-3 (289–290, 2), C49-5 (292–293, 2), C49-7 (295, 1), §6 G49-3's per-field witness table and RED-when table (813–835, 23), §6 G49-6 (1082–1089, 8), §6 G49-7 (1090–1097, 8), §7 rows U49-3/U49-4 (1126–1127, 2).

---

## S49-4 — `spacing-affordance-mark`

**scope.** Given (`plan-A.md:476`): `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts` — `figureFor`, the `SPACING_GLYPH_PATHS` record, and "the reveal predicate". **Inferred and explicitly delegated:** "A *reveal* change moves when nodes exist at all and therefore does touch that spec's subject set. Grep the e2e for the strip and apron roles before writing the lands list (PM-5)" (`plan-A.md:483`). The plan hands the reveal half's scope discovery to the executor. Hard constraint: `SPACING_GLYPH_PX` stays at 8 (`plan-A.md:481`).

**completion_condition.** If the owner takes U49-5a and defers U49-5b, the story ships the mark alone (`plan-A.md:478`). The C46-1 `glyph-conditional` obligation in `e2e/spacing-gesture.spec.ts` — an `svg` descendant, hidden below the published size term — is untouched by a mark change (`plan-A.md:480`). The G49-7 obligation is discharged against the override witness S49-1 lands (G49-3's spacing/padding row) on a mutation of the emitted `d`, because no gate pins the glyph today; **if S49-1 did not land that witness, S49-4 has no gate to relax and no gate to show RED, and that is what blocks the story** (`plan-A.md:485`).

**verification_path.** `e2e/spacing-gesture.spec.ts` for the C46-1 obligation (`plan-A.md:480`); the override `d` witness through `sh scripts/gate-g49-3-look-witnesses.sh` (`plan-A.md:819`, `:833`); the PM-5 e2e grep with a recorded non-zero baseline before the change (`plan-A.md:1184`).

**invented.**
1. **The reveal predicate's entire design.** The backlog direction is "reveal when the pointer is inside the object" (kickoff:34, `plan-A.md:478`). The plan says the reveal "touches the hit model, not the paint" (`plan-A.md:478`) and stops there. What "inside the object" means against the existing placement pass, what happens on nested objects, and how the strips behave on exit are all invented by the worker.
2. **The reveal half's file list.** `plan-A.md:483` instructs the worker to grep for it.
3. **Whether the reveal change re-pins e2e assertions.** The same line says it "does touch that spec's subject set" without saying which rows, and the plan's own PM-5 row (`plan-A.md:1184`) says phase-48 shipped this exact defect three times.
4. **The new mark's path data.** "one `-` mark per edge" — no `d` string given, here or in §7 (`plan-A.md:1128`).
5. **What happens if the owner takes 5b and the reveal's e2e cost turns out to be large.** No abort or deferral path is given for a scope discovery mid-story; C49-6 covers owner deferral only (`plan-A.md:294`).

**would_ask.** For the plan's author, before dispatch: what is the reveal predicate? The story asks a worker to design an interaction change on the hit model with one sentence of direction and an instruction to find its own blast radius. That is the largest unpriced item in the phase.

**one_round.** **split**, and the split is by owner answer rather than by file. Files in scope: 1 given + an unknown e2e set the story must discover. Distinct acceptance claims: 3 for the mark (figure routing changed, C46-1 intact, `d` witness RED then GREEN); the reveal half has none stated. Gates to implement: 0 authored; the story depends on a witness another story lands. Evidence gates to run: 2 + an undetermined e2e set. **U49-5a is one round: yes.** **U49-5b is not dispatchable as written** — see the closing section. If both are taken, split along the owner's two rows, which is what D49-3's 5a/5b split already anticipates (`plan-A.md:162`, `:1133`).

**reading_cost.** ~48 lines, ~9,500 characters for the mark half. Sections: §5 S49-4 (474–491, 18), §3 D49-3 (154–171, 18 — the 5a/5b deferral semantics), §6 G49-3's spacing/padding row (819, 1) and RED-when row (833, 1), §6 G49-7 (1090–1097, 8), §7 rows U49-5a/5b (1128–1129, 2). The reveal half's reading cost is not computable from the plan, because the story tells the worker to build its own lands list.

---

## S49-5 — `padding-glyph`

**scope.** Given (`plan-A.md:494`): two entries in `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts` — `"pad-x"` and `"pad-y"`. Measured to occur nowhere else: `grep -rIn -e 'M4 4v8' -e 'SPACING_GLYPH_PATHS' e2e packages src | grep -v use-spacing-affordances` returns nothing (`plan-A.md:496`).

**completion_condition.** No contract-first split is performed, because no gate asserts the path strings — the plan says so explicitly rather than splitting against an empty set (`plan-A.md:496`, `:499`). What the story owes instead: the override witness on the emitted `d` (G49-3's spacing/padding row) shown RED on the old figure and GREEN on the new, plus the C46-1 obligation confirmed intact — still an `<svg>` with a path, still hidden below `SPACING_GLYPH_PX`, still declared `glyph-conditional` (`plan-A.md:499`). Deferral default is **change**, not status quo: the standing G48-8 direction executes (`plan-A.md:500`).

**verification_path.** The `d` witness through `sh scripts/gate-g49-3-look-witnesses.sh`; `e2e/spacing-gesture.spec.ts` for the C46-1 obligation; the grep at `plan-A.md:496` re-run.

**invented.**
1. **The two new path strings.** "a plain directional bar (`-` on horizontal edges, `l` on vertical)" (`plan-A.md:1130`) — the actual `d` values, their length, weight and alignment inside the 16-unit box the existing paths use are the worker's. For a story whose entire deliverable is two path strings, that is the whole story.
2. **Dependency on S49-1's `d` witness**, same as S49-4: if that witness did not land, this story has no evidence path at all (`plan-A.md:499`, `:819`).

**would_ask.** None. The direction is standing and the deferral default is stated.

**one_round.** **yes.** Files in scope: 1 (plus one witness file if the `d` assertion needs extending). Distinct acceptance claims: 3 (`d` witness RED on old / GREEN on new; C46-1 intact; the figure matches the standing direction). Gates to implement: 0. Evidence gates to run: 2. This is the smallest and cleanest story in the plan.

**reading_cost.** ~22 lines, ~4,500 characters. Sections: §5 S49-5 (492–501, 10), §6 G49-7 (1090–1097, 8), §6 G49-3's spacing/padding row (819, 1), §7 row U49-6 (1130, 1), §3 D49-3's `padding-glyph` paragraph (170, 1).

---

## S49-6 — the reorder arming threshold (optional rider)

**Not dispatched.** U49-B was ruled NO by the owner on 2026-09-04 (`plan-A.md:1107`); the execution order runs it "only if U49-B is answered yes" (`plan-A.md:39`); its §7 row is struck (`plan-A.md:1131`).

**scope** (if ever revived, `plan-A.md:504`): `packages/descvi/src/react/overlay/canvas/pointer-thresholds.ts`, three hard pins, one regime tripwire, G47-3's diagonal control, two e2e sub-threshold rows, plus two hand-added pins for the stale-green copies `PURCHASE_FLOOR_PX` in `handle-geometry.test.ts` and the `4 px floor` literal in `e2e/resize-handles.spec.ts`, which land **first**.

**completion_condition.** The two new pins exist and have been shown RED by editing the constant; the chosen value ships; G47-3 has been shown RED at a value it should reject; the value is inside `[3, 4.243]`, derived once in U49-B (`plan-A.md:506`, `:1115`).

**verification_path.** Change `POINTER_DRAG_THRESHOLD_PX` and run the full suite; the two stale-green files must stay green while others go red — and the plan flags this as an unexecuted **negative** claim, "the shape of claim most likely to be wrong", to be settled *before* believing U49-B (`plan-A.md:1225`).

**invented.** Not applicable — the story is not dispatched. Worth recording that its `Done when` depends on U-8, a negative claim the plan says should be executed before U49-B is believed (`plan-A.md:1225`), and U49-B has now been answered without that execution.

**one_round.** **no**, if revived: two hand-added pins shown RED, a shared five-gesture constant, a one-value reachable box, and a full-suite blast-radius run. The plan itself calls it "not a rider on a look phase; it is a small phase" (`plan-A.md:1115`).

**reading_cost.** ~19 lines, ~5,500 characters: §5 S49-6 (502–514, 13), §7 U49-B (1107–1115, 9 — the reachable box has exactly one home there and is stated nowhere else, `plan-A.md:506`).

---

## Closing

### Dispatch today, dispatch with a question, cannot dispatch

| story | verdict |
|---|---|
| S49-0 | **Dispatch today**, if the executor is told the gate script is theirs to write. As written the Lands line implies otherwise. |
| S49-P | **Dispatch with a question**: does the spike build its own throwaway override reader, and does it widen to the ring family for legs (3)/(4)? Its scope line and its legs disagree (`plan-A.md:342` vs `:346–347`). |
| S49-1a | **Dispatch with a question**: are the four field spellings the whole contract, and which witness file carries G49-6 (`plan-A.md:365`, `:1088`)? |
| S49-1 | **Dispatch with two questions**: `localStorage` or `window` for `descvi-look-override` (`plan-A.md:302`); and how `[`/`]` selects among four overridable families (`plan-A.md:280`). Both are design decisions, not details. |
| S49-2 | **Dispatch today** once the owner table is filled. The cleanest story in the plan. |
| S49-3 | **Dispatch with a question**: are `OverlayShell-hover-channels.test.tsx`'s five inflation rows re-expressed as arithmetic over `hoverInflatePx` in the contract commit? Guessing wrong produces the C49-5 violation the phase exists to prevent. |
| S49-4 (U49-5a, the mark) | **Dispatch today** once the owner answers 5a. |
| S49-4 (U49-5b, the reveal) | **Cannot dispatch.** No predicate, no file list, no acceptance claim — `plan-A.md:476` names "the reveal predicate" and `plan-A.md:483` instructs the worker to grep for its own blast radius. |
| S49-5 | **Dispatch today** — the path strings are the worker's to draw, which is legitimate for a look story. |
| S49-6 | **Not dispatched** — ruled NO (`plan-A.md:1107`). |

### Material decisions parked for the owner

| decision | lines | can a worker proceed without the answer? |
|---|---|---|
| U49-1 reorder weight | `plan-A.md:1124` | Yes for the contract commit, no for the value commit. Default 2 px (`plan-A.md:448`). |
| U49-2 reorder length rule | `plan-A.md:1125` | Yes for the contract commit. If (3) "extent plus a fixed overhang" is chosen, the overhang value is *also* unanswered — the table offers a candidate with no number in it. |
| U49-3 ring radius | `plan-A.md:1126` | Yes for the contract commit. Default 6 px. |
| U49-4 ring width + hover relation | `plan-A.md:1127` | Yes for the contract commit — but the answer determines whether the inflation moves, which determines how the five `hover-channels` rows must be written in that same contract commit. So this one leaks backwards into pre-gate work. |
| U49-5a mark | `plan-A.md:1128` | Yes. Default: shipped mark. |
| U49-5b reveal | `plan-A.md:1129` | No — and not because of the owner. The plan does not specify the alternative it is asking the owner to choose beyond "revealed when the pointer is inside the object". |
| U49-6 pad glyph | `plan-A.md:1130` | Yes, and it does not block at all: the direction is standing and deferral defaults to change (`plan-A.md:170`, `:500`). |
| U49-C's observation sheet | `plan-A.md:1116`, `:448` | Ruled, but the artefact has no name, format, file or owner anywhere in the plan. A worker will either invent one or silently drop the question. |
| S49-P's abort → a reopened D49-1 | `plan-A.md:350` | Owner-blocking by construction; the plan supplies three executable successors (b′)/(a′)/(z), which is more than most reopen clauses get. |

Three questions ruled on the plan are genuinely closed and need no further owner time: U49-A (`plan-A.md:1104`), U49-B (`plan-A.md:1107`), U49-C (`plan-A.md:1116`).

### What would make a worker do wasted work

**1. Roughly half the plan is addressed to reviewers, not executors.** The Status block is 38 lines / 17,212 characters of revision history, lane verdicts and twelve numbered reversals of the plan's own earlier revisions (`plan-A.md:3–40`). §11's UNVERIFIED register is another 27 lines / 16,721 characters, largely a record of which review round settled which claim (`plan-A.md:1206–1232`). §9's PM-10 row alone (`plan-A.md:1189`) is a thirteen-instance catalogue of defects in *superseded drafts of this plan*. None of it changes what any worker types. A worker who reads §5 and §6 for their story still meets this material, because the stories cite back into it.

**2. The gate sections are 80% demonstration transcripts of runs on a tree the executor does not have.** G49-2 is 171 lines / 23,191 characters; G49-3 is 129 / 15,958; G49-4 is 139 / 15,157; G49-5 is 106 / 10,918 — 545 lines and ~65,000 characters, 44% of the plan, for four gates. The content that an executor needs — the legs, the exit codes, the allow-list predicate, the RED-when direction — is perhaps a fifth of that. The rest is pasted output (`plan-A.md:589–600`, `:719–729`, `:734–743`, `:750–760`, `:796–801`) and a history of forms that could not work (`plan-A.md:223–227`, `:839–846`, `:978`). Every content hash and count in those transcripts is explicitly disclaimed as unreproducible (`plan-A.md:34`), so a worker who tries to match them is chasing nothing.

**3. Repeated constraints.** The CI step-block rule — 6/8 indentation, `Audit gate — ` prefix, single-line `run:` scalars because `scripts/gates.mjs` treats a block scalar as a parse error — is stated three times in full (`plan-A.md:326`, `:383`, `:417`). The `dist/` reversal is stated in six places (`plan-A.md:28`, `:298`, `:846`, `:1143`, `:1180`, `:1229`). The esbuild-mangling measurement in five (`plan-A.md:28`, `:298`, `:302`, `:844`, `:1189`). The reorder thickness's one-sided bound in six (`plan-A.md:226`, `:437`, `:442`, `:745`, `:827`, `:1221`). The one-home rule for counts is itself stated in four places (`plan-A.md:24`, `:224`, `:257`, `:506`).

**4. A gate guarding a subject no story changes.** G49-5 enumerates five fields (`plan-A.md:993–997`) of which one — the reorder thickness — is already GREEN and is not what the gate exists for; meanwhile the two z values S49-1a puts in the same record (`plan-A.md:363`) have no row at all, and `plan-A.md:999` says the table is "its entire reach". A worker who assumes the gate covers the record will be wrong in one direction and over-careful in the other.

**5. A fully specified story the owner has ruled out.** S49-6 is 13 lines of Lands and Done-when plus a 9-line derivation in U49-B (`plan-A.md:502–514`, `:1107–1115`), all of it live text in §5, while `plan-A.md:39` and `:1131` say it does not run. The struck table row explains why it is kept; the story section does not, and §5 is where an executor looks.

**6. The plan's own instruction to distrust its measurements is correct and expensive.** The census (`plan-A.md:213–222`), the anchor counts (`plan-A.md:251–255`) and the arbitrary-value token counts (`plan-A.md:35`) are each accompanied by a rule that they must be re-derived rather than trusted (`plan-A.md:224`, `:257`). That is the right call, but it means several hundred characters of tables in the plan are, by the plan's own instruction, not usable as inputs — the commands beside them are the deliverable and the tables are scenery.
