# §3 — "An instruction costs attention, not tokens"

Stage-1 analysis. Angle: the attention claim, and compression as a tool distinct from cutting.
Grounded only in this repo, its git history, `~/Documents/wiki/`, `~/.codex-orca` measurement records, and `~/.claude/kein/prompts/`. No external prompt-writing material was read (see *Deliberate non-reads*).

---

## 0. What §3 actually asserts, decomposed

The paragraph is four separable claims travelling as one. They have very different evidential standing and they should probably not stay in one section.

| | Claim | Standing in our evidence |
| :-- | :--- | :--- |
| A | An instruction's cost is attention, not tokens | Plausible framing, **zero measurement either way** |
| B | Adding a rule weakens the rules already present | **Asserted. Nothing in our evidence measures it; the nearest measurements point the other way** |
| C | Compression *raises* the survivor's salience | **Asserted, and now measured to be at best partly false** — see §2 |
| D | Compression is sound iff the specifics re-derive from the general form | **A real test, but underspecified in three ways, and it fails on its own best case** — see §2 |

Claim D is the useful one and the only one that survives contact with the evidence. Claims A and B are the ones the note leans on rhetorically and the ones it cannot support.

---

## 1. The deliberations

Each is stated as a question someone revising a standing prompt actually has to answer, with what would settle it.

### D1 — What is the unit that competes? Lines, bytes, rules, or topics?

§3's arithmetic ("thirty-four lines of which five are about one subject means the other twenty-nine compete with those five") assumes the **line** is the unit. Our own largest revision makes the units come apart badly:

- `reference/kickoff.md`: 10,344 B, 34 lines, **16 discipline bullets**, 8 of them carrying `Measured 2026-…` narrative.
- `~/.claude/kein/prompts/lead.md`: 4,386 B, 43 lines, **10 numbered standing rules**.

Bytes fell 58%; rules fell 38%; lines *rose*. `_raw/note/260809-…md:81-85` attributes the byte saving primarily to narrative stripping — "roughly 60% of kickoff.md's bytes were dated incident narratives" — which is a reduction in *bytes per rule*, not in rule count. If lines/bytes are the unit, that was the whole win. If rules are the unit, it did nothing.

**What would settle it:** an A/B on a fixture that reproduces one named failure, with three arms at matched byte counts — (a) full prompt, (b) same rules with narratives stripped, (c) fewer rules with narratives intact. If (b) ≈ (a) and (c) < (a), the unit is rules. If (b) > (a), the unit is bytes. `ocs eval` (`plugin/libexec/eval/run.py`) is the wrong shape as built — it A/Bs skill presence against a worktree fixture — but it already solves the hard part (pinned worktree per replicate, isolated config home, arm-level model pinning), so the instrument is a variant of one that exists.

**Caution on the 60% figure:** I could not reproduce it cheaply. `grep -o "Measured 2026[^.]*\."` over `reference/kickoff.md` yields 1,553 B of 10,344 (15%), because the narratives run several sentences past the first period. 60% is plausible but is itself an unverified number in a note about unverified numbers.

### D2 — Is the cost a function of rule *count*, or of rule *vagueness and conflict*?

This is the load-bearing question and §3 does not ask it. The two mechanisms recommend opposite actions: count → cut anything; vagueness → rewrite, and possibly *lengthen*.

Evidence bearing on count:

- **Cutting 63% of a prompt changed nothing.** OMC's Critic at 3,047 words → codex-orca's at 1,115 words produced no behavioural difference; and a three-line restoration of the removed severity floor and asymmetric-loss framing produced no difference across 5 replicates per variant on a fixture with a planted data-loss defect under deliberate pressure — 5/5 `MUST_FIX`, defect ranked first, zero downgrades, both arms (`~/.codex-orca/docs/superpowers/verification/agent-prompt-evals.md`; summarised at `docs/prompt-porting-notes.md:48-56` and `docs/purpose.md:37-41`). If ~1,900 words of competing instruction had a detectable attention cost, that is where it should have shown. It did not.

Evidence bearing on conflict/vagueness:

