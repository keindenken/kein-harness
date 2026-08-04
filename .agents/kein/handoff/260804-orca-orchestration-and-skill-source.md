# Handoff: Orca orchestration in the workflows, then the skill-source decision

**Date:** 2026-08-04

## Next-session objective

Two things, in order.

1. Put Orca orchestration into `skills/ralplan` and `skills/execute` — as guidance in the
   SKILL.md or as a shared reference file, not as a separate `team` skill.
2. Decide whether skills move to a single cross-vendor source. The gate for that decision
   was "after `ralplan` and `execute` are ported", and both are now ported, so the data
   exists.

## Start here

Read `docs/purpose.md` first. It carries the scope, the non-goals, the operating rules,
and the v1 done condition, and every decision below is recorded there rather than here.

Then, for objective 1:

- Orca already ships `orca-cli` and `orchestration` skills. The recorded decision is that a
  `team` wrapper would duplicate them, so read what those two actually contract for before
  writing anything into the workflows.
- `execute` has the natural insertion point: its review lanes are already selected per
  round, and read-only reviewers are already allowed to run concurrently. `ralplan`
  dispatches two blind lanes that are likewise independent.
- The constraint that must survive: an official review lane is a newly spawned agent that
  has seen no earlier findings. Whatever Orca adds must not turn a fresh lane into a
  resumed one.

For objective 2, the measured divergence from the Codex originals:

| skill | diverged lines | absorbed by the CLI | residual |
| :--- | ---: | ---: | ---: |
| `interview` | 6 | 4 | 2 |
| `ralplan` | 10 | 3 | 7 |
| `execute` | 11 | 6 | 5 |

All 14 residual lines are one of two kinds: agent-name namespacing (`Executor` →
`kein:executor`) and vendor API translation (`fork_turns: "none"` has no Claude
counterpart, because the Agent tool always starts fresh). **No policy diverged anywhere.**
That is the argument for a single source with a renderer that fills role names per vendor;
the counter-argument is that a renderer is machinery for 14 lines.

## Authoritative artifacts

- `docs/purpose.md` — why the harness exists, scope, non-goals, operating rules, order,
  and the open questions with their gates.
- `docs/prompt-porting-notes.md` — what the Codex port did to the omc/omx prompts and where
  it went too far.
- `.agents/kein/requirements/260803-kein-ask-bridge.md` — approved requirements for
  `ocs ask`, produced by `kein:interview`.
- `~/.codex-orca/docs/DECISIONS.md` — the decision log the ported workflows implement.
  Particularly the skill-to-agent dispatch boundary, which is what keeps authoring guidance
  in `planner.md` and orchestration in the skills.
- `~/.codex-orca/docs/superpowers/verification/agent-prompt-evals.md` — the differential
  evaluation method, and one rejected hypothesis. Read before restoring anything to a
  prompt on the strength of "omc had it".
- `README.md` — layout, load mode, where state goes, model routing, the `ask` contract.

## Current state

Working tree: `/Users/kein/Documents/workspace/dev/kein-harness`, loaded as
`kein@skills-dir` through a symlink at `~/.claude/skills/kein`. Nine commits, tip
`8297ce1`.

Skills: `interview`, `ralplan`, `execute`, `handoff`, `ping`. Agents: fourteen, generated.
CLI: `ocs` with `ask`, `state`, `state-dir`, `validate`, `sync-prompts`, `check-prompts`,
`render-agents`, `doctor`.

Verify the harness is intact before changing it:

```sh
ocs check-prompts     # prompts match canonical, agents match prompts
ocs doctor
```

Two things are deliberately unfinished:

- `~/.codex-orca` has uncommitted changes from this work: `foundation/manifest.json` gained
  a `tier` field, `foundation/tools/build_agents.py` validates it, and
  `foundation/tests/test_build_agents.py` covers it. Committing that repository is the
  owner's call. Its suite is 224 tests with one pre-existing failure in
  `test_skill_isolation`, unrelated to this work.
- The Codex side still runs the old `handoff` from `~/.agents/skills/handoff`, which writes
  to the OS temp directory. Only the Claude side was migrated.

## Open questions

- **Single-sourcing skills across vendors.** Data above. Fixed boundary: vendor coupling is
  absorbed by the CLI, never written into skill prose.
- **`kein:handoff` cannot be invoked by the model.** It carries
  `disable-model-invocation: true` from upstream, so a request to write a handoff fails
  with a tool error and only `/kein:handoff` works. This document was written by following
  the skill manually. Decide whether that flag stays.
- **superpowers' "No Placeholders" rule.** Not in `planner.md`, and its absence is a real
  partial gap — `Under-planning` catches "implement the feature" but not "add appropriate
  error handling". Treat as a candidate to measure, not a rule to restore.
- **Task granularity across vendors.** Settled as a non-issue: superpowers' *task* matches
  `planner.md`'s "few verifiable stages"; its 2–5 minute *step* is the inner TDD cycle,
  which `execute` defers to repository policy. Recorded here so it is not re-litigated.
- **Extracting the canonical prompt library out of `~/.codex-orca`.** Gate: when a second
  consumer needs it without the Codex home present.

## Suggested skills

- `orca-cli` and `orchestration` — read both before objective 1. They define what Orca
  actually contracts for, and the decision not to build `team` rests on them.
- `kein:ralplan` — if objective 1 turns out to need a design decision rather than an edit.
  It is also the subject of the change, so running it on itself is a real test.
- `kein:interview` — if objective 2 needs its boundaries drawn before implementing.
- `superpowers:verification-before-completion` — this harness claims verification
  discipline; nothing here should be reported as working without a command and its output.

## Conventions worth knowing

- State and work products go to `<repo>/.agents/kein/`, resolved by `ocs state-dir`. Never
  `docs/`, which is reserved for reference documentation. `runs/` is gitignored;
  `requirements/`, `plans/`, and `handoff/` are records.
- Prompts and agents under `prompts/` and `agents/` are generated. Edit
  `~/.codex-orca/foundation/prompts/` and run `ocs sync-prompts`; `ocs check-prompts` fails
  loudly if either copy drifts.
- Before adding a rule to a prompt because an upstream harness had it, measure it. The
  harness for that is `~/.codex-orca/foundation/tests/evals/agents/`.
