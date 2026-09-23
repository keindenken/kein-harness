# One continuous unattended flow — `/kein:fsd`

Status: Approved
Date: 2026-09-19

## Context

The harness already has the stages of a delivery: `interview` for requirements, `ralplan` for a consensus-reviewed plan, and `execute` for implementation through final audit. The user invokes them one after another and hands artifacts between them by hand.

oh-my-claudecode 5.x `launch` chains the same stages into one run, but it places a human sign-off at five checkpoints. The user runs `execute` for hours without watching it, so a flow that waits on them mid-run stalls until they return. They trust an agent consensus gate over their own approval, and want their input at the front and at the end only.

## Desired outcome

After one human session at the front, a flow carries work from idea to audited change without asking the user anything. Every judgement it could not make safely on its own arrives in one final report: the assumptions it took, the questions it parked, and the lessons it proposes.

## Scope

### In scope

- A new skill, `/kein:fsd`, that routes by input and chains `interview`, `ralplan`, `execute`, and a closeout.
- A mid-run decision policy split by reversibility, applied both in execution and when `ralplan` does not converge.
- Per-task parking in `execute`, so a decision parks only the tasks that depend on it.
- Closeout: stale project documents fixed, a retrospective written, lessons for AGENTS.md proposed.
- Aligning `execute`'s prose with its disjoint-scope parallelism.

### Out of scope

- launch's human checkpoints C1–C5.
- drydock surfaces (`docs/standards/`, `docs/business/`, `design-system/`) as closeout destinations.
- Pushing, deploying, or opening pull requests.

## Requirements

- Entry routes by input: an idea starts at `interview`, an approved requirements document at `ralplan`, an approved plan at `execute`. A stage already done is not repeated.
- The interview's consolidated approval is the only human sign-off. After it, the flow does not ask the user anything until the final report.
- A reversible decision is taken on the recommended option and recorded as an assumption, with what reversing it would cost.
- An irreversible or expensive decision (schema, public API, data deletion, an externally visible action) parks only the tasks that depend on it; the others continue to acceptance.
- When `ralplan` reaches its diagnostic trigger without approval, the remaining blocking grounds are split by the same test: reversible ones become assumptions with recorded deferrals and the plan is approved; irreversible ones park the tasks that depend on them and the rest proceed to `execute`.
- Execution uses `execute`'s existing parallelism for tasks with disjoint scopes.
- Project documents the change made stale are fixed as `execute` tasks, so the final audit covers them.
- A retrospective is written to a file under `ocs state-dir`.
- Lessons for AGENTS.md are not applied; the final report lists them, each line vetoable, the report-then-approve shape of `/kein:instructions --check`.
- The final report lists assumptions, parked questions, lesson proposals, and the retrospective's path. An empty list is stated as empty.
- Re-invoking `fsd` after the user answers parked questions resumes the parked tasks without redoing accepted ones.
- `fsd` is invoked by slash command only (`disable-model-invocation: true`).
- `execute`'s `SKILL.md` ("Then advance serially") and `docs/skills/execute/open.md` stop describing the ledger as serial where scopes are disjoint.

## Constraints

- `ralplan` remains the plan gate; no human approval replaces an agent gate.
- Code closeout stays `execute`'s finalization.
- AGENTS.md is not modified during the flow.
- Prompt prose names no model; tiers come from `agents.json`.
- Run state lives under `ocs state-dir`.
- Any hook that enforces stage transitions allows by default and blocks only on positive evidence of a gap between stages (one stage's receipt complete, the next stage's run not started). Quiescence inside a running stage is never judged, so a stage waiting on its own lanes is never blocked. (Superseded 2026-09-23 by `.agents/kein/plans/260923-fsd-run-fixes.md` S1, after the first live run lost about eight hours to a lead that ended its turn waiting on a lane that had silently stopped: the Stop hook now blocks once when a run is active and no gap exists, excepting the interview stage, and tells a waiting lead to check its lane is alive.)
- A Stop hook never blocks twice in a row: when its input's `stop_hook_active` is true, it allows. One nudge catches a turn that announced an action without taking it; a legitimate wait costs one extra turn, not a loop.
- A block's reason names an action whose single invocation clears the condition (invoking the next stage's skill, whose entry records its run). A condition the model cannot satisfy immediately is not used to block. (Superseded for the mid-stage block by the same S1: its reason names a demand and two exits rather than one action, and says which of its commands to run and when.)
- A PreToolUse gate denies only writing tools, never the Skill tool, reads, or agent dispatch.
- The hooks carry an off-switch of their own.
- Hooks declared in `fsd`'s frontmatter do not survive a new process (`claude -c`, `--resume`, an app restart), so resuming a run means invoking `/kein:fsd` again, which re-arms them.

## Decision boundaries

- How stages are chained: one session, subagents, or a Workflow script under `plugin/workflows/`.
- Where and in what format assumptions and parked questions are recorded.
- The retrospective's exact location under `ocs state-dir` and its shape.
- The concrete list that decides reversibility, within the examples above.
- The shape of per-task parking in `execute`'s state machine.
- Whether a notification is sent when the flow ends.

