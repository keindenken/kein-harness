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

Two things to expect when turning it on, both recorded in `resolve_lead_prompt`. `plugin/prompts/lead.md` is now only the core; the owner's Korean-language rule moved to the user layer `~/.agents/kein/prompts/lead.md`, so a run meant to reproduce the owner's lead needs a file that concatenates the two — and that language rule then lands on a headless `claude -p`. Against the built-in `with-skill`/`without-skill` pair it also hands the control arm instructions naming `ocs ask` and `ocs team`, which are on PATH only through the plugin that arm does not have. Neither applies to a `--variant` pair, which is the cleaner place to take the first reading. A third: the lead prompt now leaves `SendMessage` loading to the worker prompt, which reaches only an interactive session's subagents, so an arm's workers never get it.

## A default eval run's plugin copy could now be dropped

Now that the manifest records the harness commit (closed 2026-09-26, `docs/closed-threads.md`, "A default eval run does not record which harness it ran"), the copy itself — ~800K for a default run, ~1.4M for a `--variant` one — is no longer the only record of what ran. Not urgent; worth doing next time the manifest shape is touched.

## Seven notes from the old wiki bear on how the harness is written, and none has been weighed

The findings drain of 2026-09-19 (`~/Documents/wiki` commit `639dd30`, plan `.agents/kein/plans/findings-wiki.md` S4) kept only measurements of runtime behaviour. Seven items were not that, but each argues for a change to a rule or a skill here, so they are listed for `/kein:deliberate` rather than kept in the findings store:

- `~/Documents/wiki_deprecated/_raw/note/260802-consensus-round-lessons.md`, `260803-parallel-verification-lane-operation.md`, `260804-lead-prescriptions-and-truncated-populations.md`, `260805-attribution-by-capability-and-neighbouring-claims.md`, `260806-a-red-gate-in-a-world-that-cannot-happen.md`: lessons from running verification lanes on descvi. Much of this already shaped `plugin/prompts/` and the execute and ralplan skills through the 260810 prompt revision; what has not been checked is which of it did not land.
- `~/Documents/wiki_deprecated/_raw/note/260809-rewriting-standing-agent-prompts-on-measurement.md`: the test for whether an instruction is worth its tokens. `plugin/prompts/standing-prompt.md` is its descendant; whether anything was lost in the move is unchecked.
- `260819-Building Docs for Agents, Not Humans Inside OpenWiki.md`, in `~/Documents/wiki` snapshot `28e2385` under `_raw/`: how to write repository docs for an agent reader, which is what the `instructions` skill does to AGENTS.md.

## An Orca-launched interactive Claude worker would get the lead prompt

An interactive Claude worker that Orca orchestration launches in its own pane would run under `CLAUDE_CODE_ENTRYPOINT=cli`, same as any other interactive session, and would get the lead prompt from `plugin/hooks/prompt-layers.py`, and not the worker prompt, which only SubagentStart delivers. No flow launches one today, since `ocs team` starts Codex, and what tells such a worker apart is unmeasured. `~/.local/bin/claude-kein` sits outside the repository and is the owner's to delete.

## `writer` and `designer`: experiments and wiring

Raised 2026-09-23 as two roles meant to consult other material and produce the single best version from it, not to generate from scratch. `writer` now exists (`agents/writer.md`, rendered to `plugin/agents/writer.md`): a general writer whose expected main use is code documentation, not a prompt-writing specialist. Prompt-writing rules stayed out of the role body; they live in `plugin/prompts/standing-prompt.md`, a path-scoped rule injected into a subagent on its first Read of a matching file. The design's evidence is `references/corpora/260926-github-agents/` — read its README and `analysis/synthesis.md` Q6 for the list of experiments E1–E12 — which shows what popular authors write, not what works; no part of the role is measured.

Open:

- Which experiments to run first, since no eval case exists for `writer` yet: E2 (does the path-scoped rule reach a writer that creates a new file without first reading a matching one, and is it followed), E4 (edit mode: preserve-by-default vs. cut), E7 (missing input: stop and ask vs. assume and disclose), E8 (writer or eval runs the mechanical checks) — the four the role's own choices hinge on.
- `standing-prompt.md`'s `paths:` do not match role files such as `agents/*.md` or `.claude/agents/**`, so a writer editing a role prompt gets no rule injected. Whether to widen `paths:` is undecided.
- Cross-vendor dispatch (`ocs team`/`ocs ask` with `--agent writer`) sends only the role body; no rule is injected on the other vendor, so the brief must name the rule file. Nothing does this automatically.
- Whether `execute` should route documentation tasks to `writer` instead of handing everything to `executor` is undecided.
- The owner's original wish — synthesising the single best version from several drafts or outside examples — is covered in the role only as "outside material shapes wording and structure, never facts". Whether a dedicated synthesis mode is needed is untested (E9).

