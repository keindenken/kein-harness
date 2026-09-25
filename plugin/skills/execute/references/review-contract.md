# Execute Review Contract

## Reviewer Selection

Choose lanes by the current evidence question. This is neither a fixed reviewer matrix nor a fixed reviewer count. Every implementation or correction round requires at least one independent reviewer; complementary read-only lanes may run concurrently.

## Official Package

Supply the original bounded task, completion condition, repository instructions, relevant current code or diff, current fresh verification, selected rubric, task ID, round, and exact worktree fingerprint.

A new blind reviewer after correction receives no earlier finding, verdict, reviewer identity, correction note, claimed fix, closure result, or desired outcome. Wait for every selected lane, then consolidate the blocking findings before correction.

## Response

```markdown
VERDICT: PASS | REVISE | BLOCK
TASK_ID: task-001
ROUND: 1
WORKTREE_FINGERPRINT: <exact supplied fingerprint>

FINDINGS:
- Claim: <falsifiable defect or proof gap>
  Evidence: <precise location, observation, or contradiction>
  Impact: <realistic consequence>
  Required correction: <specific correction or missing proof>
  Severity: critical | important | minor
  Confidence: high | medium | low
  Blocks: <the clause of this task's completion condition it defeats, quoted — or `regression: <what>`, or `instruction: <which>` — or None>

UNCERTAINTY:
- <unresolved concern and discriminating evidence, or None>
```

The verdict follows the findings. `PASS` carries none; `REVISE` carries findings that all read `Blocks: None`; `BLOCK` carries at least one that cites something. The state refuses each way those can disagree, so the word is a summary of the findings rather than a second judgement about them. Every verdict binds to the supplied task, round, and fingerprint.

**`Severity` and `Blocks` answer different questions, and only the second decides acceptance.** Severity is how bad the defect is — the role's own calibration, kept. `Blocks` is whether *this task* is done, and it is a citation rather than a weight: quote the clause of the completion condition the finding defeats, verbatim, and the state checks that the clause is there. A `critical` defect outside this task's completion condition does not block this task; it becomes a task of its own. A `minor` one that defeats a clause blocks, because the task is not done.

`REVISE` accepts. The word means "accept, and disposition each of these", not "revise and review again": a finding fixed in place is checked by the lead reading the diff, with no fresh lane. Its findings are real, carried on the task and into the receipt, and none of them says the task is incomplete. That channel is why a lane never has to inflate a finding to keep it from evaporating — and why a `PASS` that lists findings in prose is a contradiction the state now refuses.

## Correction and Closure

Consolidate the `BLOCK` findings into one correction brief. After correction, require fresh `kein:executor` verification and at least one newly spawned, independent, new blind reviewer. A previous reviewer may run a primed closure check for a subtle or high-risk finding; its positive result cannot approve, unless the run was started with `--primed`: then the reviewer that raised the `BLOCK` may check its own correction and its verdict counts toward acceptance, still bound to the same task, round, and fingerprint as any other verdict, and still required to be independent of the executor. A blocking lane that raised nothing this round still gets a fresh lane. A negative closure check remains blocking evidence and stays hidden from fresh reviewers, primed or not.

A run started with `--max-rounds <n>` corrects at most `n` rounds per task, the first attempt counted as one of them. A `BLOCK` still open once the bound is reached stops the task rather than opening another round: it checkpoints blocked, and the lead reports the open findings. Nothing is accepted by running out of rounds; without the flag, correction is unbounded exactly as it always was.

## What acceptance carries

A task accepts over the findings a `REVISE` lane returned. Each is dispositioned once, at acceptance, and the disposition is one of three:

- **Fix it.** The executor corrects it within its `required_correction`, the task's verification path is re-run on the corrected tree, and the lead reads that diff. No fresh lane: the review that found it already happened, the finding never touched whether the task is done, and the final audit reads the whole change again. The acceptance records it under `fixed`, and it stands at the corrected fingerprint while the verdicts stand at the one they reviewed. A finding that cites the completion condition cannot take this route; that is a correction round.
- **Promote it.** Append a task whose rationale names the finding, and remove the finding from the task. The ledger already accepts an appended task at round zero; this is the existing mechanism, pointed at its intended input.
- **Carry it.** Leave it on the task; it projects into the receipt as `carried_findings`, which is the residual risk the final report names. Carrying costs the least now and the most later, so an `important` or `critical` carried this way must record `carried_because` — the state refuses acceptance without it — and a promotion that did not happen is a written decision rather than a silence. Severity prices the carry; it never gates the acceptance.

Nothing else is a disposition. A finding cannot be answered by deleting it from the list, because the receipt projects the list and a fresh audit reads the receipt.

## Revision Re-confirmation

Each acceptance records the input hash current at the moment it was made. `amend` moves the run's input without touching any acceptance already on the ledger, so an accepted task keeps naming the revision it was accepted under until something re-confirms it against the new one — the input-identity binding stays exactly as strict as it always was; `amend` is still the only way the input moves, and still only with a reason.

After an `amend`, dispatch one fresh, independent lane per amendment — not per task — given the amendment and the complete current text of every task accepted under an earlier revision. For each, it judges whether the task still satisfies its completion condition under the amended plan. A task it confirms moves to the amended revision, its verdict appended to the acceptance's own reviewers alongside whatever verdict originally accepted it; a task it judges no longer satisfying returns to correcting, the same route a `BLOCK` reopens through. The run cannot complete while any accepted task still names a superseded revision.

## Final Audit

Final reviewers receive the complete post-simplification tree, all task completion conditions, repository instructions, final verification, and the exact final fingerprint. Any later mutation invalidates their verdicts.

The audit is a sequence, and the sequence stops. The first pass is a fresh blind read of the whole change. Every later pass receives the previous pass's findings **and what was done with each one**, and answers two questions: are those dispositions sound, and is there a defect of a class no pass has raised yet. Nothing else is asked of it.

It has to stop somewhere, because it does not converge on its own: each correction enlarges the change the next pass reads, so a fresh blind lane keeps finding new claims for as long as lanes keep being dispatched. The stop is a disposition rule rather than a count. From the third pass on, a newly raised finding is **carried** — recorded in the run-level `carried_findings` with its `carried_because`, so the receipt's residual risk names it — unless it cites a task's completion condition, or the run itself introduced it as a regression. Those two are corrected, because a citing finding cannot be carried past acceptance or completion at all, and a regression is this run's own debt rather than something it inherited. The pass that carries answers `REVISE`, and completion accepts it: a final-audit verdict is held to the same coherence as an acceptance, against the run-level list rather than a task's -- `PASS` with none of its role's findings there, `REVISE` with at least one and none that cites. The match is by `reviewer_role`, not by lane, because a finding records only its role; so a later clean pass from a role whose finding an earlier pass carried answers `REVISE`, not `PASS`. That is what lets the sequence stop without a pass relabelling what it found.

A lane's prescription is not applied until the lead re-derives the claim under it. A second lane repeating a claim is not evidence for it; two lanes can be wrong about the same thing, and a prescription applied on the strength of repetition has to be undone by whichever later pass finally checks it.

Ask each pass for its substantive findings first and its convention sweep — comment wording, formatting, house style — as an appendix. The two cost the same to report and nothing like the same to act on, and a defect queued behind a wording breach is a defect found a pass later than it needed to be.