- **A conditional produced both branches.** `_raw/note/260805-…md:468-471` records removing a `SendMessage` conditional from `worker-brief.md` on the user's standing objection to conditionals in prompts, "from having seen 'do A or B' produce results containing both." That is a *behavioural* failure caused by one instruction's form, not by twenty-nine neighbours.
- **A rule already present was violated anyway, and adding another was rejected as the remedy.** `_raw/note/260803-…md:73` — "It was already covered by existing instructions and was violated anyway, which is the argument that a further rule is not the remedy." `_raw/note/260805-…md:291` — "after you ask, STOP" "was being violated routinely, and for a defensible reason: stopping costs a round trip." The diagnosed cause is *incentive*, not dilution.

So our evidence supports the *conclusion* §3 reaches (another rule does not help) via a mechanism §3 does not name (marginal return on an already-imperfectly-followed rule), and offers no support at all for the mechanism §3 does name (competition scaling with count).

**What would settle it:** the same fixture run against (a) a prompt with the target rule alone, (b) that rule plus 20 unrelated rules, (c) that rule plus 20 rules one of which is a near-conflict. If (b) ≈ (a) and (c) < (a), §3's mechanism is wrong and the deliberation should be "does this rule conflict with or blur an existing one", not "how many rules are there".

### D3 — Before adding, has the rule already been said somewhere the agent will see?

This is cheap, mechanical, and already in use — and §3 does not mention it even though it is the only operational form of the attention argument we have. Reproduced live in `plugin/prompts/`:

- scope discipline: **11/14** canonical role prompts
- self-approval: **1/14** (executor only)
- "ask the lead": **0/14**

These reproduce `_raw/note/260809-…md:225-228` exactly. The 260809 pass cut scope discipline from the worker brief on filter 2 ("not derivable from the role's own purpose") precisely because 11/14 already carried it.

**What would settle a proposed addition:** one grep across `plugin/prompts/*.md` plus `~/.claude/kein/prompts/lead.md`. A rule already present in the role prompt the agent is running under is not an addition, it is a duplicate, and it is the one case where the attention argument is decidable without an experiment.

### D4 — When a rule appears in *n* of *m* prompts, is that redundancy to cut or a defect to fix?

The same instrument gave opposite verdicts on the same day. Scope discipline at 11/14 → *cut from the brief, it is already covered*. Self-approval at 1/14 → "a defect in thirteen prompts rather than something the brief should keep patching" (`_raw/note/260809-…md:227-228`).

The distinction is defensible — coverage vs. gap — but it is not stated as a criterion anywhere, and it is exactly the judgement someone will get wrong. The implied rule is: **a high count means the rule belongs downstream and the upstream copy is the duplicate; a low count means the rule belongs downstream and is missing there.** In both cases the answer is "fix it downstream", and in neither case is the answer "compress".

**What would settle it:** deciding whether the standing prompt is a *backstop* for role prompts or a *supplement* to them. If backstop, 11/14 is a defect too (3 roles are unguarded). If supplement, 1/14 is fine and the brief should carry it. That decision has not been made anywhere I could find, and it silently governs both verdicts.

### D5 — Re-derivable by whom, and tested how?

§3's test — "the specific cases can be re-derived from the general form" — is silent on the reader. Three readings that give different answers:

1. **The author, reading their own compression.** Trivially passes; the author remembers the specifics. This is the reading that will be used by default and it is worthless.
2. **The agent, asked whether it can derive them.** Directly measured to be unreliable: `_raw/note/260809-…md:183-196` records a session confidently denying, twice, that its own appended system prompt contained a section that was demonstrably in the file, with a fabricated inventory of what it claimed to see instead. Conclusion recorded there: **"Introspection about one's own system prompt is not evidence."**
3. **A fresh reader with the general form and nothing else, asked to enumerate.** The only honest cheap form. Run below.

**What would settle a compression:** (3) as a screen, and behaviourally — the fixture that reproduces the specific failure, run against the compressed prompt — as the actual test. §5 of the note already says this ("whether a *named failure recurs* is binary and cheap"); §3 does not connect to it, and it should.

### D6 — Does the general form carry the *fact* and the *remedy*, or only the *policy*?

This is the failure mode the worked attempt below exposes, and §3 has no vocabulary for it. A standing rule usually bundles three things:

- a **policy** ("do not trust that"),
- a **harness fact** ("the environment snapshot is captured at session start and never updates"),
- a **remedy** ("read the line back", "run `git status`").

A general form reliably carries the policy. It does not carry the fact — a fact is not derivable from a principle by construction — and it carries the remedy only sometimes. §3's test as written asks about "the specific cases", which reads as policies and passes when the facts have been silently dropped.

