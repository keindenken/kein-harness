# `/kein:fsd` — one unattended flow from idea to audited change

Status: Approved — round 2 fresh Architect and Critic both returned REVISE with no blocking ground at this review hash. The approval stands over nine carried REVISE findings recorded in the ralplan receipt (guard's root-scope reading, sealing the dispatch fingerprint before dispatch, HEAD in the restored-scope comparison, associating resumed stage runs, post-skill name forms, close/resume precedence with open questions, retrospective location vs execute's fingerprint); execution must settle each. Gate G1 remains a bounded Evidence Gate inside U4.

## Source and scope

Requirements: `.agents/kein/requirements/260918-unattended-flow.md` (Approved, sha256 `87238768…4600`). That document governs. This plan settles only what it leaves as decision boundaries: how stages are chained, where assumptions and parked questions are recorded, where the retrospective goes and what it looks like, the concrete reversibility list, the shape of per-task parking in `execute`, and whether a notification is sent.

Classification: a feature. It adds one skill and its state machine and hooks, extends `execute`'s state machine, and makes two prose corrections.

Non-goals, taken from the requirements or following directly from them: launch's human checkpoints, drydock surfaces, push/deploy/PR, any change to `ralplan`'s or `interview`'s state machines, any edit to AGENTS.md by the flow, and a version bump. `plugin/workflows/` stays empty.

Throughout, "requirements" means that document, "verified" means read in the repository at this commit, and "inferred" marks a planning inference.

## Repository facts this plan stands on

