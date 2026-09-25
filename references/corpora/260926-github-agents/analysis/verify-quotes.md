# Verification of quotes and record attributions in synthesis.md

Scope: every quoted instruction and every record id attribution in `analysis/synthesis.md`, checked against `corpus/<file>` (id → `clusters.json[n]`) and `records.json`. Where the report gives a figure next to an id, I recomputed it where that was cheap.

## Method

- A script pulled every double-quoted string from each line that names a `cNNNNN` id (172 quote/id pairs) and tested whether the quote occurs in the named record's corpus file, after normalising whitespace, markdown emphasis (`*`, `_`, backticks), escaped quotes and curly quotes, and splitting on `...`/`…`. Every pair that failed was read by hand. So were the backtick-quoted markers (`[MATERIAL GAP]`, `[NO PUBLISHED PRICE]`, `<<PLACEHOLDER: …>>`, `<!-- VERIFY: {claim} -->`, `claim_intent_manifests[]`, `CANNOT_COMPLETE`, `edgeLabelBackground`, `ZeroDivisionError`, `[PASTE ACTUAL REQUEST HERE]`, `[verify]`, `morphir kb check`, `tools: ["codebase"]`).
- About 70 quotes were read in their surrounding text to check whether the context changes the meaning.
- The cluster build was re-run in the scratchpad with full member lists, to check the owner and repo counts the report attaches to ids.

## What holds

- **Verbatim.** Every quoted instruction occurs verbatim in the record it is attributed to. The script's misses were all the report's own phrases in quote marks ("cut by default", "runs judge", "the caller decided", "what readers need" and similar), which are not attributed to a record, or table rows that cite several ids with the quotes in the same order (c00007/c00087, c00003/c00004/c00016, c00003/c00136/c00006). The Spanish, Chinese, Japanese and Korean glosses (c00201, c00715, c00763, c00541, c00879, c01627, c00935, c00943, c00185) are accurate.
- **Owner and lineage attributions.** These match the corpus and the deep reads: modu-ai (c00063), Imbad0202 (c00041, c00493, c00494), JuanLunaIA (c01317), JetBrains (c00710), KiwiCanopy (c00936), tractorjuice (c00605, c00608, c00609), duc01226 (c01600), fabioc-aloha (c00112, c00197; lastReviewed 2026-05-01 against 2026-05-30, so "successor" is consistent), finos (c00268: 2 repos, 1 owner; eight external files named), nanikasheila (c00185), gsd (c00006: 43 repos, 41 owners), al-folio (17 owners per deep/c00029.md), drmoisan (c00062: 0 stars, 7 repos, 1 owner), c00061 (4 owners), adcontextprotocol (c00087, c00088), claude-octopus (c00083), josipjelic (c00058), knightdx91-alt (c00076, c00114), and the copy counts c00000 = 130, c00003 = 72, c00004 = 54, c00005 = 53 repos.
- **Recomputed figures that match.** These all match `records.json`: 1,089 records / 820 repos / 776 owners; 690 single-writer repos and 633 single-writer owners; the scope table; the general-purpose doc-type owner table; 38 records / 37 owners and the 7 listed owners (c00003, c00309, c01062, c01081, c01441, c01481, c01549); every flag triple in Q2 and the 634 / 463 self-review figure; the per-doc-type flag table; the 10 records carrying all three core flags plus reasoning_kept_out; audience_first at 69% general against 30% single-type; the evidence flag at 61–64% in each star bucket; 39% against 20% (n = 33) for records in 10 or more repos; tiny-flowlab's 16 writing roles; and the single-type primary-type owner counts. The c00036 CVSS example also checks out: the `cvss` library scores `AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:L/VA:N/SC:H/SI:H/SA:N` at 6.4 Medium, not the file's 8.8.

## Issues

### 1. The per-type split list leaves out API reference, and the interpretation built on it does not hold (medium; close to high)

- **Report text** (lines 65–66): "Across the 34 repos, the types involved in the split are report-analysis (16 repos), project-docs (16), prd-spec (13), academic (5), marketing (5) and fiction (4)." and "Interpretation: when authors do split, they split off the types whose *evidence model* differs from code docs ... They do not split README from API reference."
- **What is wrong.** The recomputed list over the same 34 repos is: report-analysis 16, project-docs 16, prd-spec 13, **api-reference 6**, marketing 5, academic 5, **social-media 4**, fiction 4, blog 3, other 3, changelog 2, code-comments 2, prompt 1. API reference is left out even though it outranks academic, marketing and fiction. Several repos do split README or guides from API or comment docs:
  - vinnie357/claudio: c00311 `documentation-api-creator` against c00312 `documentation-readme-creator` (and c01485 user-guide). This is authored design, not a catalogue.
  - ansys/pydpf-core: c00929 (code-comments) against c00930 (project-docs).
  - rohitg00: c00118 against c00042.
  - viksant: c01065 against c01070.
