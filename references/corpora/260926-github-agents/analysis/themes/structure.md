# Themes: structure

Source: `claims/structure.jsonl`, 1,039 quote lines from 677 distinct records, 527 repos, 507 owners. Every line was read; there was no sampling. Counts below are computed from the file, not estimated.

Method. A first keyword-regex pass seeded candidate themes. I then read every line and assigned records to themes by hand as explicit id lists (one rater, no second coder). A record can belong to more than one theme. Counts are distinct records / distinct repos / distinct owners (owner = the part of `repo` before `/`). "Concentration" gives the doc types carrying the most theme records, as the share of theme records carrying that type, with the lift over that type's share among all 677 records in this dimension in brackets (a record can carry several types). Baseline shares: project-docs 54%, api-reference 36%, report-analysis 18%, prd-spec 16%, changelog 14%, code-comments 10%, marketing-copy 8%, other 8%, blog-article 5%, ux-microcopy 4%, academic 4%, fiction-narrative 3%, social-media 3%, prompt-instructions 3%. Scope baseline: 54% of records are single-type, 13% general-purpose. The appendix lists the record ids per theme so the counts can be reproduced.

Coverage. The 27 candidate themes together touch 495 of 677 records (388 of 507 owners); a record counts as touched if any of its quotes fits a theme. The rest is long tail: fiction beats and scene rules (tiny-flowlab alone has 16 lines), patent-claim sentence forms, game dialogue trees, LaTeX preambles, and report fields that only make sense in one domain.

## 1. Top recurring themes (by distinct owners)

### T1. Follow the prescribed skeleton: a template file or a fixed section list, in the given order, with no sections added, dropped or reordered
Counts: 73 records / 72 repos / 71 owners. Concentration: prd-spec 27% (1.7x), report-analysis 27% (1.6x), project-docs 45% (0.8x). 52 of 73 records (71%) are single-type roles, against 54% overall. 35 records / 33 owners point to an external template, skill or file rather than listing the sections inline. 15 records demand completeness outright ("never skip", "all sections required", "no section is optional").
- "Do not add, remove, or reorder sections." (c01312)
- "Derive section headings and order from the skill templates — do not improvise structure" (c00994)
- "WHEN creating a report NEVER skip any section of the template." (c00937)

### T2. Lead with the point: answer, outcome, verdict or purpose first, detail after, no preamble
Includes BLUF, inverted pyramid, executive summary at the top, one-sentence purpose line, and "urgent items at the top".
Counts: 52 records / 49 repos / 48 owners. Concentration: project-docs 50% (0.9x), api-reference 38% (1.1x), report-analysis 23% (1.3x); highest lift academic 12% (3.1x) and prompt-instructions 8% (2.7x). It is spread across types, not type-bound. 8 owners phrase it as executive summary/BLUF/verdict.
- "Lead with the point — First sentence answers the reader's question" (c01549)
- "Lead with what matters most. The critical finding goes in the first paragraph, not buried on page 3." (c00340)
- "Lead with outcomes — "After this step, you'll have a running server" not "This section covers server setup"" (c00323)

### T3. Explain the why: rationale, design decisions, and the alternatives rejected, not just mechanics
Counts: 42 records / 41 repos / 40 owners. Concentration: project-docs 67% (1.2x), api-reference 43% (1.2x), changelog 24% (1.6x). Spread across types. Two sub-signals: 8 owners put why before how/what (c00338, c00400, c00402, c00710, c00755, c01054, c01256, c01436); 7 owners require the rejected alternatives or exclusions with reasons (c00137, c00388, c00420, c00444, c00547, c00605, c01201). One owner orders it the other way: "Lead with what, then how, then why" (c01481).
- "Document Why: Explain rationale, not just mechanics" (c00821)
- "Alternatives — ≥2 genuine options, no strawmen; each: what, why considered, why rejected." (c00547)
- "Capture decisions and the alternatives rejected. This is what stops a future reader from silently undoing the work." (c01201)

### T4. Cover failure paths: error responses, edge cases, troubleshooting, limitations, anti-patterns, not only the happy path
Counts: 38 records / 35 repos / 35 owners. Concentration: api-reference 71% (2.0x), changelog 34% (2.4x), code-comments 32% (3.1x), project-docs 71% (1.3x).
- "Show the failure paths. What the error looks like and what to do about it is usually the most-read part of any guide." (c01364)
- "Include both happy path and error scenarios in usage examples" (c00314)
- "The anti-pattern block is the most valuable part of the document. A code generator that has only seen correct examples will still emit plausible-looking wrong code" (c01132)

