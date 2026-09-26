# Direction and taste: recurring instruction themes

Source: `claims/direction-taste.jsonl`, 260 quotes from 157 design-role records (106 agents, 51 skills) across 136 distinct owners. All 260 lines were read. Theme membership is assigned per quote and rolled up to records; one record can sit in several themes. The id lists are in `direction-taste.assign.json`, and every count below was computed from that file joined with the claims file. 144 of 157 records fall in at least one theme; the 13 left over are one-off remarks (several of them appear under "Sharp but rare").

Counting conventions: "owners" is the part of `repo` before `/`. "Non-FD owners" excludes the frontend-design template family defined under "Lineage warnings" (15 records, 15 different owners, so owner counting alone does not deflate it). The baseline for concentration is the 157 records in this dimension: spec-or-handoff 51%, production-code 46%, design-tokens 46%, written-critique 44%, design-system-docs 34%, redesign-existing 17%, html-mockup 11%, prototype 10%, wireframe 10%; modes create 87%, review 57%, revise-existing 45%; skills are 32% of records.

## 1. Top recurring themes (ordered by distinct owners)

### 1. Commit to one clear direction before building; do not hedge or blend
The role picks a single, specific aesthetic direction up front and executes it consistently instead of an averaged middle ground.
- Counts: 30 records, 29 owners (15 non-FD owners). Agents 18 records / 18 owners; skills 12 / 12. 14 of the 30 records are the FD family.
- Concentration: production-code 77% (vs 46%), redesign-existing 27% (vs 17%); under-represented in spec-or-handoff (33%) and written-critique (30%). A build-mode theme.
- Quotes:
  - "Pick one design principle. Don't mix randomly." (c00024)
  - "Do not blend many archetypes; blended taste turns generic quickly." (s0025)
  - "State the chosen direction (or confirm you are following the existing one already established in `src/frontend`) before generating markup. Do not silently mix directions across pages within the same app." (c00424)

### 2. Derive the direction from the product, domain and audience, not from a house style or trend
Style choices are mapped to what the product is and who uses it; operational and high-trust products get restraint, expressive briefs get expression.
- Counts: 28 records, 27 owners (25 non-FD). Agents 18 / 18; skills 10 / 9.
- Concentration: wireframe 18% (vs 10%), design-tokens 54%, production-code 54%; spread across create and review.
- Quotes:
  - "This default reads well for editorial, hospitality, portfolio, and brand briefs — but is inappropriate for dashboards, dev tools, fintech, healthcare, enterprise apps, and data-dense UIs." (c00042)
  - "For operational SaaS and internal tools, prefer restrained density, scannable tables, calm surfaces, and clear controls." (s0103)
  - "A prototype for a field tool, an editorial workflow, and a financial approval should not feel like the same product." (s0093)

### 3. General anti-generic stance: the result must not read as templated or AI-made
A stated goal or test, without a concrete list: "could a default prompt have produced this?"
- Counts: 25 records, 24 owners (24 non-FD). Agents 16 / 15; skills 9 / 9. The only owner with two records is semaj90.
- Concentration: close to baseline on every output; redesign-existing slightly high (24%). It is a stance attached to every kind of role, not to one output.
- Quotes:
  - "The \"AI slop\" test: If you removed the logo, could you tell this from a default Next.js template? If yes, you haven't designed anything yet." (c00322)
  - "If another AI, given a similar prompt, would produce substantially the same output — you have failed." (s0061)
  - "Treat visual tells as review prompts, not blanket bans on cards, fonts, or branding. Fix the observable problem and respect the user's brief and existing design system." (s0050, the counter-voice inside this theme)