`designer` now exists too (`agents/designer.md`), grounded in `references/corpora/260926-github-designers/` (`analysis/synthesis.md` Q6 lists evals 1–13). Its output form is set by the brief, taste comes from project rules or a design skill the brief names, it renders and reads what it made where a renderer exists and labels everything else not verified, and it reports facts rather than quality verdicts. Open:

- The evals its distinctive choices hinge on: 1 (does it follow the no-render rule), 3 (does a loaded taste skill override the product's design system), 7 (skill self-critique in the designer versus a separate reviewer), 9 (an ambiguous brief with nobody to ask), and 12, which is cheap and settles runtime beliefs several readings rest on (MCP tools reaching a subagent, reading a PNG back).
- No design reviewer exists. The role refuses to approve its own work and leaves the pick among variants to the brief, so a verdict currently falls to the lead or the owner. Whether `critic` can carry design review, or a reviewer role is needed, is undecided.
- The harness ships no design skill, so craft comes only from what the project or the session already has. Whether to ship one (Anthropic's `frontend-design` is the corpus's best base) is undecided.
- With claude-in-chrome as the session's browser, exercising controls runs in the owner's signed-in Chrome, and permission prompts could stall an unattended run. Unmeasured.

## Per-directory `AGENTS.md` for subagents

oh-my-claudecode had a skill (probably `deepinit`) that writes an `AGENTS.md` into subdirectories such as `src/`, plus a hook that feeds them to the agent. The idea, raised 2026-09-23, is that these would help subagents most.

What is known: Claude Code loads a subdirectory's `CLAUDE.md` on its own but not an `AGENTS.md`. The owner has confirmed that Codex does not load a subdirectory's `AGENTS.md` automatically either. So these files are read only if something feeds them in: a hook on the Claude side, and the lane package on the `ocs team` side, since the harness puts no hook on a vendor lane.

Open: how omc's hook chose the file and when it fired (the source is worth reading before designing anything); whether generated per-directory docs stay accurate or become one more thing to keep up to date; and whether this belongs in the `instructions` skill, which already writes the root `AGENTS.md`.


## The global no-hard-wrap rule is broken early and fixed late

Reported by the owner 2026-09-26 from recent descvi `execute` traces, where the executors were Claude native subagents: comments get written hard-wrapped while the code is being written, and near the end of the task the executor notices and unwraps them — the work is done twice. The rule sits in `~/.claude/CLAUDE.md` and is not ambiguous. Whether the late fix is self-noticed or prompted by a reviewer has not been looked at, and why it is noticed only at the end is unknown.

The owner's plan is to move it to a user-level path-scoped rule in `~/.claude/rules/` (not the plugin — it has nothing to do with kein), beside `kein-standing-prompt.md`. Two reasons. The rule only matters for source code — `.ts`, `.tsx`, `.py` and the like, which an editor soft-wraps anyway — and hard-wrap there hurts on a narrow screen and, the owner suspects, costs an agent reading the file; in an extensionless script such as `plugin/bin/ocs` it matters little, and outside source editing it is dead text in every session. And a rule injected beside the first source file read should draw more attention than a line that is always in `CLAUDE.md`, at the point where the slip actually happens — early, while writing.

What is established: user-level path-scoped rules reach Claude subagents, injected once on the subagent's own first Read of a matching file (`~/Documents/wiki/findings/260926-path-scoped-rules-reach-subagents-once.md`). An executor edits existing files only after reading them, so it would get the rule before its first edit; a lane that only creates new source files without reading one would not.

Moved 2026-09-26: `~/.claude/rules/no-hard-wrap.md`, `paths:` listing common source extensions plus `**/*.md` (the old line covered documents too), and the line removed from `~/.claude/CLAUDE.md`. A probe session confirmed one `nested_memory` injection in the main session and one in a subagent, each on its own read of a source file.

Still open: whether it works — compare comment rewrites in descvi executor transcripts before and after the move. Whether `paths:` accepts brace expansion (`**/*.{ts,tsx,py}`) is unmeasured, which is why the file lists extensions one per line.

## `ocs team codex` failed to start a worker twice in one descvi session, then worked — raised 2026-09-29

In a descvi `text-canvas` session (launched in the descvi checkout, moved into a worktree with EnterWorktree) `ocs team codex --agent executor` failed twice on 2026-09-29 (~09:27 and ~09:30), then worked on the retry the next day with the same package and flags. The first failure's `worker-start.json` reads `state=failed, stage=agent_readiness, lastError=timeout` after about three minutes, on a reused terminal; `ocs team` took the returned dispatch id as attached and reported "failed after 0s". The second attempt left no `worker-start.json`, and its terminal sat idle on codex's welcome screen with the brief unsent until the session ended.

What is established: the misreport (0d600e2 now stops on `failed`/`outcome_unknown`, names the state and stage, and leaves the terminal open). What is not: the cause. Not reproduced from the harness pane with the same role, model (`gpt-5.6-terra`), effort, a 6.4 KB brief, a target worktree other than the pane's, or codex 0.158.0 (auto-updated 2026-09-29 07:51, before both failures). The remaining difference is the session's launch checkout plus EnterWorktree, and Orca's app state at the time (it restarted afterwards, so no live state was left to read).

**Reopen when** a lane fails again with the new message; the terminal it leaves open and `worker-start.json` are the evidence.

Related: the same session's fsd hooks also missed its worktree run (`docs/skills/fsd/open.md`, "The hooks do not see a run started in a worktree"), which points at the same launch-checkout versus worktree split.

## `ocs ask` traces and the SessionStart home-run are not covered by the `ocs team` lane fixes — raised 2026-09-29

Left open by bdf2030, which serialized the Orca binding for parallel `ocs team` lanes from one pane and made their run directories unique.

- **`ocs ask` trace names.** `ocs-ask` names its trace directory `runs/ask/<YYMMDD-HHMMSS>-<role>` and creates it with `mkdir -p`, so two calls with the same role finishing in the same second share one directory and overwrite each other's `prompt.txt`, `command.txt`, `response.txt` and `stderr.txt`. The answer itself goes to stdout, so only the trace is lost. Not observed in a real run. `ocs team` claims its name with `mkdir` and takes a numeric suffix on a collision; `ocs ask` would take the same.
- **SessionStart `ocs home-run --hook` takes no lock.** The `ocs team` binding lock (`~/.local/state/kein/orca-bind/<terminal handle>`) does not cover it. It matters only when a new or resumed `claude` starts in a pane while one of its lanes is inside the few-second locked stretch, which needs lanes that outlive their session. A cheap fix is for `--hook` to try the lock once without waiting and skip when it is held, since a held lock means a lane will return the pane home itself. Not observed.

**Reopen when** either shows up: a lost `runs/ask` trace, or a lane fenced right after a session start in the same pane.

## `ocs team codex --resume` of a large session delivered no brief — raised 2026-10-01

In the descvi `text-canvas` worktree, `--resume` of run `261001-002014-executor` (a 2.4 MB codex session, 329 events, whose first dispatch ended `worker_report outcome=failed` after 480 s) started a dispatch that stayed `ready` with `turn_start=unsupported`. The session file was not written after the resume, so no turn was taken; the lead stopped the lane by hand after four minutes and started a fresh worker. The terminal was closed before its screen could be read. The lead later found the resumed worker's own terminal still alive, and its screen ended with `Fork created. You can continue here.`, a weekly-usage-limit warning, and an empty prompt: the brief had not landed and left no draft, so the composer-draft nudge had nothing to press. Which of the two notices, if either, took the typed input is not established.

Not reproduced: resuming a fresh small session from the harness pane worked, including a resumed task that ran past 90 s, and `turn_start=unsupported` also appears there, so it does not tell the two apart. The likeliest cause is the resumed TUI still loading a long history when the brief was typed, so the input was lost, but nothing measured supports it over another. `ocs team`'s existing composer-draft nudge presses Enter only when Orca reports a draft in the composer.

`ocs team` now warns once after 90 s when a resumed worker's session file has not been written since launch, and saves the worker's screen to `stalled-screen.txt` in the run directory. **Reopen when** that warning appears: the terminal it leaves open holds the screen, and `orca terminal read --terminal <handle> --screen` says what the resumed TUI was showing.
