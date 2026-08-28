# Open threads

Work that is parked rather than finished, with enough context to pick it up cold. Skill-specific items live beside the skill: `docs/skills/plan/open.md`, `docs/skills/ralplan/open.md` and `docs/skills/execute/open.md` are the ones that exist.

The phase-46 comparison — the two kickoff traces, the two finished plans, the seven-round run ledger, and the five threads they produced about the plan artifact — has moved to `docs/skills/ralplan/260826-phase-46-comparison.md`, in Korean, because it is one investigation rather than five parked items and the working discussion around it is Korean. Entry cost, the artifact carrying its own review history, the lead authoring its own requirements, and the Evidence Gate validator are all there.

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

## `plan`'s pre-mortem gate is unchecked — the reading was wrong, closed 2026-08-20

Recorded as an internal inconsistency: output required, verification absent. Two real plans say otherwise.

The instruction is conditional — "for deliberate high-risk planning" — and nothing in `plan/SKILL.md` sets that mode, so the first guess was that it never fires. It fires. The e3-v3 planning round produced `## 9. Pre-mortem — three credible ways this ships wrong` under this harness, and the incumbent produced `## 7. Pre-mortem` on the same subject, independently.

Nor is it ceremonial. Each scenario binds itself to a check — which acceptance criterion catches it, which mechanism prevents it, what residual is accepted because nothing does — and the incumbent's plan cites a scenario by identifier from a measurement table row (`G43-7, pre-mortem S2`), so the section is load-bearing on the rest of the document. One scenario carries its own correction: an earlier round had credited the shared type with preventing a divergence, "which inverted the discriminant's whole purpose". That correction came from a review lane. The element is being evaluated; what is absent is a *rubric naming it*, which is not the same thing.

So the fix is not the missing rubric. Adding six named dimensions to a Critic lane that blocked sixteen times on real defects without them is adding verification material to something already verified, against exactly the lens `purpose.md` sets.

What was actually missing is a place to put it. `plan-template.md` named Status, Status reason, Open Questions and Evidence Gates, and left the pre-mortem to the free-form body — so two harnesses invented their own section numbering for an element both reliably produce. It now has an optional exact shape there, beside Evidence Gates, with the decision about *whether* to write one left where it was: Planner's role contract.

The wider observation this came from still stands and is not closed. `docs/prompt-porting-notes.md` files it under "Where the reduction went too far" with three siblings, and one of those is worse than this ever was: `tracer` still says to rank by evidence strength while the six-tier scale that defined the ranking was deleted, which makes the instruction unexecutable rather than merely unnamed.

## Extracting the canonical prompt library from `~/.codex-orca`

The library is vendor-neutral but lives inside a lead-tuned Codex home. `ocs ask` runs the provider against the vanilla home while reading prompts from the tuned one, which was the first sign that the location is incidental rather than meaningful.

The gate used to be "when a second consumer needs it without the Codex home present", and that has partly arrived. As of `9ec1616` a dispatch no longer touches the Codex home at all: `ocs ask` and `ocs team` check freshness against `prompts/` and its recorded hashes, and only `kein-dev check-prompts` compares against canonical. So the consumers are already free of it and the remaining dependency is the build side — `kein-dev sync-prompts` cannot run without it. Restate the gate against that before acting: what is left is where canonical *lives*, not whether running the harness requires it.

## The ported skills have never been read against `standing-prompt.md`

Every skill except `plan` arrived from `~/.codex-orca` rather than being written here, and the rules for editing a standing prompt were written afterwards. `~/Documents/wiki/_rules/standing-prompt.md` lists `**/SKILL.md` and `**/prompts/**/*.md` in its own `paths:`, so it already claims these files; nothing has been read against it.

Its eight rules are not stylistic. Four of them delete text rather than reword it: a line that binds nothing, a restatement of what the repository already shows, an enumeration where a principle would cover the unforeseen case, and a number that is neither regenerable nor version-anchored. A fifth moves text out — provenance belongs in the commit that makes the change, not beside the rule.

Two findings from 2026-08-19 are what makes this worth a pass rather than a habit. `execute`'s serial-ledger sentence was read as forbidding the thing it permits, which is a "point at the collision" failure — the sentence carries a permission and a prohibition in one line and settles neither. And `ralplan` required a `Status reason` naming why approval is absent while its own review contract forbade a fresh lane from receiving exactly that, which is a collision between two files that nothing named.

Do it as a pass over one skill at a time with the rules open, not as a sweep. The measurement programme exists to catch what a rewrite breaks, and `plan` is the only skill it currently covers.

## Two Claude Code skill-surface features the skills do not use

