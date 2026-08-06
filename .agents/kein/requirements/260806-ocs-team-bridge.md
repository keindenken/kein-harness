# ocs team — the supervised write-capable lane bridge

Status: Approved
Date: 2026-08-06

## Context

`ocs ask` bridges kein's canonical roles to another vendor for read-only work. It runs `codex exec --ephemeral` as a one-shot with the role prompt prepended, pins the vanilla `CODEX_HOME`, resolves the model from the role's tier, and leaves a four-file trace under `ocs state-dir runs/ask`. It refuses write-capable roles on purpose, with the reason stated in the script: a remote vendor editing the worktree through a bare one-shot has no workflow around the write.

That leaves five of the fourteen canonical roles unreachable from any other vendor, `executor` among them. Both `execute/references/lanes.md` and `ralplan/references/lanes.md` currently refuse a vendor for their write-capable lane and record that it waits for this work.

Orca supplies the missing supervision — worktrees, a task and dispatch lifecycle, a durable completion signal, recovery verbs. A measurement session on 2026-08-06 compared the two ways to put a kein role into an Orca worker and found that Orca's own agent launch cannot set a per-lane model, reasoning effort, sandbox, or `CODEX_HOME`; those come from one global setting in the Orca client. The full record is at `~/Documents/wiki/_raw/note/260806-orca-worker-launch-paths-measured.md`.

## Desired outcome

A lead running `execute` can hand one task to a codex Executor, and that worker starts in the canonical worktree at the model its role's tier specifies, does the work under supervision, and returns a report the lead can read — with the same shape of invocation, gating, and trace that `ocs ask` already established for advisory lanes.

## Scope

### In scope

- `ocs team <provider> --agent <role> [--trace] [--model M] [--effort E] <task...>`, serving the five `workspace-write` canonical roles.
- Composition of an Orca terminal carrying kein's argv with an Orca dispatch attached to it, so Orca owns the lifecycle and kein owns the execution environment.
- A pre-flight failure when the target project is not trusted in the resolved `CODEX_HOME`.
- A mandatory worker report written to a file, and a trace of the invocation on disk.
- Wiring in `execute/references/lanes.md` so `--executor <vendor>` is served rather than refused.
- Amending `docs/purpose.md` order item 6 and the Orca non-goal, which currently read against any wrapper.

### Out of scope

- Reimplementing or replacing any part of Orca's orchestration runtime or command namespace.
- A `team` skill. The recorded decision that none exists still holds; `orca-cli` and `orchestration` remain the skills for free-form orchestration outside a kein workflow.
- Read-only lanes. They stay on `ocs ask`.
- A coordination verb that creates or waits on several workers in one invocation.
- Any change to `execute`'s state schema.

## Requirements

- One invocation launches one worker and blocks until that worker reports, then writes the worker's report location and summary to standard output and exits with a status reflecting the worker's outcome.
- Several lanes are obtained by invoking the command several times in the background. The command must be safe to background, which means every artifact a caller needs survives on disk without the caller waiting.
- The command serves exactly the canonical roles whose `sandbox_mode` is `workspace-write`, and refuses `read-only` roles by naming `ocs ask` as their path. Together with `ask`'s existing gate this covers all fourteen roles with no overlap and none unreachable.
- The assembled worker prompt is the canonical role prompt followed by the caller's task text, matching `ocs ask`'s contract. Repository instructions are not injected; the caller supplies them in the task, as with `ask`.
- The worker's model and reasoning effort are resolved from the role's tier in the canonical manifest, using the same mapping `ocs ask` already applies. `--model` and `--effort` override it.
- The worker runs against the pristine vendor home, not a tuned one.
- The worker's sandbox permits both writing in the worktree and reaching the Orca app.
- The worker must write its full report to a file and report that path on completion. The command surfaces that path to the caller.
- `--trace` records the assembled prompt, the exact launch argv, the worker's report, and any error, under the run state directory, following the layout `ocs ask` established.
- A worker that cannot start, cannot be attached, or fails to report is an explicit nonzero failure naming the stage that failed. It is never reported as a completed lane.
- Before creating any terminal, the command verifies that the target project has a trust record in the resolved vendor home. Without one it exits nonzero, creates nothing, and prints the exact remedy.
- `execute`'s lane reference gains the write-capable vendor path, and the recording convention already used for reviewer lanes extends to the Executor.

