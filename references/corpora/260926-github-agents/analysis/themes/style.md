# Style dimension: recurring instruction themes

Source: `claims/style.jsonl`, all 1,162 lines read in full (no sampling). They come from 656 distinct records, 536 repos and 513 owners.

Method: a first pass tagged lines by keyword pattern. Then every hit was reviewed by hand, and lines were added or removed. Lines the patterns missed but a full read turned up were added. The final line lists are in `final.py` in the session scratchpad and are not in the repo. One quote can count toward several themes, for example "Use active voice, direct language, no filler words." counts for both active voice and filler.

How to read the numbers:
- Counts are distinct records / repos / owners.
- "Voices" is the owner count after merging owners whose quotes in the theme are near-identical text (difflib ratio > 0.85, at least 12 normalized characters). It is a rough lower bound on independent sources.
- Doc-type "lift" is the theme's share of records carrying that type, divided by the share across all 656 style records. Lift above 1 means the theme is concentrated in that type. Records carry several types, so the shares add up to more than 100%.

## 1. Top recurring themes (ordered by distinct owners)

| # | Theme | Records | Repos | Owners | Voices |
|---|---|---|---|---|---|
| 1 | Cut filler, throat-clearing, preamble; every word earns its place | 88 | 87 | 85 | 79 |
| 2 | No marketing/hype language; banned buzzword lists | 66 | 62 | 61 | 59 |
| 3 | Examples over prose; examples must be real, runnable, copy-pasteable | 66 | 63 | 61 | 59 |
| 4 | Specific and quantified over vague | 65 | 63 | 60 | 60 |
| 5 | Match the existing project voice, format and conventions | 63 | 60 | 60 | 57 |
| 6 | Active voice | 49 | 47 | 45 | 36 |
| 7 | Explain why, not what; do not restate the code | 42 | 41 | 39 | 33 |
| 8 | Output-language / locale mandate | 39 | 37 | 37 | 37 |
| 9 | Imperative, verb-first instructions, titles and commit subjects | 30 | 30 | 30 | 29 |
| 10 | Ban or cap em dashes | 28 | 28 | 28 | 28 |
| 11 | Address the reader as "you" | 25 | 25 | 24 | 23 |
| 12 | Define jargon, acronyms and terms on first use; plain language | 24 | 24 | 24 | 22 |
| 13 | Calibrate claims: no overclaiming; separate fact from assessment and shipped from planned | 26 | 23 | 23 | 23 |
| 14 | Ban minimizers ("simply", "just", "obviously", "easy") | 25 | 20 | 20 | 20 |
| 15 | Lists, tables and structure over walls of text | 20 | 20 | 20 | 19 |

Below the cut, by owners: numeric readability targets (Flesch score, grade level, sentence-length caps) 19; emoji banned or limited 19; consistent terminology 19; sound human, not AI (anti-slop) 19; preserve the author's voice when editing 18; lead with the outcome or finding 18; present tense 17; no hedging 17; actionable recommendations 17; sentence-case headings 14; realistic data, not foo/bar 14; diagrams/Mermaid 12; descriptive link text and alt text 11; timeless docs with no process history 9; follow a named external style guide (Google, Microsoft, NHS, Strunk) 8; fiction craft (show don't tell, "said", clichés) 7; language hint on code fences 5; no Latin abbreviations 4.

### 1. Cut filler, throat-clearing and preamble (85 owners)
Instruction: delete words, sentences and framing paragraphs that carry no information: intros, recaps, "it should be noted", verbal fat.
Counts: 88 records, 87 repos, 85 owners (79 voices).
Concentration: spread across types. Mild lift in code-comments (1.7), changelog (1.4) and academic (2.1); project-docs 68% of records (lift 1.2).
- c00239: "Every sentence must earn its place. No filler, no hedging, no \"it should be noted that.\""
- c01072: "Cut throat-clearing (\"It's important to note,\" \"In order to,\" \"This section will cover\") and never restate a fact for emphasis."
- c01047: "No preamble, no closing prose."

### 2. No marketing/hype language; banned buzzword lists (61 owners)
Instruction: do not use promotional adjectives or "AI-tell" vocabulary (powerful, seamless, robust, leverage, delve...). Say what the thing does.
Counts: 66 records, 62 repos, 61 owners (59 voices).
Concentration: marketing-copy (lift 3.2), ux-microcopy (2.5) and blog-article (1.9). Most anti-hype rules sit inside marketing agents themselves. It is also present in project-docs (53% of records, lift 1.0).
- c00239: "No marketing language. Don't say \"powerful\" or \"robust\" — describe what it does and let the reader judge."
- c00888: "Banned adjectives: *revolutionary, seamless, cutting-edge, blazing-fast, next-gen, game-changing, powerful, magical, effortless, delightful, beautiful, amazing, incredible*."
- c01361: "Avoid filler such as \"seamless\", \"powerful\", \"robust\", or \"easy\" unless the claim is specific and demonstrated."

