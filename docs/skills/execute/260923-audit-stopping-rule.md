# The first run to stop its final audit by rule (2026-09-23)

Run `260923-140504-fsd-run-fixes`, plan `.agents/kein/plans/260923-fsd-run-fixes.md`: five fixes the first live `fsd` run earned (`docs/fsd-test-run-260922-descvi-ki.md`), plus a sixth task the audit itself exposed. Completed with a final audit of five passes, the last a `critic` REVISE carrying four findings — the first completion that went through the stopping rule this run wrote into `review-contract.md`, rather than through a pass that happened to find nothing.

## What it cost

| Task | What it changed | Rounds to accept |
|---|---|---|
| task-001 | `gap`'s `diagnosis`; `attach`'s terminal-candidate sentence | 6 |
| task-002 | the occupant block's five facts | 2 |
| task-003 | the Stop hook's mid-stage block | 8 |
| task-004 | `park`'s second route, clean against HEAD | 4 |
| task-005 | the fsd reference and skill text | 3 |
| task-006 | a final-audit REVISE that carries can complete | 1 |

Final audit: five passes. Passes 1 and 2 corrected everything they found. Pass 3 found task-003 still short of its condition. Pass 4 found that the stopping rule itself could not complete. Pass 5 was the first pass allowed to carry what it found.

## What found the holes

**The `kein:test-engineer` lane, once it was used.** `review-contract.md` requires one in every round whose task names a check, and every task here named one. The lead omitted it until final audit pass 3. From then on every task-003 round carried one, and each found an oracle hole the code-reading lanes had passed over: a closing instruction replaceable wholesale with the check still green; an off-switch offer in prose that no spelling list could see; a golden-text window that began one sentence too late. The contract's own sentence — "the holes that survived a review were oracles nobody read" — described this run before it happened.

**Walking the real CLI, not reading it.** The mid-stage block's first two-exit design read correctly and was wrong: a critic drove it with `ocs` and found that a structural `close` refusal — a guard violation, or AGENTS.md drift — left the pause exit dead-ended while the reason forbade `halt`, the only command that worked. The fix that held stopped the reason predicting the state machine at all: *if close refuses, halt; if halt says close would succeed, fix what close named.* `halt`'s own refusal is the signal, so the text is true in every state without knowing which one it is in.

## What the lead got wrong

- **Three briefs carried a wrong premise, and each cost a round.** Registration of carried findings through `kein-findings` (that plugin records runtime behaviour, not defects under review); "the mid-stage block names no command at all" (it names three, resolved); a `_running_stage` hole that turned out to be unreachable, whose fix was then deleted.
- **The ledger's times before audit pass 3 are invented.** `observed_at` and `reviewed_at` were written as round-minute values, some in the future, rather than read from a clock. Nothing refused them. Carried in the receipt as an `important` finding.
- **A comment-reflow script fused a section separator with its header**, and the next audit pass had to find it.

## What the harness got wrong

- **The stopping rule could not stop.** As first written, a pass from the third on carries what it finds and so answers REVISE — but completion accepted PASS only. The rule could end an audit only by relabelling a REVISE as PASS. task-006 held the final audit to the same verdict coherence as an acceptance, matched by `reviewer_role`, and required `carried_because` on an above-minor run-level carry.
- **`check-execute-state` now takes about four and a half minutes**, longer than a single tool call holds. Lanes backgrounded it and returned "waiting" as their result four times; the lead restarted each, and one took the whole session down with it. The working fix was for the lead to run the long suite itself and brief lanes to stop at the scoped section.

## Where the carried findings went

Into the receipt's `carried_findings`, and into `docs/skills/execute/open.md` and `docs/skills/fsd/open.md` as open items with what would reopen each.
