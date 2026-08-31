# `kein:execute` — the phase-47 run, and what it says about the harness

**Run:** `260829-091832-phase-47-s3-s5`, worktree `phase-47-drag-reorder-in-kein`, executor lane `claude`.
**Subject:** descvi phase-47 (drag-to-reorder), stories S47-1 → S47-3 landed, S47-4/S47-5 pending.
**Written:** 2026-08-29, by the lead session that ran it.

**Provenance, because this document is partly about evidence discipline.** The timeline and the commit record are read from disk (`.agents/kein/reports/` mtimes, `git log`). **Per-lane wall-clock durations are from run metadata held in the lead session's context — the lane transcripts under `/tmp` have since been cleaned and cannot be re-read.** Where a number comes from that second source it is marked *(session metadata)*. That distinction is not pedantry here: the single most expensive process defect this run found was evidence that existed only in one session's context.

A sibling record exists for the codex-executor attempt at `260828-kein-p47-execute-codex.md` (currently empty).

---

## 1. What ran

| | |
|---|---|
| Stories landed | S47-1 (`7797771`), S47-2 (`4ac1dec`), S47-3 (`7e96964`) |
| Correction rounds on S47-3 | **6** |
| Blind review lanes on S47-3 | **10** (5 × code-reviewer, 5 × test-engineer) |
| Other lanes on S47-3 | 7 executor runs, 1 verifier, 1 qa-tester (Evidence Gate EG-1) |
| Final state | `pnpm gates` 13/13, `pnpm test:e2e` 206 passed / 13 skipped, artifact byte-identical |
| Still owed | the owner's live pass (sheet assembled), S47-4, S47-5 |

**S47-3 alone consumed 19 agent runs over 11 hours 10 minutes of wall clock** (first report 10:17, commit 21:31).

---

## 2. Pacing — the question that prompted this document

Round completion times, from report mtimes on disk:

| Round | Ended | Gap | Outcome |
|---|---|---|---|
| R1 implementation | 10:17 | — | |
| R2 correction | 14:36 | 4h19m | DR47-5 shipped as a paint-only override; acceptance 52 could not go RED |
| R3 | 15:59 | 1h23m | cursor read in the bubble phase behind a capture-fed tracker |
| R4 | 17:19 | 1h20m | acceptance 31's ink leg could not go RED; first-slot position ungated |
| R5 | 18:38 | 1h19m | **destructive**: the drain deleted the author's page subtree |
| R6 (tidy) | 20:43 | **2h05m** | three gates over unwatched lifetimes; **no production change** |
| EG-1 | 20:58 | (concurrent) | pass path, no STOP |
| Final verification | 21:27 | 44m | 59's three legs jointly RED; live smoke |

**R3–R5 are strikingly regular at ~1h20m each. R6's window is 2h05m, and the cost is not in the fix.** *(session metadata)* the blind gate audit preceding it ran **~70 min** and the tidy round itself **~45 min**, roughly serial — which accounts for the window almost exactly.

**Why that audit was slow, and why it was worth it.** It rebuilt `node_modules` in its scratch copy as a real directory of per-entry links (with `.bin` **copied**, not linked, because pnpm's bin shims resolve `$basedir/../<pkg>`), then proved the rig could discriminate before trusting it, then drove 20+ mutations each requiring a full Playwright run. It did this because **the previous round's audit had symlinked `node_modules` wholesale, which re-resolved pnpm's relative `descvi -> ../packages/descvi` link back to the original unmutated package** — so its mutations did nothing and it reported a false "non-discriminating" verdict on a real gate.

**The longest lane in the story produced the fewest changes and the most trustworthy measurements.** R6 changed no production behaviour. It measured the right-button chord (a blue line paints on a gesture begun with the right button), found the effect-cleanup lifetime ungated, and — by *stating how it built its rig* — retro-explained a contradiction two earlier lanes had left standing.

---

## 3. What the method caught, and when

**Severity peaked at round 4, not round 1.** The most serious defect — clause 4's drain resolving `#dsh-reorder-layer` document-wide, so a prototype page carrying that id won the lookup and `replaceChildren()` **deleted the author's subtree on every stage press** — was found by the *fifth* blind lane. The round immediately before it had fixed the identical hazard at the child ids, argued the divergence in a docblock, and shipped an e2e decoy gate for it. The parent id, the one with `replaceChildren()` behind it, was missed.

That is the argument for per-round blind review stated as a measurement rather than a principle: **a review that had stopped after round 3 would have shipped a page-destroying write in a story whose whole contract is "paint only, no write".**

### The dominant defect class

**Four of the five defects were gates that passed for a reason other than the code under test:**

| Gate | What actually satisfied it |
|---|---|
| `pointer-events: none` on the paint layer | inherited from the parent `#dsh-ring-layer` — deleting the declaration moved nothing |
| acceptance 52's "the paint is drained" | the paint hook's own RAF `tick() → clearAll()` restored the asserted state inside the test's wait |
| acceptance 31's "the accent is the ink" | the dogfood app's `@layer base` rule on `*`, from `src/app/globals.css` |
| a whole audit pass | the measurement rig's own symlink resolution |

**Every one was invisible to reading and visible to a mutation in under a minute.** Two independent lanes proposed *wrong mechanisms* for the third (a CSS initial value; Tailwind's preflight) before a third lane read the actual stylesheet.

The rule this suggests, for any harness that reviews gates: **an assertion that compares a property to a value the platform, a framework, an ancestor, or the test rig would produce anyway is not a gate.** Reviewing cannot find these. Only mutating can.

---

## 4. Findings about the harness itself

### 4.1 Blind-lane results live only in the lead's context — and it cost a false verdict

Ten blind lanes returned their verdicts **as task results to the lead session, not to files.** A verification lane later audited S47-3's completeness, could read only `.agents/kein/reports/` (the executor's own reports), and consequently flagged acceptances 50 and 59 as un-driven since round 1 — **when a blind audit had driven both on the current tree two rounds earlier.**

The verdict was wrong for a structural reason, not a careless one: the evidence was not on disk.

**Recommendation:** `kein:execute` should write each review lane's returned text to the run directory the moment it lands, exactly as the RALPLAN retention rule already requires for planning rounds. This run's lead wrote them retrospectively (`<run>/review-lanes/S47-3-blind-lanes.md`) after the cost had already been paid.

### 4.2 Input-identity freezing and plan amendment collide by construction

**Three execute runs were retired** because the plan was amended while a run was open, which moves `input.sha256`, and a run may not change input identity.

Both rules are individually right. But the repository's own governing rule is *"if reality forces a deviation, update the plan in the same change"* — and building against a plan is the activity most likely to falsify it. **In this run, building S47-3 falsified the plan in twelve places**, including a ruling (`§3.7`'s "reuse the shipped string") that had *caused* a user-facing defect.