### T5. One home per fact: link to the owner instead of restating it elsewhere
Counts: 34 records / 34 repos / 33 owners. Concentration: project-docs 91% (1.7x), api-reference 50% (1.4x), changelog 29% (2.0x). 8 of 34 records (24%) are general-purpose roles, against 13% overall, the highest general share of any top theme. Several give the reason as drift.
- "Put each fact in exactly one place. If two documents would both plausibly own it, the more specific one wins and the other gets a pointer, not a copy." (c01091)
- "Link to peer docs instead of duplicating them. If two docs explain the same thing, one of them is wrong and both will drift." (c01132)
- "reference artifacts, do not duplicate them. If a paragraph repeats something that's already in a PRD, commit, or PR, replace it with the link." (c00237)

### T6. Requirements carry stable IDs and testable, observable acceptance criteria, traceable to tests and back
Counts: 34 records / 31 repos / 31 owners. Concentration: prd-spec 88% (5.4x). No general-purpose record.
- "Cada `R<n>` que escribes DEBE ser verificable por un test concreto. Si no lo es, parte el requirement o márcalo como blocker." (c00137) ("Every `R<n>` you write MUST be verifiable by a concrete test. If it is not, split the requirement or mark it as a blocker.")
- "Acceptance Criteria: Given/When/Then, IDs `AC-<linkedID>-<seq>`, each references at least one F-/API-/EVT-/DM-/NFR-" (c00172)
- "Every step's `expect` must name something a person or a browser can **observe**" (c01502)

### T7. Visuals: diagrams (mostly Mermaid), screenshots and figures, and where they go
Counts: 33 records / 32 repos / 30 owners. Concentration: project-docs 70% (1.3x), api-reference 39% (1.1x), report-analysis 18% (1.0x). Not type-bound. Internally split: Mermaid is named by 11 owners, and by my reading 6 owners mandate a diagram (c00113, c00182, c00465, c00729, c00788, c00967), while 4 restrict visuals to cases where prose fails (c00101, c00104, c00669, c00683).
- "Place diagrams immediately after introducing the concept they illustrate" (c01400)
- "Use a user journey diagram, scope boundary diagram, or both only when prose does not make a material flow or boundary clear." (c00683)
- "Todo gráfico lleva: título, unidades, fuente y timestamp de la data." (c00434) ("Every chart carries: title, units, source and the data's timestamp.")

### T8. README recipe: what it is, install, quick start, usage, configuration, contributing/license, with a quick start that works in minutes
Counts: 30 records / 30 repos / 30 owners. Concentration: project-docs 97% (1.8x), api-reference 60% (1.7x), code-comments 33% (3.3x). No single owner has more than one record. The section lists vary in detail but the order is nearly constant.
- "README: одно-двухстрочное «что это и зачем» → установка → быстрый старт (минимальный рабочий пример) → использование → конфигурация → ссылки/лицензия." (c01276) ("README: one or two lines on what it is and why → install → quick start (minimal working example) → usage → configuration → links/license.")
- "For READMEs you order sections by reader priority: pitch, quick-start, install, usage, reference link-out, contributing link-out, license." (c01263)
- "Write integration quickstart guides that walk a developer from zero to a successful API call in under five minutes" (c00118)

### T9. Progressive disclosure: overview or quick reference first, depth layered after, simple to complex
Counts: 27 records / 26 repos / 26 owners. Concentration: project-docs 74% (1.4x), api-reference 59% (1.7x). 12 of the 26 owners use the phrase "progressive disclosure" with no operational detail. The operational ones name the layers or a size target.
- "Quick reference at top, details below. Let users find their depth." (c00210)
- "Progressive disclosure: Start with the overview, then drill into details (simple → complex)." (c00505)
- "Progressive disclosure: SKILL.md is the entry point (<150 lines, <5,000 tokens target). Detailed content goes in supporting docs" (c01269)

### T10. One unit, one job: one idea per paragraph, one concept per section or page, one change per bullet; split rather than combine
Counts: 25 records / 25 repos / 25 owners. Concentration: project-docs 56% (1.0x), other 28% (3.6x), social-media 20% (7.1x), blog-article 20% (4.0x). Spread across types. Several pair it with cutting, not only splitting.
- "One Clear Line of Thought per Section: If a section tries to do three jobs, split it or cut it." (c00012)
- "One idea per paragraph: Each paragraph has a job. If it doesn't advance the argument, cut it." (c01441)
- "One change per bullet. Do not combine: "Added X and fixed Y" → two separate bullets." (c00345)

