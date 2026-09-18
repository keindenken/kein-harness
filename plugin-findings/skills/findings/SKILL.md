---
name: findings
description: Use before answering, deciding, or designing on a belief about how an agent runtime behaves — Claude Code, Codex, Orca, subagents, skills, hooks, sandboxes, headless runs — because it may already be measured. Also use to record a new measurement.
---

# Findings

A finding is something that was run and observed about an agent runtime, kept so the next session does not re-derive it or, worse, assume it. Your training describes these runtimes as they were; a finding describes one as it was measured, pinned to a version.

## Look one up

1. Run `findings list`. If the command is missing, exits 3, or prints nothing, there is nothing recorded: carry on with the task and do not mention findings.
2. Each line is `<file>\t<measured>\t<status>\t<claim>`. Pick the files whose claim bears on what you are about to rely on, and read only those, from `$(findings where)`.
3. When a finding shapes your answer, name the file and its `versions`.
4. A finding is evidence for the version it names. If the runtime in front of you differs, or `versions` is `unrecorded`, treat the claim as unconfirmed; when your conclusion rests on it, say so and offer to rerun its `reproduce`.

Read nothing else from the directory `findings where` sits in. Only the findings root is written for an agent to read.

## Record one

Record only what was run and observed. A preference, a correction, or the state of ongoing work is not a finding and belongs in memory or the project's own state.

Write `$(findings where)/YYMMDD-<slug>.md`. If `where` exits 3 there is no root; tell the user rather than creating one.

```markdown
---
claim: <what was measured, one sentence, at most 200 characters>
measured: YYYY-MM-DD
versions: <tool version; tool version> | unrecorded
reproduce: <the command to rerun, or the section of this file that describes it> | unrecorded
status: current
---
# <title>

<what was asked, what was run, what came back>
```

`measured` matches the date in the file name. `project: <repository>` may be added. No other keys: `findings check` rejects them, and that refusal is what keeps the store from growing an index or a taxonomy.

When a new finding overturns an old one, set the old file's `status: superseded` and `superseded_by: <new file name>`; never delete it. `disputed` marks a claim that two measurements disagree on.

Run `findings check` until it exits 0. If the root is inside a git work tree, commit the new file there. Report the path, not the content.
