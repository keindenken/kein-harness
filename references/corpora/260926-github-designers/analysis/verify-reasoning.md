# Verify: reasoning in synthesis.md

A skeptic's pass over `analysis/synthesis.md`. The job was to refute it: find where it moves from "authors do X" to "X works", where lineage or overlapping theme unions inflate a count, where the theme and close-read files contain counter-evidence it leaves out, and where a recommendation goes beyond the data.

Method. I recomputed every count I challenge from `records.json` (design roles only, owner = repo prefix) and from `analysis/themes/*.assign.json`, using the union groups listed in the synthesis's Appendix B. I reproduced these as stated: ground 173/154, render 58/52, unverified 27/26, anti-generic 89/82, self-check 40/37, separate review 22/19, variants 35/35, ask-or-gate 81/74, states 121/110, the output-form coverage table, the mode splits (168/169/62), the 15 split owners and the tool table. Two unions reproduce only after adding themes Appendix B does not name (issues 6 and 7). I read all ten theme files and the verdict, conflict and defect sections of all 31 close reads, and I checked the quotes I rely on against the original files. Where I was unsure I say so, and I flag it anyway.

Severity: **high** means the finding changes a recommendation. **Medium** means it changes a figure, a quote or a confidence level. **Low** means wording, or an omission that does not change a conclusion.

## Summary

| # | Issue | Severity |
|---|---|---|
| 1 | "Sketch, pick, proceed" contradicts the scope theme's "present the set and stop", and the designer picking a variant is a quality verdict | high |
| 2 | s0072's KEEP / GENERIC / DUPLICATE sorts audit findings, not design output, and jezweb has no split system | high |
| 3 | The scorecard reads clause (6), "no self-judgement", as "Supported" although practice runs the other way | high |
| 4 | Split owners' rendering sits almost entirely in their review-only records | medium (possibly high) |
| 5 | "Ask 81 vs proceed 17" is not two camps: 7 records sit in both, including the form the report recommends | medium |
| 6 | "Commit to one direction: 47 from 46" is inflated by a merged theme and by the frontend-design family | medium |
| 7 | The scorecard reads clause (2) as "Supported" although the process theme calls the direction rule contested | medium |
| 8 | The no-render behaviour is called the corpus's "consensus shape" with high confidence | medium |
| 9 | "At least 44 of 82 say nothing about a missing tool" gets the inequality backwards | medium |
| 10 | "High that it is needed" (clause 3) is a claim about need, not about what authors write | medium |
| 11 | "The largest cross-cutting construct in the corpus" is not the largest, and the union counts harness-file reads | medium |
| 12 | "Agents mostly carry their taste inline" rests on 34 of 82, which is not most | medium |
| 13 | The top-20-copied rendering comparison is confounded by kind, and stars point the other way | medium |
| 14 | "At least 14 records from 12 owners" with a mode table counts create/audit toggles and single-form fidelity switches | medium |
| 15 | "The majority habit is one role that makes and reviews" is a minority (41%) | medium |
| 16 | "Static interfaces are strictly forbidden." is attributed to s0006, but it is in s0018 | medium |
| 17 | The 16px vs 13–14px body-text "contradiction" is not one: s0069 prescribes both | medium |
| 18 | The claim that no finding records MCP under a `tools:` allowlist is wrong, and c00133 and c00263 are condemned on that belief | medium |
| 19 | Critique formats "concentrate in review roles" is near-circular, and 9 of 23 sit in maker+review roles | medium |
| 20 | "Written for greenfield" treats a missing claim as evidence of absence | medium |
| 21 | "Confidence: high for 1–3" includes an item resting on two owners | medium |
| 22 | Exemplars were scrutinised unevenly: the favoured ones skipped the adversarial close-read protocol | medium |
| 23 | c00681, the "closest existing model", cannot render its own maker output | medium |
| 24 | Omission: the output theme's "a prototype alone is not enough; the handoff must be spec-grade" | medium |
| 25 | The agent/skill gaps in Q1 are partly an output-type effect | low |
| 26 | s0078 is called "the one piece of evidence" of tuning against failure, contradicting the report's own s0112 row | low |
| 27 | The c00042 "pair avoid with target" claim is propped up with this repo's unrelated priming view | low |
| 28 | "Carefully built" is the synthesiser's judgement, then used as evidence | low |
| 29 | The opt-in-rendering counter-position is dismissed as review skills, but s0013 is a maker | low |
| 30 | Reviewer bases are cited without their close-read defects (c00214, c00286, s0110) | low |
| 31 | Omission: s0094's distinctness check is a self-judgement by the maker | low |
| 32 | Omissions: accessibility intent in redesign, a11y conformance with no a11y role, and user/brand context that is not in code | low |

