# Number check of synthesis.md

Scope: every count, percentage and owner tally in `analysis/synthesis.md`, recomputed from `records.json` (design_role true only), `stats.txt`, `claims/*.jsonl` and `analysis/themes/*.assign.json`, using the theme groups named in the report's Appendix B. Owner = repo prefix before "/". "FD" = the 15-record frontend-design family listed in `themes/direction-taste.md`.

Result: 17 issues, 1 high. Most headline figures reproduce exactly. The problems come from how some constructs were built, from inverted or overstated wording, and from template families left in some counts while other counts remove them.

## Issues

### 1. Mode tables are not what the multi-form roles do (high, somewhat unsure)

- Report text: "The multi-form roles with the clearest contracts (at least 14 records from 12 owners) declare an explicit mode table" (scorecard row 1). Also "The clearest way the corpus handles several forms in one role is an explicit mode table" and "the corpus's working form of it is a table, not an open instruction" (Q2).
- What is wrong: 14 records and 12 owners reproduces, but most of those 14 are not multi-form roles, and most multi-form roles have no mode table. The reading "Keep it only with a mode table" is presented as the corpus's pattern. The evidence supports only "a few roles, c00681 foremost, use one".
- Evidence (counts over the proposal's six forms):
  - Of the 14 listed records, 5 cover 3 or more forms: c00681, c00322, c00320, s0112 and c00701.
  - c00135 and c00576 cover 0 forms, and s0085 covers 1.
  - Of the 6 records covering 4 or more forms, only c00701 has a mode table. The report itself says c00021, c00337, s0052 and s0049 use other devices.
  - Of the 53 records covering 3 or more forms, 5 appear in the mode-table list.
  - Independence: c00113 (`gem-designer.agent.md`) and c00430 (`gem-designer-mobile.agent.md`) are one template family (`themes/accessibility.md` pairs them). bpmforge and microsoft each supply 2 records. That is about 11 voices.
- Why high: this is the evidence behind the scorecard's first recommendation. I rated it high because the recommendation's stated basis ("the working form") does not hold. The recommendation may still be a sound design choice on c00681's merits, which is why I am only somewhat sure of the severity.

### 2. "Commit to one direction: 47 from 46" is a widened construct with FD left in (medium)

- Report text: "Commit to one direction: 47 from 46. Offer variants: 35 from 35. Only 5 records say both." (scorecard row 2)
- What is wrong: 47/46 reproduces only if direction-taste `name-direction-concretely` is added to `commit-one-direction` and process `commit-direction-before-building`. Naming a direction concretely is a separate instruction, and the Q4 table lists it separately (14/14). It contributes 9 records, all agents, that are not in either commit theme. The union also keeps all 15 FD records. The report's own Q4 table deflates commit-one-direction from 29 owners to 15 for FD.
- Evidence:
  - Strict commit union (direction commit-one plus process commit-direction): 38 records / 37 owners.
  - Strict union without FD: 24 records / 23 owners.
  - The 47-record union without FD: 32 records / 31 owners.
  - "Only 5 records say both" (c00042, c00158, c00346, s0013, s0112) becomes 4 under the strict definition, because c00042 drops out. c00042 and c00158 are also one lineage (c00158 is a fork), so it is 3 or 4 voices.
- The scorecard should give the strict or deflated figure, or say that it includes "name the direction concretely".

### 3. "At least 44 of 82 say nothing" should be "at most 44" (medium)

- Report text: "At least 44 of those 82 say nothing about a missing tool." (scorecard row 3). Also "So roughly half of the roles that ask for rendering say nothing about the missing tool (at least 44 of 82)." (Q3)
- What is wrong: the arithmetic is 82 − 33 (regex hits) − "at least five more" (hand-read misses) = 44. Because the hand-read added *at least* five, the number of silent roles is *at most* 44. The bound points the wrong way.
- Evidence: the 33 is regex-dependent and not reproducible. A broader regex of mine (not verified, possibly verified, unavailable, no browser or screenshot, fallback, degraded, unable to, and similar) matched 39 of the 82 flagged files. That would put the silent count nearer 38 or fewer. Unsure about the exact figure. Sure about the direction of the bound.

### 4. "The largest cross-cutting construct in the corpus" is not the largest (medium)

- Report text: "The largest cross-cutting construct in the corpus: 173 records from 154 owners have a verified quote for it." (scorecard row 1 and Q3)
- What is wrong: 173/154 reproduces (agents 137/128, skills 36/28), but accessibility is larger on the same kind of evidence.
- Evidence:
  - The accessibility themes alone (`accessibility.assign.json`, all keys) cover 207 records / 185 owners.
  - Adding interaction `reduced-motion`, layout `touch-targets` and visual `readability-baseline` and `minor:touch-targets-44` gives 223 / 194.
  - `claims/accessibility.jsonl` holds 214 records / 189 owners.
  - The accessibility flag is on 291 of 405 records, against 250 for `inspects_existing_ui`.
- Fix: call it "one of the largest", or "the largest construct about process".

### 5. "No single process instruction appears in more than about 15% of owners" uses a different denominator (medium)

- Report text: "Agreement is thin across the whole corpus. No single process instruction appears in more than about 15% of owners (process theme)."
- What is wrong: 15% is 32 of the 215 owners who have any process claim (`themes/process.md`). Of the corpus's 314 owners it is 10%. The sentence says "across the whole corpus", and the report's own figures contradict that:
  - Grounding: 154 of 314 owners (49%).
  - Contrast ratio text: 96 owners (31%).
  - States: 110 owners (35%).
- Fix: say "no single *process-dimension* theme exceeds about 10% of all owners (15% of the owners with process claims)". Drop the claim that agreement is thin across the whole corpus.

### 6. "Agents mostly carry taste inline" is not what the cited figure shows (medium)

- Report text: "**Agents mostly carry taste inline.** 82 agents from 75 owners carry the anti-generic flag, and 34 of those records (31 owners) reference no external file at all, so their taste sits in the role text." The scorecard says "Agents mostly carry their taste inline."
- What is wrong: both numbers reproduce, but 34 of 82 is 41%, a minority. The other 48 flagged agents do reference external files. That does not show their taste lives there, but it does not support "mostly" either. And only 82 of 308 agents (27%) carry the anti-generic flag at all.
- Fix: soften "mostly" to "many", or support it with the close reads (9 of 18 agent close reads have taste inline).

### 7. The "load a named skill" count is presented as agents but includes 5 skills (medium)

- Report text: "**A minority of agents are thin wrappers around a skill.** "Load a named skill or generator first" appears in 18 records from 18 owners, about 16 lineages"
- What is wrong: process `load-named-skill-or-generator-first` is 13 agents / 13 owners plus 5 skills / 5 owners. For agents, the figure is 13 records, 13 owners and 13 − 3 = about 11 lineages. The ui-ux-pro-max family (c00164, s0084, c00395) includes the skill s0084.

### 8. The most-copied comparison is confounded by kind (medium)

- Report text: "The 20 most-copied records render and look in 2 cases (10%), against 80 of the other 385 (21%). Their mean specificity rating is 3.45 against 3.98."
- What reproduces: 2/20, 80/385, 3.45 and 3.98, with no tie at the cut (rank 20 has 15 copies, rank 21 has 14).
- What is wrong: all 20 are agents, and the other 385 include all 97 skills, which render at 39% against 14% for agents. On agents only:
  - The other 288 agents render at 42/288 (15%), with mean specificity 3.83.
  - The top 20 includes c00000, a BMAD activation stub rated 1. Without it the top-20 mean is 3.58.
  - The top 20 is 18 owners (davila7 and wshobson have two each).
- The gap still points the same way, but it is 10% against 15%, not 10% against 21%.

### 9. The AA (96 owners) against AAA (10 owners) contrast split is not two camps (medium)

- Report text: "Contrast target | AA 4.5:1 and 3:1 (96 owners) against AAA 7:1 (10 owners)"
- What is wrong: 7 of the 10 `aaa_or_higher_target` records also sit inside `contrast_ratio_text` (99 records / 96 owners). Several say "AA minimum, AAA preferred" (c00277). Only 3 design records have a claim quoting a 7:1 ratio, and 9 quote "AAA" at all.
- Evidence: the overlap between `contrast_ratio_text` and `aaa_or_higher_target` is 7 records / 7 owners. Claims with "7:1": 3 records / 3 owners.
- Fix: something like "AA 4.5:1 (about 90 owners) vs a 7:1 requirement (3 owners)".

### 10. The ask-or-gate (81/74) against proceed (17/16) ratio is built asymmetrically (medium)

- Report text: "Ask or gate first: 81 from 74, against proceed on stated assumptions: 17 from 16." (scorecard row 2 and Q4 item 8)
- What reproduces: 81/74 is the union of six themes in four dimensions:
  - process `ask-clarifying-questions` and `human-approval-gate`;
  - scope `clarify-or-block` and `human-owns-the-decision`;
  - output `approval-gate`;
  - direction `user-sets-direction-first`.

  17/16 is two themes: process `proceed-on-stated-assumptions` and scope `surface-assumptions-and-open-decisions`.
- What is wrong: the construction is lopsided.
  - 7 records (6 owners) are in both groups, so "against" hides an overlap.
  - Inside the process dimension alone, the comparison is 44 / 41 against 12 / 12.
  - Adding process `record-assumptions-tradeoffs-open-questions` (24 records) to the proceed side gives 36 / 34.
  - The majority direction holds. The 81 against 17 ratio overstates it. Neither side is deflated for families.

### 11. The "11 owners with a design-system role" list is hand-picked and inconsistent (medium, unsure)

- Report text: "11 owners have a design-system role beside another maker: Orkas-AI, bpmforge, ccplugins, expo, google-labs-code, josstei, plugin87, proflead, semaj90, softaworks and verifywise-ai."
- What is wrong:
  - No field or theme yields this list. Only google-labs-code and verifywise-ai have a record in the components theme "Create, document and steward the design system itself".
  - Orkas-AI's candidate, c00517, is a reference file (`ui-reference-packs/references/design-system-packs.md`, "A decision table of 16 neutral design-system archetypes"), not a role.
  - ccplugins is an aggregator. The report calls it one in Limits (4) and removes the aggregators davila7 and microsoft from the neighbouring split count, but keeps ccplugins here.
  - ccplugins' candidate c00059 (brand-guardian) is borderline.
  - A defensible count is about 8 to 10. Unsure of the exact number.

### 12. Variants 35/35 is not deflated for families (low)

- Report text: "Offer variants: 35 from 35." (scorecard row 2)
- Evidence: the union contains the CCGS family (c00017, c00150, c00611), the c00042 / c00158 fork, the c00208 / c00511 "3-5 ASCII mockup variations" pair and the gem-designer pair (c00113, c00430). That is about 30 voices. The Q4 table does deflate the process part (about 17 lineages), but the scorecard does not.

### 13. Other scorecard and Q3 unions are rated "High" without family deflation (low)

- Report text: "**High**: many independent owners". The scorecard rates row (1) High on 173/154, and Q3 rates rendering on 58/52.
- Evidence: the component themes carry deflations the unions drop.
  - Evidence `inspect-existing` goes from 70 to 65 owners.
  - Render-and-look goes from 40 to 36 owners.
  - WCAG baseline is 48 owners but 45 voices (`themes/accessibility.md`). The Q1 table gives 49 / 48.
  - "Implementable handoff specs (18 owners)" is about 14 voices (`themes/output.md`).
  - "Breakpoint sets disagree across 21 owners" includes the agency-agents family (3 owners, one set) and the ClaudeKit family (c00001, c00028; one set). That is about 18 voices, so "about as many sets" overstates the variety.
- None of these changes a conclusion, but the figures are presented as independent owners.

### 14. The zero-form records are not all spec, wireframe or docs roles (low)

- Report text: "The 56 records with none of these forms are spec, wireframe or docs roles."
- Evidence: 9 of the 56 have an empty `outputs` list. A few carry only `visual-asset` or `other` alongside spec (for example spec-or-handoff plus visual-asset).

### 15. The maker/reviewer split comparison counts owners on an any-record basis (low)

- Report text: "14 of the 15 split owners have at least one rendering record. Among the 257 single-record owners, 42 (16%) do, and among the 42 other multi-record owners, 9 do."
- What reproduces: all numbers.
- Caveat: the split owners average 2.8 records each, and jakubkrehel's 6 skills all render. At record level the association still holds within each kind (split-owner agents 10/17 against other agents 34/291; split-owner skills 18/25 against other skills 20/72), so this is wording only.

### 16. The project-design-file regex count is not reproducible (low, unsure)

- Report text: "A broad regex finds 45 agent records from 39 owners that name a project design file (DESIGN.md, tokens.json, design-guideline, STYLE.md, `.interface-design`, a brand spec)."
- Evidence: two readings of that description gave 37 / 31 (literal names) and 75 / 66 (brand spec or guide read loosely). The count depends heavily on the pattern, and the pattern is not recorded.

### 17. c00062 was not copied "unchanged" (low)

- Report text: "a non-existent "MPC (Multi-Page Capture)" tool, copied unchanged into 6 files."
- Evidence: `clusters.json` gives the cluster 2 distinct text members across 6 repositories (`members: 2, repos: 6`). The copies are near-duplicates, not identical.

## Figures that reproduced exactly

- Corpus size: 405 / 314; agents 308 / 254; skills 97 / 68.
- All `stats.txt` rates in the Q1 table and in the flag-by-mode lines.
- Output-form coverage: 56 / 169 / 127 / 47 / 4 / 2 / 0; 352 cover two or fewer.
- Records covering 3 or more forms: 53 / 50. Covering 4 or more: 6 / 6, with the ids as listed.
- Mockup or prototype plus critique: 16 / 15, and 7 / 7 with tokens.
- Mean output tags: 2.7 for agents, 2.5 for skills.
- Mode-table list: 14 / 12.
- Grounding union: 173 / 154 (agents 137 / 128, skills 36 / 28). Evidence inspect-existing: 74 / 70.
- Render union: 58 / 52. Rendering flag: 82 / 65.
- Unverified union: 27 / 26. Unverified overlapping render: 13.
- Anti-generic union: 89 / 82; 74 / 68 without FD. Anti-generic overlapping grounding: 36 / 35.
- Anti-generic flag on agents: 82 / 75. Of those, 34 / 31 reference no external file.
- Self-check: 40 / 37. Separate review: 22 / 19. Both: 1. Return-report: 14 / 11.
- Naming the user: 32 / 32. States: 121 / 110.
- No-production-code: 41 / 40, 39 agents; html-mockup 10%, prototype 7%.
- Production code: 138 / 120. With the boundary flag: 42 / 42.
- Middle position: 48 / 41, 40 agents. With the boundary flag: 41 / 35.
- Handoff to a named implementer: 37 / 35. Defer adjacent specialties: 40 / 34.
- Mode combinations: 168 / 148, 169 / 145 and 62 / 55. 257 single-record owners (82%), 114 of whom make and review.
- The 15 split owners and their render counts; 37 review-only owners; split owners' records are 25 of 42 skills.
- Tool-allowlist table: 24 / 13 / 6 / 1 for agents and 36 / 1 / 1 for skills.
- The Q4 taste table: every records / owners figure, every FD-deflated figure, the lifts (2.2x, 2.3x), 77% and 90%.
- "Purple gradient(s) on white" and "Space Grotesk": 23 owners each.
- Touch target: 44px is the most common value (60 records, against 15 for 48 and 11 for 24).
- Restraint: 12 owners. Purposeful motion: 10 owners.
- Stars and copies for the exemplars. s0037 is 71 lines; s0005 is about 87 KB. 174 of 405 are rated 5.
- c00013: 10 of its copies come from one owner (digitie, by path match).
