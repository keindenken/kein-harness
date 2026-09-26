# Themes: components-system

Source: `claims/components-system.jsonl`, all 314 lines read. The dimension covers 213 distinct records from 186 distinct owners: 163 agent records (147 owners) and 50 skill records (41 owners). Theme assignments are by claim line and are saved in `components-system.assign.json`. All counts below were computed from that file joined to the claims, not estimated. A record counts once per theme however many of its quotes land there. One quote can sit in more than one theme; the two states themes share 22 records.

"Owners" is the repo prefix before "/". "Fam-adj" merges owners confirmed to be one voice or one template family (see section 2): slabgorb and slabgorb-org, ye-lynn-htet and HKUDS, YanBerdin and melandlabs, tjsasakifln and gaahzx. Output and mode concentration are given as lift, meaning the share of the theme's records carrying that tag divided by the share across all 213 records in this dimension. Only tags on 2 or more of the theme's records are counted.

## 1. Top recurring themes (ordered by distinct owners)

### T1. Design the data and screen states (loading, empty, error, success, partial), not just the happy path
- Counts: 47 records, 44 owners (fam-adj 44). Agents 38 records / 36 owners, skills 9 / 8.
- Concentration: wireframe (lift 1.44), spec-or-handoff (1.10). Mode-neutral (create 1.01, review 1.08).
- Quotes:
  - "Render critical states, not just the happy path: loading, populated, empty, error, disabled, selected, hover/focus, validation, and mobile behavior when relevant." (s0024)
  - "Include states (empty, loading, error) when mockup has them" (c00112)
  - "Score based on: loading states present, error boundaries exist, empty states handled, disabled states for actions, confirmation for destructive actions" (c00133)

### T2. No hardcoded values: every colour, spacing and type value references a design token
- Counts: 37 records, 36 owners (fam-adj 34). Agents 33 / 33, skills 4 / 3.
- Concentration: written-critique (1.47), design-tokens (1.38), design-system-docs (1.21). Leans review (1.18) and revise-existing (1.12) over create (0.82). This is mostly phrased as something to check for.
- Quotes:
  - "Tokens first, components second. No raw values inline." (c00024)
  - "Fixes use the project's token variables and components — never introduce a new framework, library, or styling approach, and never hardcode a value the token system expresses" (c00320)
  - "Are all colors, spacing, fonts from tokens.css? Flag any hardcoded values (hex codes, pixel values, font names not from tokens)." (c00403)

### T3. Specify interactive states for every component (default, hover, focus, active, disabled)
- Counts: 34 records, 33 owners (fam-adj 33). Agents 30 / 29, skills 4 / 4.
- Concentration: wireframe (1.68), prototype (1.45). Leans create (1.15).
- Quotes:
  - "Specify default, hover, focus, active, disabled, loading, empty, error, success, and selected states when applicable." (c00449)
  - "Make every interactive state explicit - hover, active, focus-visible, disabled. A control with no states feels dead." (s0098)
  - "Verify: hover, active, and disabled states exist and differ; destructive actions are guarded; loading/empty/error states are handled, not blank." (c00441)

### T4. Reuse existing components and patterns before creating new ones; no one-off or duplicate components
- Counts: 33 records, 32 owners (fam-adj 32). Agents 30 / 30, skills 3 / 2.
- Concentration: wireframe (1.42), spec-or-handoff (1.08). Mode-neutral.
- Quotes:
  - "Don't create one-off components when a design system pattern already exists." (c00170)
  - "If components exist that match or partially match what you need to build, extend or compose them. Do not create duplicates." (s0074)
  - "Reuse existing primitives in `src/frontend/components/ui/` (`button.tsx`, `card.tsx`, `input.tsx`) rather than introducing one-off styled elements that drift from the established look." (c00424)

### T5. Align with the project's existing design system and conventions unless the brief asks for a redesign
- Counts: 26 records, 25 owners (fam-adj 25). Agents 21 / 20, skills 5 / 5.
- Concentration: redesign-existing (1.32), written-critique (1.20). Leans revise-existing (1.37) and review (1.12).
- Quotes:
  - "Stay within the project's existing design system and CSS framework unless explicitly asked to redesign." (c00311)
  - "Respects existing design tokens and component patterns — does NOT overwrite them unless the user requests a full redesign." (s0047)
  - "Preserve the existing design system when it is coherent; elevate weak areas instead of rewriting everything." (c00348)