### 3. Examples over prose; examples must work (61 owners)
Instruction: show with code or concrete examples before or instead of describing. Examples must be complete, runnable and copy-pasteable, with expected output.
Counts: 66 records, 63 repos, 61 owners (59 voices).
Concentration: api-reference (lift 1.8) and project-docs (1.5, 85% of records). Low in prd-spec (0.6).
- c00884: "show_code > describe_code | when_both → code_first_then_brief_explanation"
- c00065: "Code examples must be complete and runnable"
- c00088: "No \"...\" elision — show every required field, even if the example is longer"

### 4. Specific and quantified over vague (60 owners)
Instruction: replace vague words with exact names, numbers, paths and observable behavior. Several quotes give a fail/pass pair.
Counts: 65 records, 63 repos, 60 owners (60 voices).
Concentration: report-analysis (lift 2.2) and prd-spec (1.5). Under-represented in api-reference (0.4) and project-docs (0.6), where theme 3 carries the same idea.
- c00294: "\"Works well\" is NOT acceptable. \"Login with invalid password returns 401 and error message\" IS acceptable."
- c00870: "Fail: \"three-level policy\", \"configured threshold\", \"see constants\". Pass: `15%`, `10%`, `14 days`, `1_000_000` minor units."
- c01116: "Specific numbers (\"3.4 ETH\", \"~$12K\") over adjectives (\"significant\")."

### 5. Match the existing project voice and conventions (60 owners)
Instruction: read neighboring docs, or a named voice or brand file, before writing, and match their tone, structure, terminology and formatting instead of imposing a new style.
Counts: 63 records, 60 repos, 60 owners (57 voices).
Concentration: project-docs (75%, lift 1.3) and changelog (1.5). Otherwise fairly even across types.
- c00694: "Match existing style. Detect tone, structure, formatting from neighboring docs. Don't impose your own."
- c01129: "Read the affected doc sections *before* editing; match their voice and format exactly — terse, factual, tables for module maps, one-line \"File | What\" entries, dates as YYYY-MM-DD."
- c01447: "No existing house style → Google developer style defaults: second person, present tense, active voice, sentence-case headings."

### 6. Active voice (45 owners)
Instruction: use active voice. Some quotes give a numeric cap on passive voice.
Counts: 49 records, 47 repos, 45 owners (36 voices, the largest drop from shared wording; see §2).
Concentration: changelog (2.5), code-comments (2.1) and api-reference (2.0). Often bundled in one line with "second person, present tense" (the Google developer-style triad).
- c00003: "Active voice: \"The function processes data\" not \"Data is processed by the function\""
- c00448: "sentences starting with \"There is\" or \"There are\" rewritten to active subject-verb"
- c01229: "No passive voice overuse (under 20%)"

### 7. Explain why, not what; do not restate the code (39 owners)
Instruction: comments and docs carry intent, constraints and gotchas the code cannot show. Restating names, signatures or obvious behavior is deleted.
Counts: 42 records, 41 repos, 39 owners (33 voices).
Concentration: code-comments, strongly (74% of records, lift 5.1), then api-reference (1.8).
- c00840: "코드를 읽으면 아는 것은 쓰지 않는다. 코드만으로는 알 수 없는 것을 쓴다." ("Do not write what reading the code tells you. Write what the code alone cannot tell you.")
- c00638: "Explain intent, constraints, gotchas, and relationships to other code. The reader can see the \"what\" from the code; give them the \"why.\""
- c01055: "Start from the premise that **every comment added in the PR should be removed.**"

### 8. Output-language / locale mandate (37 owners)
Instruction: write the deliverable in a fixed language or spelling variant (English only, Japanese, zh-CN, pt-BR, British/US spelling), often separate from the chat language. Several say it must be native, not translated.
Counts: 39 records, 37 repos, 37 owners (37 voices).
Concentration: none notable (project-docs lift 1.0; code-comments 1.6).
- c00098: "all documentation must be written in English only, regardless of the chat language used to request it"
- c01358: "Spanish quality: ES content must be natural, professional Spanish — not machine-translated English"
- c01139: "FR is written as French, not translated from English. French business register is more formal and more precise than its English equivalent."

