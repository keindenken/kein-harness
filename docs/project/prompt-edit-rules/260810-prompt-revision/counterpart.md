# §4 — what the rule costs when it is wrong

Stage-1 analyst note. Grounded in `kein-harness` git history, `descvi/repo` git history, `~/Documents/wiki/_raw/note/`, and the current standing prompts (`reference/kickoff.md`, `reference/worker-brief.md`, `~/.claude/kein/prompts/lead.md`, `descvi/repo/AGENTS.md`, `docs/purpose.md`).

## 0. What the heading actually contains

The heading bundles three claims that behave differently and should be separated before anything is written:

1. **The existing filters test the failure, not the rule.** True, and the evidence is that all three filters in the 2026-08-09 note ask about the *incident* (is it silent, is it derivable, does it survive a change of harness) and none about the *rule's own behaviour once installed*.
2. **A rule with no visible downside usually has an unfound one.** Well supported here — six cases below — but the reason is sharper than the heading gives. The cost of a *prohibition* is a counterfactual: it lands on work that never gets attempted, so it cannot be observed by watching. It is revealed only by someone attempting the forbidden thing. That is why it stays invisible, and it also says what to do about it (schedule an attempt) rather than merely warning.
3. **Widening an existing rule is a compression rather than an addition.** This is the weakest of the three and I think it is partly wrong as stated. Widening is *less visible* than addition, which is not the same as cheaper. See §3.

## 1. The deliberations

Each is stated as a question someone has to answer, with what would settle it and where the repo already paid for the answer.

### D1. What behaviour does this rule forbid that you would actually want?

**Settles it:** write down the best action a strong agent would take in the situation the rule covers, then check whether the rule scores that action as compliant. If the best available behaviour fails the rule, the rule is wrong at its boundary, not at its centre.

This is the single most productive question in the whole corpus. It has fired three times in our own material and it fired the same way each time — the rule punished the *better* artifact:

- `8d8cee6` — the check demanded a verbatim line from the repository instructions. The lead's brief carried a digest plus a pointer, which is the better artifact and which the lane reference had never asked to be pasted. The check scored it as "no briefing at all".
- `736cc30` — the same check, widened to cover `~/.claude/CLAUDE.md`, was tried and reverted. The first observed team run "carried those conventions faithfully, as a paraphrase, which is what a lead should do". Substring matching read the paraphrase as omission. Note the detail that matters most: the commit says this is "the same false negative this check's own comments already warn about twice". A written warning did not prevent it. Only the run did.
- The self-approval rule (2026-08-09 note). "Never self-approve, including your own rulings" was read by the user as forbidding a fast plan skill with no review lane. Correct objection — and the skill it forbade was then built (`0b593e4`, `a2ab0b4`). The rule's cost was one whole workflow, unpaid for months, discovered by a use attempt.

**Corollary for prohibitions.** Because the cost is counterfactual, "we have not seen a problem" is not evidence about a prohibition at all — it is the expected observation whether the rule is right or wrong. The only settling evidence is an attempt.

### D2. If the rule requires something to be produced, who reads it?

**Settles it:** name the consumer — code, a later stage, or a human decision. If nothing reads it, the requirement buys nothing and costs whatever fabrication it induces.

- `7b3a350` — Execute's reference required the lead to record `executor@codex`. `TASK_FIELDS` is checked by exact set equality, so **a lead that complied would have written an invalid state**. The requirement was cut rather than given a slot, because "`reconcile` resolves continuation without the Executor's vendor, acceptance judges the worktree rather than its author". The commit's own summary is the reusable form: *a state that grows a field per fact nobody reads costs more than the fact is worth.*
- `399b26b` — `created_at`/`updated_at` were required in every nonterminal state and no code read either. The cost was a clock call per update, "and a model has no clock". One shipped receipt records a completion nine hours before its own run started, at an exact UTC midnight — invented rather than measured. **A required field an agent cannot honestly fill is a fabrication generator.**

### D3. What does this instruction displace?

**Settles it:** a behavioural probe on something the reader previously did correctly — never the reader's self-report.

