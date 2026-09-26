# Output: recurring themes

Source: `claims/output.jsonl`, 233 quote lines from 184 distinct design-role records (146 agents from 126 owners, 38 skills from 30 owners) by 153 distinct owners. Theme assignment is by quote line, and a line can sit in two themes. The ids per theme are in `output.assign.json`, in the same order as below; every count here was computed from that file joined with the claims file. The 15 top themes cover 184 of the 233 lines, from 156 records and 134 owners. Three smaller themes (variants, diagrams, brevity) are kept in the assign file under a `minor:` prefix and discussed in sections 2 to 4. The remaining 35 lines are singletons or noise, such as a vendor signature link the page must carry (s0041), a deploy project-name rule (s0046) and a JSON return schema owned by another skill (c00214).

"Concentrates in" lists outputs or modes whose share among the theme's records is at least 1.3 times their share among the 184 records in this dimension, with the count. The numbers are small, so read the ratios as direction only. "Copies" is the sum of `copies_in_repos` over the theme's records, which measures reach, not independence.

## 1. Top recurring themes (ordered by distinct owners)

### T1. Write the deliverable to a named file path, not into chat (`file-path`)
The role names the exact file or directory its output goes to, often with a slug pattern, and sometimes says outright that chat is the wrong place.
- 28 records / 26 owners; agents 24 (23 owners), skills 4 (3 owners). Copies 69.
- Concentrates in: wireframe (13/28, x1.8), design-system-docs (15/28, x1.5), spec-or-handoff (24/28, x1.4).
- Every path is different (`docs/design/`, `.claude/doc/{feature_name}/`, `_workspace/`, `.agents/results/`, `specs/NNN-slug/`), so what recurs is the habit of fixing a location, not any one convention.
- "Visual deliverables in artifacts, not chat. Mockup HTML belongs in the spec dir, not pasted in chat." (c00346)
- "Long specs (>80 lines total): save the full spec to a file at `.github/tmp/design-spec-<feature-slug>.md`" (c00311)
- "Write the current asset to `.copilot-tracking/ux-artifacts/{project-slug}/{subject-slug}/{mode}.md`. A rerun updates that file rather than creating dated duplicates or hidden state." (s0085)

### T2. Critique comes as a structured findings list, ranked by severity or priority (`structured-findings`)
Findings carry a severity tag, are ordered most severe first, and often have fixed fields (problem, impact, fix) or a Before/After table. Some cap the count.
- 23 records / 22 owners; agents 14 (14), skills 9 (8). Copies 42.
- Concentrates in: written-critique (22/23, x2.2), review mode (23/23, x1.7). Under-represented in create (x0.4) and production-code (x0.7). This is a reviewer's format, not a builder's.
- "Findings (ordered by severity): [High|Med|Low] <issue> — <why it matters> — <concrete suggestion> (file:line)" (c00274)
- "Use a markdown table with **Severity**, **Location**, **Before**, **After**, and **Why** columns. Include every change made or proposed, not a subset." (s0066)
- "Prioritize: 3-5 most critical UX concerns, not exhaustive list" (c00240). s0066 says the opposite ("not a subset"), and s0064 caps it at three.

### T3. Specs precise enough to implement without the designer (`spec-handoff`)
Handoff specs give measurements, token names and states, so a developer can build without asking.
- 20 records / 18 owners; agents only (20 records, 18 owners). No skill in this dimension says it. Copies 126.
- Concentrates in: prototype (11/20, x3.7), wireframe (13/20, x2.5), design-system-docs (x1.8), spec-or-handoff (20/20, x1.7), design-tokens (x1.6).
- "Specifications must be detailed enough for implementation without UX designer present" (c00317)
- "Handoff: Specify spacing by token, colors by token name, typography by size/weight/line-height, and always include every state (default, hover, active, focus, disabled, loading, error, empty)." (c00603)
- "Return a component brief — detailed enough for builder to code from without asking questions" (c00659)

