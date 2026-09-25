# Acting on the live open items

Status: Approved
Date: 2026-09-26

## Context

On 2026-09-26 the open-item files (`docs/open-threads.md`, `docs/skills/*/open.md`) were triaged. Closed and explanatory sections moved to `closed.md` / `docs/closed-threads.md` (ce2c3da), and stale references were fixed. About twenty-five live items remained, of mixed kinds: small fixes, owner decisions, measurements, Orca integration, and items already parked with their own reopen triggers. This document settles a disposition for every one of them and specifies the ones to be done now.

## Desired outcome

- `ralplan` no longer carries run history in the plan artifact or pastes the plan into lane packages.
- Both review skills treat a `REVISE` finding as accept-and-disposition, including a fix that needs no fresh lane.
- The owner can bound review cost with `--primed` and `--max-rounds`.
- An amended plan cannot leave a task accepted against a condition that no longer holds.
- A codex writer, whether Executor or Planner, can be resumed rather than respawned.
- The listed small defects in execute, eval and fsd are gone.
- A lead is reachable by mail from session start.
- `ocs` cannot silently run from a different harness tree than the session's.

## Scope

### In scope

- ralplan: the run account moves to state, lanes get the plan path, and the `Status` line is neutral during review.
- A fix-it route for `REVISE` in ralplan, plus `REVISE` wording in both review contracts.
- `--primed` and `--max-rounds <n>` on `ralplan` and `execute`.
- execute: acceptance bound to plan revision, and re-confirmation after `amend`.
- `ocs team` codex worker resume, replacing `--keep`, with worktree lifetime tied to task acceptance.
- `--planner codex` in `plan`, inherited by `ralplan`.
- Small fixes: execute state guards; eval harness commit and `visited_outside`; the four fsd items left by the 2026-09-23 run; a faster `check-execute-state`.
- Orca: a home Run per lead, and `ocs` refusing a mismatched plugin root.

### Out of scope

- A verdict tier weaker than `REVISE`.
- A `--quick` flag.
- `--round <n>` as a separate flag. It is folded into `--max-rounds`.
- Primed or fresh-lane review of a fix-it change.
- Any rule in ralplan about committing plan revisions before approval.
- Everything listed under Deferred items.

## Requirements

### R1. ralplan run account out of the artifact

- R1.1 While a plan is `Draft` or `In Review`, the `Status` line's reason is neutral. It names no round, verdict, revision, change summary or finding.
- R1.2 `Approved` keeps a one-line reason in the owner's preferred form, e.g. `Status: Approved — two-vendor consensus, 2026-09-26`.
- R1.3 The run history moves into ralplan state and the receipt: phase, round, findings, what an approval stands over, deferrals, and parked stories.
- R1.4 Lane packages give the plan's path instead of its text. The rules that required the pasted plan or the stripped `Status` line are removed or re-grounded:
  - `review-contract.md` package item and "The removed line is why"
  - `SKILL.md` step 5, "Each receives the complete current plan"
  - `plan-gate.md` "The reason half additionally carries…" and "The package a fresh lane receives is this artifact whole…"
  - `SKILL.md` step 6 "set Draft with a concrete reason" and step 7's `Status`-line explanation
- R1.5 `fsd/references/decision-policy.md` step 5, and the paragraph after it, put deferrals, parked stories and `Caught by` in the receipt or state instead of the `Status` line.
- R1.6 The validator (`STATUS_LINE_PATTERN`, `validate_plan_text`), fsd's input classifier, and `check-ralplan-state`'s `header()` accept the new `Status` shape.
- R1.7 The skill says nothing about lanes reading plan history through git.

### R2. `REVISE` fix-it route

- R2.1 In ralplan, a final blind round that ends in `PASS`/`REVISE` may be followed by fixing `REVISE` findings, and the plan is then approved with no fresh lane. The approval records both the reviewed hash and the post-fix hash. The lead reads the diff.
- R2.2 A `BLOCK` still requires a revision round (or `--primed`, R3).
- R2.3 In `execute` the fix-it route stays as it is. In both skills a fix-it change is checked by the lead reading the diff after the verification path re-runs.
- R2.4 Both review contracts word `REVISE` so it reads as "accept, and disposition each finding" rather than "revise and re-review". A `PASS` carrying findings stays refused.

