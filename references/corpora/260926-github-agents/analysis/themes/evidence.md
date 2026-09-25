# Evidence dimension: recurring instruction themes

Source: `claims/evidence.jsonl`, 1,170 quote lines from 678 distinct records, 543 distinct repos, 519 distinct owners. Every line was read.

## Method

- Each line was tagged against 21 candidate themes with keyword patterns. Every theme's matches were then read one by one: lines that matched only on a word (for example "flag" meaning a CLI flag, or "verify code examples compile" landing in the verify-against-code theme) were removed by hand, and lines the patterns missed were added by hand. A line can belong to several themes. After review, 1,032 of 1,170 lines (614 of 678 records) sit in at least one theme. The 138 lines left over are mostly bare accuracy slogans ("Technical accuracy 100% verified") or checks tied to a single domain (WCAG criteria, fiction continuity, prospect dossiers).
- Counts are distinct records / distinct repos / distinct owners among the assigned lines. The owner is the part of the repo name before "/". Themes are ranked by owners.
- "Concentrates in" uses lift: the share of the theme's records carrying a doc type, divided by that doc type's share across all 678 evidence records. The baseline shares are project-docs 0.59, api-reference 0.39, report-analysis 0.19, changelog 0.15, prd-spec 0.14, code-comments 0.12, academic 0.05, blog-article 0.05, marketing-copy 0.06, prompt-instructions 0.02. Only types with at least 3 records in the theme are listed.
- Specificity ratings were not used.

## 1. Top recurring themes

| # | Theme | Records | Repos | Owners |
|---|---|---|---|---|
| 1 | Ground claims in the code/repo: read or check it before writing | 221 | 202 | 193 |
| 2 | Never invent, fabricate, guess or assume | 195 | 167 | 163 |
| 3 | Every claim traceable to a named source (citation, file:line, URL) | 138 | 119 | 116 |
| 4 | Examples and commands must be run, compiled or tested before inclusion | 91 | 85 | 83 |
| 5 | Mark unverifiable points instead of filling the gap | 82 | 68 | 68 |
| 6 | Document what exists now, not what is planned, intended or specified | 64 | 62 | 62 |
| 7 | Docs must track the code; stale or inaccurate docs are a defect | 59 | 55 | 55 |
| 8 | Identifiers and paths copied exactly from source and checked to exist | 55 | 52 | 47 |
| 9 | Don't write from model memory; fetch current, authoritative external sources | 38 | 38 | 37 |
| 10 | Grade evidence or confidence and don't promote weaker to stronger | 38 | 37 | 37 |
| 11 | Closed world: facts only from the supplied brief, payload or research | 47 | 36 | 36 |
| 12 | Numbers, metrics and scores only from measurement or source data | 47 | 35 | 35 |
| 13 | Never fabricate citations, quotes, URLs or issue numbers | 33 | 31 | 30 |
| 14 | Editing and restating must not change what is asserted | 34 | 29 | 29 |
| 15 | Existing prose, summaries, specs and scraped text are leads to check, not evidence | 23 | 23 | 23 |

These fell below the cut: read the diff or git history to learn what changed (22 records / 22 repos / 22 owners); when sources conflict, surface both, and in docs the code wins (20/19/19); specific numbers over vague words (19/18/18); missing is not zero and unknown stays unknown (14/12/12); requirement traceability (14/10/9, with prd-spec lift 6.7).

### 1. Ground claims in the code/repo: read or check it before writing
Records 221, repos 202, owners 193. Concentrates in code-comments (lift 1.9), api-reference (1.7), project-docs and changelog (1.5 each). It is under-represented in report-analysis (0.3) and prd-spec (0.7). Scope split: general-purpose 52, few-types 109, single-type 60.
- "Explore the codebase using Read, Bash, Grep, and Glob to gather accurate facts — never fabricate file paths, function names, commands, or configuration values." (c00006)
- "The code is the only reliable witness; names, comments, old documents, and briefings are testimony to verify before repeating" (c01283)
- "Accuracy over speed. Every claim in documentation must come from actual code you've read." (c01342)

