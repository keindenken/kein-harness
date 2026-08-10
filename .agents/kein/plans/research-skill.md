# Research skill: design and implementation plan

Status: Draft
Status reason: First draft, ready for execution. All five required design decisions (completion signal, artifact shape/location, task bounding, review-gate, state) are resolved below with repository evidence, and the seventh-skill and `autoresearch`-deferral questions are resolved directly rather than left implicit. No blocking evidence gap remains for Steps 1-3 (the skill itself). Step 4 is a small `docs/purpose.md` reconciliation that purpose.md's own header calls for ("revise it when a decision here is overturned") and can be reviewed and merged independently of Steps 1-3.

## What this plan is

A design for `plugin/skills/research/` — the harness's first workflow whose deliverable is a cited, prose synthesis rather than a code change or another artifact type already in the harness (implementation plan, requirements document, handoff note). This document specifies what to build; it does not build it. Steps 1-4 below are for a later `execute` round or manual authoring.

## Two threshold questions, resolved directly

### Does `research` get to be a new skill directory?

`plugin/skills/*` currently holds six directories: `execute`, `handoff`, `interview`, `ping`, `plan`, `ralplan` (verified by listing the directory). `docs/purpose.md` Non-goals states six is the working ceiling and a seventh needs removing one or arguing the ceiling was wrong.

`ping` is not a workflow skill in the sense that line means. Its entire body is `Reply with exactly one line: \`kein: pong (skills-dir, loaded in place)\` — nothing else.` (`plugin/skills/ping/SKILL.md`, 6 lines). It dispatches no agent, produces no artifact, and is absent from `docs/purpose.md`'s own Scope enumeration (`interview · plan · ralplan · execute · handoff · ralph · autopilot · orca orchestration`) — it was added later as a load-diagnostic, not as one of the workflow components the Scope section is counting. Treating it as infrastructure rather than a workflow skill is not a stretch to make room for `research`; it is already how `docs/purpose.md` itself enumerates the workflow set.

With `ping` excluded, the built workflow skills are `execute`, `handoff`, `interview`, `plan`, `ralplan` — five. `research` becomes the sixth, landing exactly at the stated ceiling rather than past it.

This does not make the ceiling problem disappear. `docs/purpose.md` Scope already names `ralph` and `autopilot` as committed-but-unbuilt, which is two more workflow-shaped things wanting a slot under a five-that-becomes-six budget. That collision is real and is **not resolved by this plan** — `ralph` and `autopilot` may not need their own directories at all (compare how `team` was resolved: "no separate skill... Orca orchestration lives in `ralplan` and `execute` as a conditional reference," per `docs/purpose.md` Order item 6), or the ceiling itself may need to move once a fourth prose-shaped workflow is proposed. Deciding that now, for skills that do not exist yet, would be scope creep on this plan. It is recorded as an Open Question below.

**Alternative considered and rejected: fold research into `plan` instead of a new directory.** `plan` already matches research's shape on several axes — one dispatch, no adversarial gate, no state file, Planner as sole writer. The difference that rules this out: `plan`'s artifact contract (implementation steps, acceptance criteria, verification commands) and Planner's own `Success_Criteria` (e.g. "Every step has specific acceptance criteria and traceable verification") are built around "how do we build this," not "what is true and how well-supported is it." Bolting a structurally different prose-synthesis contract onto Planner would force conditional branches through Planner's `Process` and `Success_Criteria`, which is exactly the failure `docs/purpose.md` names when describing why OMC's skills were bad: "Several are large single files, and size correlates with the model losing the thread inside them. Wrapping one produced two skills for one role, which added a confusion point rather than removing one." Two artifact contracts inside one role is the same problem in the other direction. A new, thin directory is the smaller design.

### Does this override `docs/purpose.md`'s "Not in v1: `self-improve`, `autoresearch`" deferral?

`docs/purpose.md` Scope: "Both are wanted, but how to use them is unresolved, and an unresolved use is a signal that the need has not arrived."

Read next to `self-improve`, `autoresearch` names an autonomous, self-triggered loop — something that decides on its own when to research and what to do with the result, with no settled trigger, cadence, or reviewer. That is a genuinely different shape from what this plan specifies: a bounded, user-dispatched, single-invocation workflow that behaves like `plan` — one concrete question in, one artifact out, stop. The objection in the Scope line ("how to use it is unresolved") targets the autonomy question (when does it fire, who is accountable for its output landing unreviewed), not the existence of a research capability invoked the same way `plan` and `interview` already are.

