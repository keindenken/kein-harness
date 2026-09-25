# Scope-boundary themes in writing-role agents

Source: `claims/scope-boundary.jsonl`, 960 quote lines from 626 distinct records, 515 repos, 493 owners. All 960 lines were read. Each line was tagged by hand into one or more themes (777 lines tagged; the 183 untagged lines are mission statements, domain content rules such as CTA limits, or one-off project facts). The counts below are computed from those tags by script, not estimated. The tagging is one reader's judgement, so the theme boundaries are interpretation; the counts within a boundary are exact.

Counts are distinct records / distinct repos / distinct owners. "Lift" is the share of the theme's records carrying a doc type divided by that doc type's share among all 626 records (1.0 = no concentration). The base is dominated by project-docs (356 of 626 records) and api-reference (185), so a theme that sits mostly in project-docs with lift near 1 is simply following the corpus.

## 1. Top recurring themes (by distinct owners)

### 1. The writer does not write or change code; it edits documentation only
132 records / 125 repos / 123 owners. Mostly project-docs (97) and api-reference (56); mild lift in api-reference, code-comments, changelog (about 1.4). Includes "never implement", "docstrings only", "do not change logic".
- "Only edit markdown files (.md). Never modify code files, config files, or anything that isn't documentation." (c00002)
- "Never modify source code, tests, configs, or build files. If a doc change seems to require a code change, STOP and report it instead of doing it." (c00964)
- "Don't change application code to make the docs true — that's a separate ticket. Report the mismatch." (c01364)

### 2. Stay in your lane: name the role that owns what you do not
77 records / 65 repos / 62 owners. Spread across doc types; strongest lift in fiction-narrative (14 records, lift 3.9). Most lanes are drawn against implementation, architecture, or planning roles rather than against other writers; the writer-vs-writer splits are concentrated in fiction and marketing.
- "Do NOT touch `lib/` or `spec/` (including inline YARD comments) — that belongs to the `ruby` agent." (c00346)
- "content-strategy decides WHAT to write (topic clusters, calendars, prioritization). This agent writes and polishes the piece. Route planning-only requests there." (c00521)
- "Decline commit messages, pull-request descriptions, changelogs, release notes, and diary entries; those remain with the caller." (c01209)

### 3. Write only to an allowlist of paths or to the files the caller names
67 records / 61 repos / 61 owners. project-docs (43), prd-spec (13, lift 1.3), report-analysis (11). Themes 1 and 3 together: 170 records / 157 repos / 155 owners, a third of all owners in this dimension.
- "Edit ONLY the files named in your brief. Read each file fully before editing." (c00963)
- "Do not expand your own write scope. If the task needs an off-lease file, stop and report blocked." (c00934)
- "ONLY write to the output path you were given." (c01239)

### 4. Minimal footprint when updating: change only what is stale or asked; do not rewrite, restructure, or reformat the rest
48 records / 47 repos / 46 owners. project-docs (37, lift 1.4), changelog (9, lift 1.45).
- "Never reformat or \"tidy up\" docs you were not asked to touch — that hides the real change in the diff" (c00369)
- "Update only the sections that are stale — do not rewrite unrelated content." (c01019)
- "Supplement mode must NEVER modify, reorder, or rephrase any existing line in the file. Only append new ## sections that are completely absent." (c00006)

### 5. Hands off generated, archived, human-owned, or other-role artifacts
46 records / 40 repos / 39 owners. project-docs (27); marketing-copy lift 2.2 comes entirely from one owner (see lineage).
- "Never hand-edit generated assets: docs/logo.png, docs/pipeline.svg, and the docs/cli/ Markdown reference" (c00711)
- "Never edit `CHANGELOG.md` — Versionize generates it." (c00787)
- "The README is written exclusively by humans. Never modify it; notify if it's out of spec." (c01103)

### 6. Document only what exists: no planned features, invented capabilities, or promises
34 records / 33 repos / 33 owners. project-docs (22), api-reference (12), changelog (8, lift 1.8).
- "Document what exists, not what might exist; no speculative sections" (c00183)
- "Never introduce new product promises not supported by existing docs/specs." (c00170)
- "Asked to write aspirational docs for unbuilt features as if they exist — mark them clearly as planned, or decline." (c01127)

