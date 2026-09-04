# Forced-choice comparison — plan-A vs plan-B (phase-49)

Reading order: `plan-B.md` in full, then `plan-A.md` in full. Kickoff: `base/docs/handoff/260903-phase-49-kickoff.md`.

| Dimension | Winner | Confidence |
|---|---|---|
| 1. Scope fidelity | A | medium |
| 2. Decision completeness | A | medium |
| 3. Executability | A | medium |
| 4. Gate proportionality | B | high |
| 5. Handoff readability | B | high |
| **Overall** | **A** | **medium** |

## 1. Scope fidelity — A

**For A.** The kickoff's S0 (kickoff:22) inherits the repository's own archiving convention, and only A applies it. `base/docs/README.md:57` states that `docs/handoff/*` and archived plans under `.omc/archive/` "are point-in-time records and are deliberately **not** rewritten". A's D49-4 census excludes exactly those namespaces and publishes the live set as 11 pointers across 6 files (plan-A:213-222), with the exclusion argued rather than assumed and narrowed at `.omc/archive/README.md` because an index is not a record (plan-A:181). I reproduced A's table on `base/`: `docs/e3/tracker.md` 5, `.omc/archive/README.md` 2, `docs/architecture.md` 1, `docs/known-issues.md` 1, `.omc/research/phase48-strip-band-pricing.md` 1, `.omc/plans/ralplan-phase-46-ring-furniture-restyle.md` 1 — file for file.

Second, A handles `padding-glyph` as the kickoff records it. The kickoff states the direction as already given — "the pad strip's arrow-up-to-line → a plain directional bar" (kickoff:35) — and A's S49-5 treats it as confirmation, with the deferral default set to **execute the change**, naming the reason: "treating silence as 'keep the arrow' would reverse an owner input" (plan-A:500).

**Against A.** The kickoff's process ruling is that "**codex is excluded by the owner's standing ruling of 2026-09-02** — consensus is the Claude lanes' alone" (kickoff:51). A ran codex in every review round (plan-A:9) and asserts the owner reversed the exclusion on 2026-09-04, adding that "the lead has corrected the kickoff doc" (plan-A:10). The base kickoff still carries the exclusion, so the deviation rests on a claim not visible in the inputs, and it involves editing the document the kickoff itself calls the owner's scope-ruling record (kickoff:3). B's lanes (plan-B:3, architect + critic) match the kickoff as written.

**Against B, decisively.** B's S49-0 done-when requires "The two old paths have zero references across the tracked tree AND the non-ignored working tree, including `.omc/plans` and `.omc/archive`" (plan-B:232), and its §2.5 sizes the work at "90 occurrences across 47 tracked files" (plan-B:103). Measured on `base/`, that figure is right and 41 of those 47 files are under `.omc/archive/` — mostly `.omc/archive/260818-phase-42-consensus/**`, the phase-42 consensus round records. B's completion condition therefore orders the rewrite of point-in-time records that `base/docs/README.md:57` forbids rewriting; B never cites that convention anywhere (grep for "point-in-time", "frozen", "not rewritten" over `plan-B.md` returns nothing). B also reopens `padding-glyph` as a choice — "Owner live ruling between the current arrow-to-line and a directional bar" (plan-B:47), and U49-5 asks "Should padding use the plain directional bar" (plan-B:516) — where the kickoff records the direction as already received.

## 2. Decision completeness — A

**For A.** A closes the mechanism questions its own chosen form creates. The candidate-switch channel is named down to the key and its guard: `[` / `]` bare, ruled after enumerating every keydown owner in the overlay (plan-A:278), with the text-entry guard specified as a copied line (plan-A:284) and a decided fallback to `F2`/`F3` if the IME kills the channel (plan-A:288). It also names the ambient-declaration problem before an executor meets it: `import.meta.env.DEV` is untyped in the package and the fix is `readonly DEV: boolean` on the existing interface, not `vite/client` (plan-A:403). Where A cannot decide, it labels: U49-A/B/C are answered on the plan (plan-A:1104-1116), the mid-phase table has a `Defer?` column per row (plan-A:1122-1131), and §11's register lists each unverified claim with the instrument that would settle it (plan-A:1216-1232).

**Against A.** S49-4's reveal half is left partly to the executor: "Grep the e2e for the strip and apron roles before writing the lands list" (plan-A:486) is a research instruction inside a story rather than a decision.

