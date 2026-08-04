# Real-environment A/B evaluation harness for kein skill changes

Status: Approved
Date: 2026-08-04

## Context

The kein harness has ported `interview`, `ralplan`, and `execute`, and is about to gain Orca orchestration inside `ralplan` and `execute`. That pending change targets the harness's most sensitive invariant: an official review lane must be a newly spawned agent that has seen no earlier findings.

Nothing in the repository can currently observe whether a skill change moved behaviour. The existing coverage stops at the workflow boundary, as `~/.codex-orca/docs/superpowers/verification/agent-prompt-evals.md` records: the 223-test suite validates state machines and dispatch, and `smoke_agents.py` validates that each role returns a protocol-conforming line, but neither can see whether a role's judgement changed when its prompt changed.

Workflow-level evaluation scenarios already exist for `interview`, `ralplan`, and `execute`, complete with replicates, pressure tags, and hidden rubrics. No runner exists for any of them. They also score a *described* procedure rather than observed behaviour, because their prompts ask the subject to state what it would do.

This work builds the missing instrument, and does so while the harness is still at a pre-feature baseline so that later changes have something to be measured against.

## Desired outcome

A repeatable evaluation that runs two arms of a real Claude session against an identical starting state, in the real environment rather than a synthetic prompt fixture, and produces a durable record from which two questions can be answered: whether the arms differed in process compliance, and whether they differed in work-product quality.

## Scope

### In scope

- An evaluation surface that runs N arms by M replicates from a fixed commit and records, per run, the arm identity, the resolved skill variant, the run's state artifacts, and the final work product.
- Process compliance extracted from durable run state without manual reading.
- Work-product quality judged by a newly spawned same-vendor Claude agent, blind to arm labels, comparing arms pairwise.
- One minimal calibration run, skill-present versus skill-absent, at one replicate per arm.
- The opening ablation as the first exercise of the instrument: `ralplan` with an addition-direction ablation against `prompts/planner.md`.

### Out of scope

- The Claude-side launcher (`orclaude` / `kclaude`). Deferred to its own scope.
- A rewording round that varies phrasing while holding policy fixed.
- Objective verification of agent freshness from external spawn records.
- An `execute` round.
- Any change to the skills themselves beyond the ablation variants the evaluation constructs.

## Requirements

- Every arm and every replicate starts from a byte-identical repository state, established by pinning a real repository at a fixed commit.
- The two arms differ by exactly one thing: the presence or absence of the ablated section. Every other input is identical, and the difference must be inspectable as a diff before the round runs.
- The skill variant reaches the session through `--plugin-dir`, pointing at the `plugin/` directory of two kein-harness checkouts that differ only in the ablated section.
- Runs execute in the real environment — real `claude`, real Orca worktrees, a real loop against a real repository.
- The judge receives outputs with arm labels stripped, and its input must be inspectable to confirm this.
- The calibration run establishes whether the instrument registers a known-large difference, and its result is recorded as the reference point for later rounds.
- A round produces a written result record naming the variant diff, the replicate count, per-arm process compliance, the judge's verdicts, and whether the conclusion is interpretable given the calibration outcome.
- Where a round bounds its own coverage — replicate count, a single fixture, a single task shape — the record says so rather than presenting the result as general.

## Constraints

- `docs/purpose.md` non-goal: "Growing the skill count. Six is the working ceiling." Five skills exist and the v1 scope list already claims `ralph` and `autopilot`, so no skill slot is available for an evaluation surface.
- `docs/purpose.md` rule: no skill may share a name with an `ocs` subcommand.
- `docs/purpose.md` non-goal: "Replacing Orca's command namespace or reimplementing its orchestration runtime."
- Prompts under `prompts/` and agents under `agents/` are generated. The canonical source is `~/.codex-orca/foundation/prompts/`, and `ocs check-prompts` fails when either copy drifts. An ablation variant must not be produced by hand-editing a generated file in a way that leaves the drift check red for reasons unrelated to the experiment.
- The evaluation must not require the deferred launcher, and must not absorb a launcher's responsibilities.

