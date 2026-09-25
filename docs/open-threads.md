# Open threads

Work that is parked rather than finished, with enough context to pick it up cold. Skill-specific items live beside the skill: `docs/skills/plan/open.md`, `docs/skills/ralplan/open.md`, `docs/skills/execute/open.md`, and `docs/skills/fsd/open.md` are the ones that exist. Closed items move to `docs/closed-threads.md`, or to a `closed.md` beside the skill's own `open.md`.

The phase-46 comparison — the two kickoff traces, the two finished plans, the seven-round run ledger, and the five threads they produced about the plan artifact — has moved to `docs/skills/ralplan/260826-phase-46-comparison.md`, in Korean, because it is one investigation rather than five parked items and the working discussion around it is Korean. Entry cost, the artifact carrying its own review history, the lead authoring its own requirements, and the Evidence Gate validator are all there.

## The `research` skill has not been checked against its own falsifying questions

It has now been run once, `.agents/kein/research/260919-llm-wiki-design.md` (2026-09-19), but whether that run answered the memo's falsifying questions — separating a blind spot from a reachability failure, whether the round section is enough to resume from, and whether all three lanes fired — has not been checked.

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

Deferred to a measurement round (`.agents/kein/requirements/260926-open-items.md`), with the rule fixed in advance: run tracer several times on one question; if the rankings disagree, restore a defined strength scale with its conflict rule; otherwise leave the prompt as is.

## The lead prompt can now be an arm's, and no run has used it yet

`kein-dev eval --lead-prompt <path>` appends a standing lead prompt to every arm, which is what a launcher does in real use and what no measured run has ever done. It defaults to `none`, so nothing about the twelve runs on disk changed; the manifest records which side a run was on.

Two measurements it makes possible, neither taken:

`where-justification-lives.md` closes on "No `ocs eval` comparison of `kickoff.md` vs `lead.md` exists" — the rewrite that cut 56% of the words was never measured against the prompt it replaced. Both files exist. This is the flag that would run it.

And the plainer one: whether any of the plan-quality results move when the lead is not bare. Every number in the programme was produced under a lead with no standing prompt at all, which is not the configuration anyone actually works in.

Two things to expect when turning it on, both recorded in `resolve_lead_prompt`. `plugin/prompts/lead.md` ends with a Korean-language rule that exists specifically because a `CLAUDE.md` would carry it into every headless `claude -p` — and an arm is a headless `claude -p`. Against the built-in `with-skill`/`without-skill` pair it also hands the control arm instructions naming `ocs ask` and `ocs team`, which are on PATH only through the plugin that arm does not have. Neither applies to a `--variant` pair, which is the cleaner place to take the first reading.

## A default eval run's plugin copy could now be dropped

Now that the manifest records the harness commit (closed 2026-09-26, `docs/closed-threads.md`, "A default eval run does not record which harness it ran"), the copy itself — ~800K for a default run, ~1.4M for a `--variant` one — is no longer the only record of what ran. Not urgent; worth doing next time the manifest shape is touched.

## Seven notes from the old wiki bear on how the harness is written, and none has been weighed

The findings drain of 2026-09-19 (`~/Documents/wiki` commit `639dd30`, plan `.agents/kein/plans/findings-wiki.md` S4) kept only measurements of runtime behaviour. Seven items were not that, but each argues for a change to a rule or a skill here, so they are listed for `/kein:deliberate` rather than kept in the findings store:

- `~/Documents/wiki_deprecated/_raw/note/260802-consensus-round-lessons.md`, `260803-parallel-verification-lane-operation.md`, `260804-lead-prescriptions-and-truncated-populations.md`, `260805-attribution-by-capability-and-neighbouring-claims.md`, `260806-a-red-gate-in-a-world-that-cannot-happen.md`: lessons from running verification lanes on descvi. Much of this already shaped `plugin/prompts/` and the execute and ralplan skills through the 260810 prompt revision; what has not been checked is which of it did not land.
- `~/Documents/wiki_deprecated/_raw/note/260809-rewriting-standing-agent-prompts-on-measurement.md`: the test for whether an instruction is worth its tokens. `plugin/prompts/standing-prompt.md` is its descendant; whether anything was lost in the move is unchecked.
- `260819-Building Docs for Agents, Not Humans Inside OpenWiki.md`, in `~/Documents/wiki` snapshot `28e2385` under `_raw/`: how to write repository docs for an agent reader, which is what the `instructions` skill does to AGENTS.md.

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

