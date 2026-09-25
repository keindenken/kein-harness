# Number check of synthesis.md

Scope: every count, percentage and owner/repo tally in `analysis/synthesis.md`, recomputed from `records.json` (writing_role true), `claims/*.jsonl`, `stats.txt`, the theme files and their `*.assign.json` id lists, and `clusters.json`. Owner-level counts across copies were recomputed by rerunning `cluster.py`'s grouping into the scratchpad (0 mismatches against `clusters.json` repo counts). Quotes carrying an id were checked verbatim against the corpus file by script (193 checked; every miss was a gloss, a label or a multi-id line, except the items listed below).

Result: 21 issues, 0 high, 9 medium, 12 low. Most figures hold. Listed at the end are the figures that were checked and found correct.

## Issues

### 1. "c00004, 54 repos" is not a general writer (medium)

- Report text (Bottom line 5, Q5): "the two most-copied general writers (c00003, 72 repos; c00004, 54 repos) are poor fits" and "The two most-copied general writers are both poor fits".
- What is wrong: c00004 (monoes/monomind) has `scope: few-types`. The most-copied `general-purpose` records are c00003 (72), c00005 (davila7, 53), c00006 (gsd, 43), c00008 and c00009 (OpenAgentsControl, 34 each).
- Evidence: `records.json` c00004 `scope: few-types, doc_types [project-docs, api-reference]`. The corrected second place, c00005, is still a poor fit (the report itself rejects its fabricated sample output in Q4), so the "popularity is not evidence" point survives. But the third, c00006, is the report's own recommended project-docs base, which the sentence as written hides.

### 2. "They do not split README from API reference" is contradicted, and the type list omits two types (medium; possibly high, unsure)

- Report text (Q1): "Across the 34 repos, the types involved in the split are report-analysis (16 repos), project-docs (16), prd-spec (13), academic (5), marketing (5) and fiction (4)." and "Interpretation: when authors do split, they split off the types whose evidence model differs from code docs ... They do not split README from API reference."
- What is wrong: the recomputed type counts over the same 34 repos include api-reference 6 (more than academic or marketing) and social-media 4 (equal to fiction). Both are left out. Three repos do split project-docs from api-reference into separate single-type roles, and one splits code-comments from project-docs.
- Evidence: vinnie357/claudio c00311 `documentation-api-creator.md` [api-reference] vs c00312 `documentation-readme-creator.md` [project-docs] (the literal README/API split, not a catalogue); rohitg00/awesome-claude-code-toolkit c00042 vs c00118 `api-documentation.md`; viksant/vibe-coding-tools-content c01065 `api-documentation-generator.md` vs c01070; ansys/pydpf-core c00929 [code-comments, other] vs c00930 [project-docs, code-comments]. Full count: project-docs 16, report-analysis 16, prd-spec 13, api-reference 6, marketing 5, academic 5, social-media 4, fiction 4, blog 3, other 3, changelog 2, code-comments 2, prompt 1. The "evidence-model lines" reading may still hold for most splits, but the absolute "do not" is false. I rate it medium because the Q1 verdict leans on this sentence, and I am not sure it would change the recommendation.

### 3. Writer-versus-writer lanes: most of the five cited records do not route to a writing role (medium)

- Report text (Q1): "Only 5 scope-boundary quotes, from 5 owners, route work to another *writing* role (c00206, c00338, c00521, c01209, c01270). For example, c01209 says: 'Decline commit messages, ... those remain with the caller.'"
- What is wrong: in their scope-boundary quotes, c00338 defers to "human review" and the "repository maintainer", c01209 hands work back to "the caller" (the example chosen), and c01270 reserves files "for the Reviewer Agent". None of these is a writing role. Only c00206 (changelog and release notes delegated to `[skill:dotnet-release-management]`) and c00521 (the content-humanizer skill; planning goes to content-strategy) are plausibly writer-to-writer.
- Evidence: `claims/scope-boundary.jsonl` lines for those five ids. On the report's own definition the count is about 2, not 5. It is also unsure whether the fiction lane files (tiny-flowlab and similar), which the report puts in a separate sentence, should be counted here.

### 4. "Do not spawn or chain agents: 25 owners" counts all tool limits (medium)

