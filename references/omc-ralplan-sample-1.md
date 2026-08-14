# RALPLAN — phase-27: KI-32 client-side liveness

**Mode: DELIBERATE. Revision r2** — revised against `.omc/artifacts/phase27-revision-brief-r2.md` (three lanes: `audit-r2` primed closure audit, `arch-r2` unprimed probing, codex flagship; all CHANGES REQUIRED). r1 revised against `.omc/artifacts/phase27-revision-brief-r1.md`. Branch: `feat/phase-27-ki32-liveness` off `main`. Subject: KI-32 in `docs/known-issues.md`.
Input brief: `.omc/specs/phase-27-ki32-liveness-input.md`. Planner lane: `plan-r0`.

**Gate labels are prefixed `P27-` throughout r2.** r1 used bare `G2`/`G4`, which collide with **phase-23's** gate labels quoted inside `e2e/reporters/artifact-oracle.ts` — a collision that produced a real misreading (§R2-10 / E19).

**What r2 changed, at the top.**
1. **Real tab backgrounding does not fire `visibilitychange` or `focus` in this harness** (E22, measured, 12 iterations with a passing control). OQ-4 is **answered NO**, not open. P3's primary path is dead and is replaced by a *stated coverage boundary*, not a fallback.
2. **`context.setOffline` is a genuine browser-emitted trigger that leaves an open socket alone** (E23, measured). The `online` limb — added in r1 for a coverage reason that r2 downgrades — turns out to be **the only limb in the whole option table with a live trigger**. Its justification is replaced accordingly.
3. **§3.2's replacement reason from r1 was itself part-wrong.** My r1 dissent's *conclusion* held and was measured; its *reason* ("focus and visibilitychange are microseconds apart") was an unmeasured Chromium timing claim, and by E22 nobody in this harness can measure it. It is replaced by a **structural** reason that needs no timing at all (E24) — and the residual the structural reason does *not* cover is now stated instead of hidden. This plan has caught that exact shape in others twice; it caught me too.