### R3. Flags

- R3.1 `--primed` on `ralplan` and `execute`. After a `BLOCK` correction, the reviewer that raised the finding checks the fix and may approve. For a run with this flag, that inverts "a primed closure check cannot approve".
- R3.2 `--max-rounds <n>` on `ralplan` and `execute`: at most n official rounds. If a `BLOCK` is still open at the bound, the run stops, leaves the plan `Draft` (ralplan) or the task blocked (execute), and reports the open `BLOCK` findings. Nothing is approved by deferral.
- R3.3 Without `--max-rounds`, the five-round diagnostic trigger behaves as today.

### R4. Plan amendment and accepted tasks

- R4.1 Each task acceptance records the plan revision (input hash) it was made under.
- R4.2 After `amend`, one fresh lane per amendment receives the amendment and every task accepted under an earlier revision. For each task it judges whether the task still satisfies its completion condition under the amended plan.
- R4.3 A task judged no longer satisfying returns to correcting. The run cannot complete while any task accepted under a superseded revision is unconfirmed.

### R5. codex worker resume

- R5.1 `ocs team` records what is needed to resume the worker's session (session or rollout reference).
- R5.2 A correction round can resume that worker instead of starting a fresh one. The resumed invocation gets its own completion channel, so its report is read.
- R5.3 `--keep` is removed.
- R5.4 A `--worktree new` lane's tree stays until its task is accepted or abandoned, then closes.
- R5.5 Writers only. Review lanes stay fresh (`ocs ask --ephemeral`).
- R5.6 Whether `codex resume` restores the role layer, model, effort and sandbox, or they must be passed again, is measured and recorded with `/kein-findings:findings` before the route is built on.

### R6. `--planner codex`

- R6.1 `plan` takes `--planner codex`: a codex Planner writes the plan.
- R6.2 `ralplan` inherits the flag. It passes it to `plan` for the round-one draft, and revives the same codex Planner through R5 for each revision round.
- R6.3 `ralplan/references/lanes.md`'s refusal of `--planner <vendor>` is replaced by this.

### R7. Small fixes

- R7.1 execute state refuses an `observed_at` or `reviewed_at` later than the checkpoint's own clock read.
- R7.2 execute state normalises `reviewer_role` (`kein:critic` ≡ `critic`) before every role comparison, and refuses a role not in `plugin/agents.json`.
- R7.3 The eval default with-skill/without-skill pair records the harness commit in its manifest beside the plugin path.
- R7.4 eval writes `record["visited_outside"]` from `sessions_outside` against each replicate's permitted worktrees, including `--case` mode, so `check_plumbing` can fail.
- R7.5 The four fsd items from the 2026-09-23 run (`docs/skills/fsd/open.md`):
  - the mid-stage Stop block tells a waiting lead it may end the turn for the lane's notification;
  - `report` stops inviting an answer on a halted run;
  - whether `claude --resume` re-arms frontmatter hooks is measured and recorded;
  - `closeout.md` step 4's wording covers `halt`'s other refusals.
- R7.6 `check-execute-state` completes within two minutes, so a lane can run it in one tool call, with no loss of coverage.

### R8. Orca and environment

- R8.1 A lead has a home Run from session start, so mail sent to it is delivered and nudged before it has started any `ocs team` lane.
- R8.2 After `ocs team` starts a lane, the lead is again bound to its home Run. The lane's `worker_done` handling still works without relying on the lane Run staying bound.
- R8.3 `ocs` refuses to run, and says why, when more than one kein harness tree has `bin/ocs` on PATH. (Amended 2026-09-26: the Bash tool is not given `CLAUDE_PLUGIN_ROOT`, measured in a pinned `--plugin-dir` session, so that variable could never fire; PATH is where the mix is visible. Eval arms have operator plugin `bin/` directories stripped so they are not refused.)

## Constraints