### 4. Named reference benchmarks, and borrow their system rather than their surface
Roles name studios, masters, brands or inspiration sites as the bar, and several add that the pattern should be extracted, not copied.
- Counts: 21 records, 21 owners (21 non-FD). Agents 17 / 17; skills 4 / 4. Includes c00001 (mrgoonie, copied into 77 repos), so copies inflate its reach far more than its owner count.
- Concentration: review 67% (vs 57%), redesign-existing 29%, written-critique 52%.
- Quotes:
  - "Your aesthetic north star is the work of studios like Linear, Stripe, Vercel, and Raycast: restrained palettes, confident typography, purposeful motion, generous whitespace." (c00322)
  - "you don't just copy surface-level aesthetics — you extract the underlying *system*: the spacing scale, typography hierarchy, color relationships, motion language, and interaction patterns" (c00334)
  - "Do not use named brands as imitation. Borrow controllable qualities such as density, typography rhythm, interaction attitude, and role structure." (s0025)

### 5. User needs outrank aesthetics; describe choices in terms of user behaviour
Taste is subordinate to the user's task; the role pulls discussions back from portfolio polish to what users will do.
- Counts: 22 records, 19 owners (19 non-FD). Agents 20 / 17; skills 2 / 2. davepoon contributes 4 records (one persona family).
- Concentration: written-critique 82% (vs 44%), wireframe 41% (vs 10%), review 82% (vs 57%); design-tokens only 14%. This is the critic's and UX-generalist's theme, almost absent from build-oriented skills.
- Quotes:
  - "Describe design decisions in terms of user behavior, not visual preference." (c00198)
  - "Your goal is not to make the interface look nicer. Your goal is to make the product more trustworthy, more legible, and easier to use" (c00433)
  - "The goal is not \"prettier UI\"; the goal is **fewer doubts, fewer fields, fewer dead ends, and faster confident action**." (s0014)

### 6. Pick from a named catalogue of styles, archetypes or packs
The role is handed a menu (brutalist, editorial, retro-futuristic, glassmorphic, starter kits, design-system packs) and chooses one entry.
- Counts: 21 records, 19 owners (11 non-FD). Agents 12 / 11; skills 9 / 9. 8 of 21 records are FD; Orkas-AI and curiositech contribute 2 each.
- Concentration: production-code 71%, design-tokens 62%, create 90%; review only 29%.
- Quotes:
  - "Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc." (c00025; the same string appears in s0000, s0038, s0041)
  - "Pick the closest starter kit from starter-kits/ (glass-on-beige/, flat-modern/, or editorial-serif/) per starter-kits/README.md." (c00335)
  - "Select ONE archetype per project. Apply consistently." (s0020)

### 7. A named blacklist of AI-default tells
Concrete looks to avoid: purple gradients, Inter/Roboto/Space Grotesk, centered hero with three feature cards, cream/serif/terracotta, glassmorphism everywhere, placeholder names and copy clichés.
- Counts: 19 records, 19 owners (16 non-FD). Agents 10 / 10; skills 9 / 9. 3 FD records; 2 records (c00114, s0004) share the "three looks" text.
- Concentration: production-code 74%, html-mockup 16%; spec-or-handoff and design-system-docs low. A generation-time list for roles that write UI code.
- Quotes:
  - "Do not default to: AI-purple gradients, centered hero over dark mesh, three equal feature cards, generic glassmorphism on everything, infinite-loop micro-animations everywhere, Inter + slate-900." (s0005)
  - "AI-generated design right now clusters around three looks: (1) a warm cream background (near #F4F1EA) with a high-contrast serif display and a terracotta accent; (2) a near-black background with a single bright acid-green or vermilion accent; (3) a broadsheet-style layout with hairline rules, zero border-radius, and dense newspaper-like columns." (c00114; also s0004)
  - "Trained eye for generic AI-generated patterns — purple gradients, 3-column icon grids, centered-everything layouts, uniform border-radius, decorative blobs, generic hero copy. Flag immediately and suggest product-specific alternatives." (c00256)

