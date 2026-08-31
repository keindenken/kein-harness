# phase-47 run state, both harnesses — what is kept and what is not

Two archives of the run state the two phase-47 attempts left in `descvi/repo`, taken 2026-08-31 so that the harness comparison has material after the worktrees go.

They are **curated, not complete.** What follows is the coverage record: read it before concluding that something is missing rather than excluded.

| | |
|---|---|
| `kein-agents.tar.gz` | 502 KB — `phase-47-drag-reorder-in-kein/.agents/`, minus the `ralplan` run |
| `omc-omc-state.tar.gz` | 2.3 MB — `phase-47-drag-reorder-in-omc/.omc/{state,artifacts,sessions,project-memory.json}` |

## The rule that decided what went in

**Only what git would lose.** Both branches carry their own tracked material, so anything committed is preserved by the branch and duplicating it here would be two copies to keep true.

That rule cut most of the volume:

- omc's `.omc/archive/` (6.5 MB, **353 tracked files**), `plans/` (1.7 MB, 9), `research/` (864 KB, 31), `specs/` (2), `spikes/` (23) — all in git on `phase-47-drag-reorder-in-omc`.
- kein's `runs/ralplan/260827-235007-phase-47-drag-reorder` (2.0 MB, 33 files) — already at `docs/artifacts/ledgers/260827-235007-phase-47-drag-reorder` in this repository. Compared file by file before excluding: **33 of 33 byte-identical**.

**The branches are not pushed.** `phase-47-drag-reorder-in-kein` and `phase-47-drag-reorder-in-omc` both had `upstream=NONE` when this was written, so "preserved by the branch" currently means preserved on one machine. That is the same shape that lost phase-46's run ledger. These archives do not cover it — the branches themselves still need pushing.

## What is inside

**kein** — 56 entries. `reports/` is the executor and lane reports; `runs/ask`, `runs/team`, `runs/execute` are the dispatch traces. The `ralplan` run is deliberately absent, per above.

**omc** — 258 entries. `state/` holds the gate logs (`gates-*.log`, e.g. `gates-final.log` at 3,432 lines of CI step output), the cross-vendor lane output (`codex-*.log`), the round backups, the measurement spike's own rig (`probe-r3/`, 39 files), and `p47-edit-map.json`. `artifacts/ask/` is three cross-vendor review-lane transcripts, 3.5 MB before compression. `sessions/` is two small session records.

## mtimes are evidence, which is why these are tars

`260829-kein-p47-execute-claude.md` reads its entire round timeline from the mtimes of `.agents/kein/reports/`. Committing those files as files would have destroyed that timeline; `tar` keeps it. Spot-check: `260829-143446-executor.md` carries `Aug 29 14:36`, which is the retrospective's R2 row.

What is already gone, and was before this: that document records the per-lane transcripts under `/tmp` as cleaned and unrecoverable, and the per-lane wall-clock durations as surviving only in one session's context.

## What this material is for

The open measurement is a cross-check of each run's recorded defects against the other's tree — four cells, and one is already filled: kein's most expensive finding, the document-wide `#dsh-reorder-layer` lookup behind a `replaceChildren()`, does not exist on the omc side at all. omc built a headless model (`reorder-model.ts`, `reorder-drag-machine.ts`) and never created that DOM host, so there was nothing there to find.

Both runs also recorded gate defects of the same class — kein's four, and omc's own `S47-4` ("two gates that were lying") and `S47-5` ("the regression pnpm gates could not see"). The gate logs in `omc-omc-state.tar.gz` are the record of what those gates actually printed.
