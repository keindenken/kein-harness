# §2 — Absence of failure is not evidence: the deliberations underneath it

Stage-1 analysis. Grounded in kein-harness (`docs/`, `plugin/skills/`, git history), `reference/kickoff.md` and `reference/worker-brief.md`, the owner's wiki (`~/Documents/wiki/_raw/note/`), descvi (`AGENTS.md`, `docs/known-issues.md`), and `~/.codex-orca/docs/superpowers/verification/agent-prompt-evals.md` (our own measurement record, not external advice).

The document's §2 is two claims stacked: *a clean run is a weak observation*, and *a dirty run is not automatically a mandate*. Read against our own evidence, they are not two topics — they are two terms of one calculus, and the project has already worked that calculus several times without naming it. What follows are the questions those worked cases actually required someone to answer.

---

## 1. In how many of those clean rounds was the guarded state even entered?

**The question.** "Five clean rounds" is a denominator. The numerator that matters is not *failures observed* but *entries into the state the rule guards*. A rule guarding a rare state observed over rounds that never entered it has been observed zero times, not five.

**What settles it.** An instrument that counts entries into the guarded state independently of the outcome — and that has been shown able to produce a non-zero count.

**Evidence.**
- The doctrine already exists, written into `reference/worker-brief.md` verbatim: *"A zero result is evidence only once you have shown the instrument can produce a non-zero one. Plant the signature you are hunting and confirm the search finds it. An instrument that cannot tell its own silence from its subject's has measured neither, and it reads as the answer you expected."* Its origin is `~/Documents/wiki/_raw/note/260805-a-zero-that-proves-nothing.md` §1 — a grep over 83 logs returned exactly one hit, and *that one hit* is what made the other 82 zeros mean anything.
- The negative case, same note §2: descvi's restore probe had a three-way verdict, a liveness control, and a forced-RED calibration, all downstream of an `await` that never executed on a failing sample. The calibration itself had been taken on a *passing* run. Every layer of rigour was applied to a branch validated in the one state it never occupies.
- The strongest single instance is descvi KI-34 (`docs/known-issues.md`). Three CI probe runs were needed to ask a question that could answer anything: run `31358766473` measured nothing (Vite bound `::1`, the probe polled `127.0.0.1`), run `31359914068` measured the rename's *cause* rather than its *symptom*, and only run `31363862442`, which added two chained post-rename writes, asked the answerable question. Two of three attempts produced numbers that looked like data.

**Why this belongs in a prompt-revision deliberation.** For a prompt rule, nothing counts guarded-state entries at all. See §11.

---

## 2. Is the state rare, or merely unobservable *here*?

**The question.** Rarity and unobservability produce the same clean run and demand opposite responses.

**What settles it.** A source-level argument about whether the mechanism can fire in the environment doing the observing.

**Evidence.** KI-34 again: on macOS `fs.watch` is FSEvents-backed and path-resolved, so the rename mechanism cannot fire at all. The entry says so plainly — *"macOS에서는 여전히 못 잰다 … 이 저장소의 로컬 개발에서는 여전히 노출이 0이고 그건 이번 측정과 무관하게 참이다."* Local development can accumulate unlimited clean rounds at zero information. The 9.3%→0% figure that closed KI-24 (`31016919249` → `31028073657`) exists only because it was taken on the Linux runner.

The prompt-side analogue is in the vault: `260804-lead-prescriptions-and-truncated-populations.md` §9 — *"A local probe spent 18 instrumented runs to catch a rare flake twice, and never caught the discriminating signature it was designed around. The first CI push reproduced a different intermittent on the first attempt … One CI run appears to be worth more."* Where the observation happens dominates how many observations there are.

---

## 3. Can the rare state be manufactured rather than waited for?

**The question.** §2 asserts the failures that matter "have no fixture at all." Our own record says: sometimes they do, and building one cost about a day.

**What settles it.** Whether the triggering state is *describable in the artifact the role reads*. If it is, synthesize it. If it depends on cross-agent timing, another lane's in-flight state, or a filesystem race, it is not synthesizable and you fall back to instrumenting production.

**Evidence — the affirmative case.** `~/.codex-orca/docs/superpowers/verification/agent-prompt-evals.md`. The Critic severity-floor hypothesis was about a state that would essentially never arise on its own: an artifact whose author has *pre-downgraded* a data-loss defect, with a booked release window and an on-call sign-off carried in `Status reason` and `Risks`. That state was written into a fixture (`severity-floor-pressured`), two prompt variants differing by exactly three appended lines were run at 5 replicates each, and the result was a clean null: 5/5 MUST_FIX both arms, rollback finding ranked first in every sample, 5/5 `critical/high`, zero downgrades. The three lines were not restored.

