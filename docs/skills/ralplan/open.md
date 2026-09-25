# `ralplan`: what is still open

Observed during the e3-v3 fixture round in `descvi/kein-e3v3`, with the harness pinned at `fb55678`, and by later runs noted inline below. Most of what that fixture round raised has since closed; `docs/skills/ralplan/closed.md` holds it.

## What the run cost, measured — the four-checkpoint cycle closed 2026-08-19

The cycle is three states as of `4eef755`, and `b48c0b1` replaced the hand-authored candidate with one command per transition. The rest of this section is the measurement and stands.

The e3-v3 fixture round completed at round 17 in about six hours, against seven rounds for the same input under the incumbent harness. The artifacts are comparable — 846 lines and 195,142 bytes here, 877 lines and 162,842 bytes there — so the extra ten rounds did not buy a larger plan.

Every blocked round ran the same four-checkpoint cycle, and the ledger has one candidate file per checkpoint:

| | `Status` | phase | what it records |
| :--- | :--- | :--- | :--- |
| 1 | `In Review` | `reviewing` | the round opens, verdicts empty |
| 2 | `In Review` | `reviewing` | one lane's `MUST_FIX` |
| 3 | `Draft` | `revising` | blocked, findings persisted, verdicts cleared |
| 4 | `Draft` | `drafted` | the revision landed, findings cleared |

**Row 2 is erased by row 3.** It writes a verdict that the next checkpoint clears, and it is never read: one `MUST_FIX` already blocks, so the decision does not need it. Its only consumer is a resume after a crash between the lane returning and the revision starting, which is the ledger purpose being demoted here. It is the one row that comes out under a smoothness criterion without touching any invariant.

Rows 3 and 4 are two writes because the state machine expresses the findings-and-hash invariant on `plan.status`. Moving that invariant to `phase` merges them and keeps the enforcement, which is the change already described above.

72 candidate files survive in the run directory. `state-schema.md` says to create one and check it in and never says to remove it, so nothing does. The lead also abandoned its own naming scheme partway: rounds 1-6 are hand-named (`candidate-revising3`, `candidate-redrafted4`, `candidate-round5`), and from round 7 on it is `c1` through `c44`.

## The five-round diagnostic trigger fires once and never re-arms — closed 2026-08-19

Closed by `927f460`: a decision to continue covers five rounds rather than the run.

The skill says around five unsuccessful official rounds is a diagnostic trigger, that the run should reassess whether the problem needs user authority, missing evidence, a bounded conditional plan, or an explicit `Draft` handoff, and that approval must not be manufactured from repetition.

It fired at round 5, the owner was asked whether to continue, and the run went twelve more rounds without asking again. The prose names a threshold and no interval, so a trigger answered once is answered forever.

## Still open

**The phase-46 comparison is worked through.** Its table in `260826-phase-46-comparison.md` carries the disposition of every item; the phase-47 ledger under `docs/artifacts/ledgers/` is what closed the ones that needed a run to answer. Two are folded rather than done: the sizing declaration, because a run that reached `plan`'s Sizing section and one that never did produced round-one plans three lines apart, and `validate-plan` in the Planner prompt, because the check it would have caught no longer exists. What is still open there is the standardisation A/B, which needs a run rather than a decision.

## Raised 2026-09-24

**The `Status` line still reaches a fresh lane.** Seen in the e3-v4 run (`e3-v4` worktree, plan `plan-e3-v4.1-position-model.md`, codex Architect and Critic lanes). Round 6 opened with:

> Status: In Review — ralplan round 6 open: rounds 1 to 5 blocked (both lanes), the plan was revised after each, and fresh codex Architect and Critic lanes are reviewing it; not approved, so not yet executable.

That is a round number, earlier verdicts, and the fact of a revision, all on the contract's forbidden list, and round 5's line also carried a change summary ("redesigned around candidate verification and compiler classification").