### 7. Keep implementation detail out: public surface only, and specs say WHAT not HOW
34 records / 33 repos / 32 owners. Strongest doc-type concentration of any top theme: prd-spec 21 of 34 records (lift 4.0); also code-comments (lift 1.7), api-reference (1.4). The same principle takes two forms: "public API only" in project/API docs, "no implementation" in specs.
- "Focus on WHAT, not HOW (no implementation details)" (c00588)
- "Document the **public API surface only** — do not expose internal implementation details" (c00337)
- "Presentation properties (dimensions, spacing, color, icon glyphs) stay out; they change without a requirement change and would make this document stale" (c00684)

### 8. Do exactly the requested task and nothing adjacent; often one item per invocation
34 records / 31 repos / 30 owners. project-docs (17); lift in code-comments (2.2) and fiction-narrative (3.2).
- "Scope creep: Documenting adjacent features when asked to document one specific thing. Stay focused." (c00508)
- "Stay in scope. If asked for the auth module README, don't also rewrite the database docs." (c00694)
- "One example per invocation. Do not attempt to create multiple example files in one shot." (c00929)

### 9. Do not duplicate; link to the canonical source (code, config, another doc)
27 records / 27 repos / 27 owners. project-docs (23, lift 1.5), api-reference (13, lift 1.6).
- "Maintainable — Prefer linking to source-of-truth over duplicating information that will drift" (c00314)
- "Suspect a sentence that is helpful rather than owned. The commonest defect in this tree is a correct rule written in a second place; it reads like diligence and behaves like drift." (c00936)
- "Do not restore tables, charts, or per-module pages: a copy of a moving number is wrong the day after it is written." (c00812)

### 10. Tool and execution limits: no shell, no web, no spawning agents
27 records / 25 repos / 25 owners. report-analysis lift 1.95, prd-spec 1.45. Many of these restate a tool grant in prose.
- "CANNOT RUN CODE** - you have no bash access, cannot verify examples work" (c00121)
- "Do NOT spawn other agents or coordinate work. You are a writer, not a manager." (c01350)
- "Fetch anything. You have no `WebSearch`, `WebFetch`, or MCP tools, and that is intentional." (c00248)

### 11. When editing someone else's text, preserve meaning: no new claims or facts, technical content untouched
24 records / 24 repos / 24 owners. Concentrated in editing/polishing roles: academic (lift 9.5), other (5.2), blog-article (4.9), fiction (2.7). This is a mode (polish an existing text) more than a doc type.
- "내용은 단 한 글자도 더하거나 빼지 않고, 문체·리듬·어휘·구조만 조정한다." [Do not add or remove a single character of content; adjust only style, rhythm, vocabulary, structure.] (c00126)
- "Preserve technical accuracy exactly. Never change a command, API name, type, path, flag, version number, or code sample." (c01028)
- "Do NOT change the argument or add new claims" (c00766)

### 12. Stop and ask or escalate on ambiguity, missing input, or a human decision; do not guess
26 records / 24 repos / 23 owners. prd-spec lift 1.8. A small counter-theme (3 owners) says the opposite: assume, state the assumption, proceed.
- "If the audience or purpose is missing, stop before guessing and end your report with the specific question." (c01209)
- "If you hit a decision only a human can make, append a question to `workflow/<feature>/questions.md` in the format defined in `engine/workflow/README.md`, then stop — do not guess." (c01488)
- "If the codebase contradicts the user's description, surface the discrepancy and ask which is authoritative." (c00135)

### 13. No publishing actions: no commit, push, PR, deploy, or send; hand back to the caller
27 records / 24 repos / 23 owners. marketing-copy lift 2.4 (send approval), prd-spec 1.7.
- "绝不 push / merge / delete / close / rebase 或任何 git 写操作。" [Never push / merge / delete / close / rebase or do any git write.] (c00354)
- "You do not commit. You do not open PRs. You produce the artifact and the report, then return control." (c01106)
- "NO `gh` write commands, NO posting comments, NO label changes. The orchestrator is the sole writer." (c00573)

