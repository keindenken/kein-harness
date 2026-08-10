# §1 The ratchet — the deliberations underneath it

Stage-1 analyst pass. Grounded in `kein-harness` git history, `descvi/repo` git history, `~/Documents/wiki/`, and the standing prompts themselves. No external prompt-writing material read.

---

## The short version of what the evidence changed

§1 says the ratchet exists because removal requires an expensive warrant (proof a failure no longer recurs) that nobody collects. **The repos contain many removals from standing prompts, and none of them used that warrant.** They used six or seven other warrants, all cheap, all one reading or one grep. So the ratchet is real but its stated cause is wrong, and the deliberations that follow are about *which warrant applies*, not about affording an experiment.

Two measured counters worth putting up front:

- `descvi/repo` `AGENTS.md` — the longest-lived standing prompt available, 25 revisions over 11 weeks — **does not grow monotonically.** It grows in runs and then drops sharply at structural events: 16,710 B → 6,333 B (`b7cbb70`, 2026-07-12, "213 lines -> 68"), 9,511 → 9,111 (`be1b2fa`, 2026-08-04), 11,261 → 9,072 (`a995bba`, 2026-08-10). Between those events it does ratchet: 6,411 B on 2026-07-18 to 11,261 B on 2026-08-07, +76% in three weeks, every intervening step an increase.
- `reference/kickoff.md` (10,344 B) was cut to `~/.claude/kein/prompts/lead.md` (4,386 B) in one pass on 2026-08-08/09 — a 58% reduction, no ablation, no recurrence proof (`~/Documents/wiki/_raw/note/260809-rewriting-standing-agent-prompts-on-measurement.md`).

So the working question is not "how do I afford removal" but "which of the cheap removal warrants is the one I actually have, and am I deleting or relocating?"

---

## D1. On what ground am I cutting this line?

**The question:** name the removal warrant before writing the diff. §1 assumes there is exactly one and it is unaffordable. The repos show at least seven, each settled by an artifact you can produce in minutes.

**What settles it** — pick one and produce the evidence it names:

| Warrant | What settles it | Evidence |
| :--- | :--- | :--- |
| **No consumer** | grep for what reads the thing the rule requires; find nothing | `7b3a350` "stop requiring records nothing reads" — `executor@codex` had nowhere to go and nothing would have read it. `399b26b` — `created_at`/`updated_at` required in three schemas, "no code read either one" |
| **The cause is gone** | show the condition that motivated the rule no longer holds | `b7cbb70` — the quality-conventions section existed because codex workers read only `AGENTS.md` and never saw the dev guidelines; once the guidelines *became* `AGENTS.md` the section went. `9d79fdd` — the six-skill ceiling was a v1 scoping device and v1 was done |
| **Subsumed by a more general line already present** | quote the surviving line and show the specific case re-derives from it | `9d79fdd` — "the line right above the scope list already carries the real constraint". The note's table — "scope discipline — cut, 11/14 canonical prompts already carry it" |
| **Unnecessary by construction** | show the mechanism now refuses the thing the prose forbade | `a2ab0b4` — "Three instructions disappeared into structure rather than being cut for brevity": `plan`'s template knows only `Draft`, and `ocs state plan` already errors, so the paragraphs defending both are unnecessary |
| **Compliance produces false data** | exhibit an artifact where following the rule made something wrong | `399b26b` — "One shipped receipt records a completion nine hours before its own run started, at an exact UTC midnight: the value was invented rather than measured." `736cc30` — widening the instruction check "turned a correct pass into a false failure" |
| **The rule contradicts its own enforcement** | show the validator refusing what the prose promises | `7b3a350` — `:advisory` "was promising semantics its own validator contradicted"; execute's verdicts are a list and `state.py` blocks on any `MUST_FIX` |
| **Over-generalised from the founding incident** | show the incident and the strictly narrower rule that covers it | `ca1c7e9` — purpose.md rule 1 banned all writes into the target repo; "that over-generalized 'omc leaves too much behind': the objection was always the hook-generated `.omc/state/`". `0879ea7` "Dropping `model:` was over-applied on my part." `b4585d3` overturns purpose.md order item 6 |

