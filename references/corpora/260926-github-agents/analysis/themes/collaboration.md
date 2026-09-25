# Collaboration dimension: recurring themes

Source: `claims/collaboration.jsonl`, 350 quotes from 304 distinct records, 255 repos, 247 owners (owner = the repo part before `/`).

## Method

- I read all 350 lines in full. Nothing was sampled.
- I assigned each line to zero or more themes by hand, by line index. The assignment is in `analysis/themes/collaboration.assign.json`: keys are theme codes, values are 0-based line indices into `collaboration.jsonl`. Keys with a suffix (for example `ASK_PROTOCOL_one_at_a_time`) are sub-groups inside a theme. `EDIT_IN_PLACE` is the union of `UPDATE_IN_PLACE` and `PRESERVE_EXISTING`, and `ROLE_BOUNDARY` is the union of `STAY_IN_LANE` and `NO_DIRECT_INVOKE`. A script computed every count from that file. 322 of 350 lines fall in at least one theme listed below; the other 28 are one-off workflow steps, domain details, or tool quirks.
- Quotes are verbatim; where a source quote was hard-wrapped, the line breaks are collapsed to spaces and marked.
- Counts are distinct records / distinct repos / distinct owners. For doc types, I list the most frequent types with their lift: the type's share inside the theme divided by its share across all 350 lines. Lift is shown only when the type has 3 or more lines in the theme.
- One person coded every line and no one checked it, so the edges of each theme are judgment calls. The order by owner count is more reliable than the exact numbers.
- `copies_in_repos` is not added into the counts. Where a large copy count inflates a theme's apparent reach, section 2 says so.

## 1. Top recurring themes (ordered by distinct owners)

### 1. Ask when information is missing or ambiguous; do not guess
If purpose, behavior, audience, or scope is unclear, the writer stops and asks (the user, or the developer) before writing.
- Counts: 44 records / 43 repos / 42 owners
- Doc types: project-docs 26 (1.0x), api-reference 19 (1.2x), prd-spec 9 (1.1x), code-comments 8 (1.4x). The theme is spread evenly across types.
- "If you don't have enough information to complete a section, ask rather than guess." — c00188
- "Escalate ambiguity. If a source component's purpose is unclear from the source code, ask the developer before writing documentation." — c00449
- "Ask the researcher to paste the exact HTTP request and response" — c00036

### 2. Propose first, then wait for approval before writing
The writer presents an outline, structure, topic list or planned changes and does not write until the user confirms. Some roles add checkpoints partway through.
- Counts: 24 records / 24 repos / 24 owners
- Doc types: project-docs 14 (1.0x), api-reference 7 (0.8x), changelog 3, report-analysis 3. No concentration.
- "Create a list of topics/features to cover and ask the user for approval before writing anything" — c01484
- "Suggest documentation structure and get confirmation before proceeding" — c00052
- "先写章节蓝图，作者确认方向再动笔，避免写完整章才发现跑偏" (write the chapter blueprint first and start only after the author confirms the direction, so you do not find out after a whole chapter that it drifted) — c01626

### 3. Role boundary: stay in lane, do not invoke other agents, and report out-of-scope work to the owner
This merges two sub-patterns:
- stay in lane: out-of-scope problems such as code changes, reviews or translations are reported to the owning role, not fixed (10 records / 9 owners)
- no direct invocation: the writer names other agents but does not spawn or chain to them, because the orchestrator routes (9 records / 9 owners)

Merged:
- Counts: 19 records / 19 repos / 18 owners
- Doc types: project-docs 13 (1.2x), api-reference 6, changelog 5 (2.0x), code-comments 4 (1.7x)
- "If a file needs a behavioral change to document it correctly, report that to the coordinator instead of making it." — c00779 (the same line appears in c00866 from the same owner)
- "You don't invoke other agents. If you need help, name them via Handoffs; the orchestrator routes." — c01591
- "Never invoke the illustrator yourself. Return a placeholder; the parent orchestrates." — c00112

