# Visual craft: recurring instruction themes

Source: every line of `claims/typography-color.jsonl` (219 lines) and `claims/visual-rules.jsonl` (195 lines), 414 quotes in all. Together they come from 204 distinct design-role records and 174 distinct owners: 143 agent records from 128 owners, and 61 skill records from 50 owners. That is half of the 405 design roles. Visual-craft quotes are more common in skills (61 of 97, 63%) than in agents (143 of 308, 46%).

Method: I read each quote and assigned it by hand to zero or more themes. A quote can sit in more than one theme. All counts were then computed from the assignments against `records.json`. `visual-craft.assign.json` holds the ids for each theme, and the `minor:` keys hold the themes that are cited below but fall outside the top 15. The top 15 themes cover 167 records and 145 owners, and all themes together cover 185 of the 204 records. The rest are one-off quotes (CLI output formatting, logo misuse, CSS bundle size and similar).

"Concentrates in" gives the output or mode whose share among the theme's records is highest compared with its share among all 405 design roles (lift). Only outputs and modes with at least 3 records are listed. In quotes, line breaks from the source are flattened to spaces, and nothing else is changed.

Lineage detection: a record belongs to a template family if its original file contains that family's signature sentence. The families are:

- **frontend-design verbatim**: `sharp accents outperform|converge on common choices|gradient meshes, noise textures|cookie-cutter design`, which are sentences from Anthropic's frontend-design skill and the agents built from it.
- **impeccable**: `cyan-on-dark|gray text on colored`.
- **taste-skill**: `LILA|AI Purple/Blue`.
- **ui-ux-pro-max**: `No Emoji as Structural|ui-ux-pro-max`.
- **weight-extremes**: `200 vs 800`.

## 1. Top recurring themes (ordered by distinct owners)

### 1.1 Ban the "AI palette": purple/blue gradients, purple on white, neon glow
Do not reach for purple/violet/indigo gradients, purple on white, cyan on dark or neon glows. Models default to these, so they mark the output as generated.
- Counts: 43 records, 41 owners. Agents: 22 records, 22 owners. Skills: 21 records, 19 owners.
- Concentrates in: production-code (32 of 43, 2.2x) and redesign-existing (9, 1.8x). These are mostly greenfield-build roles.
- Quotes:
  - "NEVER purple gradient on white (the #1 AI slop indicator)." (c00024)
  - "Purple/indigo everything | Models default to visually "safe" palettes, making every app look identical | Use the project's actual color palette" (s0035)
  - "FORBIDDEN COLORS: purple (#800080-#9370DB), violet (#8B00FF-#EE82EE), indigo (#4B0082-#6610F2), fuchsia (#FF00FF-#FF77FF), blue-purple gradients" (s0031)

### 1.2 Ban default typefaces (Inter, Roboto, Arial, system-ui, Space Grotesk) and pick a characterful one
Display type should be a deliberate and distinctive choice, not the default family.
- Counts: 33 records, 33 owners. Agents: 22 records, 22 owners. Skills: 11 records, 11 owners.
- Concentrates in: production-code (26 of 33, 2.3x) and design-tokens (18, 1.4x).
- Quotes:
  - "NEVER as display fonts: Inter, Roboto, Open Sans, Lato, Arial, Helvetica, system-ui. That's the AI-default look." (c00024)
  - "Avoid generic fonts (especially Arial, Roboto, Inter, and system defaults) unless the project or user mandates them." (c00072)
  - "Choose your typefaces deliberately, not the default families you would reach for on any other project, and set a clear type scale following the default guidance of The Elements of Typographic Style" (s0037)

### 1.3 Every visual value comes from a token; no raw hex, px or arbitrary values
Colours, spacing, radii and type are referenced through the project's tokens or theme, and a raw value counts as a defect.
- Counts: 24 records, 24 owners. Agents: 22 records, 22 owners. Skills: 2 records, 2 owners. This is agent-heavy.
- Concentrates in: revise-existing (16 of 24, 1.6x), design-tokens (13, 1.4x) and production-code (11, 1.35x).
- Quotes:
  - "Tokens are law. Every visual value references a token. Raw hex codes, arbitrary pixel values, and magic numbers are bugs." (c00270)
  - "no raw hex/px in mockup html under any circumstance" (c00112)
  - "`bg-red-500` → `bg-destructive` - `text-gray-700` → `text-muted-foreground` - `bg-orange-400` → `bg-accent`" (c00419)

