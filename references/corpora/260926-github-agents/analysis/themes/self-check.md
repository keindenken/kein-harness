# Self-check dimension: recurring themes

Source: `claims/self-check.jsonl`, all 784 lines read (784 quotes from 550 records, 435 repos, 416 owners). Every quote is from a writing-role agent. Non-English quotes are given verbatim with an English gloss in brackets.

## Method

- Themes were assigned by a regex per theme over the full file. Every theme's hit list was then read by hand, and false positives were removed or missed quotes added by line index (for example, "character" in fiction was matching the length-limit theme, and "todos" in Portuguese was matching TODO). No sampling was done. A quote can belong to more than one theme.
- 137 quotes (63 records that have no other hit) fit no theme. They are generic ("Technical accuracy check", "Validate accuracy and completeness") or domain-specific (WCAG contrast, OpenAPI operationIds, frontmatter fields, clinical coding).
- Counts are distinct records / distinct repos / distinct owners. "Voices" is a second owner count that treats a confirmed template family as one voice. A family was confirmed from `clusters.json` file names plus identical wording:
  - ECC `doc-updater`: affaan-m (7 translated copies), sangrokjung, 0xb7a7dd61
  - agency-style `engineering-technical-writer`: monoes, imMamdouhaboammar, Olatisunkanmi
  - awesome-copilot `gem-documentation-writer`: github, borgius, melnikov1512
  - `docs.agent.md` Pages template: Dao-AILab, CalaW
  - oh-my-claudecode `writer`: Yeachan-Heo, LimiNode
  - `technical-writer` with "Readability score > 60": davila7, jtgsystems
  - awesome-copilot `update-docs-on-code-change`: ibragimov-oasis, hoangsonww
  - Chinese `technical-writer` preset: liaoxinjie666, xuanbingbingo
- "Lift" is a doc type's share among the theme's records divided by its share among all 550 self-check records. 1.0 means no concentration.
- `copies_in_repos` was not used as a weight. A 72-copy file is still one voice.

## 1. Top recurring themes (ordered by distinct owners)

| # | Theme | Records | Repos | Owners | Voices |
|---|---|---|---|---|---|
| 1 | Code examples are run or compiled | 80 | 67 | 67 | 63 |
| 2 | The self-check blocks "done" | 57 | 53 | 53 | 53 |
| 3 | Run the repo's own validators (lint, build, type-check) | 56 | 53 | 53 | 53 |
| 4 | Links, anchors and cross-references resolve | 56 | 51 | 51 | 49 |
| 5 | Coverage against an enumerable source, counts match | 52 | 45 | 44 | 44 |
| 6 | Mark what is unverified or inferred | 51 | 45 | 43 | 42 |
| 7 | Every statement checked against current code | 42 | 41 | 40 | 38 |
| 8 | Report the check back beside the deliverable | 44 | 42 | 39 | 39 |
| 9 | Commands, steps and paths executed or shown to exist | 42 | 33 | 33 | 31 |
| 10 | Newcomer or cold-read test | 35 | 30 | 30 | 29 |
| 11 | Read back the actual written output | 30 | 29 | 29 | 29 |
| 12 | Cross-document consistency | 27 | 27 | 27 | 27 |
| 13 | Staleness and drift check | 22 | 22 | 22 | 22 |
| 14 | Scan for AI-writing tells or banned words | 20 | 20 | 20 | 20 |
| 15 | Read aloud, or ask "does it sound like the author?" | 19 | 18 | 18 | 18 |

Just below the cut, by owners:
- Self-scored numeric thresholds: 29 / 18 / 18, 16 voices
- No placeholders or TODO left: 22 / 18 / 18, 17 voices
- Every claim or number cited: 21 / 17 / 17
- Requirements are testable: 17 / 16 / 16
- No invented content: 16 / 15 / 15
- Cut check ("is every sentence necessary?"): 15 / 14 / 14
- Length or character limits: 11 / 11 / 11
- Scope and edit-boundary check: 9 / 9 / 9
- Adversarial self-review: 9 / 8 / 8
- No secrets or personal data: 8 / 8 / 8