### T11. Reports: rank findings by severity or impact, and end with actionable next steps tied to findings
Counts: 27 records / 23 repos / 23 owners. Concentration: report-analysis 100% (5.7x). 25 of 27 records are single-type.
- "Include a clear "what to do next" section. A report without action items is just a complaint." (c00340)
- "Sort by score ascending (worst first) by default" (c01597)
- "Every remediation item must map to at least one finding." (c01464)

### T12. Procedures are numbered steps, one action each, with an expected result or a way to confirm success
Counts: 22 records / 22 repos / 22 owners. Concentration: project-docs 86% (1.6x), changelog 23% (1.6x). One owner says the opposite about list type: "bullet_lists_for_sequences" (c00884).
- "Write procedural steps as numbered lists where each step begins with an imperative verb, contains a single action, and states the expected result" (c00042)
- "Every setup or procedure section should end with a way to confirm success." (c00135)
- "Numbered steps for procedures — never bullet points for sequences; bullets imply unordered" (c00278)

### T13. Marketing and social copy follows named frameworks: hook, AIDA/PAS, headline → body → CTA, one CTA
Counts: 28 records / 22 repos / 22 owners. Concentration: marketing-copy 89% (11.2x), social-media 32% (11.5x), ux-microcopy 29% (7.2x). The most type-bound theme in the dimension.
- "One page, one goal, one CTA" (c00087)
- "Write a compelling hook (first 2 lines must trigger "see more" click)." (c00234)
- "PAS: Problem, Agitation, Solution." (c01547)

### T14. Every command, endpoint or concept gets a concrete example, complete enough to copy and run
Counts: 26 records / 21 repos / 21 owners. Concentration: api-reference 92% (2.6x), project-docs 85% (1.6x), code-comments 23% (2.3x).
- "Examples must be complete and runnable — no `...` or `// rest of code` shortcuts" (c01540)
- "Show a concrete, copy-pasteable example for every command." (c01100)
- "Include a copyable example for runnable claims and at least one end-to-end example where the target supports execution." (c00641)

### T15. Numeric size caps that force a split: max steps, items, lines, headings, sentences per paragraph
Counts: 22 records / 21 repos / 21 owners. Concentration: project-docs 73% (1.4x), blog-article 32% (6.3x), marketing-copy 23% (2.8x). The numbers disagree with each other (7 steps, 7±2 elements, 9 items, 200 lines, 12 KB, 5 H2s, 4 heading levels, 2–4 sentences), which reads as house convention rather than a shared finding. T15 ties with the changelog theme at 21 owners and 22 records; I placed it above the cut because it is not type-bound.
- "Write procedures with no more than seven numbered steps" (c00839)
- "Split Strategy: When content exceeds 200 lines, split into multiple focused documents" (c01369)
- "Count bullet lists: max 3 per page; collapse the rest into prose or tables" (c00197)

Just below the cut, by owners:
- Changelogs grouped by change type, breaking changes first or prominent with a migration path, entries written for users rather than as a commit list. 22 records / 21 repos / 21 owners; changelog 77% (5.3x).
- Heading conventions: one H1, no skipped levels, sentence case, depth caps. 22 records / 22 repos / 20 owners.
- Cross-link related docs: See Also and Next Steps sections, links back to the README, every page registered in the index. 21 records / 20 repos / 20 owners.
- No filler: no empty or boilerplate sections, no placeholders, no preamble, structure only where it earns its place. 19 records / 18 repos / 18 owners; prompt-instructions 16% (5.6x).
- Scannable formatting: headers, bullets, tables, short paragraphs, no wall of text. 15 records / 15 owners. A counter-signal of 6 owners says prose over lists where the items are not parallel (c00197, c00448, c00726, c01028, c01103, c01335).
- When editing, preserve the existing structure, headings, anchors and frontmatter, and match neighbouring docs. 15 records / 15 owners.
- Example or code first, prose after. 14 records / 14 owners; api-reference 71% (2.0x).
- Diátaxis: one doc type per page, never mix modes. 15 records / 15 repos / 14 owners.
- Table of contents past a length threshold. 13 records / 13 owners. The thresholds are more than 5 sections, 3+ sections, about 300 words, about 400 words, 1 page, and 300 lines.
- Organize by the reader's task, not the code's structure. 17 records / 13 repos / 13 owners.
- Last-updated or freshness timestamps. 14 records / 9 repos / 9 owners (see lineage).

