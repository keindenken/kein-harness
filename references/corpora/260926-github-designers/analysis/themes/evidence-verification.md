# Evidence and verification themes in design roles

Source: `claims/evidence-inspection.jsonl` (187 lines) and `claims/verification-visual.jsonl` (143 lines), every line read. Together they carry 330 quotes from 212 distinct records (159 agents, 53 skills) and 180 distinct owners. 317 lines were assigned to at least one theme; a line can sit in more than one theme. 13 were left out as too generic or off-topic (e1, e36, e45, e68, e78, e79, e122, e137, e164, v3, v16, v54, v133, keyed by file letter and 0-based line number). The id lists are in `evidence-verification.assign.json`, and every count below was computed from those lists joined to `records.json`.

How to read the counts:
- "records / owners" means distinct record ids and distinct owners (the part of the repo before "/"). "Collapsed" also merges known template families across owners (see section 2).
- Concentration compares the theme's records with all 405 design-role records. For example, "review 85% vs 57%" means 85% of the theme's records have mode `review`, against 57% of all design roles.
- Baseline: the `renders_and_looks` flag is set on 82/405 design roles (agents 44/308 = 14%, skills 38/97 = 39%). The claims files hold only specific, verbatim-verified quotes, so they undercount a flag-level behaviour but show how people actually phrase it.

## 1. Top recurring themes (ordered by distinct owners)

### 1. Inspect the existing code and design system, and match it
Before designing, read the product's components, styles, tokens and stack, then reuse and conform to them. Do not introduce a competing system.
- 74 records / 70 owners (collapsed 65). Agents 62 records / 61 owners; skills 12 / 10.
- Concentrates in `revise-existing` mode (61% vs 41%) and in `redesign-existing` (23% vs 12%) and `production-code` (43% vs 34%) outputs. It is weaker than average in review-only roles.
- "Match the project. Use the existing CSS approach, component library, icon set, and animation library. Never introduce a competing one." (c00024)
- "Read before designing. `batch_get` the most recent existing screen root (readDepth 3) and `get_variables` FIRST. The established palette, typography, spacing, radius, and card treatment are now constraints, not suggestions." (c00490)
- "Grep for the existing sibling component first and reuse its container, motion, and typography tokens; inventing a new style needs a stated reason why no existing component fits." (s0112)

### 2. Render the result and look at it before claiming anything
Open it in a browser or run the app, take screenshots, read them, and only then report.
- 42 records / 40 owners (collapsed 36). Agents 27 / 27; skills 15 / 15. Skills over-index: 15 of 97 skills (15%) against 27 of 308 agents (9%).
- Concentrates in `html-mockup` (19% vs 7%), `visual-asset` (17% vs 5%) and `production-code` (43% vs 34%) outputs, and in `review` mode (69% vs 57%). It is rare in `design-system-docs` roles (14% vs 37%).
- "Then Read the screenshot — a prototype is a visual deliverable; don't ship it sight-unseen." (s0076)
- "You must look before you speak. Screenshot every screen or harness at 1280 and 390 wide, in light and dark, with the pointer parked off the UI. Then click the controls." (c00532)
- "Run the harness. Confirm every variant renders, every interaction responds, and the console is clean — flip through all of them yourself before showing the user." (s0108)

### 3. Check a matrix of viewports, and often themes
Screenshots or tests at named widths (375/768/1440 dominate), plus light and dark.
- 27 records / 22 owners (collapsed 21). Agents 17 / 15; skills 10 / 8.
- Concentrates in `redesign-existing` (30% vs 12%) and `visual-asset` outputs, and in `review` (70%) and `revise-existing` (52%) modes.
- The breakpoint sets disagree: 375/768/1440 (c00095, c00320, c00322, c00324), 1280/390 (c00532), 1440×900/768×1024/390×844 (s0092), and "smallest and largest supported widths and at one awkward intermediate width" (s0109).
- "Capture: 375/768/1440 screenshots + snapshot + console per target screen" (c00320)
- "Test both modes - never assume colors work in both" (c00197)
- "Render the product's supported viewport or window range yourself: web breakpoints on both sides, and native minimum width, minimum height, their combination, and normal size." (s0112)

