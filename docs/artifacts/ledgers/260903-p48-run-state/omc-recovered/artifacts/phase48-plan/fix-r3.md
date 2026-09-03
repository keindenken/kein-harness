# S48-5 — the owner's live-pass ruling: CLIP EVERYWHERE (D48-7 → (i)); the chip sits on the vertex

Read `docs/prompt/worker-brief.md`; it binds you (no git; restore by `cp`; assert each edit applied once; report reversals loudly). The tree is CLEAN at `294add7`; the descvi:dev server on :3001/:7331 is the LEAD's (started for the owner's smoke) — do not kill it; do not start another sidecar.

**The ruling (owner, 2026-09-02, after G48-8):** the corner chip must sit exactly on each vertex, everywhere. D48-7's ruled option (iii) kept the renderer sandwich (clamp into the clip rect → `pushOutOfArcs` → clamp) for corner roots; its FIRST clamp translates a corner root inward at a straight flush edge, so the chip leaves the vertex — the very thing the owner's 2026-08-27 「밀지 말고 잘라라」 ruling forbade, which the plan claimed (iii) honoured and did not. **Now ruled: option (i) — the pure model is what renders; corner roots are never translated; the ring layer's `overflow-hidden` clips whatever hangs outside; at a rounded frame corner the corner handle is known-unreachable by ruling (purchase 0.86).**

## H1 — production (OWNER: S48-1 lane) — `use-resize-handles.ts` only

- `placementFor` returns the region rect for corners exactly as it does for strips: delete the corner branch's sandwich. `translateIntoRect`, `pushOutOfArcs`, `cornerInArcQuadrant` (and any helper that existed only for them) become dead in the renderer — **delete them** (AGENTS.md reason 1 in the report: the code they served is gone by ruling). `fitsInClip` in `handle-geometry.ts` stays (G48-5's containment leg uses it? — check its callers; if it has none left, say so and leave it: it is §3.10 KEEP).
- Docblocks: the D48-7(iii) explanation becomes the (i) ruling with its date and reason; §3.7's cost sentence ("rendered box and derived box differ at arcs") is now false — replace with "rendered == derived everywhere; nothing is rescued".
- `pnpm typecheck`, `pnpm lint`, citation gate (anchors into the deleted helpers — the plan's §3.10 rows name `translateIntoRect` and `pushOutOfArcs` as MOVED; the lead re-points those), your port-conformance probe unchanged (the pure model did not move). Report exact lines. No e2e, no vitest beyond `resize-handle-layer.test.tsx` if a row there asserted the clamp (check; if one does, report it — S48-2's file is not yours).

## H2 — e2e (OWNER: S48-3 lane, AFTER H1 lands) — `e2e/resize-handles.spec.ts`, `e2e/resize-handle-shield.spec.ts` if affected

- G48-5's flush rows: rendered now equals the pure model, so the recorded two-sided intervals are the pure model's T6 values (23×100 flush left 2.09 etc.); re-record from the rendered rects and confirm they equal T6 to the bracket; the "rescue may only restore" history stays as prose.
- The rounded-corner fixture: the `nw` root is clipped; its row asserts **known-unreachable by ruling** — the witness press is skipped with that reason and the emptiness/containment legs still run. U48-11's table collapses to identity: print it once more and report.
- Clause 2 (containment) rows: a corner root now legitimately hangs outside the effective clip by up to half its side (like a strip); re-scope 2a exactly as 2b was scoped for strips ("outside by at most its own half"); RED-when stays (a root wholly outside → fires).
- Scoped runs: `npx playwright test e2e/resize-handles.spec.ts --project=design-view`, then the other three resize/spacing specs scoped; then ONE full `pnpm test:e2e` over the quiesced tree; regenerate the golden if any title changed (traced diff). Ports: the lead's descvi:dev holds :3001/:7331 — Playwright's own servers will collide; tell the lead in your report BEFORE running the full suite if you need the ports freed, or run scoped against the lead's live server if the config allows a `baseURL`. Do not kill the lead's server.

## H3 — plan / backlog / record (OWNER: the lead)

D48-7 → (i) RULED by the owner after the live pass; U48-7 moot; U48-11 → identity; §3.10 rows for `translateIntoRect` / `pushOutOfArcs` → delete; backlog row for the padding-handle glyph (arrow-up-to-line → a plain bar); the handoff record's §2.
