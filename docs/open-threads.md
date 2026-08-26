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

## `ocs team` cannot be exercised without spending a session

Every precondition it owns — the prompt library's freshness, the role roster, the trust record, Orca's reachability, the `developer_instructions` probe — runs before anything is created, and then the command immediately creates a terminal and starts a worker. There is no way to check that the preconditions pass for a given invocation without also launching one.

Found by launching one accidentally while testing `--worktree`: the lane attached to no dispatch, left an idle provider terminal in an unrelated repository, and created a run directory there that had to be removed by hand. Nothing was damaged, and nothing in the command's design prevented it.

A `--check` that stops after the last precondition and exits would make the command testable. It is small and the ordering it needs already exists.

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

## The plan artifact carries its own review history, which is both the length and a hole in the blind lanes

Two finished plans for the same phase, kept at `docs/260825-omc-v35-ralplan.md` and `docs/260826-kein-v35-ralplan.md`. Not identical in scope, and the gap survives allowing for that: 610 lines against 1069, 8 ruling subsections against 22, four pre-mortem scenarios against thirteen.

The length is a symptom. What produces it is that RALPLAN revises one artifact in place across rounds, and each round's correction gets written as a **diff against the previous text** rather than as the current state. Counting references to the plan's own revision history — "corrected at round 2", "revision 1's elimination for (b) was wrong", "RE-RULED at round 1", "reproduced" — the body carries 149 against the incumbent's 20, which is about three times the density per line. The thirteen pre-mortem scenarios are ordered S1–S8 then S13, S12, S11, S10, S9: sorted by the round that discovered them, which is an ordering no reader of the plan needs.

Two things are being conflated in that prose and only one of them belongs:

A **fact** the correction established — the pill's outward reach is the whole band, `R42-D3` clause 4 is violated in the shipped build, the corrected inequality in §2.11 — is load-bearing and an executor needs it.

An **attribution** — which revision was wrong, what it had claimed, that this is "P46-1's own class landing on P46-1's own section, twice" — is not. The current ruling is the whole of what an executor can act on.

That distinction is the one the owner has been reaching for since before this harness existed, and it is mechanically checkable: state the fact, never state which revision was wrong about it.

**And the attribution is not merely noise — it breaks the review contract.** `review-contract.md` says a fresh reviewer receives "no previous finding, verdict, reviewer identity, revision note, change summary, claimed fix, closure result, or expected outcome". It then explains that `Status` and `Status reason` are stripped from the package precisely because a round-two `Status reason` names "the round, the verdicts it carried, and what the revision changed — four of the things in that list, arriving inside the artifact this package is required to carry whole."

The contract found the leak, identified exactly why it mattered, and plugged two lines of it. The same four forbidden things are spread through the body, which the package carries whole and unredacted. A lane told it is blind is reading "⚠ **Corrected at round 1. Revision 1 named two and omitted the one that matters**" and pre-mortem entries labelled "(NEW, round 5)". `plan-gate.md` states the same goal for `Status` in its own words — "a reader who opens the plan cold gets that answer without reconstructing the round history" — and nothing below that line enforces it.

So the seventeen rounds and sixteen revisions on the earlier plan are not straightforwardly evidence that the loop converges. Some part of each round's blindness was already spent.

What the two documents are good for, in order of how cheap each is:

**A gate, and the function it needs already exists.** `state.py` has `review_text()`, which is exactly the artifact minus the two lines the package strips — the same text a lane reads. A sibling to `_evidence_gate_errors` that fails when *that* text attributes a claim to a revision or a round would move this from a reader's complaint to a RED at the gate. Scoping it to `review_text()` is what keeps `Status reason` free to go on naming the round, which it is required to do.

**Evidence for a template change.** `prompt-revision.md` asks for evidence before a prompt is changed, and a finished pair on one task is the strongest kind available. The incumbent's answer is a `## 10. Revision log` — one place for the history, with the body left alone. `plan-template.md` names Status, Status reason, Open Questions, Evidence Gates and Pre-mortem, and gives round history no home at all, which is why it goes everywhere.

**A grader.** History density per hundred lines of body is a number, and it is the kind of thing `dev/eval`'s case mode grades. Worth having before any template change, so the change can be shown to have moved it.

Not yet established: how much of the 149 is load-bearing fact wearing attribution's clothes. Sampling a dozen and classifying each as fact or attribution would settle whether a gate can be strict or has to be advisory, and it is an hour's work on documents that already exist.

## `ralplan` costs far more to enter than the incumbent, and most of it is not the process

