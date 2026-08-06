---
name: interview
description: Use when the user asks to be interviewed, presents a vague or conflicting idea, or needs intent, scope, constraints, non-goals, decision boundaries, or acceptance criteria clarified before planning or implementation.
---

# Interview

<Purpose>

Turn the user's free-form idea into a requirements document whose material decisions are explicit enough for downstream work without inventing product choices.

Success means the document captures the intended outcome, boundaries, constraints, and acceptance evidence. Question count and elapsed time are not success measures.

</Purpose>

<Use_When>

Treat the invocation arguments and current user message as the initial brief. If the brief is already sufficient, do not ask the user to restate it.

</Use_When>

<Do_Not_Use_When>

Do not use this workflow to plan, implement, review an already complete requirements document, or make a purely discoverable repository fact into a user decision.

</Do_Not_Use_When>

<Non_Negotiable_Boundaries>

- Remain in requirements clarification from intake through artifact finalization.
- Ask at most one user question per message.
- Do not plan, implement, commit, or invoke another workflow.
- Do not persist a full transcript or routine question-by-question history.
- Do not use numeric clarity thresholds, question quotas, or routine progress displays.
- Distinguish descriptive repository facts, inferences that require confirmation, and human decisions.
- Obtain explicit consolidated approval before marking an artifact `Approved`.
- Write the requirements document and stop after reporting its path and explicit deferrals.

</Non_Negotiable_Boundaries>

<Workflow>

1. Read the initial brief and any surviving active ledger.
2. Ground brownfield work in the smallest useful repository evidence before asking the first question.
3. Frame the intended outcome and independent top-level components internally.
4. Establish the requirements output path and create or resume the active ledger.
5. Ask one highest-leverage unresolved human-decision question at a time.
6. Apply one proportional pressure question only when a material decision needs discriminating evidence.
7. Audit readiness against the required artifact sections and unresolved decisions.
8. Present one consolidated decision-bearing summary and request explicit approval.
9. Write either an approved document or a clearly blocked draft, validate the artifact and ledger, then stop.

Continue questioning only when the next answer could materially change scope, behavior, constraints, acceptance evidence, or a downstream architectural decision. Stop asking when another answer would only improve wording.

</Workflow>

<Question_Selection>

Choose the unresolved decision with the greatest chance of changing the resulting work. Prefer product intent, behavior, scope, and operational boundaries over implementation details.

For a multi-component request, identify outcomes that can succeed or fail independently. If the supplied detail is uneven, first ask one topology or scope-framing question when a different interpretation would change implementation; do not request detailed flows and acceptance criteria for every component in one message.

Use an open-ended question for intent, context, or an unenumerated domain rule. Ask it as ordinary prose.

Use a bounded question when genuine alternatives are already understandable. Name the competing decision boundaries explicitly, include a justified recommended option when evidence supports one, and allow free-form correction when the choices may be incomplete. A confirmation question that proposes only one behavior is not a bounded comparison while a competing material behavior remains viable; state both alternatives in the user-facing question. Do not replace the material boundary with a nearby but lower-impact question.

Ask a bounded question with `AskUserQuestion`, one question per call: each competing boundary is an option whose description states its actual consequence, the recommended option comes first and is labelled so, and the automatic free-form choice carries the correction path. Fall back to prose when the boundaries do not survive compression into short labels, when more than four are genuinely live, or when the choice depends on reasoning the option descriptions cannot carry. A bounded question that has been flattened into unrecognisable labels has become a different, lower-impact question.

When a material design choice exists, compare two or three viable approaches, state their actual trade-offs, recommend one, and ask the user to decide or correct the framing.

Pressure-test only when a high-impact answer rests on an assumption, conflicts with evidence or terminology, lacks an acceptance signal, or leaves a material boundary unclear. Use the cheapest discriminating move: an example, counterexample, exposed assumption, forced trade-off, boundary case, or governing-term choice.

</Question_Selection>

<Repository_Grounding>

Before the first brownfield question, inspect applicable `CLAUDE.md` and `AGENTS.md` files, project documentation conventions, relevant requirements or decision records, and the smallest useful code surface.

Use direct read-only inspection first. Delegate to an exploration agent only when direct inspection cannot efficiently resolve a materially broad or ambiguous evidence question.

Do not ask the user to rediscover a repository fact that inspection can establish. Record exact descriptive facts with paths or symbols. Label uncertain interpretations as inferences and ask for confirmation only when they affect desired behavior.

