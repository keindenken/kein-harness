# 104 planning skills, surveyed

Read 2026-08-11 by six agents over disjoint slices of `planning-readlist.json` — 104 files, 375,000 words, selected from 578 name-and-body matches in the corpus by requiring two independent body signals and deduplicating (`planning-with-files` alone ships eighteen near-copies). Each agent answered the same six questions per file and was instructed to write "nothing" rather than invent, because a file that specifies little is itself a finding.

Slices at `references/corpora/260811-github-skills/slices/`. Roughly a quarter of the 104 turned out not to be planning skills at all — SEO audits, offensive-security playbooks, financial reports — and those are reported as "nothing" throughout rather than dropped, so the denominators below are honest.

## Name the files; do not write the code

This was the open question, and the corpus answers it lopsidedly.

**Implementation code inside a pre-implementation plan: required by one, forbidden by seven.**

Required: `obra/superpowers/writing-plans` — "code blocks required for code steps", with a failing test and a minimal implementation embedded in every task.

Forbidden, each in its own words:

- `AlpacaLabsLLC/workplan` — "Do not pre-write implementation code or turn the plan into command-by-command choreography."
- `addyosmani/planning-and-task-breakdown` — "**Do NOT write code during planning.**"
- `thedotmack/design-is` — "You do not write implementation code."
- `garrytan/gstack/office-hours` and `slopus/happy/office-hours` — "**HARD GATE:** Do NOT invoke any implementation skill, write any code, scaffold any project."
- `breaking-brake/jira-driven-planning` — "過度に詳細な実装レベルまで踏み込まず、計画レベルに留める."
- `mattpocock/to-tickets` — forbids code and paths together.

Several others require code, and every one of them is a case where the code *is* the deliverable rather than a description of one: Terraform HCL, Google Cloud IaC, `seo-analysis`'s JSON-LD, `openloomi/create-task`'s Jinja templates (the artifact being designed is a prompt), and `prisma/create-pr`'s snippet — which sits in a PR body, after the implementation exists.

**File paths inside the plan: required by six, forbidden by one.**

- `speckit-workflow` makes it structural — a path is a component of every task line: `` - [ ] T001 [P] [US1] Task description `path/to/file.ts` ``
- `addyosmani` — a `**Files likely touched:**` block per task, written as `src/path/to/file.ts`
- `rohitg00/task-decomposition` — `**Files to Create/Modify:**` as a checkbox list
- `ultrawork` — todo lines are path-prefixed by required form: `` `src/foo/bar.ts: Implement validateEmail() … — verify by foo.test.ts GREEN` ``
- `omc-plan` — a measured bar rather than a slot: "80%+ claims cite file/line"
- `AlpacaLabsLLC/workplan` — required, with the one refinement nobody else states: "Use project-relative paths inside the plan. **Never put machine-specific absolute paths in the artifact.**"

The lone dissenter is `mattpocock/to-tickets`, and it gives its reason: "avoid specific file paths or code snippets — **they go stale fast**", with one carve-out for a prototype snippet that "encodes a decision more precisely than prose can (state machine, reducer, schema, type shape) … not a working demo, just the important bits."

So the position of naming targets without writing implementations is where the corpus sits, and `plan-template.md` currently states neither half of it.

One asymmetry worth keeping: `file:line` is near-universal for **evidence** while being absent from most **plans**. `gstack/review` is the sharpest — "If you cannot quote the motivating line(s), the finding is unverified. Force its confidence to 4-5 (suppressed from the main report)" — and `gstack/design-review` forbids reading source during its audit while requiring `file:line` from its reviewers. Locators are being asked for where something is being asserted about code that exists, not where work is being proposed.

## Three families of sizing rule, and one hard cluster

**By files touched.** This is where independent houses land on the same number.

- `addyosmani`: XS 1 · S 1-2 · M 3-5 · L 5-8 · XL 8+ "**Too large — break it down further**", with "An agent performs best on S and M tasks" and a closing check, "No task touches more than ~5 files."
- `gstack/review` and `gstack/investigate`: "**If the fix touches >5 files:** Use AskUserQuestion to flag the blast radius."
- `gstack/plan-eng-review`: "more than 8 files or more than 2 new classes/services … treat that as a smell."
- `tlc-spec-driven`: "**Small** | ≤3 files."

**By budget.** `mattpocock/to-tickets` — "sized to fit in a single fresh context window." `echoVic/spec-flow` — "1-2 tool calls." `ultrawork` — "small enough to finish within a few tool calls." `addyosmani` — "more than one focused session (roughly 2+ hours of agent work)." `rohitg00` — "less than half a day." `Prat011` — "1-2 days."

**By reviewability.** Only `superpowers`, and it is the most transferable of the three because it names the decision rather than a number: "split only where a reviewer could meaningfully reject one task while approving its neighbor."

`addyosmani` also supplies the cheapest smell test in the survey: "You find yourself writing 'and' in the task title (a sign it is two tasks)."

## What ends planning: three mechanisms, not one

**A human approves.** The default, and near-universal — `workplan`, `office-hours`, `addyosmani`, `create-site`, `luwill/research-proposal` ("**Do not start writing content on an unapproved outline**"), `google-cloud`, `beagle/web-research` (gate G3).