32 issues, 3 high.

---

## 1. "Sketch, pick, proceed" contradicts the scope theme and clause (6) — high

**Report text.** Q4 item 5: "**Sketch, pick, proceed.** "For ambiguous briefs, propose 3-4 distinct visual directions (… ), select the best-fit default for the brief and context, and proceed." (c00042). This keeps "commit to one" while handing the lead the alternatives at almost no cost, and it works in an unattended run." Appendix A (2): "Several directions sketched, one picked, the others reported (c00042)."

**What is wrong.**
- The recommendation rests on one lineage. c00042 (Yeachan-Heo/oh-my-claudecode), c00158 (LimiNode, a fork) and c00116 (a fork named oh-my-claudecode) share the text. The direction theme says "the idea itself has three voices at most", and the process theme groups c00042 and c00158 as one wording.
- The scope theme reaches the opposite recommendation from a wider base. Its theme 11, "The human owns the choice" (12 records, 12 owners, 58% skills), leads it to write: "When variants are asked for, s0108's "present the set and stop — the choice belongs to the user" is the contract; the designer does not pick the winner." The s0078 close read agrees: "The variant-comparison ground rule belongs to whoever picks among the designer's variants, which may be the lead or the reviewer". The synthesis never mentions this position. Instead it counts human-owns-the-decision inside its "ask or gate" union and rejects the whole union as "mandatory user gates".
- Picking the "best-fit" direction is a quality verdict by the author, which the synthesis's own clause (6) reading forbids ("Facts only, never a quality verdict").
- Counter-voices are left out: s0109 "Prefer one defensible direction over a menu of weak variations unless the user asks to explore", c00360 "Never present only one option — always offer alternatives", s0120 (listing a single option as an anti-pattern), and s0094 and s0112 producing variants unasked. The process theme's verdict is "The direction rule is contested."

**Evidence.**
- The process union for proceed-on-stated-assumptions (12 records) includes c00042, c00158 and c00072 (frontend-design family).
- The scope theme lines 99–104 and 177.
- The s0078 verdict in `deep/s0078.md`.

**Consequence.** For a designer that returns to a lead, "present the set, recommend without choosing, stop" fits the unattended constraint as well as "pick and proceed" does. It also avoids a self-verdict. The recommendation should either say it takes a side in a contested question, or switch.

## 2. s0072's KEEP / GENERIC / DUPLICATE is an audit-finding filter — high

**Report text.**
- Q4 item 10: "**An anti-generic check run in a separate context.** "dispatch a fresh sub-agent with the draft list … KEEP / GENERIC / DUPLICATE" (s0072). This is how the proposal's "review is separate" can still catch generic output."
- Q1: "The corpus's strongest statements that an author cannot review its own work come from split systems: … (s0072)".

**What is wrong.** The "draft list" is a list of UX-audit findings, and "GENERIC" means a finding "would apply to any web app". It does not mean design output that looks generic. The source (`corpus-skills/jezweb_claude-skills__plugins_dev-tools_skills_ux-audit_SKILL.md` lines 350–354) reads: "Read these audit findings. For each, mark KEEP / GENERIC / DUPLICATE. KEEP = specific to this app, this persona, this surface. GENERIC = would apply to any web app." The process theme made the same misreading ("The anti-generic check done by a separate context"), and the synthesis inherited it.

s0072 is also not from a split system. jezweb's only other record, s0073, is not a design role, and jezweb is absent from the synthesis's own list of 15 split owners. The same file argues against fresh-context review, three times by the close read's count: "Drive the audit from the main session, not a sub-agent … A fresh sub-agent starts cold and misses second-order findings" and "Don't hand screenshots to a fresh agent for opinions" (lines 435–436).

