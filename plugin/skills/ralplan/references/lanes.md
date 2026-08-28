# RALPLAN Cross-Vendor Lanes

Read this only when the invocation names a vendor for a review lane.
A run without such a flag uses the native lanes described in the skill body and needs nothing here.

## Roster

`--architect <vendors>` and `--critic <vendors>` take a comma-separated vendor list and default to `claude`.

| Flag | Effect |
| :--- | :--- |
| `--critic claude` | the native lane, identical to passing nothing |
| `--critic codex` | the native lane is replaced |
| `--critic claude,codex` | two lanes for one role, both blocking |
| `--critic claude,codex:advisory` | the codex lane reports but cannot block |

A vendor suffixed `:advisory` records a verdict and contributes findings without gating approval.
Every unsuffixed lane blocks, which is the rule the skill body already states for the native pair.

Planner takes no vendor.
`ocs ask` serves read-only roles only, and a remote vendor authoring the canonical artifact would be writing with no workflow around the write.
Refuse `--planner <vendor>` and say so rather than silently planning natively.

## Mechanism

```sh
ocs ask codex --agent <role> --trace --task-file <the lane package>
```

Write the package to a file and name it. A review package is a document — the first measured cross-vendor round wrote 646 lines and a wrapper script to get it through `argv`, which is what `--task-file` replaces. `-` reads standard input.

The mechanism is not a choice to make.
`ocs ask` serves exactly the roles whose canonical `sandbox_mode` is read-only, which is every review lane here.

`ocs ask` pins the vendor home to `KEIN_CODEX_HOME`, and without it the operator's own `~/.codex`, so a lane reads the skills that home's plugins publish, its `AGENTS.md` and its memories along with its role prompt.

`--trace` is required rather than optional.
It writes the prompt, the exact command, the response, and stderr under `ocs state-dir runs/ask`, and that is what makes the lane's verdict recoverable after the fact.

## What the package carries that the native lane's does not

`ocs ask` assembles the role prompt and nothing else.
It does not inject repository instructions, by design: it cannot know whether a repository's conventions bear on a given question, and the caller can.

So a codex lane's package is the official package from the review contract plus the repository instructions a native lane receives from its own environment.
Do not restate the role prompt; `ask` already supplies it.
Everything else in the review contract applies unchanged, including the review-content plan hash and the response shape.

## Freshness and concurrency

A codex lane is structurally fresh.
`ocs ask` runs `codex exec --ephemeral`, so there is no session to continue and no history to clear, and the blindness requirement is met without the lead doing anything to secure it.

Start a codex lane first and the native lanes alongside it.
`--trace` puts a codex verdict on disk whether or not the lead is waiting when it lands, so the two kinds of lane overlap without either being waited on.

## Recording

Key each verdict by lane rather than by role — `architect@claude`, `critic@codex`.
One role with two vendors produces two verdicts against one review hash.

An advisory verdict is stored and its findings are consolidated for Planner like any other.
It is excluded from the approval decision and from nothing else.

A nonzero exit from `ocs ask` is not a lane result.
A blocking lane that failed to run has not passed, so the round is incomplete until it runs.
An unavailable advisory lane is reported and nothing more: a lane that cannot block by returning `MUST_FIX` must not be able to block by failing either.