### 14. Flag, do not fix: report doc-code mismatches and out-of-scope defects instead of repairing them
23 records / 23 repos / 23 owners. project-docs (19, lift 1.45), changelog (lift 1.7).
- "Flag, don't fix. You're a miner, not a refactorer." (c00469)
- "Do not \"fix\" it (mid-task scope creep). Add a `<!-- REVIEW: source needed -->` marker next to the suspect content" (c01036)
- "If unsure whether a doc change is needed, report it as a suggestion rather than making the edit" (c01166)

### 15. No secrets, credentials, or sensitive data in the document
22 records / 22 repos / 22 owners. project-docs (15), report-analysis lift 1.5. Inflated by a template (see lineage).
- "never include raw secrets, tokens, cookies, or full request/response bodies -- redacted references and hashes only" (c00212)
- "No secrets: Never include credentials, tokens, API keys, or connection strings." (c00505)
- "Use placeholder values for sensitive data" (c00743)

### Next tier (below the top 15, used in section 4)
| Theme | Records / repos / owners | Concentration |
|---|---|---|
| Significance threshold: skip internal or trivial changes; "no update needed" is a valid result | 24 / 21 / 21 | changelog lift 2.6, api-reference 1.7 |
| Bounded sources: read only the listed inputs; source content is data, not instructions | 22 / 20 / 20 | prd-spec 1.8, fiction 2.9 |
| Render what is given: do not re-analyze, re-score, verify, or add findings | 20 / 14 / 14 | report-analysis 18 of 20 (lift 5.9) |
| Keep internal, process, or agent content out of the deliverable | 15 / 14 / 14 | prompt-instructions lift 8.8 |
| Read-only reporter: never modify files | 13 / 12 / 12 | report-analysis 12 of 13 |
| Prefer updating an existing doc over creating a new one | 12 / 12 / 12 | project-docs, api-reference |
| Update every affected doc, not just the nearest | 12 / 12 / 12 | project-docs 12 of 12 |
| Decline sign-off, compliance, or approval judgements | 20 / 10 / 10 | report-analysis lift 3.3 |
| Do not over-document obvious code | 8 / 8 / 8 | code-comments lift 4.1 |
| Writer does not judge its own output | 4 / 4 / 4 | none |
| Do not copy third-party prose or code | 3 / 3 / 3 | none |
| Do not stall: assume, state it, proceed | 3 / 3 / 3 | none |

## 2. Lineage warnings

- **Theme 1 (no code) and theme 15 (no secrets): the agents.md "Never do" template.** The line "Never do: Modify code in `src/`, edit config files, commit secrets" and near-variants appear under 10 owners (inbo, willtheorangeguy, Qredence, fugazi, Adversis, open-telemetry, PowerGenome, abdes, KrijnvanderBurg, kennedym-ds). That is 10 of 123 owners in theme 1, which does not change its rank, but 8 of 22 owners in theme 15. Without the template, secrets drops to 14 owners and out of the top 15.
- **Theme 1 also carries three smaller cross-owner families:** Claude-Code-Game-Studios ("Write code or implement dialogue systems", Donchitos c00000 with 130 repo copies, and bullish0x c01376/c01377); the al-folio theme ("Modify source code files (`_layouts/`, ...)", Dao-AILab and CalaW); and "No bash. Only edit markdown and docs." (48Nauts-Operator and ScorpionConMate). Together these add 5 owners from 3 voices.
- **Theme 8 (exact task): the oh-my-claudecode writer.** "Document precisely what is requested, nothing more, nothing less." appears under 4 owners (yangyuan-zhen, zereight, LimiNode, Yeachan-Heo), two of which also carry "Scope creep: Documenting adjacent features...". Independent owners are about 27, not 30.
- **Theme 2 (lanes): the fiction concentration is lineage.** tiny-flowlab alone has 6 records (Action/Dialogue/Emotion/Prose Writer lanes), and the Game Studios family adds 2 owners. The lift of 3.9 in fiction-narrative comes from a handful of multi-agent fiction generators, not from many independent fiction writers.
- **Theme 5 (hands off): caioimori.** Six records repeat "Do not modify Claude Code configuration as part of Codex activation." That line is an install rule, not a writing rule, and it produces the whole marketing-copy lift. Owners (39) are unaffected; records (46) are inflated by 5.
- **Theme 3 (allowlist) and "render what is given": tractorjuice (arckit).** Five records in theme 3 ("Modify any file outside `{project_path}/research/`...") and 7 of 20 records in render-only come from one generator. Render-only has 14 real owners, but its record count and quote volume come mostly from one voice.
- **Significance threshold: affaan-m's doc-updater translated.** The ALWAYS/OPTIONAL trigger list appears in English, Spanish, Korean, and Turkish (c00079, c00470, c00476, c00480), with the same list again under 0xb7a7dd61 (c00199). Five records, one template.
- **Decline sign-off: two owners are half the records.** jmagly (6 records of "Cannot verify ...") and kesslernity (4) account for 10 of 20 records. Only 10 owners.
- **Theme 13 (no publishing): UitbreidenOS.** Four records are one sentence in four languages ("No sends without explicit approval.").