`argument-hint` and `` !`command` `` are both available to plugin skills — the frontmatter reference is explicit that Claude Code skills at any level, plugin skills included, get every field, and the restriction to six fields applies only to claude.ai uploads, the Skills API, and `package_skill.py`. So no probe is needed before using them; what is undecided is whether they should be used.

`argument-hint` is a pure autocomplete affordance and carries no portability cost: a Codex port cannot render it and loses nothing by not rendering it, which is the kind of platform-forced difference `purpose.md` already permits.

`` !`command` `` is different, and the difference is the whole question. It runs before the skill body reaches the model and substitutes the output, so the intended uses are: show the operator the current state, stop the run when that state is wrong, make the state check itself the point, and pre-run a `--help` the body would otherwise ask an agent to run. All four are useful and all four are Claude-only. **A skill whose instructions depend on the injected output has no Codex shape**, and two vendors doing the same work in two different shapes is the failure `purpose.md` names. The rule that falls out: inject what a reader is glad to have, never what the body then refers to.

Neither has been tried. `plugin/skills/ping/SKILL.md` is a one-line skill whose whole job is confirming the harness loaded, so it is the cheapest place to see both render.

## `ocs team` cannot be exercised without spending a session — closed 2026-08-28

Every precondition it owns — the prompt library's freshness, the role roster, the trust record, Orca's reachability, the `developer_instructions` probe — runs before anything is created, and then the command immediately creates a terminal and starts a worker. There is no way to check that the preconditions pass for a given invocation without also launching one.

Found by launching one accidentally while testing `--worktree`: the lane attached to no dispatch, left an idle provider terminal in an unrelated repository, and created a run directory there that had to be removed by hand. Nothing was damaged, and nothing in the command's design prevented it.

A `--check` that stops after the last precondition and exits would make the command testable. It is small and the ordering it needs already exists.

Shipped, and used. The first real dispatch ran `--check` before launching and read `preconditions pass. No worktree, no Orca run, no worker.`

Exercising it found the next thing. That sentence read as an occupancy report and was a spend report — the command's own comment says what a check promises is *that nothing was spent*, not that nothing is running. A live worker holding the worktree was invisible to it, and nothing else looked either: `ocs state execute check-worktree` finds an occupying run, not an occupying worker. The run that closed this thread dispatched a second Executor while the first still held its terminal, which is the guarantee `execute`'s lanes.md claims for the serial ledger and enforced only at the flag that names one vendor.

Both halves are fixed. `ocs team` now reads the dispatch every prior lane in the same worktree recorded, asks Orca whether it has settled, and refuses while one has not; `--check` answers that question too and says so. A dispatch settles when its terminal dies — verified against both of that run's, once they were killed — so a stale record cannot lock the worktree, and an id Orca cannot resolve is treated as purged rather than as a worker.

## `tracer` ranks by a scale that was deleted

`prompts/tracer.md` step 4 says to "label provenance and rank evidence strength", and step 7 to "reject, down-rank, retain, or merge explanations only as the evidence warrants". Neither the prompt nor anything in the skill tree says what the strengths are or how a conflict between two of them resolves. `prompt-porting-notes.md` records what happened: a six-tier evidence-strength scale and its conflict rule were removed in normalization, and the instructions that consumed them were not.

Not unexecutable — a model asked to rank will rank. Undefined, which is worse in a specific way: two tracers reach different orderings from the same evidence and neither is wrong, so the ranking cannot be argued with. That is the failure the scale existed to prevent, and it leaves no trace in any single run.

Unlike `plan`'s pre-mortem, this one has no in-repo home. There is no `tracer` skill — the role is a prompt and nothing else — so a scale cannot be added beside it the way the pre-mortem's shape went into `plan-template.md`. Either the scale returns to the canonical prompt, or the two instructions stop naming a ranking they cannot define. That is a decision about canonical, which drags in the extraction thread below.

It is the sharpest of the four siblings `prompt-porting-notes.md` lists under "Where the reduction went too far", now that the pre-mortem has turned out to work without its rubric. Worth taking before the other two, and worth measuring first: whether two tracer runs on one question actually disagree about ordering is a cheap thing to find out and would settle whether this costs anything in practice.

## The isolation check that caught a lane reaching live work no longer runs

`run.py` defines `sessions_outside`, which reads the project-slug directories under a run's config home and names every working directory the run opened a session in. `check_plumbing` reports on `record["visited_outside"]`. Nothing writes that key, so the check reads a missing field, finds an empty list, and passes on every run.

