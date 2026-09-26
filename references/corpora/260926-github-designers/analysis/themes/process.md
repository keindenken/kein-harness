# Process themes in design roles

Source: `claims/process.jsonl`, 424 verified quotes from 258 distinct records (190 agents, 68 skills) held by 215 distinct owners. Every line was read and hand-assigned to zero or more themes (354 lines assigned, 70 left unassigned as one-offs or off-topic, e.g. report tone, CLI product goals). Counts below are computed from those assignments against the record metadata; the ids per theme are in `process.assign.json`. "Lift" compares how often an output or mode appears among a theme's records against the 258-record baseline (baseline: spec-or-handoff 136, written-critique 121, design-tokens 98, design-system-docs 91, production-code 89, wireframe 46, redesign-existing 30, prototype 25, html-mockup 22; create 194, review 165, revise-existing 109).

A theme with 20+ owners is common in this corpus only relative to others: no single process instruction appears in more than about 15% of the 215 owners.

## 1. Top recurring themes (ordered by distinct owners)

| # | Theme | Records | Owners | Agents (rec/own) | Skills (rec/own) |
|---|---|---|---|---|---|
| 1 | Name the user and goal before designing | 32 | 32 | 25/25 | 7/7 |
| 2 | Ask clarifying questions | 29 | 26 | 20/19 | 9/8 |
| 3 | Calibrate critique severity and priority | 27 | 24 | 20/18 | 7/6 |
| 4 | Record assumptions, trade-offs, open questions | 24 | 23 | 22/21 | 2/2 |
| 5 | Offer several distinct options | 21 | 21 | 17/17 | 4/4 |
| 6 | Human approval gate before building | 18 | 18 | 13/13 | 5/5 |
| 7 | Load a named skill or generator first | 18 | 18 | 13/13 | 5/5 |
| 8 | Cover all UI states | 19 | 18 | 14/14 | 5/4 |
| 9 | Pre-delivery self-check | 21 | 18 | 12/12 | 9/6 |
| 10 | Read project context files first | 16 | 16 | 14/14 | 2/2 |
| 11 | Follow the existing system: tokens, reuse | 17 | 16 | 12/11 | 5/5 |
| 12 | Fixed phase pipeline, one unit at a time | 14 | 13 | 9/9 | 5/4 |
| 13 | Proceed on stated assumptions | 12 | 12 | 11/11 | 1/1 |
| 14 | Be specific, no vague advice | 13 | 12 | 12/11 | 1/1 |
| 15 | Ground decisions in research or data | 10 | 10 | 8/8 | 2/2 |

Below the cut (all counted, ids in the JSON): commit to a direction before building 9/9 (4 agents, 5 skills); foundations before screens 9/9 (agents only); flows before screens with error paths 9/9; validate with real users 9/9; budget and retry caps 9/9; anti-generic self-review 7/7 (1 agent, 6 skills); match code complexity to aesthetic 7/7; no claim without inspection 7 records/6 owners; named heuristic framework 5/5; inspect the live rendered UI 5/5; real content, not lorem ipsum 4/4.

### 1. Name the user and goal before designing
Before any visual work, state who the user is, what job or goal they have, and what success looks like. 32 records, 32 owners (25 agents, 7 skills). Spread evenly over create and review; mild lift in redesign-existing (1.6) and wireframe (1.4). The most distributed theme in the dimension, with no owner contributing twice.
- "Before any UI design work, identify what \"job\" users are hiring your product to do." (c00002)
- "If you find yourself designing a component before understanding the user goal, stop and restart from step 1" (c00132)
- "Name the success metric first, then judge against it. Onboarding = completion rate + time-to-value + drop-off, not pattern richness." (s0078)

### 2. Ask clarifying questions
Ask the requester when the brief is unclear. 29 records, 26 owners (20 agents/19 owners, 9 skills/8 owners). Concentrates in wireframe (lift 1.7) and html-mockup (1.6); rare in written-critique (0.6). The corpus disagrees on the form: one question at a time, or one batch.
- "Ask exactly **one** clarifying question - never a multi-question dump - and only when the design read genuinely diverges." (s0005)
- "Gather these before designing or writing. Ask only for what is missing, and ask in one batch rather than one question at a time." (s0049)
- "If the user hasn't provided the tool's test output or a schema, you MUST ask before generating. Do NOT guess the data shape." (s0086)