## Decision boundaries

- The evaluation surface is an `ocs` subcommand rather than a skill. The skill ceiling leaves no slot, and a CLI surface does not compete for one.
- The fixture repository is not kein-harness itself, so that arms do not modify the harness under test.
- The fixture task is a specification-to-plan task, matching the opening ablation's subject; its work product is a plan document, which a judge can compare as text.
- Replicates start at three per arm for the ablation and one per arm for the calibration, and rise only when a result is borderline.
- The implementer chooses how the two checkouts are materialised — worktree, clone, or overlay — provided the diff between them is exactly the ablated section.

## Acceptance criteria

- [ ] A round can be launched from a single command and produces, per run, a durable record containing arm identity, the resolved skill variant, the run's state artifacts, and the final work product.
- [ ] The diff between the two arms' plugin directories is exactly the ablated section, demonstrated by a diff command and its output.
- [ ] Process compliance is derived from run state programmatically, with no manual transcript reading.
- [ ] The judge's input contains no arm labels, demonstrated by inspecting the recorded judge input.
- [ ] The calibration run completes and its outcome is recorded as either "instrument registers a known-large difference" or "instrument did not register a known-large difference".
- [ ] When the calibration did not register a difference, the round's report states that its ablation result is uninterpretable rather than reporting a conclusion.
- [ ] The round's result record names every bound on its own coverage, including replicate count, the single fixture, and the single task shape.
- [ ] `ocs check-prompts` and `ocs doctor` pass after the work, so the evaluation surface has not disturbed the generated-artifact invariants.

## Decisions and rationale

- **Real environment over a synthetic one-shot fixture:** skill process is an orchestration-dependent property, and a one-shot prompt fixture cannot observe it. The existing eval's own record states that its routing smoke supplies the expected evidence terms inside the lead prompt, so coverage stops at the workflow boundary.
- **Two independently shippable deliverables, evaluation first:** the launcher and the evaluation share a spawn surface but not a purpose. Building the evaluation first means the launcher later inherits a demonstrated flag set rather than a guessed one.
- **Fixed-commit fixture, throwaway output accepted:** work-product quality was deliberately weighted, and it is the noisiest observable. A differing start state would make a quality difference unattributable. The rejected alternative — running the arms on genuinely pending work — yields one replicate per arm and produces an anecdote.
- **Environmental fidelity is preserved under a fixed start:** what was rejected was the synthetic prompt fixture, not a fixed starting point.
- **Two observables, not one:** state-derived process compliance is the gate that can go RED, which `docs/purpose.md` identifies as where an external checker still earns its cost. Work-product quality is a weighted co-primary, because dropping it removes the only means of measuring whether the harness earns its cost — the question `docs/purpose.md` puts under the obsolescence lens.
- **Section ablation in both directions:** addition, where another plugin's equivalent prompt carries a section kein lacks; deletion, where a section has no counterpart elsewhere. The addition direction implements an operating rule the project already holds, which is to measure imported prompt material rather than restore it.
- **Skill-present versus skill-absent rejected as the round's variable, retained as calibration:** as a finding the difference is too obvious to be worth the inference, but as a ruler it is exactly what is needed. The existing eval record contains two null results that cannot be separated from instrument insensitivity, and one calibration run removes that ambiguity for every later round.
- **Same-vendor judge first:** `docs/purpose.md` argues cross-vendor review adds information because a different vendor's errors are less correlated. Measured experience in the `descvi` project qualifies this: a freshly spawned same-vendor Claude reviewer achieves a comparable effect, the two sometimes surface the same finding and sometimes different ones, and when they differ, whether the `gpt-5.6-sol` or the Claude material is more valuable varies case by case. The operative variable is reviewer freshness, which `purpose.md`'s argument did not separate from vendor difference. Cross-vendor judging through `ocs ask codex` remains available as a check.
- **The opening ablation is `ralplan` against `planner.md`, addition direction:** the fixture is cheap because it produces a document rather than a diff, and the work product is text a judge can compare cleanly.
- **The opening ablation's proposition is restated:** repository inspection contradicts the premise recorded in the handoff. The round no longer asks whether filling a missing rule helps; it asks whether an explicit narrow rule adds anything where a general rule already arguably covers the case. Under this framing a null result is informative, because it supports the standing operating rule against importing prompt material on the strength of another harness carrying it.
- **Proceeding despite low expected discriminating power:** the difficulty of measuring this effect is accepted and is itself the record worth having, because it has never been attempted here. Absent this method, the available means of improving skill and agent prompts are too limited to rely on.

