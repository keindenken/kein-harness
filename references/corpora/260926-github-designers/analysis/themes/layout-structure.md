# Layout and structure: recurring instruction themes

Source: `claims/layout-structure.jsonl`, 274 quotes from 189 records (139 agents, 50 skills) held by 161 distinct owners. Every line was read and assigned by hand; 36 lines fit no theme (one-off tool, platform or aesthetic specifics). The assignment is in `layout-structure.assign.json` (a record counts once per theme if any of its quotes fits; a record can sit in several themes). Counts below are computed from that file against the claims file.

Baseline for reading "concentrates in": across all 189 records, outputs are spec-or-handoff 52%, production-code 44%, design-tokens 42%, design-system-docs 39%, written-critique 39%, wireframe 20%, prototype 11%, html-mockup 7%; modes are create 85%, review 55%, revise-existing 46%. Skills are 26% of records.

## 1. Top recurring themes (ordered by distinct owners)

| # | Theme | Records | Owners | Agents (owners) | Skills (owners) | Lineage-adjusted owners |
|---|---|---|---|---|---|---|
| 1 | Mobile-first ordering | 35 | 35 | 32 (32) | 3 (3) | ~33 |
| 2 | Spacing on a 4/8 scale | 35 | 34 | 30 (29) | 5 (5) | ~33 |
| 3 | Touch targets at least 44px / 48dp | 29 | 29 | 22 (22) | 7 (7) | ~28 |
| 4 | Named breakpoint values | 21 | 21 | 19 (19) | 2 (2) | ~18 |
| 5 | Anti-template layout (no hero + three equal cards) | 18 | 18 | 11 (11) | 7 (7) | ~13 |
| 6 | Non-happy states designed (empty, loading, error) | 18 | 17 | 13 (13) | 5 (4) | 17 |
| 7 | Responsive coverage in general, mobile and desktop both intentional | 16 | 14 | 13 (11) | 3 (3) | ~13 |
| 8 | Check the layout at specific widths | 13 | 13 | 10 (10) | 3 (3) | ~12 |
| 9 | Specify structure: IA, navigation, screen inventory | 13 | 12 | 12 (11) | 1 (1) | 12 |
| 10 | Progressive disclosure and cognitive-load limits | 10 | 10 | 7 (7) | 3 (3) | 10 |
| 11 | One focal point / one primary action per screen | 9 | 9 | 6 (6) | 3 (3) | 9 |
| 12 | Column grid system | 8 | 8 | 6 (6) | 2 (2) | 8 |
| 13 | Thumb reach and bottom placement on mobile | 7 | 7 | 4 (4) | 3 (3) | 7 |
| 14 | Surface purpose decides composition | 6 | 6 | 5 (5) | 1 (1) | 6 |
| 15 | Generous whitespace | 5 | 5 | 2 (2) | 3 (3) | 5 |

### 1. Mobile-first ordering
Design or write the smallest viewport first and add complexity upward.
- 35 records, 35 owners; 32 agents, 3 skills.
- Concentrates in spec-or-handoff (26/35, 74%) and design-system-docs (25/35, 71%); create mode 33/35. Mostly stated as a principle in a bullet list, rarely with a check attached.
- "Ignoring mobile-first responsive design — start with the most constrained viewport and add complexity for larger screens" (c00233)
- "Mobile-first — write base styles for mobile, layer up with `md:` and `lg:`" (c00377)
- "Build mobile layout first, then scale up. This is non-negotiable." (s0074)

### 2. Spacing on a 4/8 scale
All spacing comes from a fixed scale on a 4px or 8px base; no arbitrary values.
- 35 records, 34 owners; 30 agents (29 owners), 5 skills. ccplugins has 2 records.
- Concentrates in design-tokens (23/35, 66%) and design-system-docs (21/35, 60%). Often a literal token block pasted into the prompt (c00038, c00059, c00108, c00425, s0044).
- "All spacing MUST use this scale. No arbitrary values like `px-[13px]`. The 8px grid ensures visual alignment across all screen sizes." (c00407)
- "Spacing: compact 4/8 scale for tools; 8pt editorial rhythm for content/marketing." (c00517)
- "Use 4pt or 8pt grid system" (c00079)

### 3. Touch targets at least 44px / 48dp
Interactive elements get a minimum hit area, 44px (Apple) or 48dp (Android).
- 29 records, 29 owners; 22 agents, 7 skills.
- Spread evenly; somewhat review-leaning (review mode 20/29, 69% vs 55% baseline; written-critique 12/29). The most convergent numeric rule in the dimension, and it converges on an external standard rather than on a shared prompt.
- "Touch targets minimum 44x44px." (c00024)
- "Interactive elements should prefer a 44×44px hit area for touch or mobile contexts. In dense desktop interfaces, use at least 40×40px." (s0066)
- "모바일 퍼스트 — 터치 타깃 최소 44pt(iOS)/48dp(Android), 한 손 조작 영역(thumb zone)을 고려한다" (c00266)