**Where the framing breaks:** §1's "removing needs proof a failure no longer recurs" describes only ablation. Ablation is the warrant for one narrow case — a rule whose *only* defence is that it changes model behaviour. Most lines in a standing prompt are not that; they are lookups, restatements, scaffolding for a condition that has since changed, or requirements on a consumer that does not exist. Those have documentary warrants.

---

## D2. Am I deleting this, or moving it?

**The question:** what is the destination file, and who reads it?

This is the deliberation §1 misses most completely. **Nearly every measured shrink event in the evidence is a relocation, not a deletion.**

- `b7cbb70` — implementation reference → `docs/architecture.md`, `.omc/` description → `.claude/CLAUDE.md`, two gate rules → the gates section. 213 lines to 68.
- `be1b2fa` — the hard-wrap rule promoted out of `descvi/AGENTS.md` into `~/.claude/CLAUDE.md`, where it still sits.
- `a995bba` — the enumerated gate list replaced by a pointer to CI's `verify` job. "The measured reasons behind the list were not deleted with it, they moved into `ci.yml`'s step comments."
- The 2026-08-09 note's git block: "the useful move was neither keep nor drop but **re-file**" — three editing-discipline rules had been "filed under 'restore' by accident" and moved out.
- `8297ce1` — the handoff skill's temp-directory instruction: "practice had already left the instruction behind", so the instruction moved to `<ocs state-dir handoff>/`.
- The note's `lead-omc.md` pass explicitly separates what it absorbed from descvi's `CLAUDE.md` from what it "deliberately **not** absorbed, and still needed where it is: … Those are project rules, not harness rules — moving them would promote descvi's optimisation into a global file".

**What settles it:** name the destination and confirm the audience that needs the rule actually reads that destination. The failure mode is documented and expensive: `3f310c6` — the background-report guard adopted in descvi on 2026-07-26 "did not come across in the port: neither `run_in_background` nor `SendMessage` appears anywhere in kein", and the identical failure recurred in kein on 2026-08-05, 135 turns producing nothing.

**The sharpest line in the evidence** is the note's: *"All the deleted messaging rules had real incidents behind them and were still wrong to write down at that altitude. **Having evidence does not establish altitude.**"* That inverts §1. The evidence attached to a rule answers "did this failure happen"; removal turns on "does this rule belong in this file", which is a different question that the incident log cannot answer either way.

---

## D3. Does this file declare what kind of content it holds, and does this line qualify?

**The question:** is there a stated admission rule for this file? If yes, removal is a type check, not an evidence problem.

**What settles it:** the scope line, applied to the candidate.

- `descvi/AGENTS.md:7` — "Keep it short: if something is a lookup ('where does X live', 'how is Y wired'), it belongs in a reference doc, not here." `a995bba` invokes exactly that line as its warrant, and adds the diagnosis: "the enumeration was a lookup; **that it lived there is why it rotted**."
- `lead.md:7` — "These hold regardless of harness, vendor, or project. **Everything below them is disposable.**" A declared tier boundary with a declared expiry.
- `descvi/docs/README.md` — "a subdirectory names the KIND of scope it holds", the rule that retired `docs/process/` on 2026-08-04 and sent process lessons to the wiki. Cited again in `reference/kickoff.md:31`.
- `docs/purpose.md` operating rule 1 — `docs/` "is reserved for reference documentation … rather than the output of a work session."

This is the cheapest removal mechanism in the whole corpus and it costs one reading. It is also the one §1 cannot see, because it never requires knowing whether a failure recurs.