- **Effect.** The Q1 verdict sentence "when they do it is along evidence-model lines" is weaker than stated. The recommendations do not depend on it.

### 2. The README cap attributed to c00495 applies to AGENTS.md (medium)

- **Report text** (line 121): "README caps run from 80 to 120 lines (c00495) up to 1,000 (c01362)".
- **Evidence.** In c00495 the target sits under the `### AGENTS.md` heading: "The project entry map for AI agents. This is the most important file. ... **Target**: 80-120 lines. This is a map, not a manual." It is not a README cap. c01362 ("Keep README under 1000 lines") is correct. The README range therefore lacks its lower anchor.

### 3. The five "writer-to-writer" routing records mostly route elsewhere, and the example routes to the caller (medium)

- **Report text** (line 68): "Only 5 scope-boundary quotes, from 5 owners, route work to another *writing* role (c00206, c00338, c00521, c01209, c01270). For example, c01209 says: \"Decline commit messages, ... those remain with the caller.\""
- **Evidence from `claims/scope-boundary.jsonl`.**
  - c00338 defers to "repository maintainer" and "human review".
  - c01209 hands work to "the caller".
  - c01270 is a read restriction ("NEVER read or reference files in `human-bench/articles/` - those are for the Reviewer Agent only").
  - c00521 routes planning to content-strategy and hands de-AI work to a skill.
  - c00206 delegates to a release-management *skill*.
  - At most c00206 and c00521 route to a writing capability.
- **Omissions.** Real writer-to-writer routes are missing from the list. c00539 (zenstory-ai): "不拥有：角色对话风格（character-designer）、文字去AI味（narrative-writer）…" [does not own: dialogue style (character-designer), de-AI prose (narrative-writer)…]. c00397: "`documenter` owns **internal** artifacts ... If the document is for someone who does **not** know the repo → your responsibility." The tiny-flowlab records c01284, c01286 and c01288 do the same, although the report treats fiction separately.
- **Effect.** The quoted example does not show what the sentence claims, and the count and ids are wrong. The conclusion that such lanes are rare survives.

### 4. c00839 does not forbid asking (medium)

- **Report text** (line 184): "One forbids asking (c00839). In an unattended run the writer cannot ask..."
- **Evidence.** c00839's workflow says "ask the questions one by one and wait for answer before asking the next question", and then: "There is no need to ask about the target audience." It skips one question inside an ask-heavy flow and forbids nothing. Presenting it as the no-ask precedent next to the unattended-run argument misstates it.

### 5. c00873's user-profile line is about the agent's persona, not about two readers (medium)

- **Report text** (line 185): "Missing: the writer has two readers. ... one owner guards the difference: \"Do not adopt the human's Claude.ai user profile / occupation. That profile is about **them**, and it leaks into every product.\" (c00873)."
- **Evidence.** In c00873 the line sits in a setup list and is followed by "Your hats are below." / "## Profession hats (only these)". It tells the agent not to take on the operator's occupation as its own identity. It says nothing about the caller as a reader separate from the document's reader. The quote is verbatim, but the context changes what it supports.

### 6. c00016 asks for syntactic correctness, not compilation (medium)

- **Report text** (line 235): "TaxCore asks the writer to confirm C# compiles with `tools: [\"codebase\"]` only (c00016)."
- **Evidence.** c00016 line 134 reads "Confirm all code examples are syntactically correct C# / .NET 6". The file never uses "compile". Syntax can plausibly be judged by reading, so this is a weak example for "verify needs tools". The c00003 example on the line before it ("Verify all code examples compile/run" with tools `codebase, edit/editFiles, search, web/fetch`) is accurate.

### 7. "Only one record uses the word [tier] as the proposal does" undercounts (medium; unsure)

- **Report text** (line 290): "Only one record uses the word as the proposal does: \"Declare the evidence tier.\" (c00420)."
- **Evidence.** Other writing-role records tier sources or evidence by strength:
  - c00835: "Tier 1-3 sources only".
  - c01236: "Extract 15+ credible sources (Tier 1-2 preferred: academic journals, official docs, established…".
  - c01045: "…it defines page format, confidence tiers, and conventions".