### 9. Imperative, verb-first instructions, titles and commit subjects (30 owners)
Instruction: steps, button labels, issue/PR titles and commit subjects start with a bare verb ("Add", "Run"), not "You should..." or "Added".
Counts: 30 records, 30 repos, 30 owners (29 voices).
Concentration: changelog (2.0) and prd-spec (1.6). In prd-spec this covers ticket and issue titles.
- c00980: "Use the imperative for instructions: \"Create the file\", not \"You should create the file\""
- c01492: "Start with a verb: \"Add\", \"Fix\", \"Refactor\", \"Update\", \"Remove\""
- c01599: "Write subjects in imperative tense, lowercase, no period, max 100 characters"

### 10. Ban or cap em dashes (28 owners)
Instruction: no em dashes, or a numeric cap per paragraph or post. Some quotes give the replacement punctuation. Several frame this as an "LLM pattern".
Counts: 28 records, 28 repos, 28 owners (28 voices). No shared wording was found, so this looks like independent convergence.
Concentration: blog-article (lift 4.0), "other" (2.5) and marketing-copy (1.8). Project-docs is only at 0.8.
- c01072: "No em-dashes, anywhere. Use a period, comma, colon, or parentheses instead."
- c01164: "Never use em-dashes (`---`). Rewrite every em-dash as one of: a separate sentence, a parenthetical in `(...)`, a colon, or a comma."
- c00394: "Maximum one em dash per paragraph"

### 11. Address the reader as "you" (24 owners)
Instruction: use second person, not "we" or "the user". A minority splits by mode: second person for guides, third person for reference.
Counts: 25 records, 25 repos, 24 owners (23 voices).
Concentration: social-media (3.6), ux-microcopy (3.3), api-reference (1.9) and changelog (1.9).
- c00972: "Use the second person (\"you can...\") not first person plural (\"we recommend...\")"
- c01023: "Second person for guides (\"You can configure...\"), third person for reference (\"The endpoint accepts...\")"
- Counter-instruction, c00095: "不使用第一人称或第二人称，包括\"我\"\"我们\"\"你\"\"你的\"\"你们\"等称呼。" ("Use neither first nor second person, including forms such as 'I', 'we', 'you', 'your'.")

### 12. Define terms on first use; plain language (24 owners)
Instruction: expand acronyms, gloss domain terms at first use, avoid unexplained jargon.
Counts: 24 records, 24 repos, 24 owners (22 voices).
Concentration: changelog (2.2), project-docs (1.3) and prd-spec (1.3).
- c00710: "Gloss every domain term in place at first use."
- c00104: "Spell out an abbreviation on its first use in each document, followed by the abbreviation in parentheses. Use the abbreviation alone afterward."
- c01585: "Define before use. Every symbol, metric, and method name gets a definition on first use."

### 13. Calibrate claims (23 owners)
Instruction: do not overclaim or exaggerate. Keep observation apart from assessment, guarantee apart from goal, shipped apart from planned. Hedge only where there is real uncertainty, and state it once.
Counts: 26 records, 23 repos, 23 owners (23 voices).
Concentration: report-analysis (lift 2.9), academic (2.7) and prd-spec (1.8).
- c01233: "Distinguish facts from assessments — \"we observed\" vs \"we assess\""
- c01277: "Честно называй, что гарантия, а что цель." ("Honestly name what is a guarantee and what is a goal.")
- c00493: "One clear statement of a caveat beats three softened ones."
- c01116: "\"Could be\" / \"may be\" only when actually uncertain. Don't soften real bugs."

### 14. Ban minimizers (20 owners)
Instruction: do not write "simply", "just", "obviously", "easy" or "clearly". The usual reason: they belittle readers who find the step hard, and in proofs they hide a missing step.
Counts: 25 records, 20 repos, 20 owners (20 voices). The record count is inflated by one owner (see §2).
Concentration: academic (lift 3.7), api-reference (1.9) and changelog (1.6).
- c00323: "No \"simply\" or \"just\" — if it were simple, they wouldn't need documentation"
- c00707: "Never write \"clearly\", \"obviously\", \"standard argument\", \"similarly\", or \"one checks\" in place of a mathematical step."
- c00357: "Avoid: \"Simply,\" \"Just,\" \"Obviously,\" \"Easily\"—these minimize user struggles."

