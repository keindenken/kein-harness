# fsd and execute: the fixes the first live run earned

Status: Approved — a bounded correction plan written by the lead from a diagnosed run record, not through ralplan. Each story below is traceable to a numbered item in `docs/fsd-test-run-260922-descvi-ki.md`, which is the evidence.

## Source and scope

Evidence: `docs/fsd-test-run-260922-descvi-ki.md`, the descvi remaining-KI batch run (2026-09-22), twelve recorded issues. The owner triaged them on 2026-09-23 and chose five. This plan covers exactly those five.

Classification: a correction. It changes one hook mode, two diagnostics, one state-machine refusal, and two standing prompts.

Non-goals, each a triage decision with its reason:
- Per-story approval in `ralplan` (item 2/3's expensive half). It would re-cut the review hash, which every part of `ralplan` reads as one plan. S6's split route addresses the same cost.
- `attach` accepting a completed interview ledger (item 1b). The belonging rule reached its present shape after three redesigns; admitting a terminal artifact is the design it replaced. S2 gives the lead the diagnosis instead.
- Measurement tooling, and a rule against piping `checkpoint` output (item 6). The first is the other repository's; the second is a rule that was already in memory and was broken anyway, so prose is not the mechanism.
- Lane routing and executor report shape (items 8, 9, 10). Worth doing, deferred as one unit so the codex lane contract is settled once.

Throughout, "verified" means read in this repository at f0f582a.

## Repository facts this plan stands on

- `plugin/skills/fsd/scripts/hook.py` `mode_stop` allows unless `gap()` reports a gap, and returns early when `stop_hook_active` is true, so it can never block twice in a row. `_resolve` returns `None` — read by every mode as allow — for the off-switch, an unimportable state machine, no nonterminal run, or an unloadable state file. (verified)
- `plugin/skills/fsd/scripts/state.py` `gap()` returns `{gap, completed, next, action}` and answers `{"gap": False, ..., "action": "no gap"}` both for a nonterminal lifecycle and for every case where no row fires. A stage that was entered but has no run linked fires no row at all. (verified)
- `status()` is the stage table plus `gap()`. A stage whose association reads `"none"` already carries `association_reason` from `_none_association_reason`, which names the command that would have linked it. A stage that was never entered reads `"not entered"` and carries no reason. (verified)
- `_execute_occupant_block` names the occupant's path and lifecycle and prints an abort command, and describes finishing or aborting it as "decisions for whoever owns that occupant". It has nothing that distinguishes an earlier run of the same lead's from a stranger's. (verified)
- `plugin/skills/execute/scripts/state.py`: `park` is `pending | implementing | correcting -> parked`. `validate_transition` refuses a write-active task's park while its scope differs from `dispatch_scope_fingerprint`, and `validate_external_state` makes the live comparison and names the differing paths. `_scope_content_digest` reads the path list under the scope's pathspec and each path's bytes on disk, with no HEAD anywhere in it. `unpark` drops the seal so the next `dispatch` seals fresh. (verified)
- `worktree_fingerprint` reads `git diff` output, so a HEAD-relative comparison of a scope is already available in this module's idiom. (verified)
- `dev/libexec/check-fsd-hooks` pipes synthetic hook JSON into `hook.py` and asserts each mode's decision; `check-fsd-state` and `check-execute-state` drive the state machines over fixtures. All three support `--list` and `--only <section>`. (verified)

## Stories

### S1 — the Stop hook does not let an active flow end a turn silently

**Issue 5a.** A lead turn ended with no tool call while an unattended run was live, and the run sat idle for about eight hours. The Stop hook was armed and allowed, because a running stage produces no gap.

Scope: `plugin/skills/fsd/scripts/hook.py`, `dev/libexec/check-fsd-hooks`.

Change: in `mode_stop`, when `_resolve` yields a state and `gap()` reports no gap, block once anyway if the run's `lifecycle` is `active`, **except** while the `interview` stage's own status is the one that is running. The interview is the one stage that is supposed to wait for the user, so it keeps the present allow. The reason text names the run's own `next_action`, the diagnosis S2 adds when there is one, and the two ways out: reach a terminal outcome (`closeout`, then `close` or `halt`), or create the off-switch.

Why this cannot loop: `stop_hook_active` already returns allow before any of this, so a blocked stop that comes straight back is allowed through. This is the same guarantee the existing gap block relies on.

Completion condition: a Stop payload over an active run with a running `ralplan` or `execute` stage and no gap blocks exactly once, with a reason naming `next_action`; the identical payload with `stop_hook_active: true` allows; the same run with `interview` running allows; a paused, completed, halted or aborted run allows; the off-switch allows.

Verification path: `dev/kein-dev check-fsd-hooks --only stop` covers the new assertions, then the whole check.

### S2 — an entered stage with no link says so instead of "no gap"

**Issue 1a.** The interview stage never linked, `status` said `association: none`, and `gap` answered `no gap` — a silent dead end. `attach` then refused with "must be a live run of this flow" and nothing about what that left the lead.

Scope: `plugin/skills/fsd/scripts/state.py`, `dev/libexec/check-fsd-state`.

Change, two parts:
1. `gap()`'s no-gap result carries a `diagnosis` field: for each stage that is entered and whose association reads `"none"`, the stage's name and its `_none_association_reason` text; `None` when there is none. `gap` stays `False` — a stage that is merely still running must not block a write or a stop through the existing gap path — so this is a diagnosis, not a new row. `ocs state fsd gap` prints it under the `no gap` line.
2. `attach`'s refusal over a terminal candidate names the consequence as well as the cause: the link is made while the run is live, this stage will stay unlinked for the rest of the run, and the rows that read it (the next stage's own `--input`) will not fire, so the next stage is invoked with the path in hand.

