# E3 v3 — On-canvas direct manipulation

Status: Draft
Status reason: Drafted (phase: drafted). Planner first draft complete; not yet reviewed — awaiting round-1 fresh Architect and Critic lanes.

---

## 0. What this plan is, and what it is not

This turns the completed three-lane spike (`.omc/spikes/e3-v3-handles/synthesis.md`, sha256 `bc5fabe761dff57030db4498c4bce95c1dc47266cb2cb924b2cac8b5219aa9a6`) into an executable ladder. The approach questions are **closed** — this plan does not re-survey them. What it does is resolve the five decisions the spike handed over, amend the interaction ontology's v3 row to match what Lane B falsified, and phase the work with gates that can go RED.

**Not in scope, deliberately:** absolute positioning (v4), the screen-tab/code-tab HTML-first horizon recorded in the spike README (v3 must neither foreclose nor build toward it), the `_scratch`/E4 track-3 conflict (Open Question OQ-1 below — owner ruling, not this plan's job), and KI-10's shared-oid ring disposition (STOP AND REPLAN stands; this plan routes around it rather than deciding it).

**Deliverable scope is `packages/**`.** `src/app/**` changes exist only to verify an example end-to-end.

**Engine invariant:** v3 is a UX-only version. Every gesture compiles to a v1 attribute (`className`) write through the already-shipped path. No new engine class, no new write verb, no schema change.

---

## 1. Inputs and their authority

| Input | Tier | What it settles |
|---|---|---|
| `.omc/spikes/e3-v3-handles/synthesis.md` | verdict set | the six verdicts; open items 1–6 |
| `.omc/spikes/e3-v3-handles/lane-b-figma-checklist.md` | **LIVE-B** (owner, real Figma, macOS 2026-08-15/16) | gesture semantics in auto-layout; the alignment falsification |
| `.omc/spikes/e3-v3-handles/lane-c-probe.md` + `.patch` | **LIVE-C** (in-repo, real Chromium, 4 drag→commit cycles) | integration risk; the shield swallow; the post-commit tear |
| `.omc/spikes/e3-v3-handles/lane-a-onlook.md` | **READ-A** (Onlook @ `423e2e9`, tldraw @ `68fc38b`) | precedent shapes; the preview/commit divergence cautionary tale |
| Owner rulings (spike README + brief) | binding | Q1 write vocabulary; Q2 auto-layout default; Q4 v3.x must complete the row; Verdict-6 effort allocation |
| Repo source, re-read while writing this plan | ground truth | every anchor below |

**Where a lane and the repo disagree, the repo wins and this plan says so out loud** (see §6, D6-b: Lane A's "the shield needs zero changes" is architecturally inapplicable here).

---

## 2. Principles

1. **One serializer, one write path.** Exactly one module turns intent (Fixed 347px / Hug / Fill / align / gap) into a Tailwind token, and exactly one code path commits it. Onlook's live bug — panel-Hug writes `0px` where the canvas double-click writes `fit-content` — is what two entry paths for one concept costs (READ-A, `lane-a-onlook.md` Q5).
2. **The panel is the trunk; gestures are the rough-in.** Owner's own Figma usage and Onlook's shipped gating agree: flow elements get panel sizing, drag roughs it in (LIVE-B §5, READ-A `shouldShowHandles && isAbsolutelyPositioned`). Effort follows that, not gesture fidelity.
3. **Figma vocabulary for sizing intent, CSS vocabulary for structure.** Hug/Fill/Fixed on the sizing tri-state; Flex/Direction/px/`justify`/`items` for structure. One React+Tailwind precedent already chose exactly this split.
4. **A gesture never invents a coordinate.** v3 is flow-only. There is no x/y, no free-form rect, no marquee geometry. Anything whose meaning requires an anchor coordinate belongs to v4 and is cut here rather than approximated.
5. **Refuse loudly rather than guess.** Non-editable targets, shared-oid instances, and non-flex parents get a visible refusal with a reason, not a handle that writes somewhere surprising. This is the same discipline the shipped chip editor already uses for `dynamic-class`.

---

## 3. Top three decision drivers

1. **Write-path singularity** — the cost of a second serializer is silent divergence between what the user sees and what lands in source, and it is expensive to find. This drives D2, the parked-panel disposition, and a new RED-able caller gate.
2. **Flow honesty** — descvi's containers are auto-layout by owner ruling (Q2). Semantics that only exist in free-form (invert-below-zero, distribute, marquee-then-align, center-resize) must be cut or re-expressed, not ported.
3. **Reversibility of the slice** — v3.0 must be independently shippable and dogfoodable (roadmap sequencing principle 2), so the cut line is drawn where the panel is useful without any handle, and the handle is useful without gap/padding drag.

---

## 4. Options considered where a real choice remained

The spike closed the approach. Three sub-choices were genuinely open and are compared here; everything else is a verdict, not an option.

### 4.1 Where the handle layer mounts

| Option | Benefit | Cost | Verdict |
|---|---|---|---|
| **A. Inside `#dsh-ring-layer`, with a shield bypass** | ring-relative geometry is already scroll-invariant by construction; measured working end-to-end (LIVE-C Q1/Q2) | needs a ~4-line escape hatch in the shield wiring; frame-edge clipping to manage | **CHOSEN** |
| B. A sibling layer above the shield (Onlook's pattern) | zero shield changes | **does not work here**: descvi's shield is a *native capture-phase listener on the ancestor `#dsh-stage`*, not a sibling overlay, so paint order cannot pre-empt it. A layer outside `#dsh-stage` would be viewport-pinned and go stale — the exact failure the BUG-1 architect review rejected | rejected on mechanism |
| C. Handles as children of the page element | no layer at all | mutates page DOM; re-opens the whole BUG-5 family (per-node style writes) | rejected |

### 4.2 Drag capture

| Option | Benefit | Cost | Verdict |
|---|---|---|---|
| **A. `setPointerCapture` on the handle** | measured working across select / per-move remeasure / mid-drag scroll / commit in 4/4 probe runs; hover machinery is starved for free by capture semantics | none found | **CHOSEN** |
| B. Full-screen fixed capture div (Onlook) | works across iframes | Onlook needs it because they use mouse events across an iframe boundary; descvi has neither constraint. Extra DOM, extra teardown paths | rejected — solves a problem we do not have |

### 4.3 Fill on the cross axis

Compared in D2 below, where the mechanism argument is the decision.

---

## 5. ADR — the amended v3 row

**Decision.** "Align/distribute" leaves v3's multi-select gesture family entirely. It compiles to **parent-level `justify-*` × `items-*`**, surfaced as a **3×3 widget that appears only when the selected element is itself a flex container**, writing to that same element. Marquee multi-select is cut from v3. Alt+handle center-resize is cut from v3. `Cmd/Shift-click multi-select + align/distribute` is deleted as a v3 cell.

**Drivers.** Flow honesty (driver 2); the ontology's obligation to be the canonical reference rather than a wish list; owner ruling Q4 (the v3.x series must COMPLETE the row, so a row containing falsified cells is a series that can never close).

**Alternatives considered.**
- *Per-child `self-*` on a multi-selection.* Falsified by LIVE-B: selecting auto-layout children shows no alignment control at all, and a cross-parent multi-selection shows none either. Lane A confirms the negative independently — Onlook ships no align/distribute in any form, and its only alignment UI writes `align-items`/`justify-content` on the selected container.
- *Multi-select coordinate ops (Figma "Tidy up").* LIVE-B: activates only for NON-auto-layout nodes. That is free-form territory, which is v4 by owner ruling Q2. Building it in v3 would require the coordinate model v3 does not have.
- *Keep marquee as selection-only, without align.* Viable but valueless: LIVE-B says multi-select in Figma exists mainly for batch panel edits and free-form tidy-up. Batch panel edit is a panel feature that does not need a marquee, and it is not a v3 cell. Recorded as a later, unowned candidate rather than built.

**Why chosen.** It is the only reading consistent with the one live observation the checklist called its most important item, it removes rather than adds surface, and it makes the v3 row closable.

**Consequences.**
- The alignment widget needs **no cross-oid write machinery** — Figma shows alignment on the parent when the parent is selected, so descvi's widget writes to the currently-selected element. The single-serializer invariant is preserved for free.
- `.omc/specs/interaction-ontology.md` cannot be amended in place (`.omc/` is read-only under the current harness). The living spec **migrates** — see D1.
- Marquee's cells in §3.F-7 become `deferred-v4-or-later`, not `deferred-v3`. Somebody reading the old row and building a marquee would be building a thing with no operation to perform.

**Follow-ups.** Batch panel edit over a multi-selection (Figma's actual multi-select use) is recorded as unowned in the migrated ontology, at no version.

---

## 6. Resolved decisions

### D1 — the ontology amendment and where it lands

**Migrate, do not fork.** `.omc/specs/interaction-ontology.md` moves to **`docs/reference/interaction-ontology.md`**, and the v3 amendment is made in the new copy.

Grounds:
- `.omc/` is read-only historical record; the file's own header says `Status: living reference`, and a living reference that cannot be edited is the highest-leverage stale claim a document can carry (phase-22's most portable finding).
- `docs/README.md` states the placement rule directly: `reference/` holds "one subject per file, deep", scoped to a **kind** rather than an initiative. The canvas interaction contract outlives E3's version numbering — it is exactly that shape.
- A pointer stub cannot be left behind (the source tree is read-only), so the pointers must be updated at the **reader's entry points** instead. There is exactly **one living citation** of the ontology outside `.omc/`: the Refs line in `docs/e3/tracker.md`. Everything else that mentions it (`.omc/archive/260707-e3/ralplan-e3-v15-chip-hardening.md`, the three spike files) is a frozen point-in-time record and is left alone by the `docs/README.md` convention.

**Two obligations the move creates, both of them RED-able:**
1. The ontology's References section pins code by **line number into paths that no longer exist** — `overlay/selection-shield.ts`, `overlay/ClassNameChipEditor.tsx`, `overlay/live-preview.ts`, `overlay/utility-source.ts` all moved into `canvas/`, `panel/`, `engine/` subfolders in the phase-11 decomposition. These convert to anchors during the move. `node scripts/check-citation-anchors.mjs` leg (b) treats a non-existent cited path as a violation, so a converted anchor is machine-checked where the line pin never was.
2. `docs/README.md` gains a `reference/` row, and `docs/e3/tracker.md`'s Refs line is re-pointed. Both are doc commits of their own.

**The exact amendment** (all of it in the migrated copy):

| Section | Change |
|---|---|
| §6 v3 row, cells | Replace `resize/gap/padding handle-drag; Shift+resize aspect-lock; Alt+handle center-resize; marquee multi-select; Cmd/Shift-click multi-select + align/distribute` with: `resize handle-drag (edge + corner, per-axis) → Fixed conversion on first size change; sizing tri-state (Hug/Fill/Fixed) panel + edge-double-click gestures; parent 3×3 alignment widget → justify-* × items-* on the selected flex container; gap/padding affordance (drag + integrated numeric popup); Shift+resize aspect-lock` |
| §3.F-4, handle row | Shift+resize aspect-lock stays `deferred-v3`, annotated LIVE-B: works on **edges as well as corners**, diagonal indicator during lock, releasing Shift mid-drag unlocks |
| §3.F-5, handle row | Alt+handle center-resize: `deferred-v3` → **`deferred-v4`**, with the LIVE-B reason (it technically works in auto-layout but degenerates to normal resize UX because growth follows alignment — meaningless without a free coordinate) |
| §3.F-6 | Resize/gap/padding rows keep `deferred-v3` and gain the LIVE-B semantics: drag converts the axis to Fixed **at the first size change** (not pointerdown, not release); siblings reflow live; gap `Auto` (`justify-between`) + handle drag forces back to a numeric `gap-[..]` |
| §3.F-7 marquee | `deferred-v3` → **`deferred-v4-or-later`**, with the falsification recorded: Figma's marquee-plus-align is free-form-only, and the auto-layout analog of distribute is the parent's gap `Auto` |
| §3.A / §5-C1 | Shift-click add-to-selection: the C1 overload note stays, but the "v3 multi-select" gate reference is removed — nothing in v3 consumes a multi-selection |
| §3.B | Add a note that a `dblclick` on a **handle** is a distinct target-type from the reserved element `dblclick` (v1.9's TRIGGER NOTE reservation), so the v3.2 edge-double-click gestures do not collide with it |
| Header | The `Branch context: feat/phase-8-e3-v1-visual-editing` line and the `Date` line are updated to record the migration; the `Supersedes` line gains the `.omc/specs/` original |

**Row-closure criterion** (this is what makes owner ruling Q4 checkable): the v3 row is COMPLETE when every cell in the amended row is SHIPPED or explicitly reclassified to another version, and no cell remains `deferred-v3`. Phase-43 is the phase that must produce that state.

### D2 — Fill write mapping per axis, and the single-serializer requirement

**The mapping.**

| Sizing state | Main axis of the parent | Cross axis of the parent |
|---|---|---|
| **Fixed** | `w-[347px]` / `h-[52px]` — **always an explicit unit, never a bare number** | same |
| **Hug** | `w-fit` / `h-fit` | same |
| **Fill** | `flex-1` | **`self-stretch`** |

Grounds for the cross-axis choice (`self-stretch` over `w-full`/`h-full`):
- A percentage size resolves against a **definite** parent size. `self-stretch` does not need one. In a `flex-row` parent the cross axis is height, and `h-full` against an auto-height parent resolves to nothing while `self-stretch` still stretches. Choosing the token that works in both parents is not a preference, it is the only one of the two that is correct in both.
- One token covers both cross-axis cases (width in a column parent, height in a row parent), which halves the vocabulary the serializer and the read-back parser must agree on.
- `w-full`/`h-full` remain legal in the corpus and must still **read back** as Fill; they are simply never **written**.

Grounds for "always an explicit unit": `utilityFor` in the existing model snaps a bare number to a scale token — `packages/descvi/src/react/overlay/engine/tailwind-class-model.ts#export function utilityFor(prefix: string, value: string): string {` matches `/^\d+(\.\d+)?$/` first, so `347` becomes `w-347`, not `w-[347px]`. That directly contradicts owner ruling Q1. The serializer therefore takes a value **with its unit** (`347px`), which the same function already turns into `w-[347px]` — the existing test file pins exactly this pair. Scale tokens surface later, as a variables-like preset concept, and never as a snap target.

**Two defects in the parked model that this decision forces us to fix rather than inherit:**
- `packages/descvi/src/react/overlay/engine/tailwind-class-model.ts#state.width = { mode: "fill", value: null };` maps `flex-1` unconditionally to **width** fill. In a `flex-col` parent, `flex-1` grows the **height**. The read-back must route by the parent's flex axis, not assume width.
- `packages/descvi/src/react/overlay/engine/tailwind-class-model.ts#function stripSizingAxis(className: string, axis: "w" | "h"): string {` strips `w-*`/`h-*`/`flex-1`/`grow` but knows nothing about `self-*`. Adopting `self-stretch` as a sizing token means the strip set for the cross axis must include it, or Hug-after-Fill leaves both tokens standing.

**The single-serializer requirement, concretely.**
- One module owns intent → token for every v3 write: sizing tri-state, alignment, gap, padding. Nothing else composes a Tailwind sizing/alignment/spacing token.
- Every entry path — drag preview, drag commit, panel commit — goes through the **already-shipped** preview controller: `packages/descvi/src/react/overlay/engine/live-preview.ts#selectedEl.className = composeChips(chips);` for preview and its `commit()` for the POST. The composition boundary is `packages/descvi/src/react/overlay/engine/classname-tokenizer.ts#export function composeChips(chips: string[]): string {`, which is already documented as "BOTH the live-preview `el.className` string AND the committed POST `newClassName`". v3 adds token producers **above** that boundary and moves the boundary nowhere.
- **The second serializer already exists and is dormant.** `packages/descvi/src/react/overlay/panel/parked/PropertyPanel.tsx#import { composeClassName, parseClassName } from "../../engine/tailwind-class-model";` calls `applyClassNameEdit` directly, bypassing the preview controller entirely. v3's panel widgets mount on the **chip session**, not on the parked panel. The parked tree stays compiling and green (it is dormant, not dead, by its own header) but is never the mount point.
- **New gate, RED-able:** extend `packages/descvi/src/react/overlay/__tests__/write-coordinator-callers.test.ts#describe("C4 ordinary caller coordinator reachability", () => {` with the negative half it currently lacks. Today it asserts a positive topology (this file contains that call); it would not notice a second live caller. The new assertion: across `src/react/overlay/**` minus an explicitly-enumerated `panel/parked/**` exemption, `applyClassNameEdit` is referenced by exactly one non-test module. The RED recipe is planting a second call in any live panel file.

### D3 — clamp, not invert, at minimum size

**Decision: clamp.** The drag's written value floors at `1px`; the gesture never inverts.

Grounds:
- Figma inverts (LIVE-B: below 1 it flips and restarts from 1 on the other side) because in free-form a drag manipulates a rect with an origin and a signed extent, and crossing the origin is a coherent operation. **In flow there is no origin the gesture owns** — the parent's layout algorithm places the box. An inverted drag has nothing to express; the element would not move, and only the number would misbehave.
- The serialization has no inverted form. A negative arbitrary width is not a valid Tailwind utility, so an inverting gesture would have to invent a second, un-serializable state mid-drag.
- `1px` rather than `0px`: at zero extent the ring collapses and the handles land on top of one another, which is undefined for a hit-tested affordance. `1px` is also Figma's own floor, so the number is familiar rather than arbitrary.

**The hazard this decision does NOT close, and how it is closed:** a flex item's default `min-width: auto` means the rendered box can stop shrinking at its content size while the written value keeps falling. The written value and the ring would then disagree, silently. **EG-1** below measures this before the handle ships, and both outcomes already have a planned path: if the box follows, clamp-at-1 is sufficient; if it does not, the drag's written value is derived from the **measured** box rather than the raw pointer delta, so the number stops when the box stops. `min-w-0` is never auto-injected — that would be an unrequested second write and a layout semantic change the user did not ask for.

### D4 — the v3.0 slice and the v3.x ladder

Confirmed, with one adjustment, and phased in §7.

**The adjustment, stated loudly because it reconciles two inputs that disagree:** the brief's Verdict-6 restatement puts "gap/padding **numeric inputs**" in the trunk, while the synthesis's v3.0 candidate defers "gap/padding affordance" to v3.1. Both are right about different surfaces, and Verdict 4 is explicit that the integrated numeric popup is the second half of the **on-canvas** affordance. Resolution: **panel** numeric gap/padding inputs ship in v3.0 (trunk, and nearly free once the panel section and the serializer exist); the **on-canvas** gap/padding affordance — hatched region, drag strip, click-to-popup, padding edge handles — ships whole in v3.1, popup included.

| Version | Phase branch | Contents |
|---|---|---|
| **v3.0** | `feat/phase-41-e3-v3-sizing-align-resize` | ontology migration + amendment · late-remeasure fix · the single serializer · panel sizing tri-state + parent 3×3 alignment + gap/padding numeric inputs · ring resize handles with the shield bypass |
| **v3.1** | `feat/phase-42-e3-v31-gap-padding-affordance` | the on-canvas gap/padding affordance, drag **and** integrated numeric popup, one affordance |
| **v3.2** | `feat/phase-43-e3-v32-row-closure` | Shift aspect-lock (edges and corners) · edge-double-click Hug / Alt+edge-double-click Fill · text width-drag acceptance · the row-closure pass that leaves no `deferred-v3` cell |

**Cuts, per Verdict 6 and the ADR:** Alt+handle center-resize (reclassified to v4), marquee multi-select (reclassified to v4-or-later), multi-select align/distribute as a gesture (deleted). Batch panel edit over a multi-selection is recorded unowned.

**Phase numbering:** 41 is the next free number. The highest allocated across `docs/**` and `.omc/**` today is 40 (the `src/app/` restructure, landed 2026-08-13, recorded in the E4 backlog row). One branch per plan phase, per the branching rule; the P-steps inside each phase are commits on that branch, not branches.

### D5 — the late-remeasure defect is a prerequisite, and it is worse than the probe could see

Lane C found it as a race (1 of 4 runs, ring at 624px against a 524px element, persisting ≥2.5s). Re-reading the source while writing this plan turns the REASONED mechanism into a structural one:

- **The className-commit path never re-anchors the ring at all.** `packages/descvi/src/react/overlay/engine/use-preview-session.ts#const reselectBySpecId = useCallback(` is the post-commit reselect, and it does **not** call `remeasure()` — unlike the two neighbouring reselect paths (`handleSelectAncestor` and the undo consumer's retry) which both do. It calls `setSelectedEl(node)`, and Lane C measured that Fast Refresh patches the className on the **same DOM node**, so that setter receives the identical reference, React bails out, and the ring effect's `selectedEl` dep never changes.
- A drag therefore looks correct only because the last per-pointermove `remeasure()` already placed the ring at the final width. **Panel numeric input has no per-move remeasure at all**, which is exactly why Lane C says the defect bites it too.
- What produced the *visible* 624px tear is the opposite problem: an unrelated remeasure trigger firing **inside** the CSS gap. The only survivors are `packages/descvi/src/react/overlay/OverlayShell.tsx#const observer = new ResizeObserver(() => remeasure());` (scoped to `#dsh-stage`, not to page elements), the `#dsh-screen` scroll listener, and `window` resize. Any of them landing while the JIT `<style>` is cleared and before the `globals.css` hot-update arrives anchors the ring to the unstyled width — and nothing measures after.

**Decision:** the fix is a **post-commit late re-anchor**, owned by the ring layer, not a widened remeasure trigger. Primary shape: an **element-scoped `ResizeObserver` on `selectedEl`** driving `remeasure()`, connected on selection and disconnected on deselect/unmount. It closes both halves — it fires when the box settles after the CSS lands, and it is not sensitive to whether React bailed on the setter. **EG-2** measures whether it fires at all in that window and names the fallback path if it does not.

Guard the plan already carries: the observer must never observe an element the ring writes to. The ring divs live in `#dsh-ring-layer` and page element styles are never touched (that was the BUG-5 fix); if the observer ever fires continuously, the layer isolation is broken and that is a stop condition, not a tuning problem.

---

## 7. Phasing

Each phase is one `feat/phase-{N}-{slug}` branch. Per-phase rhythm is the repo's: implement → independent verification pass → atomic commit. **The whole-set audit runs as each phase LANDS**, not once at the end — a cross-phase contract mismatch (P2 promises a token shape, P4 consumes a different one) is invisible to per-phase review by construction.

**Gate set for every phase, without exception:** `pnpm gates` (which parses CI's `verify` job rather than trusting any list written here), plus `pnpm test:e2e` for the Playwright projects that `pnpm gates` deliberately excludes. Phase-specific gates are named per step below and are additional, never a substitute.

**Artifact byte-identity applies per step:** `git diff --exit-code .descvi/screens.json` must be clean for every `packages/**`-only step. The two steps that touch `src/app/**` fixtures declare their artifact diff as the deliverable and get it reviewed as such.

---

### Phase 41 — v3.0 (`feat/phase-41-e3-v3-sizing-align-resize`)

#### P0 — migrate and amend the interaction ontology (docs only)

- **Purpose.** The contract the rest of v3 is built against lands first, in a place it can be edited.
- **Touches.** New `docs/reference/interaction-ontology.md`; `docs/README.md` (`reference/` table row); `docs/e3/tracker.md` (Refs line).
- **Must achieve.** The full §5 ADR amendment table applied; every References line-pin converted to an anchor or to an immutable `git show <sha>:path` record; the row-closure criterion written into §6 so a later phase can check it.
- **Acceptance.** No cell in the migrated §6 v3 row still reads `marquee multi-select` or `Cmd/Shift-click multi-select + align/distribute`; §3.F-5's Alt+handle row reads `deferred-v4`; §3.F-7 reads `deferred-v4-or-later`; `docs/e3/tracker.md` no longer cites `.omc/specs/interaction-ontology.md`.
- **Verification.** `node scripts/check-citation-anchors.mjs` GREEN; `node scripts/check-citation-anchors.mjs --selftest` GREEN (proves the instrument can fail). **RED recipe:** corrupt one converted anchor's text by a single character — leg (b) must report it by name. Do this before believing the green.
- **Failure behavior.** If any converted anchor cannot be made unique (the source text repeats in its file), pick a longer enclosing line rather than a line number; if no unique text exists, the citation is a `git show` record instead. Never a line pin.
- **Commit.** `docs(spec):` — doc updates get their own commits.

#### P1 — the late-remeasure fix (D5)

- **Purpose.** Prerequisite for both the panel numeric commit and the handle. Ships alone so its effect is attributable.
- **Touches.** `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts` (or a sibling hook in `canvas/` if the observer's lifecycle does not belong inside a layout effect); `packages/descvi/src/react/overlay/OverlayShell.tsx` wiring only if the observer needs a ref it does not already hold.
- **Must achieve.** After a committed className edit that changes the selected element's box, the ring and badge are anchored to the element's **settled** geometry, with no persistent divergence — whether the commit came from a drag or from a panel field.
- **Blocked by EG-2.** Do not write the fix before the gate's observation; the gate chooses between the observer shape and the trailing-tick shape.
- **Acceptance.** (a) a jsdom test drives commit → simulated box change → asserts a re-anchor fires; (b) the observer is disconnected on deselect and on unmount (a leak here is a per-selection accumulation); (c) no re-anchor storm — the re-anchor count for one commit is bounded and asserted.
- **Verification.** New unit tests in the existing jsdom style + a live `descvi:dev` observation on `src/app/lab/tests/style-edit/page.tsx#data-oid="v002k2"`: commit a width change from the panel, screenshot the ring against the element at settle. **RED recipe:** revert the fix and re-run the jsdom test; it must fail. jsdom has no `ResizeObserver`, so the guard pattern already used at `packages/descvi/src/react/overlay/OverlayShell.tsx#const observer = new ResizeObserver(() => remeasure());` applies and the jsdom assertion must drive the trigger directly rather than relying on the real observer.
- **Failure behavior.** If the live observation still shows a persistent tear after the fix, STOP: the mechanism is not the one D5 names, and the remaining candidate (a remeasure that fires inside the CSS gap and is never followed) needs its own probe before P4 proceeds.

#### P2 — the single serializer (pure, no UI)

- **Purpose.** One module, fully tested, before anything renders. Everything downstream imports it.
- **Touches.** A new module under `packages/descvi/src/react/overlay/engine/`; `packages/descvi/src/react/overlay/engine/tailwind-class-model.ts` only for the two defects D2 names.
- **Must achieve.** Intent → token for: sizing tri-state per axis with parent-axis routing; alignment (`justify-*` × `items-*` from a 3×3 cell); gap; padding per edge and symmetric. Plus the inverse read: token set + parent axis → intent, so the panel shows what the source says rather than a default.
- **The decision the prose cannot carry precisely** — the shape the module must expose and every caller must speak:

  ```ts
  type Axis = "w" | "h";
  type SizingMode = "hug" | "fill" | "fixed";
  /** A dimension ALWAYS carries its unit — a bare number is not representable. */
  type Dimension = { value: number; unit: "px" };
  /** The parent's flex main axis, read from computed style at gesture/render time. */
  type ParentAxis = "row" | "col" | "none";
  ```

  and the one assertion that pins D2 rather than restating it:

  ```
  sizingToken("w", { mode: "fill" }, "row")  === "flex-1"        // width is the MAIN axis of a row parent
  sizingToken("w", { mode: "fill" }, "col")  === "self-stretch"  // width is the CROSS axis of a column parent
  sizingToken("h", { mode: "fill" }, "row")  === "self-stretch"
  sizingToken("h", { mode: "fill" }, "col")  === "flex-1"
  sizingToken("w", { mode: "fixed", dim: { value: 347, unit: "px" } }, "row") === "w-[347px]"
  ```

- **Acceptance.** (a) the five assertions above; (b) `w-full`/`h-full` READ BACK as Fill but are never produced; (c) the cross-axis strip removes a stale `self-stretch` when switching Fill → Hug on that axis; (d) the parent-axis-blind `flex-1` read is gone — `flex-1` in a `col` parent reads as **height** Fill; (e) prefixed/important/custom tokens survive every write untouched (the ADV2 property the existing model already holds — do not regress it).
- **Verification.** Unit tests beside `packages/descvi/src/react/overlay/__tests__/tailwind-class-model.test.ts` in the same style. **RED recipe:** change the `col`-parent width case to `flex-1`; assertion (a) must fail.
- **Failure behavior.** If twMerge resolves any of these pairs differently than the strip assumes, the strip widens — never the assertion.

#### P3 — the panel: sizing tri-state, parent 3×3 alignment, gap/padding numerics

- **Purpose.** Verdict 6's trunk. This step alone must be dogfoodable with no handle on the canvas.
- **Touches.** `packages/descvi/src/react/overlay/panel/` — new section components mounted into the existing chip-session panel; `packages/descvi/src/react/overlay/engine/use-preview-session.ts` for the widget→chips seam only.
- **Must achieve.**
  - Sizing tri-state per axis, Figma vocabulary (Hug / Fill / Fixed) with a numeric field for Fixed, seeded from the element's source className via the P2 read.
  - The 3×3 alignment widget renders **only when the selected element is itself a flex container** and writes `justify-*` × `items-*` on that element. A non-container selection shows no widget — matching LIVE-B exactly, where selecting a child offers no auto-layout alignment.
  - Gap and padding numeric inputs on a container selection.
  - Every widget change flows through `packages/descvi/src/react/overlay/engine/use-preview-session.ts#const handleChipsChange = useCallback(` and commits through `packages/descvi/src/react/overlay/engine/use-preview-session.ts#const handleChipCommit = useCallback((): void => {` — the same auto-apply boundary the chip editor already uses. No widget calls the bridge.
- **Acceptance.** (a) a widget edit and the equivalent hand-typed chip produce a byte-identical POST body; (b) the chip set visibly updates when a widget writes (they are one state, not two); (c) a non-editable target (`dynamic-class`, no className) shows the existing disabled affordance and no widgets; (d) Fill is disabled with a visible reason when the parent's computed display is not flex; (e) Korean panel strings round-trip (no jamo separation).
- **Verification.** jsdom tests in the existing `OverlayShell-*` style + a live `descvi:dev` pass on `lab/tests/style-edit`. The D2 caller gate lands here. **RED recipe for the caller gate:** add a direct `applyClassNameEdit` call in a live panel file; the gate must name that file.
- **Failure behavior.** If (a) fails, the widget is composing its own string — stop and route it through the serializer rather than reconciling the two outputs.

#### P4 — ring resize handles

- **Purpose.** The rough-in layer, on top of a panel that already works.
- **Touches.** A new `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts` (pure controller + thin hook, mirroring the existing ring/shield split); `packages/descvi/src/react/overlay/OverlayShell.tsx` for the handle mount inside the ring layer; `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts` for the bypass; `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts` if the ring's geometry writes move into the drag handler.
- **Must achieve.**
  - Eight handles (4 corner, 4 edge) on the selection ring, mounted inside `packages/descvi/src/react/overlay/OverlayShell.tsx#className="z-40 absolute inset-0 overflow-hidden pointer-events-none"` with `pointer-events: auto` on the handle shapes only. Sizes with two precedents: ~8px glyph, ~20px effective hit target, edge strips spanning the full edge.
  - **The shield bypass — exactly two sites, and forgetting either is a known failure.** An early return before suppression when the event target is inside a handle, in **both** `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#const onPointerSuppress = (e: Event) => suppressShieldPointer(e);` and `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#const onClick = (e: Event) => {`. Omitting the `onClick` half reintroduces deselect-on-release (LIVE-C: the synthesized click resolves the handle to `null` and clears the selection). The bypass belongs in the **wiring**, not in `packages/descvi/src/react/overlay/canvas/selection-shield.ts#export function handleShieldSelect(`, which suppresses unconditionally at its top by design.
  - Drag lifecycle: `setPointerCapture` on the handle; per-pointermove preview through the existing controller; **exactly one POST on pointerup**. The per-move path must bypass the chip-editor's `setDraftChips` React commit and write ring+handle geometry directly in the drag handler.
  - Axis semantics: the dragged axis converts to **Fixed at the first size change** (not pointerdown, not release), whatever it was before. Siblings reflow live because the preview is a real DOM write.
  - Clamp at 1px per D3, subject to EG-1's outcome.
  - **Refusals, all visible:** no handles on a non-editable target (no chip session — LIVE-C measured the refusal path already exists); no handles on a **shared-oid** target (KI-10: `reselectBySpecId` resolves by first-match `querySelector` and cannot discriminate instances, so a drag on instance 3 would re-anchor to instance 0 — the panel path already ships for these elements and is unaffected); handle hit boxes clamped to stay inside the ring layer's rect so a full-bleed element's corners are not clipped away by the layer's `overflow-hidden`.
- **Acceptance.** (a) one `POST /edit → 200` per drag, asserted, not counted by eye; (b) the committed token is byte-identical to what P3's panel would write for the same final size; (c) mid-drag `#dsh-screen` scroll keeps element, ring and handle in step; (d) undo of a drag-committed resize works through the existing Cmd+Z; (e) a drag on a shared-oid element is refused with a reason; (f) `git diff --exit-code .descvi/screens.json` clean.
- **Verification.** jsdom tests for the controller and the bypass; **two Playwright specs**, both of which reproduce deterministically per LIVE-C: the shield-swallow case (without the bypass, zero handle events and a cleared selection) and the post-commit anchor case. Both go in the `design-view` project — and the spec filename must be added to that project's `testMatch` list in `playwright.config.ts`, because a missing entry drops the file **silently** and even `--list` exits 0. Plus a live `descvi:dev` smoke: drag, release, read the source diff.
- **Failure behavior.** More than one POST per drag means the commit is firing off a per-move path — stop, do not debounce over it. A ring that lags more than one frame during drag means the geometry is still going through `setState`; move it into the drag handler rather than raising the remeasure rate.

#### P5 — whole-set audit for phase 41

Runs as the phase lands, not later. Reads P0→P4 as one contract: does the token the serializer emits equal the token the panel claims to write equal the token the handle commits equal the token the ontology row promises? Names any cell of the amended v3 row that phase 41 was supposed to close and did not.

---

### Phase 42 — v3.1, the gap/padding affordance (`feat/phase-42-e3-v31-gap-padding-affordance`)

One affordance with two halves, per Verdict 4 — the popup is not polish, it is the other half.

- **Appears when the PARENT is selected**, between that parent's own children only. Sibling-of-parent gaps do not show (LIVE-B).
- The whole gap region is hatched; the **draggable strip is 16–24px**; **the rest of the region is click → numeric popup**.
- Padding: four edge-center handles, hover reveals the hatch, click opens a per-edge input, drag grows that edge. At padding 0 the handle sits flush with the edge.
- Value readout floats near the cursor, offset from it; children reflow live.
- Modifiers: **Shift = 10-step**, **Alt/Option = symmetric (both sides)**. No Cmd/Ctrl role — do not bind one.
- `justify-between` (gap "Auto") + a handle drag **forces back to numeric**: the write is a concrete `gap-[Npx]` and the packed mode is restored.
- All of it through the P2 serializer and the P3 commit boundary. Zero new write paths.
- **Gates:** the standard set; one POST per gesture; a Playwright spec for the popup half (registered in `testMatch`); `git diff --exit-code .descvi/screens.json` clean.
- **Failure behavior.** If the hatched region's click target and the drag strip cannot be separated reliably at small gaps, the drag strip wins and the popup moves to a click on the hatch outside the strip — never make both ambiguous. If the gap is too small to host a 16px strip, the region is popup-only.

### Phase 43 — v3.2, row closure (`feat/phase-43-e3-v32-row-closure`)

- **Shift aspect-lock**, on **edges as well as corners** (LIVE-B — this is the part a corners-only implementation would get wrong): the dragged edge grows and the perpendicular dimension follows the ratio; a diagonal indicator is shown while locked; **releasing Shift mid-drag unlocks** and the drag continues unconstrained.
- **Edge double-click = Hug** on that axis; **Alt/Option + edge double-click = Fill**. Both Figma-documented and ported verbatim by Onlook. Corner double-click has no action (LIVE-B). This is an **addition** to the amended row rather than an existing cell, adopted because it is the cheapest possible Hug/Fill entry once handles exist and it is already familiar; §3.B's `dblclick` reservation is about the **element** target-type and does not collide (P0 records that).
- **Text acceptance case:** a width drag on a text element converts to Fixed width with auto-height wrap (LIVE-B). This is not new machinery — it is the generic handle applied to a text element — but it is an acceptance case that must be asserted, because "the height follows" is the part that could silently not happen.
- **Row closure.** The phase does not land until the migrated §6 v3 row has no `deferred-v3` cell left: every cell is SHIPPED or reclassified. That is the checkable form of owner ruling Q4.
- **Gates:** the standard set; a Playwright spec for aspect-lock-then-release (registered in `testMatch`); the row-closure check is a documentation assertion made in the phase's audit, not a script.

---

## 8. Risks and responses

| Risk | Response |
|---|---|
| **KI-10 shared-oid**: a drag on instance N commits, then the post-commit reselect snaps the ring to instance 0 | Refuse handles on shared-oid targets in v3.0 (P4). The panel path is unaffected and already ships for these elements. Does not pre-decide KI-10's four options. |
| **Second serializer creeps back in** via un-parking the structured panel | The D2 caller gate, planted in P3, with `panel/parked/**` as an explicitly enumerated exemption and its reason recorded beside it. |
| **Per-move cost**: JIT `ensure()` + a React commit per pointermove | The drag path bypasses `setDraftChips` and writes geometry directly; acceptance (a) in P4 bounds the state updates per gesture. LIVE-C drove ~40Hz with no errors but never profiled the JIT cost — if the live smoke shows lag, rAF-throttle the preview, never the commit. |
| **Frame-edge clipping** of corner handles on a full-bleed element (the ring layer is `overflow-hidden` by BUG-1 design) | Clamp handle hit boxes into the layer rect (P4). Do not remove `overflow-hidden` — that re-opens BUG-1 and BUG-6. |
| **Auto-scroll on drag near the edge** is unbuilt and unmeasured (LIVE-C), and shrinking an element mid-drag can remove the overflow that made the screen scrollable | Out of v3.0. If the live smoke makes it necessary, it is a v3.x addition with its own step, not an unplanned P4 growth. |
| **Device-mode (`#dsh-stage` scroll) mid-drag** is scroll-invariant by construction but unmeasured live | Add it to P4's live smoke checklist. Layer-relative math says it holds; "says" is not "measured". |
| **Concurrent chip-editor draft during a drag** — unmeasured | The drag enters through the same session; a dirty draft resolves through the existing `resolveInFlightDraft` boundary before the gesture applies. Assert it in P4 rather than assume it. |
| **Backlog/tracker drift** — the E3 backlog row still describes phase-11 as in progress | Not this plan's scope to fix, but each phase's tracker entry is part of its landing, per the repo's own record-keeping. |

---

## 9. Pre-mortem — three credible ways this ships wrong

1. **The panel and the handle disagree by one pixel, forever.** The handle derives its value from a pointer delta and the panel from a typed number; they round differently, so dragging to 347 and typing 347 produce different source. Nobody notices until a diff review. **Caught by:** P4 acceptance (b), which requires the drag's committed token to be byte-identical to the panel's for the same final size. **Prevented by:** both going through the same `Dimension` type and the same serializer, with no float anywhere near the token.
2. **The v3 row is "complete" but the ontology still says otherwise.** P0 migrates the file, phases 41–43 ship the cells, and the migrated §6 is never re-read — so a v4 planner picks up `marquee multi-select · deferred-v3` from the frozen `.omc/` copy that is still the first search hit. **Caught by:** P0's requirement that `docs/e3/tracker.md` stop citing the `.omc/` path, plus phase-43's row-closure assertion. **Residual:** search still surfaces the frozen copy. Accepted — it is a point-in-time record by the repo's own convention, and the living one is indexed in `docs/README.md`.
3. **The late-remeasure fix ships as a widened trigger and creates a storm.** The tempting fix is "remeasure more often" — a `setInterval`, or observing `#dsh-screen`. It papers over the visible tear and costs a re-anchor on every layout event in the page. **Caught by:** P1 acceptance (c), which bounds the re-anchor count for one commit, and D5's stop condition on a continuously-firing observer. **Prevented by:** the fix being scoped to the selected element, whose box is the only thing whose settling matters.

---

## Evidence Gates

### EG-1 — the flex minimum-size floor

- **Claim:** a committed `w-[Npx]` below the element's content minimum renders at N, so clamping the written value at 1px is sufficient and the ring never disagrees with the number.
- **Evidence method:** in a live `descvi:dev` session on `src/app/lab/tests/style-edit/page.tsx#data-oid="v002k2"`, commit descending widths from the panel (200px, 60px, 12px, 1px) and record the element's measured `getBoundingClientRect().width` beside each written value. One session, four commits, no new code.
- **Pass path** (measured width tracks the written value to 1px): D3 stands as written — clamp the drag at 1px, no further work.
- **Alternate path** (measured width floors at the content minimum while the written value keeps falling): the drag's written value is derived from the **measured** box rather than the raw pointer delta, so the number stops when the box stops. `min-w-0` is never auto-injected. The panel's typed input still accepts the smaller number and the ring shows the rendered box — the divergence is visible rather than hidden.
- **Required before:** P4 (the drag's clamp behavior) and P3's Fixed numeric field.
- **Unexpected result** (the element vanishes, the ring inverts, or handles become unhittable at small sizes): **STOP.** Handle geometry has no defined behavior at zero extent; halt P4 and bring the observation back before choosing a floor.

### EG-2 — what actually re-anchors after a commit

- **Claim:** an element-scoped `ResizeObserver` on `selectedEl` fires after the Tailwind CSS hot-update lands, and is therefore the right trigger for the post-commit re-anchor.
- **Evidence method:** in a live `descvi:dev` session, attach a throwaway element-scoped `ResizeObserver` logger to the selected element, commit a `w-[Npx]` panel edit, and record: whether it fires, how many times, at what widths, and the final settled box. Run it enough times to catch the tear window Lane C hit in 1 of 4 runs. Throwaway code, reverted after.
- **Pass path** (it fires, with a final entry at the settled width): P1 implements the observer shape — connect on selection, disconnect on deselect and unmount, drive `remeasure()`.
- **Alternate path** (it never fires, i.e. the box does not change and the tear is a pure measurement race): P1 implements the trailing-tick shape instead — after `commit()` resolves, a bounded sequence of trailing rAF re-anchors, or a re-anchor keyed on the CSS hot-update. Either way the trigger gets its own deterministic unit test, since the live window is not reproducible on demand.
- **Required before:** P1, and therefore before P3's numeric commit and all of P4.
- **Unexpected result** (the observer fires continuously, or a ring write feeds back into it): **STOP.** A ring write must never resize the observed element; if it does, the ring-layer isolation that BUG-5 established is broken and that is a defect to fix before any observer ships.

### EG-3 — how much of the corpus has a flex parent at all

- **Claim:** the Fill state is meaningful for the large majority of selectable elements, so a tri-state that leads with Hug/Fill/Fixed is the right default shape.
- **Evidence method:** in a live `descvi:dev` session, walk every `[data-oid]` under `#dsh-screen` across the corpus screens and tally the parent's computed `display` — flex / grid / block / other. One script, read-only, no writes.
- **Pass path** (non-flex parents are a small minority): the tri-state ships as designed; Fill is disabled with a visible reason on the minority, per P3 acceptance (d).
- **Alternate path** (non-flex parents are a large share): the widget leads with Fixed/Hug and Fill is a secondary state, **and** a row is recorded against E4 track 2 — a corpus whose containers are mostly non-flex is a corpus that under-represents what the tool is for, which is a distribution-design finding, not a v3 defect.
- **Required before:** P3 (the widget's shape and default), and it informs P4's refusal set.
- **Unexpected result** (an element's parent display differs between what the source className says and what computed style reports, in a way that would flip the axis routing mid-session): **STOP.** The serializer's `ParentAxis` input would be unstable, and D2's mapping rests on it being stable.

---

## Open Questions

None of these block execution; each would change something if answered.

**OQ-1 — `_scratch` versus E4 track 3 (owner ruling needed; explicitly out of this plan's scope).** `packages/descvi/src/extractor/screen-scan.ts#export const SCREEN_SCAN_IGNORE: readonly string[] = [` contains `'**/_*/**'`, so `src/app/_scratch/` is invisible to the extractor **by construction** — nothing there gets an oid, and nothing there is selectable or editable. E4 track 3's stated purpose is a gitignored sandbox for edit-testing, which that sandbox therefore cannot serve. **Why it matters here:** v3 is the version that most wants a disposable screen to drag things around on, and every live smoke in this plan is consequently pinned to `lab/tests/style-edit` instead. Someone will reach for `_scratch` and find silence. The ruling is the owner's: change the ignore pattern, move the sandbox out from under the underscore, or accept that the sandbox is for source-editing only and say so where people look.

**OQ-2 — do Tailwind scale tokens become a preset concept in v3.x or later?** Owner ruling Q1 defers them to a "variables-like preset" concept, which Figma puts in the same dropdown as Hug/Fill/Fixed, after a divider. **Why it matters:** if the answer is "in v3.x", the sizing widget's layout should reserve that slot now; if "later", it should not, because an empty divider is worse than none. This plan assumes **later** and reserves nothing.

**OQ-3 — batch panel edit over a multi-selection.** LIVE-B says this is what multi-select is actually for in Figma (values show Mixed and an edit writes both). The ADR removes multi-select as a v3 *gesture* cell, and records this as unowned at no version. **Why it matters:** it is the only surviving justification for ever building element multi-select, and if it is wanted, the selection model's single-`selectedEl` shape is what would have to change — a bigger change than any cell in v3.

**OQ-4 — does the alignment widget ever need a canvas affordance?** Verdict 1 mentions a "possibly on-canvas 9-dot affordance" alongside the panel widget. This plan ships the panel widget only. **Why it matters:** if the canvas affordance is wanted, it is a v3.x addition to the amended row and phase-43's row-closure criterion would need to include it, rather than closing without it.

**OQ-5 — the parked structured panel's long-term disposition.** `packages/descvi/src/react/overlay/panel/parked/PropertyPanel.tsx` is kept compiling and green as an un-parking target, and this plan builds its own widgets on the chip session instead. **Why it matters:** after v3.0, the parked tree holds a *second* implementation of the sizing tri-state, with a different serializer and a direct bridge call. Keeping it is now a maintained divergence rather than a dormant option. Either it gets rewritten onto the v3 serializer, or it gets retired under the repo's deletion rule — but "dormant, not dead" stops being true once a live implementation of the same concept exists beside it.
