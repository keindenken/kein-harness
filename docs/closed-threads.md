# Closed threads

Items moved out of `docs/open-threads.md` once closed, kept verbatim with a note on what closed them.

## The `research` skill was abandoned mid-build — closed 2026-08-29

Closed 2026-08-29: the skill was written, at `plugin/skills/research/`, from the design at `docs/project/research-skill/notes.md`.

Started, then displaced by the `plan` measurement programme, and the reason for the switch was no longer remembered by anyone involved. Nothing was written down at the time.

Written, at `plugin/skills/research/`. The design it was written from is `docs/project/research-skill/notes.md`, which is where the reasoning lives; the skill carries only what a run reads.

It has never been run. What the first run has to answer is in the memo's own terms: whether the audit actually separates a blind spot from a reachability failure, whether the artifact's round section is enough to resume from — which is the falsifying condition for shipping it without a ledger — and whether all three lanes fire.

## `docs/prompt-revision.md` is documentation that wants to be a prompt

Closed 2026-08-15: the file moved into `docs/project/prompt-edit-rules/` (commit 9d2e454, with the drafts and distillation that produced it), and the rules it wanted invocable now live in the `deliberate` skill and in `plugin/prompts/standing-prompt.md`.

It describes how a prompt is revised — what evidence a change needs, what counts as deletion evidence — and it is currently prose nobody executes. The measurement programme has been generating exactly the evidence it asks for, so it is worth turning into something invocable rather than read.

## Development commands ship to anyone who installs the plugin — closed 2026-08-16

Closed by `dev/`. `sync-prompts`, `render-agents`, `check-prompts` and `eval` answer to `dev/kein-dev`, and the runner and its cases sit at `dev/eval/`. Nothing under `plugin/` builds the harness any more, so an install carries only what running it needs.

The naming collision that had stalled it was measured against the wrong case. It was `omc team` beside `/oh-my-claudecode:team` — a command and a skill answering to the same word — and no skill is planned for any of these four. `kein-dev` reuses the harness name and collides with nothing.

What the split actually needed was not a folder move. `ocs ask` and `ocs team` called the drift gate as a development command, so the two audiences were coupled by a call path and not only by a directory; that came apart first, into `plugin/libexec/lib/prompt-freshness.sh`. The move was the easy half.

## Bridge prompt layering

Closed 2026-09-26: both `plugin/skills/execute/references/lanes.md` and `plugin/skills/ralplan/references/lanes.md` already say `ocs ask` does not inject repository instructions, by design, and that the caller assembles the package's repository-instructions half itself. The gap this section asked about is answered by that design.

None of the fourteen canonical prompts reference `AGENTS.md` or `CLAUDE.md`. That is correct inside a workflow that injects repository context into the brief, and a gap on a bare one-shot call: a bridge call needs role prompt plus repository instructions plus task brief, and only the first is assembled for it. Unresolved: whether Codex and Claude inject repository instructions into a subagent automatically, which decides whether the gap is real or already covered.

## `plan`'s pre-mortem gate is unchecked — the reading was wrong, closed 2026-08-20

Recorded as an internal inconsistency: output required, verification absent. Two real plans say otherwise.

The instruction is conditional — "for deliberate high-risk planning" — and nothing in `plan/SKILL.md` sets that mode, so the first guess was that it never fires. It fires. The e3-v3 planning round produced `## 9. Pre-mortem — three credible ways this ships wrong` under this harness, and the incumbent produced `## 7. Pre-mortem` on the same subject, independently.

Nor is it ceremonial. Each scenario binds itself to a check — which acceptance criterion catches it, which mechanism prevents it, what residual is accepted because nothing does — and the incumbent's plan cites a scenario by identifier from a measurement table row (`G43-7, pre-mortem S2`), so the section is load-bearing on the rest of the document. One scenario carries its own correction: an earlier round had credited the shared type with preventing a divergence, "which inverted the discriminant's whole purpose". That correction came from a review lane. The element is being evaluated; what is absent is a *rubric naming it*, which is not the same thing.

So the fix is not the missing rubric. Adding six named dimensions to a Critic lane that blocked sixteen times on real defects without them is adding verification material to something already verified, against exactly the lens `purpose.md` sets.

What was actually missing is a place to put it. `plan-template.md` named Status, Status reason, Open Questions and Evidence Gates, and left the pre-mortem to the free-form body — so two harnesses invented their own section numbering for an element both reliably produce. It now has an optional exact shape there, beside Evidence Gates, with the decision about *whether* to write one left where it was: Planner's role contract.