- Report text (Q3, scope table): "Do not spawn or chain agents; name them for the orchestrator | 25 (scope theme 10, tool limits including no spawning)".
- What is wrong: scope theme 10 is "no shell, no web, no spawning agents", 25 owners in all. The spawning-specific count is the collaboration theme's `NO_DIRECT_INVOKE`: 9 records / 9 owners.
- Evidence: `themes/scope-boundary.md` theme 10; `collaboration.assign.json` NO_DIRECT_INVOKE recomputed as 9 / 9 / 9.

### 5. "36 records / 35 owners" mark inference, interpretation or assumptions: not reproducible, and it conflicts with other counts (medium, unsure)

- Report text (Q2, point 2): "A script over all claims found 36 records / 35 owners that tell the writer to mark inference, interpretation or assumptions." It supports "Misframed: 'interpretation' is the rarest of the states the corpus marks."
- What is wrong: no script or id list for this count is saved in the directory, and other counts disagree. self-check theme 6, "Mark what is unverified or inferred ... label inference as inference", has 43 owners. structure.md counts "about 9 owners" who mark interpretation. A regex over all claims for infer/interpret/assum/speculat/hypothes plus a marking verb gives 63 records / 59 owners (upper bound, not hand-cleaned). Only 3 quotes contain "interpret" with a marking verb (c00652, c00937, c00111), and just 1 of them (c00652) marks interpretation.
- Evidence: see above. The direction (mark inferred and assumed states, not only "interpretation") is probably right, but the number cannot be checked and the unknown-vs-inferred contrast depends on how self-check theme 6 is split.

### 6. README cap "80 to 120 lines (c00495)" is an AGENTS.md cap (medium)

- Report text (Q1): "README caps run from 80 to 120 lines (c00495) up to 1,000 (c01362)".
- What is wrong: c00495's "Target: 80-120 lines" sits under the heading "### AGENTS.md — The project entry map for AI agents". It does not apply to a README.
- Evidence: corpus file `sickn33_agentic-awesome-skills__...creator-docs.md` (c00495). c01362's "Keep README under 1000 lines" is correct.

### 7. c00029 "al-folio (17 owners, one theme)" (medium)

- Report text (Q5 table): "c00029 al-folio (17 owners, one theme)".
- What is wrong: the c00029 cluster covers 12 repos / 12 owners. Across every corpus file that names al-folio, together with its copies, there are 22 repos / 22 owners. No count gives 17. The deep read's "17" counts files containing "Ask first" ("72 files under 49 owners contain 'Ask first', 17 of them this al-folio agent"), not owners.
- Evidence: cluster membership rebuilt from `cluster.py`; `analysis/deep/c00029.md` lines 5 and 7.

### 8. "Evidence rules are weakest here" for marketing (medium)

- Report text (Q1): "Evidence rules are weakest here: only 38% of marketing records carry verify-against-source."
- What is wrong: fiction-narrative is lower, at 34%, and the report's own table shows it. Marketing is second-lowest among the types listed.
- Evidence: `stats.txt` verify_a: fiction-narrative 34, marketing-copy 38, ux-microcopy 44.

### 9. Persona memory attributed to c00007 (medium)

- Report text (Q4 reject table): "Persona memory and experience: 'You remember what confused developers in the past...' | c00004 (54 repos), c00007".
- What is wrong: c00007 (mrgoonie/human-mcp) has no persona-memory line. Its only "Remember" is "**Remember:** Your job is to make people stop, read, and act." The quoted line is in c00004 and c00131, which are one template family.
- Evidence: script over the source files of writing-role records: "remember what confused" occurs in c00004 and c00131 only.

### 10. "Only one record uses the word [tier] as the proposal does" (low, unsure)

- Report text (Q2): "Only one record uses the word as the proposal does: 'Declare the evidence tier.' (c00420)."
- What is wrong: at least one other claim ranks sources by tier: c01236 (ivfarias/ceo) "Extract 15+ credible sources (Tier 1-2 preferred: academic journals, official docs, established news outlets)". c00835's corpus file also says "Tier 1-3 sources only". Whether ranking sources counts as "as the proposal does" is a judgement call.
- Evidence: `claims/*.jsonl` quotes containing "tier" (14 records; most are risk or model tiers).

### 11. c00185 "The only rule in the set derived from a run" contradicts the report's own incident list (low)

- Report text (Q5 table, c00185 row): "The only rule in the set derived from a run".
- What is wrong: Q1 lists 7 owners whose rules cite a run or incident, and three of them are in this same exemplar table: c00112 (`edgeLabelBackground` bug), c00063 (the AC-regex post-incident paragraph, "reads as a post-incident fix" in its own row) and c00041 (review rounds). c00936 ("earned its second sentence") is also cited.
- Evidence: synthesis.md Q1 "No comparison exists" list and Q5 table rows; corpus text confirmed for c00112, c00185 and c00936.