## Relevant system evidence

- `skills/execute/scripts/state.py:64`: `VERDICT_FIELDS` persists `fresh`, `independent`, `reviewer_role`, `round`, and `worktree_fingerprint` per verdict; `ACCEPTANCE_FIELDS` persists `reviewers`. The invariant that pending Orca work endangers is already instrumented in durable state.
- `skills/execute/scripts/state.py:197-215`: enforcement is partial and its boundary is exact. A `worktree_fingerprint` mismatch (line 209) and a `round` mismatch (line 208) are rejected, so a verdict provably covers the live tree at the stated round. `fresh` and `independent` are only type-checked as booleans (line 213), so freshness is a self-declared claim.
- `skills/ralplan/scripts/state.py:66`: `VERDICT_FIELDS` is `{"lane", "verdict", "plan_sha256", "reviewed_at"}`. `ralplan` records neither `fresh` nor `independent`, so the opening ablation's state-derived observable is narrower than `execute`'s would be.
- `skills/ralplan/scripts/state.py:286,383`: "Approved requires fresh PASS verdicts from both lanes" and "Opening In Review must advance to a fresh round with empty verdicts". Verdict freshness is enforced by the state machine rather than self-declared, even though agent freshness is not recorded.
- `prompts/planner.md:56,59`: "Under-planning: writing a directive such as 'implement the feature' without boundaries or acceptance criteria" and "Untraceable validation: saying 'test thoroughly' without a command, observable behavior, or failure condition". A grep for `placeholder`, `TODO`, `appropriate`, `as needed`, and `etc.` over `planner.md` returns nothing.
- `~/.codex-orca/foundation/tests/evals/`: `interview/`, `ralplan/`, and `execute/` each hold a `scenarios.json` with replicates, pressure tags, and hidden rubrics. No runner exists for any of them; `agents/run_agent_eval.py` is the only runner.
- `~/.codex-orca/foundation/tests/evals/ralplan/scenarios.json` and `execute/scenarios.json`: rubrics include "uses fresh blind Architect and Critic over the complete revised plan", "does not expose prior findings", and "uses at least one newly spawned blind reviewer for official re-review".
- `~/.codex-orca/docs/superpowers/verification/agent-prompt-evals.md`: a three-line prompt overlay produced no measurable difference across five replicates per variant under deliberate pressure.
- `docs/purpose.md`: records that porting the Critic from 3,047 to 1,115 words changed no behaviour, and concludes "Prompt material that reads as load-bearing frequently is not."
- `claude --help`: `--system-prompt[-file]`, `--append-system-prompt[-file]`, `--plugin-dir`, `--settings`, and `--agents` all exist.
- `descvi` at `c60be28` is the point where primed re-review was abandoned. Primed re-review asked a returning reviewer to confirm whether its own earlier finding had been addressed; dropping it is what led to this harness's `ralplan` and its blind lanes. The fixture pin is therefore the birth point of the invariant the harness is built on, which is also why plans in `.omc/plans/` at that pin were produced under the older regime and are exemplars of output shape rather than of process.
- `717edcb` shows information loss across the decomposition: the first plan document records what went wrong per iteration, and the split `ralplan-e3-v21a-undo.md` drops that record. A judge looking for plan quality has a concrete thing to look for here.
- A model's self-report is not admissible as a plumbing check, measured 2026-08-05. Asked whether an omc capability was available, both arms answered yes while `claude plugin list` in the same worktree reported the plugin disabled; the model was reporting what the instructions it had read described, not what it could invoke. Configuration-derived checks are the authority, and the model probe is corroboration with its question narrowed to what is invocable.
- `--plugin-dir` bypasses the `enabledPlugins` gate, measured 2026-08-04. A headless `claude --plugin-dir <path> --model sonnet -p ...` in a project where kein is disabled returned the `kein:ping` line, so an arm receives the plugin explicitly while the ambient default stays off. This is what makes a genuinely skill-absent control arm possible.
- A plain subdirectory is not isolation, measured 2026-08-04. Claude Code scopes settings from the working directory, so a subfolder does not inherit the parent's `.claude/settings.json`; but `ocs state-dir` resolves through `git rev-parse --show-toplevel`, which walks up to the nearest `.git` and lands on the parent repository. The two roots diverge, and only a worktree or clone makes them agree.
- Plugin discovery has no project-level equivalent, measured 2026-08-04. A probe plugin planted at `<project>/.claude/skills/probe/.claude-plugin/plugin.json` never appeared in `claude plugin list`, so only a *user* skills directory registers a plugin. Per-project control happens at the activation layer through `enabledPlugins`, not at discovery.