### T4. Keep a canonical design document that later agents read (`living-doc`)
A single file (DESIGN.md, design-guideline.md, design-state.md, a decisions log) is the design system's source of truth. The role creates it and keeps it current after every change.
- 16 records / 16 owners; agents 12 (12), skills 4 (4). Copies 105, of which 77 come from c00001.
- Concentrates in: design-system-docs (13/16, x2.3), html-mockup (3/16, x2.3), design-tokens (x1.7), revise-existing (10/16, x1.6).
- DESIGN.md "at the repo root is the canonical visual contract for the project. It follows [Google's DESIGN.md spec]" (c00257)
- "You must create a structured directory layout in the project to document all design decisions for future agent reference." (c00178)
- "Keep a run capsule at `decisions.md` in this run's directory, so the next skill does not need this session." (s0015)

### T5. Give the concrete change, not a description of it (`concrete-fix`)
Recommendations come as exact code, CSS or token swaps. "Fix the colours" is not a recommendation.
- 14 records / 14 owners; agents 12 (12), skills 2 (2). Copies 64.
- Concentrates in: redesign-existing (4/14, x3.1), production-code (6/14, x1.8), written-critique (9/14, x1.5).
- "\"Change `text-primary` on decorative border to `text-muted`\" not \"fix colors\"" (c00133)
- "권고는 항상 코드 레벨 patch. 추상적 advice 금지 (\"focus를 챙기세요\" 안 됨, 정확한 CSS / JSX 변경 emit)." (c00577; roughly: "Recommendations are always a code-level patch. No abstract advice; emit the exact CSS/JSX change.")
- "Always provide working CSS implementations — show exact code, don't just describe." (c00179)
- Counter-voices: c00441 "explain the *why*, don't prescribe pixel values unless asked"; c00607 "No fixes. No edits. No code changes."; c00267 "No massive code dumps".

### T6. Tokens are delivered as a machine-readable artifact (`tokens-artifact`)
Tokens go out as JSON (often W3C DTCG) or CSS custom properties, in the format the stack consumes, sometimes with a gap analysis.
- 15 records / 14 owners; agents 11 (10), skills 4 (4). Copies 77, of which 49 come from c00006.
- Concentrates in: design-tokens (14/15, x2.5), prototype (x1.8), design-system-docs (x1.7).
- "Write canonical `tokens.json` in W3C DTCG format." (c00193; the same line is in c00262, same owner)
- "Include the tokens **in the format that matches the project's stack**" (c00290)
- "then propose the minimum token set that covers ~90% of usage, and call out which tokens are missing." (c00314)

### T7. A review ends in a score or a fixed verdict token (`score-or-verdict`)
Either a numeric score or grade, or a closing token such as `APPROVE` or `Block` that a caller can parse.
- 16 records / 13 owners; agents 9 (9), skills 7 (4). Copies 22.
- Concentrates in: written-critique (16/16, x2.3), review (16/16, x1.7).
- "End with `Block` when any `HIGH` remains, `Approve` otherwise, leaving the rest in the table as work to do." (s0067; near-identical in s0069, s0070, s0071)
- "`UX_DECISION: PASS` or - `UX_DECISION: CHANGES`" (c00383)
- "**Grade:** A / B / C / D (A = award-worthy, B = solid, C = needs work, D = significant issues)" (c00680)

### T8. Say why for each design decision (`rationale`)
Each non-obvious choice comes with a short reason, often tied to a named principle or guideline.
- 12 records / 12 owners; agents 9 (9), skills 3 (3). Copies 25.
- Concentrates in: redesign-existing (6/12, x5.4), production-code (9/12, x3.1), revise-existing (9/12, x2.0). Rationale is asked for mostly when the role changes existing UI or code.
- "Add a brief rationale for any non-obvious design decision (e.g. why a specific easing curve or spacing value was chosen)." (c00371)
- "After editing, give a one-sentence summary of what changed and why it achieves the desired look" (c00081)
- "Return the absolute file path, the names and tradeoffs of the directions, and the visual decisions deliberately deferred to a later mockup or prototype." (s0094)

### T9. Follow a fixed template or section list (`template-structure`)
The output fills a named template file or a fixed list of sections.
- 13 records / 12 owners; agents 11 (10), skills 2 (2). Copies 25.
- Concentrates in: design-tokens (8/13, x1.7), production-code (5/13, x1.6).
- "If the skill defines a strict report or artifact format, follow it exactly." (c00194)
- "Write docs/DESIGN.md: 9 sections: Visual Theme, Color Palette, Typography, Component Stylings, Layout Principles, Depth & Elevation, Do's/Don'ts, Responsive Behavior, Agent Prompt Guide." (c00430)
- "Produce `STYLE.md` using `ai_docs/templates/STYLE.template.md` with fonts, colors, tokens, visual constraints, and source-of-truth references when applicable." (c00427)

