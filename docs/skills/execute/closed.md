# `execute`: what has closed

Items moved out of `docs/skills/execute/open.md` once closed, kept verbatim with a note on what closed them.

## A dispatched worker sometimes invokes `/kein:execute` itself

Closed 2026-09-26: `plugin/hooks/spawn-guard.py`, a PreToolUse hook, refuses a subagent's `Agent`/`Task` call for any type but a lookup role, its `Skill` call for the kein skills that dispatch workers, `Workflow`, and `ocs team`/`ocs ask`; the lead prompt's prose rule was removed with it. `disallowedTools: Skill` in role frontmatter was not used because it blocks every skill, including the reference skills roles such as `designer` load, and does not reach built-in subagent types. Left uncovered, by design or by reach: `SendMessage` to a worker that already exists (also how siblings coordinate), anything a worker on another vendor does, since no Claude hook runs there; and a worker starting an agent through another CLI (`claude -p`, `codex exec`, `orca`), which nothing in a worker's context suggests and which a measurement probe legitimately runs. A kein skill is refused unless `spawn-guard.py` lists it as non-dispatching, and `kein-dev bump-version` refuses to release while a skill sits in neither list.

Seen rarely, reported by the owner 2026-09-26: a subagent `execute` spawned — `executor` or another lane — called the `execute` skill on its own task and started putting its own work through review. The lead prompt's "workers do not spawn writers" says in its own words that nothing in the harness enforces it; the brief is the only place it exists, and a worker's skill listing still shows `kein:execute`, whose description ("a bounded code change … carried through implementation, verification, independent review") matches the task the worker was just handed.

No trace of an occurrence has been archived, so neither the frequency nor what in the brief preceded it is known. Candidates to weigh with `/kein:deliberate` once one is captured: a line in `execute`'s worker brief, a role-level refusal in `agents/*.md`, or a mechanism — a `PreToolUse` hook on `Skill` that refuses `kein:execute` (and the other orchestrating skills) outside the lead session. The hook is the only one that does not rely on the worker reading a sentence, which is the failure being described.

## One worktree admits one run, and that was never a bar to parallelism

Closed 2026-09-26: recorded as an explanatory record rather than open work — the section's own last line already says nothing here needs changing.

The sentence this section was written about is gone from `SKILL.md`, and so is the last prose that described the ledger as serial: 2da9b80 made disjoint scopes concurrent, and the 2026-09-23 run removed "Then advance serially." along with it. What the prose used to say badly, the mechanism says exactly, and the mechanism is what remains.

The rule that survives is about runs, not tasks: taking tasks out of *one* run's ledger and scattering them across worktrees is what nothing supports. N briefs producing N runs in N worktrees was always the shape it permitted.

The prose is one half of a mechanism. `scripts/state.py` takes an exclusive `flock` on `<tmp>/kein-execute-<uid>/<sha256 of the canonical worktree>.lock`, and `canonical_worktree()` computes that key from `git rev-parse --show-toplevel` — the worktree's own root. It also computes `--git-common-dir` and does **not** use it for the lock. So two worktrees of one repository take two different locks and their runs do not exclude each other.

That is the deliberate opposite of how Codex resolves project trust, which does follow the common dir and so makes a linked worktree inherit the main one. Two path-derived keys in the same neighbourhood, resolved on purpose to different things.

`worktree_fingerprint()` is the other half: HEAD plus staged, unstaged and untracked content, so a run notices the tree moving underneath it. Splitting lanes across worktrees makes that check stronger rather than weaker, because nothing else is writing in the tree it fingerprints.

**Nothing here needs changing.** It is recorded because the rule was read the wrong way round during the worktree work of 2026-08-19 and stated as a blocker, and because the next reader will parse the sentence the same way.

## Its reason is not in this repository

Closed 2026-09-26: recorded as an explanatory record rather than open work — it explains why the lock is named as it is and finds nothing to change here.

`04206fa` ported the loop wholesale from the Codex side on 2026-08-04, and the lock predates that: it arrived named `codex-orca-execute-<uid>` and was renamed to `kein-execute-<uid>` on both sides at once, because a rename on one side only "would silently break exclusion between the two vendors."