So the two rules guarantee a collision whenever the work is going well. Options, in preference order:

1. Bind the run to a hash that **excludes** doc-only regions (citation lines, correction notes) — narrow, but most amendments in this run were exactly that.
2. An explicit `--input-changed <reason>` checkpoint that records the amendment rather than retiring the run.
3. Status quo, with the retirement documented as expected rather than exceptional.

### 4.3 Read-only lane boundaries were crossed twice

A lane ran `git add` despite a brief binding it read-only; another transiently modified a source file under `src/app/`. Nothing was lost either time, and both self-restored. **Briefs in this run were progressively hardened to "no git command that writes — not even `git add`"**, which held afterwards. The lesson is that "read-only" is not self-evidently a *git* constraint to a lane; it must be spelled.

### 4.4 The executor reversed the lead's brief in **all five** correction rounds — and was right every time

| Round | What the lead said | What the source said |
|---|---|---|
| R2 | "assert the selection after the release" | non-discriminating — the shipped click arm already swallows at N>1 for an unrelated reason |
| R3 | "one computed-style read closes the `pointer-events` clause" | the removal mutation leaves every row green; only an explicit `auto` discriminates |
| R4 | "`border-color`'s initial value is `currentColor`" | did not reproduce; the value came from elsewhere |
| R5 | "`no-adjacent-sibling` has one emitter and looks unreachable" | **two** emitters; the dominant one is dragging an only child |
| R6 | "re-point the detached branch at `chain-disagrees`" | that sentence asserts screen and source disagree; in a detach they agree perfectly |

**Every brief in this run carried an explicit instruction to check the source rather than the brief, and to report a mismatch instead of implementing around it.** That instruction is doing real work and belongs in the skill rather than in each lead's prose.

The R5 row deserves attention: **the lead and an independent blind reviewer reached the same wrong conclusion, for the same reason — each read one of the sentence's two emitters.** A brief that says "find *every* branch that emits this, do not stop at the first" would have caught it. Later briefs in this run say so.

### 4.5 A lead's corrections need the same whole-file sweep the lane brief demands

Two of the lead's own plan corrections left a surviving unqualified restatement elsewhere in the file. And in R6 the lead's plan text repeated an over-claim (*"true of both emitters"*) that the **code** had just been corrected for in the same round — caught by the executor, not by the lead.

### 4.6 Evidence-Gate discipline held, and one lane improved on it

EG-1's brief required an instrument check before any zero was believed. The lane ran the required leg, and then **added a second of its own** because one bucket had reported zero and the brief's own rule said a zero is not believed on silence. It built a synthetic case, made the bucket fire, and thereby converted an absence of evidence into a measurement.

It also **falsified the plan's account of that bucket**: the plan grounded it in an optional field, but all 770 entries carry that field, and the population actually arrives through a different refusal path — 122 of 186, against 62 for the shape the plan named. An owner question would have been asked about a third of the population it was about.

---

## 5. What to change in the harness

1. **Persist review-lane output to the run directory on arrival.** (§4.1 — cost already paid once.)
2. **Resolve the input-identity / plan-amendment collision.** (§4.2 — three runs retired.)
3. **Put "check the source, not this brief; report a mismatch rather than implementing around it" into the skill**, not into each lead's prose. (§4.4 — five for five.)
4. **Add to review briefs: for any string, branch, or refusal, find every emitter — do not stop at the first.** (§4.4 — two independent readers, same error.)
5. **Add to gate-audit briefs: state how you built `node_modules`.** A wholesale symlink of a pnpm workspace produces false greens for every mutation. (§2 — cost one full audit pass.)
6. **Add to gate-audit briefs: any assertion comparing a property to a value the platform, a framework, an ancestor, or the rig could supply is suspect by default — drive it.** (§3 — four of five defects.)
7. **Spell "read-only" as "no git command that writes, not even `git add`".** (§4.3.)

---

## 6. Verdict on the run

The method worked, and it worked in the expensive direction: **it kept finding real defects at round 4 and round 5, after two rounds had already returned PASS on adjacent questions.** Six correction rounds on one story is a lot; a page-destroying write shipped into a paint-only story would have been worse, and nothing cheaper than a fifth blind lane found it.

The pacing question that prompted this document has a clean answer — **the slow round was slow because an audit rebuilt its own instrument before trusting it, and that audit produced the run's most durable findings.** That is the trade the harness should want.