**A script refuses.** Fewer, and more interesting. `tlc-spec-driven` runs `validate_spec.py` and `validate_tasks.py` before human review, with "A non-zero exit means STOP and fix before proceeding" and the reason stated: "Deterministic gates run before human review — not from memory … so they cannot silently drift when the model forgets a step." `ts-paper-plan` loops `blueprint_lint.py --fix` "until `ok=true`. Do not proceed on a failing blueprint." `outline-agent` and `Light-skills` do the same shape. This is `trailofbits/skills`' "put the check where it cannot be talked out of firing", implemented.

**A content criterion is met.** Rarest. `mattpocock/wayfinder` — done when nothing is left to decide. `superpowers` — a three-check self-review, then "fix and move on. No need to re-review."

## The two findings that bear on what was measured here yesterday

`plan` was measured inert on a fixture with nothing unresolved: four of five assertions passing in both arms, at 21–23 turns against 8–10. Two houses solve exactly that, and they solve it the same way.

**Depth tiers over one fixed process.** `AlpacaLabsLLC/workplan` offers Lightweight, Standard and Deep, and pins the invariant: "**Depth changes research and detail, not the artifact contract.**" `tlc-spec-driven` is more aggressive — "**Small** ≤3 files, one sentence → skip Design and Tasks" — and then adds the part that makes skipping safe:

> Even when Tasks is skipped, Execute ALWAYS starts by listing atomic steps inline … If that listing reveals >5 steps or complex dependencies, STOP and create a formal `tasks.md` — the Tasks phase was wrongly skipped.

A runtime check that catches its own wrong skip, rather than a judgement made once at the top.

**Absence as the correct state.** `tlc-spec-driven` again, and it reads as if written for the Evidence Gate question:

> **Create artifacts lazily.** Write each file only when its phase actually produces content — never scaffold empty `context.md`, `design.md`, or `tasks.md` up front. **An empty file signals a phase happened when it did not; absence is the correct state for a skipped phase.**

The 2026-08-11 measurement established that the gate does stay absent when nothing is unresolved. This names the principle behind why that is the right behaviour, and generalises it past the gate to every optional section.

## Claims worth carrying regardless of what gets adopted

- **Turn count beats token price.** `superpowers/subagent-driven-development`: "Wall-clock and context cost scale with how many turns a subagent takes, and the cheapest models routinely take 2-3× the turns on multi-step work — costing more overall." The conformance instrument in `260810-skill-measurement-program.md` pins Haiku on the assumption that cheaper is cheaper.
- **A pre-filtering instruction is grep-able.** Same file: "never instruct a reviewer to ignore or not flag a specific issue … If the prompt you are writing contains 'do not flag,' 'don't treat X as a defect,' 'at most Minor,' or 'the plan chose' — stop." This is `trailofbits`' pre-filter warning arrived at independently, and turned into a check a script could run over `plugin/prompts/`.
- **The plan-review failure is over-conservatism, not error.** `yzhao062/implement-review`: "The single biggest plan-review failure mode in this maintainer's history was not 'the plan had a bug' — it was 'the plan's scope was over-conservative, deferring user value across an extra release cycle worth of process tax.'" With the paired question: "Could a strictly smaller scope close most of it? Could a marginally larger scope close all of it for low marginal cost?"
- **The author does not verify.** `tlc-spec-driven`: "the Verifier re-derives coverage independently using evidence-or-zero; it does not inherit the author's mental model", backed by a mutation sensor that "injects behavior-level faults in an isolated scratch (temp worktree or file copies — never `git stash`), confirms tests kill them", with "the fix→re-verify loop bounded to 3 iterations before escalating."
- **Controllers lose their place.** `superpowers/subagent-driven-development`: "Conversation memory does not survive compaction. In real sessions, controllers that lost their place have re-dispatched entire completed task sequences — the single most expensive failure observed."
- **From the incumbent.** `oh-my-claudecode/omc-plan`: "**Consensus mode agent calls MUST be sequential, never parallel.** Always await the Architect Task result before issuing the Critic Task." `ralplan` here dispatches Architect and Critic in one message, deliberately, to keep them blind to each other. The two houses disagree and both state a reason; ours is recorded in `ralplan/SKILL.md`.

## What this does not settle

- **Nothing here was measured.** These are 104 statements of intent. The one question the survey cannot answer is whether a plan naming files outperforms one that does not, which needs the fixture where the code moved between planning and execution.
- **The counts are of skills, not of evidence.** Seven files forbidding code is seven authors agreeing, and the corpus has already shown that authors converge on structure while staying silent on why. `mattpocock` is the only one of the eight that states a cost.
- **Selection favoured revision depth.** Files were ranked by commits, so a well-reasoned skill committed once ranks below a mediocre one revised forty times.
- **Roughly a quarter were not planning skills.** The name-and-body filter admitted SEO audits and security playbooks; their "nothing" answers are real data about the filter, not about planning.

## One thing found that is not about planning

`itechmeat/llm-code/vibekanban` records that Vibe Kanban "runs agents with `--dangerously-skip-permissions`/`--yolo` by default for autonomous operation. Each task runs in isolated worktree, but agents can still perform system-level actions." The surveying agent's report was flagged by the harness for carrying an instruction-shaped string; it was describing a third-party tool's default, not instructing anything. Worth knowing before that tool is ever pointed at this repository.