The package was not the leak. All twelve `runs/ask/*/prompt.txt` traces carry the plan inline with no `Status:` line, so the lead stripped it as told. The lane read it anyway: the round-6 architect's `stderr.txt` shows it recomputing the review hash its package gave it, by reading `.agents/kein/plans/plan-e3-v4.1-position-model.md` from disk and stripping `^Status:` itself, then running `sed -n 1,12p` and `git diff` on the same file, both of which print the line. Every trace's `stderr.txt` contains the `Status: In Review` line one to four times. So a lane that sits in the same worktree and is handed a hash to check will open the artifact, and removing the line from the package cannot stop that.

Where a fix can live, cheapest first: keep the reason neutral while a gate is open (`In Review` needs no reason a reader cannot get from state — the round history is what `phase` and the ledger are for), so the line leaks nothing whichever route a lane takes; or stop handing lanes the hash, which is the thing that sends them to the file; or keep the working artifact outside the lane's readable tree while in review. The first is a rule change in `plan-gate.md` ("the reason half additionally carries the current workflow phase and why approval is absent" is what asks for the history today).

**Pasting the plan is itself required, and it is not free.** The owner ranks this above the leak it was meant to prevent: the slightly broken blindness is the smaller cost, the plan re-emitted on every review is the larger one. The package is not assembled by `ocs ask`; the lead writes it, so every round spends the whole plan as the lead's output tokens, once per lane — the round-6 architect package was 463 lines, most of it the plan. Native lanes pay the same in the Agent prompt, so this is not a codex question. The instructions that require it: `review-contract.md` ("the complete current canonical plan, with its `Status` line removed"), `SKILL.md` step 5 ("Each receives the complete current plan"), and `plan-gate.md` ("The package a fresh lane receives is this artifact whole").

The owner's direction, not yet acted on: move the run's account out of the artifact into state (`state.json` already carries `phase`, `round`, `findings` and `next_action`), delete the rules that make the `Status` reason carry it, and the lead will then naturally hand lanes a link rather than a copy — which the strip-the-line rule is the only reason not to do today. What that touches, found while reading and not changed:

- `plan-gate.md` "The reason half additionally carries the current workflow phase and why approval is absent" — the rule that asks for the history.
- `SKILL.md` step 6 "set Draft with a concrete reason" (already stale: `plan-gate.md` keeps `In Review` through revision) and step 7 "explain the approval, what it stands over, and any bounded Evidence Gates in the `Status` line's reason". What an approval stands over already survives in the receipt's findings and deferrals.
- `review-contract.md`'s package item and its "The removed line is why" paragraph, and the `plan-gate.md` paragraph under "What the body may not narrate" that argues from the package carrying the body whole. The no-narration rule itself still holds when a lane reads the file, so it keeps its place with a different reason.
- `state.py` `STATUS_LINE_PATTERN` and `validate_plan_text` require `word — non-empty reason`; a bare `Status: In Review` would be refused. `fsd`'s input classifier goes through the same validator. `dev/libexec/check-ralplan-state`'s `header()` always writes a reason.
- `plan`'s template keeps `Status: Draft — <reason>` for a standalone plan, which is fine: the lead replaces it with `In Review` at round 1.
- **`fsd` depends on the reason.** `fsd/references/decision-policy.md` step 5 has the approving `Status` line name every deferral and parked story, and the paragraph after it puts a deferred ground's `Caught by` in the `Status` line because revising the plan would reopen the round. That has to move to the receipt or state along with the rest.

A link does not make a lane blind to history either: the plan file is in the worktree the lane reviews, and `git log` or `git diff` on it shows earlier revisions whenever Planner's revisions are committed between rounds. In e3-v4 it was an untracked-then-new file, so the diff showed only the current text.

**`--planner codex`.** Considered for `ralplan`, and possibly `plan`, as the counterpart of `execute`'s `--executor codex`. The owner once passed it by mistake, believing it existed, and the run went through without visible trouble, so the lead improvised something that worked; what it actually did is not recorded. Adding it means a Planner row in `lanes.md` and deciding how a codex Planner revises the same artifact across rounds, since a codex call cannot be continued.
