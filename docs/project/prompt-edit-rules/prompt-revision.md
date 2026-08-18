# Changing a standing prompt

What to check when adding to or cutting from a `CLAUDE.md`, a `SKILL.md`, or an agent persona.

Its purpose is that a prompt gets changed the same way in November as in August, rather than according to whatever seemed reasonable that afternoon.

**This document is prose, not a prompt.** The form rules below govern prompts and do not govern this file. The exposure is real anyway: an agent reads this at the moment it edits a prompt, so however the checks below are written is a template it may copy. That is a reason to keep the *shape* of a check honest here, not a reason to treat this file as bound by its own contents.

Rewritten 2026-08-11 after ten analyses and three reviews. The analyses are at `docs/project/prompt-edit-rules/260810-prompt-revision/`, every claim in them cited to a path or a commit. `git show` on this file has the two earlier versions, and the second one had several claims the reviews then falsified — those are listed at the end rather than quietly dropped.

## Which kind of rule is this

A rule that describes an **external surface** — an API, a tool's behaviour, a file format — gets its edits handed to it. When the surface changes the rule becomes false and someone has to fix it, on a schedule nobody here chose.

A rule that describes **how you would like an agent to work** never gets that. Nothing external will ever tell you it is stale. Every standing prompt in this harness is of the second kind, which is why the rest of this document is needed and why several warrants below can never fire here.

Do not read this as "external rules shrink". Across three releases of one vendor corpus the deltas ran both ways — one release added a paragraph, the next removed a topic from four sites. What arrives on someone else's schedule is the *occasion to edit*, not a direction.

## Adding

**Can it bind?** An instruction that narrates what happens instructs nothing, and an instruction that needs a tool the agent was not granted fails silently.

**What does it forbid that you would want?** Ask whichever of these applies. Each can come back unanswerable, and an unanswerable one is the finding:

- *Name the consumer.* If the rule requires an artifact, who reads it? Twice here the answer was nobody — `7b3a350`, where the state schema would have rejected the artifact a compliant lead produced, and `399b26b`, where a model asked for a timestamp it could not know invented one nine hours before the run started.
- *Name the best behaviour.* Write what a strong agent would do at its best, then check the rule scores it a pass. Three times here the rule punished the better artifact; `736cc30` is the clearest, where a check was widened against a warning its own comments carried twice.
- *Name the mechanism.* Could a config field, a schema, or a script hold this instead of prose? Only across a process boundary — see the call/paste distinction under Placing.

**Does it collide?** Point at the decision where this rule meets an existing one. If you can name that point, one of the two loses there and you have to say which. This is the one dilution mechanism with evidence behind it; rule *count* has none.

**Is it already said where the agent will see it?** `rg -w '<term>' plugin/prompts/*.md plugin/skills/*/SKILL.md plugin/skills/*/references/*.md` — fourteen role prompts and the skill bodies. That is the whole canonical set.

**Ship it with its own off-switch.** No cost of a rule in this repository was ever found by thinking about it; every one was found by a run, a use attempt, or a reader objecting. So make the run able to answer. A per-agent opt-out, a flag file, an `enabled: false` — the affordance exists in other harnesses, though none of them connects it to measurement either. It also dissolves the removal problem below: not following the rule becomes a use rather than a breach.

## Placing

**Content leaves the main file when a given run will not read it.** Not because it is long, and not because it is code — a router file in one vendor corpus held 546 words inline and pushed out 8,034, while a single-path file of the same family held 4,441 inline. There is no reliable correlation between branch count and file size across that corpus, so treat this as a rule about what a run reads, not as a size heuristic.

Splitting content that every run reads is pure cost. And progressive disclosure can relocate a mandatory read rather than shrink it: the file the same family defers to declares a 14,557-word obligatory read across three files.

**Trigger text has two known stops, and needs one.** Both failure directions repair by addition — under-firing wants more scenarios, over-firing wants more exclusions — so it ratchets with nothing to stop it. Two caps observed elsewhere: a maximum of five routing scenarios, and a character limit enforced by silent truncation at runtime. The second works and the first is argued about, which is the general lesson: **a budget holds when the thing obeying it is a process that gets re-run, and fails when a person has to argue against it each time.**

**Comments behave differently by file kind.** Measured 2026-08-11, three runs per condition: an HTML comment in `CLAUDE.md` never reaches the model, while one in a `SKILL.md` or in a file passed to `--append-system-prompt-file` is delivered verbatim. Only the first is documented; the other two are not, and the flag is not in `--help`. So a `CLAUDE.md` can carry a rule's provenance beside it at no cost to the agent while staying visible to whoever opens the file — which is the reader who decides whether to delete it. Nothing else can. Re-check with a marker in a comment and one outside it before relying on this.

**Moving text into `references/` breaks its relative links.** The same path string resolves from the skill root and dies one level down. After moving, add a `../` and re-grep the links — the failure is silent.

## Writing

**Write only claims whose falsity a reader can establish from what they already have open.** Adapted from a rule this owner adopted for a different artifact after three consecutive audit passes found its own numbers wrong: *a number that is neither regenerable nor anchored gets deleted, not corrected*.

Three shapes qualify — a pointer to the source that regenerates the claim, a fact anchored to a version and a probe that re-checks it, or a mechanism. A fourth disqualifies: a claim whose value moves with a defensible choice of method is underdetermined, and writing it at whatever number you happened to get is worse than writing the qualitative form.

One exception: a cached value may stay when the retrieval instruction beside it does not depend on the cache being right. A vendor index of stale line numbers costs nothing because the same file names grep-by-symbol as primary and the numbers only as an accelerator.

