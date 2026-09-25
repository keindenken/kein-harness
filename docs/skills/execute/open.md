# `execute`: what is still open

## A completion condition's own wording cannot be corrected inside a run

`state.py` refuses any change to an existing task's `scope` or `completion_condition`, and `amend` moves only the plan. So when measurement falsifies the literal words a condition was ledgered with, the only exit is `blocked`, then abort and a new run. oh-my-claudecode 5.x gave ralph the opposite route: a criterion is replaced or superseded, the original kept verbatim with reason, evidence, authority and time, and every completion claim and approval bound to the criteria revision it was made under.

Deliberated on 2026-09-18 and not added. Every falsified ruling in the archived runs (`docs/artifacts/ledgers/260829-p47-run-state`, `260903-p48-run-state`: eight execute runs) was a plan clause, and the conditions defer to the plan ("DR47-6 lands", "the plan's §4 … text governs"), so `amend` carries the correction. The freeze is also what stops a lead fitting the condition to what got built; omc needed more than a dozen hardening commits to make its route safe.

**Reopen when** a run shows a condition written as literal values rather than a pointer — S48-1a's "20→8 / 80→16 clamped" is the shape — whose wording measurement refutes, and a lane's `blocks` cites that wording so the task cannot accept after the plan is amended.

The neighbouring question is in `docs/open-threads.md`, "A plan correction ends the run": whether an amendment that touches the condition an already accepted task passed under should unseat that acceptance. `amend` now keeps the run, so the acceptance stands; omc's revision binding is one answer to that thread, not to this one.

## Left open by the 2026-09-23 run

Carried in that run's receipt; the run record is `260923-audit-stopping-rule.md`.

- **No guard against a future time.** `observed_at` and `reviewed_at` accept any timezone-aware value, and that run's ledger carries invented future stamps because nothing refused them. Reopen when adding the guard: refuse a time later than the checkpoint's own clock read.
- **`reviewer_role` is matched as an exact string.** The final-audit coherence rule, and acceptance's before it, compares roles verbatim, and runs on disk already spell them both `kein:critic` and `critic`. A PASS under the other spelling passes silently over its own role's carried findings — the relabel the rule exists to stop. Normalise the role before comparing, or validate it against `plugin/agents.json`.
- **`check-execute-state` outlasts a tool call.** At about four and a half minutes it cannot finish inside one call, so a lane briefed to run it backgrounds it and returns early. Either the suite gets faster or briefs keep naming its runtime and leaving the full run to the lead.


## A codex worker could be resumed rather than respawned — raised 2026-09-24

For a native worker the lead already chooses: continue the subagent that did the investigation, or dispatch a fresh one, and step 5 names that choice for a correction ("choose the original or a fresh Executor"). A codex worker from `ocs team` gets no choice: the invocation ends, the terminal is closed, and a correction to its own work is a new worker that has to re-learn the tree.

The owner's point is that it need not be. `ocs team` launches the interactive `codex` TUI (the `launch=` line in `plugin/libexec/ocs-team`), not `codex exec --ephemeral` as `ocs ask` does, so the session is written under the pinned `CODEX_HOME` like any other — the owner has confirmed it survives — and `codex resume` can reach it. So the lead could get the same continue-or-fresh choice for a codex Executor.

What it would take, found by reading and not tried:

- **Nothing records the session id.** `ocs team` writes `spec.txt` and `command.txt` to its run directory, but no session or rollout reference, so there is nothing to resume by. Capturing it is the first piece.
- **`--keep` is not the answer, and resume should replace it.** It leaves the worker terminal open after completion, but nothing ever closes it afterwards, and in practice the lead rarely sends a kept worker anything. Closing on completion and reopening with `codex resume` only when a follow-up is actually wanted is cheaper and leaves nothing standing — the owner's call is that this beats `--keep` outright.
- **Completion is per invocation.** Each `ocs team` call creates one Orca run and task and reads completion from that dispatch and its report file. A resumed session needs a new task to report into, or it finishes with nobody reading it.
- **The worktree has to outlive the first invocation.** A `--worktree new` lane's tree is removed by `ocs team close`, and a resume into a removed tree is meaningless.
- **Only for writers.** Review lanes stay fresh by construction, and `ocs ask`'s `--ephemeral` is what gives them that; this is about `ocs team`'s Executor.
- **Still unverified:** that `codex resume` on a session started with `developer_instructions`, a pinned `CODEX_HOME` and the per-launch `-c` overrides comes back with the same role layer, model, effort and sandbox, or whether those have to be passed again. Measure before building on it, and record the answer with `/kein-findings:findings`.