### 4. Read the project's named design documents and supplied inputs first
Read DESIGN.md, the style guide, product brief, PRD, approved palette files, and supplied Figma or screenshots, and treat them as the source of truth.
- 23 records / 21 owners. Agents 19 / 18; skills 4 / 3.
- Weak concentration: slightly more `html-mockup` (13% vs 7%) and `revise-existing` (48% vs 41%). Almost every quote names a project-specific path.
- "Kiểm tra file design system đã có chưa... Nếu có → đọc file đó, dùng làm nguồn sự thật. KHÔNG sinh lại nếu chưa có `--force`." (c00253). In English: check whether a design-system file exists; if so, read it and use it as the source of truth; do not regenerate it without `--force`.
- "**Re-read `design_md_path`** even if you "remember" it. Record the read timestamp in the report header." (c00575)
- "先检查 [artifact:PRD] 与 [artifact:Prototype] 是否齐备；缺失时按 BLOCKED 模板返回。" (c00296). In English: first check that the PRD and prototype exist; if either is missing, return using the BLOCKED template.

### 5. Reading source code is not visual evidence
Code, class names, passing gates or "it compiles" cannot support a claim about how something looks.
- 20 records / 19 owners. Agents 13 / 13; skills 7 / 7.
- Strongly concentrated in reviewers: `written-critique` 75% vs 41%, `review` 85% vs 57%, `create` only 40% vs 79%.
- "NEVER review visual output by reading source code alone." (c00263)
- "You have no `Bash`. You cannot run the app, so you cannot claim how something looks from reading source." (c00380)
- "Gates prove contrast/a11y — they do NOT prove pixels. RENDER AND LOOK." (s0095)

### 6. Admit what was not verified, and never fabricate
When a check cannot run, label it (Not verified, DEGRADED, UNAVAILABLE, Incomplete or BLOCKED). Do not invent findings, screenshots or behaviour, and return an empty result when there is nothing to report.
- 20 records / 19 owners. Agents 11 / 11; skills 9 / 8.
- Concentrates in `written-critique` (65%) outputs and `review` mode (85%).
- "A URL's HTML alone does not prove rendered layout or interaction. If no rendered evidence is available, mark `DEGRADED: no screenshot` and perform a source-only audit." (c00681)
- "A check you cannot run is **Not verified**, never a finding." (s0068)
- "If you could not open the page, say so plainly and report only the heuristic-script results — never invent findings." (c00441)

### 7. Use automated checks and scripts as evidence
Grep for hardcoded values, run token lint, axe, Lighthouse, contrast scripts, or visual-regression baselines, and act on their output.
- 19 records / 17 owners. Agents 14 / 13; skills 5 / 5.
- Concentrates in `prototype` outputs (32% vs 13%) and in `review` (79%) and `revise-existing` (53%) modes.
- "grep -REn '#[0-9a-fA-F]{3,8}\b|rgba?\(' <files-you-wrote>` excluding the token/theme file(s). Any hit outside tokens is a failure" (c00024)
- "Use `visual_baseline` + `visual_compare` for before/after comparisons" (c00263)
- "Run `omd check contrast <page.html>` (in this repo, `node test-v2/tools/text-contrast.mjs`) and quote its numbers." (c00575)

### 8. Every finding cites its evidence
Each claim carries a `file:line`, a screenshot path, or a measured value. Opinions without a source are rejected.
- 17 records / 17 owners. Agents 15 / 15; skills 2 / 2.
- The most review-bound theme: `written-critique` 88%, `review` 94%, `create` 18%.
- "Every verdict MUST cite at least one `<file>:<line>` reference from `source_scope`, OR a screenshot path" (c00639)
- "Every finding cites its evidence — `file:line` (L1), a screenshot you **verified with the Read tool** (L2), or a captured value / snapshot (L3)." (s0078)
- "Every finding cites a token or a named principle — no vibes" (c00320)