### 8. Give a reason for every choice: principle or evidence, not personal preference
- Counts: 16 records, 16 owners (16 non-FD). Agents 14 / 14; skills 2 / 2.
- Concentration: spec-or-handoff 75%, written-critique 69%, design-system-docs 50%; production-code 31%. The written-output theme.
- Quotes:
  - "A design decision without a stated reason is a preference, and preferences do not survive review." (c00380)
  - "Frame every design decision as SAFE (category baseline) or CREATIVE RISK (deliberate departure). Risks must articulate: what you gain, what you risk, why it works for THIS product." (c00256)
  - "Propose design solutions with clear rationale and alternatives considered" (c00022)

### 9. Name the direction concretely; "modern and clean" is not a direction
The direction is written down as specific words, fonts and hex values, specific enough that another designer would reproduce it.
- Counts: 14 records, 14 owners (12 non-FD). Agents 12 / 12; skills 2 / 2.
- Concentration: review 71%, revise-existing 57%; otherwise near baseline.
- Quotes:
  - "Generic negations (\"don't use cream\", \"make it minimal\") shift the default to another fixed palette rather than producing variety. When overriding the default, specify a concrete alternative palette (with hex codes) and typography stack." (c00042)
  - "it must be specific enough that two different designers would produce recognizably similar work" (c00139)
  - "Name it precisely: dense editorial, raw terminal, ink-on-paper, brutalist grid, warm analog. \"Clean and modern\" is not a direction." (s0112)

### 10. Match the existing product and familiar patterns over novelty
- Counts: 14 records, 13 owners (13 non-FD). Agents 9 / 9; skills 5 / 4 (expo has 2). slabgorb and slabgorb-org are counted as two owners but are very likely one author.
- Concentration: redesign-existing 29%, wireframe 21%, spec-or-handoff 64%, revise-existing 57%.
- Quotes:
  - "Every new pattern you introduce is cognitive load. Every deviation from the existing system is a moment of confusion." (c00117)
  - "Preserve the product's intent before preserving its current pixels." (s0109)
  - "Follow each platform's own design language: Apple Human Interface Guidelines on iOS, Material Design 3 on Android. Never dress one platform in the other's uniform - no FAB or ripple in iOS layouts; no hand-built iOS chrome (back-chevrons, large-title text, iOS-styled switches) on Android." (s0051)

### 11. Restraint: a tight palette, fewer levers, remove one thing
- Counts: 13 records, 12 owners (10 non-FD). Agents 7 / 7; skills 6 / 5 (Uxcel-Lab has 2).
- Concentration: revise-existing 77% (vs 45%), design-tokens 62%, production-code 62%.
- Quotes:
  - "**Restraint** — a tight palette and a single consistent scale beat a sprawling one. Don't invent tokens nobody will use." (c00290)
  - "The brand color appears in <5% of the pixels and earns its weight by marking only what's interactive or active." (s0045)
  - "Stacking every persuasion lever — perks + urgency + pop-ups + sticky chat — is the failure mode; it reads as a hard sell and erodes trust." (s0034)

### 12. Offer several materially distinct directions with trade-offs
- Counts: 12 records, 12 owners (12 non-FD). Agents 9 / 9; skills 3 / 3.
- Concentration: spec-or-handoff 100%, prototype 33% (vs 10%), html-mockup 25% (vs 11%), create 100%. The exploration-output theme.
- Quotes:
  - "When the brief is open-ended, offer two contrasting directions (e.g. restrained editorial vs. bold playful) with clear trade-offs, then converge" (c00053)
  - "Present at most three materially different directions when a choice matters." (c00541)
  - "Two variations that differ only in tint = one wasted slot." (s0099)
- Counter-voice: "Prefer one defensible direction over a menu of weak variations unless the user asks to explore." (s0109)