It is not a hypothetical check. Its docstring records what it found the one time it ran: *"A first run left a directory for the origin fixture repository, meaning a lane had been pointed at live work rather than at its detached copy."* A lane reaching outside its arm can read, and in principle write, work that is not a fixture — and it would also invalidate the comparison silently, which is the failure mode this whole harness is built to refuse.

Reviving it is small: call `sessions_outside(config_home, [<the arm worktrees>])` where the record is assembled and store the result. The awkward part is `--case` mode, where each replicate has its own home and its own single permitted worktree, so the allowed set differs per replicate rather than per arm.

Retiring config homes at the end of a run does not block this — the slugs move to `transcripts/` intact, which is why the move preserves them rather than flattening — but it does mean a revival has to read them before the retirement or from their new home.

## A pinned `--plugin-dir` loses `ocs` when the launching shell already has one

`--plugin-dir <path>` pins everything it should. Measured 2026-08-20 against the descvi fixture, where `enabledPlugins` has `kein@skills-dir: false`: without the flag no kein skill is invocable at all, with it the skills load, and from a clean `PATH` `ocs` resolves inside the pinned directory.

It stops being true when the launching shell already carries `~/.claude/skills/kein/bin`, which any session launched from inside a kein-loaded session does. That entry precedes the pinned one on `PATH`, so the skills come from the pinned tree and `ocs` comes from wherever the symlink points — currently `dev/kein-harness/plugin`, i.e. main. Two harness versions in one session, and nothing says so.

Harmless while the trees are identical, which they are. It bites the first time an experiment pins an older or a branch build to compare against main, since that is precisely when the two differ and precisely when the result would be attributed to the pinned tree.

No fix chosen. The cheap mitigation is to launch from a shell that has never loaded kein and check `command -v ocs` before starting; the real fix is either for the flag to prepend rather than append, which is not this repository's to make, or for `ocs` to refuse when its own path is outside `CLAUDE_PLUGIN_ROOT`.

## The lead prompt can now be an arm's, and no run has used it yet

`kein-dev eval --lead-prompt <path>` appends a standing lead prompt to every arm, which is what a launcher does in real use and what no measured run has ever done. It defaults to `none`, so nothing about the twelve runs on disk changed; the manifest records which side a run was on.

Two measurements it makes possible, neither taken:

`where-justification-lives.md` closes on "No `ocs eval` comparison of `kickoff.md` vs `lead.md` exists" — the rewrite that cut 56% of the words was never measured against the prompt it replaced. Both files exist. This is the flag that would run it.

And the plainer one: whether any of the plan-quality results move when the lead is not bare. Every number in the programme was produced under a lead with no standing prompt at all, which is not the configuration anyone actually works in.

Two things to expect when turning it on, both recorded in `resolve_lead_prompt`. `prompts/lead.md` ends with a Korean-language rule that exists specifically because a `CLAUDE.md` would carry it into every headless `claude -p` — and an arm is a headless `claude -p`. Against the built-in `with-skill`/`without-skill` pair it also hands the control arm instructions naming `ocs ask` and `ocs team`, which are on PATH only through the plugin that arm does not have. Neither applies to a `--variant` pair, which is the cleaner place to take the first reading.

## A default eval run does not record which harness it ran

`--variant` arms record their resolved commit in the manifest, so the plugin copy each one launched under is reproducible. The default `with-skill`/`without-skill` pair records only a path: `arms_spec.with-skill.plugin` points at `<run>/plugin`, and nothing anywhere says which commit that copy came from.

That makes the copy the only record of what actually ran, which is why it is still kept — six runs on disk depend on it. It also means the six cannot be compared against a later run except by reading their plugin trees, and that a run whose copy is lost is unattributable.

The fix is one line where `prepare_plugin` is called without a `source`: resolve `HEAD` of the harness repository and put it in the manifest beside the path. `prepare_plugin` also re-renders agents onto one model, so the commit alone does not reproduce the copy — the manifest already records `model`, and the pair does.

Doing it unlocks dropping the copy, which is ~800K of a default run and ~1.4M of a `--variant` one. Not urgent on its own; worth doing next time the manifest shape is touched.

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

The mint half is fixed. `start` and `checkpoint` now take `--run-root` with `--slug` and name `<run-root>/<YYMMDD-HHMMSS>-<slug>/` themselves. What is left is the `ocs ask` half, above.

Recorded here because the diagnosis generalises. Both were the harness asking a lead to assemble something in the shell that the harness could assemble itself, and in both cases the shell turned out to be the wrong place: a compound command is refused outright by a worktree-isolated session, and a 646-line argument is a shape a document does not take. Anything else that reads as "compute this and pass it in" is worth checking against that pair.

