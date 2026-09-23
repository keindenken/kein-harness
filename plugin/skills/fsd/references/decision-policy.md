# Decisions after the interview

Every decision the run takes on the user's behalf must be answerable later from one place: an assumption or a question in the fsd state, each carried into the report and the retrospective. A decision that leaves no record there has been taken without the user and hidden from them.

## Reversible or not

A decision **parks** when undoing it after the run takes more than discarding or reverting the run's own worktree changes. It parks when it:

1. sets a schema or persisted format for data that lives outside the worktree, or that already-deployed code reads;
2. changes a public interface whose consumers are outside the change: exported names, CLI flags, config keys, file formats, network APIs;
3. deletes or irrecoverably rewrites data Git cannot restore;
4. takes an externally visible action: a network write, push, publish, deploy, PR, message, account or billing change, or spending money. None of these is taken at all; each is parked as a question.

Everything else is reversible.

## Taking a reversible decision

Take the recommended option, then record it:

```sh
ocs state fsd assume <state> --stage <stage> --decision <what was open> --chosen <what you took> \
  --alternatives <others> --reversal-cost <files and tasks that would change> --where <where it landed>
```

`--reversal-cost` is what the user reads when deciding whether to veto, so name files and tasks, not effort.

## Parking an irreversible decision

Record the question, then park only what depends on it:

```sh
ocs state fsd question <state> --stage <stage> --question <the decision, as asked> --options <a,b> \
  --recommended <a> --why-irreversible <list item and reason> --parks <task ids, or 'whole run'>
ocs state execute park <execute state> <task>... --question <the same question> --ref Q<n>
```

- Park every task that depends on the decision, including ones whose scope does not touch it.
- A task already under way parks by either of `park`'s two routes: its scope restored to its content at dispatch, or its scope clean against HEAD with nothing untracked under it. `park` refuses until one of them holds, and its refusal names both.
- Tasks that do not depend on the decision go on to acceptance.
- `execute` blocked for any other reason is a question with `--parks 'whole run'`.

## What this flow never does

- **An occupying execute run.** When `gap` names an execute run that is not this flow's own, it prints that run's id, whichever of its start, last checkpoint, phase and accepted-task count it can read, and an abort command. Those facts identify the run and say how far it got; they never establish that its work is safe to discard. Read that from `git log` and `git status`: whether what the run produced is committed here, and pushed. A run whose tasks are accepted and whose work this worktree already holds, with nothing live behind it, is this worktree's own stale occupant and may be aborted, with that evidence recorded as an assumption. Never infer staleness from the start or the last checkpoint alone: an old timestamp is what a long run and an abandoned one have in common. Anything left unsettled is someone's live work, so do not run the abort -- it destroys work Git does not hold. Record a question with `--parks 'whole run'`, then run `ocs state fsd closeout <state>`.
- **AGENTS.md.** No task in the execute ledger may have AGENTS.md in its scope. A story that would edit it becomes a lesson (`ocs state fsd lesson`). If other stories need that edit to exist first, it becomes a question that names the lesson. After `execute start` and after every appended task, run `ocs state fsd guard <state>`; when it fails, do what its output says.

## When `ralplan` does not converge

`ralplan` treats about five unsuccessful rounds as a moment to reassess with the user, and says "Do not manufacture approval from repetition." Inside this flow there is no user to reassess with, so this section takes precedence at that trigger. It does not manufacture approval: every standing ground is recorded against a named catcher, and nothing irreversible is approved.

When the standing grounds keep coming from one story while the others have settled, split before the round count matters. Removing a story edits the plan, which moves the review hash, so the round under way cannot resolve over the remainder -- `approve` is refused from a moved hash, and the only way past an edited plan is another round. The split costs that round and buys back every one after it:

1. Record an assumption naming what the removal defers and what the remaining stories still cover.
2. `ocs state ralplan block <state> --findings <file>`, which is what clears the round's verdicts; `revised` does not, and a candidate that leaves `reviewing` carrying a standing verdict is refused.
3. Remove the story from the plan.
4. `ocs state ralplan revised <state>`, which moves to `drafted` and drops the findings.
5. `ocs state ralplan open <state>` with fresh lanes over the trimmed plan.

The prohibition on `block` below belongs to the round-5 exit alone, where the point is to reach `approve` without another round. Here another round is the price, so `block` is the right first step.

The split story goes back through its own requirements-and-plan pass after this run rather than holding the settled ones behind it.

That is a different situation from grounds that move across stories as each is fixed. Those are what the round count is for, and the exit below applies to them.

When an official round numbered 5 or higher resolves with a standing BLOCK:

1. Do not run `ralplan`'s `block`. `block` moves the run to `revising`, and `approve` is refused from there. A round that already ran `block` goes through `revised` and one more round, and this section applies when that round resolves.
2. Split every standing ground by the list above.
3. For each reversible ground, record an assumption. Defer the ground with `deferral.reason` saying why it does not hold for an unattended run, and `caught_by` = `fsd assumption A<n>; execute final audit`.
4. For each irreversible ground, record a question. Defer the ground with `caught_by` = `fsd question Q<n>; tasks from <stories> start parked`.
5. From that round's `reviewing` phase, run `ocs state ralplan approve <state> --findings <file>` with every standing ground deferred. The approving `Status` line's reason names every deferral and every parked story.
6. After `ocs state execute start`, park the tasks normalized from those stories, then run `ocs state fsd guard <state>`.

`ralplan` wants a deferred ground's `Caught by` in the plan's pre-mortem. Here it goes in the `Status` line, the receipt and the retrospective instead, because revising the plan moves the review hash and reopens the round, which is the loop this exit exists to break.

A ground whose correction would edit AGENTS.md follows the AGENTS.md rule above. It never becomes a task.