### 9. Exercise the states and interactions, not just a static frame
Walk hover, focus, loading, empty, error, keyboard paths, reduced motion and content stress. Build a state harness.
- 21 records / 16 owners. Agents 6 / 6; skills 15 / 11. This is the most skill-heavy theme, with plugin87, jakubkrehel, plannotator and suleimanodetoro each contributing 2-3 records.
- Concentrates in `html-mockup` (24% vs 7%) and `prototype` (19% vs 13%) outputs.
- "Build a **states harness**: render the component in each applicable state (default, hover, focus, active, disabled, loading `aria-busy`, error `aria-invalid`, selected `aria-pressed`/`aria-selected`) × each variant in one HTML file" (s0095)
- "Test the artifact at wide desktop and narrow mobile widths. Exercise every modeled state and control. Test `Tab`, `Shift+Tab`, `Enter`, `Space`, arrow keys where appropriate, and `Escape` for dialogs." (s0093)
- "Verify empty, loading, error, success, long-text, and narrow-screen states." (c00541)

### 10. Ground recommendations in external authority, or look things up
Cite NN/g, WCAG, HIG or Material, check current docs (context7, Sosumi), search reference products, and use named books.
- 17 records / 15 owners (collapsed 14). Agents 13 / 12; skills 4 / 3.
- Concentrates in `written-critique` (65%) outputs and `review` mode (71%).
- "Always cite sources - Include NN Group URLs, study names, research papers" (c00009, and the same text in c00179)
- "ALWAYS use #context7 MCP Server to verify current docs for UI frameworks, component libraries, design systems, accessibility guidance, and platform APIs when they matter to the task." (c00618)
- "Reference real projects, not Pinterest boards." (c00504)

### 11. Evaluate with user research, heuristics or scored rubrics rather than opinion
Base judgments on research, flag assumptions when there is none, and score against Nielsen's heuristics or numeric rubrics.
- 16 records / 15 owners. Agents 15 / 14; skills 1 / 1.
- Concentrates in `wireframe` (44% vs 20%), `prototype` (31%) and `spec-or-handoff` (69%) outputs, and in `review` mode (88%).
- "Base recommendations on user research insights when available; flag assumptions when research is absent" (c00233)
- "For each step, the agent scores 1–5 on clarity, delight, friction, and error quality, and proposes a fix when a score falls below 3." (c00620)
- "4/4 is achievable, 1/4 means real problems, not perfectionism" (c00133)

### 12. Perceptual self-tests: squint, swap, "would people say AI made this", three-second
Quick taste probes run on your own output.
- 14 records / 14 owners (collapsed 12). Agents 6 / 6; skills 8 / 8.
- Concentrates in `production-code` (71% vs 34%) and `redesign-existing` (36%) outputs. It sits in `create` mode (93%), so the maker checks itself.
- "If you showed this interface to someone and said "AI made this," would they believe you immediately? If yes, that's the problem." (s0002, and the same text in s0052)
- "The squint test: Blur your eyes. Can you still perceive hierarchy? Is anything jumping out harshly? Craft whispers." (s0061)
- "Score the artifact out of 10 (10 = maximum slop). State the score and list which tells fired, in one short report." (c00337)

### 13. Measure, do not eyeball
Compute contrast, lift exact values, and sample computed styles. Numbers over impressions.
- 12 records / 11 owners. Agents 8 / 7; skills 4 / 4.
- Concentrates in `written-critique` (75%) and `redesign-existing` (33% vs 12%) outputs, and in `review` mode (92%).
- "Do NOT grade contrast by eyeballing; compute the ratio." (c00639)
- "Never report a contrast value you did not measure, and never estimate a color you could compute." (s0067)
- "Lift exact values: hex codes, spacing scale entries, font stacks, border radii. A rough approximation is not pixel fidelity." (s0112)

### 14. Compare the result against the spec or reference design
Check it against Figma, supplied screenshots or specs, and allow for legitimate rendering variance.
- 11 records / 11 owners. Agents 9 / 9; skills 2 / 2.
- Concentrates in `spec-or-handoff` (73%), `redesign-existing` (27%) and `visual-asset` outputs.
- "Review implemented UI against Figma design intent and screenshot references." (c00486)
- "Some variations might be intentional (e.g., browser rendering differences)" (c00107)
- "Open the downloaded HTML files in the browser using Chrome DevTools MCP to visually inspect each screen. Compare them side-by-side for drift." (c00389)

