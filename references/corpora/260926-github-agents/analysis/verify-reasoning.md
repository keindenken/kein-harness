# Verify reasoning: a skeptic's pass over synthesis.md

Scope: this pass attacks the conclusions of `analysis/synthesis.md`. It looks for places where the report moves from "authors do X" to "X works", leans on counts inflated by lineage or by how the corpus was built, ignores counter-evidence in `themes/` and `deep/`, or recommends something the data does not carry. Recomputations used `records.json`, `clusters.json`, `claims/*.jsonl`, `harvest.py`, `cluster.py` and the corpus files. Scratch scripts are in the session scratchpad and are not part of the repo.

Severity: **high** changes a recommendation; **medium** changes a figure, a quote, or an interpretation the report relies on; **low** is wording. Where I was unsure, the issue says so and is still flagged.

Totals: 23 issues, 6 high, 11 medium, 6 low.

---

## High

### 1. The corpus is the top 31% of harvested clusters, and the report never says so

- **Report text.** "**Corpus shape.** 1,089 writing-role records from 820 repos and 776 owners." And in Q1: "Interpretation: a writer as broad as the proposal (READMEs, reports, PRDs, blog posts and prompts in one role) is about 1% of practice."
- **What is wrong.** `cluster.py` produced 5,264 clusters. `batches/` covers all 5,264, but `results-sonnet/` and `records.json` hold only c00000 to c01629, which is 1,630 clusters. Clusters are sorted by copies and then stars, so the read slice is every multi-copy cluster plus single-repo clusters with at least 9 stars. All 3,634 unread clusters are single-repo files with 0 to 9 stars. They span 3,056 repos and 2,905 owners, and 3,048 of those repos appear nowhere in the read slice. So the unread tail holds about 3.7 times as many owners as the report counts. Every "% of owners", every "rare" (Q4 "1–2 owners"), "about 1% of practice", "7 of 776 owners" and "84% of repos" describes the popular, multi-copy end of the corpus. The low-star independent authors are exactly the population that the independence argument needs.
- **Evidence.** Recomputed: `clusters.json` has 5,264 entries. The highest record id is c01629. c01629 has repos=1 and stars=9. The star buckets of `clusters.json[1630:]` are {0–9: 3,634}. One hint that the tail differs on the rare traits the report cares about: `reasoning_kept_out` is 10% in the read 0–9-star bucket (n=211) and 4% in every other bucket.
- **Also.** The Q5 claim "The evidence flag sits at 61 to 64% in every star bucket (0–9, 10–99, 100–999, 1000+)" compares a range-restricted 0–9 bucket. Its 211 records are mostly multi-copy clusters and 9-star singletons, not a sample of low-star files.
- **Irony worth stating.** The report adopts c00608's "if the total distinct repository count … is under 10, say so in the Executive Summary", yet it does not put its own sampling limit in the Bottom line.
- **Severity: high.** Q1's "far wider than anything common" and Q4's "rare" labels (adopt/test/reject) rest on prevalence in a truncated, popularity-ordered slice.

### 2. The harvest filtered out reviewer roles, so the verdict on "no self-judgement" and the counts of lanes are biased by construction

- **Report text.** "**No self-judgement: supported for quality, contradicted for checking.** … Against: self_review_checklist is flagged for 634 records / 463 owners (60% of owners)". And in Q1: "**Writer-versus-writer lanes are rare.** Only 5 scope-boundary quotes, from 5 owners, route work to another *writing* role". And: "84% of repos have exactly one writing role."
- **What is wrong.**
  - `harvest.py` keeps a file only if its name matches `WRITING` and does *not* match `NOT_WRITING = (review|test|lint|debug|security|deploy|infra|sql|database|frontend|backend)`. A repo that pairs a `doc-writer` with a `doc-reviewer` contributes the writer only. The corpus therefore cannot see the architecture in which the writer does not self-review because a sibling reviewer exists. Reading the writers' self-check rates as "practice contradicts no-self-judgement" ignores that the counter-practice was filtered out.
  - The same filter, plus the name-based selection, undercounts sibling roles per repo. "84% one writer per repo" and "5 owners route to another writing role" are partly properties of the filename regex.
  - The repo queries (`topic:claude-code`, `opencode`, `codex-cli`, `subagents` …) target coding-agent collections. The heavy lean toward code documentation, and therefore "'General' means general across code documentation", is partly produced by the search, not only by what authors choose.
