# Audience dimension: recurring themes

Source: `claims/audience.jsonl`, 443 quotes from 384 distinct records, 314 repos, 298 owners (owner = the repo part before `/`).

## Method

- I read all 443 lines. Quotes were first shown up to 260 characters, and I pulled the full text of every quote cited here. Only one quote (c00925) was longer than that. Nothing was sampled.
- I assigned each line to zero or more themes by hand, by line index. The assignment is in `analysis/themes/audience.assign.json`: keys are theme codes, values are 0-based line indices into `audience.jsonl`. A script computed every count below from that assignment. 416 lines went into at least one theme and 27 went into none. The unassigned lines are mostly role descriptions, domain one-offs and channel length limits.
- A line can belong to several themes. For example, "Assume beginner unless told otherwise; keep it skimmable" counts toward both "newcomer" and "reader state".
- Counts are distinct records / distinct repos / distinct owners. Doc-type concentration lists the most frequent types, each with its lift: the type's share of the theme's lines divided by its share across all 443 lines.
- To trace lineage, I clustered near-identical quote text across owners and grepped `corpus/` for template signature phrases. The lineage section explains how.
- There was one coder and no second rater, so each theme's edges are judgment calls. The ordering by owner count holds up better than the exact numbers.
- Context from `stats.txt`: the `audience_first` flag is set on 475 of 1,089 writing roles (44%). It runs higher for changelog (60%), api-reference (59%), ux-microcopy (59%) and marketing-copy (58%), and lower for report-analysis (35%) and fiction (14%).

## 1. Top recurring themes (ordered by distinct owners)

### 1. Identify the target audience before writing, and write for it
This is the step "who reads this?", usually followed by a menu of roles (developers, operators, end users).
- Counts: 117 records / 103 repos / 99 owners. This is a third of all owners in the dimension. It has two sub-patterns:
  - the explicit identify/assess step: 89 records / 76 repos / 72 owners
  - the bare directive "write for the (developer/target) audience": 29 records / 28 repos / 28 owners
- Doc types: project-docs 82 (1.0x), api-reference 69 (1.3x), other 21 (1.6x), changelog 21 (0.9x). Scope is spread evenly: 42 general-purpose, 39 few-types and 36 single-type records.
- "Define the audience explicitly for each document including their assumed knowledge level, common goals, and the questions they arrive with" — c00084
- "READER     Determine audience + task: what does the reader want to achieve, what do they already know, where do they start?" — c00397
- "Never write for a generic "reader."" — c00264

### 2. Assume the reader lacks your context: write for a newcomer, define terms, state prerequisites
- Counts: 39 records / 38 repos / 36 owners
- Doc types: project-docs 34 (1.3x), api-reference 19 (1.0x), code-comments 10 (1.8x), prd-spec 8 (1.5x)
- "Never assume a reader has context they don't — if a term is project-specific, define it the first time it appears" — c00369
- "NEVER assume the reader's context — state prerequisites explicitly" — c01442
- "A new developer must be able to build, run, and understand from the docs alone. Human language, not system jargon." — c01182

### 3. Calibrate depth, complexity and terminology to the reader's knowledge level
- Counts: 31 records / 30 repos / 30 owners
- Doc types: project-docs 26 (1.2x), api-reference 23 (1.5x), changelog 10 (1.5x)
- "Adapt to the audience: more context and "why" for junior developers; direct implementation detail for senior engineers; business outcomes and analogies for non-technical readers." — c00352
- "Assess the technical level of your target audience and adjust complexity accordingly" — c00122
- "Match the repository's existing terminology, heading hierarchy, link style, and audience level before introducing a new format." — c00946

### 4. Pair the reader with their task: what they want to do, and what they should be able to do afterwards
- Counts: 30 records / 27 repos / 27 owners. 13 of these owners also appear in theme 1, where the task is attached to the identify step.
- Doc types: project-docs 29 (1.4x), api-reference 20 (1.4x), changelog 7 (1.1x)
- "Open with the user job-to-be-done; documentation that does not enable a task is decoration." — c00360
- "Ask: Who reads this? What do they care about? What should they do after reading? If you can't answer all three, clarify with the user." — c01062
- "通读全文，先回答三个问题。这篇的控制性主旨是什么（一句话）。目标读者是谁、他读完要能干什么或懂什么。现在最大的问题在结构层还是句子层。" (read the whole piece and first answer three questions: what is its controlling idea, in one sentence; who is the target reader, and what should they be able to do or understand after reading; is the biggest problem now at the structure level or the sentence level) — c01627

