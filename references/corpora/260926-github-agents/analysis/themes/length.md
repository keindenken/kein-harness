# Length dimension: recurring themes

Source: `claims/length.jsonl`, 389 quotes from 326 distinct records, 278 repos, 266 owners (owner = the repo part before `/`).

## Method

- I read all 389 lines. Nothing was sampled.
- I assigned each line to zero or more themes by hand, by line index. The assignment is in `analysis/themes/length.assign.json`: keys are theme codes, values are 0-based line indices into `length.jsonl`. A script computed every count from that assignment. 384 lines went into at least one theme. 5 went into none: a sentence fragment (c00812), "Write walls of text" with no context (c01480), and three one-offs (c00861, c00904, c01169).
- A line can belong to several themes. For example, "Never pad. A doc is long because the surface area is large..." counts toward both the no-padding theme and the length-follows-need theme.
- Counts are distinct records / distinct repos / distinct owners. "Voices" is the owner count after collapsing template families: cross-owner quotes that are verbatim or near-verbatim (string similarity >= 0.75, checked by hand) or that are direct translations of each other. Family collapse only merges owners; it never adds any.
- Doc-type concentration: the most frequent types, plus lift. Lift is the type's share among the theme's records divided by its share among all 1,089 writing roles (from `stats.txt`). It is shown only for types with 3 or more records in the theme. Records carry several doc types, so the raw type counts add up to more than the record count.
- There was one coder and no second rater. Theme edges are judgment calls, especially between the three "cut" themes (generic concision, the deletion test, and edit-down passes). The ordering by owner count holds up better than the exact numbers.
- The `specificity` rating was not used. Every quote in `claims/` has already passed the specificity filter.

## 1. Top recurring themes (ordered by distinct owners)

### 1. Be concise; essential information only (no number given)
An unquantified instruction to be brief, direct, and limited to what is needed.
- Counts: 46 records / 45 repos / 45 owners (43 voices)
- Doc types: project-docs 32, api-reference 16, other 9, report-analysis 7. It is spread across types. The only lift above 1.5x is "other" (2.2x).
- "Be direct and concise; avoid unnecessary examples unless they clarify significantly different use cases" (c00029)
- "Conciseness: Documentation must be brief and to the point, never exceeding what's essential" (c00219)
- "Keep it concise - Long ADRs don't get read" (c01348)

### 2. Cut any sentence that does not earn its place; never pad
Keep a sentence only if it helps the reader do or understand something. Remove filler, preamble and hedges, and never pad to reach a length. This theme merges the deletion test (26 owners) with no-padding (13 owners).
- Counts: 34 records / 34 repos / 34 owners (30 voices)
- Doc types: project-docs 19, api-reference 12, marketing-copy 7, code-comments 6. Lift: prompt-instructions 3.4x, ux-microcopy 3.1x, blog-article 2.3x.
- "Cut ruthlessly: If a sentence doesn't help the reader do something or understand something, delete it" (c00004)
- "Cut hedges, filler, and restated context. If a sentence survives deletion without the doc losing meaning, delete it." (c01103)
- "Never pad content to hit a word count; every paragraph must carry weight" (c01229)

### 3. Hard character or word caps on short fields (platform and SEO limits, headlines, CTAs)
Tweets, meta titles and descriptions, ad fields, subject lines, headlines, CTAs and alt text each get a fixed cap, usually taken from an external platform limit. This theme merges platform character limits (18 owners) with headline and CTA word caps (10 owners).
- Counts: 29 records / 27 repos / 26 owners (26 voices)
- Doc types: marketing-copy 20, ux-microcopy 10, social-media 9, blog-article 7. Lift: social-media 11.3x, ux-microcopy 9.2x, marketing-copy 7.6x. This theme is the most type-bound in the dimension.
- "Meta description: 150–160 characters. Include the primary keyword naturally." (c00058)
- "headline ≤ 40 chars, primaryText ≤ 250 chars, description ≤ 30 chars, callToActionType do enum Meta" (c00332)
- "Headlines: max 8 words. Subheadlines: max 20 words" (c00353)

### 4. Cap sentence length (usually 15 to 25 words)
A per-sentence maximum or average, stated in words, or in characters for CJK text.
- Counts: 29 records / 25 repos / 25 owners (23 voices)
- Doc types: project-docs 20, api-reference 15, prd-spec 6, changelog 5. Lift is modest: blog-article 2.0x, marketing-copy and prd-spec 1.5x.
- The stated numbers disagree: 8-12 words (c00107), 11 words (c00417), 15 (c00173), 15-20 (c00281, c00839), 20 (c01070), 25 (c00357, c00811), and "roughly 40" (c01164).
- "Target maximum 20-25 words per sentence" (c00159)
- "Frases cortas. Objetivo: ≤25 palabras de media. Larga puntual: bien. Larga sistemática: mal." (c00201). In English: "Short sentences. Target an average of ≤25 words. An occasional long one is fine; systematically long ones are not."
- "Split sentences past roughly 40 words, or past two independent clauses plus a subordinate one." (c01164)

