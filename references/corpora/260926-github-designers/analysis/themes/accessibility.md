# Accessibility: recurring instruction themes in design roles

Source: `claims/accessibility.jsonl`, all 320 lines read. They come from 214 distinct records (176 agents, 38 skills) and 189 distinct owners (156 agent owners, 34 skill owners; `microsoft` has both). For comparison, `stats.txt` shows the accessibility flag on 291 of the 405 design roles (72%; agents 76%, skills 60%). So 82 flagged roles mention accessibility without any specific quote that passed verification.

Method: each quote was assigned by hand to zero or more themes. Line-index lists and the counting script are reproducible from `accessibility.assign.json`, which maps each theme to its record ids. Counts come from that file. "Owners" means the part of `repo` before "/". "Voices" means owners after collapsing template families. Families were found by 6-word shingle overlap above 0.3 between records from different owners, plus one manual addition: c00611 is a Chinese translation of c00017. Output and mode "concentration" is the lift of a theme's share over the 214-record base, where 1.0 is neutral. The base counts are spec-or-handoff 129, design-tokens 107, design-system-docs 101, written-critique 100, production-code 80, wireframe 47, prototype 27, redesign-existing 25, html-mockup 12, visual-asset 11, and for modes create 176, review 141, revise-existing 98. Lifts on html-mockup and visual-asset rest on very small bases.

## 1. Top recurring themes (ordered by distinct owners)

### 1. Text contrast meets WCAG AA, stated as 4.5:1 body and 3:1 large text/UI
- Counts: 99 records, 96 owners (90 voices). 85 agents from 82 owners, 14 skills from 14 owners.
- Concentration: design-tokens (1.25) and design-system-docs (1.24). Mode-neutral (create 1.01, review 0.95).
- Quotes:
  - "Text contrast minimum 4.5:1 (WCAG AA)" — c00002
  - "Verify text/background pairs meet **WCAG AA** contrast (4.5:1 body text, 3:1 large text / UI). State the ratios." — c00290
  - "Contrast ≥ 4.5:1 for text, ≥ 3:1 for large text and UI components." — s0083

### 2. WCAG (2.1/2.2) AA declared as the baseline or compliance standard, with no operational content
- Counts: 49 records, 48 owners (45 voices). 49 agents from 48 owners, **0 skills**.
- Concentration: prototype (1.62), visual-asset (1.59) and wireframe (1.49). Leans revise-existing (1.25).
- Quotes:
  - "Accessibility validated at WCAG 2.1 AA level." — c00006
  - "Accessibility is not optional. WCAG 2.1 AA is the floor, not the ceiling." — c00270
  - "WCAG AA minimum for all designs" — c00080

### 3. Visible focus indicator and a logical focus order
- Counts: 35 records, 34 owners (31 voices). 28 agents from 28 owners, 7 skills from 6 owners.
- Concentration: html-mockup (1.53) and production-code (1.45). Slightly below 1 in every mode (revise-existing 0.69).
- Quotes:
  - "Never remove the focus ring without replacing it. This is the single most common SaaS accessibility regression." — s0045
  - "All interactive elements keyboard-accessible with visible focus indicators" — c00316
  - "specify focus order and keyboard interaction where interactive elements change" — c00013

### 4. Minimum touch or hit target size, with no agreement on the number
- Counts: 34 records, 33 owners (32 voices). 28 agents from 27 owners, 6 skills from 6 owners.
- Concentration: redesign-existing (1.76) and written-critique (1.13).
- The stated number varies: 44px is the modal value, 24px is cited as the WCAG 2.2 minimum (c00002, c00009, c00179, s0014), and 48px/48dp appears in c00613, c00628, s0072 and s0083.
- Quotes:
  - "Touch targets (44×44px design target; WCAG 2.2 SC 2.5.8 sets 24×24px minimum with adequate spacing)" — c00009
  - "Interactive elements minimum 24x24px touch target" — c00002
  - "Touch minimum: 48 px is the default. Some controlled environments (fixed-grip medical instruments, secured industrial panels) may justify smaller targets after explicit safety review." — s0083

### 5. Everything is operable by keyboard alone
- Counts: 33 records, 33 owners (32 voices). 28 agents from 28 owners, 5 skills from 5 owners.
- Concentration: near-neutral, with a slight lean to written-critique (1.10). Mode-neutral.
- Quotes:
  - "All interactive elements reachable via Tab key" — c00002
  - "Checkout/signup/settings can be completed by keyboard." — s0014
  - "Can the entire UI be navigated and operated using only the keyboard? Check for logical focus order and visible focus indicators." — c00569

