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

## What the artifacts say

`ocs eval --compare … --judge-model opus`, arm labels stripped, every pair judged in both orders:

```
with-skill 3   without-skill 0   tie 0
```

All three pairs, and all six orderings, agreed. The judge preferred the skill's plan whether it was shown first or second, so this is not position preference.

Every one of the six reasons named the same difference, and it is the difference the `strengthens` assertions were pointing at:

> B decides the load-bearing consequences rather than deferring them — it fully specifies the FTS5-absent branch (schema, tokenizer, BM25-in-app scoring) as an executable alternate path, whereas A's "fork" for the same unknown collapses into an unscoped packaging task.

**The two layers agree, and that is the result.** The vocabulary control said the skill moves the form; a comparison that found no preference would have meant it moves only the form. It found a unanimous preference, for the behaviour the content assertions measured. `plan` changes the plan.

One difference between the layers is worth keeping. The Haiku grader passed the baseline on `gate-decides-both-paths` in one run of three; the Opus comparison preferred the skill's plan in that same pair. A binary criterion has a floor and a comparison does not, so a plan can clear the bar and still be the worse of two. Neither instrument substitutes for the other.

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
- **The Opus comparison is one judge.** Order was controlled; the judge was not varied, and a second vendor reading the same pairs is the obvious next control given how often a cross-vendor pair disagrees here.
- **Routing was measured because the case prompt names no skill.** That is the opposite of the fixture path in `ocs eval`, which prefixes the invocation. A null on routing in some later case would not mean the workflow does nothing.

## Instrument defect found and fixed

The first classification called both `strengthens` rows `flaky`, because the classifier collapsed any within-arm inconsistency into one label. The treatment arm was 3/3 in both; the inconsistency was entirely in the control, which is not instability but the measurement itself. Fixed in `3952544`'s successor: an inconsistent treatment arm is `unreliable` and is a defect, an inconsistent control arm under a consistent treatment arm is `strengthens` and is the finding.

It is worth recording that the instrument's most informative output was the one its first classifier hid.
