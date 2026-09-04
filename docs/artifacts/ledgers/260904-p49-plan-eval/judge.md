# Task: compare the two plans, forced choice per dimension

Read `common.md` first (same directory as this file).

Read the kickoff document. Then read the two plans **in full, in the order your task names** (first plan, then second). Do not skim the second because the first was long.

For each of the five dimensions below, choose `A` or `B`. A tie is not allowed. Give `confidence` as `low`, `medium`, or `high`. Give at least two line-cited reasons for the plan you chose and at least one line-cited reason that favours the other, so a reader can see what you weighed.

1. **Scope fidelity.** Which plan answers the kickoff document's rulings more exactly: covering what the owner ruled in, leaving out what the owner ruled out, and not quietly deciding what the owner reserved. Cite kickoff lines and plan lines.
2. **Decision completeness.** Which plan leaves fewer material decisions (architecture, scope, acceptance semantics, safety) unmade and unlabelled. A decision explicitly parked for the owner with a named question counts as made; a silent assumption counts against.
3. **Executability.** From which plan could a worker start a story and finish it in one round without asking, with a completion condition that is bounded and testable. Consider story size: files, acceptance claims, gates to implement and drive to a failing state.
4. **Gate proportionality.** Whose gates can each fail for a named reason, guard something a story actually changes, and are not larger than the thing they guard. Cite the gate section's size in lines against the code change it guards.
5. **Handoff readability.** Which plan costs a worker less to find what to do for one story: fewer forward references, less repetition, less text addressed to reviewers rather than workers.

Then: an **overall** choice with confidence, and one paragraph on what the losing plan does better that the winner should take.

Finally, **framing.** In each plan, find up to five sentences that tell the reader how to weigh or feel rather than stating a fact or an instruction to act — a constraint hoisted above the problem it belongs to, a rubric ending that tells a reviewer what to look for, an adjective doing the work an argument should. Quote each with its line number. This section is observation, not a scored dimension.

Output as headed markdown: one heading per dimension, then Overall, then Framing.