**Justification is three different things and they go to three places.** *Mechanism* — why the thing behaves this way — goes inline, because it is bounded, checkable from source, and is what actually licenses a later deletion. *Provenance* — which incident produced the rule — goes outside, because it is unbounded and cannot settle a removal anyway. *Environment facts* go inline but quarantined: a dated, version-pinned block that says it is perishable and names the probe that re-checks it. `~/.claude/kein/prompts/lead.md` is the only file here that does this; copy its shape.

The two external corpora disagree about provenance. One carries no dated incidents in 158,000 words; the other includes them and its own skill template prescribes a "Real-World Impact" section. This is a live disagreement between houses, not a settled convention.

**Test a premise by negating it.** If a line rests on a stated fact, deny the fact and see whether the instruction survives. Survives: drop the fact. Dies: it is an environment fact and belongs in the quarantined block.

## Removing

**The deciding question is whether the standing cost of prevention beats the exposure.** Not the size of the failure. Standing cost is what the rule charges on runs where nothing was going to go wrong: tokens on every dispatch, steps a compliant agent must take, and good outputs it refuses. A guard that costs nothing when it does not fire survives a zero exposure measurement; one that polls four times a second does not.

**There are four moves, not two.** Cutting is the last of them. Demote it to declared insurance with the measurement attached; make it conditional so an unaffected run pays nothing; move it to a mechanism; or narrow the boundary it claims. Reaching for cut-or-keep first is how a real finding gets thrown away with a rule that only needed a condition.

**Warrants that a command settles.** Each is one grep or one reading:

- nothing consumes the artifact it requires
- it is unnecessary by construction, because a mechanism now holds it
- complying produces false data
- it contradicts its own checker — and when prose and checker disagree, default to the checker being the older one, since prose is cheaper to edit
- the transcript shows work wasted in obeying it
- it has been amended repeatedly. `git log -G` on the line; a line that keeps being patched may not fit, though this rests on three lines in one file and could be measuring contentiousness instead

**Warrants that need something the file does not hold.** These are real but not cheap, because the provenance they need lives outside by the rule above: the cause it was written for is gone; it over-generalises from the single incident that produced it. Budget a search, or leave them.

One warrant cannot fire here at all — *the surface it describes changed* — because no standing prompt in this harness describes an external surface.

And one carries a caveat: *a surviving general rule already covers it* is a claim that the general form re-derives the specific case, which is testable and has failed. Run the derivation before trusting it.

**Absence of failure is not a warrant.** A rule guarding a state entered once in twenty rounds survives five clean rounds trivially, and nothing here counts how often the guarded state was entered. A routing rule reads backwards on top of that: its violation count goes *up* when it is working.

**The experiment is a violation, but it has been done.** Testing whether a rule is needed means removing it, and removing it is disobeying the rule — which explains why nobody reaches for it, not why it is impossible. It was done once here: the Critic's severity floor was restored as a three-line overlay and produced no behavioural change across five replicates per arm, against a fixture built to contain the rare state on purpose. "No fixture exists" is a conclusion, not a starting condition. The two ways round the violation are the off-switch under Adding, and an external change that authorises the removal for you — the second only for the first kind of rule.

## What is not true, and was believed here

Recorded so it is not rediscovered and re-adopted. The first three were in the 2026-08-09 version; the rest were introduced by the 2026-08-10 rewrite and caught by review.

- **Adding a rule weakens the rules already present, by count.** No evidence either way. The measurement that looked like evidence — a Critic prompt at 3,047 words against one at 1,115 — was never run; what was run compared 1,115 against 1,115 plus three lines, and bounds only very small changes.
- **A rule carrying its own argument makes removal ordinary.** Real removals here came from disproven mechanism. Whether the dated clauses helped was inferred from a narrative, not observed.
- **Commit messages are where the argument lives.** Still not true here, but the reason given above was itself wrong and closed off a route that is open. Retrieval works: `git log -S` matches a change in occurrence *count*, so it finds the commit that removed a line rather than only commits about present text, and `git log -- <path>` needs no wording at all. Checked 2026-08-15 — `git log -S'Six is the working ceiling' -- docs/purpose.md` returns `9d79fdd`, the commit that deleted it, and the path filter alone lists every commit that touched the file with its reason in the subject. What fails is supply, not retrieval: most prompt words here attribute to a handful of bulk port commits carrying no argument for any individual line. So the belief is false as a description of this repository and true of any repository whose commit convention makes it true. Re-derive with `git blame` over `plugin/**/*.md` before citing a figure.
- **Dissolving an instruction into structure is always best.** Only across a *call* boundary, where the script runs in another process. A script that gets pasted costs more than the prose it replaced.
- **A good compression must let you re-derive the specific cases from the general form.** Overstated as a failure. Tested on two live prompts, it passed one and failed the other, and the failures identified rules that a separate pass had independently flagged as misfiled. It is a usable check — but it measures enumeration, not behaviour, so a failure is decisive and a pass is not.
- **Rules about an external surface shrink over time.** They change over time. Direction was read off two deltas, one of which was an addition.
- **One topic growing until it crowds the rest is a supported dilution mechanism.** It is a plausible reading of an older note, with nothing behind it.

## Open

Three reviewer-design questions surfaced while writing this and do not belong here: which way a reviewer should default, whether a `PASS` must carry an artifact of the attempted attack, and how the Critic should be told to weight a plan's own rationale. They are in the analyses at `docs/project/prompt-edit-rules/260810-prompt-revision/` and want their own decision, not a paragraph in this file.
