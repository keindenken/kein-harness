# Open threads

Work that is parked rather than finished, with enough context to pick it up cold. Skill-specific items live beside the skill: `docs/skills/plan/open.md`, `docs/skills/ralplan/open.md`, `docs/skills/execute/open.md`, and `docs/skills/fsd/open.md` are the ones that exist. Closed items move to `docs/closed-threads.md`, or to a `closed.md` beside the skill's own `open.md`.

The phase-46 comparison — the two kickoff traces, the two finished plans, the seven-round run ledger, and the five threads they produced about the plan artifact — has moved to `docs/skills/ralplan/260826-phase-46-comparison.md`, in Korean, because it is one investigation rather than five parked items and the working discussion around it is Korean. Entry cost, the artifact carrying its own review history, the lead authoring its own requirements, and the Evidence Gate validator are all there.

## The `research` skill has not been checked against its own falsifying questions

It has now been run once, `.agents/kein/research/260919-llm-wiki-design.md` (2026-09-19), but whether that run answered the memo's falsifying questions — separating a blind spot from a reachability failure, whether the round section is enough to resume from, and whether all three lanes fired — has not been checked.

## How far to cut `execute`'s verification rounds

The obsolescence argument says fewer. The invariant that a gate must be able to go RED says a round without a failable gate is the one to cut, not rounds in general. Resolve by measurement on a real round rather than in advance.

## The ported skills have never been read against `standing-prompt.md`

Every skill except `plan` arrived from `~/.codex-orca` rather than being written here, and the rules for editing a standing prompt were written afterwards. `plugin/prompts/standing-prompt.md` lists `**/SKILL.md` and `**/prompts/**/*.md` in its own `paths:`, so it already claims these files; nothing has been read against it.

Its eight rules are not stylistic. Four of them delete text rather than reword it: a line that binds nothing, a restatement of what the repository already shows, an enumeration where a principle would cover the unforeseen case, and a number that is neither regenerable nor version-anchored. A fifth moves text out — provenance belongs in the commit that makes the change, not beside the rule.

Two findings from 2026-08-19 are what makes this worth a pass rather than a habit. `execute`'s serial-ledger sentence was read as forbidding the thing it permits, which is a "point at the collision" failure — the sentence carries a permission and a prohibition in one line and settles neither. And `ralplan` required a `Status reason` naming why approval is absent while its own review contract forbade a fresh lane from receiving exactly that, which is a collision between two files that nothing named.

Do it as a pass over one skill at a time with the rules open, not as a sweep. The measurement programme exists to catch what a rewrite breaks, and `plan` is the only skill it currently covers.

## `tracer` ranks by a scale that was deleted

`agents/tracer.md` step 4 says to "label provenance and rank evidence strength", and step 7 to "reject, down-rank, retain, or merge explanations only as the evidence warrants". Neither the prompt nor anything in the skill tree says what the strengths are or how a conflict between two of them resolves. `prompt-porting-notes.md` records what happened: a six-tier evidence-strength scale and its conflict rule were removed in normalization, and the instructions that consumed them were not.

Not unexecutable — a model asked to rank will rank. Undefined, which is worse in a specific way: two tracers reach different orderings from the same evidence and neither is wrong, so the ranking cannot be argued with. That is the failure the scale existed to prevent, and it leaves no trace in any single run.

Unlike `plan`'s pre-mortem, this one has no in-repo home. There is no `tracer` skill — the role is a prompt and nothing else — so a scale cannot be added beside it the way the pre-mortem's shape went into `plan-template.md`. Either the scale returns to the canonical prompt, or the two instructions stop naming a ranking they cannot define. That is a decision about canonical, which is the same per-vendor-wording question the closed extraction thread left unresolved (`docs/closed-threads.md`).

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

Two things to expect when turning it on, both recorded in `resolve_lead_prompt`. `plugin/prompts/lead.md` ends with a Korean-language rule that exists specifically because a `CLAUDE.md` would carry it into every headless `claude -p` — and an arm is a headless `claude -p`. Against the built-in `with-skill`/`without-skill` pair it also hands the control arm instructions naming `ocs ask` and `ocs team`, which are on PATH only through the plugin that arm does not have. Neither applies to a `--variant` pair, which is the cleaner place to take the first reading.

