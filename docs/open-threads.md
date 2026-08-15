# Open threads

Work that is parked rather than finished, with enough context to pick it up cold. Skill-specific items live beside the skill — `docs/skills/plan/open.md` is the one that exists.

## The `research` skill was abandoned mid-build

Started, then displaced by the `plan` measurement programme, and the reason for the switch is no longer remembered by anyone involved. Nothing was written down at the time. Whatever exists of it is in the git history around `260810`; start by reading that rather than by starting again.

## `docs/prompt-revision.md` is documentation that wants to be a prompt

It describes how a prompt is revised — what evidence a change needs, what counts as deletion evidence — and it is currently prose nobody executes. The measurement programme has been generating exactly the evidence it asks for, so it is worth turning into something invocable rather than read.

## Development commands ship to anyone who installs the plugin — closed 2026-08-16

Closed by `dev/`. `sync-prompts`, `render-agents`, `check-prompts` and `eval` answer to `dev/kein-dev`, and the runner and its cases sit at `dev/eval/`. Nothing under `plugin/` builds the harness any more, so an install carries only what running it needs.

The naming collision that had stalled it was measured against the wrong case. It was `omc team` beside `/oh-my-claudecode:team` — a command and a skill answering to the same word — and no skill is planned for any of these four. `kein-dev` reuses the harness name and collides with nothing.

What the split actually needed was not a folder move. `ocs ask` and `ocs team` called the drift gate as a development command, so the two audiences were coupled by a call path and not only by a directory; that came apart first, into `plugin/libexec/lib/prompt-freshness.sh`. The move was the easy half.
