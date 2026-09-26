# RALPLAN Cross-Vendor Lanes

Read this only when the invocation names a vendor for a lane.
A run without such a flag uses the native lanes described in the skill body and needs nothing here.

## Roster

`--reviewer <vendors>` takes a comma-separated vendor list and defaults to `claude`. It applies to both review roles at once, Architect and Critic, the same way `execute` applies it to whichever reviewer roles a round selects.

| Flag | Effect |
| :--- | :--- |
| `--reviewer claude` | the native lanes, identical to passing nothing |
| `--reviewer codex` | both native lanes are replaced |
| `--reviewer claude,codex` | each role runs in both vendors, all four lanes blocking |
| `--reviewer claude,codex:advisory` | the codex lanes report but cannot block |

A vendor suffixed `:advisory` records a verdict and contributes findings without gating approval.
Every unsuffixed lane blocks, which is the rule the skill body already states for the native pair.

`--planner codex` belongs to the `/plan` skill, and this skill passes it through.
The first draft comes from the codex Planner `/plan` starts with `ocs team`, and every revision resumes that same worker, so it revises the plan it wrote instead of re-reading it cold: `ocs team codex --resume <run-dir> --task-file <the correction brief>`, where `<run-dir>` is the directory the last Planner invocation printed. After a compaction or a resume, that is the newest `runs/team/*-planner` under this tree's `ocs state-dir` whose `command.txt` carries a `session=` line.
`ocs ask` cannot serve Planner: it runs the vendor read-only and refuses a role that writes.
`codex` is the only other vendor; refuse any other `--planner` value and say so rather than silently planning natively.

## Mechanism

```sh
ocs ask codex --agent <role> --trace --task-file <the lane package>
```

Write the package to a file and name it. A review package is a document — the first measured cross-vendor round wrote 646 lines and a wrapper script to get it through `argv`, which is what `--task-file` replaces. `-` reads standard input.

The mechanism is not a choice to make.
`ocs ask` runs the vendor in a read-only sandbox and refuses a write-capable role for `--agent`; Architect and Critic are both read-only, so every review lane here goes through it.

`ocs ask` pins the vendor home to `KEIN_CODEX_HOME`, and without it the operator's own `~/.codex`, so a lane reads the skills that home's plugins publish, its `AGENTS.md` and its memories along with its role prompt.

`--trace` is required rather than optional.
It writes the prompt, the exact command, the response, and stderr under `ocs state-dir runs/ask`, and that is what makes the lane's verdict recoverable after the fact.

## What the package carries that the native lane's does not

`ocs ask` assembles the role prompt and the user's and project's worker layers (`.agents/kein/prompts/worker.md`), and nothing else.
It does not inject repository instructions, by design: it cannot know whether a repository's conventions bear on a given question, and the caller can.

So a codex lane's package is the official package from the review contract plus the repository instructions a native lane receives from its own environment.
Do not restate the role prompt; `ask` already supplies it.
Everything else in the review contract applies unchanged, including the review-content plan hash and the response shape.

## Freshness and concurrency

A codex lane is structurally fresh.
`ocs ask` runs `codex exec --ephemeral`, so there is no session to continue and no history to clear, and the blindness requirement is met without the lead doing anything to secure it.

Start a codex lane first and the native lanes alongside it.
A codex lane that fails is moved, not restarted: `open --lanes` at the next round puts the role on another vendor and the run keeps its rounds.
`--trace` puts a codex verdict on disk whether or not the lead is waiting when it lands, so the two kinds of lane overlap without either being waited on.

## Recording

Key each verdict by lane rather than by role — `architect@claude`, `critic@codex`.
One role with two vendors produces two verdicts against one review hash.

An advisory verdict is stored and its findings are consolidated for Planner like any other.
It is excluded from the approval decision and from nothing else.

A nonzero exit from `ocs ask` is not a lane result.
A blocking lane that failed to run has not passed, so the round is incomplete until it runs.
An unavailable advisory lane is reported and nothing more: a lane that cannot block by returning `BLOCK` must not be able to block by failing either.