**Rejected variant, worth recording:** a size or count budget does *not* work as a forcing function here. `9d79fdd` cut the six-skill ceiling because "keeping a number that the next proposal has to argue against turns a budget into a rule." A stated *kind* constraint cuts; a stated *quantity* constraint becomes another line to argue with.

---

## D4. Where does this rule's argument live, and what is it costing where it lives now?

**The question:** inline provenance, or a pointer to a durable store?

§1's own exhibit is §6's prescription — `reference/kickoff.md` carries a dated measurement on most rules — and that is precisely what got cut. The note: *"Roughly 60% of kickoff.md's bytes were dated incident narratives (`Measured 2026-07-26: …`). Those were cut entirely — the incidents already live in this vault, and a standing prompt needs the rule plus one clause of consequence, not its provenance. **Evidence accumulates without bound; rules do not.**"*

The same owner holds the opposite position elsewhere, and both are defensible because they are about different kinds of evidence:

- Narrative provenance → history / vault. `7b3a350`: "Each deletion leaves its reason behind. An absence invites the next reader to fill it back in; an argument does not" — and that argument is in the *commit message*, not the file. `lead.md:42` routes lessons to `/wiki-record`, "not in this repository."
- Runnable evidence → beside the rule. `.agents/kein/requirements/260810-skill-measurement-program.md:76` — "`evals/` inside a skill despite being unlike its neighbours … keeping a rule's evidence beside the rule is what makes deleting the rule an ordinary review rather than archaeology."

**What settles it:** whether the argument is re-runnable. A rubric or eval that can be executed belongs beside the rule; a story about one Tuesday belongs in history with a date and one clause of consequence in the file.

**A checkable structural fact that bears on this, which I found and which §1 does not mention:** every standing prompt in this system is outside version control. `reference/kickoff.md` and `reference/worker-brief.md` are untracked (`git status` → `?? reference/`); `~/.claude/kein/prompts/lead.md` and `lead-omc.md` are under no repository; `~/.claude/CLAUDE.md` likewise. The note records the consequence: *"`reference/` in kein-harness is **untracked**, so the pre-rewrite `worker-brief.md` now exists nowhere."* Meanwhile the one prompt-like file *with* a commit history — `descvi/AGENTS.md` — is the only one observed to shrink repeatedly, and each shrink carries its argument in the commit message. **The correlation is real; the causal claim is mine and unproven.** See "What I could not ground".

---

## D5. What is this rule's decay class, and has the thing it depends on changed?

**The question:** what would have to change in the world for this rule to become false — model generation, harness build, vendor, project — and has it?

**What settles it** depends on which:

- *Harness fact* — settled by re-running the original probe. Cheap. `lead.md:28` pre-registers this: "Dated 2026-08-08, measured on Claude Code 2.1.226 with **agent teams disabled**. These are the lines most likely to rot; check them before trusting them." That block is quarantined precisely so it can be re-measured as a unit, and it is the block that *was* replaced wholesale: three of kickoff.md's five messaging bullets "had their premise removed outright", including "Nothing you send interrupts a working agent" (false with teams off) and "A background subagent's final plain text is NOT visible to you" (false — it arrives in the completion notification's `<result>` field).
- *Model tendency* — settled only by measurement, and this is where §2's objection genuinely bites. `~/Documents/wiki/harness/harness-obsolescence.md` claims "roughly half [of accumulated rules] end up guarding against mistakes the current model no longer makes", tabulates four capability shifts against the harness category each retires, and reports "One 200-line rule file was cut to 40 by asking, per line, 'why was this added? — if you can't remember, delete it.'" `context-engineering-claude-5.md` reports Anthropic deleting 80%+ of the Claude Code system prompt for the 5th generation with no coding-benchmark loss.

