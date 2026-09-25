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

## How far to cut `execute`'s verification rounds

Closed 2026-09-26: the owner settled it with three changes instead of measuring a live round — a `REVISE` finding is fixed with no fresh lane (8f3593c for ralplan; `execute` already had this through its own fix-it route), and `--primed` and `--max-rounds` bound review cost on both skills (8f3593c ralplan, 4a41c57 execute).

The obsolescence argument says fewer. The invariant that a gate must be able to go RED says a round without a failable gate is the one to cut, not rounds in general. Resolve by measurement on a real round rather than in advance.

## The isolation check that caught a lane reaching live work no longer runs

Closed 2026-09-26: d06aa8d — each fixture arm and each `--case` replicate now records `sessions_outside` over its own config home, read before the home is retired, so `check_plumbing`'s `record["visited_outside"]` reads a real value instead of a field nothing ever wrote.

`run.py` defines `sessions_outside`, which reads the project-slug directories under a run's config home and names every working directory the run opened a session in. `check_plumbing` reports on `record["visited_outside"]`. Nothing writes that key, so the check reads a missing field, finds an empty list, and passes on every run.

It is not a hypothetical check. Its docstring records what it found the one time it ran: *"A first run left a directory for the origin fixture repository, meaning a lane had been pointed at live work rather than at its detached copy."* A lane reaching outside its arm can read, and in principle write, work that is not a fixture — and it would also invalidate the comparison silently, which is the failure mode this whole harness is built to refuse.

Reviving it is small: call `sessions_outside(config_home, [<the arm worktrees>])` where the record is assembled and store the result. The awkward part is `--case` mode, where each replicate has its own home and its own single permitted worktree, so the allowed set differs per replicate rather than per arm.

Retiring config homes at the end of a run does not block this — the slugs move to `transcripts/` intact, which is why the move preserves them rather than flattening — but it does mean a revival has to read them before the retirement or from their new home.

## A pinned `--plugin-dir` loses `ocs` when the launching shell already has one

Closed 2026-09-26: eeda04d — `ocs` now refuses to run, naming both trees, when a second kein harness tree's `ocs` is also on PATH (R8.3, amended to check PATH rather than `CLAUDE_PLUGIN_ROOT`, which the Bash tool is never given). d06aa8d strips the operator's plugin `bin/` directories from an eval arm's environment and re-appends the arm's own, so an eval arm is not itself caught by the same mix.

`--plugin-dir <path>` pins everything it should. Measured 2026-08-20 against the descvi fixture, where `enabledPlugins` has `kein@skills-dir: false`: without the flag no kein skill is invocable at all, with it the skills load, and from a clean `PATH` `ocs` resolves inside the pinned directory.

It stops being true when the launching shell already carries `~/.claude/skills/kein/bin`, which any session launched from inside a kein-loaded session does. That entry precedes the pinned one on `PATH`, so the skills come from the pinned tree and `ocs` comes from wherever the symlink points — currently `dev/kein-harness/plugin`, i.e. main. Two harness versions in one session, and nothing says so.

Harmless while the trees are identical, which they are. It bites the first time an experiment pins an older or a branch build to compare against main, since that is precisely when the two differ and precisely when the result would be attributed to the pinned tree.

No fix chosen. The cheap mitigation is to launch from a shell that has never loaded kein and check `command -v ocs` before starting; the real fix is either for the flag to prepend rather than append, which is not this repository's to make, or for `ocs` to refuse when its own path is outside `CLAUDE_PLUGIN_ROOT`.

## A default eval run does not record which harness it ran

Closed 2026-09-26: d06aa8d (R7.3) — each treatment arm, including the default with-skill/without-skill pair, now records the harness repository's resolved commit and whether the tree was dirty, beside the plugin path. `--variant` arms already named their commit. The section's own point that this unlocks dropping the plugin copy is carried forward as a live remainder in `docs/open-threads.md`, "A default eval run's plugin copy could now be dropped".

`--variant` arms record their resolved commit in the manifest, so the plugin copy each one launched under is reproducible. The default `with-skill`/`without-skill` pair records only a path: `arms_spec.with-skill.plugin` points at `<run>/plugin`, and nothing anywhere says which commit that copy came from.

That makes the copy the only record of what actually ran, which is why it is still kept — six runs on disk depend on it. It also means the six cannot be compared against a later run except by reading their plugin trees, and that a run whose copy is lost is unattributable.

The fix is one line where `prepare_plugin` is called without a `source`: resolve `HEAD` of the harness repository and put it in the manifest beside the path. `prepare_plugin` also re-renders agents onto one model, so the commit alone does not reproduce the copy — the manifest already records `model`, and the pair does.

Doing it unlocks dropping the copy, which is ~800K of a default run and ~1.4M of a `--variant` one. Not urgent on its own; worth doing next time the manifest shape is touched.