Completion condition: a state whose `interview` is entered with no association reports `gap: false` with a `diagnosis` naming `interview` and the validate command; the same state with every stage linked reports `diagnosis: null`; `attach` over a completed ledger refuses with a message that names both the cause and what stays unlinked.

Verification path: `dev/kein-dev check-fsd-state --only gap` and `--only attach`, then the whole check.

### S3 — a task whose scope moved under a rebase can park

**Issue 4, root cause.** `park` refuses a `correcting` task whose scope content no longer matches its dispatch seal. A rebase changes that content for reasons that have nothing to do with unfinished writes, so the task could never park and its run stayed `active` forever — which is what blocked a later flow three days on.

Scope: `plugin/skills/execute/scripts/state.py`, `plugin/skills/execute/references/state-schema.md`, `dev/libexec/check-execute-state`.

Change: a write-active task whose scope diverges from `dispatch_scope_fingerprint` may still park when its scope is **clean against HEAD** — no staged or unstaged modification under the scope's own pathspec, the run ledger excluded exactly as the existing fingerprint readers exclude it. The question the seal exists to answer is "does this task still hold writes nobody has accepted", and a scope clean against HEAD answers it directly, so this is a second sound route to the same answer rather than an exemption to it. The park record says which route it took and lists the paths that diverged from the seal.

The seal route stays first: a scope that matches its dispatch seal parks as it does today, without reading HEAD. A scope that matches neither is refused as it is today, and the refusal now names both routes.

Completion condition: a `correcting` task whose scope content differs from its seal but is clean against HEAD parks, and its park record names the HEAD-clean route and the diverging paths; the same task with an uncommitted modification under its scope is refused, naming both routes; a task matching its seal parks without any HEAD read; `unpark` is unchanged.

Verification path: `dev/kein-dev check-execute-state --only park`, with a fixture that commits a change under a dispatched task's scope, then the whole check.

### S4 — the occupant row says whose run it is

**Issue 4, diagnosis half.** `gap` framed a three-day-old run of this same lead's as "decisions for whoever owns that occupant", and the printed action was an abort command.

Scope: `plugin/skills/fsd/scripts/state.py`, `dev/libexec/check-fsd-state`.

Change: `_execute_occupant_block` reads the occupant's own receipt for the facts that answer "is this mine, stale?" — its run id, when it started, its last checkpoint's time, and its current phase and task statuses in brief — and prints them before the abort command. A fact it cannot read is omitted rather than guessed, and the block still fires.