**Live disagreement in the owner's own material, and it is a real deliberation:** the wiki's audit protocol says *not remembering why a rule exists is itself the removal warrant* ("Prune oldest-first … if you can't recall why it exists, delete it and run a week without it"). §6 says the opposite — that nobody removes precisely because nobody remembers, and the fix is to make rules carry their arguments. Both cannot be the operating policy. The repos have used the wiki's version at least once, explicitly: `b7cbb70` — **"Re-add a rule if the problem actually recurs, rather than pre-emptively hard-coding a workaround for a split that no longer exists."**

---

## D6. Is the behaviour already produced without this instruction?

**The question:** would a control — a model with no such line, or the other files in the stack — produce this anyway?

This is the one removal warrant that is genuinely evidential, and critically **it is a positive test, not an absence test, so §2's objection does not reach it.** You are not showing a failure did not occur; you are showing the instruction is not what produces the behaviour.

**What settles it,** cheapest first:

1. *Grep the rest of the prompt stack.* Free. The 2026-08-09 note: "scope discipline — cut — 11/14 canonical prompts already carry it."
2. *Observe the behaviour arriving unprompted.* `8297ce1` — "The sample artifact organised itself into objective, start-here, authoritative artifacts, and current state with no template telling it to, **which is an argument against adding one**."
3. *Run the ablation.* It has been done once, successfully: `docs/prompt-porting-notes.md` — a three-line restoration of the Critic's severity floor and asymmetric-loss framing "produced no behavioural change across 5 replicates per variant, on a fixture where the plan pre-assessed a data-loss defect as minor under deadline pressure. Both variants returned MUST_FIX with the defect ranked first at critical severity in every sample." Conclusion drawn: "Persona-intensity language and severity scaffolding appear to be carried by current models without explicit instruction."

**The affordability problem §1 gestures at is real and is dated.** `ocs eval` was built (`e87d8e0` … `236d7ac`) and then paused: "each arm ran 35 to 40 minutes on the cheap fixture with everything pinned to Sonnet, and with-skill was killed at a 2400-second timeout. The primary fixture is more than twenty planning iterations, so it is not viable as designed."

**It is being fixed, today, in direct response to this document.** `.agents/kein/requirements/260810-skill-measurement-program.md` (Approved, 2026-08-10) cites `docs/prompt-revision.md` by name twice and states the reframe that dissolves §1's cost problem:

> "`docs/prompt-revision.md` argues that a standing prompt grows monotonically because adding needs one incident while removing needs proof a failure no longer recurs, and that nobody collects the second. **An assertion that passes with the skill and without it is exactly that proof: that part of the skill is doing nothing.** This program is how that evidence starts being collected."

Its acceptance criteria require ≥3 repeats per configuration, per-assertion classification across configurations where "passes in both" is reported as *the skill doing nothing there, not as a pass*, and an arm representation that admits a content variant later — "part of a skill's content present against absent is **the ablation that produces deletion evidence**." What made it affordable is stage decomposition, not a better instrument: measuring `plan` alone rather than a full draft-review-revision round.

Its own recorded risk is the honest boundary: "A control lead may well produce the same headings and status fields a skill asks for, in which case those assertions pass in both configurations. That is a real result about those instructions rather than a broken measurement."

---

## D7. Is the failure this rule prevents loud or silent — and does that answer change on the removal side?

**The question:** filter 1 from the 2026-08-08/09 diet — "the failure it prevents is **silent** — no error, no red gate, no output that looks wrong."

The note reports this as the strongest of its three filters and reports a finding it did not plan: "Every rule that survived this pass turned out to be of the 'green but wrong' kind, which was not planned and is probably the useful generalisation."

**The deliberation §1 should have reached and did not:** silence does double duty, in opposite directions.

- A *silent* failure is what makes a rule worth writing (nothing else will teach the agent).
- A *silent* failure is also what makes the rule impossible to cut-and-see, because you will not notice the recurrence.