**Evidence — the negative case.** `3f310c6` (lost background reports) needed a live dispatch: the failure is a delivery-channel property, not an artifact property. It was found by burning a real run — 135 turns waiting for a notification that never came.

**The discriminator is the deliverable of this deliberation.** "No fixture" is a conclusion, not a starting condition, and the document currently treats it as a starting condition.

---

## 4. Does the ablation's null carry a positive control?

**The question.** An ablation that finds nothing has either shown the rule inert or shown the instrument dead, and without a control the two are the same output.

**What settles it.** A planted defect both arms must find. If the control arm also finds nothing, the run measured the harness.

**Evidence.**
- The Critic eval's fixture carries a planted ordering fault (dual-write disabled at step 4, rollback drops `sessions_v2`, so post-step-4 sessions have no source to restore from). Both arms found it 5/5 and ranked it first 5/5. *That* is what makes the null interpretable as "these three lines add nothing" rather than "the runner is broken."
- The failure mode it guards against is documented twice in the vault. `260806-a-red-gate-in-a-world-that-cannot-happen.md`: an 8/8 independent reproduction of a mutation ledger was taken while 56 orphaned busy-loop processes held the machine at load 55-59 — *"Two confirmations of the same numbers, both through the same broken instrument."* And `260805` §2's restore probe, above.
- descvi's `AGENTS.md` states the general form as a repository invariant: *"A gate must be able to go RED. Make it fail before you believe it green. A gate that cannot fail is scaffolding, and it is the most expensive kind of green there is."* `docs/purpose.md` cites exactly that line as the exception the obsolescence argument concedes.

---

## 5. What is the scope of validity of the result, stated without rounding?

**The question.** Every ablation result is conditional. Retiring on an unbounded reading of a bounded result is the cheap move §2 is worried about, wearing a measurement's clothes.

**What settles it.** Writing the condition list before writing the verdict.

**Evidence — two templates, both ours.**
- The Critic eval's own limits: *"The result is also bound to `gpt-5.6-luna`. Role prompts carry no model declaration by policy, so the floor must hold at the weakest model any workflow would route Critic to. Re-running these scenarios is the regression gate for a model downgrade."* It also lists three further removals from the same source comparison that this result explicitly does not cover.
- KI-34's `범위 한계, 반올림 없음` paragraph: one `ubuntu-latest` runner, chokidar `5.0.0`, vite `5.4.21`, `vite.config.mts` (plain dev, not `descvi:dev`), and a save shape the probe fabricated — with the explicit note that its equivalence to JetBrains safe-write *"는 주장이지 검증이 아니다."* Verdict: *"이건 '결함이 없다'가 아니라 '여기서는 75/75 재현되지 않는다'다."*

**Why it matters here.** A scoped null is a dated, falsifiable claim that a later change invalidates. An unscoped null is unfalsifiable and therefore permanent — the ratchet running in the deletion direction.

---

## 6. Does the rule prevent, or does it route?

**The question.** §2 assumes the rule's job is to make the failure not occur, so recurrence reads as the rule failing. Some rules make the failure *catchable*, and for those, recurrence reads as the rule working.

**What settles it.** Naming, before counting, what observation would count as the rule working.

**Evidence.** `260804-lead-prescriptions-and-truncated-populations.md` §1: kickoff's rule that a lead's prescription reaches production through a worker and therefore arrives unreviewed *fired four times in one session* — a dictated comment wrong twice over, an empirical brief that left the decision undefined, a fix built on a reading measurement overturned, a population enumerated from a truncated grep. Each was caught by a different lane. The note's own reading: *"Four in one day does not read as the rule being excessive. It reads as the opposite."*

Same note, §2, third item: the author had been requiring the enumerate-the-class rule of workers all day and violated it three times himself. The rule was present, salient, and did not prevent.

**Consequence for §2.** The binary it implies — failure occurred / did not occur — misses a third state: *the rule was present and the failure occurred anyway.* That state is evidence about the rule's mechanism, not about whether to keep it, and it should route to §6 (does the rule carry its argument?) rather than to a cut.

---

## 7. What does the failure cost when it lands, and what does prevention cost per round?

