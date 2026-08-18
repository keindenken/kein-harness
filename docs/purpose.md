# Purpose

What this harness is for, what it deliberately is not, and how to tell when it is done.
Written 2026-08-03, rewritten 2026-08-18. Revise it when a decision here is overturned, not when work happens.

**Two halves, carrying different weight.** Everything under **Commitments** binds: it decides what gets built, what does not, and what counts as finished. Everything under **Why these commitments** explains how they were arrived at; it binds nothing, and a choice that contradicts it is an argument worth having, not a violation. If a sentence is not under Commitments, it is not asking you for anything.

Progress is not recorded here. What has been built is visible in `plugin/skills/` and `plugin/libexec/`; what is parked is in `docs/open-threads.md`.

## Commitments

### Scope

Skills, capped at what is actually used:

`interview` · `plan` · `ralplan` · `execute` · `handoff` · `ralph` · `autopilot` · orca orchestration

After v1: `research`. In scope and its use is clear — it answers a question someone asked and leaves a cited artifact behind — but it is not part of what the v1 gate measures.

Out of scope until the use is clear: `self-improve`, `autoresearch`. Both are wanted, and an unresolved use is a signal that the need has not arrived. `autoresearch` differs from `research` in exactly that way: it would have the harness decide on its own that a question is worth answering, which is a judgement nobody has specified.

Agents: the fourteen canonical roles, rendered for both vendors from one source.

**No skill may share a name with an `ocs` subcommand.** Cheap insurance rather than a live hazard: the CLI is `ocs`, the plugin is `kein`, and a command already cannot be mistaken for a skill on its prefix alone. Naming costs nothing at the moment a thing is created and everything afterwards, so the rule is kept as a habit and not as a defence against something currently happening.

### Non-goals

- Hooks. Start at zero. Adding one requires naming the failure it prevents and how its misfire would be detected.
- Restoring prompt material because an upstream harness had it.
- Reimplementing Orca's orchestration runtime, or shadowing the `orca` executable to add subcommands to its namespace. Composing its commands from `ocs` is not that, and is how the cross-vendor bridge reaches a supervised worker.

### Portability

A Codex port is planned. Whichever vendor leads, the experience should be as close to identical as the platforms allow.

Detail may differ for two reasons, and both are legitimate. A platform can force it — flags, sandboxing, which instruction files a runtime discovers. A model's temperament can call for it, where the same instruction lands differently on a different model and the wording has to change to mean the same thing.

What must not differ is the design. Two vendors doing the same work in two different shapes is the failure this guards against, not two wordings of one shape.

### v1 done

**Turn OMC off and complete one full round in `descvi` using only `kein` components:**
plan, implement, review, accept. Needing to re-enable OMC at any point means not done.

Development continues past v1. This is the first gate, not the finish.

## Why these commitments

Nothing below binds. It is here so that a later reader can tell whether a commitment above still has a reason, and delete it if it does not.

### The obsolescence lens

The argument that set this scope: execution harness has been retired by model capability, and only planning harness survives. It is a contested claim, not a settled one — hold it as the strongest available hypothesis rather than as a finding. It lands on half of this project either way, so it sets the scope rather than sitting beside it.

*Planning* here means the product-management layer — deciding what to build, what the policy is, how it should be shaped. It is not the `plan` skill, which is one implementation of a slice of it.

The measured evidence so far agrees. Porting OMC's Critic from 3,047 words to 1,115 changed no behaviour, and a three-line restoration of the removed severity floor changed nothing across ten samples under deliberate pressure. Prompt material that reads as load-bearing frequently is not.

Two of the argument's conclusions do not apply here, for reasons the source does not address:

- **Subagents are context management, not role division.** An explorer that reads a hundred files and returns three lines is compression, not a telephone game — the loss is the point. The 6x token figure describes re-sending shared context between agents, which is the opposite of isolated dispatch.
- **Cross-vendor calls are an ensemble, not self-critique.** "Run self-review three times and the first answer wins" holds when the reviewer shares the author's error correlations. A different vendor's errors are less correlated, so a second opinion adds information instead of flattening.

And the source states its own exception: a fixed, checkable criterion is where an external checker still earns its cost. The rule that a gate must be able to go RED is that exception stated as a repository invariant. Review rounds without such a gate are what the argument retires.

### What that classification produces

| Component | Kind | Consequence |
| :--- | :--- | :--- |
| `interview` | planning harness | the one class the argument keeps |
| `plan` | planning harness | the artifact survives even if the gate is retired |
| `ralplan` (`plan` + consensus gate) | verification | conditional on a gate that can fail |
| `execute` | execution harness | most exposed; carry fewer verification rounds over time |
| `ralph` | execution loop | a general-purpose loop |
| orca orchestration | cross-vendor | outside the argument's scope |
| the fourteen agents | context isolation | outside the argument's scope |

`autopilot` wraps `interview -> plan -> execute`, resuming at whichever stage has not been done, so it depends on those three and on nothing else.

### Why one prompt library rather than two

Canonical role prompts live in one place and both vendors render from it. A single resolver is what prevents the two vendors' prompt sets from drifting apart, and it is why `ocs` carries more than the bridge commands.

It also makes evaluation transferable: a measurement taken against the canonical prompt holds for both sides. Two prompt sets would mean two evaluations and no guarantee that a result on one applies to the other.

### Why state lives in the repository

Work products go under `<repo>/.agents/kein/`, resolved by `ocs state-dir`, and nothing is written that the user did not ask for. The objection to `.omc` was always the hook-generated state tree, not artifacts someone asked for.

`.agents/` rather than a `.kein/` of its own, because that is already the vendor-neutral namespace at both the project and home level. In the repository rather than a vendor's config home, because a run started from Claude should be resumable from Codex.