## Constraints

- Orca must own the Run, Task, Dispatch, completion signal, heartbeat, escalation, and recovery. Nothing in that lifecycle is reimplemented.
- The Orca orchestration feature must be enabled, and the Orca app running, for the command to work at all. Neither is something the command can arrange.
- The command must not write to the operator's vendor configuration home.
- No skill may share a name with an `ocs` subcommand, per `docs/purpose.md`.
- Work products and state belong under `<repo>/.agents/kein/`, resolved through `ocs state-dir`.
- Comments and prose break per sentence rather than at a column.

## Decision boundaries

- The tier-to-model-and-effort table is the one already present in `ocs ask`; it is not re-derived.
- Trace directory layout and file names follow the `runs/ask` precedent.
- How the command avoids the shared mailbox is an implementation choice. Orca's coordinator inbox is per-Run and returns the oldest delivery, so two concurrent waiters on one Run would contend; isolating each invocation in its own Run and polling the dispatch directly are both acceptable, and the visible consequence is only how lanes group in Orca's interface.
- How the worker's state root is pinned so its ledger lands in the run's tree rather than in whatever worktree it occupies.
- Exact flag spellings, help text, and error wording, provided the failure stages remain distinguishable.
- Whether the report file lives beside the trace or at a caller-supplied path.

## Acceptance criteria

- [ ] Invoking the command for a `workspace-write` role starts a worker, and the recorded launch argv contains the model and effort that role's tier resolves to.
- [ ] The worker's status line and the dispatch record agree that it ran at that model, with the vendor configuration default set to something different, so inheritance is ruled out.
- [ ] The worker's completion is received through Orca's own signal and the dispatch reaches a completed status.
- [ ] The worker's report file exists at the reported path and contains the worker's own account of the work.
- [ ] `--trace` leaves the assembled prompt, the launch argv, and the report on disk, and they are readable after the invoking process has exited.
- [ ] Two invocations backgrounded from one shell both complete and both leave complete traces, with neither consuming the other's completion.
- [ ] Invoking the command for a `read-only` role fails and names `ocs ask`.
- [ ] Invoking it against a project with no trust record in the resolved vendor home fails before any terminal is created, and the message names the missing record.
- [ ] A worker whose start is blocked produces a nonzero exit naming the stage, and no lane is reported as complete.
- [ ] The pristine vendor home is what the worker ran against, verifiable from the recorded launch environment.
- [ ] `execute` dispatching a vendor Executor records it with the vendor-qualified role, and its existing state validator accepts the result unchanged.
- [ ] `ocs check-prompts` and `ocs doctor` pass.

## Decisions and rationale