- `98b2fe8` — setting Codex's API-level `instructions` replaces the vendor's own operating manual instead of adding to it. Measured: with `instructions` set, the worker "no longer knew to prefer `rg` and invented 'Resource templates over web search' in its place. Editing still worked, so this would have degraded quietly." The Claude side found the same thing independently: `--agent` overrides the system prompt.
- `260801-lead-only-context-channels.md` — `CLAUDE.md` is inherited by subagents, so lead-only discipline placed there "burns worker context on rules that do not apply to them".
- §3 of the note (attention, not tokens) is the general form. What makes D3 answerable rather than hand-waving is that displacement is measurable behaviourally.
- **Do not use introspection to answer this.** The 2026-08-09 note records two consecutive confident denials, by a session, that content demonstrably present in its own appended system prompt was there — with a confident inventory of what it claimed to see instead. "Introspection about one's own system prompt is not evidence."

### D4. What fact makes this rule true, and what would falsify that fact?

**Settles it:** name the premise and where it is measured. A rule whose premise died is pure cost.

- `b7cbb70` (descvi) — a whole quality-conventions section existed only because codex workers read `AGENTS.md` and never saw guidelines living in `CLAUDE.md`. Once the guidelines *became* `AGENTS.md`, the cause was gone: "Re-add a rule if the problem actually recurs, rather than pre-emptively hard-coding a workaround for a split that no longer exists."
- The 2026-08-08 message-delivery measurements deleted three of `kickoff.md`'s five messaging bullets outright — the premise, not the wording, was false. "Nothing you send interrupts a working agent" is false with teams off; the asymmetry paragraph and the rule built on it went with it.
- `~/.claude/kein/prompts/lead.md` now has the mitigation built in: a dated **Harness facts** block, teams-disabled stated, and the line "These are the lines most likely to rot; check them before trusting them." Fact-shaped rules get an expiry; behaviour-shaped rules do not need one.
- `b4585d3` + `purpose.md` item 6 — a non-goal ("reimplementing Orca's orchestration runtime, or shadowing the `orca` executable") read as forbidding *composition*. It was amended because "neither knew that a lane's model was unreachable through Orca's own launch". The premise was not false when written; it was incomplete, and the missing fact was only discoverable later.

### D5. Could a mechanism hold this instead of the prose?

**Settles it:** can a config field, a tool list, a template, or a validator make the violation unrepresentable? If yes, the prose form's benefit is duplicated and its attention cost is pure.

- `docs/prompt-porting-notes.md` — `sandbox_mode` moved out of prose into agent config, "so read-only is enforced by the runtime rather than by instruction… the Claude equivalent is the agent's `tools` list, not a sentence in the prompt body."
- `a2ab0b4` — "Three instructions disappeared into structure rather than being cut for brevity." `plan` cannot produce a gated-looking artifact because its template knows only `Draft`; `ocs state plan` already fails with a clear message. The defending paragraphs became unnecessary.
- The negative case is equally instructive and is already written down. `lead.md` rule 9: "Nothing in the harness enforces this — a subagent has the spawn tool with no depth guard — **so the brief is the only place this rule exists.**" That clause is what a discharged D5 looks like in shipped prose.

### D6. If you cut it, where does the cost land?

**Settles it:** name the party who now pays, and ask whether they can detect the situation at all. A cut that relocates a cost onto someone who cannot see the trigger is not a cut.

- The 2026-08-09 note, on replacing the two `git checkout` restore rules with "stop and ask the lead": rejected on two arguments, the decisive one being that **a worker cannot tell whether it restored correctly, so it cannot know it is in a situation worth asking about.** The other: the rules do not disappear under that scheme, they relocate to the lead.
- `a995bba` (descvi) — the gate enumeration was cut from `AGENTS.md`, and "the measured reasons behind the list were not deleted with it, they moved into `ci.yml`'s step comments". A deliberate relocation, named.
- `7b3a350` closes with the general form: "Each deletion leaves its reason behind. An absence invites the next reader to fill it back in; an argument does not." That is §6 of the note reached from the cost side.

### D7. Who else reads this file, and what does the rule cost them?

**Settles it:** enumerate the readers of the surface, and mark the ones the rule does not apply to. If more than one audience reads it, the conditionals in the text are an artifact of the file, not of the rule.

- `260801` — `CLAUDE.md` reaches every subagent by design; there is no project-level lead-only channel through it.
- `736cc30` — `prepare_config_home` does **not** isolate `~/.claude/CLAUDE.md`, so "a planning rule added there reaches the control arm too and would move a comparison without the fixture or the skill moving". A rule can silently contaminate a measurement of itself.
- `e87d8e0` — the eval fixture's `CLAUDE.md` carried a delimited OMC block restating in prose the invariants `ralplan` enforces, so "a control arm that keeps it is not skill-absent". Prose rules leak across boundaries that plugin toggles respect.
- The 2026-08-09 note's own open item: the worker rules are one file serving read-only roles, write-capable roles, and Codex at once, and "the conditionals in the file exist only because one file serves three audiences; rendering deletes them mechanically."