## Assumptions and risks

- **~~The plugin is user-scoped and therefore active in every project.~~ Resolved 2026-08-04, after approval.** The risk was that a skill-absent calibration arm would still have kein loaded, making the control arm invalid. Activation is now opt-in: `~/.claude/settings.json` carries `"kein@skills-dir": false` and this repository opts itself in through its own `.claude/settings.json`. Verified by `claude plugin list` reporting `Status: loaded` inside kein-harness and `Status: disabled` from an unrelated project. A control arm must still assert the absence rather than assume it.
- **`ralplan` does not record agent freshness**, so the opening ablation's compliance observable is narrower than `execute`'s. Verdict freshness is enforced structurally, and that is the whole of what the state can show.
- **Three replicates per arm will not resolve a small quality difference.** Given the effect sizes this harness has already recorded, a null outcome is the most likely single result.
- **A single fixture task bounds the conclusion to that task shape.** Nothing measured here generalises to other task shapes without another round.
- **The judge shares error correlations with the arms**, being the same vendor. This was accepted on measured grounds, and `ocs ask codex` remains available as a cross-check.
- **The handoff's recorded gap in `planner.md` appears not to exist as stated.** That proposition was restated to survive this, but the same doubt may apply to other candidates drawn from the handoff's open questions.
- **The existing `scenarios.json` rubrics score a described procedure, not observed behaviour**, so they cannot be reused unchanged as this harness's compliance criteria.

## Environment decisions, settled 2026-08-05 after approval

These extend the approved requirements rather than revising them. Where one narrows a recorded decision boundary, it is noted.