- I am unsure how narrowly the report meant "as the proposal does". c00835 and c01236 rank sources much as the proposal's ledger tiers do, so I count at least three records, not one.

### 8. c00487 is about rewriting wording, not about treating generated text as leads to check (medium)

- **Report text** (line 281, under "treat existing prose ... as leads to check, not evidence"): "\"Treat the generated wording as source material, not a preferred baseline.\" (c00487)".
- **Evidence.** The rest of that bullet in c00487 reads: "Rewrite retained entries to make them clearer, more precise, and more user-facing. ... Preserve the original meaning and do not invent or broaden claims." The generated changelog entries are the factual source, and only their *wording* is not a baseline. That is close to the opposite of "a lead to verify". The theme's count (23 owners) may still stand, but this example does not show it.

### 9. The Q5 table calls c00185 "the only rule in the set derived from a run", which the report contradicts elsewhere (medium)

- **Report text** (line 494, c00185 row, "Evidence beyond popularity"): "The only rule in the set derived from a run".
- **Evidence.**
  - The same table says c00112 has "One rule cites a real bug" (the `edgeLabelBackground: 'transparent'` precedence rule) and that "c00063's regex paragraph reads as a post-incident fix".
  - Q1 (lines 129–136) lists about seven owners with run- or incident-derived rules: c00185, c00936, c00950, c01193, c00063, c00112 and c00041. c00041's self-gate cites "codex round-7 F17 observed that standalone deep-research output had no NO-LOCATOR enforcement layer".
- The claim is wrong as stated.

### 10. "One template family carried by 4 owners" for the deletion test (low)

- **Report text** (line 245): "This is the best-known phrasing, but it comes from one template family carried by 4 owners."
- **Evidence.**
  - The 4 are record owners, per themes/length.md: monoes c00004, imMamdouhaboammar c00131, and two Chinese translations (liaoxinjie666 c00068, xuanbingbingo c00909).
  - The c00004 cluster alone spans 54 repos under 50 owners, and the corpus search finds the English line in c00004, c00131 and c03570.
- "4 owners" follows the report's no-copy-weighting rule, but it understates how widely the line is carried. It should say "4 record owners (c00004 alone is copied into 54 repos / 50 owners)".

### 11. c00197 did not fully replace skill loading with inline rules (low)

- **Report text** (line 140): "c00112 → c00197 went the other way: it replaced \"load and follow these skills\" with inline rules".
- **Evidence.** c00197's "Rules you MUST follow" section still lists "`doc-hygiene` skill (anti-drift rules and link integrity for living documents)". The move was partial. The quote itself is correctly placed in c00112.

### 12. The paraphrase "a diff shows what changed, never why" is attributed to c00062, which does not say it (low)

- **Report text** (line 431): "A diff shows what changed, never why (c00062)."
- **Evidence.** c00062 names the why-sources ("Rely on embedded feature-doc excerpts (spec/plan/user-story) and PR Intent fields as the sole “why” sources; do not speculate beyond provided sources.") and never mentions the diff's limits. The sentence is the report's own generalisation and should be marked as interpretation.

### 13. c00684's "no state exists only to fill the template" refers to UI component states (low)

- **Report text** (line 262): "The corpus's reconciliation keeps the section but does not pad it: ... \"no state exists only to fill the template\" (c00684)."
- **Evidence.** c00684 is a UI spec designer. The line is a checklist item: "Every in-scope interactive component records each applicable state/display contract; no state exists only to fill the template". Here "state" means component states such as loading and error, not document sections. The analogy is reasonable, but it is not a statement about required sections.

### 14. The quote from c00006 undercuts the reason it is cited for (low)

- **Report text** (line 451, "Mandatory engagement or filler sections"): "\"Include at least 2 issues; leave as a placeholder list if none are discoverable\"" with "They force content that has no evidence behind it".
- **Evidence.** In c00006 the line belongs to a "Common setup issues" section with a "Discover:" recipe (`.env.example`, `engines`, the existing troubleshooting section). Its own fallback is a placeholder, not invented content. It still forces a section, but the quoted clause says the opposite of "forces unevidenced content". The report does not say that "issues" here means setup problems.

### 15. The c01281 quote appears in English with no original (low)

- **Report text** (line 456): "\"If the rule and the example contradict each other, follow the example\" (in Russian)".
- **Evidence.** The original is "Если правило и пример противоречат друг другу, ориентируйся на пример." The translation is accurate. Elsewhere the report gives non-English quotes in the original with a bracketed gloss (line 7). Here it puts a translation inside quote marks as if it were verbatim.

