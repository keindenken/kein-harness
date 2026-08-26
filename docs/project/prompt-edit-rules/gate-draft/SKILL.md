---
name: revise
description: Use before adding a rule to a standing prompt, and when auditing one that already has rules — a CLAUDE.md, an AGENTS.md, a skill, a role prompt. Decides whether a rule should exist at all and what would license removing it. Not for writing the line once that is decided.
---

# Revising a standing prompt

This decides **whether a rule should exist**. How to write it once decided is a separate question, and the `standing-prompt` rule injects itself when the file is opened.

A rule that describes how you want an agent to work gets no staleness signal. Nothing external marks it false, and testing whether it is still needed means removing it — which is disobeying it. So the two decisions this skill covers are asymmetric on purpose. Adding needs one moment of resistance at the point where hands are already moving. Removing needs an arsenal, because nothing ever brings it up.

Two modes, and both handle addition and removal:

- **Before.** A rule is about to be added or a prompt is about to change.
- **After.** A prompt already has rules and nobody has re-argued them.

## Adding

**Almost none of this goes into the file.** These checks are instruments for deciding, and an instrument that leaves residue in the product has become part of it. Of the checks below, one leaves a clause beside the rule — *name the mechanism* — and one leaves a setting outside it — *the off-switch*. The rest leave nothing at all.

That is easy to get wrong in one direction only. Having just written a paragraph about what a strong agent would do here, you will want to keep the paragraph. Keeping it puts reasoning in a file that is read as instruction, and a later reader will obey it, cite it as precedent, and stretch it to a case it does not cover. Put that paragraph in the commit that makes the change, where a rule's reasons already go.

**What does it forbid that you would want?** Every rule refuses some outputs. Name them before you find them at runtime. Three sub-questions settle it:

- *Name the consumer.* Who reads the artifact this rule requires? A rule that mandates work nobody consumes is pure standing cost.
- *Name the best behaviour.* Write what a strong agent doing its best would produce here, then check the rule lets it through. If the rule would block that output, the rule is wrong and the failure it was written for is somewhere else.
- *Name the mechanism.* Why does this work — bounded, checkable, and stated in a form a later reader can find false. This is the one sub-check with a product — one clause, beside the rule, in the form the `standing-prompt` rule prescribes. The other two are pure gates and end when you have answered them.

**Is it already written?** Search the prompts you already ship before adding an eleventh sentence about the same thing. A rule restated in a second place does not double its force; it splits the reader's attention and gives you two copies to keep true.

**Can a run answer whether it earned its place?** Ship the rule with a way to turn it off — a flag, a setting, a mode, not a sentence saying the rule is optional. A rule's cost is not found by thinking about it — it is found in runs, in attempted use, in a reader's objection. An off-switch turns not following the rule from a violation into a use, which is the only thing that dissolves the removal problem below.

**What stops this text from growing?** Trigger text is the clearest case: firing too rarely adds scenarios, firing too often adds exceptions, and both directions add. Every bound you write needs to name what stops it. A budget holds when the thing obeying it is a process that gets re-run, and fails when a person has to argue against it each time — which is why the answer here is a process and not a number written into the prompt.

**Does prevention's standing cost beat the exposure?** Not the size of the failure — the standing cost is what the rule charges on every run where nothing happens: tokens on each dispatch, steps a compliant agent walks, and the good outputs it makes an agent refuse. A guard that charges nothing until it fires survives even at zero exposure. A guard that polls does not.

## Removing

**Absence of violations is not evidence.** A rule guarding a state that is rarely entered passes clean round after clean round for free, and nobody counts how often the state was entered. Routing rules read backwards on top of that: the violation count rises when the rule is working, because a rule that is doing its job is a rule people are hitting.

**The moves are four, not two.** Cutting is the last one, not the first:

- attach a measurement and demote it to insurance that says it is insurance;
- make it conditional, so a run it does not bear on pays nothing;
- move it to a mechanism, so the runtime enforces what prose was asking for;
- narrow the boundary it claims, so it stops asserting where it was never tested.

Reaching for cut-or-keep first is how a real finding gets thrown out alongside a rule that needed one condition.

**Warrants a single command settles.** Each of these is a command to run rather than a judgement to make, so run them:

1. Nobody consumes the artifact the rule requires.
2. A mechanism now holds it, so it is structurally redundant.
3. Complying manufactures false data.
4. It contradicts its own checker. When prose and checker disagree, default to the checker being the older side — prose is cheaper to change, so it is the side that drifted.
5. The transcript shows work wasted on compliance.
6. It has been amended repeatedly (`git log -G`).
7. The cause it was written for is gone.
8. It overgeneralised from the single incident that produced it.

The last two need the reason the rule was added, which is in the commit that added it, so `git log -- <file>` settles them the same way the others are settled.

**The experiment is a violation, and there are two ways around it.** Testing whether a rule is needed means running without it, and running without it means disobeying it. That explains why nobody touches a rule; it does not make touching one impossible.

- The off-switch above. If the rule shipped with one, using it is not a violation.
- An external change that licenses the deletion for you. This works only for a rule describing an external surface — when the surface moves, the rule is already false and removing it needs no experiment.

"There is no fixture for this" is a conclusion, not a starting condition. Ask what a fixture would have to show before accepting that none can exist.
