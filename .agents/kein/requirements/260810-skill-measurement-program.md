# Skill measurement program

Status: Approved
Date: 2026-08-10

## Context

`260804-skill-ab-eval-harness.md` built `ocs eval` and left it working but unused. Its own closing note says the instrument "is paused on cost, not on doubt": 22 of 23 plumbing checks passed, and each arm then ran 35 to 40 minutes on the *cheap* fixture with every model pinned to Sonnet, with `with-skill` killed at a 2400-second timeout after 238 turns. That figure covers a full draft-review-revision round rather than a single lane, which is the fact that makes the present scope affordable.

Two things changed since. `plan` now exists as a standalone skill, so a planning stage can be run without the review rounds that made the earlier measurement expensive. And `skill-creator` was read closely enough to name what `ocs eval` lacks: per-eval expectations, pinned input files, repeats per configuration, a per-assertion classification across configurations, and a version-over-version ledger.

The classification is the part that matters most here. `docs/prompt-revision.md` argues that a standing prompt grows monotonically because adding needs one incident while removing needs proof a failure no longer recurs, and that nobody collects the second. An assertion that passes with the skill and without it is exactly that proof: that part of the skill is doing nothing. This program is how that evidence starts being collected.

## Desired outcome

Two working instruments, each answering a question the other cannot, and one real result from each.

A conformance run reports, per skill, whether its process completes end to end on Haiku. A benchmark run reports, per assertion, whether a skill's presence changes the outcome — and reports honestly when it changes nothing.

## Scope

### In scope

- A conformance instrument that runs a skill on Haiku and reports whether its process completed, over the six skills that exist.
- A benchmark instrument that runs one stage of a workflow against a pinned input, with repeats per configuration, and classifies each assertion by how it behaved across configurations.
- A first benchmark subject: `plan` alone, as `/kein:plan` against no skill.
- Eval definitions placed by nature — self-contained ones inside the skill, environment-dependent ones outside it.

### Out of scope

- Opus, in either instrument.
- Benchmarking a whole workflow end to end. Whether a workflow follows its own process is the conformance question.
- Adopting `skill-creator` as a dependency, or reshaping `ocs eval` to match it.
- Content-ablation and cross-harness arms, which are deferred but must not be foreclosed.

## Requirements

- The conformance instrument reports a per-skill result on Haiku, and a failure is reported as the skill's difficulty floor rather than as a failed run.
- The benchmark runs a named stage against a pinned input, so that the stage under measurement does not inherit an earlier stage's variance.
- An eval carries expectations that are graded per run, not only the process-level plumbing checks `ocs eval` produces today.
- A configuration is run more than once, so that a consistent result is distinguishable from a variable one.
- Each assertion is classified by its behaviour across configurations, including the case where it passes in both — which is reported as the skill doing nothing there, not as a pass.
- A result in which no assertion discriminates is reported as such rather than presented as a successful measurement.
- An arm is represented so that a later content variant or a foreign harness can be an arm without the representation being rewritten.

## Constraints

- Sonnet for every benchmark arm; Haiku for conformance; never Opus.
- `ocs eval` keeps its existing paired arms, pinned fixture, worktree sanitisation, and plumbing checks. This program adds to that instrument rather than replacing it.
- A self-contained eval carries no machine-specific path. Anything needing an external repository stays in `.agents/kein/eval/`.
- The earlier program's environment findings still hold: a worktree excludes anything an arm could read as a reference implementation of the process, and the task text does not point an arm at existing artifacts.

## Decision boundaries

- Repeat count per configuration, and whether repeats run concurrently.
- Whether the per-assertion classification is computed or written by an agent. `skill-creator` assigns it to an analyst agent although it is a deterministic computation over per-expectation results; this harness is free to compute it.
- The concrete expectation set for the first fixture, derivable from that fixture's own `reference_commit`.
- The concrete representation of an arm, provided it admits a content variant and a foreign harness later.
- Whether the conformance instrument reuses `ocs eval --verify` or gets its own entry point.

## Acceptance criteria

- [ ] A planner-only benchmark runs at least three times per configuration and emits a per-assertion classification across them.
- [ ] At least one assertion discriminates between configurations; if none does, that outcome is reported explicitly as an insensitive instrument or an insensitive expectation set.
- [ ] A conformance run on Haiku reports, for each of the six existing skills, whether its process completed.
- [ ] An arm carrying a content variant can be expressed without changing how arms are represented, demonstrated by writing one such arm definition even though it is not run.
- [ ] A self-contained eval lives inside its skill and contains no path specific to this machine.