### 5. Cap paragraph length (usually 2 to 5 sentences or lines)
A maximum per paragraph or text chunk.
- Counts: 25 records / 25 repos / 25 owners (23 voices)
- Doc types: project-docs 18, api-reference 14, blog-article 6, marketing-copy 5. Lift: blog-article 4.7x, marketing-copy 2.2x.
- The numbers vary from owner to owner: 2 sentences (c00001), 2-3 (c00151), 3-4 (c00402), 3-5 (c00239), 4 lines (c00135), 40-80 words (c00835).
- "Chunks of text should not be more than 2 sentences long" (c00001)
- "Keep paragraphs short — 3-5 sentences maximum" (c00239)
- "모든 단락은 1~3문장. 4문장 이상 단락은 즉시 분리." (c01084). In English: "Every paragraph is 1-3 sentences. Split any paragraph of 4 or more sentences immediately."

### 6. Cap a named unit (summary, overview, description, abstract, entry)
One component of the document gets a sentence or word budget, even when the whole document does not.
- Counts: 29 records / 25 repos / 23 owners (23 voices)
- Doc types: report-analysis 13, project-docs 7, prd-spec 6, changelog 4. Lift: report-analysis 2.9x, prd-spec 1.5x.
- "Write the executive summary as a 3–5 sentence narrative covering the most critical findings, skills assessed, total checks, and verification outcomes" (c00086)
- "Each endpoint description must be one sentence under 30 words." (c00717)
- "Overview: One paragraph. State what and why." (c00294)

### 7. Cap total document size (lines, words, pages, screens, KB)
The whole file or report gets a maximum size: README under 200 lines, codemap under 500 lines, report under 600 words. This theme merges doc and file caps (18 owners) with report caps (9 owners).
- Counts: 33 records / 23 repos / 23 owners (19 voices)
- Doc types: project-docs 22, api-reference 17, report-analysis 11. Lift: report-analysis 2.2x.
- "README.md is the front door and stays under 200 lines" (c00752)
- "Short: under 600 words. Triagers skim." (c00036)
- "NEVER create long documentation files (max 3-4 screens of content)" (c00219)

### 8. Counter-theme: completeness or need sets the length, not brevity
Either brevity is explicitly subordinated to completeness or clarity, or length is said to follow the content's surface area or risk rather than a fixed cap. This theme merges completeness-over-brevity (13 owners) with length-follows-need (11 owners).
- Counts: 22 records / 22 repos / 22 owners (22 voices)
- Doc types: project-docs 11, api-reference 10, code-comments 6, report-analysis 4. Lift: code-comments 2.3x. The strongest individual cases are PRDs (c00286, c00754), mathematical reports (c00707) and business-logic comments (c01222).
- "Prioritize clarity over brevity - PRDs should be comprehensive" (c00286)
- "Do not optimize for brevity and do not impose an executive-summary length cap: use as many pages as the complete definitions, proofs, route explanations, and failure analyses require." (c00707)
- "Never pad. A doc is long because the surface area is large, not because you restated the intro three times." (c01132)

### 9. Measure length in reader time or the reader's attention
Length is set by how long the reader has: "understood in 30 seconds", "running in 5 minutes", "readable in 2 minutes". It is also justified that way: "developers are busy", "triagers skim". This theme merges the stated rationale (13 owners) with time-to-value targets (11 owners).
- Counts: 22 records / 22 repos / 22 owners (22 voices)
- Doc types: project-docs 14, api-reference 11, changelog 7, report-analysis 6. Lift: changelog 2.3x, report-analysis 1.8x.
- "If it can't be understood in <30 seconds, it's too long." (c00002)
- "README should guide a user from zero to running in 2-5 minutes." (c00282)
- "keep the demo doc tight (under 200 lines). A PO reviewing a chain landing has minutes, not hours." (c00401)

### 10. Budget agent-instruction files because they load into context
CLAUDE.md, SKILL.md, prompts and tool descriptions get line or token caps, and the rationale is context cost, not reader patience.
- Counts: 22 records / 21 repos / 21 owners (20 voices)
- Doc types: project-docs 16, prompt-instructions 8, code-comments 5. Lift: prompt-instructions 14.1x, the highest single-type lift in the dimension.
- "Length is a cost — every line you add is loaded on every invocation." (c01218)
- "Keep SKILL.md <500 tokens; overflow → references/" (c00356)
- "Budget ~100 tokens per tool description — tool descriptions compete for context window space" (c00088)