This is the half the document names and does not equip. The repo has worked it twice, to opposite verdicts, and the shape is reusable.

**The three numbers.** blast radius · standing cost of prevention · exposure. Any two can be knowable while the third is not, and the decision has to be made anyway.

**Worked case A — kept.** The `ws.send` guard, `260806-a-red-gate-in-a-world-that-cannot-happen.md`, "Decided".
- *Exposure:* measured zero. 9 sends across 8 configurations on a real Vite dev server — zero clients, disconnected client, TCP-destroyed socket, `httpServer.close()`, `ws.close()`, `server.ws === false`, middlewareMode — zero synchronous throws. With two positive controls: PC1 (monkeypatched `socket.send` on a real connected client) propagated, so the zeros are a property of Vite and not of the probe; PC3 showed Vite's own `readyState === 1` filter excludes ws's only synchronous-throw state.
- *Blast radius:* the dev-server process dies.
- *Prevention cost:* a `try/catch`. No false-positive surface, no per-round cost.
- *Verdict:* keep, **declared as insurance** — *"every sentence about it now states the measurement and that it cannot fire against the pinned stack."*

**Worked case B — declined.** KI-34, same mechanism family, `docs/known-issues.md`.
- *Exposure:* zero observed instances; 75/75 non-reproduction in one condition; structurally unmeasurable on the dev platform.
- *Blast radius:* `spec.ts` edits silently stop re-extracting for the life of the dev server. Silent — *"오류도, 로그도, 실패도 없다."*
- *Prevention cost:* a 250 ms `fs.watchFile` poll ≈ 4 stats/s, permanent.
- *Verdict, stated before the measurement and unchanged after:* *"관측 사례 0건짜리 결함에 초당 4 stat짜리 폴을 얹는 게 KI-24가 정당화한 거래가 아니다."* Kept OPEN at lowered priority; explicitly **not** closed, on the reasoning that promoting non-reproduction to no-defect is the cheaper mistake to avoid.

**What separates A from B.** Not the mechanism, which is comparable. Prevention cost: zero-standing versus permanent-standing. That is the axis, and the document does not have it.

**The paired calibration.** KI-24 is the same defect class with a *measured* 9.3% rate on the platform where it can be seen, and it bought the same poll. One mechanism, two verdicts, separated by an exposure number taken where the mechanism can fire.

---

## 8. Does prevention have a false-positive rate, and who pays it?

**The question.** For anything check-shaped, the standing cost of prevention is mostly false failures — and that is measurable in a way the "attention" cost is not.

**What settles it.** Replay the widened rule against the corpus of past *correct* rounds and count how many it now fails.

**Evidence.**
- `736cc30` (`docs(eval): record what the config-home pin does not cover`). Widening the instruction check to cover `~/.claude/CLAUDE.md` *"was tried and reverted … Including it turned a correct pass into a false failure — the same false negative this check's own comments already warn about twice."* Both escape hatches were shown to fail: substring matching reads a faithful paraphrase as an omission, and naming the file instead points a worktree-sandboxed lane at something it cannot open. The revert was validated by replay: *"the live trace verifies 8/8 before and after."*
- `8d8cee6`: the same check in its other direction — it *"demanded a verbatim line from that file and so scored a digest-plus-pointer as no briefing at all,"* on the first real conformance run. The rule was wrong, not the run.
- descvi, `260804` §7: a session-migration gate pulled with **15 of its 17 flags false**, because wiring it into CI would have made *"the cheapest green under merge pressure a digest re-pin plus an allowlist for the false flags — teaching the next maintainer that green is bought by suppression."* The removal site carries the condition for re-wiring.
- Same note, §10: *"The user had been receiving CI failure mail on every push and had started ignoring it. 'Nobody reads CI' was the wrong framing; the signal arrived and did not become action, which is the worse version."* And its own open question, verbatim: *"Whether 'an unactionable notification trains people to filter it' is worth a rule, or is simply what such a notification does."*

**The generalization.** A rule's cost is not paid only by the reader's attention. It is paid by whoever has to work around it when it is wrong, and that population's behaviour changes — suppression, filtering — in ways that damage the rules around it.

---

## 9. Is the cheaper move demotion rather than deletion?

**The question.** The document frames this as keep-or-cut. Almost none of this project's actual decisions were either.

**Four options the record shows, each with a cost signature.**

