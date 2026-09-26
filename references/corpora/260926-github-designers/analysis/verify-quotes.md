# Quote and attribution check of synthesis.md

Scope: every double-quoted span in `analysis/synthesis.md` (228 spans) was extracted by script and searched in the named record's `file` after normalising whitespace, curly quotes, backslashes and Markdown emphasis; ellipses were treated as gaps. Spans with no record id on the line (labels, theme names, the proposal's own words) were checked by hand. Quotes that failed, and a sample of quotes that passed, were then read in their surrounding lines to check context. Record ids used as attributions without a quote (contradiction tables, tool table, mode table, paired sets, split-owner list) were checked with grep and recomputed from `records.json`.

Result: nearly every instruction quote is verbatim in the named record, and the recomputed tables (form coverage 56/169/127/47/4/2/0; the six 4+-form records; 16/15 mock+critique; 48/41/40 middle position; 44-agent tool table 24/13/6/1; skill tool table 36/1/1; 15 split owners, 14 rendering, 42 records with 25 skills; 257 single-record owners with 42 rendering and 114 make+review; "Purple gradient(s) on white" and "Space Grotesk" each in 23 owners) all match. The issues below are the exceptions: 20 in total, 1 high, 6 medium, 13 low.

## High

### 1. s0072's KEEP / GENERIC / DUPLICATE pass prunes generic audit findings, not generic design output