### 1. Code examples are run or compiled before they ship
Every code sample is executed or compiled. A sample that cannot be run is marked or removed.
- Counts: 80 records, 67 repos, 67 owners (63 voices).
- Doc types: code docs. project-docs 96% of records, api-reference 90% (lift 2.2), changelog and code-comments lift about 2.2.
- Quotes:
  - "STOP. Does this example actually compile/run? If you haven't tested it or verified the imports exist, it's fiction, not documentation." (c00718)
  - "Code example testing: Before including a code example, verify it runs (`python -c` or `curl`); mark untested examples with ⚠️" (c00384)
  - "If a block cannot be made to run, it does not belong on the page" (c01001)

### 2. The self-check blocks "done"
Run the check explicitly, item by item, before declaring complete, committing or returning. Do not claim completion until it passes.
- Counts: 57 records, 53 repos, 53 owners (53 voices). This is a framing theme that overlaps the others: it records how the check is enforced, not what it checks.
- Doc types: none. project-docs lift 0.9, prd-spec and changelog 1.3.
- Quotes:
  - "Before declaring documentation complete, execute this checklist literally as actual tool invocations" (c00718)
  - "voice guide compliance must be checked rule-by-rule, not holistically" (c00526)
  - "Do NOT claim the writing task is complete until you have invoked the docs-release-readiness skill and it passes with zero errors." (c01302)

### 3. Run the repository's own validators and treat failure as not done
Examples of validators: markdown lint, docs build, type-check, Vale, Spectral, a project script.
- Counts: 56 records, 53 repos, 53 owners (53 voices). Nearly every owner names a different command, which is strong evidence that the owners wrote these independently.
- Doc types: 32 of 56 records are single-type. project-docs 64% (lift 1.1). No type dominates.
- Quotes:
  - "**A docs change is not done until `npm run build` passes.** Docusaurus fails the build on broken internal links, which is exactly the error prose reviews miss." (c01100)
  - "The OpenAPI specification must pass Spectral linting with zero errors and zero warnings before publication." (c00118)
  - "After editing a page run `npm run lint:vale <path_to_file>` to make sure that your changes respect the standard imposed by the vale configuration." (c01061)

### 4. Links, anchors and cross-references resolve
- Counts: 56 records, 51 repos, 51 owners (49 voices).
- Doc types: project-docs 96% (lift 1.6), changelog lift 1.8, api-reference lift 1.5.
- Quotes:
  - "Does NOT invent link targets to pages that do not exist; internal documentation links must resolve, so broken links are treated as build failures." (c00738)
  - "Confirm heading IDs match anchor references" (c00167)
  - "**README cross-links:** every `[text](FOO.md)` resolves; every section reference exists." (c01323)

### 5. Coverage against an enumerable source, with counts that match
Every endpoint, requirement, finding or required section is present, and totals reconcile with the source.
- Counts: 52 records, 45 repos, 44 owners (44 voices).
- Doc types: prd-spec (lift 2.0), report-analysis (1.7), api-reference 44%.
- Quotes:
  - "STOP. Count the endpoints in source vs endpoints in your doc. If they don't match, you missed something or invented something." (c00718)
  - "Completeness Self-Check: After generating, count unique finding IDs in the appendix vs. `threats.md` Sections 3 + 4 + 4a. Counts must match exactly." (c00925)
  - "Coverage Summary table totals match the per-level test counts" (c01163)

### 6. Mark what could not be verified, in place, and label inference as inference
Labels used include UNVERIFIED, NEEDS CITATION, hypothesis, and stated limitation.
- Counts: 51 records, 45 repos, 43 owners (42 voices).
- Doc types: report-analysis lift 2.5 (29% of records). Otherwise spread.
- Quotes:
  - "Distingue afirmaciones verificadas de inferencias. Si infieres comportamiento, dilo: "Inferido del código en src/auth.ts:120; no probado en entorno real."" [Distinguish verified claims from inferences. If you infer behavior, say so: "Inferred from the code at src/auth.ts:120; not tested in a real environment."] (c00201)
  - "Never write a code sample you are not confident compiles. If unsure of a signature, say so in `UNCERTAIN` rather than guessing silently" (c01132)
  - "Label mapping explanations as hypotheses. Do not present a paired comparison as causal proof." (c01326)