**What would settle it:** before compressing, split each surviving specific into policy / fact / remedy and check the general form against each column separately. Any fact in the fact column is non-negotiable evidence that the compression must keep a clause, not a principle.

### D7 — What does the general form *additionally* license, and does it argue against neighbouring rules?

Untouched by §3, and measured below to be the larger cost. Several specific rules are a fixed set of behaviours. One general rule is a *generator*, and a generator samples: it produces different instantiations per run, some of them rules nobody wanted, and it can actively argue *against* rules that live elsewhere in the same prompt.

**What would settle it:** the enumeration probe, read for false positives as well as recall — which of the enumerated items are things you would refuse if proposed, and which of your existing rules does the general form declare unlicensed.

### D8 — Is the move cut, compress, re-file, or dissolve? §3 offers two of four.

Our history contains all four, and the two §3 omits are the ones that did the most work.

- **Cut** — kill dev servers before a full-suite run (loud failure, filter 1); the "archive round byproducts" bullet (project rule, not harness rule). `_raw/note/260809-…md:63`, `:148-151`.
- **Compress** — see §2. Rare.
- **Re-file** — the git block. "The useful move was neither keep nor drop but **re-file**. Three of them … are not restore rules at all. They are general editing discipline … and they were only ever filed under 'restore' by accident" (`_raw/note/260809-…md:110-114`).
- **Dissolve into structure** — commit `a2ab0b4`: "**Three instructions disappeared into structure rather than being cut for brevity.** `plan` cannot produce a gated-looking artifact, because its template knows only `Draft`, so the paragraph defending that property is unnecessary. `ocs state plan` already fails with 'no state machine for workflow plan', so the paragraph explaining the absence of state is too." Same move elsewhere: `sandbox_mode` "moved out of prose into the agent config, so read-only is enforced by the runtime rather than by instruction" (`docs/prompt-porting-notes.md:25-27`); the OMC keyword-trigger table dropped because "hooks fire those anyway" (`_raw/note/260809-…md:153`); commit `399b26b` deleting required timestamp fields no code read.

**What would settle which move applies:** ask, in order — (1) can the mechanism make the instruction unsatisfiable or unnecessary (dissolve, always best: it cannot be forgotten); (2) is the rule in the wrong document (re-file); (3) is the failure loud (cut); (4) only then, is there a general form (compress). §3 skips straight to (4).

There is a fifth, named as the agreed direction and not built: **render per audience.** `_raw/note/260809-…md:213-218` — the worker brief's conditionals "exist only because one file serves three audiences; rendering deletes them mechanically", with `manifest.json`'s `sandbox_mode` (9 read-only, 5 workspace-write) as the discriminator that already exists. That is a compression that a *build step* performs and a human never has to defend.

### D9 — Who pays the maintenance cost of the compressed form?

`_raw/note/260809-…md:177-181`: `--append-system-prompt-file` is **not repeatable** — given twice, only the last file survives (probed with `ALPHA7`/`BRAVO9` tokens; only `BRAVO9` returned). So a shared core plus per-harness overlay is unavailable, each prompt file is self-contained, and shared discipline is maintained twice by hand. A compression that produces one elegant general rule in two files is two rules to keep in sync. §3 counts only the model's cost.

### D10 — What does the compressed rule cost when it is wrong?

This is §4's question applied to §3's tool, and the two sections should probably be connected. A specific rule that is wrong is wrong in one situation. A general rule that is wrong is wrong across the whole family it generates — and, per the probe below, across a family the author never enumerated.

---

## 2. Worked compression attempts on a real standing prompt

**Method.** Two arms. Each: take a group of specific rules from a live standing prompt, write the generative rule I believe sits under them, hand *only* that general rule plus role context to a fresh agent that has never seen the specifics, ask it to enumerate the concrete instructions the principle licenses and, separately, what it decided the principle does *not* license. Score recall against the real rules; read the excess for false positives.

**Proxy warning, stated up front.** This measures *enumeration*, not *behaviour*. §3's test is about whether an agent operating under the compressed prompt acts the same; this probe asks whether an agent can name the specifics. Enumeration is the easier task, so recall here is an **upper bound** on the real thing. A failure here is decisive; a pass here is not.

### Arm A — `reference/worker-brief.md`, the reporting rules

Five surface rules, lines 24-28:

