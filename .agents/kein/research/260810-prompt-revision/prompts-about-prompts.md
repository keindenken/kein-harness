# Stage 2 — prompts about prompts

Corpus: the eight skills whose subject is writing instructions, in `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/`. Every file in each directory read (28 files, ~370 KB): `plugin-dev/skills/{skill,agent,command,hook}-development`, `hookify/skills/writing-rules`, `claude-md-management/skills/claude-md-improver`, `example-plugin/skills/{example-skill,example-command}`.

Baseline: all six Stage-1 analyses read first. Nothing already in them is reported here as a finding.

---

## 0. Independence, stated before anything else

**This corpus is far less independent than its file count suggests, and one measurement settles it.** `plugin-dev/skills/skill-development/references/skill-creator-original.md` and `plugin-dev/skills/skill-development/SKILL.md` share whole paragraphs verbatim — "About Skills", "Anatomy of a Skill", the three-level progressive-disclosure list, the `references/` bullet, the imperative-form paragraph. `skill-development` is a fork of `skill-creator` with plugin-specific steps grafted on. The four `plugin-dev` skills cross-cite each other as exemplars (`skill-development/SKILL.md:296-316`, `:606-614`) and share a section skeleton (Overview → Format → Fields → Best Practices DO/DON'T → Validation Checklist → Quick Reference → Additional Resources).

So: **agreement inside `plugin-dev` is one author templating and carries no evidential weight.** The only genuinely separate voices are `hookify/writing-rules` (different plugin, different mechanism, different assumptions) and `claude-md-management/claude-md-improver` (different plugin, different genre). Where I report convergence below I say which of these three sources it spans.

**The frame that governs how much of this transfers.** `command-development/references/marketplace-considerations.md:7`: *"Commands distributed through marketplaces need additional consideration beyond personal use commands. They must work across environments, handle diverse use cases, and provide excellent user experience for unknown users."* A large fraction of the corpus's apparatus — semver, deprecation windows, `/help` copy, platform fallbacks, beta channels, keyword blocks for marketplace search — exists because these instructions have **strangers as dependents**. kein's standing prompts have one reader. Discount accordingly, and note the corollary in §3 item 4: the corpus's real evaluation instrument is the stranger, which is an instrument we do not have.

---

## 1. The delta

### D1. A prohibition taught by counterexample cannot be stated without instantiating what it prohibits

The corpus's dominant instructional unit is not "rule + mechanism" — it is the paired contrast: ❌ bad / ✅ good, with a `**Why bad:**` / `**Why good:**` label attached to the *demonstration* rather than to the rule (`skill-development/SKILL.md:451-539`; `agent-development/references/system-prompt-design.md:272-336`; `command-development/references/frontmatter-reference.md:56-58`; `writing-rules/SKILL.md:264-281`; `claude-md-improver/references/update-guidelines.md:64-107`). It appears in all three independent sources.

The consequence is structural and it is the closest thing in this corpus to the Stage-1 calibration insight. `skill-development/SKILL.md` bans second person — line 160: *"Write the entire skill using imperative/infinitive form … not second person"* — and in order to teach that ban it contains, verbatim, second-person text at lines 377-378, 393, 410, 494-496. **The file that forbids a string must contain the string.** Stage 1's D9 ("does the document obey its own rule", `counterpart.md`) scores that as a defect caught three times in kein's history. Here the violation is not a lapse; it is entailed by the teaching form. A prohibition-by-counterexample is self-violating by construction, exactly as removing a rule to test it is a violation of the rule being tested.

Two second-order costs, both visible in the corpus and neither acknowledged by it:

- **The form doubles the token cost of every rule and it is what busts the corpus's own budget.** `skill-development/SKILL.md` is 3,195 words against its own stated ceiling (`:329` *"Keep under 3,000 words, ideally 1,500-2,000 words"*), and the overflow is largely paired examples — the "Common Mistakes to Avoid" section alone (`:451-539`) is four rules expressed as eight code blocks.
- **The negative half enters context as literal text.** The corpus never asks whether an instruction that displays the forbidden form has a different effect from one that only names it. Nothing here measures it; I flag it as the obvious probe this stage suggests and Stage 1 could not have suggested, because kein's prompts are almost entirely declarative one-liners and the question does not arise.

**Why Stage 1 could not have produced it:** the house form in `kickoff.md`, `lead.md`, `worker-brief.md` and `AGENTS.md` is *rule plus one clause of mechanism*. There is not one ❌/✅ pair in the material Stage 1 read. The tradeoff between the two teaching forms is invisible from inside a corpus that only uses one.

### D2. Grammatical form can make a rule inert, and that is a named, first-party failure mode

`command-development/SKILL.md:34-59`, under the heading **"Critical: Commands are Instructions FOR Claude"**: *"When a user invokes `/command-name`, the command content becomes Claude's instructions. Write commands as directives TO Claude about what to do, not as messages TO the user."* With the worked pair: `Review this code for security vulnerabilities including: …` versus `This command will review your code for security issues. You'll receive a report…` — and the diagnosis at `:59`: *"The second tells the user what will happen but doesn't instruct Claude."*

Restated in the second independent-ish file: `command-development/examples/simple-commands.md:5` — *"All examples below are written as instructions FOR Claude (agent consumption), not messages TO users. Commands tell Claude what to do, not tell users what will happen."*

**Why Stage 1 could not have produced it:** every question in the six analyses is about whether a rule is *needed*, *justified*, *loaded*, *costly*, or *stale*. None asks whether a rule that is present and correct is **syntactically capable of binding**. A descriptive sentence about the workflow reads as a rule to its author and as narration to the model. This is a desk-time test with a failure state — does every paragraph contain an imperative whose subject is the reader — and `counterpart.md §5` explicitly reports that it could find no desk-time test that works on prose. This is one.

The corpus then violates it comprehensively: `command-development/references/documentation-patterns.md:208-224`, `marketplace-considerations.md:218-223`, `:581-594`, `:809-811` and `advanced-workflows.md:50-55` all put user-facing UI copy ("💡 TIP", an emoji rating widget, "**Thank you for beta testing!**") in the command body, which *is* the prompt. So the rule's own corpus supplies its base rate.

### D3. The rules whose failure mode is *never being loaded*, and where both repairs are additions

Every artifact in this corpus is loaded conditionally, on a routing decision the model makes from a `description` field. That creates a failure class kein has no instance of, and the corpus treats it as the primary one.

- `agent-development/references/triggering-examples.md:180-197` — the debugging section. **"Agent not triggering"** → *"Fix: add or expand scenarios in the body, and tighten the prose summary in `description:`."* **"Agent triggers too often"** → *"Fix: narrow the scenarios; add a 'Do not invoke when…' line to `description:` if needed."*
- `:187` — *"There isn't a more-specific competing agent winning the routing decision."*
- `example-plugin/skills/example-skill/SKILL.md:85` — *"Avoid overlap with other skills' trigger conditions."*
- `skill-development/SKILL.md:243` — the first listed "common improvement" is *"Strengthen trigger phrases in description."*
- `command-development/references/plugin-features-reference.md:56-73` — name-collision avoidance: *"Avoid conflicts with common command names"*; avoid `/test`, `/run`, `/do-stuff`.

**Both directions of routing error are repaired by adding text.** Under-firing adds scenarios; over-firing adds a negative clause. That is a second ratchet with a completely different driver from §1's — not an incident, a missed dispatch — and it runs in a field that is **always in context** (`skill-development/SKILL.md:81`, *"Metadata (name + description) — Always in context"*), across every installed skill simultaneously. It is the one place in this whole domain where per-line attention cost is unambiguously real and unambiguously paid whether or not the rule ever applies.

The corpus's answer is a two-tier split of the trigger text itself, and it is the sharpest engineering move in the corpus: `agent-development/references/triggering-examples.md:5-11` puts a flat prose summary in `description:` (loaded always, at routing time) and the worked scenarios in a **"When to invoke" body section** (loaded only after the agent is dispatched, i.e. after the routing decision it describes has already been made). Every shipped example ends its description with a pointer into the body (`examples/complete-agent-examples.md:12`, `:96`, `:178`, `:248`).

**Why Stage 1 could not have produced it:** kein's standing prompts are injected unconditionally — `--append-system-prompt-file`, `CLAUDE.md`, role prompts on dispatch. There is no artifact in the Stage-1 material whose presence depends on a model judging a description. `attention-cost.md D3` gets closest with the 11/14 grep, but that is about duplication among *loaded* prompts, not about competition for *loading*.

### D4. Just-in-time rule delivery, and its three prices

Two of the three independent sources put the rule text **outside the context entirely** until the guarded action is attempted, then inject it.

- `hook-development/SKILL.md:22-41` — prompt-based hooks, *"(Recommended)"*: a rule is a natural-language string handed to a separate model invocation at a lifecycle event, with only the tool input in scope.
- `hookify/skills/writing-rules/SKILL.md` (whole file) — a rule is a regex + a markdown message; the message reaches Claude only when the pattern matches an actual Bash command or edit.

This dissolves §3's attention question by construction: an instruction that is not in context cannot compete with anything. It is a fifth move for `attention-cost.md D8`'s list (cut / compress / re-file / dissolve / render-per-audience) — **externalise to a just-in-time judge** — and it is not the same as "dissolve into structure", because the rule stays in natural language and stays fallible.

The prices, which are the specialist part and which Stage 1's "dissolve is strictly best when available" does not carry:

1. **No rule can depend on another rule.** `hook-development/SKILL.md:497-518`: *"All matching hooks run in parallel … Hooks don't see each other's output. Non-deterministic ordering. Design for independence."* Restated `references/advanced.md:198`, `:431`, `:442-448` (*"This can fail because hooks run in parallel!"*). Prose rules in one file can be sequenced; externalised rules cannot. Ordering constraints have to be re-expressed as cross-*event* state (`advanced.md:113`, *"only works for sequential hook events (e.g., PreToolUse then PostToolUse), not parallel hooks"*).
2. **Editing a rule costs a session restart.** `hook-development/SKILL.md:574-582`: *"Hooks are loaded when Claude Code session starts … Editing `hooks/hooks.json` won't affect current session … Must restart Claude Code."* The iteration loop on an externalised rule is therefore an order of magnitude slower than on a prose rule.
3. **Hookify exists because of (2).** `writing-rules/SKILL.md:309` — *"Test immediately - rules are read dynamically on next tool use"*; `:313-315` — *"Edit the `.local.md` file / Adjust pattern or message / Test immediately."* An entire separate plugin exists whose contribution is making the rule layer **data rather than configuration**, so that the edit-test loop is instant. That is a design position on the exact constraint `absence-of-failure.md` identifies as binding for kein — the cost of one iteration on a rule.

**Why Stage 1 could not have produced it:** `docs/purpose.md` puts hooks at zero as a standing non-goal. The entire cost structure of the mechanism route is unexplored in the Stage-1 material, so "dissolve is strictly better when available, because the instruction cannot be forgotten" was stated without a price.

### D5. The removal experiment made reversible — the domain's answer to the calibration insight

Three shipped mechanisms, across two independent sources, all of which turn *off* into a state rather than a deletion:

- `writing-rules/SKILL.md:37-40` — `enabled: true|false` is a **required** frontmatter field: *"`false`: Rule is disabled (won't trigger). **Can toggle without deleting rule.**"* And `:319-321`: *"Temporary: Set `enabled: false` in frontmatter. Permanent: Delete the `.local.md` file."* Two named grades of removal, with the reversible one first.
- `hook-development/SKILL.md:526-570` and `references/patterns.md:265-298` — flag-file and config-file activation. Stated use cases at `SKILL.md:564-568` / `patterns.md:292-296`: *"Enable strict validation only when needed / Temporary debugging hooks / Feature flags for hooks / Performance-intensive checks only when needed."* Plus `advanced.md:438`: *"**Provide escape hatches**: Allow users to bypass hooks when needed."*
- `command-development/references/frontmatter-reference.md:314-317` — `disable-model-invocation: true` removes a command from the model's selection pool without deleting the command.

And the part that inverts who holds the warrant: `hook-development/SKILL.md:570` — *"**Best practice:** Document activation mechanism in plugin README so users know how to enable/disable temporary hooks."* **The off-switch belongs to the population the rule is imposed on, not to its author.** A rule everyone disables is a rule that was wrong, and that datum arrives without anyone scheduling an experiment.

**Why Stage 1 could not have produced it:** `absence-of-failure.md §9` enumerates four alternatives to keep-or-cut, and the conditionalisation case it has (`d46e9ca`, `references/lanes.md` read only when a flag names a vendor) is keyed to a *workload* condition for *cost* reasons. Nowhere in the Stage-1 material is an off-switch shipped as an evaluation affordance, and nowhere is it handed to the reader. The corpus does not connect this to measurement either — it never says "disable it and see" — but the affordance is there, built, three times.

### D6. An instruction can be evicted from context mid-session, and there is an event for putting it back

`hook-development/SKILL.md:270-272`: *"**PreCompact** — Execute before context compaction. Use to add critical information to preserve."*

**Why Stage 1 could not have produced it:** across 1,132 lines, the six analyses debate whether instructions compete for attention, whether compression raises salience, and whether a rule was ever read — and never once consider that a standing instruction may simply **no longer be in the context window** by the time the guarded moment arrives. `attention-cost.md`'s claims A–D all presuppose presence. This supplies a duller mechanism for a phenomenon several analysts attribute to attention or to nobody re-reading the file: a rule "stops working" late in a long session because it is gone. It is checkable, it is orthogonal to everything in §3, and it has a shipped remedy (re-injection at a lifecycle event) that is not "write it more emphatically".

### D7. Enforcement drift has a direction, and the direction gives a free staleness warrant

`ratchet.md D1` lists "the rule contradicts its own enforcement" as one of seven removal warrants, with one exhibit (`7b3a350`, `:advisory` — prose promising semantics its validator contradicted). This corpus has at least five, and crucially they all point the same way.

- `agent-development/scripts/validate-agent.sh:109-112` warns when a description lacks `<example>` blocks. `references/triggering-examples.md:61-67` **bans** that shape: *"Bad (transcript shape — do not use) … The bad version mixes a turn-marker shape into the agent file."* All four shipped example agents have zero `<example>` blocks (`examples/complete-agent-examples.md:12`, `:96`, `:178`, `:248`).
- `hook-development/scripts/validate-hook-schema.sh:139` warns on any `timeout < 5`; `references/advanced.md:210`, `:215` recommend `"timeout": 2`.
- `scripts/hook-linter.sh:50` warns when `set -euo pipefail` is absent; **none** of the skill's own prose snippets in `advanced.md` or `patterns.md` contain it.
- `hook-development/SKILL.md:64-81` requires the plugin wrapper `{"description":…, "hooks": {…}}`; `validate-hook-schema.sh:43,65` iterates top-level keys against an event allowlist, so a correctly-wrapped file yields *"Unknown event type: hooks"*. `SKILL.md:344-381` then shows the unwrapped form, contradicting `SKILL.md:64-81`.
- `validate-hook-schema.sh:124-126` warns on a prompt hook attached to any event but Stop/SubagentStop/UserPromptSubmit/PreToolUse; `SKILL.md:162-173` ships a prompt hook on PostToolUse.

**In every case the prose is the newer statement and the checker is the fossil.** In kein's one exhibit it went the other way. The generalisable rule, which Stage 1 has no basis for: **when prose and its checker disagree, default to the checker being older, because prose is cheaper to edit.** That converts a class of contradiction from "which is wrong?" into a one-question staleness check. (`ratchet.md`'s "the rule contradicts its own enforcement" warrant should carry this default.)