### 1.4 Use a defined type scale with few sizes and weights
Use a real scale, whether a modular ratio or fixed steps, and cap the number of distinct sizes and weights on a screen.
- Counts: 26 records, 24 owners. Agents: 20 records, 18 owners. Skills: 6 records, 6 owners.
- Concentrates in: design-tokens (18 of 26, 1.75x) and design-system-docs (14, 1.45x).
- Quotes:
  - "Flag if >4 font sizes or >2 font weights in use" (c00133)
  - "Real scale (e.g. 12/14/16/20/28/40), not everything 16px." (s0010)
  - "If an existing size does not land exactly on a step, snap it to the closest step below, taking both the size and its paired line height." (s0049)

### 1.5 Restrained palette: a dominant colour plus one sparing accent (60/30/10)
Neutral-dominant surfaces with one accent kept for the few elements that must stand out, instead of an evenly spread multi-hue palette.
- Counts: 24 records, 23 owners. Agents: 15 records, 14 owners. Skills: 9 records, 9 owners.
- Concentrates in: redesign-existing (6 of 24, 2.1x) and production-code (17, 2.1x).
- Quotes:
  - "Dominant colors with sharp accents outperform timid, evenly-distributed palettes." (c00025)
  - "Neutral-dominant, accent-sparing — the 60-30-10 rule. ~60% primary/neutral surface, ~30% secondary, ~10% accent reserved for elements that must stand out (CTAs)." (s0032)
  - "Accent reserved-for list is empty or says "all interactive elements"" (c00102, a failure condition)

### 1.6 Named AI-template tells beyond font and colour
Card grids of equal items, the same rounded card with a soft shadow on every surface, glassmorphism, blobs and orbs, "SECTION 01" labels, perfectly centred layouts and em-dashes are all named as things that make output read as generated.
- Counts: 24 records, 22 owners. Agents: 14 records, 13 owners. Skills: 10 records, 9 owners.
- Concentrates in: production-code (15 of 24, 1.8x). The theme also appears in review and written-critique at about baseline.
- Quotes:
  - "Avoid generic AI defaults: interchangeable SaaS card grids, card wrappers without semantic or interactive purpose, pill clusters, purple-on-white or dark-mode bias, gratuitous gradients/glassmorphism, excessive rounding, ornamental icons, filler copy" (c00449)
  - "Defaulting to Inter/system-ui with no intentional pairing - Indigo/purple gradient hero sections and buttons as a fallback - Every surface using the same `rounded-lg` card with a soft shadow - Emoji used as the only iconography" (c00424)
  - "Everything is the same weight and size, so the eye has nowhere to land. Three equal cards in a row, four equal stats, a page of identical grey boxes." (c00532)

### 1.7 A consistent radius system (scale, one shape language, nested-radius math)
Radii come from a small scale, and one shape language is used throughout. Some roles give a formula for nested corners. Excessive or pill rounding is a named tell.
- Counts: 24 records, 20 owners. Agents: 12 records, 10 owners. Skills: 12 records, 11 owners.
- Concentrates in: html-mockup (3 of 24, 1.8x), prototype (5, 1.65x) and design-tokens (15, 1.6x).
- Quotes:
  - "全局统一使用一种风格：要么偏方（radius-sm/md），要么偏圆（radius-lg/xl），不要混用" (c00701). In English: use one style everywhere, either squarer (radius-sm/md) or rounder (radius-lg/xl), and do not mix them.
  - "Rounded everything (rounded-2xl) | Maximum rounding signals "friendly" but ignores the hierarchy of corner radii in real designs | Consistent border-radius from the design system" (s0035)
  - "Outer radius = inner radius + padding. Mismatched radii on nested elements is the most common thing that makes interfaces feel off." (s0102)

### 1.8 Stay inside the existing visual language and brand
Use the project's palette, framework classes and design language. Do not invent new ones or drift from a brand document.
- Counts: 21 records, 19 owners. Agents: 17 records, 15 owners. Skills: 4 records, 4 owners.
- Concentrates in: revise-existing (12 of 21, 1.4x) and production-code (10, 1.4x).
- Quotes:
  - "Preserve an established visual language. For greenfield UI, use a cohesive token system, strong hierarchy, deliberate typography, disciplined spacing, one clear accent, restrained depth, real or context-specific product copy, and at most one memorable visual idea per view." (c00449)
  - "Avoid inventing new CSS classes if existing framework/app classes cover the need." (c00311)
  - "Write every fix in the project's styling system, and use the exact values below rather than familiar-looking equivalents." (s0069)

