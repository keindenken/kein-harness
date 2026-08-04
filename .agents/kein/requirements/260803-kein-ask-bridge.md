# The `ocs ask` Bridge

Status: Approved
Date: 2026-08-04

## Context

The kein harness ports fourteen canonical agent role prompts that already exist,
normalized and vendor-neutral, at `~/.codex-orca/foundation/prompts/`. Nothing yet lets a
Claude session hand one of those roles a task and get another vendor's answer back.

The harness inherits this capability's shape from `omc ask`, which the incumbent harness
provides and which the existing `2plan` and `2execodex` workflows depend on entirely.
Replacing OMC therefore requires replacing `ask` before those workflows can move, and the
v1 done condition — completing one full round in `descvi` with OMC off — cannot be reached
without it.

The value is not merely a second opinion. A reviewer that shares the author's error
correlations mostly flattens an answer rather than improving it; a different vendor's
errors are less correlated, so its opinion adds information. That distinction is what this
command exists to exploit.

## Desired outcome

A Claude session can name a canonical role and a task and receive that role's answer from
another vendor's CLI, with the assembled prompt containing exactly the role prompt and the
task and nothing else. The command leaves no trace in the target project, runs the other
vendor in an untuned environment, and fails loudly when its rendered copy of the canonical
prompts has fallen behind the source.

## Scope

### In scope

- An `ocs ask` subcommand that resolves a canonical role prompt, appends a task brief, and
  invokes a provider CLI one-shot.
- Codex as the single enabled provider, behind an allowlist that admits more later.
- A rendered copy of the fourteen canonical role prompts inside the harness repository,
  produced by a sync step.
- A drift check that fails when the rendered copy no longer matches canonical.
- A trace facility, off by default, that exposes the assembled prompt and the invocation so
  the two-layer guarantee can be asserted by a test.

### Out of scope

- Installing `ocs` on the Codex side, and any Codex-initiated call outward.
- Providers other than Codex.
- Injecting repository instructions into the assembled prompt.
- Single-sourcing skills across vendors.
- `ocs team`. `docs/purpose.md` assigns multi-agent orchestration to Orca.
- Any durable artifact in normal operation.

## Requirements

- `ocs ask <provider> --agent <role> <task>` resolves the named role and returns the
  provider's response on standard output.
- The assembled prompt is the rendered role prompt, a blank-line separator, and the task
  brief. No other content is added.
- Repository instructions reach the callee only when the caller has put them in the task
  brief.
- The provider process runs with `CODEX_HOME` set explicitly to the vanilla Codex home. The
  ambient value is never inherited.
- An unknown role fails with a message listing the roles that are available.
- A provider outside the allowlist fails without invoking anything.
- A sync step renders the canonical prompts into the harness repository.
- A drift check compares the rendered copy against canonical and fails when they differ.
- A trace flag writes the assembled prompt, the exact invocation, and the response to the
  run root. Without the flag, nothing is written anywhere.

## Constraints

- Canonical role prompts have one source, `~/.codex-orca/foundation/prompts/`, and both
  vendors render from it. From `docs/purpose.md`.
- Nothing is written into the target repository's working directory. From
  `docs/purpose.md`.
- Provider invocation must not bypass approvals or sandboxing by default, must not write
  `.omc`-style artifacts, and must not enable providers outside the selected set. From
  `~/.codex-orca/DECISIONS.md:407`.
- `ocs` is the only executable on the Bash tool's PATH. Subcommands live off PATH and are
  reached through it.
- `CLAUDE_PLUGIN_ROOT` is not present in the Bash tool's environment, so no component may
  depend on it to locate itself.

## Decision boundaries

- `ask` may warn when a brief appears to carry no repository context, but must never inject
  it.
- The drift-check mechanism — a hash manifest, or regenerate-and-diff — is free, provided a
  stale rendered copy is detectable and fails the check.
- The trace format is free, provided the assembled prompt is recoverable verbatim.
- The allowlist's internal representation is free, provided adding a provider does not
  require changing call sites.
- No skill may share a name with an `ocs` subcommand.

## Acceptance criteria

- [ ] `ocs ask codex --agent <role> "<task>"` returns the role's response on stdout.
- [ ] With the trace flag, the recorded assembled prompt equals the rendered role prompt,
      a blank line, and the task brief, with nothing else present.
- [ ] Without the trace flag, a completed call leaves no new file in the working directory
      and none in the run root.
- [ ] The recorded invocation shows `CODEX_HOME` pointing at the vanilla Codex home and not
      at `~/.codex-orca`.
- [ ] An unknown role exits non-zero and names the available roles.
- [ ] A provider outside the allowlist exits non-zero without spawning a provider process.
- [ ] The drift check passes on a freshly synced copy, and fails after canonical is changed
      without a re-sync.
- [ ] No skill name collides with an `ocs` subcommand.

## Decisions and rationale

- **One-directional, contract fixed:** `ask` ships in the Claude plugin and calls outward.
  The v1 done condition needs Codex consultation, while Codex has fourteen native subagents
  and no present need to call out. The command surface, layering, and prompt resolution are
  settled now so a later Codex-side install requires no redesign.
