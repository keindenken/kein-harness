# What other people's planning skills know

Read 2026-08-11 from the corpus at `.agents/kein/research/260811-github-skill-corpus/corpus/`, selected by name and body match and ranked by revision depth (`planning-candidates.json`, 578 candidates). Nothing here has been added to `plan` or `planner`; this is the reading that comes first.

Four houses, plus the incumbent:

| Source | File | |
| :--- | :--- | :--- |
| `obra/superpowers` | `writing-plans`, `executing-plans` | the closest analogue to `plan` + `execute` |
| `mattpocock/skills` | `wayfinder`, `to-tickets` | the lightest house; `handoff` came from here |
| `garrytan/gstack` | `plan-eng-review` | 8,957 words, ~100 revisions |
| `OthmanAdi/planning-with-files` | `planning-with-files` | 80 revisions, 14 authors |
| `Yeachan-Heo/oh-my-claudecode` | `ralplan`, `plan` | the incumbent this harness replaced |

Findings are sorted by the transmission path they need. A rule in `SKILL.md` reaches the lead, which reads it and writes a brief; the sub-agent gets it second-hand if at all. A rule in `planner.md` reaches the sub-agent directly and the lead never sees it. So `SKILL.md` is for judgement that varies by case and for anything both must know; `planner.md` is for what the lead would otherwise re-brief every single time.

## A plan written for a reader with no memory of the rest of it

`writing-plans` says it outright — "assume the engineer has zero context for our codebase" — and then carries three separate devices that exist only because of it:

- `## Global Constraints`, values copied verbatim from the spec, because "every task's requirements implicitly include this section";
- `**Interfaces:** Consumes / Produces` with exact signatures, because "a task's implementer sees only their own task; this block is how they learn the names and types neighboring tasks use";
- a ban on "Similar to Task N" — "repeat the code — the engineer may be reading tasks out of order".

`to-tickets` reaches the same place from the other end: each ticket declares its **blocking edges**, and a session works the **frontier** — any ticket whose blockers are all done.

`plan-template.md` carries none of this: no constraint block, no interface contract between units, no dependency structure.

**This was first written up here as a defect, and it is not one.** `execute` dispatches a fresh executor per unit, but strictly one at a time — "keep later tasks pending; no second write-capable task may run elsewhere as a deadline workaround" — and against a real repository. So when task 2 needs the signature task 1 created, that code is already on disk and its executor can read it. The contract is recoverable without being written down. Superpowers' block earns its place where tasks run in parallel, or where the plan is executed somewhere the earlier code is not; neither describes this harness.

What survives is smaller and worth stating precisely. An executor with no interface block pays a search on every dispatch, which is cost rather than correctness. And nothing checks the plan against itself, so `clearLayers()` in task 3 can become `clearFullLayers()` in task 7 — superpowers catches that in its own self-review, and it is a defect in the plan rather than in the execution. Both are real; neither is the structural gap the first version of this document claimed.

## The disagreement this harness has not noticed it is in

`writing-plans` requires exact paths and real code: `Modify: exact/path/to/existing.py:123-145`, working test bodies, and a "No Placeholders" list that names "add appropriate error handling" as a plan failure.

`to-tickets` forbids the same thing: "avoid specific file paths or code snippets — **they go stale fast**." Its one exception is a snippet from a prototype that "encodes a decision more precisely than prose can", trimmed to the decision-rich parts.

Both give reasons and the reasons are compatible: the implementer has no context, and the plan is written before the code moves. They just weigh differently. `plan-template.md` says nothing either way, and the measured plans on 2026-08-11 ran 1,600 to 4,100 words with file-level detail — so this harness is on the `writing-plans` side without ever having chosen it. That is the decision worth making explicitly, and it belongs in `planner.md`, since it governs what the artifact contains.

## For `SKILL.md` — the lead's judgement

**A completion criterion stated positively.** `wayfinder`: the map is done "when the way is clear — nothing left to decide before someone goes and does the thing", and "the pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off".

This was first written up here as something `ralplan` lacks. It is not. `ralplan/SKILL.md` already carries "around five unsuccessful official rounds is a diagnostic trigger, not a maximum", with four named remedies — user authority, missing evidence, a bounded conditional plan, or an explicit Draft handoff — and "do not manufacture approval from repetition". The last of those four is exactly the escape the twenty-round omc failure took.

The difference that remains is one of kind rather than of presence. `ralplan`'s trigger is negative and counted: after enough failures, stop and reassess. `wayfinder`'s is positive and about content: you are finished when nothing is left to decide. A negative trigger tells you when to worry that you are not finished; it never tells you that you are. Whether that is worth adding is a smaller question than it looked, and it belongs to `ralplan` rather than to `plan`.