### T6. Follow a named platform or house design language (Apple HIG, Material, Fluent, Primer, Aksel, Weave)
- Counts: 17 records, 17 owners. Agents 15 / 15, skills 2 / 2.
- Concentration: prototype (1.45, n=3), design-system-docs (1.32), spec-or-handoff (1.26). Mostly mobile and native surfaces.
- Quotes:
  - "iOS: Respect Apple's design language while maintaining brand" (c00059)
  - "Where the project follows a third-party design language (Material Design 3, Apple Human Interface Guidelines, Fluent 2), map its tokens to the corresponding Qt Quick Controls style rather than introducing a parallel token vocabulary." (s0083)
  - "Bruk Aksel-komponenter og -mønstre" ("Use Aksel components and patterns") (c00298)

### T7. Build tokens in tiers (primitive, then semantic, then component) and name them by role, not by value
- Counts: 16 records, 14 owners (fam-adj 14). Agents 13 / 11, skills 3 / 3.
- Concentration: design-tokens (2.13), design-system-docs (1.82). Strongly create (1.22) and weak in review (0.57).
- Quotes:
  - "Primitives name a value (`--blue-500`) and are never applied in a component. Semantic tokens name a job (`--color-text-secondary`), point at a primitive and are the only tier components reference." (s0067)
  - "**Semantic naming** — name by role (`color-surface`, `color-text-muted`, `space-4`), not by value (`gray-200`, `blue`)." (c00290)
  - "Small project (<10 components) | Primitive + Semantic | Full three-layer hierarchy adds unnecessary indirection" (c00232)

### T8. Work inside the project's chosen component library and styling approach; do not introduce a parallel one
- Counts: 15 records, 14 owners (fam-adj 14). Agents 8 / 7, skills 7 / 7. Skills are over-represented here (7 of 14 owners, against 41 of 186 across the dimension).
- Concentration: redesign-existing (2.29), production-code (2.06). Leans revise-existing (1.58).
- Quotes:
  - "Before suggesting or writing a fix, identify the project's existing styling system and express the change in that system: Tailwind in a Tailwind project, plain CSS in a CSS project, or the established CSS-in-JS approach." (s0066)
  - "If a component library is already in TECH_STACK.md, work within it. Never propose a token/component system that conflicts with an already-chosen library (shadcn/MUI/Ant) — extend its primitives, don't shadow them." (c00321)
  - "shadcn primitives are untouchable — wrap them for custom behavior" (c00310)

### T9. Create, document and steward the design system itself (token pipelines, component libraries, docs, design/code parity)
- Counts: 14 records, 13 owners. Agents 12 / 11, skills 2 / 2.
- Concentration: html-mockup (3.04, n=3), prototype (2.34), wireframe (2.23), design-system-docs (1.76). Leans review (1.43) and revise-existing (1.41).
- Quotes:
  - "Design token creation and management (Figma Variables, Style Dictionary)" (c00008)
  - "require token usage, state inventory, accessibility annotations, and a usage example for every new component." (c00601)
  - "Design system stewardship: contribute patterns back to the design system; avoid one-off solutions" (c00182)

### T10. A single source-of-truth design file (DESIGN.md, master file with page overrides) that all work cites
- Counts: 12 records, 11 owners (fam-adj 10). Agents 9 / 8, skills 3 / 3.
- Concentration: prototype (2.05, n=3), design-tokens (1.42). Leans revise-existing (1.48).
- Quotes:
  - "ui mockups use only tokens already in DESIGN.md OR tokens already approved + appended to current sprint's `design-md-delta.yaml`" (c00112)
  - "When building a specific page (e.g., "Checkout"), first check `design-system/pages/checkout.md`... If the page file exists, its rules override the Master file" (s0084)
  - "Design-system-first is the token fix. The biggest token sink is re-inferring your brand on every pass and then correcting it." (s0047)