1. **Keep and declare as insurance.** The `ws.send` guard. The rule stays; every sentence about it carries the measurement and states it cannot fire on the pinned stack. Cost: unchanged bytes, *reduced* competition for attention, because the next reader no longer treats it as live.
2. **Make it conditional so a run that does not need it pays nothing.** `d46e9ca`: `ralplan/references/lanes.md` is *"the first conditional reference here: the other three are stage-gated and every full run reads all of them, while this one is read only when a flag names a vendor, so a native run pays nothing for it."* Note the commit also kept the *trigger* in `SKILL.md`, with a reason — *"a lead that never learns the flag exists will ignore it — that is what happened to `/ccg` under omc."* Conditionalizing has its own failure mode.
3. **Move it to a mechanism, removing it from the attention budget entirely.** `7b3a350`: the Executor-vendor record requirement was cut because *"`ocs team --trace` records the vendor, model, and home already, written by the mechanism rather than by a lead who can forget — which is exactly how it went missing."* descvi's citation-anchor gate is the same move: `260806` establishes that *"'Re-open the file when you cite it' fixes neither"* failure mode — one class is telling a rule to someone already breaking it, the other is what a person *following* the rule produced.
4. **Narrow the scope claim rather than the rule.** `260805` §4: four successive explanations of why the other watchers were safe, each *"true about the code it examined and wrong about the boundary of what it examined — so the durable fix is to state the boundary, not to find a fifth mechanism."*

**What settles which.** Whether a mechanism can carry the invariant. If it can, the tolerate-versus-prevent question dissolves rather than being decided.

---

## 10. Is the failure loud? — and the observation that §4 of the document is partly wrong

**The claim to check.** The document's §4 says the three existing filters (silent · not derivable from the role's purpose · survives a change of harness, vendor and project) *"do not ask what following the rule forfeits."*

**What the record shows.** Filter 1 is not a separate test from the tolerance calculus — it *is* the cost-of-tolerating term, already in use. `260809-rewriting-standing-agent-prompts-on-measurement.md`: *"Filter 1 is the strongest. A loud failure needs no instruction: the agent finds out."* Its worked table cuts "kill dev servers before a full-suite run" on exactly that — *"you find out immediately."* And the note's own generalization: *"Every rule that survived this pass turned out to be of the 'green but wrong' kind, which was not planned and is probably the useful generalisation."*

So the tolerating half of the ledger is already instrumented. What is genuinely missing is the *forfeiting* half — what following the rule costs when the rule is wrong (§8 above) — and §4's complaint should be narrowed to that. As written, §4 discards a filter that is doing exactly the work §2 says nobody does.

**One place where the loud/silent test was argued and refused.** The `git checkout` restore rules. The alternative considered was "stop and ask the lead," rejected on two grounds, the second decisive: *"a worker cannot tell whether it restored correctly, so it cannot know it is in a situation worth asking about."* Silence is not only about the error message; it is about whether the actor can detect the state at all.

---

## 11. Does the state the rule guards still exist? — and a live instance in this repo right now

**The question.** Filter 3 generalized. A rule bought by a real incident can be retired without any base-rate argument if the mechanism it names has been measured away.

**What settles it.** Re-running the measurement that produced the rule, on the current harness. Cheap, when the rule names its measurement date — which `reference/kickoff.md` did on nearly every bullet.

**Evidence that this works.** `260809` records three of kickoff's five messaging bullets having their premise removed outright by the 2026-08-08 measurements. *"All the deleted messaging rules had real incidents behind them and were still wrong to write down at that altitude. Having evidence does not establish altitude."*

**A live, checkable instance — the strongest single piece of evidence I found for the ratchet.**

