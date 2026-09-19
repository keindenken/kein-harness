# Closeout

The run is done when every decision the agents took on the user's behalf can be answered with one pointer to where it was recorded, and the user has one report to read.

## Stale documents, inside `execute`

After the last plan task is accepted and before `execute`'s Finalization, find the project documents the change made stale. Run a read-only `kein:explore` sweep over docs that name the changed paths, symbols, commands or flags. Append one task per disjoint set of documents. Leave `AGENTS.md` and `CLAUDE.md` out of each task's scope. `execute`'s final audit then covers the edits, which it would not if they were made after it.

## After `execute` ends

In this order:

1. `ocs state fsd closeout <state>`.
2. Propose lessons for AGENTS.md: what this run taught that the next run in this repository should know and could not find by looking. Record each with `ocs state fsd lesson <state> --line <the proposed line> --why <what happened>`, and never edit AGENTS.md. If nothing was learned, record no lesson and write "no new lessons" in the retrospective. A lesson made up so that the list is not empty is worse than none.
3. Write the retrospective under this run's own directory, next to its `state.json`. `close` moves it to `ocs state-dir retros/` once the run completes. It has these sections:
   - **Outcome:** the requirements, plan and `execute` receipt paths.
   - **Stages:** the entry stage, `ralplan`'s rounds, and the tasks accepted and parked.
   - **Assumptions:** every A<n>, with its reversal cost, the ones the user is most likely to veto first. The user reads this once, so the ones they would reverse must come before the ones they would accept without reading.
   - **Parked questions:** every Q<n>, with the recommended option.
   - **What cost the most:** the rounds, retries or detours that took the most time, and why.
   - **Lessons proposed:** every L<n>.

   `close` refuses a retrospective that leaves any id out.
4. `ocs state fsd close <state> --retro <path>`. It pauses the run when a question is unanswered, and completes it when `execute` completed. When it refuses over the retrospective (a missing file or missing ids), fix the retrospective and close again. On any other refusal, run `ocs state fsd halt <state> --reason <its refusal>` and repair nothing afterwards.
5. Print `ocs state fsd report <state>` verbatim as the final message. Do this whatever the outcome. A paused run's report already says how to answer, by re-invoking `/kein:fsd Q1=<answer> …`.