- `agents/<role>.md` frontmatter is the role source; `plugin/agents/` and `plugin/agents.json` are renders (AGENTS.md).
- Standing prompts follow `plugin/prompts/standing-prompt.md`. A rule removed or changed carries its argument in the commit that changes it.
- The input-hash binding that stops a plan being swapped under a live ledger stays. R4 adds to it and does not loosen it.
- Unattended flows keep humans at the front and the end. No new mid-run human approval is introduced.

## Decision boundaries

- How the in-scope work is split into runs, and in what order, respecting dependencies: R5 before R6's revision rounds, and R1 together with its fsd counterpart R1.5.
- The exact neutral `Status` text, and the state and receipt fields that take over the run account.
- How ralplan state records the reviewed and post-fix hashes for a fix-it approval.
- The wording that makes `REVISE` read as accept-and-disposition.
- The re-confirmation lane's role and package.
- Where the home Run is created (SessionStart hook, first `ocs` call, or otherwise), decided after measuring when pane identity is available.
- How `check-execute-state` gets under two minutes: split, parallelise or trim duplicated setup.
- Whether resume must re-pass the role layer, model, effort or sandbox, per R5.6's measurement.

## Acceptance criteria

- [ ] A ralplan round-2+ lane package contains the plan path and no plan body. The plan file's `Status` line during review names no round, verdict, revision or finding. `check-ralplan-state` passes.
- [ ] An fsd run's approval records deferrals and parked stories in the receipt/state, not the `Status` line. `check-fsd-state` passes.
- [ ] A ralplan run ending `REVISE` can fix a finding and reach `Approved` without a new lane. The approval records both hashes. A `BLOCK` cannot reach `Approved` without a revision round unless `--primed` is set.
- [ ] `--primed` lets the raising reviewer approve a `BLOCK` correction. Without it, a primed check still cannot approve.
- [ ] `--max-rounds 1` with an open `BLOCK` stops with the plan `Draft` / task blocked and reports the open findings.
- [ ] After `amend`, an execute run with a task accepted under the earlier revision cannot complete until a re-confirmation lane has judged it. A task judged unsatisfied is back in correcting.
- [ ] An `ocs team` codex Executor can be resumed for a correction, and its report is read. `--keep` no longer exists. A `--worktree new` tree survives until its task is accepted.
- [ ] `plan --planner codex` produces a plan written by a codex Planner. `ralplan --planner codex` uses it for round one and resumes the same Planner for a revision.
- [ ] execute state refuses a future `reviewed_at` and a `reviewer_role` not in `plugin/agents.json`, and treats `kein:critic` and `critic` as one role.
- [ ] A default eval run's manifest names the harness commit. A replicate that opens a session outside its worktree fails `check_plumbing`.
- [ ] The four fsd items are closed in `docs/skills/fsd/open.md` with evidence. The `--resume` hook measurement is recorded in findings.
- [ ] `dev/kein-dev check-execute-state` finishes in under two minutes on this machine, with no section removed.
- [ ] A lead that has started no lane receives and is nudged for mail from another session. After starting an `ocs team` lane it still receives mail on its home Run.
- [ ] `ocs` refuses with a message when a second kein harness tree's `bin/ocs` is on PATH, and runs normally with one tree, however many times its `bin/` appears.

## Decisions and rationale

- **Every live item gets a disposition; only do-now items get requirements:** the backlog and the next work are settled in one place.
- **Neutral review `Status`, one-line approval reason:** blocks the history leak, keeps the owner's preferred approval line, and makes a pasted plan unnecessary. The owner ranks the paste's cost above the residual blindness gap.
- **git-visible plan history accepted and unmentioned:** whether plan revisions are committed before approval is the target project's commit convention.
- **No weaker verdict tier:** the "approve once fixed" tier the owner weighed is what `REVISE` already means. The confusion was the name, so the wording changes instead.
- **Lead reads the fix-it diff:** cheapest, and the final audit reads the whole change again.
- **`--quick` dropped:** telling a lane to review fast produced a sub-two-minute review that did not look read. Speed asked of a reviewer buys shallowness, not economy.
- **`--round` folded into `--max-rounds`:** the intent was "run only up to round n".
- **Stop unapproved at the bound:** approval is not manufactured from a round limit.
- **Revision binding with one re-confirmation lane per amendment:** conditions point into the plan, so no mechanism can tell which task an amendment touched. A fresh lane judges, and it runs once per amendment rather than once per task to bound cost (phase-47 saw four amendments in one run).
- **Worktree lives until task acceptance:** resume needs the tree. Closing at acceptance keeps a resumed correction possible without recreating trees.
- **`--planner codex` in `plan`, inherited by `ralplan`:** the round-one draft is already `plan`'s. Resume carries the Planner across revisions the way a native Planner is continued.
- **`ocs` refuses on a plugin-root mismatch:** a mixed-version session is silent and corrupts exactly the comparisons that pin a version.

