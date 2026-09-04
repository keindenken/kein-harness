# Execution ledger — plan-A.md

Lead's reading for dispatch. Every entry is what a worker would be handed and what I would have to supply myself.

One fact governs four of the nine entries and is stated once here rather than repeated: **none of the four gate scripts the plan calls "COMMITTED SCRIPTS" (`plan-A.md:6`, `plan-A.md:519`) exists in the repository.** `base/scripts/` holds `check-citation-anchors.mjs`, `check-handle-constants.mjs`, `check-v3-registers.mjs`, `check-ki-register.mjs`, `check-session-migration.mjs`, `check-extract-outcome.mjs`, `e2e-gate-cx1.mjs`, `e2e-gate-cx2.mjs`, `gates.mjs` and three others — no `gate-g49-*`. The plan pastes their **output transcripts** (`plan-A.md:589-604`, `plan-A.md:615-631`, `plan-A.md:717-730`, `plan-A.md:749-766`, `plan-A.md:867-873`, `plan-A.md:877-891`, `plan-A.md:1008-1019`) and never their source, while assigning them to stories as Lands (`plan-A.md:317`, `plan-A.md:370`, `plan-A.md:408`). So each of those stories carries a hidden sub-project: reconstruct a shell gate from its own printout.

---

## S49-0 — the v3.5 close (docs only)

**scope** — plan-given, except as marked.
- `docs/e3/tracker.md` — new phase-48 section + replaced archiving paragraph (`plan-A.md:311-312`)
- `git mv .omc/plans/ralplan-e3-v3-direct-manipulation.md .omc/plans/ralplan-phase-42-resize-handles.md .omc/archive/260901-e3-v3/` (`plan-A.md:313`)
- `.omc/archive/README.md` (`plan-A.md:314`), `docs/architecture.md`, `docs/known-issues.md`, `.omc/research/phase48-strip-band-pricing.md`, `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` (`plan-A.md:315`) — I confirmed all six carry the pointers in `base/`
- `scripts/gate-g49-2-archive-pointers.sh` — **new file, inferred**: the Lands line says it "IS COMMITTED BY THIS STORY" (`plan-A.md:317`) but no source is given and none is in `base/scripts/`
- `.github/workflows/ci.yml` verify job, two steps (`plan-A.md:320-324`)

**completion_condition** — The two dead v3 plans sit in `.omc/archive/260901-e3-v3/`, the eleven live pointers across six files are rewritten in the same commit as the move (`plan-A.md:315`), the archive index gains its missing `260901-e3-v3/` row (`plan-A.md:314`), the tracker gains a phase-48 routing section carrying only the per-story ledger S48-0a…S48-5 and no substance already in the plan or the close handoff (`plan-A.md:311`), and the tracker's stale archiving-deferral paragraph is replaced rather than merely satisfied (`plan-A.md:312`, `plan-A.md:243`). Evidence: `node scripts/check-citation-anchors.mjs` green, `sh scripts/gate-g49-2-archive-pointers.sh` exit 0, its `--selftest` exit 0, both steps present in the CI verify job, `pnpm gates` green, `git diff --exit-code .descvi/screens.json` clean (`plan-A.md:332`).

**verification_path**
- `node scripts/check-citation-anchors.mjs` (`plan-A.md:248`, `plan-A.md:533`) — explicitly NOT sufficient: a moved `.md` target does not turn it red (`plan-A.md:534`)
- `sh scripts/gate-g49-2-archive-pointers.sh` — exit 0/1/2 is the verdict (`plan-A.md:549-551`); red before the move by construction, and leg (a) is the rewrite list (`plan-A.md:587`)
- `sh scripts/gate-g49-2-archive-pointers.sh --selftest` (`plan-A.md:698`)
- `pnpm gates`, `git diff --exit-code .descvi/screens.json` (`plan-A.md:332`)
- Pre- and post-move anchor counts re-derived in the same tree and recorded in the commit message (`plan-A.md:257`)

**invented**
1. **Whether the worker authors the gate script or receives it.** `plan-A.md:519` says "THE GATES THIS PHASE AUTHORS ARE COMMITTED SCRIPTS AS OF r3'", `plan-A.md:7` says at r3' they were "UNTRACKED (`git ls-files scripts/ | grep g49` → empty)", and `plan-A.md:317` puts the script in this story's Lands. The tree has no such file. I have to rule that the worker writes it — and then that it must reproduce the pasted transcript's row prefixes (`LIVE POINTER`, `DANGLING`, `DEAD FRAGMENT`), its four plants and four named controls, its three exit codes, its `mktemp -d` fixture, its self-assembled plants (`plan-A.md:637`), and both resolution branches of leg (c) (`plan-A.md:566`) — from prose and output alone. Nothing in the plan says how close the reconstruction must be to count.
2. **The phase-48 tracker section's prose.** The plan fixes the heading form and the story ids (`plan-A.md:311`) and forbids substance ("The substance does NOT move here"), leaving the *What shipped* paragraph's content entirely to the worker while binding it not to duplicate the plan, the commit messages or the close handoff. Where the boundary sits is mine to draw.
3. **The archive index's new row text.** "in the table's existing shape, naming the four ralplans and the spike tree" (`plan-A.md:314`) — the row's description column is authored, not specified.

**would_ask**
- Do the four gate scripts exist as artifacts from the planning session, and if so where? If the executor rebuilds them, is the acceptance criterion behavioural (three verdicts, controls silent) or transcript-identical?
- The Done-when reads "it exits 1 before the move … so a run that is still RED after the commit means a pointer was missed" (`plan-A.md:332`). Confirm the CI wiring lands in this same commit — a red G49-2 wired into `verify` before the move would break `pnpm gates` for the tree the move is prepared on.