## Decisions and rationale

- **Two instruments rather than one:** conformance and benchmark ask different questions and cannot share a model. Haiku failing to follow a process is a finding about the skill's difficulty, and treating it as a failed benchmark would discard that.
- **One stage per benchmark run:** a stage handed a pinned input measures that stage. Recorded independently on 2026-08-05 — "reviewer lanes do not need a full run to compare", since a Critic is a leaf whose contract is a pure function of task, artifact, and review contract, and "a planner-only comparison is available and is worth separating out".
- **`plan` first:** its arm is skill-present against skill-absent, which `ocs eval` already implements, so the work concentrates on the assertion, repeat, and classification pipeline rather than on new arm machinery. It also gives the newest skill its first measurement.
- **Arms grow in three stages:** skill present against absent establishes the baseline; part of a skill's content present against absent is the ablation that produces deletion evidence; kein against another harness is the third. Building only the first is deliberate, foreclosing the others is not.
- **Eval location by nature, not uniformly:** the same criterion that split `plan` from `ralplan` — what a thing is decides who owns it. Stage decomposition is what makes an in-skill eval possible at all, since a planner-only fixture is a requirements document plus expectations and needs no external repository.
- **`evals/` inside a skill despite being unlike its neighbours:** `references/` and `scripts/` are the parts of a skill that do not change, and evals do. Recorded because that is the argument someone will use to move them out again; the answer is that they constitute the skill regardless, and keeping a rule's evidence beside the rule is what makes deleting the rule an ordinary review rather than archaeology.

## Relevant system evidence

- `.agents/kein/requirements/260804-skill-ab-eval-harness.md`: Approved. The instrument works; the pause was cost. Also records that a skill-free control reconstructed the workflow from artifacts left in the worktree, which is why the environment excludes them.
- `plugin/libexec/eval/run.py`: `ARMS` is `{"with-skill": inject True, "without-skill": inject False}`, so an arm is currently the presence of the plugin and nothing more. `check_plumbing` asserts process facts, not work-product quality.
- `.agents/kein/eval/fixtures.json`: both fixtures name an external repository and a planning task, so neither is self-contained.
- `skill-creator`, at `~/.claude/plugins/cache/claude-plugins-official/skill-creator/`: `evals.json` carries per-eval `expectations` and a `files` list, the latter being what makes a pinned-input stage fixture expressible; `run_eval.py` defaults to three runs per query; `aggregate_benchmark.py` computes mean, standard deviation, and a delta against baseline; the five-way per-assertion classification lives in `agents/analyzer.md` as an agent's reading rather than in code. Its SKILL.md prefers scripts to graders wherever an assertion can be checked programmatically.
- `docs/prompt-revision.md`: states the deletion problem this program's classification answers.

## Assumptions and risks

- **Structural assertions may not discriminate.** A control lead may well produce the same headings and status fields a skill asks for, in which case those assertions pass in both configurations. That is a real result about those instructions rather than a broken measurement, but it means the first run may return little and the expectation set will need a second pass.
- **Three repeats may not separate consistent from variable.** The count is a decision boundary precisely because it is a guess until a run has been observed.
- **Haiku may fall below the floor for every skill at once.** If nothing completes, the conformance instrument reports a floor above Haiku for all six and says little about any one of them. Still a result, but a coarse one.
- **The planner-only fixture is new.** The existing fixtures were built for a full round; a stage fixture and its expectations have never been exercised.

## Deferred items

- **Content-ablation arms and cross-harness arms.** Boundary: the first run must not make either impossible, which acceptance covers by requiring one variant arm to be expressible. Gate: once the assertion, repeat, and classification pipeline has produced one real result.
- **The `primary` fixture and any full-workflow benchmark.** Boundary: conformance remains the instrument for whole-process questions. Gate: not before a stage benchmark is affordable and calibrated.
- **`execute` as a benchmark subject.** Carried from 2026-08-04 unchanged. Gate: after calibration, since it is the more expensive fixture and the harder work product to judge.
- **A rewording round.** Carried from 2026-08-04. Gate: when a variant can be specified precisely enough to diff, and when calibration has shown the instrument sensitive enough to have a chance at the smallest effect class.