**Where r2 does not simply comply:** `[PLANNER DISSENT]` markers in §3.1 (rejecting R2-12) and §3.2 (the structural reason has a residual the ruling's phrasing implies away).

Deliverable tree is `packages/**` plus the e2e harness that gates it. `src/app/**` is dogfood, touched only as a *fixture*.

---

## 0. Evidence ledger

Tier order: **LIVE / MEASURED** > **RUN** > **PROBE** > **READ** > **REASONED**. Nothing at READ or REASONED may be stated as settled in a commit, doc, or review.

| # | Fact | Tier | Source |
|---|---|---|---|
| E1 | `vite:ws:connect` fires exactly once per document; the reconnect-refetch repair recovers nothing. | **LIVE** | KI-32, 11 runs, two instruments. |
| E2 | SIGKILL / SIGINT / graceful shutdown all recover under 2.5 s via `1006` → poll → `location.reload()`. | **LIVE** | KI-32. |
| E3 | Clean close (`wasClean=true`, 1000) leaves the client permanently stale. | **LIVE** | KI-32, with a negative control. |
| E4 | Half-open produces no close event; **minimum** 45 s stale, upper bound unmeasured. | **LIVE (lower bound)** | KI-32. |
| E5 | Dispatched `visibilitychange` on `document` and `focus` on `window` reach listeners; zero after unmount. | **RUN** | `arch-r1`, vitest + jsdom 25.0.1 + RTL. |
| E6 | `document.visibilityState` is stubbable via `Object.defineProperty` and restorable. | **RUN** | `arch-r1`. |
| E7 | `document.hasFocus()` is `false` under jsdom. | **RUN** | `arch-r1`. |
| E8 | A component-level jsdom row over `DescviBootstrap` already exists: `packages/descvi/src/vite/__tests__/bootstrap.test.tsx#// @vitest-environment jsdom`. | **READ** | r0. |
| E9 | The overlay already wakes on window focus, **session only**: `packages/descvi/src/react/DescviOverlay.tsx#window.addEventListener('focus', refresh);` → `refreshSidecarSession`. | **READ** | r0. |
| E10 | The edit-map is fetched once per `bridge` identity (`packages/descvi/src/react/DescviOverlay.tsx#.fetchEditMap()`) and after a committed className edit. No wake touches it. | **READ** | r0. |
| E11 | `visibilitychange` / `visibilityState` / `hasFocus` occur zero times across `packages/`, `e2e/`, `src/`. | **READ** | r0. |
| E12 | A `spec.ts` save is off Vite's HMR watcher (`descvi.vite.config.mts#watch: { ignored: ['**/spec.{ts,tsx}'] },`) and reaches the client **only** through the descvi ws channel (`descvi.vite.config.mts#Re-extraction on a spec`). | **READ** | r0. Load-bearing for P0 — see R10. |
| E14 | The session handshake is a global single-flight that dedups even a FORCED refresh: `packages/descvi/src/react/overlay/engine/session-coordinator.ts#if (handshake !== null) return handshake;` sits after `packages/descvi/src/react/overlay/engine/session-coordinator.ts#if (!force && current !== null) return { sessionId: current };`. | **READ** (lead-verified, re-read) | r1 brief §A. |
| E15 | The dedup window is the in-flight duration of the promise (cleared in the `.finally` at `packages/descvi/src/react/overlay/engine/session-coordinator.ts#}).finally(() => {`), not one tick. | **READ from source** | This lane, r1. ⚠ **r1's ledger claimed `P27-C19` pins this. It does not — C19 pins E14.** Correction per R2-4: with §3.2's reason now structural (E24), **nothing in this design depends on E15**, so it is recorded as an observation and is **knowingly ungated**. That is a deliberate choice, not an oversight. |
| E16 | `e2e/undo-session-restart.spec.ts#// The focus listener attaches in a React effect after mount;` dispatches `focus` and asserts a `/status` GET returns 200. | **READ** (lead-verified) | r1 brief §B. |
| E17 | `DescviOverlay` has **no bridge prop**: `packages/descvi/src/react/DescviOverlay.tsx#const bridge: SidecarBridge = useMemo(` builds it internally with an empty dep array. | **READ** (two lanes) | r1 brief §C1. |
| E18 | jsdom delivers dispatched `online`/`offline` on `window`. ⚠ This proves **delivery of a dispatched event only** — it says nothing about when a real `online` fires. | **PROBE** | This lane, r1. Scope narrowed per R2-11. |
| E19 | The artifact oracle is a **delta**, not an absolute clean-tree check: `e2e/reporters/artifact-oracle.ts#EVERY TREE CHECK BELOW IS A DELTA`. ⚠ **r1 misread its next clause.** `e2e/reporters/artifact-oracle.ts#so G2 and G4 CAN share a run` means *a mutant present before a run leaves no tree delta* — **not** that two implementations can execute in one invocation. Those `G2`/`G4` are **phase-23's** labels, not this plan's. | **READ** (lead-verified; lead records passing the misreading through in r1) | r1 brief §C3, corrected by R2-10. |
| E20 | The identity golden's `distribution` is hand-edited **first**, then regenerated (`e2e/reporters/identity-oracle.ts#The pin is hand-maintained on purpose`); it is the raw `TestResult.status` axis (`e2e/reporters/identity-oracle.ts#Reconciliation note: both lines above are this golden's RAW`). | **READ** (lead-verified) | r1 brief §C4. |
| E21 | `testMatch` is a per-project allow-list and a non-match is **silent** (`playwright.config.ts#The failure is silent`). | **READ** | r1 brief §C5. |
| **E22** | **Real tab backgrounding fires NOTHING.** `chromium.launch()` → one context → two pages → `bringToFront()`, 12 iterations, headless and headed, with a passing control (a synthetic dispatch in the same page logged `vc` then `focus`). Page A stayed `visibilityState=visible`, `hasFocus()=true`; **zero** `visibilitychange`/`focus`/`blur` after return. `CDP Emulation.setPageVisibility` absent in this build. | **MEASURED** | `arch-r2`. **OQ-4 is answered NO.** |
| **E23** | **`context.setOffline(true)` then `(false)` produces a genuine in-page `["offline:false","online:true"]` (baseline `[]`), and does NOT disturb an already-open socket** — against a local `ws` server the page's `readyState` stayed `1` through both toggles with no `close` event. | **MEASURED** | `arch-r2`. This is the only browser-generated live trigger available to this plan. |
| **E24** | **Same-turn dedup is structural, not timing-dependent.** Measured against the real `session-coordinator.ts`: two synchronous calls → `getStatus` **1**; gap 1 ms / roundtrip 30 ms → **1**; gap 50 ms / roundtrip 5 ms → **2**; microtask apart / instant stub → **1**. `window.dispatchEvent` is synchronous and `packages/descvi/src/react/overlay/engine/session-coordinator.ts#  handshake = getStatus().then((result) => {` executes before the function's first `await`, so two refreshes in one synchronous turn dedup by JS semantics. | **MEASURED** | `arch-r2` + codex by reading. **Replaces r1's timing reason in §3.2.** |
| **E25** | **Two committed rows already pin this dedup**: `packages/descvi/src/react/overlay/__tests__/session-coordinator.test.ts#holds two distinct real bridges and mutation kinds behind one global initial handshake` and `packages/descvi/src/react/overlay/__tests__/session-coordinator.test.ts#single-flights a held re-handshake across two real bridges without clearing fresh surfaces twice`. | **READ** (lead-verified) | R2-6. **r1's P-F premise ("there was no gate") was false** — P-F re-grounded in §1. |
| **E26** | The overlay holds the edit-map **separately** (`packages/descvi/src/react/DescviOverlay.tsx#const [editMap, setEditMap] = useState<EditMapData \| null>(null);`) and the edit surface reads from it, not the manifest (`packages/descvi/src/react/overlay/OverlayShell.tsx#Read from the RESOLVED TARGET (edit-map → live spec.ts join), not from the screens.json manifest`). **A successful manifest wake can therefore leave the manifest fresh and the editor stale.** | **READ** | R2-13. Makes this a **half** recovery — see `P27-C21`. |
| **E27** | `e2e/undo-session-restart.spec.ts` is collected by the **`solo`** project (`playwright.config.ts#name: 'solo',`), not `design-view`, and `solo` runs last via `playwright.config.ts#dependencies: ['plain', 'design-view'],`. | **READ** | `arch-r2`. r1 implied the wrong project. |
| E13 | Citation gate reading on the tree carrying this plan. | **RUN, NOT a baseline** | The corpus includes `.omc/plans`, so this plan's own arrival moves the numbers. The only durable statement is the exit code. `arch-r2` independently re-checked every code anchor with its own matcher plus a non-uniqueness control. |

---

## 1. Principles

1. **P-A — Cover the shape, not the symptom.** Only a mechanism that never waits for a close event covers both stale paths.
2. **P-B — A conclusion is worth its reason.** r1 exists because §3.2's reason was separable; **r2 exists partly because r1's replacement reason was separable too.** The reason is what the next gate gets built on.
3. **P-C — Every gate carries a RED-when a stranger can run, and the RED is observed.** ⚠ Sharpened in r2 (R2-7): **an import failure is not a RED.** A pre-fix run of a suite whose module does not exist fails once, at import, which every row would "prove" equally. The RED-when must be a **per-row mutant against existing code**.
4. **P-D — Do not let the design lean on an unmeasurable.** *Correctness* must not depend on exposure. **Priority explicitly may.**
5. **P-E — Prefer state you cannot leak.** `P21-F30` and `P21-F22` are paid-for scars.
6. **P-F — A design that leans on an invariant must know exactly which half of it is gated.** ⚠ Re-grounded in r2. r1 stated this as "there was no gate", which E25 shows is **false** — two committed rows already pin the dedup. The principle survives with a sharper premise: the existing rows pin that dedup *happens*, through mutation kinds; nothing pins `refreshSidecarSession`'s own contract, and nothing pins that dedup *ends*. Gate the ungated half, not the whole thing again.

## 2. Decision drivers

- **D1 — Coverage per unit of always-on state.**
- **D2 — Gate reachability**, now split by E22/E23 into *unit-gateable* and *live-gateable*, which are no longer the same question (§4.2).
- **D3 — Exposure-independence of the argument.**

---

## 3. The forks, resolved

### 3.1 Fork #1 — what triggers a wake

**Resolution: unchanged in shape — `visibilitychange`→visible, `focus`, `online` (option 1D). The reason for the `online` limb is replaced, and its coverage claim is withdrawn.**

| Option | Pros (bounded) | Cons (bounded) |
|---|---|---|
| **1A — `visibilitychange`→visible + `focus`** | Zero timers. One manifest fetch per tab return, at most one per throttle window, loopback. **Covers the dominant descvi workflow**: the manifest changes because the user edited a source file in their editor, so they left the tab and will return. | Does not cover a socket dying while the tab holds focus. **And by E22 it cannot be live-verified at all in this harness** — see §4.2. |
| **1B — 1A + heartbeat** | Covers the focused-tab case outright. | Permanent recurring timer, torn down with the effect, must not fire under test; interval is a guess; gates need fake timers, which is where timer-teardown bugs hide. |
| **1C — 1A + throttled interaction wake** | Covers focused-and-interacting, zero timers. | Misses focused-and-idle — the case that motivates 1B. A second predicate for a partial slice. |
| **1D — 1A + `online`** ⬅ **chosen** | **It is the only option in this table with a browser-generated live trigger** (E23): `context.setOffline` toggling produces a real `online` and leaves an open socket at `readyState 1`, so it can drive an end-to-end live gate on a genuinely stale page. Zero timers, zero new predicate — same handler, guard and throttle, one more `addEventListener`. | ⚠ **Its coverage claim is withdrawn (R2-11).** E18 proves only that jsdom delivers a *dispatched* `online`. A real `online` fires when `navigator.onLine` goes false→true — not on every wifi or VPN change — and `onLine` does not imply origin reachability. r1 called it *"a substantial slice of the population 1B was deferred over"*; that was **unmeasured and is retracted.** It is an **opportunistic low-cost hint**, and it may not carry the argument for deferring 1B/1C. |
| **1E — ship `online` ALONE** (steelman, new in r2) | Fully live-gateable end to end; needs no artificial `close(1000)`; defers everything unverifiable until OQ-1 resolves or a live trigger appears. | **Ships the one limb whose coverage was just retracted, as the entire feature.** R2-11 and R2-12 pull against each other: 1E would have phase-27 deliver exactly the limb we can no longer claim covers anything measured, while the dominant workflow (edit in editor → return to tab) stays broken indefinitely. |

**`[PLANNER DISSENT] — 1E is tabled and rejected.** The ruling is right that after E22 it is the honest competitor, and r1 not containing it was a real gap. But adopting it inverts P-A and D1 in one move: it would let *gate convenience* select the shipped population. The correct response to "the best slice has no live gate" is to **name the coverage boundary and ship anyway** (§4.2), not to reshape the product around what the harness can watch. If review disagrees, the smallest concession that preserves the argument is to ship 1D and mark the `visibilitychange`/`focus` limbs as **unit-gated-only** in `docs/architecture.md` — which `P27-C24` does regardless.

**Why not 1B.** On **D1 + P-E**: permanent always-on state of a class this repo has already paid for, with gates that need fake timers (D2). **Secondarily** on P-D's *priority* clause, correctly scoped: 1B's *value* is governed by OQ-1/OQ-2; its correctness is not in question. ⚠ Note the r2 weakening: with `online`'s coverage claim withdrawn, **the residual population 1B would cover is larger than r1 implied.** The deferral now rests on D1/P-E alone, and OQ-2 is correspondingly more live.

**Named trigger to revisit:** OQ-2.

### 3.2 Fork #2 — what a wake refetches, and where it lives

**Resolution: 2A, unchanged. The reason is replaced for the second time, and this time the residual is stated.**

> **⚠ TWO REASONS HAVE NOW FAILED HERE. Both are kept, because the next reader will reach for one of them.**
> **r0's reason:** *"On every focus the session is refreshed twice — two concurrent forced adoptions."* **False** (E14). It charged 2A for a phantom cost and built a gate that could never go RED.
> **r1's replacement reason (mine):** *"`focus` and `visibilitychange` are separated by microseconds, so the handshake is always still in flight."* **Unmeasured** — a claim about Chromium event timing that, by E22, nobody in this harness can measure. Its conclusion was right (E24 row 4 confirms the lead's proposed G3 rewrite would have been vacuously green) and its reason was not. That is the same defect this plan caught in r0's text.

**The reason that replaces it, which needs no timing claim (E24).** On the **`focus`** path both refreshes occur in the **same synchronous turn**: `window.dispatchEvent` is synchronous, and `getOrAdoptSession` assigns the handshake before its first `await`, so the second caller cannot observe a null handle. Dedup is guaranteed by JS turn semantics. On the **`visibilitychange`** path there is no second refresh to dedup at all, because `P27-C04`'s throttle suppresses the sibling bootstrap wake. **§3.2 was charging itself with a race that JS turn semantics and its own throttle already exclude.**

**`[PLANNER DISSENT] — the structural reason has a residual, and the ruling's phrasing implies it away.** The two arms above cover *within-one-event* and *the suppressed sibling wake*. They do not cover the cross-event sequence: `visibilitychange` fires → bootstrap wake → bus → refresh #1; then `focus` fires in a **later task** → the bootstrap wake is throttled but **the overlay's own raw focus listener is not** → refresh #2. If #1's `getStatus` has settled by then, that is a genuine second GET (E24 row 3 shows the shape). So the honest cost of 2A is **at most one extra read-only `/status` GET per wake window**, not zero. I state it rather than let a clean "structural" claim absorb it, because the thing r0 actually feared — two *adoptions racing* — is what the structural reason genuinely excludes, and one extra sequential read-only GET is not that. E24 is measured; this residual is **REASONED from it** and is deliberately ungated: no design decision turns on it.

| Option | Pros | Cons |
|---|---|---|
| **2A — bootstrap-only wake; `onWake` dispatches `DESCVI_SESSION_REFRESH_EVENT` and calls `load()`. Overlay untouched.** ⬅ **chosen** | One source file. Covers the session on both wake paths via the bus listener that already exists. `DescviOverlay.tsx` stays out of scope; E16's committed spec keeps its unthrottled listener; E17's missing bridge seam stops mattering. Same idiom as `onManifestUpdate`. | Depends on E14 — gated for the half that was not already covered (`P27-C19`, re-grounded per E25). Residual: at most one extra read-only `/status` GET per wake window (dissent above). |
| **2B — shared factory consumed by bootstrap and overlay** (r0's choice) | No listener-level redundancy on focus. | **Its entire justification was a phantom** (E14/E24). Throttles a behaviour E16's committed spec exercises; needs an overlay component row E17 shows is not implementable without a banned convenience seam. ⚠ Note per R2-9 that E16's spec would **not** actually catch the throttle regression — see `P27-C20`. |
| **2C — bootstrap-only, no session dispatch** | Smallest diff. | No session refresh on visibility-without-focus — a new asymmetry of exactly the kind KI-32 is about, to save one dispatch the overlay already consumes. |

**Chosen: 2A, justified against 2C.** One line separates them; 2A pays an existing event dispatch and gets session coverage on the visibility path, 2C saves the line and keeps a hole.

**Edit-map — still OUT of the fix, but no longer out of the RECORD.** *Conclusion:* no edit-map wake in phase-27. *Reason:* E10/E26 show it is a **separate holder that the edit surface actually reads from**, so a successful manifest wake can leave the manifest fresh and the editor stale. That makes phase-27 a **half** recovery, which `P27-C21` must state and which promotes OQ-3 from optional to a mandatory entry in the KI-32 update (R2-13). Deciding to *fix* it is not this phase's call; deciding to *disclose* it is.

### 3.3 Fork #3 — is a component-level gate vacuous here?

**Resolution: NO, and it is measured.** `arch-r1` built a faithful replica: manifest fetch delta **1** post-fix, **0** pre-fix. E5–E7 transferred into the real runner.

**The item's conclusion survives; the item's reason does not (P-B).** The precedent at `packages/descvi/src/vite/bootstrap-entry.ts#Exported as a pure factory because a gate driven through` rests on `packages/descvi/src/vite/bootstrap-entry.ts#function getHot(): HotLike | undefined {` rejecting jsdom's `off`-less partial hot (`packages/descvi/src/vite/bootstrap-entry.ts#Under vitest the shape is ENVIRONMENT-DEPENDENT`). A `document`/`window` listener does not pass through `hot`. The factory is still extracted, because the predicate has seven behaviours (§7) far cheaper to gate directly than through a mounted component.

**Three vacuity traps, all contracts.** (1) `packages/descvi/src/vite/bootstrap-entry.ts#if (initialManifest !== undefined) return;` early-returns the effect → `P27-C11`. (2) `fetchManifestMap` falls back to `/screens.json` **and** a global counter sums three routes → `P27-C12`, per-URL. (3) `document.hasFocus()` is `false` under jsdom → `P27-C05`.

**⚠ A fourth, found in r2 (R2-8).** A *factory-level* latest-wins row is itself vacuous: the factory takes `onWake` as an opaque option and owns no loader, so such a row could only test a loader the test built — the very class `P27-C11` bans. That row moves to P2 as a `DescviBootstrap` wiring row (`P27-G2.2`).

---

## 4. What the design leans on that it cannot control

### 4.1 Exposure

- **Path ① (clean close) is exposure-gated by measurement.** KI-32: this repo's stack never produces a clean close (vite's own `ws.close()` is a `terminate()`); something in the network path is required.
- **Path ② (half-open) may also be exposure-gated — unresolved.** *Reasoned:* on pure loopback a VPN flap or wifi switch does not touch the connection, and on sleep both endpoints suspend together. KI-32 attaches the caveat to ① and not ②, and this lane cannot tell whether that was measured. → **OQ-1**, the largest uncertainty here.
- **The design's correctness does not depend on the answer (P-D); its priority does**, which is P-D's permitted use.
- **`online` interacts with OQ-1:** on loopback it fires for transitions that never broke the socket — a wasted throttled loopback fetch, bounded by `P27-C04`.

### 4.2 The verification tension — required section, and it is NOT resolved

**The limb with the best live gate covers the worst slice, and the limbs covering the best slice have no live gate at all.**

- `online` is **live-triggerable** (E23) and **weakly-covering** (E18 narrowed, R2-11).
- `visibilitychange` / `focus` cover the **dominant descvi workflow** and **cannot be live-observed** — E22 measured zero events across 12 iterations, headless and headed, with a passing control.

r1 resolved this silently by bundling all three limbs into one factory and letting one live row stand for all of them. **That is no longer allowed.** P3 splits the live gate:

- **`P27-G4a` — fully live**, driven by `context.setOffline` (E23), on a genuinely stale page. This is real end-to-end evidence for the `online` limb and for the shared handler, guard, throttle and loader wiring behind it.
- **`P27-G4b` — synthetic dispatch, and labelled as such.** It is evidence that the `visibilitychange`/`focus` listeners are **attached and wired**, and nothing more. r1's own words — *"a synthetic dispatch wearing a live label"* — apply, so the label is removed instead of the dispatch.

**The consequence, stated rather than mitigated:** phase-27 ships two limbs whose *trigger* is verified only in jsdom and whose *effect path* is verified live through a sibling limb. That is a coverage boundary, not a gate. `P27-C24` requires it in `docs/architecture.md` so the next person does not discover it the way P3 would have.

---

## 5. Scope

**IN:** `packages/descvi/src/vite/bootstrap-entry.ts`, a new factory module, and their gates.
**OUT:** `packages/descvi/src/react/DescviOverlay.tsx` (r0 moved it in only to enable 2B; reversed in r1), KI-33/KI-34, KI-31, the edit-map **fix** (its disclosure is IN — §3.2), a heartbeat (OQ-2), an interaction wake (1C), and **any change to `onWsConnect`**.

---

## 6. Contracts

**Design**

- **P27-C01** — New module `packages/descvi/src/react/overlay/engine/liveness-wake.ts` exports `createLivenessWakeSubscription(options): () => void`. Options: `onWake: () => void`; optional `minIntervalMs` (default `1000`); optional `now: () => number` (default `Date.now`). Its suite goes in `packages/descvi/src/react/overlay/__tests__/` — **the `engine/__tests__/` path r1 named does not exist** (jsdom still applies via `src/react/**`).
- **P27-C02** — Exactly three listeners: `visibilitychange` on `document`, `focus` and `online` on `window`. **One** unsubscribe removes all three (`P21-F30`; precedent `packages/descvi/src/vite/bootstrap-entry.ts#export function createManifestChannelSubscription(`).
- **P27-C03** — Run `onWake` only if `document.visibilityState === 'visible'`.
- **P27-C04** — Leading-edge throttle on `now()`: fire immediately, suppress until `now() - last >= minIntervalMs`. **Zero timers.**
- **P27-C04a** — **The `P27-C03` guard runs BEFORE the `P27-C04` stamp, and a guard-rejected event must not update `last`.** A real tab switch fires `visibilitychange`(hidden) on the way out; if that stamps, a return inside `minIntervalMs` is suppressed — the exact staleness this phase exists to end. Gated by `P27-G1.6`; `P27-G1.4` alone passes under both orderings.
- **P27-C05** — Must not read `document.hasFocus()` (E7).
- **P27-C06** — Throttle state is per subscription instance.
- **P27-C07** — `DescviBootstrap` creates the subscription **inside the existing fetch effect**; `onWake` dispatches `DESCVI_SESSION_REFRESH_EVENT` and calls the effect-local `load` from `packages/descvi/src/vite/bootstrap-entry.ts#const load = createLatestWinsLoader<ManifestMap>({`. **Same loader instance** — a fresh loader per wake gives every call ticket 1 and restores `P21-F22`. Unsubscribe joins the cleanup returning at `packages/descvi/src/vite/bootstrap-entry.ts#}, [manifestUrl, initialManifest, reloadKey]);`.
- **P27-C08** — Created **outside** the `getHot()` branch at `packages/descvi/src/vite/bootstrap-entry.ts#const unsubscribe = hot`.
- **P27-C09** — **`packages/descvi/src/react/DescviOverlay.tsx` is not modified.**
- **P27-C10** — `packages/descvi/src/vite/bootstrap-entry.ts#onWsConnect: () => window.dispatchEvent(new Event(DESCVI_SESSION_REFRESH_EVENT)),` is **byte-identical** before and after. Reason (E1): the callback fires once per document, so any repair there recovers nothing and costs one duplicate fetch per page load.

**Gate integrity**

- **P27-C11** — No wake gate row may pass `initialManifest` to `DescviBootstrap`.
- **P27-C12** — Component rows stub `fetch` ok with `{ "screens": [] }` and assert a **PER-URL delta**, naming the route. A global counter sums `/@descvi/manifest`, `/@descvi/edit-map` and the sidecar `/status`.
- **P27-C13** — **Rewritten in r2 (R2-7).** Every row is observed RED **by applying that row's own mutant from the §7 table to existing code**, and the runner output is pasted. ⚠ **A module-not-found is not a RED.** The factory does not exist on the pre-fix tree, so a pre-fix run of its suite fails once at import — which every row would "prove" equally. The mutant procedure is: land the module, then break one behaviour per row. (Asymmetry worth noting: `P27-C19`'s subject **does** exist pre-fix, so its RED is real without this ceremony.)
- **P27-C14** — `node scripts/check-citation-anchors.mjs` exits 0 on every commit. Counts are never quoted as a baseline (E13).
- **P27-C15** — The e2e spec restores everything it writes and must not mention the `claude/order-detail` route. Fixture: `e2e/fixtures/mutable-paths.json#src/app/shop/member-detail/spec.ts`, already declared.
- **P27-C16** — Golden procedure in this order (E20): **(1)** hand-edit `distribution` and say why; **(2)** run `pnpm test:e2e:update-identities`, which refuses on mismatch. Raw `TestResult.status` axis — cite `e2e/reporters/identity-oracle.ts#Reconciliation note: both lines above are this golden's RAW` rather than re-deriving.
- **P27-C17** — The spec joins a project's `testMatch` **in the commit that creates it**, with the `.spec.ts` extension (E21).
- **P27-C18** — **Rewritten in r2 (R2-10).** E2E acceptance is a **run-induced delta**, never "the tree is clean" (E19). **And the mutant RED and the green pass are TWO Playwright invocations**: mutant → observe RED → restore → green run. r1 claimed they could share one; that misread E19, which is about tree deltas, not about two implementations executing in one run. A row that times out under the mutant makes that whole invocation RED, so it cannot also be the green pass.
- **P27-C19** — **Re-grounded in r2 (E25, R2-5, R2-6).** r1 justified this as "there was no gate", which is false: E25's two committed rows already pin the dedup through mutation kinds. What C19 adds is (a) `refreshSidecarSession`'s **own** contract — the entry point 2A actually uses — and (b) **the half nothing pins: that dedup ENDS.** Two rows:
  - **C19a** — two *overlapping* forced `refreshSidecarSession` → exactly **1** `getStatus`. RED-when: move `packages/descvi/src/react/overlay/engine/session-coordinator.ts#if (handshake !== null) return handshake;` below the assignment, or delete it → 2.
  - **C19b** — two *sequential* forced refreshes (second issued after the first settles) → exactly **2** `getStatus`. RED-when: delete the clear inside `packages/descvi/src/react/overlay/engine/session-coordinator.ts#}).finally(() => {` → 1, and the session can never be re-adopted again while C19a stays green. This is the P-F half that was missing.