### D8. What does this contradict once it lands — and which document is nearer the reader?

**Settles it:** grep every other standing surface for the same subject before shipping, and check the *nearest* document to the reader first, because that is the one that wins.

- `7b1c9d2` (descvi) — `.claude/CLAUDE.md` routed `2plan` through `/plan --consensus`, which `2plan/SKILL.md` forbids in bold, with a specific reason (parallel independence). "Following the pointer means instructing a worker to violate the skill it was told to follow." Measured, not reasoned: the session did exactly that and the user caught it.
- `a995bba` — the codex commit-brief template prescribed `pnpm -r typecheck` and `pnpm -r lint`, "the exact two forms `AGENTS.md` forbids in bold… Codex reads only `AGENTS.md` and the brief, so a whole vendor's workers were being told to run gates that cannot go RED, **by the more proximate of the two documents**."
- `kickoff.md` already carries this move one level down — after a ruling, grep the plan for every claim whose *cause* the ruling moved. D8 is that rule applied to standing prompts, which is where nobody currently applies it.

### D9. Does the document obey its own rule?

**Settles it:** apply the rule to the file that contains it. Cheap, and it has caught three real defects.

- `9a4e744` (descvi) — "retire the counts a file banned in the sentence that banned them". A comment saying NO CONCRETE COUNTS ARE QUOTED HERE ON PURPOSE carried phase-23 arithmetic that a later phase falsified. "The rule is right, was violated by its own statement, and the violation is the second generation of the rot it was written to end."
- `565a6b0` — the citation audit "committed the class it exists to fix, in the paragraph teaching what went wrong". Its resolution is a structural stopping rule rather than more care: every number is either regenerable by a published command or anchored to an immutable object; a number that is neither gets **deleted, not corrected**.
- `4690908` — "This is the file that says a gate must be able to go RED, so it should not be the file naming a gate that cannot."

### D10. Is the rule correct but insufficient — does it buy false confidence?

**Settles it:** ask what a reader who follows it exactly still gets wrong. A partially-correct rule is worse than none where the reader stops looking.

- `09825ed` (descvi) — the worker brief's restore rule said the snapshot must be "younger than the work". That "holds only at the instant the snapshot is taken; a review lane whose subject is still being written can hold a snapshot that was fresh when made and stale when used. It happened — `cp` restores put a stale copy back at least twice over a teammate's newer work, and the live tree survived only because the last write landed after the last restore."

### D11. What does it cost, in units you can state?

**Settles it:** state both sides in the same currency. A discharged counterpart reads as a priced comparison, not as an assurance.

Worked examples already in this repo, all three of them counterparts *named and priced at or near zero*:

- `ralplan/SKILL.md:31` and `execute/SKILL.md:24` — `run_in_background: false` is required, and the obvious objection (loss of concurrency) is answered mechanically: "synchronous dispatch still runs them concurrently, so nothing is lost by not backgrounding them."
- `d46e9ca` — `references/lanes.md` is the first conditional reference, "read only when a flag names a vendor, so **a native run pays nothing for it**." The attention cost is made conditional rather than argued away. The trigger stays in `SKILL.md` because "a lead that never learns the flag exists will ignore it — that is what happened to `/ccg` under omc", which is the price of the alternative, also stated.
- `9df93e9` (descvi) — the whole-set audit rule ships with both sides in one sentence: "Cost of auditing per landing is one lane; cost of auditing at the end is re-opening a phase you called done."

## 2. Cases where a rule's cost showed up later