A related mechanical finding worth passing on because it makes the drift invisible: `validate-hook-schema.sh:5` sets `set -euo pipefail` and increments counters with `((error_count++))`, which returns status 1 on the 0→1 transition — **the validator aborts on its first finding, never prints its summary, and reports a warning as a hard failure.** `hook-linter.sh` escapes this only by accident of being called as `if ! check_script`.

### D8. Deprecation exists for instructions. Deletion does not — across 370 KB.

The corpus has a full lifecycle apparatus for instruction text with dependents: `marketplace-considerations.md:452-479` and `documentation-patterns.md:539-549` prescribe deprecate-at-`v2.1.0`, remove-at-`v3.0.0`, ship an old→new example pair, name the migration command, and *"[Handle both old and new flags during deprecation period…]"*. `documentation-patterns.md:714-720`: *"1. Version everything 2. **Deprecate gracefully**: Warn before removing features 3. Migration guides 4. Archive old docs 5. Review regularly."* `marketplace-considerations.md:839-843` even sets a cadence: *"Patches: As needed / Minors: Monthly / Majors: Annually."*

And the measured absence, which both independent readings of the corpus reached separately: **nothing anywhere covers deleting an instruction, pruning a stale rule, detecting a rule that never fires, or deciding whether a rule earns its place.** Deprecation applies only to user-facing *flags and arguments* — never to prompt text. There is no guidance on renaming a command (which changes what users type), no aliasing, no account of what a user sees when an installed instruction disappears on update.