- **Evidence.** `harvest.py` lines 72 and 114. The collaboration theme (§4) notes: "In the corpus, the judge is a reviewer agent, an editor or a human". Those judges exist *outside* the harvested files.
- **Severity: high.** The report advises stating the no-self-judgement rule as "the writer runs fact and mechanics checks … quality verdicts belong to runs and evals". It frames the corpus as partly *against* the proposal on a population that excludes the proposal's own design.

### 3. Q3 calls popular instructions "Tier-3" and says the proposal "lacks" them, which turns prevalence into a requirement

- **Report text.** "## Q3. Tier-3 instructions the proposal lacks, by dimension". Bottom line: "The proposal lacks five things that recur across many independent owners". And: "almost everything here is 'recurring across independent sources' (tier 3)".
- **What is wrong.**
  - In the proposal's ledger, a tier grades evidence *for a claim*. The claim these counts support is "many authors write X". The claim the recommendation needs is "X improves a writer's output", and for that claim the corpus is at no tier at all. The report says as much in Q1 ("'X works' is not addressed") and Q6. Q3 then drops the distinction and uses the tier label as though it transferred.
  - "Lacks" also presumes each item should be added. Some of them (write surface, tool limits) the report itself says belong in tool grants, not prose.
  - The Q3 threshold is "at least 10 independent owners after the theme analyses' lineage discount". It is applied to counts from a truncated, coding-agent-skewed sample (issues 1 and 2) and from single-coder themes (issue 14).
- **Severity: high.** The section should read as "candidates that recur", each with a stated eval, not as gaps to fill.

### 4. "Misframed: interpretation is the rarest state" compares incompatible counts and omits the corpus's larger stance, which bans inference

- **Report text.** "**Misframed: 'interpretation' is the rarest of the states the corpus marks.** A script over all claims found 36 records / 35 owners that tell the writer to mark inference, interpretation or assumptions. … Far more owners mark the *unknown or unverified*: 68 owners in the evidence dimension, 43 in self-check." Bottom line: "It is **misframed in three places**: practice marks *unknown, assumed and inferred* claims far more than 'interpretation'".
- **What is wrong.**
  1. **Apples and oranges.** A regex count that cannot be reproduced (35 owners; the script is not in the repo) is set against hand-coded theme counts (68 and 43).
  2. **The report's own figures point the other way.** `separate_fact_from_opinion` is flagged for 83 owners (quoted in the same section), which is more than the 68 who mark unknowns. The self-check theme's "43" is theme 6, "Mark what could not be verified, in place, **and label inference as inference**" (51 records, 43 owners). The self-check theme calls it direct support: "Theme 6 (43 owners) directly supports it".
  3. **An omitted camp.** A sizeable group forbids interpretation rather than marking it: "Fact-check every claim against the actual source code before writing it. Never infer or speculate." (c01538); "Do not invent features or infer unverified behavior." (c00716); "Do not invent or infer data — only use what is provided in the input." (c01312); "Never speculate ("this will likely...") — only document verified behaviour" (c00278); also c00290, c00094, c00636, c01250, c00264, c00183, c00037, c00870 and c00223. That is about 13 owners from a quick regex (unsure of the exact count). For code docs the corpus norm looks closer to "exclude inference" than to "mark it". That bears on whether "interpretation is marked" belongs in a general core at all.
  4. **Prevalence does not make wording wrong.** That fewer authors mark interpretation says nothing about whether marking it helps.