### 15. Loop: fix, re-capture, and keep before/after screenshots
Iterate until the checks pass, with a screenshot showing the problem and another showing the fix.
- 8 records / 8 owners (collapsed 7). Agents 7 / 7; skills 1 / 1. The records' `copies_in_repos` sum to 101, of which c00001 alone contributes 77.
- Concentrates in `visual-asset` and `html-mockup` outputs (38% each vs 5-7%) and in `review` mode (88%). Small sample.
- "Never fix without a screenshot showing the problem; never close without a screenshot showing the fix" (c00320)
- "Repeat steps 6a–6c until **all screens pass every check**. Do not proceed to documentation or handoff until the checklist is fully green." (c00389)
- "Always save screenshots before making fixes" (s0017)

## 2. Lineage warnings

- **oh-my-claudecode designer family** (c00029 yangyuan-zhen, c00042 Yeachan-Heo, c00077 zereight, c00158 LimiNode, each with 3-13 copies). The shared lines "Match existing code patterns. Your code should look like the team wrote it.", "Detect the frontend framework from project files before implementing" and "Verify: component renders, no console errors, responsive at common breakpoints" appear in many more corpus files than the four clusters. The family puts 4 records into theme 1, and 2 each into themes 2 and 3. Theme 1 drops from 70 to 65 owners once this family and VoltAgent are collapsed.
- **VoltAgent template** (c00033 acbcdev, c00074 davila7): "Always begin by requesting design context from the context-manager" is one voice, and it assumes a context-manager agent that this harness does not have.
- **ClaudeKit ui-ux-designer family** (c00001 mrgoonie with 77 copies, c00028 withkynam with 14, c00384 buisihung11). The thin lines "Use `screenshot` tools to capture and compare" and "capture screenshots and compare" come from one template. They inflate theme 15 by copy count (c00001 is 77 of its 101 copies) and add 2 owners to theme 2 with little operational content.
- **Anthropic frontend-design lineage** (c00114 ye-lynn-htet, s0004 HKUDS, s0037 anthropics): "Critique your own work as you build, taking screenshots ... a picture is worth 1000 tokens" is one sentence copied across three records, and grep finds it in 8 corpus files. It carries theme 2's self-critique strand, which bears on contract point 6.
- **Impeccable / "AI made this" family** (s0002 tech-leads-club, s0052 fengshao1227, and close variants in s0112 tw93 and elsewhere) and the **swap/squint pair** (c00186 et0175, s0061 holaboss-ai). Theme 12 is mostly these few sources. The squint test itself shows up in a dozen corpus files. It is a meme more than an independent convergence.
- **NN/g citation line** (c00009 davila7, c00179 Brahiamm56) is one template. It accounts for 2 of theme 10's 15 owners.
- **One agent in two formats**: kwakseongjae c00575 and c00580 are the same review agent in `.md` and Codex `.toml`. They double themes 4, 7 and 13 by one record each.
- **Single owners with several records**: plugin87 (c00532, s0095-s0097), jakubkrehel (s0066-s0071, 5 skills), Orkas-AI (c00517, s0023-s0025), lobehub (s0076-s0078), bpmforge (c00320-c00322), plannotator (s0093-s0094) and suleimanodetoro (s0109-s0110). Theme 9's 21 records come from only 16 owners for this reason. slabgorb and slabgorb-org ("Find THREE existing examples first") are almost certainly one person under two owner names.
- **Wide-copy but thin**: c00010 tjsasakifln (28 copies) contributes "browser # Test web applications and debug UI", which is a tool listing and not an instruction.

## 3. Sharp but rare