**one_round** — **split.** Files in scope: 11 (6 pointer files incl. two also being moved, 2 moved paths, tracker, archive index, ci.yml) plus one new script. Distinct acceptance claims in the completion condition: 6 (`plan-A.md:332`). Gates to implement and drive to a failing state: 1 script, 3 legs, plus a selftest asserting 4 plants, 4 controls, 3 verdicts and its own scope (`plan-A.md:527`, `plan-A.md:615-631`). Evidence gates to run: 4. Split as **S49-0a** the docs move and pointer rewrite (verified by `check-citation-anchors` plus a hand grep) and **S49-0b** the gate script, its selftest and the CI wiring. The second half is a gate-authoring task with a different skill and a different review.

**reading_cost** — ~303 plan lines: S49-0 (`plan-A.md:308-335`, 28), D49-4 (`plan-A.md:172-269`, 98), G49-1 (`plan-A.md:531-536`, 6), G49-2 (`plan-A.md:537-707`, 171). Add the status block's real-tree gate table (`plan-A.md:14-23`, 10) or the worker reads G49-2's red as a broken gate → ~313.

---

## S49-P — the live-switch spike

**scope** — plan-given: no permanent files. "The spike's diff is discarded" (`plan-A.md:356`). Subject is one constant, `REORDER_INDICATOR_THICKNESS_PX`, one override, one drag, in a running `pnpm descvi:dev` (`plan-A.md:342`).

**completion_condition** — Five legs hold in a live browser: the override's value paints without reload (`plan-A.md:345`); it switches from the bare `[`/`]` keys mid-gesture and repaints on the same gesture (`plan-A.md:346`); switching does not extinguish the subject — the drag survives, the hover ring survives (`plan-A.md:347`); switching does not *change* the subject, verified by reading the previewed node's oid before and after a keypress with the pointer stationary (`plan-A.md:348`); and typing `w-[200px]` into the className chip editor lands intact with no switch firing, with the IME on and off (`plan-A.md:350`). Failure of legs 1–4 reopens D49-1 (`plan-A.md:352`); failure of leg 5 moves the binding to `F2`/`F3` and reopens nothing (`plan-A.md:354`, `plan-A.md:288`).

**verification_path** — Manual, in `pnpm descvi:dev`; the plan names no command. Legs 2/4/5 are the ones the register says only runtime settles (`plan-A.md:1219`, `plan-A.md:1227`). Per the kickoff, `:7331` is a fixed-port singleton, so an EADDRINUSE is concurrency (`plan-A.md:1188`).

**invented**
1. **Where the spike's result is recorded.** "its OUTPUT is a recorded result — which of (1)(2)(3) held, on which screen, at which commit — and that result is what S49-1 is written against" (`plan-A.md:356`). No file, no section, no owner for the record. S49-1's brief depends on it, so I have to name a destination.
2. **Who decides "fragile".** The leg-5 branch is "if the guard is judged fragile the fallback is … a non-printable key" (`plan-A.md:288`). The judgement is unowned; a spike runner who wants the phase to proceed and one who wants it safe reach different answers.
3. **Legs 4 and 5 are on families the spike's own scope excludes.** Scope is "ONE constant (the reorder indicator's thickness)" (`plan-A.md:342`), but leg 3 asks that "on the ring family the hover ring survives a switch" and leg 4 says "The spike checks this explicitly, on the ring family" (`plan-A.md:347-348`) — and the ring has no constants at all until S49-1a (`plan-A.md:78`), which runs *after* the spike (`plan-A.md:340`). I have to rule that legs 3–4 observe the ring rather than override it.

**would_ask**
- Where does the spike's result live, and does S49-1 block on it being written down?
- Legs 3/4 name the ring family while the spike's scope names one reorder constant and the ring's constants do not exist yet — observe-only, or does the spike pull S49-1a's naming forward?

**one_round** — **yes.** Files: 0 permanent. Acceptance claims: 5, all observational. Gates implemented: 0. Evidence gates run: 0 — it is a browser session. One sitting, one review round, provided the runner has a machine that can run `descvi:dev` and a Korean IME (`plan-A.md:350`).

**reading_cost** — ~95 lines: S49-P (`plan-A.md:336-359`, 24), C49-2 (`plan-A.md:275-288`, 14), D49-1 (`plan-A.md:81-131`, 51) for what the abort reopens, plus register rows U-2 and U-15 (`plan-A.md:1219`, `plan-A.md:1227`, 2 very long lines).

---

## S49-1a — name the ring's look values

**scope** — plan-given: `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts` (`plan-A.md:364`). **Inferred additions:** a new unit test file for G49-6 (`plan-A.md:369`, `plan-A.md:1084` — no path given); `scripts/gate-g49-3-look-witnesses.sh` and `scripts/gate-g49-5-one-home.sh`, both new files with no source given (`plan-A.md:370`); `.github/workflows/ci.yml`, four steps (`plan-A.md:373-380`).

**completion_condition** — The three inline ring literals — `2.5px solid ${color}`, `borderRadius = "6px"`, `1.5px solid ${shades.light}` (`plan-A.md:78`; confirmed at `base/packages/descvi/src/react/overlay/canvas/use-selection-rings.ts:60,61,273`) — become fields of one exported record read by both the selection writer and the hover path, with the radius as a single field consumed twice (`plan-A.md:364`, C49-3 at `plan-A.md:289`). Field keys are exactly `selectionWidthPx`, `selectionRadiusPx`, `hoverWidthPx`, `hoverInflatePx`, flat (`plan-A.md:366`). No pixel moves: every existing assertion passes **unedited**, and a gate edit in this commit is a defect (`plan-A.md:387`). G49-6 lands here (`plan-A.md:369`). No comment may spell a retired literal, because G49-5's bare legs are `grep -F` with no comment stripping (`plan-A.md:367`).