### T10. The deliverable spells out every UI state (`states`)
Default, loading, empty and error, sometimes hover, focus, disabled and disconnection, each named in the output.
- 11 records / 11 owners; agents 10 (10), skills 1 (1). Copies 35.
- Concentrates in: prototype (5/11, x3.1), wireframe (6/11, x2.1), spec-or-handoff (10/11, x1.5).
- "States: - default: [description] - loading: [description] - error: [description] - empty: [description]" (c00294, line breaks flattened)
- "Real-time data must define update frequency, stale threshold, and disconnection state." (c00354)
- "Produces `flow.md` in `.caf/discovery/{slug}/` for human review. Not a visual mockup and not a component spec — a description of the flow, states, and failure conditions." (c00342)

### T11. The report back to the caller says what was made, where, and what was left out (`return-report`)
A closing summary names the artifact and its path, the states covered, the tokens used, what was deferred or not verified, and who acts next.
- 14 records / 11 owners; agents 12 (10), skills 2 (1). Copies 32.
- Concentrates in: prototype, production-code and design-tokens (each x1.5), revise-existing (x1.3).
- "Return the absolute file path, the fidelity mode, the scenario modeled, the states implemented, and the production behavior deliberately left out." (s0093)
- "Give a one-line summary of what you built (e.g., \"Built a 4-screen mobile onboarding flow with the Indigo style guide.\"). Do not dump JSON, node trees, or raw DSL into the chat." (c00490)
- "End with a `handoff:` line naming who acts next." (c00380)

### T12. Findings cite the exact file and line (`cite-location`)
- 10 records / 10 owners; agents 7 (7), skills 3 (3). Copies 18.
- Concentrates in: written-critique (8/10, x1.9), review (9/10, x1.5).
- "Suggesting changes without specific file:line references" (c00113, listed as a failure)
- "every fix-hint/next-step must name the *real* path/command, never a literal `<path>`; suggested commands must actually run" (c00650)
- "A finding without reproduction + evidence + suspected location is rejected." (s0072)

### T13. Claims rest on observation or sources, and unverified items are named (`evidence`)
Visual claims come from what was seen or from a cited source. What could not be checked is said.
- 10 records / 10 owners; agents 8 (8), skills 2 (2). Copies 14.
- Concentrates in: written-critique (6/10, x1.4). No clear create or build skew.
- "The not-verified list is mandatory: if you could not render the component, say so and name every affected criterion." (c00581)
- "Start with 'From the visual evidence, I observe...'" (c00203)
- "Never include screenshots or image data in your report. Describe what you see in words." (c00680)

### T14. HTML mockups are self-contained files that open in a browser (`html-artifact`)
- 9 records / 9 owners; agents 6 (6), skills 3 (3). Copies 16.
- Concentrates in: html-mockup (5/9, x6.8), production-code (x1.9).
- "HTML examples are photographs — static, self-contained, double-click-openable, visually accurate." (c00335)
- "Build the mockup as a self-contained, interactive HTML file that demonstrates the real interactions and renders at mobile, tablet, and desktop widths" (c00597)
- "Static mockup -- a single `mockup.html` openable in a browser, stdlib-served-friendly, no JS" (c00346). This conflicts with c00387 ("MUST create HTML/CSS prototypes - production-ready, interactive demos") on interactivity.

### T15. Ask before writing files (`approval-gate`)
The role waits for a human's yes before it writes, or asks the human to pick an option.
- 8 records / 8 owners; agents only (8 records, 8 owners). Copies 40.
- No strong skew (spec-or-handoff and wireframe x1.5).
- "Get approval before writing files" (c00017; identical in c00150)
- "Present mockups in a numbered format and ask the user to select their preferred option." (c00208)
- "Produce design guidance as response sections, not as repo edits, unless the parent agent explicitly changes your sandbox or task." (c00198)
- Opposite: "Apply changes directly to the files — do not just suggest code blocks" (c00081).

## 2. Lineage warnings