**Consequence.** Item 10 has no corpus example left of a separate-context anti-generic check on design output. It becomes the synthesiser's proposal. The Q1 list of split-system statements loses one of its three members.

## 3. The scorecard reads clause (6) as "Supported" — high

**Report text.** Scorecard (6): "Return-report quotes: 14 records from 11 owners. Self-check: 40 from 37. Separate or read-only review: 22 from 19. Only 1 record says both. | Supported, if fact-checking is separated from quality verdicts. … | Medium-high".

**What is wrong.** The data show the opposite of the reading.
- Self-check (40/37) outnumbers any statement that a maker should not judge itself. The "separate or read-only review" union is almost entirely reviewers declaring themselves read-only (scope read-only-review, 19 records / 17 owners). The theme that actually says an author must not approve its own work, no-self-approval, has 4 records from 3 owners.
- The `self_review_checklist` flag is set on 58% of roles and on 74% of skills.
- The process theme says outright: "The "no self-judgment" half is contradicted by practice." The evidence theme heads its paragraph "**Contradicted on "does not judge its own quality"**".
- Every recommended craft base self-critiques: s0037, s0112, s0061, s0013, c00337, and the skeleton c00681 ("Critique against the brief … Fix issues").

The fact-versus-verdict reconciliation is a reasonable design, but it is the synthesiser's construction, not what the corpus supports. A return contract (14/11, 3.5% of owners) is also thin by the report's own confidence definition.

**Consequence.** The reading should be "a harness choice against majority practice; the corpus supplies a reconciliation, not support", at medium or low confidence. That changes what the owner is told about the distinctive part of clause (6).

## 4. Split owners' rendering sits in their review-only records — medium (possibly high)

**Report text.** Q1: "Owners who split making from review are far more likely to render and look. 14 of the 15 split owners have at least one rendering record. Among the 257 single-record owners, 42 (16%) do".

**What is wrong.** The numbers reproduce, but the rendering belongs to the reviewer, not the maker.
- In 13 of the 14 split owners, a review-only record carries `renders_and_looks`. Only 9 of the 15 split owners have a maker record that renders.
- For 6 owners, the maker never renders and only the reviewer does: wshobson (c00203), rennf93, flick-git-anhnv, nextlevelbuilder, Devin-AXIS and ibelick (ibelick has none at all).
- Across the corpus, review-only records render at 44% (27/62), maker+review at 23% (39/168) and make-only at 9% (16/169).
- Split owners also have at least two records, which gives them more chances to have "at least one". Their records are 60% skills, and single-record skill owners render at 31% (14/45) against 13% for single-record agent owners (28/212).

**Consequence.** The corpus pattern in split systems is "the reviewer renders". That is counter-evidence the report does not surface for clause (3), which puts rendering on the maker. It does not refute clause (3), but it means the split systems are not a model for a rendering maker. I rate it medium because the report already labels the claim as correlation. It is high if the owner reads Q1 as support for the maker rendering.

## 5. "Ask 81 vs proceed 17" is not two camps — medium

**Report text.** Scorecard (2): "Ask or gate first: 81 from 74, against proceed on stated assumptions: 17 from 16." Q4 reject item 8: "Ask-or-gate quotes cover 81 records from 74 owners, against 17 from 16 that say to proceed on stated assumptions. The transferable form is c00194's …"

**What is wrong.**
- Seven records are in both unions: c00072, c00194, c00198, c00360, c00541, c00681 and s0092. The recommended form, c00194 ("Ask targeted questions only when … otherwise proceed with explicit assumptions"), is counted on the "ask" side. So are c00681 ("Otherwise state a reversible assumption and proceed") and c00541 ("Include a recommended default").
- The 81 also include human-owns-the-decision (present options and stop) and output approval-gate. Those are end-of-run hand-backs, not questions asked before designing.
- The 17/16 only reproduces after adding scope surface-assumptions-and-open-decisions to process proceed-on-stated-assumptions (12/12). Appendix B does not list that addition.