### 11. Say it once: no duplication, link to the source of truth
Remove restatement and duplicate entries, and point to the single canonical place instead.
- Counts: 17 records / 17 repos / 17 owners (17 voices)
- Doc types: project-docs 12, api-reference 6, changelog 3. No notable lift.
- "Eliminate redundancy: Say it once, say it well, link to it everywhere else" (c00065)
- "Keep prose tight — if a diagram covers the concept, the surrounding text must orient the reader and highlight key points, not re-describe the diagram in words" (c00375)
- "重复信息红线：同一论点出现 3 次以上，留最强的一次" (c01627). In English: "Red line on repetition: if the same point appears 3 or more times, keep only the strongest instance."

### 12. Cap the number of items (bullets, recommendations, steps, slides, questions)
A count limit that forces the writer to choose.
- Counts: 16 records / 15 repos / 15 owners (15 voices)
- Doc types: project-docs 6, report-analysis 5, api-reference 4. Lift: report-analysis 2.0x.
- "3-5 skills, hard cap. If you find yourself listing more, you haven't picked. Choose." (c00237)
- "建议数量：每周建议不超过 5 条，避免信息过载" (c00790). In English: "Number of recommendations: no more than 5 per week, to avoid information overload."
- "Troubleshooting (top 3 issues only)" (c01395)

### 13. Prefer examples over prose, and keep examples minimal
Show rather than explain, but keep each example short: one example, a few lines, runnable.
- Counts: 15 records / 15 repos / 15 owners (14 voices)
- Doc types: project-docs 14, api-reference 8, code-comments 5. Lift: code-comments 2.8x.
- "One clear example beats three variations" (c00698)
- "Never include code blocks longer than 5 lines." (c01216)
- "Exemplos Primeiro: Priorize exemplos práticos sobre explicações longas" (c00289). In English: "Examples first: prioritize practical examples over long explanations."

### 14. Target word ranges for long-form pieces
Blog posts, pillar content, chapters, papers and profiles get a band such as 800-1500 words.
- Counts: 15 records / 14 repos / 14 owners (13 voices)
- Doc types: marketing-copy 7, blog-article 6, report-analysis 3, fiction-narrative 3. Lift: blog-article 7.8x, marketing-copy 5.1x, fiction-narrative 5.0x.
- "Length: 800-1500 words. Enough to explain, not enough to bore." (c00509)
- "Word count within mode limits (full: 3000-8000, quick: 500-1500)" (c00041)
- "生成 3000-5000 字正文，保证前段有吸引力，结尾留钩子。" (c01138). In English: "Generate a 3,000-5,000 character body; make the opening compelling and end on a hook."

### 15. When a document grows, split it or move detail elsewhere
Overflow goes to `references/`, `docs/`, a design doc or code comments, or the document is split into several files.
- Counts: 14 records / 14 repos / 14 owners (14 voices)
- Doc types: project-docs 9, prd-spec 3, prompt-instructions 3. Lift: prompt-instructions 8.3x.
- "500줄 이내. 길어지면 `references/`로 분리하고 SKILL.md에서 포인터." (c00461). In English: "Under 500 lines. If it grows longer, split it into `references/` and point to it from SKILL.md."
- "Non-bloat — if a section grows, something else must shrink. Total documentation size trends flat or down." (c00242)
- "One capability, one spec file. ... If the file exceeds 500 lines, the capability is probably too broad — split it." (c00469)

Just below the top 15, by owners:
- Skip the obvious and document only the non-obvious: 11 records / 11 owners (c00310, c00827, c00753).
- Make the smallest edit when updating docs: 11 / 11. Examples: "Smallest diff. Do not rewrite surrounding prose." (c00976) and "Prefer precise updates over broad rewrites." (c01363). Every record in this theme except one carries project-docs.
- Run an explicit cutting pass: 11 / 11. Examples: "Second draft is for cutting 40% of the words." (c00087) and "Always edited down (more cuts than adds)" (c01405). Lift: ux-microcopy 9.7x.
- Cap line width in characters: 11 records / 10 owners / 9 voices.
- Hit a target length within a tolerance: 7 / 6.

## 2. Lineage warnings