- **T3 spec-handoff**: c00003 and c00256 share the line "Generate detailed design specifications with measurements" (c00003), and c00069 has the Chinese version "生成包含尺寸的详细设计规格" (c00069) from one `design-ui-designer` template, so they are one voice across 3 owners. verifywise-ai contributes 3 records (c00602, c00603, c00605), which are one matched role set. That leaves about 14 independent voices, not 18. The 126 copies are mostly c00003 (62) and c00007 (39).
- **T4 living-doc**: 77 of the 105 copies are c00001 alone. The owner count (16) is sound.
- **T6 tokens-artifact**: c00193 and c00262 (kinncj) carry the same sentence. 49 of the 77 copies are c00006, a context-manager template family. c00074 in that family is not in this theme, but it shares c00006's boilerplate "Delivered comprehensive design system with 47 components, full responsive layouts, and dark mode support." (left unassigned in both records).
- **T7 score-or-verdict**: 4 of the 7 skill records are jakubkrehel (s0067, s0069, s0070, s0071), all with the same Block/Approve sentence. On the skill side that is 4 owners, and one of them supplies most of the lines.
- **T15 approval-gate**: c00017 and c00150 come from one game-studio family and share the exact sentence. Copies (40) are mostly c00017 (18) and c00036 (11). About 7 independent voices.
- **T9 template-structure, T1 file-path, minor:diagrams**: thebobhuff's paired ui/ux agents (c00427, c00428) are one design with two roles.
- **T11 return-report**: 14 records but 11 owners. microsoft, semaj90 and plannotator each contribute two records.
- **minor:brevity** (9 records, 6 owners): 4 records are davepoon's meeting-roleplay set (c00504 to c00507, "Under 250 words per contribution."). Without it the theme is 5 scattered voices.
- **T2 structured-findings** is spread widely (22 owners out of 23 records). Only jakubkrehel repeats.

## 3. Sharp but rare (1-2 owners, unusually operational)

1. "Return the absolute file path, the fidelity mode, the scenario modeled, the states implemented, and the production behavior deliberately left out." (s0093). A complete return contract for a prototype, in one sentence.
2. "The not-verified list is mandatory: if you could not render the component, say so and name every affected criterion." (c00581). This is the fallback when no renderer is available.
3. "Names describe the direction... never \"Option A/B/C\"." (s0108)
4. "One root cause is one finding. List every confirmed location in the same row rather than one row per occurrence." (s0068; also "One row equals one root cause." in s0110)
5. "If no candidate survives, write `No supported findings were found.` under `## Findings` and `No supported recommendation.` under `## Improve first`." (s0064). A fixed empty result, so the reviewer is not pushed to invent findings.
6. "every fix-hint/next-step must name the *real* path/command, never a literal `<path>`; suggested commands must actually run" (c00650)
7. "Write the current asset to `.copilot-tracking/ux-artifacts/{project-slug}/{subject-slug}/{mode}.md`. A rerun updates that file rather than creating dated duplicates or hidden state." (s0085)
8. "If `design-system/<project-slug>/MASTER.md` already exists, `--persist` **skips writing and leaves it untouched** unless you also pass `--force`" (s0039). The existing design system is protected by the tool, not by prose.
9. "Output a one-line \"Design Read\" before generating" (s0005). A cheap way to commit to a direction before building.
10. "Treat any brand/source provenance as internal inspiration. In user-facing summaries, use the neutral archetype ID and concrete token decisions." (s0025). The opposite rule appears in s0030: "在生成代码中注释说明哪部分来自哪个品牌" ("annotate in the generated code which part comes from which brand").

## 4. Bearing on the proposed designer

Context: the `output_contract` flag is set on 310 of 405 design roles (77%). In this dimension the biggest themes are about where the output goes (T1, T4) and how critique is formatted (T2, T7, T12). Very few are about what a builder hands back (T11: 11 owners).

**Caller-set output form.** Supported indirectly. The corpus has many single-form roles (spec writers, token authors, mockup builders, reviewers), and each hard-codes its own form and path. No record lets the caller choose the form. The format themes split cleanly by mode: T2, T7 and T12 sit almost entirely in review/written-critique, while T3, T6, T10 and T14 sit in create/prototype/wireframe. One role covering both would carry two unrelated format sets. That argues for format details coming from the brief or a skill, not the role text.

