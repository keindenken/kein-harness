# descvi phase-47 — drag-to-reorder on the canvas

Status: In Review
Status reason: RALPLAN round 2 is open — a fresh Architect and a fresh Critic are reviewing this revised text blind, and approval is absent because no lane has returned against it yet. Round 1 returned MUST_FIX from BOTH lanes on five blocking findings, two of which the lanes reached independently: EG-2 compared a computation against itself and so could not go RED, and the geometric slot list was never reconciled against the engine's own op-unit neighbour chain. All five are addressed in this revision. The owner ruled on 2026-08-27 that one grab-drag-drop gesture must collapse to exactly one undo with the mechanism delegated, which closed this plan's first Open Question and removed the n-undo fallback EG-2's alternate path had rested on. Two load-bearing facts remain held as Evidence Gates with stop boundaries rather than assumed — EG-1 (the eligible-parent population) and EG-2 (whether the fold matches the sequential write path); S47-4 must not start before EG-2 answers. Not executable until this round approves.

---

## 0. RALPLAN-DR summary

### Principles

1. **The gesture may not change what any existing press does.** Three target classes reach the selection shield today and each has a measured behaviour; phase-47 adds a consumer, not a row.
2. **Refuse by measurement, not by declaration.** Where a fact about the live layout decides eligibility, read the live layout. A declaration channel that was built to answer a different question will answer this one plausibly and wrongly.
3. **A refusal names the relationship that is actually broken, and never points at a fix the product does not ship.** That is KI-17, and its closed record is the reason this is a principle rather than a preference.
4. **One gesture, one undo.** The user made one movement; anything that costs N presses of Cmd+Z to reverse is a defect wearing a mechanism's clothes.
5. **The look is ratified live before the write is wired.** A blue line nobody has driven is a guess, and a guess that has already written to disk is expensive to withdraw.

### Decision drivers

1. **Blast radius on the selection shield.** Its own docblock records the arm table being got wrong repeatedly, once in a way that made a whole shipped row unreachable and that only two independent measuring lanes caught. Every option is scored first on how much of that table it disturbs.
2. **Reversibility of the visual half.** The insertion indicator and the drag readout are owner-judged artefacts; the sequence must let the owner reverse them without reversing a write path.
3. **Staying inside "no new write class."** The owner's ruling is the phase's charter. An option that needs a new `StructuralOp`, a new `JournalSubject` arm or a new wire `target` is out, and an option that merely parameterises an existing verb has to be argued as such rather than assumed.

### Real decisions, with options — full arguments in §3

