# `execute` after its first real run

Everything here came out of one run: 2026-08-28, `--executor codex`, descvi phase-47 story S47-1. It was the first time `execute` had been exercised at all, and the first time `ocs team` dispatched a write-capable vendor lane. Nine commits repaired what it exposed. **None of the repairs has itself been through a run.**

## What the run did

The lead ran in `descvi/repo/phase-47-drag-reorder-in-kein`; the Executor was codex through `ocs team`. Two workers were dispatched; both stopped without completing; the owner killed both.

Stopping was the correct outcome and is worth reading before assuming the run failed. Worker #1 drove the mutation acceptance 42 named, found that one of its rows stayed refused before the predicate the acceptance claimed to measure, and declined to reword the gate or add a test to prop it up — which is exactly what its brief demanded of it. Worker #2 stopped for the same reason on the correction round.

Traces, as they were pasted into the session:

- `docs/artifacts/260828-kein-p47-execute-codex-kickoff.md` — invocation through dispatch, the lead's side
- `docs/artifacts/260828-kein-p47-execute-codex-message.md` — the package the worker received, plus its first moves
- `docs/artifacts/260828-kein-p47-execute-codex.md`

**These three were untracked when this was written.** If they still are, commit them before relying on anything above; phase-46's run ledger was lost exactly this way.

## What was repaired

Read the commit messages rather than a summary — each carries the observation it came from.

| | |
|---|---|
| `008acb3` | `ocs state execute start` |
| `a2bd619` | `--task-file` on `ask` and `team` |
| `a3dece5` | the vendor home was never "pristine"; a worker that does not signal held the terminal silently |
| `217c517` | `## At entry` injection for `execute` |
| `76a6d3e` | field-set mismatch names the difference; the `--check` thread closes |
| `42ddd22` | a second dispatch refuses while a worker holds the worktree |
| `88a7ce4` | naming the repository instructions is the repository's job |
| `4487c7b` | a lane runs without the operator's plugins |

## What to watch on the next run

Each of these is a claim made against one run's evidence and never tested by a second.

**`start` was never used.** The run that motivated it hand-authored its first checkpoint. Watch: does the lead reach for `ocs state execute start --run-root … --slug … --kind plan --input … --worktree … --tasks …`, or does it write a candidate JSON and call `checkpoint`? If the latter, the reference did not reach it and the fix is placement, not code.

**Does codex honour `-c 'plugins."X".enabled=false'`?** Unverified. The launch string's shape was checked; codex's response to it was not. Watch: whether the worker mentions a plugin's procedure at all. The incident that motivated this was a worker citing `superpowers`' dispatch rules as authority for not waiting on approval. `KEIN_CODEX_PLUGINS=inherit` turns the suppression off.

**The live-worker guard was tested against settled records only.** Both of the run's dispatches read `failed` once their terminals died, which is what proves a killed lane cannot lock the worktree. The refusing path — a present, unsettled status — has never fired. Watch: dispatch a second lane deliberately while the first runs, and confirm it refuses rather than launching.

**The unsignalled-report notice has never printed.** It fires when a report file exists while the dispatch has not settled, which is what worker #1 did. Watch for it in a backgrounded call's output and in `runs/team/<run>/command.txt`.

**Injection.** `ralplan`'s injection was confirmed working by a later run (the lead stopped fetching `--help` by hand). `execute`'s has not been. Watch: whether `ocs state execute --help` and `ocs state-dir runs/execute` still appear as hand-typed Bash calls.

## Still open

**The worker home is only half closed.** Plugins are suppressed by name; `~/.codex/AGENTS.md` and `~/.codex/memories/MEMORY.md` still arrive with the home, and worker #1's opening command was a grep over that MEMORY.md. Closing them means a home of the run's own, which needs a decision about how that home gets credentials — the vendor's auth lives where its home does. `KEIN_CODEX_HOME` is the existing way to point at one.

**`execute` has no transitions past `start`.** `ralplan` has seven; `execute` has `start` and then `checkpoint`, so every state after the first is hand-authored JSON against a fifteen-field shape. `start` closed the worst of it and the field-set errors now name what is missing, but the standing cost is still there. Whether it is worth transitions depends on how much a run actually checkpoints — the phase-47 run's ledger is the sample to count.

**`ocs team`'s 3600-second timeout is untouched.** Shortening it would be a number chosen against one run. A better signal may be the unsignalled-report notice above; see whether it makes the timeout moot before changing it.

**Two authoring slips in the brief the lead wrote** — a sentence that ends mid-clause before the report contract's numbered list, and a dangling "Later stories own those." Both are in `…-codex-message.md`. They belong to whoever writes the next brief, not to the harness.

## Where the rest of the context is

- `docs/open-threads.md` — `ocs ask`/`ocs team` argv (closed), the `--check` thread (closed, with what exercising it found), the pinned `--plugin-dir` thread that `command -v ocs` injection now mitigates
- `plugin/skills/execute/references/lanes.md` — the vendor-lane contract, including what the pinned home does and does not carry
- `plugin/skills/execute/references/state-schema.md` — `start` and `checkpoint`, and what `"auto"` fills
- `plugin/libexec/lib/vendor-home.sh` — the plugin suppression and its off-switch