## A default eval run does not record which harness it ran

`--variant` arms record their resolved commit in the manifest, so the plugin copy each one launched under is reproducible. The default `with-skill`/`without-skill` pair records only a path: `arms_spec.with-skill.plugin` points at `<run>/plugin`, and nothing anywhere says which commit that copy came from.

That makes the copy the only record of what actually ran, which is why it is still kept — six runs on disk depend on it. It also means the six cannot be compared against a later run except by reading their plugin trees, and that a run whose copy is lost is unattributable.

The fix is one line where `prepare_plugin` is called without a `source`: resolve `HEAD` of the harness repository and put it in the manifest beside the path. `prepare_plugin` also re-renders agents onto one model, so the commit alone does not reproduce the copy — the manifest already records `model`, and the pair does.

Doing it unlocks dropping the copy, which is ~800K of a default run and ~1.4M of a `--variant` one. Not urgent on its own; worth doing next time the manifest shape is touched.

## A plan correction ends the run, and the question it forces is per-task

`execute` binds a run to its input by hash. `validate_transition` refuses a nonterminal transition that changes input identity, and `reconcile` answers a changed input with `block and reassess the changed input before resuming`. That is what stops a plan being swapped under a live ledger, and it is not the thing to loosen.

It collides with the repository's own rule. descvi's `AGENTS.md` requires the plan to be updated in the same change when reality forces a departure from it, and `task-ledger-template.md` blesses the smaller half of that already — a factual correction may update a task when it stays inside the authorized outcome and its rationale is recorded. So a correction that the work forces is required, and making it ends the run.

Measured on the phase-47 execute run: story one of five forced two plan corrections (acceptance 24's element-keyed reading, part 2's band removal). The run was aborted with a reason naming the one accepted task, and a second run opened carrying the remaining four. One story, one split.

The lead gave two reasons and only the first holds. The input hash is immutable within a run, which is true and decisive. The second was that task-001's acceptance was bound to a fingerprint that HEAD has since moved past, so re-asserting it would be an unmeasured claim — but that is not how acceptance is validated. `_validate_acceptance` checks each reviewer verdict against the acceptance's **own** recorded fingerprint and never against the current worktree, so an acceptance is a sealed, self-describing record and a later worktree move does not touch it. Nothing in the machine would have refused carrying task-001 forward as accepted.

What would have been wrong is subtler and is the actual thread. One of the two corrections changed acceptance 24 — the condition task-001 was accepted against. So the question is not "is this acceptance stale" but "did this correction touch what that task was accepted for", and that is a per-task question the input hash answers for the whole ledger at once. A run that corrects a plan section no accepted task depended on is split for nothing; a run that corrects the very condition a task passed under must not carry it, and today both get the same answer.

Not acted on. The cheap-looking fix — a transition that records old hash, new hash and a reason while keeping the run — moves the judgement to whoever writes the reason, which is the lead, which is the one agent in the loop no lane reviews. Worth deciding only with more than one run's evidence; the remaining four stories will produce it, since the same rule fires on every correction they force.


**State as of 2026-09-18.** The evidence came in and the cheap-looking fix shipped. The remaining phase-47 stories retired three more runs on the same rule, one of them over four amendments, and phase-48 retired two. `3841bc2` (2026-09-05) added `amend --reason`: it records `{at, reason, from, to}` in `input.amendments` and keeps the run, and the completed receipt carries them, so the reason the lead writes is at least inherited by the next reader. No lane reviews it, which was the objection above, and that objection still stands.

The per-task half is unchanged and now sharper. An amendment keeps every accepted task accepted, including one whose condition the amendment touched, where before the abort at least dropped it. The template sentence quoted above was narrowed in `30b7136`: a correction may change a task's title, verification path or rationale, never its scope or completion condition. oh-my-claudecode 5.x answers this half by binding each completion claim and approval to the criteria revision it was made under; `docs/skills/execute/open.md` records why its companion route, replacing a criterion inside the run, was not taken here.

## Seven notes from the old wiki bear on how the harness is written, and none has been weighed

