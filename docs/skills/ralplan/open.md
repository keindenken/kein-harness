# `ralplan`: what is still open

Observed during the e3-v3 fixture round in `descvi/kein-e3v3`, with the harness pinned at `fb55678`. Nothing here has been acted on: the instrument is fixed for the length of that run, so any change waits for it to finish.

## A fresh lane is not blind, and the artifact contract is why — closed 2026-08-19

Closed by `927f460`: the lane package drops both status lines, which `review_text()` was already excluding from the hash.

`review-contract.md` requires each lane package to contain "the complete current canonical plan", and one paragraph later requires that "a fresh reviewer receives no previous finding, verdict, reviewer identity, revision note, change summary, claimed fix, closure result, or expected outcome."

`plan-gate.md` requires the artifact to carry a `Status reason` saying why approval is absent. Round 5 of the fixture run opened with this one:

> Round-4 findings were addressed by Planner revision and every round-4 verdict (including the architect PASS) invalidated by the content change.

That is a previous verdict, a revision note, a change summary, and a claimed fix — four of the eight forbidden items — delivered to a fresh Architect and Critic inside the artifact the contract mandates including. Nothing in either file excludes the status lines from the package.

The code already knows those lines are not review content: `review_text()` strips both by line prefix before hashing, which is what makes a status-only edit leave the review hash stable. The strip exists for the hash and was never extended to the package.

This is not a cost question. Blind lanes are the whole mechanism the consensus gate rests on, and after the first round they have not been blind.

## The post-revision checkpoint is required by the state machine

An earlier version of this file recorded that checkpoint as a state the lead invented because no workflow step names it. That was wrong, and the correction is the interesting part.

`validate_transition` refuses to open `In Review` while the previous state carries unresolved findings, and step 6 requires those findings to be persisted. So `Draft(revising, findings) -> In Review` is rejected outright, and the run has to pass through a `Draft` checkpoint that clears them. Clearing them is itself gated: a same-hash `Draft` that drops its findings is rejected too.

Together those two rules say **findings may only be dropped by actually changing the plan**, and the checkpoint in the middle of the round is where that is enforced. It is the mechanism that makes a `MUST_FIX` unskippable. The prose not mentioning it is a documentation gap; the call is doing real work.

## `Status` carries two facts and can only express one — closed 2026-08-19

Closed by `3e6d97b`, verified by replaying the run's 70 candidates for zero difference and by six constructed cases. Two of them showed the change was not cosmetic: under the new convention the old code accepted re-entering review without advancing the round.

`plan-gate.md` gives `Draft` three meanings: before review, after a must-fix verdict, and for a terminal unapproved plan. A reader who opens the artifact cannot tell an abandoned plan from one whose Planner is mid-revision, and the field flips twice within about half an hour of wall clock on a live round.

The alternative reading is that `Status` should answer only "is a gate running over this artifact" — `Draft` when no run is open, `In Review` for the length of a run including its revisions, `Approved` when it passed. `phase` already exists and already carries `revising` / `drafted` / `reviewing`, so the sub-state has a home that is not the artifact header.

The mechanism does not object. What the state machine actually protects is the findings-and-hash invariant above, which it happens to express on `plan.status`; expressing it on `phase` would preserve it exactly while freeing `Status` to mean one thing. That is the change to weigh, not the flip itself.

## The two-field header is not the only shape

The incumbent artifacts in `descvi` use a single free-form line — `Status: APPROVED — two-vendor unanimous consensus, 2026-08-17` — rather than a fixed token plus a separate `Status reason`, and that is the preferred style here.

`validate_plan_text` currently rejects it twice over: it requires exactly one `Status:` whose stripped value is exactly `Draft`, `In Review`, or `Approved`, and separately requires a non-empty `Status reason`. Accepting `Status: <state> — <free text>` and dropping the second field is a small parser change, and `review_text()` already strips by line prefix, so one merged line stays out of the review hash without any further work.

Note that merging the fields does not fix the blindness leak above. That one is fixed by stripping the status lines from the lane package, and the two changes are independent.

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

## The rounds were doing real work, and an earlier reading here said otherwise

An earlier version of this section read the `verdicts` map, saw one lane recorded and the other `null` in every blocked round, and concluded that two blind readers were sampling a large document and each surfacing a different item. That was wrong, and the way it was wrong is worth keeping.