- **Models. Corrected 2026-08-05 after a first task run.** "The arms run on Sonnet" was false as implemented: `--model sonnet` sets only the lead, and a subagent's `model:` frontmatter wins. `planner`, `architect`, and `critic` all carry tier `deep`, so `ralplan` was dispatching three Opus lanes under a Sonnet lead. Two consequences. Cost: roughly a third of a five-hour window went in twenty minutes on the cheap fixture. The second consequence was narrower than first recorded. The control's plan was authored by its own Sonnet lead, and the haiku `Explore` it summoned only gathered material, so the arms did not differ by model across the board. What differed was the model that authored the plan — Opus in `with-skill`, Sonnet in the control — which is the part that bears on the comparison, and pinning every tier to the arm model settles it. A difference in whether `Explore` is used at all remains, but that is a difference in tool use rather than a model confound. Every agent's model must be pinned to the arm model for the run, so lead and lanes match and the only variable is the one under test.
- **Models, as intended.** The arms run on Sonnet end to end, the judge on Opus. The asymmetry is deliberate and favours detection: a judge stronger than the authors is more likely to see a difference than to manufacture one. Neither model was named in the approved text.
- **Fixture.** `descvi`, pinned at `c60be28` (2026-07-17). The spec input is `.omc/specs/deep-interview-e3-v21-insert-undo.md`, 296 lines, already present in the tree. The task is to produce the consensus plan for E3 v2.1a undo. `.omc/plans/` holds eight plans from earlier phases at that pin and none of the v2.1 set, so the arms see the project's house style while the target artifact is absent.
- **The next commit is a reference, never a score basis.** `717edcb` is one commit and the same day later, but it carries the output of more than twenty planning iterations, and it records that consensus was never reached — `open-questions.md` runs to 189 lines, and the combined plan survives alongside the split one. It is the point where planning was abandoned in favour of resolving the rest during implementation. Scoring against it would reward an arm that fakes a clean single plan, which is further from the real outcome rather than closer.
- **The a/b/c decomposition is not derivable from the spec.** The split into undo, insert, and publication emerged from the planning process itself. An arm producing one combined plan is not wrong; it is where the original stood partway through.
- **Contamination control.** `.claude/settings.json` is tracked at the pin and enables `oh-my-claudecode@omc`, and `.claude/skills/omc-reference/SKILL.md` is tracked as a project skill. Both are disabled or removed in every arm.
- **A third contamination source, found during the smoke and more dangerous than the other two.** `.claude/CLAUDE.md` carries a delimited `OMC:START`/`OMC:END` block, 61 of its 137 lines, and that block restates in prose the invariants kein's `ralplan` enforces: keep authoring and review as separate passes, never self-approve in the same active context, verify before claiming completion. Disabling the plugin does not remove it, because it survives as project instructions. A control arm that keeps it is not skill-absent in any meaningful sense, and the calibration's expected difference would collapse toward zero — defeating the one thing the calibration exists to establish. Only the delimited block is stripped; the remaining 76 lines are genuine project grounding the task needs, and they stay. A second harness's planning guidance sitting in the same session can mask the ablated rule and manufacture a false null, which is precisely the outcome the calibration exists to make interpretable. `enabledPlugins` handles the plugin; the project skill must be removed from the worktree, because project-level skill discovery works where project-level plugin discovery does not.
- **Isolation.** Each replicate gets its own `git worktree add --detach` at the pinned commit, prepared by the harness before the arm launches. This narrows the approved boundary that allowed worktree, clone, or overlay. Arms never create their own worktree, because a worktree made inside a session is a variable the harness does not control and would differ per arm.
- **The observable is sharpened for this ablation.** Alongside the two approved observables, the count of unbounded directives in the produced plan is recorded. Holistic quality faces a floor here: every arm falls far short of a twenty-iteration outcome, and that gap is dominated by task difficulty rather than by the ablated section. Vagueness density can still separate the arms when absolute quality cannot, and it is close to countable, so it can go RED.
- **A smoke fixture, distinct from the calibration.** `073e96d` → `538b2d9`, a 108-line spec and a 68-line plan that reached consensus in two critic iterations, exercises the plumbing: worktree isolation, omc suppression, plugin injection, blind judge input, artifact capture. It does not validate instrument sensitivity, which is fixture-dependent, so the calibration stays on `c60be28`.
- **Rounds are bounded at two, by instruction rather than by enforcement.** The limit lives in the shared task text so both arms receive it identically and only the invocation differs. Nothing in the CLI can hold a lead to it, and a lead may also end its turn before a second review lands. That is tolerable because the actual round count is recorded from run state, which turns non-compliance into an observation rather than a spoiled run — and compliance with a stated process bound is itself a thing worth measuring. `--max-turns` sits at 500 as a runaway backstop only; a run that produced a plan took 135 assistant turns, and the flag cannot reach a subagent's own turns in any case.
- **A shared worker brief was considered and declined for now.** The `descvi` project keeps one, and sending it with every lane would suppress lead-to-lead variation. It does not exist at either pinned commit, so including it would be a treatment decision rather than a fixture property, and it is planning-process guidance of exactly the kind already stripped from the worktree. The decisive objection is that a worker brief is partial skill: giving it to the control arm hands the control part of what the treatment provides, shrinking the very difference the calibration exists to establish. Revisit once replicates show how much lead-side variance there actually is.
- **Replicate count is set by the calibration, not before it.** The approved default of three per arm is suspended until the calibration reports real cost and duration on this fixture.

