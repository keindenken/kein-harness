# Writing a rule you will never measure

Stage-1 analyst note. Angle: what a person does at the moment of editing a standing prompt, given no measurement will ever arrive — and what that lack should change about what they are willing to write down at all.

Grounded in `kein-harness` (`docs/`, git history), `descvi/repo` `AGENTS.md` and its history, `~/Documents/wiki/_raw/note/`, `reference/kickoff.md`, `reference/worker-brief.md`, `~/.claude/kein/prompts/lead.md`. §5 of the source note is out of scope by instruction.

---

## 0. The situation, priced

Measurement is not merely absent, it is priced. `ocs eval`: 35–40 min per arm on the *cheap* fixture with every model pinned to Sonnet, `with-skill` killed at a 2400 s timeout after 238 turns, the primary fixture "not viable under this design" (`.agents/kein/requirements/260804-skill-ab-eval-harness.md`). One prompt-line hypothesis has ever been tested in this corpus, and it was rejected (`docs/prompt-porting-notes.md`: a three-line restoration of the Critic's severity floor, 5 replicates per arm, null).

So the edit-time question is not "how do I get evidence" but **"what may I write, given that the only thing that will ever check this line is a person or an agent reading it for some other reason?"**

That reframing is the whole of my answer. The other analysts asked what licenses a deletion, where the argument lives, and whether the rule does anything. Nobody asked what property of a *written line* makes its own falsity self-announcing. That property is choosable at the desk, costs nothing, and is the only lever that survives the absence of an instrument.

---

## 1. The corpus already contains the answer, in another domain

descvi `565a6b0` (2026-08-05) is the closest thing to a solved version of this problem. Three consecutive audit passes had found the note's own numbers wrong; the third pass found the audit "committed the class it exists to fix, in the paragraph teaching what went wrong". The resolution was explicitly **not** another round of care:

> Every number here is either regenerable by a command this note publishes, or anchored to an immutable object (a commit SHA, a `git show`). A number that is neither gets deleted, not corrected.

And the diagnosis behind it, in the same commit, about a citation that occupied four different line positions in one day:

> That is the argument for naming it by **mechanism**, and it is stronger than "it was wrong" ever was.

This is a complete authoring policy derived under exactly my constraint — no instrument, only readers — and it was reached by giving up on diligence. It has never been generalised past citations. Generalised, it gives **three legal shapes for a claim in a standing prompt**, and *delete* as the default for anything that is none of them:

**(1) A pointer to the source that regenerates the value.** descvi `a995bba` (2026-08-10) is this move applied to a rule: the enumerated gate list left `AGENTS.md`, replaced by "the gate set is CI's `verify` job — not a list written here. Run `pnpm gates`, which parses that job." The commit's own diagnosis is the criterion: *"the enumeration was a lookup; that it lived there is why it rotted."* The prompt keeps the rule; the world keeps the value.

**(2) A claim anchored to an immutable object.** `lead.md`'s `## Harness facts` block: "Dated 2026-08-08, measured on Claude Code 2.1.226 with agent teams disabled. These are the lines most likely to rot; check them before trusting them." A fact pinned to a version and a probe is anchored the way a SHA is anchored — it cannot become quietly wrong, only visibly stale.

**(3) A mechanism.** "Your edit vanishes with no conflict and no error when the lane next rewrites from its own context" (`lead.md` rule 6). A mechanism is falsifiable by opening one file. It is also what lets an agent apply a rule to a case the rule did not name.

Everything else — a rate, an effect claim, a hand-copied enumeration, "this makes output better" — is a claim whose falsity only a measurement programme could establish, which under the stated constraint means *nobody will ever establish it*. The corpus's own verdict on that class is not "write it carefully". It is **delete, not correct**.

**The direct answer to the brief's second half, then:** the lack of measurement does not make you write fewer lines, or shorter ones. It makes you write **only claims whose falsity a reader can establish from what they already have open** — and fewer lines is a consequence, because most candidate lines are not of that kind.

---

## 2. Evidence that the shapes separate: rot is concentrated in one of them

The claim is checkable in the one standing prompt under version control, at line granularity. `descvi/repo/AGENTS.md`, same file, same section, same author, same three weeks:

| Line | Shape | Touches | Fate |
| :--- | :--- | ---: | :--- |
| "A gate must be able to go RED. Make it fail before you believe it green." | mechanism | **1** (`1d0661d`, 2026-07-27) | untouched to today |
| "Cite code by ANCHOR, never by line number — `node scripts/check-citation-anchors.mjs`" | pointer + mechanism | **1** (`e6d02dd`, 2026-08-07) | untouched |
| "`pnpm typecheck` IS N COMMANDS OVER DISJOINT TREES…" | cached enumeration | **4–5** (`4690908` 07-28, `09825ed` 07-29, `f364bc1` 08-03, `8ede02d` 08-04) | **deleted** `a995bba` 08-10 |

The enumeration was amended roughly every three days for a fortnight. Its own text records the rot inline and escalating: `f364bc1` changed "TWO COMMANDS" to "THREE COMMANDS" and added a ⚠ sub-bullet confessing *"this line said 'TWO COMMANDS' for a day after it shipped. A gate description that lags the gate is worse than none: it tells you which half you may skip, and it is wrong about which halves exist."* `8ede02d` rewrote the confession because the branch had falsified it too. Then the class was removed.

Two things follow, both usable at the desk and neither requiring an experiment:

- **Amendment count is a free rot signal, and the data already exists.** `git log -G '<phrase>' -- <file>` costs one command. A line amended three times in a fortnight is not a line someone keeps improving; it is a cache of a truth that lives somewhere else. In both this case and `565a6b0`, the correct move after the third correction was structural, and both times the author reached it only after paying for a fourth.
- **A prompt that begins carrying warnings about its own accuracy has entered the terminal phase.** The ⚠ bullet is a standing prompt spending attention to say "the line above may be wrong". That is the strongest available signal that the content has the wrong home, and it is visible without any measurement at all.

Note also the direction this cuts against the fifth analyst's tempting correlation. `descvi/AGENTS.md` is not shrinking because it is under version control; it is shrinking because it declares a membership rule and because its high-churn lines are of a shape whose rot is *loud in the diff*. A tracked file full of mechanism claims would show no churn and would ratchet just as happily.

---

## 3. The premise-inversion test: which of the three shapes a braided line actually is

The hardest edit-time case is a line that is a rule and a harness fact welded together, because the two rot at different rates and the weld hides which half is load-bearing. There is one exhibit in the corpus where both the before and the after survive.

`reference/kickoff.md:17` — *"Size tasks so turns end often. A subagent's whole run is one turn… Measured 2026-07-26: a message sent mid-run crossed six tool-call boundaries untouched and arrived only at the turn boundary. **Nothing you send interrupts a working agent; only the human pressing Escape does.**"*

The 2026-08-08 measurements falsified that last sentence outright (`260808-mid-turn-message-delivery…`; messages land at the next tool round with teams off, and `TaskStop` plus a send by name is a real interrupt). The instruction nonetheless survived into `lead.md` rule 10 — *"Size work into pieces you can inspect. You can steer a running lane, but you cannot review what has not been reported yet."*

Same instruction; **inverted premise**. The old reason was "you cannot steer, so size small." The new reason is "you *can* steer, but you cannot review what has not been reported." The rule was rescued only because a full rewrite happened to be underway. An incremental edit would have left it standing on a corpse, which is the source note's own "a sentence that stays true while its reason dies", caught here at a specific line with both sides in hand.

**The test that falls out, and it costs one thought:** *negate the fact this line rests on. Does the instruction survive?*

- **Survives** → the fact was decoration. Write the instruction with a mechanism that does not depend on it, and drop the fact. (Rule 10 is the worked example.)
- **Dies** → the line is a harness fact wearing an instruction's clothes. It belongs in the dated, version-pinned quarantine, not among the standing rules — and it belongs there *as a fact*, so that re-measuring the block re-decides it automatically.

This is the desk-time discriminator for the structural split `lead.md` performed by hand, and it discharges under the criterion the brief cares about: it has a state in which you cannot answer. If you cannot state the fact the line rests on, you have written an assertion of taste, and taste is the class that no reader can ever falsify.

---

## 4. The instrument you actually have is the reader-in-passing

With no eval, the only recurring check on a standing prompt is somebody reading it for an unrelated reason. That channel is real and has fired:

- `9d79fdd` (2026-08-10): the six-skill ceiling in `docs/purpose.md` was caught *"by a Planner reading `purpose.md` before answering an unrelated question, and reported back as a violation, because the count had silently stopped matching the plan."* The commit message shows the arithmetic was wrong in two directions at once.
- `7b1c9d2` (descvi): the `2plan` pointer contradiction was caught by the user watching a session follow it.
- `f364bc1`: a rate the author had written *that morning* — "measured at 1 in 4 full runs" — withdrawn the same day when nine further runs produced zero.

The instructive contrast is between the first and the last, because they are both numbers and they behave oppositely. The six-skill count is a claim over the document's own scope: any reader holding the document can recount it, so it self-reports the moment it goes false, at zero marginal cost. The 1-in-4 rate is a claim over stochastic events: no reader can check it from what they have open, so it can only be caught by someone deliberately spending ten runs — which happened once, by luck, and would not happen again. The commit that withdrew it titles its own moral: *"a recipe with no numbers has nothing to go stale"*, and the remedy adopted was to record **events and their conditions** rather than a rate.

So the rule for numbers, and by extension for every claim: **write what a reader who is here for something else can check; never write what only a measurement programme could re-derive.** The reader-in-passing is not a weak substitute for an eval. It is a continuous, free, adversarial detector — but it can only report on claims whose falsity is visible from inside the reading. Line shape is what determines whether that detector can reach a given line, and line shape is chosen at the desk.

This is also why "does the document obey its own rule" (the fifth analyst's D9) is more than a self-consistency curiosity: it is the one class of claim where the reader is *guaranteed* to hold the evidence.

---

## 5. Fewer lines, but not for the attention reason

The third analyst is right that "adding a rule weakens the rules already present" is unsupported and that the one relevant measurement points the other way (1,932 words removed from the Critic, no behaviour change). Restraint still follows, from a different and better-evidenced argument:

- **P(a given added line does anything) is low and unmeasured.** One hypothesis tested, rejected. The corpus's own summary, `docs/purpose.md`: *"Prompt material that reads as load-bearing frequently is not."* And `docs/prompt-porting-notes.md`: *"A gap found by reading two prompts side by side is a hypothesis, not a defect."*
- **P(the costs land) is 1, and the costs are observed rather than theorised.** The duplication tax: `--append-system-prompt-file` is not repeatable (measured with `ALPHA7`/`BRAVO9`), so every shared rule is maintained twice by hand. The rot tax: five amendments in thirteen days, above. The relocation debt: nearly every large shrink in the corpus is a move, and a move is work someone has to do later. The fabrication tax: `399b26b`, a required field a model cannot honestly fill produced a receipt dated nine hours before its own run.

Certain costs against an uncertain benefit is an argument for restraint that does not depend on any model of attention, and it survives the attention claim being wrong. It also says *which* lines to refuse first: the ones whose benefit is not merely unmeasured but **unmeasurable in principle by the reader** — i.e. exactly the shapes §1 rules out.

---

## 6. At the desk

Five minutes, no instrument, in order. The first two are established elsewhere and I do not restate their evidence; the last three are this note's.

1. Can the runtime refuse the violation instead? (dissolve into structure)
2. Is it already carried by the prompt the agent runs under? (one grep)
3. **Which of the three legal shapes is my claim — pointer, anchored fact, or mechanism?** If none, it is a taste assertion; delete it or rewrite it into one of the three.
4. **Negate the fact this line rests on.** Survives → drop the fact, keep the mechanism among the standing rules. Dies → it is a harness fact; move it into the dated block so re-measurement re-decides it.
5. **Could a reader who is here for another reason tell this line had gone false?** If not, you have written something only you will ever check, and you will not.

And once, retrospectively, on any prompt older than a month: `git log -G` each rule. The lines you have amended three times are telling you where they belong.

---

## 7. Delta against the other five

**What I would have missed without them.** That deletion has at least seven cheap documentary warrants, so the ratchet's stated cause is wrong — I had relocation and the scope line, not the taxonomy. That `git log -S` structurally cannot retrieve a deletion's argument, because it searches present text (`where-justification-lives` §2); that undercuts my §2 recommendation, since churn is retrievable but reasoning is not. That compression is a recall/variance trade with measured excess, including a general form that manufactured an objection to `lead.md` rule 1 (`attention-cost` §2) — I had treated compression as safe. That "name the counterpart" has no failure state and every cost in the record was found by a run or an objection, never at the desk (`counterpart` §4) — which is a direct warning that my §6 list is diagnostic and unproven as preventive. That the `run_in_background: false` mechanism in three SKILL.md files is contradicted by a measurement four days old and nothing surfaced it (`absence-of-failure` §11) — a live instance of exactly the braiding failure in my §3.

**What they missed that I found.**

1. **`565a6b0`'s stopping rule generalises.** `counterpart` §D9 cites the commit as a self-consistency anecdote. The transferable content is the policy — regenerable, anchored, or deleted — and it is the corpus's own answer to writing without an instrument, reached after diligence had failed three times.
2. **Rot is concentrated by claim shape, and the evidence is line-level and already in git.** One touch for the two mechanism rules; four to five for the cached enumeration, then deletion. Amendment count is a free warrant nobody proposed, and it is retrospective — unlike the 260810 programme, the data exists now.
3. **The premise-inversion test**, with `kickoff.md:17` → `lead.md` rule 10 as the worked exhibit: an instruction that survived the *inversion* of the fact it was written on. Three analysts noted the harness-facts quarantine; none supplied a test for deciding which side of it a braided line belongs on.
4. **The reader-in-passing as the operative instrument, and the shape criterion that determines its reach.** `9d79fdd` and `f364bc1` are cited by others as a cost case and an epistemics case respectively. Paired, they give the authoring rule about which numbers — and which claims — are safe to write.
5. **A replacement argument for restraint** after `attention-cost` demolished the attention mechanism: certain costs (duplication, rot, relocation, fabrication) against a measured-near-zero benefit prior.

---

## 8. What I could not ground

- **Whether the three shapes are exhaustive or merely the three this corpus reached.** They are read off two commits in two repos plus `lead.md`'s structure. A fourth shape may exist; "taste" may sometimes be right and unwritable in any of the three.
- **Whether churn actually predicts wrong-home, or only predicts contentiousness.** n=3 lines in one file. The mechanism rules are also the *older* and more abstract ones, and abstraction alone could explain low churn. What would change my mind: a mechanism-shaped rule with high amendment churn, or an enumeration that sat unamended for a quarter.
- **Whether the premise-inversion test ever fires preventively.** It is derived from one rewrite and has never been run at authoring time. `counterpart` §5's finding — that no cost in the whole record was found at the desk — applies to it with full force, and I flag it rather than argue past it.
- **Whether reader-in-passing detection is frequent enough to matter.** Two instances (`9d79fdd`, `7b1c9d2`) over roughly three months. That is a channel, not a rate, and I decline to write the rate for the reason `f364bc1` gives.
- **The `f364bc1` / `9d79fdd` contrast is post-hoc.** Two numbers, opposite fates, and I constructed the discriminator after seeing both. It predicts nothing yet.
- Per the boundary: no `~/.claude/plugins/`, no external prompt-writing material, no web search. `~/Documents/wiki/context-engineering/context-engineering-claude-5.md` was not read.