**Consequence.** Conditional asking ("ask only if it changes the outcome, else assume") is the shared middle ground, not a 1-in-5 minority. The recommendation survives. The "81 against 17" framing overstates the opposition and hides the fact that the recommended form comes from the "ask" camp.

## 6. "Commit to one direction: 47 from 46" is inflated — medium

**Report text.** Scorecard (2): "Commit to one direction: 47 from 46. Offer variants: 35 from 35. Only 5 records say both."

**What is wrong.**
- The count reproduces only when direction name-direction-concretely is merged in. Commit-one-direction plus process commit-direction-before-building gives 38 records / 37 owners, and 4 records say both.
- Naming a direction concretely is not committing to one. c00042 is in the naming theme and proposes 3–4 directions.
- The frontend-design family (15 records under 15 owners) is not deflated in the scorecard, although Q4 deflates it. Without it, the commit-only union is 24 records / 23 owners, and with the naming theme it is 32/31.
- Variants (35/35) are about 17 lineages by the process theme's count, also not deflated.

## 7. The scorecard reads clause (2) as "Supported" — medium

**Report text.** Scorecard (2): "Supported. Turn "ask" into "state the assumption". … | Medium-high".

**What is wrong.**
- The process theme's reading is "The direction rule is contested. Options (21 owners, about 17 lineages) is more common than commit-first (9 owners)".
- Turning "ask" into "state the assumption" goes against the numerical majority, even after issue 5's correction. It is justified by the harness (unattended runs), not by the corpus.
- Naming the user rests on 32 owners, about 10% of the corpus, and c00017 and c00611 are one text.

**Consequence.** It should read "partly supported; the direction default is contested; the assumption rule is a harness choice".

## 8. The no-render behaviour is called a "consensus shape" — medium

**Report text.** Q3: "The corpus already has the answer. The proposal lacks it." and "Confidence: **high** that this is the corpus's consensus shape."