### 15. Lists, tables and structure over walls of text (20 owners)
Instruction: prefer bullets, tables and headings to dense paragraphs, because readers scan.
Counts: 20 records, 20 repos, 20 owners (19 voices).
Concentration: prompt-instructions (lift 3.9, small n), changelog (1.7) and project-docs (1.3).
- c01625: "结构化优先于叙述：能用表格和清单的地方不写大段文字。PRD 是给人照着干的说明书，不是读后感。" ("Structure over narrative: where a table or checklist works, do not write long paragraphs. A PRD is a manual people follow, not a book report.")
- c01103: "Bold the load-bearing phrase of a paragraph so a skimmer gets the argument from the bold alone."
- Counter-instruction, c01427: "Reducing the amount of bullet point lists and replace them with natural and flowing paragraphs"

## 2. Lineage warnings

Record counts that are inflated by one owner. Owner counts are not affected, but record totals and per-type shares are.
- **UitbreidenOS**: one rule translated into five languages as five records (c01411–c01415, DE/EN/ES/FR/NL). That is 5 of 19 records in "realistic data" and 5 of 25 in "ban minimizers". Another four records (c01416–c01419) are one "email subject avoids sales language" line in four languages, inside "no marketing".
- **tiny-flowlab**: 7 of 14 fiction-craft records, mostly the same rules in English and Korean (for example c01288/c01293 and c01299/c01295). Without this owner, fiction craft has 6 owners.
- **kcenon** (c01160/c01161/c01162), **Fearvox** (c01172/c01173, near-identical), **kesslernity** (c00896/c00897, identical banned-vocabulary line), **isac322** (c01024/c01144/c01145, one SEO/terminology template used for two projects), **prmichaelsen** (3 records in consistent terminology), **Pantani** (3 in match-existing). Each is one voice counted as several records.

Template families: the same text under different owners. These inflate owner counts too.
- "Use active voice, direct language, no filler words." is word-for-word identical in yangyuan-zhen (c00022, 16 copies), zereight (c00085), LimiNode (c00183) and Yeachan-Heo (c00508). This is one writer-agent template counted as 4 owners in both active voice and filler.
- Active voice has further shared example sentences: "Click the button" not "The button should be clicked" (9thLevelSoftware, smart-connective, SoundDocs), "Run the command" not ... (tranhieutt, azat-io), "We will use X" not ... (zbruhnke, UitbreidenOS), "The service processes requests" ... (github, Arcanada-one), and the Genocs/jucish2019-a11y pair. That is why active voice falls from 45 owners to 36 voices, the largest drop of any theme.
- "NEVER use generic boilerplate (match project existing style)" appears in borgius, melnikov1512, paodealho404 and asleekgeek: one template inside match-existing.
- "Be concise, specific, and value dense" appears in inbo, open-telemetry and PowerGenome. "Generate concise, high-signal docs; prefer examples and short lists" appears in 48Nauts-Operator and ScorpionConMate.
- "Explain the why, not (just) the what" has near-identical wording across microsoft, shark-hunt, enuno, johnrogers and stevessr (39 owners down to 33 voices). This short slogan may be common phrasing rather than a copied template.
- **iannuttall (c00160) and NicholasSpisak (c00756)** share one "humanizer" template: Flesch-Kincaid 8th grade, "Replace 30% of words with less common synonyms", and the same delve/tapestry list. It counts twice in anti-AI tone, readability and no-marketing.
- "Use sentence case for headlines/headings" in rhpds, dotnet, okrlinkhub and asfaload: 14 owners become 11 voices. This is probably convergence on the Google/Microsoft style guides rather than copying.

Copy counts (`copies_in_repos`) are collapsed in the counts above, but they show where apparent popularity comes from copying. Imperative section titles and sentence-case titles come from c00001 (cyberpapiii, 99 copies). "Prefer short lists and working code examples" comes from c00002 (darrenhinde, 84). The active voice / "Confident but humble" pair comes from c00003 (github/awesome-copilot, 72). "Use second person" comes from c00004 (monoes, 54). Also, `github` (awesome-copilot) and `microsoft` are treated as one owner each although their agents come from many authors. This undercounts them slightly.

## 3. Sharp but rare (1–2 owners), adoptable by a writer role