### 3. Calibrate critique severity and priority
In review mode: rank by user impact, use a severity scale and verdict rule, do not inflate or average findings, do not grade taste. 27 records, 24 owners (20 agents/18, 7 skills/6). All 27 records carry written-critique and review (lift 2.1 and 1.6); nearly absent from create (0.3). This is reviewer content, not maker content.
- "If everything you found is Minor, say so plainly and let the work ship. A critique that manufactures Critical findings to look rigorous is as useless as one that praises everything." (c00532)
- "A trigger is a failure whatever the style guide says; a density, radius, or voice you merely disagree with is not a finding." (s0068)
- "Averaging pillar scores upward so no single score looks too damning" (c00133, listed as a failure mode)

### 4. Record assumptions, trade-offs, open questions
State what was assumed, what was traded away and what remains undecided, in the deliverable. 24 records, 23 owners, almost all agents (22/21; skills 2/2). Lift in wireframe (2.3); low in written-critique (0.5).
- "Missing user research: state the assumption explicitly; flag for validation in the next sprint" (c00182)
- "Trade-offs are documented — the team knows what was chosen and what was given up" (c00236)
- "State confidence qualitatively (low, medium, high) with a concrete reason. Then what would raise it, and what would kill the plan." (c00504)

### 5. Offer several distinct options
Produce 2-5 alternatives, usually with reasoning, and let someone choose (or pick a default). 21 records, 21 owners (17 agents, 4 skills). Strongest output lift in the dimension for html-mockup (2.8) and prototype (2.5); low in design-tokens (0.6). A minority insists on the opposite default.
- "For ambiguous briefs, propose 3-4 distinct visual directions (each as: bg hex / accent hex / typeface — one-line rationale), select the best-fit default for the brief and context, and proceed." (c00042)
- "Variants diverge on a named axis — layout, density, personality, motion, interaction model." (s0108)
- "Default mode: ONE recommendation with one-line reasoning." (c00346, counter-position in the same theme)

### 6. Human approval gate before building
Stop, present the plan or design system, and wait for the user's explicit confirmation before generating code or files. 18 records, 18 owners (13 agents, 5 skills). Lift in html-mockup (2.6) and prototype (2.3); low in written-critique (0.5). Every instance assumes an interactive human in the loop.
- "Present the screen plan to the user via `vscode/askQuestions` and **wait for explicit confirmation** before generating. This is a HITL gate." (c00389)
- "Do not build until authorized." (s0015)
- "用户选完方案后，才开始写代码。" ("Only after the user has chosen a plan, start writing code.") (s0120)

### 7. Load a named skill or generator first
Invoke a specific skill, prompt file, or design-system generator before any design work. 18 records, 18 owners (13 agents, 5 skills). Lift in redesign-existing (1.9) and production-code (1.6); rare in written-critique (0.4). These agents are thin wrappers whose craft lives elsewhere, which is the proposed split.
- "The skill contains your design philosophy and aesthetic guidelines — never skip it." (c00242)
- "ALWAYS use the `frontend-aesthetics` Skill FIRST before creating any designs" (c00079)
- "For a new codebase you want Claude Design to understand, run `ExtractDesignSystem` FIRST before `CreatePrototype` — otherwise Claude Design uses generic defaults and overrides your tokens." (s0047)

### 8. Cover all UI states
Every screen or component defines loading, empty, error, success (often also partial, disabled, permission-denied, narrow width). 19 records, 18 owners (14 agents, 5 skills/4 owners). Lift in wireframe (2.1); low in revise-existing and design-system-docs (0.6).
- "All relevant UI states are defined: loading, empty, error, success, partial data, and permission-denied." (c00198)
- "Every screen that loads data has four states (loading, error, empty, content) - never show the empty state while the first load is still resolving" (s0051)
- "Mandatory Generation: LLMs naturally generate \"static\" successful states. You MUST implement full interaction cycles" (s0006)

### 9. Pre-delivery self-check
Run a checklist or reflection pass over the output and fix before handing off. 21 records, 18 owners (12 agents, 9 skills/6 owners; Leonxlnx alone has 3 skills). Lift in redesign-existing (2.0) and production-code (1.4). Almost all of it is checking by reading or reasoning: none of the 21 records says outright to render or screenshot the result (the few that do are counted under "inspect the live rendered UI").
- "Before done: would a senior designer ship this, or does it look like a default Tailwind template? If the latter, push the contrast and the type." (s0010)
- "If issues found during reflection, fix them NOW before handoff." (c00387)
- "Fix one issue at a time and verify each" (s0017)