| Rule | Cost, when it surfaced | Where |
| :--- | :--- | :--- |
| "Never self-approve, including your own rulings" | Forbade a gate-free `plan` skill; axis had to move to "what reaches code was seen by someone who is not you" | wiki `260809-rewriting-standing-agent-prompts-on-measurement.md`; the skill then built in `0b593e4`, `a2ab0b4` |
| Brief must carry the repository instructions (as a check) | Scored a digest-plus-pointer — the better artifact — as no briefing at all | `8d8cee6` |
| …the same check, widened by one file | A faithful paraphrase read as omission; correct pass turned into false failure; reverted | `736cc30` |
| …the same check, from the other side | Demanded instruction files from a repository that has none | `ab698cc` |
| Record `<role>@<vendor>` for the Executor | Complying would have written a state the validator rejects; nothing reads the field | `7b3a350` |
| `:advisory` in Execute | Promised semantics Execute's own validator contradicted (verdicts are a list; any `MUST_FIX` blocks) | `7b3a350` |
| `created_at` / `updated_at` required | A model has no clock; a shipped receipt records completion nine hours before its run started | `399b26b` |
| Six-skill ceiling in `purpose.md` | A scoping number became a rule the next proposal had to argue against; a Planner reported a false violation | `9d79fdd` |
| `purpose.md` Orca non-goal | Read as forbidding composition rather than shadowing; blocked the only place a lane's model can be pinned | `b4585d3`, `purpose.md` item 6 |
| `AGENTS.md` naming the gate set as a prose list | Drifted; named a command that cannot go RED on `src/app`; a vendor's whole worker population briefed to run it | `4690908`, `a995bba` |
| Codex API `instructions` used to carry role identity | Replaced the vendor's operating manual; the worker lost `rg` and invented a substitute; editing still worked, so it degraded silently | `98b2fe8` |
| `2plan` pointer in `.claude/CLAUDE.md` | Told workers to run the skill that forbids it, with a specific structural reason | `7b1c9d2` |
| Restore rule "younger than the work" | True at snapshot time only; stale restores landed over newer work twice | `09825ed` |
| "No concrete counts here" comment | Carried counts; violated itself twice over four phases | `9a4e744` |
| Rules written for the `AGENTS.md`/`CLAUDE.md` split | Outlived their cause; the split was fixed at the root and the rules stayed | `b7cbb70` |
| `kickoff.md` messaging bullets (three of five) | Premise removed outright by the 2026-08-08 measurement | wiki `260809-…measurement.md` |
| "Kill dev servers before a full-suite run" | Guarded a loud failure — cut on filter 1 | same note |
| "Scope discipline" | Already carried by 11 of 14 canonical prompts — pure duplication cost | same note |
| "After you ask, STOP" | Measured false | same note |

