# One sentence, measured

Run 2026-08-13, case `plan-no-unknown`, six replicates per arm, Sonnet lead and Sonnet lanes. The arms differ by one sentence in `planner.md` and nothing else.

Raw runs under `.agents/kein/runs/eval/`: `260813-003416` (rules against no rules) and `260813-142157` (the sentence against no sentence).

## The change

`<Artifact_Contract>`'s fourth bullet forbids pre-writing the implementation, with an exception for a fragment that fixes a decision more precisely than prose can. That exception listed a schema, a type or state shape, and an interface signature. `93bf0e0` added one more item and one more sentence:

> …an interface signature, **or the assertion that says what a step must prove** — belongs in the plan, trimmed to the part that is the decision. **An acceptance check written as prose is the common way a plan looks complete while leaving the implementer free to prove something weaker than the requirement asks.**

## The result

| | with the sentence | without |
| :--- | ---: | ---: |
| Borda points | **520** | 272 |
| mean finishing position | **4.5** | 8.5 |

Twelve plans, four judges — `critic@codex`, `architect@codex`, `verifier@codex`, and `opus` — three presentation orders each, arm labels withheld. All twelve readings were usable.

All four judges placed the same plan first. Three of the four placed the same three plans last, and all three are from the arm without the sentence. Nothing else in this programme has produced agreement at that level.

## Why it is the sentence and not something else

The judges name the axis, and it is the one the sentence targets.

The last-place plan drew the same complaint in all nine codex notes:

> postpones discovering the existing unreadable-file exit code until implementation time, leaving unresolved the exact repository fact the requirements explicitly require the plan to establish

The first-place plan drew its mirror image:

> combines source-confirmed exit/error behavior with live parity testing and byte-exact JSON assertions that pin indentation and the trailing newline

The rest of the arm without the sentence failed the same way and the notes say so plainly: an error assertion left as "stderr is non-empty and contains the path", another as "matches the same shape", a third leaving whether to change `USAGE` to the implementer.

## What the proxy metrics said, and why they were wrong

Counting `assert` mentions gave 8.2 for the arm with the sentence against 8.0 without, and code blocks 2 against 6. Read alone, that is a null, and it was reported as one before the ranking ran.

It was measuring the wrong thing. The plan with the most assertions in the field — seventeen, more than any other — finished ninth, because its error assertion was the weakest in the field. **The judges sort on the strength of the proof, not on how much of it there is**, and no count distinguishes those.

The per-plan notes are what caught this, and they exist because the ranking was asked for them. A ranking says the field was sorted and not on what.

## What this does not establish

**The arms still interleave.** Third place and sixth place both come from the arm without the sentence, and third place beat four plans that had it. Plan-to-plan variance remains comparable to the arm difference; what changed is that the arm difference is now large enough to see through it.

**One fixture, six replicates a side.** Three earlier attempts to measure the whole rule set on this same fixture returned nothing at all, which is the reason to trust a result that isolates one sentence — and also the reason not to over-read it.

**The judge prompt changed between the two runs.** `260813-003416` was ranked before per-plan notes were added and `260813-142157` after, so the 458/334 of the earlier run and the 520/272 of this one were taken with different instruments. Within either run both arms share an instrument, so each split is internally valid; the reversal between them is not a measured quantity.

## Instrument notes worth carrying

**Entry is pinned and it mattered.** Before pinning, three of twelve replicates never reached the skill — thirteen to sixteen turns against a normal thirty, no dispatch, the lead writing a plan itself. Every grader difference in that run traced to those three plus one plan written to the wrong path, not to content. After pinning, twelve of twelve dispatched and every grader went inert.

**A pinned arm never calls the `Skill` tool.** The slash command is the injection. A `tool_used: Skill` assertion fails precisely when entry worked.

**The judge inherits `~/.claude/CLAUDE.md`.** It is invoked as a plain `claude -p`, outside the pinned config home the arms get. Observed here as `opus` writing some notes in Korean, which is that file's language instruction reaching it. Harmless for a language preference, and identical across arms so attribution holds, but a planning instruction placed there would reach every judge.

## The five graders are dead on this fixture

Sixty out of sixty, `inert` across the board, three runs in a row. `covers-the-error-path`, `no-evidence-gate`, `no-manufactured-unknown`, `plan-file-written`, `vocabulary-status-metadata` no longer separate anything here. Every result in this document came from the ranking instead.

That is deletion evidence for the graders, not for the skill. It is also the argument for the next fixture: two of the four planner rules — project-relative paths, and no pre-written implementation — have never been measured at all, because all thirty plans across every run carry zero absolute paths and nothing in `tally` invites the violation.
