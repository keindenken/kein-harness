# Execute Cross-Vendor Lanes

Read this only when the invocation names a vendor for a lane.
A run without such a flag uses the native lanes described in the skill body and needs nothing here.

## Roster

`--reviewer <vendors>` and `--executor <vendor>` take a comma-separated vendor list and default to `claude`.

| Flag | Effect |
| :--- | :--- |
| `--reviewer claude` | native lanes, identical to passing nothing |
| `--reviewer codex` | each selected reviewer role runs as codex instead |
| `--reviewer claude,codex` | each selected reviewer role runs in both, both blocking |
| `--executor codex` | the round's Executor runs as codex |

The flag names vendors rather than roles, which is where this differs from RALPLAN. RALPLAN has a fixed Architect and Critic to name; here the reviewer roles are chosen per round from the evidence question, so the roster applies to whichever roles that selection produces.

Every lane blocks. RALPLAN offers an `:advisory` suffix and this does not, because there the roster is fixed for the run and the state can hold it — verdicts are keyed by lane, so a silent lane is visible and an advisory one can be skipped by name. With the roles varying per round there is no roster to fix and nothing for a suffix to be enforced against. The rule is the one the review contract already states: a current `MUST_FIX` stops acceptance, whichever lane returned it.

`--executor <vendor>` takes exactly one vendor, because the task ledger is serial and two writers is the thing it exists to prevent.

## The write-capable lane

```sh
ocs team codex --agent executor --trace "<the task package>"
```

`ocs team` is the write-capable counterpart to `ocs ask`: it composes a vendor terminal, hands it to Orca as a supervised worker, and blocks until Orca's own completion signal arrives. Orca owns the dispatch lifecycle and recovery; the command owns the execution environment, which is the part Orca cannot vary per lane.

The command is what enforces the environment, so there is nothing here for the lead to arrange. It resolves the model from the role's tier, pins the pristine vendor home, sets a sandbox that can both write in the worktree and report completion, and refuses before creating anything if the project is untrusted in that home.

Two things do fall to the lead. The task package must carry the repository instructions, for the same reason a review lane's does — the bridge assembles the role prompt and nothing else. And the worker's report arrives as a file whose path the command prints; treat that file as the Executor's self-verification evidence, exactly as you would a native Executor's returned account, and hold it to the same standard. Self-verification is still not approval.

A vendor Executor is otherwise an ordinary Executor. It takes one task, its scope, completion condition, repository instructions, and verification path; its work is reviewed by the round's reviewer lanes; and a `MUST_FIX` returns to a correction round in the usual way. A correction may go to a fresh vendor Executor or a native one, whichever the evidence favours.

## Mechanism

```sh
ocs ask codex --agent <role> --trace "<the lane package>"
```

The mechanism is not a choice to make. `ocs ask` serves exactly the roles whose canonical `sandbox_mode` is read-only, which is every reviewer role the contract offers, and it resolves the model from the role's tier so a lane does not inherit the operator's own default.

`--trace` is required rather than optional. It writes the prompt, the exact command, the response, and stderr under `ocs state-dir runs/ask`, and that is what makes the lane's verdict recoverable after the fact.

## What the package carries that the native lane's does not

`ocs ask` assembles the role prompt and nothing else. It does not inject repository instructions, by design: it cannot know whether a repository's conventions bear on a given question, and the caller can.

So a codex lane's package is the review-contract package plus the repository instructions a native lane receives from its own environment — which the contract already requires for a final audit and which every round needs here. Quoting them or naming the file that holds them both work, since the lane runs with the worktree as its working directory. Do not restate the role prompt; `ask` already supplies it.

Everything else in the review contract applies unchanged, including the task, round, and fingerprint binding and the response shape.

## Freshness and concurrency

A codex lane is structurally fresh. `ocs ask` runs `codex exec --ephemeral`, so there is no session to continue and no history to clear. Its `fresh` and `independent` facts are true by construction rather than by the lead's care, and a previous codex lane cannot be continued for a closure check at all.

A codex lane may run in the background. The skill body forbids backgrounding an Agent tool lane because a backgrounded subagent's final message never reaches the lead, so a verdict simply never arrives. That reason does not hold for a shell call whose response is persisted: `--trace` puts the verdict on disk whether or not the lead is waiting when it lands. Start the codex lanes first and the native lanes alongside them.

## Recording

A verdict's `reviewer_role` becomes `<role>@<vendor>` — `code-reviewer@claude`, `critic@codex`. Findings carry the same identifier as the verdict they came from. No schema change is needed: verdicts are already a list and the role is already free text. Nothing in the workflow reads the vendor half, and it is worth the two characters only because a native lane leaves no trace of its own: the ledger is the sole record of which vendor judged.

The Executor's vendor is not recorded, and putting it in the state would be a fact with no reader. `reconcile` resolves continuation without it, acceptance judges the worktree rather than its author, and a correction round may switch vendors either way. `ocs team --trace` already holds the vendor, the model, and the home, written by the mechanism instead of by a lead who can forget — which is how the first observed run recorded none of it. The worktree fingerprint binds verification to the round exactly as before: a vendor Executor wrote to the same canonical worktree.

A nonzero exit from `ocs ask` or `ocs team` is not a lane result. A lane that failed to run has not passed, so the round is incomplete until it runs, and this one is the lead's to hold rather than the state's: verdicts are a list rather than a roster, so a lane that never reported leaves nothing behind to notice. A vendor Executor that exits nonzero has not implemented the task, whatever the worktree looks like: re-read the fingerprint before deciding what happened.