### 7. Every statement is checked against the current code
The check runs after writing, by re-reading the source. Nothing is written from memory.
- Counts: 42 records, 41 repos, 40 owners (38 voices).
- Doc types: project-docs 90% (lift 1.5), changelog lift 1.9, api-reference lift 1.5.
- Quotes:
  - "Every statement in those pages traces to code you read." (c00096)
  - "Verify accuracy: After writing, re-read the implementation or trace the code path to confirm every claim is accurate." (c00278)
  - "does any doc claim something the code contradicts?" (c00175)

### 8. Report the check back beside the deliverable
The report covers how claims were verified, the decisions made, what was skipped or left unverified, and sometimes a confidence level.
- Counts: 44 records, 42 repos, 39 owners (39 voices).
- Doc types: no code-doc concentration. academic lift 2.4, other 1.6, api-reference 0.5.
- Quotes:
  - "Verification: how you confirmed technical claims (commands/files read)." (c00964)
  - "The validation scripts were run and their real last lines are in the description." (c00388)
  - "Points where you had to make a judgment call, or contradictions found between code and docs" (c01397)
- Where the note goes varies and was not counted:
  - A separate file: "After writing, save a self-report to `manuscript/chapters/chapter-[N]-report.md`" (c00076), and "Write `.planning/<phase>/DOCS.md` -- a diff summary listing every file touched + a checklist of human-review items" (c00758).
  - Inside the deliverable: "state them in one sentence at the very end after a `---` divider" (c00112), and "{Any uncertainties, assumptions, or follow-ups for human reviewers.}" as a template field (c00636).

### 9. Every command, step and file path is executed or shown to exist
Methods include `ls`, `--help`, and walking through the steps in a clean environment.
- Counts: 42 records, 33 repos, 33 owners (31 voices).
- Doc types: api-reference 71% (lift 1.8), project-docs 90% (lift 1.5).
- Quotes:
  - "Verify commands work: build commands listed in docs must match actual Makefile targets" (c01563)
  - "Test every instruction by following the documented steps literally on a clean environment and noting where the documentation assumes knowledge it should provide" (c00042)
  - "Каждый показанный пример команды прогони или сверь с `--help`; каждый путь и имя символа проверь, что существует." [Run every shown command example or check it against `--help`; check that every path and symbol name exists.] (c01276)

### 10. Newcomer or cold-read test
Ask whether someone new, or an agent with no context, can complete the task from this document alone. The test is often timed at 5 or 10 minutes.
- Counts: 35 records, 30 repos, 30 owners (29 voices).
- Doc types: api-reference 74% (lift 1.8), prd-spec lift 1.6.
- Quotes:
  - "If a new user lands on this page cold, can they complete the named task without leaving the page or asking for help?" (c00360)
  - "The PRD must be self-contained: a fresh Claude session with only this PRD can implement the feature" (c00294)
  - "Test readability — would a coding agent with no prior context produce correct code from this doc alone?" (c00088)

### 11. Read back the actual written output, not the draft in mind
The output to read is the saved file, the diff or the persisted body.
- Counts: 30 records, 29 repos, 29 owners (29 voices).
- Doc types: spread. other lift 2.0, report-analysis 1.7, academic 2.6 (3 records).
- Quotes:
  - "MUST immediately use the Read tool on the saved file to confirm it exists and reflects the generated drafts." (c00794)
  - "Complete Read-Back Required: After writing documentation, read the ENTIRE output." (c01372)
  - "Re-fetch the PR and confirm persisted body contains all template headings and checklist items." (c00361)

### 12. Cross-document consistency
Terminology, versions, paths and statements agree across related docs and across language versions.
- Counts: 27 records, 27 repos, 27 owners (27 voices).
- Doc types: prd-spec lift 1.6. Otherwise spread.
- Quotes:
  - "Cross-document consistency: Related docs do not conflict on behavior, status, commands, or file paths" (c00316)
  - "Cross-reference consistency — file paths, URLs, version numbers, and config keys must match across all docs." (c01192)
  - "double-check that each section in English has its counterpart in each other language, and that they match in content" (c00300)