**Why this is a finding and not just an absence:** §1's diagnosis is that removal needs a warrant nobody collects. The closest thing to prior art in the ecosystem has spent thousands of lines on how to *write* instructions, has built an audit skill, three validators, a linter and a rubric — and has produced **zero deletion criteria for instruction text**. The ratchet is not a local pathology and prior art does not solve it. It does, however, supply a different answer to *why*: in this domain an instruction is a **published interface with dependents**, so removal is a compatibility event rather than an epistemic one, and the whole question gets routed into semver instead of into evidence.

### D9. Two genres of standing prompt, with a weighted rubric that scores rules at zero

`claude-md-improver` audits CLAUDE.md against a 100-point rubric (`references/quality-criteria.md`): Commands/Workflows 20, Architecture 20, Non-Obvious Patterns 15, Conciseness 15, Currency 15, Actionability 15. **No criterion scores rules, policies, or behavioural instructions at all.** Currency is verified operationally (`:92-95`): *"Cross-reference with actual codebase: Run documented commands … Check if referenced files exist."* Red flags (`:101-109`) include *"Generic advice not specific to the project"* and *"Duplicate info across multiple CLAUDE.md files"*. `references/update-guidelines.md:64-107` refuses four shapes by name: obvious code info, generic best practices, **one-off fixes** (*"We fixed a bug in commit abc123 …" → "Won't recur; clutters the file"*), and verbose explanations.

