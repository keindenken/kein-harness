# E3 v3 — On-canvas direct manipulation

Status: Draft
Status reason: Drafted (phase: drafted). Planner revision after round 1 is complete — all 8 consolidated MUST_FIX findings addressed, every round-1 verdict invalidated by the content change. Not yet reviewed at the new review hash; awaiting round-2 fresh Architect and Critic lanes.

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

1. **One serializer, one write path.** Exactly one module turns intent (Fixed 347px / Hug / Fill / align / gap) into a Tailwind token, and exactly one code path commits it. The cautionary evidence is Onlook's two entry paths for one concept — panel-Hug funnels `fit-content` through a digit-matching regex and emits `0px` where the canvas double-click writes `fit-content` directly. **Tier: READ-A plus REASONED — read in their source at `423e2e9` and explicitly NOT runtime-verified by Lane A**, so it is a divergence the code shows rather than a bug anyone watched fail. That is enough to justify the principle (the divergence is structural and visible in the source) and not enough to call it a shipped defect.
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
| **A. Inside `#dsh-ring-layer`, with a shield bypass** | ring-relative geometry is already scroll-invariant by construction; measured working end-to-end (LIVE-C Q1/Q2) | needs a ~4-line escape hatch in the shield wiring; frame-edge clipping to manage; **and the layer carries `aria-hidden="true"`, which excludes anything mounted under it from the accessibility tree** — see the mechanism note below | **CHOSEN** |
| B. A sibling layer above the shield (Onlook's pattern) | zero shield changes | **does not work here**: descvi's shield is a *native capture-phase listener on the ancestor `#dsh-stage`*, not a sibling overlay, so paint order cannot pre-empt it. A layer outside `#dsh-stage` would be viewport-pinned and go stale — the exact failure the BUG-1 architect review rejected | rejected on mechanism |
| C. Handles as children of the page element | no layer at all | mutates page DOM; re-opens the whole BUG-5 family (per-node style writes) | rejected |

**The `aria-hidden` mechanism, decided here because it changes both P4's touch list and the two specs' locator strategy.** Handles mounted under an `aria-hidden="true"` ancestor are invisible to role- and name-based Playwright locators, so a `getByRole` spec cannot tell "the handle received zero events" (the RED case it is asserting) from "the locator matched nothing". Two facts settle the fix:

- **The container's attribute is redundant.** All three ring divs already carry `aria-hidden="true"` individually (`#dsh-hover-ring`, `#dsh-selection-ring`, `#dsh-selection-badge`), so removing it from the layer container leaves every existing ring exactly as hidden as it is today. Nothing BUG-1/5/6 constrained is touched: those defects were about geometry, overflow and per-node style writes, not about the accessibility tree.
- **`aria-hidden="false"` on the handle container does NOT work** and must not be used. Per ARIA, a descendant of an element with `aria-hidden="true"` is excluded from the accessibility tree regardless of its own value — `false` cannot un-hide a subtree its ancestor has hidden.

So: **scope the attribute down to the ring divs (drop it from the layer container), never add `aria-hidden="false"`.** Independently of that, the two specs locate handles by a stable attribute (`data-dsh-handle` / `data-testid`, matching the `data-testid` convention the three ring divs already use) rather than by role, and assert **existence first, behavior second**, so a missing handle and an inert handle fail with different messages.

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
- A pointer stub cannot be left behind (the source tree is read-only), so the pointers must be updated at the **reader's entry points** instead. Living citations of the ontology outside `.omc/`, re-counted at the file level rather than the file-list level: **`docs/e3/tracker.md` carries TWO**, spelled differently — the Refs line (`.omc/specs/interaction-ontology.md`) and, two lines later, the 2026-07-07 archival note listing `specs/interaction-ontology.md` (living) in the prefix-less form. A census that greps for the full `.omc/`-prefixed path finds one of the two and reports the job done. Everything else that mentions it (`.omc/archive/260707-e3/ralplan-e3-v15-chip-hardening.md`, the three spike files) is a frozen point-in-time record and is left alone by the `docs/README.md` convention.
- **`docs/e3/roadmap-v2plus.md` is living, git-tracked, and is the definition of the version ladder — and it still promises the falsified cell in two places**: the ladder table's v3 row (`resize handle; gap/padding drag handle; multi-select align/distribute`) and the `### v3` 범위 bullet (`multi-select + align/distribute`). Amending the ontology while leaving the roadmap intact would leave the two living documents contradicting each other, with the roadmap being the one a version planner reads first. It is in scope for P0.

**Three obligations the move creates:**
1. **Every line pin in the migrated file converts — not just the References section.** Measured on the current file: **38 `file:line` pins, of which 26 are in the document BODY (lines 1–328) and 12 in References.** The body pins are already rotted in the same two ways — pre-phase-11 paths (`selection-shield.ts`, `ClassNameChipEditor.tsx`, `utility-source.ts`, all since moved into `canvas/`, `panel/`, `engine/`) and stale offsets into a file that has been rewritten many times over (`OverlayShell.tsx:801` appears three times; `OverlayShell.tsx:281` three times). Scoping conversion to References would migrate 12 rotted pins and leave 26.
2. **The existing citation gate's green does not discharge obligation 1, and this must be stated rather than assumed.** `scripts/check-citation-anchors.mjs` has two legs and neither sees a bare `file.ts:NNN` here: leg (a)'s pin ban is scoped to `PIN_TARGETS`, which is only `packages/descvi/src/vite/plugin.ts`; leg (b) checks `path#anchor` forms for uniqueness and existence. So the migrated file can carry all 38 rotted pins and the gate reports GREEN. Conversion therefore needs a **hand-checkable acceptance** of its own (P0), not a gate signature. What the gate does buy is the other direction: once converted, `path#anchor` citations are machine-checked, and a non-existent cited path is a leg (b) violation.
3. `docs/README.md` gains a `reference/` row; both of `docs/e3/tracker.md`'s citations are re-pointed; `docs/e3/roadmap-v2plus.md`'s two v3 promises are rewritten. Doc updates get their own commits.

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

**And in `docs/e3/roadmap-v2plus.md`** (living, and not part of the migrated copy):

| Location | Change |
|---|---|
| Ladder table, v3 row | `resize handle; gap/padding drag handle; multi-select align/distribute` → the amended cell set: resize handle (Fixed conversion on first size change); sizing tri-state panel; parent 3×3 alignment widget; gap/padding affordance. The Engine-delta column (`없음 (gestures → v1 attribute writes)`) is correct and stays |
| `### v3` 범위 bullet | `multi-select + align/distribute` → the parent alignment widget, with the LIVE-B falsification named in one clause so a reader does not re-propose it |
| `### v3` 게이트 리서치 bullet | Currently says the Figma/Onlook spike must happen before the ralplan. Mark it **satisfied**, pointing at `.omc/spikes/e3-v3-handles/synthesis.md` — an unsatisfied gate line on a version that is being executed is the same stale-STATUS class the amendment exists to remove |

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
- `w-full`/`h-full` remain legal in the corpus and must still **read back** as Fill; they are simply never **written**. **And an axis already expressed as `w-full` is LEFT AS-IS when the user re-writes Fill on that same axis** — a no-op edit must stay a no-op. Rewriting it to `self-stretch` would make merely opening the panel on an untouched element produce a source diff, which is the one behavior most likely to make a user stop trusting the tool. The token changes only when the mode changes (Fill → Fixed → Fill lands on `self-stretch`, because that path genuinely re-derives it). Pinned in P2 acceptance (f).

Grounds for "always an explicit unit": `utilityFor` in the existing model snaps a bare number to a scale token — `packages/descvi/src/react/overlay/engine/tailwind-class-model.ts#export function utilityFor(prefix: string, value: string): string {` matches `/^\d+(\.\d+)?$/` first, so `347` becomes `w-347`, not `w-[347px]`. That directly contradicts owner ruling Q1. The serializer therefore takes a value **with its unit** (`347px`), which the same function already turns into `w-[347px]` — the existing test file pins exactly this pair. Scale tokens surface later, as a variables-like preset concept, and never as a snap target.

**Three defects in the parked model that this decision forces us to fix rather than inherit — one on the read side and two on the write side:**
- **READ, axis-blind.** `packages/descvi/src/react/overlay/engine/tailwind-class-model.ts#state.width = { mode: "fill", value: null };` maps `flex-1` unconditionally to **width** fill. In a `flex-col` parent, `flex-1` grows the **height**. The read-back must route by the parent's flex axis, not assume width.
- **WRITE, axis-blind — and this one is created by our own mapping, not merely inherited.** `packages/descvi/src/react/overlay/engine/tailwind-class-model.ts#function sizingAxisOf(utility: string): "w" | "h" | null {` classifies a utility's axis through `isWidthSizing`, which returns true for `flex-1` and `grow` unconditionally. Under D2's mapping `flex-1` is the **height** Fill token in a `col` parent, so writing it there makes `sizingAxisOf` answer `"w"`, `stripSizingAxis` strip the **width** tokens, and a stale `h-*` survive beside the new `flex-1` — two height tokens, one of them a loser that twMerge will not resolve because they are different conflict groups. The axis of a sizing utility is no longer derivable from the token alone; it is a function of (token, parent axis), and the strip must take the axis as an argument rather than infer it.
- **WRITE, incomplete strip set.** `packages/descvi/src/react/overlay/engine/tailwind-class-model.ts#function stripSizingAxis(className: string, axis: "w" | "h"): string {` strips `w-*`/`h-*`/`flex-1`/`grow` but knows nothing about `self-*`. Adopting `self-stretch` as a sizing token means the strip set for the cross axis must include it, or Hug-after-Fill leaves both tokens standing.

**The single-serializer requirement, concretely.**
- One module owns intent → token for every v3 write: sizing tri-state, alignment, gap, padding. Nothing else composes a Tailwind sizing/alignment/spacing token.
- Every entry path — drag preview, drag commit, panel commit — goes through the **already-shipped** preview controller: `packages/descvi/src/react/overlay/engine/live-preview.ts#selectedEl.className = composeChips(chips);` for preview and its `commit()` for the POST. The composition boundary is `packages/descvi/src/react/overlay/engine/classname-tokenizer.ts#export function composeChips(chips: string[]): string {`, which is already documented as "BOTH the live-preview `el.className` string AND the committed POST `newClassName`". v3 adds token producers **above** that boundary and moves the boundary nowhere.
- **The second serializer already exists and is dormant.** `packages/descvi/src/react/overlay/panel/parked/PropertyPanel.tsx#import { composeClassName, parseClassName } from "../../engine/tailwind-class-model";` calls `applyClassNameEdit` directly, bypassing the preview controller entirely. v3's panel widgets mount on the **chip session**, not on the parked panel. The parked tree stays compiling and green (it is dormant, not dead, by its own header) but is never the mount point.
- **New gate, RED-able — and specified as CALL SITES, because the obvious predicate is born RED.** Extend `packages/descvi/src/react/overlay/__tests__/write-coordinator-callers.test.ts#describe("C4 ordinary caller coordinator reachability", () => {` with the negative half it currently lacks: today it asserts a positive topology (this file contains that call) and would not notice a second live caller.

  The predicate must **not** be "referenced by exactly one non-test module". Measured on the tree today, `applyClassNameEdit` appears in six non-test places and only two of them are calls:

  | Site | Kind | Disposition |
  |---|---|---|
  | `engine/sidecar-bridge.ts` | the **definition** + two JSDoc `{@link}` mentions | excluded — the defining module |
  | `engine/live-preview.ts` | import + two prose comments + **the one real call** | the measured baseline: this is the single live call site |
  | `panel/parked/PropertyPanel.tsx` | import + **a call** | excluded by the enumerated `panel/parked/**` exemption, with the reason recorded beside it |
  | `shared/UnresolvedRecordBanner.tsx` | a **comment** naming the function | excluded — comment/JSDoc occurrences are not call sites |

  So the assertion is: **across `src/react/overlay/**`, excluding test files, excluding the defining module, excluding `panel/parked/**` by enumeration, and counting call sites rather than textual occurrences, `applyClassNameEdit` has exactly ONE — in `engine/live-preview.ts`.** A comment mentioning the name must not move the count; a JSDoc `{@link}` must not move the count.
- **Both legs of that gate get run, not just the forward one.** Reverse leg: the untouched tree is GREEN (assert it on the unmodified tree before believing the forward leg means anything). Forward leg: plant a real second call site in a live panel file and confirm the gate names that file. A gate that has only ever been seen green over a tree that already satisfies it is the "green but not evidence" shape this repo has shipped before.

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

**Artifact byte-identity applies per step:** `git diff --exit-code .descvi/screens.json` must be clean for every step. **And it must be run knowing what it can and cannot see, or it becomes exactly the "green but not evidence" shape this repo has shipped before.** Measured on the current artifact: the string `className` appears 17 times and **every one of them is inside an authored Korean `description`** — prose that happens to discuss the chip editor. **No element's className VALUE is recorded anywhere in `screens.json`.** So a pure className write — which is what every v3 gesture and every v3 panel widget produces — **cannot move this artifact, and the gate cannot go RED on it.** It stays in the per-step gate set because it catches the things v3 might do by accident (an element added to a fixture, an extraction path disturbed), and for those it is a real gate. It must never be cited as evidence that a className write behaved. No step in this plan adds a fixture element; if one does, its artifact diff becomes the deliverable and is reviewed as such.

---

### Phase 41 — v3.0 (`feat/phase-41-e3-v3-sizing-align-resize`)

#### P0 — migrate and amend the interaction ontology (docs only)

- **Purpose.** The contract the rest of v3 is built against lands first, in a place it can be edited.
- **Touches.** New `docs/reference/interaction-ontology.md`; `docs/README.md` (`reference/` table row); `docs/e3/tracker.md` (**both** citations — the Refs line and the 2026-07-07 archival note's prefix-less `specs/interaction-ontology.md` (living) entry); `docs/e3/roadmap-v2plus.md` (ladder v3 row, `### v3` 범위 bullet, `### v3` 게이트 리서치 bullet).
- **Must achieve.** The full §5 ADR amendment table applied to the migrated copy; the three roadmap changes applied; **every one of the 38 `file:line` pins in the migrated file converted — the 26 in the body as well as the 12 in References** — each to an anchor (`path#exact source text`) or, where no unique text exists or the number is the point, to an immutable `git show <sha>:path` record; the row-closure criterion written into §6 so a later phase can check it.
- **Acceptance.**
  - **Spelling-independent, so the census cannot pass by matching one form:** `grep -n 'interaction-ontology' docs/e3/tracker.md` returns no line carrying an `.omc/`-relative reference in ANY spelling — neither the `.omc/specs/…` form nor the prefix-less `specs/…` form.
  - `grep -n 'multi-select' docs/e3/roadmap-v2plus.md` returns nothing in the v3 ladder row or the `### v3` section; the 게이트 리서치 bullet names the spike.
  - **Hand-checkable pin conversion, because the gate is blind to this:** a scan of the migrated file for `[A-Za-z0-9_./-]+\.(ts|tsx|md|mts|mjs):[0-9]+` returns **0** hits outside lines that also carry a commit SHA (the immutable-record form the gate itself exempts). Baseline for that scan on the source file today is 38, so the check has a measured before and after rather than an assumed zero.
  - No cell in the migrated §6 v3 row still reads `marquee multi-select` or `Cmd/Shift-click multi-select + align/distribute`; §3.F-5's Alt+handle row reads `deferred-v4`; §3.F-7 reads `deferred-v4-or-later`.
- **Verification.** `node scripts/check-citation-anchors.mjs` GREEN; `node scripts/check-citation-anchors.mjs --selftest` GREEN (proves the instrument can fail). **RED recipe:** corrupt one converted anchor's text by a single character — leg (b) must report it by name. Do this before believing the green. **And state in the commit that the gate's green is not evidence for the pin conversion** — it cannot see a bare `file.ts:NNN` in this file at all, so the grep above is the only instrument for that half.
- **Failure behavior.** If any converted anchor cannot be made unique (the source text repeats in its file), pick a longer enclosing line rather than a line number; if no unique text exists, the citation is a `git show` record instead. Never a line pin. If a body pin's referent cannot be located at all — the code it named is gone — the citation is deleted and the sentence rewritten, not migrated as a guess.
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
  sizingToken("w", { mode: "fill" }, "none")                                   // NOT REPRESENTABLE — see (g)
  ```

- **Touches.** The new module, plus `packages/descvi/src/react/overlay/engine/tailwind-class-model.ts` for all **three** D2 defects: the axis-blind `flex-1` read, the axis-blind `sizingAxisOf` write classification, and the `self-*`-blind strip set.
- **Acceptance.** (a) the assertions above; (b) `w-full`/`h-full` READ BACK as Fill but are never produced; (c) the cross-axis strip removes a stale `self-stretch` when switching Fill → Hug on that axis; (d) the parent-axis-blind `flex-1` read is gone — `flex-1` in a `col` parent reads as **height** Fill; (e) prefixed/important/custom tokens survive every write untouched (the ADV2 property the existing model already holds — do not regress it).
  - **(f) the no-op rule from D2:** re-writing Fill on an axis already expressed as `w-full` produces a className byte-identical to the input. Fill → Fixed → Fill lands on `self-stretch` and is expected to differ.
  - **(g) `ParentAxis: "none"` has one defined behavior and it is a refusal.** `sizingToken` for `mode: "fill"` with a `"none"` parent **throws** rather than returning a token — Fill is meaningless without a flex main axis, and a silently-returned `w-full` there would be the plan inventing a semantic. Hug and Fixed are unaffected by parent axis and return normally. This is the assertion that makes P3 acceptance (d) and P4's refusal set enforceable rather than aspirational: both consume the same refusal.
  - **(h) the write-side axis defect, both directions:** in a `col` parent, switching height Fill → Fixed leaves exactly one height token and **no stale `h-*`**; the symmetric case in a `row` parent (width Fill → Fixed) leaves exactly one width token. Without the `sizingAxisOf` fix, the `col` case leaves two.
- **Verification.** Unit tests beside `packages/descvi/src/react/overlay/__tests__/tailwind-class-model.test.ts` in the same style. **RED recipe:** change the `col`-parent width case to `flex-1`; assertion (a) must fail. **Second RED recipe, for (h):** revert the `sizingAxisOf` fix alone and confirm the `col` height case leaves a stale `h-*` — the two fixes must be independently RED-able or the second one is untested cargo.
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
- **Touches.** A new `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts` (pure controller + thin hook, mirroring the existing ring/shield split); `packages/descvi/src/react/overlay/OverlayShell.tsx` for the handle mount inside the ring layer **and for scoping `aria-hidden` down to the three ring divs per §4.1** (they already each carry it, so this removes a redundant container attribute and changes nothing about how the rings are exposed); `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts` for the bypass; `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts` if the ring's geometry writes move into the drag handler; **`packages/descvi/src/react/overlay/engine/use-preview-session.ts` for the drag-preview seam** — the per-move entry point that bypasses `setDraftChips`. **P4 creates that seam, not P3:** P3 touches the same file only for the widget→chips seam, which rides the existing `handleChipsChange`, and a seam nobody consumes yet is a seam nobody can test. Two steps touching one file is fine; two steps each believing the other created the seam is not.
- **Must achieve.**
  - Eight handles (4 corner, 4 edge) on the selection ring, mounted inside `packages/descvi/src/react/overlay/OverlayShell.tsx#className="z-40 absolute inset-0 overflow-hidden pointer-events-none"` with `pointer-events: auto` on the handle shapes only. Sizes with two precedents: ~8px glyph, ~20px effective hit target, edge strips spanning the full edge.
  - **The shield bypass — exactly two sites, and forgetting either is a known failure.** An early return before suppression when the event target is inside a handle, in **both** `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#const onPointerSuppress = (e: Event) => suppressShieldPointer(e);` and `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#const onClick = (e: Event) => {`. Omitting the `onClick` half reintroduces deselect-on-release (LIVE-C: the synthesized click resolves the handle to `null` and clears the selection). The bypass belongs in the **wiring**, not in `packages/descvi/src/react/overlay/canvas/selection-shield.ts#export function handleShieldSelect(`, which suppresses unconditionally at its top by design.
  - Drag lifecycle: `setPointerCapture` on the handle; per-pointermove preview through the existing controller; **exactly one POST on pointerup**. The per-move path must bypass the chip-editor's `setDraftChips` React commit and write ring+handle geometry directly in the drag handler.
  - Axis semantics: the dragged axis converts to **Fixed at the first size change** (not pointerdown, not release), whatever it was before. Siblings reflow live because the preview is a real DOM write.
  - Clamp at 1px per D3, subject to EG-1's outcome.
  - **Refusals, all visible:** no handles on a non-editable target (no chip session — LIVE-C measured the refusal path already exists); no handles on a **shared-oid** target (KI-10: `reselectBySpecId` resolves by first-match `querySelector` and cannot discriminate instances, so a drag on instance 3 would re-anchor to instance 0 — the panel path already ships for these elements and is unaffected); handle hit boxes clamped to stay inside the ring layer's rect so a full-bleed element's corners are not clipped away by the layer's `overflow-hidden`. **And when the resolved parent axis is `"none"` (a non-flex parent), the handle still renders and still drags** — Fixed sizing is meaningful in any parent — but the Fill-conversion path is unreachable there by P2 acceptance (g), and a double-click-to-Fill gesture (phase 43) refuses with the same reason the panel shows.
- **Acceptance.** (a) one `POST /edit → 200` per drag, asserted, not counted by eye; (b) the committed token is byte-identical to what P3's panel would write for the same final size; (c) mid-drag `#dsh-screen` scroll keeps element, ring and handle in step; (d) undo of a drag-committed resize works through the existing Cmd+Z; (e) a drag on a shared-oid element is refused with a reason; (f) `git diff --exit-code .descvi/screens.json` clean — **but see §7 on why that gate cannot go RED on a className write and must not be cited as evidence that one behaved**.
- **Verification.** jsdom tests for the controller and the bypass; **two Playwright specs**, both of which reproduce deterministically per LIVE-C: the shield-swallow case (without the bypass, zero handle events and a cleared selection) and the post-commit anchor case.
  - **Locator strategy, per §4.1:** handles are located by a stable attribute (`data-dsh-handle` / `data-testid`), never by role, and each spec asserts **existence before behavior** as a separate expectation. Otherwise the shield-swallow spec's RED condition ("zero handle events") is indistinguishable from a locator that matched nothing, and the spec passes hardest exactly when the feature is most broken.
  - **A new spec has THREE registration obligations. Naming only `testMatch` is how two of them get discovered by a red CI job instead of by the plan:**
    1. **`testMatch`** — add the filename to the `design-view` project in `playwright.config.ts`. A missing entry drops the file **silently**; even `--list` exits 0.
    2. **The identity golden.** `e2e/reporters/identity-oracle.ts` compares the collected test set against `e2e/fixtures/expected-identities.json`, whose `distribution` field is a **hand-maintained, hand-reviewed pin** (today `{"failed":2,"passed":64,"skipped":13}`). The regeneration command **refuses to write** when the run's distribution differs from the reviewed pin, so the order is: hand-edit `distribution` deliberately → run `pnpm test:e2e:update-identities` on an **unfiltered** run → review the regenerated identities. The edited pin is a **named deliverable of the commit and is reviewed as one**, not a mechanical byproduct. ⚠ The pin counts RAW `TestResult.status`, which is a different unit from Playwright's own summary (a held `test.fail` counts as passed in the summary and failed in the pin) — a reviewer who reconciles the golden to the summary is "correcting" the one field that exists to be edited by a human.
    3. **The mutable-path declaration.** `e2e/reporters/artifact-oracle.ts`'s clause 4 fingerprints every path in `e2e/fixtures/mutable-paths.json` at `onBegin` and again at `onEnd`, with **existence-plus-byte** semantics: a declared path that appears, disappears, or changes content across the run is RED. **Declaring a path does not license mutating it — it enforces the restore.** These specs drag-commit against `src/app/lab/tests/style-edit/page.tsx`, which **is not in `mutablePaths` today** (the list holds `insert-scratch`, `shared-oid`, `single-screen`, `three-screen`, and the two `.descvi/` artifacts). The spec must therefore restore it byte-exact, and the declaration is what turns that from a claim into a checked one: the file is tracked, so clause 1's `git status` delta already catches a stranded mutation, but as the declaration's own doc puts it, `git status` names a **mode** while the byte check names the **file** — "a restore that puts back different bytes at the same path is the failure this catches first". Every existing mutating lab subject is declared for exactly that reason; follow the convention rather than relying on clause 1 alone. (Do **not** confuse this with `harnessWritten`, which is a different list, holds only `expected-identities.json`, and is the one that carries the `DESCVI_E2E_UPDATE_IDENTITIES=1` exemption.)
  - Plus a live `descvi:dev` smoke: drag, release, read the source diff.
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
- **Gates:** the standard set; one POST per gesture; a Playwright spec for the popup half, carrying **all three registration obligations from P4** (`testMatch` entry · reviewed `distribution` pin then `pnpm test:e2e:update-identities` · mutable-path declaration or verified byte-exact restore for any newly mutated source); `git diff --exit-code .descvi/screens.json` clean.
- **Failure behavior.** If the hatched region's click target and the drag strip cannot be separated reliably at small gaps, the drag strip wins and the popup moves to a click on the hatch outside the strip — never make both ambiguous. If the gap is too small to host a 16px strip, the region is popup-only.

### Phase 43 — v3.2, row closure (`feat/phase-43-e3-v32-row-closure`)

- **Shift aspect-lock**, on **edges as well as corners** (LIVE-B — this is the part a corners-only implementation would get wrong): the dragged edge grows and the perpendicular dimension follows the ratio; a diagonal indicator is shown while locked; **releasing Shift mid-drag unlocks** and the drag continues unconstrained.
- **Edge double-click = Hug** on that axis; **Alt/Option + edge double-click = Fill**. Both Figma-documented and ported verbatim by Onlook. Corner double-click has no action (LIVE-B). This is an **addition** to the amended row rather than an existing cell, adopted because it is the cheapest possible Hug/Fill entry once handles exist and it is already familiar; §3.B's `dblclick` reservation is about the **element** target-type and does not collide (P0 records that).
- **Text acceptance case:** a width drag on a text element converts to Fixed width with auto-height wrap (LIVE-B). This is not new machinery — it is the generic handle applied to a text element — but it is an acceptance case that must be asserted, because "the height follows" is the part that could silently not happen.
- **Row closure — and it reads TWO tables, not one.** The phase does not land until:
  1. the migrated **§6 v3 row** lists only cells that are SHIPPED or reclassified; and
  2. **no `deferred-v3` status cell survives anywhere in §3.x** — the per-gesture matrix is where the status legend actually lives, and §6 is a summary of it. A §6 row that reads clean over a §3.F table still carrying `deferred-v3` is the two-documents-disagreeing failure this plan already fixed once for the roadmap.
  - **One §3.F-6 row needs an explicit disposition rather than a status flip:** `resize handle | absolute element | Write w-[..]/h-[..] (+ may adjust left/top)` is dual-classified `deferred-v3` (size) + `v4` (x/y). v3 never renders a handle on an absolutely-positioned element, because absolute is v4 by owner ruling Q2 and v3 is flow-only. **Disposition: the whole row moves to `deferred-v4`** — its size half is not shipped by v3, and leaving a `deferred-v3` size half on a target type v3 refuses to draw on would leave the row promising something no version is building.
- **Gates:** the standard set; a Playwright spec for aspect-lock-then-release, carrying **all three registration obligations from P4**; the row-closure check is a documentation assertion made in the phase's audit, not a script — so it is stated as two greps (no `deferred-v3` in the migrated file; no `multi-select` in the v3 row) whose expected result is 0, run and pasted rather than asserted from memory.

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
2. **The v3 row is "complete" but some other living document still promises the falsified cell.** P0 migrates the ontology, phases 41–43 ship the cells, and a v4 planner picks the old promise up somewhere the amendment never reached. **The inventory of places that can say it, measured rather than assumed:** the migrated ontology (§6 row + the §3.x status cells — phase-43's two-table check), `docs/e3/roadmap-v2plus.md` (the ladder v3 row **and** the `### v3` 범위 bullet — both in P0's touch list, and both would otherwise have survived this plan's first draft untouched), `docs/e3/tracker.md`'s two ontology citations, and the frozen `.omc/` copy. **Caught by:** P0's spelling-independent tracker grep, P0's roadmap grep, and phase-43's row-closure greps. **Residual, and it is only the last one:** search still surfaces the frozen `.omc/` copy. Accepted — it is a point-in-time record by the repo's own convention, and the living one is indexed in `docs/README.md`. **What is NOT residual and was nearly recorded as such:** the roadmap. It is living and git-tracked, and calling it accepted collateral would have left the version ladder itself — the document a future planner reads first — as the most authoritative statement of the falsified cell.
3. **The late-remeasure fix ships as a widened trigger and creates a storm.** The tempting fix is "remeasure more often" — a `setInterval`, or observing `#dsh-screen`. It papers over the visible tear and costs a re-anchor on every layout event in the page. **Caught by:** P1 acceptance (c), which bounds the re-anchor count for one commit, and D5's stop condition on a continuously-firing observer. **Prevented by:** the fix being scoped to the selected element, whose box is the only thing whose settling matters.

---

## Evidence Gates

### EG-1 — the flex minimum-size floor

- Claim: a committed `w-[Npx]` below the element's content minimum renders at N, so clamping the written value at 1px is sufficient and the ring never disagrees with the number.
- Evidence method: **the subject must be a flex item on the parent's MAIN axis, or the gate cannot fail.** Flexbox's automatic minimum size (`min-width`/`min-height: auto` resolving to a content-based minimum) applies to the **main axis only**; on the cross axis it resolves to zero. So a width drag inside a `flex-col` parent can never floor, and pinning the gate there would guarantee its own pass path by construction. **The discriminating subject is `src/app/lab/tests/style-edit/page.tsx#data-oid="xnf2ei"`** — a `<span className="font-medium">` carrying non-empty Korean text, whose parent `v002k2` is `flex items-center gap-3 …`, i.e. a ROW parent, so width is the main axis and the content minimum is live. Commit descending widths (200px, 60px, 12px, 1px) from the panel and record `getBoundingClientRect().width` beside each written value. **Then measure the control and the second orientation in the same session:** the same descent on `v002k2` (width in the `flex flex-col` parent `seroot` — expected to track exactly, confirming the instrument is not simply always-flooring), and a HEIGHT descent on `v002k2` (height IS the main axis of a column parent — the second combination where flooring is predicted). Three descents, one session, no new code. **The row-parent width case on `xnf2ei` is the observation the gate turns on**; the other two are what tell a flooring result apart from a broken measurement.
- Pass path: (measured width tracks the written value to 1px on the ROW-parent subject) D3 stands as written — clamp the drag at 1px, no further work.
- Alternate path: (measured width floors at the content minimum while the written value keeps falling) the drag's written value is derived from the **measured** box rather than the raw pointer delta, so the number stops when the box stops. `min-w-0` is never auto-injected. The panel's typed input still accepts the smaller number and the ring shows the rendered box — the divergence is visible rather than hidden.
- Required before: P4 (the drag's clamp behavior) and P3's Fixed numeric field.
- Unexpected result: (the element vanishes, the ring inverts, or handles become unhittable at small sizes) **STOP.** Handle geometry has no defined behavior at zero extent; halt P4 and bring the observation back before choosing a floor.

### EG-2 — what actually re-anchors after a commit

- Claim: an element-scoped `ResizeObserver` on `selectedEl` fires after the Tailwind CSS hot-update lands, and is therefore the right trigger for the post-commit re-anchor.
- Evidence method: in a live `descvi:dev` session, attach a throwaway element-scoped `ResizeObserver` logger to the selected element, commit a `w-[Npx]` panel edit, and record: whether it fires, how many times, at what widths, and the final settled box. **Also record, at settle, whether the observed node is still `isConnected` and whether it is still the node `[data-oid="…"]` resolves to** — Lane C measured Fast Refresh patching the className on the SAME node, but the shield's own resolver comments contemplate a re-render swapping the DOM out from under a held element reference, and an observer holding a detached node is silently dead rather than loud. Run it enough times to catch the tear window Lane C hit in 1 of 4 runs. Throwaway code, reverted after.
- Pass path: (it fires, with a final entry at the settled width, on a node still connected and still oid-resolvable) P1 implements the observer shape — connect on selection, disconnect on deselect and unmount, drive `remeasure()`.
- Alternate path: (it never fires, i.e. the box does not change and the tear is a pure measurement race) P1 implements the trailing-tick shape instead — after `commit()` resolves, a bounded sequence of trailing rAF re-anchors, or a re-anchor keyed on the CSS hot-update. Either way the trigger gets its own deterministic unit test, since the live window is not reproducible on demand.
- Third path: (it fires, but the observed node is detached or no longer what the oid resolves to at settle) the observer is re-attached on every reselect rather than only on selection change — the same identity discipline the hover channel already uses, where a stale element reference falls back to a fresh query. This is a real third outcome with its own fix, not a variant of the other two: an observer on a detached node produces the same silence as the alternate path and would otherwise be misread as it.
- Required before: P1, and therefore before P3's numeric commit and all of P4.
- Unexpected result: (the observer fires continuously, or a ring write feeds back into it) **STOP.** A ring write must never resize the observed element; if it does, the ring-layer isolation that BUG-5 established is broken and that is a defect to fix before any observer ships.

### EG-3 — how much of the corpus has a flex parent at all

- Claim: the Fill state is meaningful for the large majority of selectable elements, so a tri-state that leads with Hug/Fill/Fixed is the right default shape.
- Evidence method: in a live `descvi:dev` session, walk every `[data-oid]` under `#dsh-screen` across the corpus screens and record, per element, **both** the parent's computed `display`/`flex-direction` **and** the parent's source `className` — then tally. Recording only the computed value would make this gate's own STOP clause (source-vs-computed divergence) unobservable by construction, since the comparison needs both sides. One script, read-only, no writes.
- Pass path: (non-flex parents are a small minority) the tri-state ships as designed; Fill is disabled with a visible reason on the minority, per P3 acceptance (d).
- Alternate path: (non-flex parents are a large share) the widget leads with Fixed/Hug and Fill is a secondary state, **and** a row is recorded against E4 track 2 — a corpus whose containers are mostly non-flex is a corpus that under-represents what the tool is for, which is a distribution-design finding, not a v3 defect.
- Required before: P3 (the widget's shape and default), and it informs P4's refusal set.
- Unexpected result: (an element's parent display differs between what the source className says and what computed style reports, in a way that would flip the axis routing mid-session) **STOP.** The serializer's `ParentAxis` input would be unstable, and D2's mapping rests on it being stable.

---

## Open Questions

None of these block execution; each would change something if answered.

**OQ-1 — `_scratch` versus E4 track 3 (owner ruling needed; explicitly out of this plan's scope).** `packages/descvi/src/extractor/screen-scan.ts#export const SCREEN_SCAN_IGNORE: readonly string[] = [` contains `'**/_*/**'`, so `src/app/_scratch/` is invisible to the extractor **by construction** — nothing there gets an oid, and nothing there is selectable or editable. E4 track 3's stated purpose is a gitignored sandbox for edit-testing, which that sandbox therefore cannot serve. **Why it matters here:** v3 is the version that most wants a disposable screen to drag things around on, and every live smoke in this plan is consequently pinned to `lab/tests/style-edit` instead. Someone will reach for `_scratch` and find silence. The ruling is the owner's: change the ignore pattern, move the sandbox out from under the underscore, or accept that the sandbox is for source-editing only and say so where people look.

**OQ-2 — do Tailwind scale tokens become a preset concept in v3.x or later?** Owner ruling Q1 defers them to a "variables-like preset" concept, which Figma puts in the same dropdown as Hug/Fill/Fixed, after a divider. **Why it matters:** if the answer is "in v3.x", the sizing widget's layout should reserve that slot now; if "later", it should not, because an empty divider is worse than none. This plan assumes **later** and reserves nothing.

**OQ-3 — batch panel edit over a multi-selection.** LIVE-B says this is what multi-select is actually for in Figma (values show Mixed and an edit writes both). The ADR removes multi-select as a v3 *gesture* cell, and records this as unowned at no version. **Why it matters:** it is the only surviving justification for ever building element multi-select, and if it is wanted, the selection model's single-`selectedEl` shape is what would have to change — a bigger change than any cell in v3.

**OQ-4 — does the alignment widget ever need a canvas affordance?** Verdict 1 mentions a "possibly on-canvas 9-dot affordance" alongside the panel widget. This plan ships the panel widget only. **Why it matters:** if the canvas affordance is wanted, it is a v3.x addition to the amended row and phase-43's row-closure criterion would need to include it, rather than closing without it.

**OQ-5 — the parked structured panel's long-term disposition.** `packages/descvi/src/react/overlay/panel/parked/PropertyPanel.tsx` is kept compiling and green as an un-parking target, and this plan builds its own widgets on the chip session instead. **Why it matters:** after v3.0, the parked tree holds a *second* implementation of the sizing tri-state, with a different serializer and a direct bridge call. Keeping it is now a maintained divergence rather than a dormant option. Either it gets rewritten onto the v3 serializer, or it gets retired under the repo's deletion rule — but "dormant, not dead" stops being true once a live implementation of the same concept exists beside it.