- **Also missed.** Other three-way splits exist besides c00652, for example "Observe … Interpret … Hypothesize" (c00043) and "Distinguish facts from assessments — 'we observed' vs 'we assess'" (c01233).
- **Severity: high.** The recommended four-state vocabulary may well be right, but "misframed" is not established, and the ban-versus-mark split is the decision the core actually has to make.

### 5. "Evidence discipline and cutting hardly vary by type" is contradicted by the report's own table

- **Report text.** Bottom line Q1: "Evidence discipline, cutting, matching house style and leading with the point hardly vary by type."
- **What is wrong.** The Q1 flag table printed a few lines below shows large spreads:
  - verify-against-source: 34% (fiction), 38% (marketing), 52% (blog) and 58% (prd), against 73–76% for code docs.
  - cut: 37% (report) and 40% (prd), against 67% (code-comments) and 73% (ux-microcopy, in `stats.txt`).
  - The self-check theme says outright: "The evidence *checks* are strongly type-specific (… project-docs and api-reference at 90 to 100%)". The length theme's theme 8 has 22 owners overriding brevity for PRDs and proofs.
  - What is flat across types is the *slogan* "never invent" (lift ≤1.6), not evidence discipline or cutting as practised.
- **Severity: high.** This sentence is the basis for putting evidence and cutting in the general core as uniform rules. The data supports a core *principle* with type-dependent force and defaults, which is a different design.

### 6. The report adopts two opposite missing-input policies, on thin support

- **Report text.**
  - Q3: "Missing input: resolve by reading, then assume, disclose and proceed | 46 ask vs 15 assume | core".
  - Q4 item 10: "**Unattended missing input.** c01056 (Q3)."
  - Q4 item 11: "**Failure return and in-place gap markers.** 'CANNOT_COMPLETE: <one-sentence reason>' and 'Do not guess at content. Do not produce partial output and hope the parent fills in the gaps.' (c00112 …)".
- **What is wrong.**
  - Items 10 and 11 are both under "Worth adopting", and they prescribe opposite behaviour for the same situation: proceed on disclosed assumptions, or refuse and return a failure. E7 is designed to test exactly these two against each other, which confirms the report knows they conflict.
  - The support for "assume and proceed" is thinner than stated. The scope-boundary theme counts "23 owners stop and ask, against 3 owners who assume and proceed". The collaboration theme finds "5 owners in the never-ask group". c01209, which the report quotes approvingly as the model brief ("Expect the caller's brief to state … the audience"), also says "If the audience or purpose is missing, stop before guessing" (scope-boundary §4).
- **Severity: high.** The Q3 carrier column puts assume-and-proceed in the core before E7 has run. Both items should be marked "test", not "adopt".

---

## Medium

### 7. "The carrier mechanism works" overstates a one-run observation of delivery

- **Report text.** "**The carrier mechanism works in Claude Code (measured; tier 1).**"
- **What is wrong.** `~/Documents/wiki/findings/260926-path-scoped-rules-reach-subagents-once.md` covers one run per condition, on `--model haiku`, and records whether a `nested_memory` attachment appeared. It shows that the rule is *delivered* on a Read. It does not show that the writer follows the rule, that delivery happens on Write to a new path, or that it survives compaction. The report lists some of these gaps below the heading, but the heading says "works" and applies "tier 1" ("measured in runs") to a single transcript observation.
- **Severity: medium.** Suggested wording: "rules are delivered to a subagent on its first matching Read (one run, claude-code 2.1.282)".

### 8. Omitted: the only incident evidence about externalised conventions shows them being skipped, and the incident count is low