### 13. Staleness and drift check
Check for stale references, outdated screenshots and versions, deprecated items left unmarked, and anything that will go stale.
- Counts: 22 records, 22 repos, 22 owners (22 voices).
- Doc types: changelog lift 2.9, code-comments 2.8, api-reference 2.1. project-docs is 100% of records.
- Quotes:
  - "No stale references to renamed or removed functionality" (c00314)
  - "Is this going to go stale? — Avoid hardcoding versions or paths that will change" (c00637)
  - "Compare doc claims (endpoint counts, LOC) against current codebase; flag docs >7 days out of sync" (c00384)

### 14. Scan the draft for AI-writing tells or banned words
The scan is often done with grep or a script, and hits are replaced.
- Counts: 20 records, 20 repos, 20 owners (20 voices).
- Doc types: blog-article lift 4.4, fiction-narrative 3.9, other 2.5, marketing-copy 2.3.
- Quotes:
  - "forbidden.md 단어 사용 전 grep 자가 점검. 발견되면 즉시 치환." [Before using words from forbidden.md, self-check with grep. Replace immediately if found.] (c01084)
  - "grep -n "the [a-z]* to\|value of\|represents the\|specifies the" docs/**/*.md" (c00717)
  - "Reread the body once, only hunting banned patterns and register drift. Fix what you find." (c00268)

### 15. Read aloud, or ask "does it sound like the author?"
Rewrite where the reader stumbles.
- Counts: 19 records, 18 repos, 18 owners (18 voices).
- Doc types: social-media lift 6.2, marketing-copy 4.8, blog-article 4.7, fiction-narrative 4.1. project-docs 0.4.
- Quotes:
  - "Read it aloud. If you stumble, rewrite." (c01549)
  - "Read your copy out loud. If you would never say it in a bar, a boardroom, or a text to a friend (depending on context), rewrite it." (c00394)
  - "每一段成稿都问一句：这话作者本人会这么说吗。不会，就退回声音档案重写。" [For every finished paragraph ask: would the author actually say this? If not, go back to the voice profile and rewrite.] (c01626)

## 2. Lineage warnings

- **ECC `doc-updater` (affaan-m, sangrokjung, 0xb7a7dd61).** It contributes 9 records to themes 1, 4, 7 and 9. Seven of them are affaan-m's translations of one file (es, ko, pt-BR, tr, zh-CN, zh-TW, kiro). It is the largest owner in theme 9: 7 of 42 records, one voice. Theme 9 falls from 33 owners to 31 voices, and about a sixth of its records are one file.
- **UitbreidenOS.** One documentation-engineer file appears in 5 languages (c01411 to c01415). That is 5 of 35 records in theme 10 and 5 of 22 records in "no placeholders", counted once as an owner.
- **tiny-flowlab (novel-studio, Korean and English mirrors).** It holds 10 of 29 records in the self-scored-threshold theme ("Show/Tell ratio: 80/20 or higher", "Naturalness: 8/10 or higher"), plus 2 in theme 15. This is why numeric self-scoring looks bigger by records (29) than by owners (18). Without tiny-flowlab and borghei (3 records), 16 records remain. The gem family ("If confidence < 0.85 …", c00066 and c00098) and the "Readability score > 60 achieved" family (c00005 and c00780) cut the theme further, to 16 voices.
- **taxideftis.** The same agents are mirrored in `.claude/_base`, `.claude` and `.codex` (c01180 to c01184). They contribute 5 records to theme 6, 4 of 21 to "every claim cited", and 3 to theme 8. The cited-sources count (17 owners) is solid, but its record count is inflated.
- **Template families in theme 1.** The agency-style `engineering-technical-writer` (c00131 and c00323 carry "Code examples must run — every snippet is tested before it ships"), the awesome-copilot `update-docs-on-code-change` text (c00425, c00426, c00432: "Code examples are tested and work"), and the oh-my-claudecode `writer` (c00183 and c00508: "If examples cannot be tested, explicitly state this limitation") remove 4 voices, from 67 to 63. Short checklist lines such as "Code examples tested and working" (jmagly and unisone) converge on identical wording without a shared source, so they were not merged.
- **Theme 10.** The Chinese technical-writer preset (c00068 and c00909: "用不熟悉该项目的开发者进行用户测试" [user-test with a developer unfamiliar with the project]) is one voice.
- **Copy counts.** Themes 4 and 10 carry high `copies_in_repos` totals (180 and 166), mostly from c00003 (github/awesome-copilot, 72 copies). This affects reach, not independence.
- **kcenon.** One SDLC pipeline supplies 4 of 52 records in theme 5.