| # | Decision | Chosen | Beaten alternative, and why |
|---|---|---|---|
| DR47-1 | Where the reorder press is armed | The shield's own ordinary arm, **no fourth row** | A fourth arm (changes `defaultPrevented` for nearly every canvas element); a listener above `#dsh-stage` (re-implements the arm table) |
| DR47-2 | How the pointer stream is obtained | **Extend the one shipped travel recording** into a two-consumer stream | A second document-capture stream (doubles the stale-recording surface the shield's own WC-1/WC-2 note records) |
| DR47-3 | Which gestures engage reorder | **Plain drag only** — no Shift, Cmd/Ctrl, Alt | Shift-drag reorder (collides with the shipped Shift travel-swallow on the same target class) |
| DR47-4 | The trailing click after a reorder drag | **A third disjunct in the shipped swallow condition** | Leave it (the release sits over a different element than the press, so the click selects the wrong node) |
| DR47-5 | Multi-select drag | **Refused, with a Korean string, shown in the drag readout** | Silent no-op (reads as a bug); block movement (needs the forbidden new write class) |
| DR47-6 | The n-step move | **One request carrying a step count, folded inside `prepare` → one journal entry → one undo** | N sequential POSTs → N undo entries (**FORBIDDEN by the owner's 2026-08-27 ruling — no longer a fallback**); a second folding mechanism is the live alternate (EG-2) |
| DR47-7 | Which parents admit a reorder | **Geometric flow-order eligibility, measured from the sibling rects, reconciled against the engine's chain (part 3)** | `ParentContext`-driven eligibility (collapses `flex-row-reverse` to `unsupported` and would refuse a reorderable row) |
| DR47-8 | Where the indicator and readout live | **A new `#dsh-reorder-layer`, no `data-dsh-handle`, pointer-events none** | The handle layer (turns three shipped e2e handle censuses RED and walks straight into F46-D's hazard) |
| DR47-9 | The `undo-focus-ownership` rider | **Widen the ownership guard to admit `document.body`** | The owner's own sketch (move default focus to `#dsh-screen`) — rejected with reason, and the owner may overrule |
| DR47-10 | Live-pass placement | **After the paint half ships, before the write is wired** | Before implementation (nothing exists to drive); at the end (a reversal would then reverse a write path too) |
| DR47-11 | Whether the geometric slot list is trusted as the engine's op-unit list | **NO — reconciled against the engine's published `prevOid`/`nextOid` chain and REFUSED on mismatch.** Ruled as part 3 of DR47-7's predicate (§3.7) | Trusting the DOM slot list (round 1: a `{false && <El/>}` op-unit renders nothing, so a one-slot drag commits a 200 that moves nothing; a `.map()` op-unit renders k siblings, so a one-slot drag moves the whole list); detecting it post-hoc in EG-1 (EG-1's stop trigger could not observe it) |

---

## 1. Scope

### IN — exactly three things, per `docs/e3/tracker.md` §"v3 CLOSE" (2026-08-24), re-confirmed by the owner 2026-08-27

1. **Drag-to-reorder as a canvas gesture**, riding the shipped structural verbs in `packages/descvi/src/extractor/structural-edit.ts#export const STRUCTURAL_OPS: readonly StructuralOp[] = ['delete', 'move-up', 'move-down', 'duplicate', 'insert-after'];` — no new write class. Blue insertion indicator.
2. **The cheap B-Q4 mitigation** — a W×H readout during the drag. The `B-Q4` row in `docs/post-loop-backlog.md` carries the owner's ruling that a readout is a legitimate cheaper precursor to auto-scroll, and this gesture is where dragging blind bites.
3. **The `undo-focus-ownership` QoL rider**, routed to 47 because 47 touches focus anyway (the same tracker line).

### OUT — refused as riders by the owner in this session. Each stays UNROUTED and OPEN

| Item | Where it lives | Disposition |
|---|---|---|
| `KI-47` — theme-toggle stale ring/chip colour | `docs/known-issues.md` | **Refused as a phase-47 rider (owner, this session). Stays OPEN and UNROUTED.** It is a ring *colour* defect; this phase paints no ring. |
| `KI-54` — padding-popup outside-click wipes the screen | `docs/known-issues.md` | **Refused as a phase-47 rider (owner, this session). Stays OPEN and UNROUTED.** Cause unknown and undiagnosed; the `commit === true` arm has never been traced. Not a reorder subject. |
| `selection-ring-treatment` — ring rounding / thickness / hover-vs-selection size | `docs/post-loop-backlog.md` | **Refused as a phase-47 rider (owner, this session). Stays OPEN and UNROUTED.** Its own row already records that it is new scope, not phase-46 inheritance. |
| `spacing-affordance-mark` — the single `-` mark direction | `docs/post-loop-backlog.md` | **Refused as a phase-47 rider (owner, this session). Stays OPEN and UNROUTED.** Its row explicitly says no phase owns it and the next destination is an owner ruling. |

Named here so none of them re-enters by silence. Phase-47 must not touch any of the four, and the landing audit at S47-5 re-asserts that.

### OUT and already routed elsewhere

- **B-Q5** (small-element handle admission) → **phase-48**, by owner ruling 2026-08-25.
- **Marquee / rubber-band** → **deferred-v4**.
- **KI-10** (shared-oid reselect lands on instance 0) → **inherited**, not fixed here. It reaches this phase through the journal reselect path and is not made worse by it.

### OUT by scope rule

- `src/app/**` is the dogfood app. The deliverable is `packages/**` plus `e2e/**`. Corpus pages are read as fixtures and edited only by the gesture under test, and any such edit is restored before the story's commit.
- **`undo-history-loss`** is a *different* backlog row from `undo-focus-ownership` — its own row says so and says why. Phase-47 fixes the focus window and does not touch, diagnose, or claim anything about the history-loss observation.

---

## 2. Repo facts, re-read in this tree

Every claim below was re-opened at the moment it was written. Where a claim is a *population*, it is derived by a command that is given.

### 2.1 The shield's ordinary arm halts descent — and that is MEASURED, not reasoned

`packages/descvi/src/react/overlay/canvas/selection-shield.ts#export function suppressShieldPointer(event: ShieldEvent): void {` calls both `stopPropagation()` and `preventDefault()`. The shield binds it in the CAPTURE phase on `#dsh-stage`, so on an ordinary press the event never descends to `#dsh-screen` or to the element. The shield's own docblock carries the control for this: `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#a handle press recorded `handleDown: 0`` — zero with the shield shipped, one with it removed.

**Consequence, and it is the whole of hard point (a):** a reorder listener attached to any DESCENDANT of `#dsh-stage` will never see an ordinary press. That is why the resize machine's listener host is `#dsh-handle-layer` (`packages/descvi/src/react/overlay/canvas/use-resize-drag.ts#  handleLayerRef: RefObject<HTMLDivElement | null>;`) and why ROW D returns with `preventDefault()` **only** — no `stopPropagation` — so the handle's own listener still runs.

**And the correction the brief needs:** the shield does NOT block a *pointer-event* drag. `preventDefault()` on `pointerdown` cancels the native focus / text-selection default and the HTML5 `dragstart` the ontology's §3.F note is about; it does not stop `pointermove`, `pointerup` or `setPointerCapture`. Two shipped drag machines (resize, spacing) prove it. What the ordinary arm blocks is *reaching a descendant listener*, not *dragging*.

### 2.2 The arm table has three rows, and the order is load-bearing

Shipped order in `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#    const onPointerSuppress = (e: Event) => {`:

1. `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#      maxTravelRef.current = 0;` — unconditional, ahead of every arm return.
2. `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#      void takeTrailingClickSuppression();`
3. **ROW P** — `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#      if (isFocusableHandleEvent(e)) return;` — before ROW D, because a focusable handle target is also a handle target.
4. **ROW D** — `preventDefault()`, no `stopPropagation`, return.
5. **Ordinary** — `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#      suppressShieldPointer(e);` then `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#      if (e instanceof MouseEvent) beginTravelRecording(e);`

The gate that pins three rows rather than two is the `defaultPrevented` pair in `e2e/spacing-gesture.spec.ts`: a press on a handle/strip reads `true`, a press on the spacing popup's input reads `false`. The predicate regression that made ROW D unreachable — `closest()` where `matches()` was needed — is recorded on `isFocusableHandleEvent` and was found by measurement, never by reading.

### 2.3 The travel guard is one number with one shipped consumer

`packages/descvi/src/react/overlay/canvas/pointer-thresholds.ts#export const POINTER_DRAG_THRESHOLD_PX = 4;`, recorded as greatest distance from the press point (travel, not displacement), consumed once, at the click:

`packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#        maxTravelRef.current >= POINTER_DRAG_THRESHOLD_PX`, guarded by `shiftKey || selectionRef.current.length > 1`.

The recording lives in `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#    const beginTravelRecording = (e: MouseEvent) => {` with its idempotence/replacement cell `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#const activeTravelGestureRef = useRef<{ pointerId: number | null; stop: () => void } | null>(null);` and three document-capture terminals (`pointerup`, `pointercancel`, effect teardown).

### 2.4 The undo unit is a journal ENTRY, and one entry holds whole-file pre-images

`packages/descvi/src/sidecar/commit-write.ts#export type JournalEntry = { entryId: number; subject: JournalSubject; pageRelPath: string; files: { abs: string; before: string; fromHash: string; toHash: string }[] };`

The structure subject arm is `packages/descvi/src/sidecar/commit-write.ts#  | { kind: 'structure'; op: 'move-up' | 'move-down' | 'duplicate' | 'delete'; screenId: string; oid: string }` — one op, one oid, one entry, and each `structure` POST pushes exactly one entry (`packages/descvi/src/sidecar/server.ts#  async function handleStructureEdit(body: EditBody): Promise<HandleEditResult> {`, `journal: { mode: 'push' }`).

**So N sequential moves cost N presses of Cmd+Z, mechanically.** There is no coalescing anywhere on that path.

**And there is a shipped precedent for folding N into one entry without a new write class:** `packages/descvi/src/sidecar/server.ts#  async function handleClassNameBatchEdit(body: EditBody): Promise<HandleEditResult> {` folds N members inside a single `prepare` over an accumulating buffer, under one lock, pushing one entry. Its own docblock states the invariant that makes the fold sound: nothing a member's splice writes can change what a later member resolves.

`packages/descvi/src/extractor/structural-edit.ts#export function moveAdjacent(` is a pure `string → string` with an optional `expect` baseline. That is the shape a fold needs.

### 2.5 `ParentContext` cannot answer the eligibility question, and the reason is in its own consumer

`packages/descvi/src/react/overlay/engine/tailwind-class-model.ts#export type ParentDirection = "row" | "col" | "unset" | "unsupported";` and `packages/descvi/src/react/overlay/engine/tailwind-class-model.ts#export type ParentWrap = "wrap" | "nowrap" | "unsupported";`, produced by `packages/descvi/src/react/overlay/panel/parent-context.ts#export function readLayoutContext(` and projected by `packages/descvi/src/react/overlay/panel/parent-context.ts#export function deriveParentContext(el: Element | null | undefined): ParentContext {`.

**It maps a REVERSE direction token to `unsupported`.** `packages/descvi/src/react/overlay/panel/LayoutSection.tsx#a reverse token, where the rendered direction IS readable` states it plainly: `direction === "unsupported"` covers two different states, one of which is a `flex-row-reverse` that renders a perfectly readable row. An eligibility predicate keyed on `ParentContext.direction` would therefore refuse a container whose reorder is completely well-defined.

That is not a bug in `ParentContext`. Its docblock says what it is for: *"the truth about what descvi may WRITE"* as a Tailwind token. Reorder does not write a layout token. It is the wrong channel for this question.

### 2.6 There is NO shipped affordance to make a non-flex parent into a flex one

`packages/descvi/src/react/overlay/panel/LayoutSection.tsx#{/* ── The two toggles: ABSENT on a non-flex element (G43-2d's literal clause).` — the direction and wrap toggles do not render at all unless the element's own base layer already carries `flex`/`inline-flex`.

**This falsifies the escape route the ontology's own §3.F-1 cell suggests** (*"may require 'add auto-layout' first"*). A refusal string that tells the user to add auto-layout would name a fix the product does not offer — exactly the KI-17 shape. The honest escape route is the panel's own ↑ / ↓ buttons, which are source-order moves and are available regardless of the parent's display: `packages/descvi/src/react/overlay/panel/StructureSection.tsx#"위로 이동"` / `packages/descvi/src/react/overlay/panel/StructureSection.tsx#"아래로 이동"`.

### 2.7 The engine's refusal vocabulary is closed and total, and it is the WRONG home for the gesture's refusals

`packages/descvi/src/react/overlay/panel/StructureSection.tsx#const REASON_TEXT: Record<StructuralRefusalReason, string> = {` is `Record<StructuralRefusalReason, string>` — a new key is a compile error, deliberately. Its members are facts about the SOURCE (`packages/descvi/src/extractor/structural-edit.ts#  | 'no-adjacent-sibling'`, `packages/descvi/src/extractor/structural-edit.ts#  | 'unequal-indent'`, `packages/descvi/src/extractor/structural-edit.ts#  | 'unsupported-sibling'`, …).

Phase-47's refusals are facts about the LAYOUT ("these siblings are not in one line") and about the SELECTION ("more than one thing is selected"). They are not engine reasons, they must not be added to `StructuralRefusalReason`, and they get their own closed map in the reorder module. Where the ENGINE refuses a move the gesture attempted, the shipped `REASON_TEXT` strings are reused verbatim — a second Korean sentence for `no-adjacent-sibling` would be two answers to one question.

### 2.8 The handle layer is a census with three shipped assertions over it

`e2e/resize-handle-shield.spec.ts`, `e2e/resize-write.spec.ts` and `e2e/resize-handles.spec.ts` each assert `#dsh-handle-layer [data-dsh-handle]` has count 8 (and `e2e/multi-select-shield.spec.ts` asserts it is not 0). Derived by command, not by hand:

```
grep -rn '#dsh-handle-layer \[data-dsh-handle\]' e2e/
```

Any new node placed in `#dsh-handle-layer` carrying `data-dsh-handle` turns those RED, and would also walk into F46-D's hazard by way of `e2e/resize-handles.spec.ts#    const handleLayerEl = document.getElementById("dsh-handle-layer") ?? layerEl;`.

### 2.9 Static corpus proxies (derived by command; each is a PROXY and is labelled as one)

```
grep -ro 'className="[^"]*\bflex\b[^"]*"' src/app --include=page.tsx | wc -l   # 164
grep -ro 'className="[^"]*\bgrid\b[^"]*"' src/app --include=page.tsx | wc -l   #  20
grep -ro 'flex-wrap[a-z-]*'               src/app --include=page.tsx | wc -l   #  18
grep -ro 'data-oid="'                     src/app --include=page.tsx | wc -l   # 798
find src/app -name page.tsx | wc -l                                            #  21
```

⚠ **These are attribute counts, not parent-of-a-selectable-element counts, and they cannot answer EG-1.** An element's layout parent is frequently an oid-less host wrapper — `parent-context.ts`'s own docblock measures 72 of 714 intrinsic host opening tags carrying no `data-oid`, 9 of them carrying `flex` — so a static scan of authored classNames is structurally unable to say what fraction of the 798 selectable elements sit in a reorder-eligible parent. EG-1 is the measurement; these five numbers are only its order of magnitude.

### 2.10 The engine ALREADY publishes its own sibling chain per oid — and round 1 of this plan did not cite it

⚠ **This section exists because both review lanes found the same hole: the round-1 text derived the drop-index contract from DOM element children alone, and never looked for the engine's own answer to "who are this element's siblings". The engine publishes that answer already, and the panel already consumes it.**

The extractor emits, on every structure entry, the source-order neighbour chain: `packages/descvi/src/extractor/edit-map.ts#  parentOid: string | null;`, `packages/descvi/src/extractor/edit-map.ts#  prevOid: string | null;`, `packages/descvi/src/extractor/edit-map.ts#  nextOid: string | null;` — plus the op-unit's kind, `packages/descvi/src/extractor/edit-map.ts#  opUnitKind?: 'conditional-container';`.

**It is computed by the same function the WRITE uses.** `packages/descvi/src/extractor/structural-edit.ts#function adjacentOpUnit(` is the one function that produces both the D7 staleness baseline and the move's swap partner, and `packages/descvi/src/extractor/structural-edit.ts#export function deriveStructuralBaseline(` is what the artifact carries. So the chain in the artifact is not a second opinion about siblinghood — it is the engine's own, and a slot list that disagrees with it is addressing something the write will not move.

**It is reachable from the client for EVERY oid, not just the selected one.** The overlay mirrors the shape at `packages/descvi/src/react/overlay/engine/source-resolver.ts#  opUnitKind?: 'element' | 'conditional-container';` and the map is keyed `editMap.oids[screenId][oid]`, so a walk over a parent's children can look each child's chain up directly. The panel already reads exactly these three fields as its staleness receipt — `packages/descvi/src/react/overlay/panel/StructureSection.tsx#        prevOid: structure.prevOid,`.

**Why the two populations diverge in this corpus, with the idiom counts derived by command (PROXIES — EG-1 is the measurement):**

```
grep -rn '&& <'   src/app --include=page.tsx | wc -l   #  4   — {cond && <El/>}: ONE op-unit, ZERO or ONE DOM node
grep -rn '\.map(' src/app --include=page.tsx | wc -l   # 37   — one op-unit, k DOM siblings (KI-10 shared-oid)
```

Both directions are live. A `{false && <El/>}` op-unit sits in the engine's chain and renders nothing, so a one-slot drag past it computes one step too few and commits a 200 that moves nothing on screen. A `.map()` op-unit renders k siblings under one oid, so a one-slot drag over a card commits a move of the whole list. **Neither is a refusal the user can read**, which is why DR47-11 makes the reconciliation a precondition rather than a residual.

---

## 3. Rulings

### 3.1 DR47-1 — the reorder press is armed **inside the shield's own ordinary arm**. There is no fourth row. (RULED — and this REVERSES the kickoff brief)

⚠ **The brief states that "phase-47 opens a fourth arm in that table." Reading the shipped file says it does not, and this plan reverses that premise loudly rather than silently.** The reversal is stated here, in §0's table, and again in the report to the lead.

The three options:

| Option | What it does | Verdict |
|---|---|---|
| **A-i — a fourth arm (ROW R)** | An ordinary press that is a reorder candidate takes `preventDefault()` without `stopPropagation()`, so a descendant listener sees it | **REJECTED.** Nearly every canvas element is a reorder candidate, so ROW R is not a fourth *class* — it is a rewrite of the ordinary arm. `stopPropagation` is exactly what keeps the host page's own bubble-delegated `pointerdown` handlers from seeing a canvas press, and dropping it for the common case discards the shield's primary job. It also makes the arm table's identity depend on a *layout* predicate evaluated at press time, which is a new and much worse failure surface than the `closest`/`matches` mistake the docblock already records. |
| **A-ii — the shield arms it itself** | The ordinary arm, after `suppressShieldPointer(e)`, additionally arms the reorder gesture beside `beginTravelRecording(e)` | **CHOSEN.** No target class changes behaviour. `defaultPrevented` is unchanged on all three rows. The shield is the one component that legitimately sees every ordinary press, so nothing has to re-derive who owns a press. |
| **A-iii — a listener above `#dsh-stage`** | Bind reorder `pointerdown` at `#descvi-root` or `document`, capture phase | **REJECTED.** Capture runs ancestor-first, so this listener sees a press on a resize handle and on the spacing popup's input BEFORE the shield classifies it — so it must re-implement ROW P and ROW D to stay out of their way. A second copy of the arm table is precisely the defect class this area has already paid for twice. |

**Placement, exactly.** The arming call is the LAST statement of the ordinary arm, after `suppressShieldPointer(e)` and after `beginTravelRecording(e)`. Order relative to the existing arms: **ROW P → ROW D → ordinary(suppress → travel → reorder-arm)**. Placing it before ROW P or ROW D would arm a reorder from a press on a resize handle or on the spacing popup's numeric input.

**What goes RED if the order is wrong** — four legs, each with its RED-when.

⚠ **Round 1 named the shipped `defaultPrevented` triple as the leg that catches a misplaced arming call. It does not, and this plan reverses that claim rather than restating it.** `defaultPrevented` on the popup-input row is `false` because ROW P returns *before* `packages/descvi/src/react/overlay/canvas/selection-shield.ts#export function suppressShieldPointer(event: ShieldEvent): void {`, the only call that invokes `preventDefault()` on that arm. The arming call arms a gesture; it does not call `preventDefault()`. Move it above ROW P and ROW P still returns early, so the popup input still reads `false` and the triple stays green under the exact misplacement it was claimed to catch. **The discriminating measurement is the ARMING COUNT, not `defaultPrevented`.** The triple is retained below, but for the one mutation it genuinely does catch.

| Leg | Home | RED-when mutation | What goes RED |
|---|---|---|---|
| **A — a press on a `data-dsh-handle` target arms ZERO reorder gestures** | new jsdom test beside the shield's | Move the arming call above ROW D | the count reads 1 |
| **B — a press on the spacing popup's `<input>` arms ZERO reorder gestures** | same file | Move the arming call above ROW P | the count reads 1 |
| C — the `defaultPrevented` triple (handle `true`, popup input `false`, ordinary `true`) is byte-identical to HEAD's verdicts | the shipped pair in `e2e/spacing-gesture.spec.ts`, extended with the ordinary row | Make the reorder arm call `preventDefault()` on its own arm | the popup input's press reads `true` — this is the mutation the triple CAN see, and it is the one worth seeing, because it silently rewrites ROW P's contract |
| D — the travel recording still zeroes on every press including handle presses | shipped behaviour, asserted | Move the zeroing below the arming call | a handle press stops zeroing |

Legs A and B are the arm-order gates. Leg C is a no-regression gate on the three rows' `preventDefault` contract and must not be read as evidence about placement.

**Acceptance criteria (S47-2).**
1. `#dsh-stage`'s capture-phase `pointerdown`/`mousedown` listener count is unchanged from HEAD (one handler, both events) — asserted, not assumed.
2. A press on a `data-dsh-handle` target arms no reorder gesture and leaves `defaultPrevented === true`.
3. A press on the spacing popup's `<input>` arms no reorder gesture and leaves `defaultPrevented === false`.
4. A press on an ordinary canvas element arms exactly one reorder gesture and leaves `defaultPrevented === true`.
5. The handler is bound to BOTH `mousedown` and `pointerdown`; two events for one press arm exactly one gesture (jsdom dispatches both — see 3.2).

### 3.2 DR47-2 — ONE pointer stream with two consumers, not two streams (RULED)

`beginTravelRecording` already attaches `pointermove` / `pointerup` / `pointercancel` on the stage's `ownerDocument`, in the capture phase, filtered by `pointerId`, torn down on all three terminals, with a replacement rule for a foreign pointer. The reorder gesture needs exactly that stream and nothing else.

**Chosen:** widen it into an ordinary-press gesture with two consumers — the travel maximiser (unchanged) and the reorder tracker — sharing one `activeTravelGestureRef` cell, one `stop()`, one set of terminals.

**Rejected:** a second, independent document-capture stream owned by the reorder machine. It would double the surface of the failure the shield's own note records — a recording whose terminal never arrives keeps measuring from a press point the user's finger never touched — and it would introduce an ordering question between two streams for one press that nothing in the file can answer.

**Pointer capture: NO `setPointerCapture` is called, on any element, at any point in the gesture. Ruled here, once, and every other section derives from this sentence.** ⚠ Round 1 contradicted itself on this — DR47-2 chose a stream that needs no capture while DR47-8 and §9 both reasoned from a captured pointer. The ruling is *no capture*, for three reasons: (i) the chosen stream is `beginTravelRecording`'s document-capture `pointermove`/`pointerup`, which already sees every move regardless of what is under the pointer, and already counts out-of-stage travel (§2.3); (ii) the reason capture is MANDATORY for the two shipped drag machines does not transfer — `packages/descvi/src/react/overlay/canvas/use-resize-drag.ts# *  1. **Capture is MANDATORY, not an optimisation.** Without` is about keeping the release click retargeted ONTO the affordance so the `data-dsh-handle` bypass keeps matching, and reorder's press target is an ordinary element with no bypass to preserve; (iii) capture on an ordinary canvas element would change the trailing click's target for a gesture the shield already classifies, adding a second mechanism to a question DR47-4 answers with one.

**Two consequences, both load-bearing and both re-derived from this ruling.** DR47-8's indicator does not need capture to stay out of the pointer stream — it stays out because its layer is `pointer-events: none`. And without capture the release click is dispatched on the **nearest common inclusive ancestor of the press target and the release target** (the UI Events dispatch rule), which for a within-parent reorder is the PARENT: so the click certainly fires, and without DR47-4's swallow it would select the dragged element's parent. §9 carries that as a measured leg rather than as an open question.

**Why this is not a refactor risk.** The rename/widening touches one closure in one file, and the recording's three documented properties (out-of-stage travel counts; removal on all three terminals; `pointerId` replacement) are the reorder tracker's requirements too, verbatim. If a later story finds them in conflict, that is a stop boundary, not a merge.

**Acceptance criteria (S47-2).**
6. After a `pointercancel`, zero live document listeners remain, and a subsequent press of the same pointer arms a fresh gesture (both legs, both measured — the count leg fires first).
7. Two simultaneous pointers: the second press replaces the first's recording and the first gesture's reorder tracking is torn down, not left running.
8. The travel number read at the click is byte-identical to HEAD's for every gesture that does not engage reorder. **RED-when:** make the reorder tracker write `maxTravelRef` → the shipped Shift/multi-select swallow rows move.

### 3.3 DR47-3 — reorder engages on a PLAIN drag only (RULED — hard point (b))

**The problem, restated from source.** Today the travel number is consumed once, under `shiftKey || selectionRef.current.length > 1`. Its two Shift meanings are disambiguated by TARGET first (a Shift press on a `data-dsh-handle` is an aspect lock and never reaches the recording at all) and by TRAVEL second (a Shift press on an ordinary element is add/remove-from-selection). **A reorder target is an ordinary element, so the TARGET half of that separation is unavailable to it** and only TRAVEL is left — which the multi-select meaning has already claimed.

**Ruling.** Reorder engages iff, at the press: no `shiftKey`, no `metaKey`, no `ctrlKey`, no `altKey`. The modifier is read at the PRESS for engagement and re-read at the CLICK for the swallow (see DR47-4) — the shield's own note is that a user can press without Shift and be holding it by release, so the two readings genuinely differ and each is read where its question is asked.

**How the signals stay distinguishable.** After this ruling the same `travel ≥ 4` number is consulted by three disjoint predicates over disjoint modifier states:

| Gesture | Target class | Modifier at press | Modifier at click | Travel meaning |
|---|---|---|---|---|
| Aspect-locked resize | `data-dsh-handle` | Shift | (click swallowed by the handle bypass) | per-move engagement, inside the resize machine |
| Add / remove from selection | ordinary | any | Shift | swallow the click |
| Collapse-guard at N > 1 | ordinary | any | none | swallow the click |
| **Reorder (new)** | ordinary | **none** | (see DR47-4) | engage the gesture past threshold |

**What breaks if they are not kept distinguishable.** A Shift-drag on an ordinary element would both (i) be swallowed as a selection toggle and (ii) commit a structural move — a source mutation produced by a gesture the user performed to select something. It would be undoable and it would still be the worst defect this phase can ship, because the user has no model in which that drag writes to disk.

**A Cmd/Ctrl or Alt drag is likewise inert** for reorder. Those modifiers are spoken for by the ontology's §3.F-2 / §3.F-3 / §3.F-5 (absolute move and duplicate-drag, both deferred-v4/v2). Engaging reorder under them would occupy a cell another version is holding, and would have to be un-occupied later.

**Acceptance criteria (S47-2).**
9. A Shift-drag past threshold on an ordinary element: zero reorder gestures armed, zero POSTs, the shipped click-swallow still fires. **RED-when:** drop the modifier gate → a POST appears.
10. Cmd-drag, Ctrl-drag and Alt-drag past threshold on an ordinary element: zero reorder gestures armed, and the shipped Cmd-click parent-resolution still works on a sub-threshold Cmd click.
11. A plain sub-threshold press on an ordinary element: zero reorder gestures engaged, selection resolves exactly as at HEAD.

### 3.4 DR47-4 — the trailing click after a reorder drag is swallowed (RULED)

**Why it must be.** After a committed reorder the release point sits over a DIFFERENT element than the press point — that is what a reorder is. The shipped condition does not swallow a plain click at N ≤ 1, so today's code would let that click resolve a selection against whatever now sits under the pointer. Two bad outcomes, both reachable: the selection lands on a sibling the user did not touch, or (after the write's re-extract and node swap) on nothing, clearing the selection the gesture was operating on.

**Ruling.** Add a third disjunct: the click is swallowed when a reorder gesture ENGAGED during the press that produced it — engaged meaning "passed the threshold", whether it went on to commit or to refuse. Read from the gesture cell, one-shot, consumed at the click exactly as `takeTrailingClickSuppression` is.

**Deliberately NOT** keyed on "a write happened": a refused reorder past threshold has still moved the pointer off the pressed element, so the click is just as wrong there. Keying on the write would leave the refusal case selecting a neighbour, which is the surprising half.

**Deliberately NOT** a fourth latch module. The existing `takeTrailingClickSuppression` is the resize gesture's, owned by `resize-gesture-guard.ts`, and consumed in `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#      terminateActiveResizeGesture();`'s neighbourhood; reorder's cell is the gesture cell the shield already owns, so there is one new read and no new lifetime contract.

**The inherited residual, named rather than rediscovered.** The shield's docblock records that under an injected `selectedTarget` prop the no-Shift half of the guard goes inert against the raw selection set, and states that every injector in the tree is a test. The reorder disjunct is computed from the gesture cell rather than from `selectionRef`, so it does NOT inherit that hole. This is stated because the neighbouring condition does inherit it and a reader will assume symmetry.

**Acceptance criteria (S47-2 for the swallow, S47-4 for the post-write leg).**
12. After a reorder gesture that engaged and committed: the trailing click changes no selection and reaches no page handler. **RED-when:** remove the disjunct → the selection moves to the press and release targets' common inclusive ancestor, which for a within-parent reorder is the PARENT (no capture is taken — DR47-2; §9 carries the derivation). Driven in a browser, because that dispatch rule is the browser's, not jsdom's.
13. After a reorder gesture that engaged and was REFUSED: same.
14. After a reorder gesture that never engaged (sub-threshold): the click selects exactly as at HEAD.
15. The reorder disjunct is one-shot — a second click with no intervening press does not consume it again.

### 3.5 DR47-5 — a multi-member selection REFUSES the drag, with a Korean string (RULED — lead default, adopted with reason)

**The lead default is adopted.** Reason, restated so a reviewer can contest it: `move-up` / `move-down` move ONE op-unit by ONE position. Block movement — N members travelling together, preserving their relative order, across a gap — is not expressible as a sequence of those two verbs without inventing an ordering discipline the engine has no notion of, and expressing it properly means a new composer, which is the new write class the ruling forbids.

**"It cannot happen" is not available**, and the plan does not use it: multi-select is live (`packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#  const selectionRef = useRef<readonly SelectionMember[]>(EMPTY_SELECTION);` mirrors an ARRAY, and the toggle table's T3/T5/T9 rows put more than one member in it).

**What the gesture DOES when the selection holds more than one member.** It arms and it engages past threshold — so the readout appears and the user gets an answer — but it computes no drop target, paints no insertion line, and commits nothing. The readout carries the refusal instead of the W×H. The gesture is refused on the SELECTION, before any layout is read, so it refuses identically in an eligible and an ineligible parent.

**Korean string (deliverable):**

> `"여러 요소를 한 번에 끌어 옮길 수는 없습니다. 하나만 선택한 뒤 다시 시도해 주세요."`

It names the relationship that is actually broken (the size of the selection) and the action that resolves it, and it promises nothing the product does not ship.

**Rejected alternative — silently do nothing.** A dead gesture on a live-looking canvas reads as a bug; the phase-42 refused-readout form exists precisely because this repo already ruled that refusals get words.

**Rejected alternative — drag the pressed member only, dropping the rest of the selection.** It performs a silent selection mutation as a side effect of a movement gesture, which is the T1-collapse defect the travel guard was built to prevent, re-entering through a new door.

**Acceptance criteria (S47-3).**
16. With N = 2 selected, a plain drag past threshold on a member: readout shows the refusal string, zero insertion-line nodes exist, zero POSTs. **RED-when:** remove the selection-size check → an insertion line appears.
17. With N = 2, the refusal is reached in an ELIGIBLE parent too (the check precedes the layout read).
18. The string is asserted by its WORDS, not by a reason code. (The `REASON_TEXT` erratum is explicit that every structural test asserted codes and none asserted words, which is why the wrong-rendering defect survived.)

### 3.6 DR47-6 — one drag is ONE journal entry, via a step count folded inside `prepare` (RULED — hard point (c); gated on EG-2)

**THE OWNER'S RULING, 2026-08-27, given during RALPLAN round 1 in answer to this plan's own first Open Question ("does 'no new write class' admit a repeat count on an existing verb?").** In the owner's framing: *what matters is that one grab → drag → drop collapses to exactly ONE undo; the mechanism is delegated — pick the most efficient one and close it.* Recorded here with its date and provenance rather than deleted, because the question is what the ruling answers.

Two things follow, and the second is the sharper one:

1. A repeat count on an existing verb is **admitted**. C-ii stands as ruled, and the Open Question is CLOSED (§"Open Questions" carries the closure, not the question).
2. **C-i — n sequential POSTs, n undo entries — is now FORBIDDEN, not a fallback.** It was offered to the owner and refused. Nothing in this plan may route to it: not EG-2's alternate path, not a story's failure behaviour, not a lane's judgement call. Where the fold cannot be shown correct, the branch is a DIFFERENT one-undo mechanism or a STOP to the lead (EG-2, rebuilt in §6).

**The fact, from §2.4:** each `structure` POST pushes exactly one journal entry, and one Cmd+Z pops one entry. A drag across n positions is n applications of one verb. Naively that is n POSTs, n entries, n undos.

**Options, priced.**

| Option | Undo cost | Write class impact | Other cost | Verdict |
|---|---|---|---|---|
| **C-i — n sequential POSTs** | **n undos** | none | n lock acquisitions, n re-extracts, n HMR passes — the canvas visibly steps | **FORBIDDEN by the owner's 2026-08-27 ruling.** It is no longer EG-2's alternate path and is no longer any story's fallback. It survives in this table only as the OPPOSING ARM of EG-2's rebuilt comparison — run against a throwaway tree to produce the reference bytes, never as a shipping path |
| **C-ii — one POST carrying `steps: n`, folded inside `prepare`** | **1 undo** | `StructuralOp` unchanged; `JournalSubject` unchanged; wire `target` unchanged; ONE optional integer field on an existing body | one lock, one re-extract, n in-memory parses | **CHOSEN** |
| **C-iii — a new `structure-batch` wire target** | 1 undo | **new write class** | new subject arm, new renderer arm, new refusal surface | **REJECTED — the ruling forbids it** |
| **C-iv — clamp the drag to ±1 position** | 1 undo | none | the gesture stops being a reorder | **REJECTED — it does not ship the feature** |

**Why C-ii is inside "no new write class", argued rather than assumed.** The owner's ruling is that the gesture rides the existing verbs. C-ii adds no `StructuralOp` (`STRUCTURAL_OPS` is untouched), no `JournalSubject` arm (the shipped `{ kind: 'structure'; op: 'move-up' | … }` arm carries the entry unchanged, and `reselectTargetFor` needs no new case), no wire `target`, and no engine composer — `moveAdjacent` is called n times exactly as it is called once today. What it adds is a repeat count on one existing verb. **Round 1 flagged this as the decision most open to contest and routed it to the owner; the owner ruled it admitted on 2026-08-27 (above). It is no longer contested and it has no fallback.**

**The fold's shape, and the one thing it must get right.** `packages/descvi/src/sidecar/server.ts#  async function handleClassNameBatchEdit(body: EditBody): Promise<HandleEditResult> {` is the precedent: validate-and-fold in one pass over an accumulating buffer, inside `prepare`, inside the write lock, returning the next bytes only after every step folds — so the first refusal returns before a byte is written. Reorder's fold differs in ONE respect and it is load-bearing:

- the className fold's members address DISJOINT oids, so a splice cannot change what a later member resolves;
- **the reorder fold applies the SAME oid n times, and each application deliberately changes that oid's structural neighbourhood.**

Therefore the `expect` baseline is compared on step 1 ONLY. Steps 2..n pass no baseline, because the baseline they would be compared against is one this same request just invalidated. That is not a weakening of the staleness contract: the lock is held for the whole fold, so no concurrent write can slip between the steps.

**The assertion a step must prove**, written here because prose cannot fix it precisely enough. ⚠ Round 1 wrote this assertion against the pure composition on both sides, which is the same expression twice; both lanes found it. **The two arms must run different code, so the assertion is stated against the SIDECAR:**

```
arm A: one POST { target: 'structure', op, screenId, oid, steps: n, expect }   → final page.tsx bytes, journal entries pushed = 1
arm B: n POSTs  { target: 'structure', op, screenId, oid, expect: <re-derived each time> }, each its own commitWrite
                                                                              → final page.tsx bytes, journal entries pushed = n

assert  bytesA === bytesB   AND   entriesA === 1   AND   entriesB === n
```

byte-for-byte on the on-disk file, for every n in 1..N and both directions, from a byte-identical starting tree per arm. The entry-count legs are not decoration: they are what proves arm B really took the sequential path and the comparison is not one path measured twice.

**Partial-move policy — RE-RULED, and this REVERSES round 1's ruling. Taken from the critic's finding, with the reason.** Round 1 said a `no-adjacent-sibling` refusal at step k > 1 commits the first k−1 steps as a clamped move. The critic's evidence is that under an unreconciled slot list a step-count error is *indistinguishable* from a genuine overshoot, so that policy silently commits a wrong move under the exact defect DR47-11 exists to catch. It is reversed on that ground:

- **Clamping moves to the CLIENT and happens before the request.** DR47-11's reconciliation makes slot index and op-unit index the same number, so the client knows the reconciled list's bounds and clamps the drop index into them. `n` therefore never asks for more positions than exist, and the last slot stays reachable by gesture — which is the property round 1's policy was protecting.
- **The server-side fold aborts the WHOLE request on ANY refusal at ANY step, `no-adjacent-sibling` included, and writes nothing.** After the client clamp, a refusal at step k > 1 is not an overshoot: it means the client's reconciled view and the server's re-derivation disagree, which is staleness, and staleness must not half-commit. The response is the engine's own status (409 or 422) unchanged.

The asymmetry round 1 ruled is gone; there is now one rule on each side and neither has a special case.

**Acceptance criteria (S47-4).**
19. A drag of n = 3 produces exactly ONE journal entry; `journal.remaining` increments by 1. **RED-when:** replace the fold with a loop of POSTs → it increments by 3.
20. One Cmd+Z after that drag restores `page.tsx` byte-identically to its pre-drag bytes. **RED-when:** same mutation → one Cmd+Z leaves the file two steps from home.
21. **The two-arm sidecar gate (EG-2's rebuilt probe, promoted).** Over the `packages/descvi/test/sidecar/handle-structure-edit.test.ts#import { createSidecar, type EditMeta } from '../../src/sidecar/server.ts';` harness — a real temp repo on disk, real `commitWrite`, real CAS, real journal — arm A (one folded POST) and arm B (n sequential POSTs from a byte-identical copy of the same tree) produce identical `page.tsx` bytes, for n ∈ {1,2,3} and both directions, while pushing 1 and n journal entries respectively. **RED-when (primary):** hoist the parse out of the fold so steps 2..n resolve their spans from step 1's `ModuleContext` instead of re-parsing — arm A then splices against stale spans and either diverges from arm B's bytes or throws `span-sentinel-failed`, while arm B, which never enters the fold, is untouched. **RED-when (backup, if the primary mutation is refused by the type system):** apply the fold's steps in reverse order. The two arms execute different code by construction — arm B goes through `packages/descvi/src/sidecar/server.ts#  async function handleStructureEdit(body: EditBody): Promise<HandleEditResult> {` n times with n disk read-backs and n `packages/descvi/src/extractor/structural-edit.ts#export function deriveStructuralBaseline(` re-derivations; arm A goes through it once.
22. A drag refused at ANY step writes nothing: `git diff --exit-code` on the corpus page is clean and `journal.remaining` is unchanged. **RED-when:** restore round 1's partial-move policy (commit the first k−1 steps on a `no-adjacent-sibling` at step k) → the diff is non-empty and the entry count increments.
23. `STRUCTURAL_OPS` is byte-identical to HEAD, and `JournalSubject` gains no arm. Asserted by test, not by review.
41. **The element lands where the blue line promised.** Driven end-to-end in `e2e/reorder-gesture.spec.ts`, not in jsdom: after a committed n-step drag and the re-extract settling, the dragged element's index among its parent's rendered `[data-oid]` element children equals the slot index the insertion line displayed at release. **RED-when:** compute the step count from the RAW DOM slot delta instead of DR47-11's reconciled list, against a fixture parent carrying a `{false && <El/>}` sibling → the element lands one slot short of the line's promise while every other criterion in 19–23 stays green. This criterion is the feature's correctness core and round 1 shipped without it; the RED-when is what proves it is not scaffolding.

### 3.7 DR47-7 — eligibility is GEOMETRIC and measured, not declared (RULED — hard point (d))

**The question is not "is this parent flex".** It is: **does source order drive visual order here, and are the siblings laid out along one axis?** Those are two different questions and only the second is about flex.

**Rejected — `ParentContext`-driven eligibility.** §2.5: it collapses `flex-row-reverse` to `unsupported`, so it refuses a container whose reorder is entirely well-defined. It also cannot see a component-internal CSS-authored flex parent as anything but `directionSource: 'computed'`, and it says nothing at all about whether the children actually line up.

**Rejected — pure geometry (sibling rects alone).** Monotonic sibling rects do NOT imply that a source-order move produces the expected visual result. A CSS `grid` with explicit placement, or a flex container whose children carry `order`, can be visually monotonic while source order is unrelated to it. A move there would teleport the element somewhere the blue line did not promise.

**CHOSEN — a THREE-part predicate, all three required.** ⚠ Round 1 ruled two parts and left the third as a residual in the pre-mortem; both lanes found that the residual is the feature's correctness core. Part 3 is DR47-11 and is ruled below.

**Part 1 — the parent is a FLOW-ORDER container.** Read `getComputedStyle(parent).display` once. Admitted: `flex`, `inline-flex`, `block`, `flow-root`, `inline-block`, `list-item`. Refused: `grid`, `inline-grid`, `table` and every `table-*`, `contents`, `none`. Additionally refused if ANY candidate sibling's computed `order` is not `"0"`.

*Why `block` is admitted at all:* block-level children stack in source order along Y by definition, and the panel's own ↑/↓ already move them correctly. Refusing them would refuse the single most common container in the corpus for a reason that is false of it.

**Part 2 — the siblings are ONE LINE.** Collect the parent's element children, take their rects, and require that they are non-overlapping and monotonically ordered along exactly one axis, in DOM order. The axis that satisfies it is the drag axis; if both or neither satisfy it, the parent is refused.

**Why part 2 is free.** It is not an extra check bolted on — it IS the drop-index computation. The same sorted rect list produces the insertion index, the blue line's coordinates, and the eligibility verdict. There is one pass.

**Part 3 — DR47-11: the slot list RECONCILES with the engine's own op-unit chain, or the parent is refused.** (RULED. This is the round-1 correction both lanes reached independently; §2.10 is the evidence.)

The predicate builds two sequences for the candidate parent and requires them to be **equal as sequences of oids**:

- **The geometric slot list** — the parent's rendered element children in DOM order, as part 2 already sorted them.
- **The engine chain** — starting from the dragged element's oid, walk `prevOid` back to `null` and `nextOid` forward to `null` through the edit map (`editMap.oids[screenId][oid].structure`), collecting oids in source order, and require every entry's `parentOid` to equal the dragged element's `parentOid`.

Equal length, equal order, position by position. Anything else refuses the parent:

| Disagreement | What it means in this corpus | Verdict |
|---|---|---|
| the engine chain is LONGER | an op-unit renders nothing — `{false && <El/>}`, §2.10's 4 sites | refuse |
| the geometric list is LONGER | one op-unit renders k DOM siblings (`.map()`, KI-10 shared-oid, §2.10's 37 sites), or a slot is an oid-less host wrapper the engine cannot address (§2.9's 72-of-714) | refuse |
| equal length, different order | source order does not drive visual order — the same fact part 1's `order` check is after, caught by measurement instead of by declaration | refuse |

**Why this is a precondition and not a post-hoc check.** Once the two sequences are equal, the slot index and the op-unit index are the same number by construction, so DR47-6's step count `n` is exactly the number of `move-up`/`move-down` applications the engine will perform. That is what makes the blue line's promise a promise. Round 1 derived `n` from geometry alone and routed the disagreement to EG-1, whose stop trigger fires only on a REFUSED ↑/↓ — and in both live cases above the ↑/↓ are ENABLED, so EG-1 as written could not produce its own trigger. Detection was unreachable; this makes it structural.

**Cost.** Three field reads per sibling from a map the overlay already holds, in the pass part 2 is already making. No new channel, no new fetch, no new classifier.

**⚠ The scope consequence, named rather than absorbed.** This will refuse parents round 1's predicate admitted, and how many is unknown — a `.map()`-rendered list is one of the most common shapes in this corpus. **How many is EG-1's job, and EG-1's alternate path is where an owner question about widening lives.** If EG-1 shows the reconciliation refuses so much that the phase ships mostly refusals, that is a scope question for the owner and the lead, not a lane decision, and it is NOT resolved by relaxing part 3 — relaxing it restores the silent wrong write.

**Four consequences that fall out rather than needing their own rulings:**

- **`flex-row-reverse` / `flex-col-reverse` work.** Part 2 tests monotonicity **in DOM order**, so a reversed row is monotonic *decreasing* along X — which is still monotonic, and the sign tells the mapping which direction a leftward drop means. Nothing reads a direction token.
- **`flex-wrap` needs no separate ruling.** A container that has actually wrapped fails part 2 (its children are not monotonic on either axis) and refuses. A container that *declares* `flex-wrap` but currently fits on one line passes and is correct at that moment. ⚠ **The residual is stated, not hidden:** a wrapping container refuses or admits depending on the current viewport, so the same element can be draggable at one window size and not another. Accepted: it is honest about what is on screen, which is the thing the blue line has to be honest about.
- **Grid refuses by part 1**, before any geometry is read.
- **A one-child or zero-child parent** refuses at part 2 with the "no sibling" relationship, and reuses the engine's shipped `packages/descvi/src/react/overlay/panel/StructureSection.tsx#  "no-adjacent-sibling": "이 방향에 형제 요소가 없습니다.",` string rather than minting a second sentence for the same fact.

**Korean strings (deliverables). THREE new sentences, and they name the layout or source relationship, never a fix the product does not offer (§2.6, KI-17):**

| Refused because | String |
|---|---|
| part 1 — the parent is not a flow-order container (grid, table, `order` present) | `"이 상위 요소는 소스 순서대로 배치되지 않아 끌어서 순서를 바꿀 수 없습니다. 패널의 위로 이동 · 아래로 이동 버튼을 사용해 주세요."` |
| part 2 — the siblings are not on one line | `"형제 요소들이 한 줄로 이어져 있지 않아 끌어 놓을 자리를 정할 수 없습니다. 패널의 위로 이동 · 아래로 이동 버튼을 사용해 주세요."` |
| part 3 / DR47-11 — the slot list and the engine chain disagree | `"화면에 그려진 형제 요소와 소스의 형제 구성이 서로 달라 끌어 놓을 자리를 정할 수 없습니다. 패널의 위로 이동 · 아래로 이동 버튼을 사용해 주세요."` |
| the selection holds more than one member (DR47-5) | `"여러 요소를 한 번에 끌어 옮길 수는 없습니다. 하나만 선택한 뒤 다시 시도해 주세요."` |

⚠ **The part-3 string deliberately does NOT say "형제 요소가 없습니다" ("there is no sibling").** The critic's point: on a `.map()`-rendered list the user is looking at four siblings, and a refusal claiming there are none is the KI-17 shape — a sentence that is false about what is on screen. It says the two orders disagree, which is the fact, and it points at the ↑/↓ buttons, which work on exactly these parents.

Each points at `packages/descvi/src/react/overlay/panel/StructureSection.tsx#"위로 이동"` / `packages/descvi/src/react/overlay/panel/StructureSection.tsx#"아래로 이동"` — an affordance that exists, is enabled on exactly these parents, and does the thing the user was trying to do.

**Acceptance criteria (S47-1, driven as a pure module; re-driven live at S47-3).**
24. The eligibility module is a pure function of `(parent display, sibling rects in DOM order, sibling order values, sibling oids in DOM order, the engine chain looked up per oid)` and touches the DOM and the edit map through two injected readers — so its table is unit-testable without a browser.
25. Table rows, each measured: `flex-row` → row; `flex-col` → col; `flex-row-reverse` → row, reversed mapping; `block` with block children → col; `grid` → refused (part 1); `display:table` → refused (part 1); a flex row carrying `order` on a child → refused (part 1); a wrapped row → refused (part 2); a single-child parent → refused, `no-adjacent-sibling` string.
26. **RED-when:** admit `grid` in part 1 → the grid row flips to eligible while every other row stays green, proving part 1 is load-bearing on its own.
27. **RED-when:** test monotonicity in VISUAL order rather than DOM order → the `flex-row-reverse` row's mapping inverts.
28. No new member is added to `StructuralRefusalReason`; the four new strings live in the reorder module's own closed map, and that map is `Record<ReorderRefusal, string>` so a new reason is a compile error (the discipline `REASON_TEXT` already establishes). The strings are asserted by their WORDS, per acceptance 18's reason.
42. **DR47-11's reconciliation table, each row measured against a fixture whose geometry passes parts 1 and 2** — so a failure can only be part 3. Rows: (a) three rendered siblings, chain of three, same order → eligible, and the drop index equals the op-unit index for every slot; (b) chain of four where one op-unit renders nothing (`{false && <El/>}`) → refused, part-3 string; (c) four rendered siblings whose chain has one entry (one `.map()` op-unit) → refused, part-3 string; (d) a rendered child carrying no `data-oid` between two oid-bearing ones → refused, part-3 string; (e) equal length, permuted order → refused, part-3 string. **RED-when:** delete part 3 and keep parts 1 and 2 → rows (b)–(e) all flip to eligible while rows of acceptance 25 stay green, which is exactly the round-1 predicate and is what makes the mutation the right one.
43. The step count handed to the write is computed from the RECONCILED list, never from the raw DOM slot delta, and the drop index is clamped to the reconciled list's bounds on the CLIENT (DR47-6's re-ruled partial-move policy). **RED-when:** clamp against the raw slot list instead → fixture row (b) asks for one step too few and acceptance 41 goes RED.

### 3.8 DR47-8 — the indicator and the readout live in a new `#dsh-reorder-layer` (RULED)

**Ruling.** One new sibling layer, `#dsh-reorder-layer`, holding two nodes: the blue insertion line and the drag readout. `pointer-events: none` on the layer. **No node in it carries `data-dsh-handle`.**

**Why the marker is wrong here.** The marker's meaning, per its own corrected docstring, is *"a canvas affordance that owns its own pointer, and whose press must reach its own listener"*. The insertion line owns no pointer — it is paint in a `pointer-events: none` layer, which (per DR47-2's capture ruling: **no `setPointerCapture` is taken anywhere in this gesture**) is exactly why it never enters the pointer stream. Round 1 justified this as "paint under a captured pointer"; there is no captured pointer, and the layer's `pointer-events: none` is the whole mechanism. Marking it would make the shield treat a press on it as ROW D, and it would enter `#dsh-handle-layer`'s census.

**Why the layer is new rather than reused.** §2.8: three shipped e2e specs assert `#dsh-handle-layer [data-dsh-handle]` has count 8. And `e2e/resize-handles.spec.ts#    const handleLayerEl = document.getElementById("dsh-handle-layer") ?? layerEl;` is F46-D's fallback — under it, `readScene` collects the ring layer instead, where a stray marked node would be mis-classified by `isCorner(c) = c.length === 2` and read as a geometry verdict.

**The readout's look is ADOPTED, not chosen.** `packages/descvi/src/react/overlay/canvas/use-spacing-drag.ts#export const SPACING_READOUT_ID = "dsh-spacing-readout";`'s family — the 3 px leading accent in the node's own hue, and the FLIP-never-CLAMP placement rule — is the shipped treatment for a cursor-adjacent readout, and phase-46 already ruled that a fourth treatment in this ring is what it exists to prevent. Phase-47 takes it. The refusal readouts take the refusal hue the same family already uses.

**Acceptance criteria (S47-3).**
29. `#dsh-handle-layer [data-dsh-handle]` still counts 8 during and after a reorder drag, and `#dsh-reorder-layer [data-dsh-handle]` counts 0 at every moment of the gesture.
30. Derived by command, not by hand — the sweep that proves nothing new carries the marker. ⚠ **Round 1's sweep was `grep -rn 'data-dsh-handle' … | grep -i reorder`, which only matches when the word "reorder" is in the path or on the line. A marker added in `OverlayShell.tsx` — the file S47-3 names as the new layer's host — would not have matched, so its zero result was not evidence.** The instrument is a set comparison between two different trees instead:
    ```
    git grep -l 'data-dsh-handle' -- packages/descvi/src/react/overlay/ | sort > /tmp/p47-now
    git grep -l 'data-dsh-handle' main -- packages/descvi/src/react/overlay/ | sed 's|^main:||' | sort > /tmp/p47-base
    diff /tmp/p47-base /tmp/p47-now
    ```
    must produce no output, and the story shows the command with its result. The command names 15 files on `main` today (`git grep -l 'data-dsh-handle' main -- packages/descvi/src/react/overlay/ | wc -l`) — a number the command re-derives rather than a number to trust. **Non-zero check, required before the zero is believed:** plant `data-dsh-handle` in a scratch file under that directory, re-run, confirm the `diff` reports it, remove it. A sweep that has not been shown able to speak has not been shown to be silent.
31. The readout's DOM shape and computed styles match the spacing family's on the accent, the ink and the flip rule. **RED-when:** write a `border` shorthand after the shared styler → the accent is wiped (the exact hazard the spacing popup's own note records).
32. The B-Q4 content: the readout shows the dragged element's live W×H throughout the drag. **RED-when:** freeze it at the press box → it stops tracking a reflowing element.

### 3.9 DR47-9 — the `undo-focus-ownership` rider: widen the guard, do not move focus (RULED)

**The defect, from source.** `packages/descvi/src/react/overlay/OverlayShell.tsx#const owned = stage.contains(active)` combines with the text-field yield above it. A panel value field remounts on commit (`key={value}`), focus falls to `document.body`, and `body` is neither inside the stage nor inside any listed host — so `owned` is false and Cmd+Z does nothing until the user clicks an element. The same dead window exists with nothing selected.

**There is a SECOND exit on the same path, and round 1 measured only the first.** `packages/descvi/src/react/overlay/OverlayShell.tsx#      if (!(active instanceof Element)) return;` returns before the ownership test whenever `document.activeElement` is `null` — a state the spec permits (no focused element, and in some browsers a focused element inside a detached or cross-document context). Whether the observed dead window ever *presents* as `null` rather than as `body` is not established, and this plan does not claim it does. **The ruling covers both anyway, because covering only one is how the round-1 text ended up with a guard whose measurement could not see half its own surface:** the widening admits `active === null` as owned as well as `document.body` / `document.documentElement`, and the `null` arm gets its own acceptance criterion (44 below) rather than being assumed equivalent to the `body` arm. The text-field yield is unaffected in the `null` case — there is no element to be inside a field.

**Options.**

| Option | Verdict |
|---|---|
| **The owner's sketch** — make default focus fall to `#dsh-screen` so the ownership guard is always satisfied | **REJECTED here, and the owner may overrule.** It is a focus MOVEMENT, and the backlog row's own "decide" line names the collision it has to clear: the canvas selection / focus-steal family (KI-31). Buying a keyboard fix with a focus-movement change is the larger of the two available changes and the one with a known collision class — and phase-47 is already the phase that touches focus, which is precisely why it should not be the phase that also moves it. |
| **CHOSEN — admit `document.body` (and `document.documentElement`) as owned** | It is the exact complement of the observed window: focus fell to `body`, so `body` is what the guard must not treat as foreign. No focus moves. No selection changes. The text-field yield still runs FIRST and is untouched, so a Cmd+Z inside any field still goes to the field. |
| Widen to "the overlay is alive ⇒ owned" | **REJECTED.** It intercepts Cmd+Z when focus is on a genuinely foreign element, which is the thing the ownership guard was added for. |

**Bounded surface, stated.** The widening makes Cmd+Z reach the sidecar when focus is on `body` — i.e. when nothing in the document is focused. In design-view the overlay is the document, so there is no other plausible owner of that keystroke. The residual is that a host page which itself listens for Cmd+Z on `document` in the bubble phase now loses it while focus is on `body`; the handler is already capture-phase and already `preventDefault()`s, so this widens *when* that happens rather than introducing it.

**Acceptance criteria (S47-5).**
33. With focus on `document.body` and a non-empty journal, Cmd+Z fires exactly one `bridge.undo` call. **RED-when:** revert the widening → zero calls (this is the shipped dead window, so the RED state is HEAD's behaviour and the mutation is a revert).
34. With focus inside a panel `<input>`, Cmd+Z fires zero `bridge.undo` calls (the yield is unchanged).
35. With focus on an element genuinely outside the overlay tree, Cmd+Z fires zero calls.
44. With `document.activeElement === null` and a non-empty journal, Cmd+Z fires exactly one `bridge.undo` call. **RED-when:** widen only the `body`/`documentElement` case and leave the `instanceof Element` early return as HEAD's → zero calls, while criterion 33 stays green. That divergence is the point: it is what shows 33 and 44 measure two different exits on one path.
36. The live leg: in `descvi:dev`, commit a panel value field, press Cmd+Z without clicking anything, observe the undo land. This is the leg the backlog row was raised from and it is the one that has to be driven, not reasoned. `e2e/undo-cmdz.spec.ts` is the home.
37. The row is closed in `docs/post-loop-backlog.md` in the doc commit, and `undo-history-loss` is explicitly left OPEN with a line saying phase-47 did not touch it.

### 3.10 DR47-10 — the live pass sits between the paint half and the write half (RULED)

The owner's standing preference is one live break on UI/UX-heavy items, after planning or after implementation. The insertion indicator does not exist yet, so there is nothing to drive before implementation — placing the pass "after planning" would produce a conversation about a description, which is the thing phase-46 spent five review rounds learning is not evidence.

**Ruling.** S47-3 ships the gesture with FULL paint and NO write: the indicator, the readout, the refusal strings, the drop-index computation, all live, and release commits nothing. The live pass runs at the end of S47-3. S47-4 wires the write afterwards.

**What this buys.** A reversal of the look, the line's thickness/colour/placement, the readout's content or the refusal wording costs one paint-only story and reverses no write path. It also gives the owner the one thing a static description cannot: whether the blue line lands where their hand expects it to.

**What it costs.** One extra story boundary and one extra commit. Named and accepted.

---

## 4. F46-D — determined, and the answer is NO

**Determination: phase-47 does NOT touch `readScene`, so the `getElementById("dsh-handle-layer") ?? layerEl` fallback removal is NOT phase-47's.**

The derivation, rather than an assertion:

1. The phase's new furniture goes in `#dsh-reorder-layer` and carries no `data-dsh-handle` (DR47-8), so it is outside `readScene`'s universe under BOTH the primary read and the fallback.
2. The phase's e2e home is a new spec, `e2e/reorder-gesture.spec.ts`, plus rows appended to `e2e/spacing-gesture.spec.ts` (the arm-table `defaultPrevented` gate's shipped home) and `e2e/undo-cmdz.spec.ts` (the rider). None of those is `e2e/resize-handles.spec.ts`.
3. No story in §5 edits `e2e/resize-handles.spec.ts`.

**The standing condition is carried forward, not dropped.** If any story ends up editing `e2e/resize-handles.spec.ts#    const handleLayerEl = document.getElementById("dsh-handle-layer") ?? layerEl;`'s function, the removal becomes that story's by F46-D's own standing reason, and the story must take it. S47-5's landing audit checks this by command:

```
git diff --name-only main...HEAD -- e2e/resize-handles.spec.ts
```

Empty ⇒ the determination held. Non-empty ⇒ the removal was owed and must be in the diff.

---

## 5. Story ladder

Per `AGENTS.md`: implement → independent verification pass → atomic commit, one logical change per commit, Conventional Commits, and **the whole-set audit runs as each story LANDS**.

### S47-1 — the eligibility module and the refusal vocabulary (pure)

- **Purpose.** Land DR47-7 as a pure, unit-drivable module before anything touches the shield.
- **Touches.** New `packages/descvi/src/react/overlay/canvas/reorder-eligibility.ts` (the THREE-part predicate incl. DR47-11's reconciliation, the drop-index computation, the client-side clamp, the axis and reversal determination) and a new closed Korean map beside it. New unit test file under `packages/descvi/src/react/overlay/__tests__/`.
- **Depends on.** Nothing. The engine chain it reconciles against is read through an injected lookup, so the module needs no live edit map to be driven.
- **Acceptance.** 24–28, 42, 43.
- **Verification.** `pnpm gates`. Expected: green, including step 12's citation-anchor leg over this plan. Failure behaviour: an eligibility row that disagrees with its own RED-when mutation stops the story — it means the predicate is not the thing being tested.
- **Commit.** `feat(descvi): phase-47 S47-1 — reorder eligibility, measured from the flow and the rects`

### S47-2 — the arm, the stream, and the click swallow (no paint, no write)

- **Purpose.** Land DR47-1 through DR47-4. This is the highest-risk edit in the phase.
- **Touches.** `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts` (the ordinary arm's last statement; the widened recording; the third swallow disjunct), a new reorder gesture module in the same directory, and rows appended to `e2e/spacing-gesture.spec.ts` plus new jsdom tests.
- **Depends on.** S47-1 (the gesture asks the module whether to engage).
- **Acceptance.** 1–15.
- **Verification.** `pnpm gates`, then `pnpm test:e2e`. **Legs A and B of DR47-1's table — the ARMING-COUNT assertions — must each be shown RED under their own arm-order mutation before either is believed green.** Do not substitute the `defaultPrevented` triple for that: it does not move under those mutations (DR47-1's warning), and reading its green as confirmation is the recorded failure mode of this exact file. Leg C's own mutation (make the reorder arm call `preventDefault()`) is driven separately.
- **Failure behaviour.** If the widened recording changes the travel number read at the click for ANY non-reorder gesture (acceptance 8), stop. That is DR47-2's stop boundary and it means the two consumers are not compatible; route to the lead rather than reconciling in-lane.
- **Commit.** `feat(descvi): phase-47 S47-2 — the reorder press rides the shield's ordinary arm`

### S47-3 — the indicator, the readout, the refusals, and the LIVE PASS (still no write)

- **Purpose.** Land DR47-5 and DR47-8, and put the whole gesture in front of the owner while a reversal is cheap.
- **Touches.** `packages/descvi/src/react/overlay/OverlayShell.tsx` (the new layer), a new `use-reorder-affordances.ts`, and a new `e2e/reorder-gesture.spec.ts`.
- **Depends on.** S47-2.
- **Acceptance.** 16–18, 29–32.
- **Verification.** `pnpm gates` + `pnpm test:e2e` + **a real `descvi:dev` smoke** — `AGENTS.md` is explicit that unit tests routinely mask defects only a running server exposes, and an insertion indicator is exactly that class.
- **The live pass** (DR47-10) runs at the end of this story, over: the line's colour, thickness and inset; whether the line sits between the two neighbours or flush against one; the readout's position, content and whether W×H is the right pair; the four refusal sentences read as Korean (DR47-7's three plus DR47-5's). **The owner's readings are RECORDED, not silently applied** — that is the shape phase-46's live pass established.
- **Failure behaviour.** A look reversal is re-paint within this story. A reversal of WHERE the line is computed (e.g. "the line should follow the pointer, not snap to a slot") changes S47-1's drop-index contract and re-opens S47-1; that is a story boundary crossing and goes to the lead.
- **Commit.** `feat(descvi): phase-47 S47-3 — the blue insertion line, the drag readout, and the refusals`

### S47-4 — the write, and one drag = one undo

- **Purpose.** Land DR47-6.
- **Depends on.** S47-3, and on **EG-2 having answered**.
- **Touches.** `packages/descvi/src/sidecar/server.ts` (`handleStructureEdit`'s body validation and its `prepare` fold), `packages/descvi/src/react/overlay/engine/sidecar-bridge.ts` (the request shape), the reorder gesture's release path, and gates in `packages/descvi/src/__tests__/` plus `e2e/reorder-gesture.spec.ts` and `e2e/structural-editing.spec.ts`.
- **Acceptance.** 19–23, 41.
- **Verification.** `pnpm gates` + `pnpm test:e2e` + **artifact byte-identity**: after the gesture's own writes are reverted, re-run the extractor and `git diff --exit-code .descvi/screens.json` must be clean. Phase-47 is not meant to move the artifact; if it does, that diff is a defect, not a deliverable.
- **Failure behaviour.** A fold whose on-disk output is not byte-identical to the sequential arm's (acceptance 21) stops the story — see EG-2's stop boundary. **The lane may NOT resolve it by shipping n sequential POSTs: the owner refused n undos on 2026-08-27 (DR47-6).** The branch is EG-2's alternate mechanism, and if that also fails, the route is the lead.
- **Commit.** `feat(descvi): phase-47 S47-4 — one drag, one journal entry, one undo`

### S47-5 — the rider, the landing audit, and the document sweep

- **Purpose.** Land DR47-9; run the whole-set audit that per-story verification cannot see; leave no correction to a reader.
- **Touches.** `packages/descvi/src/react/overlay/OverlayShell.tsx` (the guard widening), `e2e/undo-cmdz.spec.ts`, and — in a SEPARATE doc commit — `docs/e3/tracker.md` (a phase-47 section, the v3 CLOSE line's status), `docs/post-loop-backlog.md` (`B-Q4` mitigation shipped; `undo-focus-ownership` CLOSED; the four refused riders re-marked OPEN and UNROUTED), and `.omc/specs/interaction-ontology.md` §3.F-1 — **row by row, because the section has six rows and this phase ships one of them.** ⚠ Round 1 said "the plain-drag rows move to SHIPPED", which would mark a durable spec shipped for four behaviours that do not exist:

  | §3.F-1 row | Phase-47's edit |
  |---|---|
  | `element in flex/auto-layout parent` · within-parent | **deferred-v2 → SHIPPED at phase-47.** The "WOULD do" cell is rewritten to what shipped: reorder within the parent, blue insertion indicator, subject to DR47-7's three-part predicate — so the cell says *flow-order and one-line and reconciled*, not *flex*. |
  | `element in flex parent` · cross-parent | **UNCHANGED — deferred-v2 (hard).** §8's follow-ups already name it as untouched. |
  | `element in non-flex (block/grid) parent` | **Cell REPLACED, class SPLIT.** The `"may require 'add auto-layout' first"` escape route is deleted and §2.6 is cited as falsifying it (no shipped affordance makes a non-flex parent flex — a refusal naming it would be the KI-17 shape). `block` / `flow-root` / `inline-block` / `list-item` parents that pass parts 2 and 3 → **SHIPPED at phase-47**, same as row 1. `grid` / `inline-grid` / `table*` / any child carrying `order` → **REFUSED BY RULING at phase-47**, with DR47-7's part-1 Korean string named. The `"undefined blue-line; clarify at gate"` gate cell is discharged and says so. |
  | `component instance` | **within-parent → SHIPPED at phase-47; cross-parent and def-move → UNCHANGED.** The gesture's predicate reads display, rects, oids and the engine chain, and never asks whether a node is an instance, so an instance in an eligible parent reorders through the same `move-up`/`move-down` on its JSX node. The row's own `(def move = v5)` parenthesis is untouched — nothing here moves a definition. |
  | `selection box (drag the selection)` | **Class REPLACED.** N = 1 is row 1 by construction (the box is not a separate press target — DR47-8's layer is `pointer-events: none` and the press lands on the element). N > 1 → **REFUSED BY RULING at phase-47** (DR47-5), with its Korean string named. It is no longer deferred-v2: it has an answer. |
  | `stage background (empty)` | **UNCHANGED** — routes to §3.F-6 (marquee, deferred-v4 per §1). |

  Each changed cell carries a `v3-cell` anchor back to this plan's DR number.
- **Acceptance.** 33–37, 44, plus:
  38. The landing audit's own findings are recorded in `docs/e3/tracker.md`'s phase-47 section whether or not they are fixed here — the phase-46 precedent is that an unrouted note left inside a source comment routes to nobody.
  39. §4's `git diff --name-only` check is run and its result recorded.
  40. The four refused riders are re-checked by command against the diff:
      ```
      git diff --name-only main...HEAD
      ```
      and none of `use-selection-rings.ts`, the padding-popup close path, the ring model or the spacing affordance geometry appears. A hand-written claim that they were not touched is exactly the "sweep list that was a proper subset" defect phase-46 hit three times.
  45. `.omc/specs/interaction-ontology.md` §3.F-1 still has SIX rows after the edit, and exactly the rows the table above marks SHIPPED say SHIPPED. Checked by re-reading the section, not by trusting the diff — a row silently merged away is the failure this criterion exists for.
- **Verification.** `pnpm gates` + `pnpm test:e2e` + the live leg of acceptance 36.
- **Commits.** `fix(descvi): phase-47 S47-5 — Cmd+Z owns the keystroke when focus falls to body`, then `docs(e3): phase-47 — the landing audit, the ontology cells, and the routing`.

---

## 6. Evidence Gates

### EG-1: the eligible-parent population

- Claim: the fraction of the 798 oid-bearing corpus elements whose layout parent passes DR47-7's THREE-part predicate (parts 1 and 2 and DR47-11's reconciliation) is high enough that this phase ships a gesture rather than mostly shipping refusals.
- Evidence method: with `descvi:dev` running, walk every `[data-oid]` in each screen and evaluate the shipped `reorder-eligibility` module (S47-1's) against its live parent; report, per screen and in total, the buckets `eligible / refused-part-1 / refused-part-2 / refused-part-3 / refused-single-child`. **And — the round-1 correction — for EVERY candidate parent, eligible or not, emit the two populations side by side: the geometric slot oids in DOM order, the engine chain oids in source order, their two lengths, and the first index at which they differ.** Round 1 reported four bucket counts and made the mismatch observable only through a REFUSED ↑/↓; §2.10 shows both live mismatch shapes leave the ↑/↓ ENABLED, so the round-1 method could not observe the thing it was assigned. Cheapest discriminating observation because both sequences are already computed by the predicate — the probe is the module plus a walk, and it prints what the module already knows.
- Pass path: eligible ≥ 40% of selectable elements ⇒ S47-3's live pass leads with the working gesture and the refusal strings are secondary furniture; proceed as planned.
- Alternate path: eligible < 40% ⇒ the refusal strings are the phase's primary user-facing surface. S47-3's live pass leads with the four refusal sentences and their placement, and the owner is asked (a) whether `block` containers with inline-level children, which part 2 refuses, are the missing population, and (b) whether the `.map()` population that part 3 refuses is large enough to be a scope question for phase-47 at all. **Both are owner questions and neither is answered by relaxing the predicate** — a relaxed part 3 restores the silent wrong write DR47-11 exists to stop.
- Required before: S47-3's live pass. It decides what that pass is about. It is NOT required before S47-1 or S47-2.
- Instrument check, required before any zero or any bucket count is believed: run the walk against a page known to contain a `.map()` (§2.10's command finds 37 sites) and confirm the mismatch report is NON-empty there. A census that has not been shown able to report a mismatch has not shown that it found none.
- Unexpected result: the two populations differ on a parent the predicate nonetheless calls ELIGIBLE. **STOP.** That is part 3 not doing what DR47-11 rules it does, and every downstream number — the drop index, the step count, the blue line's promise — is unsound. Route to the lead before S47-3.

### EG-2: one folded write produces the same bytes as n sequential writes

⚠ **REBUILT. Round 1's EG-2 compared the in-memory fold against the n-fold composition of the same pure function, which is the same call sequence on both sides of an equality — it could not go RED, and both lanes found it independently. This version's two arms run different code, and it is now the plan's own instance of the standing rule that a gate must be able to fail.**

- Claim: **one folded `structure` request produces byte-identical on-disk `page.tsx` to n sequential single-step `structure` requests**, for both directions, on a real page, through the real server path — while pushing one journal entry instead of n.
- Evidence method: the shipped sidecar harness `packages/descvi/test/sidecar/handle-structure-edit.test.ts#import { createSidecar, type EditMeta } from '../../src/sidecar/server.ts';` — a temp repo on disk, a real `createSidecar`, real `commitWrite` CAS, a real journal. From one fixture tree, take two byte-identical copies:
  - **Arm A** — one POST carrying `steps: n`, folded inside `prepare` (DR47-6's mechanism), one lock, one entry.
  - **Arm B** — n POSTs through `packages/descvi/src/sidecar/server.ts#  async function handleStructureEdit(body: EditBody): Promise<HandleEditResult> {`'s shipped single-step path, each with its own lock, its own disk read-back, its own `packages/descvi/src/extractor/structural-edit.ts#export function deriveStructuralBaseline(` re-derivation of `expect`, its own CAS and its own entry.

  Compare the final `page.tsx` bytes, and assert the entry counts are 1 and n. **The entry-count legs are the proof that the arms are different paths**, which is precisely what round 1's version lacked.
- What makes it able to go RED, stated as a mutation and driven before the green is believed: **hoist the parse out of the fold** so steps 2..n resolve their spans from step 1's `ModuleContext` rather than re-parsing (`packages/descvi/src/extractor/structural-edit.ts#export function moveAdjacent(` re-parses on every call today, and that is the property under test). Arm A then splices against stale spans and either diverges from arm B's bytes or throws; arm B never enters the fold and is unmoved. If the type system refuses that mutation, the backup is to apply the fold's steps in reverse order. Drive one, record which.
- Pass path: DR47-6 stands. Acceptance 21 promotes this probe to a permanent gate in S47-4.
- **Alternate path — a REAL branch that still delivers ONE undo.** ⚠ Round 1's alternate was "fall back to n sequential POSTs, n undo entries". **The owner was offered exactly that on 2026-08-27 and refused it** (DR47-6), so it is not a path and must not be restored. If arm A and arm B diverge, the branch is a DIFFERENT one-undo mechanism, not a different undo count: keep one request, one lock and one journal entry, and replace the fold's inner call — instead of applying `moveAdjacent` n times, apply the whole `computeStructuralEdit` n times over the accumulating buffer inside the same `prepare`, which is by construction the per-step semantics arm B exercises, executed once under one lock. Re-run EG-2 against that mechanism, unchanged.
- **Stop, not a third path.** If the replacement mechanism ALSO diverges from arm B, the divergence is in the shipped single-step path composing with itself at all — a defect in code that ships today, outside phase-47's charter. **STOP and route to the lead.** Do not ship n undos, and do not ship a fold whose output has not been shown equal to the sequential bytes.
- Required before: S47-4. Nothing else depends on it.
- Unexpected result: arm B — the SHIPPED path, run n times — throws on step 2 with anything other than `no-adjacent-sibling` (e.g. `span-sentinel-failed`, `reparse-failed`). **STOP.** That is a defect in a shipped path, not a phase-47 question. Route to the lead; do not work around it.

---

## 7. Pre-mortem

### S1: the fourth arm goes in anyway

- Caught by: acceptance 2–4 read as **arming-count** assertions — legs A and B of DR47-1's table — each driven RED under its own arm-order mutation before it is believed. ⚠ **NOT by the `defaultPrevented` triple.** Round 1 named the triple here and declared the residual closed on it; the triple does not move when the arming call is placed above ROW P or ROW D (DR47-1's warning states the mechanism), so that closure was false. Leg C keeps the triple for the mutation it can see.
- Prevented by: DR47-1 placing the arming call as the LAST statement of the ordinary arm, so there is no new branch to get the order of.
- Residual: **named, not "None".** Legs A and B live in jsdom, so arm-order discrimination is proven against jsdom's event dispatch rather than a browser's; the browser leg of this file is leg C, which measures `preventDefault` and not arming. Nothing in the phase measures arm order in a real browser, and this is accepted because the arming call has no browser-dependent behaviour — it reads modifier flags and a target from the same event object jsdom hands it. If a later story gives the arming call any layout- or capture-dependent behaviour, that assumption expires and the residual becomes a gap.

### S2: the drag writes from a gesture the user made to select

- Caught by: acceptance 9 (Shift-drag past threshold produces zero POSTs), with the RED-when being the removal of the modifier gate.
- Prevented by: DR47-3's press-time modifier gate, which is evaluated before any layout is read, so there is no path where a modified drag reaches a drop-index computation.
- Residual: a user who presses plain, drags, and presses Shift before release still commits a reorder. That is correct — the gesture they performed was a plain drag — but it is a case where the click-time and press-time modifier readings disagree, and it is recorded rather than gated.

### S3: the blue line promises a position the write does not deliver

⚠ **REWRITTEN. Round 1 said "Prevented by: nothing structural" and accepted this as a residual, routing detection to EG-1 — whose stated measurement could not observe it (§2.10). Both lanes found it. It is now prevented structurally and gated in three places.**

- Caught by: acceptance 42 (DR47-11's reconciliation table, five rows, RED-when = delete part 3), acceptance 41 (the element lands at the index the line displayed, driven end-to-end, RED-when = compute the step count from the raw slot delta), acceptance 43 (the step count comes from the reconciled list), and EG-1's rebuilt per-parent mismatch report.
- Prevented by: **DR47-7 part 3 / DR47-11.** The slot list and the engine chain must be equal as sequences of oids before the parent is eligible at all, so slot index and op-unit index are the same number by construction, and a drag whose two populations disagree is refused with a Korean sentence rather than committed as a 200 that moves nothing (or that moves a whole `.map()`-rendered list).
- Residual: **the reconciliation is only as good as the artifact.** The engine chain is read from the edit map, which is a build product; a stale edit map yields a stale chain, and the reconciliation would then compare against yesterday's source order. This is not new — it is the same staleness the panel's ↑/↓ already carry, and it terminates in the server's own D7 re-derivation under the write lock, which 409s on mismatch. So a stale chain produces a refused write, never a wrong one. Second residual: part 3 refuses correct-but-unaddressable parents (a `.map()` list is genuinely reorderable in source; the engine simply has one oid for k nodes). That is KI-10's shape, inherited, and widening it is an owner question in EG-1's alternate path — not a lane's.

### S4: the phase reverses the look after the write has shipped

- Caught by: nothing — by the time it happens the write is on disk.
- Prevented by: DR47-10's story boundary. S47-3 ships paint with no write, the live pass runs there, and S47-4 cannot start until the look is ratified.
- Residual: None.

### S5: a refused rider re-enters by silence

- Caught by: acceptance 40's command-derived diff check at S47-5.
- Prevented by: §1's exclusion table naming all four with their disposition, which is what a reviewer reads the diff against.
- Residual: the four rows stay OPEN and UNROUTED after this phase, so the next lane inherits the same silence risk. That is the owner's ruling, not a gap in this plan.

---

## 8. ADR

**Decision.** Ship drag-to-reorder as a consumer of the selection shield's existing ordinary press arm, with geometric flow-order eligibility measured from the live layout **and reconciled against the engine's own published op-unit chain before any parent is eligible**, one folded server request per drag producing one journal entry, and a paint-only story that ends in an owner live pass before any write is wired.

**Drivers.** (1) Blast radius on the shield's arm table, whose own record is of repeated, measurement-only-detectable errors. (2) Reversibility of the owner-judged visual half. (3) The owner's "no new write class" charter.

**Alternatives considered.**
- *A fourth arm in the shield's arm table* (the kickoff's own premise). Rejected: nearly every canvas element is a reorder candidate, so the "fourth class" is the ordinary class, and admitting it drops the `stopPropagation` that is the shield's primary job.
- *A reorder listener above `#dsh-stage`*. Rejected: capture order forces it to re-implement ROW P and ROW D.
- *`ParentContext`-driven eligibility*. Rejected: it collapses `flex-row-reverse` to `unsupported` and would refuse a container that reorders correctly; it answers "what may descvi write", not "does source order drive visual order".
- *Pure sibling geometry*. Rejected: visually monotonic does not imply source-order-driven (grid with explicit placement; flex `order`).
- *Geometry WITHOUT reconciliation against the engine chain* (round 1's own ruling). Rejected on both lanes' evidence: the two populations diverge in this corpus in both directions, the failure is a silent successful write rather than a readable refusal, and the round-1 detection route (EG-1's stop trigger) could not observe either shape. See DR47-11.
- *n sequential POSTs*. **FORBIDDEN, not merely rejected**: the owner was offered n undos for one gesture on 2026-08-27 and refused it. It survives only as EG-2's reference arm, run against a throwaway tree.
- *Committing a partial move when step k > 1 refuses* (round 1's own ruling). Reversed on the critic's evidence: after reconciliation a mid-fold refusal is staleness, not overshoot, and half-committing staleness is a silent wrong write. Clamping moved to the client, where the bounds are known.
- *A `structure-batch` wire target*. Rejected: it is the new write class the owner's ruling forbids.
- *Multi-select block drag*. Rejected: not expressible in `move-up`/`move-down`, so it needs the forbidden new composer.
- *The owner's own `undo-focus-ownership` sketch (default focus to `#dsh-screen`)*. Rejected in favour of the guard widening, on the ground that a focus MOVEMENT has a named collision class (KI-31 family) that a guard widening does not; the owner may overrule.

**Why chosen.** The chosen set is the only one in which no shipped target class changes behaviour, no new write class appears, the reversal of the look costs one paint-only story, and every eligibility answer is a measurement of the thing the blue line is about to claim.

**Consequences.**
- The shield's ordinary arm gains one statement and its travel recording gains a second consumer; that closure becomes the phase's single highest-risk edit and carries three RED-when'd legs.
- `handleStructureEdit`'s body gains one optional integer and its `prepare` gains a bounded loop; `STRUCTURAL_OPS`, `JournalSubject` and the wire `target` set are all byte-identical to HEAD.
- A wrapping container's eligibility becomes viewport-dependent — honest about what is on screen, and recorded as a residual.
- **The eligible population is narrower than round 1 assumed**, because part 3 refuses every parent whose rendered children and source op-units are not the same sequence — including `.map()`-rendered lists (one oid, k nodes) and parents holding an unrendered `{cond && <El/>}`. How much narrower is EG-1's measurement, and a widening is an owner question, never a lane's.
- **No `setPointerCapture` is taken anywhere in the gesture**, so the release click is dispatched on the press and release targets' common inclusive ancestor — the parent — which is what DR47-4's swallow exists to absorb.
- `docs/post-loop-backlog.md`'s `B-Q4` mitigation and `undo-focus-ownership` rows close; the four refused riders stay OPEN and UNROUTED.

**Follow-ups (named, not scheduled, and NOT routed by this plan).**
- Auto-scroll at the viewport edge — `B-Q4`'s confirmed direction, of which this phase ships only the cheaper precursor.
- Cross-parent drag, absolute drag, Alt-duplicate-drag, marquee — ontology §3.F cells this phase does not touch.
- Whether `block` containers with inline-level children should be admitted (EG-1's alternate path may raise it as an owner question).

---

## 9. Residual risk and unverified facts

- ⚠ **UNVERIFIED — the fold's per-step parse cost.** `className-batch`'s own note prices a page parse at ~2.6 ms on the largest corpus page. A reorder fold of n = 3 is 3 parses inside the lock. Not measured here; expected to be immaterial against the shipped 32-member cap's ~83 ms, and stated as an expectation rather than a measurement.
- **The release click after a reorder drag — re-derived from DR47-2's capture ruling, and no longer an open question about whether it fires.** ⚠ Round 1 reasoned from "reorder holds capture on an ordinary element", which contradicted DR47-2's own choice of stream; DR47-2 now rules that **no capture is taken**. Without capture, a click is dispatched on the nearest common inclusive ancestor of the press target and the release target, so for a within-parent reorder the click fires **on the parent** — it does fire, and without DR47-4's swallow it would select the dragged element's parent. That makes acceptance 12–15 non-inert and gives 12 a concrete RED-when (remove the disjunct → the selection lands on the parent). **DERIVED from the UI Events dispatch rule, not measured** — S47-2's e2e leg measures it, and the derivation is written here so that a lane which finds no click knows it has falsified something and must say so rather than declaring the rows inert.
- **KI-10 is inherited unchanged.** A reorder of a shared-oid element resolves reselect to instance 0 after an undo, exactly as `className-batch` does. Not made worse, not fixed.
- **The pinned-`selectedTarget` residual** in the shield's click arm is inherited but not extended: DR47-4's disjunct reads the gesture cell, not `selectionRef`.

---

## Open Questions

- ~~**Does "no new write class" admit a repeat count on an existing verb?**~~ **CLOSED — owner ruling, 2026-08-27, given during RALPLAN round 1.** Kept here with its provenance rather than deleted, because the closure is the answer to a question this plan asked. The owner's framing: *what matters is that one grab → drag → drop collapses to exactly ONE undo; the mechanism is delegated — pick the most efficient one and close it.* So: the repeat count is admitted (DR47-6 / C-ii stands), and **n sequential POSTs with n undo entries is now FORBIDDEN rather than a fallback** — it was offered and refused. Every place round 1 routed to it has been rewritten: EG-2's alternate path is a second one-undo mechanism plus an explicit stop to the lead, S47-4's failure behaviour says so, and the C-i row in DR47-6's option table is re-marked.
- **NEW, raised by round 1 and routed rather than taken: does DR47-11's reconciliation refuse so much of the corpus that phase-47's scope needs revisiting?** The reconciliation is required for correctness and this plan does not soften it — but it refuses every `.map()`-rendered list (37 idiom sites by §2.10's command, a proxy, not a count of refused parents) and every parent holding an unrendered `{cond && <El/>}` (4 sites). If the eligible population lands low, the honest options are (a) ship phase-47 as mostly-refusals with good sentences, (b) route a follow-up phase to give the engine per-instance addressing for `.map()` children (that is KI-10's territory and a much larger change), or (c) reduce phase-47's scope. **All three are owner/lead decisions and none is a lane's.** EG-1 produces the number; its alternate path is where the question is asked. Non-blocking for S47-1 and S47-2, which are unaffected by the answer; it must be answered before S47-3's live pass, which is what EG-1 already gates.
- **Should the `undo-focus-ownership` fix be the owner's own sketch instead?** DR47-9 rejects moving default focus to `#dsh-screen` in favour of admitting `document.body` to the ownership guard, on the ground that a focus movement carries a named collision class. The sketch is the owner's, so the reversal is flagged. It matters because the guard widening closes the *observed* dead window and the sketch would close a slightly wider class — if the owner has seen dead windows the widening does not cover, the sketch wins and S47-5 changes shape.
- **What should a reorder drag do when it leaves the parent?** The ruling scopes phase-47 to WITHIN-parent reorder (`move-up`/`move-down` cannot express anything else), so a pointer dragged outside the parent's box is clamped to the nearest end slot. The alternative — refusing while outside, and showing no line — is arguably clearer. It matters because it is the difference between a drag that always ends in a defined place and one that can end in nothing, and it is exactly the kind of thing the S47-3 live pass answers better than a plan does. Not blocking: the clamp is the shipped default and the live pass may change it inside S47-3.
- **Is the W×H pair the right readout content for a reorder?** `B-Q4`'s rationale is about dragging blind during a RESIZE, where W×H is the quantity being changed. During a reorder the quantity being changed is a POSITION, and W×H may be the wrong number on the right principle. The owner's ruling names W×H explicitly, so the plan ships W×H; the live pass at S47-3 is where a better answer (a slot index, a neighbour name) would surface if there is one.
