# The gate, measured

Run 2026-08-14, case `plan-evidence-gate`, five replicates per arm, Sonnet lead and Sonnet lanes. The arms are the skill present and the skill absent — not two versions of a prompt, which is what `plan-no-unknown` compares.

Raw run `.agents/kein/runs/eval/260814-171410`, with two control replicates backfilled from `260814-204410` and marked `backfilled_from` in the manifest. Earlier and superseded: `260814-151529` (one replicate), `260814-155618` (two), `260814-162343` (five, before the fixture had an entry point).

## What the graders said

| | with | without | |
| :--- | ---: | ---: | :--- |
| `routed-to-a-skill` | 5/5 | 0/5 | discriminates |
| `vocabulary-gate-shape` | 5/5 | 0/5 | discriminates |
| `vocabulary-open-questions` | 5/5 | 0/5 | discriminates |
| `vocabulary-status-metadata` | 5/5 | 0/5 | discriminates |
| `gate-decides-both-paths` | 5/5 | 4/5 | strengthens |
| `names-the-files-it-touches` | 5/5 | 2/5 | strengthens |
| `no-pre-written-implementation` | 1/5 | 0/5 | unreliable |
| `plan-file-written` | 5/5 | 5/5 | inert |
| `records-the-open-question` | 5/5 | 5/5 | inert |
| `sequences-the-irreversible-step` | 5/5 | 5/5 | inert |
| `stops-at-the-artifact` | 5/5 | 5/5 | inert |

**The three vocabulary graders are a control and they read exactly as the case file predicted they would.** They separate the arms perfectly, and the content grader each is paired with does not. `records-the-open-question` is the sharpest instance: the arm without the skill records the recency tie-break as open in every replicate — "the requirements say this is undecided and either is acceptable", "explicitly leave recency-vs-quality tie-breaking undecided", a section headed "Ranking tie-break (open decision)" — and never once writes `## Open Questions`. The substance was already there. The heading was not.

Reporting the 5/5-against-0/5 of the vocabulary graders as a benefit of `plan` is the misreading this case exists to prevent, and it is now a measured fact rather than a warning.

## What the ranking said

Ten plans, four judges — `critic@codex`, `architect@codex`, `verifier@codex`, `opus` — three presentation orders, arm labels withheld, twelve of twelve readings usable.

| | with | without |
| :--- | ---: | ---: |
| Borda points | **383** | 157 |
| mean finishing position | **3.6** | 7.4 |

The top four are all from the arm with the skill. All four judges placed a with-skill plan first and all four agreed on fifth. `opus` differs from the codex three on individual plans — it puts the others' first-place fourth — and agrees with them on every arm-level reading, so the vendor split earns nothing here beyond the assurance that it earns nothing here.

**The axis the judges name is the gate**, and they name it in the same words the case was built around. The first-place plan "fully specifies both FTS5 and manual-index branches". The one with-skill plan that fell to eighth drew a unanimous complaint:

> deliberately responds to FTS5 absence by retaining the 4–9-second unranked search, leaving the central desired outcome and two acceptance criteria unmet

## The gate grader is weaker than the question it asks

That eighth-place plan **passed** `gate-decides-both-paths`. It had decided both paths: FTS5 present, use it; FTS5 absent, keep `LIKE`. The grader asks whether the plan decided, and it had.

What it did not ask is whether the decision satisfies the requirements. "Keep `LIKE`" abandons the desired outcome the document opens with and two of its five acceptance criteria, and every judge saw that and every judge ranked it accordingly.

So the case's central grader returned 5/5 against 4/5 — nearly nothing — on the same question the ranking separated 383 to 157. **Pass/fail cannot see degree, and a bar set at "a decision was made" admits a decision that gives up the outcome.** The grader was tightened to require the alternate path to still meet the acceptance criteria, which is not a new rule imported into the case but a thing the requirements document already demands.

## Second run, and what the first one was actually measuring

Run `260814-223423`, five replicates a side, after three corrections: the tightened gate criterion, `path: PLAN.md` declared on every grader that names a file, and the judge moved off the fast tier.

| | with | without | |
| :--- | ---: | ---: | :--- |
| `gate-decides-both-paths` | 5/5 | 0/5 | discriminates |
| `routed-to-a-skill` | 5/5 | 0/5 | discriminates |
| `vocabulary-open-questions` | 5/5 | 0/5 | discriminates |
| `vocabulary-status-metadata` | 5/5 | 0/5 | discriminates |
| `names-the-files-it-touches` | 4/5 | 1/5 | unreliable |
| `records-the-open-question` | 4/5 | 5/5 | unreliable |
| `vocabulary-gate-shape` | 4/5 | 0/5 | unreliable |
| `plan-file-written` | 5/5 | 5/5 | inert |
| `sequences-the-irreversible-step` | 5/5 | 5/5 | inert |
| `stops-at-the-artifact` | 5/5 | 5/5 | inert |
| `no-pre-written-implementation` | 0/5 | 0/5 | unreached |

**This reverses the reading above.** The case file sets the test: if the content graders separate the arms by as much as the vocabulary graders do, the skill is changing the plan; if by less, it is changing the headings. The central content grader now separates 5/5 against 0/5, which is exactly what the vocabulary controls do, at twice their weight. The first run's 5/5 against 4/5 was not a measurement of the skill; it was a measurement taken with a criterion that accepted "keep `LIKE`" as a decided branch, and with a judge that hallucinated a missing artifact.