## 3. Sharp but rare (1 owner each, precise enough to adopt)

1. "Distingue afirmaciones verificadas de inferencias. Si infieres comportamiento, dilo: "Inferido del código en src/auth.ts:120; no probado en entorno real."" [Distinguish verified claims from inferences. If you infer behavior, say so: "Inferred from the code at src/auth.ts:120; not tested in a real environment."] (c00201, DPG210). The label names both the evidence location and the method that was not used.
2. "Invented interior texture (a mood, the weather at their window) is allowed and must be listed at the end under `texture:` — one line per invention." (c01226, nagisanzenin). A ledger of invented material. The same record has "Fix and re-run until green, up to 3 revisions; if still failing, keep the best version and report the failing check honestly."
3. "변경률 50% 초과: 작업 중단, 마지막 안정 버전으로 롤백, `over_polish_warning: true`." [Change rate over 50%: stop, roll back to the last stable version, `over_polish_warning: true`.] (c00126, msbaek). A mechanical guard against over-editing. The same record flags changes over 30%.
4. "Word count — did the total word count go up? If yes, what was removed to compensate? Document the trade-off." (c00242, microsoft). Makes cutting the default in a checkable form.
5. "Verify completeness with `grep -r "old_term" documentation/ flexmeasures/` before and after — it should return zero matches afterward except in a changelog entry" (c00762, FlexMeasures).
6. "Before returning, check version-control status for anything your run touched: you hold Bash, so prove the read-only claim rather than asserting it" (c01283, riekelt).
7. "If the write fails, say it failed. Do not claim draft persistence." (c00794, LilMGenius)
8. "If the recent changes only need generated-catalogue refresh or need no docs change at all, say so and stop without inventing prose." (c01618, timmo001). "No document" is a valid output.
9. "State coverage honestly: what surface was reviewed, what was not, and where recall is uncertain." (c00212, deonmenezes)
10. "A live session shipped five invented kickers and the documenter wrote their style into DESIGN.md; that is how one violation becomes the house style." (c00950, GulajavaMinistudio). This bears directly on merging outside examples: a pattern seen in a draft is not evidence that the pattern is right.

A few rare instructions argue against self-scoring. They are too few to count as a theme:
- "No trailing self-review of "what I just wrote". The copy is the output." (c01260)
- "不自测字数句长（不跑 wc、不写统计脚本，短了也不据此重写）。" [Do not self-measure word count or sentence length: no wc, no stats script, and do not rewrite because it came out short.] (c00538)
- "変更の行数は判定に使わない" [Do not use the changed-line count for judgment] (c00935)
- "Do not assign a score or letter grade." (c00104). This one is for review mode.

## 4. Bearing on the PROPOSED WRITER

### Point 1: start from the reader and what they will do
- **Supports.** Theme 10 (30 owners) is the operational form of this point. Its test is a task, not an audience description: "can they complete the named task without leaving the page" (c00360), and "a fresh Claude session with only this PRD can implement the feature" (c00294).
- **Adds.** The proposal states reader-first as a starting stance. The corpus turns it into a self-check that runs after writing: a cold re-read or a literal walk-through. It is timed in several places (5 or 10 minutes), and one owner watches a real person read. The role could state the check as: "name the reader's task, then re-read cold and confirm the task can be done from this document alone."
- **Concentration.** 74% of theme 10's records are api-reference, so in this corpus the test is mostly used for code docs.