This plan does not silently proceed past the deferral — it narrows what "research" means for `docs/purpose.md`'s purposes: the deferred item is the autonomous-loop reading of "research capability," not a bounded synthesis workflow invoked by explicit request. Step 4 below proposes the exact `docs/purpose.md` wording to make that boundary explicit rather than leaving the deferral ambiguous about which meaning it covers.

## Design decisions

### 1. Completion signal

`execute` has a machine-checkable completion condition (exit code plus worktree fingerprint) because its claim is behavioral. `research`'s claim is "this document answers the brief," and whether it answers it *well* — the right question, weighted correctly, nothing important missed — is not a checkable property. That is the ownership gap `~/Documents/wiki/harness/harness-obsolescence.md` names: information and judgment that live only with the person who asked, not a capability gap a checker can close. Nothing stands in for that. The research skill does not claim to.

A narrower, genuinely mechanical property does exist independent of that judgment call: **structure**, not conclusion.

- Every question the brief posed has an explicit status (Answered, Partial, Unanswered, or Unanswerable — decision, not research) — nothing silently dropped.
- Every non-Unanswered finding carries at least one source.
- The document's top-level `Status` (`Complete`/`Partial`) is consistent with its per-question statuses.

This is checkable by a script, the same way `plugin/skills/interview/scripts/validate_artifacts.py` checks heading presence, status vocabulary, and blocking-gap consistency for the requirements document and ledger — not the substance of a requirement, only its declared shape. Building a `plugin/skills/research/scripts/validate_artifacts.py` on the same pattern is Step 3.

Why a script and not a reviewer's checklist: this check has no judgment content — it is presence/absence and cross-field consistency, exactly interview's validator's shape. A dispatched reviewer for that would be spending a full agent round on something a few hundred lines of Python already does deterministically and for free, which is the cost `docs/purpose.md` Operating rule 5 asks a script to absorb ("Rich references... This is also the substitute when a verification round is removed from `execute`"). `plan`, by contrast, has no validator script at all — its artifact is close to freeform Planner prose with only two fixed fields, too thin a contract to make a script worth writing. Research's contract has real enumerable structure (a variable number of per-question subsections, each needing an internally consistent status/sources pair), which is what justifies building one here where `plan` didn't.

What a script cannot check, and what a reviewer plausibly could: whether a cited source actually supports the claim it is attached to (semantic, not structural). That gap is real — see Decision 4 for why it is not closed in this plan.

### 2. The artifact: shape and location

Per `docs/purpose.md` Operating rule 1, the artifact is a work product and belongs under `<repo>/.agents/kein/`, resolved by `ocs state-dir`, never `docs/`. `docs/purpose.md` itself already names the target subdirectory when describing the preferred shape of `.omc/`: "`repo/.omc/` holding `plans/` and `research/` is the preferred shape, not the problem." Default path: `<ocs state-dir research>/YYMMDD-<slug>.md` → `.agents/kein/research/YYMMDD-<slug>.md`.

