# RALPLAN — phase-47 (E3 v3.5): drag-to-reorder, and its four ruled riders

Status: Draft
Status reason: Provisionally executable. Every material decision this phase needs is RULED here from source — the N-step commit (DR47-1), the gesture's listener home (DR47-2, which REVERSES the kickoff brief's central premise), the drop model (DR47-4), the trailing click (DR47-5), the readout's home (DR47-6), KI-47's real fix (DR47-7, whose recorded fix direction is FALSE against source), and `undo-focus-ownership` (DR47-8). Two things are NOT decided and are gates rather than stories: **KI-54's cause** (EG-1 — a measurement, never a guessed fix) and **the per-step parse cost that sets `MAX_MOVE_STEPS`** (EG-2). Both have both branches pre-decided here. Nothing in this plan waits on the owner's live pass, which is pure inspection after the phase lands (§4).

**Parent plan: `.omc/plans/ralplan-e3-v3-direct-manipulation.md` — APPROVED and BINDING.** v3 (phases 41–45) is CLOSED and merged. `docs/e3/tracker.md` §"v3 CLOSE (2026-08-24…)" is the scope authority for this phase and this plan does not re-derive it; §1 carries every owner ruling with its provenance. `.omc/specs/interaction-ontology.md` §3.F-1 is the behaviour authority for the gesture, and this phase is what closes its *"undefined blue-line; clarify at gate"* note — **this document IS that gate.**

**Tree:** branch `phase-47-drag-reorder-in-kein`, a git worktree nested inside the repo root, drafted at `a7007ff`. Predecessor phase-46 shipped 2026-08-27 with `node scripts/gates.mjs` GREEN (`docs/e3/tracker.md` §"GATE SURFACES AT CLOSE"); this plan re-ran no gate of its own and says so where it matters.

**Evidence labels.** **READ** = read from current source at the moment the sentence was written. **RUN-P** = a probe this plan ran whose instrument was shown able to produce a non-zero result. **INHERITED** = taken from a prior record, re-read but not re-measured. **⚠ UNVERIFIED** = not established against source or a run; §9 collects every one.

> ⚠ **THREE THINGS THE KICKOFF BRIEF ASSERTED ARE FALSE AGAINST SOURCE AND ARE REVERSED HERE, NOT QUIETLY CORRECTED.** (1) *"The ordinary arm's `preventDefault()` structurally blocks every drag gesture today"* — it does not, and the shipped shield proves it (§2.2). (2) *"KI-47's fix direction: both hooks already receive a `dark` prop, so wiring it into the effect dependencies removes the class sniffing"* — `dark` is **already** in all three dependency arrays and the sniff survives anyway; the recorded fix direction is stale and `docs/known-issues.md` is corrected by this phase (§2.8). (3) The lead default's *rationale* for refusing multi-select drag — *"a block move is not something `move-up`/`move-down` can express"* — is false; a contiguous block of K moved N slots is exactly K×N adjacent swaps. **The RULING stands on different ground and §3.6 states it.**

---

## 0. RALPLAN-DR summary

### Principles (5)

- **P47-1 — The gesture RIDES the shipped verbs, and "rides" means the server re-proves every swap with the shipped resolver.** Owner ruling 1 forbids a new write class. The strongest available reading of that is not "send the same verb name" but *"the bytes this phase writes are bytes N presses of the shipped button would have written"* — which is a property a gate can assert by byte comparison, and DR47-1 does.
- **P47-2 — The drop model reads the ARTIFACT's own sibling chain, never DOM order.** `edit-map.ts` already publishes `parentOid`/`prevOid`/`nextOid` **for every oid** (`packages/descvi/src/extractor/edit-map.ts#  parentOid: string | null;`, and the two fields beside it). Source order is therefore a published fact, and any client walk of the DOM to re-derive it is the classifier-vs-composer divergence class `docs/reference/structural-limits.md` deletes in terms (*"Resolve coordinates on the client"* — the engine will not, and neither will this client).
- **P47-3 — A LOOK or FEEL value the live pass may reverse must be a VALUE, never a gate edit.** Phase-46's P46-3, inherited. Every number this phase mints — the indicator's thickness, the readout's content, the flow-axis tolerance — is a named constant with a hand-written oracle, so a reversal is an edit to the constant plus the literals this plan PUBLISHES (F46-B's lesson: the price is published in the plan or it is discovered by mutation later).
- **P47-4 — A refusal names the relationship the USER is in, not the engine's code.** KI-17's closed record is the standing lesson: *"가장 흔한 거절이 틀린 관계를 이름 부른다"* — `non-canonical-separator`'s Korean text talked about siblings while `insert-child` was about a container's interior. A drag refusal that renders `StructureSection.tsx`'s `REASON_TEXT` verbatim would be KI-17's exact shape on a new surface, because those strings are worded for a BUTTON in a panel. §3.5 words them for the gesture.
- **P47-5 — A cause nobody has traced is written as a GAP, not as a shape.** `docs/known-issues.md` KI-54 says this about itself in terms: *"그럴듯한 원인을 적어 두는 것이 공백을 적어 두는 것보다 나쁘다."* KI-54 is EG-1 in this plan, never a story with a fix.

### Decision drivers (3)

- **D47-1 — A drag of N slots is N structural writes unless the repetition moves server-side, and the undo unit is the JOURNAL ENTRY.** (READ, §2.1.) `packages/descvi/src/sidecar/commit-write.ts#export type JournalEntry = { entryId: number; subject: JournalSubject; pageRelPath: string; files: { abs: string; before: string; fromHash: string; toHash: string }[] };` — an entry is a full-file preimage, and `undo` pops entries. So N client POSTs are N Cmd+Z presses for one gesture, N HMR round trips and N re-extractions **and** a reachable half-landed state when step k refuses. The repetition has to move under one `commitWrite`, and the only question is what shape it takes there.
- **D47-2 — The shield's arm table is NOT this phase's obstacle; the trailing CLICK is.** (READ + INHERITED-browser, §2.2/§2.3.) The ordinary arm already runs a document-scoped pointer gesture on every ordinary canvas press — `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#      if (e instanceof MouseEvent) beginTravelRecording(e);` sits immediately after `suppressShieldPointer(e)`, and its listeners are `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#      doc.addEventListener("pointermove", onTravel, { capture: true });`. That recording is exercised in a real browser by `e2e/multi-select-shield.spec.ts#(i) a SHIFT-drag past the threshold releasing INSIDE the same element leaves the selection unchanged`. **A pointer drag on an ordinary canvas element is therefore already a shipped, browser-gated capability.** What is NOT solved is the click that follows the release, and phase-45's guard does not cover the single-selection plain case by construction (§2.3).
- **D47-3 — The ontology's own classification of the non-flex case is wrong in one half, and the half it is wrong about is the majority of the corpus.** (READ, §2.6.) §3.F-1 says a non-flex parent makes reorder *"ambiguous (no flow axis)"*. That is true of **grid** and of a **wrapped** row; it is false of ordinary **block** flow, whose children stack in source order along the block axis and are exactly as reorderable as a flex column. A refusal policy written from that row would refuse the commonest container in the corpus, and it would name a relationship that does not hold — P47-4's failure on the phase's flagship deliverable.

### Real decisions, with options