### 13. One signature element; spend the boldness in one place
- Counts: 11 records, 11 owners (6 non-FD). Agents 8 / 8; skills 3 / 3. 5 of 11 are FD ("Differentiation: the ONE memorable thing").
- Concentration: production-code 64%, review 64%.
- Quotes:
  - "Spend your boldness in one place. Let the signature element be the one memorable thing, keep everything around it quiet and disciplined" (s0004)
  - "Give the design one product-specific signature device that helps the workflow." (s0023)
  - "Un elemento con carácter por pantalla, obligatorio.** Un dato bien presentado tiene más carácter que una ilustración; \"usaremos la tarjeta estándar\" es ausencia de decisión." (c00191; "one element with character per screen, mandatory. A well-presented data point has more character than an illustration; 'we'll use the standard card' is an absence of decision")

### 14. Vary across generations; never reuse the same look
- Counts: 8 records, 8 owners (4 non-FD). Agents 4 / 4; skills 4 / 4. Half is FD ("NEVER converge on common choices ... across generations").
- Concentration: html-mockup 38%, production-code 75%, create 100%, review 25%.
- Quotes:
  - "Never repeat yourself across projects. If your last landing page was brutalist, the next one is not also brutalist." (c00139)
  - "You are forbidden from defaulting to the same UI twice." (s0018)
  - "Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations." (c00025)

### 15. Get the direction from the user before designing
References, an anti-reference, or a confirmed choice come before any generation.
- Counts: 6 records, 6 owners (6 non-FD). Agents 5 / 5; skills 1 / 1.
- Concentration: html-mockup 50% (vs 11%), spec-or-handoff 83%, create 100%.
- Quotes:
  - "Dirección visual primero: sin ella aprobada, no dibujas." (c00191; "visual direction first: without it approved, you do not draw")
  - "Never invent the aesthetic — extract it via the interview or from explicit references." (c00335)
  - "AskUserQuestion for direction choices (layout style, component pattern), never assume" (c00112)

## 2. Lineage warnings

- **frontend-design (FD) family.** 15 records, each under a different owner: c00025, c00029, c00042, c00072, c00077, c00116, c00139, c00158, c00436, c00608, s0000, s0038, s0041, s0052, s0116. Membership was computed from the file text: the record contains "brutally minimal", "Purpose ... Tone ... Constraints ... Differentiation", "ONE thing someone will remember" or "NEVER converge on common choices". These are copies or adaptations of the published frontend-design skill text. Because every copy sits under a new owner, the owner count does not deflate them. Impact by theme: commit-one-direction falls from 29 owners to 15 once FD is removed; style-catalogue from 19 to 11; signature-element from 11 to 6; vary-across-generations from 8 to 4. The "Pick an extreme: brutally minimal, maximalist chaos, ..." string alone appears verbatim in c00025, s0000, s0038, s0041 and, lightly edited, in c00072, c00116, c00436, c00608. The current upstream skill (s0037, anthropics) no longer carries the extreme-catalogue; it says "make deliberate, opinionated choices about palette, typography, and layout that are specific to this brief, and take aesthetic risk if justified", so the catalogue is an older text that went on spreading after it was dropped upstream.
- **oh-my-claudecode house-style lineage.** c00042 (Yeachan-Heo), c00116 (mazenyassergithub, a fork named oh-my-claudecode) and c00158 (LimiNode, "model-specific house-style override policy") share the model-default-style framing. Themes 2 and 9 lean on c00042 for their best quotes; the idea itself has three voices at most.
- **"Three looks" text.** c00114 and s0004 carry the same cream/near-black/broadsheet paragraph and the same "spend your boldness in one place" idea: one voice, not two, in themes 7 and 13.
- **davila7 template.** c00009 and c00179 share "Commit to a cohesive aesthetic (dark mode, light mode, solarpunk, brutalist)" verbatim. Also davila7/claude-code-templates is a distribution hub (c00009 is copied into 31 repos), so its reach is not independent adoption.
- **Single-author persona sets.** davepoon (c00504-c00507) is 4 of the 22 records in user-over-aesthetics, all from one persona pack. Orkas-AI (c00517, s0023, s0024, s0025) and Leonxlnx/taste-skill (s0005, s0006, s0018) are single-author systems; they count once each by owner. The taste-skill vocabulary also recurs in s0019, s0062, s0089, s0116 (textual matches for "taste-skill" or its dials), so the blacklist in theme 7 has a second, smaller family behind it.
- **Copy counts.** c00001 (77 repos) and c00009 (31 repos) dominate `copies_in_repos` for reference-benchmarks and commit-one-direction. The owner counts above ignore copies on purpose.