So the invariant the lock actually protects is **cross-vendor**: a Claude `execute` run and a Codex `execute` run must not both hold the same worktree. That is why it is a harness invariant rather than a Codex detail, and why the name is load-bearing in a way no test asserts.

If the rule is ever revisited, the argument for it is on the Codex side, from before this repository existed. Nothing here ever recorded why the ledger had to be serial *within* a run, as opposed to why a worktree admits only one run -- which is why the serial reading went, and the per-worktree one stayed.

## Left open by the 2026-09-23 run

Closed 2026-09-26: the future-time guard and `reviewer_role` normalisation by 4a41c57 (R7.1, R7.2); `check-execute-state`'s runtime by 1297143 (283 s to about 46 s).

Carried in that run's receipt; the run record is `260923-audit-stopping-rule.md`.

- **No guard against a future time.** `observed_at` and `reviewed_at` accept any timezone-aware value, and that run's ledger carries invented future stamps because nothing refused them. Reopen when adding the guard: refuse a time later than the checkpoint's own clock read.
- **`reviewer_role` is matched as an exact string.** The final-audit coherence rule, and acceptance's before it, compares roles verbatim, and runs on disk already spell them both `kein:critic` and `critic`. A PASS under the other spelling passes silently over its own role's carried findings — the relabel the rule exists to stop. Normalise the role before comparing, or validate it against `plugin/agents.json`.
- **`check-execute-state` outlasts a tool call.** At about four and a half minutes it cannot finish inside one call, so a lane briefed to run it backgrounds it and returns early. Either the suite gets faster or briefs keep naming its runtime and leaving the full run to the lead.


## A codex worker could be resumed rather than respawned — raised 2026-09-24

Closed 2026-09-26: eeda04d (R5) — `ocs team codex --resume <run-dir>` continues the worker a previous invocation ran, in its session and its tree, with a completion channel of its own; `--keep` is removed and a `--worktree new` tree now stays until its task is accepted or abandoned.

For a native worker the lead already chooses: continue the subagent that did the investigation, or dispatch a fresh one, and step 5 names that choice for a correction ("choose the original or a fresh Executor"). A codex worker from `ocs team` gets no choice: the invocation ends, the terminal is closed, and a correction to its own work is a new worker that has to re-learn the tree.

The owner's point is that it need not be. `ocs team` launches the interactive `codex` TUI (the `launch=` line in `plugin/libexec/ocs-team`), not `codex exec --ephemeral` as `ocs ask` does, so the session is written under the pinned `CODEX_HOME` like any other — the owner has confirmed it survives — and `codex resume` can reach it. So the lead could get the same continue-or-fresh choice for a codex Executor.

What it would take, found by reading and not tried:

- **Nothing records the session id.** `ocs team` writes `spec.txt` and `command.txt` to its run directory, but no session or rollout reference, so there is nothing to resume by. Capturing it is the first piece.
- **`--keep` is not the answer, and resume should replace it.** It leaves the worker terminal open after completion, but nothing ever closes it afterwards, and in practice the lead rarely sends a kept worker anything. Closing on completion and reopening with `codex resume` only when a follow-up is actually wanted is cheaper and leaves nothing standing — the owner's call is that this beats `--keep` outright.
- **Completion is per invocation.** Each `ocs team` call creates one Orca run and task and reads completion from that dispatch and its report file. A resumed session needs a new task to report into, or it finishes with nobody reading it.
- **The worktree has to outlive the first invocation.** A `--worktree new` lane's tree is removed by `ocs team close`, and a resume into a removed tree is meaningless.
- **Only for writers.** Review lanes stay fresh by construction, and `ocs ask`'s `--ephemeral` is what gives them that; this is about `ocs team`'s Executor.
- **Still unverified:** that `codex resume` on a session started with `developer_instructions`, a pinned `CODEX_HOME` and the per-launch `-c` overrides comes back with the same role layer, model, effort and sandbox, or whether those have to be passed again. Measure before building on it, and record the answer with `/kein-findings:findings`.