## Where this stands, 2026-08-05

The instrument works and is paused on cost, not on doubt.

A task run on the cheap fixture passed 22 of 23 plumbing checks. The workflow entered through its slash invocation, dispatched five `kein:` lanes, all synchronous, kept its ledger inside its own worktree, and opened no session outside it. The one failure was a mis-scoped check, since the control has no rule requiring synchronous dispatch; it now reads as an observation for that arm, and an interesting one, because a bare lead does the risky thing the rule exists to prevent.

Cost is the blocker. Each arm ran 35 to 40 minutes on the *cheap* fixture with every model pinned to Sonnet — `with-skill` was killed at a 2400-second timeout after 238 turns, and the control finished at 2090 seconds after 225. The original work behind that fixture reached consensus in two critic iterations and shipped a 68-line plan; the arms produced 193 and 144 lines. The `primary` fixture represents more than twenty planning iterations, so it is not viable under this design, and the calibration that was to set the replicate count is itself now in question.

Three findings worth keeping regardless of when this resumes.

- **The control reconstructed the workflow from artifacts.** Without any skill present it ran Explore, drafted a plan itself, and moved toward Architect — apparently by imitating the process recorded in the status lines of existing plans. That is a real property of the repository, not a leak, and it speaks directly to the obsolescence question `docs/purpose.md` raises. `.omc/plans` and `.omc/archive` are now excluded from every worktree so a calibration can still establish a known-large difference, and the task no longer directs an arm to follow existing plan conventions — that sentence handed the control a template, and the template is part of the treatment.
- **The state ledger is a weak process observable for `ralplan`.** Its verdict fields are cleared on a block by contract and never filled when a run stops mid-round, so every file in a completed run held nulls. The event stream and the per-subagent transcripts under the pinned config home are the strong record, and they showed each lane's role, model, and synchronicity directly.
- **Reviewer lanes do not need a full run to compare.** `agent-prompt-evals.md` already establishes why: a Critic is a leaf whose contract is a pure function of task, artifact, and review contract. Comparing Architect and Critic against another harness's equivalents is therefore cheap and needs no orchestration; what is expensive, and what needs the whole workflow, is the orchestration itself.

When this resumes, the environment should exclude anything an arm could use as a reference implementation of the process, so that a run is genuinely skill against no-skill, skill against skill, or skill against another vendor's skill. A planner-only comparison is available and is worth separating out: dropping the review lanes measures authoring rather than verification, which `docs/purpose.md` classifies as the durable half, so it is a different experiment rather than a cheaper one.

## Deferred items

- **The Claude-side launcher (`orclaude` / `kclaude`).** Fixed boundary: the evaluation must not require it, and must not absorb its responsibilities. Gate: taken up once the evaluation has settled which spawn flags actually matter in practice. Independent motivation unchanged — replacing the session-start `kickoff` skill invocation with `--append-system-prompt-file`, symmetric to the `orcodex` entry already recorded in `docs/purpose.md`.
- **A rewording round.** Gate: when the variant can be specified precisely enough to diff, and when the calibration has shown the instrument is sensitive enough to have a chance at the smallest of the three effect classes.
- **Objective verification of agent freshness from an external spawn record.** Fixed boundary: until then, freshness is read as a claim, not an observation. Gate: when a self-declared value is seen to diverge from an actual spawn, or when Orca orchestration lands in the review lanes.
- **An `execute` round.** Gate: after the calibration has validated the instrument, since `execute` is the more expensive fixture and the harder work product to judge.
- **~~Restructuring the plugin so it activates only within kein-harness.~~ Done 2026-08-04, after approval.** The plugin source moved to `plugin/`, so `docs/`, `README.md`, and the `.agents/` state tree are no longer inside what Claude Code loads, and the symlink was retargeted at `plugin/`. Artifacts still land at the repository root because `ocs state-dir` resolves through `git rev-parse --show-toplevel`. This closes the first risk under Assumptions and risks.