## 3. Sharp but rare (1-2 owners, unusually precise or operational)

1. "Generic negations (\"don't use cream\", \"make it minimal\") shift the default to another fixed palette rather than producing variety. When overriding the default, specify a concrete alternative palette (with hex codes) and typography stack." (c00042) An observed mechanism, not a taste claim: a negative instruction moves the model to a different fixed default.
2. "Generate 6–10 genuinely divergent variations of that ONE screen. Divergence is measured by *organizing metaphor*, not paint: vary tab vs. grid→detail vs. single-scroll vs. dashboard/standings" (s0099) A testable definition of "distinct variant".
3. "❌ **Hard rule**: never recommend 3 picks from the same row — the user can't tell them apart and the contrast that makes the choice meaningful collapses." (s0013)
4. "Frame every design decision as SAFE (category baseline) or CREATIVE RISK (deliberate departure). Risks must articulate: what you gain, what you risk, why it works for THIS product." (c00256)
5. "Defaults to reject: 3 obvious choices and what replaces each" (c00186) A short output field that forces the anti-generic step into the report.
6. "Arráncale al usuario referencias reales y una antirreferencia, tres adjetivos que excluyan algo, escala tipográfica con contraste real, densidad, movimiento y qué NO va a hacer el proyecto." (c00191; "get from the user real references and one anti-reference, three adjectives that exclude something, a type scale with real contrast, density, motion, and what the project will NOT do")
7. "Source image is a chat/input homepage: reject `analytics-monitoring`, `dense-enterprise-crud`, and `project-workflow` unless the user asks to redesign it into a workspace." (c00517) A worked exclusion rule for picking a style pack from the input.
8. "The brand color appears in <5% of the pixels and earns its weight by marking only what's interactive or active." (s0045) Checkable from a render.
9. "A main region that's 80% whitespace reads as machine-generated.** Fill a dashboard with real, plausible content (stats row + activity list + a chart), not one lonely widget." (s0095) Paired with the same owner's "The work is mediocre until the render proves otherwise. The burden of proof is on the work, not on you." (c00532, plugin87): taste is judged on the rendered result.
10. "Skipping this and going straight to high-fi mockups is the field's named root cause of \"AI UI looks off\" — mockups made with invented, per-screen tokens never agree with each other." (c00321) Tokens first as a direction-quality mechanism, not an aesthetic one.

## 4. Bearing on the proposed designer

Contract point (1), start from the existing product and follow its design system. Supported by theme 10 (13 owners) and by the explicit reconciliation in c00424 ("or confirm you are following the existing one already established"), s0050 ("respect the user's brief and existing design system") and s0109 ("Preserve the product's intent before preserving its current pixels"). The larger direction-taste mass (themes 1, 3, 6, 7, 14; 74 of 157 records are in at least one of them) is written for greenfield generation and says nothing about an existing system. Several of those texts would push a designer away from the product's system if loaded unconditionally ("Vary between light and dark themes, different fonts", c00025; "You are forbidden from defaulting to the same UI twice", s0018). The proposal's "unless the brief asks for a new direction" is the right gate; the addition this dimension suggests is that when there is no existing system (s0093: "When no design system exists, create a specific direction from the subject and use case"), the role still has to state one direction rather than fall back to a default.