## A plan correction ends the run, and the question it forces is per-task

Closed 2026-09-26: 4a41c57 (R4) — each acceptance now records the input hash (the plan revision) it was made under, and after `amend` a task accepted under an earlier revision keeps the run from completing until a fresh, independent lane re-confirms it against the amended plan; a task that lane does not confirm returns to correcting. That answers the per-task question this section leaves open: an amendment touching the very condition a task was accepted under no longer carries that acceptance forward unexamined. `docs/skills/execute/open.md`, "A completion condition's own wording cannot be corrected inside a run", is the neighbouring, still-open question and is unaffected by this closure.

`execute` binds a run to its input by hash. `validate_transition` refuses a nonterminal transition that changes input identity, and `reconcile` answers a changed input with `block and reassess the changed input before resuming`. That is what stops a plan being swapped under a live ledger, and it is not the thing to loosen.

It collides with the repository's own rule. descvi's `AGENTS.md` requires the plan to be updated in the same change when reality forces a departure from it, and `task-ledger-template.md` blesses the smaller half of that already — a factual correction may update a task when it stays inside the authorized outcome and its rationale is recorded. So a correction that the work forces is required, and making it ends the run.

Measured on the phase-47 execute run: story one of five forced two plan corrections (acceptance 24's element-keyed reading, part 2's band removal). The run was aborted with a reason naming the one accepted task, and a second run opened carrying the remaining four. One story, one split.

The lead gave two reasons and only the first holds. The input hash is immutable within a run, which is true and decisive. The second was that task-001's acceptance was bound to a fingerprint that HEAD has since moved past, so re-asserting it would be an unmeasured claim — but that is not how acceptance is validated. `_validate_acceptance` checks each reviewer verdict against the acceptance's **own** recorded fingerprint and never against the current worktree, so an acceptance is a sealed, self-describing record and a later worktree move does not touch it. Nothing in the machine would have refused carrying task-001 forward as accepted.

What would have been wrong is subtler and is the actual thread. One of the two corrections changed acceptance 24 — the condition task-001 was accepted against. So the question is not "is this acceptance stale" but "did this correction touch what that task was accepted for", and that is a per-task question the input hash answers for the whole ledger at once. A run that corrects a plan section no accepted task depended on is split for nothing; a run that corrects the very condition a task passed under must not carry it, and today both get the same answer.

Not acted on. The cheap-looking fix — a transition that records old hash, new hash and a reason while keeping the run — moves the judgement to whoever writes the reason, which is the lead, which is the one agent in the loop no lane reviews. Worth deciding only with more than one run's evidence; the remaining four stories will produce it, since the same rule fires on every correction they force.


**State as of 2026-09-18.** The evidence came in and the cheap-looking fix shipped. The remaining phase-47 stories retired three more runs on the same rule, one of them over four amendments, and phase-48 retired two. `3841bc2` (2026-09-05) added `amend --reason`: it records `{at, reason, from, to}` in `input.amendments` and keeps the run, and the completed receipt carries them, so the reason the lead writes is at least inherited by the next reader. No lane reviews it, which was the objection above, and that objection still stands.

The per-task half is unchanged and now sharper. An amendment keeps every accepted task accepted, including one whose condition the amendment touched, where before the abort at least dropped it. The template sentence quoted above was narrowed in `30b7136`: a correction may change a task's title, verification path or rationale, never its scope or completion condition. oh-my-claudecode 5.x answers this half by binding each completion claim and approval to the criteria revision it was made under; `docs/skills/execute/open.md` records why its companion route, replacing a criterion inside the run, was not taken here.

## `ocs team` rebinds the lead's terminal to a new Run on every lane

Closed 2026-09-26: eeda04d — `ocs home-run` binds a lead's pane to a Run of its own, independent of any lane's Run. `ocs team` rebinds the lead to home as soon as its dispatch attaches, and again on exit after acking its own `worker_done` on the lane Run, so a lane no longer leaves the lead's binding on a Run that ended with the lane.

`orca orchestration run-create` binds the terminal that calls it, and Orca refuses to let one terminal act as another (`run-create --from <worker terminal>` answers `consumer_fenced`, measured 2026-09-19 on orca 1.4.205). So every `ocs team` invocation moves the lead's binding to that lane's Run. Two consequences, neither yet observed in a real run:

- A lead that is itself an Orca coordinator — bound to its own Run and waiting on `check --wait` — loses that binding the moment it starts a lane, and its own workers' messages stop reaching it until it runs `run-use` again.
- With several lanes started concurrently, only the last Run stays bound. `ocs team` consumes its own `worker_done` only while its Run is still the bound one, so an earlier lane's message stays in its inbox and may nudge the lead later. Whether Orca nudges for an unbound Run at all is unmeasured.