## 3. Sharp but rare (1–2 owners), adoptable by a writer role

1. "The document you produce is drafted, not reviewed: a reader other than you runs the review" (c01283, riekelt). States the writer/judge split as a property of the output.
2. "내용 변경 금지: 표현만 다듬고, 구조·내용 수정 제안은 {slug}/editor_notes.md에 기록" [No content changes: polish expression only; record structural or content suggestions in {slug}/editor_notes.md] (c00943, tobyilee). A named side file for the notes that must stay out of the deliverable.
3. "Do not \"fix\" it (mid-task scope creep). Add a `<!-- REVIEW: source needed -->` marker next to the suspect content" (c01036, Kanevry). An in-place marker for an unsourced claim, with no rewrite.
4. "Fix issues directly with Edit when the fix is mechanical (a renamed binding, a moved path, a count). Report issues that need human judgement." (c01323, chris-mclennan). A usable line between fixing and flagging.
5. "Do not restore tables, charts, or per-module pages: a copy of a moving number is wrong the day after it is written." (c00812, polydera). A reason to leave volatile figures out, not only a rule.
6. "Suspect a sentence that is helpful rather than owned. The commonest defect in this tree is a correct rule written in a second place; it reads like diligence and behaves like drift." (c00936, KiwiCanopy). A cutting heuristic keyed to ownership, not length.
7. "Investigation exceeds 5 reads without producing draft | STOP. `[Status]: ESCALATE` with `[Reason]: insufficient source signal`" (c01395, listener-He). A numeric read budget with a named exit status.
8. "Accept work only from a parent packet that names the owning skill, exact canonical role path, verified evidence sources, expected report shape, permissions, stop conditions, and integration owner." (c00403, YuChia-Wei). A checklist for the brief, which is where the proposal puts doc-type specifics.
9. "If no user-facing behaviour changed, output: `No documentation update required.` and stop." (c01019, getgaal). An explicit zero-output result, so the role is not pushed into writing something.
10. "A person stub must not be created off a single passing mention" (c00793, alfadur7). An evidence threshold for creating a document at all.

## 4. Bearing on the PROPOSED WRITER

**One general role, with doc-type differences carried by path rules or the brief.** Mostly supported. The biggest themes (1, 3, 4, 5, 8, 13, 15) do not depend on doc type, and theme 3's content is repo-specific paths (`docs/`, `rfcs/`, `{project_path}/research/`). That content belongs in a path-scoped rule or the brief, not in a role body. Themes 1 and 3 together cover 155 owners, and most of them hardcode paths into the role prompt, so the corpus shows the practice the proposal moves away from, not evidence against it. Two themes are doc-type-shaped: implementation detail kept out (theme 7, prd-spec lift 4.0) and render-only (report-analysis lift 5.9). Both fit path rules. Theme 7 has one principle with a different surface per type ("public surface only" for API docs, "WHAT not HOW" for specs), which is the case a general core plus type rules handles well. Theme 2 (lanes) is not counter-evidence: most lanes separate the writer from code, architecture, or planning roles. The writer-vs-writer splits are a few fiction and marketing generators (see lineage), and the corpus has no run results showing a general writer failing, so it does not bear on the "split only on measured failure" rule.