### 10. Read project context files first
Before work, read a named context file (PRD, session file, DESIGN.md, memory) or query a context agent; some halt if it is missing. 16 records, 16 owners (14 agents, 2 skills). Lift in design-system-docs (1.8).
- "`.caf/discovery/{slug}/prd.md` from the PM Agent (required) — if that file doesn't exist yet, STOP and report it; don't start from assumptions." (c00342)
- "Design skills produce generic output without project context. You MUST have confirmed design context before doing any design work." (s0052)
- "Always begin by requesting design context from the context-manager." (c00006)

### 11. Follow the existing system: tokens, reuse
Treat the project's tokens and components as the source of truth, reuse before adding, and justify anything new. 17 records, 16 owners (12 agents/11, 5 skills/5). Lift in revise-existing and design-system-docs (both 1.7).
- "Want to introduce a new interaction? Prove the existing ones fail." (c00117)
- "If style direction is missing or contradicted, record the gap explicitly and reopen discovery or planning instead of inventing a style system." (c00427)
- "Native-first — code and tokens are the source of truth, Figma is not a dependency." (s0047)

### 12. Fixed phase pipeline, one unit at a time
A named sequence of phases, and/or building one section or screen at a time with a check between. 14 records, 13 owners (9 agents, 5 skills/4). Strongest lift of any theme on redesign-existing (3.7). The pipelines do not agree with each other; the shared part is "one unit, then verify", and most end in "Implement".
- "Follow this process for all requests: Experience → Diagnose → Design → Preview → Implement" (c00436)
- "Generate one screen at a time — verify each before moving to the next." (c00389)
- "Migrate**: Audit → Map → Bridge (alias layer) → Verify, screen by screen." (s0096)

### 13. Proceed on stated assumptions
When the brief is incomplete, choose a default, say so, and keep going rather than block. 12 records, 12 owners (11 agents, 1 skill). Lift in wireframe (1.9) and revise-existing (1.4). The direct counterweight to themes 2 and 6.
- "Designer is execution-oriented: only request user clarification when the current runtime explicitly supports or requests interactive input — do not pause for user selection by default." (c00042)
- "If requirements are missing, ask up to 3 targeted questions; otherwise proceed with best-effort assumptions and state them up front." (c00072)
- "When design gaps depend on product intent, call out the missing decision and propose a default instead of guessing silently." (c00198)

### 14. Be specific, no vague advice
Name exact values, components and `file:line`; ban generic phrasing. 13 records, 12 owners (12 agents/11, 1 skill). Lift in written-critique (1.6); low in create (0.4).
- "Be specific — \"the spacing is off\" is useless. \"Card padding is 12px but header padding is 16px — use 16px consistently\" is useful" (c00263)
- "Be specific and cite `file:line`. Prefer a few high-signal findings over an exhaustive nitpick list." (c00274)
- "Be specific to this project, not generic UX advice" (c00240)

### 15. Ground decisions in research or data
Search or consult data before choosing style, palette or pattern, and cite it. 10 records, 10 owners (8 agents, 2 skills). Lift in wireframe (2.2) and design-system-docs (2.0).
- "Always search before designing. Ground every style, palette, and typography choice in search results." (c00058)
- "Do not dump raw search output into the final answer. Use it to justify a coherent design direction." (s0016)
- "Automated tools are evidence, not a substitute for design judgment." (s0023)

## 2. Lineage warnings