| # | Decision | Options considered | Chosen | Why the loser lost |
|---|---|---|---|---|
| **DR47-1** | How a drag of N slots becomes ONE write | **(a)** N sequential single-step POSTs from the client; **(b)** an optional `steps` count on the SHIPPED `move-up`/`move-down`, executed as N in-memory applications of `moveAdjacent` inside ONE `commitWrite`; **(c)** a new `move-to-index` wire verb; **(d)** the client sends a span rotation | **(b)** | **(a) loses on four measurable costs and one unnameable state.** N journal entries = N Cmd+Z (D47-1); N page writes = N HMR round trips, and `docs/e3/tracker.md` KI-19's record measures that path as HMR-dominated; N re-extractions; N selection handoffs through `handleStructureSaved`'s retry budget. The unnameable state is the decisive one: if step k refuses (`unequal-indent`, `unsupported-sibling` — both permanent per `docs/reference/structural-limits.md`'s move section), the element is left between where it was and where the user dropped it, and there is no request that describes that outcome. **(c) is refused by owner ruling 1 in terms**, and independently by `docs/reference/structural-limits.md`'s posture *"Resolve coordinates on the client … No client-side classifier, no derived anchor field"* — a target index is a coordinate. **(d) re-derives the admission the shipped resolver owns**, which is the third-implementation class the phase-46 landing audit names (`docs/e3/tracker.md` §8's B-Q5 inheritance: *"a third implementation of the admission rule inside `pnpm gates` whose agreement today is fixture coincidence"*). **(b) is literally N presses of the shipped button**: `packages/descvi/src/extractor/structural-edit.ts#export function moveAdjacent(` takes a source string and returns one, so iterating it feeds each output to the next and every iteration re-runs `resolveJsxChildOp` in the shipped precedence. `STRUCTURAL_OPS` is unchanged, the journal subject's shape is unchanged, `reselectTargetFor` and `structureSubjectOid` need no new arm, and G47-1 asserts the byte identity rather than asserting it in prose |
| **DR47-2** | Where the gesture's `pointerdown` listener lives | **(a)** a FOURTH arm in the shield's ROW D / ROW P / ordinary table; **(b)** an extension of the ORDINARY arm inside `use-canvas-selection-shield.ts`; **(c)** a separate hook with its own `document`-capture listener, and NO edit to the arm table | **(c)** | ⚠ **(a) IS THE KICKOFF BRIEF'S PREMISE AND IT DESCRIBES A ROW THAT HAS NO SUBJECT.** An arm-table row is a class of pointerdown TARGET that takes different suppression. A reorder target is an ordinary `[data-oid]` element inside `#dsh-screen` and wants **exactly** the ordinary arm's suppression — no focus, no text-selection — which is what a drag wants anyway. There is no fourth class of target, so a fourth row would be a row whose predicate is *"an ordinary element, again"*. **(b) is honest but buys nothing and costs the riskiest file in the phase.** `#dsh-ring-layer` is a SIBLING of `#dsh-screen` under `#dsh-frame` (`OverlayShell.tsx`'s JSX), so scoping the new listener to `screenEl.contains(target)` excludes every handle, strip, apron and popup **by construction** — the new hook needs no `data-dsh-handle` predicate at all, and therefore needs nothing exported from the shield. That matters concretely: `isResizeHandleEvent` is anchor-cited from TWO sibling plans (`.omc/plans/ralplan-phase-44-gap-padding.md` and `.omc/plans/ralplan-phase-45-multi-select.md`, three citations between them), so adding `export ` to its declaration turns `node scripts/check-citation-anchors.mjs` — `gates.mjs` step 12 — RED at those documents. **(c) additionally survives the capture-phase `stopPropagation`**: `packages/descvi/src/react/overlay/canvas/selection-shield.ts#export function suppressShieldPointer(event: ShieldEvent): void {` calls `stopPropagation()` **and** `preventDefault()` on a capture listener attached to `#dsh-stage`; a `document`-capture listener is ABOVE the stage in the capture path and runs first, so that `stopPropagation` cannot reach it. ⚠ **AND THE `preventDefault()` HALF BLOCKS NOTHING WE NEED — that is D47-2's measurement, not an argument** |
| **DR47-3** | What starts a reorder drag | **(a)** a press landing on the CURRENT single-member selection (or a descendant resolving to it); **(b)** a press on any element — crossing the threshold selects it and begins the drag, Figma-style; **(c)** a dedicated drag handle on the ring | **(a)** | **(b) loses on an async hazard that is in shipped source, not hypothetical.** The shield applies a new selection through `switchSelection`, which is `void resolvePendingEdits().then(apply)` whenever anything is dirty — so under (b) the selection can land **asynchronously, mid-gesture**, after the drag has already computed its sibling snapshot against a different subject. (b) also needs `handleShieldSelect`'s resolution re-run at pointerdown, i.e. a second implementation of the deepest/parent pick. **(c) puts a new OPERABLE node in `#dsh-ring-layer`**, which under C46-1 owes a declared kind from the closed three-value set and would make the reorder family a fourth declared population — real contract cost for a gesture that Figma performs on the object itself. **(a)'s cost is stated rather than hidden: moving an unselected element is two gestures, click then drag.** §9 U1 puts that in front of the owner |
| **DR47-4** | How the flow axis and the drop slots are determined | **(a)** from the Tailwind class model (`parseLayout`'s direction, the LayoutSection's own source); **(b)** MEASURED from the source-order siblings' rendered rects; **(c)** from `getComputedStyle(parent)`'s `display` / `flex-direction` | **(b)** | **(a) cannot see a block parent at all** — the panel's alignment widget is *"enabled only for parents whose base layer resolves to `flex-row` or `flex-col`"* (`.omc/specs/interaction-ontology.md` §6's v3 row) — and it answers about the CLASS rather than the RENDER, which is the artifact-vs-running-app failure `docs/e3/tracker.md`'s phase-21 record names (*"Two facts were verified against the ARTIFACT and never against the running app, and both were wrong for the same reason"*). It would also reach into `parseLayout`'s read-only set, which F46-G item (i) records as belonging to nobody. **(c) is closer and still says nothing about whether the CHILDREN lay out along that axis** — `order:`, an absolutely-positioned sibling and a wrapped row all keep `flex-direction: row` while breaking the mapping from source order to visual order. **(b) refuses grid, wrap, reordered flex and absolute siblings for free**, because in every one of them the source-order rects are not monotone along either axis; and it turns §3.F-1's *"Reorder ambiguous (no flow axis)"* from a class guess into a measured predicate with a mutant (§3.4, G47-4) |
| **DR47-5** | The click that follows the release | **(a)** `setPointerCapture` on the dragged element and rely on the click retargeting to it; **(b)** arm the SHIPPED one-shot trailing-click latch, at a genuine `pointerup` whose target is inside `#dsh-stage`; **(c)** widen the shield's travel-guard condition to swallow EVERY travelled ordinary click | **(b)** | **(a) needs a measurement this phase does not otherwise need.** Chromium's click target after a capture that is released at `pointerup` is exactly the thing `resize-gesture-guard.ts`'s latch docblock says was measured 6/6 the OTHER way for a capture released early — so (a) buys an Evidence Gate where (b) buys none. **(c) is a shipped-behaviour regression outside this phase's scope**: at N ≤ 1 with no modifier, a 4 px shaky click would stop selecting, and `POINTER_DRAG_THRESHOLD_PX` is 4. **(b) reuses `packages/descvi/src/react/overlay/canvas/resize-gesture-guard.ts#export function armTrailingClickSuppression(): void {`, consumed by `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#      const trailing = takeTrailingClickSuppression();` at the top of the click arm** — one shipped mechanism, one shipped consumer, no shield edit. ⚠ **The arming condition is NARROWER than the shipped armer's and that narrowing is load-bearing** (§3.3): arm only on a real `pointerup` INSIDE `#dsh-stage`, because a release outside the stage produces a click whose path never includes the stage, so the latch would survive into an unrelated click — KI-48's exact defect, widened |
| **DR47-6** | Where B-Q4's W×H readout lives | **(a)** a FOURTH member of `use-resize-handles.ts`'s element-anchored readout stack; **(b)** a new pointer-following readout in the reorder hook, with its own `styleReadout`; **(c)** reuse `use-spacing-drag.ts`'s `placeBeside` | **(a)** | **(b) makes a THIRD independent copy of a look whose revision price is already published and large.** F46-B priced it and this plan re-verified it (§2.7): TWO production `READOUT_ACCENT_PX` declarations, FOUR hand-written `"3px"` literals in `resize-handle-layer.test.tsx`'s G46-14 row, and THREE painted assertions in `e2e/spacing-gesture.spec.ts`. A third copy makes that price a third larger and nothing in the compiler would relate it. **(c) is in the wrong file and its placement has no element anchor.** **(a) adds ZERO `styleReadout` copies, ZERO accent constants and ZERO theme reads** — `use-resize-handles.ts` already computes `isDark` once per pass and already stacks three readouts through `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts#function layoutReadouts(`, whose flip-not-clamp placement and G46-14's accent assertion the new node inherits. ⚠ **The file is not "the resize hook" for this purpose and the precedent is shipped: `#dsh-ring-instance-hint` is a shared-oid hint that has nothing to do with resizing** |
| **DR47-7** | KI-47's fix | **(a)** the RECORDED direction — wire `dark` into the effect dependencies; **(b)** consume the `dark` PROP at the paint sites and delete the `closest(".dark")` sniff, at every site; **(c)** fix only the two hooks KI-47 names | **(b)** | ⚠ **(a) IS FALSE AGAINST SOURCE AND THE KNOWN-ISSUE SAYS IT IN GOOD FAITH** — `dark` is ALREADY in all three dependency arrays (§2.8, three anchors). The effect DOES re-run on a theme change; it then re-reads the DOM class, which `OverlayShell`'s **passive** effect has not yet written, because a passive effect runs after every layout effect in the same commit. So the recorded remedy is already implemented and the defect is untouched by it. **Correcting `docs/known-issues.md` is therefore a deliverable of this phase, not a courtesy.** **(c) is P46-4's named failure mode** — *a defect names the site you probed; a fix names the class, enumerated from source*. The class is FIVE executable sites in FOUR files (§2.8), two of which (`use-spacing-affordances.ts`, `use-spacing-drag.ts`) postdate KI-47 and are invisible to its own two-hook wording |
| **DR47-8** | `undo-focus-ownership` | **(a)** the owner's own sketch — let default focus fall to `#dsh-screen` so the ownership guard is always satisfied; **(b)** widen ownership to *"the overlay is alive ⇒ owned"*; **(c)** treat *"nothing is focused"* — `document.body`, or no `activeElement` — as owned, and change nothing else; **(d)** call the SHIPPED `focusStageIfOrphaned` at the two boundaries it does not cover today | **(c)** | **(a) is the option the backlog row itself flags as needing a decision** — *"기본 포커스 이동이 캔버스 선택/포커스 스틸(KI-31 계열)과 충돌하지 않는지"* — and it MOVES focus unconditionally. **(b) claims a global keyboard shortcut while focus sits on a node the overlay does not own**, which is precisely what the shipped ownership guard exists to prevent. ⚠ **(d) IS THE STRONGEST LOSER AND ITS PRECEDENT IS SHIPPED, so it is stated rather than skipped** (§2.10a): `packages/descvi/src/react/overlay/engine/use-preview-session.ts#export function focusStageIfOrphaned(stage: HTMLElement | null): void {` already tests `active === null || active === document.body || active.isConnected === false` and focuses the stage, and its own docblock says it exists *because of* the D13 ownership gate — so the repo has already answered this exact dead window, on one path. It loses on **P46-4**: it has ONE production call site (the first statement of `handleStructureSaved`), so extending it means enumerating the boundaries it misses — a panel value commit, and a selection-CLEARING canvas click, which the shield structurally skips (`if (node !== null) focusStageIfOwned(ownership);`) — and any future path that orphans focus stays open. It also inherits an argued asymmetry rather than a neutral helper: that function's docblock records that a text-entry guard mirroring its sibling's **was built and rejected**. **(c) closes the CLASS in one predicate**, fights no other contract, moves no focus, and has a one-mutation RED (§5, G47-8). ⚠ **(c) and (d) are not exclusive** — a later lane that wants the canvas KEYBOARD alive in those same windows (Escape-deselect, not just Cmd+Z) adds (d) on top without reverting (c), and §9 RR-4 records that as the known limit of (c) |

**Two things are NOT decided here and are handed to gates rather than to an implementer.** KI-54's cause (EG-1) and the parse cost that fixes `MAX_MOVE_STEPS` (EG-2). Both branches of both are pre-decided below.

---

## 1. What this phase ships, inherits, does not touch, and is EXCLUDED from — with the owner rulings and their provenance

**The owner rulings this phase executes.** Each is recorded with where it lives, because §8's own lesson is that silence is what lets items go missing.

| Ruling | Provenance | What it binds here |
|---|---|---|
| Drag-to-reorder is IN as phase-47, **riding v2's `move-up`/`move-down` with NO NEW WRITE CLASS**, with the blue insertion indicator | `docs/e3/tracker.md` §"v3 CLOSE (2026-08-24, owner rulings recorded the same day)" | DR47-1's whole shape; §3.1 |
| It **carries B-Q4's cheap mitigation — a W×H readout during drag** — "since this gesture is where dragging blind bites" | same line | DR47-6; §3.7. ⚠ §9 U4 records what the mitigation does NOT cover |
| `undo-focus-ownership` rides 47, "which touches focus anyway" | same line, the QoL distribution sentence; re-stated at `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` §8's *"Drag-to-reorder, `undo-focus-ownership` → phase-47"* | DR47-8; §3.8 |
| **KI-47 and KI-54 ride phase-47** | ⚠ **FRESH OWNER INPUT of 2026-08-27**, given in this planning session. It is **NOT** in the v3 CLOSE record and **NOT** in either known-issue's own routing line — `docs/known-issues.md` KI-54 says in terms *"아직 어느 페이즈에도 라우팅되지 않았다 — 목적지는 owner 판정이다"*, and KI-47 was found UNROUTED by phase-46's landing audit F46-G item (ii), which is why it was invisible to every three-KI enumeration. **Recording both routings is a deliverable of this phase** (§4's sweep) | DR47-7 and EG-1; §3.9 |
| The two look items — `selection-ring-treatment`, `spacing-affordance-mark` — are **OUT** and stay unrouted backlog rows | owner, 2026-08-27, same input | §8 |
| B-Q5 → phase-48. Marquee → deferred-v4. KI-10 → inherited | v3 CLOSE, plus the 2026-08-25 B-Q5 ruling carried at `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` §8 | §8 |
| **Multi-select drag is REFUSED in 47** | ⚠ **LEAD DEFAULT, not an owner ruling — stated as such.** Its brief-supplied rationale is FALSE and §3.6 replaces it | §3.6 |

**Ships.** (i) The engine's `steps` repetition on the shipped move verbs, end to end (§3.1). (ii) The drop model — the artifact-driven sibling chain, the measured flow axis, the slot→(op, steps) map, the refusal taxonomy and its bilingual copy (§3.2, §3.4, §3.5). (iii) The gesture and its paint — the reorder pointer hook, `#dsh-reorder-layer`, the blue indicator, the trailing-click arming (§3.3). (iv) B-Q4's W×H readout as a fourth member of the shipped readout stack (§3.7). (v) The KI-47 theme-source class fix across five sites in four files, **and the correction of KI-47's own recorded fix direction** (§3.9). (vi) `undo-focus-ownership` (§3.8). (vii) EG-1 — KI-54's measurement and its recorded outcome, which is a disposition and not necessarily a fix. (viii) The `.omc/specs/interaction-ontology.md` §3.F-1 amendment this phase's behaviour forces, and the document sweep every one of the above forces (§4).

**Inherits without touching.** KI-10 (owner-ruled at v3 close) — and §3.2's instance rule is written so that a shared-oid subject REFUSES rather than guessing, which is a bound on KI-10 rather than a fix for it. KI-53's flake pair. KI-19's reselect latency, which this phase makes strictly better by turning N handoffs into one. KI-48, whose latch this phase arms from a second site — bounded in §3.3 and priced in §6 S4. C46-0/C46-1's declared-kind contract, which the new painted node sits OUTSIDE by role (§2.5). F46-D's `readScene` fallback: **phase-47 does not touch that function** (§2.11), so the obligation does not transfer.

**Does not touch.** The shield's arm table (DR47-2). `packages/descvi/src/vite/**` — deliberately, because an edit there restarts every dev server watching the repo, the owner's included (H45's second lesson, carried by phase-46 §1). The schema. The resize and spacing WRITE paths. `src/app/**` except as the e2e corpus, and every e2e row round-trips so `.descvi/screens.json` stays byte-identical.

**Excluded, stated not implied — §8 carries a disposition line for each.**

---

## 2. Repo facts, re-probed in the current tree

### 2.1 The move verb is single-target, one-step, and its composer is a pure string→string function (READ)

`packages/descvi/src/extractor/structural-edit.ts#export const STRUCTURAL_OPS: readonly StructuralOp[] = ['delete', 'move-up', 'move-down', 'duplicate', 'insert-after'];`. The composer is `packages/descvi/src/extractor/structural-edit.ts#export function moveAdjacent(` — it takes `source: string`, builds its own `moduleContext`, resolves the op, and returns a new string. The server's arm is one line: `packages/descvi/src/sidecar/server.ts#      const nextPage = moveAdjacent(pageSource, fullScreenId, oid, params.op === 'move-up' ? 'up' : 'down', params.expect);`. **That signature is what makes DR47-1(b) a loop rather than a redesign.**

The staleness baseline is `{parentOid, prevOid, nextOid}` and the server re-derives it under the write lock. **A repetition passes `expect` on iteration 1 only** — iterations 2..N operate on source this same request produced, so re-asserting a client baseline against them would 409 on a state the client never claimed.

### 2.2 ⚠ THE ORDINARY ARM DOES NOT BLOCK A DRAG, AND THE PROOF IS IN THE SHIELD ITSELF (READ + INHERITED-browser)

The kickoff brief's central premise is that `preventDefault()` on `pointerdown` structurally blocks every drag gesture today. **Three readings of shipped source falsify it.**

1. The ordinary arm calls `suppressShieldPointer(e)` and then, on the very next line, starts a document-scoped pointer gesture: `packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#      if (e instanceof MouseEvent) beginTravelRecording(e);`. Its listeners are `pointermove`/`pointerup`/`pointercancel` at **document capture** (`packages/descvi/src/react/overlay/canvas/use-canvas-selection-shield.ts#      doc.addEventListener("pointermove", onTravel, { capture: true });`). A `preventDefault()` that blocked the move stream would make that recording dead code.
2. The recording is not dead code: it is exercised in a real Chromium by `e2e/multi-search`-class rows — specifically `e2e/multi-select-shield.spec.ts#(i) a SHIFT-drag past the threshold releasing INSIDE the same element leaves the selection unchanged`, whose helper presses, moves in 12-step increments twice, and releases, and whose assertion only holds if the travel was recorded.
3. What `preventDefault()` on `pointerdown` actually suppresses is stated in the file's own docblock: the **compatibility mouse events**. The blocker for a listener BELOW the stage is the `stopPropagation()` in the same call, which is why DR47-2 puts the new listener ABOVE it, at document capture.

⚠ **The correction is propagated:** `.omc/specs/interaction-ontology.md` §3.F's v1-reality note says the capture-phase `preventDefault` *"cancels the press default before bubble, so the browser never enters a drag gesture"*. That sentence is false for pointer events as shipped and §4's sweep amends it in the same commit as the gesture.

### 2.3 The travel guard is overloaded, and it does NOT cover the plain single-selection case (READ)

The shield's click arm swallows when `(shiftKey || selectionRef.current.length > 1) && maxTravel >= POINTER_DRAG_THRESHOLD_PX`. Phase-45's own reasoning is quoted in source: the conjunct is *"INERT for a non-Shift click at N ≤ 1, which is every row this shield shipped with."* A reorder drag is exactly N = 1 with no modifier. **So the guard is not a contender and not an obstacle — it is simply silent here**, and DR47-5 answers the click with the shipped latch instead of by touching that condition.

### 2.4 The threshold is one symbol with a documented consumer count (READ)

`packages/descvi/src/react/overlay/canvas/pointer-thresholds.ts#export const POINTER_DRAG_THRESHOLD_PX = 4;`, whose module header says *"ONE SYMBOL, THREE CONSUMERS, AND THAT IS WHY IT HAS ITS OWN MODULE"* and *"A constant that lives inside its first consumer is a constant the second consumer copies."* Phase-47 is the fourth consumer and imports it. ⚠ **The `Math.hypot` computation is duplicated and that is deliberate**: the resize machine and the shield each compute their own already, so this is the shipped pattern — the CONSTANT is the thing that must not be copied, and the header says so.

### 2.5 A non-hittable painted node is OUTSIDE C46-0 / C46-1 (READ — this is the brief's open question, answered)

The closed kind set is three values (`glyph` | `glyph-conditional` | `cursor`), ring-layer-only, and the completeness half's subject is stated explicitly at `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts#any OPERABLE node under `#dsh-ring-layer` outside the rows above — **must not exist**` — continuing *"⚠ The subject is OPERABLE nodes: the four ring readouts … are rendered, unmarked children of that layer and sit outside this row by construction, being non-hittable."* The mechanism that carries the exclusion is the inline write, not the absence of a mark: *"A readout stays outside G42-7's Universe B by ROLE, and the mechanism is the inline `pointer-events: none`."*

**Consequence, and it is a two-sided obligation.** The indicator and the readout inherit NO kind obligation **provided** they are non-hittable and carry neither `data-dsh-handle` nor `data-v3-glyph-control`. The gate that catches a violation is already shipped: `e2e/resize-handles.spec.ts#    expect(scene.operable.filter((n) => n.family === "other")).toEqual([]);`. G47-6 names that as this phase's row with its own mutant.

⚠ **AND THE INLINE-vs-CLASS DISTINCTION IS NOT PEDANTRY:** the jsdom rows key on the MARKER and the e2e rows key on COMPUTED `pointer-events`; a class-only `pointer-events-none` reads back `auto` in jsdom, which is why `#dsh-selection-badge`'s exclusion is e2e-only. The new nodes write `pointerEvents = "none"` inline, like the shipped readouts.

### 2.6 §3.F-1's non-flex row is wrong about block, and right about grid (READ)

`.omc/specs/interaction-ontology.md` §3.F-1 row 3: *"element in non-flex (block/grid) parent | within/cross | Reorder ambiguous (no flow axis) — may require 'add auto-layout' first | deferred-v2 (degraded) | undefined blue-line; clarify at gate"*. **Block and grid are folded into one row and they do not behave the same.** DR47-4's measured predicate separates them without the spec having to name a display value at all, and §3.4 amends the row.

The §3.F-1 rows carry class `**deferred-v2**` and **no `<!-- v3-cell:… -->` tag**. `scripts/check-v3-registers.mjs` hardcodes exactly eleven slugs and censuses only cells still marked `**deferred-v3`. **So amending a `deferred-v2` row to `SHIPPED` is invisible to that gate, and minting a twelfth tag would turn it RED** — which is the RED-when G47-10 names.

### 2.7 The readout family, and the published price of its accent (READ, F46-B re-verified with one refinement)

`styleReadout` and `READOUT_ACCENT_PX` are each declared TWICE, once per file, neither exported: `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts#const READOUT_ACCENT_PX = 3;` and `packages/descvi/src/react/overlay/canvas/use-spacing-drag.ts#const READOUT_ACCENT_PX = 3;`. **No W×H readout exists anywhere** — a resize drag shows nothing of the sort, which is what S42-5 measured and what B-Q4's cheap-mitigation clause is about.

⚠ **F46-B's price is correct and its literal count is worth carrying: G46-14's row holds FOUR hand-written `"3px"` literals, not one**, and the three painted assertions are all in `e2e/spacing-gesture.spec.ts`. ⚠ **`e2e/resize-handles.spec.ts` carries ZERO accent assertions — the resize accent's painted coverage is jsdom-only.** That asymmetry is not in F46-B and it bounds what a fourth stack member can claim: G47-7 asserts the new readout in jsdom, and its painted leg is a new e2e row rather than an inherited one.

### 2.8 ⚠ KI-47'S RECORDED FIX DIRECTION IS FALSE AGAINST SOURCE, AND THE CLASS IS FIVE SITES IN FOUR FILES (READ)

There is no `classList.contains("dark")`, no `matchMedia` and no paint-time `documentElement` read anywhere in `packages/descvi/src`. The sniff is an ancestor walk, and its sites are:

1. `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts#const isDark = layer.closest(".dark") !== null;`
2. `packages/descvi/src/react/overlay/canvas/use-spacing-affordances.ts#const isDark = layer.closest(".dark") !== null;`
3–4. `use-selection-rings.ts` carries `const isDark = stage.closest(".dark") !== null;` **twice** — the hover pass and the selection pass — so it cannot be anchor-cited alone; disambiguate by the guard line above each (`packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#if (!stage || !layer || !hoverRing) return;` and `packages/descvi/src/react/overlay/canvas/use-selection-rings.ts#if (!ring || !stage || !layer) return;`)
5. `packages/descvi/src/react/overlay/canvas/use-spacing-drag.ts#const isDark = (): boolean => layer.closest(".dark") !== null;` — the only THUNK, re-evaluated per readout paint

And `dark` is already in every relevant dependency array, e.g. `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts#}, [placeFurniture, reanchorRef, stateMap, deviceMode, dim, collapsed, dark, tick]);` (the spacing-affordances and selection-rings arrays are the same shape). **The effect re-runs; the sniff then reads a class the passive effect in `OverlayShell` has not yet written.** ⚠ `use-spacing-drag.ts` receives no `dark` prop at all — the thread is part of the fix.

Every colour choice in this system is a bare ternary on that boolean at the point of write; there is no token layer. Example, unique in its file: `packages/descvi/src/react/overlay/canvas/use-resize-handles.ts#node.style.color = isDark ? "#FCA5A5" : "#B91C1C";`.

**Answering the brief's question directly: a new painted element would NOT become a third instance — it would be the sixth site, or the fourth file.** But if it is painted from inside a pass that already computed `isDark`, it adds **zero**. DR47-6 and §3.3 both take that route, and DR47-7 lands the class fix FIRST so the new nodes are born on the fixed pattern.

### 2.9 The blue already exists in the ring system and needs no minting (READ)

`packages/descvi/src/react/overlay/canvas/selection-ring-model.ts#export function ringGroupShades(group: RingGroup, isDark: boolean): GroupShades {` returns, for the `descriptive` group, `deep` = `#60A5FA` (dark) / `#2563EB` (light). §3.3 reads that function with a **fixed** group rather than the dragged element's group, and mints no colour. ⚠ DR46-5(b) refused *changing* those shades because they are shared with the ring and the hover label; **reading them is the opposite operation** and is what makes a future palette change carry the indicator for free.

### 2.10 The undo ownership guard, exactly as shipped (READ)

`packages/descvi/src/react/overlay/OverlayShell.tsx`'s Cmd+Z keydown effect yields to fields first, then computes `const owned = stage.contains(active) || active.closest("#dsh-panel, #dsh-toolbar, #dsh-collapse, [data-descvi-toast-host]") !== null;`. `document.body` is an `Element`, so it passes the `instanceof` guard, matches no field selector, is not inside the stage and matches no host — `owned` is false and the handler returns. **That is the backlog row's dead window, reproduced from source.**

### 2.11 F46-D does not transfer to this phase (READ)

`e2e/resize-handles.spec.ts`'s `readScene` collects roots from `getElementById("dsh-handle-layer") ?? layerEl`, and `docs/e3/tracker.md`'s F46-D rules that *"the next lane that touches `readScene` removes the fallback."* **Phase-47 touches no function in that file.** Its own e2e lives in a new spec, and G47-6's mutant is planted in the new spec rather than in the shipped `family === "other"` row. ⚠ **If any story finds itself editing `readScene`, it takes F46-D with it in the same commit** — stated as a standing condition rather than assumed away.

### 2.12 The e2e round-trip precedent is shipped and is the right acceptance shape (READ)

`e2e/structural-editing.spec.ts#adjacent-sibling move round-trips (↓ then ↑) byte-identically` is the existing move row. Phase-47's flagship acceptance is its N-slot analogue: a drag of N slots down followed by a drag of N slots up leaves `page.tsx` and `.descvi/screens.json` byte-identical. **An off-by-one anywhere in the slot→steps map breaks it**, which is why it is the phase's cheapest strong gate.

---

## 3. Rulings this plan lands

### 3.1 C47-1 — `steps` on the shipped verb: the wire, the parse, the loop, the journal (RULED — DR47-1)

1. **Wire.** `POST /edit` gains an optional `steps` on the existing `target: 'structure'` body. `target`, `op`, `expect` and the journal subject shape are all unchanged; `STRUCTURAL_OPS` and `STRUCTURAL_WIRE_VERBS` are unchanged.
2. **Parse, by op, total.** A `parseStepsForOp` mirroring the shipped `packages/descvi/src/sidecar/server.ts#function parseExpectForOp(op: StructuralWireVerb, expect: unknown): ParsedExpect {` — a switch with an arm per wire verb, no `default`, and a return type excluding `undefined`, so a future verb without an arm is a compile error. Rules: `move-up`/`move-down` accept an omitted value (⇒ 1) or an integer in `[1, MAX_MOVE_STEPS]`; **every other verb 400s on any `steps` at all**, worded as *"you must not send one"*, on `parseExpectForOp`'s own precedent that the two instructions are opposite and a shared message tells half the callers the wrong thing.
3. **Execution.** Inside the existing `prepare` callback, the move arm applies `moveAdjacent` `steps` times, each on the previous output, **passing `expect` on the first iteration only**. Any refusal on any iteration throws before `commitWrite` writes anything, so the request is atomic by the shipped lifecycle rather than by new machinery.
4. **Journal.** Unchanged. One `commitWrite`, one entry, one full-file preimage, one Cmd+Z. `structureSubjectOid` and `reselectTargetFor` need no arm.
5. ⚠ **`steps` IS NOT A COORDINATE, and this clause exists because a reviewer will ask.** `docs/reference/structural-limits.md` rules that the engine does not *"Resolve coordinates on the client."* `move-down` is already a relative verb; `steps: 3` is *"press it three times"*, and the server independently re-proves each swap partner with the shipped resolver. No index, no anchor oid, no derived field crosses the wire.
6. **`MAX_MOVE_STEPS`** is 32 pending EG-2, adopting phase-45's `MAX_MEMBERS = 32` as a precedent number **with its own re-discussion trigger recorded on the backlog**, exactly as phase-46 §3.6(e) did for that one.

**Acceptance.** (1) A `steps: N` request and N sequential single-step requests over the same subject produce byte-identical `page.tsx`. (2) A `steps: N` request produces exactly ONE journal entry and one Cmd+Z restores the pre-drag file. (3) `steps` on `delete`/`duplicate`/`insert-after`/`insert-child` is a 400 naming the verb. (4) `steps: 0`, `steps: -1`, `steps: 1.5`, `steps: "3"` and `steps: MAX_MOVE_STEPS + 1` are each a 400. (5) A request whose step k is inadmissible writes nothing and returns the typed 422 for k's own refusal.

### 3.2 C47-2 — the drop model reads the artifact's chain, and refuses rather than guessing (RULED — DR47-4, P47-2)

**The sibling chain.** From the dragged element's oid, walk `editMap.oids[screenId][oid].structure.nextOid` forward and `.prevOid` backward until `null`. That list IS the source order, published by the engine. **No DOM ordering is read at any point.**

**The DOM join, and its refusal.** Each chain member is resolved to a rendered element by querying `[data-oid="…"]` **scoped to the dragged element's own `parentElement`**. A member that resolves to zero elements, or to more than one, makes the gap it borders **unofferable**, and if the DRAGGED element itself resolves ambiguously the whole gesture refuses (`multi-instance`). ⚠ **This is a bound on KI-10, not a fix for it**: KI-10 is owner-ruled inherited, and the rule here is that a shared-oid subject gets a refusal instead of an indicator drawn on an instance nobody pointed at.

**The flow axis, MEASURED.** With the joined rects in source order, for every consecutive pair: the parent is a COLUMN flow if `next.top >= cur.bottom - FLOW_AXIS_TOLERANCE_PX` holds for all pairs; a ROW flow if `next.left >= cur.right - FLOW_AXIS_TOLERANCE_PX` holds for all pairs; otherwise **`no-flow-axis`, and the gesture refuses.** `FLOW_AXIS_TOLERANCE_PX = 1`, for sub-pixel layout rounding and nothing else. Grid, wrapped rows, `order:`-reordered flex and absolutely-positioned siblings all fall out as `no-flow-axis` without the predicate naming any of them.

**The snapshot is taken ONCE**, at the moment travel crosses the threshold, and every subsequent move only hit-tests the pointer against it. Recomputing per move would call `getBoundingClientRect` once per sibling per move — the per-oid-descent performance class the phase-45 whole-set audit found and instrumented. **If the dragged element becomes `!isConnected` mid-gesture the drag aborts with no commit** (the KI-50 detached-subtree class, guarded rather than assumed away).

**The slot arithmetic — stated as a table because an off-by-one here is this phase's likeliest defect.** With siblings `s₀ … s_{n-1}` in source order and the target at index `i`, a drop into slot `j` (meaning *"land before the element currently at index j"*, `j ∈ [0, n]`):

| Condition | Verb | `steps` |
|---|---|---|
| `j < i` | `move-up` | `i - j` |
| `j == i` or `j == i + 1` | — | no-op: the gesture commits nothing |
| `j > i + 1` | `move-down` | `j - i - 1` |

### 3.3 C47-3 — the gesture: its listener, its arming, its paint, and its release (RULED — DR47-2/3/5)

**The hook** owns a `document`-capture `pointerdown`, and admits a press only when all hold: edit mode is on; the selection holds **exactly one** member; the press target is an `Element` inside `#dsh-screen` that resolves to that member's element or a descendant of it. `#dsh-ring-layer` is a sibling of `#dsh-screen`, so every handle, strip, apron and popup is excluded by containment — **no `data-dsh-handle` predicate, and therefore nothing exported from `use-canvas-selection-shield.ts`** (whose `isResizeHandleEvent` is anchor-cited from two sibling plans and must not be renamed or re-declared; DR47-2).

**Arming.** Document-capture `pointermove`/`pointerup`/`pointercancel`, `pointerId`-filtered, removed on all three terminals and on teardown — the shipped shape of `beginTravelRecording`, for its stated reasons. The gesture ARMS the first time `Math.hypot` from the press point reaches `POINTER_DRAG_THRESHOLD_PX` (imported, §2.4). Before arming, nothing paints and nothing is suppressed.

**No `setPointerCapture`.** Document listeners already deliver out-of-frame moves; capture would buy only a click-retarget question DR47-5 does not need to ask.

**No ghost, and the element does not move.** The page element's own styles are never touched — the shipped BUG-5 invariant (`OverlayShell.tsx`: *"the element's OWN styles are never touched"*). Feedback is the selection ring (unchanged), the indicator, and the readout.

**The paint.** A new `#dsh-reorder-layer` under `#dsh-ring-layer`, declared in JSX and populated imperatively, `position: absolute; inset: 0; pointerEvents: none`, `aria-hidden`, on the same terms as `#dsh-selection-ring-pool`. Inside it, one `#dsh-reorder-indicator`:
- non-hittable (`pointerEvents = "none"` **inline**, §2.5), carrying neither `data-dsh-handle` nor `data-v3-glyph-control`;
- `REORDER_INDICATOR_THICKNESS_PX = 2` along the flow axis, spanning the cross-axis union of the gap's neighbours (or the single neighbour at either end);
- coloured `ringGroupShades("descriptive", isDark).deep` — the ring system's own blue, read from the one shared source, with the group **FIXED** so the slot never re-colours with the dragged element's kind (§2.9). **No colour is minted.**
- `isDark` comes from the `dark` **prop**, never a sniff — the pattern DR47-7 establishes one story earlier.
- The stage's inline `cursor` is set for the duration and restored on every terminal **and on teardown**.

**The release.** On `pointerup`: compute the slot from the snapshot, and if it is not the no-op slot, POST through `applyStructureEdit` and hand the outcome to the session's `handleStructureSaved` — the same consumer `StructureSection` uses (`packages/descvi/src/react/overlay/engine/use-preview-session.ts#  handleStructureSaved: (outcome: ApplyStructureOutcome) => void;`), so the edit-map refresh, the flag resync and the selection handoff are the shipped ones and not a second path. Then, **iff the gesture had armed AND the terminating event is a `pointerup` whose target is inside `#dsh-stage`**, call `armTrailingClickSuppression()`.

⚠ **BOTH HALVES OF THAT CONDITION ARE LOAD-BEARING AND THE SECOND IS THE ONE A REVIEWER WILL CUT.** A release outside the stage produces a click whose propagation path never includes `#dsh-stage`, so the shield's consumer never runs and the latch survives into an unrelated click — which is KI-48 exactly, widened by a new armer. Not arming there is also correct on its own terms: that click cannot reach `handleShieldSelect` either, so there is nothing to suppress. **`pointercancel` never arms** (no click follows a cancel).

**Escape** cancels the drag's visuals and marks the gesture cancelled; the hook keeps listening, and the eventual `pointerup` takes the same single arming rule. One arming site, one condition.

### 3.4 C47-4 — the ontology amendment (RULED — D47-3, DR47-4)

`.omc/specs/interaction-ontology.md` §3.F-1 is amended in the commit that makes it true:
- Row 1 (flex/auto-layout parent, within-parent) → **SHIPPED at phase-47**, cited by anchor into the new commit module.
- Row 3 is **split**, because block and grid are not one case: a parent whose source-order children are measurably monotone along one axis (which ordinary block flow is) reorders exactly as a flex column does; grid, wrapped rows and `order:`-reordered flex refuse as `no-flow-axis`. The *"may require 'add auto-layout' first"* wording survives only on the refusing half, and the *"undefined blue-line; clarify at gate"* note is **closed by §3.3's indicator ruling**.
- Row 2 (cross-parent) stays **deferred-v2** — phase-47 reorders WITHIN one parent only.
- Row 4 (component instance) is answered by §3.2's `multi-instance` refusal, which is a narrower statement than the row's *"Reorder instance JSX node"* and says so.
- §3.F's v1-reality note is corrected (§2.2).
- ⚠ **NO `<!-- v3-cell:… -->` TAG IS MINTED.** These are `deferred-v2`-class cells and `check-v3-registers.mjs` hardcodes eleven slugs; a twelfth turns it RED (§2.6, G47-10).

### 3.5 C47-5 — the refusal policy and its bilingual copy (RULED — P47-4)

Refusals are rendered in the ring layer through the shipped `packages/descvi/src/react/overlay/shared/refusal-messages.ts#export function bilingualLine(message: BilingualMessage): string {`, into the readout family (§3.7's node, reusing the refusal marker's own hue by role). Wording is **new and gesture-shaped**, NOT `StructureSection.tsx`'s `REASON_TEXT`, which is worded for a panel button — rendering those here is KI-17's failure on a new surface (P47-4).

A closed `ReorderRefusalReason` union, each with one `BilingualMessage`:

| Reason | When | ko | en |
|---|---|---|---|
| `no-flow-axis` | the measured predicate fails (grid, wrap, `order:`, absolute siblings) | `이 부모는 흐름 축이 하나가 아니라 끌어서 순서를 바꿀 수 없습니다 — 먼저 오토 레이아웃(flex)을 적용하세요.` | `This parent has no single flow axis, so drag-to-reorder is off — apply auto-layout (flex) first.` |
| `only-child` | the sibling chain has no other member | `형제 요소가 없어 순서를 바꿀 자리가 없습니다.` | `There is no sibling to reorder against.` |
| `multi-instance` | the dragged element, or a sibling bordering the slot, renders more than once under this parent | `이 요소는 화면에 여러 번 그려져서 어느 자리에 놓을지 정할 수 없습니다.` | `This element renders more than once here, so the drop position cannot be determined.` |
| `multi-select` | more than one member is selected | `여러 요소를 한 번에 끌어서 옮기는 것은 아직 지원하지 않습니다 — 하나만 선택하세요.` | `Dragging more than one element at a time is not supported yet — select a single element.` |
| `engine-refused` | the edit-map's own `structure.reasons['move-up' \| 'move-down']` refuses in the drag's direction | wording branches on the engine reason, and **each branch names the SIBLING relationship** the move actually failed on — e.g. `unequal-indent` → `두 형제가 서로 다른 들여쓰기에 있어 자리를 맞바꿀 수 없습니다.` / `The two siblings sit at different indents, so they cannot be swapped.`; `non-canonical-separator` → `두 형제가 같은 줄에 있어 자리를 맞바꿀 수 없습니다.` / `The two siblings are on one line, so they cannot be swapped.` | |

⚠ **`engine-refused` MUST NOT collapse to one generic sentence.** That collapse is precisely KI-17: one code, two structurally different repairs, one wrong sentence for whichever shape is not the majority.

**Where a refusal renders.** A refusal that is knowable BEFORE the gesture (`only-child`, `multi-instance` on the target, `engine-refused` in both directions) suppresses arming and paints nothing — a drag that cannot start must not paint a line and then take it away. A refusal that is only knowable at the snapshot (`no-flow-axis`) arms, paints the readout, and paints **no indicator**. `multi-select` is reported on the attempt.

### 3.6 C47-6 — multi-select drag is REFUSED in 47, on replaced grounds (RULED — LEAD, with the brief's rationale withdrawn)

⚠ **THE RATIONALE SUPPLIED WITH THIS DEFAULT IS FALSE AND IS WITHDRAWN HERE RATHER THAN REPEATED.** *"A block move is not something `move-up`/`move-down` can express"* — it is. Moving a contiguous block `[a,b,c]` one slot past `d` is `move-down` on `c`, then on `b`, then on `a`: `a,b,c,d → a,b,d,c → a,d,b,c → d,a,b,c`. K members across N slots is K×N adjacent swaps, all inside the shipped verb.

**The ruling stands on three other grounds, each from source.**
1. **A non-contiguous selection has no block move at all.** With `a` and `c` selected and `b` not, "drop here" names no sequence of swaps that preserves the user's intent, and inventing one is a design decision no owner has made.
2. **Multi-select's scope is register-bound to panel edits.** `.omc/specs/interaction-ontology.md` §6's v3 row reads *"Shift-click multi-select for **batch panel edit only** `[v3-cell:shift-click-multi-select]`"* — a tagged cell that `scripts/check-v3-registers.mjs` joins across three carriers. Extending it to a structural gesture moves that cell's meaning, which is scope the owner has not ruled.
3. **The shipped shield already makes multi-member canvas gestures inert** — phase-45's guard swallows a travelled click at N > 1 by design (§2.3), so refusing here agrees with the surface rather than contradicting it.

The gesture therefore refuses at N > 1 with `multi-select` copy, and the shipped guard means the selection survives the attempt unchanged.

### 3.7 C47-7 — B-Q4's W×H readout, as a fourth member of the shipped stack (RULED — DR47-6)

A new id in `use-resize-handles.ts`'s readout family, shown **only while a reorder gesture is armed**, carrying the dragged element's measured `W × H` in CSS px (rounded), placed by the shipped `layoutReadouts` and styled by the shipped `styleReadout`. Its hue is the neutral member's, not the refusal's. It is the same node that renders §3.5's refusal text when one applies, because §3.5 and B-Q4 are one surface and two surfaces for one gesture is the drift `refusal-messages.ts` exists to prevent.

⚠ **WHAT THIS MITIGATION DOES NOT COVER, SAID HERE RATHER THAN DISCOVERED LIVE.** `docs/post-loop-backlog.md`'s B-Q4 defines *dragging blind* as *"조작 중인 가장자리가 프레임 가시 영역을 벗어나 포인터를 놓지 않고는 되돌릴 수 없는 상태"* — an edge under manipulation leaving the visible frame. **A reorder changes no edge and no size**, so the reorder gesture's own blind case is an **off-screen drop slot**, and a W×H readout does not reach it. The answer to that is B-Q4's auto-scroll, which the owner ruled the confirmed follow-up direction and which is **OUT of 47** (§8). §9 U4 puts the readout's actual value in front of the live pass instead of asserting it.

### 3.8 C47-8 — `undo-focus-ownership` (RULED — DR47-8)

The ownership disjunction gains one term: **an active element that is the document body, or the absence of one, counts as owned.** Nothing moves focus; the field-yield guard is untouched and still runs first; no other host joins the set.

**Acceptance.** After a panel value commit that remounts the field to `document.body`, and with nothing selected, Cmd+Z reaches `bridge.undo` exactly once. Focus inside a field still yields. Focus on a node that is neither the body nor inside any listed host still does NOT own the shortcut. ⚠ **One residual, recorded not fixed:** descvi's own chrome dropdowns portal to `document.body` (`OverlayShell.tsx`'s portal-container comment), so focus INSIDE an open dropdown is on a body-portalled node — not the body itself — and stays unowned. That is a narrower window than the one being closed and it is not this rider's.

### 3.9 C47-9 — KI-47's fix names the class, and the known-issue is corrected (RULED — DR47-7, P46-4)

The five sites of §2.8 stop sniffing and consume the `dark` prop; `use-spacing-drag.ts` is threaded one prop to make that possible. **The KI-47 entry in `docs/known-issues.md` is corrected in the same commit**: its recorded remedy is already implemented and does not fix it, and its two-hook scope undercounts by two files. ⚠ **This correction is the deliverable, not a courtesy** — F46-A's whole lesson is that a ruling lands and the sites it falsifies are a second job nobody was assigned.

**Acceptance.** No `closest(".dark")` survives in `packages/descvi/src` outside tests, proved by a command whose instrument is shown able to find one (plant a sniff, see it named, remove it). A theme toggle with a selection held repaints the ring, the corner chip, the spacing affordances, the spacing readout and the reorder indicator in the new theme within the same commit as the toggle.

---

## 4. The story ladder, and the document sweep

**S47-0 and S47-1 run first and in either order** — one is server-only, one is overlay-paint-only, and neither can contaminate the other. **S47-1 must land before S47-3** so the new painted node is born on the fixed theme pattern rather than becoming the sixth sniff.

| Story | Depends on | What it lands | Parallelism |
|---|---|---|---|
| **S47-0** — the engine's `steps` | — | §3.1 (a)–(f). Wire parse, the loop, `MAX_MOVE_STEPS`, G47-1/2/3 | Sequential; owns `sidecar/server.ts`, `extractor/structural-edit.ts` (if the loop lands there), `engine/sidecar-bridge.ts`, `e2e/structural-editing.spec.ts` |
| **S47-1** — KI-47, the theme-source class fix | — | §3.9, plus the KI-47 record correction. **No pixel intent changes**; the only intended behaviour delta is that a theme toggle repaints | **∥ with S47-0**; owns `use-resize-handles.ts`, `use-spacing-affordances.ts`, `use-selection-rings.ts`, `use-spacing-drag.ts`, `docs/known-issues.md` |
| **S47-2** — the drop model | S47-0 (soft: the slot table is what S47-0's `steps` consumes) | §3.2 and §3.5 as PURE functions plus their tables, with no listener and no paint. The chain walk, the DOM join, the axis measurement, the slot map, the refusal union and its copy | Sequential; owns the new `canvas/reorder-model.ts` and `shared/refusal-messages.ts`'s new table |
| **S47-3** — the gesture and the paint | S47-1 (hard), S47-2 (hard) | §3.3 in full: the hook, `#dsh-reorder-layer`, the indicator, the arming rule, the commit through `handleStructureSaved` | Sequential; owns the new `canvas/use-reorder-drag.ts`, `OverlayShell.tsx`'s layer JSX, and a new `e2e/reorder-drag.spec.ts` |
| **S47-4** — B-Q4's readout | S47-3 (hard) | §3.7 | Sequential; owns `use-resize-handles.ts` again |
| **S47-5** — `undo-focus-ownership` | — | §3.8 | **∥ with anything**; owns `OverlayShell.tsx`'s keydown effect |
| **S47-6** — EG-1, KI-54's measurement | — | The measurement, its recorded outcome, and the disposition its result selects. **Not a fix story** | **∥**; owns `docs/known-issues.md` KI-54, and source only if EG-1's pass path selects it |
| **S47-7** — the register, the sweep, the landing audit | all | §3.4's ontology amendment; the tracker section; the document sweep below; the owner's observation sheet; the whole-set landing audit | Sequential, last |

**The live pass: AFTER implementation, pure inspection — the same shape phase-46 landed on, and the reason is different.** Phase-46 chose it because B-Q5's straddle left. Here the reason is that **there is nothing to look at before implementation**: the indicator, the readout and the feel of the threshold do not exist as artifacts. What makes "after" safe rather than expensive is P47-3 — every look and feel decision is a named constant with a hand-written oracle, so a reversal is an edit to the constant plus the literals §5 publishes, with no gate redesign and no red window. **No lane starts a dev server; the owner drives `descvi:dev`.** §9's U-rows are what the pass answers.

### The document sweep — each lands in the commit that makes it true

> ⚠ **MEMBERSHIP IS DERIVED BY COMMAND, NOT FROM THIS LIST.** Phase-46's landing audit found its own sweep list short **four times**, each layer wider than the last, and published the instrument the next lane inherits: `git grep -n 'phase-47' -- .omc/plans docs .omc/specs`, plus the anchor-extract `grep -rhoE '`[A-Za-z0-9_./-]+\.(ts|tsx|mjs)#[^`]+`' docs .omc/plans .omc/specs .omc/research | sort -u` intersected with each story's file list. **Run both; this list is the floor, not the set.**

1. **`.omc/specs/interaction-ontology.md`** — §3.F-1 rows 1–4 and §3.F's v1-reality note (§3.4, §2.2), at S47-7 and S47-3 respectively. **No v3-cell tag is minted.**
2. **`docs/e3/tracker.md`** — the phase-47 section; the v3 CLOSE line's QoL sentence annotated with where `undo-focus-ownership` landed; **the 2026-08-27 owner routing of KI-47 and KI-54 recorded as the fresh owner input it is**, since it is in neither the v3 CLOSE record nor either known-issue.
3. **`docs/known-issues.md`** — **KI-47**: the recorded fix direction corrected (§2.8) and the routing to phase-47 added; **KI-54**: the routing added, replacing *"아직 어느 페이즈에도 라우팅되지 않았다"*, and EG-1's outcome recorded whichever way it goes; **KI-48**: a cross-reference noting a second armer with its narrower condition (§3.3) — a note, not a re-grade.
4. **`docs/post-loop-backlog.md`** — `B-Q4`'s row gains the line that the cheap mitigation landed at phase-47 **and that auto-scroll is untouched**; `undo-focus-ownership` CLOSES with its residual (§3.8); `undo-history-loss` gains one line saying phase-47 did NOT touch it and why, because that row exists to keep the two apart; `MAX_MOVE_STEPS`'s re-discussion trigger is recorded beside `MAX_MEMBERS`'s.
5. **`docs/reference/structural-limits.md`** — the `move-up`/`move-down` section gains the repetition contract and the `MAX_MOVE_STEPS` bound. ⚠ **It also carries a note that the four move refusals now reach a SECOND surface** (the canvas gesture) with gesture-shaped wording, so a future lane editing one wording knows there are two.
6. **The four sibling plans.** `git grep -n 'phase-47' -- .omc/plans` — every live routing promise to this phase gets its disposition in place, and a dated erratum block per file, on F46-G's own precedent. ⚠ **Dated ✅ LANDED annotations, revision-log rows, round records and quoted probe inputs are NOT edited** — a record rewritten to match a later outcome stops being a record.

---

## 5. Gate → test mapping, and the definition of done

Every row names a mutant **by symbol** and the failure it produces. **No row records a count.** A row that cannot name a phase-47 mutant is labelled INHERITED. ⚠ **"The local loop is green" is not this phase's definition of done** — G47-4/5/6/9 live only in `pnpm test:e2e`.

| Gate | Asserts | Where it runs | RED-when |
|---|---|---|---|
| **G47-1** the repetition IS the shipped verb | for a subject with ≥ 3 admissible siblings, `computeStructuralEdit` with `steps: N` produces `page.tsx` **byte-identical** to N sequential single-step calls chained through `moveAdjacent` | `pnpm gates` | change the loop bound to `N - 1`; or pass `expect` on every iteration (iteration 2 then refuses `stale-baseline` and the request writes nothing where the chain wrote) |
| **G47-2** one gesture, one undo | a `steps: N` request appends exactly one journal entry, and one `undo` restores the pre-request bytes | `pnpm gates` | move the loop OUT of the single `prepare` callback into N `commitWrite` calls — the entry count moves and the row names it |
| **G47-3** the `steps` parse is per-verb and total | `steps` is accepted only on `move-up`/`move-down`, only as an integer in `[1, MAX_MOVE_STEPS]`, and 400s with the verb named on every other verb and every non-integer/out-of-range value | `pnpm gates` | delete the `move-up`/`move-down` guard from `parseStepsForOp` so `delete` accepts a count; or widen the range check to `>= 0` — `steps: 0` then writes nothing and answers 200, which is a 200 for an operation nobody performed |
| **G47-4** the flow axis refuses what it cannot measure | a grid parent, a wrapped flex row, and a flex row with one `order:`-moved child each produce `no-flow-axis`, paint no indicator, and render the ko + en refusal; a block parent and a flex column each produce a usable slot set | `pnpm test:e2e` | raise `FLOW_AXIS_TOLERANCE_PX` past the grid fixture's gutter — the grid case then measures as a row and offers slots that do not exist |
| **G47-5** the slot map, both directions and the no-op | the drag round-trip: N slots down then N slots up leaves `src/app/**/page.tsx` and `.descvi/screens.json` byte-identical; and a drop into slot `i` or `i+1` issues **no POST at all** (bridge spy) | `pnpm test:e2e` | change `j - i - 1` to `j - i` in the down branch — the round-trip's diff is the element one slot past where it started; the shipped `adjacent-sibling move round-trips (↓ then ↑) byte-identically` row stays GREEN throughout, which is why this row exists |
| **G47-6** the new paint stays outside the kind contract | the indicator and the readout are present during a drag, are computed `pointer-events: none`, and carry neither `data-dsh-handle` nor `data-v3-glyph-control`; the shipped `family === "other"` emptiness leg stays GREEN with the drag live | `pnpm test:e2e` | set the indicator's inline `pointerEvents` to `"auto"` — `e2e/resize-handles.spec.ts#    expect(scene.operable.filter((n) => n.family === "other")).toEqual([]);` names it, and G46-1/G46-2 name it too. ⚠ **The mutant is PLANTED in the new spec**, not applied to the shipped row, so F46-D's `readScene` obligation does not transfer (§2.11) |
| **G47-7** the readout joins the shipped stack rather than copying it | the drag readout is a child of `#dsh-handle-layer`, is laid out by `layoutReadouts` alongside the three shipped readouts (all four stack, none overlaps), and carries the family's leading accent | `pnpm gates` for the stack and the accent; `pnpm test:e2e` for the painted accent (⚠ **the painted leg is NEW — §2.7 measured that `e2e/resize-handles.spec.ts` carries zero accent assertions today**) | append the readout to `#dsh-reorder-layer` instead — it leaves the stack and the four-node non-overlap leg fires. ⚠ **A second `READOUT_ACCENT_PX` declaration in a new file is caught by `spacing-readout-accent.test.ts`'s cross-file agreement row only if the new file is added to it; adding it is part of this row** |
| **G47-8** the undo dead window | with focus on `document.body` and nothing selected, Cmd+Z calls `bridge.undo` exactly once; with focus inside a value `<input>` it calls it zero times; with focus on a node outside every host it calls it zero times | `pnpm gates` | remove the body term from the ownership disjunction — the first leg goes RED and the other two stay GREEN, which is what proves the widening did not swallow the guard |
| **G47-9** the theme source is the prop | after a theme toggle with a selection held, the ring, the corner chip, the spacing affordances, the spacing readout and the reorder indicator all read the new theme's literals in the SAME commit as the toggle | `pnpm test:e2e` | restore `layer.closest(".dark")` at any ONE of §2.8's five sites — that family alone reads the old theme and is named. Plus a source-text leg in `pnpm gates`: **plant a sniff, see the enumeration name it, remove it** (the instrument is shown able to produce a non-zero result before its zero is believed) |
| **G47-10** register and artifact | `node scripts/check-v3-registers.mjs` GREEN after the §3.F-1 amendment; `git diff --exit-code .descvi/screens.json` clean | `pnpm gates` | **INHERITED GATES, not phase-47 rows.** Both can go RED on their own mutants — mint a twelfth `<!-- v3-cell:… -->` tag on an amended §3.F-1 row (the hardcoded eleven-slug vocabulary names it); hand-edit the artifact. They are listed because they are what catches an unintended widening, not because this phase adds an assertion to either |

**The price of revising a look or feel value, PUBLISHED here so it is not discovered by mutation later (F46-B's lesson).**
- `REORDER_INDICATOR_THICKNESS_PX`: the constant, plus the hand-written literal in G47-6's row. **The literal is hand-written on purpose (RR-3) and must not be derived from the constant to make a shorter price true.**
- The indicator's colour: **zero constants** — it is `ringGroupShades("descriptive", …).deep`, so a palette change carries it; what a revision costs is the FIXED group argument plus G47-9's hand-written literals.
- `FLOW_AXIS_TOLERANCE_PX`: the constant, plus G47-4's grid fixture, whose gutter is what makes the mutant fire.
- `MAX_MOVE_STEPS`: the constant, G47-3's out-of-range literal, and the backlog's re-discussion trigger line.

---

## 6. Pre-mortem

### S1: the drag lands the element one slot off, and every gate stays green

- Caught by: G47-5's round-trip, which is asymmetric under any off-by-one — the shipped `adjacent-sibling move round-trips (↓ then ↑) byte-identically` row cannot see it because it only ever moves one slot.
- Prevented by: §3.2's slot table, stated as a table in the plan rather than derived at implementation time, plus G47-1's byte-identity against N sequential single-step calls.
- Residual: a drag whose intended slot the USER read differently from the indicator — the indicator is drawn from the same snapshot the slot is computed from, so a wrong snapshot draws a consistent lie. §9 U2 is the live read.

### S2: KI-54 gets a plausible cause written into the plan and a fix built on it

- Caught by: EG-1's stop boundary — an observation fitting no planned path stops the story and records the gap.
- Prevented by: P47-5, and KI-54 being an Evidence Gate rather than a story. **No section of this plan states a cause.**
- Residual: None.

### S3: the reorder gesture ships and a shipped Shift-click or resize gesture silently changes

- Caught by: `e2e/multi-select-shield.spec.ts`'s five travel-guard cases and `e2e/resize-handle-shield.spec.ts`, both re-run unchanged; plus `e2e/spacing-gesture.spec.ts`'s shipped `defaultPrevented` pair (a handle press reads `true`, the popup's input reads `false`) and its caret row, which are what pin THREE arms rather than two.
- Prevented by: DR47-2 — the shield is not edited, so no arm can be made unreachable the way phase-42's ROW D once was. A NEW row in the reorder spec additionally asserts that an ordinary reorder press still takes the ordinary arm (`defaultPrevented === true`), so "we did not add a fourth row" is asserted rather than assumed.
- Residual: the new `document`-capture `pointerdown` listener runs before every shield listener on every press in the app, including presses it declines. Its decline path reads one containment test and returns.

### S4: the trailing-click latch is armed and no click ever consumes it, swallowing an unrelated one

- Caught by: a row that drags, releases OUTSIDE `#dsh-stage`, then issues a programmatic `.click()` on a canvas element and asserts the selection changes — the exact KI-48 shape, driven at the new armer.
- Prevented by: §3.3's arming condition — only a real `pointerup` whose target is inside `#dsh-stage`, never a `pointercancel`, never an Escape-cancel on its own.
- Residual: a `pointerup` delivered inside the stage while the page is losing focus, after which no click arrives. That is KI-48's existing shape at a strictly narrower condition than the shipped armer's (which arms with the button still down), and the shield's own `takeTrailingClickSuppression()` on the next press drops it. **Recorded on KI-48, not re-graded.**

### S5: `steps` turns one write-lock hold into a long one, and the first anyone hears is a stalled editor

- Caught by: EG-2's measurement, and a `pnpm gates` row asserting the parse count for a `steps: N` request equals N × the parse count of one single-step request — a RELATIVE assertion that needs no absolute number and fires on any added per-step work.
- Prevented by: `MAX_MOVE_STEPS`, and the shipped `withWriteLock` lifecycle being unchanged so nothing new can hold it.
- Residual: the absolute cost at the cap on the largest corpus page is set by EG-2 and not by this plan.

### S6: the ontology amendment ships and the sites it falsifies are a second job nobody was assigned

- Caught by: S47-7's sweep, whose membership is derived by the two published commands rather than from §4's list.
- Prevented by: F46-A/E/G's own lesson written into §4 as an instrument rather than a list — the four sibling plans are in scope by command, not by whether anyone remembered them.
- Residual: the class F46-E named that no command can enumerate — a third-party anchor made AMBIGUOUS by this phase ADDING a byte-identical line somewhere. Nothing predicts it; the anchor gate names it when it happens.

---

## 7. ADR

**Decision.** Phase-47 ships drag-to-reorder as a `document`-capture pointer gesture on the current single-member selection, whose drop model reads the edit-map's published sibling chain and a MEASURED flow axis, and whose commit is an optional `steps` repetition of the shipped `move-up`/`move-down` verb executed as N in-memory applications of `moveAdjacent` inside ONE `commitWrite` — one journal entry, one Cmd+Z, atomic. It paints a non-hittable blue indicator in a new ring-layer container and a W×H readout as a fourth member of the shipped readout stack. It carries four riders: `undo-focus-ownership` (closed by widening ownership to "nothing focused"), KI-47 (closed by replacing five theme sniffs with the `dark` prop, and by correcting the known-issue's own false remedy), KI-54 (an Evidence Gate, never a fix), and B-Q4's cheap mitigation.

**Drivers.** D47-1 (the undo unit is the journal entry, so N client POSTs are N undos and one reachable half-landed state), D47-2 (the shield's arm table is not the obstacle; the trailing click is), D47-3 (the ontology's non-flex row is wrong about the commonest container in the corpus).

**Alternatives considered.** For the commit: N sequential POSTs; a `move-to-index` verb; a client-composed span rotation. For the listener: a fourth arm; an extension of the ordinary arm. For the drag start: press-selects-then-drags; a dedicated ring handle. For the axis: the Tailwind class model; `getComputedStyle`. For the click: pointer capture and retarget; widening the shield's travel guard. For the readout: a third `styleReadout`; `placeBeside`. For KI-47: the recorded dependency-array remedy (falsified); a two-site fix. For undo: moving default focus; "overlay alive ⇒ owned".

**Why chosen.** Every chosen option is the one that lets an existing, gated mechanism carry the new behaviour instead of minting a parallel one: the shipped composer carries the repetition, the shipped latch carries the click, the shipped readout stack carries the readout, the shipped shade function carries the colour, and the shipped `handleStructureSaved` carries the post-write handoff. ⚠ **The one place that argument does NOT reach is the drop model, which is genuinely new client code**, and the compensation is that it derives nothing the artifact already publishes (P47-2) and refuses everything it cannot measure (DR47-4).

**Consequences.** (i) `.omc/specs/interaction-ontology.md` §3.F-1 moves from `deferred-v2` to SHIPPED on two of five rows and is SPLIT on a third — a behaviour register change, the first since phase-45. (ii) `docs/reference/structural-limits.md`'s move section gains a repetition contract, and the four move refusals gain a second user-facing surface with its own wording. (iii) Two known-issues are corrected in place, one of them because its recorded remedy is false. (iv) **The revert is per-story and none of them is joint.** The gesture reverts by removing one hook and one layer; `steps` reverts to `undefined` with the shipped path byte-unchanged (G47-1 is what proves the single-step path never moved); KI-47's fix and the undo widening each revert alone. (v) The definition of done is explicitly larger than `pnpm gates` — four rows are `pnpm test:e2e`-only.

**Follow-ups.** B-Q4's auto-scroll (§8). Cross-parent reorder and Alt+drag duplicate stay deferred-v2. `MAX_MOVE_STEPS`'s re-discussion trigger. KI-54's disposition, whichever EG-1 selects. The indicator's thickness and the threshold's feel are §9's to revise.

---

## 8. Out of scope — with a disposition line each, because silence is what let three items go missing

| Item | Disposition |
|---|---|
| **`selection-ring-treatment`, `spacing-affordance-mark`** | ⚠ **OUT by owner ruling, 2026-08-27**, given in this planning session. They stay **unrouted backlog rows** — a destination is not invented for them here, which is the rule `docs/known-issues.md` KI-50's routing line already established for this repo |
| **B-Q5 — handle admission on small elements** | **phase-48**, by owner ruling 2026-08-25. `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` §8 carries its four inherited findings in full and this plan does not restate them |
| **Marquee** | deferred-v4 — the stage-background drag slot is contested by v4's absolute insert-on-drop |
| **KI-10** | Inherited, owner-ruled at v3 close. §3.2's `multi-instance` refusal BOUNDS it on this surface (a shared-oid subject refuses rather than guessing an instance) and does not fix it |
| **B-Q4's viewport-edge auto-scroll** | OUT. The owner ruled it the confirmed follow-up direction (2026-08-19) and ruled the W×H readout the cheaper preceding mitigation; **this phase ships the second and not the first.** ⚠ §3.7 states what that leaves uncovered rather than letting the row read as closed |
| **Cross-parent drag (§3.F-1 row 2), Alt+drag duplicate (§3.F-5)** | deferred-v2, unchanged. Row 2's own gate note names import/format preservation as the hard part; phase-47 reorders within one parent |
| **Multi-select drag** | Refused in 47 — **LEAD ruling**, §3.6, on three grounds none of which is the one supplied with the default |
| **The W×H readout during a RESIZE drag** | OUT, and it is the case B-Q4's own predicate actually describes. It is a one-condition change on the very node §3.7 builds, and taking it would be scope the owner's ruling does not cover. Recorded here so a later lane knows the node is already there |
| **KI-48** | Inherited. §3.3 adds a second armer under a narrower condition and §4 item 3 records it on the entry; the fix candidate in KI-48's own body is untouched |
| **KI-19 / KI-49 / KI-50** | Inherited, unrouted since the owner's 2026-08-24 exclusion. This phase makes KI-19's symptom strictly smaller (one handoff instead of N) without owning it |
| **`undo-history-loss`** | OUT, and the backlog row exists precisely to keep it out of `undo-focus-ownership`. It is unmeasured testimony; §4 item 4 records that phase-47 did not touch it |
| **`parseLayout`'s read-only set / the `justify-items-*` inertness** | OUT. DR47-4 chose measurement over the class model specifically so this phase does not open that set, which F46-G item (i) records as belonging to nobody |
| **Any change under `packages/descvi/src/vite/**`** | OUT, deliberately: an edit there restarts every dev server watching the repo, the owner's included |
| **v3 plan archiving** | Deferred to v3.5 close, unchanged |

---

## 9. Residual risk, and the owner's observation sheet

**RR-1 — the drop model is new client code and nothing in the compiler relates it to the engine's own admission.** The chain it walks is the engine's published output and the axis it measures is the browser's, but *"the slot the user aimed at"* has no server-side oracle. G47-5's round-trip and G47-1's byte identity bound the damage to a wrong-but-valid reorder; they do not make an aimed slot provable. **Stated as bounded rather than dismissed.**

**RR-2 — the snapshot is taken once and the DOM can change under it.** The `!isConnected` abort covers the case KI-50 measured (a subtree replaced by a react-refresh landing). It does not cover a layout shift that leaves the element connected — a lazy image resolving mid-drag moves the slots under a snapshot that will not notice. Bounded: nothing writes during a drag, so the window is the gesture's own duration.

**RR-3 — `steps` widens one wire field and the shipped panel is the control.** The panel sends no `steps` and must stay byte-identical in behaviour; G47-1 is what proves it, and it proves it by comparing the two paths rather than by asserting the panel was not touched.

### The owner's observation sheet — one row per U-item, for the live pass

| U | The question, as the owner meets it | What it costs to act on the answer |
|---|---|---|
| **U1 — is "drag the selection" the right gesture?** | DR47-3 requires the element to be selected first, so moving an unselected element is click-then-drag where Figma is one gesture. Does that read as a safety rail or as a missing step? | A "one gesture" answer is DR47-3(b), which the plan refuses on an async hazard in shipped source — so it is a REPLAN of that decision, not a value change. Stated plainly because it is the only U-row here whose answer is not cheap |
| **U2 — does the indicator read as a drop slot?** | 2 px, the ring system's blue, spanning the neighbours' cross-axis extent, no ghost and no element movement. Is the slot unmistakable, or does it read as a divider? | Thickness and span are constants; the price is §5's published list — the constant plus one hand-written literal. **No gate edit, no red window** |
| **U3 — is the 4 px threshold right for a reorder?** | It is the shipped `POINTER_DRAG_THRESHOLD_PX`, shared with the resize gesture and the shield's travel guard. A reorder may want more (a shaky click should not start one) | ⚠ **This one is NOT a free value change**: the symbol has four consumers by design and its module says so. Raising it for reorder alone means a second constant, which is what that module exists to prevent. **The answer to a "too twitchy" verdict is a reorder-specific constant with its own docblock, and the plan says so rather than implying a one-value edit** |
| **U4 — does the W×H readout help?** | The owner ruled it as B-Q4's cheap mitigation for this gesture. §3.7 records that a reorder changes no size, so the number is constant during the drag, and that reorder's own blind case is an off-screen drop slot the readout does not reach | A "it does not help" verdict costs the readout node and nothing else — it is a fourth stack member and the stack is a list. A "the blind case is the real problem" verdict routes to B-Q4's auto-scroll, which is §8 |
| **U5 — the refusal's strength and its reachability** | §3.5's five refusals are ko + en in the readout family. The `no-flow-axis` case is reachable by hand on any grid or wrapped-row parent in the corpus; the others need specific shapes. ⚠ **Phase-46's U3 went unanswered because nobody established reachability before the pass** — so this row carries it: the reachable subject is named at S47-7 by running the axis predicate over `src/app/**` and recording which screens produce which refusal | A wording change is one table. A STRENGTH change is a colour, and §5.9(1)'s shipped ranking rule binds it — the informational readout is never the loudest |
| **U6 — KI-47, seen rather than computed** | S47-1's acceptance is asserted mechanically, but the phase-46 live pass is what turned an asserted focus treatment into a confirmed one. Toggle the theme with a selection held and with a spacing popup open | If a family still lags, it is a site §2.8's enumeration missed — and the fix is one more site, not a redesign |

---

## 10. Evidence Gates

### EG-1 — KI-54's cause

- Claim: the outside-click close of the spacing popup wipes the rendered screen. **The cause is unknown**, and `docs/known-issues.md` KI-54 records that no lane has traced the `commit === true` arm. Nothing in this plan states a mechanism.
- Evidence method: reproduce the gesture live on `descvi:dev` with the browser devtools open, and capture, in this order: (1) a `MutationObserver` on `#dsh-screen` recording every childList mutation with its `removedNodes`, started before the click; (2) the console and the network panel across the click, specifically whether any `POST /edit` is issued and what it answers; (3) whether the React tree remounted (a Suspense fallback appearing) versus the subtree being removed without a replacement; (4) whether `.descvi/screens.json` and `src/app/**/page.tsx` are dirty afterwards — re-confirming the entry's disk-clean finding rather than inheriting it. **The instrument is validated first**: with the observer running, close the popup with **Escape** (the `closePopup(false)` arm S46-4 traced end to end) and confirm the observer reports the popup's own removal and nothing else. An observer that cannot report the known-good close has measured nothing.
- Pass path — **the wipe reproduces and the observer names what removed the subtree**: record the mechanism on KI-54 with the capture beside it, then rule whether the fix is in phase-47's budget. If it is one bounded change in `use-spacing-drag.ts` or its callers, it lands as S47-6b with its own RED-when; if it reaches the preview/session layer, it is routed with the measurement attached and NOT fixed here.
- Alternate path — **the wipe does not reproduce**: record the non-reproduction with the exact environment (screen, element, popup dirty vs clean, browser, whether a prior HMR had landed in that session), and record it as an observation on KI-54 rather than closing it. **A non-reproduction is not a fix and the entry stays OPEN.**
- Required before: any source change attributed to KI-54. Nothing else in phase-47 depends on it; S47-6 is parallel to the whole ladder.
- Unexpected result: the observer reports NO mutation to `#dsh-screen` while the owner's symptom is visible (i.e. the wipe is a paint or a stacking effect rather than a DOM removal), **or** a `POST /edit` is issued that the entry's disk-clean finding says cannot exist. **Either stops the story**: the finding is recorded, the entry is amended with the new boundary, and no fix is attempted in phase-47 — a cause that contradicts the recorded evidence is a new investigation, not a bug fix.

### EG-2 — the per-step parse cost, and therefore `MAX_MOVE_STEPS`

- Claim: `MAX_MOVE_STEPS = 32` is a safe bound for N in-memory applications of `moveAdjacent` under one write-lock hold. The number is adopted from phase-45's `MAX_MEMBERS = 32` as a precedent, **not measured**.
- Evidence method: over the LARGEST `page.tsx` in `src/app/**` (selected by byte size, named in the record), time `computeStructuralEdit` for `steps` = 1 and `steps` = 32, in-process, no filesystem and no HTTP, median of a stated number of runs. The instrument is validated by confirming the `steps` = 32 timing is not equal to the `steps` = 1 timing — a harness that cannot see 32× work is not measuring the loop.
- Pass path — **the 32-step time is under 250 ms**: keep `MAX_MOVE_STEPS = 32`, record the measurement and the page it was taken on beside the constant, and record the re-discussion trigger on the backlog beside `MAX_MEMBERS`'s (S47-0).
- Alternate path — **it is over 250 ms**: lower the cap to the largest N whose measured time is under it, record that N with the measurement, and add one line to §3.5's refusal table for a drop whose distance exceeds the cap, worded as a distance limit rather than as an engine failure.
- Required before: S47-0's `MAX_MOVE_STEPS` value ships. The `steps` mechanism itself does not wait — only the number does.
- Unexpected result: the timing does not scale with `steps` at all (flat, or superlinear beyond N²). **Stop and report**: flat means the loop is not running and G47-1 is passing for a reason nobody understands; superlinear means `moduleContext` is doing something per-call that this plan's model of it does not contain, and the ceiling cannot be set from two points.

---

## Open Questions

- **Does the owner want the reorder gesture available on an UNSELECTED element (one gesture instead of two)?** §9 U1. It matters because the answer is not a value change: DR47-3(b) is refused on an async selection-commit hazard in shipped source, so a "yes" is a replan of that decision and would need a way to make the selection land synchronously before the snapshot is taken.
- **Should `move-up`/`move-down`'s panel buttons also gain a repetition (press-and-hold, or a count field)?** Not proposed and not shipped. It matters because `steps` makes it nearly free, and leaving the panel single-step means two surfaces with different reach over one verb — the drift `refusal-messages.ts`'s docblock exists to prevent, one level up.
- **Where does the `no-flow-axis` refusal's suggested repair actually point?** §3.5's copy says *"apply auto-layout (flex) first"*, and the panel's alignment widget is enabled only for parents that already resolve to `flex-row`/`flex-col`. It matters because if no shipped control turns a block or grid parent INTO a flex parent, the refusal names a repair the user cannot perform — which is P47-4's failure at one remove. **Not blocking**: the refusal is still correct about why the drag is off; only the second clause is at risk, and S47-7 can delete that clause without touching the mechanism.
- **Does `steps` belong on the wire, or should the client send N and the bridge fan out?** Settled as the wire (DR47-1) and recorded here only because a reviewer may prefer the bridge. It matters for the SaaS seam: a bridge fan-out would put the repetition on the client side of the seam, where a transport failure mid-fan leaves the half-landed state DR47-1 exists to prevent.
