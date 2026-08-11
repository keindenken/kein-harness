# `plan`, measured

The first result from the instrument `.agents/kein/requirements/260810-skill-measurement-program.md` specifies. Run 2026-08-11, three replicates per arm, Sonnet lead and Sonnet lanes, case `plan-evidence-gate`.

Raw run at `.agents/kein/runs/eval/260811-155344-case-plan-evidence-gate`; re-read the classification at any time with `ocs eval --reclassify <that path>`, and the artifacts are kept under `artifacts/`.

## What the assertions say

| Assertion | Kind | with | without | |
| :--- | :--- | :--- | :--- | :--- |
| `routed-to-a-skill` | tool_used | 3/3 | 0/3 | discriminates |
| `vocabulary-gate-shape` | regex | 3/3 | 0/3 | discriminates |
| `vocabulary-open-questions` | regex | 3/3 | 0/3 | discriminates |
| `vocabulary-status-metadata` | regex | 3/3 | 0/3 | discriminates |
| `gate-decides-both-paths` | llm, w2 | 3/3 | 1/3 | strengthens |
| `sequences-the-irreversible-step` | llm | 3/3 | 2/3 | strengthens |
| `plan-file-written` | file_exists | 3/3 | 3/3 | inert |
| `records-the-open-question` | llm | 3/3 | 3/3 | inert |
| `stops-at-the-artifact` | llm | 3/3 | 3/3 | inert |

Three of the four clean separations are the `vocabulary-*` graders, which were written as a control and which separate for a trivial reason: they match this template's own headings, and the arm without the skill has no reason to produce them. The fourth is routing. **No content assertion separates cleanly.** The two that carry the skill's actual argument both land on `strengthens` — the baseline produces the behaviour sometimes, the skill produces it every time.

The sharpest cell is a pair that splits:

- `vocabulary-open-questions` — is the heading there — **3/3 against 0/3**
- `records-the-open-question` — was the non-blocking question actually carried as non-blocking — **3/3 against 3/3**

The baseline already does the thing. What `plan` adds there is the word `## Open Questions`. Splitting vocabulary from content was worth its cost for this line alone.

`stops-at-the-artifact` is inert for the same shape of reason: a Sonnet lead asked for a plan does not start implementing, with or without an instruction telling it not to. Three assertions inert is deletion evidence — the kind `docs/prompt-revision.md` says nobody collects — and it is evidence rather than a decision. One fixture at n=3 does not license a cut, and cutting is the last of the four moves anyway.

## What the artifacts say: nothing yet, and that is the finding

The first comparison — one Opus judge, both orders per pair — returned **3–0 for the skill**, with every ordering agreeing. It was recorded here as confirmation that `plan` changes the plan rather than the form.

**It did not replicate.** The same comparison, same prompt, same artifacts, same reconciliation, run a second time with a second vendor added:

| judge | with-skill | without-skill | tie |
| :--- | :--- | :--- | :--- |
| opus | 0 | 1 | 2 |
| codex:gpt-5.6-sol | 1 | 1 | 1 |

The judges agreed on **0 of 3 pairs**.

The position data says what happened. Reading which physical slot each verdict chose: the first Opus run picked first, second, first, second, first, second — always the treatment, never the position. The second Opus run picked the **second** document in five of six judgements. One run tracked the content; the other tracked the slot. Order control caught it, which is why two of its three pairs are ties rather than wins, but the earlier 3–0 has to be read as one draw from a high-variance instrument rather than as a result.

**So the claim that `plan` produces a better plan is unsupported.** The assertion-level result stands on its own evidence and is unaffected: the skill pre-decides both branches in every run and the baseline in one of three. What is now open is whether doing so makes the plan better.

And the disagreement is substantive, not noise. The second Opus run repeatedly preferred the baseline, for a reason worth quoting against this harness's own doctrine:

> On the unresolved FTS5 question B commits to a decision that collapses the branch — if any packaged target lacks FTS5, bundle a statically compiled amalgamation — leaving one code path to build and test.

The baseline's move is to **eliminate the unknown** by vendoring a SQLite it controls, so there is nothing left to branch on. `plan`'s move is to keep the unknown and plan both branches. `plan/SKILL.md` prescribes the second without ever considering the first, and a judge reading both artifacts blind preferred the first. Codex split on the same question — once calling vendoring decisive, once objecting that it "still depends on changing and validating the packaging toolchain before implementation can proceed."

That is a real argument about the Evidence Gate doctrine, surfaced by the measurement rather than by reading the prompt, and it is the most useful thing this run produced.

One observation survives from the first comparison. The Haiku grader passed the baseline on `gate-decides-both-paths` in one run of three, and both comparison runs found something to prefer in baseline plans. A binary criterion has a floor and a comparison does not, so the two instruments answer different questions and neither substitutes for the other.

## What the run cost, and the confound it confirms

| | turns | seconds |
| :--- | :--- | :--- |
| with-skill | 16, 20, 22 | 231, 274, 396 |
| without-skill | 8, 9, 9 | 148, 81, 122 |

The skill arm takes about two and a half times the turns, because it reads its template and dispatches a Planner that writes the artifact itself. `max_turns` was set to 40 on the strength of `trailofbits/skills`' `audit-context-building` case, which records the same ratio and the same failure. Calibrated on the baseline at 20, the third run would have been truncated at 22 turns and scored as a failure of the skill.

Model parity held: `prepare_plugin` re-renders the deep-tier agents onto the arm's model, so the Planner ran as Sonnet rather than as its declared Opus, and the arms differ by skill rather than by model.

## What this does not establish

- **One fixture, one skill, three replicates.** `strengthens` at 3/3 against 1/3 is three runs against three runs. The ratio is the result and the replicate count is what bounds it.
- **The vocabulary graders will separate on any fixture**, because they match headings. They are a control and must never be quoted as a benefit of `plan`.
- **`inert` here is inert on this fixture.** A requirements document that invited implementation would test `stops-at-the-artifact` properly; this one does not.
- **The comparison was not replicated before it was believed.** One run of a pairwise judge was recorded here as a result, and a second run of the same comparison contradicted it. Order control was in place and was not enough; run-to-run variance in the judge was the larger effect and nothing was measuring it. A comparison needs replicates for the same reason an arm does, and that this document asserted a 3-0 before collecting any is the instrument failure worth remembering from this run.
- **Routing was measured because the case prompt names no skill.** That is the opposite of the fixture path in `ocs eval`, which prefixes the invocation. A null on routing in some later case would not mean the workflow does nothing.

## Two instrument defects, both found by the instrument disagreeing with itself

**The classifier hid its most informative output.** The first classification called both `strengthens` rows `flaky`, because it collapsed any within-arm inconsistency into one label. The treatment arm was 3/3 in both; the inconsistency was entirely in the control, which is not instability but the measurement itself. An inconsistent treatment arm is now `unreliable` and is a defect; an inconsistent control arm under a consistent treatment arm is `strengthens` and is the finding.

**The comparison had no replicates, and one draw was written down as a result.** Order was controlled from the start, which was the variance that had been anticipated. The variance that mattered was between runs of the same judge on the same input, and a single run cannot see it. The comparison now takes `--compare-runs`, and a result from one run should not be quoted.

Both defects were caught the same way: by the instrument producing two readings of one dataset and the readings not matching. Neither would have been visible from a single clean run, which is an argument for cheap re-reads — `--reclassify` costs nothing and `--compare` costs a handful of calls.