**An unknown has three moves, and the skill names one.** `plan/SKILL.md` says resolve it now, or record a bounded gate. The 2026-08-11 measurement surfaced a third that a blind judge preferred — **eliminate it**, by vendoring the dependency so nothing is left to branch on. `wayfinder` supplies a fourth — **leave it as fog**, named in a "Not yet specified" section, to graduate when the frontier reaches it. Choosing among four is exactly the case-by-case judgement that belongs with the lead.

**Whether this is one plan at all.** `writing-plans`: if the spec covers multiple independent subsystems, break it into one plan per subsystem, "each plan should produce working, testable software on its own". `plan` produces one artifact for whatever it is handed.

**Whether to consult the user on the shape.** `to-tickets` presents the breakdown and asks three questions — is the granularity right, are the blocking edges genuine, should anything merge or split — and iterates until approved. `plan` dispatches and reports. Not obviously wrong, but it is an unmade decision rather than a made one.

## For `planner.md` — straight to the sub-agent

**A sizing criterion, stated as a criterion.** Two are available and they are different:

- `writing-plans`: "the smallest unit that carries its own test cycle and is worth a fresh reviewer's gate… split only where a reviewer could meaningfully reject one task while approving its neighbor."
- `to-tickets`: "each slice is sized to fit in a single fresh context window", cutting "a narrow but COMPLETE path through every layer — vertical, NOT a horizontal slice of one layer".

Both are interface constraints rather than enumerations, which is what `docs/purpose.md` asks for.

**The sharpness test.** `wayfinder`, on whether something is a ticket or fog: "the test is whether you can state the question precisely **now** — *not* whether you can answer it now. Ticket when the question is already sharp, even if it's blocked… Don't pre-slice the fog into ticket-sized pieces." This is the missing criterion for when an Evidence Gate is the right instrument, and it is mechanical enough to state once.

**Named plan failures.** `writing-plans` lists them concretely: "TBD", "add appropriate error handling", "write tests for the above" without test code, "Similar to Task N", and "references to types, functions, or methods not defined in any task". A list of failures is cheaper to check than a list of virtues.

**A named exception to slicing, with its remedy.** `to-tickets` on wide refactors: a mechanical change whose "blast radius fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green". The answer is expand–contract — add the new form beside the old, migrate call sites in batches sized by blast radius, delete the old form in a ticket blocked by every batch — with a further escape when even the batches cannot stay green alone. This is specialist content that would not be re-derived.

**A named failure for asking the user.** `wayfinder` splits every ticket into human-in-the-loop or agent-alone, and states the failure: "the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this)". `plan` tells the Planner to ask the user when an answer materially changes the plan, and nothing stops it answering on their behalf.

## What not to take

**`writing-plans`' self-review.** It is a three-point checklist the planner runs on its own output — spec coverage, placeholder scan, type consistency — and it is explicit that this is "not a subagent dispatch" and that fixes need no re-review. `trailofbits/skills` argues the opposite case for the general form: "double-check your answer" and similar "make output worse on current models rather than better… put the check in `make check` or the validator, where it runs deterministically and cannot be talked out of firing." The superpowers version is bounded enough to survive that objection, but `ralplan` already occupies this space with a real reviewer, so adding a self-check to `plan` would duplicate a gate rather than add one.

**Its execution handoff.** `writing-plans` ends by offering the user two execution modes. `plan` stopping at the artifact is a decision this harness made deliberately, and `docs/purpose.md` records why.

**`planning-with-files`' three-file scheme.** `task_plan.md`, `findings.md`, `progress.md` maintained continuously. Eighty revisions and fourteen authors say it works for its authors, but it is a state discipline for a long-running agent rather than a planning discipline, and `.agents/kein/` already resolves where state lives.

## What reading someone else's skill gets wrong

Two claims in the first version of this document were corrected the same day, and both failed the same way: a device another house carries was read as a gap here, without checking why this harness does not need it.

- The interface block looked structural because `execute` isolates its executors. It does not need one, because those executors run one at a time against a repository that already holds the previous task's code.
- The completion criterion looked missing because `wayfinder` states one and `plan` does not. `ralplan` states one already, in a different form, three sections further down its own file than the reading went.

The general lesson is worth more than either correction. **A rule's absence is only a gap if the condition that made it necessary elsewhere also holds here**, and that condition is usually in the other house's architecture rather than in its prose. Read for the mechanism the rule protects, then check whether this harness has that mechanism, before reading the rule as missing.

`docs/prompt-revision.md` already says the same thing from the other direction, under Adding: *name the mechanism*. It did not occur to me that the test applies just as much to importing a rule as to inventing one.

The `disable-model-invocation: true` field both `mattpocock` planning skills carry is dropped rather than checked: it would require the user to open with `/plan`, and that is not how this workflow gets entered.