1. c01201 (borschetsky): "Flag pre-existing bugs as pre-existing so they do not read as new breakage."
2. c00494 (Imbad0202): "When a reviewer asks for more confidence, strengthen the WRITING, not the CLAIM."
3. c00935 (skanehira): "過程の記録（「以前は〜だったが」）を残さず、最終状態のみを書く" ("Leave no record of the process, such as 'previously it was...'; write only the final state.")
4. c00963 (Hal0ai): "A reader should not be able to tell which paragraphs are new." The same record: "Delete stale content the brief marks stale — don't soften it into \"previously\" phrasing."
5. c01055 (microsoft), quoted with the original line break collapsed: "Cut: `// This fixes the A-1 finding`, `// as per the C-3 issue`, `// remediation for review item #7`, `// per adversarial pass`."
6. c01028 (allisterb): "unless backed by a concrete, cited number (then keep the number, drop the adjective)."
7. c00609 (tractorjuice): "Render the coverage limits with the same prominence as the findings."
8. c00932 (xiaolai): "Preserve unresolved questions instead of forcing a clean story."
9. c01081 (llopresto87): "You do not summarize so heavily that the next agent has to re-read the source anyway. Summaries are useful when they preserve the decision-relevant detail."
10. c00524 (alirezarezvani): "Cuts first, adds second. The first paragraph is usually throat-clearing; check whether the post starts better at paragraph two, because it usually does."

Near misses worth knowing: c01091 "Convert relative dates to absolute ones."; c00943 on merging chapters (quoted in §4); c01406 "Examples in prompts should be precise and reflect the exact desired behavior — the model reproduces what it sees."

## 4. Bearing on the proposed writer

### Point 1: start from the reader and what they will do
- **Supports**:
  - Lead with the outcome (18 owners), for example c00249: "lead with what the reader can do, put mechanics and `file.py:line` refs underneath, say each point once. Shortest version that fully answers."
  - Actionable recommendations (17 owners, concentrated in report-analysis at lift 5.3).
  - Define terms on first use (24 owners).
  - Ban minimizers (20), whose stated reason is about the reader.
- **Adds**:
  - In this dimension, reader-first is mostly encoded as fixed surface defaults: "you", imperative, grade 8, active voice. Few quotes ask the writer to work out who the reader is.
  - The few that do make the defaults depend on reader and mode. For example, c01023 uses second person for guides and third person for reference, and c00885 sets "READING LEVEL: Grade 7-9 for consumer UI (Hemingway/Flesch-Kincaid); lower for vernacular audiences". These support the proposal's choice to derive style from the reader rather than hard-code it.
  - Reading-level and sentence-length numbers (19 owners) are concentrated in marketing and blog (lift 4.7/5.6), which suits path-scoped rules.
- **Contradicts**: the persona split is real. Second person (24 owners) conflicts with third-person-only (c00095) and with "Never use second-person" (c01269, imperative style for skills). A single core "you" rule would be wrong for some types.

### Point 2: every factual sentence traceable; interpretation marked
- **Supports**:
  - Specific over vague (60 owners), including c00505: "Use specific class names, file paths, and code patterns discovered from the actual codebase."
  - Calibrated claims (23 owners): facts vs assessments (c01233), guarantee vs goal (c01277), implemented vs planned (c01361, c01025).
  - Anti-hype (61 owners). Its best-phrased form is an evidence rule, not a word list: "describe what it does and let the reader judge" (c00239), "unless the claim is specific and demonstrated" (c01361).
  - Per-claim attribution appears in c01236: "According to [Source Name], [claim] ([URL])".
- **Contradicts**:
  - "No hedging" (17 owners, e.g. c00036 "Ban \"could potentially\" — prove it or drop it" (line break collapsed), c01156 "No assumption language (probably, likely, assuming)"). Read literally, this conflicts with marking interpretation. The corpus's own reconciliation is c01116 and c00493: hedge only real uncertainty, once. The proposal should say "mark interpretation once, plainly" so that it is not read as permission to hedge everywhere.
  - Marketing agents push the other way: c01561 "Apply FOMO/urgency where authentic", c00053 "Content that creates FOMO...", c00758 "\"Added\" section should read like marketing copy", c00807 "Use \"comprehensive test suite\" not \"3,015+ tests\"" (which is anti-specific). This supports keeping marketing voice out of the core and in a path rule or brief. It also shows the core evidence rule will clash with some briefs, so the role needs a stated precedence.
  - Humanizer tricks directly conflict with traceability and quality: c00160 "Replace 30% of words with less common synonyms" and "Make occasional minor grammatical imperfections". A writer role should reject these even when a brief asks for them.

