# fsd slice chain

Status: Approved
Date: 2026-09-26

## Context

Some work needs its next plan written only after an earlier part is implemented, because that plan depends on what the implementation reveals: a measurement, a real API's shape, whether an approach holds. Today one `/fsd` run carries exactly one `ralplan` and one `execute`: its state has four fixed stage slots (`interview`, `ralplan`, `execute`, `closeout`), `gap` names the next stage only in that order, and `start` refuses while a nonterminal fsd run exists for the worktree. Such work therefore needs a human to start a second run, which defeats an unattended flow.

## Desired outcome

One `/fsd` invocation can carry work through `interview → ralplan 1 → execute 1 → ralplan 2 → execute 2 → … → closeout`, with the user taking part only at the interview and the final report. Each `ralplan → execute` pair is a slice, held in its own fsd state, and the states are chained.

## Scope

### In scope

- A way to end a slice and start the next one: `close --continue` (spelling is a decision boundary), which records the acceptance criteria the slice covered, closes the current state, and starts the next state at `ralplan` in one command.
- A link from each chained state to its predecessor, and whatever the chain needs to compute the criteria that remain.
- `gap`, `status`, `report`, `close` and the hooks behaving correctly on a chained state.
- A single retrospective and a single report for the whole chain, written by the last state's closeout.
- Documentation: a conditional line in `plugin/skills/fsd/SKILL.md`, a continue branch in `references/closeout.md`, `references/state-schema.md`, and `references/decision-policy.md`'s split-story sentence.
- Oracle coverage in `dev/libexec/check-fsd-state` and `dev/libexec/check-fsd-hooks`.
- A shorter Stop-hook block reason for an active run with no gap, with the procedure for bringing a run to rest moved into `references/closeout.md`.

### Out of scope

- A live chained run (deferred; see Deferred items).
- A count of slices fixed at start, or a `--max-slices` cap.
- A gate on the final `close` requiring every acceptance criterion to be covered.
- Numbering acceptance criteria in the interview's requirements template.
- A prose rule on when to split into another slice.

## Requirements

- The todo of a chain is the approved requirements document's `## Acceptance criteria` checklist. `## Deferred items` is never part of it.
- Coverage is recorded once per slice, when that slice is continued. The criteria that remain are all criteria minus every criterion covered by any earlier slice of the chain.
- The continue command refuses, and leaves the current state exactly as it was, when any of these holds:
  - the chain has no approved requirements document (the run entered at `execute` with a plan only);
  - an fsd question is unanswered;
  - `execute` has not completed;
  - the covered set is empty, or adds no criterion not already covered (the progress guard);
  - a named criterion does not exist in the requirements;
  - no criterion would remain after this slice.
- On success, the current state reaches a terminal lifecycle and the next state exists, active, entering at `ralplan` with the same requirements document as input, and linked to its predecessor. If creating the next state fails, the current state stays active.
- The continue command records why the chain continues (what the next slice needs that could not be planned before), and the final retrospective shows it for every slice.
- On the next state, `gap` names `ralplan` with the requirements path and the remaining criteria, and the `ralplan` invocation receives the remaining criteria and the earlier slices' receipts.
- A mid-chain close writes no retrospective and no report. The last state's `close` requires a retrospective citing every assumption, question and lesson id across the whole chain, and `report` lists every slice's plan and receipt.
- Assumption, question and lesson ids are unique across the chain.
- The hooks work on a chained state as on any other: the Stop hook blocks while it is active, and `ocs state ralplan start` / `ocs state execute start` link to the chained state.
- The decision-policy split route's removed story becomes a candidate for the next slice instead of a separate pass after the run.
- The Stop hook's block for an active run with no gap says only: the run and its running stage; that a lead waiting on another lane may end the turn once it has confirmed that lane is alive; that otherwise the stage continues, with `ocs state fsd gap <state>` for why it is stuck; and where in `references/closeout.md` the procedure for pausing or ending the run lives. It does not quote `next_action`, which is not updated as stages advance, nor the diagnosis, which `gap` prints. The pause/end procedure it carries today, including what to do when `close` refuses and when `halt` answers that close would succeed, moves to that section intact.

## Constraints

- A state file written by the current schema loads, validates and behaves exactly as before under the new code.
- Implementation happens in a separate git worktree on its own branch. `~/.claude/skills/kein` is a symlink to the main checkout's `plugin/`, whose hooks other live fsd sessions execute; edits in the worktree do not reach them before merge, and the merge replaces the code under any fsd run still live on main.
- `stages` keeps its four fixed slots; the chain is built from whole states, not from a phase list inside one.
- Repository rules in `AGENTS.md` apply, including no model names in prompt prose.

