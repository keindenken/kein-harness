# Interaction and motion: recurring themes

Source: `claims/interaction-motion.jsonl`, 201 quote lines from 141 distinct design-role records (97 agents, 44 skills) by 127 distinct owners (93 agent owners, 37 skill owners; a few owners have both). That is about a third of the 405 design roles. Theme assignment is by quote line; the ids per theme are in `interaction-motion.assign.json`, and every count below comes from that file joined with the claims file. 177 of the 201 lines fall into at least one theme (some lines are in two). The other 24 are singletons or off-topic, such as CLI install behaviour (c00214), TTS barge-in (c00218) and gamepad input mapping (c00017).

"Concentrates in" lists the outputs or modes that show up more often among a theme's records than among the 141 records in this dimension, as a lift ratio. Record counts are small, so read the lifts as direction only.

## 1. Top recurring themes (ordered by distinct owners)

### T1. Respect `prefers-reduced-motion`
Any animation needs a reduced-motion alternative, either through the media query or a library hook.
- 23 records / 23 owners; agents 20 (20 owners), skills 3 (3 owners). Copies across repos sum to 211, the highest reach of any theme.
- Concentrates in: design-tokens (16/23, x1.6), design-system-docs (13/23, x1.7). Spread evenly over create, review and revise.
- "Animations should respect prefers-reduced-motion preferences" (c00001)
- "Always support `prefers-reduced-motion` — use Framer Motion's `useReducedMotion` or a CSS media query" (c00377)
- "Specify motion with duration, easing, property and the reduced motion behaviour, or specify none." (c00361)

### T2. Duration budgets
Motion gets named millisecond ranges, with a hard ceiling for UI animation.
- 23 records / 23 owners; agents 16 (16), skills 7 (7).
- Concentrates in: production-code (16/23, x1.4), written-critique (14/23, x1.4), prototype (5/23, x1.9), review mode (x1.3).
- The numbers disagree. The ceiling is 300ms in s0003 ("UI animations should stay under 300ms"), 500ms in c00263 and s0083, and 200ms for interaction feedback in s0063. c00577 allows 500 to 1500ms for a marketing hero.
- "Duration budgets: Small elements (icons, badges): 100–150 ms. Medium elements (cards, panels): 200–300 ms. Full-screen transitions: 300–400 ms. Never exceed 500 ms for any UI animation — slower feels broken." (s0083)
- "Duration: 150-300ms for micro-interactions, 300-500ms for page transitions. Ease: ease-out for entering elements, ease-in for leaving. No bouncing, no elastic, no gratuitous parallax." (c00322)
- "NEVER exceed `200ms` for interaction feedback" (s0063)

### T3. Animate only compositor properties (transform and opacity), and keep animation cheap
No animating width, height, top, left, margin or padding. Some records add a 60fps target and a ban on raw scroll listeners.
- 18 records / 18 owners; agents 10 (10), skills 8 (8).
- Concentrates in: production-code (13/18, x1.5), design-tokens (12/18, x1.6), prototype (x2.0). Under-represented in review (x0.6) and written-critique (x0.4), so this is a build rule rather than a critique rule.
- "Motion: animate only `transform` and `opacity`. Respect `prefers-reduced-motion`." (c00024)
- "Animate `transform`/`opacity` only — never `top`/`left`/`width`/`height`, never a raw `scroll` event listener" (c00646)
- "DO: For height animations, use grid-template-rows transitions instead of animating height directly" (s0002)
- Counter-rule: "A component that toggles open/closed must animate its **height**, not just rotate a chevron" (s0095).

