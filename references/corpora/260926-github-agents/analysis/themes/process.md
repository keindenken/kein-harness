# Process dimension: recurring instruction themes

Source: `claims/process.jsonl`. All 1,016 lines were read in full, with no sampling. They come from 662 distinct records, 536 repos and 511 owners.

Method: every line was read and coded by hand into themes. A keyword pass was used only to cross-check. The line indices (0-based, in file order) for each theme are in `process.assign.json` next to this file. One quote can count toward more than one theme. For example, "Read existing docs and the relevant source before writing - never guess" (c00752) counts for both reading code and not inventing. 630 of the 1,016 lines (455 records) fall in at least one of the 26 coded themes. The 15 themes below cover 521 lines (397 records). The uncoded lines are mostly task-specific steps with no reusable writing instruction, such as "Shutting down the mock server after validation" (c00288) or "Pick angle (curiosity / authority / specificity / urgency / social proof)" (c00332).

How to read the numbers:
- Counts are distinct records / repos / owners.
- "Voices" is the owner count after merging owners that share one template family. The families were confirmed by a distinctive phrase in their corpus files (see section 2).
- Doc-type "lift" is the theme's share of records carrying that type, divided by that type's share across all 662 process records. Types with fewer than 3 records in the theme are left out.

## 1. Top recurring themes (ordered by distinct owners)

| # | Theme | Records | Repos | Owners | Voices |
|---|---|---|---|---|---|
| 1 | Load the project's instruction/context files (CLAUDE.md, AGENTS.md, style guide, brief, spec, skill) before writing | 68 | 63 | 61 | 60 |
| 2 | Docs change in the same PR/commit as the code; keep docs synchronized with code | 61 | 55 | 54 | 53 |
| 3 | Ask clarifying questions before writing when information is missing or ambiguous | 49 | 46 | 46 | 45 |
| 4 | Read the code/implementation before documenting it; never document code you have not read | 48 | 42 | 41 | 37 |
| 5 | Minimal, targeted edits; preserve existing content that is still accurate | 38 | 37 | 36 | 36 |
| 6 | Never invent: mark unknowns explicitly (TODO / Open Questions / TBD) instead of filling them | 38 | 36 | 35 | 35 |
| 7 | Read neighboring/sibling docs first to match tone, structure and terminology | 37 | 35 | 33 | 32 |
| 8 | Get approval of a plan or outline before writing to disk | 29 | 26 | 25 | 23 |
| 9 | Read the target document in full before editing it | 24 | 24 | 24 | 24 |
| 10 | Update existing docs rather than create new ones; check for duplicates first | 22 | 22 | 22 | 22 |
| 11 | Stale docs are worse than none: remove or fix stale content, don't leave it | 27 | 21 | 21 | 20 |
| 12 | Execute examples, commands and links before publishing | 20 | 19 | 19 | 19 |
| 13 | Scope the update from the diff/git history | 17 | 17 | 17 | 17 |
| 14 | When code and docs disagree, code wins; flag the discrepancy instead of silently resolving it | 16 | 16 | 16 | 16 |
| 15 | Append-only history: supersede, don't delete (changelogs, ADRs, decisions, dated reports) | 18 | 16 | 16 | 16 |