The wider observation this came from still stands and is not closed. `docs/prompt-porting-notes.md` files it under "Where the reduction went too far" with three siblings, and one of those is worse than this ever was: `tracer` still says to rank by evidence strength while the six-tier scale that defined the ranking was deleted, which makes the instruction unexecutable rather than merely unnamed.

## Extracting the canonical prompt library from `~/.codex-orca` — closed 2026-08-29

The library is vendor-neutral but lived inside a lead-tuned Codex home. `ocs ask` ran the provider against the vanilla home while reading prompts from the tuned one, which was the first sign that the location is incidental rather than meaningful.

The gate used to be "when a second consumer needs it without the Codex home present". By `9ec1616` the consumers were already free of it and only the build side was left — `kein-dev sync-prompts` could not run without that home — so what remained was where canonical *lives*, not whether running the harness requires it.

Moved to `agents/` and `agents.json` at the repository root, and `sync-prompts` deleted along with the home it copied from. The render target is an argument rather than a constant, which is how a second vendor's harness gets one.

Two things came off with it, and both are the same observation: **a hash answers "has this moved" only where the source is out of reach.**

`plugin/prompts/` is gone. Its bodies were byte-identical to `plugin/agents/` for as long as both existed — the difference was six or seven lines of Claude frontmatter — so `ocs ask` and `ocs team` now strip that block at dispatch instead. What the frontmatter cannot give back is what it was translated *from*, so `agents.json` renders alongside and keeps carrying `tier` and `sandbox_mode`.

`canonical.sha256` and `libexec/lib/prompt-freshness.sh` are gone, and with them the freshness gate every dispatch paid for. Three questions collapsed into one — does `plugin/agents/` equal what the renderer produces — which `kein-dev check-agents` answers by re-rendering and diffing. The gate did buy one thing the diff does not: a refusal *before* inference was spent on a hand-edited role. That was weak on inspection. A hand-edited prompt answers as the role its editor wanted; the real loss is the next render silently discarding that edit, which the gate did not prevent and `git status` already shows.

What this does not settle is whether the two vendors should ever hold different *wordings* of one role. `purpose.md` permits it where a model's temperament calls for it, and the render has never used it: fourteen bodies, byte-identical, across every commit. The place to put such a difference now exists — the renderer splits per target — so it can wait for one observed instance rather than a layer built in advance.

## Two Claude Code skill-surface features the skills do not use — closed 2026-08-29

Closed 2026-08-29: `argument-hint` was added to every skill that takes arguments meaningfully, as the section itself records. `` !`command` `` was also tried, starting with `plugin/skills/execute/SKILL.md` at commit `217c517` (2026-08-28), and now runs the same way — showing operator state before the body reads it — in `plugin/skills/execute/SKILL.md`, `plugin/skills/ralplan/SKILL.md`, and `plugin/skills/fsd/SKILL.md`. Both halves this section left open are closed.

`argument-hint` and `` !`command` `` are both available to plugin skills — the frontmatter reference is explicit that Claude Code skills at any level, plugin skills included, get every field, and the restriction to six fields applies only to claude.ai uploads, the Skills API, and `package_skill.py`. So no probe is needed before using them; what was undecided was only whether they should be used — settled below for `argument-hint`, still open for `` !`command` ``.

`argument-hint` is a pure autocomplete affordance and carries no portability cost: a Codex port cannot render it and loses nothing by not rendering it, which is the kind of platform-forced difference `purpose.md` already permits.

Closed 2026-08-29: every skill under `plugin/skills/` whose invocation meaningfully takes arguments now carries one. `onboard` already had it; `handoff` already had one too, in its own question-style wording, left as is. `execute`, `ralplan`, `plan`, `interview`, and `deliberate` got theirs new, each describing the argument the skill's own body already documents rather than an invented flag — a plan path or task brief for `execute`, the vendor flags `lanes.md` already names for `execute` and `ralplan`, and a free-form brief for `plan` and `interview`. `ping` takes nothing and was left alone.

`` !`command` `` is different, and the difference is the whole question. It runs before the skill body reaches the model and substitutes the output, so the intended uses are: show the operator the current state, stop the run when that state is wrong, make the state check itself the point, and pre-run a `--help` the body would otherwise ask an agent to run. All four are useful and all four are Claude-only. **A skill whose instructions depend on the injected output has no Codex shape**, and two vendors doing the same work in two different shapes is the failure `purpose.md` names. The rule that falls out: inject what a reader is glad to have, never what the body then refers to.

`` !`command` `` has not been tried. `plugin/skills/ping/SKILL.md` is a one-line skill whose whole job is confirming the harness loaded, so it is still the cheapest place to see it render.

## `ocs team` cannot be exercised without spending a session — closed 2026-08-28