### 2. Never invent, fabricate, guess or assume
Records 195, repos 167, owners 163. Close to evenly spread: no doc type has a lift above 1.6. The highest are social-media, prompt-instructions and blog-article (1.5–1.6) and report-analysis (1.3). This is the generic prohibition that most of the narrower themes below make concrete.
- "DO NOT invent endpoints, env vars, or behavior the code does not contain. Every claim comes from a file you read." (c00096)
- "If evidence is unavailable, narrow the claim or mark the uncertainty. Never fill gaps with plausible details." (c00389)
- "Never invent claims, prerequisites, compatibility, supported platforms, versions, performance results, or validation results." (c00804)

### 3. Every claim traceable to a named source
Records 138, repos 119, owners 116. Concentrates in academic (3.1) and report-analysis (2.1), and less so blog-article (1.6). It is under-represented in project-docs (0.7) and api-reference (0.5). Mostly single-type roles (84 of 138).
- "Every substantive claim must land on one of three grounds. If it can't, cut the claim or rewrite it until it can." (c00295)
- "Each claim then cites its source by ID and location, such as `SRC-001#NFR-014`, so a reviewer can trace any statement back to the approved document rather than to recalled text." (c00631)
- "Cite path/to/file.ts:line so claims are checkable." (c01201)

### 4. Examples and commands must be run, compiled or tested before inclusion
Records 91, repos 85, owners 83. Concentrates in api-reference (2.2), code-comments (1.7), project-docs (1.6) and changelog (1.5).
- "Run the code yourself — if you can't follow your own setup instructions, users can't either" (c00131)
- "Run what you document. If you write a command, execute it and use the real output." (c01364)
- "Every example must compile. Verify with `go build` on a throwaway file." (c01468)

### 5. Mark unverifiable points instead of filling the gap
Records 82, repos 68, owners 68. Concentrates in academic (1.8), other (1.6), blog-article (1.6) and report-analysis (1.4). Of the 68 owners, 45 put the marker inside the deliverable (placeholder, `[verify]`, "not recorded", an HTML comment) and 13 route it to a person or the caller (ask, follow-up task, open questions). Some owners do both.
- "If you cannot verify something, label it \"Unverified / Needs confirmation\" and add a follow-up task (do not guess)." (c00077)
- "Mark anything unverified as unverified where the claim appears." (c00268)
- "Anything you cannot confirm is either dropped or explicitly marked unverified - never silently promoted to fact." (c01201)

### 6. Document what exists now, not what is planned, intended or specified
Records 64, repos 62, owners 62. Concentrates in changelog and code-comments (2.2 each) and project-docs (1.5).
- "Do not document what code \"should\" do -- document what it DOES." (c00139)
- "Never describe planned functionality as if it exists." (c00242)
- "Writing documentation based on the spec instead of the actual code. *Correction*: read the changed files on the branch, not the spec. The code is the truth; the spec is the plan." (c01350)

### 7. Docs must track the code; stale or inaccurate docs are a defect
Records 59, repos 55, owners 55. Concentrates in api-reference and changelog (1.8 each), project-docs (1.7) and code-comments (1.6). A sub-slogan, "inaccurate/stale docs are worse than no docs", appears in 16 lines from 13 owners. See the lineage warnings.
- "keep every claim synchronized with the code. Documentation drift is a defect." (c00789)
- "Stale docs are worse than missing docs. Verify behavior before describing it" (c00389)
- "Record the commit. Every `Last verified` line MUST include the current git commit hash." (c00469)

### 8. Identifiers and paths copied exactly from source and checked to exist
Records 55, repos 52, owners 47. Mildly concentrated in project-docs (1.3) and api-reference (1.2).
- "Grep every parameter name you documented against the source. Any name returning 0 results is hallucinated. Remove it." (c00718)
- "Identifiers, URLs, parameter names, field names, component names, and string literals MUST be copied exactly as written in code." (c00683)
- "every file path claimed in the CHANGELOG entry MUST exist via `ls <path>` verification before committing" (c00063)

