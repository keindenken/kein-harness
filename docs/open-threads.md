# Open threads

Work that is parked rather than finished, with enough context to pick it up cold. Skill-specific items live beside the skill: `docs/skills/plan/open.md`, `docs/skills/ralplan/open.md` and `docs/skills/execute/open.md` are the ones that exist.

## The `research` skill was abandoned mid-build

Started, then displaced by the `plan` measurement programme, and the reason for the switch is no longer remembered by anyone involved. Nothing was written down at the time. Whatever exists of it is in the git history around `260810`; start by reading that rather than by starting again.

## `docs/prompt-revision.md` is documentation that wants to be a prompt

It describes how a prompt is revised — what evidence a change needs, what counts as deletion evidence — and it is currently prose nobody executes. The measurement programme has been generating exactly the evidence it asks for, so it is worth turning into something invocable rather than read.

## Development commands ship to anyone who installs the plugin — closed 2026-08-16

Closed by `dev/`. `sync-prompts`, `render-agents`, `check-prompts` and `eval` answer to `dev/kein-dev`, and the runner and its cases sit at `dev/eval/`. Nothing under `plugin/` builds the harness any more, so an install carries only what running it needs.

The naming collision that had stalled it was measured against the wrong case. It was `omc team` beside `/oh-my-claudecode:team` — a command and a skill answering to the same word — and no skill is planned for any of these four. `kein-dev` reuses the harness name and collides with nothing.

What the split actually needed was not a folder move. `ocs ask` and `ocs team` called the drift gate as a development command, so the two audiences were coupled by a call path and not only by a directory; that came apart first, into `plugin/libexec/lib/prompt-freshness.sh`. The move was the easy half.

## Bridge prompt layering

None of the fourteen canonical prompts reference `AGENTS.md` or `CLAUDE.md`. That is correct inside a workflow that injects repository context into the brief, and a gap on a bare one-shot call: a bridge call needs role prompt plus repository instructions plus task brief, and only the first is assembled for it. Unresolved: whether Codex and Claude inject repository instructions into a subagent automatically, which decides whether the gap is real or already covered.

## How far to cut `execute`'s verification rounds

The obsolescence argument says fewer. The invariant that a gate must be able to go RED says a round without a failable gate is the one to cut, not rounds in general. Resolve by measurement on a real round rather than in advance.

## `plan`'s pre-mortem gate is unchecked

The Planner is instructed to produce a pre-mortem and nothing verifies that it did. Output required, verification absent. This is a defect regardless of the obsolescence argument, because it is an internal inconsistency rather than a rule that has gone stale.

## Extracting the canonical prompt library from `~/.codex-orca`

The library is vendor-neutral but lives inside a lead-tuned Codex home. `ocs ask` runs the provider against the vanilla home while reading prompts from the tuned one, which was the first sign that the location is incidental rather than meaningful.

The gate used to be "when a second consumer needs it without the Codex home present", and that has partly arrived. As of `9ec1616` a dispatch no longer touches the Codex home at all: `ocs ask` and `ocs team` check freshness against `prompts/` and its recorded hashes, and only `kein-dev check-prompts` compares against canonical. So the consumers are already free of it and the remaining dependency is the build side — `kein-dev sync-prompts` cannot run without it. Restate the gate against that before acting: what is left is where canonical *lives*, not whether running the harness requires it.

## The ported skills have never been read against `standing-prompt.md`

Every skill except `plan` arrived from `~/.codex-orca` rather than being written here, and the rules for editing a standing prompt were written afterwards. `~/Documents/wiki/_rules/standing-prompt.md` lists `**/SKILL.md` and `**/prompts/**/*.md` in its own `paths:`, so it already claims these files; nothing has been read against it.

Its eight rules are not stylistic. Four of them delete text rather than reword it: a line that binds nothing, a restatement of what the repository already shows, an enumeration where a principle would cover the unforeseen case, and a number that is neither regenerable nor version-anchored. A fifth moves text out — provenance belongs in the commit that makes the change, not beside the rule.

Two findings from 2026-08-19 are what makes this worth a pass rather than a habit. `execute`'s serial-ledger sentence was read as forbidding the thing it permits, which is a "point at the collision" failure — the sentence carries a permission and a prohibition in one line and settles neither. And `ralplan` required a `Status reason` naming why approval is absent while its own review contract forbade a fresh lane from receiving exactly that, which is a collision between two files that nothing named.

Do it as a pass over one skill at a time with the rules open, not as a sweep. The measurement programme exists to catch what a rewrite breaks, and `plan` is the only skill it currently covers.