### T4. Async and data states: loading, empty, error
Define what the UI shows while loading, when empty and on failure. Skeletons are preferred over spinners.
- 17 records / 17 owners; agents 15 (15), skills 2 (2).
- Concentrates in: wireframe (4/17, x2.4), spec-or-handoff (11/17, x1.2). Under-represented in production-code (x0.5), which makes this a design-spec concern.
- "Don't deliver static mockups without interaction specifications. How does the dropdown animate? What happens on hover? What's the loading state?" (c00170)
- "Loading states: skeleton screens for content; spinner only for actions < 2s; progress bar for long operations" (c00182)
- "Every data-loading state needs loading, error, and empty states." (c00597)

### T5. Flow integrity: no dead ends, actionable errors, fewer steps
Every state has a next step, every control does what it advertises, errors keep the user's input, and step counts get counted.
- 14 records / 14 owners; agents 10 (10), skills 4 (4).
- Concentrates in: wireframe (4/14, x2.9), spec-or-handoff and written-critique (x1.2 to x1.3).
- "Every non-terminal state has at least one actionable next step" (c00393)
- "Every enabled control must perform its advertised action: search filters results, Save commits edits, and settings affect behavior. Empty handlers and success alerts are not implementations" (s0051)
- "Preserve user input (don't clear forms on error)" (s0027)

### T6. One orchestrated entrance with staggered reveals, instead of scattered micro-interactions
- 13 records / 13 owners; agents 5 (5), skills 8 (8). **Mostly one lineage** (see section 2).
- Concentrates in: production-code (12/13, x1.9) and create mode (13/13).
- "one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions" (s0000; the same sentence appears in s0038, s0041 and s0116)
- "Don't animate a single container. Break content into semantic chunks and stagger each with ~100ms delay." (s0102)
- "Critical: Total stagger must stay under 500ms." (s0020)
- Opposed by s0045 ("No entrance animations on page mount, no decorative parallax, no stagger on every grid."), s0044 ("The content does NOT stagger in one-by-one") and s0037, which calls "fade-and-slide-up entrances on each section" the generic AI default.

### T7. Feedback latency
Every action gets visible feedback within about 100ms, and longer operations get a progress indicator.
- 13 records / 13 owners; agents 8 (8), skills 5 (5).
- Concentrates in: written-critique (9/13, x1.6), redesign-existing (x2.3), review and revise modes. This is mostly a critique checklist item.
- "every action must have visible feedback within 100ms (instant), 1s (loading indicator), or 10s (progress bar)" (c00053)
- "Interaction latency acceptable (hover/click responses <100ms; INP target: <200ms at p75)" (c00009)
- "Does not specify motion that delays interaction." (c00361)

### T8. Component interaction states: hover, focus, active, pressed, disabled
- 13 records / 13 owners; agents 13 (13), skills 0.
- Concentrates in: design-system-docs (x1.4), html-mockup (x1.7), revise-existing (x1.5).
- "Every interactive element needs hover, focus, active, and disabled states." (c00597)
- "Don't just review static appearance; consider interactive states" (c00107)
- "a `hover:` class on an interactive element ... without a paired `active:` or `focus-visible:` class on the same element" (c00419; written as a lint pattern)

### T9. Motion must have a purpose; no decorative motion
- 12 records / 10 owners; agents 5 (5), skills 7 (6).
- Concentrates in: design-tokens (9/12, x1.8), design-system-docs (x1.7).
- "Every animation needs a one-sentence justification: hierarchy, storytelling, feedback, or state change. \"It looked cool\" is not one." (c00646)
- "Motion discipline: motion should explain state, space, or feedback. Avoid ambient motion in work tools." (s0023)
- "SaaS motion is **fast, ease-out, and only on user-initiated events**." (s0045)
- Contradicted by taste-skill (s0006, s0018): "Static interfaces are strictly forbidden." and "Every card must have an \"Active State\" that loops infinitely". In s0006 this is gated on a MOTION_INTENSITY dial.