- `plugin/skills/execute/scripts/state.py`: `TASK_STATUSES` = pending, implementing, verifying, reviewing, correcting, accepted. `WRITE_ACTIVE_STATUSES` excludes pending and accepted. `_scope_collisions` treats write-active tasks and *earlier pending* tasks as occupying their scope. `validate_transition` refuses any change to an existing task's `scope`/`completion_condition`, and it refuses completion unless every task is `accepted`. `PHASE_TRANSITIONS` lets `blocked` go back to `task`. The `task → simplifying/final_audit` transitions do not check task statuses; only completion does. `_autofill` recomputes `scope_fingerprint` for every task that was not accepted at the previous checkpoint. The completed receipt projects every task as an accepted summary. (verified)
- `execute`'s transitions are mostly checkpoints the lead writes by hand. Only `start` and `amend` are built by a command. `amend` is the existing way an owner ruling lands in the plan while a run is live. (verified: `references/state-schema.md`, `task-ledger-template.md`)
- `plugin/skills/execute/SKILL.md` Task Loop step 7 ends "Then advance serially." `docs/skills/execute/open.md` §1 quotes a "serial ledger" sentence that is no longer in `SKILL.md` and ends "Nothing here records why the ledger has to be serial *within* a run". Commit 2da9b80 made disjoint scopes concurrent. Its message also records a rule the project chose: the sentences that read as a prohibition go "rather than reworded", because "a neutral mention still primes". (verified)
- `ralplan` approval: `approve --findings` accepts a finding that names a blocking ground only when it carries `deferral: {reason, caught_by}`. It approves only from an official `reviewing` round at an unchanged review hash, and the receipt keeps the findings. The lead may edit the `Status` line without moving the review hash. `SKILL.md` puts the diagnostic trigger at around five unsuccessful rounds and says a deferred ground's `Caught by` "belongs in the plan's pre-mortem before the approval". (verified: `plugin/skills/ralplan/scripts/state.py` `approve`, `_validate_deferral`, `references/plan-gate.md`)
- `interview` ends by writing the requirements and collapsing its ledger to `status: completed` with `requirements_path`. Its ledger is at `ocs state-dir runs/interview/<run_id>/ledger.md`. (verified: `references/ledger-template.md`)
- `ocs state <workflow>` runs `plugin/skills/<workflow>/scripts/state.py`. `ocs validate <workflow>` runs `scripts/validate_artifacts.py`. So a new `plugin/skills/fsd/scripts/state.py` answers to `ocs state fsd` without any new libexec file. (verified: `plugin/libexec/ocs-state`)
- Hooks: `plugin/hooks/hooks.json` declares a UserPromptSubmit hook (`hud/repair.sh`) and a PreToolUse Bash hook (`hooks/git-guard.py`), and both commands use `${CLAUDE_PLUGIN_ROOT}`. The off-switch convention is a marker file under `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/kein/<feature>/`, and the hook exits 0 silently when the marker says so (`hud/repair.sh`). `dev/libexec/check-git-guard` tests a hook by piping synthetic hook JSON into it. (verified)
- Slash-only skills use `disable-model-invocation: true` (`onboard`, `ping`, `handoff`). Commit 8d88f63 verified this with a fresh headless session, which listed every kein skill except the disabled ones. (verified)
- `dev/kein-dev <name>` runs any executable in `dev/libexec/`, and its `#:` line is the help summary. (verified)
- Workflow scripts (the Workflow tool's documented contract): they have no filesystem access, cannot call `Date.now()`, spawn subagents whose final text is the return value, and give no channel to the user. Whether a Workflow agent can invoke a skill, or dispatch further agents, is not documented. (documented / not established)

## Decision 1 — how the stages are chained

Drivers, in order: (1) the hook constraints in the requirements, which assume one armed session ("resuming a run means invoking `/kein:fsd` again, which re-arms them"); (2) `interview` needs the user and the rest of the flow must never ask the user; (3) `ralplan` and `execute` are lead-owned loops that dispatch fresh subagents, so whatever runs them must be able to dispatch.

| Option | Benefit | Cost | Verdict |
| :-- | :-- | :-- | :-- |
| **A. One session.** `/kein:fsd` invokes `kein:interview`, `kein:ralplan`, and `kein:execute` in turn with the Skill tool, then runs the closeout itself. Hooks in `fsd`'s frontmatter hold the transitions. | Each stage runs as it already does, as the lead that dispatches subagents. The interview happens in the user's own session. The hooks behave as the 2026-09-19 probe measured: armed by invocation, surviving later turns and `/compact`. Resume is re-invocation, which is what the requirements already describe. | A multi-hour run relies on auto-compaction. Three hook facts are unmeasured (Gate G1). | **Chosen.** |
| B. A Workflow script in `plugin/workflows/` | Deterministic control flow. | The script cannot read state files. `ralplan` and `execute` would have to run inside a Workflow agent, and it is not established that such an agent can invoke a skill or dispatch the fresh reviewers those loops require. It cannot hold the interview. The Workflow tool is opt-in per session and not reachable from Codex. | Rejected: its two load-bearing capabilities are unestablished, and the interview cannot run in it even if both turn out to exist. |
| C. Headless `claude -p` stages driven by an `ocs fsd` subcommand | A fresh context per stage, so no compaction risk. | `ocs` serves both vendors and would be tied to the `claude` binary. An unattended child needs writes pre-authorised: either every run gets `--dangerously-skip-permissions`, which the requirements do not authorise, or a permission prompt stalls with nobody there to answer it. The interview still has to run in the user's session, so the flow splits across processes. The driver outlives the Bash tool's 10-minute timeout, so it has to run in the background, where its failures are silent. The frontmatter-hook constraints would govern nothing. | Rejected: its one advantage, context size, is already covered by compaction plus every stage's on-disk `reconcile`. Its costs are a permission escalation and a second process nobody watches. |

Consequence: the context-window risk the requirements name is accepted and mitigated in U5. After any compaction the lead runs `ocs state fsd status` and the current stage's own `reconcile`, which is the precedent `ralplan` and `execute` already set.

## Decision 2 — the shape of per-task parking in `execute`

Drivers: (1) independent tasks reach acceptance while a parked one waits; (2) a later invocation resumes only parked tasks and never redoes an accepted one; (3) nothing parked, and nothing half-built, gets inside an audited or completed tree; (4) change as little of the existing invariants as possible, especially "Completion requires every task accepted" and the receipt shape.

| Option | Benefit | Cost | Verdict |
| :-- | :-- | :-- | :-- |
| **P1. A `parked` task status inside one nonterminal run, holding no writes.** Independent tasks go on to acceptance. Once nothing can be dispatched, the run checkpoints the existing `blocked` lifecycle, and its `next_action` names the parked questions. Resuming reconciles the same run and unparks the tasks. Finalization and completion wait until nothing is parked. | Completion, the receipt, and the final audit stay exactly as they are. Accepted tasks keep their sealed fingerprints, so resume cannot redo them. A parked task's scope is at its pre-dispatch content, so independent tasks' verification never reads half-built work. | While paused, the run holds the worktree claim. When anything parks, the unattended run ends with accepted but unaudited work. The final report says so. Parking a task already under way costs its partial work. | **Chosen.** |
| P2. The run completes with parked tasks excluded. The receipt gains `parked_tasks`, and resume starts a new run from them. | Delivers an audited change at the pause and frees the worktree. | It changes the completion invariant and the receipt. It needs a link from one run to the next. | Rejected: it weakens two invariants to deliver a partial audit early. P1 gets the same guarantee against half-built work in the tree without changing completion. |
| P3. Reuse run-level `blocked` alone, with no task status. | No schema change. | `blocked` stops the whole run, which is the thing the requirements rule out. | Rejected. |

Partial writes are handled by one rule: **a parked task holds no writes.** A task under way parks only after its scope is back at the content it had when it was dispatched, and the ledger proves that from fingerprints.

The alternative was to keep partial writes and require only that the tree be "returned to a verifiable state". I rejected it because no fingerprint can check that; it would depend on the lead's judgement. The cost is that the parked task's partial work is lost, and the executor redoes it after the answer. The requirements' "resumes the parked tasks without redoing accepted ones" does not cover a task that was never accepted.

The fields and their rules. This fragment fixes the decision; the prose around it gives the rules.

```json
{ "status": "parked",
  "dispatch_scope_fingerprint": "<scope fingerprint sealed when the task left pending> | absent",
  "parked": { "question": "<the decision, as asked>", "from": "pending | implementing | correcting",
              "decision_ref": "<caller's id, e.g. Q1> | null", "at": "<timezone-aware time of the park checkpoint>" } }
```

- `dispatch_scope_fingerprint`:
  - goes into `TASK_OPTIONAL`;
  - is filled by `checkpoint` on the `pending → implementing` transition from the predecessor's `scope_fingerprint` for that task, which was read while the task was still pending and before its executor was dispatched;
  - is never changed after that.
- `parked` is required when the status is `parked` and refused otherwise. It also goes into `TASK_OPTIONAL`, so states written before either field existed still validate.
- Transitions:
  - `pending → parked`;
  - `implementing | correcting → parked`, only when the task's current `scope_fingerprint` equals its `dispatch_scope_fingerprint`, which means the scope has been restored. A task without a `dispatch_scope_fingerprint` (dispatched before the field existed) cannot park from a write-active status;
  - `parked → parked | pending`.

  Parking clears `latest_verification` and requires `acceptance` null. The round is unchanged. Unparking always returns the task to `pending`, and it is dispatched again in the ordinary way, so no verification or review is skipped. `parked.from` is kept for the record.
- Scope: a parked task collides exactly as a pending task does. It occupies its scope only against later tasks, which is the existing ordering rule, so an earlier independent task is never starved.
- A parked task is not write-active and cannot be named to `split-check`.
- The run cannot enter `simplifying`, `regression_verifying`, or `final_audit` while any task is parked. Completion is unchanged: every task must be accepted.
- The `blocked` lifecycle is allowed with parked tasks present. `blocked → task` already exists.

## Decisions within the other boundaries

- **Where assumptions and parked questions are recorded:** in the `fsd` run state, `ocs state-dir runs/fsd/<YYMMDD-HHMMSS>-<slug>/state.json`, written only through `ocs state fsd` commands with shapes it validates. Because `runs/` is transient, the retrospective carries a durable copy. An `execute` task parked by the flow carries the `fsd` question id as its `decision_ref`, and that id is the join.
- **Retrospective:** at `ocs state-dir retros/<YYMMDD>-<slug>.md`, which is durable, like `requirements/` and `plans/`. It has these sections: Outcome (the requirements, plan, and `execute` receipt paths), Stages (entry stage, `ralplan` rounds, tasks accepted and parked), Assumptions, Parked questions, What cost the most, and Lessons proposed. A resumed run appends a dated `Resumed` section to the same file.
- **Reversibility list.** A decision parks when undoing it after the run needs more than discarding or reverting the run's own worktree changes. Concretely, it parks when it:
  1. sets a schema or persisted format for data that lives outside the worktree or that already-deployed code reads;
  2. changes a public interface whose consumers are outside the change: exported names, CLI flags, config keys, file formats, network APIs;
  3. deletes or irrecoverably rewrites data that Git cannot restore;
  4. takes an externally visible action: a network write, push, publish, deploy, PR, message, account or billing change, or spend. None of these is taken at all; each is parked as a question.

  Everything else is reversible: it is taken on the recommended option and recorded as an assumption, with its reversal cost stated in files and tasks touched.
- **AGENTS.md is never a task's scope.** A task in the `execute` ledger whose scope meets `AGENTS.md` would write it, so such a change is a decision the flow does not take. When `execute` is started, and at the `ralplan` non-convergence exit, the lead handles every story that would write AGENTS.md in one of two ways:
  - the intended edit becomes a lesson proposal (`ocs state fsd lesson`);
  - if other stories need that edit to exist, they become a parked question that names the lesson.

  The story is never put in the ledger as a task. Appended stale-document tasks exclude it by scope. `ocs state fsd guard` checks the ledger mechanically (U3).
- **Notification:** none. The final report is the run's last message, and an OS notification depends on the environment. A user who wants one can add a `Notification` hook themselves. This is recorded here because the requirements defer the question to the implementation.

## Stories

Each story is one verified unit, and one commit under AGENTS.md's commit rule. U1 and U3 are independent. U2 follows U1. U4 needs U3. U5 needs U1, U3 and U4. U6 needs everything else.

### U1 — `execute` parks individual tasks

Purpose: Decision 2, P1, as a mechanism.

Locations: `plugin/skills/execute/scripts/state.py`, `plugin/skills/execute/references/state-schema.md`, `plugin/skills/execute/references/task-ledger-template.md`, `dev/libexec/check-execute-state`.

Required behaviour:
- Implement the fields, transitions, restored-scope rule, collision rule, and finalization refusal exactly as Decision 2 fixes them.
- Add two transition builders so nobody has to hand-author the new shape:
  - `ocs state execute park <state.json> <task-id>... --question <text> [--ref <id>]`
  - `ocs state execute unpark <state.json> <task-id>...`

  Both go through `_promote` with `"auto"` revision and fingerprints, like `amend`. `park` stamps `parked.at`, clears the task's verification, and refuses a write-active task whose scope is not restored; its error names the scope paths still differing. `unpark` sets `pending` and drops the field.
- `reconcile` needs no change: a `blocked` run's `next_action` already carries the continuation.
- The two references gain the fields, the commands, and one ledger paragraph. That paragraph says:
  - a decision only some tasks depend on parks those tasks while the rest continue;
  - a task already under way first has its scope restored to its dispatch content, and its executor stops before any decision-dependent write;
  - when nothing is dispatchable and a task is parked, the run checkpoints `blocked` and names each parked question;
  - once the decision is made, `unpark` returns the task to `pending`, and a ruling that changes the plan lands there through `amend`;
  - Finalization does not start while a task is parked.

Acceptance: `dev/kein-dev check-execute-state` exits 0 with new cases that fail if any of these moves:
- (a) `pending → parked` is accepted and stamps `parked.at`. `reviewing → parked` is refused;
- (b) `implementing → parked` is refused while the task's scope holds a write, naming the path, and accepted once the write is removed;
- (c) a task dispatched in a state written without `dispatch_scope_fingerprint` cannot park from `implementing`;
- (d) `pending → implementing` fills `dispatch_scope_fingerprint` from the predecessor, and a later candidate that changes it is refused;
- (e) `parked → accepted` and `parked → implementing` are refused, and `parked → pending` via `unpark` is accepted;
- (f) `parked` without the field, and the field on a non-parked task, are both refused;
- (g) with task-002 parked, task-001 is driven to acceptance;
- (h) entering `final_audit` while a task is parked is refused, and completion is refused;
- (i) an *earlier* task whose scope meets a parked task's scope can become write-active, and a *later* one cannot;
- (j) `split-check` refuses a parked task;
- (k) a `blocked` checkpoint holding a parked task and an accepted task validates, and `blocked → task` followed by `unpark` then continues;
- (l) the existing legacy-state fixture still validates.

Each case asserts the refusal *reason* where the existing file already does so (`refused for the wrong reason`). If the checks fail, correct `state.py`. Never relax a case to make it pass.

### U2 — `execute`'s prose stops describing a serial ledger, and names parking

Locations: `plugin/skills/execute/SKILL.md`, `docs/skills/execute/open.md`.

Required behaviour:
- Delete "Then advance serially." from Task Loop step 7 and put no replacement sentence about order there. The project's rule is deletion rather than rewording, and `task-ledger-template.md` already states the scope rule.
- Add one sentence to the Task Loop naming `park` as the route for a decision only some tasks depend on, pointing at the ledger contract. Entry step 3's whole-run `blocked` stays for a run that is not executable at all.
- In `open.md`, rewrite §1 so it no longer quotes a sentence `SKILL.md` does not contain. It should record that since 2da9b80 tasks with disjoint scopes within one run are written at once, and that the per-worktree `flock` still admits one run per worktree, a cross-vendor invariant (keep the §2 reasoning). Delete the claim that nothing records why the ledger is serial within a run.

Acceptance:
- `grep -rn "serial" plugin/skills/execute docs/skills/execute` prints no line that describes the ledger or task order as serial.
- `grep -n "park" plugin/skills/execute/SKILL.md` prints the new sentence.
- The sentence names only commands that `ocs state execute --help` lists after U1.

### U3 — the `fsd` state machine

Purpose: record everything a hook and the final report read, so neither depends on the model's memory.

Locations: `plugin/skills/fsd/scripts/state.py` (reached as `ocs state fsd`), `plugin/skills/fsd/references/state-schema.md`, `dev/libexec/check-fsd-state`.

State shape (the decision; field order free):

```json
{ "schema_version": 1, "workflow": "fsd", "run_id": "…", "lifecycle": "active | paused | completed | halted | aborted",
  "worktree": "<canonical root>", "entry": "interview | ralplan | execute",
  "input": {"kind": "idea | requirements | plan", "reference": "<path> | null", "summary": "<text>"},
  "agents_md": [{"span_started_at": "<time>", "sha256": "<hex> | null"}],
  "halt": null | {"reason": "<violation or unfinished stage, stated>"},
  "stages": {"interview|ralplan|execute|closeout": {"status": "skipped | pending | entered", "snapshot": ["<run dirs present at entry>"], "run": "<associated state/ledger path> | null"}},
  "assumptions": [{"id": "A1", "stage": "…", "decision": "…", "chosen": "…", "alternatives": ["…"], "reversal_cost": "…", "where": "…"}],
  "questions":   [{"id": "Q1", "stage": "…", "question": "…", "options": ["…"], "recommended": "…", "why_irreversible": "<list item 1-4 and reason>", "parks": "<stories or task ids, or 'whole run'>", "answer": null}],
  "lessons":     [{"id": "L1", "line": "<proposed AGENTS.md line>", "why": "…"}],
  "retrospective": "<path> | null", "next_action": "…" }
```

Commands:
- `start --run-root <runs/fsd> --slug <s> --input <path-or-text>` classifies the input mechanically:
  - a file that passes `ocs validate interview requirements` with `Status: Approved` → `ralplan`;
  - a file that passes `ocs state ralplan validate-plan` with `Status: Approved` → `execute`;
  - a plan that is not Approved → `ralplan` over that plan;
  - requirements that are not Approved → `interview`;
  - anything else is an idea → `interview`.

  Stages before the entry are marked `skipped`. `start` opens the first `agents_md` span with AGENTS.md's hash, or null when the file is absent. It refuses when a nonterminal `fsd` run already exists for the worktree, and prints that run's path and `status` instead.
- `enter <state> <stage>` marks the stage `entered`. The hook calls it. When the stage has no associated run, it snapshots the stage's run root. When the stage already has an associated run (one that `resume` kept), it keeps that association and takes no snapshot. It is idempotent for a stage already entered.
- `gap <state>` prints `{gap, completed, next, action}` using the table below.
- `assume`, `question`, `answer <id> --text`, `lesson` append to or fill the lists. Ids are minted and never reused.
- `guard <state>` reads the associated `execute` state. It exits nonzero and lists every task whose scope meets `AGENTS.md`, using `execute`'s own scope-collision reading, where a directory scope covers what is under it. The lead runs it after `execute start`, after every appended task, and `close` runs it again.
- `closeout <state>` enters the closeout stage.
- `close <state> --retro <path>` refuses, and changes nothing, when:
  - AGENTS.md's hash differs from the current span's recorded hash;
  - `guard` fails;
  - the retrospective lacks any assumption, question, or lesson id.

  Otherwise it sets `completed` only when the associated `execute` state is a `completed` receipt, and `paused` when some question is unanswered. In every other case it refuses and names the unfinished stage.
- `halt <state> --reason <text>` is the end state for a run `close` refused. It sets the terminal lifecycle `halted` with `halt.reason`, and it is refused when `close` would succeed. `report` works in every lifecycle: for a halted run it opens with a **Halted** section naming the violation or unfinished stage, then prints the usual sections. So the run still ends in a stated state and the final report is still produced.
- `report <state>` renders the final report: sections Assumptions, Parked questions (with how to answer: re-invoke `/kein:fsd` with the answers), Lesson proposals (numbered, each vetoable), and Retrospective. An empty list is printed as `None.`
- `resume <state>` does three things, and refuses while any question is unanswered:
  - it moves `paused → active`;
  - it sets `execute` and `closeout` back to `pending` while keeping `execute`'s associated run;
  - it opens a new `agents_md` span with the file's current hash, keeping earlier spans for the record. "Byte-identical before and after a run" is measured per invocation span, so an owner's edit made while the run was paused is not charged to the run.
- `status`, `validate`, `abort --reason`.

Stage association: a stage's run is the one that `resume` kept, or else the one run directory that appeared under the stage's run root since the `enter` snapshot. When there is none, or more than one new directory, there is no association, and so no gap evidence: the flow allows by default. `status` reports which case it found.

Gap table. `gap` is true only on a row whose evidence holds. Every row requires positive evidence; an unfinished or unreadable stage gives no row:

| Evidence that a stage is complete | Next stage not yet entered | `action` names |
| :-- | :-- | :-- |
| `fsd` run started and its entry stage is still `pending` | entry stage | invoke `/kein:<entry> <input>` |
| interview ledger has `status: completed` and its `requirements_path` shows `Status: Approved` | ralplan | invoke `/kein:ralplan <requirements path>` |
| ralplan state is `completed` | execute | invoke `/kein:execute <plan path>` |
| interview or ralplan state is `aborted` | closeout | run `ocs state fsd closeout <state>` |
| the associated execute state is a `completed` or `aborted` receipt; or it is `blocked`, no task is write-active, at least one task is parked, and every parked task's `decision_ref` names an `fsd` question whose `answer` is null; or it is `blocked` with no parked task and an unanswered `fsd` question whose `parks` is `whole run` | closeout | run `ocs state fsd closeout <state>` |
| `fsd` lifecycle is `completed`, `paused`, `halted`, or `aborted` | none | no gap |

The `blocked` evidence reads the parked tasks' questions. Answering them makes the row false by construction, so after `resume` the `execute` run, still `blocked` until its lead writes the checkpoint that leaves it, is a running stage and not a finished one.

Acceptance: `dev/kein-dev check-fsd-state` exits 0, driving real fixture states built in a temp repo with the real `interview`, `ralplan`, and `execute` state commands. It must cover:
- the five input classifications;
- `gap` false inside every running stage and true on each row above;
- an ambiguous association giving no gap;
- `report` printing `None.` for each empty list and every id otherwise;
- `close` refusing a changed AGENTS.md and a retrospective missing an id;
- `close` → `paused` while a question is unanswered;
- `resume` refused while a question is unanswered, and accepted after `answer`;
- **pause → answer → resume → `enter execute`, with the `execute` run still `blocked` and its task still parked:**
  - the association is the same run path as before the pause;
  - `gap` is false;
  - `close` refuses, naming `execute` as not completed;
- a `blocked` `execute` run with one parked task whose `decision_ref` is null gives `gap` false (no positive evidence);
- AGENTS.md edited while the run is paused, then `resume`: `close` succeeds and the state holds both spans. AGENTS.md edited after `resume`: `close` refuses;
- `guard` fails on a ledger with a task scoped `AGENTS.md` and on one scoped to the repository root, and passes on one scoped `docs/`. With `guard` failing, `close` refuses, and `halt --reason` then sets `halted`. `report` on that run opens with the Halted section naming the task. `halt` is refused on a run `close` would complete.

It also drives a `ralplan` run through five official rounds, each opened with `open` and resolved with `block` then `revised`. It then opens round 6 and, from that `reviewing` phase, runs `approve --findings` with deferrals on both an `architecture` ground and a `safety` ground. The case asserts that the receipt is `completed` and carries both deferrals. It also asserts that `approve` after `block` in the same round is refused, which is the ordering `decision-policy.md` depends on. It proves the non-convergence exit needs no `ralplan` change, and it fails if the requirements' "no new mechanism" claim stops holding.

### U4 — the stage-transition hooks

Purpose: catch a turn that announced the next stage without taking it, under the binding hook constraints.

Locations: `plugin/skills/fsd/scripts/hook.py`, the frontmatter of `plugin/skills/fsd/SKILL.md` (the file itself is written in U5; U4 owns its `hooks:` block), `dev/libexec/check-fsd-hooks`.

**Gate — G1, frontmatter hooks under a nested skill.**

- Claim: `fsd` runs in exactly one mode, and the probe measures that mode. The probe skill declares `disable-model-invocation: true` and is invoked by a user-level `/<probe-plugin>:<skill>` prompt, never by the Skill tool. In one process, after that invocation, three things hold:
  - (a) its frontmatter Stop and PreToolUse hooks still fire after the model invokes a *second*, model-invocable skill with the Skill tool;
  - (b) a frontmatter `PostToolUse` hook with matcher `Skill` fires, and its input carries the invoked skill's name;
  - (c) `${CLAUDE_PLUGIN_ROOT}` expands in a frontmatter hook command.

  Two more facts are recorded because the alternate path depends on them:
  - (d) the `session_id` a hook sees before and after a `claude -c` continuation in a new process;
  - (e) whether a plugin `hooks.json` UserPromptSubmit handler receives the raw `/<plugin>:<skill> …` text as its `prompt`.

  Also recorded, though no path depends on it: whether frontmatter hooks fire on a subagent's tool calls.
- Evidence method: the 2026-09-19 probe's shape, in the mode above. The throwaway plugin sits in a `mktemp -d` scratch repository:
  - a slash-only skill declares all three hooks, and each hook appends its stdin JSON to a log;
  - a second, model-invocable skill does nothing;
  - a `hooks.json` UserPromptSubmit handler and a PostToolUse `Bash` handler log their input too.

  Run headless: `claude -p '/<probe-plugin>:<skill> …' --plugin-dir <plugin>`, whose body tells the model to invoke the second skill, write a file, and stop. Then run `claude -c -p 'write another file' --plugin-dir <plugin>` in a new process. Read the log. Also run `claude plugin validate <plugin> --strict` on the probe plugin. Record the result in `docs/skills/fsd/<YYMMDD>-hook-probe.md`.
- Alternate path:
  - **If (a) or (c) fails:** the three handlers move to `plugin/hooks/hooks.json`, where `${CLAUDE_PLUGIN_ROOT}` is proven, and every handler allows unless its input's `session_id` matches the one armed in `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/kein/fsd/armed/<sha256 of project root>`. Arming follows (e):
    - if UserPromptSubmit receives the raw text, a handler on it arms when the prompt begins `/kein:fsd`;
    - if it does not, a PostToolUse `Bash` handler arms when the command runs `ocs state fsd start`, `resume`, or `status`. `fsd`'s entry always runs one of those first.

    Per (d): if `claude -c` mints a new `session_id`, a new process is disarmed until `/kein:fsd` is invoked again, as the requirements describe. If it keeps the old one, the continued session stays armed. That is harmless, because every handler still acts only on gap evidence. The probe record states which case holds.
  - **If only (b) fails:** the flow keeps the frontmatter hooks, and the lead runs `ocs state fsd enter <stage>` immediately before invoking each stage skill. The block reason then names that command.
- Unexpected result: frontmatter hooks do not fire after invocation at all (contradicting the 09-19 probe), or `--strict` rejects both the frontmatter and the `hooks.json` placement. Stop U4 and everything after it, and return to the requirements owner, since the hook constraints are binding and no decided path remains.

Required behaviour of `hook.py` (modes `stop`, `pre-write`, `post-skill`):
- Every path exits 0 and allows unless all of the following hold: no off-switch marker at `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/kein/fsd/hooks-off`; a nonterminal `fsd` run for `$CLAUDE_PROJECT_DIR`, found the way `ocs state-dir` resolves; and `gap` true. Any exception or unreadable state allows.
- `stop`: when the input's `stop_hook_active` is true, allow. Otherwise, on gap, block once with `action` as the reason, prefixed "fsd:".
- `pre-write` (matcher `Write|Edit|MultiEdit|NotebookEdit`, and nothing else, so never Bash, Skill, Agent, or reads): on gap, deny with the same reason.
- `post-skill` (matcher `Skill`): when the invoked skill is `kein:interview`, `kein:ralplan`, or `kein:execute`, call `enter` for that stage. It never blocks.

Frontmatter shape (the decision):

```yaml
disable-model-invocation: true
hooks:
  Stop:        [{hooks: [{type: command, command: 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/fsd/scripts/hook.py" stop'}]}]
  PreToolUse:  [{matcher: "Write|Edit|MultiEdit|NotebookEdit", hooks: [{type: command, command: '… hook.py pre-write'}]}]
  PostToolUse: [{matcher: "Skill", hooks: [{type: command, command: '… hook.py post-skill'}]}]
```

Acceptance: `dev/kein-dev check-fsd-hooks` exits 0. Like `check-git-guard`, it feeds synthetic hook JSON against fixture states from U3 and fails if any of these moves:
- Stop blocks on each gap row, and allows in every running stage, on `stop_hook_active: true`, with the off-switch present, with no `fsd` run, with a corrupt state, and when the hook itself raises;
- pre-write denies `Write` on a gap and allows `Bash`, `Read`, `Skill`, and `Agent` on the same gap;
- post-skill for `kein:ralplan` records the stage entry, and the next Stop allows;
- pause → answer → resume → post-skill for `kein:execute`, with the `execute` run still `blocked` and its task parked: pre-write allows `Write` (the lead's checkpoint candidate) and Stop allows.

After G1 passes: `claude plugin validate plugin --strict` passes with the frontmatter in place.

### U5 — the `fsd` skill

Locations: `plugin/skills/fsd/SKILL.md`, `plugin/skills/fsd/references/decision-policy.md`, `plugin/skills/fsd/references/closeout.md`, `README.md` (the Layout line and the skill count, the off-switch in the hooks entry, and `retros/` under "Where state goes").

Required behaviour. The prose names no model and no omc skill.

- **Entry.** Resolve the run root with `ocs state-dir runs/fsd` and run `ocs state fsd start` with the arguments. If a nonterminal run exists:
  - if it is paused and the arguments answer its questions, record each with `answer`, then `resume`;
  - otherwise follow `status`.

  Then invoke the stage `gap` names.
- **Between stages.** When a stage ends, invoke the next one in the same turn. `interview`'s own "stop without a downstream handoff" ends that skill, not the flow.
- **After the interview's approval, ask the user nothing** until the report. This overrides `ralplan`'s "ask the user immediately" and `execute`'s "ask the one question". Every such decision goes through `decision-policy.md`.
- **`decision-policy.md`** holds:
  - the reversibility list above, verbatim;
  - reversible → take the recommended option, then `ocs state fsd assume`;
  - irreversible → `ocs state fsd question`, then `ocs state execute park … --ref Q<n>` for the dependent tasks. Tasks whose scope is disjoint but which depend on the decision are named and parked by the lead. A task already under way has its scope restored first;
  - a story or appended task that would write AGENTS.md → the AGENTS.md rule above;
  - execute blocked for any other reason → a question that parks the whole run.
- **`ralplan` non-convergence exit** (in `decision-policy.md`). At the diagnostic trigger (round ≥ 5 with a blocking ground standing, re-armed every five rounds), split the standing grounds by the list.
  - Ordering: when an official round numbered 5 or higher resolves with a standing BLOCK, the lead does not run ralplan's step-6 `block`. From that round's `reviewing` phase, it runs `ocs state ralplan approve --findings` with every standing ground deferred. `block` moves the run to `revising`, and `approve` is refused from there. A round that already ran `block` goes through `revised` and the next round, and the exit applies when that round resolves.
  - Each ground is deferred in `approve --findings`. A reversible ground gets `deferral.reason` = why the ground does not hold for an unattended run and `caught_by` = "fsd assumption A<n>; execute final audit". An irreversible ground gets `caught_by` = "fsd question Q<n>; tasks from <stories> start parked".
  - The approving `Status` line reason names every deferral and every parked story.
  - This deliberately departs from `ralplan`'s "`Caught by` belongs in the plan's pre-mortem before the approval": a plan revision moves the review hash and reopens the round, which is the loop the exit exists to break. The `Status` line, the receipt, and the retrospective carry the catcher instead.
  - A ground whose correction would write AGENTS.md is handled by the AGENTS.md rule above, as a lesson proposal or a parked question, never a task.
  - After `execute start`, park the tasks normalized from those stories, then run `ocs state fsd guard`.
- **Stale documents** (`closeout.md`, run *inside* `execute`). After the last plan task is accepted and before Finalization, find the project documents the change made stale: a read-only `kein:explore` sweep over docs that name changed paths, symbols, commands, or flags. Append one task per disjoint document set, with scope excluding `AGENTS.md` and `CLAUDE.md`, so the final audit covers them.
- **Closeout** (`closeout.md`, after `execute` ends). The steps, in order:
  1. `ocs state fsd closeout`;
  2. draft lessons, and record each with `lesson`, never touching AGENTS.md;
  3. write the retrospective at `ocs state-dir retros/<YYMMDD>-<slug>.md` in the shape settled above;
  4. `close --retro`. If it refuses, run `halt --reason` with its refusal text; nothing is repaired after the fact;
  5. print `report` verbatim as the final message. This happens in every case, including a halted run.
- **After any compaction**, run `ocs state fsd status` and the current stage's `reconcile` before acting.

Acceptance:
- `claude plugin validate plugin --strict` passes.
- `grep -nE "opus|sonnet|haiku|fable|gpt-" plugin/skills/fsd -r` prints nothing.
- Every `ocs` command named in `plugin/skills/fsd` appears in `ocs state fsd --help` or `ocs state execute --help`.
- A fresh headless session in a scratch repository (`claude -p --plugin-dir plugin --output-format stream-json --verbose`) does not list `kein:fsd` in its skills, while `/kein:fsd` loads there: the hook log or transcript shows the skill body and the post-skill handler firing. This is the check 8d88f63 used.

### U6 — the unattended flow, live

Purpose: the requirements' acceptance criteria that only a real run can show, exercised cheaply in scratch repositories.

Locations: `dev/libexec/fsd-fixture` (builds a named fixture into a given directory outside any CLAUDE.md ancestry, the way `eval` does), `docs/skills/fsd/<YYMMDD>-live-run.md` (the record).

Fixtures:
- Fixture A has a tiny Python module, a README that describes it, an AGENTS.md, and an **Approved** plan with three stories:
  - T1 is independent and makes the README stale;
  - T2 carries an internal choice (reversible);
  - T3 needs a persisted-format decision consumed outside the repository (irreversible, list item 1).
- Fixture B is an Approved requirements document for a one-story change.
- Fixture C is built so that round 6 cannot pass. Its requirements name two choices as the owner's and leave both open:
  - the output format a downstream consumer reads, which is a public interface (list item 2);
  - an internal helper's name.

  Its `Decision boundaries` do not grant either to the implementer. The fixture plan picks both without authority. With that construction, a lane can approve only by inventing an owner decision the requirements withhold, so a blocking `scope` or `acceptance semantics` ground is what the review contract calls for. The fixture's `ralplan` run is advanced through five official blocked rounds with the existing commands, the way U3 drives it, and stands at `drafted` awaiting round 6.

Every run uses `claude -p --plugin-dir <repo>/plugin --permission-mode bypassPermissions --output-format stream-json --verbose > transcript.jsonl`. That permission mode is acceptable only because the repository is a throwaway.

| Run | Shows | Pass when |
| :-- | :-- | :-- |
| A1 `/kein:fsd <plan>` | AC1 (plan → execute), AC2, AC3, AC4, AC6, AC8 | `fsd` `entry` is `execute`, and no interview or ralplan run directory exists. Zero `AskUserQuestion` calls, and the last assistant message is the rendered report. T1 is `accepted` and T3 is `parked` with `decision_ref`. T3's current `scope_fingerprint` equals its `dispatch_scope_fingerprint` if it has one; if it has none, it was parked from `pending`. **T1's verification ran on a tree containing T3's parked state:** T1's accepted verification `observed_at` is later than T3's `parked.at`. If the fixture's ordering does not produce that interleaving, the row is inconclusive for this condition and is rerun with T3 ordered ahead of T1 in the plan. The report lists T2's assumption with a reversal cost, T3's question, lessons or `None.`, and the retrospective path, and T2's work is in the tree. AGENTS.md's sha256 is unchanged. |
| A2 `/kein:fsd Q1=<answer>` in a new process | AC7, AC9 | T1's `acceptance` and round are byte-identical to A1's. T3 goes from `parked` to `accepted`. The README task is in the ledger ahead of a final-audit PASS, and the `execute` receipt is `completed`. AGENTS.md is still unchanged. |
| B `/kein:fsd <requirements>` with `--max-turns` capped once `execute` is entered | AC1 (requirements → ralplan) | The first Skill call is `kein:ralplan`, and no interview run directory exists. |
| I `/kein:fsd add a --verbose flag` with `--max-turns` small | AC1 (idea → interview) | The first Skill call is `kein:interview`, and the turn ends on the interview's question with no Stop block in the hook log. |
| C `/kein:fsd` resuming Fixture C | AC5 | Round 6's lanes returned BLOCK. The lead approved from round 6's `reviewing` phase with deferrals, not through `block`, and the run went on to an `execute` stage entry. The output-format ground is an `fsd` question whose `caught_by` names it, and the naming ground is an assumption. If round 6 returns no BLOCK in two runs, AC5 is recorded as **unproven** in the live-run record. U3's mechanical case shows only that the `ralplan` mechanism admits the exit, not that the `fsd` lead takes it, so it does not close AC5. |

AC10 and AC11 are closed by U5, and AC2's post-approval half is independent of the entry stage, so A1 covers it. For the idea path, feed interview answers and the approval through `--input-format stream-json` in one process if that works. If it does not, record that the interview-to-ralplan transition is covered by U4's synthetic case alone.

Acceptance: `docs/skills/fsd/<YYMMDD>-live-run.md` records each run's command, the fixture commit, and the observed facts against its row. Every row passes, or is recorded as inconclusive or unproven under the rule stated in its row, and an unproven AC is listed in the record's first paragraph. A failed row goes back to the story that owns the behaviour. It is never waived here.

## Pre-mortem

- **S1: the Stop hook loops or blocks a legitimate wait, as omc's did.** Caught by: U4 `check-fsd-hooks`, which asserts allow on `stop_hook_active`, in every running stage, on corrupt state, and when the hook raises · Prevented by: allow-by-default `hook.py` with the `stop_hook_active` short-circuit and a gap judged only from recorded stage completion · Acts on: reads the hook's stdin JSON, the off-switch marker, and the nonterminal `fsd` `state.json` under `$CLAUDE_PROJECT_DIR/.agents/kein/runs/fsd/` plus the stage run file it associates · Residual: a misread gap costs one extra turn per stop.
- **S2: a parked task's half-written scope is read by an independent task's verification or reaches an audit, or a parked task starves an independent one.** Caught by: U1 cases (b), (c), (h) and (i), and U6 run A1's interleaving condition · Prevented by: the restored-scope rule on parking from a write-active status, the finalization refusal while any task is parked, and a parked task colliding as a pending one · Acts on: `validate_transition` and `_scope_collisions` in `plugin/skills/execute/scripts/state.py`, comparing the candidate task's `scope_fingerprint` (recomputed by `_autofill` from the worktree) with its sealed `dispatch_scope_fingerprint`, and reading each task's `status` · Residual: a task whose scope is disjoint but which depends on the unmade decision, and which the lead fails to park, builds on it. Nothing mechanical catches that before the post-resume final audit.
- **S3: the flow asks the user mid-run, or stops quietly inside a stage.** Caught by: U6 run A1 (zero `AskUserQuestion`, last message is the report) · Prevented by: `fsd` SKILL.md's no-ask rule and `decision-policy.md`. No hook may enforce this, because the requirements forbid judging quiescence and denying non-writing tools · Acts on: the lead's reading of the loaded skill body, re-established after compaction by `ocs state fsd status` · Residual: a quiet in-stage stop stalls the run until the user returns, which is accepted by the requirements' hook constraints.
- **S4: stage hooks silently disarm when `fsd` invokes `interview`, so no transition is ever enforced.** Caught by: Gate G1 (a) · Prevented by: G1's alternate path (session-armed `hooks.json` handlers) · Acts on: `plugin/hooks/hooks.json` handlers comparing input `session_id` with the armed file under `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/kein/fsd/armed/` · Residual: None.
- **S5: a task writes AGENTS.md during the flow.** Caught by: `ocs state fsd guard` after `execute start` and every appended task, and `close`'s span-hash comparison (U3 cases), then U6 runs A1 and A2 · Prevented by: the AGENTS.md rule, under which such a story becomes a lesson proposal or a parked question and never a ledger task, and the scope exclusion for appended document tasks · Acts on: `guard` reads the associated `execute` `state.json` task scopes through `execute`'s scope-collision reading; `close` compares the last `agents_md` span's `sha256` in `fsd` `state.json` with the bytes of `<worktree>/AGENTS.md` · Residual: a write made outside any task's scope (a lead's own Edit) is caught only at `close`. The run then ends `halted` with the violation named in the report, rather than being prevented.
- **S6: the `ralplan` exit approves over an irreversible ground as if it were reversible.** Caught by: U6 run C (the interface question must surface as a parked question) · Prevented by: `decision-policy.md`'s list, which a ground is classified against before its deferral is written · Acts on: the `deferral.caught_by` text written through `ocs state ralplan approve --findings` and the matching `ocs state fsd question` entry · Residual: misclassification is agent judgement, as the requirements' first risk accepts.
- **S7: after an answer and `resume`, the flow is pushed into closeout, or closes `completed`, while the task is still parked and unaudited.** Caught by: U3's pause → answer → resume case (`gap` false, `close` refuses) and U4's matching hook case · Prevented by: the closeout row's `blocked` evidence requiring every parked task's question to be unanswered, `enter` keeping the association `resume` preserved, and `close` requiring a `completed` `execute` receipt · Acts on: `gap` and `close` in `plugin/skills/fsd/scripts/state.py`, reading the associated `execute` `state.json` (`lifecycle`, task `status`, `parked.decision_ref`) and the `fsd` state's `questions[].answer` · Residual: None.

## Risks not covered above

- A paused run keeps `execute`'s worktree claim, so a second `execute` in that worktree is refused until resume. The report states the run is paused. Another worktree is unaffected (`docs/skills/execute/open.md` §1).
- A user commit while the run is paused moves HEAD. `reconcile` then reports drift and routes through inspection, which is existing behaviour; sealed acceptances are not recomputed.
- Live runs cost tokens. U6 runs once, at the end, on fixtures of a few files, and B and I are capped with `--max-turns`.
- Rollback: every story is a separate commit. U1 is additive to the schema (optional fields, legacy states validate), so reverting it strands no existing run. Only a run that parked a task, or dispatched one after U1 landed, would need U1 present.

## Open Questions

- Partial answers: `resume` currently requires every question answered, so answering only some leaves the run paused. The requirements say only "after the user answers parked questions". Letting `resume` unpark just the tasks whose questions are answered would also need the closeout row to consider only the still-unanswered questions' tasks. The answer changes `resume`'s refusal and one gap-row clause, not the structure.

- Should AGENTS.md's "상태와 기록" line list `retros/` beside `requirements/`, `plans/`, `handoff/`? It changes this repository's instructions, not the flow's behaviour, so this plan edits only README.md and leaves that to the owner.
- `task-ledger-template.md`'s lead currently decides whether to write disjoint tasks at once, and 2da9b80 chose that the harness "neither asks for this nor warns against it". The requirements' "Execution uses `execute`'s existing parallelism" is met here by removing the serial sentence, not by `fsd` prose urging concurrency. If the owner wants `fsd` to ask for it explicitly, that is one sentence in U5, and it goes against the 2da9b80 rule.