## Decision boundaries

- How a criterion is identified (for example by its order in the document), the new field names, and whether a schema version moves.
- Whether earlier slices' assumptions, questions and lessons are copied into the next state or read through the link.
- The exact CLI spelling of the continue command and its arguments.
- How the remaining criteria and earlier receipts are handed to `ralplan` (for example through `gap`'s action text), provided `ocs state ralplan start --input` stays the approved requirements path.

## Acceptance criteria

- [ ] When every precondition holds, the continue command closes slice k and creates slice k+1 in one command; a failure while creating k+1 leaves k active and unchanged.
- [ ] Each refusal listed under Requirements is exercised by an oracle section and leaves the state unchanged.
- [ ] `gap` on slice k+1 names `ralplan` with the requirements path and the remaining criteria.
- [ ] The last state's `close` refuses a retrospective missing any assumption, question or lesson id from any slice, and `report` lists every slice.
- [ ] On slice k+1, the Stop hook blocks while it is active, and `ralplan start` / `execute start` are linked to slice k+1 by the hooks.
- [ ] A state file written by the current schema behaves as before; `check-fsd-state`, `check-fsd-hooks`, `check-execute-state`, `check-ralplan-state`, and `claude plugin validate plugin --strict` pass.
- [ ] The Stop hook's no-gap block reason names no command other than `ocs state fsd gap <state>`, and carries neither `next_action` nor the diagnosis; `references/closeout.md` holds the pause/end procedure it no longer carries; `check-fsd-hooks` pins the new reason and `check-fsd-state` or a docs check pins the procedure's presence.
- [ ] `SKILL.md`, `closeout.md`, `state-schema.md` and `decision-policy.md` describe the chain.

## Decisions and rationale

- **Chain whole states, not a phase list:** the stage machinery (attach, belonging checks, hooks, park, closeout) was verified at real cost and is reused per state unchanged.
- **No count and no cap:** the number of slices cannot be known at start; the progress guard catches a runaway more precisely than a number.
- **No separate todo ledger:** the acceptance criteria already are the todo; a second record would have to be kept in agreement with it.
- **Coverage recorded at slice end only:** no plan-time deferral declaration is needed when what remains is computed from what was covered.
- **Continue is one command:** a gap between closing k and starting k+1 would leave no active run, and the Stop hook would let the turn end there.
- **An unanswered question stops the chain:** an `execute` run with a parked task stays nonterminal and occupies the worktree, so the next slice's `execute` could not start; the chain pauses as a run does today and continues after the answer.
- **Shorter Stop-hook reason:** the block fires every time a turn ends while the run waits on a lane, the common case needs one sentence, and the rare pause/end procedure already has a home the lead reads on that path.
- **No prose split rule:** ralplan's deferral test already states the principle, and a strict form would block continuing a story split off for non-convergence. The recorded reason for continuing, shown in the retrospective, is the measurement instead.

## Relevant system evidence

- `plugin/skills/fsd/scripts/state.py:224`: `stages` must name exactly interview, ralplan, execute, closeout.
- `plugin/skills/fsd/scripts/state.py:1659` (`start`): refuses while a nonterminal fsd run exists for the worktree.
- `plugin/skills/fsd/scripts/state.py:1388` (`close`): pauses on an unanswered question, completes when execute's side is done, otherwise refuses.
- `plugin/skills/execute/SKILL.md:52`: finalization waits for parked tasks.
- `plugin/skills/interview/references/requirements-template.md:41`: acceptance criteria are `- [ ]` checkboxes.
- `plugin/skills/fsd/references/decision-policy.md:61`: a split story goes back through its own pass after the run.
- `plugin/skills/ralplan/references/review-contract.md:65`: deferral is for evidence that does not exist until the code does.

## Assumptions and risks

- Coverage is the lead's own claim; the progress guard catches a slice claiming nothing new, not a slice claiming falsely.
- Merging into main swaps `state.py` and `hook.py` under any fsd run still live there; the backward-compatibility constraint is what keeps such a run's state valid.
- Requirements whose acceptance criteria are not `- [ ]` checkboxes cannot be continued.

## Deferred items

- A live chained run: measured on the next real use that needs one; recorded in `docs/skills/fsd/open.md`.