**verification_path**
- `sh scripts/gate-g49-3-look-witnesses.sh` exit 0 over its seven witnesses (`plan-A.md:710-712`); named witnesses at `plan-A.md:750-757` — all seven exist in `base/`
- `sh scripts/gate-g49-5-one-home.sh` — the four ring rows go from `RED — 0 homes` to green (`plan-A.md:993-996`, `plan-A.md:1020`)
- Both `--selftest`s exit 0 (`plan-A.md:374`, `plan-A.md:378`)
- Named exact assertions: `OverlayShell-selection-set.test.tsx` border and radius rows, the hover width rows, the five geometry rows in `OverlayShell-hover-channels.test.tsx` (`plan-A.md:387`)
- G49-6: mutate the field, assert both computed radii moved (`plan-A.md:1084`)

**invented**
1. **Whether the z values are in the record, and what they are called.** The Lands line says the record carries "selection width, selection radius, hover width, hover inflation **and the two z values**" (`plan-A.md:364`). The binding spelling list two lines later names four keys and no z (`plan-A.md:366`), and G49-5's field manifest is five rows with no z row (`plan-A.md:991-997`). Since `plan-A.md:366` makes the spellings contract and `plan-A.md:999` makes the manifest binding on this executor, a worker who adds z fields is unguarded and one who omits them contradicts the Lands line. I would rule: include them, spelled outside the gated four.
2. **Where G49-6 lives.** "A unit assertion" (`plan-A.md:1084`) with no file, no suite, no name. It is the only mechanism for C49-3 (`plan-A.md:1086`) and the only gate in the phase with no path at all.
3. **The hover-width acceptance leg, left as an explicit either/or.** "S49-1a either reads the hover width back exactly or records, in its commit message, that this leg is weaker than the others" (`plan-A.md:389`). That is a choice about how strong the story's central claim ("every assertion passes unedited") actually is, handed to the executor.
4. **The two gate scripts' source**, as for S49-0 — including G49-3's selftest, which must stage two fixture tests under `packages/descvi/test/` where the package's vitest globs collect them (`plan-A.md:747`) and assert its own seven-file enumeration plus one witness per family (`plan-A.md:749-757`).

**would_ask**
- Are the z values in the record? `plan-A.md:364` and `plan-A.md:366`/`plan-A.md:991-997` disagree.
- Which file holds G49-6, and is it a vitest unit test in `packages/descvi/src/react/overlay/__tests__/` or a witness added to an existing one?
- Same script-provenance question as S49-0.

**one_round** — **split.** Files: 1 source file, 1 new test, 2 new scripts, 1 ci.yml — but the two halves have nothing in common. Distinct acceptance claims: 5 (record exists with four exact keys; both writers read it; radius is one field; every existing assertion unedited; no gate edited). Gates to implement and drive RED: 3 (G49-3, G49-5, G49-6), of which two are shell scripts with selftests that must themselves be shown red from a scope-reduced copy (`plan-A.md:527`). Evidence gates to run: 4 script invocations plus the seven-witness vitest run. Split as **S49-1a-i** the refactor plus G49-6 (its own claim is "no pixel moved", verifiable with the existing suite alone) and **S49-1a-ii** the two gate scripts, their selftests and the CI steps.

**reading_cost** — ~300 lines: S49-1a (`plan-A.md:360-392`, 33), D49-0 (`plan-A.md:61-80`, 20), G49-3 (`plan-A.md:708-836`, 129), G49-5 (`plan-A.md:976-1081`, 106), G49-6 (`plan-A.md:1082-1089`, 8), C49-1/C49-3 (`plan-A.md:274`, `plan-A.md:289-290`, 3).

---

## S49-1 — the comparison surface

**scope** — plan-given at family level, inferred at file level. Given: the override reader (one module under `packages/descvi/src/react/overlay/`, unnamed — `plan-A.md:275`, `plan-A.md:395`); per-family records and the wiring in the four painter modules (`plan-A.md:395`, `plan-A.md:149`); the keyboard bump on the remeasure `tick` (`plan-A.md:395`); the text-entry guard in the switch handler (`plan-A.md:397`); `packages/descvi/src/vite-env.d.ts`, adding `readonly DEV: boolean` (`plan-A.md:403`); the pool-key indexing in `use-selection-rings.ts` (`plan-A.md:405`); new override witnesses, four of them, unnamed (`plan-A.md:407`); the witness list and `COVERAGE` string inside `gate-g49-3-look-witnesses.sh` (`plan-A.md:407`); `scripts/gate-g49-4-override-leak.sh` — new, no source (`plan-A.md:408`); `.github/workflows/ci.yml` two steps at the end of the gate block (`plan-A.md:411-414`). **Inferred:** which file the reader lives in; where the keydown handler is registered; the four new witness files' paths.

**completion_condition** — With no override present the rendering is byte-identical to what shipped across every family the phase touches, spacing and padding included, with G49-3's widened witness list green and unedited; with an override present each §7 candidate value renders in the live canvas and switches from the keyboard mid-gesture; the ring's spatial A/B renders two candidate values on two pooled siblings in one viewport; and `sh scripts/gate-g49-4-override-leak.sh` is green across both `dist-designview/` and `dist/`, including its leg-0 source pin, having been shown red with the guard removed and that red output recorded in the commit message (`plan-A.md:423`). The override key is exactly the literal `descvi-look-override`, written once, not assembled (`plan-A.md:399`, `plan-A.md:302`), and leg 0 excludes `__tests__` so witnesses use the reader's exported setter rather than naming the key (`plan-A.md:401`).