- **The brief carries repository instructions:** `omc ask` assembles exactly
  `agentPromptContent + "\n\n" + prompt` and injects nothing, and `execute/SKILL.md:30`
  already places repository instructions in the brief it hands an Executor. `ask` cannot
  know whether a repository's conventions bear on a given question; the caller can.
  Injecting them unconditionally is the context contamination that
  `~/Documents/wiki/harness/harness-obsolescence.md` describes, where a short question
  reaches the model as a mostly-boilerplate prompt.
- **Canonical stays in the Codex home; the harness renders a copy:** `build_agents.py`,
  `manifest.json`, `test_prompt_policy.py`, and the OMC/OMX lineage in `source-map.json`
  already surround that location and are validated. A rendered copy keeps the harness
  self-contained; a drift check keeps the copy honest.
- **Execution pins the vanilla Codex home:** the prompt library and the execution
  environment are orthogonal concerns that currently share a directory. The library is
  vendor-neutral text; `~/.codex-orca` is an environment being tuned for lead use. A
  one-shot advisory call must not inherit lead tuning, which is the same reason `orcodex`
  exists as a separate launcher.
- **Codex only, for now:** every present consumer — `2plan`, `2execodex`, `team` — targets
  Codex. This is a present-time judgement, not a permanent boundary; `antigravity` is the
  named likely addition. `claude` is excluded because under the one-directional decision it
  would be a Claude-to-Claude call, which native subagents already cover.
- **Trace is a test instrument, not a runtime feature:** its only reader is a test
  asserting the two-layer guarantee. A trace nobody reads is the accumulating by-product
  this harness exists to avoid, so it is produced only when asked for, and there is nothing
  to retain or clean up.
- **Harness `kein`, CLI `ocs`, folder `kein-harness`:** OMC's confusion came from `omc ask`
  the command sitting beside `ask` the skill. Separating the CLI name from the harness name
  keeps the two readable, and `~/.codex-orca/DECISIONS.md:392` already specifies
  `ocs ask <provider> --agent <role> <task>`, so that record now stands unrevised.

## Relevant system evidence

- `omc 4.15.7 dist/cli/ask.js:181`: layering is exactly
  `agentPromptContent + "\n\n" + prompt`. Two layers, no repository instructions.
- `omc 4.15.7 dist/cli/ask.js:174`: the prompts directory resolves from cwd, package root,
  and an environment override, so role prompts are replaceable without forking.
- `omc 4.15.7 dist/cli/ask.js:167`: providers pass a `disableExternalLLM` policy gate.
- `omc 4.15.7 dist/cli/ask.js:183`: provider invocation is delegated to a separate advisor
  script rather than built inline.
- `~/.codex-orca/DECISIONS.md:392`: the prior design is
  `ocs ask <provider> --agent <role> <task>` alongside `ocs team`.
- `~/.codex-orca/foundation/prompts/`: fourteen canonical role prompts, none of which
  reference `AGENTS.md`, `CLAUDE.md`, or any repository instruction file.
- `~/.codex-orca/skills/execute/SKILL.md:30`: the workflow already supplies repository
  instructions inside the Executor's brief.
- `kein-harness bin/ocs`: subcommand dispatch to `libexec/<cli>-<name>`, with `run-root` (since renamed
  `state-dir`) and `validate` already present.
- `ocs doctor` under a live session: `CLAUDE_PLUGIN_ROOT` is unset in the Bash tool
  environment; the plugin root resolves through the `$0` fallback.
- `kein-harness skills/interview`, ported 2026-08-03: exactly six lines diverged from the Codex
  original, four of which the `run-root` (since renamed `state-dir`) and `validate` subcommands
  absorbed.

## Assumptions and risks

- The vanilla Codex home is described as not perfectly vanilla today. Pinning it makes the
  environment explicit but does not make it clean, so an untuned-environment assumption may
  not fully hold.
- A caller that omits repository context produces an ungrounded call, and nothing prevents
  it. This is the accepted cost of not injecting; a warning is permitted but not required.
- The rendered copy can fall behind canonical between syncs. The drift check converts this
  from a silent wrong answer into a loud failure, but only at the moments the check runs.
- Codex CLI flags may change across versions, which would break invocation assembly. The
  evidence above is against `codex-cli 0.146.0`.
- `AskUserQuestion` failed to parse three consecutive times on long Korean option
  descriptions during this interview, forcing a prose fallback. Whether bounded questions
  should route through that tool or stay in prose is deliberately unsettled in the skill,
  so this is a known trade-off rather than a defect, and it bears on the interview skill
  rather than on this command.

## Deferred items

- **Single-sourcing skills across vendors.** Fixed boundary: vendor coupling is absorbed by
  the CLI and never written into skill prose. Gate: immediately after `plan` and `execute`
  are ported, since both are several times larger than `interview` and carry state
  machines, making the residual divergence measurable there.
- **Extracting the canonical prompt library out of `~/.codex-orca`.** The execution-home
  decision is the first evidence that a vendor-neutral library living inside a lead-tuned
  environment is incidental. Fixed boundary: the library's contents stay vendor-neutral
  wherever it lives. Gate: when a second consumer needs it without the Codex home present.
- **Installing `ocs` on the Codex side.** Fixed boundary: the command surface settled here
  does not change. Gate: when Codex actually needs to call out to another vendor.
- **Additional providers, `antigravity` first.** Fixed boundary: the allowlist admits a
  provider without changing call sites. Gate: when a second vendor's opinion is actually
  wanted.