### 4. Hand off through a file or a structured report that names the next owner
The output is shaped for the next agent. It is a report file under a naming convention, or a short message pointing at the file, or a report that separates decisions, blockers and next owner.
- Counts: 22 records / 18 repos / 18 owners
- Doc types: project-docs 11 (0.8x), report-analysis 7 (2.2x), api-reference 7, prd-spec 5, fiction-narrative 5 (3.5x)
- "Name the next owner only when a handoff is needed, and separate decisions, blockers, warnings, and follow-up options." — c01020
- "Teammate mode (Agent Teams): Write output to file, send brief completion message via SendMessage." — c00939
- "Your output will be used directly by the parent agent to populate documentation sections. Provide complete, ready-to-use content, not summaries or references." — c00064

### 5. Follow the project's existing conventions and sources
Before writing, the writer reads existing docs, the style guide, CLAUDE.md or AGENTS.md, or a related skill, and matches their tone, format and terms.
- Counts: 18 records / 18 repos / 18 owners
- Doc types: project-docs 12 (1.1x), api-reference 7, prd-spec 5 (1.6x)
- "Check if there are existing docs (`docs/`) and match their tone if they follow good practices." — c00181
- "When documenting code in an area another skill covers (e.g. `ngrx-signal-store`, `csharp-async`, `ef-core`, `angular-developer`), read that skill's `SKILL.md` so terminology and recommendations match the repo's standards." — c00352
- "If a canonical feature name already exists, reuse it verbatim." — c01483

### 6. Docs ship with the code change and stay in sync with it
Documentation is updated in the same PR or commit as the code it describes, and stale docs are treated as a defect.
- Counts: 18 records / 18 repos / 18 owners
- Doc types: api-reference 15 (2.2x), project-docs 17 (1.5x), code-comments 5 (2.1x), other 4 (2.5x)
- "Ship docs in the same PR as the feature/API change" — c00131
- "Si un cambio toca tipos, schemas de Sanity/Zod, contratos de API o terminología de dominio, actualizar en el mismo commit/PR toda la documentación que los referencie" (if a change touches types, Sanity/Zod schemas, API contracts or domain terms, update every doc that references them in the same commit/PR) — c01175
- "The README must always be current. A stale README is worse than no README." — c01616

### 7. Ask first before a major restructure or rewrite of existing docs
Small edits need no sign-off. Restructuring, major rewrites, or changes to doc build config need it.
- Counts: 17 records / 17 repos / 17 owners. Most of these come from one template family; see section 2.
- Doc types: project-docs 15 (1.5x), api-reference 8 (1.3x), code-comments 5 (2.3x)
- "Ask first: Before modifying existing documents in a major way." — c00177
- "Ask first: Restructuring existing documentation, changing doc build config" — c00650
- "Ask before major rewrites. Propose structural changes before executing them." — c00262

### 8. Update linked artifacts together: indexes, mirrors, translations, trackers
When the writer touches one file, it also updates the files that must agree with it: an index, a traceability matrix, a translated README, a generated mirror, or an in-app changelog. If it cannot, it says so.
- Counts: 16 records / 16 repos / 16 owners
- Doc types: project-docs 14 (1.5x), api-reference 7, changelog 4 (1.9x), report-analysis 3 (1.4x)
- "If only one locale can be updated safely, stop and report the mismatch instead of leaving silent drift." — c01077 (source line break collapsed)
- "add a comment in the code like `# NOTE: also referenced in README.md` so future editors know to update both." — c00638
- "SKILL.md is the source of truth for the agent brain. The 24 mirror files (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`, …) are **generated**. Never edit a mirror directly." — c01132