### Point 3: cutting is the default; working notes go to a separate output
- **Supports**:
  - The largest theme is cutting filler (85 owners), and it covers the deliverable-hygiene half of point 3:
    - No preamble or closing (c01047, c01049).
    - No process residue: c00884 "¬meta_commentary(\"this section was updated to...\") | version_control_tracks_history"; timeless docs, 9 owners (c00107, c00935, c01198 "Keep historical delivery narrative out of published docs.").
    - Review-trail references cut from code (c01055).
  - "Why not what" (39 owners, lift 5.1 in code-comments) is cutting applied to code docs.
- **Adds a floor**:
  - c01081 (quoted above): do not over-compress.
  - c00494 "Do not pad a section or split a coherent paragraph to meet a generic preset."
  - c01049 "Technical accuracy over simplicity — don't dumb down if it would be wrong."
  - c00900 "Always prioritize clarity and completeness over brevity."
  - Extreme cutting also appears (c01600 "Concise — sacrifice grammar for brevity."), so "cut by default" needs an explicit stop condition, such as c01540: "if removing a sentence doesn't lose meaning, remove it".
- **Gap**: nothing in this dimension addresses where reasoning goes (the separate output for the caller). The corpus only says what to keep out of the deliverable.

### Combining drafts and outside examples (claim-level merge, ledger)
- **Supports claim-over-draft**:
  - c01239 "DO NOT copy large blocks of prose verbatim from section reports — synthesize and summarize."
  - c01235 "Do not copy large verbatim chunks from vendor documentation".
  - c00794 "Reflect rolemodel patterns from `accounts.md` without copying wording."
  - c00873 "Quotes real only."
- **Adds**: c00943 on integration: "통합 과정에서 전체 윤문을 새로 하지 않는다. 전환부와 용어만 다듬는다" ("When integrating, do not re-polish the whole text; touch only transitions and terminology"). This is a concrete merge rule the proposal lacks.
- **Adds**: the preserve-voice theme (18 owners). When the input is someone's own draft, minimal edits and no normalizing (c00759, c01231, c01627 "保留作者原有语感，不做风格抹平", "keep the author's original feel; do not flatten the style"). This conflicts with claim-level recombination unless the role separates "edit this text" from "synthesize from sources". The proposal names only the second mode.
- Nothing in this dimension speaks to evidence tiers or a ledger. Silence here is not evidence against them.

### No self-judgment of output quality
- Many style rules are countable: em dash counts (c00394, c01229), passive voice under 20% or over 80% active (c01229, c01372), Flesch 60–70, sentences under 25 words, banned-word lists, sentence case, code-fence language hints (5 owners), no Latin abbreviations (4). These can move out of the role into lint or eval checks. That supports the proposal's split better than prose rules would.
- The looser self-checks ("Read it out loud—if it sounds robotic, rewrite it", c00867) are the self-judgment the proposal excludes.

### What this dimension has that the proposal lacks
1. **Match the existing house voice and conventions** (60 owners, 57 voices; 5th-largest theme). It is type-independent, so path rules are the wrong home. It belongs in the core as a first step ("read the neighbors") with a fallback (c01447: Google developer style when no house style exists). In the proposal it is at best implicit in "the brief".
2. **Output language / locale** (37 owners). It needs a slot in the brief or rule file, and a note that native writing is not translation (c01139, c01358).
3. **Consistent terminology** (19 owners). For example c00210 "If the command is `/company-init`, don't call it \"company initialization command\" in one place and \"org setup\" in another." This fits point 2 (one name per referent) but is not stated.
4. **Type-concentrated themes that confirm path-scoping**: why-not-what goes to code comments (lift 5.1); actionable and calibration go to reports (5.3 / 2.9); anti-AI tone, em dash and readability numbers go to blog and marketing (lift 4–8); examples and realistic data go to API docs (1.8 / 2.2). The distribution backs the proposal's structural choice.
5. **Prompt-instructions conflict on "explain why"**, relevant because the harness writes prompts:
   - c00088 says "Don't explain why — agents need the rule, not the reasoning".
   - c00461 says to explain *why* instead of heavy MUST/NEVER.
   - c01574 says "Explain a reason when it prevents a likely mistake."
   - c01314 says "Explain why only when it helps the reader act correctly."

   The corpus is split, and the majority conditional form (give a reason when it changes behavior) is the testable one.
6. **Line-wrapping conflict**: c00487 (astral-sh) "Avoid overlong lines by shortening prose or splitting independent changes, not by hard-wrapping; wrapping can break rendering on GitHub." is set against hard wraps at 80, 79 or 100 columns (c00888, c01056, c00175). A path or house rule has to settle this. Neither the core nor the brief can assume a default.