The Orca model is one coordinator, one Run, a whole wave inside it. Moving `ocs team` onto the lead's existing Run would fix the first, but then every lane shares one inbox with whatever else the lead coordinates, and consuming a `worker_done` there means filtering by dispatch rather than draining. Not worth doing until a lead actually coordinates an Orca Run and starts a lane from it.

Observed 2026-09-25, and not a defect after all: mail another session addressed to a lead's terminal handle landed in the Run of that lead's last `ocs team` lane. That Run is the lead's current inbox (the lead is its coordinator), so Orca nudged the lead with "You have 1 orchestration message. Run `orca orchestration check --run <lane run>`" and the lead read it. The only open part is latency: the nudge came 96 seconds after the send, and only after other input had already started a turn (findings `260925-orca-messaging-between-peer-claude-sessions.md`). Orca 1.4.207 has no verb to unbind a terminal, only `run-use` to rebind it. EnterWorktree is not a factor: the two leads made 60 `orca` calls while worktree-isolated and none was refused.

## `ralplan` and `execute`: a fix that does not need another review, and run flags — raised 2026-09-24

Closed 2026-09-26: 8f3593c (ralplan) and 4a41c57 (execute) — both review contracts now word `REVISE` as accept-and-disposition rather than revise-and-review; ralplan gained the fix-it route execute already had (`fix` after `approve`, with both the reviewed and the post-fix hash recorded and the lead reading the diff); and `--primed` and `--max-rounds <n>` ship on both skills. `--quick` was dropped rather than built — a lane told to review fast returned a review under two minutes that did not look read. `--round <n>` was folded into `--max-rounds`. The other suggestions weighed alongside — `--lanes`/`--reviewer` presets, `--dry-run`, and `--resume <run>` — were not taken.

**Fix, then approve without a re-review.** The owner wants a verdict that means "this needs correcting, but not another round" — the corrected artifact is approved without a fresh lane — as oh-my-claudecode had. The two skills are not in the same place. `execute` already has it for `REVISE`: step 7 lets a `REVISE` finding be "fixed before [acceptance] with the verification path re-run and no fresh lane". `ralplan` does not, and the reason is structural rather than a missing word: `REVISE` findings are carried into the approval unfixed, and fixing one changes the review hash, which invalidates every verdict. So the question in `ralplan` is whether some content change may be made after the last blind round without reopening it — which is exactly the drift the two hashes exist to catch — and not whether a new verdict word is needed. A `BLOCK` that the lead thinks is small still has only two exits, a revision round or a deferral.

**Invocation flags.** Wanted on both skills:

- `--primed`: a re-review does not go to a new blind lane; the previous reviewer runs the closure check only. Today a primed closure check exists in both contracts but "cannot approve", so this flag inverts a rule both review contracts state, not only a default.
- `--quick`: review runs faster. Not yet defined — fewer lanes, a lighter tier, or a shorter rubric are three different things.
- `--round <n>`: run only the n-th round.

Suggestions to weigh alongside, not yet discussed with the owner: `--max-rounds <n>` to stop at a bound and hand back `Draft` instead of re-arming the five-round trigger; `--lanes`/`--reviewer` presets such as a single-lane run; `--dry-run` that stops after the round-1 package is assembled so the package itself can be inspected (which would not have caught the `Status` leak in `docs/skills/ralplan/open.md`, since that one bypassed the package); and `--resume <run>` if resuming is not already implicit in the ledger.

## A lead that never started an `ocs team` lane cannot be nudged by mail

Closed 2026-09-26: eeda04d (R8.1, R8.2) — `ocs home-run` gives a lead a home Run from session start, through the SessionStart hook, for the interactive entrypoint, so mail sent before any `ocs team` lane is delivered and nudged. `ocs team` rebinds the lead to that home Run once a lane's dispatch attaches and again on exit, so the lead stays reachable after starting a lane too.

Measured 2026-09-25 (findings `260925-orca-messaging-between-peer-claude-sessions.md`): Orca types its "You have N orchestration message(s)" nudge into a pane about a second after mail arrives, but only when that pane is bound to a Run and has been seen idle. A busy pane gets it at its next idle, and a pane bound to no Run got none in twelve minutes. A lead is bound only as a side effect of its first `ocs team` lane, so before that, mail another session sends it just sits there.

The direction is a home Run per lead: bound once at session start, so the lead is reachable from the first minute. Where to create it is open. The SessionStart hook runs before any Orca pane identity is known to be stable, and a lane's `run-create` would still move the binding off it (Orca 1.4.207 has no unbind, only `run-use`). So `ocs team` would also have to rebind to the home Run after starting its lane, and its `worker_done` cleanup, which assumes it is bound to the lane Run, would have to change with it. The cleanup is also not stopping the late nudges it exists to stop: the two descvi leads received 40 across their lanes, often two per lane.