### 5. Serve several audiences at once through layers, sections or reading paths
- Counts: 24 records / 23 repos / 22 owners
- Doc types: project-docs 17 (1.0x), api-reference 12 (1.0x), report-analysis 8 (2.0x), code-comments 7 (2.0x)
- "Provide reading paths for different audiences (developers, architects, operations)" — c00025
- "documentation serves two audiences: 1. **Human developers** who need to understand usage patterns, constraints, and edge cases 2. **AI coding agents** that use structured documentation to build semantic understanding of codebases" — c01064
- "a comprehensive narrative threat report that communicates risk posture, threat analysis, attack paths, and remediation priorities to diverse stakeholders -- from CISOs presenting to boards, to security engineers planning remediation, to project managers converting findings into development tasks" — c00925

### 6. Use plain language for non-technical readers, sometimes with a target reading level
- Counts: 22 records / 22 repos / 22 owners
- Doc types: project-docs 10 (0.7x), report-analysis 9 (2.7x), changelog 5 (1.1x). Mostly single-type roles (16 of 22).
- "Do not assume the reader understands technology -- Every term needs a business explanation" — c00772
- "confirm reading level matches the audience (technical content roughly Grade 10-12)" — c00448
- "Simplificar linguagem` (description: `"Reduzir para nível ~14 anos"`)" (simplify language; description: "reduce to roughly a 14-year-old's level") — c00215

### 7. Name a concrete reader persona, stating what they already know and what they do not
- Counts: 22 records / 22 repos / 22 owners
- Doc types: project-docs 20 (1.4x), api-reference 9 (0.9x), prd-spec 4 (1.3x)
- "Audience: JavaScript/TypeScript developers familiar with testing (Jest, Mocha) but potentially new to contract testing" — c00624
- "Assume the reader is comfortable with C# but has never used this library before." — c00927
- "Assume the reader is a numerical methods engineer implementing the algorithm from scratch" — c01546

### 8. Write from the reader's side, not the author's or the implementer's
- Counts: 21 records / 21 repos / 21 owners
- Doc types: project-docs 17 (1.2x), api-reference 15 (1.5x), changelog 11 (2.4x)
- "実装者（developer）が「何を作ったか」を知っているのに対し、 ライターは「読者が何を知る必要があるか」を考える。" (the implementer knows "what was built"; the writer thinks about "what the reader needs to know") — c00185
- "Write from the perspective of a **consumer**, not the implementor" — c00337
- "Write in the user's language, not the product team's language. Study the PRD's target user." — c01581

### 9. Lead with what the reader needs or gets: the outcome, the verdict, the bottom line
Features and internals come after.
- Counts: 21 records / 19 repos / 19 owners
- Doc types: project-docs 14 (1.0x), api-reference 11 (1.1x), changelog 10 (2.3x), report-analysis 6 (1.9x)
- "Lead with the user's goal, not the feature: "To export your data..." not "The export feature allows..."" — c00357
- "Lead with the verdict. A reader who leaves knowing only "it runs your tests on a diff and tells you whether that proved anything" has the product." — c00785
- "Lead with outcome reader wants ("Set up Stripe webhooks", not "Webhooks Overview")" — c01447

### 10. Marketing and UX copy: persona, pain points, awareness stage and brand voice decide the text
- Counts: 21 records / 17 repos / 17 owners
- Doc types: marketing-copy 21 (9.6x), ux-microcopy 9 (8.3x), social-media 3 (4.9x). This is the most type-bound theme after executive summaries.
- "Identifying which stage of awareness the reader is in and writing accordingly" — c00394
- "Your readers are risk managers, compliance officers, CISOs and auditors — people who read regulation for a living and detect vagueness instantly." — c01139
- "Your CLAUDE.md says "no hyperbole" and your audience is ad tech professionals who've been oversold by every vendor they've met." — c00087