1. Paste the actual results; never claim "all pass" from a partial run.
2. Report no number you cannot re-derive — give the command beside it, or an immutable anchor.
3. A zero result is evidence only once you have shown the instrument can produce a non-zero one.
4. Anchor every edit by content, never by line number; a mutating script must assert it applied exactly once and print the evidence; confirm by reading the line back, never by a green suite.
5. If you disprove something the brief asserts, propagate the correction through your own output; grep the whole FILE, not your diff.

**Proposed generative rule:** *Report only what an instrument that could have returned the opposite result actually returned.*

**Result.**

| Surface rule | Re-derived? | Note |
| :--- | :--- | :--- |
| 1 — paste actuals, no "all pass" from partial | **Yes** | Probe items 4, 5 — and item 5 sharpened it into three distinct labels (ran/passed, ran/failed, not run) |
| 2 — no number you cannot re-derive | **Partial** | The re-derivability requirement came; "give the command beside it" came as item 4; "or an immutable anchor" did not |
| 3 — a zero needs a calibrated instrument | **Yes, precisely** | Probe items 2, 3, including the "run it against the broken state" remedy |
| 4 — anchor by content, not line number | **No** | Not derived. The probe explicitly filed the whole neighbourhood under *not licensed*: "the principle governs reporting, not workflow order" |
| 4b — never confirm by a green suite | **Yes (negative only)** | Item 3 covers "a check that cannot produce a failure"; the positive remedy "read the line back" did not appear |
| 5 — propagate a disproof through your own output | **No** | Item 8 covers reporting disconfirming results; propagating a correction through prose you already wrote is a different act and did not appear |

Recall: 3 clean, 1 partial, 2 misses out of 6.

**The interesting result is *which* two missed.** Rule 4 and the mutation-evidence clauses are precisely the ones `_raw/note/260809-…md:110-114` independently identified as **misfiled** — "they are not restore rules at all … they were only ever filed under 'restore' by accident." The probe found the mis-grouping without being told it existed. So a failed re-derivation is at least as often a signal that the group was wrong as that content was lost. That is a genuinely useful diagnostic and it is a better argument for the test than §3's own.

**Excess.** The probe also produced item 7 — "state the claim no wider than what the run actually exercised" — which is not in `worker-brief.md` at all. It is a reporter-side version of `lead.md` rule 2. The general form reached into a neighbouring file.

### Arm B — `~/.claude/kein/prompts/lead.md`, the state/evidence rules

Rules 2, 4, 5, 6, 7. My reading is that these are five faces of one thing: a commit standing in for its gates, an environment snapshot standing in for git, a half-written file standing in for a finished one, one probe site standing in for a population, a summary standing in for a diff.

**Proposed generative rule:** *An artifact that resembles evidence is not evidence. Before you act on a state, name what actually measured it, and when.*

**Result.**

| Rule | Re-derived? | Note |
| :--- | :--- | :--- |
| 2 — a defect names the site probed, not the population; make the lane enumerate the class from source | **No** | The probe reached provenance and staleness and never reached scope-of-population. The single most expensive rule in our history (`reference/kickoff.md:21`: without the question "the commit would have said 'fixed' over six live instances") does not fall out of this principle |
| 4 — gates run before the commit, not after | **Partial** | Item 2 says re-run before "merge, rebase, push"; *commit* is absent, and the ordering rule as such never appears |
| 5 — repo state from live git, never a session's environment snapshot | **Partial** | Item 3 got the policy exactly. The **fact** — the snapshot is captured at session start and never updates — is not derivable and did not appear. Without it, the snapshot reads as live data and the policy has no trigger |
| 6 — a file a lane is writing is neither yours to edit nor yours to read | **Half** | The *read* half falls out of staleness. The *edit* half — your edit vanishes with no conflict and no error when the lane next rewrites from its own context — is a write failure, not a measurement failure, and did not appear |
| 7 — compare the diff against the brief before spawning verification | **Partial** | Item 6 says read the diff before merging. Different trigger, different reason (summary≠code, rather than a scope shortfall wasting a review cycle) |

Recall: 0 clean, 4 partial, 1 miss out of 5. **The re-derivation test fails on this compression.** By §3's own criterion, that compression "dropped something and is a cut pretending otherwise."

**Excess, and this is the finding worth carrying.** The probe emitted eight rules where lead.md has five, and the extras are not noise — they are confident, plausible, and absent from our prompt on purpose or by omission: pin every result to the SHA it ran against and expire it on any new commit; tell each lane which commit to measure against and require it to report the SHA it observed; attach provenance and age to every state you report to the user. A reasonable person might want some of these. Nobody chose them.