1. "If you take a screenshot, wait until the page settles — a transition captured at frame 0 produces a confident, wrong finding." (c00581)
2. "Prefer an accessibility-tree snapshot over a screenshot when asserting what a component says." (c00581)
3. "Measure a foreground against the background it actually renders on, not the page background." (s0067)
4. "Claims of pixel-exact or visually identical output require fresh source/result rendering at matching viewport, state, theme, and locale" (s0024)
5. "Every finding cites its evidence — `file:line` (L1), a screenshot you **verified with the Read tool** (L2), or a captured value / snapshot (L3)." (s0078). Paired with "The core rule: a verdict must come from a layer that can see it. Don't tick a visual or runtime verdict off the code." (s0078). Both say the evidence layer must match the claim.
6. "A URL's HTML alone does not prove rendered layout or interaction. If no rendered evidence is available, mark `DEGRADED: no screenshot` and perform a source-only audit." (c00681). Also: "Playwright 缺失写 `UNAVAILABLE`，不伪造截图、截图 hash 或键盘结果。" (s0019). In English: if Playwright is missing, write `UNAVAILABLE`; do not forge screenshots, screenshot hashes or keyboard results.
7. "Ikke rekonstruer dagens side fra kode/komponentlesing og presenter det som «slik siden ser ut»." (c00298). In English: do not reconstruct today's page from reading code or components and present it as "how the page looks".
8. "Do not invent missing states from naming alone. Cite the source branch or render that proves the state exists or is absent." (s0110)
9. "Open the result at desktop and mobile widths. ..." together with "Confirm that the directions remain structurally distinct at both sizes." (s0094). This verifies that variants really are different, not only that each one renders.
10. "live URL이 있으면 WebFetch로 rendered HTML 확인. 정적 코드만 보면 hydration 후 변하는 동작 놓침." (c00577). In English: if there is a live URL, check the rendered HTML with WebFetch; reading only static code misses behaviour that changes after hydration.

Close runners-up: "Then inspect the rendered result at the smallest and largest supported widths and at one awkward intermediate width." (s0109); "Plant one invalid and one valid probe and prove only the invalid form fails." (c00657, for a lint rule the role adds); "Existing product tokens and screenshot structure outrank every pack." (c00517).

## 4. Bearing on the proposed designer

**(1) Start from the existing product.** Strongly supported. It is the largest theme in this dimension (74 records, 70 owners, 65 collapsed), with theme 4 alongside it (23 records, 21 owners). It concentrates in revise/redesign work, which matches the proposal's "unless the brief asks for a new direction". The corpus adds three things:
- a precedence rule: existing tokens outrank any loaded style pack or skill (c00517, s0025 "If an existing app already has clear tokens and components, skip this skill unless the user asks for a new style direction");
- re-read the design files on each run and do not rely on memory (c00575);
- find sibling components before inventing one, and state why when none fits (s0112, c00117/c00312).

The general rule fits in one line of role text. The named paths (DESIGN.md, `docs/design-guidelines.md`, palette.json) belong in project rule files, because nearly every quote in theme 4 names a path specific to its project.

**(2) Name the user and task; commit to a direction or produce variants.** This dimension says little about it. It adds two things. First, name assumptions when no research exists (c00233 "flag assumptions when research is absent"). Second, when variants are asked for, confirm after rendering that they are structurally distinct (s0094). The research-and-heuristics theme (16 records / 15 owners) is mostly review-mode work. Its recruit-5-8-participants and run-web-research-before-any-recommendation forms do not fit a dispatched subagent, so they belong nowhere in this role.

**(3) Render and look before reporting; appearance claims come from inspection, not code.** Supported, and the corpus makes it sharper. 42 records / 40 owners render and look, and another 20 / 19 say explicitly that code is not visual evidence. Skills say it more often than agents (15% vs 9% in the claims; 39% vs 14% on the flag). The corpus adds three things:
- **The missing-tool case is already solved in the corpus, and the proposal needs it.** The answer is a labelled downgrade, not silence: "Not verified" (s0068, s0071), "DEGRADED: no screenshot" plus a source-only audit (c00681), "UNAVAILABLE" (s0019), and "you cannot claim how something looks" (c00380). Theme 6 (20 / 19) is exactly this. Because the role cannot assume a browser, the downgrade rule belongs in the role text.
- **Taking a screenshot is not looking.** "Then Read the screenshot" (s0076) and "a screenshot you verified with the Read tool" (s0078). Wait for the page to settle (c00581).
- **Gates are not pixels.** Automated checks do not stand in for looking (s0095, c00532 "A passing gate is never evidence of taste").
- **Contrary view:** a minority makes rendering opt-in for cost reasons: "Rendered verification is opt-in. Mark visual and runtime claims **Not verified** unless the project exposes a cheap preview or the user asks" (s0071), and "Use rendered evidence only when the user provides it or explicitly requests visual inspection" (s0064). Both are review skills. For a maker whose deliverable is visual, the majority position (render when possible) is better supported. Still, the fallback label is the same in both camps, which supports putting "label it when you cannot render" in the role.