Next tier, not expanded: question budget (a cap or order on questions, a refinement of #3; 20 rec / 19 own), outline before prose (15/15), generate from code rather than hand-write (22 rec / 15 own / 13 voices), state assumptions and proceed (15/15), scheduled freshness audits (15/14), ordered editing passes, big before small (14/13), bounded retries then stop/escalate (12/11), run build/lint/validation gate before done (11/11), identify audience or doc type first (11/10), explicit source-precedence order for conflicts (9/9), write each section to disk as soon as it is done (9/8).

### 1. Load the project's instruction/context files before writing
Statement: before producing anything, read the repo's agent-instruction files, style guide, brief, spec or named skill, and follow them.
Counts: 68 records, 63 repos, 61 owners.
Doc types: spread across all types. Mild lift in prompt-instructions (2.6), marketing-copy (1.5) and other (1.4). The biggest raw counts are project-docs 36 and api-reference 15.
- "Read repo context — load `.github/copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md`, `agentrc.config.json`, and any policy JSON referenced." (c00046)
- "CLAUDE.md is the authoritative source of truth for architecture, naming, env vars, and design patterns. Read it before writing anything about the project." (c01049)
- "Read **only** the reference for the document type at hand — not the whole set." (c00352)

### 2. Docs ship with the code change; keep them in sync
Statement: a behavior change and its doc update travel in one PR/commit/change set, and docs are updated during development, not after.
Counts: 61 records, 55 repos, 54 owners.
Doc types: code-comments (lift 2.6), api-reference (2.3), project-docs (1.7), changelog (1.4). Almost absent from marketing, fiction and reports.
- "Ship docs in the same PR as the feature/API change" (c00004)
- "every user-visible behavior change must carry its doc edit *in the same change set*" (c00936)
- "Update it in the same change whenever the layout changes: a stale entry is worse than none, because it sends the next task down a path the code no longer supports." (c01056)

### 3. Ask clarifying questions before writing
Statement: if inputs are missing or ambiguous, ask the requester before drafting. Many prompts also set a question budget.
Counts: 49 records, 46 repos, 46 owners. Sub-theme "question budget": 20 records, 19 owners. It splits three ways: a numeric cap of 3–6 per round (8 owners), one question at a time (6 owners), and all questions in a single batch, ask once, or draft first and ask after (6 owners, including "ask all in a single message", c00670). These directly contradict each other.
Doc types: prd-spec (lift 2.1, 19 of 49 records), prompt-instructions (2.8), fiction-narrative (2.0). The question budget is even more PRD-heavy (prd-spec lift 3.2).
- "Before writing anything, interview the user with numbered clarifying questions (max 6 per round) covering:" (c00093)
- "Ask targeted questions only when missing context materially changes the outcome; otherwise proceed with explicit assumptions." (c00218)
- "For each design dimension, ask ONE question. Smart defaults provided. The operator answers, you draft, they refine." (c01018)

### 4. Read the code before documenting it
Statement: ground the doc in the implementation. Read source, routes, entry points and signatures, or run the app, and never describe code you have not opened.
Counts: 48 records, 42 repos, 41 owners, 37 voices.
Doc types: api-reference (lift 2.3), code-comments (1.7), project-docs (1.6).
- "Read the code/implementation FIRST, then write documentation. Never document code you haven't read. Tool calls before text output." (c00638)
- "Read the source file — copy real signatures, not made-up ones" (c00249)
- "Read the entry files first — routers, controllers, service facades, public API surfaces. These typically contain ~70% of behavioral assertions." (c00469)

### 5. Minimal, targeted edits; preserve what is still accurate
Statement: when updating, change only what is wrong or missing, keep untouched sections intact, and prefer Edit over full rewrites.
Counts: 38 records, 37 repos, 36 owners.
Doc types: code-comments (lift 1.9), other (1.7), project-docs (1.2).
Counter-voices (outside the count): "Rewrite, don't append: when updating a section, rewrite it to reflect current state." (c00278). Another prompt says a concept-level change must re-read and rewrite the whole text, and only wording fixes may be local edits (c00935).
- "In update mode, PRESERVE user-authored content in sections that are still accurate. Only rewrite inaccurate or missing sections." (c00006)
- "Minimal edits — change only what is inaccurate or missing. Don't rewrite sections for style alone unless asked." (c01192)
- "При обновлении — минимальный diff: правь разошедшееся, не переписывай целиком то, что верно." (c01276)

### 6. Never invent; mark unknowns explicitly
Statement: missing facts become visible markers ([TODO], Open Questions, Q-NNN, "Undetermined Items", draft status) rather than guesses.
Counts: 38 records, 36 repos, 35 owners.
Doc types: prd-spec (lift 2.1). Otherwise flat.
Note: the markers usually live inside the deliverable, for example a PRD "Open Questions" section or a `Status: Draft` line.
- "Mark areas needing fact-checking with [TODO]" (c00003; 72 repo copies)
- "Anything not in the source becomes `Q-NNN`. Halt and ask the user before continuing." (c01002)
- "Guessing in a test silently locks in an implementation decision the user never made." (c00850)

### 7. Read neighbor docs to match the house style
Statement: before writing, open 2–3 sibling pages or existing docs and match their tone, structure, depth and terminology.
Counts: 37 records, 35 repos, 33 owners, 32 voices.
Doc types: social-media (lift 3.2), marketing-copy (2.2, as brand voice), api-reference (1.7).
- "Read the neighborhood. Open 2–3 sibling files to absorb the local style." (c01310)
- "Before writing, survey the existing documentation in the project (using the Read and Grep tools) to identify the established style: tone, section usage, level of detail, and naming conventions." (c00325)
- "Read first — examine the existing page (if editing) and its neighbors. Understand what already exists before writing." (c00242)

### 8. Approval gate before writing
Statement: present the plan, outline or intended edits and wait for explicit approval before any file write.
Counts: 29 records, 26 repos, 25 owners, 23 voices.
Doc types: ux-microcopy (lift 3.3), fiction-narrative (2.5), prd-spec (1.5).
- "Present the plan to the user. Do not proceed until the user has explicitly approved the plan." (c00839)
- "This outline is a checkpoint. The requester confirms the structure and message hierarchy before you spend tokens writing the prose." (c01260)
- "Wait for \"yes\" before using Write/Edit tools" (c00000; 130 repo copies)

### 9. Read the target document in full before editing
Statement: open and fully read every file you will change, so existing content is not lost and edits are coherent.
Counts: 24 records, 24 repos, 24 owners. No multi-record owners, no families.
Doc types: roughly flat (project-docs 1.3, report-analysis 1.4, code-comments 1.5).
- "Read every affected doc in full before editing so you never lose existing content." (c01538)
- "Read each affected doc file in full before editing." (c01019)
- "If a read is truncated, continue until both files have been read completely." (c01185)

### 10. Update rather than create; dedupe first
Statement: check whether the topic is already covered and extend that doc or entry instead of adding a near-duplicate.
Counts: 22 records, 22 repos, 22 owners.
Doc types: api-reference (lift 1.7), project-docs (1.5).
- "Prefer updating existing docs over creating new files" (c00463)
- "Decide: new note or update. If an existing note already covers this area, append a dated ## Update — YYYY-MM-DD section to it rather than creating a near-duplicate." (c01201)
- "If an entry for the same feature already exists under `[Unreleased]`, refine it instead of adding a duplicate." (c00352)

### 11. Stale docs are worse than none
Statement: wrong documentation is actively harmful, so delete or fix it rather than leaving it or piling new text on top.
Counts: 27 records, 21 repos, 21 owners, 20 voices. The aphorism itself appears in the full corpus files of 28 owners, so it is an industry meme, not one lineage.
Doc types: api-reference (lift 2.1), code-comments (2.0), changelog (1.9), project-docs (1.8).
- "Stale docs are worse than no docs — delete rather than leave wrong content" (c01412)
- "Remove stale content instead of adding on top of it" (c00467)
- "Never copy stale wording when code changed." (c01130)

### 12. Execute examples, commands and links before publishing
Statement: run code samples, curl calls, install steps and links. A doc is not done until they pass, and an untestable example is labeled as such.
Counts: 20 records, 19 repos, 19 owners.
Doc types: api-reference (lift 2.3), changelog (1.8), project-docs (1.6).
- "Documentation is NOT complete until the verification test has been executed and passes." (c00802)
- "Run the install + quickstart from the existing README as a new user would — note every place it lies or omits" (c00369)
- "If examples cannot be tested, explicitly state this limitation." (c00085)

### 13. Scope the update from the diff
Statement: read `git diff`/log and the changes since the docs were last touched, and edit only the sections the diff invalidates.
Counts: 17 records, 17 repos, 17 owners.
Doc types: changelog (lift 2.6), project-docs (1.6), code-comments (1.6).
- "Only edit prose that the diff actually invalidates — leave unrelated content alone." (c00060)
- "Read the diff and the specification. The gap between them is what needs documenting." (c00787)
- "Determine which sections of each document are affected by the diff." (c01584)

### 14. Code wins; flag the discrepancy
Statement: when docs and implementation (or two sources) disagree, document what the code does and report the conflict, since it may be a bug. Do not silently pick one.
Counts: 16 records, 16 repos, 16 owners.
Doc types: report-analysis (lift 1.7), changelog (1.4), project-docs (1.3).
- "If you find the code and the existing docs disagree, fix the docs to match the code and flag the discrepancy in your report -- it may be a real bug." (c01100)
- "If you suspect something is factually wrong or stale, do not silently \"fix\" it — leave it and flag it for the human to verify." (c01028)
- "Never omit a finding — if sections conflict, include both perspectives and note the discrepancy." (c01239)

Note the split: c01100 fixes and flags, while c01028 flags without fixing.

### 15. Append-only history
Statement: history-bearing docs are never rewritten. Append new changelog entries, supersede ADRs, and date reports instead of overwriting them.
Counts: 18 records, 16 repos, 16 owners.
Doc types: report-analysis (lift 1.9), prd-spec (1.5).
Counter-voices (5 owners, outside the count): "Resolved unknowns leave docs/KNOWN_UNKNOWNS.md. When a question is answered, move the answer into whichever document now owns it and delete the entry." (c01091). Another: "Edit the relevant section in place — don't append a dated narrative." (c00762).
- "Never delete, reorder, or overwrite a decision. Always append new decisions at the end of the Decisions section." (c01580)
- "古いADRの `Status` だけを `Superseded by ADR-YYYY` に更新する（本文は変更しない）。" (c01399)
- "Do NOT overwrite previous reports — each review is dated." (c00816)

## 2. Lineage warnings

- ECC `doc-updater` "codemap" family (affaan-m/ECC and derivatives). affaan-m ships one doc-updater in 7+ languages (c00470, c00473, c00476, c00478, c00480, c00482, c00484), each a separate record. The phrase "codemap" ties it to zereight, 0xb7a7dd61, sangrokjung, Dach-Coin, zekdevs and Borda (7 owners, 15 writing-role records in the full corpus). Effect: theme 4 has 9 records from 4 owners of this family (41 owners → 37 voices). "Generate from code" (next tier) has 9 of its 22 records here, 7 of them affaan-m translations: 22 records collapse to 15 owners and 13 voices. Theme 11 has 4 family records from 2 owners.
- UitbreidenOS/UitKit translations. The same `documentation-engineer` appears in EN/DE/ES/FR/NL (c01411–c01415). This gives 5 records each in theme 2 and theme 11, but it is one owner and one voice.
- "Writing Principles: Accuracy First / Keep Current / Show, Don't Tell / Progressive Disclosure" list. It appears in 6 records from 5 owners (OrdinalDragons c00204, CloudAI-X c00637/c00638, microsoft c00444, schlessera c01427, zapat-ai c01621). "Keep Current — Update docs with code changes" in theme 2 is this list, not independent agreement. The looser "Keep (It) Current" heading appears in 20 owners' files and looks like a common best-practices boilerplate.
- OpenAgentsControl (darrenhinde): c00002 (84 repo copies), c00008 and c00009 (34 each), plus ScorpionConMate c00191, a ContextScout clone. This family supplies 4 of theme 8's 29 records and 2 of its owners, and inflates reach far more than owner count suggests.
- Claude-Code-Game-Studios (Donchitos) "May I write…" gate: c00000 (130 repo copies) plus bullish0x c01376/c01377 and Sincebook. In theme 8 it adds 3 records from 2 owners that are one voice. It also supplies 2 of the "ask" records in theme 3.
- High-copy records inflate apparent reach, not owner counts: c00000 (130 repos), c00002 (84), c00003 github "[TODO]" (72), c00004 monoes "same PR" (54), c00005 davila7 "context manager" (53), c00006 gsd-build "PRESERVE" (43), and mrgoonie/ClaudeKit c00007/c00010/c00013 (38/32/26). The mrgoonie "Proactively update documentation during feature development, not after" line appears twice (c00010, c00013), with a `repomix` regeneration step that is one owner's tooling.
- Aggregators: davila7/claude-code-templates and ccplugins/awesome-claude-code-plugins republish agents from other authors. Their "Query context manager…" lines (c00005, c00018; also jtgsystems) are one template that recurs.
- Question budget: alirezarezvani contributes 2 records (c00656, c00660) with near-identical "4-5 / 5-6 questions, one at a time" text.

## 3. Sharp but rare (1–2 owners each, adoptable by a writer role)

1. "Freshness verdicts are evidence, not impressions — every routed doc gets `FRESH | PATCHED | RESCAN REQUIRED | UNVERIFIED`; a doc you did not check is `UNVERIFIED`, NEVER `FRESH`" (c01600). A closed verdict vocabulary with a default of unverified. It maps directly onto a claim ledger's tier column.
2. "Search for the *old* claim, not the new one. Search for paraphrases, not just the exact string" (c01317). An operational rule for finding every stale copy of a changed fact.
3. "概念を削除・置換したときは、旧概念への参照残骸を rg で掃く" (c00935). When a concept is removed or replaced, sweep for leftover references with rg. The same prompt requires a full re-read and rewrite for concept-level changes.
4. "Also check the near-neighborhood for drift while you are there: if the module map row above the one you're editing is already stale, fix it and say so in your report." (c01129). Bounded opportunistic repair, reported through the side channel.
5. "Treat the generated wording as source material, not a preferred baseline. Rewrite retained entries to make them clearer, more precise, and more user-facing." (c00487). Drafts are raw material, not a base to patch.
6. "Treat prompt, handoff, Jira, and SME wording as factual input, not markup-ready text." (c01015). The brief's wording supplies facts, not prose to paste.
7. "Prose is what yields, in this order: delete what the flag table already says, then what `## Arguments` already says, cap `Long` at ~6 lines, cap examples at 5 (3 is the floor)." and "Those caps only ever ratchet down." (c00265). An ordered cutting procedure with a one-way ratchet.
8. "When in doubt between shortening and deleting, delete." (c01055). A one-line tie-breaker for cutting by default.
9. "Use both literal/exact search (grep_search) and natural-language/semantic search to catch synonyms, renamed concepts, and documentation that doesn't share exact strings" and "Stop when both search modes yield no new high-priority candidates or duplicative results" (c01016). A research stopping rule.
10. "Verification budget is max 2 attempts per link (1 fetch + 1 Playwright, or 1 Playwright directly for known JS-heavy sites) — if still unverifiable or Playwright is unavailable, stop and tell the user instead of continuing to search." (c00098). A bounded verification cost that ends in reporting the item as unverified.

Also notable, but more specific to one setup: "Get the date from the environment, never guess it: git log -1 --format=%cd --date=short" (c01201). "Write a complete draft of your section to the .md file FIRST, with your single `Write` call, before you do any self-checking." (c01007). "a run that ends before DESIGN.md is written has recorded nothing" (c00950). "A blocking finding from one panel is not outweighed by three panels rating the artifact 9/10." (c00573). "Before deleting or converting any passage, name what it IS doing." (c00114).

## 4. Bearing on the PROPOSED WRITER

General role, with doc-type differences carried by path-scoped rules and the brief:
- Supports. The single most common process theme (#1, 61 owners) is "load the project's instruction/context files before writing". The corpus already pushes type- and project-specific knowledge into external files that the agent reads. Several prompts go further toward path/type scoping: "Read **only** the reference for the document type at hand — not the whole set." (c00352), and load `references/` only when a matching problem appears (c01138).
- Supports, with a caveat. Most process themes are type-agnostic editing discipline (#5, #9, #10, #13). A general role can hold them. The type-concentrated ones would go into rules: same-PR sync, code reading and example execution (api-reference / code-comments / project-docs), question budgets (prd-spec), outline-first (blog / marketing), and append-only history (changelog / ADR / reports).
- Adds. The corpus instructs "read the target in full before editing" (#9) and "read neighbors to match style" (#7) as separate steps. A rule file can name the house style, but the role must still read the target and its neighbors.

Point 1 (start from the reader and what they will do):
- Weak support in this dimension. Only 10 owners give a process step to identify audience or doc type first, for example "Ask about audience if not specified" (c01150), "BEFORE writing anything, classify the documentation type." (c00132), and "Identify the core message and 3-5 key takeaways." (c00234). In the process dimension the corpus starts from the sources, not the reader. Reader-first appears in other dimensions (see `audience`), not as a workflow step. If the proposal wants reader-first to shape the process, it has to state it as a step, because the corpus does not model one.

Point 2 (every factual sentence traceable to evidence; interpretation marked):
- Strong support: #4 read the code (41 owners), #6 never invent (35), #12 execute examples (19), #14 code wins and flag (16), and the next-tier "generate from code" (13 voices).
- Adds a stronger evidence rung for project docs than "code". Several prompts require running the thing, for example "Documentation is NOT complete until the verification test has been executed and passes." (c00802) and "Run the install + quickstart … as a new user would" (c00369). For examples, commands and install steps, executed output ranks above reading the code, which parallels the proposal's "measured in runs" tier.
- Adds a staleness sweep: find old copies of a changed claim (c01317, c00935) and scope the edit from the diff (#13). The proposal traces what it writes but does not say to remove claims that are no longer true (#11, 21 owners).
- Gap: the proposal marks interpretation, but the corpus mostly marks the unknown (#6), with TODO, Open Questions or draft status. The proposal needs a rule for where unknowns go. See the next point.

Point 3 (cutting is the default; working notes go to a separate output):
- Supports the separate channel. #14 routes discrepancies to "your report" or "the final summary" rather than into the doc (c01100, c00546, c01129). Two prompts keep pre-checks out of the output: "写前静默预检（内部完成，不输出）" (c00538) and "Minimize internal reasoning verbosity" (c00139).
- Partly contradicts: 35 owners (#6) put unknowns inside the deliverable, as PRD Open Questions, `[TODO: verify]` or `Status: Draft`. For PRDs and specs the open question is content for the reader, not a working note. The proposal should decide per doc type whether unresolved items belong in the deliverable (spec, PRD) or only in the side ledger (README, report).
- Tension with cutting by default: #5 (36 owners) and #9/#10 make preservation the default when editing an existing doc: "PRESERVE user-authored content in sections that are still accurate" (c00006). Cutting by default fits prose the writer drafts. On an existing doc it becomes deleting only what is stale or wrong (#11) and editing only what the diff invalidates (#13). The proposal does not separate create mode from update mode, and the corpus treats them very differently.
- Adds a concrete cutting order: c00265's "prose yields in this order … caps only ratchet down" and c01055's "when in doubt … delete".

Point 4 (combine several drafts by claim, keep evidenced claims, ledger claim → source → tier; no self-judgment):
- Little direct evidence in this dimension. The closest instructions treat drafts as material rather than a base: "Treat the generated wording as source material, not a preferred baseline" (c00487). "Faithful preservation is about the MATHEMATICS, not the text: never copy a fact's ## proof verbatim ... re-express it" (c00708). "Gather all approved team outputs and evidence." / "Remove duplication and unresolved contradictions." (c00267).
- Partly contradicts the evidence-tier ordering. When sources conflict, the corpus resolves by authority, not by evidence strength: "Conflict resolution hierarchy: user input > template guidance > agent defaults" (c00631). "来源冲突时以已批准产品规则为准并记录冲突" (c00879: on a source conflict, approved product rules win and the conflict is recorded). "If they diverge during authoring, `findings.json` is the source of truth." (c00816). There are 9 owners with an explicit precedence order. The proposal's tiers (measured > vendor doc > recurring > single) have no slot for "the user or an approved decision said so". The ledger should carry authority as a separate axis from evidence strength, or define where a caller's directive ranks.
- Adds conflict handling to the ledger: "If two sections disagree on severity for the same finding, preserve the higher severity" and "include both perspectives and note the discrepancy" (c01239). A tier-based merge still needs a rule for equal-tier conflicts.
- Adds a verdict vocabulary: c01600's `FRESH | PATCHED | RESCAN REQUIRED | UNVERIFIED`, where an unchecked item is `UNVERIFIED`, is the ledger idea in working form.
- "Does not judge its own output": this dimension neither supports nor contradicts it. Bounded retry loops appear (next tier, 11 owners, e.g. "Two attempts fail: post BLOCKED, stop.", c01172), but they are driven by external checks such as tests, validators and reviewer feedback. That fits "runs/evals judge". The one rule that touches self-judgment, c01007, orders "draft first, self-check after" rather than forbidding self-checks.

Missing from the proposal:
1. A missing-information policy. Ask the caller (#3, 46 owners) or state assumptions and proceed (next tier, 15 owners). The corpus assumes an interactive human (#3, #8 approval gate, 25 owners). For an unattended writer the equivalent is: resolve what reading can resolve (c01057 "resolve what you can with cheap read-only checks"; c01492 "NEVER ask questions you can answer by scanning the codebase"), then record the remaining gaps as assumptions or open questions in the ledger. The approval gate (#8) belongs to the caller's brief, not the writer.
2. Update-mode discipline: read the target fully (#9), minimal diff and preserve (#5), update rather than create and dedupe (#10), scope from the diff (#13), and append-only history for changelogs, ADRs and decisions (#15). These are among the most-repeated process rules and the proposal says nothing about editing an existing document.
3. Sync with the code change (#2, 54 owners). It is mostly a caller or workflow rule (when to call the writer), but a writer brief should say whether the doc edit belongs to the same change.
4. Executing examples as evidence (#12), stated above.
5. Bounded verification and stop conditions (c00098 "max 2 attempts per link … stop and tell the user"; retry caps in 11 owners). Without a budget, "every sentence traceable" can turn into unbounded verification.
