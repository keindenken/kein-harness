# Purpose

What this harness is for, what it deliberately is not, and how to tell when it is done.
Written 2026-08-03. Revise it when a decision here is overturned, not when work happens.

## Why build one

OMC 4.15.7 is the incumbent. Keeping what works, replacing what does not.

**Keep:** the agent prompts, the bridge commands (`omc ask`, `omc team` — the commands,
not the skills), the skill names.

**Replace:**

- **Hooks.** Too many artifacts, too strict, and they misfire often enough to cost more
  than they save. The objection is reliability, not hooks as a concept.
- **Skills.** 42 exist; six are used. Several are large single files, and size correlates
  with the model losing the thread inside them. Wrapping one produced two skills for one
  role, which added a confusion point rather than removing one.
- **Cross-vendor split.** OMC and OMX are sibling plugins that do not interoperate, and
  OMX's hooks are stricter still.
- **Ecosystem lock-in.** Projects end up depending on OMC rather than using it.

Two additions that are not OMC complaints:

- **Orca as the orchestration runtime.** Orca is the main IDE now. Multi-agent work should
  run through Orca terminals and worktrees instead of OMC's tmux machinery.
- **Absorbing what Superpowers got right.** The `interview` workflow in `~/.codex-orca` is
  the first instance.

## What this is, under the obsolescence lens

`~/Documents/wiki/harness/harness-obsolescence.md` argues that execution harness has been
retired by model capability and only planning harness survives. That claim lands directly
on half of this project, so it sets the scope rather than sitting beside it.

The measured evidence so far agrees with it. Porting OMC's Critic from 3,047 words to
1,115 changed no behaviour, and a three-line restoration of the removed severity floor
changed nothing across ten samples under deliberate pressure
(`~/.codex-orca/docs/superpowers/verification/agent-prompt-evals.md`). Prompt material
that reads as load-bearing frequently is not.

Two of the argument's conclusions do not apply here, for reasons the source does not
address:

- **Subagents are context management, not role division.** An explorer that reads a
  hundred files and returns three lines is compression, not a telephone game — the loss
  is the point. The 6x token figure describes re-sending shared context between agents,
  which is the opposite of isolated dispatch.
- **Cross-vendor calls are an ensemble, not self-critique.** "Run self-review three times
  and the first answer wins" holds when the reviewer shares the author's error
  correlations. A different vendor's errors are less correlated, so a second opinion adds
  information instead of flattening.

And the source states its own exception: a fixed, checkable criterion is where an external
checker still earns its cost. `AGENTS.md`'s rule that a gate must be able to go RED is
that exception stated as a repository invariant. Review rounds without such a gate are
what the argument retires.

Component classification that follows:

| Component | Kind | Status |
| :--- | :--- | :--- |
| `interview` | planning harness | permanent — the one class the argument keeps |
| `plan` (consensus gate) | verification | conditional on a gate that can fail |
| `execute` | execution harness | most exposed; carry fewer verification rounds over time |
| `ralph` | execution loop | port as a general-purpose loop |
| orca orchestration | cross-vendor | outside the argument's scope |
| the 14 agents | context isolation | outside the argument's scope |

**`interview` is therefore first**, not the agents. It is the only component with durable
value, the code already exists and is validated, and it is the same object as the
interview pattern in `~/Documents/wiki/context-engineering/unknown-discovery-patterns.md`.

## Scope

Skills, capped at what is actually used:

`interview` · `plan` · `execute` · `ralph` · `autopilot` · orca orchestration

Not in v1: `self-improve`, `autoresearch`. Both are wanted, but how to use them is
unresolved, and an unresolved use is a signal that the need has not arrived.

Agents: the fourteen already normalized in `~/.codex-orca/foundation/prompts/`.

### Non-goals

- Growing the skill count. Six is the working ceiling. Adding a seventh means removing one
  or arguing why the ceiling was wrong.
- Hooks. Start at zero, matching `~/.codex-orca`. Adding one requires naming the failure
  it prevents and how its misfire would be detected.
- Restoring prompt material because an upstream harness had it. See the operating rules.
- Replacing Orca's command namespace or reimplementing its orchestration runtime.

## Naming and surfaces

Harness name: **kein**. CLI name: **ocs**. They are deliberately different.

| Surface | Value |
| :--- | :--- |
| Claude plugin | `kein` → `/kein:interview`, `kein:executor` |
| Helper CLI | `ocs`, one binary serving both vendors |
| Repository | `dev/kein-harness` |
| Project state | `<repo>/.agents/kein/`, or the config home with no repository in scope |
| Codex home | `~/.codex-orca`, unchanged |
| Codex launcher | `orcodex`, unchanged |

`gdr` is superseded. One CLI is a requirement rather than tidying: a single resolver for the
canonical role prompts is what prevents the two vendors' prompt sets from drifting apart.