The corpus's theory is that CLAUDE.md is a **project fact sheet**, not a rulebook — and every deletion criterion it has is a fact test you can run in the working directory. This converges strongly with `without-measurement.md`'s three legal shapes (pointer / anchored fact / mechanism), reached independently from two different directions, which is worth stating as confirmation.

Three things in it are still delta:

- **"One-off fixes" is refused as a shape, not adjudicated as evidence.** `absence-of-failure.md` spends its length on whether one incident licenses a rule. The corpus does not argue; it bans the form and gives the reason in four words.
- **The audit is gated on human approval with a per-change rationale.** `claude-md-improver/SKILL.md:59` — *"**ALWAYS output the quality report BEFORE making any updates**"*; `:97` — ask for confirmation; `:114-118` — show a diff plus *"Brief explanation of why this helps future sessions"*. That is `docs/purpose.md`'s "prove before adding" in its cheapest payable form: one sentence, attached to the diff, evaluated by someone who is not the author. `ratchet.md D8`'s complaint that an unaffordable gate silently converts into whatever the author will argue for is answered by lowering the gate rather than by buying an instrument.
- **The ratchet is shipped as a keybinding.** `claude-md-improver/SKILL.md:157` — *"**`#` key shortcut**: During a Claude session, press `#` to have Claude auto-incorporate learnings into CLAUDE.md."* One keystroke, mid-session, unreviewed, no counterpart for removal. And the same plugin ships the audit skill that cleans up after it. Stage 1 theorises the addition/removal asymmetry from git history; here it is a first-party product decision — add fast, audit later, as a deliberate pair.