So the real asymmetry is not addition-vs-removal cost in general. It is that **the class of rules worth having is exactly the class whose removal cannot be tested by removing it.** For a loud failure, "cut it and re-add if it recurs" (`b7cbb70`) is a complete and free policy. For a silent one it is not available, and either an ablation (D6) or a documentary warrant (D1) is the only route.

**Directly checkable falsification of §1's exhibit sentence.** §1 says `reference/kickoff.md` "still had no line anyone could argue for cutting." Its own line 29 — "Kill dev servers before a full-suite test run that shares a port with another suite" — appears in the note's worked-example table scored `silent: ✗` with the verdict "**cut — you find out immediately**". It also fails §4's own stated third filter (survives a change of harness, vendor, and project). Same corpus, same week, and the note's diet deleted three further bullets outright. `reference/kickoff.md` additionally cites at least six referents that do not exist in this repository: `docs/prompt/worker-brief.md`, `.omc/archive/`, `.omc/plans/`, `.claude/skills/kickoff/templates/process-lessons.md`, `docs/README.md`, and the skills `2plan` / `2ralph` / `2execodex`. A rule whose referent is gone is a cut anyone can argue for at zero cost (D1, "the cause is gone").

---

## D8. Is my addition gate one I can actually pay — and is it the same instrument as my removal gate?

**The question:** §1 treats addition as ungated. In `kein-harness` it is gated, on paper and in practice, and the gate has fired.

Standing addition gates that exist:
- `docs/purpose.md` operating rule 3 — "**Prove before adding.** New prompt rules earn their place by differential evaluation, not by precedent."
- `docs/purpose.md` non-goals — "Restoring prompt material because an upstream harness had it"; hooks start at zero and "adding one requires naming the failure it prevents **and how its misfire would be detected**."
- `docs/prompt-porting-notes.md` — "A gap found by reading two prompts side by side is a hypothesis, not a defect … do not restore them into kein on the strength of 'OMC had it'."

Additions actually refused:
- `736cc30` — widening the instruction check to cover `~/.claude/CLAUDE.md` "was tried and reverted": it "turned a correct pass into a false failure — the same false negative this check's own comments already warn about twice."
- `e37d5c4` — "A shared worker brief was considered and declined."
- `8297ce1` — a template refused because the artifact self-organised without one.

**But the gate that fired was argument, not measurement,** because the measurement was unaffordable from 2026-08-05 to 2026-08-10 (`236d7ac`). **An unaffordable gate is not a gate; it silently converts into whatever the author will argue for.** That is a better statement of the ratchet than §1's, and it generalises: the prompt drifts in whichever direction the *cheaper* gate points. The 260810 program closes this by making addition-evidence and deletion-evidence stages of one instrument (arms grow: present-vs-absent → content-ablation → cross-harness).

---

## Where §1 is wrong or incomplete

1. **Wrong about the removal standard.** "Proof a failure no longer recurs" is the standard for one narrow rule class (behaviour-changing instructions). The repos removed prompt material at least a dozen times on documentary warrants that cost one grep. `b7cbb70`, `7b3a350`, `399b26b`, `a2ab0b4`, `9d79fdd`, `a995bba`, `be1b2fa`, `ca1c7e9`, `0879ea7`, `b4585d3`, `8297ce1`, plus the whole 2026-08-08/09 kickoff diet.

2. **Its exhibit sentence is false.** `reference/kickoff.md` had cuttable lines — one is scored `cut` in the same week's own worked-example table by the same filter set §4 quotes, three bullets were deleted outright when their premises were falsified, ~60% of its bytes were provenance that was cut wholesale, and it cites at least six referents that no longer exist.

3. **It conflates deletion with relocation.** Every large measured shrink in the corpus was a relocation, a promotion, or a dedup. The operative question is "which file", not "keep or cut". "Having evidence does not establish altitude" is the finding §1 was one step away from.

4. **It doesn't notice the scope-line mechanism.** A file that declares what *kind* of content it holds gets a removal test that costs one reading and needs no failure data at all. `descvi/AGENTS.md:7` and `lead.md:7` both do this, and `a995bba` cites the scope line as its warrant.