### 16. The bottom line changes the case inside a quotation (low)

- **Report text** (line 19): "\"a count of 0 is a red flag, not a pass\" (c00063)".
- **Evidence.** The original is "A count of 0 is a RED flag, not a pass." The capitalised RED is the author's emphasis. Line 419 quotes it correctly.

### 17. c00352 describes type-scoped loading, not path scoping (low)

- **Report text** (line 74): "One owner states the path-scoping idea directly: \"Read **only** the reference for the document type at hand — not the whole set.\" (c00352)".
- **Evidence.** In c00352, the preloaded `technical-writing` skill "maps each document type ... to a template under its `references/`". Selection goes by doc type through a skill, not by file path. It supports "type content outside the role" but not *path* scoping.

### 18. c00950's "invented kickers" are design elements a build shipped, not an outside example (low)

- **Report text** (line 432, and E9 on line 537): used for "Outside examples shape style, never facts ... This bears directly on merging outside examples", and in E9 as "one outside example carrying a stylish but invented pattern (c00950)".
- **Evidence.** c00950 is a design-system documenter. The rule is "Never canonize a craft-floor refusal into the system: an element the floor bans (kickers and eyebrows, ...) is recorded ... as a defect the build carries". "Kickers" are UI eyebrow labels. The rule is about not writing a defect in the documented build into DESIGN.md. It does not address outside examples or invented facts. The analogy is the report's own and should be marked as interpretation.

### 19. c00185's `rules/` remark is weak evidence that runtimes differ on path-scoped rules (low; unsure)

- **Report text** (line 142, repeated in Q6 limit 8 on line 523): "Other runtimes differ: c00185 warns \"CLI では `rules/` が自動ロードされない\" [in the CLI, `rules/` are not auto-loaded] (Copilot CLI)."
- **Evidence.** In c00185 the line heads a section listing the framework's own rule files (`rules/workflow-state.md`, `rules/commit-message.md`) for the agent to `view` manually. It is one framework author's remark about their own `rules/` folder under Copilot CLI, not an observation about path-scoped rule injection. It is quoted accurately, but it supports less than "other runtimes differ".

### 20. c00631 is a documentation page about agents, not an agent prompt (low)

- **Report text** (lines 294 and 352): "\"Conflict resolution hierarchy: user input > template guidance > agent defaults\" (c00631)" and "\"Do not fill gaps from general knowledge.\" (c00631)".
- **Evidence.** c00631 is `microsoft/hve-core docs/agents/project-planning/brd-prd-builders.md`, with front matter `title: BRD & PRD Builders`, `ms.topic: tutorial`. The hierarchy line is a feature bullet under "Quality Controls". The closed-world line is the last sentence of a *sample user invocation* in a `text` code block. The second one fits the report's "brief" carrier well. Both are verbatim, but the record is documentation about agents, and the report treats it as a writer's instructions.

### 21. c00012 offered as a model for a claim-state vocabulary (low)

- **Report text** (line 220): "c01320 and c00012 (\"grounded in source notes, explicit assumptions, or validated references\") are the models."
- **Evidence.** In c00012 (a marketing book co-author) the line is "**Trace Claims to Sources**: Every substantial claim should be grounded in source notes, explicit assumptions, or validated references." It lists acceptable grounds and does not ask for claims to be labelled by state. c01320 ("Classify every fact as: stated by user, inferred, or unknown", with `[Assumption to be validated]` and `[TBD]` labels) is a genuine model. c00012 is not.

### 22. c00114's burden of proof for deletion is fiction-specific (low)

- **Report text** (line 267, under "edit mode reverses the default"): "\"If you can name even a minor function, make a targeted fix, not a deletion.\" (c00114)".
- **Evidence.** The full sentence in c00114 (`book-editor`, fiction) is: "Before removing anything, complete this sentence: \"This passage does nothing — not texture, not voice beat, not pacing buffer, not character noise.\" If you can name even a minor function...". Here "function" means narrative function. The quote is presented alongside documentation edit rules with no mention that it comes from fiction. Q4 item 16 and the Q5 row do say it is fiction.

## Summary

22 issues, none high. Nine are medium: 1–9. Issue 1 is closest to high, because it weakens the evidence the Q1 verdict cites. Thirteen are low: 10–22. No quoted instruction is misquoted in a way that fails a verbatim check, and no quote is attributed to a record that lacks it. The problems are context (4, 5, 8, 13, 17–22), mischaracterised content (2, 3, 6, 12), counts or lists that do not reproduce (1, 3, 7, 10) and one internal contradiction (9).