### T11. Consistent vocabulary and meaning across screens and flows (action names, colour meanings, labels, hierarchy)
- Counts: 11 records, 11 owners (fam-adj 10). Agents 4 / 4, skills 7 / 7. Mostly skills.
- Concentration: html-mockup (2.58, n=2), redesign-existing (1.87). Leans review (1.49).
- Quotes:
  - "An action keeps the same name through the whole flow, so the button that says "Publish" produces a toast that says "Published."" (s0004; the same line is in c00114)
  - "Do not make users relearn the UI for each operation. The screen may differ, but the vocabulary, section order, summary panel, validation, state labels, and primary/secondary action hierarchy should stay consistent." (s0014)
  - "Systematic application: Same color meanings throughout (green always = success)" (s0053)

### T12. Gate new tokens and components: add one only when the existing system cannot express it, and flag the deviation
- Counts: 11 records, 11 owners. Agents 10 / 10, skills 1 / 1.
- Concentration: written-critique (1.42), spec-or-handoff (1.14). Mode-neutral.
- Quotes:
  - "identify where new tokens/components are truly required vs avoidable" (c00013)
  - "Changes align with the existing design system, or deviations are flagged and justified." (c00198)
  - "Avoid inventing new themes/tokens if existing theme primitives can be used." (c00181)

### T13. Empty and error states give direction: a next action or a fix, not just "nothing here"
- Counts: 10 records, 10 owners. Agents 4 / 4, skills 6 / 6. Mostly skills.
- Concentration: written-critique (1.82). Strongly review (1.46); create (0.61) and revise-existing (0.59) are low.
- Quotes:
  - "Empty states: always actionable — never just "No data found"; include a CTA" (c00182)
  - "MUST give empty states one clear next action" (s0063)
  - "Error messages state what happened, why, and what to do next. No raw error codes." (s0087)

### T14. One icon system, used consistently (a single library, stroke weight, sizes; no emoji as icons)
- Counts: 9 records, 7 owners. Agents 4 / 3, skills 5 / 4.
- Concentration: prototype (3.64, n=4), html-mockup (3.16, n=2), production-code (1.56). All create.
- Quotes:
  - "Evaluate and recommend one primary icon system for the product (e.g. Lucide, Phosphor, Heroicons, Material Symbols, Tabler) so stroke weight, corner language, and metaphors stay consistent." (c00053)
  - "Never use emoji as icons - always use professional icon libraries (FontAwesome, Heroicons, etc.)" (s0031)
  - "Icons: `lucide-react` only; import individually; default size `16px`." (c00603)
- Taste conflict: s0089 lists "Generic Lucide thin-stroke icons (use Phosphor Bold or Radix)." as a thing to avoid, and c00603/s0095 mandate Lucide.

### T15. Atomic design hierarchy (atoms, molecules, organisms, templates, pages)
- Counts: 7 records, 7 owners. Agents 7 / 7, skills 0.
- Concentration: wireframe (2.97), design-system-docs (1.92), spec-or-handoff (1.79).
- Quotes:
  - "ATOMIC DESIGN: Atoms → Molecules → Organisms → Templates → Pages" (c00010)
  - "Atoms: Basic UI elements (buttons, inputs, icons)" (c00215)
- Every instance is a taxonomy recitation. None says how the hierarchy changes a decision.

Below the cut (also in the assign file): theming, dark mode and multi-brand handled through tokens (7 records / 7 owners); component API shape, such as variant enums with defaults, flat props and composition over configuration (6 / 6); skeleton loaders matching the layout instead of spinners (5 / 5, 3 of them skills).

## 2. Lineage warnings