**And the general form argued against a neighbouring rule.** Under *not licensed*, the probe wrote: "**Mandate a second reviewer lane, or N reviewers before merge.** More opinions are not a measurement; this substitutes headcount for provenance." That is a direct argument against `lead.md` **rule 1**, the strongest rule in the file. Compressing 2/4/5/6/7 under an evidence principle does not merely fail to re-derive them — it manufactures a principled objection to rule 1.

### What the two arms together establish

1. §3's re-derivation test is **real and discriminating** — it passed one group and failed another, and the failures were informative rather than arbitrary. Keep it.
2. It is **not the whole test**, because it only measures recall. Compression's actual cost showed up in the excess, which the test as stated never looks at.
3. **Claim C is at best half true.** Compression may raise the survivor's salience; it certainly lowers the *determinacy* of what the survivor produces. Several specific rules are a set; one general rule is a distribution. §3 presents compression as free upside and it is a variance trade.
4. The **facts** and the **positive remedies** are what compression eats, systematically, in both arms. Policies survive.

---

## 3. Where §3 is wrong, unmeasured, or incomplete

**Wrong — the mechanism.** "Adding a rule weakens the rules already present" is contradicted, as far as our evidence goes, by the one place we measured it: 1,932 words removed from the Critic prompt changed no behaviour, and 3 words' worth of decision rule added back changed no behaviour, on a fixture built to be sensitive to exactly that rule. Whatever is going on, competition-per-line at that magnitude is below our floor. The cases where a rule failed to bite trace to *incentive* (`260803:73`, `260805:291`) or to *form* (the both-branches conditional), not to neighbour count.

**Wrong — compression as free upside.** Measured above: it is a recall/variance trade, and it can generate an argument against a rule you meant to keep.

**Unmeasured — the arithmetic.** "Thirty-four lines of which five are about one subject" picks a unit (lines) that our own revision shows moving in the opposite direction from bytes and from rules. No instrument here distinguishes them.

**Unmeasured — "raises the survivor's salience."** Nothing measures salience. The only salience-adjacent claim in the repo is `docs/purpose.md:17-19` — "Several are large single files, and size correlates with the model losing the thread inside them" — which is a stated correlation with no measurement cited, and which is about *procedural* skill documents, not rule lists. It is the closest support §3 has and it is an anecdote.

**Incomplete — the move set.** Two tools named; four in use (cut, compress, re-file, dissolve into structure) and a fifth agreed but unbuilt (render per audience). Dissolve is strictly better than all of them when available, because the instruction stops needing to be followed. `a2ab0b4` is the clean instance and §3 does not know it happened.

**Incomplete — the re-derivation test's reader.** Unspecified, and the default reader (the author) makes it vacuous while the tempting reader (ask the model) is measured unreliable (`260809:183-196`).

**Incomplete — no exit to measurement.** §5 already has the right instrument ("whether a *named failure recurs* is binary and cheap"). §3 defines a test and never routes it there. A compression's re-derivation claim is exactly a named-failure-recurrence question, and the two sections should be one argument.

**Framing — the section is two topics.** Consistent with the owner's assessment: (a) *what does an instruction cost, and how would we know*, and (b) *what are the moves available when a prompt is too big, and how do you pick*. (b) is well-grounded in our history and mostly independent of (a). (a) is currently unsupported and should either be measured or demoted to a hypothesis.

---

## 4. What I could not ground

- **The attention/competition mechanism itself, in either direction.** No experiment in this repo, the wiki, or `~/.codex-orca` varies rule count while holding content and fixture fixed. The Critic eval varies *content* at n=5 and returns null; a null at n=5 bounds nothing about a small effect.
- **"Raises the survivor's salience."** No measurement exists. I could neither support nor refute it.
- **The "60% of kickoff.md's bytes were narrative" figure.** My cheap reproduction yields 15% by first-sentence match. The full figure is plausible and unverified; I flag it as one more number in the vault that nobody can re-derive, in a corpus whose own rule is that a number nobody can re-derive is a number nobody can catch (`260805:~400`).
- **Whether the compressions actually shipped preserved behaviour.** "Rule 3's git discipline compressed ~700 words → five bullets **with every operative rule kept**" (`260805:466-467`) — the claim is the author's reading, and no fixture was run. Same for the whole `kickoff.md → lead.md` revision: `_raw/note/260809-…md` records the reasoning in detail and no behavioural check at all. Our largest compression is unverified by our own standard.
- **Whether enumeration recall predicts behavioural equivalence.** My probe is a proxy. I have no calibration for it.
- **The pre-rewrite `worker-brief.md`.** `reference/` is untracked and the rewrite was applied in place (`260809:231-234`), so the before/after diff for the worker brief cannot be recovered. The kickoff→lead pair survives only because `kickoff.md` was superseded rather than deleted.