### 4. Named breakpoint values
The prompt fixes a breakpoint set in pixels.
- 21 records, 21 owners; 19 agents, 2 skills.
- Concentrates in design-system-docs (15/21, 71%), production-code (14/21, 67%) and design-tokens (14/21, 67%). The values do not agree: small-phone floor is 320, 375 or 390; the upper set is mostly Tailwind defaults (640/768/1024/1280/1536) or 768/1024/1440; one uses Android window size classes, one a Godot export var.
- "**Breakpoints**: 375px (mobile), 768px (tablet), 1024px (desktop), 1440px (large)" (c00118)
- "Mobile: 320px - 639px (base design)" (c00003)
- "Designs must adapt to **Compact** (phones, <600dp), **Medium** (foldables/small tablets, 600-840dp), and **Expanded** (tablets landscape, >840dp) window size classes." (c00628)

### 5. Anti-template layout
Ban the stock AI landing layout (centered hero, three equal cards, uniform sections) and vary composition instead.
- 18 records, 18 owners; 11 agents, 7 skills. Skills are 39% here against a 26% baseline.
- Concentrates in production-code (14/18, 78%) and html-mockup (4/18, 22% vs 7%); create mode 17/18. This is the design-engineer and taste-skill voice, not the spec-writer voice.
- "**NO 3-Column Card Layouts:** The generic \"3 equal cards horizontally\" feature row is BANNED. Use a 2-column Zig-Zag, asymmetric grid, or horizontal scrolling approach instead." (s0006)
- "A dashboard is a Monitor surface, not a Decide surface — do not give it a centered hero and three feature cards." (c00337)
- "many generic designs use numbered markers (01 / 02 / 03), but that's only appropriate if the content actually is a sequence" (c00114)

### 6. Non-happy states designed
Empty, loading, error (and sometimes permission-denied, success) states are designed, not left to the implementer.
- 18 records, 17 owners; 13 agents, 5 skills (4 owners; lobehub has 2).
- Concentrates in spec-or-handoff (14/18, 78%) and written-critique (10/18, 56%); review mode 13/18 (72%). States appear as a checklist item a reviewer ticks more than as a build step.
- "Loading, error, and empty states must be represented — the architecture requires every page to handle all three" (c00389)
- "빈 검색 결과 / 0 데이터 / 네트워크 실패 / 권한 없음 — 4 상태 모두 처리?" (c00577)
- "Show at least one non-happy-path state (empty / loading / error / in-progress), ideally behind a state-toggle strip like the template's." (s0076)

### 7. Responsive coverage in general
Every layout must work across sizes, and each size should be composed, not merely scaled.
- 16 records, 14 owners; 13 agents (11 owners), 3 skills. semaj90 and Toskysun have 2 records each.
- Concentrates in spec-or-handoff (9/16); create mode 14/16. Mostly generic ("Design responsive grid layouts for all device sizes"); the sharper ones say what must be decided per component.
- "Ensure desktop and mobile compositions are intentional, not merely scaled." (c00449)
- "Responsive behavior: navigation, filters, tables, side panels, fixed boards, and action bars need a defined mobile behavior." (s0023)
- "DO: Use container queries (@container) for component-level responsiveness" (s0002)

### 8. Check the layout at specific widths
Test or look at the result at named widths before accepting it.
- 13 records, 13 owners; 10 agents, 3 skills.
- Concentrates in review mode (10/13, 77%) and written-critique (8/13, 62%). Nearly all say "test" without saying how; only c00532 and c00254 describe an act of looking or resizing.
- "Look at the 320px render before you accept the 1280px one." (c00532)
- "Với app desktop: thử thu nhỏ cửa sổ về 800×600, 1024×768, và maximize." (c00254)
- "Test at 375px, 768px, and 1280px — responsive is non-negotiable" (c00334)

### 9. Specify structure: IA, navigation, screen inventory
Before visuals, lay out what screens exist, what each contains, how users move between them, and propose layout options.
- 13 records, 12 owners; 12 agents (11 owners; microsoft has 2), 1 skill.
- Concentrates in spec-or-handoff (12/13, 92%) and wireframe (7/13, 54% vs 20%). This is the UX-architect sub-genre; it rarely co-occurs with the anti-template theme.
- "Specify screen states, navigation, and data presentation patterns" (c00131)
- "The IA could go flat (everything on one screen) or layered (dashboard → detail). Flat is faster for power users but overwhelming for new ones." (c00236)
- "设计布局方案（含 2-3 个变体）和模块拆分方案" (c00241)