### 9. Don't write from model memory; fetch current, authoritative external sources
Records 38, repos 38, owners 37. Weakly concentrated: blog-article (1.7) and report-analysis (1.4). Some roles also give source-priority orders, such as "Prefer authoritative sources: official docs > pkg.go.dev > GitHub repos > blog posts" (c01097) and "Priority order: User statements > Recent documents > Older references." (c00629).
- "Never trust LLM memory — verify via tools, git, file reads" (c00094)
- "When documenting external tools, libraries, protocols, specifications, or standards, you MUST fetch up-to-date information before writing. Never rely solely on training data for external references." (c01097)
- "Never guess from training data — AI/LLM fields move fast enough that a 12-month offset can make the report actively wrong." (c00809)

### 10. Grade evidence or confidence and don't promote weaker to stronger
Records 38, repos 37, owners 37. Concentrates in report-analysis (3.2) and academic (2.2), and is under-represented in project-docs (0.5).
- "Distinguish between strong evidence (large sample, high quality) and preliminary findings" (c00506)
- "Confidence labels are load-bearing. In the RSM/TD32 documents, never promote something from inferred or conjectured to confirmed unless you were given the concrete evidence that confirms it." (c01091)
- "Classify every fact as: stated by user, inferred, or unknown." (c01320)

### 11. Closed world: facts only from the supplied brief, payload or research
Records 47, repos 36, owners 36. Concentrates in blog-article (2.8), report-analysis (2.5) and marketing-copy (2.3), and is nearly absent from project-docs (0.2). Almost all of it is single-type (38 of 47). These are roles fed by an upstream agent or a research step.
- "You render only what you are given. If a field is missing from the input payload, write the template placeholder (e.g. `[NOT EVALUATED]`, `[NO PUBLISHED PRICE]`) — do not invent values" (c00248)
- "Do not fill gaps from general knowledge." (c00631)
- "You cannot write this script from your own knowledge, and a script written without the brief is thrown away." (c00825)

### 12. Numbers, metrics and scores only from measurement or source data
Records 47, repos 35, owners 35. Concentrates in social-media (6.6), blog-article (3.3), marketing-copy (2.6) and report-analysis (2.3), and is under-represented in project-docs and api-reference (0.4).
- "Never write a number you did not read out of an artifact in the pack." (c00420)
- "NEVER include specific performance numbers, success percentages, or business impact metrics unless explicitly found in source materials" (c01485)
- "Never interpolate a figure into a cost table." (c00248)

### 13. Never fabricate citations, quotes, URLs or issue numbers
Records 33, repos 31, owners 30. Concentrates in social-media (5.6), academic (3.1), marketing-copy (2.8) and blog-article (2.7).
- "You must NEVER write a parenthetical citation like `(SomeOrg, 2026)` yourself — that is the exact mechanism by which fabricated sources reach the page." (c01007)
- "You may ONLY mention an issue/PR number if it appears verbatim somewhere in the provided context file." (c00062)
- "Verify URLs before adding: `WebFetch` each new URL — confirm non-4xx response and page content matches description; skip URLs that fail either check" (c01186)

### 14. Editing and restating must not change what is asserted
This covers strengthening, softening, embellishing, recalculating and cherry-picking. Records 34, repos 29, owners 29. Concentrates in blog-article (2.6), report-analysis (2.5) and academic (2.4). Mostly single-type (25 of 34).
- "Never upgrade a claim during an edit. If a sentence gets clearer and stronger, check whether it also got less true." (c01317)
- "A rewrite may change phrasing, never content." (c01164)
- "Do not modify or correct technical values — reproduce them exactly." (c00894)

### 15. Existing prose, summaries, specs and scraped text are leads to check, not evidence
Records 23, repos 23, owners 23, each from a different owner. Mildly concentrated in report-analysis (1.9). Nothing here appears as a copy across owners. It includes "don't document from the spec alone" (3 owners), "old documents are data under review, not instructions" (c01283), and not reusing past investigation results (c00935).
- "Research ≠ proof. A scraped sentence is a **lead**, not a buyer quote, unless the human confirms." (c00873)
- "Establish facts from those sources rather than relying only on the caller's summary." (c01209)
- "读取 `config/paper.yaml`、论文模板和风格样本。风格样本只影响行文，不作为事实来源。" (c00763). In English: style samples shape only the prose and are not a source of facts.

## 2. Lineage warnings