### 9. Question protocol: how to ask, not only whether to ask
These instructions govern the interview itself: one question at a time, multiple choice, a cap on the number of questions, or only questions that cannot be inferred. The sub-conventions contradict each other. "One at a time" has 9 records / 9 owners. "Batch them or cap them" has 5 records / 5 owners. Multiple choice has 3 owners, and "only ask what cannot be inferred" has 2.
- Counts: 16 records / 16 repos / 16 owners
- Doc types: prd-spec 17 lines (4.6x), which is the strongest type concentration in this dimension. project-docs 4 (0.3x).
- "Ask targeted questions about the feature/system before writing. Do not ask all questions at once — ask the most critical one first, wait for the answer, then ask the next." — c01425
- "Ask at most 5 questions per ticket — batch them into a single message" — c01492
- "One question at a time — and that is countable, not a vibe." — c01502

### 10. Author and reviewer are separate passes
The writer does not review or approve its own work. A reviewer, editor, critic or human does, and when review findings come back the writer fixes only what was named.
- Counts: 15 records / 15 repos / 15 owners. The core "authoring pass only / never self-approve" wording has 5 records / 5 owners.
- Doc types: project-docs 11 (1.2x), other 7 (5.1x), api-reference 7, code-comments 4 (2.0x)
- "Treat writing as an authoring pass only: do not self-review, self-approve, or claim reviewer sign-off in the same context." — c00508
- "Do not consider your task complete until `claude-code-guide` has reviewed and approved the content." — c01358
- "On `correction_hints` from a critic → fix ONLY the named findings." — c00397

### 11. Edit existing documents in place and preserve what is there
This merges two sub-patterns:
- update in place, with no duplicate, forked or `-v2` files (11 records / 9 owners)
- preserve existing content: append instead of removing, mark superseded items instead of deleting them, keep working prose, respect the human author's voice (11 records / 7 owners)

Merged:
- Counts: 22 records / 15 repos / 15 owners
- Doc types: project-docs 13 (1.0x), report-analysis 9 (2.9x), academic 3 (from preserve-existing, 9.7x within that sub-group)
- "Update, don’t fork:** You **MUST** update existing target files. You **MUST NOT** create `*-v2.md`, `*-new.md`, `*-draft.md`." — c00184
- "Key Findings — append new findings; mark outdated ones with "(superseded as of YYYY-MM-DD)" rather than removing." — c00611
- "Respect the user's voice. When revising text the user wrote, suggest changes rather than rewriting. Preserve their style and intent." — c01213

### 12. Get facts from the people or agents who own them
When the writer does not know how something works, it asks the owning engineer or specialist agent before writing the sentence. Fact-checking is also routed to domain owners.
- Counts: 14 records / 14 repos / 13 owners
- Doc types: project-docs 13 (1.5x), api-reference 8 (1.5x), changelog 3 (1.5x), code-comments 3 (1.6x)
- "Unsure how a feature actually works → ask @frontend-developer (for UI behaviour) or @backend-developer (for data behaviour) before writing" — c00278
- "For "what is this verdict actually allowed to claim?" to principal-engineer, before you write the sentence." — c00785
- "If product behavior is unclear or contradictory, request source-owner clarification before publishing." — c01194

### 13. Delegate specialized sub-parts to specialist agents
Diagrams, code examples, backlinks, attack trees and codebase analysis are delegated to named agents, and parallel helpers get separate focus areas.
- Counts: 11 records / 11 repos / 11 owners
- Doc types: project-docs 9 (1.4x), api-reference 5 (1.3x)
- "Let doc-diagrammer agent handle all Mermaid diagram creation and embedding in post-processing" — c01313
- "Delegate example-heavy sample maintenance to **Example Gardener** when the task is mostly about teaching code rather than prose." — c00995
- "Ensure search agents don't duplicate efforts by assigning distinct focus areas" — c00902