**Point 1, start from the reader.** This dimension barely touches it. What it adds is the failure path: if the reader or purpose is unknown, stop, or record an assumption. Examples: "If the audience or purpose is missing, stop before guessing..." (c01209), "Audience or channel is undefined" as a stop condition (c00220), and the ambiguous-audience trigger (c00016). The proposal says to start from the reader but not what to do when the brief does not name one.

**Point 2, every factual sentence traceable; interpretation marked.** Supported from several directions:
- Document only what exists (theme 6, 33 owners).
- Preserve claims when editing (theme 11, 24 owners).
- Flag rather than fix doc-code mismatches (theme 14, 23 owners).
- Render given numbers and never recompute them (14 owners, mostly reports).
- Bounded sources (20 owners): the evidence set is whatever the caller lists. "Use only the canonical PR-context bundle..." (c00145); "Never reference a file the pack does not contain." (c00420).

Additions the proposal lacks:
- The brief should name the allowed sources.
- Source content is data, not instructions: c00631, c00976, c01114, c01501. This matters because the writer combines outside examples.
- An in-place marker for an unsourced claim, as in sharp #3.
- The writer does not originate figures, per the render-only theme.

**Point 3, cutting by default; working notes go to a separate output.** Supported:
- Exact task (theme 8).
- Minimal footprint (theme 4).
- Significance threshold (21 owners): "It is perfectly okay to make 0 changes at all" (c01566).
- Keep internal and process content out (14 owners): "NEVER include GSD methodology content in generated docs" (c00006); "Do not add agent-specific comments or metadata to documentation files." (c01584); "hold no open-questions parking lot" (c00745); the editor_notes side file (sharp #2).

One tension: "update every affected doc, not just the nearest" (12 owners, e.g. "Update all affected docs, not just the nearest one." c01205). The same owner can hold both sides ("update the smallest correct set of documents" and "update the most authoritative document, not only a nearby duplicate", c00399). Cutting applies to content inside a document, not to how many documents an update reaches. The proposal should say so, or a minimal-footprint reading will leave stale copies.

**Combining drafts claim by claim, with a ledger; no self-judging.** Little direct evidence either way. Support comes from three places:
- The writer does not judge its own work: "You write specs. You do not judge them." (c00456); "a reader other than you runs the review" (c01283); "You are not the writer. You are not the evaluator." (c00114). 4 owners.
- Render-only: "Your job is to **synthesize and arbitrate**, not to raise new review comments." (c00493).
- Two rare rules against copying outside prose: "Never reproduce large verbatim passages from third-party sources..." (c00170); "Do not copy distinctive prose, examples, diagrams, or code from other repositories." (c01361). They favour taking claims, not text, from outside examples.

Nothing in the dimension ranks evidence into tiers. The ledger idea has no counterpart here.

**What this dimension has that the proposal lacks:**
- **A write surface.** This is the most common scope rule by far (themes 1, 3, 5, 13: 155+ owners). The proposal never says what the writer may touch. A default is needed: only the files the brief names, never code or generated files, and no commit, push, or send. Any extension comes through a path rule.
- **A channel for discrepancies found while writing** (theme 14). The proposal's separate output for the caller is the natural place, but it should say explicitly that doc-code mismatches and out-of-scope defects go there and are not fixed.
- **A stance on missing input** (theme 12, 23 owners stop and ask, against 3 owners who assume and proceed). For unattended runs, the minority form fits: "make a reasonable assumption, state it explicitly in analysis.md, and proceed — do not stall" (c01445), with the assumption recorded in the side output. The proposal should pick one.
- **An edit mode as distinct from a create mode.** Theme 11 (preserve meaning) and theme 4 (minimal footprint) apply when the input is an existing text. They concentrate by task mode (polish, update, append-only changelog), not by doc type. Path rules keyed on doc type will not carry them; the brief has to say which mode applies.
- **A zero-output result** ("No documentation update required.", sharp #9) and a stop budget (sharp #7).
- **Secrets** (14 independent owners after the template). Small but cheap to cover.
- **Tool limits** (theme 10, 25 owners) are mostly tool grants restated in prose. They belong in the role's tool configuration, not its text.