**verification_path**
- `sh scripts/gate-g49-4-override-leak.sh` with no arguments — builds both bundles itself; three legs, exit 0/1/2 (`plan-A.md:848`, `plan-A.md:852`, `plan-A.md:856-860`)
- `sh scripts/gate-g49-4-override-leak.sh --selftest`, no build (`plan-A.md:412`, `plan-A.md:910`)
- `sh scripts/gate-g49-3-look-witnesses.sh` with the widened list (`plan-A.md:407`)
- `sh scripts/gate-g49-5-one-home.sh` — four red rows become green (`plan-A.md:425`)
- Red demonstration: delete the `import.meta.env.DEV` guard, re-run, the literal must be found (`plan-A.md:972`)
- Manual, in `descvi:dev`: candidate switching mid-gesture and the spatial A/B (`plan-A.md:423`) — no command exists for these

**invented**
1. **Which parameter the `[`/`]` keys cycle, and how the operator changes families.** C49-2 rules the channel is "previous candidate / next candidate" on the bare brackets (`plan-A.md:280`) and S49-P tests exactly that. But the surface covers four families and at least five fields (`plan-A.md:991-997`) plus the §7 candidate lists (`plan-A.md:1124-1130`). Nothing in the plan says how the owner selects *which* field is being cycled, whether the candidate index is shared across families, or what happens at the ends of a list. This is the surface's primary control and it is unspecified.
2. **How the owner knows which candidate is showing.** The whole deliverable is a judgement instrument (`plan-A.md:43`) and the mid-phase artefact is a table the owner fills by candidate number (`plan-A.md:1122-1130`), yet no readout, label or indicator is specified anywhere. Without one the owner records numbers from memory — the instrument the plan says already failed three times (`plan-A.md:43`).
3. **The override's transport.** "a `localStorage` / `window` key" (`plan-A.md:302`) — the slash is doing real work: `localStorage` survives a reload and is readable across tabs, `window` does not and is not. It also decides what the exported setter (`plan-A.md:401`) writes and whether a candidate can persist into a session the owner did not intend.
4. **The primary ring's identity for the spatial A/B.** "the primary needs a sentinel identity or the list indexes from the secondaries alone" (`plan-A.md:405`) — two designs, executor's pick, and they differ in whether a two-element selection can show two candidates at all (only one of the two nodes carries `data-dsh-ring-key`, `plan-A.md:124`).
5. **How the key reaches the writer.** "either as a fourth argument at its two call sites or … read back off the node" (`plan-A.md:405`) — explicitly left open, and the docblock warns that a fork of the writer is what the structural gate counts (`plan-A.md:405`).
6. **Whether the reorder thickness becomes a record field.** D49-2's mechanism says each family exposes a record and "no painter reads a bare literal" (`plan-A.md:149`, C49-1 at `plan-A.md:274`), while G49-5 pins the reorder home as `export const REORDER_INDICATOR_THICKNESS_PX =` and marks it green today (`plan-A.md:997`). A worker who wraps it in a record turns that gate row red on a correct change.
7. **The four override witnesses' content and location** (`plan-A.md:407`) — one per family, including "the phase's FIRST assertion on the glyph", against "the real renderer, not a helper that re-implements the merge" (`plan-A.md:821`). Nothing names the harness they run in.
8. **G49-4's script source**, as above — with the additional burden that its selftest must stage a fixture bundle carrying page chunks and no overlay entry (`plan-A.md:944`) and assert its own two-bundle default set (`plan-A.md:926`).

**would_ask**
- What is the surface's control model — how does the owner select which field the brackets cycle, and how is the current candidate shown on screen?
- `localStorage` or `window`?
- Does the reorder thickness move into a record (D49-2 mechanism 1) or stay a bare export (G49-5 row 5)?
- Is the spatial A/B a hard requirement of this story's done-when, given the primary ring carries no pool key and S49-P does not test the pooled path?

**one_round** — **no; split into three.** Files in scope: ≥12 (reader module, 4 painter modules, `use-selection-rings.ts` indexing, `OverlayShell.tsx` keydown, `vite-env.d.ts`, 4 witness files, `gate-g49-3-*.sh` edit, `gate-g49-4-*.sh` new, `ci.yml`). Distinct acceptance claims: 5 (`plan-A.md:423`), of which two — live keyboard switching and the spatial A/B — have no automated check at all. Gates to implement and drive RED: 1 new script with 3 legs plus a selftest, plus a widening of an existing script, plus 4 new assertions. Evidence gates to run: G49-3, G49-4 + selftest (two Vite builds, ~4.7 s each per `plan-A.md:419`), G49-5, plus a manual browser pass. Split: **(1)** the override reader, records and painter wiring behind the DEV guard, with G49-4 and its CI wiring; **(2)** the keyboard channel and the text-entry/IME guard; **(3)** the ring's pool-key indexing and the spatial A/B, which is the leg the plan itself says was not renderable one revision ago (`plan-A.md:120`).

**reading_cost** — ~400 lines: S49-1 (`plan-A.md:393-428`, 36), D49-1 (`plan-A.md:81-131`, 51), D49-2 (`plan-A.md:132-153`, 22), C49-2 and C49-8 (`plan-A.md:275-288`, `plan-A.md:296-304`, 23), G49-4 (`plan-A.md:837-975`, 139), G49-3 (`plan-A.md:708-836`, 129, for the witness table it must widen). Plus register rows U-11, U-12 (`plan-A.md:1229-1230`).