- **ECC codemap family (theme 7, and 15 through c00469).** One owner, affaan-m, contributes 9 of the theme's 33 records. They are the same "keep codemaps under 500 lines" line in English, Spanish, Japanese, Korean, Portuguese, Turkish and two Chinese scripts (c00079, c00470-c00484). Three more owners carry the same line or a near copy: 0xb7a7dd61 (c00199), sangrokjung (c00661) and zekdevs (c01141). Theme 7's record count is inflated about 1.4x. On voices it drops from 23 owners to 19.
- **"Help the reader do something or understand something" family (theme 2).** monoes (c00004, 54 repo copies) and imMamdouhaboammar (c00131) have it verbatim. liaoxinjie666 (c00068) and xuanbingbingo (c00909) have Chinese translations. That is 4 owners and 1 voice. The best-known phrasing of the deletion test comes from one template.
- **"Every word must earn its tokens" (themes 2 and 10).** akiselev (c00132) and alfieprojectsdev (c00139) have it verbatim.
- **"Chunks of text should not be more than 2 sentences long" (theme 5).** cyberpapiii (c00001, 99 repo copies), EHESPO (c00107) and event-catalog (c00597, where it becomes "3 sentences") share it. The other paragraph-cap quotes use similar wording ("Keep paragraphs short (3-5 sentences)"), but their numbers differ from owner to owner. That looks like a convergent idiom, not copying, but it cannot be ruled out.
- **UitbreidenOS (theme 4).** 5 of the 29 sentence-cap records are one rule ("20 words max for procedural steps") in English, German, Spanish, French and Dutch (c01411-c01415). The theme's record count overstates it. Its owner count does not.
- **Smaller verbatim pairs.** Each of these counts as 2 owners but 1 voice:
  - Dao-AILab / CalaW: "Be direct and concise; avoid unnecessary examples..." (themes 1 and 13)
  - universetraveller / GovTechSG: "Be concise, specific, and value-dense" (theme 1)
  - github/gh-aw-firewall / deschutesdesigngroupllc: "Keep sentences under 25 words when possible" (theme 4)
  - jpantsjoha / accountex-org: "Average sentence length: < 20 words" (theme 4)
  - iannuttall / NicholasSpisak: "Maximum 300 words per section" (theme 14)
  - TheLobbi / jonlwowski012: README under 200 lines (theme 7)
  - Donchitos / bullish0x: the 120-character dialogue line, in the line-width theme
- **Copy counts, not owners, drive reach.** Four records account for most of the repo copies in their themes:
  - c00000: 130 copies, line width
  - c00001: 99 copies, paragraph cap
  - c00002: 84 copies, reader time
  - c00004: 54 copies, deletion test

  Weighting by `copies_in_repos` would move the line-width and reader-time themes to the top. That would reflect how widely a few templates spread, not how many independent authors wrote the rule.
- **Real external limits.** Theme 3's 150-160-character meta description appears across 6 owners (josipjelic, Caykhongg, davepoon, damnq030198, okrlinkhub, isac322). They converge because they share an external constraint, search-result truncation, not a common template.

## 3. Sharp but rare (1-2 owners, operational, adoptable by a writer role)

1. **The length cap is enforced by a mechanism, not by prose.** "It is OVERWRITTEN, never appended to, and stays under 150 lines. A hook (.claude/check_task_resume.ps1) fails the write when it goes over." (c01091)
2. **Measure length with a tool, match the brief, and do not pad with metadata.** "通过 generate_clean.py --stats 统计正文字符数，按简报长度调整，不用元数据或说明充字数" (c00715). In English: "Count the body's characters with `generate_clean.py --stats`, adjust to the length in the brief, and do not pad the count with metadata or explanations."
3. **Size budgets set before drafting.** "Apply pre-size budgets **before first write**: - `plan_summary` <= 600 chars - `architecture_notes` <= 400 chars" (c01553)
4. **The caller-facing return is separate from the deliverable and capped on its own.** "Format: Concise Markdown (under 200 words) - this is the command output, NOT the design document itself" (c00581). Also: "Keep output concise; reference file paths for details when needed" (c00453).
5. **Length is allotted by outcome.** "Compress failed approaches. A table row per method is enough. Save detail for what worked." (c01585)
6. **A default with named exits instead of a flat cap.** "Default ≤6 sentences or 5 bullets; exceed for requests/risk/complexity/completeness." (c01442)
7. **A conservation rule.** "Non-bloat — if a section grows, something else must shrink. Total documentation size trends flat or down." (c00242)
8. **A cap tied to the evidence that motivated it.** "Never more than one line; the file was restructured in Aug 2026 precisely because entries had grown to 600 words each." (c01193)
9. **Replace embedded code with pointers.** "DELETE: generic advice, inferable-from-code content, README material, code examples (replace code examples with file_path:line_number references)" (c00827)
10. **Stopping early is correct output.** "You do not produce documentation nobody asked for. A README that ends on section 3 because the project genuinely needs nothing more is correct output." (c01263)