- **Report text.** Q1: "rules that cite a run, incident or measurement as their origin come from about 7 owners, and none of them is about role granularity". Also: "The deep read guesses the owner may have stopped trusting skill loading; that is unverified."
- **What is wrong.**
  - c01007 (XuanRanL) ties a rule to incidents, and the rule is about loading an external conventions file before writing: "Skipping this doc has been the root cause of 4+ post-publish incidents since 2026-05-21. Always load this BEFORE writing any markdown." That is the one piece of incident evidence in the corpus that bears on the proposal's carrier, and it says an externalised convention file gets skipped.
  - c00708 (frenzymath) names the same failure: "Two failure modes this clause exists to prevent: (i) **skip-the-guide** … (ii) **skim-the-guide** … Both produce vanilla-model-default voice".
  - Deep c00029 notes that its repo uses path-scoped `.instructions.md` for code but a dedicated role for docs, "the reverse of the proposal's default". Q1 does not mention this.
  - Other rules of observed origin missing from the "about 7": c01164 ("Many of them fix one recurring failure mode: the main clause goes inert…") and c01218 ("A rule that only fixes eval-207…"). The count is closer to 9 to 11 owners. I am unsure about c01164 and c00708, which describe observed failure modes without naming an incident.
- **Severity: medium.** This supports Q1's second design consequence ("a step that exposes it to its rules"), but it also means the fallback carriers (a brief that points at a rules file, "read neighbours") are the ones the corpus shows failing.

### 9. "Run the examples" is counted as practice, but many of the roles that ask for it cannot run anything

- **Report text.** "**Execution as evidence.** … The theme has 83 owners." Q3: "Run examples and commands; label those that could not be run | 83 (about 76) | core (as a tier) + rule". Q2 treats c00003 and c00016 as isolated cautions.
- **What is wrong.** I matched run/compile/test-the-examples quotes in the evidence and self-check claims: 118 records from 107 owners. Of the 58 whose frontmatter declares a tools list, 20 (34%) grant no execution tool. Examples: c00018 `Read, Write, Edit, Glob, Grep, WebFetch, WebSearch`, c00122, c00638, c00821, c01136, c01247 `Read, Edit, Glob`, and c01333 `['read', 'edit']`. Another 60 declare no tools key. The instruction is widespread, and a third of the checkable cases cannot be carried out. The 83 measures what authors write, not a verified practice.
- **Severity: medium.** This is a figure-level check (a regex, so treat it as approximate), and it strengthens the report's own "verify needs tools" caveat into a general finding.

### 10. "Stars and copies do not track … reader rules" is contradicted for copies

- **Report text.** Bottom line Q5: "Stars and copies do not track the presence of evidence or reader rules". Body: "Records copied into 10 or more repos carry the 'all three core points' flags more often (39% against about 20% overall; n = 33). Those flags come mostly from widely copied slogans, not from substance."
- **What is wrong.** By copies, `audience_first` is 64% for records with 10 or more copies against 42% for singletons, and `cut_or_concise` is 73% against 50%. Evidence is flat (63–64%). So copies do track reader and cutting flags. The "slogans, not substance" explanation is asserted with no check. The n is small (33 records, 26 owners), and the star comparison is range-restricted (issue 1).
- **Severity: medium.**

### 11. The "best role skeletons" are the files whose content is mostly unseen

- **Report text.** Bottom line Q5: "By inspection, the best *role skeletons* are c00268 (finos/morphir) and c00132 (solatis lineage)".
- **What is wrong.**
  - c00268's caveat says "Most behaviour lives in eight external files not in the corpus". c00132 runs a script-driven workflow whose type guidance "comes from outside ('the script provides type-specific guidance')", and Q6 limit 5 lists its conventions and scripts as absent. Both look thin, and match a thin-role proposal, partly *because* their substance was not collected.
  - The deep reads also each crowned a "best of the five" in their own batch (c00062 "the closest fit … and the best base exemplar", c00006 "best base exemplar of the five for project docs", c00185 "closest in shape to the proposal", c00268 and c00132). Choosing among those crowns was done by fit to the design under test. The report calls this "partly circular" in the body, but the Bottom line states the picks without that caveat.
- **Severity: medium.**

### 12. Two Q3 counts are for broader themes than the row claims