---

## S49-2 — `reorder-indicator-look`

**scope** — plan-given: `packages/descvi/src/react/overlay/canvas/reorder-paint.ts`, the thickness constant and the cross-axis extent rule (`plan-A.md:431`). Gate move touches `packages/descvi/test/reorder/reorder-paint-geometry.test.ts` (the `toBeLessThanOrEqual(2)` bound and three extent literals) and `packages/descvi/src/react/overlay/__tests__/reorder-paint.test.tsx` (`plan-A.md:437-439`). The e2e tree is explicitly excluded (`plan-A.md:442`).

**completion_condition** — Two commits under C49-5 (`plan-A.md:292`): a contract-and-gate commit that moves the bound and the extent literals with no pixel changed, then a value commit that edits no gate and ships the owner's U49-1 weight and U49-2 length rule, defaulting to 2 px and members' cross-axis extent if the row is deferred (`plan-A.md:446`, `plan-A.md:448`). After the value lands, the amended gate is re-run and shown RED on this story's named mutation — the thickness **raised** or the extent literals moved — with that RED output recorded beside the value commit; a story that cannot produce one does not close (`plan-A.md:446`).

**verification_path**
- `pnpm vitest run packages/descvi/test/reorder/reorder-paint-geometry.test.ts` with the constant raised 2 → 3; expect **one** failing test, not three, because all three bound rows sit in one `it()` (`plan-A.md:745`, `plan-A.md:827`)
- Lowering to 1 is green — the bound is one-sided, executed as a control (`plan-A.md:438`, `plan-A.md:793-803`)
- `sh scripts/gate-g49-3-look-witnesses.sh` for the family's witnesses (`plan-A.md:818`)

**invented**
1. **The observation sheet.** The story "carries U49-C's observation question" (`plan-A.md:448`) and the owner ruled U9(E) onto "the S49-2 observation sheet" (`plan-A.md:1116`). No such artefact is defined anywhere — no file, format or owner. Also, the gap-0 demonstration is an obligation on the executor ("the owner should be shown a gap-0 parent at each candidate weight", `plan-A.md:444`) with no acceptance criterion.

**would_ask**
- What is the observation sheet and where does it live?

**one_round** — **yes.** Files: 3 (one source, two test files). Distinct acceptance claims: 3 (contract commit moves no pixel; value commit edits no gate; amended gate shown red on the raised thickness). Gates to implement and drive RED: 0 new, 1 amended and one RED transcript. Evidence gates to run: 2. One worker, two commits, one review round.

**reading_cost** — ~67 lines: S49-2 (`plan-A.md:429-449`, 21), C49-5 including the regime ruling (`plan-A.md:292-293`, 2), G49-3's RED-when table (`plan-A.md:823-835`, 13), G49-7 (`plan-A.md:1090-1097`, 8), §7's U49-1/U49-2 rows and the U49-2 note (`plan-A.md:1124-1125`, `plan-A.md:1139`, 3), U49-C (`plan-A.md:1116`, 1).

---

## S49-3 — `selection-ring-treatment`

**scope** — plan-given: the record from S49-1a (`plan-A.md:452`), and four assertion sites — `OverlayShell-selection-set.test.tsx`, `OverlayShell-canvas-hover.test.tsx`, `OverlayShell-hover-channels.test.tsx`, and `resize-handle-layer.test.tsx` for a shade change only (`plan-A.md:456-460`). All four exist in `base/`.

**completion_condition** — A contract commit re-expresses the four assertion sites against the named constants with values unchanged and no pixel moved; the value commit edits no gate and ships the owner's U49-3 radius and U49-4 triple, defaulting to radius 6 / selection 2.5 / hover 1.5 if deferred; the amended gate is then shown RED on a radius or width move in either direction, both being exact pins, with that RED recorded beside the value commit; and G49-6 is green throughout, because a width change that decoupled the two radii would pass every row in the list (`plan-A.md:462`, `plan-A.md:470`, `plan-A.md:472`). Any hover-vs-selection size change is made on the **hover** side, because `e2e/multi-select-shield.spec.ts` compares the selection ring's bounding box to the element's box under `Math.round` with no tolerance (`plan-A.md:468`).

**verification_path**
- The four assertion files, run unedited in the contract commit (`plan-A.md:456-460`)
- `sh scripts/gate-g49-3-look-witnesses.sh` — per-field RED directions at `plan-A.md:829-832`; note the hover-width row is a `toContain` and is green on any value containing `1.5` (`plan-A.md:832`)
- G49-6 green throughout (`plan-A.md:470`)
- Not run by the plan and marked unverified: `pnpm test:e2e e2e/multi-select-shield.spec.ts` with the ring inflated (`plan-A.md:1223`)

**invented**
1. **What the spatial A/B actually renders here.** The story says the ring takes its decision on the spatial staging, "two pooled siblings at two candidate widths in one viewport" (`plan-A.md:464`), but the mechanism lives in S49-1 and the plan itself records that only pooled secondaries carry `data-dsh-ring-key` while the primary carries none (`plan-A.md:124`, `plan-A.md:405`). Whether a two-element selection yields two distinct candidate renderings depends on a design decision S49-1's executor makes. I would have to tell this worker which.
2. **Site 4 is dead scope.** The chip border is listed as an assertion site "for a shade change only" (`plan-A.md:460`) while `plan-A.md:472` states no §7 candidate changes the `deep` shade. A worker will re-express an assertion nothing in this story can move.