### 1.9 Readability baseline: body size, line height, line length, text contrast
Body text is at least 16px (sometimes 14px), line height is about 1.5, lines run 45–75 characters, and grey text is not placed on coloured backgrounds.
- Counts: 20 records, 18 owners. Agents: 9 records, 9 owners. Skills: 11 records, 10 owners.
- Concentrates in: redesign-existing (5 of 20, 2.1x), design-tokens (11, 1.4x) and revise-existing (11, 1.35x).
- Quotes:
  - "Line length 50–75 characters. Longer is hard to track; too short forces choppy eye movement." (s0033)
  - "Start long-form body text at `16px`, the browser default. Move off it only for a reason you can name" (s0069)
  - "DON'T: Use gray text on colored backgrounds—it looks washed out; use a shade of the background color instead" (s0002)
- Contradiction inside the theme: "the default UI size in SaaS is **13px or 14px**, NOT 16px. Stripe is 14px. Linear is 13px. Vercel is 14px." (s0045), and verifywise-ai's house spec "Body default is `13px/400/1.5`." (c00603). The 16px floor holds for reading content but not for dense product UI.

### 1.10 Support both light and dark themes, and check each one
Every colour must work in both modes. Dark mode is designed separately, not produced by inverting light mode, and each mode is checked on its own.
- Counts: 16 records, 16 owners. Agents: 8 records, 8 owners. Skills: 8 records, 8 owners.
- Concentrates in: design-tokens (10 of 16, 1.6x) and design-system-docs (9, 1.5x).
- Quotes:
  - "Check light and dark themes separately; the same alpha rarely works for both." (s0021)
  - "Define semantic colors (purpose, not literal hue) so they adapt across modes; don't just invert light mode." (s0032)
  - "Dark mode is mandatory — every color must work in both modes" (s0060)

### 1.11 The palette is a system of semantic roles, not a set of swatches
Neutral ramp, surface/text/border roles and semantic success/warning/error colours are derived from a base scale, and functional colours are kept distinct from the brand colour.
- Counts: 14 records, 14 owners. Agents: 7 records, 7 owners. Skills: 7 records, 7 owners.
- Concentrates in: design-tokens (11 of 14, 2.0x) and design-system-docs (8, 1.5x).
- Quotes:
  - "Tokens are a scale, not a swatch. One accent color, one surface, one border, one text, one muted — semantic tokens (success/warning/error/info) are derived from that scale, not invented separately." (c00321)
  - "All colors trace back to primitives: foreground hierarchy, background elevation, border hierarchy, brand, semantic (destructive / warning / success). No random hex values." (c00186)
  - "Keep functional colors distinct from brand. If the brand color is a bright red near the error red, define a separate error family so users don't confuse branding with feedback." (s0032)

### 1.12 Spacing on a 4px/8px grid
All margins, padding and rhythm are multiples of a 4 or 8 base unit, and off-grid values count as drift.
- Counts: 14 records, 14 owners. Agents: 14 records, 14 owners. Skills: 0. No skill in the set states it.
- Concentrates in: design-system-docs (8 of 14, 1.5x) and wireframe (4, 1.45x).
- Quotes:
  - "Adhere strictly to 4dp/8dp grid multipliers for all margins and padding." (c00628)
  - "Inconsistent Spacing - mieszanie 12px, 13px, 14px, 15px zamiast trzymania sie gridu 4px lub 8px." (c00697). In English: inconsistent spacing, mixing 12px, 13px, 14px and 15px instead of sticking to a 4px or 8px grid.
  - "grid adherence: X% (8px) / Y% (4px) / Z% off-grid" (c00314)

### 1.13 State exact values; do not approximate or describe vaguely
Give hex codes, units, font names and exact letter-spacing. Map vague adjectives to concrete values, and do not round values taken from a spec.
- Counts: 16 records, 14 owners. Agents: 7 records, 6 owners. Skills: 9 records, 8 owners.
- Concentrates in: html-mockup (3 of 16, 2.7x) and design-tokens (13, 2.1x).
- Quotes:
  - "严格执行规范中的具体数值，不要自由发挥或用近似值替代。如果规范中写的是 `rgba(0,0,0,0.95)` 就不要用 `#000000`，如果字间距是 `-2.125px` 就不要四舍五入。" (s0030). In English: apply the spec's exact values strictly, with no improvising or approximating. If the spec says `rgba(0,0,0,0.95)`, do not use `#000000`, and if the letter-spacing is `-2.125px`, do not round it.
  - "Every duration, curve, scale and blur below is a specific value, not a range to approximate." (s0070)
  - "Color: describe the palette as 4–6 named hex values." (c00114; the same line appears in s0004 and s0037)