### 14. Coordinate with named roles, stated without a mechanism
These lines say "Collaborate with X", "Coordinate with Y" or "Deliver to Z" and give no protocol. They are the least operational theme here.
- Counts: 20 records / 11 repos / 11 owners
- Doc types: fiction-narrative 9 (6.5x), project-docs 6 (0.5x), api-reference 6, report-analysis 4
- "Collaborate with product-manager on features" — c00005
- "Coordinate with the SDLC Manager and Release Manager so documentation aligns with release scope." — c00213
- "Coordinate plot-location with Story Writer" — c01300

### 15. Flag decisions and discrepancies to the owner instead of settling them silently
The writer surfaces what someone else must decide: missing details, a choice between two valid rewrites, a code-versus-docs discrepancy, a deviation from canon, or its own assumptions.
- Counts: 11 records / 10 repos / 10 owners
- Doc types: project-docs 7 (1.0x), changelog 5 (3.1x), fiction-narrative 3 (4.0x), ux-microcopy 3 (8.8x)
- "call out missing product/release details needing owner confirmation" — c00037
- "call out anything that requires the author to decide between two valid rewrites" — c00448
- "If you discover a discrepancy between what code does and what docs claim, flag it to Coordinator immediately." — c00730

### Below the cut (fewer than 10 owners)
- The writer does no git operations and the orchestrator or user commits: 7 records / 7 owners. The opposite, where the writer commits itself, has 3 records / 3 owners (c00115, c00463, c01433).
- The writer records state or knowledge in a shared store (tracking file, KB, memory, decision log): 7 records / 7 owners.
- Human review before the deliverable is sent or an irreversible action is taken: 9 records / 5 owners, of which 4 records belong to one owner (see section 2).
- Never ask, and proceed on stated assumptions: 5 records / 5 owners. This is the counter-pole to theme 1 (c00441, c00670, c01056, c01057, c01306).
- A thin wrapper whose only job is to read and follow a canonical role file: 13 records / 6 owners, of which 8 belong to one owner.

### Theme families
- Human gates (themes 1, 2, 7, 9 and human review before sending): 103 records / 96 repos / 93 owners. This is 38% of the dimension's 247 owners.
- Orchestration (themes 3, 4, 10, 12, 13, 14): 94 records / 79 repos / 77 owners.
- Maintenance and consistency (themes 6, 8, 11, record-state): 60 records / 53 repos / 53 owners.

## 2. Lineage warnings

- **Theme 7 (ask first before a major restructure) comes mostly from one template.** 10 of its 17 records open with "You are an expert technical writer" and 15 of 17 have a "Boundaries" section of the form Always / Ask first / Never. Seven records contain the identical line "Ask first: Before modifying existing documents in a major way" (c00177, c00274, c00336, c00751, c01303, c01321, c01335), and most of the files are named `docs-agent.md` or `docs.agent.md` under `.github/agents/`. Only c00262, c00726 and c01202 are clearly independent. Counting the family as one voice leaves roughly 4 voices, not 17.
- **Theme 14 (coordinate with named roles) is inflated by two owners.** tiny-flowlab (novel-studio-copilot-cli) contributes 10 of its 22 lines, and all of the fiction-narrative concentration comes from there. davila7/claude-code-templates contributes 3 records, and c00005 alone is copied into 53 repos and c00018 into 18. Without those two owners, 9 owners remain, each with a vague one-liner.
- **Theme 4 (handoff artifacts) has large copy counts from one owner.** mrgoonie's two report-naming records (c00010, c00013) are copied into 32 and 26 repos. They count as 2 records / 1 owner here, but a reader weighting by copies would overrate them. tiny-flowlab adds 4 more lines.
- **Theme 11 (edit in place and preserve) depends on one owner for its preserve half.** tractorjuice/arc-kit has 6 lines across 5 records, all in the same "merge; never remove; mark superseded" style. That owner also drives the report-analysis concentration. The "update, don't duplicate" half is broad (9 owners).
- **Human review before sending** is 4 records from UitbreidenOS that are one sentence translated into German, Spanish, English and Dutch (c01416 to c01419), plus 2 near-identical records from Fearvox. Its 9 records are 5 voices.
- **The thin-wrapper pattern ("read and follow canonical file")** has 8 of its 13 records from caioimori/sinapse-ai, whose copy squad also repeats "never start a nested CLI" in 5 records (not themed).
- **Theme 10 (author and reviewer separate)**: in the core "authoring pass only / never self-approve" wording, c00508 (Yeachan-Heo/oh-my-claudecode), c00183 (LimiNode) and c00694 (evolution-foundation) use nearly identical phrasing. They may be one lineage that was adapted. c00026 (chrisime, "you are not the final writer") is copied into 13 repos.
- **Theme 9 (question protocol)**: Aco-Lone contributes 3 lines from one record and jemai7579 2. The prd-spec concentration is real across owners, but several of these PRD roles appear to follow the same brainstorming-skill style ("One question at a time", "Multiple choice is preferred").
- Themes 1, 2, 5, 6, 8 and 12 have no owner with more than 2 lines, and no shared template turned up in them.