### D10. Named specifics worth having, compactly

Each is a "do X not Y because Z", a named failure, or a threshold with a reason. None appears in Stage 1.

- **Code→prose rule translation, codified.** `hook-development/references/migration.md:320-365` gives three named transforms for when a deterministic check should become a natural-language rule: *String Contains → Natural Language* (`[[ "$command" == *"sudo"* ]]` → `"Check for privilege escalation (sudo, su, etc)"`), *Regex → Intent* (`\.(env|secret|key|token)$` → `"Verify not writing to credential files"`), *Multiple Conditions → Criteria List* (`"Check: 1) … 2) … 3) …. Deny if any fail."`). The motivating false-negative surface is named concretely at `:48-53` (exact `"rm -rf"` misses `rm -fr` and `rm -r -f`) and `:123-127` (prefix rules fail on `/etc` vs `/etc/`, and on symlinks). Stage 1 has prose→mechanism ("dissolve") and nothing for the reverse — which is the direction you take when the deterministic form's *miss rate*, not its cost, is the problem.
- **Conventions for writing a judge prompt.** Conservative default: `patterns.md:120` *"Return 'approve' only if safe"*; `advanced.md:158` *"Return 'approve' only if everything is complete."* Reason-carrying verdict: `migration.md:66` *"Return 'approve' or 'deny' with explanation"*, with the benefit named at `:81`. Bounded input: `migration.md:140` *"Content preview: $TOOL_INPUT.content (first 200 chars)"*.
- **…and the gap in it.** Nothing anywhere specifies how a judge prompt's output is parsed, what happens on timeout, or what happens on malformed output. Worse, the instructed return token is illegal: `SKILL.md:149` defines PreToolUse as `"permissionDecision": "allow|deny|ask"`, while every PreToolUse prompt string tells the model to return `'approve'` (`patterns.md:17`, `:120`, `:164`; `migration.md:66`, `:140`). **When a rule is delegated to an LLM judge, the rule text and the output schema live in different files and drift.** That is the specific new hazard of D4.
- **Regex false-positive worked examples.** `writing-rules/SKILL.md:266-281`: *"Too broad: `pattern: log` — Matches 'log', 'login', 'dialog', 'catalog'"*; *"Too specific: `rm -rf /tmp` — Only matches exact path"*. Plus a YAML escaping trap with a recommendation: quoted patterns need `\\s`, unquoted `\s` works, *"Recommendation: Use unquoted patterns in YAML."*
- **Enforcement class encoded in the rule's own name.** `writing-rules/SKILL.md:31-35`: rule names *"Start with verb: warn, prevent, block, require, check"*. And `:48-51`: `action: warn|block`, defaulting to `warn`. Graded severity as a frontmatter field, separate from the rule text — which is the thing `7b3a350` cut from `execute` because the validator contradicted it. Hookify implements the same two-level severity and makes it bind by putting it in the engine.
- **An instruction naming an ungranted capability fails silently and looks like disobedience.** `command-development/references/interactive-commands.md:903-907` — *"Questions not appearing: Verify AskUserQuestion in allowed-tools."* General form: before concluding a rule was ignored, check that the tool it names is in the agent's tool list. Stage 1's nearest is `lead.md` rule 9, which is the converse (nothing enforces it, so the prose is the only place it exists).
- **"Stop and wait" has no reliable prose form, and the corpus admits it by omission.** The only free-text stop token demonstrated anywhere is `documentation-patterns.md:224` — `[Await user input before continuing...]` — and no file names the failure of it. The corpus's actual answers are structural: delegate the pause to `AskUserQuestion` (`interactive-commands.md:13`) or set `disable-model-invocation: true` for *"Interactive workflows: Commands needing user input"* (`frontmatter-reference.md:301-307`).
- **A positional constraint on prompt layout.** `documentation-patterns.md:694` — *"**Examples before explanations**: Show, then tell"* — and it is enacted, with three worked input/output pairs at `:465-500` placed **upstream of** the actual instruction at `:502`. Stage 1 makes no positional claims about prompt text at all; it reasons entirely in presence/absence.
- **A shipped counterpart clause with a refusal test.** `frontmatter-reference.md:320-322`, on `disable-model-invocation: true`: *"Use sparingly (limits Claude's autonomy). … Consider if command should exist if always manual."* `counterpart.md §5` records that it could find **no** case of a counterpart named at authoring time. This is the phrasing kein wanted; there is no record of it ever firing, so it is a form, not a result.
- **The one threshold in the corpus with a mechanism behind it.** `agent-development/references/triggering-examples.md:97-101`: *"Minimum: 2 … Recommended: 3-4 … **Maximum: 5. More than that bloats the body without adding routing signal.**"* Note it is a cap on the *routing* text specifically, which is the one text whose cost is paid unconditionally.

