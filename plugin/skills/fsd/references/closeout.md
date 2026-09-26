# Closeout

The run is done when every decision the agents took on the user's behalf can be answered with one pointer to where it was recorded, and the user has one report to read.

## Stale documents, inside `execute`

After the last plan task is accepted and before `execute`'s Finalization, find the project documents the change made stale. Run a read-only `kein:explore` sweep over docs that name the changed paths, symbols, commands or flags. Append one task per disjoint set of documents. Leave `AGENTS.md` and `CLAUDE.md` out of each task's scope. `execute`'s final audit then covers the edits, which it would not if they were made after it.

## After `execute` ends

In this order:

1. `ocs state fsd closeout <state>`.

   If acceptance criteria remain that this slice could not take -- because their plan needed what this slice revealed, or because [decision-policy.md](decision-policy.md)'s split route removed their story from this slice's plan -- take this branch instead of steps 2-5 below.
   - `ocs state fsd continue <state> --covered <AC ids, comma-separated, e.g. AC1,AC3> --reason <what the next slice needs that could not be planned before, or which split story it carries and why it was split>`. `AC<n>` names the requirements' `## Acceptance criteria` checkboxes, in document order.
   - From here on, use the path `continue` prints, and invoke the stage its own `gap` names exactly as printed.
   - Give that slice's own plan a path of its own, never one an earlier slice's plan already used.
   - If `continue` refuses because a question is unanswered, close this slice with steps 2-5 below instead -- lessons, the retrospective, `close`, and `report`. The run pauses; once the question is answered and the run resumed, `gap` names closeout again, so run step 1 and take this branch again.
   - If `continue` refuses because no approved requirements document is linked to this run to continue from -- an execute-entry run, or one whose requirements are not yet Approved -- this run cannot chain: fall back to steps 2-5 below.
2. Propose lessons for AGENTS.md: what this run taught that the next run in this repository should know and could not find by looking. Record each with `ocs state fsd lesson <state> --line <the proposed line> --why <what happened>`, and never edit AGENTS.md. If nothing was learned, record no lesson and write "no new lessons" in the retrospective. A lesson made up so that the list is not empty is worse than none.
3. Write the retrospective under this run's own directory, next to its `state.json`. `close` moves it to `ocs state-dir retros/` once the run completes. It has these sections:
   - **Outcome:** the requirements, plan and `execute` receipt paths.
   - On a chained run, **Slices:** every slice's plan, receipts and continue reason, from `report`'s `## Slices` section.
   - **Stages:** the entry stage, `ralplan`'s rounds, and the tasks accepted and parked.
   - **Assumptions:** every A<n>, with its reversal cost, the ones the user is most likely to veto first. The user reads this once, so the ones they would reverse must come before the ones they would accept without reading.
   - **Parked questions:** every Q<n>, with the recommended option.
   - **What cost the most:** the rounds, retries or detours that took the most time, and why.
   - **Lessons proposed:** every L<n>.

   `close` refuses a retrospective that leaves any id out.
4. `ocs state fsd close <state> --retro <path>`. It pauses the run when a question is unanswered, and completes it when `execute` completed. When it refuses, run `ocs state fsd halt <state> --reason <its refusal>`. `halt` itself refuses in three cases -- the run's lifecycle is not `active`, `--reason` is empty, or `close` would in fact succeed once its own complaint is fixed -- but only the third is ever reached from this step: the run is still active here, and `--reason` is `close`'s own printed refusal, never empty. So if `halt` answers that close would succeed, fix what `close` named -- a missing file, missing ids, a retrospective outside `.agents/kein/runs/` while a question is unanswered and `execute` is still live, a durable path already taken -- and close again. Otherwise the run is halted, and nothing is repaired afterwards.
5. Print `ocs state fsd report <state>` verbatim as the final message. Do this whatever the outcome. A paused run's report already says how to answer, by re-invoking `/kein:fsd Q1=<answer> …`.

## Bringing the run to rest

The Stop hook's no-gap block fires on every no-gap Stop over an active run whose running stage is not `interview`. `ocs state fsd gap <state>` shows a diagnosis only when the running stage itself still has no run linked yet; otherwise it reports no gap, since `gap()` never raises a row for a stage that is merely still going. This section is what to do once a run in that shape should stop rather than keep going -- waiting on the user, or on a lead's own judgment that it should not continue.

There are two exits, sharing one tail, differing only in whether a question is recorded first:

- **Pause it for the user:** record a question parked against the whole run -- `ocs state fsd question <state> --stage <running stage> --question <text> --recommended <text> --why-irreversible <text> --parks 'whole run'` -- unless a question parking the whole run is already unanswered, which would otherwise mint a duplicate the user still has to answer.
- **End it outright:** skip the question and go straight to the tail below.

Then, either way:

1. `ocs state fsd closeout <state>`, unless closeout is already the running stage.
2. `ocs state fsd close <state> --retro <path>`, with the retrospective placed under this run's own directory and citing every assumption, question, and lesson id.
3. If `close` refuses, run `ocs state fsd halt <state> --reason <close's own refusal>` naming that refusal as the reason. If `halt` itself answers that close would succeed, fix whatever `close` named -- the retrospective, most concretely -- and close again.

Ending changes only this run's own state: a stage run still live underneath it -- `execute`'s own worktree claim, most concretely -- stays active and keeps occupying the worktree for whatever flow comes next, which is why pausing is the one to prefer while a stage run is genuinely still live.