Every precondition it owns — the prompt library's freshness, the role roster, the trust record, Orca's reachability, the `developer_instructions` probe — runs before anything is created, and then the command immediately creates a terminal and starts a worker. There is no way to check that the preconditions pass for a given invocation without also launching one.

Found by launching one accidentally while testing `--worktree`: the lane attached to no dispatch, left an idle provider terminal in an unrelated repository, and created a run directory there that had to be removed by hand. Nothing was damaged, and nothing in the command's design prevented it.

A `--check` that stops after the last precondition and exits would make the command testable. It is small and the ordering it needs already exists.

Shipped, and used. The first real dispatch ran `--check` before launching and read `preconditions pass. No worktree, no Orca run, no worker.`

Exercising it found the next thing. That sentence read as an occupancy report and was a spend report — the command's own comment says what a check promises is *that nothing was spent*, not that nothing is running. A live worker holding the worktree was invisible to it, and nothing else looked either: `ocs state execute check-worktree` finds an occupying run, not an occupying worker. The run that closed this thread dispatched a second Executor while the first still held its terminal, which is the guarantee `execute`'s lanes.md claims for the serial ledger and enforced only at the flag that names one vendor.

Both halves are fixed. `ocs team` now reads the dispatch every prior lane in the same worktree recorded, asks Orca whether it has settled, and refuses while one has not; `--check` answers that question too and says so. A dispatch settles when its terminal dies — verified against both of that run's, once they were killed — so a stale record cannot lock the worktree, and an id Orca cannot resolve is treated as purged rather than as a worker.

## `ocs ask` takes its task through argv, and a lane package does not fit there — closed 2026-08-28

`ocs-ask` builds the task by joining positional arguments — `task="$task $1"` — and `--help` says `<task...>`. There is no file argument and no stdin path, so the whole review package has to arrive as one shell word.

Measured on the phase-47 kein run, 2026-08-27, the first time a `--critic codex` lane has actually been dispatched. The package was 646 lines. The lead wrote a wrapper script to get it through:

```sh
exec ocs ask codex --agent critic --trace "$(cat "$RUN/round1-critic-codex-package.md")"
```

That works — `ARG_MAX` on macOS is large enough — and it is an invention, not something `lanes.md` describes. `lanes.md` shows `ocs ask codex --agent <role> --trace "<the lane package>"`, which reads as an inline string and is the shape a 646-line document cannot take.

descvi's own `2plan` already learned this and wrote it down: *"Write the brief to a file and point codex at it; its runtime reads only `AGENTS.md`, so the brief is the only channel that reaches it."* That lesson cannot be ported into `lanes.md` as prose, because `ocs ask` has nothing to point at a file with. The fix is a `--task-file <path>`, or reading stdin when no positional task is given, and then `lanes.md` documents the file form instead of the inline one.

Not changed during the run. The lead had a working method and the phase-47 instrument was already carrying three changes made mid-run; a fourth would have cost more than the documentation gap did.

Closed after that run ended. `--task-file <path>` on both `ocs ask` and `ocs team`, with `-` for standard input, refusing a positional task alongside it. Both `lanes.md` files show the file form instead of the inline one. The lesson `2plan` had already written down is now portable, because there is something to point at a file with.

## The `ocs ask` argv limit and the run-directory mint were the same shape

Closed 2026-08-28: the `ocs ask` half closed with `--task-file` (see above, commit `a2bd619`); the mint half had already closed with `start` and `checkpoint` taking `--run-root` and `--slug`.

The mint half is fixed. `start` and `checkpoint` now take `--run-root` with `--slug` and name `<run-root>/<YYMMDD-HHMMSS>-<slug>/` themselves. What is left is the `ocs ask` half, above.

Recorded here because the diagnosis generalises. Both were the harness asking a lead to assemble something in the shell that the harness could assemble itself, and in both cases the shell turned out to be the wrong place: a compound command is refused outright by a worktree-isolated session, and a 646-line argument is a shape a document does not take. Anything else that reads as "compute this and pass it in" is worth checking against that pair.

## A vendor lane cannot be isolated from the operator's home, and the flags that look like they do are inert

Superseded 2026-09-26 by "A Codex lane's vanilla state should come from its launch command, not a separate home" (below). Its claim that both bridges pass `-c 'plugins."<name>".enabled=false'` no longer holds; see the comment at the top of `plugin/libexec/lib/vendor-home.sh`, which now uses `codex_vanilla_args` and `--disable plugins` instead.

`ocs ask` and `ocs team` pin `KEIN_CODEX_HOME`, and without it the operator's own `~/.codex`. A home is pinned for its auth and carries more: the skills its installed plugins publish reach the worker's prompt, and so do its `AGENTS.md` and its memories.