---

## 2. Divergences

### V1. Grammatical person — three sibling skills, three incompatible mandates

| Artifact | Mandate | Source |
| :--- | :--- | :--- |
| Skill body | **Imperative/infinitive, second person forbidden** | `skill-development/SKILL.md:160`, `:362-413`, `:585`, `:599` |
| Agent system prompt | **Second person required** | `agent-development/SKILL.md:144`, `:181`; `references/system-prompt-design.md:236-245`; enforced by `scripts/validate-agent.sh:190-193` |
| Hookify rule message | **Second person, addressed to the violator** | `writing-rules/SKILL.md:82` — *"You're adding an API key to a .env file"* |
| Command body | Neither — imperative directives, explicitly *not* narration | `command-development/SKILL.md:34-59` |

`skill-development`'s rule, applied to `agent-development`'s output, flags every shipped agent as wrong; `agent-development`'s validator, applied to a skill, warns that it lacks second person. Both live in the same plugin.

**What each side costs.** Second person constitutes an identity and survives being the whole system prompt, but it addresses a reader who may not be the executing agent — an agent file's body is read by the agent, a skill's body is read mid-task by whoever loaded it, and "you" then binds ambiguously. Imperative is unambiguous about the actor but cannot establish a persona, which is what `system-prompt-design.md:16` is buying (*"a compelling expert identity … should inspire confidence and guide the agent's decision-making approach"*).

**The discriminator nobody states, and it is the transferable part:** person tracks **load mechanism**, not taste. Text that *becomes* a system prompt takes second person; text *injected into* an ongoing task takes imperative; text delivered *at the moment of violation* takes second person because it is an interruption addressed to an actor mid-act. kein has all three kinds — `agents/*.md` bodies, skill bodies, and `CLAUDE.md` — and mixes person freely.

### V2. Trigger descriptions — quoted phrases versus prose situations

- **Quoted-phrase enumeration.** `skill-development/SKILL.md:167` — *"Include exact phrases users would say."* Good example at `:174`; the bad example at `:180` is condemned for having *"No trigger phrases"*. `example-skill/SKILL.md:62-68` and `command-development/README.md:82-93` do the same.
- **Prose situations, quoted utterances banned.** `agent-development/references/agent-creation-system-prompt.md:47` — *"**Do NOT use quoted user utterances** at the start of sentences — describe the *situation* the user is in, not the literal phrase they say."* `triggering-examples.md:56` — *"in prose, third person, no quoted utterances."* `:89-95` — *"Don't write three near-duplicate scenarios that differ only in the literal phrase — collapse them into one prose scenario that names the variation"*, with the canonical device at `complete-agent-examples.md:23`: *"(in any phrasing)"*.

**Costs.** Enumerated phrases give the router a literal anchor and match the user's exact wording — and they fail on paraphrase, and they grow without bound because every missed phrasing is repaired by appending another. Prose generalises and is capped at 5, and gives the router a weaker hook.

This is the same decision kein met at the enforcement layer and resolved the same way: `736cc30` reverted a substring check because *"substring matching reads a faithful paraphrase as an omission"*. The corpus met it at the routing layer. **Two independent encounters with paraphrase-versus-literal, opposite artifacts, same resolution** — that is as close to convergent evidence as anything in this stage.

Note the migration is visible in the corpus's own strata: the `<example>` transcript style was removed from the agent guidance and from all four shipped examples, but `validate-agent.sh:109` still demands it (see D7).

### V3. Where the rule lives — engine-reloadable data versus session-pinned configuration

`hook-development/SKILL.md:574-582` (rules load at session start; editing requires a restart) versus `writing-rules/SKILL.md:309`/`:313-315` (rules are read dynamically on the next tool use; *"Test immediately"*).

**Costs.** Hooks get arbitrary logic, deterministic execution, and access to the full event payload; each edit costs a session restart, so the rule-iteration loop is minutes. Hookify gets an instant loop and a one-word disable, and pays by restricting every rule to a regex over one field of one event, with `all conditions must match` as the only combinator (`writing-rules/SKILL.md:98`).

**Why it matters here:** this is the same tradeoff kein hit from the other end. `absence-of-failure.md` records `ocs eval` paused because an arm cost 35–40 minutes. Hookify's answer to the same constraint is not a faster instrument but a **cheaper unit of change** — a rule you can edit and re-test inside one session. Both prior-art positions exist; only one of them is the position kein has taken.

### V4. Prompt-based versus deterministic enforcement, argued explicitly

`hook-development/SKILL.md:22-41` recommends prompt hooks by default and closes at `:712-713`: *"Focus on prompt-based hooks for most use cases. Reserve command hooks for performance-critical or deterministic checks."* `references/migration.md` argues the whole case, with named misses of the deterministic form (`:48-53`, `:123-127`) and a boundary at `:173`, `:189`, `:191-203`: use command hooks when validation is *"purely mathematical or deterministic"*, when integrating an external yes/no tool, or when the check must run in **< 50 ms**.