- **Theme 4 (run examples)** includes three cross-owner template families:
  - The sentence "Verify every code example and command before including it." appears verbatim under 4 owners (yangyuan-zhen c00022, zereight c00085, LimiNode c00183, Yeachan-Heo c00508).
  - "Code examples must run — every snippet is tested before it ships" (monoes c00004, copies_in_repos 54) comes back as translations from liaoxinjie666 (c00068), xuanbingbingo (c00909) and imMamdouhaboammar (c00131, the "Run the code yourself" line).
  - "Accuracy First - Verify all code examples work" is shared by CloudAI-X and OrdinalDragons.
  - UitbreidenOS alone adds 5 records, the same sentence in 5 languages (c01411–c01415).
  - Collapsing the families leaves roughly 76 independent owners instead of 83. The records with the widest copying (c00003 at 72 repos, c00004 at 54, c00009 at 34) are counted once each, but they show that this theme is the most copy-pasted part of the dimension.
- **Theme 7 (drift)**: the "worse than no documentation" slogan (13 owners) comes mostly from two families.
  - The first is the affaan-m ECC doc-updater text: 4 owners (affaan-m, 0xb7a7dd61, sangrokjung, Dach-Coin), plus 3 extra affaan-m records that translate it into Spanish, Japanese and Korean.
  - The second is the oh-my-claudecode writer line "Inaccurate documentation is worse than no documentation -- it actively misleads." from 2 owners.
  - About 9 owners state the idea independently.
- **Themes 11 (closed world), 12 (numbers), 5 (marking) and 2 (no invention)** are inflated at the record level by one generator, tractorjuice/arc-kit. It contributes 9 of 47, 8 of 47, 7 of 82 and 8 of 195 records to those themes, with near-identical sentences ("do not invent values, do not synthesise from general knowledge"). kesslernity (3 records each in themes 11 and 12) and vinnie357 (3 identical "requires analysis / requires measurement" lines, c00311/c00312/c01485) add smaller clusters. Owner counts are not affected much. Record counts for these themes overstate how often the idea recurs.
- **Theme 1 (ground in code)** has short shared phrasings that point to common templates rather than independent writing:
  - "Treat source code as read-only truth" (borgius, melnikov1512, paodealho404, github c00504).
  - "Document what EXISTS. Code (provided) is correct and functional." (akiselev, alfieprojectsdev; also in theme 6).
  - "Document actual tech stack, not assumed" (paodealho404, asleekgeek).
  - "Use concrete examples from the actual codebase" (wshobson, viksant).
  - These are 2–4 owners each, a small share of 193.
- **Below-the-cut requirement traceability**: kcenon supplies 4 of 14 records (one SDLC pipeline). With 9 owners it is a PRD-pipeline pattern, not a writer norm.
- Other pairs that look like one voice: "Never hallucinate information - only include facts from verified sources" (iannuttall, NicholasSpisak); "Verify all facts, names, and credentials are accurate" (davila7, davepoon); "Check factual accuracy (syntax, versions)." (github/gh-aw, kubestellar).

## 3. Sharp but rare (1–2 owners)

1. KiwiCanopy (c00936): "A plausible-sounding path is not evidence, and neither is a claim you wrote earlier in the same session." and "A correction is itself a claim — this rule earned its second sentence when a rewritten historical paragraph shipped a second wrong number in the same change set."
2. tractorjuice (c00609): "A percentage without its denominator is how a 3-repository sample gets read as a government-wide trend." and "Never render an empty vulnerability scope as a clean result."
3. modu-ai (c00063): "A count of 0 is a RED flag, not a pass. `0 == 0` is a vacuous comparison — if the command returns 0, stop and inspect `acceptance.md` by hand rather than reporting the self-test satisfied."
4. shinpr (c01327, c01326): "Use causal language only for hypotheses supported by a repeated output-to-rule mapping" and "Aggregate only differences that repeat in at least two trials."
5. my-chiefmind (c01364): "If it can't be run here (it needs prod, a secret, a paid service), say so in the text instead of guessing at the result."
6. XuanRanL (c01007): "A true, unquantified sentence beats a false, precise one every time."
7. deccanai-org (c00420): "Declare the evidence tier." and "If our metric differs from the buyer's, show both."
8. affaan-m (c00469): "Cross-validate. A function's docstring says it returns `User | null`, but every caller null-checks — the Requirement says \"returns User, null for nonexistent\". The actual contract is what callers rely on, not what docs claim."
9. MShneur (c01234): "Technically-true-but-misleading = fail. Selective omission of material counter-evidence = fail."
10. egerev (c01114): "Do not infer technology from directory names (e.g., seeing a langchain/ directory does not mean the project uses LangChain — read the imports)."