- **P27-C20** — **Narrowed in r2 (R2-9).** `e2e/undo-session-restart.spec.ts#// The focus listener attaches in a React effect after mount;` (collected by the **`solo`** project, E27) pins exactly one thing: **an isolated `focus` produces a `/status` GET.** ⚠ r1 claimed it *"would catch a future round consolidating the overlay's focus listener into the wake factory."* **False** — it dispatches `focus` once after mount with nothing before it to stamp the throttle, so under a leading-edge throttle the first focus passes and the spec stays green even under 2B. The unthrottled-ness contract is instead gated by **`P27-G6`** (§7 P3), which is the row that actually goes RED under 2B.
- **P27-C21** — **Extended in r2 (R2-13).** The KI-32 update must record the mechanism as **PARTIAL** for **two** distinct reasons, not one: (a) a socket dying silently while the tab holds focus with no network transition is not recovered; (b) **E26 — the edit-map is a separate holder the edit surface reads from, so a successful manifest wake can leave the manifest fresh and the editor stale.** OQ-3 becomes a **mandatory** entry in that update. The item must not read as though its defect were measured away.
- **P27-C22** — Doc updates get their own commit.
- **P27-C23** — **New in r2.** OQ-4 is recorded as **answered NO** (E22), not as open, wherever it appears.
- **P27-C24** — **New in r2 (§4.2).** `docs/architecture.md` must state the coverage boundary: the `online` limb is live-gated; the `visibilitychange`/`focus` limbs are **unit-gated only**, because real tab backgrounding fires neither event in this harness (E22).

