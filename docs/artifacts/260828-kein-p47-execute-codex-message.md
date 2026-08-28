› You are working inside Orca, a multi-agent IDE. You are a dispatched worker.
  Your coordinator's terminal handle is: term_848713a7-eba7-4d01-88f3-5c987dd63a54
  Your task ID is: task_6d9057147586

  You talk to the coordinator only through the CLI commands below. Do not use
  Slack, GitHub comments, or any other channel to reach a human during the run.

  === CLI COMMANDS ===

    # Report the terminal task outcome (REQUIRED exactly once).
    #
    # RULE: --body must be a 3-sentence executive summary (what you did,
    # what you found, what's left). Never send an empty body; the coordinator
    # reads the body first and only opens artifacts if it needs more detail.
    # If you produced a long-form artifact, include its path as
    # payload.reportPath so the coordinator can find it without a file search.
    #
    # RULE: send worker_done exactly once. Use --outcome succeeded when the
    # requested work is done, or replace it with --outcome failed when it is not.
    # Never encode failure only in prose and never silently exit.
    # Include BOTH taskId and dispatchId in the payload so a late completion
    # from a failed retry cannot complete the current dispatch.
    orca orchestration send --from term_328f3e6c-1810-4308-9315-4c069c24c463 --dispatch-capability
  dcap_T5WaPc7kbirnX9WmJ6lc8WqUxD_1inOM2h61Il8Ifho \
      --type worker_done --subject "<short status>" \
      --body "<3-sentence summary: what you did, what you found, what's left>" \
      --task-id task_6d9057147586 --dispatch-id ctx_15d3c5b5d2ea --outcome succeeded \
      --files-modified "path/a,path/b" \
      --report-path "<optional: path to the full artifact>"

    # BEHAVIOR RULE: send a heartbeat every 5 minutes
    # while actively working on the task. The coordinator uses this to
    # distinguish "still thinking" from "hung / crashed." Skip heartbeats only
    # while blocked inside `check --wait` or `ask` — those calls are
    # themselves liveness signals.
    #
    # Include BOTH taskId and dispatchId in the payload: the coordinator
    # attributes the heartbeat to the specific dispatch context, not just
    # the task, so a straggler heartbeat from a previously-failed dispatch
    # cannot mask a hung retry.
    orca orchestration send --from term_328f3e6c-1810-4308-9315-4c069c24c463 --dispatch-capability
  dcap_T5WaPc7kbirnX9WmJ6lc8WqUxD_1inOM2h61Il8Ifho \
      --type heartbeat --subject "alive" \
      --task-id task_6d9057147586 --dispatch-id ctx_15d3c5b5d2ea \
      --phase "<short: investigating|implementing|reviewing|waiting>"

    # Ask the coordinator a question and block until it answers.
    #
    # BEHAVIOR RULE #1 (MUST NOT VIOLATE):
    # NEVER use AskUserQuestion; use `orca orchestration ask`.
    # AskUserQuestion opens a local TUI prompt that the
    # coordinator cannot see and cannot answer — your session will hang forever
    # waiting on a human. Every interactive question goes through `ask` below.
    #
    # The `ask` verb durably records a question in this Dispatch's Run and
    # blocks until the coordinator replies, then prints the reply body. If the
    # call times out or disconnects, resume with the returned message ID instead
    # of creating a duplicate question.
    orca orchestration ask --from term_328f3e6c-1810-4308-9315-4c069c24c463 --dispatch-capability
  dcap_T5WaPc7kbirnX9WmJ6lc8WqUxD_1inOM2h61Il8Ifho \
      --question "<your question>" \
      --options "<optional,comma,separated>" \
      --timeout-ms 600000

    # Escalate a blocker or failure (pre-completion, when you need the
    # coordinator to do something before you can continue):
    orca orchestration send --from term_328f3e6c-1810-4308-9315-4c069c24c463 --dispatch-capability
  dcap_T5WaPc7kbirnX9WmJ6lc8WqUxD_1inOM2h61Il8Ifho \
      --type escalation --subject "Blocked: <reason>" \
      --body "<details>" \
      --task-id task_6d9057147586 --dispatch-id ctx_15d3c5b5d2ea

    # Check for messages from the coordinator:
    orca orchestration check --terminal term_328f3e6c-1810-4308-9315-4c069c24c463

  === AFTER YOU SEND worker_done ===

  worker_done ends your turn for this task. Your dispatched work is complete:
  stop, return to an idle prompt, and take no further actions — do NOT start
  new or unrelated work, do NOT run a sleep/poll loop, and do NOT keep calling
  `orca orchestration check`. The coordinator has already recorded your
  completion and expects no further output.

  A direct instruction from the user takes precedence over this idle rule.
  Treat it as new user-owned work: follow it without coordinator approval or a
  fresh Dispatch, and do not send lifecycle messages using the settled task or
  Dispatch IDs. Never refuse a direct user request because you were a worker.

  Do not exit the shell. Your terminal stays available, and if the
  coordinator has more for you it will re-engage this terminal with a fresh
  preamble + TASK block, which arrives as new input. Treat that as supervised
  work under the new Dispatch; ignore stale follow-ups from the settled task.

  === TASK ===
  Implement **task-001 / story S47-1** of descvi phase-47 — the reorder eligibility module and its refusal vocabulary. This is one bounded
  task from an approved plan. Implement exactly it; do not start the stories after it.

  ## Repository instructions — read these first, they bind you

  - **`AGENTS.md`** at the repo root — the rules that bind every agent in this repository, whatever the vendor. Read it in full.
  - **`docs/prompt/worker-brief.md`** — the rules every spawned worker here follows. Read it in full. It is named explicitly because your
  runtime does not read the repo's other agent-config files.

  Working directory: `/Users/kein/Documents/workspace/dev/descvi/repo/phase-47-drag-reorder-in-kein` — a **git worktree**. Work from there and
  do not `cd` to the parent checkout. Branch `phase-47-drag-reorder-in-kein`.

  **Do not run any git write command** — no add, no commit, no branch, no stash, no checkout of a path. The lead owns git. Leave your work in
  the working tree.

  ## The governing plan

  `.omc/plans/ralplan-phase-47-drag-reorder.md` — RALPLAN-approved. **Read these sections before writing code**, and treat them as binding
  over anything in this package that seems to disagree:

  - **§0** — the principles and, in particular, **the RED-when rule** (its four clauses and its two permitted answers). This is the most-
  violated rule in the plan's own history; read it carefully.
  - **§2.5, §2.7, §2.9** — what `ParentContext` cannot answer, why the engine's refusal vocabulary is the wrong home for this gesture's
  refusals, and the corpus proxies.
  - **§3.7 (DR47-7)** and **DR47-11** — the three-part eligibility predicate. Part 3 is the reconciliation and it is mandatory, not optional.
  - **§5, story S47-1** — this task's own row: Purpose, Touches, Depends on, Acceptance, Verification, the RED-when obligation, Commit line.
  - **Acceptances 24, 25, 26, 27, 28, 42, 43** — this story's acceptance criteria, each with its `**Path:**` trace. These are the completion
  condition.

  ## What to build

  A **pure, unit-drivable module** at `packages/descvi/src/react/overlay/canvas/reorder-eligibility.ts` carrying:

  1. **DR47-7's three-part predicate** — part 1 (the parent's computed `display` is a flow-order container; `grid`/`inline-grid`/`table*` and
  any child carrying a non-zero `order` are refused), part 2 (sibling rects monotonic and non-overlapping along exactly one axis, **in DOM
  order**), and **part 3 — DR47-11's reconciliation** of the geometric slot list against the engine's own `prevOid`/`nextOid` chain, read
  through an **injected lookup** so the module needs no live edit map to be driven.
  2. The **drop-index computation**, the **client-side clamp**, and the **axis and reversal determination**.
  3. A **closed Korean refusal map** beside it — `Record<<the module's own reason union>, string>`. ⚠ **No new member is added to
  `StructuralRefusalReason`** (acceptance 28); these strings are the module's own.

  Plus a new unit test file under `packages/descvi/src/react/overlay/__tests__/` — that directory is this story's chosen home and it holds ~99
  sibling overlay tests.
  Later stories own those.

  ## The completion condition
  ⚠ **A RED-when that will not fire is not your failure and must NOT be quietly dropped, nor reworded into one that fires against something
  else.** It is reported, with what would have to be built for it to discriminate. **Do not add an extra test to prop up a gate that will not
  fire.**

  This obligation exists because a gate that could not fire was found in four consecutive review rounds of this plan, and the reason is

  1. What you implemented, and any place you departed from the plan **with the reason** — a departure argued from source is welcome, a silent
  one is not.
  2. `pnpm gates` — the command you ran and its exact outcome.
  3. **The RED-when table: every mutation you drove, and for each, whether the assertion moved.** By acceptance number.
  4. Anything you found in the plan that is wrong against the source you read. Four review rounds went into this artifact and it is still
  capable of being wrong; if you find it, say so.
  5. The files you changed.

  Your report is read as self-verification evidence, and self-verification is not approval — an independent reviewer sees your work next.
  Write it so someone who did not watch you work can check you.

  ## Output contract

  Write your full report to `/Users/kein/Documents/workspace/dev/descvi/repo/phase-47-drag-reorder-in-kein/.agents/kein/reports/260828-221858-
  executor.md` before finishing: what you changed, what you verified and how, and what remains.
  Then report completion with `--report-path /Users/kein/Documents/workspace/dev/descvi/repo/phase-47-drag-reorder-in-kein/.agents/kein/
  reports/260828-221858-executor.md`.
  The file is the deliverable; the completion body is a summary of it.


• 지정된 S47-1 범위만 구현하겠습니다. 먼저 필수 작업 지침·승인 계획·관련 메모리를 확인하고, RED-when 변이 검증까지 포함해 보고서를 남기겠습니
  다.

• Ran pwd && rg -n -i -- 'phase-47|reorder|eligibility|S47-1|DR47-7|DR47-11' /Users/kein/.codex/memories/MEMORY.md || true && sed -n '1,240p'
  │ AGENTS.md && sed -n '1,260p' docs/prompt/worker-brief.md
  └ /Users/kein/Documents/workspace/dev/descvi/repo/phase-47-drag-reorder-in-kein
    100:scope: inspect and bounded-smoke-test the `plugin/libexec/ocs-team` bridge without changing source; use when validating role
    … +102 lines (ctrl + t to view transcript)
    printed text reaches nobody. If your brief tells you to send to another agent and you have no `SendMessage` tool, load it with
    `ToolSearch("select:SendMessage")`.