### 1.14 Use one SVG icon set, never emoji as icons
Use a single vector icon family (Lucide, Heroicons, Phosphor) and never use emoji as structural or navigation icons.
- Counts: 14 records, 13 owners. Agents: 10 records, 9 owners. Skills: 4 records, 4 owners.
- Concentrates in: design-tokens (12 of 14, 2.2x) and design-system-docs (9, 1.7x).
- Quotes:
  - "No Emoji as Structural Icons | Use vector-based icons... | Using emojis (🎨 🚀 ⚙️) for navigation, settings, or system controls. | Emojis are font-dependent, inconsistent across platforms, and cannot be controlled via design tokens." (s0084)
  - "使用一致的 icon set（推薦 Lucide、Phosphor、Heroicons），禁止用 emoji 當 icon" (c00391). In English: use one consistent icon set (Lucide, Phosphor or Heroicons are recommended), and do not use emoji as icons.
  - "No default AI-purple glow, no pure `#000`/`#fff`. One icon family per project." (c00646)

### 1.15 An intentional font pairing: display face plus body face, at most 2–3 families
Pair a characterful display or heading face with a refined body face, and give monospace a defined role.
- Counts: 12 records, 12 owners. Agents: 8 records, 8 owners. Skills: 4 records, 4 owners.
- Concentrates in: production-code (7 of 12, 1.7x) and design-tokens (7, 1.5x).
- Quotes:
  - "Use an intentional pairing of at most two typefaces (e.g., a display/heading face and a body face) rather than relying solely on the Tailwind default sans stack" (c00424)
  - "Type pairing: display in editorial serif (Instrument Serif / Newsreader / Lyon), body in grotesque (Geist / Switzer / SF Pro), monospace for meta/keystrokes (Geist Mono / JetBrains Mono)." (s0089)
  - "In `.tsx`, flag headings (`<h1>`–`<h4>`) without `font-display` and code blocks (`<pre>`, `<code>` styled blocks) without `font-mono`." (c00419)

### Below the cut (in `assign.json` as `minor:`)
- Concrete UI copy and data (12 records, 12 owners): no generic CTA labels, no em-dash, realistic sample rows. This belongs to the writer role more than to this dimension.
- Hierarchy by strong contrast (10 records, 10 owners): weight extremes, 3x size jumps, a heading-to-body ratio of at least 2:1.
- Restrained depth and elevation (11 records, 10 owners).
- Atmosphere and effects (10 records, 10 owners): gradient meshes, grain, glass. This contradicts 1.6 and the depth-restraint theme.
- No pure white or black (8 records, 8 owners): contradicted by s0060 "skip cream or off-white panels".
- Touch targets of 44px (4 records, 4 owners, but 139 repo copies through c00002 and c00003).
- Perceptual colour spaces, OKLCH/oklab (4 records, 4 owners).

## 2. Lineage warnings