Against this, `writing-rules` never mentions LLM judgement at all — its entire model is regex. And `hook-development/SKILL.md:521` still recommends *"command hooks for quick deterministic checks."*

**Costs, both stated:** deterministic checks are fast and auditable and miss variants; prompt checks catch intent, cost 15–30 s (`migration.md:241`), and — per D10 — have no specified failure behaviour. This is precisely the "does a rule belong in prose or in a mechanism" question kein answers as "mechanism whenever possible", and the corpus answers as "prose judge whenever the boundary is fuzzy". Two real positions.

### V5. Budgets that contradict each other inside one skill

`agent-development/SKILL.md:187` — *"Keep under 10,000 characters"*; `references/system-prompt-design.md:369` — *"Avoid > 10,000 words."* A ~6× discrepancy between a SKILL.md and its own reference. Worse, `system-prompt-design.md:358-367` recommends *"Comprehensive Agent ~2,000-5,000 words"*, which cannot fit under the same skill's 10,000-character cap; and `SKILL.md:263-265` says *"Length: 20-10,000 characters. Best: 500-3,000 characters"*, which excludes the "Standard Agent ~1,000-2,000 words" the reference recommends. `validate-agent.sh:184` enforces the character reading.

Also across artifacts: command `description` is capped at *"~60 characters"* with a reason (`/help` display, `frontmatter-reference.md:29`, `:45`), while every shipped agent `description` runs 330–390 characters (`complete-agent-examples.md:12` etc.) because it is a routing surface, not a display surface. Neither file says the two are different classes.

---

## 3. Direct contradictions of Stage-1 conclusions

**1. `ratchet.md` D3 — *"a stated **kind** constraint cuts; a stated **quantity** constraint becomes another line to argue with"* (from `9d79fdd`, the six-skill ceiling).**

The corpus runs almost entirely on quantity constraints and treats them as the primary discipline: 1,500–2,000 words / <3,000 / <5k for a skill body (`skill-development/SKILL.md:190`, `:329`, `:433`); ~60 characters for a command description; 2–4 options and max-12-character headers (`interactive-commands.md:43`, `:65`); 2–4 trigger scenarios with a hard max of 5; 3–50-character names; 20–10,000-character system prompts; *"Use when plugin has 5+ commands"* for namespacing (`plugin-features-reference.md:52`).

**Qualified.** These are not deletion budgets — they are **routing** budgets on a tier. `skill-development/SKILL.md:190` reads *"Keep SKILL.md lean: Target 1,500-2,000 words for the body. **Move** detailed content to references/"*. The budget says where text goes, never whether it lives. That is a mechanism Stage 1 does not have: a size cap that is payable because the overflow has somewhere to go, and it explains why a quantity constraint that failed in `purpose.md` could work here.

**And the corpus simultaneously supplies the best evidence that Stage 1 is right.** The numbers are internally inconsistent (V5), and the corpus's flagship file busts its own cap: `skill-development/SKILL.md` is 3,195 words against its stated <3,000. A number in a prompt is a number that goes stale — which is `without-measurement.md`'s own thesis, confirmed here on the corpus that most relies on numbers.

**2. `attention-cost.md` D8 / `ratchet.md` — *"dissolve into structure is strictly better than all of them when available, because the instruction stops needing to be followed."***

Contradicted with prices. Dissolution here costs: parallel-only execution, so no dissolved rule can depend on another (D4.1); a session restart per edit (D4.2); and a 5-of-5 observed rate of the enforcer going stale relative to the prose it enforces (D7). "Cannot be forgotten" is bought by "cannot be cheaply corrected". The corpus's own validators are the exhibit.

**3. `where-justification-lives.md` — the three homes for a rule's argument (inline mechanism / external provenance / dated quarantined fact).**

Not contradicted, but the enumeration is incomplete. The corpus's dominant home is a fourth: **the justification attaches to a demonstration pair** (`**Why bad:** Vague, no specific trigger phrases, not third person`). Its distinctive property is that the check is a pattern-match against an exhibit rather than a piece of reasoning — cheap for a reader in passing, and self-violating by construction (D1).

**4. `without-measurement.md` §4 — *"the only recurring check on a standing prompt is somebody reading it for an unrelated reason."***

True of a private prompt; false of a distributed one. `marketplace-considerations.md:7` names the real instrument: **unknown users on environments you did not test.** Everything the corpus adds over kein's practice — semver, deprecation windows, platform fallback chains (`:51-63`, `pbcopy` → `xclip` → `clip.exe`), beta channels (`:772-812`), first-run onboarding (`:179-202`), *"Did you mean: help?"* typo handling (`:240-247`) — is the cost of that instrument. This is worth stating plainly because it cuts the other way for us: **the corpus's evaluation channel is an audience we do not have, so most of its apparatus does not transfer, and the part that does is the part about writing (D1, D2, D3, D6, D10).**

**5. `counterpart.md` §5 — *"No case where naming the counterpart at authoring time caused a rule to be rejected."***