Two more that are the same shape but land on a *measurement* rather than on an agent: `e87d8e0` (a prose CLAUDE.md block restating `ralplan`'s invariants would have collapsed the control arm) and `236d7ac` (a task sentence telling arms to follow existing plan conventions "handed the control a template, and the template is part of the treatment").

## 3. On "widening is a compression, not an addition"

Half true, and the failing half is documented.

**Widening that is genuine compression:** `d46e9ca` generalized "both lanes" to "every lane" in the skill body and the review contract, because a role with two vendors makes three lanes and "if both lanes return PASS" would otherwise approve on two of three. The extension grew only over cases the rule already meant to cover. Cost: zero. This is the clean case.

**Widening that is a disguised addition:** `736cc30` widened the instruction check by exactly one file and had to be reverted, because the wider boundary landed on behaviour that was correct. Nothing was added by line count; a whole class of correct runs became failures.

**Compression that silently moved the boundary:** the self-approval rewrite is a compression — several surface rules collapsed to "what reaches code was seen by someone who is not you" — and the collapse *changed which behaviours are forbidden* (the user's own approval now counts; a worker implementing the lead's prescription does not). That change was the point, but it was invisible in the diff of the rule's own words.

The correction I would make to the heading: **widening is cheaper in attention and more expensive in review, and those are different budgets.** It escapes the ratchet's addition cost precisely by escaping the review that an addition would get. So the deliberation is not "can this be widened instead" but:

> **D12. Enumerate the cases the wider form now covers that the narrower one did not. Which of them would you refuse?**

Settled cheaply where a fixture exists — `4122b43` verified five checks against synthetic worktrees before spending a real run, and `6dd0785` ran a ten-case matrix over rosters before shipping the keyed-verdict widening. Settled expensively for prose, which has no fixture, and which is exactly why the prose widenings above were caught by a live run or a user objection rather than at authoring time.

## 4. Is "name the counterpart" usable as a test?

**As written in §4, no. It is a warning.** "Name the opposing instruction, or what is gained by not having this one" has no discharge condition and no failure state — a sentence can always be produced, and the sentence produced at authoring time is not the sentence a run produces. Every cost in §2 above was found by a run, a use attempt, or a reader objecting — not one by introspection at the moment of writing. `736cc30` is the decisive evidence: the check's own comments already warned about that exact false negative *twice*, and the widening happened anyway.

**Three narrower forms are usable, because each has a state in which you cannot answer:**

1. **Name the consumer** of anything the rule requires be produced. Fails loudly on `7b3a350` and `399b26b`. Answerable at the desk.
2. **Name the best behaviour** in the situation the rule covers, then check the rule scores it a pass. Fails loudly on `8d8cee6`, `736cc30`, and the self-approval case. Answerable at the desk, and it is the highest-yield of the three.
3. **Name the mechanism** that could hold this instead of the prose — a config field, a tool list, a template, a validator. Fails on `sandbox_mode`; discharged explicitly in `lead.md` rule 9 and in `a2ab0b4`.

**And one scheduling move for the residue.** Prohibitions cannot be tested at the desk, because their cost is counterfactual. The usable form is not a better question but an occasion: a prohibition ships with the attempt that would reveal its cost named, and that attempt is what gets re-run. This is also the missing half of §1's ratchet — removal has no occasion today, and a pre-named attempt is one.

**Worth knowing: this repo already has one counterpart clause in a standing document**, and its phrasing is better than §4's. `docs/purpose.md`, Non-goals: *"Hooks. Start at zero… Adding one requires naming the failure it prevents **and how its misfire would be detected**."* That is the counterpart expressed as detectability of the misfire, which does have a failure state. Zero hooks exist, so the clause has never been exercised — I could not check whether it works, only that it is the strongest phrasing in our own material.

## 5. What I could not ground

- **No case where naming the counterpart at authoring time caused a rule to be rejected.** The closest are `236d7ac` and `e37d5c4`, where a shared worker brief was "considered and declined" because it would shrink the difference the calibration exists to establish — but that is an experiment-design decision, not a prompt rule. `b7cbb70` rejects a re-add on premise death, not on cost. So the *preventive* value of D1–D12 is unevidenced; what is evidenced is their diagnostic value once the cost has landed.
- **No denominator for "usually has an unfound one."** I have sixteen positive cases and no count of rules that never developed a cost. Two long-lived rules with no observed downside — "a gate must be able to go RED" and "a zero result needs a calibrated instrument" — suggest the word "usually" is doing unearned work. My tentative discriminator is that both of those *require evidence before belief*, so their cost is paid per-use, visibly, and cannot hide; whereas a prohibition's cost lands on work that never happens. That discriminator is a hypothesis, not a finding.
- **The strongest cases are checks and validators, not prose.** `8d8cee6`, `736cc30`, `399b26b`, `7b3a350` all surfaced because a machine scored the behaviour and disagreed with a human reading it. Prose rules in `kickoff.md`, `AGENTS.md`, and `purpose.md` surfaced only via a person noticing (`9d79fdd` a Planner's report, self-approval a user objection, `7b1c9d2` the user catching it). Whether any desk-time test works on prose *without* a fixture is not settled by this material.
- **The "attention" cost of §3 is asserted, never measured here.** The one relevant measurement points the other way: porting the Critic from 3,047 words to 1,115 changed no behaviour, and a three-line restoration changed nothing across ten samples under deliberate pressure (`docs/prompt-porting-notes.md`, `docs/purpose.md`). Displacement is measured only in the Codex `instructions` case (`98b2fe8`), where the mechanism is replacement, not competition.
- **Deliberately not read**, per the stage boundary: `~/.claude/plugins/`, any external prompt-writing guidance, and `~/Documents/wiki/context-engineering/context-engineering-claude-5.md` plus `prompt-engineering-foundations.md` — the wiki is in scope, but those two are digests of vendor guidance and reading them would contaminate the later stage's measurement.

**What would change my mind:**

- A record of a rule *rejected before being written* on a cost argument, which would move D1–D12 from diagnostic to preventive.
- A case where a counterpart argument produced a *false* cut — a rule removed on its stated cost whose failure then recurred. That is the failure mode this heading has no defence against, and its absence in the record may only mean nobody has tried.
- A prose rule whose cost was found at the desk rather than by a run. One instance would make the desk-time forms in §4 usable for `CLAUDE.md`, not only for validators.
- A count of standing rules that never developed a cost, which would settle whether "usually" survives.
