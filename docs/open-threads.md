# Open threads

Work that is parked rather than finished, with enough context to pick it up cold. Skill-specific items live beside the skill — `docs/skills/plan/open.md` is the one that exists.

## The `research` skill was abandoned mid-build

Started, then displaced by the `plan` measurement programme, and the reason for the switch is no longer remembered by anyone involved. Nothing was written down at the time. Whatever exists of it is in the git history around `260810`; start by reading that rather than by starting again.

## `docs/prompt-revision.md` is documentation that wants to be a prompt

It describes how a prompt is revised — what evidence a change needs, what counts as deletion evidence — and it is currently prose nobody executes. The measurement programme has been generating exactly the evidence it asks for, so it is worth turning into something invocable rather than read.

## Development commands ship to anyone who installs the plugin

`bin/` is where a file becomes a command on the Bash tool's PATH, so `ocs` is deliberately the only entry point there, and `libexec/` holds the subcommands. That mixes two audiences: `ocs ask` and `ocs team` are for using the harness, `ocs eval` is for building it, and someone who installs the plugin has no use for the second kind.

Splitting it was raised before and set aside over a naming collision — an `omc ask` / `/oh-my-claudecode:ask` confusion that a second `kein` entry point looked likely to repeat. The counter-argument, on the table and not yet answered: there is no `/kein:eval` skill planned, and the development commands only ever run inside this repository, so the collision that made the earlier objection real may not apply here.

Moving `evals/` out of the plugin is the first half of it and is done. What remains is the commands themselves, and it is not a folder move.