Dated rather than bare-slug (unlike `plan`'s `<slug>.md`): a project accumulates many distinct research questions over its life the way it accumulates many requirements documents and handoffs, not one evolving plan. `handoff` and `interview`'s requirements artifact both use `YYMMDD-<slug>.md` for the same reason; `plan` doesn't because a piece of work usually has exactly one live plan, revised in place. Follow interview's own resumption rule for what "revise in place" means here: continue an existing artifact only when it belongs to the same brief (same-day, same question set); otherwise write a new dated file, and use a short numeric suffix when provenance is ambiguous.

Shape (full contract goes in `plugin/skills/research/references/research-template.md`, Step 2):

```markdown
# <Research title>

Status: Complete | Partial
Date: YYYY-MM-DD
Brief: <original question(s) or prompt-safe summary>

## Q1: <question text>

Status: Answered | Partial | Unanswered | Unanswerable — decision, not research

<synthesized finding, hedges and confidence carried through from source lanes, not smoothed away>

Conflicts: <material source disagreement not resolved by blending, or None>

Sources:
- `<path>` or <URL>: <what it establishes>

## Q2: <question text>
...

## Unanswered questions

- <question, why it is unanswered, what evidence would resolve it, or None>

## Assumptions and limitations

- <scope boundary, evidence gap, or caveat that bears on how findings should be used, or None>
```

`Status: Complete` requires every `Q` subsection to be Answered (Unanswerable counts as resolved-as-a-routing-decision, not blocking); `Status: Partial` is used when at least one subsection is Partial or Unanswered, and that gap is also listed in `## Unanswered questions`. This is interview's `Approved`/`Draft` + `## Blocking gaps` pattern adapted without the approval semantics: nobody approves a research finding, so there is no `Approved` value here, only whether every posed question got a real answer.

`Unanswerable — decision, not research` exists as its own status, distinct from Unanswered, because a brief question is sometimes actually a product or priority decision in question form ("should we use X or Y") rather than a fact with a discoverable answer. Marking it Unanswerable rather than quietly picking a side is the guard against the ownership-gap collapse named in the pre-mortem below.

### 3. What bounds a single research task

`execute` bounds a task by scope, completion condition, and serial ordering. `research`'s bound is: **the brief must decompose into independently-answerable questions before dispatch.** If it already does (a list of concrete questions, or one narrow question), proceed directly. If it doesn't — genuinely vague, conflicting, or resting on an undecided product/priority call — do not invent the decomposition. Two escalation levels, chosen by how far off "already decomposable" the brief is:

- **Mildly underspecified** (one ambiguous term, one missing scope boundary): ask one direct clarifying question in the same turn, the way `interview`'s own `Repository_Grounding` section prefers direct inspection before delegating — a lightweight version of the same judgment, not a full loop.
- **Genuinely vague or conflicting** (the brief is closer to "figure out what we should build" than "find out whether X is true"): recommend invoking `interview` first and stop. Do not build a second, smaller interview loop inside `research` — `interview`'s ledger and one-question-at-a-time discipline already exist for exactly this, and duplicating it would be the "wrapping one produced two skills for one role" failure again, this time between `research` and `interview`.

Once decomposed, **one artifact, one section per question** — not one artifact per question. A single document is what a user reads once, matches `plan` producing one canonical artifact for a bounded piece of work, and is what the structural validator's cross-question consistency check (Decision 1) assumes. Fragmenting into per-question files would also make "every brief question addressed" unverifiable by a single script run.

**Investigation:** research does not need a new agent. The lead (the session running the `research` skill) is the default investigator and the sole author, mirroring how `plan`'s `Planner` inspects the repository directly with its own tools rather than dispatching `explore` for everything, and matching `interview`'s own stated preference: "Use direct read-only inspection first. Delegate to an exploration agent only when direct inspection cannot efficiently resolve a materially broad or ambiguous evidence question." Dispatch a lane only when a question specifically needs a specialized read-only role's discipline, or when several questions are genuinely independent and worth parallelizing:

| Question shape | Lane |
|---|---|
| Repo-local fact, symbol, or file location | Direct inspection first; `kein:explore` only if broad/ambiguous |
| Authoritative external documentation, version/compatibility, package evaluation | `kein:document-specialist` |
| "Why did X happen" / causal, competing-hypotheses questions | `kein:tracer` |
| Design comparison, tradeoffs, viable-options questions | `kein:architect` |

This table is the whole of the guidance — no separate `references/lanes.md` the way `execute`/`ralplan` have one, because those exist for cross-vendor dispatch mechanics (`ocs ask codex --agent ...`) that this plan does not build for v1 (see Open Questions). A four-row table belongs in `SKILL.md` directly under progressive disclosure (`docs/purpose.md` Operating rule 2) — it's not substantial enough to earn a deferred file.

Dispatch every lane with `run_in_background: false` and put independent lanes in one message so they still run concurrently, for the same reason `execute` and `ralplan` require it: a lane's report is a deliverable the lead needs synchronously, and a backgrounded subagent's final message never reaches the lead.

**Synthesis discipline** (goes in `SKILL.md` prose, principle-based per `docs/purpose.md` Operating rule 4 rather than a checklist): carry each lane's citations, hedges, and confidence language into the shared document without flattening them into a more confident claim than the source supports, and flag rather than blend a conflict between two lanes' findings on the same fact — the same discipline `document-specialist`'s own contract already states ("Conflicting or stale information is flagged rather than blended into false certainty") applied to the synthesis step, since the lead is now doing what document-specialist would do if it were writing the shared document itself.

This whole shape — lead-direct with optional delegation, single artifact, explicit section for what remains open, no dedicated writer-agent — is closer to `interview`'s own pattern (which also never dispatches a separate writer role) than to `plan`'s dedicated-Planner-writer pattern. `handoff` is the existing precedent for a lead-authored artifact with zero subagent dispatch at all; research sits between the two.

### 4. Whether a review lane earns its place

No review round in the base `research` skill.

The genuinely falsifiable thing a reviewer could check is real: whether a cited source actually supports the claim attached to it, and whether a claimed conflict is genuinely a conflict rather than two compatible statements. `kein:verifier`'s own contract is built for exactly this ("Evaluate evidence adequacy, not merely existence... Check that the oracle, scenario, inputs, environment, and asserted outcome bear directly on the claim"), and this is not the "re-editing a good answer" pattern `~/Documents/wiki/harness/harness-obsolescence.md` warns about — that warning is specifically about a *self*-review re-editing its own already-good output; a fresh, independent verifier checking a fixed citation-support criterion is the source's own named exception ("Fixed, checkable criteria... are the exception where an external checker still earns its cost").

It is left out anyway, for the same reason `ralplan` exists as an optional gate over `plan` rather than being folded into it: `docs/purpose.md` Operating rule 3 requires a new prompt rule or round to earn its place by differential evaluation, not by an argument that it plausibly could catch something. No evidence yet exists that research artifacts built the way this plan specifies actually ship citation-support defects at a rate that justifies a mandatory extra dispatch on every run. Building the gate now would be exactly the "review round without a proven gate" `docs/purpose.md`'s obsolescence-lens section retires.

If this need materializes — a shipped research artifact is found to cite a source that doesn't say what the claim says it says — that is the trigger for a `ralresearch`-shaped composite (a verifier lane over the same artifact, the same relationship `ralplan` has to `plan`), built the same way the most recent commit on this repo (`a2ab0b4 refactor(plan): make plan the base and RALPLAN the composite`) treats `plan`/`ralplan`: base skill first, gate added only once a concrete failure justifies its cost. Not built now; recorded as an Open Question.

### 5. State

No state file, no ledger. `research` is a single dispatch (or a small set of concurrent lanes converging into one synthesis step within that dispatch) that produces one file and stops — there is no multi-round convergence loop, no adversarial gate to track verdicts for, and no multi-turn live interaction with the user to resume mid-way. That combination of properties is exactly what makes `plan` stateless: the artifact itself, through its `Status` field and (for research specifically) its per-question status markers, is the resumability device. A later research session on the same brief reads the `Unanswered questions` section to see what's still open, the same way a later `plan` invocation reads a Draft plan's body.

Contrast with why `interview` *does* carry a ledger despite also having no adversarial gate: its workflow is a live, one-question-at-a-time loop across a conversation (potentially many turns, potentially resumed by a different vendor mid-loop), and the ledger exists to make that partial dialogue resumable. Research's lane dispatches are not a multi-turn loop with the user — they are concurrent, complete within one invocation, and synthesized once. `ralplan`/`execute` carry state for a third, unrelated reason: round-tracking for a convergence loop against a gate that can return MUST_FIX. None of the three conditions that justify a ledger or a JSON state machine elsewhere in this harness apply here.

## Pre-mortem

1. **Synthesis drift.** Under context pressure while assembling several lane reports into one document, the lead quietly drops a hedge ("the changelog doesn't confirm this for the current version" becomes "this is supported") or attaches a citation to a paraphrase the source doesn't actually back. The structural validator (Decision 1) cannot catch this — it checks that *a* citation exists, not that it supports the claim. This is the concrete shape of the gap Decision 4 leaves open; the mitigation there (explicit synthesis discipline in `SKILL.md`, plus naming this exact failure as the trigger for a future gated composite) is the answer, not a script.
2. **Ownership-gap collapse.** A brief question that is actually a product or priority decision ("should we build A or B") gets treated as answerable, and a dispatched `architect` lane or the lead's own synthesis quietly picks a side and presents it as a finding instead of surfacing it as a decision the user owns. The `Unanswerable — decision, not research` status (Decision 2) exists specifically to give this failure an explicit, checkable escape hatch rather than relying on judgment alone to catch it every time.
3. **Ceiling erosion by precedent.** Landing `research` as the sixth workflow skill (Decision: ping excluded) quietly normalizes "just add one more" for every future prose-shaped workflow that wants a slot — `self-improve`, a fuller `autoresearch`, and `ralph`/`autopilot` are all still coming. If nobody revisits `docs/purpose.md`'s ceiling line when the next one is proposed, the six-skill discipline erodes by accumulation exactly the way `~/Documents/wiki/docs/prompt-revision.md`'s "ratchet" describes standing rules eroding — quietly, because removing or re-arguing a limit is nobody's assigned job. Step 4 below is a partial mitigation (it makes the current count and the reasoning explicit in the doc itself, so the next proposal has to argue against a stated position instead of a silent one); it does not solve the `ralph`/`autopilot` collision, which is recorded as an Open Question rather than pre-decided here.

## Implementation steps

### Step 1 — `plugin/skills/research/SKILL.md`

Purpose: the thin entry point. Contents to include, each traceable to a decision above:

- Frontmatter: `name: research`, `description:` in the existing trigger-phrase convention, e.g. "Use when a question needs a cited, evidence-grounded answer captured as a durable artifact — not turned into a code change or a decision made on the user's behalf." (Checked: `research` does not collide with any `ocs` subcommand name — `ask, check-prompts, doctor, eval, render-agents, state, state-dir, sync-prompts, team, validate` per `ocs help` — satisfying `docs/purpose.md`'s "no skill may share a name with an `ocs` subcommand" rule.)
- Overview: states the ownership-gap framing from Decision 1 up front — this skill produces a structurally complete, cited document; it does not certify that the conclusions are right, and it does not decide questions that are actually the user's to decide.
- Non-goals, stated explicitly (per `docs/prompt-revision.md`'s standing-instruction bar, each with its reason so a future reader can evaluate it rather than archaeology it later): no `Approved` status (nobody approves a research finding); no adversarial review round (Decision 4); no state file (Decision 5); does not resolve a brief question that is actually a product or priority decision (routes to `Unanswerable — decision, not research` and/or recommends `interview`).
- Workflow section (four to five steps, mirroring `plan/SKILL.md`'s shape): resolve brief and canonical path → decompose into questions, escalating to a clarifying question or to `interview` per Decision 3 when the brief doesn't decompose cleanly → direct inspection or lane dispatch per the table in Decision 3, `run_in_background: false`, concurrent lanes in one message → synthesize into the one artifact per the template in Step 2, preserving hedges/citations per the synthesis-discipline paragraph in Decision 3 → run `ocs validate research <path>` and correct until it passes → report path, `Status`, and any `Unanswered`/`Unanswerable` questions.
- Reference pointer to `references/research-template.md` (Step 2), read before writing the artifact.

Acceptance criteria: file exists at `plugin/skills/research/SKILL.md`; every non-goal above is present with its stated reason, not as a bare rule (per `docs/prompt-revision.md`, an instruction with no visible downside or counterpart is the shape that tends to hide an unfound failure case — each non-goal here already carries its "why" in this plan and that reasoning should carry into the file, not just the bullet); length stays in the range of `execute/SKILL.md` (69 lines) rather than approaching `interview/SKILL.md` (154 lines, which is long specifically because of interactive-loop machinery this skill deliberately doesn't have).

Verification: `claude plugin validate /Users/kein/Documents/workspace/dev/kein-harness/plugin --strict` passes (confirms frontmatter and plugin structure are well-formed). Failure behavior: a validation error names the malformed field directly; fix and rerun before proceeding to Step 2.

### Step 2 — `plugin/skills/research/references/research-template.md`

Purpose: the artifact contract, playing the role `plugin/skills/plan/references/plan-template.md` plays for `plan` — read before writing the artifact. Full shape is specified in Decision 2 above; transcribe it directly, including the `Status`/subsection-status consistency rule and the `Unanswerable — decision, not research` status.

Acceptance criteria: every field and status value the validator (Step 3) will check is documented here first, in the same order the validator checks it — no undocumented mechanical requirement, matching how `interview/references/requirements-template.md` documents exactly what `interview/scripts/validate_artifacts.py` enforces.

Verification: cross-read against Step 3's validator once both exist; every check the script performs traces to a sentence in this file. Failure behavior: a validator rule with no corresponding template sentence means either the template is incomplete or the check is inventing a requirement — resolve by editing whichever one is wrong before shipping either.

### Step 3 — `plugin/skills/research/scripts/validate_artifacts.py`

Purpose: the structural gate from Decision 1, built directly on `plugin/skills/interview/scripts/validate_artifacts.py`'s pattern (its `_section_body` heading-presence helper and status/consistency-checking shape transfer with minor adaptation). Checks:

- Top-level `Status:` line is exactly `Complete` or `Partial`.
- `## Unanswered questions` and `## Assumptions and limitations` headings are present.
- At least one `## Q` (or equivalently-patterned) subsection exists.
- Every `Q` subsection has a `Status:` line whose value is one of `Answered`, `Partial`, `Unanswered`, `Unanswerable — decision, not research`.
- Every `Q` subsection with status `Answered` or `Partial` has a non-empty `Sources:` list.
- If the document `Status` is `Complete`, no subsection may be `Partial` or `Unanswered`.
- If the document `Status` is `Partial`, at least one subsection is `Partial` or `Unanswered`, and `## Unanswered questions` is non-empty.

No CLI wiring needed beyond placing the file at this exact path: `plugin/libexec/ocs-validate` already resolves `$KEIN_ROOT/skills/$workflow/scripts/validate_artifacts.py` generically for any `$workflow` argument, so `ocs validate research <path>` works the moment the file exists there.

Acceptance criteria: running the script against a hand-built conforming fixture exits 0; against each of the following broken variants it exits 1 with a message naming the specific defect — missing a required heading, an invalid `Status` value (document- or subsection-level), an `Answered` subsection with an empty `Sources:` list, a `Complete` document containing a `Partial`/`Unanswered` subsection, a `Partial` document with an empty `## Unanswered questions` section.

Verification: build the fixtures above as throwaway local files during implementation (this repo has no committed test suite for its validators — `interview`'s own validator ships without one — so ad hoc fixtures checked by hand during the implementation session match existing practice rather than introducing a new convention) and run `ocs validate research <fixture-path>` against each, confirming exit code and stderr message match the acceptance list. Failure behavior: an unexpected exit code or a message that doesn't name the actual defect means the check logic is wrong; fix before considering Step 3 done.

### Step 4 — `docs/purpose.md` reconciliation (small, separable from Steps 1-3)

Purpose: `docs/purpose.md`'s own header instructs "Revise it when a decision here is overturned, not when work happens" — this plan overturns two things stated or implied there (the six-skill count's treatment of `ping`, and the scope of the `autoresearch` deferral), so the header's own rule calls for this now rather than leaving the doc silently stale. Scope is narrow:

- Add `research` to the Scope enumeration.
- Add a clause noting `ping` is excluded from the six-skill count as infrastructure rather than a workflow skill (making Decision "seventh skill" above's reasoning part of the doc itself, not just this plan).
- Qualify the "Not in v1: `self-improve`, `autoresearch`" line to state that the deferral targets the autonomous, self-triggered reading of that capability, not a bounded, user-dispatched synthesis workflow — i.e., note that `research` is not what was deferred.

Acceptance criteria: the three edits above are present; nothing else in `docs/purpose.md` changes (in particular, do not pre-decide the `ralph`/`autopilot` ceiling collision named in the pre-mortem and Open Questions — that stays open).

Verification: there is no automated check for prose accuracy here — this is itself an ownership-gap edit (what the doc should say is a call the maintainer makes, not a checkable property), so verification is a human read-through by whoever merges it, not a script. This step can be reviewed and merged independently of Steps 1-3; it does not block building the skill itself.

## Open Questions

- **`ralph`/`autopilot`'s eventual shape.** `docs/purpose.md` Scope names both as committed, unbuilt workflow items that would collide with the just-reached six-skill ceiling once either is proposed. Whether either needs its own directory or can compose the way `team`/orchestration did ("no separate skill") is unresolved and deliberately not decided by this plan — deciding it now, for skills that don't exist yet, would be scope creep. Matters because the next proposal after this one will re-open the ceiling question this plan just closed for `research`.
- **Future `ralresearch`-style citation-integrity gate.** Decision 4 leaves the semantic citation-support check unbuilt pending evidence it's needed. If it is built later, the calibration/ablation `ocs eval` harness (`.agents/kein/eval/fixtures.json`, `ocs eval --help`) is the natural way to test whether a research-skill variant with the gate outperforms one without it, the same role it plays for `plan`/`ralplan` today — worth a fixture then, not now (machine-specific config, out of scope for this plan per the dispatch's own note).
- **Same-brief re-invocation convention.** Decision 2 calls for revising the same dated file when a follow-up invocation continues the same brief same-day, and writing a new dated file otherwise, mirroring `interview`'s continuation rule. This is a low-stakes convention call; if it proves awkward in practice (e.g., ambiguous same-brief detection), it can be adjusted during Step 1 without touching any other decision in this plan.
- **Cross-vendor research lanes.** `execute`/`ralplan` support naming another vendor for a lane via a dedicated `references/lanes.md`. This plan does not build an equivalent for `research` — `ocs ask` already serves all four candidate lane roles (`document-specialist`, `explore`, `tracer`, `architect`) as read-only roles, so the mechanism would transfer directly if ever needed, but nothing in this plan's evidence suggests it's needed for v1. Recorded as a deferred extension point, not a gap in the current design.