Splitting the CLI name from the harness name is a direct response to how OMC read in
practice, where `omc ask` the command sat beside `ask` the skill under a plugin also called
`omc`. The rule that follows: **no skill may share a name with an `ocs` subcommand.** The
plugin name is not the problem; a command and a skill answering to the same word is.

`ocs` was already the Codex-side helper name in `~/.codex-orca`'s decision log, so adopting
it here leaves that record correct as written instead of requiring a revision.

`~/.codex-orca` keeps its name. It is not a surface anyone types, and renaming it would
invalidate the paths recorded in its verification documents — worse than an asymmetric
directory name.

## Portability

Canonical role prompts live in one place, `~/.codex-orca/foundation/prompts/`, and both
vendors render from it. `build_agents.py` already does this for Codex; Claude needs an
equivalent renderer.

Vendor-specific detail may differ. The requirement is that whichever vendor leads, the
experience is as close to identical as the platforms allow.

This also makes evaluation transferable: a measurement taken against the canonical prompt
holds for both sides. Two prompt sets would mean two evaluations and no guarantee that a
result on one applies to the other.

## Operating rules

1. **No automatic state in the project; work products belong in it.** The objection to
   `.omc` was always the hook-generated `.omc/state/`, not artifacts the user asked for —
   `repo/.omc/` holding `plans/` and `research/` is the preferred shape, not the problem.
   So: write nothing the user did not ask for, and put what they did ask for under
   `<repo>/.agents/kein/`, resolved by `ocs state-dir`.

   Not `docs/`. That tree is reserved for reference documentation — how things work and
   how to use them — rather than the output of a work session.

   `.agents/` rather than `.kein/`: it is already the vendor-neutral namespace at both the
   project and home level, which is what a harness serving two vendors should sit under.
   Keeping state in the repository rather than a vendor's config home is also what lets a
   run started from Claude be resumed from Codex.
2. **Progressive disclosure.** `SKILL.md` stays thin and defers to `references/` read at
   the stage that needs them. `execute/SKILL.md` is 64 lines in front of three references
   and an 808-line script. This is the prescription for the diagnosis that large single
   files confuse the model.
3. **Prove before adding.** New prompt rules earn their place by differential evaluation,
   not by precedent. The harness is at
   `~/.codex-orca/foundation/tests/evals/agents/`. A gap found by reading two prompts side
   by side is a hypothesis; an unproven hypothesis restored into a prompt is exactly the
   stale rule the obsolescence argument warns about.
4. **Judgement over rules.** Prefer a stated principle to an enumerated rule, and an
   interface constraint to an example. Examples narrow the search space as a side effect.
5. **Rich references.** Prefer executable references — test suites, rubrics, real code —
   over prose specification. This is also the substitute when a verification round is
   removed from `execute`.

## v1 done

**Turn OMC off and complete one full round in `descvi` using only `kein` components:**
plan, implement, review, accept. Needing to re-enable OMC at any point means not done.

Development continues past v1. This is the first gate, not the finish.

## Order

1. `interview` — port and use it. Durable value, code exists, validated. Done.
2. `ocs ask` — done. One resolver for canonical prompts; also the eval harness's invocation path.
   Requirements: `.agents/kein/requirements/260803-kein-ask-bridge.md`.
3. Agents — render the fourteen for Claude from the canonical source. Done: `ocs
   render-agents`, gated by `ocs check-prompts`.
4. `ralplan` — done. Consensus planning, one skill.
5. `execute` — done. The implementation loop; may later carry parallel dispatch the
   way `team` does.
6. `team` — either an orchestration-only wrapper, or Orca orchestration folded into
   `plan` and `execute` directly. Undecided.
7. `ralph` — the general-purpose loop. Needs 6 first.

`autopilot` wraps `interview -> plan -> execute`, resuming at whichever stage has not
been done, so it can land at any point once those three exist.

## Open

- **Bridge prompt layering.** None of the fourteen prompts reference `AGENTS.md` or
  `CLAUDE.md`. Correct inside a workflow that injects repository context into the brief; a
  gap on a bare one-shot call. A bridge call needs role prompt + repository instructions +
  task brief. Unresolved: whether Codex and Claude inject repository instructions into a
  subagent automatically.
- **How far to cut `execute`'s verification rounds.** The obsolescence argument says
  fewer; `AGENTS.md` says a gate must be able to fail. Resolve by measurement on a real
  round, not in advance.
- **`plan`'s pre-mortem gate.** The Planner is instructed to produce a pre-mortem and
  nothing checks it. Output required, verification absent — a defect regardless of the
  obsolescence argument, since it is an inconsistency rather than a stale rule.
- **Extracting the canonical prompt library from `~/.codex-orca`.** `ask` runs the provider
  against the vanilla Codex home while reading prompts from the tuned one, which is the
  first evidence that a vendor-neutral library living inside a lead-tuned environment is
  incidental. Gate: when a second consumer needs it without the Codex home present.