### 10. Progressive disclosure and cognitive-load limits
Hide what is not needed now; cap nav items, chunk sizes and disclosure depth.
- 10 records, 10 owners; 7 agents, 3 skills.
- Concentrates in spec-or-handoff (8/10) and written-critique (7/10); review mode 8/10.
- "Rule: if a decision is not required now, do not put it in the main path." (s0014)
- "Most interfaces work best with max two disclosure levels. Three or more causes disorientation." (s0087)
- "Progressive Disclosure: Don't show all 20 tools at once" (c00002)

### 11. One focal point / one primary action per screen
Hierarchy is set by size, weight and space so that one element leads; primary and secondary actions are distinct.
- 9 records, 9 owners; 6 agents, 3 skills.
- Concentrates in written-critique (6/9).
- "one clear focal point per screen. Size, weight, and space do the work, not borders everywhere." (s0010)
- "Each surface should declare exactly ONE primary action (most prominent button, brightest accent). Multiple peer-level primaries → `HIERARCHY_TIE`." (c00638; line breaks in source collapsed)
- "Content-First: Most important content gets most space (70/30). Don't let chrome overwhelm data." (c00085)

### 12. Column grid system
Name a column grid with gutters (12 columns, sometimes 8/4 by breakpoint).
- 8 records, 8 owners; 6 agents, 2 skills.
- Concentrates in design-system-docs (6/8) and design-tokens (5/8).
- "Grid**: 12 columns (desktop), 8 (tablet), 4 (mobile), 24px gutters" (c00252)
- "Grid | 8px snap, 24px gutter | All x/y/w/h must be multiples of 8" (s0092)
- "Reach for `grid-cols-3` / `grid-cols-4` / `grid-cols-6` whenever the items are conceptually parallel." (s0061)

### 13. Thumb reach and bottom placement on mobile
Put frequent and primary actions in the lower, one-hand-reachable part of the screen and out from under the keyboard.
- 7 records, 7 owners; 4 agents, 3 skills.
- Concentrates in production-code (5/7) and revise-existing mode (5/7): these are mobile optimizers working on existing apps.
- "Bottom third of screen = easy reach zone" (c00231)
- "iOS placement: prefer the bottom toolbar — it animates above the keyboard and stays within thumb reach" (s0100)
- "A form's primary action must never sit under the keyboard." (s0051)

### 14. Surface purpose decides composition
Classify the surface (monitor vs decide, tool vs editorial, data type) and let that decide layout and density, rather than a fixed section recipe.
- 6 records, 6 owners; 5 agents, 1 skill.
- Concentrates in create and revise-existing (6/6 each) and design-tokens (4/6).
- "Do not force a fixed section count, a fixed stack order, or a fixed number of cards or chips on every screen. Let the screen's purpose determine the layout." (c00490)
- "Before you write any colors, type scale, or components, commit out loud to exactly one surface archetype." (c00337)
- "Pick the right visual for the data. Maps for coordinates. Charts for numeric/trend data. Cards for structured records. Tables for comparisons. Timelines for events. Don't default to any one visual type." (s0086)

### 15. Generous whitespace
Use more space than feels necessary.
- 5 records, 5 owners; 2 agents, 3 skills.
- All 5 are production-code, create mode. It is contradicted inside the corpus by density rules for tools and dashboards (c00517 "Compact controls, clear table affordances, status chips, dense form groups, 4/8 grid.", c00392 "Design data-dense layouts suitable for wealth management dashboards"), and c00025 frames it as a choice: "Generous negative space OR controlled density."
- "Whitespace is a design element. Use generous spacing — at least 2x what feels \"enough.\"" (c00055)
- "Extreme whitespace. Padding and margins 2-3x what feels \"normal.\" Elements breathe." (s0074)
- "White space is a feature. Resist the urge to fill every pixel. Breathing room makes content digestible. When in doubt, add more space, not more content." (c00270)

Minor themes kept in the assignment file but below the cut: follow the project's own layouts and breakpoints (4 records, 4 owners, all agents; see section 4), text measure and alignment (4 records, 3 owners), and the "69% more time on the left half" statistic (2 records, 2 owners, one lineage).

## 2. Lineage warnings