`verdicts` is not where a round's review lands. `findings` is, and every finding carries its lane. Read there, eleven of the sixteen blocked rounds carry findings from **both** lanes; only five are single-lane. No review was discarded. What the partial `verdicts` map shows is that the ledger records one lane's verdict and then clears the map at the next checkpoint, which is a completeness gap in the record and not a gap in the review.

The findings series is `8 5 4 4 5 5 4 4 3 2 3 2 1 2 1 3` and then a clean pass. Noisy, and downward.

The late rounds are not nitpicks either. Round 16 blocked on a `LIVE` evidence tier attached to something its own source files as not-measured, and on an acceptance bound that can go RED on a correct implementation — both squarely inside what the review contract calls blocking, and the second is the repository's own "a gate must be able to fail" invariant pointed at the plan. Round 15 blocked on an amendment contradicting two cells it never dispositioned.

So the seventeen rounds are not ceremony, and the round count on its own does not say the loop is inefficient. What it costs and what it caught have to be weighed separately, and the caveat on the incumbent's seven is that its planning began with the spike context still in the session rather than reconstructed from the artifact.

## The five-round diagnostic trigger fires once and never re-arms — closed 2026-08-19

Closed by `927f460`: a decision to continue covers five rounds rather than the run.

The skill says around five unsuccessful official rounds is a diagnostic trigger, that the run should reassess whether the problem needs user authority, missing evidence, a bounded conditional plan, or an explicit `Draft` handoff, and that approval must not be manufactured from repetition.

It fired at round 5, the owner was asked whether to continue, and the run went twelve more rounds without asking again. The prose names a threshold and no interval, so a trigger answered once is answered forever.

## What "the script earns its place" now means

The criterion recorded here is whether the skill runs without friction, not whether it enforces the artifact's rules — the plan wants more freedom in its shape, not less, and the ledger's resumability across a compaction or a vendor switch is a hedge rather than the point.

Those pull on two different halves of `state.py` and only one of them is the artifact's rules. `validate_plan_text` is the half that governs shape: exactly one `Status` token from a fixed set, a non-empty `Status reason`, a level-one title, and a labelled field on every Evidence Gate. That half is what "plans should be freer" is about.

`validate_transition` is the other half, and it governs nothing about shape. It is what makes a `MUST_FIX` unskippable and what stops a changed plan from keeping an old approval. Relaxing it does not buy freedom in the artifact; it removes the gate's ability to fail, which is the thing the whole workflow exists for.

Keep them apart when acting on any of this.

## Still open

**The two-field header.** The incumbent's single free-form `Status: APPROVED — two-vendor unanimous consensus, 2026-08-17` is the preferred shape and `validate_plan_text` still rejects it twice over. Untouched.

**`ocs team` never creates a worktree.** It addresses the current directory as an existing Orca worktree — `orca terminal create --worktree "path:$PWD"` — and Orca's own model would give each worker its own, which `orca worktree create` exists for. One invocation is one worker and several lanes come from backgrounding several invocations, so today that is N write-capable workers in one tree. The lead prompt's rule that a file a worker is writing is not yours to touch covers lead against worker and says nothing about worker against worker. This goes live the moment `execute` is exercised.

**The phase-46 comparison is worked through.** Its table in `260826-phase-46-comparison.md` carries the disposition of every item; the phase-47 ledger under `docs/artifacts/ledgers/` is what closed the ones that needed a run to answer. Two are folded rather than done: the sizing declaration, because a run that reached `plan`'s Sizing section and one that never did produced round-one plans three lines apart, and `validate-plan` in the Planner prompt, because the check it would have caught no longer exists. What is still open there is the standardisation A/B, which needs a run rather than a decision.

**`dev/eval/run.py` leaves its arm worktrees behind.** Ten had accumulated, about 11 MB per run, removed 2026-08-19. Nothing is lost by removing them — `artifacts/<arm>/<n>/PLAN.md` holds each replicate's output and `manifest.json` records the arm commits in full — which is exactly why the runner should do it itself.

## Raised 2026-09-24

**The `Status` line still reaches a fresh lane.** Seen in the e3-v4 run (`e3-v4` worktree, plan `plan-e3-v4.1-position-model.md`, codex Architect and Critic lanes). Round 6 opened with:

> Status: In Review — ralplan round 6 open: rounds 1 to 5 blocked (both lanes), the plan was revised after each, and fresh codex Architect and Critic lanes are reviewing it; not approved, so not yet executable.