Completion condition: an occupant run readable on disk produces a block naming its run id, start, last checkpoint and phase; an unreadable or partial occupant still produces the same block with the missing facts left out.

Verification path: `dev/kein-dev check-fsd-state --only occupant`, then the whole check.

### S5 — the final audit gets a stopping rule (lead-authored prose)

**Issues 11 and 12.** The whole-set audit ran twelve passes and used about half the run; four of the last five each raised a new claim, and one pass's prescription was applied without re-derivation and had to be falsified by the next. Three early passes found only convention breaches, which crowded out the first real defect until pass 4.

Scope: `plugin/skills/execute/references/review-contract.md`, `plugin/skills/execute/SKILL.md`.

Change (the lead writes this prose, not an executor):
- The final audit becomes a sequence with a contract. The first pass is what it is today. Every later pass receives the previous pass's findings **and their dispositions**, and answers two questions only: are these dispositions sound, and is there a defect of a class not yet raised.
- After the second pass, a new finding is registered rather than fixed in this run, unless it is a regression this run itself introduced. Registration is the existing `kein-findings` route, and the receipt's residual risk names it.
- A lane's prescription is not applied without re-deriving it; a pass that only repeats an earlier lane's claim does not license the edit.
- The audit brief asks for substantive findings first and the convention sweep as an appendix.
- Carried over from the fsd plan's U2, in the same edit because it is the same file: delete "Then advance serially." from Task Loop step 7, name `dispatch` in step 1, and say that a task parks rather than blocking the run.

Completion condition: `review-contract.md`'s Final Audit section states the per-pass contract, the registration default and its one exception; `SKILL.md`'s Finalization names it; `SKILL.md` no longer says "Then advance serially."; `docs/skills/execute/open.md` §1 no longer quotes a sentence that is not in `SKILL.md`.

Verification path: `claude plugin validate plugin --strict`; `/kein:instructions --check` over both files; a grep that "Then advance serially" is gone.

### S6 — the contested story has a sanctioned exit (lead-authored prose)

**Issues 2 and 3.** One story of seven produced a blocking ground in every round while the other six had settled, and each round re-reviewed a 400–500 line plan at roughly 600k tokens. The lead's own logged decision — move that story to its own plan and approve the rest — had no route in the skill.

Scope: `plugin/skills/fsd/references/decision-policy.md`.

Change (lead-authored): in the non-convergence section, before the round-5 exit, add the split route. When the standing grounds concentrate on one story while the others have settled, remove that story from the plan, record the removal as an assumption naming what it defers, let the round resolve over the remainder, and queue the split story as its own requirements-to-plan pass after the run rather than holding six settled stories behind it. The round-5 exit stays what it is for grounds that are spread across stories, which is what this run's own rounds 4 and 5 actually were.

Also: the occupant rule stops saying "another operator's run" and starts saying what the lead now sees. With S4's facts printed, the judgment is whether the occupant is this flow's own worktree work under a different run — abort it only on the evidence S4 prints, and park the decision when that evidence does not settle it.

Completion condition: `decision-policy.md` carries the split route and the evidence-based occupant rule; the round-5 exit is unchanged in substance.

Verification path: `/kein:instructions --check` (the file is not covered by the standing-prompt paths, so this is a read-through, not a gate); `claude plugin validate plugin --strict`.

## Ordering

S1 depends on S2's diagnosis text, so S2 lands first. S3 and S4 are independent of both and of each other. S5 and S6 are prose the lead writes and can land beside any of them; they touch no file the code stories touch except `SKILL.md`, which no code story touches.

## Pre-mortem

- **The stop block fires where a lead legitimately has nothing to do.** Most likely at the very end, between `close` and the final report. Caught by: the lifecycle is no longer `active` once `close` or `halt` lands, so the block cannot reach the report; and the reason text names the off-switch.
- **The HEAD-clean park route hides a real partial write.** A file written but also committed would pass. Caught by: committing a task's partial work is itself outside what execute's loop does, and the park record names the diverging paths, so the receipt carries them.
- **The audit stopping rule ships a known defect.** That is the trade: pass 12's own finding was real. Caught by: registration is a record, not a silence, and the receipt's residual risk names every registered item.