Two kickoff traces on the same phase-46 task, scraped 2026-08-24 and kept at `docs/260824-omc-plan-kickoff.md` and `docs/260824-kein-plan-kickoff.md`. To the planner dispatch: the incumbent took about four steps, this harness about twelve, seven of them Bash.

Where the difference is not:

The incumbent's MCP server exposes 67 tools — state, notepad, project memory, shared memory, wiki, LSP bridges, a Python REPL, trace readers. It is a persistence surface, it was called once in that trace, and it is not what made the entry cheap.

Its hooks are: 22 across 11 events, of which `SessionStart` runs three that inject up to 6000 characters of prioritized context — project memory, notepad priority, pending tasks, restored modes — before the user types anything. That is the onboarding, and it never appears on the trace's clock. Conceding this one is acceptable: it is a different architecture, not a defect here. What is not acceptable is leaving anything optimizable unoptimized on this side, which is the rest of this entry.

Even that overstates it. `descvi/repo` sets `OMC_SKIP_HOOKS` covering `skill-injector` and `keyword-detector`, so the incumbent ran that trace with its injectors off and still entered in four steps.

Where the difference actually is:

Its `2plan` is one file, 62 lines, no references. `ralplan` is 73 lines plus four references plus `plan`'s own SKILL.md and template — roughly 330 lines across six files, read one `cd … && cat` at a time.

And `## Required Files` says "Read these when their stage begins", which did not happen: all three were read at kickoff, `review-contract.md` included, whose stage is many rounds away. So the staging instruction is either unrealistic — a lead cannot set up a run without the state schema and the gate — or unenforceable. If it is the first, the honest fix is to say which two are needed at entry and stop splitting the rest for a laziness nobody practises.

Two specific things, one of which is a defect and one of which is not:

`ls -R` over the skill directory is not one. It is cheap orientation and reading it as waste would be a rule about tidiness rather than about cost.

Reaching `plan`'s contract by `cat`-ing `plan/SKILL.md` is one. `ralplan/SKILL.md:14` says "the only skill it runs is `plan`" and its Required Files line says the artifact's contract "arrives with the `plan` invocation" — the lead did the opposite of both. Neither line is wrong; both are too quiet to beat a directory listing that is already open. The wording needs strengthening to a refusal, not a description.

Worth noting about the measurement itself: "steps to planner" structurally favours whoever pays at session start. The incumbent pays it in every session whether a plan follows or not, and measuring from skill invocation makes that cost invisible by construction. Six files against one is real; four steps against twelve is inflated.

## A planning run authored its own requirements when the contract asked for a summary

`ralplan/SKILL.md:35` says to "preserve the original requirements by path and hash when possible; otherwise store a prompt-safe summary and its hash", and `state.py`'s `start --input` takes a requirements path. The fallback is a *summary*.

The phase-46 kickoff wrote a 132-line `requirements.md` into the run directory instead, growing past 250 lines, assembled from documents that already exist in the repository and are cited by path inside it. That is not what either half of the contract asks for: the sources have paths, so the first half applied, and what was produced is not a summary in any case.

Not obviously harmless. The lead is the one agent in the loop with no independent review, so a requirements document it authors alone becomes the governing text for every lane downstream without anything having checked it against the sources it paraphrases.

Unresolved whether the contract is at fault. "Preserve by path and hash" assumes one requirements file exists; a phase assembled from a tracker, a spec section, a known-issues file and three owner rulings has no single path to preserve, and the summary fallback may simply be too small a hole for the case that actually occurs. If so the fix is a third option that is honest about what it is, with a bound on it — not a lead-authored document that presents as requirements.

## A 20-minute planner round was spent on punctuation, because only the lead can run the validator

`validate-plan` rejected four Evidence Gates on the phase-46 plan. The content was right; the labels read `- Pass path (조건): …` where `_evidence_gate_errors` requires `^- Pass path:\s*\S`. `plan-template.md` does say "use this exact optional shape", so the validator is not wrong to be strict — a label that drifts is how a gate silently stops being machine-checkable.

The cost is the problem. The planner ran 20m15s, returned, was validated by the lead, and was resumed for a formatting pass it could have caught itself in a second. `validate-plan` is documented in exactly one place — `state-schema.md`, which is a lead-facing reference — and `prompts/planner.md` never mentions it. The agent that writes the artifact has no way to check the artifact's shape.

Nothing here needs a new mechanism. The validator exists, it is a single command, and the planner is already given the canonical plan path. What is missing is the instruction to run it before returning, which is a change to a canonical prompt and therefore not a quiet one.

Worth measuring first: whether the label drift is a one-off or the common failure. If gates are the usual reason a first draft bounces, this is the cheapest round in the whole loop to delete.

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