### T10. Press and hover feedback specifics
Every pressable element reacts on press, hover changes stay small, and a hover scale must not move the layout.
- 10 records / 10 owners; agents 3 (3), skills 7 (7).
- Concentrates in: production-code (9/10, x1.9), redesign-existing (x3.0).
- "Any pressable element gets `transform: scale(0.97)` on `:active` with a ~160ms `ease-out` transition." (s0098)
- "every pressable thing moves on press, not only on hover, because hover is pointer-only and an unmoved control leaves the click unacknowledged" (s0112)
- "Hover effects should be subtle, not dramatic (2–4px lift max)" (c00334)
- The records disagree on scale: c00197 says "Hover feedback (color, shadow, border - NOT scale transforms)", and c00602 wants no button transitions at all.

### T11. Motion is specified as a system: tokens and written specs
Durations and curves are named tokens, and specs state each motion's duration, easing, property and reduced-motion fallback.
- 9 records / 9 owners; agents 8 (8), skills 1 (1).
- Concentrates in: prototype (5/9, x4.9, the strongest lift in the dimension), design-system-docs (x2.0), spec-or-handoff (x1.5).
- "Motion is systemic, not ad-hoc — every duration and curve is a named token." (c00335)
- "Define animation duration scale (fast: 150ms, base: 300ms, slow: 500ms)" (c00079)
- "Animation specifications with detailed timing and easing documentation" (c00692)

### T12. Easing: ease-out for UI, never ease-in, no linear or bounce; springs where they fit
- 9 records / 9 owners; agents 4 (4), skills 5 (5).
- Concentrates in: design-tokens (x1.3), create mode (9/9).
- "Never use `ease-in` for UI. It delays the first moment of movement - exactly when the user is watching - so a 300ms `ease-in` dropdown feels slower than a 300ms `ease-out` one." (s0098)
- "Never linear for spatial movement — always use easing curves (linear only for spinners, progress bars)" (s0020)
- "Spring Physics default: `stiffness: 100, damping: 20` — premium, weighty feel. No linear easing" (s0058)
- Conflict: c00108 and c00322 prescribe ease-in for exits, while s0003 and s0098 ban ease-in for UI.

### T13. Entrance and exit geometry
Never animate from scale(0), scale from the trigger's origin, and make entrances longer than exits.
- 8 records / 8 owners; agents 0, skills 8 (8). **Mostly two schools** (see section 2).
- Concentrates in: production-code (x1.6), html-mockup (x2.7), prototype (x2.2).
- "Never animate from `scale(0)`.** Nothing real appears from nothing. Start at `scale(0.9)` or higher plus opacity so the entrance has shape." (s0098)
- "Entrances 30-50% longer than exits. Users care about what appears." (s0020)
- "Keep press feedback immediate... Start movement from the element or control that caused it." (s0109)