---

## 7. Phases

### P0 — Observe the defect, with the spec actually collected

**Work.** Create `e2e/liveness-wake.spec.ts` and **add it to the `design-view` project's `testMatch` and complete `P27-C16` in the same commit** (`P27-C17`). Rows against the **pre-fix** code:

1. **Positive control.** Socket healthy; edit `src/app/shop/member-detail/spec.ts` → the manifest-derived observable changes within 5 s. E12 is why this fixture works.
2. **Defect + no-wake control, MERGED** (codex noted r1's rows 2 and 3 overlapped in discriminating power). `page.addInitScript` installs a `window.WebSocket` `Proxy`; `close(1000)` the HMR socket; assert no navigation (a `window` sentinel survives); edit the fixture again → the observable is unchanged at 5 s **and still unchanged at 10 s with no wake fired**. Two assertions, one setup, no redundant row. **The distinct populations they cover:** the 5 s assertion says *the publish was lost*; the 10 s assertion says *nothing other than a wake recovers it* — which is what makes `P27-G4a`'s green attributable rather than coincidental.
   ⚠ **The spec's doc comment must record that `close(1000)` induces a state KI-32 says this stack never produces** (a proxy/tunnel is required in reality), so the artificiality lives beside the code and not only in PM-1.
3. **Edit-map residual measurement (E26), conditional.** From the stale state, check whether the edit surface is also stale. **Decision rule, so this is not open-ended:** if it costs one assertion against an already-rendered edit surface, take it and record the result in OQ-3; if it needs its own edit round-trip, skip it and record OQ-3 as unmeasured. Either way OQ-3 goes into the KI-32 update (`P27-C21`).

**Gate `P27-G0` = the positive control. RED-when:** point the fixture edit at a file the extractor does not watch → row 1 stops observing a change.

**Acceptance.** Row 1 passes, row 2 holds on the pre-fix tree, output pasted. Spec collected (prove it: `--list` names it). Golden updated per `P27-C16`. The 5 s bound is **2× the measured recovery ceiling** (E2), not a round number. The observable is named in the spec's doc comment and proven by row 1.

### P1 — The factory, gated directly (seven rows)

**Work.** `P27-C01`–`P27-C06`. Suite at `packages/descvi/src/react/overlay/__tests__/liveness-wake.test.ts`.

| Row | Assertion | RED-when (per-row mutant, `P27-C13`) |
|---|---|---|
| `P27-G1.1` | dispatched `visibilitychange` → `onWake` once | drop the `document` registration → 0 |
| `P27-G1.2` | dispatched `focus` (clock past `minIntervalMs`) → once | drop the `window` `focus` registration → 0 |
| `P27-G1.3` | both inside one throttle window → exactly 1 | make the handler unconditional → 2 |
| `P27-G1.4` | `visibilityState` stubbed `'hidden'` (restored in `afterEach`) → 0 | remove the `P27-C03` guard → 1 |
| `P27-G1.5` | after unsubscribe, all three events → 0 | return a no-op unsubscribe → 3 |
| `P27-G1.6` | `visibilitychange` while hidden, then visible **inside one window** → exactly 1 | stamp before the guard (`P27-C04a` violated) → 0. **The only row separating the two orderings.** |
| `P27-G1.7` | dispatched `online` → once | drop the `online` registration → 0. Converts E18 PROBE → RUN **for delivery only**; it does not restore the coverage claim R2-11 retracted. |

**Moved out (R2-8):** r1's `G1.8` latest-wins row cannot live here — the factory owns no loader, so a factory-level row would test a loader the test built. It becomes `P27-G2.2`.

**Acceptance.** Seven rows green, seven observed RED by their own mutants. `pnpm typecheck` (all three legs) and `pnpm lint` clean at the **root** scripts.

### P2 — Wire the one consumer, and gate the ungated halves

- **`P27-G2.1` — component-level.** Render `DescviBootstrap` **without** `initialManifest` (`P27-C11`), `fetch` stubbed ok (`P27-C12`); await mount; dispatch `visibilitychange`; assert the **`/@descvi/manifest` per-URL delta is exactly 1**. RED-when: remove the `P27-C08` subscription → 0. Already replicated by `arch-r1`.
- **`P27-G2.2` — latest-wins across a wake** (moved from P1 per R2-8). Control the initial fetch **A** and the wake fetch **B**; **resolve B first, then A**; assert B's manifest is retained. Needs **`now()` injection** to cross the throttle — state it in the test. RED-when: build a fresh loader inside `onWake` → both get ticket 1 and the later-settling A wins. **This is R1's mechanism**; the failure it names compiles fine, so only a row detects it.
- **`P27-G2.3` / `P27-G2.4` — `P27-C19a` and `P27-C19b`.** RED-whens as stated in the contract.
- **No overlay component row** (E17).

**Acceptance.** All four green and observed RED. Full suite green **both ways** (`pnpm -r --filter './packages/**' test` and repo-root `npx vitest run`). `git diff --exit-code .descvi/screens.json` clean after re-running the extractor.

### P3 — The live gate, split by what can actually be triggered

- **`P27-G4a` — FULLY LIVE.** From P0 row 2's stale state, `context.setOffline(true)` then `(false)` (E23: real `online`, socket undisturbed at `readyState 1`, so the stale state survives the trigger) → the observable updates within 5 s.
  **RED-when:** revert `P27-C07`'s subscription, run, observe `P27-G4a` time out while P0 rows pass; restore; **run again for the green** (`P27-C18` — two invocations, not one).
- **`P27-G4b` — SYNTHETIC, and labelled so.** `page.evaluate` dispatching `visibilitychange` and `focus` → the observable updates. **This is evidence of attachment and wiring, not of live triggering** (E22). The spec's doc comment must say so in those terms; §4.2 is the reason.
- **`P27-G6` — the unthrottled-focus contract `P27-C20` cannot pin.** Immediately after `P27-G4a`'s `online` wake, dispatch `focus` **inside `minIntervalMs`** and expect a **second** `/status` GET. Under 2A the overlay's raw listener is unthrottled and issues it; **RED-when:** implement 2B (route the overlay's focus through the throttled factory) → the second GET never arrives. This is the row r1 wrongly believed E16's spec already provided.

**Acceptance.** `pnpm test:e2e` green. Stated as a **run-induced delta** — this run restored every path it touched — never "the tree is clean" (`P27-C18`, E19). Golden bumped in the `P27-C16` order. E16's `solo` spec green **unmodified** (E27).

### P4 — Documentation and the whole-set audit

`P27-C21` (PARTIAL for **both** reasons, OQ-3 mandatory), `P27-C22`, `P27-C23` (OQ-4 = NO), `P27-C24` (the §4.2 coverage boundary). Update KI-32, `docs/architecture.md`, `docs/post-loop-backlog.md`. Append OQ-1..4 to `.omc/plans/open-questions.md`.

**Gate `P27-G5`.** Citation gate exits 0; the audit re-reads `P27-C10`'s anchor for byte-identity; every fact carried into `docs/` keeps its §0 tier. **RED-when:** introduce a wrong anchor in the KI-32 edit → leg (b) violation, non-zero exit.

---

## 8. Risks

| # | Risk | Mechanism |
|---|---|---|
| R1 | The wake reintroduces `P21-F22` by building a fresh loader inside `onWake` — which **compiles fine**. | **`P27-G2.2`** (moved to P2 per R2-8, because a factory-level version would have been vacuous). |
| R2 | Listeners added, not all removed — `P21-F30`. | `P27-C02` + `P27-G1.5`, which counts all three. |
| R4 | Focus and visibility both fire on one return → two fetches. | `P27-C04` + `P27-G1.3` (exactly 1). |
| R5 | Component gate vacuous via the `initialManifest` seam. | `P27-C11` + `P27-G2.1`'s observed RED. |
| R6 | Component gate vacuous via fetch-count inflation across three routes. | `P27-C12` — per-URL delta. |
| R7 | `onWsConnect` gets "fixed" in passing. | `P27-C10` cites that line as a citation-gate **anchor**; leg (b) proves the text occurs exactly once, and `P27-C14` runs the gate every commit. Change the line, the gate goes RED naming this plan. |
| R8 | The e2e addition reddens the suite through the identity oracle rather than the subject. | `P27-C16` names the order, the axis and the reconciliation source. |
| R10 | The live observable does not exist and P3 degrades to asserting a network request. | P0 row 1 must change the observable **before** any fix exists; if it cannot, P0 fails and the plan re-opens. E12 is READ, so this is live. |
| R11 | 2A leans on E14, in a file this phase does not touch. | `P27-C19a`/`b`. ⚠ Re-grounded: E25 shows dedup was **already** partly gated, so C19's value is `refreshSidecarSession`'s own entry point plus **the clear**, which nothing pinned. |
| R12 | `online` fires on transitions irrelevant to a loopback socket. | Bounded by `P27-C04` and by the route being loopback; cost equals one tab return, which the design already accepts. |
| **R13** | **New in r2 (§4.2).** Two of three limbs ship with no live trigger, so a Chromium-specific failure in exactly those limbs is invisible to CI forever. | **Not mitigated — disclosed.** `P27-C24` puts the boundary in `docs/architecture.md`; `P27-G4b` is labelled synthetic; `P27-G4a` covers the shared handler/guard/throttle/loader path live through the `online` limb, so what is unverified is narrowed to *trigger delivery* rather than the whole mechanism. |
| **R14** | **New in r2 (E26).** A green `P27-G4a` reads as "recovered" while the editor is still stale, and the phase gets remembered as a full fix. | `P27-C21` requires PARTIAL for both reasons and makes OQ-3 mandatory in the KI-32 update; P0 row 3 measures it if it is one assertion. |

*(R3 and R9 were closed in r1 — the overlay left scope, and `arch-r1` ran E5–E7 in the real runner.)*

---

## 9. Pre-mortem

**PM-1 — "It shipped, it is green, and nobody was ever stale."** OQ-1 resolves against us: ② cannot occur on loopback, ① needs a proxy, no user runs one.
*Early warning:* P0 row 2 needs an artificial `close(1000)` to produce staleness at all — now recorded in the spec's own doc comment, not just here.
*Hedge:* P4 records OQ-1 in KI-32 so the doubt is inherited. 1D stays cheap enough that a zero-population outcome is a small loss.

**PM-2 — "Green the whole time, and two of the three limbs never fired in a real browser."** ⚠ **This is no longer a hypothetical; E22 measured its precondition.** It is now R13, disclosed rather than hedged.
*Early warning:* none available — that is the point of §4.2.
*Hedge:* `P27-G4a` narrows what is unverified to trigger delivery; `P27-C24` writes the boundary down.

**PM-3 — a future round consolidates the overlay's focus listener into the factory, re-entering 2B without re-arguing it.** ⚠ r1 claimed E16's committed spec would catch this. **False** (R2-9): that spec dispatches one focus after mount with nothing to stamp the throttle, so it stays green under 2B.
*Early warning:* **`P27-G6`**, which is the row that actually goes RED under 2B. r1's protection was a phantom; this one is measured against a stated mutant.
*Hedge:* §3.2's table keeps 2B's cons intact where the next reader will look.

---

## 10. Test plan

**Unit** (`packages/descvi/src/react/overlay/__tests__/liveness-wake.test.ts`, jsdom via `packages/descvi/vitest.config.ts#['src/react/**', 'jsdom'],`): `P27-G1.1`–`P27-G1.7`.
**Unit, invariant** (existing session-coordinator suite): `P27-C19a`/`b`.
**Component** (jsdom + RTL): `P27-G2.1` per-URL manifest delta, `P27-G2.2` latest-wins across a wake. No overlay row (E17).
**E2E** (`design-view`): `P27-G0`, P0 row 2, `P27-G4a` (live), `P27-G4b` (synthetic, labelled), `P27-G6`. Plus E16's `solo` spec green unmodified.

**Observability.** No new logging by default. The wake is observable as a `/@descvi/manifest` request per tab return; `docs/architecture.md` states that as the by-hand confirmation alongside `P27-C24`'s boundary. A single `console.debug` behind an existing debug flag is the smallest alternative — named so it is a decision, not a drive-by.

**Cross-invocation.** Suite both ways at P2 and P3. All three `pnpm typecheck` legs every phase. CI green on the branch before merge (`gh run list --branch feat/phase-27-ki32-liveness`).

---

## 11. ADR

**Decision.** Add a client-side liveness wake — `visibilitychange`→visible, `window` `focus`, `window` `online` — visibility-guarded then leading-edge throttled, **zero timers**, as one exported factory consumed by **`DescviBootstrap` only**: `onWake` dispatches `DESCVI_SESSION_REFRESH_EVENT` (already consumed by the overlay) and calls the effect-local latest-wins loader. `DescviOverlay` and `onWsConnect` untouched. The ungated halves of the session single-flight are pinned. Heartbeat, interaction wake and the edit-map **fix** are deferred; the edit-map **residual is disclosed**.

**Drivers.** D1; D2, now split into unit-gateable vs live-gateable (§4.2); D3. Plus P-F as re-grounded.

**Alternatives considered.**
- *`load()` on `onWsConnect`* — invalidated by measurement (E1). KI-32 records this repair authored once and stopped at the last moment, which is why `P27-C10` is a contract.
- *2B, shared factory across bootstrap and overlay* (r0's choice, reversed r1) — its justification was a phantom cost (E14/E24); it widens scope, needs an un-implementable row (E17), and E16's spec would not even have caught its regression (R2-9).
- *2C, no session dispatch* — the honest competitor to 2A; rejected for a coverage hole on the visibility path to save one existing dispatch.
- *1B heartbeat* — deferred on D1/P-E, secondarily on P-D's priority clause. ⚠ Weakened in r2: with `online`'s coverage claim retracted, the residual population is larger than r1 implied, so OQ-2 is more live.
- *1C interaction wake* — deferred.
- *1E, `online` alone* (new in r2, `[PLANNER DISSENT]`) — rejected: it lets gate convenience select the shipped population and would ship the one limb whose coverage was just retracted, while the dominant workflow stays broken.
- *A WebSocket relay as the live instrument* — rejected: needs a WS-aware intermediary to emit a real close frame; the in-page `WebSocket` `Proxy` reproduces the same client-visible state far cheaper and is the instrument KI-32 already used.

**Why chosen.** It covers both stale paths an event can reach, at no always-on state, with every unit gate carrying an observed per-row RED and the shared effect path verified live through the one limb that has a browser-generated trigger.

**Consequences.**
- **PARTIAL for two reasons, and KI-32 must say both:** the focused-tab silent death with no network transition is not recovered; and **the edit-map is a separate holder the edit surface reads from (E26), so a green manifest wake can leave the editor stale.**
- **Two of three limbs are unit-gated only** (E22) — a disclosed coverage boundary (§4.2, R13, `P27-C24`), not a mitigated risk.
- At most one extra read-only `/status` GET per wake window (§3.2 dissent).
- One more spec in a `workers: 1` suite, plus a hand-maintained golden field.

**Follow-ups.** OQ-1 gates OQ-2 and gates whether this phase mattered. OQ-3 is now mandatory in the KI-32 record. OQ-4 is closed NO.

---

## 12. Open questions

Also appended to `.omc/plans/open-questions.md`.

- **OQ-1 — Can a *loopback* socket go half-open at all?** KI-32 attaches the "needs an intermediary" caveat to ① and not ②, and this lane cannot tell whether that was measured. *Why it matters:* if ② is also intermediary-gated, both stale paths are exposure-gated and this phase's value is conditional on deployments nobody here can count.
- **OQ-2 — Does a socket die silently while the tab holds focus, in a real session?** *Why it matters:* the entire remaining justification for 1B/1C. **More live after r2**, because `online`'s coverage claim was retracted (R2-11) and no longer narrows this population by a measured amount.
- **OQ-3 — Does the edit-map go stale alongside the manifest, and does the user see it?** E26 says the edit surface reads from a separately-held edit-map, so a green manifest wake can leave the editor stale. **Promoted in r2 to a mandatory entry in the KI-32 update** (`P27-C21`); P0 row 3 measures it if it costs one assertion.
- **OQ-4 — ANSWERED NO.** Real tab backgrounding fires no `visibilitychange`, `focus` or `blur` in this harness; `CDP Emulation.setPageVisibility` is absent in this build (E22, 12 iterations, headless and headed, passing control). Recorded as closed per `P27-C23`; the consequence is §4.2 and R13, not a further question.