That is a round number, earlier verdicts, and the fact of a revision, all on the contract's forbidden list, and round 5's line also carried a change summary ("redesigned around candidate verification and compiler classification").

The package was not the leak. All twelve `runs/ask/*/prompt.txt` traces carry the plan inline with no `Status:` line, so the lead stripped it as told. The lane read it anyway: the round-6 architect's `stderr.txt` shows it recomputing the review hash its package gave it, by reading `.agents/kein/plans/plan-e3-v4.1-position-model.md` from disk and stripping `^Status:` itself, then running `sed -n 1,12p` and `git diff` on the same file, both of which print the line. Every trace's `stderr.txt` contains the `Status: In Review` line one to four times. So a lane that sits in the same worktree and is handed a hash to check will open the artifact, and removing the line from the package cannot stop that.

Where a fix can live, cheapest first: keep the reason neutral while a gate is open (`In Review` needs no reason a reader cannot get from state — the round history is what `phase` and the ledger are for), so the line leaks nothing whichever route a lane takes; or stop handing lanes the hash, which is the thing that sends them to the file; or keep the working artifact outside the lane's readable tree while in review. The first is a rule change in `plan-gate.md` ("the reason half additionally carries the current workflow phase and why approval is absent" is what asks for the history today). Separately, `plan-gate.md` still says the contract "removes two lines" where the contract now removes one.

**Pasting the plan is itself required, and it is not free.** The package is not assembled by `ocs ask`; the lead writes it, so every round spends the whole plan as the lead's output tokens, once per lane — the round-6 architect package was 463 lines, most of it the plan. Native lanes pay the same in the Agent prompt, so this is not a codex question. The instructions that require it: `review-contract.md` ("the complete current canonical plan, with its `Status` line removed"), `SKILL.md` step 5 ("Each receives the complete current plan"), and `plan-gate.md` ("The package a fresh lane receives is this artifact whole").

The owner's direction, not yet acted on: move the run's account out of the artifact into state (`state.json` already carries `phase`, `round`, `findings` and `next_action`), delete the rules that make the `Status` reason carry it, and the lead will then naturally hand lanes a link rather than a copy — which the strip-the-line rule is the only reason not to do today. What that touches, found while reading and not changed:

- `plan-gate.md` "The reason half additionally carries the current workflow phase and why approval is absent" — the rule that asks for the history.
- `SKILL.md` step 6 "set Draft with a concrete reason" (already stale: `plan-gate.md` keeps `In Review` through revision) and step 7 "explain the approval, what it stands over, and any bounded Evidence Gates in the `Status` line's reason". What an approval stands over already survives in the receipt's findings and deferrals.
- `review-contract.md`'s package item and its "The removed line is why" paragraph, and the `plan-gate.md` paragraph under "What the body may not narrate" that argues from the package carrying the body whole. The no-narration rule itself still holds when a lane reads the file, so it keeps its place with a different reason.
- `state.py` `STATUS_LINE_PATTERN` and `validate_plan_text` require `word — non-empty reason`; a bare `Status: In Review` would be refused. `fsd`'s input classifier goes through the same validator. `dev/libexec/check-ralplan-state`'s `header()` always writes a reason.
- `plan`'s template keeps `Status: Draft — <reason>` for a standalone plan, which is fine: the lead replaces it with `In Review` at round 1.
- **`fsd` depends on the reason.** `fsd/references/decision-policy.md` step 5 has the approving `Status` line name every deferral and parked story, and the paragraph after it puts a deferred ground's `Caught by` in the `Status` line because revising the plan would reopen the round. That has to move to the receipt or state along with the rest.

A link does not make a lane blind to history either: the plan file is in the worktree the lane reviews, and `git log` or `git diff` on it shows earlier revisions whenever Planner's revisions are committed between rounds. In e3-v4 it was an untracked-then-new file, so the diff showed only the current text.

**`--planner codex`.** Considered for `ralplan`, and possibly `plan`, as the counterpart of `execute`'s `--executor codex`. The owner once passed it by mistake, believing it existed, and the run went through without visible trouble, so the lead improvised something that worked; what it actually did is not recorded. Adding it means a Planner row in `lanes.md` and deciding how a codex Planner revises the same artifact across rounds, since a codex call cannot be continued.