- **The two biggest themes (1.1 and 1.2) are one doctrine spread by copying.** 16 of the 41 owners in 1.1 and 16 of the 33 owners in 1.2 carry verbatim sentences from the frontend-design lineage. Adding impeccable (5 owners in 1.1, 2 in 1.2), taste-skill (3 and 2) and ui-ux-pro-max leaves only **20 of 41** owners (1.1) and **16 of 33** owners (1.2) outside every detected family. Even the "independent" ones repeat the same short list (Inter/Roboto/Arial, purple gradient on white, Space Grotesk). The phrase "purple gradient(s) on white" appears in the files of 23 distinct owners, and "Space Grotesk" in 23. After discounting, both are still the most widespread themes, but they measure how far one meme travelled, not independent agreement.
- **Theme 1.5 (dominant plus accent)**: 8 of 23 owners carry the frontend-design sentence "Dominant colors with sharp accents outperform timid, evenly-distributed palettes." verbatim. 12 owners sit outside all families. Those include the 60/30/10 phrasings (gsd-build, HermeticOrmus, Uxcel-Lab, fengshao1227), which form an older and independent convention.
- **Theme 1.14 (SVG not emoji)**: 7 of 13 owners carry ui-ux-pro-max text ("No Emoji as Structural Icons", "Use SVG icons (Heroicons, Lucide), not emojis"). Only 6 owners are independent.
- **Hierarchy by strong contrast (minor)**: the "200 vs 800 / 3x size jump" text is one sentence family (poshan0126 c00024, zebbern c00055, coco-research c00231, and in the files of davila7 and Brahiamm56). 3 of the theme's 10 owners use it.
- **verifywise-ai** contributes 4–5 records (c00600, c00601, c00603, c00605), which are one product's house spec (4px/2px radius, 13px body, #13715B). It is counted as one owner, but it inflates 1.7 (3 records) and 1.14 (2 records) at the record level.
- **jakubkrehel** has four skills (s0066, s0067, s0069, s0070), and samuelclay's s0102 repeats its lines verbatim ("Use `font-variant-numeric: tabular-nums` for any dynamically updating numbers to prevent layout shift."). Most of the sharp OKLCH, hue-tolerance and weight-floor rules come from this one voice.
- **"Color: describe the palette as 4–6 named hex values."** is one template in anthropics s0037, HKUDS s0004 and ye-lynn-htet c00114. It accounts for 3 of the 14 owners in 1.13.
- **Leonxlnx** has 3 skills (s0005, s0006, s0018), and google-labs-code s0058 copies its "AI Purple/Blue ... BANNED" line almost verbatim.
- **Repo copies inflate reach, not agreement.** 1.12 (spacing grid) has a copies sum of 121, but c00003 alone has 62 copies. The Vietnamese-font rule (c00001, 77 copies; c00028) is a project leak from one kit (ClaudeKit: mrgoonie and withkynam), not a design principle.
- **gsd-build** (c00102 and c00133, a checker and an auditor from one project) appears twice in 1.4 and 1.5.

## 3. Sharp but rare (1–2 owners, unusually precise or operational)

1. "Nested radius formula. When a shape sits inside another shape and the gap between them is less than 32px: inner radius = outer radius − gap" (s0049). s0102 states the same rule as "Outer radius = inner radius + padding".
2. "Type rhythm: line-height should resolve to a multiple of the base unit (typically 4px or 8px). Off-rhythm → `RHYTHM_BREAK`." (c00638). This is a named, machine-checkable finding code.
3. "grid adherence: X% (8px) / Y% (4px) / Z% off-grid" (c00314). The audit output is a measurement, not an adjective.
4. "Use a color for one purpose across the whole interface, treating anything within `15°` of hue as the same color." (s0067)
5. "Below `18px`, stay at weight `400` or heavier. Weights under `300` are display-only at `28px`+; they disappear at text sizes." (s0069)
6. "Higher surfaces mix slightly more white. Turn shadows off: if elevation is still legible, the surface ramp works." (c00657). This is an operational test for depth.
7. "Forbidden anywhere in `.tsx` or `.css` other than inside a comment. Suggest the closest semantic token (`bg-background`, `text-foreground`, `bg-primary`...)" (c00419). Together with "Pattern: `rounded-\[` Forbidden. Suggest one of `rounded-sm | rounded-md | rounded-lg | rounded-xl`." (c00419), this is effectively a lint rule written as prose.
8. "Check light and dark themes separately; the same alpha rarely works for both." (s0021)
9. "The H1 MUST NEVER exceed 2 to 3 lines. 4, 5, or 6 lines is a catastrophic failure." (s0018). It can only be verified by rendering at real widths.
10. "Alarms require three independent cues: color + shape + text." (s0083)

## 4. Bearing on the proposed designer

**(1) Start from the existing product and follow its design system.** Supported, and this dimension sharpens it. Token discipline (1.3, 24 owners) and staying in the existing language (1.8, 19 owners) are among the most independent themes: almost none of their owners belong to a template family (1 of 24 and 1 of 19). There is also a conflict. The largest themes (1.1, 1.2, 1.6) are written for greenfield builds. They lift in production-code at 1.8–2.3x, and many are absolute ("FORBIDDEN FONTS: Inter, Roboto, Arial, Helvetica, system-ui, -apple-system", s0031). Applied to a product whose brand uses Inter or purple, they would override the design system. The better sources already scope them: "unless the project or user mandates them" (c00072), "Preserve an established visual language. For greenfield UI, ..." (c00449), and "Use the project's actual color palette" (s0035). This supports the proposal's order: the existing system comes first, and anti-generic doctrine applies only when there is no system or the brief asks for a new direction. The role should state that precedence in a single line and leave the doctrine out.