### What would change my mind

- **On claim B (adding weakens):** any A/B holding the target rule and the fixture fixed while varying only the count of unrelated rules, showing a compliance drop on the target. One fixture, one named failure, ≥10 replicates per arm. That result would make §3 correct as written and I would drop the objection.
- **On claim C (compression raises salience):** the same fixture run against a compressed arm and a specific arm, where the compressed arm shows *equal or better* compliance on every specific and no drift into unlicensed behaviour. My probe suggests the drift is real; a behavioural run showing it does not survive contact with a real task would overturn me.
- **On the re-derivation test:** a behavioural run of the Arm B compression showing it holds despite the enumeration miss. That would establish that enumeration recall is the wrong proxy and that §3's test should be run some other way — which is itself worth knowing.
- **On the unit question:** the three-arm matched-byte experiment in D1.

## Deliberate non-reads

`~/Documents/wiki/context-engineering/context-engineering-claude-5.md` exists and its heading list includes "규칙 → 판단" (rules → judgement), which is squarely on this angle. It is ingested third-party guidance, and reading it would contaminate the measurement of what the later external-material stage adds. I read its headings only and no body. Flagging it as the first thing that stage should reconcile against this document.

## Evidence index

| Path / commit | Used for |
| :--- | :--- |
| `docs/prompt-revision.md:19-23` | the §3 text under analysis |
| `docs/prompt-porting-notes.md:48-61` | Critic 3,047→1,115 null; three-line restoration null; "a gap found by reading two prompts side by side is a hypothesis, not a defect" |
| `docs/prompt-porting-notes.md:25-27` | `sandbox_mode` moved from prose to config — dissolve-into-structure |
| `docs/purpose.md:17-19` | "size correlates with the model losing the thread" — the only salience-adjacent claim we have |
| `docs/purpose.md:37-41` | "prompt material that reads as load-bearing frequently is not" |
| `reference/kickoff.md` (10,344 B, 16 bullets, 8 `Measured` narratives) | the before side of the compression |
| `reference/kickoff.md:21` | the population-vs-site rule and its cost ("six live instances") |
| `reference/worker-brief.md:24-28` | Arm A subject |
| `~/.claude/kein/prompts/lead.md` (4,386 B, 10 rules) | the after side; Arm B subject |
| `plugin/prompts/*.md` (live grep) | 11/14 scope, 1/14 self-approval, 0/14 ask-the-lead |
| `plugin/libexec/eval/run.py`, `plugin/libexec/ocs-eval` | the A/B instrument that exists and its shape |
| commit `a2ab0b4` | "three instructions disappeared into structure rather than being cut for brevity" |
| commit `399b26b` | required fields deleted because nothing read them; an invented timestamp as the cost |
| commit `9d79fdd` | a budget turned into a rule, cut once the number stopped matching |
| commit `3df0e93` | the note's own commit message — §3's intent in the author's words |
| `~/.codex-orca/docs/superpowers/verification/agent-prompt-evals.md` | the differential method, fixture, and the 5-replicate null |
| `wiki/_raw/note/260809-rewriting-standing-agent-prompts-on-measurement.md` | the three filters; the 60% narrative claim; the re-file move; the introspection failure; `--append-system-prompt-file` non-repeatability; the 11/14 and 1/14 counts; render-per-target |
| `wiki/_raw/note/260805-a-zero-that-proves-nothing.md:291`, `:464-471` | "after you ask STOP" violated routinely; ~700 words → five bullets; conditionals producing both branches |
| `wiki/_raw/note/260803-parallel-verification-lane-operation.md:73` | already covered by existing instructions and violated anyway |
| `wiki/_raw/note/260804-lead-prescriptions-and-truncated-populations.md:62` | a day-old rule violated by the artifact everyone re-reads |
| Arm A / Arm B enumeration probes | run this session, two fresh agents, no file access; transcripts in this session's task outputs |