**Against B.** B chooses form (b) — runtime controls in overlay chrome (plan-B:28) — and never asks what A's D49-1 second reason asks: reaching for a control moves the pointer, and three of the four subjects exist only under a live pointer or an in-flight drag. B's C49-3 requires the owner to judge the reorder indicator "during the live gesture" (plan-B:144) and the hover-versus-selection relation (plan-B:145), while S49-1's only interaction requirement is that the panel "is keyboard reachable" (plan-B:244) — reachability, not a mid-gesture switch channel. Whether the instrument can show its own subject is a material architecture question B leaves unasked, not parked.

## 3. Executability — A

**For A.** Every story closes without the owner. C49-6 states it — "Owner deferral changes what value ships, never whether the story lands" (plan-A:294) — and every table row carries a shipped default that is one of the offered candidates (plan-A:166), so a deferral costs a row rather than the phase (plan-A:39). A worker who starts S49-2 can finish it.

Second, A's RED-when is per field and per direction, which is what a worker actually needs: raising the reorder thickness is RED, lowering it to 1 is GREEN because the bound is one-sided, and the run reports one failing test rather than three because all three assertions sit in one `it()` (plan-A:825-834, measured at plan-A:745). A worker who mutates in the wrong direction and sees green would otherwise conclude the look is ungated.

**Against A.** S49-1 is oversized for one round: the override reader, per-family records, wiring across four painter modules, the keyboard tick channel with its guard, the spatial A/B by pool-key indexing, a new gate script with CI wiring, plus the widened witness list (plan-A:395-425).

**Against B.** S49-2 through S49-5 and S49-R each contain an owner live checkpoint inside the story — "S49-2 through S49-R deliberately contain later live-decision checkpoints whose answers must be recorded before any shipped default moves" (plan-B:3) — with `Dependencies: S49-1 and owner availability for the live pass` (plan-B:268). Four of B's seven stories cannot be finished without stopping to ask. B also makes a completion condition depend on a census result rather than fixing it at plan time: "G42-7 Universe B's leg is conditional on EG49-5 and is written the way that census came back" (plan-B:300).

## 4. Gate proportionality — B

**For B.** B's gate section is `## 5. Gates and verification` at plan-B:334-349 — a 14-row table, ~16 lines — plus Evidence Gates at plan-B:351-399, ~50 lines. Roughly 66 lines govern a LARGE surface story, a new validator, contract moves across five hand-written closed sets and four promotions. Each row carries a named RED-when and a failure action.

Second, G49-1's two-oracle split is a gate sized exactly to a real hazard: O1 holds pre-phase expectations and expires at the first promotion, O2 is rewritten per promotion carrying the authorising record entry, and each has its own RED — "restore that family's pre-phase value in `SHIPPED_OVERLAY_PROFILE`; the promoted family's row must fail — a rewrite that left the old value acceptable proves the oracle stopped asserting anything" (plan-B:339). That is a gate that can fail for a named reason on a thing the stories actually change.

**Against B.** B's gates are specified, not demonstrated: no RED has been staged for G49-0, G49-2, G49-3 or G49-5, so their falsifiability is a claim.

**Against A.** A's §6 runs plan-A:515-1096 — about 580 lines, roughly 47% of the plan — to guard a two-file `git mv` with 11 pointer rewrites, a four-field constants refactor, and one string literal. G49-2's demonstration transcripts alone occupy plan-A:585-706, ~120 lines, for the move. G49-4 occupies plan-A:837-975, ~140 lines, to prove one literal is absent from two bundles, and it charges every local run: "from S49-1's commit onward every local gate run gains two full Vite builds… measured at r4' at **4.80 s and 4.66 s**" (plan-A:421). G49-5 covers five fields (plan-A:991-997) at the cost of a whole committed script with a ten-plant selftest (plan-A:1024-1053). Each gate is falsifiable and each guards something a story changes; several are larger than what they guard.

## 5. Handoff readability — B

**For B.** Every story uses one shape — Purpose, Affected locations, Required behavior, Dependencies, Done when, Stop/failure behavior (plan-B:199-236 and repeated through 320-332) — so finding what to do for one story is one section. S49-4's Affected locations (plan-B:292) enumerates every file and every gate leg by anchor, so the worker does not assemble the list from three other sections.