**would_ask**
- Does S49-1's ring indexing support a two-candidate render on a primary+secondary selection, or only among secondaries? The story's chosen decision instrument depends on it.

**one_round** — **yes, with the question answered.** Files: 5 (the record plus four test files). Distinct acceptance claims: 4 (contract commit re-expresses four sites with no pixel moved; value commit edits no gate; amended gate red in either direction; G49-6 green throughout). Gates to implement and drive RED: 0 new, 1 amended, 1 RED transcript. Evidence gates to run: 2 plus one e2e spec the plan never executed (`plan-A.md:1223`). If the answer to the spatial-A/B question is "not supported", the story becomes a decision-instrument change and I would split the staging out.

**reading_cost** — ~95 lines: S49-3 (`plan-A.md:450-473`, 24), D49-1's spatial-staging box (`plan-A.md:120-128`, 9), C49-3, C49-5, C49-7 (`plan-A.md:289-290`, `plan-A.md:292-293`, `plan-A.md:295`, 6), G49-3's per-field and RED-when tables (`plan-A.md:813-835`, 23), G49-6 (`plan-A.md:1082-1089`, 8), G49-7 (8), §7's U49-3/U49-4 rows (`plan-A.md:1126-1127`, 2), PM-8 (`plan-A.md:1187`, 1), U-6/U-13 (`plan-A.md:1223`, `plan-A.md:1231`, 2).

---

## S49-4 — `spacing-affordance-mark`

**scope** — plan-given: `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts` — `figureFor`, the `SPACING_GLYPH_PATHS` record, and "the reveal predicate" (`plan-A.md:476`). **Inferred:** the reveal half "moves when affordances are placed at all, which touches the hit model" (`plan-A.md:478`) — no file or function is named for the placement pass, and the plan instructs the worker to build the rest of the lands list by grepping the e2e tree before writing it (`plan-A.md:486`, PM-5 at `plan-A.md:1184`).

**completion_condition** — Two independently deferrable halves (`plan-A.md:478`): U49-5a replaces the two per-edge arrow icons with one `-` mark per edge; U49-5b changes the reveal to fire when the pointer is inside the object. Either may ship alone; the deferred one keeps its shipped value (`plan-A.md:490`). `SPACING_GLYPH_PX` stays at 8 (`plan-A.md:484`). The `<svg>` and the C46-1 `glyph-conditional` obligation survive (`plan-A.md:482`). G49-7's obligation is discharged by showing the override witness S49-1 landed RED on a mutation of the emitted `d`; if S49-1 did not land that witness, the story is blocked rather than shipped (`plan-A.md:488`).

**verification_path**
- `e2e/spacing-gesture.spec.ts` — asserts DOM presence and the 8 px hide threshold, not the path data (`plan-A.md:482`, `plan-A.md:484`)
- G49-3's spacing/padding override witness, shown RED on a `d` mutation (`plan-A.md:488`, `plan-A.md:819`)
- A grep of the e2e tree for strip and apron roles, run *before* the lands list is written (`plan-A.md:486`)

**invented**
1. **The reveal predicate's semantics.** The kickoff and the backlog ask for "reveal when the pointer is *inside* the object", and the plan restates that and stops (`plan-A.md:478`). Inside which box — the element's border box, its padding box, the strip's own hit region? What happens on nested declaring nodes, where more than one object contains the pointer? What replaces the current strip-hover trigger for edges the pointer is not near? This is a behaviour change to the hit model with no acceptance criterion anywhere in the plan, and no gate: the only named evidence is a `d`-mutation witness (`plan-A.md:488`), which tests the mark, not the reveal.
2. **The new mark's path data.** "one `-` mark per edge" — the actual `d` strings are the deliverable and are not given (`plan-A.md:476`).
3. **The lands list itself.** The plan delegates its construction to the executor's grep (`plan-A.md:486`), which is scope inference by design.

**would_ask**
- What exactly does "pointer inside the object" mean, and what is the acceptance check for the reveal half? As written the expensive half of the story has neither a specification nor a gate.
- Did S49-1 land the glyph `d` witness? The story blocks on it (`plan-A.md:488`).

**one_round** — **split**, along the plan's own seam. The mark half: 1 file, 2 acceptance claims, 1 witness to drive RED — one sitting. The reveal half: an unbounded number of files (the placement pass, the hit model, and whatever the e2e grep turns up), 0 gates, and no stated completion condition. Splitting is also what the owner table already assumes, since U49-5a and U49-5b are separate rows (`plan-A.md:1128-1129`, `plan-A.md:1133`).

**reading_cost** — ~55 lines: S49-4 (`plan-A.md:474-491`, 18), G49-3's spacing row (`plan-A.md:819`, 1), G49-7 (8), C49-5 (2), S49-1's witness Lands item (`plan-A.md:407`, 1), §7's U49-5a/5b rows and note (`plan-A.md:1128-1129`, `plan-A.md:1133`, 3), PM-5 (`plan-A.md:1184`, 1). The kickoff's own backlog row is the only source for the reveal's intent, which is outside the plan.

---

## S49-5 — `padding-glyph`

**scope** — plan-given: two entries in `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts`, `"pad-x"` and `"pad-y"` (`plan-A.md:494`).

**completion_condition** — The two arrow-up-to-line paths become plain directional bars — `-` on horizontal edges, `l` on vertical (`plan-A.md:1130`). No contract-first split is performed, because the path strings occur nowhere outside their module and no gate asserts them (`plan-A.md:496`). What the story owes instead is the override witness on the emitted `d` shown RED on the old figure and GREEN on the new, plus the C46-1 obligation confirmed intact — still an `<svg>` with a path, still hidden below `SPACING_GLYPH_PX`, still declared `glyph-conditional` (`plan-A.md:498`). If U49-6 is deferred, the story **executes the standing direction anyway** — the one row whose deferral default is change rather than status quo (`plan-A.md:500`).