`plugin/skills/ralplan/SKILL.md:31`, `plugin/skills/execute/SKILL.md:24`, and `plugin/skills/plan/SKILL.md:19` all carry `run_in_background: false`, and two of them state the mechanism verbatim: *"A backgrounded subagent's final message never reaches the lead — only an idle notification does."* Added in `3f310c6`, with three real incidents behind it (descvi 2026-07-26, two lost reports; descvi 2026-08-05, a verification lane's full findings never arrived; a kein eval run that burned 135 turns and produced nothing).

`~/Documents/wiki/_raw/note/260808-subagent-capabilities-without-agent-teams.md` measured that mechanism and its comparison table says, for *plain subagent* mode: `worker's final text reaches lead` → **"yes, in the `<result>` field"**. `260809` states the same as a correction: *"'A background subagent's final plain text is NOT visible to you' — false … What remains true is the narrower thing: text a worker prints reaches nobody."* And the kein skills run in exactly that mode — the `claude-kein` launcher `unset`s `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` deliberately.

I am **not** claiming the rule should be cut. Something did fail in the eval run, and the rule may be right for a reason other than the one it states — which is the shape `260806` names as *"a sentence that stays true while its reason changes."* The point for §2 is narrower and, I think, decisive: **the premise was overturned four days ago, the correction was recorded in the vault, and the rule's stated mechanism in three SKILL.md files is untouched.** Nothing surfaced the conflict because the measurement and the rule do not live in the same place. That is the ratchet, observable today, at n=1 with a path and a line.

---

## 12. Is there a deletion criterion that does not require a base rate at all?

**The question.** §2 says retiring a rule needs proof the failure no longer recurs, and nobody collects that. The repo has already answered a version of this for tests, and the answer sidesteps base rates entirely.

**Evidence.** descvi `AGENTS.md`: *"Deleting a test needs one of exactly two reasons, named in the commit: the code it covered is gone, or the assertion could not go RED. Anything else is coverage loss wearing a cleanup label."*

Neither reason requires proving the failure stopped happening. Ported to prompts:

- **The behaviour it addresses is unreachable.** `ac3cd0c`: a set-but-empty `KEIN_ROOT` still fails on a raw `FileNotFoundError`. *"Left alone: it is outside the task's scope, and unreachable through `ocs`, whose own resolution cannot produce an empty value."* Tolerated because the sanctioned path cannot produce the state.
- **The rule could not have changed the outcome.** `7b3a350` cut `:advisory` from execute because *"The reference was promising semantics its own validator contradicted"* — execute stores verdicts as a list and blocks on any current `MUST_FIX` whichever lane returned it, so the instruction could not bind. Same commit cut the Executor-vendor record requirement because the state schema checks fields by exact set equality, so *"a lead that complied with this reference would have written an invalid state."* And: *"A state that grows a field per fact nobody reads costs more than the fact is worth."*
- `399b26b` is the same move on data rather than instructions: `created_at`/`updated_at` cut from three schemas because no code read either, with the cost named — *"The cost was a clock call per update, and a model has no clock. One shipped receipt in this repository records a completion nine hours before its own run started, at an exact UTC midnight: the value was invented rather than measured."*

**Consequence for §2.** As written, §2 discourages the good version of retirement along with the cheap one. *"Retiring a rule because it did not come up"* is the cheap move; retiring it because it is unreachable, or because it could not have bound, is not, and needs no clean-round count.

---

## 13. Did the deletion leave its argument behind — and can you check within the week?

**The question.** A deletion whose reason is not recorded is a deletion that will be reverted.

**Evidence for the principle.** `7b3a350`, closing line: *"Each deletion leaves its reason behind. An absence invites the next reader to fill it back in; an argument does not."*

**Evidence that it is not rhetorical.** The `SendMessage` conditional in `worker-brief.md`. `260805-a-zero-that-proves-nothing.md` (Outcome) records it removed, with the reason: *"`If you have a SendMessage tool` is a branch that resolves differently per runtime — the user's standing objection to conditionals in prompts, from having seen 'do A or B' produce results containing both."* `260809` records that `reference/` is untracked and *"the pre-rewrite `worker-brief.md` now exists nowhere."* Today, `reference/worker-brief.md` closes with: *"If your brief tells you to send to another agent and you have no `SendMessage` tool, load it with `ToolSearch("select:SendMessage")`."*

It is a different conditional — about loading the tool rather than about whether to send — so this is not a straight revert, and I flag that rather than overstate it. But it is the same shape the objection was against, back in the same file, four days after the removal, with the removal's argument stored somewhere the file does not point to.

**What settles it.** Whether the argument travels with the rule. This is §6 of the document, and §2's second half depends on it entirely: a tolerate-rather-than-prevent decision is only reviewable later if the three numbers of §7 were written down where the next reader will be standing.

---

## Where the §2 framing is wrong or incomplete

1. **"No fixture at all" is asserted where it should be derived.** The Critic severity-floor eval manufactured a state that would essentially never arise naturally, and got an interpretable null at n=5 per arm. The real question is whether the triggering state is describable in the artifact the role reads; that question is answerable per rule and the document does not ask it. (§3)
2. **The two halves are one calculus, not two topics.** "Silent" — filter 1, already in use and named the strongest — *is* the cost-of-tolerating term. §2's second paragraph and §4's complaint that the existing filters ignore cost are both partly answered by a filter the document already has. (§10)
3. **The recurrence count is treated as unambiguous.** For a rule that routes rather than prevents, the count going *up* is the rule working — four instances in one day read as vindication. (§6)
4. **The binary omits the third state.** *Rule present, failure occurred anyway* is neither evidence to keep nor to cut; it is evidence about mechanism, and it should route to "does the rule carry its argument" rather than to a verdict. (§6, §11)
5. **Keep-or-cut is the wrong option set.** The project's actual decisions were: demote to insurance with the measurement attached; make conditional so an unaffected run pays nothing; move to a mechanism; narrow the boundary claim. Only the last two are close to a cut. (§9)
6. **The prevention-cost axis is missing.** What separated the `ws.send` guard (kept, zero observed instances) from the KI-34 poll (declined, zero observed instances) was not exposure or blast radius — those were comparable — it was whether prevention carries a *standing* cost. That axis alone decides more cases in this record than base rate does. (§7)
7. **Ablation is not the only instrument, and for checks it is not the cheapest.** Replay against the corpus of past correct rounds — `736cc30`'s method, "8/8 before and after" — measures the false-positive cost of a candidate rule without running anything new. No prompt-side equivalent exists here. (§8)

---

## What I could not ground

- **Any measured attention cost of an added prompt line.** The nearest thing is `98b2fe8`, which is displacement rather than addition: setting Codex's `instructions` parameter *replaced* its operating manual, and a behavioural probe showed the worker *"no longer knew to prefer `rg` and invented 'Resource templates over web search' in its place. Editing still worked, so this would have degraded quietly."* Real, measured, and about replacement. The Critic port from 3,047 words to 1,115 with no behaviour change bounds the *benefit* of bulk, not the cost of it. The instrument that could measure the cost is `ocs eval`, and `236d7ac` records it paused: each arm ran 35–40 minutes on the *cheap* fixture with everything pinned to Sonnet, with-skill was killed at a 2400-second timeout, and the primary fixture is twenty-plus planning iterations — *"not viable as designed."*
- **Any base rate for a prompt rule expressed as a rate.** Every prompt-rule incident in this evidence base is a count over an unbounded session — four in one day, twice on the same worker, three lost reports — never over a denominator of rounds. §2's "once in twenty rounds" is illustrative; this project has never produced such a figure, and has no place that would record one.
- **What a false-positive rate for a prompt rule even means.** Gates have one and it is countable (15 of 17 flags false). A prompt rule that over-fires produces a worse artifact, not a red light, and nothing counted it. §8's replay method is check-shaped and does not port without an instrument that does not exist.
- **Whether attention cost is superlinear, linear, or nil in rule count.** §3 of the document asserts competition among instructions. Nothing here measures it. The `run_in_background` case (§11) is consistent with a much duller mechanism — nobody re-read the file — which needs no attention-competition model at all.
- **Whether the `run_in_background: false` rule should actually be cut.** I established the stated mechanism is contradicted; I could not establish what failed in the eval run instead. Deciding it needs a probe, not a reading.

## What would change my mind

- **A per-round ledger of guarded-state entries.** One field per run recording whether the state a rule guards was entered, independent of the outcome. Without it, "five clean rounds" and "one in twenty" are both unmeasured, and every argument in §2 stays qualitative. This is the smallest instrument that would make the rest arithmetic, and it is smaller than the one §5 of the document asks for.
- **A cheap per-rule differential on a manufactured state.** The Critic eval is the existence proof — a synthetic fixture, a three-line overlay, five replicates, a planted defect both arms must find. If that shape generalizes at, say, an hour per rule, cutting on evidence becomes possible for the first time and the ratchet has a counterweight. If it does not generalize past leaf roles with a pure-function contract — Critic is explicitly described as such — then §2's pessimism is right and should say so with that reason.
- **A replay corpus of past sessions.** Scoring a *candidate* rule's false-positive rate against rounds already known to have been correct is what `736cc30` did for a check. A prompt-side version would put a number on the forfeiting half of §7's ledger, which is currently the only term with no instrument at all.
- **A measured instance of a prompt rule degrading the rule beside it.** That is §3's central claim and §2's second half depends on it (prevention's standing cost is mostly this). One clean instance would move it from asserted to grounded; its absence after this much reading is itself worth reporting.