- **slabgorb / slabgorb-org** (c00117, c00312) carry the identical line "Choosing colors/spacing/type? Use the design system. No exceptions." and share 8 long lines. They are one author and count as one voice in T2.
- **AIOS-style design-system family** (c00010, 28 repo copies; c00021, 16 copies): both open with "ZERO HARDCODED VALUES", c00010 as "All styling from design tokens" and c00021 as "All styling from tokens". The files share no long lines, but the slogan comes from one framework. T2 drops from 36 owners to 34 when both families are merged. Copy counts do not inflate these theme counts, because each cluster is one record. They do show that this phrasing reached 44 repositories through two templates.
- **frontend-design family** (c00114 and s0004, 17 shared long lines): both carry the "Publish"/"Published." line. T11 falls from 11 to 10 independent voices.
- **ui-ux-pro-max family** (c00164 and s0084, 142 shared long lines): both carry "If the page file exists, its rules override the Master file". T10 falls from 11 to 10.
- **Single-project clusters**: verifywise-ai contributes 5 records (c00600 to c00605), 2 of them in T3, T9 and T14 each. kinncj (c00193 and c00262, 18 shared lines, both "{category}.{group}.{role}") and josstei (c00232, c00591) each put two records into T7, so T7 has 16 records but 14 owners. jakubkrehel has three skills, and s0066 and s0070 repeat the same icon-stroke line, so T14 has 9 records but 7 owners. Orkas-AI (3 skills) and lobehub (2 skills) are each one voice.
- **Theme overlap, not lineage**: T1 and T3 share 22 records, because most state lists mix interactive states and data states in one line. Taken together, the states material is 59 records from 55 owners, not 81.
- **Enumeration-only content**: T15 and much of T9 come from long-lived catalogue templates (wshobson c00008 with 35 copies, ccplugins c00007 with 39 copies, amurata, Smith-Happens's "EXPERT TIER TEMPLATE"). They list topics such as "Design token creation and management (Figma Variables, Style Dictionary)" without an operating rule. The owners are independent, but the catalogue style is one inherited genre.

## 3. Sharp but rare (1 owner each)

1. "Every repeated visual value is a token. A literal that appears twice belongs in the theme." (s0050, expo). This is a mechanical threshold for when to tokenize.
2. "When a component's props start describing *content* (`leftIcon`, `subtitle`, `footerText`, `badgeCount`), stop adding props and accept `children` instead." (s0050, expo)
3. "Do not invent values when the repository provides a token or component contract. Introduce a primitive only after proving why the existing system cannot express the decision and which consumers should share it." (s0064, ibelick). It states the burden of proof for a new primitive.
4. "First try an existing ramp step. Optical corrections supported by measurement may remain local; do not tokenize every pixel." (c00657, wlsdks). It pushes against rule 1 and against T2 absolutism.
5. "Never introduce a token not in the valid bound graph or standalone Core projection. If you need one, halt and tell master: "Need new token: <path>. Graph-first Phase 5 must extend it."" (c00576, kwakseongjae). It gives an escalation message to use instead of improvising.
6. "Every theme (light, dark, high-contrast, brand variants) must implement this full shape. Missing values are a build error, not a runtime fallback." (c00232, josstei)
7. "Treat shadcn/Radix/Headless UI/React Spectrum/Ant/MUI-style components as behavioral references only unless the local repo already uses them." (s0024, Orkas-AI)
8. "Match exact values (if hardcoded #007AFF and theme has colors.primary: '#007AFF', that's the match)" (c00664, senaiverse). This is a concrete algorithm for mapping literals to tokens that a checker could implement.
9. "**Consistency across files is non-negotiable.** The same component (e.g. checkbox) must use byte-identical CSS + markup in every harness/page." (s0095, plugin87). It is aimed directly at multi-file HTML mockups.
10. "Persona consistency** | The same fake user name/avatar is used across all screens (no mix of different personas)" (c00389, g-nogueira). It is a mockup-specific consistency check that no one else states.

## 4. Bearing on the proposed designer

**(1) Start from the existing product and follow its design system unless the brief asks for a new direction.** This dimension supports it more strongly than any other point. T4, T5, T8 and T12 together cover 71 records from 67 owners (14 of them skills), about 36% of the dimension's owners. The proposed "unless the brief asks for a new direction" exception appears almost word for word in the corpus (c00311 "unless explicitly asked to redesign", s0047 "unless the user requests a full redesign", c00427 "unless a change is explicitly required"). The corpus adds three things the contract leaves implicit: (a) find out which styling mechanism the project uses (Tailwind, plain CSS, CSS-in-JS, the chosen component library) and work in it, not only which tokens exist (T8, s0066, s0109, c00267); (b) outside libraries count only as behavioural references when the repo does not already use them (s0024); (c) a new token or component needs a stated reason and is flagged (T12, s0064, c00576). Item (c) is the part worth having in role text. The rest is the ordinary meaning of "follow its design system".

**(2) Name the user and task; commit to one direction or produce variants.** This dimension has nothing on it. The closest line is c00321 "Every component in the inventory earns its place from a real screen", which ties components to the task rather than to the user.

**(3) Render and look before reporting.** This dimension has almost nothing on it. The only render-flavoured line is s0024 ("Render critical states, not just the happy path"), which is about states rather than visual inspection. Conformance checks here (T2, and c00371 "verify the result matches the existing design system (variable names, spacing scale, breakpoints)") are code-level and can be done without a browser. That fits the no-screenshot-tool case: token and component conformance can be checked by reading the code, and appearance cannot.

**(4) States, responsive behaviour, accessibility baseline.** The states part is well supported. States material is 59 records from 55 owners, the most-owned theme family in the dimension. The corpus adds that the state list varies: partial, no-permission, success, selected and validation appear beyond empty, loading and error (c00191, c00266, c00449, s0024). c00112 adds a mockup-specific scoping, "Include states (empty, loading, error) when mockup has them". Better than a fixed list, the role could require the output to say which states were covered and which were left out. T13 (empty and error states give direction) and the below-the-cut skeleton rule concern how states should look, not whether they exist. They are craft and belong in a skill, and T13 comes mostly from skills anyway.

**(5) Boundary: the designer prototypes and production integration goes to an implementer.** This point is neither supported nor contradicted directly, but it has one real implication. T8 concentrates in production-code (lift 2.06) and redesign-existing (2.29), and T2 quotes such as c00320 ("Fixes use the project's token variables and components") come from designers who edit production code. If the designer's prototypes are built from the project's real tokens and components (T4, T8), the handoff to the implementer is integration, not a rewrite. The boundary line should say prototypes use the project's system. That is a reason to keep point (1) binding even for throwaway mockups. c00112 and s0095 apply token and markup discipline to mockups explicitly.

**(6) Report what was made, the direction, screenshots or paths, deviations, open questions; no self-judgement of quality.** The "deviations from the design system" item is supported by c00198 ("deviations are flagged and justified"), c00176 (an output slot "Existing Design Tokens: [...] Recommendations: [how new design maps to existing patterns]") and c00576 (halt and name the needed token). The corpus is split on self-review. Many T2 and T3 lines are self-check items ("Are all colors, spacing, fonts from tokens.css?", c00403; "Verify: hover, active, and disabled states exist and differ", c00441). These are checks of conformance and completeness, not judgements of quality, so they do not conflict with "review is separate". The designer can report facts (the new tokens it introduced, the states it covered) without grading its own taste.

**Where this dimension's content belongs**
- **Role text (a few lines):** start from the project's existing tokens, components and styling mechanism; reuse before creating; introduce a new token or component only when the existing system cannot express the need, and list each one as a deviation in the report; state which UI states the output covers. These are working-contract rules that apply to every output form.
- **Skill or project rule file:** token tier architecture and naming (T7), theming (below the cut), component API shape, platform design languages (T6), icon choice and stroke rules (T14), empty and error-state copy (T13), skeleton-versus-spinner, cross-screen vocabulary (T11), and the tokenization threshold debate (sharp items 1 and 4, which conflict and need a project decision). All of these are taste or project-specific, and the corpus disagrees internally (Lucide mandated versus avoided).
- **Tool or check:** hardcoded-value detection. T2 is the second-largest theme and the most mechanical, and sharp items 8 and 1 already describe the algorithm (exact-value matching and repeated-literal detection). A lint-style check is more reliable than prose, and it runs without a browser. A state-inventory presence check could also run on component files. The DESIGN.md source-of-truth pattern (T10) belongs to the project's own files, and the role only needs "read the project's design rules file if one exists".
- **Nowhere:** atomic-design recitations (T15) and catalogue lines like "Design token creation and management (Figma Variables, Style Dictionary)". They carry no decision and come from inherited enumeration templates.