**(4) States, responsive behaviour, accessibility baseline.** Supported (viewports and themes 27 / 22; states and interactions 21 / 16; measurement 12 / 11). The corpus adds that coverage is proven by rendering or exercising each state, walking the keyboard path and computing contrast, not by listing the states (s0095, s0093, c00639, s0067). The details disagree across sources: breakpoint sets differ, and some check both themes while others do not. Those details belong in a skill or project rule. Contrast computation and hardcoded-value detection belong in a tool or check (a contrast script, token lint, grep), which is how the most operational sources ship them (c00575 `omd check contrast`, c00024 grep, s0096 `scripts/contrast.py`). The role text needs only "cover states, responsive behaviour and an accessibility baseline, and verify them by rendering or measurement, or mark them not verified".

**(5) Boundary: the designer prototypes, and an implementer integrates.** Little in this dimension either way. Two indirect supports: "Output fidelity ≠ production-ready ... hand-off code often needs a verification + a11y pass" (s0047), and whole agents exist only to check implemented UI against the design (c00107, c00486, c00203). Both suggest implementation-fidelity review is a separate job.

**(6) Returns; no self-judgment of quality.**
- **Supported and extended on returns.** Theme 8 (17 / 17) and the layered evidence in s0078 suggest each claim in the return should carry its evidence (screenshot path, `file:line`, or a measured number), and should be marked rendered-verified or source-only. MarceloClaro's provenance legend (c00273: extracted from config / inferred from screenshots / referenced but undefined) is a compact form of this. Deviations from the design system can use the same form.
- **Contradicted on "does not judge its own quality".** A visible strand tells the maker to self-critique while building:
  - the Anthropic frontend-design lineage's "Critique your own work as you build, taking screenshots" (3 records, one sentence);
  - the perceptual self-tests (14 / 14, collapsed 12), which are 93% `create`-mode;
  - "Score the artifact out of 10 (10 = maximum slop)" (c00337);
  - "use as the final self-critique pass before delivering UI work" (s0038).

  The two positions reconcile if the proposal separates **verification of fact** from a **quality verdict**. Fact checks are the designer's job and are well supported: did it render, which states exist, the measured contrast, does it match the brief and design system. A quality verdict (is it good or distinctive) goes to review, and plugin87's "A passing gate is never evidence of taste" backs that separation. Taste probes such as the squint and slop tests live in the skills the proposal already puts taste in, so a loaded skill will tell the designer to self-critique. The role should say how that output is used: as a check during building, not reported as a verdict. Otherwise the role and its skills contradict each other.

**Placement for this dimension**
- **Role text** (short, and it holds in every project):
  - inspect the existing product before designing;
  - claims about appearance come only from a rendered result the designer actually viewed, and when rendering is unavailable the designer says so and labels those claims not verified;
  - never fabricate screenshots or results;
  - each returned claim carries its evidence and a verified or source-only mark.
- **Skill or project rule file:** viewport and theme matrices, the state-harness method, screenshot settle timing, the perceptual tests, heuristics and rubrics, which design documents to read and in what order, and when to cite external guidelines.
- **Tool or check:** contrast computation, hardcoded-value and token lint, screenshot capture with visual baseline and compare, axe, and Lighthouse. The measure-don't-eyeball theme is best enforced by a tool, not by prose.
- **Nowhere:**
  - "Always begin by requesting design context from the context-manager": the lead's brief already carries that context.
  - "ALWAYS run web research via subagents before making any recommendation" and "Always cite sources - Include NN Group URLs".
  - Recruiting study participants.
