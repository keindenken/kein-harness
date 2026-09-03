# phase-48 run state, both harnesses — what is kept, what was recovered, what is gone

Taken 2026-09-03, the day both phase-48 worktrees closed. The rule is the one `260829-p47-run-state` set: **only what git would lose.** Both branches keep their tracked material; nothing committed is duplicated here.

| | |
|---|---|
| `kein-agents.tar.gz` | 1.3 MB, 100 files — `phase-48-kein/.agents/` whole, mtimes preserved |
| `kein-s48-1a-uncommitted.patch` | 278 KB — the S48-1a working tree as `git diff --binary` against `5a53259`, 16 files, 1,608 insertions / 708 deletions; `git apply --check -R` was clean when taken |
| `kein-s48-1a-worktree-files.tar.gz` | 476 KB, 17 files — the same 16 files as they stood plus the untracked `e2e/region-set-instrument.spec.ts`, which the patch cannot carry; mtimes preserved (last touch 07:53) |
| `omc-recovered/` | 256 KB, 36 files — `phase-48-omc/.omc/{artifacts/phase48-plan, state/sessions}` rebuilt from the omc lead's session transcript, see below |

## kein — what is inside the tar

`runs/ralplan/260902-013722-phase-48-bq5-handle-admission` (38 files) is the 18-round ralplan run: `state.json`, one plan and one findings file per round, the lane packages. `runs/execute/` holds the three execute runs (run1 and run2 aborted over input identity, run3 live at S48-1a correction round 5), the task ledgers, the frozen plan input, every task and correction brief. `reports/` is the twelve executor reports, whose mtimes are the round timeline. `runs/team/` is the ten codex dispatch packages; the two S48-1a ones stopped on the sandbox's `EMFILE` and the task moved to the native lane at 01:49. `skills/kickoff` is the one kickoff file.

The S48-1a patch is the six hours of work the run never accepted. It is not a deliverable; it is the material for the question of what five correction rounds bought.

## omc — the worktree was already gone

`phase-48-omc` had been removed before this archive was taken. Its branch `feat/phase-48-bq5-handle-admission` survives at `cc6f631` with the tracked `.omc/{plans,research,spikes,archive}`. The ignored `.omc/artifacts/`, `.omc/state/` and `.omc/sessions/` went with the directory.

`omc-recovered/` is what could be rebuilt from the lead session `~/.claude/projects/-Users-kein-Documents-workspace-dev-descvi-repo/2d904c1c-b443-4f29-a109-68b81d8b5e8e.jsonl` (2026-08-31 to 2026-09-03): every `Write` into those directories replayed with its later `Edit`s, and `progress.txt` rebuilt from its `Write` plus sixteen heredoc appends. That gives the whole ralplan lane trail (`planner-brief`, `architect-r1`, `critic-r1`, `revision-r1..r5`, `fresh-r2..r5`, `closure-r2..r6`, `approval-r6`, `review-common`), the execute briefs and reports (`exec-s48-0a..3`, `report-s48-1..3`, `verify-*`), the four post-code fix rounds (`fix-r1..r4`), and `prd.json`.

**Fidelity.** Four of these files had been read from disk by the harness session that took this archive, before the worktree went. `approval-r6`, `closure-r6` and `review-common` are byte-identical to the disk copies. `fresh-r5` was not (the lead edited it by a route the transcript does not carry) and the disk copy is what is kept. `fix-r3` differs from its disk copy in the first 24 lines and only the `Write`-time version exists; read it as the draft, not the final. One `Edit` to `progress.txt` did not match its base and was dropped. Everything else is the `Write`-time content and may have been edited afterwards without a record.

**Not recovered:** the gate logs and cross-vendor lane logs under `.omc/state/`, and `.omc/sessions/`. Nothing wrote them through a tool the transcript records.

## Branches are not pushed

`phase-48-kein` (`5a53259`) and `feat/phase-48-bq5-handle-admission` (`cc6f631`) both have no upstream. Everything above that says "preserved by the branch" means preserved on one machine, the same shape that lost phase-46's ledger and that the p47 archive warned about.

## Transcripts that survive outside the worktrees

Not archived here, because closing a worktree does not touch them: the kein execute lead at `~/.claude/projects/-Users-kein-Documents-workspace-dev-worktree-repo-phase-48-kein/15289c41-764c-4782-9d41-932badbefee6.jsonl` (18 MB, interrupted 07:59, resumed 13:34) and the omc lead named above.

## What this material is for

The phase-48 comparison. Both harnesses planned the same B-Q5 change with the same lead model: kein's ralplan closed in 18 rounds with the plan at 212 KB (§6 alone 45 KB), omc's in 5 plus a cap with a 12.7 KB gate section. omc then shipped S48-1+2+3 as one commit in 2 h 25 min and paid four fix rounds and an owner ruling after a live pass; kein's execute spent six hours and five correction rounds on S48-1a alone without accepting it. The findings files, the correction briefs and the recovered omc lane trail are the record of where each of those rounds went.