### 11. Keep implementation details out of user-facing text: no code references, internal names or internal jargon
- Counts: 17 records / 17 repos / 17 owners
- Doc types: project-docs 15 (1.3x), api-reference 8 (1.0x), changelog 8 (2.3x)
- "User-guide content **MUST** be written for end users — no implementation details, no code references, no internal jargon." — c00184
- "User-facing language. Never mention internal function names, CGI script paths, or AT commands." — c01223
- "Identify the **outward-facing** subset (public APIs, headline features, how-to-run) — skip internal WAL / governance content." — c01395

### 12. Ask or confirm the audience when it is unclear
- Counts: 15 records / 15 repos / 14 owners. One record says the opposite: "There is no need to ask about the target audience." — c00839
- Doc types: project-docs 8 (0.8x), blog-article 5 (6.0x), marketing-copy 5 (3.0x), report-analysis 4 (1.6x)
- "Ask the user which audience the report is for (internal management or customer-facing) if this is not clear from the input, as tone and detail level differ." — c00896
- "Every document has one audience. Ask if unclear." — c01057
- "Clarify the ask. What file? What audience? What learning objective?" — c01310

### 13. An explicit map from audience role to content
Developers get code, users get steps, stakeholders get outcomes.
- Counts: 15 records / 13 repos / 13 owners
- Doc types: project-docs 10 (0.9x), api-reference 7 (1.0x), report-analysis 6 (2.4x), prd-spec 5 (2.3x)
- "Audience: devs = APIs/snippets; users = steps; stakeholders = outcomes." — c00504
- "Write for the audience: technical details for engineers, impact statements for stakeholders, action items for project managers." — c00340
- "For customer-facing: use less technical language, omit internal team details, focus on impact and resolution. For internal: include full metric detail, team performance context, and root cause references." — c00896

### 14. The reader may be an AI agent, so write for how an agent consumes the text
- Counts: 14 records / 13 repos / 13 owners
- Doc types: project-docs 12 (1.1x), changelog 5 (1.5x), prd-spec 4 (1.8x). There are no general-purpose roles in this theme.
- "Your output is read by both humans and other AI agents, which sets a higher bar than usual: an agent will copy your code samples verbatim into a real project." — c01132
- ".omp/AGENTS.md: assume reader is an AI agent about to write code" — c00292
- "A future coding agent must act from **this page alone**." — c00870

### 15. Write for the reader's state: hurried, impatient, stressed, mid-task, or on a time budget
- Counts: 13 records / 13 repos / 12 owners
- Doc types: project-docs 11 (1.3x), api-reference 6 (1.0x), other 3 (2.1x), code-comments 3 (1.7x)
- "You write for the stressed developer at 3 AM with a deadline, ensuring every sentence reduces cognitive load and moves them toward task completion." — c01090
- "You write for the reader who is mid-task and impatient: lead with what they need, cut the throat-clearing, never explain what the code already shows." — c01127
- "You write for someone at 3am who did not build this. That audience changes everything about how the document should read." — c01318

### Themes below the top 15

These are still counted from the assignment. Several bear directly on the proposal (section 4).