## 4. Bearing on the proposed writer

### One general role, with type differences carried outside it
- **Supports.** The obligation itself is stated the same way everywhere. Theme 2 (no invention) is almost flat across doc types, with no lift above 1.6. The code-grounding theme appears in 52 general-purpose records.
- **Adds.** What counts as evidence depends on the doc type:
  - Code for project-docs, api-reference, code-comments and changelog (themes 1, 4, 6, 7, 8, lift 1.5–2.2).
  - A supplied payload or brief for report, blog and marketing (theme 11, lift 2.3–2.8, nearly absent from project-docs).
  - Citations for academic and report (theme 3, lift 2.1–3.1).
  - Requirement traceability for prd-spec (lift 6.7).
- The proposal's split is a good fit for this: the core says "traceable to evidence" and a path rule or the brief says which evidence. The type-specific rules to move out are the doc-type-concentrated themes listed above.

### Point 1: start from the reader
- The evidence dimension says little about the reader. Only 13 owners tie evidence to the reader, and they do it through execution: "Run the code yourself — if you can't follow your own setup instructions, users can't either" (c00131), test from a fresh environment, copy-pasteable commands. There is no contradiction.
- **Adds.** For how-to documents, the reader's action (running the steps) is itself the test of the evidence. That links point 1 to theme 4.

### Point 2: every factual sentence traceable; interpretation marked
- **Strongly supported.** Themes 1, 2 and 3 are the three largest in the dimension (193, 163 and 116 owners). The proposal's mapping of doc type to evidence (code for project docs, data and sources for reports) matches where themes 1 and 3 concentrate.
- **"Measurements for prompts" has almost no corpus behind it.** prompt-instructions is 2% of evidence records. The only measurement-style rules are shinpr's (repeat in at least two trials; causal language only for repeated mappings) and hyhmrright's "A rule that only fixes eval-207 and would mis-fire on a near-miss is overfitting — reject it." (c01218). The corpus neither contradicts nor confirms this part.
- **Marking interpretation is supported but narrower than the corpus.** Themes 5 and 10 (68 and 37 owners) mark three states, not two: verified, inferred or assumed, and unknown. Examples are "Classify every fact as: stated by user, inferred, or unknown." (c01320) and "distinguish measured facts from planning assumptions". A fact-versus-interpretation split leaves out "unknown / not recorded" and "assumed".
- **What point 2 lacks, from this dimension:**
  - **Execution as evidence (theme 4, 83 owners).** A claim that a command or example works is evidenced by running it, not by pointing at code. "Traceable" as written sounds static.
  - **Exact-identifier fidelity (theme 8, 47 owners).** Names, flags and paths are copied, not paraphrased, and checked mechanically: grep with zero hits means hallucinated; `ls` the path. This check can be scripted, which fits the proposal's preference for checks outside the role.
  - **Evidence has a timestamp (theme 7, 55 owners).** Record the commit a claim was verified at (c00469), and re-verify when code moves. The proposal's ledger has no version or commit field.
  - **A conflict rule (below the cut, 19 owners).** When sources disagree, state both. In code docs, "the code wins" and the mismatch is noted ("If code and description conflict: document the code, note the mismatch." c00636; "Where they diverge, the build wins and the prose may note the divergence." c00950). The proposal has tiers but no tie-break or disclosure rule.
  - **Missing is not zero (below the cut, 12 owners, report-heavy).** An empty result is not a clean result, and unknown stays unknown (c00609, c00652).
  - **Closed world when a brief supplies the facts (theme 11, 36 owners).** The caller's brief can define the allowed fact set, so gaps are not filled from general knowledge. The proposal lets the brief carry type differences but does not say the brief can also cap the facts.
  - **No memory for external facts (theme 9, 37 owners).** Vendor or library facts are fetched current, not recalled.