## Acceptance criteria

- [ ] Given an idea, a requirements document, or a plan, `fsd` starts at `interview`, `ralplan`, or `execute` respectively and does not repeat an earlier stage.
- [ ] After the interview's approval, the run asks the user nothing until its final report.
- [ ] With one irreversible decision arising in one task, tasks independent of it reach acceptance and the dependent task is parked.
- [ ] A reversible decision appears in the final report as an assumption with its reversal cost, and the work built on it is present.
- [ ] A `ralplan` round sequence that reaches the diagnostic trigger continues to `execute` with its reversible grounds recorded as assumptions, rather than stopping.
- [ ] The final report contains assumptions, parked questions, lesson proposals, and the retrospective path, each stated as empty when empty.
- [ ] Re-invoking after answering parked questions resumes only the parked tasks; accepted tasks are not redone.
- [ ] AGENTS.md is byte-identical before and after a run.
- [ ] A stale-document fix made by the run is covered by `execute`'s final audit.
- [ ] `kein:fsd` does not appear in the model-visible skill list, and `/kein:fsd` loads.
- [ ] `claude plugin validate plugin --strict` passes.

## Decisions and rationale

- **Human input only at the front and the end:** runs last hours unattended; any mid-run wait stalls until the user returns.
- **Agent gates stay, human checkpoints do not come in:** the user trusts `ralplan`'s consensus over their own sign-off, which is the opposite of launch's choice to replace agent plan review with human signatures.
- **Split by reversibility:** always assuming lets an agent make irreversible choices alone; always parking can leave the core task stopped for hours. The split takes launch's own boundary test, whether the system can detect and undo a wrong choice, and applies it to decisions.
- **The same split for `ralplan` non-convergence:** its roughly-five-round trigger asks someone to reassess, and nobody is there. `ralplan` already admits a blocking ground with a recorded deferral, so the reversible part needs no new mechanism.
- **Entry by input:** avoids redoing stages the user already ran, the way launch routes a supplied spec past its first phase.
- **Stale documents fixed inside `execute`:** fixing them after the final audit would change an audited tree.
- **Lessons proposed, not applied:** a rule chosen by an agent would enter every later session unreviewed; the user reads `deliberate` and `/kein:instructions --check` the same way, report first and fix on approval.
- **Slash-only:** a multi-hour unattended flow should not start from a model's reading of a request.
- **Hooks allow by default and block once:** omc's persistent-mode Stop hook blocks by default and exempts only the waits it can detect (`hasPendingOwnedAsyncWork`, over its own HUD state with a freshness TTL), so an untracked wait loops "still waiting → block" until a 20- or 30-reinforcement circuit breaker releases it; the user has hit that loop. Blocking only on stage-gap evidence, and never twice in a row, removes the need for an exemption list and a breaker.
- **Named `fsd`:** the user's choice, after Tesla's Full Self-Driving, in the spirit of omc's `autopilot`, and it shares no name with an omc skill.

## Relevant system evidence

- `plugin/skills/execute/scripts/state.py` (commit 2da9b80, 2026-09-12): tasks whose scopes do not meet may be write-active at once, each bound to its own scope fingerprint; `task-ledger-template.md` says the same, while `SKILL.md` Task Loop step 7 still says "Then advance serially".
- `plugin/skills/execute/SKILL.md`: `blocked` stops the run; "It does not invoke RALPLAN."
- `plugin/skills/ralplan/SKILL.md`: about five unsuccessful rounds is a re-arming diagnostic trigger, not a maximum; a `BLOCK` reaches approval only with a deferral recorded against its ground.
- `docs/artifacts/ledgers/260903-p48-run-state/README.md`: kein's phase-48 ralplan closed in 18 rounds.
- `plugin/workflows/`: empty except `.gitkeep`.
- `README.md` "Sharing names with omc": delegation prose is not namespaced, so shared names are ambiguous while both plugins are enabled.
- Probe on 2026-09-19 (throwaway plugin with a skill declaring PreToolUse on `Write` and a Stop hook in frontmatter, headless sessions): the hooks did not fire before the skill was invoked; after invocation they fired on later turns of the same process and after a `/compact`; they did not fire in a `claude -c` continuation in a new process. The Stop hook saw `stop_hook_active` false on the first stop and true on the stop after its block, and allowing on true ended the sequence after one nudge.
- oh-my-claudecode v5.4.0 `skills/launch/SKILL.md`: C4 parks a ticket before decision-dependent mutation and lets other frontier tickets continue; C5 reports Open Assumptions and a per-line vetoable sediment list.

## Assumptions and risks

- Reversibility is judged by the agent; a wrong call either parks work needlessly or builds on a choice that is costly to undo. The examples bound it but do not remove the judgement.
- Chaining multi-hour stages may exceed one context window; the chaining choice is left to the implementer and relies on the stages' existing on-disk state for resumption.
- Approving a `ralplan` plan with reversible grounds deferred trades plan soundness for progress, which the user accepted for unattended runs.

## Deferred items

- Whether `fsd` notifies the user when it ends: an implementation decision within the boundaries above.