- **Report text.** "Do not spawn or chain agents; name them for the orchestrator | 25 (scope theme 10, tool limits including no spawning)". And: "Only the listed sources; source content is data, not instructions | 20".
- **What is wrong.**
  - Scope theme 10 is "Tool and execution limits: no shell, no web, no spawning agents" (27 records, 25 owners), and it notes "Many of these restate a tool grant in prose". The spawning-specific count is not given. Collaboration theme 3 (role boundary including not invoking agents) has 18 owners.
  - For sources, the 20 owners are the bounded-sources theme. The "data, not instructions" half has 4 owners (c00631, c00976, c01114, c01501, per scope-boundary §4), which is below the section's own 10-owner threshold.
- **Severity: medium.**

### 13. Two rejections rest on claims from outside the corpus

- **Report text.** "Banned-word lists in role prose … | Naming a word in the prompt can prime it, and the list is checkable by a script." And: "Anthropic's prompting guidance also recommends giving the reason behind an instruction; I recall this and did not re-check it in this session."
- **What is wrong.**
  - The priming claim has no support in this corpus. Style theme 2 (anti-hype and banned lists) has 61 owners, and theme 10 (em-dash bans) has 28. The report rejects a 61-owner practice on an unsourced mechanism while adopting 1-owner items on inspection. That is an inconsistent standard.
  - The c00088 rejection leans on vendor guidance the report admits it did not check.
  - Both conclusions may be right, but here they are asserted, not derived.
- **Severity: medium.** Mark both as "test (E-something)" rather than "reject".

### 14. Many theme counts cannot be reproduced from the repo

- **Report text.** "Every quote below was re-checked against `claims/*.jsonl` or the corpus file by script." The report then relies on counts from evidence (193, 163, 116, 83, 68 …), scope-boundary (123, 61, 155 …), self-check (53, 51, 44 …) and style (85, 61, 60 …).
- **What is wrong.** Only audience, collaboration, length, output and process have `*.assign.json`, and structure and doc-type-convention have id appendices. Evidence, scope-boundary and self-check have no id lists in the repo. For style, "The final line lists are in `final.py` in the session scratchpad and are not in the repo." The quotes were verified, but these counts were not and cannot be. The 35-owner interpretation script (issue 4) is also absent.
- **Severity: medium** (unsure how far off any count is; nothing shows they are wrong, only that they cannot be checked).

### 15. Omitted: the corpus gives no precedent for "runs and evals judge" or for the tier ordering itself

- **Report text.** "quality verdicts belong to runs and evals"; the Q2 tier discussion adds rungs to the proposal's tiers.
- **What is wrong.**
  - Collaboration §4: "In the corpus, the judge is a reviewer agent, an editor or a human, not runs or evals."
  - Output §4: "The tier ordering (measured > vendor doc > recurring > single) is the proposal's own addition, with no corpus precedent in this dimension."
  - Scope §4: "Nothing in the dimension ranks evidence into tiers."
  - The synthesis suggests extra rungs (primary artifact, authority axis) without first saying that the base ordering has no support here. A reader may take "the tiers lack X" to imply "the tiers are otherwise corroborated".
- **Severity: medium.**

### 16. Omitted: two Q3-sized items that meet the report's own threshold

- **What is missing.**
  - **Bounded verification and stop conditions.** From process §4: "c00098 'max 2 attempts per link … stop and tell the user'; retry caps in 11 owners. Without a budget, 'every sentence traceable' can turn into unbounded verification." The self-check theme adds revision-loop caps (c00098, c01226, c01553). This matters for an unattended writer whose point 2 has no budget.
  - **"Update every affected doc, not just the nearest"** (12 owners, scope §4). This is a direct tension with minimal footprint and cut-by-default across documents. The report covers only the stale-copy search (c01317).
- **Severity: medium.**

### 17. "They do not split README from API reference" has counterexamples in the report's own split set

- **Report text.** "Interpretation: when authors do split, they split off the types whose *evidence model* differs from code docs … They do not split README from API reference."
- **What is wrong.** Of the 34 repos with single-type writers for two or more primary types:
  - Several non-catalogue repos split *within* code docs: vinnie357/claudio (api-reference / project-docs), ansys/pydpf-core (code-comments / project-docs) and TheLobbi/claude (api-reference / report). Catalogues rohitg00 and viksant do the same.
  - Five non-catalogue splits are academic / report (Galaxy-Dawn, Imbad0202, frenzymath, saptarsibhowmick, taxideftis). Both sides share a citation evidence model, so these do not fit an "evidence model differs from code docs" reading.