### Point 3: cutting by default; working notes go to a separate output
- **Supported.** 24 owners tell the writer to cut or omit an unsupported claim rather than keep it: "Accuracy over completeness. Incomplete documentation is better than inaccurate documentation. If you are unsure about a detail, flag it rather than guess." (c01587); "cut the claim or rewrite it until it can" (c00295). The "worse than no docs" slogan (about 9 independent owners after lineage) backs the same default.
- **Tension on where uncertainty goes.** Theme 5 mostly puts the marker in the deliverable (45 owners): placeholders, "not recorded", `[verify]`, or hidden HTML comments such as "`<!-- REVIEW: source needed -->`" (c01036). Only 13 owners route it to the caller. So the corpus treats "this is unverified" as reader-facing content, not as a working note. The proposal needs a stated rule on which it is.
  - A reading consistent with the corpus: a gap the reader must know about to act stays in the file, as with "exposure is unknown for them, not absent" (c00609). A to-do for someone else goes to the side output (follow-up task, open question).
- **Adds.** Cutting is an edit, and theme 14 (29 owners) warns that edits distort claims: "Never upgrade a claim during an edit. If a sentence gets clearer and stronger, check whether it also got less true." (c01317). A cut-by-default writer needs this guard, or tightening will strengthen claims.

### Combining drafts or outside examples by claim, with a ledger and evidence tiers
- **Supported by theme 15 (23 owners, no template lineage).** Existing prose, caller summaries, specs, scraped sentences and even the writer's own earlier claims are leads to corroborate, not evidence. That is the proposal's "the unit is a claim with its source, not a whole draft". sghwr (c00763) adds a split the proposal does not state: outside samples may shape style but may never supply facts.
- **Tiers are partly echoed.**
  - Measured at the top: "Performance numbers must be measured" (c00444); "Declare the evidence tier." (c00420).
  - Independent recurrence: at least 2 independent sources on different domains (c00541); differences repeated in at least two trials (c01326).
  - Official documentation over memory: theme 9.
  - **What the proposal's tiers lack:** for project docs, the top evidence in this corpus is the primary artifact read directly (the code, the payload, the data file). That is neither "measured in runs" nor "vendor documentation". For code facts, the corpus does not rank "recurring across independent sources" above a single read of the code. riekelt calls every secondary text "testimony" (c01283).
  - **Suggested fix:** add a "primary artifact, read directly" tier, and state that for facts about the artifact it beats any amount of agreeing secondary text.
- **Ledger: partial support.** 19 owners ask for structured claim-to-source records: Sources tables, evidence IDs, a Location column, `Last verified` commit lines, a Citations block, `<!-- Source: ... -->` headers. Most put them inside the deliverable (inline citations, frontmatter, HTML comments), not beside it. Only a few keep a separate matrix or ledger ("keep claim-evidence matrices, literature theme maps, repo/source indexes, citations, and assumptions in source", c01367). For reports and academic writing (theme 3, lift 2–3) the reader needs the citation inline, so the ledger is not a substitute for in-text citation there. That rule belongs in the path-scoped layer.

### "Does not judge its own output"
- This dimension is full of self-verification by the writer: "Before returning, silently verify every claim against the source and the linked notes." (c00628), grep every parameter, `ls` every path.
- These are mechanical claim checks, not quality judgments, and they are compatible with the proposal. The proposal should say explicitly that the writer checks claims against evidence (and can be given scripts for the mechanical parts, such as grep for identifiers, `ls` for paths and URL status for links), while judging quality stays with runs and evals.

### Tension the proposal should decide on
- Theme "specific numbers" (18 owners, report and marketing) pushes toward quantification, for example "Specific beats generic: \"reduced load time from 4.2s to 0.8s\" not \"significantly improved performance.\"" (c01062).
- One owner sets a quota, "Minimum 8 unique statistics per 2,000-word post" (c00835), which pressures the writer to fabricate.
- The counterweight, "A true, unquantified sentence beats a false, precise one every time." (c01007), comes from one owner.
- The proposal's evidence rule implies the counterweight. It is worth stating directly because the specificity pressure is common in the corpus.