**(1) Start from the existing product.** Supported and extended. T4 (16 owners) treats a canonical design doc as the system's source of truth, and T6 asks for tokens "in the format that matches the project's stack" (c00290). New from the corpus: when the designer creates or updates such a doc, the guard belongs in a mechanism (s0039's no-overwrite unless `--force`). The deviations part of point 6 has one direct precedent: "Rate: ✅ Matches spec | ⚠️ Minor deviations (list them) | 🔴 Significant deviations (must fix)" (c00399).

**(2) Name user and task, commit to one direction or give variants.** Weakly covered in this dimension. Variants appear in 5 records from 5 owners (minor theme). c00360 says "Never present only one option — always offer alternatives", which contradicts committing to one direction unless the brief asks for variants. s0108 (name directions by what they are) and s0005 (one-line Design Read before generating) are small, concrete ways to state the direction. T8 rationale (12 owners) supports "the direction and why" in the return.

**(3) Render and look before reporting.** Thin here. Only T13 (10 owners) touches it. c00581's mandatory not-verified list is the right fallback for a role that cannot assume a browser. It supports making "rendered: yes/no, and what was not verified" part of the return rather than assuming screenshots. c00680 ("Never include screenshots... Describe what you see in words") conflicts with returning screenshots, though its reason (keeping image data out of a text report) fits the proposal's "screenshots or paths". Returning paths, not inline images, reconciles the two.

**(4) States, responsive, accessibility baseline.** T10 (11 owners, mostly agents) supports states as an output requirement, concentrated in prototype and wireframe work. c00354 adds a data-freshness state (stale, disconnected) that the proposal's list (empty, loading, error) lacks. c00597 ties responsiveness to the artifact itself (renders at mobile, tablet and desktop widths). Accessibility mostly shows up in other dimensions, not here.

**(5) Boundary: the designer decides and prototypes, the implementer integrates.** T3 (18 owners, about 14 independent) is the strongest agent-side theme that bears on this, and it adds something. When the designer does not integrate, what it hands over must be spec-grade: tokens by name, measurements, every state. A prototype alone is not enough. T15 and c00198 show the other side: some roles stay out of the repo unless told otherwise, and c00081 edits directly. The proposal's "unless the brief says otherwise" matches that split. c00081's direct edits are one voice (microsoft).

**(6) Return what was made, direction and why, screenshots or paths, deviations, open questions; no self-judgement.** T11 supports the return contract, and s0093 and s0094 are close to the proposal as written. They add "production behavior deliberately left out" and "decisions deliberately deferred", which the proposal lacks and which help the implementer. On self-judgement, the corpus leans the other way: T2, T7 and T12 (22, 13 and 10 owners) are all self-contained review formats, and some builder roles self-score (c00003's "95%+ consistency" target, c00006's boilerplate brag). Those formats belong to a separate reviewer, which supports keeping them out of the designer. c00581's "what acceptance criteria you verified" is factual verification, not quality judgement, and fits the proposal.

**Where this dimension's content belongs**
- **Role text**: the return contract (what, path, direction and why, states covered, deviations, deferred or not-verified items, open questions, next actor), and the rule to put deliverables in files rather than chat. Both are short and apply in every project (T1, T11, s0093, c00581).
- **Caller brief or project rule file**: the concrete path conventions (T1: 26 owners, no two alike), the living-doc name and format (T4), the token format (T6), and any template (T9). These are per-project and should not be baked into the role.
- **Skill**: spec-handoff detail (T3), the per-state checklist (T10) and HTML mockup conventions (T14), loaded when the brief asks for that output form.
- **Reviewer role, not the designer**: severity-ranked findings, file:line citations, scores and verdict tokens (T2, T7, T12).
- **Tool or check**: verdict tokens and return fields are parseable, so a script can check them, as with c00214's JSON schema and s0064's fixed empty-result strings. Overwrite protection for the canonical design doc also belongs in a tool (s0039).
- **Nowhere**: word caps and "no preamble" (minor:brevity, mostly one owner), the approval gate for an unattended subagent (T15, a human-in-the-loop habit that clashes with caller-set briefs), and self-scoring targets like "95%+ consistency".