- Report text (line 396, "Rare instructions worth adopting" #10): "**An anti-generic check run in a separate context.** "dispatch a fresh sub-agent with the draft list … KEEP / GENERIC / DUPLICATE" (s0072). This is how the proposal's "review is separate" can still catch generic output."
- What is wrong: the quote is verbatim, but the context changes its meaning. In s0072 (jezweb ux-audit, a review-only QA skill) the "draft list" is the auditor's own list of findings. GENERIC means "would apply to any web app", so the pass drops boilerplate findings from an audit report. It does not judge whether a designed artifact looks generic. The report's recommendation #10 rests only on this source, so the corpus gives no example of a separate-context check on generic design output.
- Evidence: s0072 L348-354: "### Self-critique pass (mandatory before publishing) / After the findings draft, dispatch a fresh sub-agent with the draft list and this prompt: > "Read these audit findings. For each, mark KEEP / GENERIC / DUPLICATE. KEEP = specific to this app, this persona, this surface. GENERIC = would apply to any web app. …""
- Severity: high. The recommendation loses its only cited source. The idea may still transfer, but the report should call it an analogy, not a corpus instruction.

## Medium

### 2. The "author cannot review its own work" quotes do not come from split systems as the report defines them

- Report text (lines 98-101): "The corpus's strongest statements that an author cannot review its own work come from split systems:" followed by c00581, c00320 and s0072.
- What is wrong: by the report's own definition (an owner with a review-only record beside a maker record, line 82), none of the three owners is split. me2resh (c00581, c00230) has no review-only record. bpmforge (c00320 revise+review, c00321 create, c00322 create+revise+review) has none either. jezweb has only s0072, a single review-only skill. None of the three is among the 15 listed split owners. c00581's reason is also a tooling fact ("You cannot nest the Agent tool, so you cannot spawn the real code-reviewer (Rex). Because of this, any review you produce is not independent"). c00320's "Verifier" is a report field, not a separate role in the corpus.
- Evidence: records.json modes per owner, recomputed. The split-owner list recomputes exactly as the report states, with davila7, davepoon and microsoft excluded.
- Severity: medium. The quotes support "authors want independent review", but not the link to split systems that the medium-confidence interpretation in that paragraph relies on.

### 3. s0085 has no "Detectable request" routing

- Report text (line 140): "c00135 and s0085 microsoft hve-core | `frame-needs` … `prepare-handoff` | Keyed to a "Detectable request", with required context per mode". Line 560: "c00135 and s0085 route by "Detectable request"."
- What is wrong: "Detectable request" is only in c00135 (the agent, L88 table header "Mode | Detectable request | Required context"). s0085 (the ux-artifacts skill) takes an explicit `mode=` argument, with a table of "Mode | Outcome | Reference", and "Ask one routing question only when the requested asset matches more than one mode." Both records belong to one system from one owner, so this is one voice counted as two records.
- Evidence: `grep -c -i detectable` returns 0 for s0085 and 1 for c00135. s0085 L4 is the argument-hint `[mode=frame-needs|…|prepare-handoff]`, and L21-37 hold the mode table and the routing rule.
- Severity: medium (a wrong attribution in a table and in Correction 1).

### 4. "Static interfaces are strictly forbidden." is in s0018, not s0006

- Report text (line 405): "and taste-skill's perpetual looping animation, "Static interfaces are strictly forbidden." (s0006)."
- What is wrong: the sentence is in s0018 (Leonxlnx/taste-skill `skills/gpt-tasteskill/SKILL.md` L47: "Static interfaces are strictly forbidden. You must write real GSAP …"). It is not in s0006 (`skills/taste-skill-v1`). s0006 does have perpetual micro-interactions, but only behind a dial: "When `MOTION_INTENSITY > 5`, embed continuous, infinite micro-animations" (L70, default 6), and it offers "1-3 (Static): No automatic animations" (L88). The owner is the same, so it is one voice.
- Severity: medium (quote attributed to the wrong record, and the conditional is dropped).

### 5. s0069 is not a "16px floor" and does not contradict 13–14px for dense tools

- Report text (line 71): "Body text is 16px in s0069 and 13–14px for SaaS in s0045 and c00603." Line 349: "Body text | 16px floor (s0069) against 13–14px for dense SaaS (s0045, c00603)".
- What is wrong: s0069 sets 16px as a starting point for long-form text and names dense professional tools as a valid reason to go smaller. It therefore agrees with s0045 and c00603 rather than contradicting them. (Its separate 16px rule for inputs is about iOS zoom, not body text.)
- Evidence: s0069 L112: "Start long-form body text at `16px`, the browser default. Move off it only for a reason you can name: the typeface runs small, the measure is narrow, or the product is a dense professional tool."
- Severity: medium. One of the five "taste sources contradict each other" examples and one row of "Concrete values disagree" do not hold. The conclusion survives on the other rows.

### 6. s0044 does not cleanly reject staggered entrances

- Report text (line 354): "Staggered entrance | recommended (the frontend-design family) against rejected (s0037, s0044, s0045)".
- What is wrong: s0044 (cloudflare/vibesdk frontend-design-landing-page) ships stagger variants: "// Stagger children const staggerContainer = { animate: { transition: { staggerChildren: 0.1 } } }" (L396-398) and "// Stagger container (for card grids) export const staggerContainer" (L1400-1411). Its "does NOT stagger in one-by-one" (L1102) applies only to whole page sections. It is mixed, not a rejection. s0037 rejects "fade-and-slide-up entrances on each section" but endorses "one page-load sequence", which is close but not the same as rejecting stagger (I am unsure on s0037). s0045 is a clean rejection.
- Severity: medium (a figure or attribution in the values table).

### 7. Contrast of animation ceilings mixes different scopes

- Report text (line 350): "UI animation ceiling | 200ms (s0063), 300ms (s0003), 500ms (s0083)".
- What is wrong: s0063's 200ms is for interaction feedback only ("NEVER exceed `200ms` for interaction feedback", L53). s0083's 500ms is an absolute cap above budgets of 100–400ms ("Never exceed 500 ms for any UI animation", L89), and those budgets overlap s0003's "under 300ms". Read in context, the three values are largely compatible. I am unsure whether this should be medium or low.
- Severity: medium (it inflates the disagreement the table is used to show).

## Low

### 8. "fewer, not zero" is a paraphrase in quotation marks
- Report text (line 458, s0003): ""fewer, not zero" for reduced motion." Source L540: "Reduced motion means fewer and gentler animations, not zero." Low.

### 9. "click it and watch the DOM" is a paraphrase in quotation marks
- Report text (line 465, s0072): "Borrow only its capability probe and "click it and watch the DOM"." Source L219-222: "1. **Click it.** … 3. **Watch the DOM.** …". The verbatim form appears correctly at line 251. Low.

### 10. "AI made this" is placed next to records that do not contain it
- Report text (line 401): "**Slop and "AI made this" self-scores.** … (c00337), … (s0061)". The phrase is in s0002, s0052 and s0112 only. c00337 says "slop" and s0061 says "If another AI … you have failed". It reads as a label, but the quotation marks suggest a source. Low.

### 11. "could a default prompt have produced this?" is a paraphrase in quotation marks
- Report text (line 333, Q4 table): "General anti-generic stance ("could a default prompt have produced this?")". The corpus wording is "If it could have been generated by a default prompt, it is not good enough." No record contains the question form. Low.

### 12. c00003's precedence line is present in one copy of a 62-repo cluster
- Report text (line 217): "c00003 adds a duty to report conflicts: "Project `AGENTS.md` … overrides any advice in this persona. …"". Also Appendix A (1). The quote is verbatim in the representative file, which is GammaLabTechnologies/harmonist: a `<!-- precedence: project-agents-md -->` block added above the shared persona. Of the 74 corpus files carrying the same "UI Designer Agent Personality" body, 1 has the "overrides" line. The attribution is correct, but a reader who weighs c00003 by its 62 copies (line 440) would overstate how far the line spread. The report does not claim spread here. Low.

### 13. c00042's "pair every avoid with a concrete target" and "sketch, pick, proceed" are scoped to overriding one model's house style
- Report text (lines 371, 386): these are presented as general mechanisms. In c00042 L35 and L72 both sit inside rules for overriding "Opus 4.7's default house style" under a domain mapping ("Non-editorial briefs … override the default explicitly"). c00042 also allows "surfacing the options to the user before proceeding" when the runtime supports clarification. The report does note the model tie under reject #4 and marks #1 as low confidence. Low.

### 14. s0013's "stunning" line continues in the same sentence with "Respect design systems"
- Report text (line 405): ""The bar is "stunning," not "functional."" and "Aim to Stun" (s0013) … Wrong defaults for extending an existing product." Source L10: "The bar is "stunning," not "functional." Every pixel is intentional … Respect design systems and brand consistency while daring to innovate." The omitted clause softens the reading. Low.

### 15. s0071's opt-in also triggers on a cheap preview, not only on a user request
- Report text (line 302): "Minority counter-position: rendering as opt-in. "Rendered verification is opt-in." (s0071)". Source L106: "Mark visual and runtime claims **Not verified** unless the project exposes a cheap preview or the user asks for a rendered review." Grouping it with s0064's user-only trigger slightly overstates the opt-in position. Low.

### 16. c00699 is given as an example of lists that say "right now"
- Report text (line 482): "Several lists say "right now". Two examples: c00699, "neumorphism umarl w 2024" …". c00699 does not say "right now". Its line dates a trend ("Flaguje trendy które odchodza (neumorphism umarl w 2024)"). The quote is verbatim, and only the framing is off. Low.

### 17. The 56 zero-form records are not all spec, wireframe or docs roles
- Report text (line 120): "The 56 records with none of these forms are spec, wireframe or docs roles." 9 of the 56 have no output tag at all (c00000, c00004, c00015, c00071, c00155, c00181, c00338, c00374, c00618). c00000, for example, is an activation stub with 93 copies. The other 47 are spec, wireframe or docs roles. Low.

### 18. The mode-table count includes one template twice
- Report text (lines 133, 144): "at least 14 records from 12 owners". c00113 (borgius) and c00430 (uramigal8-a11y) are the same gem-designer template ("Parse mode (create|validate)"), and c00135 and s0085 are one microsoft system. That leaves about 10 independent voices. The report's own rule is to count families as one voice. Low.

### 19. s0005 does not simply "prescribe" single-word italic emphasis
- Report text (line 68): "Single-word italic emphasis in a headline is prescribed in s0005 and listed as an AI tell in s0037." s0005 L179 is conditional ("When you want to emphasize a word within a headline … use italic or bold of the SAME font"), and L650 bans "`<br>`-broken-and-italicized headlines as a default "design move."" The two files still differ, but less sharply than "prescribed". Low.

### 20. s0037 "never mentions an existing design system" (unsure)
- Report text (line 455). This is literally true, since the phrase "design system" is absent. However, the description scopes the skill to "building new UI or reshaping an existing one", and L45 says "the brief's own words always win". A reader may take the caveat to mean s0037 ignores existing UI entirely. I am unsure this is an error. Low.

## Checked and found correct (not issues)

- All translated quotes match their originals: c00298 (Norwegian, three quotes), c00351 (Chinese, two), c00191 (Spanish) and c00699 (Polish).
- The analysis-file quotes in "Corrections" are verbatim: output.md L159, scope-collaboration.md L183 and deep/c00001.md L42.
- The tool-allowlist attributions are correct: c00114, c00324, c00441, c00389, c00608, c00613, c00629, s0099 and s0042. s0042's includes `mcp__chrome-devtools__take_screenshot`.
- The contradiction attributions for Lucide, glassmorphism, easing and em-dash are correct. Cream is correct as a colour family, though s0089 says "warm off-white" and s0060's rejection is about blending into a host UI.
- The deep-read defect claims cited in Q5 (c00062 MPC, c00079 tool names, c00003 escaping, c00102 12px, s0003 greeting and checklist, s0005 contradictions) match the deep files.