### 6. Screen-reader semantics: semantic HTML, ARIA roles and labels, names for icon-only controls
- Counts: 33 records, 31 owners (31 voices). 25 agents from 24 owners, 8 skills from 7 owners.
- Concentration: html-mockup (2.16), wireframe (1.38) and prototype (1.20). Below 1 in review (0.74).
- Quotes:
  - "MUST add an `aria-label` to icon-only buttons" — s0063
  - "Keyboard/accessibility failure: interactive controls are not keyboard reachable, focus-visible is absent, icon-only controls lack names, or native elements are replaced with inert divs." — s0023
  - "Create accessible designs (ARIA labels, semantic HTML, keyboard navigation)" — c00242

### 7. Respect `prefers-reduced-motion`
- Counts: 20 records, 19 owners (17 voices). 13 agents from 12 owners, 7 skills from 7 owners.
- Concentration: html-mockup (2.67), production-code (2.14) and design-tokens (1.30). Leans create (1.16). This theme lives with the roles that actually emit animation code.
- Quotes:
  - "Every animation — generated in Create mode or reviewed in Audit mode — must handle `prefers-reduced-motion`. No exceptions." — s0075
  - "Reduced motion means fewer and gentler animations, not zero. Keep opacity and color transitions that aid comprehension. Remove movement and position animations." — s0003
  - "Build to a quality floor without announcing it: responsive down to mobile, visible keyboard focus, reduced motion respected." — c00114

### 8. A concrete check, tool or pass/fail gate instead of "ensure compliance"
- Counts: 19 records, 18 owners (18 voices). 14 agents from 13 owners, 5 skills from 5 owners.
- Concentration: prototype (1.67), written-critique (1.58) and spec-or-handoff (1.22). Leans review (1.36) and away from create (0.77).
- Quotes:
  - "const results = await new AxeBuilder({ page }).analyze(); expect(results.violations).toHaveLength(0);" — c00281
  - "Hard-gate: > 0 axe Critical OR > 0 axe Serious on any page = audit Fails." — s0072
  - "Focus not obscured (SC 2.4.11): Focused elements must not be fully hidden by sticky headers, cookie banners, or chat widgets — check with Tab key while scrolled" — c00179

### 9. Never convey meaning by colour alone
- Counts: 14 records, 14 owners (13 voices). 11 agents from 11 owners, 3 skills from 3 owners.
- Concentration: prototype (1.70), written-critique (1.38) and wireframe (1.30). Leans review (1.19).
- Quotes:
  - "Don't rely on color alone (use icons + color)" — c00002
  - "Positive/negative must be distinguishable without color alone (icon/direction/label)." — c00354
  - "Don't use color as the only means of conveying information. Color blindness affects approximately 8% of males." — c00170

### 10. Accessibility belongs at the start and is not an afterthought
- Counts: 15 records, 14 owners (13 voices). 15 agents from 14 owners, **0 skills**.
- Concentration: prototype (3.17), wireframe (2.73) and redesign-existing (1.71). Leans create (1.22).
- Quotes:
  - "Build accessibility into the foundation rather than adding it later" — c00003
  - "Meet WCAG 2.2 AA from inception: use at least 4.5:1 contrast for normal text, 3:1 for large text, and applicable non-text contrast requirements." — c00449
  - "Include the ability spectrum from the start — every flow, every journey map, every persona considers permanent, temporary, and situational disabilities" — c00236

### 11. Accessibility is written into the deliverable (annotations, per-component contracts, stated ratios)
- Counts: 15 records, 14 owners (14 voices). 15 agents from 14 owners, **0 skills**.
- Concentration: prototype (1.59), spec-or-handoff (1.55) and design-system-docs (1.27). Low in review (0.40), which makes this a create/spec habit.
- Quotes:
  - "Include per role the foreground/background pairing used, so the a11y auditor can compute contrast. Do NOT emit CSS/Tailwind/Mantine." — c00262
  - "This table must be included in the component API specification document. No component ships without its accessibility contract satisfied." — c00232
  - "Accessibility is not optional — every component gets aria and keyboard notes." — c00659

### 12. Text scaling, zoom and minimum font size (200% zoom, Dynamic Type, fontScale, 16px body)
- Counts: 11 records, 11 owners (11 voices). 7 agents from 7 owners, 4 skills from 4 owners.
- Concentration: production-code (1.46), design-tokens (1.27) and written-critique (1.17). Low in revise-existing (0.60).
- Quotes:
  - "Text Scaling: Design works with browser text scaling up to 200%" — c00090
  - "UI must gracefully handle `fontScale = 2.0f` (200% text size) without clipping, overlapping, or broken layouts." — c00628
  - "Never disable scaling app-wide with `allowFontScaling={false}`." — s0050