| Theme | Records / repos / owners | Concentration | Example |
|---|---|---|---|
| One audience per document: split rather than blend | 15 / 11 / 11 | prd-spec 2.6x | "One audience per document. README is for users/integrators; ADRs are for maintainers; API reference is for callers. Don't blend." — c01127 |
| Executives and decision-makers get a plain top section: bottom line, risk, action | 13 / 11 / 11 | report-analysis 6.5x (12 of 13 records single-type) | "Executive Summary: one sentence for each of: what happened, severity, immediate action. Non-technical language." — c00938 |
| The document type fixes the audience (tutorial = beginner, README = never seen the project) | 11 / 11 / 11 | api-reference 1.7x, changelog 1.9x | "Identify the audience per doc (Diátaxis): tutorial = beginner, how-to/reference = competent practitioner, explanation = someone seeking understanding" — c01567 |
| Don't dumb it down: assume a competent or expert reader | 11 / 11 / 11 | project-docs | "Assume the reader is competent and intelligent." — c01103 |
| The audience comes from an outside source: the caller's brief, a persona file, a ticket or a profile | 10 / 10 / 10 | marketing 5.8x, ux-microcopy 7.7x, blog 7.7x | "Expect the caller's brief to state what to write, the audience, the purpose, and pointers to relevant material." — c01209 |
| Self-contained: the reader has only the document, not the process that produced it | 9 / 9 / 9 | academic 11.5x, report-analysis 2.4x | "You draft for a reader who has only the finished document — never the planning conversation, never your own context." — c00710 |
| Audience fit as a review check | 8 / 7 / 7 | api-reference, blog | "Every documentation change must include: affected sections, target audience, and verification that examples work." — c00425 |
| Write in the audience's natural language or locale | 6 / 6 / 6 | prd-spec, changelog | "If the codebase or existing docs are in Japanese, write in Japanese" — c01400 |
| Write for the future reader or maintainer, months later | 6 / 6 / 6 | prd-spec, other | "Written for future readers — understandable 12 months later" — c00547 |
| State the audience in the document or its record | 6 / 5 / 5 | project-docs | "Every document states its audience and its scope near the top." — c01317 |

## 2. Lineage warnings

- **"Assume the reader lacks your context" (theme 2) and the "write for the developer audience" sub-pattern of theme 1 rest partly on one template.** GitHub's published `docs-agent` example contains "You are an expert technical writer for this project", "You write for a developer audience, focusing on clarity and practical examples" and "don't assume your audience are experts in the topic/area you are writing about". I grepped `corpus/` for those signature phrases: 19 files contain the second phrase and 12 contain the third. In the audience claims the family covers 10 records from 10 owners: Adversis, GovTechSG, KrijnvanderBurg, PowerGenome, Qredence, extenda, fugazi, inbo, open-telemetry and universetraveller. terraware's `docs-agent.md` ("Write for developers who are new to the codebase") is probably another variant. The family's share by theme:
  - theme 2: 7 of 36 owners (8 with terraware)
  - the "write for the (developer) audience" sub-pattern of theme 1: 7 of 28 owners
  - theme 1 as a whole: 7 of 99 owners

  Discounted, theme 2 is about 28 independent owners. It stays second, but its lead over theme 3 mostly disappears.
- **Theme 1 carries the most copying.**
  - "Identify target audience and their needs" appears verbatim at github (c00003, which alone has copies in 72 repos), diet103, josstei and Tuntii.
  - "Identify the audience: Who will read this?" is shared by CloudAI-X and github.
  - A checklist line appears in three repos: "读者是谁？（初学者、有经验的开发者、架构师？）" (who is the reader? beginner, experienced developer, architect?) at liaoxinjie666 and xuanbingbingo, and in English at imMamdouhaboammar.
  - "Identify audience and goals" appears at j0hnnymiller, ssdeanx and accountex-org.
  - jmagly contributes 7 records that are template slots ("Audience: [...]") from one generator. They inflate the record count (117) but add only one owner.
  - The copies sum across theme 1's records is 354, driven by c00003 (72), c00009 (34) and c00012 (27). Owner counts ignore copies, so the ordering holds.