- **Severity: medium.** The evidence-model reading is one pattern among several, from about 20 non-catalogue repos.

---

## Low

### 18. "Load the project's instruction files" is used as evidence of moving conventions out of the role

- **Report text.** "**Even single-type authors move conventions out of the role.** … 61 owners tell the writer to load the project's instruction and context files before writing".
- **What is wrong.** Reading CLAUDE.md or AGENTS.md is project context, not doc-type conventions carried outside the role. Only the 33 external-template owners and c00352 bear directly on the claim.
- **Severity: low.**

### 19. c00185 is called the only run-derived rule in the set, but Q1 lists others from the same deep-read set

- **Report text.** Q5 table, c00185: "The only rule in the set derived from a run".
- **What is wrong.** Q1 lists c00063, c00112 and c00041, all deep-read, among the rules of incident or run origin. The Q5 section itself says c00063's AC-regex paragraph "reads as a post-incident fix".
- **Severity: low.**

### 20. "Only one record names the full three-way split" misses other records

- **Report text.** "Only one record names the full three-way split: 'Separate observed facts, calculated values, and interpretation.' (c00652)".
- **What is wrong.** c00043 ("Observe … Interpret … Hypothesize") and c00342 ("high (grounded in sources), medium (inferred), low (speculative)") also name three-way splits.
- **Severity: low.**

### 21. The report and the output theme disagree on point 3, and the report does not say so

- **Report text.** "reasoning_kept_out: 55 / 52 / 51, 7% of owners, the rarest core flag".
- **What is wrong.** The output theme judged point 3 "**Supported most strongly of the three**", from claims: "Only the deliverable, no preamble or notes" (25 owners) and "File is the deliverable, reply is a pointer" (33 owners). The Bottom line reports only the 7% flag, which the model set.
- **Severity: low.**

### 22. The general-role reader comparison is read in one direction

- **Report text.** "audience_first is flagged for 69% of general-purpose records against 30% of single-type. Interpretation: a role that cannot inherit its reader from the doc type has to name one, so this supports keeping point 1 explicit".
- **What is wrong.** By owner the split is 70% against 35% (recomputed). The confound is acknowledged, but the rate also fits "general roles are more boilerplate-heavy". The deep reads describe c00003 and c00004 as persona boilerplate, and audience theme 1 is 72 owners of bare "identify audience". So this is not support for the proposal's *form* of point 1.
- **Severity: low.**

### 23. The general-purpose doc-type table leaves out two rows

- **Report text.** The Q1 table "counts owners whose general-purpose role carries each doc type".
- **What is wrong.** It omits `other` (35 owners) and `social-media` (12 owners, recomputed). Both are non-code, so leaving them out slightly strengthens "general means general across code documentation".
- **Severity: low.**

---

## Recomputations that held

These were checked and match the report:

- Core flag counts (475/393/374; 687/568/543; 562/480/466; 55/52/51; 99/87/83; 634/486/463).
- 690 of 820 repos and 633 of 776 owners with one role.
- The scope-by-owner splits.
- 38 records / 37 owners and the 7 listed ids for broad general roles.
- 34 split repos / 32 owners.
- The 10 records with all three core flags plus `reasoning_kept_out`.
- The 39% against 20% figure for records with 10 or more copies (n=33).
- c00006 at 43 repos / 41 owners.
- c00036's CVSS 6.4 result as the deep read reports it.
- The lineage direction c00049 → c00132, supported by the `.archive_deprecated_20251025_` filename in deep c00049.

Counting the copies of each cluster, 87% of 2,220 repos have one writing role, so the 84% is robust to how copies are attributed. It is not robust to the truncation in issue 1.