The ranking said this before the graders could. It separated the arms 383 to 157 on the gate axis while the gate grader was reporting almost nothing, and the disagreement was the grader's fault. That is the second time in this programme the ranking has been right about something the per-assertion graders could not see, and both times the fix was to the grader.

What survives from the first run unchanged: `records-the-open-question` still has the control ahead, 5/5 against 4/5. `no-pre-written-implementation` is now 0/5 on both sides — nobody follows it, including the arm that carries the rule.

### The ranking of the same ten plans

Three Codex role lenses, all at the deep tier, three presentation orders, nine of nine readings usable. `opus` is left out until the Claude-side routing is settled: `--append-system-prompt` appends to Claude Code's own system prompt, and a native subagent is documented as receiving its own, so the two sides are not yet the same environment.

| | with | without |
| :--- | ---: | ---: |
| Borda points | **314** | 91 |
| mean finishing position | **3.0** | 8.0 |

```
order by arm: with with with with with without without without without without
```

**No interleaving at all, and each judge produced that separation independently.** Every run in this programme until now has printed the line about interleaved arms meaning the arm is not what the ranking is ranking. This is the first time it does not apply.

The axis is the same in all nine readings, and it is the gate:

> The top plans fully choose an executable ranked-search backend for both FTS5 outcomes, while the bottom plans leave the no-FTS5 outcome requiring a new architecture decision or knowingly abandon the required outcome.

The last-placed plan "hands the key decision to the packaging owner and even permits accepting LIKE-only search, which fails the desired outcome" — which is the clause the gate grader was tightened to include. The grader was made to ask what the judges were already sorting on, and on these ten plans the two instruments now return the same answer: 5/5 against 0/5, and 314 against 91.

That agreement is on one set of plans, not across two runs, which is what makes it worth more than this morning's. And it is the first run of either case that turned up no defect in the instrument.

## On the rule against pre-written implementation

Nine of ten plans carried implementation, so the grader labels it `unreliable` at 1/5 against 0/5 and separates nothing. Three things are worth keeping straight about that.

**The rule is moving behaviour, and the grader cannot see it.** Counting Python blocks that contain a loop, a `try`, or a transaction: one across the five plans with the skill, twelve across the five without. The grader flattens that to 1 against 0 because it also catches the backfill routine written as prose pseudocode, which both arms do in almost every replicate.

**The violation everyone commits is the harmless kind.** The fixture's invitation is the batched, resumable, progress-reporting backfill — read a batch, commit a marker in the same transaction, report progress. There is one conventional way to write that, so pre-writing it costs the reader nothing. The reason the rule exists is the opposite case: code that cannot be known until it is implemented, which goes stale or wrong between planning and building and which a reviewer would flag. This fixture has no such place. Its one unresolved fact is answered by a probe, and the plans that write out a probe script are writing the cheap discriminating observation the gate asks for, not code against an answer they do not have.

**Nothing here says how a judge weighs pre-written code.** The ranking prompt says nothing about implementation in a plan, so its silence is not a verdict. "Wrote out the code" reads as thoroughness as easily as it reads as a defect, and adding a line to the judge telling it otherwise would make the judge measure our rule instead of measuring what serves the person building from the plan.

The rule stays. Measuring what it is for needs a fixture where a plan genuinely cannot know the code, and neither case has one.

## Instrument defects this run found

**The judge stopped answering and it looked like a verdict.** The account's session limit landed mid-run, and six llm graders on two replicates recorded `unreadable verdict: You've hit your session limit`, which counts as a failure. Both plans were complete on disk. A judge that could not answer and a grader that answered no are the same `x` in the table. Twelve at once was visible; one would not have been. `--regrade` now re-asks only verdicts that were never reached and leaves every honestly-obtained one alone.

**`--arm` crashed the report.** With one arm there is no `roles["treatment"]` to name — in the mode that exists precisely for filling a gap in an interrupted run.

**A judge was shown evidence that was false.** `stops-at-the-artifact` failed a replicate on the reasoning that `PLAN.md` "was not actually created as a file on disk", while the deterministic grader beside it confirmed the file was there. The judge had been handed `record["files_written"]`, which is read off the lead's event stream and holds nothing a subagent wrote. It now gets the list `collect()` builds from `git status`.

**That fix immediately failed the self-test**, which is what it is for: `_record.json` is the self-test's own contract file, no run writes one, and listing it told a judge grading "is `PLAN.md` the only file written" that a second file had been written.

**`vocabulary-gate-shape` demanded a colon.** It scored zero against a plan that wrote `- Alternate path (all shipped targets report FTS5_AVAILABLE=0):` and split the unexpected result into `case A` and `case B` — more of the template's shape than the template asks for. A control reading a thorough plan as an empty one is the worst grader to have wrong, because the content graders are read against it.

**The fixture was missing the file five plans said they could not name.** `names-the-files-it-touches` came back 4/5 against 1/5 and every failure said the same thing: the step wiring the index build into launch cannot name a file because "the entry point is not in the three reviewed files". It was not there. `marginalia/app.py` now is, and the grader reads 5/5 against 2/5 — the first time either of the two rules added on 260812 has measured itself rather than an omission of mine.