Contract point (2), name the user and task and commit to one direction, or produce several variants when asked. Strongly supported: themes 1 (29 owners, 15 outside FD), 2 (27 owners), 5 (19) and 9 (14). The corpus adds three things. First, the direction should be written as concrete terms (fonts, hex, density), because vague or negative directions do not move the output (c00042, s0112, c00139). Second, "several variants" needs a definition of distinct: organizing metaphor rather than paint (s0099), and at most three (c00541). Third, the corpus is split on whether to ask the user first (theme 15, 6 owners, mostly interactive roles) or to decide alone (c00449: "make one context-appropriate choice instead of returning a generic template"). For a subagent without a live user, the second is the only workable default; the choice goes into the report as an open question rather than a blocking ask.

Contract point (3), render and look before reporting. Direction-taste quotes touch this only at the edges: c00532 ("The work is mediocre until the render proves otherwise") and s0095 (80% whitespace reads as machine-generated), and several checks in themes 7 and 11 (brand colour under 5% of pixels, three equal feature cards) are only verifiable on a render. That supports keeping taste judgements tied to inspection, and it is an argument for point (3) over code-reading, but this dimension is not the main evidence for it.

Contract point (4), states, responsive, accessibility baseline. Direction-taste adds only a priority order for conflicts: "IF conflicting requirements: Prioritize accessibility > usability > platform conventions > aesthetics." (c00430) and "Golden ratio may inspire composition, but never outranks usability, accessibility, responsiveness, or clarity." (s0014). s0076 ties states to direction ("A happy-path-only prototype under-specifies the design and silently blesses missing states"). No contradiction.

Contract point (5), the designer decides and prototypes; integration goes to an implementer. Not addressed by this dimension. One relevant tension: the build-oriented themes (1, 6, 7, 14) concentrate in production-code outputs (71-77% vs 46% baseline), i.e. most taste doctrine in the wild was written for a role that also ships code. The proposal's split does not conflict with the doctrine, but a skill borrowed from this corpus will often assume it is writing production UI.

Contract point (6), report the direction and why, and do not judge its own design. Theme 8 (16 owners) supports reporting the reason for each choice, and c00256's SAFE / CREATIVE RISK framing and c00186's "Defaults to reject" are compact report fields. There is a conflict with "does not judge its own quality": the anti-generic test (theme 3, 24 owners) is by nature a self-check at generation time ("If it could have been generated by a default prompt, it is not good enough", s0112). The resolution consistent with the proposal is to let the designer apply named, checkable avoid-rules while building and list which defaults it rejected, and to leave the verdict on overall quality to the separate review. Also, theme 5 is 82% written-critique/review: the "user over aesthetics" stance mostly lives in critics, which is support for review being a separate role that brings that lens.

Where this dimension's content belongs:
- Role text: only the structural items. Commit to one stated direction (or follow the existing one) before building; derive it from product, domain and audience; write it concretely; report the direction, the reason for each consequential choice and the defaults rejected. These are process and are independent of any particular aesthetic.
- Skill or project rule file: everything aesthetic. The style catalogues (theme 6), the named AI-tell blacklists (theme 7), benchmark studios (theme 4), restraint rules (theme 11), signature-element doctrine (theme 13) and domain-to-style maps (theme 2's concrete tables). These are the parts that date (the "three looks" list is explicitly "right now"; c00699 flags that "neumorphism umarl w 2024", "neumorphism died in 2024"), vary by product, and come in competing lineages. The FD family itself shows the cost of freezing them in role text: the catalogue kept spreading after the upstream skill dropped it.
- Tool or check: the measurable subset of the blacklist and restraint rules (default font stacks such as Inter or Space Grotesk, purple-gradient heroes, three equal cards, brand-colour pixel share, whitespace share of the main region) could be a check run on the render, where one exists. Without a screenshot tool it falls back to review.
- Nowhere: "vary across generations" (theme 14). A subagent has no memory of its previous generations, the idea is carried half by one template family, and it works against point (1) inside an existing product. Also persona-voice lines ("Do not let anyone tell you how to do your job", c00343; "you can tell within ten seconds...", c00504), which carry no operational content.