- **Theme 5, multi-audience reading paths.** wshobson (c00025, 13 copies) and viksant (c01068) carry the same sentence, so they count as one voice. davila7/claude-code-templates is an aggregator whose records re-host other authors' agents: c00515 repeats jasonmichaelbell78's c00216 word for word. It appears in themes 1 and 12.
- **One-audience-per-document (below the cut).** It has 15 records but only 11 owners. UitbreidenOS contributes 5 records that are one sentence in five languages (c01411 to c01415). The record count overstates the theme by a third.
- **Theme 10, marketing.** UitbreidenOS contributes 4 records that are one "ATL format for VP-level outreach" line in four languages (c01416 to c01419).
- **Executive summary (below the cut).** taxideftis contributes 3 records that are one line in Korean and English (c01180, c01181, c01183).
- **Themes 2 and 15.** vchelaru has 3 identical records, "Assume beginner unless told otherwise" (c00686, c01438, c01484).
- **Theme 7, persona.** Dao-AILab (c00029, 12 copies) and CalaW (c00100) share "You write for academics and researchers who may not have a coding background".
- **Theme 8, "not yourself".** Two slogans recur verbatim: "Write for your audience, not for yourself" (SuperClaude-Org, 27 copies, and jucish2019-a11y) and "Write for the reader, not the writer" (micronugget and kennedym-ds). The theme has 21 owners, but a real share of them repeat a slogan and add no operational content.
- **Audience-fit review check (below the cut).** borgius and melnikov1512 carry the identical "Validate readability: appropriate audience language, consistent terminology, good hierarchy", which is 2 of that theme's 7 owners.
- **prmichaelsen/agent-context-protocol** has 17 writing roles repo-wide. Only 2 of its records land in any theme here (the agent-reader theme), so it does not distort this dimension.

## 3. Sharp but rare

Each of these is carried by 1 or 2 owners and is precise enough for a writer role to adopt as written.

1. The reader gets only the deliverable. The writer's context never reaches it: "You draft for a reader who has only the finished document — never the planning conversation, never your own context." — c00710 (JetBrains)
2. A testable rule for keeping process residue out: "If a phrase would only make sense to someone who watched the work being produced, it does not belong in the report." — c00707 (frenzymath)
3. Put the strength of the evidence where a skimming reader will see it: "If the total distinct repository count across all variations is under 10, say so in the Executive Summary as well, so a reader skimming the top does not mistake a thin result for a survey of government practice." — c00608 (tractorjuice)
4. Update per audience and report the skips: "Large change, narrow audience: Session changed 30 files but only one is user-facing. → Update only the user-facing doc." and "If a given audience has no relevant change, skip it and note in the audience-split report." — c01036 (Kanevry)
5. The caller is not the reader: "Do not adopt the human’s Claude.ai user profile / occupation. That profile is about **them**, and it leaks into every product." — c00873 (VKirill)
6. An agent reader acts on text literally: "Your output is read by both humans and other AI agents, which sets a higher bar than usual: an agent will copy your code samples verbatim into a real project." — c01132 (Nagarjuna2997)
7. Use the reader's vocabulary, down to UI labels: "manual steps are written in the user's vocabulary (palette wording, surface titles, chip labels — never symbol names), one observable expectation per step" — c00788 (RafaelGB)
8. Rank the readers when there are several: "Who is the primary reader (highest stakes)? Who is the secondary reader (emotional resonance)? Set register to primary reader." — c01234 (MShneur)
9. The reader must be able to tell assumed values from computed ones: "审阅者可以扫描工作表，立即区分假设值与计算值。" (a reviewer can scan the worksheet and immediately tell assumed values from computed values) — c00406 (Zeus-Center)
10. A fixed shape for the top of a report: "Executive Summary: one sentence for each of: what happened, severity, immediate action. Non-technical language." — c00938 (FlorianBruniaux)

## 4. Bearing on the PROPOSED WRITER

**Point 1, start from the reader and what they will do with the document: supported, with a caveat about form.**
- Audience-first is the largest theme in the dimension (99 of 298 owners). The flag is also on 44% of all 1,089 writing roles.
- Most of that support is the bare step "identify the target audience" (72 owners), which usually comes with a role menu and nothing operational.
- The form the proposal wants, reader paired with task, is a minority, but a sharper and less template-driven one. It covers theme 4 (27 owners) and theme 9, leading with what the reader needs (19 owners).
- c01062's three questions give a concrete test: who reads it, what they care about, what they should do after reading, and clarify with the user if any answer is missing. c00084 adds a fourth item: the questions the reader arrives with.
- Recommendation: word point 1 as "reader + task + what they already know" rather than "audience".