### 13. AAA or higher as the target (7:1 contrast)
- Counts: 10 records, 10 owners (10 voices). 9 agents from 9 owners, 1 skill.
- Concentration: wireframe (1.82), design-system-docs (1.48) and spec-or-handoff (1.33). Leans create (1.22).
- This theme conflicts with theme 1 on the number: one role pairs "AAA" with 4.5:1 for large text, others ask for "AAA where possible".
- Quotes:
  - "Accessibility Compliance**: WCAG AAA contrast ratios (7:1 for normal text, 4.5:1 for large)" — c00247
  - "Apply color theory with accessibility as a primary constraint (WCAG 2.1 AA minimum, AAA preferred)" — c00277
  - "Normal text: 7:1 contrast ratio" — s0055

### 14. When accessibility and aesthetics conflict, accessibility wins
- Counts: 9 records, 9 owners (9 voices). 6 agents from 6 owners, 3 skills from 3 owners.
- Concentration: production-code (1.78) and design-tokens (1.33). Leans revise-existing (1.46).
- Two roles push the other way: "Aim for WCAG 2.1 AA where practical, but prioritise flexibility to build any kind of UI." (c00597), and "Discard accessibility and HTML/ARIA semantic findings unless the user explicitly requests them." (s0064, which only scopes a review skill).
- Quotes:
  - "If design conflicts with accessibility, prioritize accessibility and explain trade-offs" — c00001
  - "Never violate accessibility for the sake of aesthetics. Contrast ratios are not a suggestion." — c00139
  - "Ignoring contrast ratios: WCAG AA minimum. Beautiful but unreadable is a failure." — s0038

### 15. Deep accessibility conformance is deferred to a separate accessibility role
- Counts: 6 records, 5 owners (5 voices). 4 agents from 3 owners, 2 skills from 2 owners.
- Concentration: written-critique (1.43). Leans review (1.26).
- Quotes:
  - "Technical conformance, WCAG criteria, keyboard and screen-reader implementation, contrast, target size, zoom, ARIA patterns, COGA guidance, runtime validation, and accessibility review belong to `accessibility`." — c00135
  - "Inline `color:` + `background-color:` pairs computed at <3.0 ratio → `OBVIOUS_CONTRAST_FAIL` HIGH. Defer subtler AA cases to the accessibility-reviewer." — c00638
  - "Never rely on color alone, and check every text/icon/surface pair for contrast — defer the actual ratios and color-blindness checks to the accessibility audit" — s0032

Just below the cut: two owners treat light and dark themes as separate things to check (c00021 "dark mode parity", c00361 "check them on both themes"). Four owners ask for the user range or disability spectrum to be named (c00236, c00507, c00330, s0085).

## 2. Lineage warnings

- **Owner inflation is minimal.** Owners are close to records in every theme; the largest gap is 3 (99 records against 96 owners in theme 1). No theme is carried by a single owner.
- **Copy counts inflate the top themes.** Measured by `copies_in_repos`, the top themes rest on a handful of widely copied agents: c00001 (77 copies), c00002 (75, awesome-copilot), c00003 (62), c00006 (49), c00007 (39) and c00008 (35). In theme 4, c00002 alone supplies 75 of the 188 summed copies. In theme 10, c00003, c00007 and c00008 supply 136 of 205. The counts above are per record, so they are not copy-weighted, but anyone weighting by copies will see these few voices dominate.
- **Aggregator owners are not authors.** `github` (awesome-copilot), `davila7` (claude-code-templates), `ccplugins` (awesome-claude-code-plugins), `wshobson`, `ChrisRoyse/610ClaudeSubagents` and `Toskysun/sub-agents` are collections. Their records can duplicate agents found elsewhere under other names, and the shingle check catches only close text copies.
- **Template families that were detected:**
  - The agency-agents "UI Designer" family: c00003 harmonist, c00069 ForceMind (a Chinese translation), c00090 riqor and c00256 legion. This family is three records in theme 1 and two in theme 10. The phrases "Build accessibility into the foundation" and "Default requirement: Include accessibility compliance (WCAG AA minimum) in all designs" come from this family, not from independent authors.
  - Anthropic's frontend-design "quality floor" line: c00114, s0004 and s0037. These are three owners and one voice in themes 3 and 7, so 19 owners become 17 voices in theme 7.
  - The Claude-Code-Game-Studios family: c00017, c00150, and c00611 in Chinese. It appears in themes 5, 9, 12 and 14, and its checklist items ("Usable with keyboard only", "Functional without reliance on color alone") recur verbatim.
  - c00009/c00179 (davila7 template; "Focus not obscured (SC 2.4.11)"), c00006/c00074 ("Accessibility validated at WCAG 2.1 AA level."), c00053/c00132 ("Colour contrast: 4.5:1 for normal text (< 18px)"), c00001/c00028, c00616/c00621 (a Chinese/English pair), c00164/s0084 and c00113/c00430.