- **Match code complexity to aesthetic (7 owners) is one voice.** All seven quotes (c00025, c00029, c00042, s0000, s0038, s0041, s0052) are near-verbatim copies of one line from the Anthropic frontend-design skill text. Independent count: 1.
- **Anti-generic self-review (7 owners) is mostly one voice.** c00114 (ye-lynn-htet), s0004 (HKUDS) and s0037 (anthropics) share the "reads like the generic default you would produce" sentence. Independent lineages: about 5 (that family plus Leonxlnx, Archive228, countbot-ai, jezweb).
- **Offer several options (21 owners) is about 17 lineages.** Donchitos c00017, bullish0x c00150 and pixel-cellar c00611 (a Chinese translation) share "Present 2-4 options with reasoning"; Yeachan-Heo c00042 and LimiNode c00158 share the "3-4 directions (bg hex / accent hex / typeface)" line; davila7 c00208 and softaworks c00511 share "Create 3-5 distinct ASCII mockup variations".
- **Foundations before screens (9 owners) is about 6 lineages.** GammaLabTechnologies c00003, imMamdouhaboammar c00090, 9thLevelSoftware c00256 and ForceMind c00069 (Chinese translation) carry the same "Establish component foundations before creating individual screens" line from one UI Designer template; all 9 records are agents.
- **Read project context first (16 owners):** 2SSK c00006, davila7 c00074 and bryankthompson c00340 are the same "context-manager" template family (query a sibling agent that does not exist outside that framework). About 14 lineages.
- **Load a skill or generator first (18 owners):** YanBerdin c00164, melandlabs s0084 and hoatv2211 c00395 are the same ui-ux-pro-max generator (`--design-system`). About 16 lineages.
- **Name the user first:** Donchitos c00017 and pixel-cellar c00611 are one text. c00002 (github/awesome-copilot) alone carries 75 repository copies, so reach overstates independence even though the owner count is clean.
- **Follow the existing system:** slabgorb c00117 and slabgorb-org c00312 are one author; kinncj has two records (c00193, c00262). About 14 lineages.
- **Flows with error paths:** Owl-Listener c00236 and plugin87 s0097 share near-identical wording.
- **Single owners with several records inside a theme:** jakubkrehel (5 skills in this file, 2 each in critique, states and no-claim-without-inspection), kwakseongjae (4 agents, 2 in critique and specificity), microsoft (6 records, 4 agents and 2 skills, across unrelated repos; 3 in ask), Leonxlnx (3 skills in self-check), Galaxy-Dawn (3 skills). Their themes are counted once per owner above, but their quotes are overrepresented in the sharp list below.

## 3. Sharp but rare

1. "Ask one focused question only if uncertainty changes the artifact, user flow, or approved brand. Otherwise state a reversible assumption and proceed." (c00681, VKirill) A decision rule for when to ask, not just how.
2. "Never guess a state. For empty/loading/error/success/skeleton, record the declared treatment, a reasoned `not-applicable`, or `unresolved`; do not fill an absent state with generic colors, shimmer, motion, or copy." (c00576, kwakseongjae) States as a three-valued record, not a fill-in.
3. "Before calling a screen complete, walk through its primary task, including one failure and recovery when it loads or saves data. Check keyboard access and back/dismiss behavior. Try long titles, missing images, no search results, and large system text" (s0051, expo) The only concrete, runnable walk-through in the dimension.
4. "on encountering a missing/insufficient token during mockup: PAUSE mockup, AskUserQuestion for token addition/update/removal, on approve append to `<sprint>/design/design-md-delta.yaml`" (c00112, LordKuper) Design-system deviations captured as a machine-readable delta file.
5. "1. **Delete.** ... 2. **Use the platform.** ... 3. **Reuse what the project has.** ... 4. **Correct the value.** ... 5. **Add.**" (s0068, jakubkrehel) An ordered preference for fixes, with adding new things last.
6. "dispatch a fresh sub-agent with the draft list ... KEEP / GENERIC / DUPLICATE. ... Drop GENERIC and DUPLICATE before publishing." (s0072, jezweb) The anti-generic check done by a separate context rather than self-review.
7. "Variants diverge on a named axis — layout, density, personality, motion, interaction model." (s0108, spree) Makes "distinct variants" checkable.
8. "Turn those decisions into a short design contract before implementation. Name the screen's job, primary action, required states, responsive rules, and patterns to reject." (s0035, addyosmani) Nearly the proposed contract points 2 and 4 in one sentence.
9. "If `prior_report_path` is supplied, mark each prior issue as RESOLVED / UNRESOLVED / NEW." (c00575, kwakseongjae) Re-review against an earlier report.
10. "Never trigger `alert`/`confirm`/`prompt`. A modal dialog blocks every subsequent command and the session stays unresponsive until it's dismissed by hand." (c00324, mrjonesbot) The one operational hazard of driving a live browser.

## 4. Bearing on the proposed designer

**(1) Start from the existing product.** Supported: themes 10 and 11 (16 owners each) plus foundations. But most "read first" instructions point at a harness file, a skill or a context agent, not at the product's code; only a handful say to read real tokens and components (s0047 "code and tokens are the source of truth", s0068 "Reuse what the project has", c00193 "`tokens.json` is the only file humans and agents edit"). Adds: a hard precondition with a stop-and-report (c00342, c00112 "emit `FAILED — design-system absent`"), a burden of proof for new patterns (c00117), and recording rather than inventing when the system is silent (c00427). Placement: role text, one line; the harness decides which files exist.