## 3. Sharp but rare

These come from 1 or 2 owners and are precise enough for a writer role to adopt:

1. "You run in the background and cannot ask the user questions: when the scope is ambiguous, state your assumptions, proceed on them, and report them in a self-contained final response that lists every file you changed." — c01056 (source line breaks collapsed). This is the unattended-subagent version of theme 1.
2. "Do not silently edit files when acting as reviewer; report findings unless the caller explicitly switches you back into edit mode." — c01363
3. "If you launch sub-agents, pass each one its own registry tier explicitly. Never let a sub-agent inherit your model." — c01324
4. "Request challenge when: confidence < 0.8, documenting complex architecture, or security-sensitive APIs" — c01168
5. "Preserve existing sections that cover material the notes confirm — don't rewrite working prose for its own sake." — c00971
6. "Existing target doc would be overwritten | Read first, merge content rather than overwrite; record in `[Issues Found]`" — c01395
7. "Comments starting with `%` followed by initials (e.g., `%EM`, `%JH`, `%TB`) are editorial notes between collaborators. You may read and understand these comments to gain context, but you must NEVER remove, modify, or suggest removing them." — c01164
8. "If a requirement is ambiguous: do not guess. Ask one specific clarifying question. Frame it as Given/When/Then to show exactly what's unclear." — c01425
9. "`/utility-doc-audit` は**ユーザー起動専用**。自分で起動せず、判定結果を依頼 1 行にしてユーザーに委ねる" (the audit command is user-only: do not launch it yourself; turn the verdict into a one-line request and leave it to the user) — c00935
10. "Follow `oma-docs` host-LLM contract — CLI emits structured data, you do natural-language synthesis and patch drafting" — c00060. This splits the work: a deterministic tool produces the facts and the writer only phrases them.

## 4. Bearing on the PROPOSED WRITER

Labels: **supports**, **contradicts**, **adds** (something the proposal does not have). Counts are owners unless stated. Lines marked "interpretation" are my inference, not something the corpus states.

### Point (1): start from the reader and what they will do with the document
- **Supports, weakly.** This dimension says little about the human reader. When it does, the reader is often the next agent. Theme 4 (18 owners) shapes output for a downstream consumer: "Your output will be used directly by the parent agent … complete, ready-to-use content" (c00064). c01232 says a PRD is "the single source for both human reference and downstream agents".
- **Adds.** An unclear audience is one of the listed triggers for asking (c00741 "The feature's purpose or intended audience is unclear"; c01537 asks about "target audience"). Interpretation: a writer that starts from the reader needs a fallback for when the brief does not name the reader, and theme 1 is the corpus's answer.