The findings drain of 2026-09-19 (`~/Documents/wiki` commit `639dd30`, plan `.agents/kein/plans/findings-wiki.md` S4) kept only measurements of runtime behaviour. Seven items were not that, but each argues for a change to a rule or a skill here, so they are listed for `/kein:deliberate` rather than kept in the findings store:

- `~/Documents/wiki_deprecated/_raw/note/260802-consensus-round-lessons.md`, `260803-parallel-verification-lane-operation.md`, `260804-lead-prescriptions-and-truncated-populations.md`, `260805-attribution-by-capability-and-neighbouring-claims.md`, `260806-a-red-gate-in-a-world-that-cannot-happen.md`: lessons from running verification lanes on descvi. Much of this already shaped `plugin/prompts/` and the execute and ralplan skills through the 260810 prompt revision; what has not been checked is which of it did not land.
- `~/Documents/wiki_deprecated/_raw/note/260809-rewriting-standing-agent-prompts-on-measurement.md`: the test for whether an instruction is worth its tokens. `plugin/prompts/standing-prompt.md` is its descendant; whether anything was lost in the move is unchecked.
- `260819-Building Docs for Agents, Not Humans Inside OpenWiki.md`, in `~/Documents/wiki` snapshot `28e2385` under `_raw/`: how to write repository docs for an agent reader, which is what the `instructions` skill does to AGENTS.md.

## `ocs team` rebinds the lead's terminal to a new Run on every lane

`orca orchestration run-create` binds the terminal that calls it, and Orca refuses to let one terminal act as another (`run-create --from <worker terminal>` answers `consumer_fenced`, measured 2026-09-19 on orca 1.4.205). So every `ocs team` invocation moves the lead's binding to that lane's Run. Two consequences, neither yet observed in a real run:

- A lead that is itself an Orca coordinator — bound to its own Run and waiting on `check --wait` — loses that binding the moment it starts a lane, and its own workers' messages stop reaching it until it runs `run-use` again.
- With several lanes started concurrently, only the last Run stays bound. `ocs team` consumes its own `worker_done` only while its Run is still the bound one, so an earlier lane's message stays in its inbox and may nudge the lead later. Whether Orca nudges for an unbound Run at all is unmeasured.

The Orca model is one coordinator, one Run, a whole wave inside it. Moving `ocs team` onto the lead's existing Run would fix the first, but then every lane shares one inbox with whatever else the lead coordinates, and consuming a `worker_done` there means filtering by dispatch rather than draining. Not worth doing until a lead actually coordinates an Orca Run and starts a lane from it.

Observed 2026-09-25, and not a defect after all: mail another session addressed to a lead's terminal handle landed in the Run of that lead's last `ocs team` lane. That Run is the lead's current inbox (the lead is its coordinator), so Orca nudged the lead with "You have 1 orchestration message. Run `orca orchestration check --run <lane run>`" and the lead read it. The only open part is latency: the nudge came 96 seconds after the send, and only after other input had already started a turn (findings `260925-orca-messaging-between-peer-claude-sessions.md`). Orca 1.4.207 has no verb to unbind a terminal, only `run-use` to rebind it. EnterWorktree is not a factor: the two leads made 60 `orca` calls while worktree-isolated and none was refused.

## An Orca-launched interactive Claude worker would get the lead prompt

An interactive Claude worker that Orca orchestration launches in its own pane would run under `CLAUDE_CODE_ENTRYPOINT=cli`, same as any other interactive session, and would get the lead prompt from `plugin/hooks/lead-prompt.py`. No flow launches one today, since `ocs team` starts Codex, and what tells such a worker apart is unmeasured. `~/.local/bin/claude-kein` sits outside the repository and is the owner's to delete.

## `writer` and `designer` roles

Two roles to add, raised 2026-09-23. Both are meant to consult other material and produce the single best version from it, not to generate from scratch.

- `writer`: tuned for now to writing prompts, where "prompt" covers skills, `AGENTS.md` and every other instruction file. The rules it would work to already exist: `plugin/rules/standing-prompt.md`, `docs/project/prompt-edit-rules/`, and the `instructions`, `deliberate` and `sharpen` skills. A general prose-writing role may come later, and whether it shares this prompt is open.
- `designer`: UI/UX.