- **Boilerplate inflation.** Theme 2 has 48 owners but zero skills, and almost every quote is a one-line declaration with no check attached. Theme 10 is the same. Their breadth reflects a common agent-template habit, not a practice. Skills never phrase accessibility this way, and when they mention it they give a mechanism: axe gates, a primitives library, reduced-motion policy, or scaling flags.
- `slabgorb` (c00117) and `slabgorb-org` (c00312) are probably the same author under two owner names. Both are counted as separate owners.

## 3. Sharp but rare (1-2 owners, precise or operational)

1. "Focus not obscured (SC 2.4.11): Focused elements must not be fully hidden by sticky headers, cookie banners, or chat widgets — check with Tab key while scrolled" — c00179 (the same template as c00009, 2 owners)
2. "A no-text control (carousel dot, kebab, icon button) is held to **3:1** (WCAG 1.4.11), not 4.5" — s0095
3. "Inline `color:` + `background-color:` pairs computed at <3.0 ratio → `OBVIOUS_CONTRAST_FAIL` HIGH. Defer subtler AA cases to the accessibility-reviewer." — c00638. This splits the work into a cheap computed check and a specialist review.
4. "Include per role the foreground/background pairing used, so the a11y auditor can compute contrast. Do NOT emit CSS/Tailwind/Mantine." — c00262
5. "Text color #666 on white background has insufficient contrast ratio (3.1:1)" / "Use #595959 or darker for 4.5:1 ratio" — c00154
6. "Give dialogs an accessible name, contain focus, close on `Escape`, and restore focus to the trigger." — s0093
7. "UI must gracefully handle `fontScale = 2.0f` (200% text size) without clipping, overlapping, or broken layouts." — c00628, with "Use `Modifier.minimumInteractiveComponentSize()` when needed." (same record)
8. "Set accessibility targets as numbers and behaviours, and check them on both themes." / "Does not approve a screen whose focus state is invisible on either theme." — c00361
9. "Reduced motion means fewer and gentler animations, not zero. Keep opacity and color transitions that aid comprehension. Remove movement and position animations." — s0003
10. "\"44pt is too big for this icon\" | Minimum is minimum. Expand hit area, not visual." — c00430

Also notable:
- "Visible focus indicator required. Focus trap prevention in loading state." and "aria-busy: When loading" (c00064) tie accessibility to the loading state.
- "Content or a control clipped, overlapped, or unreachable at 320px width or 200% zoom." (s0068)
- "MUST use accessible component primitives for anything with keyboard or focus behavior (`Base UI`, `React Aria`, `Radix`)" (s0063)

## 4. Bearing on the proposed designer

**(1) Start from the existing product and follow its design system.** The evidence supports this and adds to it. Several roles tie accessibility to what the project already has, not to a fixed number: "per the project's accessibility standard" (c00330), "Maintain WCAG AA color contrast for text and interactive elements regardless of the chosen aesthetic." (c00424), and "MUST use accessible component primitives…" (s0063). For redesign work, s0024 adds a point the proposal lacks: "Preserve accessibility intent such as label relationships, focus order, landmark roles, and keyboard affordances." A redesign can silently drop semantics that the existing UI had, so "follow the existing system" should include its accessibility behaviour, not only its look. Nothing in the corpus contradicts this point.

**(2) Name the user and the task, then commit to a direction.** Support is weak but present. Theme 10 and the user-range items (c00236 "ability spectrum", c00507 "the quiet users: … small screen, in low light, on a weak connection") treat situational constraints as part of who the user is. There is a caution against over-reach: "Do not name a specific disability, demographic, age, language, literacy, or comparable cohort as excluded without `Observed` or `Reported` support." (s0085). Nothing here requires more role text.

**(3) Render and look before reporting.** This point is the most informative for this dimension, and it refines the proposal more than it confirms it. Accessibility claims divide into two kinds:
- **Claims decidable without a browser.** Contrast can be computed from colour pairs, and the corpus does exactly that (c00638 computes pairs, c00262 emits pairs "so the a11y auditor can compute contrast", c00154 names hex values). The presence of `aria-label`, `lang` or `:focus` styles can be read in source (c00639 "Missing `:focus` is always BLOCK").
- **Claims that need a run.** Focus hidden under sticky headers "check with Tab key while scrolled" (c00179), reflow "at 320px width or 200% zoom" (s0068), "Verify behavior with reduced-motion enabled and Dynamic Type at largest size" (s0084), a focus state visible "on both themes" (c00361), and axe run against a live page (c00281, s0072). A screenshot is not enough for these; they need keyboard traversal and emulated preferences.