**Where the audience comes from: the proposal is silent, and the corpus splits.**
- Theme 12 (14 owners) asks the user when the audience is unclear. The outside-source theme below the cut (10 owners) takes it from a brief, persona file or ticket. One record forbids asking (c00839).
- The proposal routes doc-type differences through the caller's brief. That fits the brief-supplied camp: c01209 expects the caller's brief to state the audience, and c00264 determines it "from the delegation prompt or file type".
- In an unattended run the writer cannot ask mid-run, so it needs a fallback. vchelaru's "Assume beginner unless told otherwise" is one default. The writer should then name the assumed reader in its separate notes output so the caller can correct it.
- c00873 adds a guard the proposal lacks: the caller who writes the brief is not the reader.

**Carrying doc-type differences outside the role: supported.**
- Several themes are strongly type-bound. These fit path-scoped rules or the brief rather than the core role:
  - executive summaries: report-analysis 6.5x
  - marketing persona, pain points and awareness stage: marketing 9.6x, ux 8.3x
  - plain language: report 2.7x
  - no internals in user docs: changelog 2.3x
- The doc-type theme (11 owners) says outright that the document type fixes the audience: tutorial = zero knowledge, README = never seen the project, AGENTS.md = an AI agent about to write code (c00292, c00181, c01567). That mapping is exactly what a path-scoped rule could hold.
- The corpus contains no counter-evidence for the general-role choice here: no audience instruction appears that only a dedicated per-type role could carry.

**Tensions a general role must settle, and the proposal does not:**
- **One audience per document** (11 owners) **vs. several audiences in layers** (22 owners). The two owner sets do not overlap. "A page that tries to serve beginners and power users simultaneously serves neither. Split it." (c00242) contradicts reading paths for developers, architects and operations (c00025). A default is needed. c01234's "set register to primary reader" reconciles the two: one primary reader decides the register, and secondary readers get marked sections.
- **Don't assume expertise** (theme 2, about 28 independent owners after the template discount) **vs. don't dumb it down** (11 owners). The direction depends on the document. It belongs in the brief or a path rule as a stated persona baseline (theme 7), not in the core as either default.

**Point 2, every factual sentence traceable to evidence and interpretation marked: little direct bearing, and three additions.**
- c00641 and c00643 (Spielewoy, one owner) record "the audience, information structure, and authoritative source for each material claim". That is a per-claim ledger that also names the audience, close to the proposal's claim → source → tier ledger.
- c00406 wants a reader to tell assumed values from computed ones, which is interpretation-marking framed from the reader's side.
- c00608 wants a thin evidence base disclosed where a skimming reader will see it. This suggests evidence tier belongs in the deliverable's headline when it is weak, not only in the side ledger.

**Point 3, cutting is the default and working notes stay out of the deliverable: supported from the reader's side.**
- The self-contained theme (9 owners) and sharp items 1 and 2 state that the reader has only the document, which is the reader-side reason for keeping notes out.
- The reader-state theme (theme 15, 12 owners) supplies the cutting criterion that the proposal's "cutting is the default" lacks:
  - "cut the throat-clearing, never explain what the code already shows" (c01127)
  - "If a paragraph doesn't help someone get unstuck, cut it." (c01424)
  - "adding only project-specific information the reader cannot infer" (c00738)
- Recommendation: define cutting relative to the reader's task and what they can infer, not as brevity in general.

**Combining drafts and the claim ledger: no bearing.** No audience instruction addresses merging drafts or outside examples. The nearest analogue is c01036's "audience-split report", a return-side record of which audiences got updates and which were skipped.

**What this dimension adds that the proposal lacks:**
1. The reader can be an AI agent (13 owners). This matters for the proposal's "prompts" doc type: an agent copies samples verbatim and must act "from this page alone". The core's idea of the reader should cover agent readers explicitly.
2. The document should state its audience (5 owners), for example near the top (c01317). Because the proposal leaves quality judgment to runs and evals, an eval needs the intended reader written down to score audience fit. Stating the audience in the brief or in the output notes serves that.
3. Language and locale (6 owners): write in the reader's language, and avoid translationese (c00273).
4. Audience fit as a review check (7 owners) conflicts with the proposal's "does not judge its own output". The resolution is the proposal's own: the check belongs to the eval, and it needs item 2 to work.
