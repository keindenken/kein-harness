---
name: findings
description: Use before answering, deciding, or designing on a belief about how an agent runtime behaves — Claude Code, Codex, Orca, subagents, skills, hooks, sandboxes, headless runs — because it may already be recorded. Also use to record one.
---

# Findings

A finding is something that was run and observed about an agent runtime, kept so the next session does not have to re-derive it.

## Look one up

1. Run `findings list`. If the command is missing, exits 3, prints nothing, or prints nothing that bears on your question, carry on as if you had not looked. An empty result says nothing about the runtime, so it does not belong in your answer.
2. Each line is `<file>\t<measured>\t<status>\t<claim>`. Pick the files whose claim bears on what you are about to rely on, and read only those, from `$(findings where)`.
3. When a finding shapes your answer, name the file and its `versions`.
4. A finding is evidence for the version it names. If the runtime in front of you differs, or `versions` is `unrecorded`, treat the claim as unconfirmed; when your conclusion rests on it, say so and offer to rerun its `reproduce`.

Read nothing else from the directory `findings where` sits in. Only the findings root is written for an agent to read.

## Record one

To record a new measurement, read [record.md](references/record.md) first and follow it.