Second, B is 517 lines against A's 1232 for the same phase, and B's reviewer-addressed text is confined to the status paragraph (plan-B:3).

**Against B.** C49-4 (plan-B:152-195) restates in prose what S49-4 (plan-B:288-304) then restates again and the pre-mortem S3 (plan-B:417-422) restates a third time; the delegated-mark disposition is readable only by holding all three in mind.

**Against A.** A's first 39 lines are addressed to a reviewer, not a worker — "A reviewer should read these first" (plan-A:25) introduces twelve revision reversals — and revision archaeology (r0/r1'/r2'/r3'/r4'/r5) runs through every section. Worse for a worker: the four field spellings that S49-1a must produce are contract, but they are stated in the story (plan-A:366) and enforced from a gate table 630 lines later (plan-A:991-999), with the plan itself noting an executor who nests them "satisfies the contract, moves no pixel, passes every witness, and leaves the gate permanently at `homes=0`". Finding one story's work requires the story, two or three contracts, and two gate tables.

## Overall — A, medium confidence

A wins on the three dimensions that decide whether the phase lands as the owner ruled it: it obeys the archiving convention the kickoff's S0 inherits, it closes the mechanism decisions its own form choice creates, and every story completes without waiting on the owner. B's S49-0 completion condition (plan-B:232) would send a worker into 41 archived files that `base/docs/README.md:57` forbids editing, and four of B's seven stories stop mid-story for an owner session.

The cost of choosing A is real and should be stated: 1232 lines, ~580 of them gates, and two extra Vite builds on every local `pnpm gates` run from S49-1 onward.

**What B does better that A should take.** B's story ladder — one fixed shape per story, with Affected locations enumerating every file and gate leg by anchor, and Done when / Stop-failure as separate fields — makes one story's work findable in one section, which A's cross-referenced arrangement does not. A should adopt that shape wholesale and, with it, B's gate economy: B governs a larger contract surface in ~66 lines by writing each gate as a claim, a RED-when, a command and a failure action, keeping the demonstration transcripts out of the plan. A's transcripts prove its gates can fail — that evidence is worth keeping — but it belongs beside the committed scripts, not in the document a worker reads to find their next task. A should also take B's EG-style evidence gates: a bounded, named observation with a pass path, an alternate path and a stated unexpected-result branch is a better home for A's §11 register entries than a table of claims annotated with what would settle them.

## Framing

Sentences that tell the reader how to weigh or feel rather than stating a fact or an instruction to act.

### plan-A

- **plan-A:23** — "Three of the four are RED on the tree right now and every one of those REDs is the gate working. A gate that were GREEN today would be a gate with no subject." Instructs the reader how to read a failure before the reader has seen it.
- **plan-A:25** — "A reviewer should read these first, because each is a place where the input and the tree disagreed and the tree won." Addressed to a reviewer, and frames the plan's revisions as vindication.
- **plan-A:508** — "A conclusion that survives its own reason being wrong is the most expensive kind of correct there is, and a claim that the duplication is gone while it is still there is worse than the duplication." An aphorism doing the work of the measurement it sits beside.
- **plan-A:803** — "**That GREEN is the finding.**" Tells the reader what to conclude from an output printed three lines above.
- **plan-A:1074** — "The elided rows are the point, not a saving: they are all `ok`." Pre-empts the reader's reading of an elision.

### plan-B

- **plan-B:11** — "**Compare the mechanism that actually paints.** A facsimile is not evidence about imperative furniture." A principle hoisted above the D49-1 option table it decides, so the option arrives already judged.
- **plan-B:12** — "**The shipped default is a gate subject, not a convenient preset.**" The adjective "convenient" carries the argument against the alternative.
- **plan-B:36** — "The price is a small permanent comparison control in the existing toolbar and sequential A/B viewing, which is lower risk than preserving a second renderer." "Small" and "lower risk" are asserted comparatives, not measurements; the option they dismiss is not the one on the table.
- **plan-B:217** — "Naming it is what keeps it from being coverage loss wearing a cleanup label." Tells the reader how to feel about an accounting entry rather than what the entry obliges.
- **plan-B:466** — "The runtime surface is the only option that compares the actual painter with live geometry and theme while avoiding a second renderer and a new screen." "Only option" is a rubric ending inside the ADR's Why Chosen, restating the ruling rather than evidencing it.