### T14. Frequency rule: the more often an action happens, the less it should move
Keyboard-initiated and high-frequency actions are not animated.
- 6 records / 6 owners; agents 1 (1), skills 5 (5). **One school** (see section 2).
- Concentrates in: production-code and written-critique (5/6 each).
- "The deciding factor is frequency. The more often a user sees it, the less it should move." (s0098)
- "Never animate keyboard-initiated actions. These actions are repeated hundreds of times daily." (s0003)
- "No transitions on buttons / primary interactive elements — feedback is instant (`transition: \"none\"`)." (c00602; this is a project's own motion language)

### T15. Destructive and irreversible actions need deliberate confirmation
- 6 records / 6 owners; agents 5 (5), skills 1 (1).
- Concentrates in: review mode (5/6), written-critique (x1.5).
- "Every irreversible action (order submit, cancel, liquidate) must have an explicit confirmation flow." (c00354)
- "Require a deliberate gesture for unrecoverable or broad destructive actions and report partial failure." (s0077)
- "Destructive actions: use confirmation dialogs — never plain links for delete/destructive operations." (c00311)

## 2. Lineage warnings

- **T6, orchestrated staggered entrance.** 9 of its 13 records (c00025, c00029, c00072, c00116, c00608, s0000, s0038, s0041, s0116) come from Anthropic's frontend-design skill, repeating its sentence "one well-orchestrated page load with staggered reveals" verbatim or nearly so. Two more (s0066, s0102) are one author's make-interfaces-feel-better skill. That leaves about 4 independent voices, not 13. Several independent owners argue against it (s0037, s0044, s0045). Treat T6 as a single house style, not a consensus.
- **T13, entrance geometry, and T14, frequency rule.** Both are mostly one motion school. Emil Kowalski is named in s0003, s0075 and s0108. s0098, s0112 and s0109 restate his rules without attribution; s0098 is near-verbatim ("Never animate from scale(0)", "Never use ease-in for UI"). s0066, s0070 and s0102 are jakubkrehel's skill family, and s0102 (samuelclay/NewsBlur) is a copy of it. Taking those out leaves about 3 to 4 independent voices per theme. T12's anti-ease-in position and part of T10 have the same source (s0003, s0098, s0108, s0112).
- **T1, reduced motion.** c00001 and c00028 are the same ClaudeKit ui-ux-designer template, and c00003 and c00090 are the same agency-agents UI-designer template with identical wording. So 23 owners come to about 21 independent voices. The copy total of 211 comes mostly from c00001 (77 copies) and c00003 (62 copies), so reach overstates independence. The theme still stands: it has many distinct wordings.
- **T2, duration budgets.** c00179 and c00231 share one research-cited critic template ("Slow animations (>300ms for UI elements)"). Three of the skill records are the Emil school. That leaves about 19 independent voices, and their numbers still disagree.
- **T3, compositor-only.** s0002 and s0052 both come from the Impeccable DO/DON'T catalog, a fork of frontend-design. That leaves about 17 voices.
- **T9, purposeful motion.** Orkas-AI contributes 2 records (c00517, s0023) and cloudflare 2 (s0044, s0045). Owners are already counted once each, but 10 owners for 12 records shows the skew.
- Themes with no detectable shared template: T4, T5, T8, T11, T15.

## 3. Sharp but rare (1 to 2 owners, precise or operational)

1. "Inject `*,*::before,*::after{transition:none !important}`, force a reflow, then remove it on the next frame." (s0070): suppresses transitions during theme switches.
2. "If velocity exceeds ~0.11, dismiss regardless of distance. A quick flick should be enough." (s0003): a gesture threshold for swipe dismissal.
3. "Use `initial={false}` on `AnimatePresence` to prevent enter animations on first render." (s0102)
4. "Popovers and dropdowns scale from their origin, not their center. Modals stay centered." (s0098)
5. "a `hover:` class on an interactive element ... without a paired `active:` or `focus-visible:` class on the same element" (c00419): an interaction rule already written as a mechanical lint check.
6. "Don't paint affordances you don't wire (`cursor: zoom-in` with no zoom, keycap chips with no keys) — in an interactive prototype a dead affordance is a spec bug." (s0076): aimed at prototypes specifically.
7. "Validation timing: inline validation on blur (not on keystroke); submit-time summary for multi-field forms" (c00182)
8. "Never opacity-only for important state changes — combine with position or scale" (s0020)
9. "Critical alerts (margin call, circuit breaker, API disconnect) must interrupt — not just notify." (c00354)
10. "Use a small, keyboard-operable selector so reviewers can compare them without opening several files." (s0094): the one operational rule in this dimension for presenting several variants.

## 4. Bearing on the proposed designer

**(1) Start from the existing product and follow its design system.** Supported, and this dimension adds evidence for keeping motion values out of the role. Where a project has its own motion language, records defer to it: "All interaction specs must respect the VerifyWise motion language defined in `Clients/src/presentation/pages/StyleGuide`" (c00602); "Preserve current route flow behavior and CTA intent during visual changes." (c00344); "Hover states use `var(--mantine-color-default-hover)` not transparent" (c00392). The generic numbers conflict across the corpus: T2 ceilings run from 200 to 500ms, T12 disagrees on ease-in for exits, and T10 disagrees on press scale versus no transition. The role should read the project's motion tokens first and should not carry defaults of its own.

**(2) Name the user and the task; commit to a direction or produce variants.** This adds a useful link. In T14, how much motion is right follows from the task: how often the user repeats the action ("The deciding factor is frequency", s0098). T9 ties motion to purpose and to product type ("Avoid ambient motion in work tools", s0023). So naming the task has a concrete downstream use for motion. For variants, s0094 is the only operational rule: a keyboard-operable selector for comparing them.

**(3) Render and inspect before reporting.** Supported, but this is the dimension where a screenshot is weakest. Timing, easing, press feedback and reduced-motion behaviour are temporal, and a still image cannot confirm them. The corpus mostly treats motion as something to specify or grep for: c00361 asks for a written spec, and c00419 and c00024 rely on grep-style checks. Only c00441 says "verify `prefers-reduced-motion` is respected". With a browser tool, reduced-motion emulation and hover or press states can be observed. Without one, the role should report motion claims as specified in code, not as observed. That fits the contract's rule that claims about appearance come from inspection, and it needs saying explicitly for motion.

**(4) States, responsive behaviour and an accessibility baseline.** Strongly supported, and this dimension suggests widening the wording. T4 (loading, empty and error; 17 owners) confirms the listed states. T8 (13 owners, all agents) adds interactive states: hover, focus, active or pressed, and disabled. T1 (23 owners, the top theme) is the motion part of the accessibility baseline. T5 (no dead ends, actionable errors; 14 owners) is a flow-level state concern that the current contract does not name. A contract line such as "cover data states (empty, loading, error), interactive states, reduced motion" would match the evidence better than "states (empty, loading, error)" alone.

**(5) Boundary: the designer decides and prototypes, and implementation goes to an implementer.** Mixed. T3, T6, T10, T12 and T13 concentrate in production-code output (lifts 1.5 to 1.9), so much of the motion craft in the corpus is implementation-level: compositor properties, `useMotionValue`, `AnimatePresence`. T11 concentrates in prototype and spec output (x4.9 and x1.5), which suggests the designer's part is to specify motion as tokens or specs, and to implement it only inside the prototype. Nothing here contradicts the boundary.

**(6) Returns what was made, the direction, screenshots, deviations and open questions, and does not judge its own quality.** This dimension adds one item: a motion and interaction spec for handoff (duration, easing, property and reduced-motion fallback per c00361, plus the list of states covered). c00170 treats a static mockup handed over without it as incomplete. On self-judgement, T7, T15 and part of T5 lean toward review mode and written critique. They read as reviewer checklists, which is consistent with keeping review separate.

**Where this content belongs**
- **Role text:** only the contract-level points: cover interactive and data states and reduced motion; follow the project's motion tokens; report motion as a spec and say whether it was observed or read from code. None of the numbers.
- **Skill or project rule file:** duration budgets, easing, compositor-only, press and hover specifics, entrance geometry, the frequency rule, the purpose test, and the staggered-entrance position (T2, T3, T6, T9, T10, T12, T13, T14). These are contested craft positions, often from one school, and they should be swappable per project.
- **Tool or check:** reduced motion present wherever animation is (grep for `prefers-reduced-motion` or `useReducedMotion`); animated layout properties or `transition-all` (grep); `hover:` without `focus-visible:` or `active:` (c00419 already gives the pattern); durations over a project ceiling (grep). With a browser, emulate reduced motion and capture hover and press states. These checks belong to a reviewer or checker, not to the designer's self-assessment.
- **Nowhere:** vague lines ("Implement smooth, tasteful animations and transitions", c00371), the taste-skill mandate for perpetual looping animation (s0006, s0018), and the off-dimension items (CLI composability c00214, TTS barge-in c00218, gamepad input mapping c00017).
