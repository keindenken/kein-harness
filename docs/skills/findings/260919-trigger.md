# kein-findings: does the description fire when it should, and only then

Date: 2026-09-19. Plan: `.agents/kein/plans/findings-wiki.md` (S3, Gate G1). Arms ran Claude Code 2.1.276 at the start and 2.1.277 by the end (the CLI updated mid-session; read from each run's `system/init`). Arm model: sonnet. Run directories are under `../eval/` (the hub's eval root), named below.

## What was measured

Whether `kein-findings:findings` is invoked through its description alone (no slash command) on tasks that rest on a belief about an agent runtime, and stays out of tasks that do not. Each case gives the arm the `kein-findings` plugin only and a synthetic findings store copied outside the worktree; the synthetic findings carry markers no model knows (`FX-7Q`, `FX-3K`, `FX-9Z`), so an answer that cites one could only have come through the skill. Every count is `skills_invoked` from the arm's event stream, with-skill arm, three replicates.

Reproduce one case: `dev/kein-dev eval --case findings-trigger-direct` (add `--arm with-skill` to skip the control). Cases are `dev/eval/cases/findings-{trigger,hard,heldout}-*`.

## Gate G1 (first measurement, L0, both arms)

| case | fired (with-skill) | control inventory had the skill |
|---|---|---|
| direct | 3/3, answer cited FX-7Q 3/3 | 0/3 |
| implicit | 3/3 | 0/3 |
| quiet-unrelated | 0/3 | 0/3 |
| quiet-near | 0/3 | 0/3 |

D=3/3, I=3/3, Q=0/6: the pass row of the plan's G1 table, on the first draw, so the planned single revision was not needed. With the skill, the direct answer took 29–30 s against 64–91 s without it. Runs: `260919-022935`, `-023105`, `-023140`, `-023159`.

## Improvement loops

The four gate cases saturated, so the loops ran on harder cases added one set at a time, with-skill only unless noted.

| loop | change under test | result | runs |
|---|---|---|---|
| L1 | none; six hard cases | English indirect hook design 3/3 fired and cited FX-3K; with the kein plugin also loaded 3/3; translation of a subagents doc 0/3. A hook-script edit fired 3/3, each time reasoning that the payload field name is a runtime assumption. The case was built as quiet; the reasoning holds, and the cost was one `findings list` and about 10 s, so it is recorded as borderline rather than fixed. No store: 1/3 answers mentioned that no findings were recorded. A runtime question with no finding: 2/3 timed out at 600 s. | `023425`–`024636` |
| C1 | control for the last two | without the skill the unrecorded question took 60–91 s with no live `codex exec` calls; with it, 2–4 live `codex exec` probes per run. No-store control 131–146 s against 74–121 s with the skill. | `024908`, `025040` |
| L2 | the empty-list branch says an empty result says nothing about the runtime and does not belong in the answer; the record step checks only the new file | no-store mentions 0/3; unrecorded timeouts 1/3; direct and English unchanged | `025342`–`030627` |
| L3 | removed the opening line contrasting training with measurement | live probes unchanged (3–4 per run), 2/3 timeouts; hits unchanged | `030740`–`031818` |
| L4 | moved the record procedure into `references/record.md`, which a lookup never reads | 0/3 timeouts, live probes 1–4 per run | `031912` |
| L5 | description: "may already be recorded" instead of "measured" | unrecorded 3/3 graded, 0 timeouts, 135–190 s, live probes 2–4; direct 3/3, implicit 3/3, quiet-near 0/3 | `032640`–`033100` |
| L6 | held out: four prompts not used in tuning | an Orca review 3/3 fired and cited FX-9Z; a Korean SessionStart-hook plan 3/3 fired and each flagged that subagents would not see the hook (its grader looked for PLAN.md at the root, the arms wrote `fixture/PLAN.md`; the grader was corrected after); a unit test 0/3; an AGENTS.md summary 0/3 | `033155`–`033341` |

Over the whole run the skill fired on 57 of 57 replicates of a runtime question or design (counted per loop above, with-skill arms) and on 3 of 21 replicates built as quiet, all three in the hook-script case above.

## What is left

- On a runtime question the store does not cover, the skill still turns the arm toward measuring for itself: two to four live `codex exec` probes per run where the control ran none, and roughly twice the wall clock. Three wordings did not remove it, and the timeouts stopped after the record procedure left the main file. It is kept as a known cost rather than a defect: the answers were graded correct and none cited a finding that does not exist.
- Everything here is headless with one or two plugins. An interactive session with a long skill list is not measured; the plan's open question on sampling real sessions stands.
- The store was synthetic except for one manual query against the real store (12 findings), which picked `260808-mid-turn-message-delivery-differs-by-agent-mode.md`, named its version (2.1.226) against the running 2.1.277, and offered to rerun it.
- Two manual record runs wrote a valid finding, passed `findings check`, and committed in the store.