Still unrefuted, but the corpus supplies a shipped clause of the right shape with a refusal test attached (`frontmatter-reference.md:320-322`, D10). No record of it firing. The finding survives; the phrasing gap closes.

---

## 4. Where this corpus speaks with one voice

Reported because a uniform corpus is one input to deciding whether to seek genuine disagreement outside. For each, I say how many of the three genuinely separate sources it spans (`plugin-dev` counts as **one**).

| Position | Sources | Dissent |
| :--- | :--- | :--- |
| Progressive disclosure: metadata always in context, body on trigger, references on demand | 1 (`plugin-dev`, forked from `skill-creator`) | none |
| A `description` must enumerate concrete trigger conditions; vague descriptions are the top-listed defect | 3/3 | only on *form* (V2), never on the principle |
| ❌ bad / ✅ good paired contrast as the teaching unit | 3/3 | none |
| A trailing validation checklist ends the document | 3/3 | none |
| Least privilege on `tools` / `allowed-tools` | 2/3 | none |
| "Be specific, not vague" as a stated principle | 3/3 | none — and it is contentless |
| Iterate after real use; fix what struggled | 3/3 | none |
| **Nothing on deleting instruction text, ablation, A/B, differential evaluation, or any evidence that an instruction did anything** | 3/3 silent | zero coverage, hence zero dissent |

The pattern: **one voice on structure, silence on evidence.** The corpus has thoroughly settled what an instruction file looks like and has not once asked whether any given line in it works. What is missing is not a second opinion on layout — it is anyone who has measured. If the next stage goes outside, that is the axis to go looking on, and the useful search is for a corpus with an eval loop attached, not for another style guide.

---

## 5. Read, found nothing in — do not repeat

- `example-plugin/skills/example-skill/SKILL.md` and `example-plugin/skills/example-command/SKILL.md` (2.7 KB and 1.2 KB): pure format demos. The only two non-obvious lines in either are `example-skill:85` (*"Avoid overlap with other skills' trigger conditions"*, folded into D3) and `example-command:10` (the `skills/<name>/SKILL.md` and `commands/*.md` layouts are loaded identically, which only matters for locating files).
- `claude-md-improver/references/templates.md` (3.7 KB): section skeletons with `<placeholder>` fillers. No rationale, no thresholds, nothing about rules. The four "Update Principles" at `:246-254` restate the rubric.
- `command-development/references/testing-strategies.md` (14.8 KB): despite the title, it is **entirely about testing the file, not the instruction**. YAML marker counts, `.md` extension, argument substitution, `!`backtick`` execution, `@` file references, a CI job that greps for `TODO`. The one relevant line is `:526` (*"Acceptable threshold: < 3 seconds"*, about latency). Nothing about whether a prompt produced the intended behaviour; its "test matrix" (`:166-174`) has "Manual test required" in every row. If you are looking for how this domain evaluates a prompt, it is not here.
- `agent-development/references/system-prompt-design.md` §"Patterns 1-4" (`:40-230`): four fill-in-the-blank system-prompt skeletons (Analysis / Generation / Validation / Orchestration) that differ only in section labels. The only extractable items are the length guidelines (V5) and `:157` (*"No false positives"* listed as a quality standard for validation agents, with no method).
- `command-development/references/advanced-workflows.md` and `examples/plugin-commands.md`, `examples/simple-commands.md`: read in full. Everything usable is in D2 and the contradiction list; the remainder is shell pseudo-code inside command bodies that the harness does not execute, plus invented syntax presented as real (`plugin-features-reference.md:453-456`, `$IF($1 in [dev, staging, prod], …)`). Treat these three files as unreliable on mechanics.
- `hook-development/examples/*.sh` and `scripts/*`: read in full. The scripts matter only as the D7 exhibits; the example hooks contribute two contradictions (`validate-write.sh:26` trips the shipped linter's hardcoded-path check; `validate-bash.sh:38` pairs `"permissionDecision": "ask"` with exit 2, which `SKILL.md:297` defines as blocking).
- `skill-development/references/skill-creator-original.md`: ~85% verbatim duplicate of `skill-development/SKILL.md`'s first half. Its only unique content is the packaging path (`init_skill.py`, `package_skill.py`, ZIP distribution) — irrelevant to plugin skills, and `skill-development/SKILL.md:146` and `:278-280` say so.
- **Not read, deliberately:** the other seventeen skills under `claude-plugins-official/plugins/*/skills/` (`claude-security`, `frontend-design`, `mcp-server-dev`, `receipts`, `project-artifact`, `math-olympiad`, `cwc-makers`, `playground`, `session-report`, `claude-automation-recommender`, and `plugin-dev`'s `mcp-integration` / `plugin-settings` / `plugin-structure`). They are instruction files, not files *about* instructions, so they are a corpus of specimens rather than of doctrine. `plugin-dev/skills/plugin-structure` and `plugin-settings` are the two most likely to hold anything, and `skill-development/SKILL.md:311-315` describes `plugin-settings` as the one with real-world implementation references — that is the first place to look if this corpus is revisited.
