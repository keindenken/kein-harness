# Execute Cross-Vendor Lanes

Read this only when the invocation names a vendor for review lanes.
A run without such a flag uses the native lanes described in the skill body and needs nothing here.

## Roster

`--reviewer <vendors>` takes a comma-separated vendor list and defaults to `claude`.

| Flag | Effect |
| :--- | :--- |
| `--reviewer claude` | native lanes, identical to passing nothing |
| `--reviewer codex` | each selected reviewer role runs as codex instead |
| `--reviewer claude,codex` | each selected reviewer role runs in both, both blocking |
| `--reviewer claude,codex:advisory` | the codex lanes report but cannot block |

The flag names vendors rather than roles, which is where this differs from RALPLAN. RALPLAN has a fixed Architect and Critic to name; here the reviewer roles are chosen per round from the evidence question, so the roster applies to whichever roles that selection produces.

A vendor suffixed `:advisory` records a verdict and contributes findings without gating acceptance. Every unsuffixed lane blocks, which is the rule the review contract already states.

Executor takes no vendor. `ocs ask` serves read-only roles only, and a remote vendor writing to the worktree needs supervision this skill does not have. Refuse `--executor <vendor>` and say so rather than silently implementing natively.

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

A verdict's `reviewer_role` becomes `<role>@<vendor>` — `code-reviewer@claude`, `critic@codex`, `critic@codex:advisory`. Findings carry the same identifier as the verdict they came from. No schema change is needed: verdicts are already a list and the role is already free text.

Acceptance counts blocking lanes only. An advisory lane that has not reported does not hold up acceptance, and an advisory `MUST_FIX` does not stop it, but its findings are consolidated into the correction brief like any other.

A nonzero exit from `ocs ask` is not a lane result. A blocking lane that failed to run has not passed, so the round is incomplete until it runs. An unavailable advisory lane is reported and nothing more: a lane that cannot block by returning `MUST_FIX` must not be able to block by failing either.