5. **The asymmetry is misdiagnosed.** The real asymmetry is that the rules worth having are the ones guarding silent failures, and silent failures are exactly what cut-and-see cannot detect. §1's version (cheap to add, expensive to remove) is a special case of that.

6. **"Nobody collects that" was true for five days and is no longer.** `.agents/kein/requirements/260810-skill-measurement-program.md` cites this document and specifies the instrument, with the cost problem solved by stage decomposition rather than by a cheaper measurement. §1's diagnosis was load-bearing enough to produce its own remedy; the note should probably record that the sentence has an expiry.

7. **It doesn't ask whether the addition gate is payable.** The stronger general claim: a prompt ratchets in whichever direction has the cheaper gate. When addition is gated by an unaffordable eval and removal by an argument, you get the *opposite* ratchet — and `b7cbb70`'s 213→68 is what that looks like.

**What §1 gets right and the evidence confirms.** The ratchet is real *between* structural events: `descvi/AGENTS.md` +76% in three weeks with no intervening cut, and `docs/purpose.md` grew rules from three commits' worth of incidents without any of them being revisited until a Planner reading it for an unrelated reason reported a violation (`9d79fdd`). Incidents genuinely are cheap and continuous — the owner's own framing, quoted in the note: "세세한 건 끊임없이 나온다."

---

## What I could not ground

- **The core causal claim I am tempted to make — that a standing prompt ratchets because it has no version history to carry its argument — is mine, not the evidence's.** The correlation is real and checkable: `reference/kickoff.md`, `reference/worker-brief.md`, `~/.claude/kein/prompts/*.md` and `~/.claude/CLAUDE.md` are all outside version control and none has a recorded shrink; `descvi/AGENTS.md` has 25 tracked revisions and four recorded shrinks. But n=1 on each side, different authors' attention, different ages, and the untracked files are also the *newest*. **What would change my mind:** putting `reference/` under version control and watching whether removals start appearing with arguments — or finding a tracked standing prompt elsewhere that still ratcheted monotonically, which would kill it.

- **I could not verify the ratchet claim on `lead.md` at all.** It is two days old, untracked, and the note says it is "a first draft and the user has deliberately paused it." Whether the post-diet prompt starts growing again is the actual test of §1 and it has not been run.

- **I could not find any case of a removed rule being re-added after a recurrence** except `3f310c6`, and that one is a rule *lost in porting*, not a rule deliberately cut. That matters: it is the only recurrence datum in the corpus, and it came free — the failure simply happened again and was measured. So "nobody collects recurrence data" is not quite right either; the collection mechanism is suffering the failure, and nobody *schedules* it. But one instance is not a base rate, and the note itself records why a base rate from one event is a defect (`f364bc11`: "I WITHDREW A FREQUENCY I WROTE THIS MORNING … One event in a small sample is not a rate").

- **I could not test whether the seven removal warrants in D1 are exhaustive**, or whether they generalise past this owner's two repos. They are what these repos used, read off 25 commits. A larger corpus might collapse them or add more.

- **I did not read** `~/.claude/plugins/**`, any external prompt-writing advice, or `skill-creator` itself, per the boundary. `skill-creator` is described second-hand in `260810-skill-measurement-program.md:83`; I took that description as evidence about the owner's design decisions, not about `skill-creator`.

- **`docs/prompt-revision.md` cites a "dated measurement on nearly every rule" in `kickoff.md`.** By my count 10–11 of the 16 Discipline bullets carry `Measured YYYY-MM-DD`. The six that do not (lines 16, 19, 27, 28, 29, 30) are precisely the ones the diet cut or demoted. That is suggestive — undated rules are the cuttable ones — but it is a post-hoc reading of one file, and the diet also cut heavily-dated rules on altitude grounds, so it is not a rule I would write down.
