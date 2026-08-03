# Porting agent prompts from omc/omx

Notes from comparing `~/.codex-orca/foundation/prompts/*.md` (14 roles, already ported
and normalized) against their OMC 4.15.7 and OMX 0.20.3 sources. Relevant to kein
because the same prompts are the porting candidates here.

## What the codex-orca port did

Sizes, in words. Line counts mislead — OMC hard-wraps, codex-orca keeps one line per
paragraph.

| role | orca | omc | omx |
| :--- | ---: | ---: | ---: |
| critic | 1,115 | 3,047 | 685 |
| code-reviewer | 831 | 2,005 | 1,570 |
| tracer | 712 | 1,589 | 1,219 |
| executor | 764 | 1,006 | 1,029 |
| planner | 1,098 | 1,151 | 1,119 |

All 14 roles were flattened onto one skeleton: `Role`, `Why_This_Matters`,
`Operating_Contract`, `Process`, `Success_Criteria`, `Failure_Modes`. Removed: model and
effort declarations, product tool names, `.omc`/`.omx` paths, workflow verdict
vocabularies, output templates, orchestrator-only routing, unverifiable pseudo-metrics.

`sandbox_mode` moved out of prose into the agent config, so read-only is enforced by the
runtime rather than by instruction. Worth keeping in kein — the Claude equivalent is
the agent's `tools` list, not a sentence in the prompt body.

## Where the reduction went too far

The normalization policy correctly targets product-specific material. It also removed
decision instruments that were not product-specific, replacing procedures with adjectives.

- **critic** — the plan-investigation rubric (assumption rating, pre-mortem, dependency
  audit, ambiguity scan, feasibility, rollback analysis) was supposed to move into the
  planning workflow. It did not arrive. `skills/plan/references/review-contract.md` is a
  packaging and response-shape contract; its Critic lane is one sentence. `pre-mortem`,
  `ambiguity`, and `feasib` return zero hits across the whole skill tree.
- **planner** still instructs the author to write a pre-mortem, but nothing gates its
  quality. Output required, verification absent.
- **tracer** lost the six-tier evidence-strength scale and its conflict rule, while the
  prompt still says to rank by evidence strength. The ranking is now undefined.
- **critic** lost the fixed perspective sets (security / new-hire / ops; executor /
  stakeholder / skeptic), replaced by "choose perspectives that expose distinct risks".
  The original existed to force lenses a reviewer would not naturally adopt.
- **Examples** survive in 2 of 14 roles; OMC had them in 13 of 14.

## What measurement said

One hypothesis from this list has been tested and rejected. A three-line restoration of
the Critic's severity floor and asymmetric-loss framing produced no behavioural change
across 5 replicates per variant, on a fixture where the plan pre-assessed a data-loss
defect as minor under deadline pressure. Both variants returned MUST_FIX with the defect
ranked first at critical severity in every sample.

Full record: `~/.codex-orca/docs/superpowers/verification/agent-prompt-evals.md`.

The lesson generalizes. A gap found by reading two prompts side by side is a hypothesis,
not a defect. Persona-intensity language and severity scaffolding appear to be carried by
current models without explicit instruction. The untested items above may fall the same
way — do not restore them into kein on the strength of "OMC had it".

## Carry into kein

1. Port from `~/.codex-orca/foundation/prompts/`, not from omc. The vendor-neutral pass
   is already done and the omc residue is already gone.
2. `executor.md` is the cleanest of the fourteen and needs no rework.
3. Before restoring anything the codex-orca port dropped, run the differential first.
   The harness is at `~/.codex-orca/foundation/tests/evals/agents/` and is model-agnostic
   in shape; only the invocation line is Codex-specific.
4. Keep prompts free of repository-instruction assumptions. None of the 14 mention
   `AGENTS.md` or `CLAUDE.md`, which is correct inside a workflow that injects repository
   context into the brief, and a gap on a bare one-shot bridge call. A bridge prompt needs
   three layers, not two: role prompt + repository instructions + task brief.
