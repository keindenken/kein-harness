---
name: fsd
description: Carry work from an idea, approved requirements, or an approved plan to an audited change, asking the user nothing after the interview's approval; every decision it could not take safely arrives in one final report.
argument-hint: "<idea | requirements path | plan path | Q1=<answer> ...>"
disable-model-invocation: true
hooks:
  Stop:
    - hooks:
        - type: command
          command: 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/fsd/scripts/hook.py" stop'
  PreToolUse:
    - matcher: "Write|Edit|MultiEdit|NotebookEdit"
      hooks:
        - type: command
          command: 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/fsd/scripts/hook.py" pre-write'
  PostToolUse:
    - matcher: "Skill"
      hooks:
        - type: command
          command: 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/fsd/scripts/hook.py" post-skill'
    - matcher: "Bash"
      hooks:
        - type: command
          command: 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/fsd/scripts/hook.py" post-bash'
---

# FSD

The user takes part once, at the front, in the interview and its approval, and once at the end, in the report. Between the two, this flow runs the stages that already exist, `interview` → `ralplan` → `execute`, adds a closeout, and asks nothing. `ocs state fsd` records where the run stands. The hooks this skill arms catch a stage transition that was announced but not taken, and link each stage's run to the flow when it is created.

## At entry

- `command -v ocs` → !`command -v ocs || echo "NOTHING ON PATH — no state command will run"`
- `ocs state-dir runs/fsd` → !`ocs state-dir runs/fsd 2>&1`

## References

- Read [decision-policy.md](references/decision-policy.md) before taking or leaving any decision after the interview's approval, and when `ralplan` reaches its diagnostic trigger.
- Read [closeout.md](references/closeout.md) when `execute`'s last plan task is accepted.
- Read [state-schema.md](references/state-schema.md) only when a command's output does not say enough to act on.

## Entry

1. Run `ocs state fsd start --run-root <runs/fsd> --slug <slug> --input <the argument>`. It classifies the input: an idea starts at `interview`, approved requirements at `ralplan`, an approved plan at `execute`. Stages before the entry are skipped rather than repeated.
2. If `start` refuses because a run for this worktree is still open, it names that run. When the run is paused and the arguments answer its questions (`Q1=<answer>`), record each with `ocs state fsd answer <state> Q1 --text <answer>`, then run `ocs state fsd resume <state>`. Otherwise read `ocs state fsd status <state>` and continue from where it stands.
3. Invoke the stage `ocs state fsd gap <state>` names.

## After the interview, ask nothing

Once the interview's requirements are approved, do not ask the user anything until the final report. This outranks `ralplan`'s "Ask the user immediately" and `execute`'s "ask the one question that would unblock it". A decision either of them would have asked is taken as an assumption or parked as a question, as [decision-policy.md](references/decision-policy.md) directs, and the report carries both. Nobody is watching the run: a question asked mid-run waits until the user comes back, and everything after it waits with it.

## Between stages

A stage ending is not a place to stop. When the interview's requirements are approved, when `ralplan` approves, when `execute` completes, invoke the next stage in the same turn. `ocs state fsd gap` names it.

If `execute` aborts, `gap` names nothing, by design. Decide whether to restart it or give it up; to give it up, run `ocs state fsd closeout <state>`, and closeout ends in `halt`.

`interview`'s "stops without a downstream handoff" and `ralplan`'s "grants no execution authority" end those skills, not this flow. This flow is the authority that carries the work on. An approval or a receipt is a checkpoint inside the run, not a moment to summarise and wait for acknowledgement.

## What the hooks need from you

The hooks read the Bash commands you run and their output, so they see only what you do:

- Pass `--input <the approved requirements path>` to `ocs state ralplan start`. Give `ocs state execute start` an absolute `--input`, or one relative to the repository root.
- Validate the interview ledger with `ocs validate interview ledger <path>` while the ledger is still active.
- Run `ocs state ralplan start`, `ocs state execute start` and `ocs validate interview ledger` each as its own Bash call, with the path written out literally.
- Run `ocs state execute dispatch <state> <task>` before starting that task's executor.

When `status` shows a stage with no association, its `association_reason` names the command that would have linked it. `ocs state fsd attach <state> <stage> <run>` links a run of this flow that is still live.

When a hook blocks, its reason names one command. Run that command.

## After compaction

Run `ocs state fsd status <state>` and the current stage's own `reconcile` before acting. The state records where the run is; the transcript does not.

## Finishing

Follow [closeout.md](references/closeout.md). The last message of the run is `ocs state fsd report <state>` printed verbatim, whatever the outcome: completed, paused on a question, or halted.

The hooks stop acting while `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/kein/fsd/hooks-off` exists.
