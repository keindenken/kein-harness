# Brief for the descvi lead: name who owns the port-exclusive gates

Written 2026-08-19 from the kein harness repository, against `dev/descvi/repo` at `35ab13f`. Nothing in descvi has been changed. This is a proposal to rule on, not a patch to apply.

Citations use descvi's own anchor convention (`AGENTS.md` "Cite code by ANCHOR"). Every non-`.md` anchor below was checked to occur exactly once in its file on 2026-08-19.

## What prompted it

Two agent sessions cannot verify in descvi at the same time. The blocker is not the worktree, the branch, or the harness — it is that `:3000`, `:3001` and `:7331` are machine-global and two of the verification lanes claim them exclusively.

This surfaced while planning parallel `execute` lanes with a second harness. It is not a kein-specific problem: it binds any two workers on this repository, including two omc lanes today.

## The line already exists

descvi has already separated the port-touching work, and said why:

- `scripts/gates.mjs#separation onto independent GitHub Actions runners is what avoids :3000/:3001/:7331 port collisions` — `pnpm gates` reproduces CI's `verify` job only, and `e2e` / `e2e-contract-gates` are left out on purpose.
- `AGENTS.md` "Verification gates" says the same in prose and points at `pnpm test:e2e` for those two.

So the split is not a new taxonomy to invent:

| | ports |
| :--- | :--- |
| `pnpm gates` — typecheck, lint, vitest, citation anchors, register gates | none |
| `pnpm test:e2e` — `e2e` + `e2e-contract-gates` | `:3000` `:3001` `:7331` |

**The exclusivity is deliberate, not incidental.** `scripts/e2e-gate-cx2.mjs#This gate arranges and inspects that port` refuses to start when anything already holds `:7331`, because the gate's subject *is* port ownership: it runs a clean control, then injects faults and asserts specific named rejections about the listener not being the one the run owns. An ambient listener makes the injected fault and the ambient condition indistinguishable. `playwright.config.ts#the harness claims :7331 or hard-fails naming the port` is the same requirement one layer up.

Do not read those as accommodations for a stray dev server. Removing them removes what the gate measures.

## Why renumbering the ports does not work

The runtime is parameterised and the harness is not.

- Server side is configurable — `packages/descvi/src/sidecar/cli.ts#sidecar port (default 7331; --port wins)`, and Vite takes `--port`.
- Client side is injected — `SidecarBridgeConfig.baseUrl` is a constructor field, so the browser half follows.
- But `e2e/fixtures/sidecar-registry.ts#export const SIDECAR_PORT = 7331;` is pinned by `scripts/e2e-gate-cx2.mjs` as a literal source match, precisely so a port change cannot silently desynchronise the gate's expected message from the runtime one.

So per-worktree ports are fine for an interactive `descvi:dev` and unavailable for the gates. Making the gates port-parameterised means editing gate source, which is the wrong thing to do while that gate is the instrument.

## The proposal — two sentences, no new mechanism

**1. `AGENTS.md`, Verification gates.** State that `pnpm test:e2e` and a real `descvi:dev` smoke are port-exclusive and belong to the lead; a delegated worker runs `pnpm gates` and stops there.

The second half matters and is easy to miss: `AGENTS.md` currently tells a worker doing UI work to run a dev smoke ("UI changes need a real `descvi:dev` smoke"), and that smoke binds `:3001` and `:7331`. Handing only `e2e` to the lead leaves this one behind.

**2. `docs/prompt/worker-brief.md`.** State that a worker does not start a listener unless its brief names one, and escalates instead.

This is an application of what is already there, not a new rule. `docs/prompt/worker-brief.md#including the gates it names` already forbids skipping named gates and adding unnamed scope, and the file already lists "a gate that cannot run" as a low-bar reason to tell the lead. What is missing is only that a worker cannot tell which gates are port-exclusive, so it reaches for `pnpm test:e2e` in good faith.

## What this is not proposing

- No change to any gate, port constant, or config. The pins stay.
- No change to any agent role prompt. Both edits are repository instructions, which is the right layer: which suites are port-exclusive is a fact about this repository, not about what an Executor is.
- No claim that parallel verification should be made to work. Serialising one lane is the cheap answer; the expensive one is per-lane port allocation through the e2e harness, and nothing yet justifies it.

## Open, for the lead to rule

**Does the dev smoke really belong to the lead, or to a worker holding a token?** Moving every UI smoke to the lead makes the lead the bottleneck on exactly the work that most needs a running server. The alternative is a claim protocol — one worker at a time holds the port — which is more machinery than the problem has earned so far. Recorded rather than decided.

**Is `pnpm gates` genuinely port-free?** Asserted here from `scripts/gates.mjs`' own scope statement and the CI job it parses, not from running the suite twice concurrently. Worth confirming by running two at once before the instruction is written as fact.
