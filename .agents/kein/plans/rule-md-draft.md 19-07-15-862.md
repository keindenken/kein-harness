---
paths:
  - "**/CLAUDE.md"
  - "**/CLAUDE.local.md"
  - "**/AGENTS.md"
  - "**/SKILL.md"
  - "**/.claude/rules/**"
---

# Writing into a standing prompt

This file is loaded whether or not the run needs it, so what follows is about how a line is written, not about whether the rule should exist. That second question has its own procedure, and by the time this file is open it has usually already been answered — if it has not, go answer it before writing.

**Every line has to be executable by whoever reads it.** Narration instructs nothing, and an instruction resting on a capability the reader was not granted fails without saying so. Name what a reader does differently because the line is there.

**Write only claims a reader can falsify from what they already have open.** Three shapes qualify: a pointer to the source that regenerates the claim, a fact pinned to a version together with the probe that re-checks it, or a mechanism. One shape disqualifies — a claim whose value moves with a defensible choice of method is underdetermined, and writing it at whatever number you happened to get is worse than writing the qualitative form. A number that is neither regenerable nor anchored gets deleted rather than corrected, and a number promoted into a rule is worse than one left in a measurement: the rule applies where the measurement never ran, so the figure stops meaning what it measured while still reading as authority. This bites on claims and not on preferences — a line that says which of two good things to prefer asserts nothing to check, and is not what this is asking you to justify.

**Test a premise by negating it.** If a line rests on a stated fact, deny the fact and read the instruction again. Survives: drop the fact, it was decoration, and decoration outlives its truth. Dies: the fact is load-bearing, and prose is the wrong place for it.

**Justification is three different things and only one of them goes here.** *Mechanism* — why the thing behaves this way — goes inline: it is bounded, checkable from source, and is what licenses a later deletion. *Provenance* — which incident produced the rule — goes in the commit message of the change that introduces it, so the history is the index and the rule carries no pointer to maintain. *An environment fact* goes into a mechanism that can hold it — a config field, a schema, a runtime check — because prose describing an environment cannot notice when the environment moves. Write the core and nothing else. A standing prompt is not a record of what happened on which afternoon.

**Content leaves the main file when a given run will not read it.** Not because it is long, and not because it is code. Splitting what every run reads is pure cost, and deferring a mandatory read relocates it rather than shrinking it — a reference the reader is told to open is still being paid for.

**Name the collision.** Point at the decision where this line meets one already present. If you can name that point, one of the two loses there and you have to say which. That there are already many rules is not itself an objection; a decision where two of them disagree is.