### Point 2: every factual sentence traceable to evidence, interpretation marked
- **Strongly supports.** Six of the top 9 themes are evidence checks: themes 1, 4, 5, 6, 7 and 9. The four mechanical themes (1, 3, 4, 9) together cover 189 records and 165 owners.
- **Interpretation marked.** Theme 6 (43 owners) directly supports it, with concrete label formats (c00201, c01132, c01326).
- **Contradicts the "one general role" framing only partly.** The evidence *checks* are strongly type-specific:
  - Code docs: run examples, resolve links, check paths, check staleness (project-docs and api-reference at 90 to 100%).
  - Reports and academic writing: cite every claim or number (lift 5.7 and 7.5).
  - PRDs: testable acceptance criteria (16 of 17 records are prd-spec).

  This fits the proposal's plan to carry type differences in path-scoped rules. Theme 3 fits especially well, since nearly every owner names a different repo-specific command. The role itself should hold only the type-independent part: trace to evidence, mark inference, and report what was not verified.
- **Adds.** The corpus has a verification-method axis the proposal's tiers lack: executed or compiled, then read in source, then inferred, then unverified (c00201, c00384, c01333 "Tested code examples work (or noted they are illustrative)"). The proposal's tiers (measured in runs, vendor documentation, recurring across independent sources, a single source) rank the source of a claim, not how the writer checked it. The ledger could carry both columns.

### Point 3: cutting as default, working notes go to a separate output
- **Cutting.** Weakly represented in this dimension. The cut check has 14 owners and falls below the top 15. c00242 (word count must not rise without a documented trade-off) is the most operational form. Cutting may be stronger in another dimension; here the corpus checks correctness far more than concision.
- **Separate output: supported.** Theme 8 (39 owners) shows that returning verification notes, decisions and skipped items to the caller is common.
- **Separate output: contradicted in practice.** Where the note goes is split. Some roles write it into the deliverable (c00112, a note after a `---` divider; c00636, a PR-body field). c01260 ("The copy is the output") is the one explicit statement of the proposal's rule. Where to put the notes is the contested part.

### Ledger, and "does not judge its own quality"
- **Supports the ledger.** Themes 8 and 6 are an informal ledger. c01226's `texture:` list and c00964's "Verification: how you confirmed technical claims (commands/files read)" are the closest single-owner analogs.
- **Supports "does not judge its own quality".** Numeric self-scoring (18 owners, 16 voices, inflated by tiny-flowlab) and confidence reports (9 records, 9 owners, 8 voices; one of them is not a score) are minority practices. They are concentrated in fiction and marketing, and several rare quotes reject them. Independent final checks also appear: "One independent final verifier checks audience fit, structure, completeness, clarity, and every material claim against its source, then executes examples in the real environment." (c00641); "落盘 OUTPUT_PATH 后由调用方做确定性小节校验，缺节会退回重写。" [After writing OUTPUT_PATH, the caller runs a deterministic section check and sends it back for rewrite if sections are missing.] (c01474).
- **Needs one distinction.** The corpus's strongest self-checks are mechanical verifications (run it, build it, resolve it, count it), not quality judgments. If "does not judge its own output" is read as "does no self-check", the role drops the corpus's top themes. The proposal should say that the writer runs checks of facts and mechanics and reports their results, while quality verdicts belong to runs and evals.

### What this dimension has that the proposal lacks
- **A definition of done** (theme 2, 53 owners). The self-check is a blocking gate run item by item. Three roles bound the revision loop: "max 2 loops" (c00098), "up to 3 revisions … keep the best version and report" (c01226), "retry exactly once" (c01553).
- **Read back what was actually written** (theme 11, 29 owners), and check the edit boundary with `git status` or a diff: "prove the read-only claim" (c01283; scope theme, 9 owners).
- **Honest reporting of the check itself.** Examples: "If the write fails, say it failed" (c00794), "Never suppress a check." (c01317), and "Reporting synthesis as passing when warnings exist. Instead: parse and report all warnings." (c01034). The ledger should record failed and skipped checks, not only kept claims.
- **Coverage and count reconciliation** (theme 5, 44 owners). This is a completeness check that the evidence-per-sentence rule does not cover: every sentence can be traceable while an endpoint is still missing.
- **Consistency across documents and drift** (themes 12 and 13). These are checks against sibling documents, not against evidence.
- **"No change needed" as a valid result** (c01618). A writer given a brief should be allowed to return that finding instead of prose.