### Point (2): every factual sentence is traceable to evidence, and interpretation is marked
- **Supports.** Theme 12 (13 owners) routes facts to the people or agents who own them before the sentence is written. c00785 is the sharpest version: ask "what is this verdict actually allowed to claim?" before writing it. Theme 15 (10 owners) surfaces code-versus-docs discrepancies and assumptions instead of resolving them silently, which matches marking what is not established. Sharp item 10 (c00060) puts facts in a CLI and synthesis in the writer.
- **Adds: cross-file consistency.** Themes 6 and 8 (18 and 16 owners) treat evidence as more than one sentence to its source. A doc must stay in sync with the code it describes, and with its indexes, translations and mirrors. The proposal's point 2 is sentence-level only. Interpretation: almost every theme-8 line names a repo-specific file (a traceability matrix, a Portuguese README, 24 generated mirrors). That supports the proposal's design choice of carrying these rules in path-scoped rule files rather than in the role.

### Point (3): cutting is the default, and working notes go to a separate output
- **Supports the separate channel.** Theme 4 separates the deliverable from the report to the caller (c00939 "Write output to file, send brief completion message"; c01020 "separate decisions, blockers, warnings, and follow-up options"). Theme 15 supplies what goes in that report: decisions for the owner, discrepancies, and assumptions.
- **Contradicts cut-by-default, when the text already exists.** Theme 11 (15 owners) preserves existing content: update in place, do not fork (c00184), keep working prose (c00971), mark findings superseded instead of deleting them (c00611), respect the human author's voice (c01213). Theme 7 requires sign-off before a major restructure. Its independent reach is small (section 2), but it points the same way. Interpretation: the proposal should limit "cutting is the default" to the writer's own new text. For existing text, the corpus default is to preserve it and flag removals.

### Combining drafts by claim, with a claim → source → tier ledger
- **Not attested.** Nothing in this dimension combines drafts claim by claim, ranks evidence tiers, or returns a ledger. The closest lines give the combining job to someone else: c00026 ("You are not the final writer; the primary agent will synthesize your draft with a separate review", copied into 13 repos) and c00817 ("you integrate the sub-agent findings with your own reading"). This is an absence, not a contradiction. The ledger is the proposal's own design and has no support here.

### The writer does not judge its own output
- **Supports, with a different judge.** Theme 10 (15 owners) separates authoring from review and forbids self-approval. In the corpus, the judge is a reviewer agent, an editor or a human, not runs or evals.
- **Adds a revise-mode protocol.** When findings come back, fix only the named findings (c00397). A reviewer does not edit (c01363).

### One general writer, with doc-type differences carried outside the role
- **Mostly supports.** The type-concentrated behaviors in this dimension are few and belong in a brief or rule. Theme 9 (question protocol) sits in prd-spec at 4.6x lift. Interpretation: that one is an interaction mode that happens before any file is touched, so a path-scoped rule, which loads when a matching file is touched, would load too late. The caller's brief, or a separate interview step, is the right carrier for it.
- **Counter-evidence is concentrated.** The per-type or per-facet writer splits (dialogue writer, emotion writer, prose writer; ad, funnel and conversion copywriters) come almost entirely from tiny-flowlab and caioimori (section 2). Across independent owners, this dimension does not show a pattern of many narrow writers.

### What this dimension has that the proposal lacks
- **Missing information, in unattended runs.** The largest family here is human gates (93 of 247 owners): ask, propose and wait, confirm. The proposal says nothing about what the writer does when the brief is incomplete. Interpretation: a subagent in an unattended flow cannot use the majority pattern. The fitting minority is "state assumptions, proceed, report them" (c01056, and 5 owners in the never-ask group), combined with theme 15's flag-to-owner. If the role does not say this, the corpus prior leans toward stopping to ask.
- **Role and tool boundaries.** Theme 3 (18 owners): report needed code changes instead of making them (c00779), and do not spawn or chain other agents but name them for the orchestrator (c01591). Git boundary (7 owners): the writer does not commit. None of these is in the proposal.
- **Following existing conventions.** Theme 5 (18 owners) has the writer read existing docs, the style guide or a related skill before writing. This fits the proposal's path-scoped rules, but the role still needs the habit of looking for them when no rule has loaded.