**verification_path**
- `grep -rIn -e 'M4 4v8' -e 'SPACING_GLYPH_PATHS' e2e packages src | grep -v use-spacing-affordances` → empty, with the grep shown non-zero before the exclusion (`plan-A.md:496`, `plan-A.md:1222`)
- The G49-3 spacing/padding override witness, RED on the old `d` and GREEN on the new (`plan-A.md:498`)
- `e2e/spacing-gesture.spec.ts` for the C46-1 obligation (`plan-A.md:482`)

**invented**
1. **The two replacement path strings.** The direction is decided; the `d` data is not written anywhere in the plan (`plan-A.md:494`, `plan-A.md:1130`), and it is the entire deliverable.

**would_ask** — none. The one gap is a drawing decision a worker can make and the owner confirms on the surface (`plan-A.md:500`).

**one_round** — **yes.** Files: 1 source file plus the shared override witness. Distinct acceptance claims: 3 (new figure ships; witness red-then-green; C46-1 obligation intact). Gates to implement: 0. Evidence gates to run: 2. Smallest story in the phase.

**reading_cost** — ~45 lines: S49-5 (`plan-A.md:492-501`, 10), G49-3's spacing row and the "no default witness exists" note (`plan-A.md:819`, 1), G49-7 (8), the S49-4 box on `SPACING_GLYPH_PX` (`plan-A.md:484`, 1), §7's U49-6 row (`plan-A.md:1130`, 1), U-5 (`plan-A.md:1222`, 1), plus S49-1's witness item (`plan-A.md:407`).

---

## S49-6 — the reorder arming threshold (optional rider)

**scope** — `packages/descvi/src/react/overlay/canvas/pointer-thresholds.ts` plus three hard pins, a regime tripwire, G47-3's diagonal control, two e2e sub-threshold rows, and two hand-added pins for the stale-green copies `handle-geometry.test.ts`'s `PURCHASE_FLOOR_PX` and `e2e/resize-handles.spec.ts`'s `4 px floor` literal, which land FIRST (`plan-A.md:504`, `plan-A.md:1112`).

**completion_condition** — Not dispatchable: **U49-B was ruled NO by the owner on 2026-09-04** and U49-7 is struck from the table (`plan-A.md:1107`, `plan-A.md:1131`). Recorded here because §5 still carries the story. If it were taken: the two new pins exist and have been shown RED by editing the constant, the chosen value ships, G47-3 has been shown RED at a value it should reject, and the value is inside the reachable box derived in U49-B — `[3, 4.243]`, i.e. 3 px is the only alternative to the shipped 4 (`plan-A.md:506`, `plan-A.md:1115`).

**verification_path** — Change `POINTER_DRAG_THRESHOLD_PX` and run the full suite; the two stale-green files must stay green while others go red (`plan-A.md:1225`) — the register flags this as an unexecuted negative claim, the shape most likely to be wrong.

**invented** — none; the story is not dispatched.

**would_ask** — none.

**one_round** — **not dispatched.** Were it live: **no** — a shared five-gesture constant, 8+ pinned sites, two pins that must land before anything is safe to change, and the plan itself calls it "not a rider on a look phase; it is a small phase" (`plan-A.md:1115`).

**reading_cost** — ~35 lines if taken: S49-6 (`plan-A.md:502-514`, 13), U49-B (`plan-A.md:1107-1115`, 9), the U49-7 box (`plan-A.md:1131`, `plan-A.md:1135-1137`, 4), U-8 (`plan-A.md:1225`, 1).

---

## Closing

### Dispatch state

| story | today, no question | needs one question | not dispatchable as written |
|---|---|---|---|
| S49-0 | — | script provenance | — (split first) |
| S49-P | ✅ (runner needs a browser + Korean IME) | where the result is recorded | — |
| S49-1a | — | z fields; G49-6's file | — (split first) |
| S49-1 | — | — | ✅ |
| S49-2 | ✅ | observation sheet | — |
| S49-3 | — | the spatial A/B's reachability | — |
| S49-4 (mark) | ✅ | — | — |
| S49-4 (reveal) | — | — | ✅ |
| S49-5 | ✅ | — | — |
| S49-6 | ruled NO (`plan-A.md:1107`) | | |

**S49-1 is the one I could not dispatch.** Not because of the gate work, which is merely large, but because the surface's control model is absent: nothing says how the owner selects which field the `[`/`]` keys cycle across four families and five-plus fields (`plan-A.md:280`, `plan-A.md:991-997`, `plan-A.md:1124-1130`), and nothing specifies a readout telling the owner which candidate is on screen. The plan's own first principle is that the deliverable is a judgement instrument (`plan-A.md:43`); the instrument's interface is the piece it does not describe.

**S49-4's reveal half is the second.** "Reveal when the pointer is inside the object" is restated, never specified, and the only evidence named for the story is a `d`-mutation witness that tests the mark instead (`plan-A.md:478`, `plan-A.md:488`).

### Material decisions parked for the owner