Runner-up: the repetition threshold "同一论点出现 3 次以上，留最强的一次" (c01627), which means "if the same point appears 3 or more times, keep only the strongest instance".

## 4. Bearing on the PROPOSED WRITER

**Type differences carried outside the role.** This is supported, and strongly. Most numeric length rules are type-bound:
- Short-field caps concentrate in social, microcopy and marketing (7.6x to 11.3x lift).
- Long-form word ranges concentrate in blog, marketing and fiction (5x to 7.8x).
- Unit caps concentrate in reports (2.9x).
- Context budgets concentrate in prompt-instructions (14.1x).

Even inside one type the numbers disagree:
- Sentence caps run from 8-12 words (c00107) to about 40 (c01164).
- Paragraph caps run from 2 to 5 sentences.
- README caps run from 80-120 lines (c00495) to 1,000 (c01362).

No single number could live in a general role. The numbers belong in path-scoped rule files or in the brief. What does recur across types is the unquantified instruction: themes 1, 2 and 11 spread over nearly every doc type with little lift. That is the part a general role can hold.

**Point 1: start from the reader and what they will do.** Supported. Theme 9 (22 owners) measures length in reader time, and the most-copied phrasing of the deletion test defines "earns its place" as helping "the reader do something or understand something" (c00004 family). This dimension adds one thing: reader-time targets such as "zero to running in 2-5 minutes" (c00282) and "understood in <30 seconds" (c00002) give point 1 a checkable form. The proposal states the stance but not a measure.

**Point 2: every fact traceable to evidence.** This dimension barely touches it. The adjacent signals are:
- "Accuracy Over Volume: Correct information beats extensive coverage" (c00725)
- "A correct doc covering 80% beats a doc that's 100% but wrong on one line." (c01127)
- "Minimum content, bulleted, nothing speculative." (c00223)
- Code examples replaced by `file:line` references (c00827)
- An abstract that states "only measured results" when it has quantitative results (c01184)

These support treating unsupported content as the first thing to cut, which ties point 2 to point 3. No contradiction.

**Point 3: cutting is the default, and working notes go to a separate output.**
- *Cutting as default* is the dimension's center of gravity: themes 1, 2 and 11, plus the just-below themes on edit-down passes and skipping the obvious.
- *A contradiction to keep:* theme 8 (22 owners, 22 voices, no template family) explicitly overrides brevity for PRDs, proofs, business-logic comments and "no time or token budget" documentation (c01225). The proposal should state cutting as a default that the brief or path rule can override, as c01442 does ("exceed for requests/risk/complexity/completeness"). A flat rule would fail on those types.
- *The separate caller output* has direct but rare support: c00581, c00453, and c01553's budgets set before drafting. Nothing in the corpus contradicts it.

**Claim-level combining and the evidence-tier ledger.** The length dimension says nothing about combining drafts. One adjacent signal is theme 11: keep only the strongest instance of a repeated point (c01627), and link to one canonical place instead of restating (c00065, c01587). That is the same move as keeping one sourced claim instead of several restatements, so it is compatible.

**"It does not judge its own output."** This is compatible with the mechanism-enforced caps in c01091 and c00715. Length is one property a run or hook can check without the writer grading itself. It suggests the eval side, not the role, should hold the numeric length checks.

**What the proposal lacks in this dimension:**
1. **An update mode.** "Smallest diff; do not rewrite surrounding prose" (11 owners, almost all project-docs) says editing an existing document is not the same as writing one. The proposal treats every task as a fresh draft.
2. **Where overflow goes.** Theme 15 (14 owners) sends overflow to `references/`, `docs/` or a design doc, or splits the file. The proposal only routes working notes to the caller. It has no rule for deliverable content that is true and useful but too long for this file.
3. **Length as context cost for prompt deliverables.** Theme 10 (21 owners, 14x prompt lift) justifies length by load cost, not reader patience. That rationale differs from point 1 and belongs in the prompt rule file.
4. **Honoring a length stated in the brief.** Tolerance rules (±20% in c01084, c01295, c01299; "Write to the config's target length" in c00825) show that when the caller gives a length, hitting it is part of the job. The proposal does not say the brief's length target binds.
5. **Count caps that force choice** (theme 12). "If you find yourself listing more, you haven't picked" (c00237) is a cutting rule for lists, which sentence-level deletion does not cover.