Unions that matter for the proposal:
- Cutting and splitting (T5 + T10 + T15 + no filler): 95 records / 89 owners.
- Reader-first ordering (T2 + T9 + example-first + reader's-task organization): 101 records / 89 owners.
- Fixed skeleton or preserve existing structure (T1 + preserve): 86 records / 84 owners.
- Linking, de-duplication or cross-linking (T5 + cross-link): 53 records / 50 owners.

## 2. Lineage warnings

- **Freshness timestamps.** affaan-m has 6 of the 14 records (c00470, c00473, c00476, c00478, c00480, c00482), the same line in Spanish, Japanese, Korean, Portuguese, Turkish and Chinese. 0xb7a7dd61 (c00199) and Dach-Coin (c01131) carry the same English line word for word, "Freshness Timestamps - Always include last updated date". That is one doc-updater template family across 3 of the 9 owners, so about 7 independent voices. c00002 (darrenhinde, "Version/date stamps where required") is merged across 84 repos, so the theme's reach is mostly one file.
- **Reader's task, not code structure.** UitbreidenOS has 5 of the 17 records (c01411–c01415), one sentence in German, English, Spanish, French and Dutch: "Sidebar navigation must reflect this structure, not the codebase structure." The owner count (13) is correct; the record count is inflated by 4.
- **T13 Marketing.** UitbreidenOS again has 4 records (c01416–c01419), one CTA line in four languages, so 28 records are 22 owners. c00007 (mrgoonie, "Write in Layers…") is merged across 38 repos and counts in both T13 and T9.
- **T2 Lead with the point, and T3 Why.** c00004 (monoes, merged across 54 repos) and c00131 (imMamdouhaboammar) carry the identical "5-second test" line from the widely copied "engineering-technical-writer" family. They are 2 owners but one voice in both themes. The same family's translations (c00068 liaoxinjie666, c00909 xuanbingbingo) carry "every document stands alone or links its prerequisite context". That is why a "self-contained docs" theme looked recurring; it is mostly this one family, and I left it out of the list.
- **T6 IDs/testable.** "Assign a unique requirement ID (e.g., US-001)…" in c00054 (iannuttall) reappears as "(e.g., GH-001)" in c00152 (github/awesome-copilot), and NicholasSpisak (c00754) carries other iannuttall-derived agents; the "maximum of 5 H2 sections" line in c00160/c00756 is identical. Treat these 3 owners as about 1–2 voices: 31 owners, about 29 independent. kcenon has 3 records that are one SDLC document suite.
- **T14 Runnable examples and T4 Failure paths.** ruvnet has 3 records (c00027, c00148, c00149) that repeat one claude-flow API-docs agent, and Ashhad1200 (c00106) repeats its "Group endpoints logically with tags". Spielewoy's c00641 and c00643 are the same line. prmichaelsen has 3 records in T14. In T14, 26 records reduce to 21 owners and about 20 voices.
- **TOC.** "Include (a) table of contents for longer documents" is word for word the same in CPS-IT (c00380), ammarion (c00877) and SoundDocs (c01095). Dao-AILab (c00029) and CalaW (c00100) share the identical "Link to existing files instead of duplicating content", which inflates both T5 and TOC by 1.
- **Scannable.** zereight (c00085) and Yeachan-Heo (c00508) carry the identical "Wall of text: Dense paragraphs without structure…" line: one voice.
- **Diátaxis.** github (c00158) and kubestellar (c01197) have the identical heading "Structure (Diátaxis-inspired)"; GulajavaMinistudio has 2 records. That is 14 owners and about 13 voices.
- **Headings.** c00003 (github/awesome-copilot, Title Case/Sentence case) is merged across 72 repos; iannuttall and NicholasSpisak are identical (above); Hack23 has 2 records.
- **High-reach single records.** Owner counts are unaffected, but these records are copies of one file: c00001 (cyberpapiii, page-title rules, 99 repos, in T15), c00011 (SuperClaude "Structure content for scanning and task completion", 27 repos), c00012 (CarlosCaPe "One Clear Line of Thought per Section", 27 repos), c00010 (mrgoonie "Examples First", 32 repos), and c00016 (github TOC over 5 sections, 20 repos).
- **Within-owner multiplicity.** prmichaelsen has the most lines in the dimension (29, all API/project docs for one codebase), tiny-flowlab has 16 (fiction), and tractorjuice/arc-kit has 3 records in T11 (report rendering order). Each is a single voice.
- T1, T5, T8, T10 and T12 have no owner with more than 2 records and no cross-owner identical wording that I found. Their owner counts are close to their independent-voice counts.

## 3. Sharp but rare (1–2 owners, precise, adoptable by a general writer)

1. "新出のコマンド・ファイル・環境変数・用語は「定義・生成者・消費者」を同時に書く。「後述」「別途定義」のまま宙に浮いた参照を残さない" (c00935, skanehira, project-docs/prd) ("When a command, file, env var or term first appears, write its definition, producer and consumer together. Leave no dangling 'see below' / 'defined elsewhere' references.") The same record adds a dated list of "external facts relied on". This is a structural test for traceability that a general writer could run on any doc.
2. "Separate observed facts, calculated values, and interpretation." (c00652, hoangsonww, report) This is the proposal's point 2 as a layout rule. Looser relatives exist: observe/interpret/hypothesize in c00043, "clearly separate current behavior from future work or recommendations" in c01461, and a current/target/experiment banner in c01122. Only this record names the three layers.
3. "Every claim must carry a confidence label (DATA_SUPPORTED, CORRELATION, or HYPOTHESIZED)." (c00908, xinzhuwang-wxz, academic/report) frenzymath has the same move with a larger vocabulary: "Use the truth vocabulary in the problem statement: PROVED, CONDITIONAL, COMPUTATIONAL, ARCHIVE CLAIM, REFUTED, SUPERSEDED, and OPEN." (c00707)
4. "Uncertainty goes in the document's Open questions section, never in the fact tables." (c00784, shm11C3, prd-spec) A placement rule that keeps interpretation out of the factual core.
5. "改后全文、对照表、开放问题三块分清" (c01627, HeiGeAi, blog/other) ("Keep the revised full text, the comparison table, and the open questions as three separate blocks.") The deliverable is kept apart from the change ledger and the unresolved items, which is close to the proposal's file-plus-ledger return.
6. "List the adjacent films, superseded briefs and neighbouring deliveries a reader could mistake for evidence, and why each is excluded." (c00420, deccanai-org, report) With "List HOLD findings as leads; summarize SKIP/rejected with their roadblock so effort is auditable." (c00212, deonmenezes). Both are an explicit exclusions ledger.
7. "Return compact evidence-backed content, evidence gaps, and a parent action of `accept`, `decide`, or `reroute`." (c00403, YuChia-Wei, report) A defined return shape for the caller, separate from the content.
8. "every H2/H3 section opens with a 1–3 sentence direct answer to the question the heading poses" (c00058, josipjelic) This turns "lead with the point" into a rule that can be checked per section.
9. "Group related findings into themes. Ten individual bugs in auth are really one story: "authentication needs hardening."" (c00340, tmcleod3) With "Discuss correlated findings as logical units -- do not individually repeat each finding's narrative when they are part of the same correlation group" (c00925, davidmatousek). A merge unit for combining many inputs.
10. "Context — a `**Load this when:**` line stating concrete triggers, not a topic. "Load this when adding navigation to more than two screens" beats "This document covers navigation."" (c01132, Nagarjuna2997) This fits the proposal's path-scoped rule files and any doc written for an agent reader.

## 4. Bearing on the PROPOSED WRITER

**Differences between doc types live outside the role.** Supported, with a caveat.
- The largest theme, T1 (71 owners), is structure imposed per doc type. It lives mostly in single-type roles (71% of its records against 54% overall). In 33 owners it already works as a pointer to an external template, skill or repo file ("Follow `templates/report-template.md` exactly.", c01026). That is the proposal's mechanism: the brief or a rule file carries the skeleton.
- The type-bound themes have high lift and belong in rule files: requirement IDs (prd-spec 5.4x), report ranking and actions (5.7x), changelog shape (5.3x), marketing frameworks (11.2x), and the README recipe (project-docs 97%).
- The themes that cut across types have lift near 1: lead with the point, why, one idea per unit, visuals and one home per fact. These are the candidates for the role's core.
- Caveat: the corpus shows where authors put structure rules, not that a general role fails without them. It neither confirms nor refutes the "split only when runs fail" rule.

**Point 1, start from the reader.** Supported in form; the instructions are mostly positional.
- Support: the reader-first ordering union has 89 owners (T2, T9, example-first, reader's-task organization).
- Most of these instructions say what to put first. Few ask what the reader will do. Exceptions: "Write for the reader's task, not the writer's source structure; topic-based authoring beats document-based." (c00360), "Purpose: What question does this doc answer?" (c01621), and the "Load this when" trigger line (c01132).
- The corpus disagrees on what comes first: why first (8 owners), code or example first (14 owners), what → how → why (c01481), and answer or verdict first (T2). My reading is that a reader-first rule settles this only if it says the order follows what the reader will do: task docs lead with the runnable example, decision docs with the conclusion, explanations with the why. The corpus does not state this rule; it is my inference.
- Contradicting signals: T1's fixed skeletons put structure before the reader. A few roles mirror the code tree in navigation ("Instruction files mirror the `/src` folder structure for easy navigation.", c00999; c00834; the feature-local docs line in c00052/c01244). Against them, 13 owners say to organize by task and not by codebase.

**Point 2, every factual sentence traceable; interpretation marked.** Traceability has support; marking interpretation has little.
- In this dimension traceability takes structural forms:
  - requirement → test chains (T6, 31 owners);
  - remediation → finding (c01464);
  - a pointer to the owning source instead of a restatement (T5, 33 owners), which is traceability between documents;
  - kept rationale and rejected alternatives (T3).
- Marking interpretation is rare: c00652, c00908, c00707, c00784, c00867 ("Mark estimates as estimates"), c00434 (real vs projected lines), c00043, c01461 and c01122, about 9 owners with no shared wording. The proposal is not contradicted, but the corpus shows it is uncommon practice. Items 1–4 of section 3 are concrete devices the role could adopt: per-claim labels, an Open questions section, fact/calc/interpretation separation, and definition/producer/consumer for new terms.

**Point 3, cutting is the default; working notes go to a separate output.** Cutting is supported; completeness mandates conflict with it; there is almost no evidence on separate output.
- Support: the cutting union has 89 owners. T5 cuts across documents, T10 says "split it or cut it", T15 sets caps, and the no-filler theme (18 owners) is the strongest direct support: "Every section must exist because the product needs it. Remove template filler." (c00504), and "no "Overview" sections that restate the title, no "In this document you will find..." introductions" (c00655).
- Contradiction: completeness mandates in T1 and elsewhere, such as "WHEN creating a report NEVER skip any section of the template." (c00937), "All 15 sections required" (c00967), "Keep it exhaustive — Every feature needs: happy path, error paths, edge cases, validation, out-of-scope" (c00436), and "Nunca remover conteúdo bom" ("never remove good content") (c00215). The corpus's own reconciliation: keep the section but do not pad it. "Use `N/A` only when a section is truly not applicable." (c00361) and "no state exists only to fill the template" (c00684). The proposal needs this distinction whenever the caller supplies a template.
- Tension with T3: 7 owners require the rejected alternatives and exclusion reasons inside the deliverable (ADRs, decision docs, reports). "Working notes go elsewhere" must therefore separate process notes (how the writer got there) from rationale the reader needs (why this and not that). Without that line, the role will strip content that decision documents require.
- Separate output for the caller has only a few voices: c01627 (three separate blocks), c00403 (return shape with evidence gaps and a parent action), and "The handoff itself stays short — the artifacts carry the detail." (c00523). It is not contradicted, but it rests on little evidence from this corpus.

**Combining drafts into claims with a ledger.** Nothing in this dimension talks about merging drafts or about evidence tiers. The nearest material:
- the T5 tie-break "the more specific one wins and the other gets a pointer" (c01091), a rule for which source keeps a claim;
- grouping correlated findings into one unit (c00340, c00925) and "summarize into themes rather than enumerating each commit" (c00062), rules for the unit of combination;
- exclusion ledgers with reasons (c00420, c00212, c00605), the closest thing to the proposal's claim → source ledger.
"Does not judge its own output" has no bearing here.

**What this dimension has that the proposal lacks.**
1. Editing, not only writing. Preserve existing headings, anchors, section order and frontmatter unless restructuring is asked (15 owners), and keep the TOC, index and anchors in sync after a change (c00711, c00830, c01219, c00175). The proposal says nothing about edits to an existing document.
2. What to do with a supplied template. Follow it exactly, fill every slot from evidence, write N/A only when true, and never leave placeholders ("Nunca deixe placeholder como `<TODO>` ou `...`" ("never leave a placeholder like `<TODO>` or `...`"), c01345; "Render only as many bullet lines as there are entries; delete any leftover `[KEY_FINDINGS_n]` bullet lines that have no entry.", c00612). T1 is the biggest theme; the role needs one line on how it treats a skeleton from the brief.
3. Cutting across documents. "One home per fact, link instead of restating" (T5, 33 owners, the most general-purpose of the top themes) is a cutting rule the proposal's within-document "cut by default" does not cover.
4. Instructions the reader can verify. For how-to content, each step states its expected result or a success check (T12, 22 owners). This is point 2's counterpart for instructions: the reader can check the document against reality.
5. Failure paths as required content (T4, 35 owners). The cutting default could remove them unless the role marks them as the most-read part.
6. Identifying the doc type before writing. The Diátaxis owners say "Every artifact occupies exactly one quadrant. Decide before writing." (c01106). If type differences come from path-scoped rules, a new file or an unusual path may load none, so the role needs a step that names the doc type and mode, or it must ask the caller.
7. Numeric caps (TOC thresholds, step limits, split-at-N-lines). They recur (T15, TOC) but the numbers disagree, which argues for leaving them to rule files, not the role.

## Appendix: record ids per theme (for reproducing counts)

- `lead_with_point`: c00004, c00023, c00025, c00036, c00042, c00058, c00087, c00088, c00101, c00122, c00131, c00182, c00268, c00323, c00340, c00402, c00446, c00467, c00549, c00601, c00610, c00650, c00671, c00708, c00710, c00733, c00752, c00770, c00816, c00817, c00833, c00927, c00946, c00972, c01017, c01023, c01068, c01135, c01175, c01184, c01214, c01223, c01229, c01233, c01273, c01318, c01435, c01436, c01549, c01561, c01577, c01578
- `fixed_skeleton`: c00026, c00092, c00109, c00136, c00145, c00173, c00200, c00222, c00237, c00246, c00284, c00294, c00297, c00298, c00322, c00325, c00361, c00376, c00388, c00420, c00423, c00521, c00543, c00592, c00648, c00654, c00674, c00690, c00708, c00712, c00716, c00758, c00762, c00767, c00816, c00868, c00873, c00898, c00908, c00937, c00941, c00944, c00950, c00955, c00967, c00982, c00994, c00998, c01001, c01002, c01005, c01018, c01026, c01057, c01072, c01081, c01086, c01143, c01159, c01242, c01280, c01312, c01337, c01422, c01424, c01574, c01580, c01582, c01583, c01587, c01597, c01601, c01602
- `preserve_existing`: c00026, c00193, c00592, c00636, c00655, c00672, c00711, c00802, c00830, c01015, c01092, c01380, c01569, c01584, c01610
- `no_filler`: c00077, c00101, c00104, c00361, c00389, c00504, c00655, c00669, c00683, c00684, c00686, c00819, c01015, c01227, c01345, c01435, c01437, c01445, c01538
- `link_not_dup`: c00029, c00100, c00105, c00183, c00210, c00213, c00237, c00242, c00369, c00399, c00443, c00467, c00725, c00884, c00886, c00964, c01081, c01091, c01103, c01106, c01127, c01128, c01132, c01161, c01218, c01219, c01276, c01317, c01364, c01431, c01438, c01484, c01537, c01550
- `crosslink_nav`: c00175, c00219, c00268, c00339, c00463, c00802, c00857, c00861, c00868, c00888, c00982, c01016, c01081, c01107, c01159, c01219, c01302, c01329, c01342, c01351, c01613
- `reader_task_org`: c00011, c00037, c00051, c00130, c00200, c00360, c00389, c00892, c01046, c01052, c01263, c01318, c01411, c01412, c01413, c01414, c01415
- `examples_first`: c00010, c00265, c00310, c00509, c00601, c00686, c00921, c01072, c01106, c01127, c01136, c01257, c01335, c01375
- `progressive`: c00007, c00117, c00122, c00130, c00146, c00210, c00265, c00391, c00499, c00505, c00549, c00725, c00755, c00868, c00948, c00975, c01052, c01054, c01137, c01218, c01257, c01269, c01358, c01369, c01375, c01559, c01567
- `one_idea_unit`: c00012, c00029, c00087, c00131, c00181, c00215, c00260, c00345, c00352, c00353, c00487, c00524, c00670, c01062, c01281, c01304, c01434, c01441, c01442, c01467, c01481, c01540, c01549, c01555, c01615
- `diataxis`: c00158, c00181, c00296, c00397, c00452, c00515, c00751, c00972, c00980, c00992, c01072, c01106, c01197, c01442, c01471
- `size_caps`: c00001, c00081, c00160, c00173, c00183, c00197, c00265, c00279, c00309, c00346, c00756, c00824, c00839, c00921, c01062, c01269, c01279, c01281, c01369, c01462, c01538, c01563
- `scannable`: c00011, c00033, c00081, c00085, c00417, c00508, c00694, c00717, c00723, c00772, c01038, c01062, c01142, c01342, c01462
- `prose_over_lists`: c00197, c00448, c00726, c01028, c01103, c01335
- `headings`: c00003, c00033, c00070, c00160, c00221, c00309, c00357, c00384, c00419, c00597, c00684, c00756, c00811, c00812, c00824, c00884, c00888, c01251, c01274, c01279, c01315, c01446
- `toc`: c00016, c00029, c00219, c00262, c00380, c00515, c00711, c00830, c00877, c01095, c01246, c01467, c01574
- `why_rationale`: c00004, c00025, c00070, c00104, c00131, c00135, c00137, c00164, c00213, c00313, c00338, c00352, c00388, c00400, c00402, c00420, c00444, c00547, c00605, c00610, c00710, c00755, c00762, c00807, c00810, c00821, c00885, c01023, c01054, c01128, c01201, c01206, c01223, c01256, c01276, c01436, c01465, c01468, c01481, c01559, c01580, c01585
- `steps_verify`: c00029, c00042, c00048, c00077, c00104, c00123, c00135, c00190, c00246, c00278, c00279, c00339, c00441, c00788, c00839, c00884, c00937, c01142, c01225, c01424, c01447, c01613
- `errors_edges`: c00023, c00027, c00037, c00077, c00140, c00148, c00149, c00244, c00282, c00288, c00314, c00339, c00348, c00374, c00426, c00435, c00436, c00601, c00650, c00762, c00788, c00800, c00841, c00843, c00885, c00946, c00952, c01093, c01132, c01225, c01256, c01303, c01364, c01425, c01564, c01576, c01581, c01623
- `ids_testable`: c00054, c00111, c00113, c00137, c00152, c00172, c00253, c00343, c00371, c00378, c00443, c00466, c00468, c00581, c00588, c00629, c00684, c00754, c00788, c00879, c01002, c01063, c01108, c01159, c01161, c01163, c01182, c01232, c01277, c01385, c01464, c01492, c01502, c01582
- `visuals`: c00082, c00101, c00104, c00113, c00163, c00182, c00190, c00206, c00224, c00268, c00384, c00434, c00441, c00460, c00465, c00661, c00669, c00683, c00686, c00729, c00788, c00847, c00878, c00905, c00906, c00908, c00967, c00985, c01103, c01400, c01438, c01480, c01484
- `report_rank_act`: c00039, c00182, c00190, c00212, c00267, c00340, c00355, c00403, c00610, c00611, c00612, c00652, c00735, c00926, c00949, c01026, c01060, c01125, c01287, c01292, c01354, c01426, c01464, c01465, c01573, c01597, c01601
- `changelog`: c00062, c00164, c00285, c00321, c00345, c00352, c00383, c00487, c00514, c00624, c00663, c00749, c00758, c00844, c00848, c00900, c00954, c00992, c01145, c01193, c01472, c01607
- `readme_recipe`: c00035, c00050, c00118, c00173, c00200, c00206, c00282, c00298, c00348, c00542, c00664, c00946, c00952, c01019, c01022, c01048, c01052, c01177, c01210, c01222, c01227, c01263, c01271, c01276, c01396, c01570, c01576, c01583, c01592, c01602
- `runnable_examples`: c00027, c00117, c00121, c00148, c00149, c00312, c00337, c00374, c00391, c00641, c00643, c00650, c00840, c00841, c00842, c00855, c00953, c00994, c01038, c01100, c01127, c01210, c01225, c01271, c01540, c01555
- `marketing_frameworks`: c00007, c00032, c00053, c00073, c00081, c00087, c00165, c00178, c00234, c00276, c00334, c00353, c00394, c00417, c00455, c00595, c00948, c01084, c01260, c01394, c01416, c01417, c01418, c01419, c01466, c01547, c01561, c01562
- `freshness`: c00002, c00109, c00199, c00465, c00470, c00473, c00476, c00478, c00480, c00482, c00745, c00917, c01131, c01202