| decision | lines | can a worker proceed without the answer? |
|---|---|---|
| U49-1 reorder weight | `plan-A.md:1124` | Yes — the contract/gate commit lands first and the shipped 2 px is the deferral default (`plan-A.md:448`, C49-6 at `plan-A.md:294`) |
| U49-2 length rule | `plan-A.md:1125` | Yes, same mechanism |
| U49-3 ring radius | `plan-A.md:1126` | Yes — contract commit re-expresses the pins at unchanged values (`plan-A.md:462`) |
| U49-4 ring width + hover relation | `plan-A.md:1127` | Yes for the contract commit; **no** for the value commit — triples (3) and (4) move the hover inflation, which moves `OverlayShell-hover-channels.test.tsx`'s exact rows (`plan-A.md:458`) |
| U49-5a mark | `plan-A.md:1128` | Yes |
| U49-5b reveal | `plan-A.md:1129` | **No** — and not only for the owner's answer: the plan does not specify the behaviour either (`plan-A.md:478`) |
| U49-6 pad glyph | `plan-A.md:1130` | Yes — it does not block on the owner at all and executes the standing direction on deferral (`plan-A.md:170`, `plan-A.md:500`) |
| U49-A surface form | `plan-A.md:1104` | Answered — ruled (b), reopens only through S49-P's abort |
| U49-B rider | `plan-A.md:1107` | Answered — NO; S49-6 does not run |
| U49-C the `n / N` readout | `plan-A.md:1116` | Answered — observation sheet, but the sheet is undefined (S49-2 above) |
| KI-47, phase-47 items (ii)/(iii) | `plan-A.md:57`, `plan-A.md:1200` | Yes — explicitly out of scope, no worker touches them |

The deferral machinery itself is sound: every row's shipped value is one of its candidates (`plan-A.md:166`) and C49-6 lets each story land its gate move regardless (`plan-A.md:294`), so a silent owner costs rows and not the phase.

### What would make a worker do wasted work

**1. Text addressed to reviewers, not executors — the dominant cost.** The status block is 36 lines of revision archaeology: lane verdicts across r0…r5 (`plan-A.md:9-10`), a twelve-item list of "things this plan reverses" (`plan-A.md:25-37`), and a table of which gates are red on the tree today with why each red is correct (`plan-A.md:14-23`). Every gate opens with a history of the forms that could not work — `plan-A.md:539-548`, `plan-A.md:839-847`, `plan-A.md:978`. Every gate then pastes session transcripts as evidence: `plan-A.md:585-707` (G49-2), `plan-A.md:714-836` (G49-3), `plan-A.md:864-975` (G49-4), `plan-A.md:1005-1081` (G49-5) — roughly 470 lines, a third of the plan, recording what one machine printed on one tree. An executor needs the RED-when and the verdict semantics; the r4'-vs-r5 selftest narrative (`plan-A.md:527`, `plan-A.md:770-791`, `plan-A.md:926-970`) is a record of the planning loop.

**2. Repeated constraints.** The `dist/` reversal is stated in full at `plan-A.md:28`, `plan-A.md:298`, `plan-A.md:862`, `plan-A.md:892`, `plan-A.md:1143`, `plan-A.md:1180` and `plan-A.md:1229` — seven times, each several lines. The PM-10 census-roots story appears at `plan-A.md:32`, `plan-A.md:209`, `plan-A.md:226`, `plan-A.md:315` and `plan-A.md:1189`. The CI-step formatting rule (6/8 indentation, single-line `run:` scalar) is repeated verbatim at `plan-A.md:326`, `plan-A.md:383` and `plan-A.md:417`. The hover-width `toContain` weakness appears at `plan-A.md:389`, `plan-A.md:459`, `plan-A.md:817`, `plan-A.md:832` and `plan-A.md:1231`. The plan's own one-home rule (`plan-A.md:24`, `plan-A.md:508`) is the rule it breaks most.

**3. Gates guarding things no story changes.**
- **G49-2 leg (c)** validates markdown fragment resolution across the whole repo (`plan-A.md:558`, `plan-A.md:566`). Nothing S49-0 does creates or repairs a fragment; the leg's first find was a dead fragment in *this plan's own §1* (`plan-A.md:1212`). It is a repo-wide citation-corpus gate wired into CI on the back of a docs move, and its documented false negative (`plan-A.md:568`) means it does not even guarantee what its name says.
- **G49-5 row 5** (reorder thickness) is green today and has no bare form to forbid (`plan-A.md:997`); no story changes its home. It is enumerated so that the gate can pass a row.
- **G49-3's spacing/padding default witness** is named as covering the family while the plan states in the same table that it contains no glyph, `svg`, `path` or `d` assertion (`plan-A.md:819`) — so for S49-4 and S49-5 it guards nothing until S49-1's override witness lands.
- **S49-3's fourth assertion site** (the chip border) is scoped "for a shade change only" (`plan-A.md:460`) while `plan-A.md:472` rules that no candidate changes the shade.
- **S49-6** occupies 13 lines of §5 plus its derivation in U49-B (`plan-A.md:1107-1115`) and the struck table row (`plan-A.md:1131-1137`) for a story the owner ruled out (`plan-A.md:1107`). A worker reading §5 in order reads a story that will not run.

**4. The largest single item of unbudgeted work is not marked as work.** Four shell gates with selftests that stage `mktemp` fixtures, assert their own enumerations, emit three exit codes and produce specific row prefixes must be *written* by executors from transcripts (`plan-A.md:317`, `plan-A.md:370`, `plan-A.md:408`), while the plan's prose consistently reads as though they already exist ("THE COMMITTED FILE, INVOKED BY PATH", `plan-A.md:585`, `plan-A.md:714`, `plan-A.md:864`, `plan-A.md:1005`). Every measured cost the plan quotes — 0.56 s, 2.9 s, 0.34 s, 4.80 s (`plan-A.md:328`, `plan-A.md:330`, `plan-A.md:419`) — is a run cost. None is an authoring cost.