### 12. Owner units mix record-level and copy-level counts (low)

- Report text: Q5 "c00006 gsd `doc-writer` (41 owners, one voice)", "c00061 (4 owners)", "c00132 ... the opening line appears under 9 owners", against Q2 "The deletion test ... comes from one template family carried by 4 owners" and Units: "copies_in_repos and stars are never used as weight".
- What is wrong: c00006 is 1 record / 1 owner at record level, and 41 is the owner count across its copies. Measured the same way, the deletion-test family reaches 53 owners (c00004's cluster alone spans 50 owners), not 4. The figures are each defensible, but under two different units in the same report, so a template can look narrow in one place and broad in another.
- Evidence: rebuilt cluster membership: c00004 54 repos / 50 owners; c00006 43 / 41; c00061 7 / 4; the "Every word must earn its tokens" line appears in 11 repos / 9 owners (this 9 is correct).

### 13. "mechanical checks ... 47 to 76 owners each" mixes voices and owners (low)

- Report text (Bottom line 3): "mechanical checks (run the examples, grep the identifiers, resolve the links, build; 47 to 76 owners each)".
- What is wrong: 76 is the voices figure for run-examples. The owner count is 83 (evidence theme 4), or 67 owners / 63 voices in self-check theme 1. Stated consistently, the range is 47 to 83 owners.
- Evidence: `themes/evidence.md` theme 4 (83 owners, about 76 voices); identifiers 47; links 51; validators 53.

### 14. General-purpose doc-type table and single-type list leave out rows (low)

- Report text (Q1): the general-purpose table (project-docs 127 ... fiction 2) and "single-type roles take these primary types: project-docs 126, report-analysis 86, prd-spec 71, api-reference 25, academic 20, marketing 19, blog 17, fiction 17, prompt-instructions 15."
- What is wrong: the listed numbers are correct, but the general-purpose table leaves out other (35 owners), social-media (12) and ux-microcopy (4). The table lists prompt, academic and fiction at 2 to 3 owners, yet omits social-media, which is larger than all three. The single-type list leaves out other (19), which is larger than several types it does list, and code-comments (13).
- Evidence: recomputed from `records.json`.

### 15. "Only 7 owners span two or more": independence and definition caveats (low)

- Report text (Q1): "Only 7 owners span two or more: c00003, c00309, c01062, c01081, c01441, c01481 and c01549."
- What is wrong: the 7 is correct under the stated definition. Two of the seven, though (github/awesome-copilot c00003 and jmagly/carbonyl-agent c00309), are owners the report itself classes as catalogues. If the model's scope label is ignored, two few-types records also span code docs plus two of the listed types (c00010 mrgoonie [project-docs, api-reference, prd-spec, report-analysis]; c00298 nasrulhazim [project-docs, prd-spec, changelog, report-analysis]), which makes 9 owners. Counting social-media, fiction and ux as non-code types gives 11 owners.
- Evidence: recomputed from `records.json`.

### 16. "Numbers disagree even within a type": the sentence-cap example spans two types (low)

- Report text (Q1): "sentence caps run from 8 to 12 words (c00107) up to about 40 (c01164)".
- What is wrong: c00107 is project-docs/api-reference and c01164 is academic, so the pair does not show disagreement within one type. Within project-docs the range is still wide (8 to 12 in c00107, 20 to 25 in c00159, under 30 in c00717), so a within-type example exists.
- Evidence: `records.json` doc_types; `claims/length.jsonl`.

### 17. Scope table drops 2 records (low)

- Report text (Q1 scope table): single-type 539, few-types 381, general-purpose 167.
- What is wrong: the rows sum to 1,087. Two records have `scope: null` (2 repos, 2 owners).
- Evidence: `stats.txt` "None: 2".

### 18. c00268 and c00132 are presented as general role skeletons but are rated few-types (low)

- Report text (Q5): "Role skeleton (general) | c00268 finos/morphir".
- What is wrong: c00268 is `scope: few-types` [project-docs, academic, other], and c00132 is few-types too. Neither is a general-purpose record in the corpus's own labels. Choosing them as skeletons is a judgement, but the label reads as a corpus fact.
- Evidence: `records.json`.

### 19. "Calibrate: hedge only real uncertainty, once — 23" relabels a different theme (low)

- Report text (Q3 structure and style table): "Calibrate: hedge only real uncertainty, once | 23".
- What is wrong: style theme 13 (23 owners) is "Calibrate claims: no overclaiming; separate fact from assessment and shipped from planned". The "hedge once" idea comes from a single quote (c00493), so the 23 owners do not back the label as worded.
- Evidence: `themes/style.md` table row 13.

### 20. A single-owner item appears under the "at least 10 independent owners" heading (low)

- Report text (Q3 intro): "These are items with at least 10 independent owners after the theme analyses' lineage discount." Then under Collaboration: "In revise mode, fix only the named findings (c00397, within the 15-owner author/reviewer theme)."
- What is wrong: the 15 owners back author/reviewer separation, not "fix only named findings". That specific instruction is cited from 1 record. Also, "Get facts from the people ... (13 owners)" and "Honest draft status (13)" are fine, but "Missing is not zero (12)" and "Revisions ... (14)" sit close to the threshold with no lineage discount shown.
- Evidence: `collaboration.assign.json`: c00397 is assigned only to NO_SELF_REVIEW.

### 21. Two quoted strings are not verbatim (low)

- Report text: Q4 "'If the rule and the example contradict each other, follow the example' (in Russian) | c01281"; Q5 c00036 row "a case for 'numbers come from a tool'".
- What is wrong: the first is an English rendering placed in quotation marks with no original, which departs from the report's own practice of verbatim original plus bracketed gloss. The second is the report's own phrase, placed in quotation marks as if quoted.
- Evidence: the quote-check script found neither string in the cited corpus file.

## Checked and correct

- Corpus shape: 1,089 records / 820 repos / 776 owners. Exactly one writing role: 690 of 820 repos (84%) and 633 of 776 owners (82%).
- Scope by records / repos / owners: 539/413/394, 381/342/336, 167/149/145.
- General-purpose owners by type (project-docs 127, api 106, changelog 51, code-comments 39, prd 19, blog 17, marketing 17, report 14, prompt 3, academic 2, fiction 2). 38 records / 37 owners span code docs plus one other type. 34 split repos / 32 owners. All 12 named catalogue owners are among the 34.
- Flag tallies by records / repos / owners: audience 475/393/374 (48%), verify 687/568/543 (70%), cite 230/187/182, separate 99/87/83 (11%), cut 562/480/466 (60%), reasoning_kept_out 55/52/51 (7%), self_review 634 records / 463 owners (60%). The 10 records carrying all three core flags plus reasoning_kept_out match the list exactly.
- audience_first: general-purpose 69%, single-type 30%. The verify flag falls between 60.8% and 64.3% in every star bucket. Records with 10 or more copies: 13 of 33 carry all three core flags (39%), against 219 of 1,089 (20%) overall.
- The doc-type flag table matches `stats.txt`.
- All theme-file figures cited in the report agree with the theme files. For audience, collaboration, length, output and process they were also recomputed from the `*.assign.json` id lists: 99, 72, 36 (7 from the template), 27, 30, 22, 22, 13, 9, 14, 10, 11 vs 22; 61, 54, 46, 36, 35, 33, 25, 24, 22, 21, 17, 16, 15 assume; 42 ask, 93 of 247, 17 to about 4 voices, 15 author/reviewer, 13 facts from owners; 53, 38, 33, 22, 21, 14, 14, 13, 15; 22 counter-brevity, 21 agent-file budget (14.1x), 14 overflow (8.3x), 15 item caps; source_precedence 9 owners (the "9 owners resolve conflicts by authority" figure). All lifts cited were found in the theme files.
- The seven incident-origin owners are all distinct, and the cited text exists (c00185, c00936, c00950, c01193, c00063, c00112, c00041).
- c00036 CVSS: recomputed with the `cvss` package (CVSS4). The stored-XSS vector scores 6.4 Medium, not 8.8. The IDOR (7.1) and SSRF (9.3) vectors match the file.
- c00065 contains merge-conflict markers. c00003's tools are `codebase, edit/editFiles, search, web/fetch`, with no run tool. c00016's tools are `["codebase"]` only. c00132 contains "no arbitrary token limits". c00049 carries hard token MAX caps.
- Copy counts: c00000 130, c00003 72, c00004 54, c00005 53, c00006 43. The c00160 humanizer lines appear in 2 record owners (c00160, c00756).