Both bridges pass `-c 'plugins."<name>".enabled=false'` for every plugin the home registers. It does nothing. Measured 2026-08-29 with `codex debug prompt-input`, which renders the model-visible prompt: disabling `visualize@openai-bundled`, a plugin that is loaded and listed, leaves the prompt byte-identical at 12015 bytes with `visualize` still in its skill list. The override parses and has no effect on this version.

Kept rather than removed, on the owner's call: it costs a dozen flags on a launch line and would begin working if a later version honours the key. `KEIN_CODEX_PLUGINS=inherit` stops passing them. `lanes.md` no longer claims the suppression, because a lead cannot act on a mechanism that does not fire.

What would work is a home of the run's own, and that is the open half. (2026-09-26: no longer needed. `--disable plugins` does what the per-plugin key did not, and the launch-flag route is closed below under "A Codex lane's vanilla state should come from its launch command".) The vendor's auth lives where its home does, so a separate home has to be given credentials before it will run — copied, symlinked, or provisioned — and that is a decision about credential handling rather than a shape this repository can pick on its own.

One correction to the incident that started this. The `superpowers` procedure the first cross-vendor Executor cited as authority for not waiting on approval was never in its prompt: `config.toml` registers those skills under 6.2.0 and the disk holds 6.3.0, so none of them loaded, and the home's memories do not mention them. It read them off disk or asserted them without a source. No loaded plugin was speaking, which means suppressing plugins would not have prevented it even if the flags worked.

## The lead prompt reaches a session only through a launcher Orca does not use — closed 2026-09-23

`prompts/lead.md` reached a session through `~/.local/bin/claude-kein`, which ran `claude --append-system-prompt-file` on it and unset `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`. Orca restarts a session with the command its settings name (`claude --dangerously-skip-permissions ...`), so getting the lead prompt into an Orca session meant closing the pane, relaunching with `claude-kein` and `/resume`-ing. By then the launcher was also broken: its default path pointed at the hub's `prompts/`, which no longer exists.

Moved to a plugin SessionStart hook, `plugin/hooks/lead-prompt.py`, with the prompt at `plugin/prompts/lead.md`. Why each objection to a hook turned out not to apply, all measured on Claude Code 2.1.280 (findings `260923-sessionstart-reaches-only-interactive-main-session.md`):

- Subagents: SessionStart does not fire for them. A subagent fires SubagentStart, with `agent_id` and `agent_type`, so no git-guard-style inversion is needed.
- Headless `claude -p`: SessionStart does fire, but `CLAUDE_CODE_ENTRYPOINT` is `sdk-cli` there and `cli` in an interactive session. The hook injects only on `cli`, so a script's `claude -p`, a future Codex harness calling a Claude reviewer, and every eval arm stay bare. That makes per-project scoping unnecessary: eval arms are `claude -p` (`dev/eval/run.py` `launch_command`), and `--lead-prompt` still appends the prompt on purpose.
- Clear, compact and resume each fire SessionStart again, and the hook re-injects every time. After resume the prompt is in the transcript twice.
- Agent teams: a hook cannot unset the variable. This Orca launch (1.4.207) did not set it, so the hook only shows the user a notice when the variable is on. The launcher's comment said Orca sets it itself, which is not true on this path.

Still open: an interactive Claude worker that Orca orchestration launches in its own pane would be `cli` too and would get the lead prompt. No flow launches one today, since `ocs team` starts Codex, and what tells such a worker apart is unmeasured. `~/.local/bin/claude-kein` sits outside the repository and is the owner's to delete.

## A Codex lane's vanilla state should come from its launch command, not a separate home — closed 2026-09-26

Done as the owner proposed: both bridges launch with `codex_vanilla_args` (`plugin/libexec/lib/vendor-home.sh`), which turns off plugins, apps, every MCP server the home declares, memories and the notifier, each measured against an empty `CODEX_HOME` on codex-cli 0.156.1. The comment there holds the measurements; `dev/kein-dev check-codex-vanilla` re-checks the plugin, app and MCP half. The largest finding was not memories: a read-only `ocs ask` lane had the operator's `filesystem` MCP server over all of `$HOME`, which runs outside the sandbox.

Two things still reach a lane. `hooks.json` stays on purpose, since Orca reads a worker's state through it. The home `AGENTS.md` stays because no config key separates it from the repository's; it is the operator's writing rules and does no harm today, but it is the one piece of the home a lane cannot shed.

On the memories contradiction noted above: the owner found the `superpowers` references and the Korean in the memory folder and cleared it, which is why the folder on 2026-09-26 mentions neither. The 2026-08-29 note above found no mention in the folder at that time. Memories do reach a lane when on (it quoted the summary), and the folder still holds summaries of other runs and a skill memories wrote.
