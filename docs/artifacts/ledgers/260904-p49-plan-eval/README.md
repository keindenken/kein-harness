# phase-49 plan evaluation — kein vs omc, blind, sixteen readers

Taken 2026-09-04 evening, before either execute run had accepted a code story. Both plans answer the same kickoff commit (`9473225`) with the same lead model. The plans were copied as `plan-A.md` and `plan-B.md` with the assignment sealed (`sealed.json`: A = omc, B = kein) and every reader was told not to guess origin. The repository they were checked against is `git archive 9473225`, the tree both plans started from.

Three instruments, all on opus:

| instrument | readers | what it measures |
|---|---|---|
| `verify-*` | 2 per plan, one per half | claims about the repository, checked against the base tree |
| `ledger-*` | 2 per plan | an execute lead building the task ledger from one plan alone: what had to be invented, what would be asked, whether each story is one round |
| `judge-*` | 8, four per reading order | forced choice per dimension with line-cited reasons; framing sentences as observation |

## Results

**Judges, 8.** Overall: kein 6, omc 2. Per dimension, kein–omc: scope fidelity 6–2, decision completeness 3–5, executability 5–3, gate proportionality 8–0, handoff readability 8–0. Reading order had no effect: each order produced one omc overall.

**Verification.** omc: 87 claims, 77 true, 5 partly, 1 false, 4 uncheckable. kein: 103 claims, 93 true, 2 partly, 4 false, 4 uncheckable. Error rates are the same. kein's false claims are load-bearing: the `glyph-conditional` home list at `plan-B.md:170` says five production sentences where the tree has eight, the missing four including the sole production writer of the kind; `plan-B.md:221` says one audit gate lacks a selftest where four do; `plan-B.md:60` cites an anchor that does not resolve; `plan-B.md:304` says four closed sets where the plan itself says five elsewhere. Two of those were recorded as carried findings at approval and are still in the text. omc's are counts: one export where there are five, three dogfood importers where there is one, four painter modules where there are six, a reference count off by seven.

**Ledgers.** From omc's plan neither reader could dispatch S49-1: the surface's control model is absent (how `[`/`]` selects among four families and five fields; no on-screen readout of which candidate is showing), and S49-4's reveal half has one sentence of direction and an instruction to grep for its own blast radius. From kein's plan both readers found S49-4 labelled SMALL while carrying eight RED demonstrations and thirteen acceptance claims, S49-1 needing the plan's own three-commit split, and the status paragraph contradicting itself ("Not executable until the owner approves D49-1" after saying D49-1 was ruled). Four of kein's seven stories queue behind one owner session by design.

**The two findings that decided the dissenting judges.** kein's S49-0 done-when (`plan-B.md:232`) requires zero references to the moved paths "including `.omc/plans` and `.omc/archive`"; on the base tree 41 of the 47 referring files are archived records that `docs/README.md:57` says are not rewritten. omc scopes the rewrite to six live files, reproduced file-for-file by three judges. The second is the missing kind writer above. Both A-voting judges weighed those over omc's structure; the six B-voting judges weighed the structure.

**omc's structure.** The gate section is 583 of 1,232 lines, 47 percent, guarding a two-file move and a constants record; 292 references to its own revision rounds; 207 warning signs against kein's 3. It ran codex lanes against the kickoff's exclusion and records having edited the kickoff document. It re-asks a direction the kickoff records as given (spacing mark cardinality, `plan-A.md:1128` offers the shipped form as a candidate) and strikes the owner-stated rider. It asserts the mark change keeps the svg obligation untouched (`plan-A.md:482`) where the base tree gives every strip and apron root its own glyph, so one mark per edge is an ownership change; kein designs that change (C49-4) and omc does not see it.

## Two corrections to the raw outputs

The base tree predates both plans' own work. omc's four gate scripts, which both `ledger-A` readers and one judge treated as absent and therefore as hidden authoring work, exist in omc's worktree, committed with the plan (`b720628`). Discount every sentence in `ledger-A-*` and `judge-AB-2` that rests on their absence. kein's owner-pass validator is likewise absent by design and the plan says so.

Second, the executability standard the ledger readers applied is kein's own (`task-ledger-template.md`'s gate: bounded outcome, ordering without inventing a material decision, completion condition, verification path). It is a reasonable definition, and it is kein's.

## Harness finding

kein's ralplan receipt carries four findings addressed to the executor. kein's execute run for this phase (`260904-193412-phase-49-surface`) carries none of them: nothing in its state names the missing kind writer, the selftest uniqueness claim, the B2 plant location or the synthetic-overlap owner. The carry stops at the receipt. The two findings the dissenting judges weighed most were both in that receipt.

## Reading against phase-48

In phase-48 the gate weight sat on kein (212 KB plan, 45 KB gate section, 18 rounds). In phase-49 it sits on omc (246 KB, 47 percent gates, 5 rounds) and kein closed in three rounds at 134 KB over four carried findings. Same leads, same kickoff. One phase each way says the harness is not the dominant variable in how a lead frames a topic, and that what a harness can do is make the framing visible and bounded, which is what the ralplan verdict change did for kein this time.

## Limits

n = 1 per harness. Eight judges of one model family scoring two plans written by another model of the same family. Reading-order was controlled; nothing else was. The execute results, due within a day, are the measurement this one precedes.