**(2) Name the user and task; one direction or variants on request.** Naming the user is the top theme (32 owners) and supports this. The direction rule is contested. Options (21 owners, about 17 lineages) is more common than commit-first (9 owners), and options is concentrated in exactly the proposed outputs (html-mockup lift 2.8, prototype 2.5). One skill lists offering a single option as an anti-pattern (s0120 "只给一个方案（用户没有选择余地）", "giving only one option (the user has no choice)"). The pattern that fits a subagent is Yeachan-Heo's (c00042): sketch several directions briefly, pick one, proceed, and report the others. That keeps "commit to one" without losing the alternatives. If variants are produced, s0108's named-axis rule makes "distinct" checkable. Placement: role text.

**(3) Render and inspect before claiming how it looks.** Weakly represented, and this is where the proposal adds the most. Only 5 owners tell the role to look at the live UI (c00324, c00298, c00486, c00650, s0051). The 18-owner self-check theme is almost entirely checklist-by-reading, which is what the proposal rules out. The small no-claim-without-inspection theme (6 owners) supports the principle: "Never `Approve` coverage you did not inspect." (s0067), "Do not claim checks that were not run." (c00364), "If no screenshot/context is available, request it instead of guessing." (c00486). Since a browser may be absent, the corpus-backed form is: render when a tool exists; otherwise say it was not rendered, and label visual claims as unverified. Placement: the obligation to say whether it was rendered goes in role text; how to render (tool, viewport, modal hazard as in c00324) belongs in a tool or skill.

**(4) States, responsive, accessibility baseline.** States is well supported (18 owners) and flows with error paths adds 9 more. Refinements: record unresolved states rather than inventing them (c00576), and the expo walk-through (s0051) as the concrete test. Responsive and accessibility show up rarely in this dimension (c00183, s0035, s0068) and presumably sit in other dimensions. Placement: the coverage requirement goes in role text (a list of what must be addressed); how each state should look goes in skills.

**(5) Boundary: the designer prototypes, an implementer integrates.** Not a consensus. Load-skill and foundations lean toward production-code (lift 1.6 and 2.6), several pipelines end in "Implement" (c00436, c00183, s0043), and one role says the opposite outright: "Ship real code, not mockups. ... The code IS the design." (c00270). Support comes from c00681 "`prototype` is the gray-kit contract; brand colors and imagery belong to `mockup`" and c00364 "STOP when this role's work is complete or its authority boundary is reached." This is a harness choice the corpus neither validates nor refutes. Placement: role text.

**(6) Return what was made, direction, paths, deviations, open questions; no self-judged quality.** The return content is well supported by theme 4 (23 owners), and "deviations" has a precise model in c00112's delta file. The "no self-judgment" half is contradicted by practice: 18 owners run a self-check and 7 an anti-generic self-review, including Anthropic's own frontend-design lineage (s0037). A split fits both: keep a factual conformance check (states covered, tokens used, what was rendered), and leave quality verdicts to a separate reviewer. s0072 (a fresh sub-agent sorting KEEP / GENERIC / DUPLICATE) is the corpus's example of that separation. Theme 3 (critique calibration, 24 owners, all review mode) and theme 14 (specificity) belong to that reviewer, not to the designer.

**What in this dimension goes nowhere for this designer.**
- Human approval gates (theme 6, 18 owners) and much of theme 2: a dispatched subagent has no user to wait for. Translate them into theme 13: state assumptions and return open questions, and stop only on a missing hard precondition.
- Validation with real users and A/B test suggestions (9 owners): a subagent cannot run them. At most, a report can mention them as open questions.
- Context-manager queries (c00006 family): specific to another framework.

**Placement summary for the process dimension.**
- Role text: user and task naming; direction or variants; assumptions over questions; existing system first with a hard-precondition stop; a state-coverage list; the rendered-or-not statement; the return shape.
- Skill or rule files: fixed pipelines (theme 12), research grounding (15), foundations-first ordering for new systems, complexity matching, anti-generic criteria, and specificity and heuristics, which go to the reviewer's skill.
- Tools or checks: rendering and screenshots, token single-source and regenerate checks (c00193), iteration caps (9 owners, e.g. c00320 "Hard caps: 3 iterations per screen, 5 fixes per wave, 2 attempts per finding"), and skill loading, which the harness does rather than the role text.