Only 37 of the 214 records carry the `renders_and_looks` flag. Of the 19 records in the concrete-check theme, 4 have it (c00281, c00361, s0068, s0072). Because the role cannot assume a browser, the useful contract wording is this: state computed contrast ratios (c00290 "State the ratios."), and label keyboard, zoom and motion behaviour as either "exercised" or "not exercised". Do not claim accessibility from reading code. This matches the proposal's rule that claims about appearance come from inspection, and extends it to claims about behaviour.

**(4) States, responsive behaviour and an accessibility baseline.** The evidence strongly supports this. Accessibility appears in 72% of design roles, and the owner counts give the actual baseline: contrast (96), visible focus (34), touch target (33), keyboard (33), screen-reader names (31), reduced motion (19), not colour alone (14), and text scaling or zoom (11). The corpus also links accessibility to states: "Ensure the design system covers all states: default, hover, focus, active, disabled, error, loading" (c00299), and "Focus trap prevention in loading state" / "aria-busy: When loading" (c00064). The numbers conflict: touch targets are 24, 44 or 48; contrast targets are AA or AAA; non-text contrast is 3:1 (s0095) where others apply 4.5 to everything. So the role should name the baseline categories and leave the numbers to a rule file or the project.

**(5) Boundary: the designer decides and prototypes, and an implementer integrates.** Theme 15 supports a second boundary the proposal does not name: conformance auditing goes to an accessibility reviewer (c00135, c00638, s0032, c00262). c00182 shows the reverse direction, "Accessibility vs aesthetics conflict: accessibility wins; document the constraint for the UI designer". This fits the proposal's statement that review is separate. The designer covers the design-level baseline, and conformance (ARIA patterns, screen-reader runtime, WCAG criteria) belongs to review. The harness has no accessibility role, so that work would fall to the generic reviewer, or the brief would have to name it.

**(6) Return what was made and do not judge its own quality.** Theme 11 (14 owners) supports adding accessibility notes to the return, but they should be concrete: fg/bg pairs with their ratios, per-component keyboard and aria notes, and the checks that were and were not run. This part of the proposal needs care. Many roles in the corpus self-gate ("Re-audit after fixes are applied — do not approve until AA compliant" c00399; "BLOCK if any body-text pair under 4.5:1…" c00639; "Does not approve a screen whose focus state is invisible" c00361), but those are review-mode roles. Measured facts, such as a computed ratio or "Tab reaches all controls", are not quality judgments, so reporting them does not conflict with "review is separate". A verdict such as "accessible" or "WCAG AA compliant" would conflict, and it is exactly the unverified boilerplate of theme 2.

**The aesthetics precedence (theme 14, 9 owners, 2 counter-voices).** This is a conflict-resolution rule between craft and baseline, not craft itself. It is small enough to be a candidate for `/kein:deliberate`, not an automatic inclusion.

**Where the content should live:**
- **Role text:** at most two contract-level items. First, the accessibility baseline is part of what the designer covers, named by category and with no numbers. Second, the report states computed ratios and says which keyboard, zoom and motion behaviours were actually exercised and which were not. Everything else is too specific or too contested for a standing role prompt.
- **Skill or project rule file:** all thresholds (4.5/3:1, non-text 3:1, 24/44/48 touch, AA versus AAA, 16px body), reduced-motion policy (s0003's "fewer, not zero"), not colour alone, dialog focus handling (s0093), the choice of primitives library (s0063), and the aesthetics-versus-accessibility precedence if it is kept. These differ by project and platform (Compose dp, iOS Dynamic Type, web), which is why they should not sit in the role.
- **Tool or check:** contrast computation over token or colour pairs is deterministic and cheap, so the role could call it whether or not a browser exists (c00638 already does this with a threshold split). An axe run and a scripted Tab traversal, zoom and reduced-motion pass are checks to run when a browser tool is present. A mechanism should hold these rules; prose should not.
- **Nowhere:** theme 2 declarations ("WCAG 2.1 AA compliance", 48 owners, 0 skills) and theme 10 slogans ("from the start", "not an afterthought"). They carry no operation, the skills in the corpus do without them, and they invite the unverified compliance claims that point (6) should forbid.