The route is the usual one: body and its `description`, `tier` and `sandbox_mode` frontmatter in `agents/<name>.md`, then `dev/kein-dev render-agents` and `check-agents`. Settle each role's reason to exist with `/kein:deliberate` before writing it, above all what `writer` does that a lead running `instructions` or `sharpen` does not.

## Per-directory `AGENTS.md` for subagents

oh-my-claudecode had a skill (probably `deepinit`) that writes an `AGENTS.md` into subdirectories such as `src/`, plus a hook that feeds them to the agent. The idea, raised 2026-09-23, is that these would help subagents most.

What is known: Claude Code loads a subdirectory's `CLAUDE.md` on its own but not an `AGENTS.md`. The owner has confirmed that Codex does not load a subdirectory's `AGENTS.md` automatically either. So these files are read only if something feeds them in: a hook on the Claude side, and the lane package on the `ocs team` side, since the harness puts no hook on a vendor lane.

Open: how omc's hook chose the file and when it fired (the source is worth reading before designing anything); whether generated per-directory docs stay accurate or become one more thing to keep up to date; and whether this belongs in the `instructions` skill, which already writes the root `AGENTS.md`.

## `ralplan` and `execute`: a fix that does not need another review, and run flags — raised 2026-09-24

**Fix, then approve without a re-review.** The owner wants a verdict that means "this needs correcting, but not another round" — the corrected artifact is approved without a fresh lane — as oh-my-claudecode had. The two skills are not in the same place. `execute` already has it for `REVISE`: step 7 lets a `REVISE` finding be "fixed before [acceptance] with the verification path re-run and no fresh lane". `ralplan` does not, and the reason is structural rather than a missing word: `REVISE` findings are carried into the approval unfixed, and fixing one changes the review hash, which invalidates every verdict. So the question in `ralplan` is whether some content change may be made after the last blind round without reopening it — which is exactly the drift the two hashes exist to catch — and not whether a new verdict word is needed. A `BLOCK` that the lead thinks is small still has only two exits, a revision round or a deferral.

**Invocation flags.** Wanted on both skills:

- `--primed`: a re-review does not go to a new blind lane; the previous reviewer runs the closure check only. Today a primed closure check exists in both contracts but "cannot approve", so this flag inverts a rule both review contracts state, not only a default.
- `--quick`: review runs faster. Not yet defined — fewer lanes, a lighter tier, or a shorter rubric are three different things.
- `--round <n>`: run only the n-th round.

Suggestions to weigh alongside, not yet discussed with the owner: `--max-rounds <n>` to stop at a bound and hand back `Draft` instead of re-arming the five-round trigger; `--lanes`/`--reviewer` presets such as a single-lane run; `--dry-run` that stops after the round-1 package is assembled so the package itself can be inspected (which would not have caught the `Status` leak in `docs/skills/ralplan/open.md`, since that one bypassed the package); and `--resume <run>` if resuming is not already implicit in the ledger.

## A lead that never started an `ocs team` lane cannot be nudged by mail

Measured 2026-09-25 (findings `260925-orca-messaging-between-peer-claude-sessions.md`): Orca types its "You have N orchestration message(s)" nudge into a pane about a second after mail arrives, but only when that pane is bound to a Run and has been seen idle. A busy pane gets it at its next idle, and a pane bound to no Run got none in twelve minutes. A lead is bound only as a side effect of its first `ocs team` lane, so before that, mail another session sends it just sits there.

The direction is a home Run per lead: bound once at session start, so the lead is reachable from the first minute. Where to create it is open. The SessionStart hook runs before any Orca pane identity is known to be stable, and a lane's `run-create` would still move the binding off it (Orca 1.4.207 has no unbind, only `run-use`). So `ocs team` would also have to rebind to the home Run after starting its lane, and its `worker_done` cleanup, which assumes it is bound to the lane Run, would have to change with it. The cleanup is also not stopping the late nudges it exists to stop: the two descvi leads received 40 across their lanes, often two per lane.