## Relevant system evidence

- `plugin/skills/ralplan/references/plan-gate.md:19`: the reason half carries workflow phase and why approval is absent.
- `plugin/skills/ralplan/scripts/state.py:116`: `STATUS_LINE_PATTERN` requires `<state> — <non-empty reason>`.
- `docs/skills/ralplan/open.md` "Raised 2026-09-24": the e3-v4 lane read the plan file from disk and printed the `Status` line through `sed` and `git diff`. The round-6 package was 463 lines, mostly the plan.
- `plugin/skills/ralplan/references/review-contract.md:43` and `plugin/skills/execute/references/review-contract.md`: `PASS` carries no findings, and the state refuses a `PASS` over the lane's own finding.
- `plugin/skills/execute/SKILL.md` step 7: `REVISE` findings may be fixed before acceptance with the verification path re-run and no fresh lane.
- `docs/open-threads.md` "A plan correction ends the run": `amend --reason` (3841bc2) keeps every accepted task accepted, including one whose condition the amendment touched.
- `plugin/libexec/ocs-team`: launches the interactive `codex` TUI, so the session persists under the pinned `CODEX_HOME`. It records no session id.
- `plugin/skills/ralplan/references/lanes.md:21`: refuses `--planner <vendor>`.
- `dev/eval/run.py:1032`, `:412`: `visited_outside` is read but never written, and `sessions_outside` is unused.
- `dev/eval/run.py:720-722`: the default pair records a plugin path and no commit.
- `docs/skills/execute/open.md`: `reviewer_role` is spelled both `kein:critic` and `critic` on disk, and `check-execute-state` takes about 4.5 minutes.
- `docs/open-threads.md` "A lead that never started an `ocs team` lane cannot be nudged by mail": an unbound pane got no nudge in twelve minutes, and Orca 1.4.207 has no unbind, only `run-use`.
- `docs/open-threads.md` "A pinned `--plugin-dir` loses `ocs`…": measured 2026-08-20.

## Assumptions and risks

- `codex resume` may not restore the role layer or sandbox. R5.6 measures this before R5 and R6 rely on it. If resume proves unusable, R6's revision rounds fall back to a fresh codex Planner, which would need a new decision.
- A home Run created too early may bind before Orca's pane identity is stable. The creation point is measured first.
- Re-confirmation after amendment adds a lane per amendment. Frequent amendments make runs costlier; that cost is accepted.
- `--primed` weakens independence for the runs that set it. It is opt-in per run.
- Removing the pasted plan means lanes read the working file. A lane in the same worktree can still reach history through git, which is accepted.

## Deferred items

- **Measurement and review group:** plan's two never-separating graders and the `plan-no-unknown` re-run; a `--lead-prompt` eval; reading the 2026-09-19 research run against its memo's falsifying questions; the standing-prompt pass over ported skills; the seven old wiki notes; the tracer ranking scale. Gate: the owner schedules a measurement round. The tracer rule is fixed now: run tracer several times on one question; if rankings disagree, restore a defined strength scale with its conflict rule; otherwise leave the prompt.
- **The lead prompt reaching an Orca-launched interactive Claude worker.** Gate: porting the harness as a Codex plugin.
- **Per-directory `AGENTS.md` for subagents.** Gate: the owner raises it again.
- **Already parked, unchanged, with their own reopen triggers:** fsd accepted residual risk and "what would reopen the design"; execute's "a completion condition's own wording cannot be corrected inside a run"; plan's "what the ranking keeps catching".
- **`writer` / `designer` roles:** another session owns them.