**What is wrong.**
- The report's own numbers contradict it. "Admit what was not verified" covers 27 records from 26 owners, 8% of owners. Only 13 of the 58 render-and-look records have it, and "roughly half of the roles that ask for rendering say nothing about the missing tool".
- The five-step procedure is assembled from single sources: s0072's probe, c00133's dev-server probe (c00133 is the report's own clearest negative exemplar), s0109's widths, s0076's "read the screenshot", and c00581's settle timing.
- The labels exist, and they recur across about 8 owners. "Consensus" is wrong, and "high" violates the report's own definition ("many independent owners, consistent across dimensions").

**Consequence.** Confidence should be medium. The shape is a well-sourced minority practice.

## 9. "At least 44 of 82" gets the inequality backwards — medium

**Report text.** Q3: "A broad regex over the 82 flagged files finds wording about the no-render case in 33. Reading the misses adds at least five more … So roughly half of the roles that ask for rendering say nothing about the missing tool (at least 44 of 82)." The scorecard repeats "At least 44 of those 82 say nothing about a missing tool."

**What is wrong.** If at least 38 (33 + at least 5) have such wording, then at most 44 lack it. The report inverts the inequality. My own broader regex (not-verified / unverified / DEGRADED / UNAVAILABLE / "if … unavailable|missing|fails" / "no browser|screenshot|vision" / "say so" / "manual validation") matches 50 of the 82 files. That would leave at most 32 silent. The regex has not been validated for false positives, so the true figure lies between the two. Either way, "at least 44" is unsupported.

## 10. "High that it is needed" is a claim about need — medium

**Report text.** Scorecard (3): "Supported, and ahead of the corpus. … | High that it is needed. Unknown whether agents comply."

**What is wrong.** "Needed" is an outcome claim. By the report's own rule, "Nothing in this corpus measures outcomes." The evidence is:
- 52 of 314 owners write render-and-look;
- the layout theme calls it "Thin support";
- the process theme calls it "Weakly represented";
- negative exemplars show prompts that *say* screenshot but judge from code.

That last point shows prompts fail at rendering. It does not show that rendering improves designs. This is the report sliding from "authors do X" to "X is needed". The confidence should attach to "authors who care about visual claims ask for it", or be marked **Interpretation**.

## 11. "The largest cross-cutting construct in the corpus" — medium

**Report text.** Scorecard (1): "The largest cross-cutting construct in the corpus: 173 records from 154 owners have a verified quote for it." Q3: "**The largest cross-cutting construct.**"

**What is wrong.**
- Accessibility is larger. The union of `accessibility.assign.json` themes is 207 records / 185 owners, or 187/169 excluding the WCAG boilerplate theme. Accessibility theme 1 (AA contrast) alone is 99 records / 96 owners, which the report cites elsewhere.
- A union's size also grows with the number of themes merged. Ground merges 12 themes across 6 dimensions, while render merges 4, so "largest" partly measures how the union was built.
- The ground union includes process read-project-context-files-first, which contains the context-manager template family (c00006, c00074, c00340: "query a sibling agent that does not exist outside that framework"). It also includes evidence read-named-design-docs. The process theme warns: "most "read first" instructions point at a harness file, a skill or a context agent, not at the product's code." Without those two themes the union is 154 records / 135 owners.

**Consequence.** The claim stays strong, but "largest" is false. The count should be stated with its composition.

## 12. "Agents mostly carry their taste inline" — medium

**Report text.** Q1: "**Agents mostly carry taste inline.** 82 agents from 75 owners carry the anti-generic flag, and 34 of those records (31 owners) reference no external file at all, so their taste sits in the role text."

**What is wrong.** 34 of 82 is 41%, a minority. The other 48 reference an external file. A reference does not prove the taste lives there, but the figure given cannot carry "mostly". The close-read tally that follows (11 of 18 agents) comes from a selected set (issue 22), not a sample.

## 13. The top-20-copied comparison is confounded — medium

**Report text.** Q5: "The 20 most-copied records render and look in 2 cases (10%), against 80 of the other 385 (21%). Their mean specificity rating is 3.45 against 3.98."

**What is wrong.** All 20 most-copied records are agents, and agents render at 14% against 39% for skills. Against the other agents:
- rendering is 2/20 (10%) against 42/288 (14.6%), a difference of about one record at n=20;
- specificity is 3.45 against 3.83.

The top 20 by *stars* render 8 of 20 (40%), about twice the base rate. The data therefore do not show that popularity signals lower quality. They show nothing either way, and stars lean positive. "Stars and copies are not quality" is a fair caution, but it is not a finding from this comparison.

## 14. The mode-table count mixes different things — medium

**Report text.** Scorecard: "The multi-form roles with the clearest contracts (at least 14 records from 12 owners) declare an explicit mode table". Q2: "the corpus's working form of it is a table". Correction 1: "The caller-set form exists in about a dozen owners, always as a mode table."

**What is wrong.**
- Several of the 14 are not output-form tables. c00403, c00113, c00430 and s0075 are create/audit toggles, and s0093 and s0024 are fidelity switches inside a single form.
- Records with a table that chooses among several *make* forms are about 6–8 (c00681, c00322, c00135/s0085, s0112, c00576, c00701, possibly c00320), from roughly 6 owners.
- Of the 6 records that actually cover 4 or more of the proposal's forms (c00021, c00337, c00701, s0013, s0049, s0052), only c00701 uses a table. The report itself notes the others use routers, per-form sections or playbooks.
- The list was "hand-identified from a search for mode headings", and "clearest contracts" is the synthesiser's judgement.

**Consequence.** The mode-table recommendation is plausible, but its corpus base is about half what is stated, and it is not the form the widest roles use.

## 15. "The majority habit is one role that makes and reviews" — medium

**Report text.** Q1 bearing: "The majority habit is one role that makes and reviews, which is what the proposal rejects."

**What is wrong.** Maker+review records are 168 of 405 (41%). Make-only (169) plus review-only (62) records are 231. Among single-record owners, 114 of 257 (44%) make and review. The report's own previous bullet says "Combining is as common as specialising." It is a plurality among single-role owners at most, not a majority. The report also notes that "review" inside maker roles is usually a self-check, so the flag overstates a make-and-critique habit.

## 16. "Static interfaces are strictly forbidden." is attributed to s0006 — medium

**Report text.** Q4 reject item 6: "taste-skill's perpetual looping animation, "Static interfaces are strictly forbidden." (s0006)".

**What is wrong.** The sentence is in `corpus-skills/Leonxlnx_taste-skill__skills_gpt-tasteskill_SKILL.md` line 47, which is record s0018. It is not in s0006 (`taste-skill-v1`). The interaction theme pairs them correctly ("(s0006, s0018)"). s0006's perpetual micro-interactions are partly gated: "When `MOTION_INTENSITY > 5`, embed continuous, infinite micro-animations" (line 70). The report drops the gate. The Bento section's "Every card must have an "Active State" that loops infinitely" (line 207) is scoped to SaaS dashboards and feature sections.

## 17. The body-text "contradiction" is not one — medium

**Report text.** Q1: "Body text is 16px in s0069 and 13–14px for SaaS in s0045 and c00603." Q4 table: "Body text | 16px floor (s0069) against 13–14px for dense SaaS (s0045, c00603)".

**What is wrong.** s0069 says both things. Its line 112 reads "Start long-form body text at `16px` … Move off it only for a reason you can name: … or the product is a dense professional tool." Line 114 reads "UI text can go smaller. `14px` is a useful starting point for inputs and menus, `13px` for captions". The visual-craft theme already reconciles them: "The 16px floor holds for reading content but not for dense product UI." One of the five "taste sources contradict each other" examples, and one row of the "concrete values disagree" table, is therefore not a disagreement.

## 18. A finding does bear on MCP under a `tools:` allowlist — medium

**Report text.**
- Q3: "A runtime belief to check before relying on it: that a Claude Code subagent's `tools:` allowlist excludes MCP tools not named in it. … No finding in this repo records it".
- The same section, stated as fact: "c00133 and c00263 both require MCP browser steps their own `tools:` allowlist leaves out."
- Q5 negative exemplars: "Its MCP branch cannot run under its own allowlist" (c00133) and "a render-first rule that its own `tools:` list cannot carry out" (c00263).

**What is wrong.** The finding the report cites elsewhere, `260808-subagent-capabilities-without-agent-teams.md` (it lives under `~/Documents/wiki/findings/`, not in this repo), quotes the docs: "a background subagent keeps every MCP tool". Its open questions say: "MCP tools are said to be kept regardless, but that was not verified for these roles." So a recorded, unverified claim leans *against* the close reads' assumption.

**Consequence.** The two exemplars' "cannot run" defects, and the "Contradictions inside single files" bullet, should be downgraded to "may not run, unverified". It remains a `kein-findings` candidate, but not a blank one.

## 19. "Critique formats concentrate in review roles" is near-circular — medium

**Report text.** Q2: "Critique formats concentrate in review roles: structured findings are 22 of 23 in written-critique (output theme T2)." Also "The best critique machinery lives in dedicated reviewers" and "One role covering both would carry two unrelated format sets".

**What is wrong.**
- A critique format appearing in roles tagged `written-critique` is close to tautological.
- The informative split is review-only against maker+review. Maker+review records hold 9 of 23 structured-findings records, 6 of 16 score-or-verdict records and 3 of 10 cite-location records. So a sizeable share of the corpus's critique formats already sit in roles that also make.
- "Best critique machinery" is a selection by the synthesiser. All five examples it names (s0110, s0078, c00286, c00102, c00214) are review-only records.

**Consequence.** The recommendation to narrow or drop "written critique" can stand as a design choice, but the corpus does not show that combined roles cannot carry both format sets.

## 20. "Written for greenfield" treats a missing claim as absence — medium

**Report text.** Q1: "Its anti-generic rules were written for greenfield work. Of the 89 records (82 owners) with verified anti-generic quotes, only 36 (35 owners) also have a verified quote about following the existing product."

**What is wrong.** The report warns that claims "are stricter and undercount a behaviour". Here it uses a missing claim as evidence that the behaviour is absent. By flags, 84 of the 131 anti-generic records (64%) also carry `follows_design_system`, and 84 carry `inspects_existing_ui`. The greenfield concern is real (the themes show the lift in production code). But "only 36 of 89" understates the overlap, and co-occurrence does not show scoping in either direction.

## 21. "Confidence: high for 1–3" — medium

**Report text.** Q3, on what grounding adds: "Confidence: **high** for 1–3, **medium** for 4–6 (few voices)."

**What is wrong.** Item 2, what counts as having read the product, rests on two owners: s0024 (Orkas-AI) and s0112 (tw93). Item 1, precedence, draws on the scope theme's brief-and-project-rules-precedence (8 records, 7 voices, all skills) plus four scattered quotes. Both are as thin as items 4–6, which the report rates medium for "few voices". By the report's own definition, items 1 and 2 should be medium.

## 22. Exemplars were scrutinised unevenly — medium

**Report text.** Q5: c00681 "(… I read it in full; it was not in the close-read set)" and c00581 "(513 stars; I read it in full)". Also "The judgements below rest on what each file does and on defects the close reads actually found."

**What is wrong.**
- The 31 close reads each have a mandatory "What looks wrong or untested" section. The two exemplars the synthesiser read itself had no such pass, and they are the most heavily used (c00681 is cited 15 times).
- `deep-read-selection.json` records no selection criterion. The set includes the most-copied records (c00001, c00002, c00003 and c00009, with 77, 75, 62 and 31 copies), so popular files received adversarial reads and then supplied the negative exemplars.
- The close-read verdicts are batch-relative ("the best of the five": c00013, s0109; "best base in this batch": s0093). Two close reads each call their record the best role base (s0093, s0109), and the synthesis picks s0109 without saying why.

**Consequence.** The Q5 ranking may reflect who was examined and how, not which files are better.

## 23. c00681 cannot render its own maker output — medium

**Report text.** Q5: "**c00681** … Skeleton for a dispatched designer with output modes" and "c00681 is the closest existing model." Caveats listed: self-critique, stack-specific skills, no evidence of testing.

**What is wrong.** The omitted caveat bears directly on the proposal's centrepiece, clause (3).
- Its `tools:` line is "Bash, Read, Write, Edit, Grep, Glob, WebFetch, SendMessage, ListAgents": no browser or MCP tool.
- Its boundaries forbid "service starts".
- It reads screenshots only "when supplied".
- Its maker procedure ends in "Critique against the brief … Fix issues", with no render step.

Its `renders_and_looks` flag rests on reading screenshots supplied by the caller. Its mode behaviour also depends on seven preloaded skills and on `web-design/references/*.md`, none of which were collected. Most of what makes its mode table work is therefore unread, which the report counts against s0109 and s0112 but not against c00681. It is single-owner with 1 copy.

## 24. Omission: a prototype alone is not enough; the handoff must be spec-grade — medium

**Where.** The output theme, T3 (20 records / 18 owners, about 14 voices; "agents only"): "When the designer does not integrate, what it hands over must be spec-grade: tokens by name, measurements, every state. A prototype alone is not enough." The interaction theme adds a motion spec for handoff (c00361 "Specify motion with duration, easing, property and the reduced motion behaviour, or specify none"; c00170 treats a static mockup without interaction specs as incomplete). The scope theme's theme 5 (27 records / 23 owners) makes the same point.

**What the report does.** Its Appendix A (5) boundary and (6) return list many items: paths, direction, states, deviations, "production behaviour left out". It never requires an implementable spec beside the prototype. For a designer whose output goes to an implementer, this is the largest agent-side theme bearing on clause (5), and it would add a return field.

## 25. The Q1 agent/skill gaps are partly an output-type effect — low

**Report text.** Q1 table, with "Confidence: **high** for the direction of every row above", and "Skills carry anti-generic doctrine at about twice the agent rate (51% vs 27%)."

**What is wrong.** Skills write production code at 58% against 27% for agents, and anti-generic lifts with production code. Stratified by output:
- Anti-generic is agents 43% vs skills 62% among production-code roles, and 21% vs 34% among the rest. That is about 1.5x, not 2x.
- `commits_to_direction` shows the same pattern (43 vs 62, and 19 vs 27).
- The rendering gap does hold within strata: 15 vs 38, and 14 vs 41.

So "authors split along the proposal's line" is partly "skills are build-oriented".

## 26. "The one piece of evidence" of tuning against failure — low

**Report text.** Q5: s0078 "is the only file among the close reads whose rules are traced to recorded product misses, which is the one piece of evidence that anything here was tuned against failure."

**What is wrong.** The same table's s0112 row says "Gotchas that read as learned from real failures". The s0024 close read says "Several passages read like patches for specific observed failures". "Traced to recorded misses" is narrower than "read as learned", but "the one piece of evidence" overstates.

## 27. The c00042 claim is propped up with an unrelated repo view — low

**Report text.** Q4 adopt item 1: "This is a claim about how instructions behave … and it matches this repo's own view that a neutral rewording still primes."

**What is wrong.** The repo's view is about a *rule* priming the behaviour it names, even when reworded. c00042 claims that a *negation* shifts the model to another fixed default. The two are related but distinct, and citing one as agreement with the other is confirmation by analogy. The report does keep confidence low, which is right.

## 28. "Carefully built" is used as evidence — low

**Report text.**
- Scorecard: "The most carefully built sources keep taste out of the role."
- Q1: "The best-built agents put taste outside the role".
- Q1 bearing: "One designer role plus a separate reviewer matches the minority of carefully built systems".

**What is wrong.** "Carefully built" and "best-built" are the synthesiser's judgements, made partly on whether a file matches the proposal's architecture. They are then cited as support for that architecture. No independent quality criterion is given.

## 29. The opt-in-rendering counter-position is dismissed by kind — low

**Report text.** Q3: "Minority counter-position: rendering as opt-in. … (s0071), … (s0064), and s0013's harness "**only when the user explicitly asks**". All three are review-oriented or interactive skills."

**What is wrong.** s0013 (web-design-engineer, 10,402 stars) is a create-mode maker skill. Its close read calls rendering-off-by-default "the sharpest conflict in the file" with the proposal. The evidence theme's dismissal ("Both are review skills") covered only s0071 and s0064. Adding s0013 puts a popular maker in the counter-camp, which the report's "or interactive" hedge hides.

## 30. Reviewer bases are cited without their close-read defects — low

**Report text.** Q5 reviewer-side bases: c00286 ("an evidence gate …, a viewport matrix and an evidence pack"), c00214 ("an empty return is valid") and s0110 ("the evidence-class table").

**What is left out.**
- c00286 forces "List 3 to 5 items" for critical and moderate issues, which makes the reviewer invent or drop findings. It also demands exact Tailwind changes from pixels without reading source.
- c00214's REJECT-on-any-finding combined with "an empty return is valid" gives "a strong incentive to under-report".
- s0110 has a "Considered and rejected" minimum that pushes toward invention, and arbitrary finding caps.

These defects matter if the harness borrows these files for its reviewer.

## 31. Omission: s0094's distinctness check is a self-judgement — low

**Report text.** Q4 adopt item 4 and Appendix A (2): "Variants distinct by a stated axis, checked after rendering (s0094 …)".

**What is left out.** The s0094 close read says "structurally distinct" is "judged by the same agent that built the directions, with no criterion beyond the list of decision axes". Under the report's clause (6), that is a verdict by the author. It needs either the named-axis form (s0108) or the reviewer.

## 32. Omissions from the accessibility and scope themes — low

- **Accessibility intent in redesign.** s0024: "Preserve accessibility intent such as label relationships, focus order, landmark roles, and keyboard affordances." The accessibility theme notes that a redesign can silently drop semantics the existing UI had. Appendix A (1) does not include it.
- **Conformance with no accessibility role.** The accessibility theme notes that conformance auditing goes to a separate accessibility role (theme 15), and "The harness has no accessibility role". The report's Appendix A (4) baseline does not say who does conformance.
- **User and brand context that is not in code.** The scope theme's counter-voice s0052 says to ask for user and brand context "and do NOT infer context from the codebase instead". Reading code settles the design system, not who the users are or what the brand means. The report's clause (1) grounding and clause (2) assumption rule do not address this.
- **c00337 as a skill base.** Its close read calls it "the best base for a design skill that the designer loads, specifically the process half", and recommends lifting its tiered Verification section and "Diagnose first, treat second". The synthesis uses c00337 mainly as a form-coverage example and a slop-score rejection.