- **agency-agents "design-ui-designer" family** (GammaLabTechnologies c00003, ForceMind c00069 in Chinese translation, imMamdouhaboammar c00090): same file name and the same line "Mobile: 320px - 639px (base design)". Three owners, one voice, in mobile-first and breakpoint values (and ForceMind also in touch targets, spacing, grid). c00003 alone carries 62 repository copies, so any copy-weighted view of breakpoints or mobile-first is dominated by this template.
- **ClaudeKit ui-ux-designer family** (mrgoonie c00001, 77 copies; withkynam c00028): identical quotes "All designs must be responsive and tested across breakpoints (mobile: 320px+, tablet: 768px+, desktop: 1024px+)" and "Touch targets must be minimum 44x44px for mobile". One voice across touch targets, breakpoint values and check-at-widths. With the agency family, these two templates supply 164 of the 206 copies summed under breakpoint values.
- **taste-skill family** (Leonxlnx s0005/s0006/s0018, google-labs-code s0058, withkynam s0116, nexu-io s0089 whose notes say it was distilled from a taste-skill repo): near-identical bans on centered heroes and "3 equal cards". Four owners, one voice, inside the anti-template theme.
- **Anthropic frontend-design / Impeccable lineage** (Pana-g c00025 and minicoohei c00608 share "Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements."; tech-leads-club s0002 is a frontend-design fork with Impeccable-style DON'Ts; fengshao1227 s0052 fuses Impeccable). Together with taste-skill, the anti-template theme drops from 18 owners to about 13 independent voices. It is still a real theme, but a younger and more copied one than its owner count suggests.
- **ascii-ui-mockup-generator** (davila7 c00208, softaworks c00511): identical "Demonstrate responsive considerations when relevant", one voice in responsive coverage.
- **ui-ux-designer reviewer** (davila7 c00009, Brahiamm56 c00179): identical "Users spend 69% more time viewing the left half of screens". The whole minor theme is one voice.
- **Aggregator owners**: davila7 (claude-code-templates), ccplugins (awesome-claude-code-plugins) and github (awesome-copilot) are collections, so their owner counts stand for the original authors, not the aggregator. ccplugins' c00007 and c00223 are from the studio-style agent set.
- **Convergent, not copied**: touch targets (44/48) and the 4/8 spacing scale read like paraphrases of Apple HIG, Material and Tailwind conventions. Most wording differs (similarity mostly below 0.9), so the high owner counts reflect a shared external standard rather than one template. That makes them common but not distinctive: they are what any designer prompt reaches for first.

## 3. Sharp but rare

1. plugin87 (2 records, 1 owner). An operational CSS rule with its failure mode, plus a render-inspection order: "**`auto-fit`, never `auto-fill`** for card grids. `auto-fill` keeps empty phantom tracks so 3 cards cluster left with a void on the right" (s0095); "Look at the 320px render before you accept the 1280px one." (c00532)
2. jakubkrehel. A geometric invariant that can be checked: "Outer radius = inner radius + padding. Mismatched radii on nested elements is the most common thing that makes interfaces feel off." (s0066)
3. FerroxLabs. Layout rules turned into countable findings with codes: "Information density: count interactive elements per surface; flag >9 peer-level CTAs as `INTERACTION_OVERLOAD`." (c00638; line breaks collapsed)
4. lobehub. Splits "empty" into distinct cases: "Distinguish first-use empty, no search matches, loading, and failure; include a useful body state beneath persistent chrome." (s0077)
5. seaworld008. Names layout shift as a defect class, and limits `clamp()` to layout: "Components that resize when hover, badges, counters, or loading text appear." and "Use `min()`, `max()`, `clamp()` for layout dimensions, but do not scale font sizes with viewport width." (s0103)
6. expo. A single checkable placement rule: "A form's primary action must never sit under the keyboard." (s0051)
7. plannotator. Defines what counts as a distinct variant: "Do not call color changes or minor card rearrangements separate directions." (s0094)
8. Rigos0. Shows what useful layout feedback looks like, measured and with a target: "\"The gap between the hero section and the terminal panels (currently ~80px) feels too large — 40-48px would create better visual connection\" is useful." (c00680)
9. meetpateldev18. Turns the spacing scale into a lintable ban: "All spacing MUST use this scale. No arbitrary values like `px-[13px]`." (c00407)
10. samuelclay. Keeps the hit area and the visible size separate: "Interactive elements need at least 40×40px hit area. Extend with a pseudo-element if the visible element is smaller." (s0102)

## 4. Bearing on the proposed designer

**(1) Start from the existing product.** Weakly supported in this dimension, and mostly undercut by it. Only 4 records (4 owners) tie layout to the project: "Decide responsive behaviour per breakpoint from the project configuration." (c00361), "The project provides **THREE** layout approaches - always use these instead of creating custom layouts" (c00368), "Ensure breakpoints match design specifications" (c00107), and states that "follow the same patterns as elsewhere" (c00629). Against that, the four biggest themes (mobile-first, 4/8 spacing, 44px targets, breakpoint sets) hard-code generic values in the prompt. That is 21 different breakpoint sets that disagree with one another and would override a project's own tokens. The evidence supports the proposal's choice to keep values out of the role: a role carrying "768/1024/1440" would clash with point (1) in every project that uses other numbers. One addition: the role should say that breakpoints, spacing scale and grid are read from the project (config, tokens) and that any departure is reported as a deviation.

**(2) Name user and task; one direction or distinct variants.** Supported by the structure/IA theme (12 owners), which puts screen inventory and navigation before visuals, and by surface-fit composition (6 owners): "commit out loud to exactly one surface archetype" (c00337) is close to "commit to one direction", and c00241 asks for 2-3 layout variants. plannotator adds a useful definition the proposal lacks, that a colour swap or card shuffle is not a separate direction (s0094). If the role keeps "distinct variants", it needs a one-line bar for "distinct"; the rest belongs in a skill.

**(3) Render and look before reporting.** Thin support. 13 owners say to test at named widths, but only c00532 ("Look at the 320px render before you accept the 1280px one.") and c00254 (resize the window) describe looking at output, and none says what to do when no renderer exists. The proposal's point is ahead of the corpus here, not contradicted by it. What this dimension adds is the order and the widths: check the narrowest width first, and check at the project's breakpoints, not at a fixed set. Because rendering may be unavailable, the role must also say what to claim without it (layout claims marked as not visually verified). This is contract material and belongs in the role. The width list belongs in the project or a check script.

**(4) States, responsive, accessibility baseline.** Strongly supported. Responsive in some form is the most widespread concern in the dimension (mobile-first 35 owners, breakpoints 21, general coverage 14, check-at-widths 13), states have 17 owners, and touch targets (29 owners) are the most common accessibility-adjacent layout rule. Two adjustments come from the evidence. First, "responsive" should mean each size is composed ("intentional, not merely scaled", c00449; per-component mobile behaviour, s0023), not just "doesn't break". Second, states should be broken into their real cases (first-use empty vs no results vs failure vs permission-denied: s0077, c00577, c00198). Whitespace vs density conflicts inside the corpus, which is another reason to leave doctrine to skills.

**(5) Boundary: designer decides and prototypes; implementer integrates.** This dimension says little directly. It does show a split in the population: the anti-template, whitespace and thumb-reach themes sit in production-code records (78%, 100%, 71%), while the structure, states and disclosure themes sit in spec and critique. The rules that matter most for a designer who hands off (structure, states, per-breakpoint behaviour) are the spec-side ones, which fits the proposed boundary. Code-level layout rules (auto-fit, container queries, Tailwind classes, `grid-flow-dense`) are implementation craft and belong in a skill the implementer can load too.

**(6) Return what was made, direction, screenshots, deviations, open questions; no self-judgement.** Indirect support. Review-mode records carry layout as checklists ("Works on mobile / tablet / desktop?", c00376; "Does the layout work at 375px and 1280px?", c00403), and FerroxLabs turns layout faults into coded findings. Both belong to a separate reviewer, which matches the proposal's split. Rigos0 (c00680) shows the form a reviewer's layout comment should take (measured value, proposed value). The designer's report should state per-width results and which states were built, as facts, which gives the reviewer something to check against.

**Where this dimension's content belongs**

- Role text: only the obligations. Take layout primitives (breakpoints, spacing scale, grid) from the project; cover each breakpoint as its own composition; build the non-happy states; check the narrowest width first when a renderer exists, and mark visual claims as unverified when it does not; report deviations from the project's layout system.
- Skill or project rule file: every numeric default (breakpoint sets, 4/8 scale, 12-column grid, 44/48 targets as a fallback when the project has none), the anti-template and whitespace/density doctrine, disclosure limits, thumb-zone placement and focal-point hierarchy. These are craft, they disagree across sources, and a project may override them.
- Tool or check: the rules that are mechanical. Spacing values off-scale (c00407, s0092), hit area below minimum (s0102, s0066), nested radius mismatch (s0066), `auto-fill` in card grids (s0095), layout shift on hover or badge (s0103), too many peer CTAs (c00638), and screenshots at the project's breakpoints narrowest-first. These can be verified without taste, so a script or reviewer checklist catches them more reliably than prose.
- Nowhere: the "69% left half" statistic (one lineage), golden-ratio sizing (c00249), and generic "design responsive layouts for all device sizes" lines, which add nothing a model does not already do.