- **Compose an Orca terminal rather than use Orca's agent launch:** Orca's `worker-start --agent <id>` takes only an agent identifier, so model, effort, sandbox, and vendor home all come from one global client setting. Creating the terminal with kein's own argv and attaching the dispatch to it was measured working — the dispatch reported ready with the terminal reused, and completion arrived normally.
- **The wrapper exists for environment control, not prompt injection:** Orca's task specification accepts arbitrary text, so the role prompt reaches the worker either way. This corrects the reason the work was first proposed.
- **One worker per invocation, blocking:** `execute`'s task ledger is serial by contract, so no current workflow dispatches write-capable lanes in parallel. Concurrency is available by backgrounding the call, which is safe because the trace persists the result — the same argument already written into the lane references for advisory lanes.
- **Sandbox permits the app connection:** a worker reports by calling Orca from inside its own sandbox. Under a read-only sandbox and under a plain workspace-write sandbox that call failed with the app unreachable, while the binary itself ran; enabling network access for workspace-write let it through. This is why Orca's own agent launch bypasses the sandbox entirely, and the narrower setting is available to us.
- **Accept losing the vendor transcript hook:** a hand-created terminal gets no hook, so Orca's reader falls back to scraping terminal output, which in practice is interface frames interleaved with the text. A mandatory report file gives a better artifact than the hook would have, and the actual loss is tool-call-level detail rather than the result.
- **Fail on a missing trust record rather than create one:** writing the operator's configuration would silently edit a home the harness does not own and would make a security judgement on the user's behalf, against the operating rule that the harness writes nothing the user did not ask for. A per-invocation configuration override was considered and rejected as unmeasured.
- **Scope stops at `execute`:** a vendor Planner writes the canonical planning artifact, which activates the worktree-placement invariant and both artifact hashes at once. That deserves its own verification rather than riding along.
- **Keep the name `team`:** it is available because no skill claims it, and it parallels `ask` — one advisor asked, one teammate added.

## Relevant system evidence

- `plugin/libexec/ocs-ask`: pins the vanilla vendor home, gates to read-only roles with the reason stated inline, maps tier to model and reasoning effort, and writes a four-file trace under `runs/ask` when `--trace` is passed.
- `plugin/prompts/manifest.json`: carries `sandbox_mode` and `tier` per role. Nine roles are `read-only`; five are `workspace-write` — `executor`, `planner`, `code-simplifier`, `qa-tester`, `test-engineer`.
- `plugin/libexec/ocs-sync-prompts`: copies the canonical manifest verbatim, so `tier` and `sandbox_mode` are cross-vendor facts rather than Claude-side additions.
- `plugin/skills/execute/SKILL.md`: the task ledger is serial, and no second write-capable task may run elsewhere as a deadline workaround.
- `plugin/skills/execute/references/lanes.md` and `plugin/skills/ralplan/references/lanes.md`: both refuse a vendor for their write-capable lane and name this work as the gate.
- `plugin/skills/execute/scripts/state.py`: review verdicts are a list and `reviewer_role` is free text, so a vendor-qualified role needs no schema change.
- `docs/purpose.md`: order item 6 and the Orca non-goal both currently read against a wrapper of any kind.
- `~/Documents/wiki/_raw/note/260806-orca-worker-launch-paths-measured.md`: the measurement record behind the launch-path, sandbox, and transcript decisions.

## Assumptions and risks

- Assumes Orca's dispatch attachment to a hand-created terminal remains supported. It was measured on the current build and is documented as the path for custom argv, but it is a lower-level surface than the agent launch and could change.
- Assumes the vendor's sandbox continues to permit the app connection under the chosen setting. This is a vendor behavior, not an Orca contract, and a future sandbox change could break reporting without breaking anything else.
- The pristine vendor home carries whatever tool servers the operator has configured there, which a one-shot advisory call does not pick up but a supervised session does. Whether that matters is unresolved and can be settled by the operator disabling them on that side.
- A blocking invocation ties the lead's turn to the worker's duration, which for an implementation task can be long. The mitigation is backgrounding, which shifts the waiting to the caller.
- The vendor's own instruction files are loaded by the worker in a way a one-shot call does not replicate, so a supervised lane may behave differently from an advisory one for reasons unrelated to the role prompt.

## Deferred items

- **A vendor Planner** through `ralplan --planner <vendor>`. The refusal in `ralplan/references/lanes.md` stays until then. Gate: a round that verifies the canonical artifact path, the worktree placement requirement, and both plan hashes against a remote writer.
- **Asynchronous start and wait handles.** One invocation stays one worker, blocking. Gate: a workflow that genuinely needs write-capable lanes in parallel; `execute`'s serial ledger means none exists today.
- **Reviewer lanes through this command.** Read-only roles stay on `ocs ask`, which is cheaper and structurally fresh. Gate: a reviewer needing tools or duration a one-shot cannot provide.