If documentation and code conflict, cite both facts and ask which behavior should govern. If inspection fails, record the evidence gap and ask only the human decision that cannot safely proceed without it.

</Repository_Grounding>

<Ledger>

Read [ledger-template.md](references/ledger-template.md) completely before creating or finalizing a ledger.

Run `ocs state-dir runs/interview` to resolve the run root, and store the ledger at `<run-root>/<YYMMDD-HHMMSS>-<slug>/ledger.md`. The run root sits inside the repository so an interrupted interview can be resumed by any vendor working there, not only the one that started it.

For a new interview, record the canonical working directory, canonical repository or `none`, resolved output path, original request or prompt-safe summary, confirmed decisions, constraints and non-goals, decision boundaries, repository evidence, open questions, and explicit deferrals.

Update the ledger only when a decision is established, changed, invalidated, or deferred, or when material evidence changes the decision surface. Never append every exchange.

On resume or after compaction, search for active ledgers matching the canonical repository and topic. Resume a single unambiguous match; ask the user to choose only when multiple matches remain. Read the ledger first, treat its confirmed decisions and unresolved questions as authoritative surviving context, and show unresolved decisions once.

Show unresolved decisions only when the user asks for status, after resume or compaction, or immediately before approval.

Do not silently convert an unresolved blocking decision into a deferral. A valid deferral names the boundary that remains fixed and the later decision gate; otherwise keep the artifact Draft or ask the one blocking question.

Run `ocs validate interview ledger <path>` before relying on an active ledger and before accepting a terminal receipt as valid.

After a validated Approved artifact, replace the active ledger with the compact completed receipt. Preserve an interrupted active ledger. On explicit cancellation, replace it with an aborted receipt and do not create an approved document.

</Ledger>

<Requirements_Artifact>

Read [requirements-template.md](references/requirements-template.md) completely before writing the artifact.

Run `ocs state-dir requirements` and write to `<that path>/YYMMDD-<slug>.md`. Follow the target project's own convention instead when it already has one for requirements documents specifically; a general `docs/` tree is not that convention, and this artifact does not belong there.

Continue an existing artifact only when it belongs to the active interview. Refuse to overwrite a differing artifact from another interview; use a short numeric suffix when provenance remains ambiguous.

The artifact must cover context, desired outcome, in-scope and out-of-scope behavior, requirements, constraints, implementation decision boundaries, acceptance criteria, decisions and rationale, relevant system evidence, assumptions and risks, and explicit deferrals.

Present one consolidated summary containing all decision-bearing material and ask for explicit approval. A casual request to write and start building does not resolve a blocking decision or authorize an Approved status.

Use `Status: Approved` only after explicit consolidated approval and when no blocking decision remains. If the user requests a document while a blocking gap remains, use `Status: Draft`, add a non-empty `## Blocking gaps` section, keep the ledger active, and do not imply readiness for planning or implementation.

Generate prose only from the approved summary and ledger. Do not introduce a new product decision while writing.

Validate the generated document against the approved summary and active ledger, then run `ocs validate interview requirements <path>`. If validation or comparison fails, keep the ledger active, correct the document, and revalidate before reporting completion.

</Requirements_Artifact>

<Interruption_And_Failure>

- On temporary interruption, preserve the active ledger and report how to resume.
- On explicit cancellation, write only an aborted receipt and report that no approved artifact was created.
- When project instructions conflict with a default path or format, follow the project instructions and record the resolved output path.
- When the user asks to proceed into planning or implementation, complete only the requirements boundary allowed by the current approval state and stop.
- When writing fails, preserve the active ledger, report the exact failure, and do not claim that an artifact exists.

</Interruption_And_Failure>

<Final_Checklist>

- Repository grounding used applicable instructions, documentation conventions, and the smallest relevant code surface.
- Every user question resolved one material human decision and did not ask for discoverable facts.
- Every independent outcome is covered, excluded, or explicitly deferred.
- Scope and non-goals are explicit.
- Constraints and implementation decision boundaries are explicit.
- Acceptance criteria are observable or testable.
- Pressure was applied only where a high-impact answer needed discrimination.
- Approved status has explicit consolidated approval and no blocking decision.
- Draft status exposes every blocking gap and leaves the ledger active.
- The requirements artifact passes `ocs validate interview requirements`.
- The ledger passes `ocs validate interview ledger` and is active or collapsed consistently with artifact status.
- The final response reports the artifact path and explicit deferrals, then stops without a downstream handoff.

</Final_Checklist>