**(2) Name the user and task, then commit to one direction or give variants.** Weakly touched. In this dimension "commit" appears as one-strategy rules: "Depth: pick one strategy (borders-only / subtle shadows / layered / surface shifts) and commit" (c00186), and c00701's rule of using one style everywhere, either squarer or rounder, without mixing (1.7). The themes also contradict each other: atmosphere effects against restrained depth, cream canvases (s0044, s0089) against "skip cream or off-white panels" (s0060), and glassmorphism recommended (c00109, c00384) against glassmorphism banned (s0044, c00449). Taste rules depend on the chosen direction, so they cannot be universal role text. The loaded skill has to be picked after the direction is set. User and task hardly appear here, apart from colour psychology per industry (c00095).

**(3) Render and look before reporting.** Supported, and this dimension shows where it is needed. Only 50 of the 204 visual-craft records (25%) have `renders_and_looks`. Among those that state the anti-AI palette rules (1.1) it is 11 of 43, and among the anti-generic font rules (1.2) it is 6 of 33. Most visual doctrine is issued as rules to follow, not results to verify. The rules fall into two kinds. Some can be checked statically without a browser: raw hex, arbitrary radius classes, font-size and weight counts, grid adherence, nested-radius math and contrast ratios (sharp items 2, 3 and 7; c00133 "Flag if >4 font sizes or >2 font weights in use"). Others can only be checked by rendering: H1 line count (s0018), "The gradient is visible at normal zoom but barely noticeable when scanning." (s0021), dark-mode alpha (s0021), the shadow-off test (c00657), and "the eye has nowhere to land" (c00532). The proposal should also say what happens when no browser is available: static checks still run, render-only claims are reported as unverified, and the role must not state them as fact.

**(4) Cover states, responsive behaviour and an accessibility baseline.** Supported, with one addition and one caution. The addition is theming: 16 owners require both light and dark modes and require each to be checked separately. That is as common as many a11y items here and is missing from the proposal's list. It could read "the themes the product supports". Touch targets of 44px and body text of at least 16px on mobile (to prevent iOS zoom, s0074, s0116) also belong to the baseline. The caution is that baseline numbers conflict with real systems (16px vs 13–14px SaaS body, s0045 and c00603). The role should require that the baseline be checked, and take the numbers from the design system or a rule file, not from the role text.

**(5) Boundary: the designer prototypes and the implementer integrates.** This dimension adds a handoff argument. Prototypes should use the project's tokens too ("no raw hex/px in mockup html under any circumstance", c00112), because a token-true prototype is what makes the implementer's integration cheap. Otherwise neutral.

**(6) Return what was made, the direction, screenshots, deviations and open questions, without self-judgement.** Deviations are supported by "Call out token misuse, spacing drift, typography drift, and asset substitutions." (c00486) and by mateaix's font-substitution rule (s0081). The report should list substituted fonts and every raw value it introduced. On self-judgement: many visual-craft quotes are self-review checklists ("Is there a consistent type scale (e.g., Major Third 1.25)?", c00362; "Are there too many font sizes (more than 4-5 distinct sizes = messy)?", c00613). Under the proposal these belong with the separate reviewer or with a check tool, not in the designer's report.

**Placement verdict for visual craft**

- **Role text:** none of the doctrine. It keeps only three contract lines already implied by (1), (3) and (6): the existing system and tokens take precedence over any taste guidance; the report must separate what was rendered and seen from what was only read in code; the report must name deviations and substitutions.
- **Skill or rule file:** palette, type, radius, depth, font pairing, anti-generic lists, dark-mode rules and readability numbers. These are conditional on the product and the direction, and they contradict each other across sources (cream vs no cream, 16 vs 13px, atmosphere vs restraint, glass vs no glass). That is the evidence that they must be chosen per project and not fixed in the role. A project's own rule file should override the house skill.
- **Tool or check:** token discipline (raw hex, px and arbitrary Tailwind values), size and weight count, grid adherence, radius scale and the nested-radius formula, contrast ratio, touch-target size, line length and H1 line count. The corpus already writes these as lint-shaped prose (c00419, c00314, c00638, c00133). A script checks them more reliably than a prompt.
- **Nowhere, as a general rule:** named-font blacklists as universal law (Inter/Space Grotesk bans spread mostly by copying one lineage, see section 2), project leaks (the Vietnamese character set in c00001 and c00028, the KZTEK palette in c00254, "Exact HubSpot color scheme" in c00365), and the em-dash ban (c00646, c00650, s0005), which belongs to the writer role's domain, not the designer's.
