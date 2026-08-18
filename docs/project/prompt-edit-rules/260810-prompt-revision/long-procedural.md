# Stage 2 — long, heavily procedural skills

Corpus: `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/{mcp-server-dev,plugin-dev,claude-code-setup,playground}/skills/*` (6 skills) and `~/.claude/plugins/cache/claude-plugins-official/figma/2.2.91/` (12 skills + 2 workflow-skills, plus the 2.2.88 and 2.2.90 caches of the same tree).

Baseline read in full first: all six files in `stage1/`. Everything below is delta.

Word counts are `wc -w`. Code share is lines inside ``` fences over total lines. Both are reproducible with `/private/tmp/.../scratchpad/fence.py`, `agg.py`, `links2.py`, written this session.

---

## 1. Size and structure

### 1a. The assigned corpus

| Skill | SKILL.md words | SKILL.md lines / bytes | aux files | aux words | aux/SKILL | SKILL code% | scripts |
|---|---:|---:|---:|---:|---:|---:|---:|
| `build-mcp-app` | 2,539 | 392 / 19,391 | 6 | 3,951 | 1.56 | 51.1% | 0 |
| `build-mcp-server` | 1,807 | 221 / 12,084 | 8 | 5,170 | 2.86 | **5.0%** | 0 |
| `build-mcpb` | 1,058 | 199 / 7,867 | 2 | 1,509 | 1.43 | 55.5% | 0 |
| `mcp-integration` | 1,665 | 554 / 12,530 | 3 + 3 json | 4,185 | 2.51 | 30.8% | 0 |
| `claude-automation-recommender` | 1,529 | 289 / 10,995 | 5 | 4,530 | 2.96 | 27.6% | 0 |
| `playground` | 555 | 76 / 3,824 | 6 templates | 3,505 | 6.32 | 32.5% | 0 |
| `figma-create-new-file` | 580 | 80 / 3,946 | **0** | 0 | — | 8.6% | 0 |
| `figma-design-to-code` | 780 | 61 / 4,983 | **0** | 0 | — | 0.0% | 0 |
| `figma-swiftui` | 546 | 36 / 4,049 | 2 | 8,034 | **14.71** | 0.0% | 0 |
| `figma-generate-diagram` | 1,494 | 112 / 10,272 | 7 | 14,378 | 9.62 | 0.0% | 0 |
| `figma-generate-design` | 4,441 | 478 / 33,206 | 2 | 956 | **0.22** | 41.5% | 0 |
| `figma-generate-library` | 3,232 | 365 / 22,652 | 7 | 22,491 | 6.96 | 13.7% | **8 (.js)** |
| `figma-use` | 4,639 | 435 / 34,164 | 19 md + 1 `.d.ts` | 27,116 (+61,827) | 5.85 | 28.9% | 0 |
| `figma-use-figjam` | 913 | 64 / 7,089 | 13 | 19,754 | **21.64** | 4.6% | 0 |
| `figma-code-connect` | 3,569 | 528 / 26,669 | 2 | 3,958 | 1.11 | 43.9% | 0 |
| `figma-use-slides` | 3,234 | 214 / 22,033 | 6 | 7,142 | 2.21 | 20.5% | 0 |
| `figma-implement-motion` | 3,137 | 146 / 23,279 | 6 | 6,341 | 2.02 | 4.1% | 0 |
| `figma-use-motion` | 952 | 80 / 6,910 | 2 | 3,166 | 3.33 | 0.0% | 0 |
| `workflow-skills/generate-project-plan` | 3,901 | — | 14 | 11,232 | 2.88 | — | 0 |
| `workflow-skills/video-interaction-mapper` | 1,677 | — | 1 README | 248 | 0.15 | — | **5 (.py)** |

Aggregates (`agg.py`):

| | SKILL.md | aux `.md` |
|---|---:|---:|
| figma, 12 skills | 2,611 lines, **25.5% code** | 18,239 lines, **54.7% code** |
| Anthropic, 6 skills | 1,737 lines, **34.5% code** | 5,685 lines, **42.6% code** |

### 1b. How much is reached only under a condition

I classified every load directive in each SKILL.md as unconditional (`"Before any…"`, `"Required"`, `"always"`, `"mandatory reading"`) or conditional (`"Load when…"`, a routing table row, `"as needed"`).

| Skill | reference structure | typical single-run read | as % of skill |
|---|---|---:|---:|
| `figma-generate-diagram` | **partition** — 6 mutually exclusive type refs + 1 shared | 1,494 + ~2,114 = **3,608** | **23%** |
| `playground` | **partition** — exactly 1 of 6 templates | 555 + ~584 = **1,139** | 28% |
| `figma-swiftui` | **partition** — 1 of 2 directions | 546 + 2,663 or 5,371 | 37% or 69% |
| `figma-use-figjam` | library, "load only what your task needs", typ. 3–4 of 13 | 913 + ~2,470 + ~4,500 | ~40% |
| `figma-use` | 2 refs declared unconditional (`index.md`, `gotchas.md`) | **floor 14,557** before any conditional ref | **46% floor** |
| `figma-generate-library` | 5 of 7 refs marked **Required**, one per phase, all phases run | 3,232 + ~19,880 | ~90% |
| `claude-automation-recommender` | 5 refs, one per category; skill recommends **all five categories every run** | 1,529 + 4,530 = **6,059** | **100%** |
| `build-mcpb` | `local-security.md` declared "mandatory reading, not optional" | 1,058 + 764 (+745 cond.) | 71% |
| `figma-generate-design` | 2 refs, both cross-skill, both conditional | 4,441 of 5,397 | 82% |

Two ends worth naming. `claude-automation-recommender` is a five-way split in which **all five branches always fire**: it pays the full structural cost of progressive disclosure and buys zero reduction in read volume. `figma-use` — the file every other figma skill defers to — declares a **14,557-word mandatory floor** (SKILL.md 4,639 + `plugin-api-standalone.index.md` 2,554 + `gotchas.md` 7,364), of which its own SKILL.md is only 32%. Its progressive disclosure relocates the mandatory read; it does not shrink it.

---

## 2. Delta

Each item is labelled with why Stage 1 could not have produced it.

### D1 — The one observed edit across three releases of a 158,000-word corpus is a deletion, propagated to every site by grep

`~/.claude/plugins/cache/claude-plugins-official/figma/{2.2.88,2.2.90,2.2.91}/` are three cached releases of the same tree, dated 2026-08-04, 08-05 and 08-08. Total corpus size: 157,995 → 158,043 → 157,911 words. `diff -rq` over the whole tree:

- **2.2.88 → 2.2.90**: two hunks, both the *same* factual narrowing, in `figma-use/references/api-reference.md` and `.../working-with-design-systems/wwds-components.md`. "Components, component sets, and instances all inherit `PublishableMixin`" → "Components and component sets inherit `PublishableMixin`. Frames, instances, and other scene nodes do not; accessing `description` on them throws." A false claim corrected by narrowing, at both of its sites, in one release.
- **2.2.90 → 2.2.91**: one topic (`sharedPluginData`) removed from four sites at once — `figma-use/SKILL.md` rule 3a, a `gotchas.md` paragraph, a `gotchas.md` table row, and a `gotchas.md` code sample. Zero residue in any `.md` except the generated API index. Net −25 words in SKILL.md.

Zero additions in either release.

Why Stage 1 could not produce this: Stage 1 (`ratchet.md`) had exactly one tracked standing prompt (`descvi/AGENTS.md`, n=1) and concluded the ratchet is real between structural events. This is a second, independent, much larger tracked corpus whose entire observed prose delta over four days is one narrowing and one deletion — and the deletion was executed with the discipline `reference/worker-brief.md` rule 5 asks for ("grep the whole FILE, not your diff"), by someone outside this project.

### D2 — The removal warrant these vendors use is not in Stage 1's list of seven

`ratchet.md` D1 enumerates seven cheap removal warrants read off this owner's commits. Both observed deletions here use an eighth: **the world the rule describes changed under the author** — an API discouraged upstream (`sharedPluginData`), a type mixin narrowed (`description`). It is adjacent to "the cause is gone" but distinct in a way that matters operationally: the trigger is *external and dated*, so it arrives on someone else's schedule and the author only has to propagate it. That is why the edit rate is near-zero and the direction is down. A standing prompt whose rules describe an external surface gets its deletions handed to it; a standing prompt whose rules describe *the author's own preferred behaviour* never does. Stage 1 could not see this, because every prompt in its evidence base is of the second kind.

### D3 — Two vendor skills that are *required to be co-loaded* give directly contradictory instructions, and the residue localises the failed propagation

`figma-generate-library/SKILL.md:11` — "The `figma-use` skill **MUST** also be loaded for every `use_figma` call." `figma-use/SKILL.md:17` — "If the task involves creating or building a component in Figma (even a single component), also load `figma-generate-library`." They are mandated into the same context.

- `figma-use/SKILL.md:63-82`: "split it into N `use_figma` calls (one per target page) and **emit them in parallel**… **you MUST issue the N tool calls in one message**… Default to parallel fan-out for any multi-page work — reads and writes alike."
- `figma-generate-library/SKILL.md:138` rule 13: "**NEVER parallelize `use_figma` calls** — Figma state mutations must be strictly sequential. Even if your tool supports parallel calls, never run two use_figma calls simultaneously."

The contradiction is also *internal* to `figma-generate-library`: line 120 tells you to split multi-page work into one call per page and links the parallel-fan-out gotcha; line 138 forbids running them simultaneously.

The propagation residue is exactly locatable. `gotchas.md:191`'s heading was renamed to "…split multi-page work **into parallel calls**". Four files cite that anchor:

| citing file | anchor cited | resolves? |
|---|---|---|
| `figma-use/SKILL.md:82` | `…-into-parallel-calls` | yes |
| `figma-use/references/component-patterns.md:271` | `…-into-parallel-calls` | yes |
| `figma-generate-library/references/discovery-phase.md:260` | `…-into-parallel-calls` | yes |
| `figma-generate-library/SKILL.md:120` | `…-**across**-calls` | **no** |

A policy reversal (sequential → parallel) propagated to 3 of 4 citation sites. The one site it missed is in the file that still carries the old policy as a numbered Critical Rule. The stale link and the stale rule are the same miss.

Why Stage 1 could not produce this: `counterpart.md` D8 ("what does this contradict once it lands — and which document is nearer the reader") had only in-house instances (`7b1c9d2`, `a995bba`), and `counterpart.md` §5 explicitly records that no cost in the whole record was found at the desk. This one is findable at the desk by one grep, in someone else's corpus, and it comes with a measurable propagation rate (75%) and a mechanical residue marker (the stale anchor) that points at the surviving contradiction. **A renamed heading is a free detector for a policy change that did not finish propagating.**

### D4 — Moving a paragraph out of SKILL.md silently breaks its relative cross-skill links, and two independent vendors hit it

`links2.py` over both corpora, 298 resolvable internal links:

| corpus | links | resolve | within-skill | cross-skill |
|---|---:|---:|---:|---:|
| figma 2.2.91 | 298 (whole tree: 399) | 98.7% | 185/186 (99.5%) | 109/112 (**97.3%**) |
| `mcp-server-dev` | 20 | 85.0% | 16/16 (100%) | **1/4 (25%)** |
| `claude-automation-recommender` | 8 | 62.5% | 5/8 | n/a |
| `playground` | 6 | 100% | 6/6 | n/a |

Every cross-skill failure is the same off-by-one. `build-mcp-app/SKILL.md:59` writes `../build-mcp-server/references/elicitation.md` and it resolves. The *identical string* in `build-mcp-app/references/widget-templates.md` does not, because the base directory is now `references/`. Verified directly:

```
build-mcp-app/../build-mcp-server/references/elicitation.md              → exists
build-mcp-app/references/../build-mcp-server/references/elicitation.md   → No such file
```

Same error in `build-mcpb/references/local-security.md` (×2) and in `figma-use/references/working-with-design-systems/wwds-variables.md` → `../../figma-generate-library/references/token-creation.md` (needs three levels). Four of the seven dead links in both corpora are this.

Why Stage 1 could not produce this: Stage 1 established relocation as the dominant shrink move (`ratchet.md` D2, "nearly every measured shrink event is a relocation") and never priced it. This is the price, measured: relocation is not free even when the text is unchanged, because a relative pointer's meaning is a function of where the text sits, and the failure is silent at authoring time. It is also the mechanism by which a *correct* move produces a *broken* artifact — precisely `counterpart.md` D1's shape ("the rule punished the better artifact") arising from the act of splitting rather than from a rule.

### D5 — Two implementations of the same anti-rot device, opposite failure behaviour, and the discriminator is one clause

`mcp-server-dev/skills/build-mcp-server/references/versions.md` is a cross-file reverse index of every version-sensitive claim in three sibling skills, with a `## How to verify` block of runnable commands (`npm view`, `gh api`, `curl -sI`). It is the strongest instance of `without-measurement.md`'s "pointer that regenerates the value" I found anywhere, and it is better than `lead.md`'s harness-facts block in one respect Stage 1 did not consider: it quarantines the *pointers to* the volatile facts, so each fact stays at its point of use instead of being lifted into a block away from the rule it qualifies.

It has rotted. Its locators are bare line numbers:

| index entry | claimed | actual | drift |
|---|---|---|---|
| `elicitation.md:15` | L15 | L15 | 0 |
| `build-mcp-server/SKILL.md:43,76` | L43, L76 | L45, L79 | +2, +3 |
| `auth.md:20,24,41` | L20, L24, L41 | L11/12, L36/40, L55/57/61 | −9 … +20 |

Four of six locators are wrong; two point at blank lines.

`figma-use/references/plugin-api-standalone.index.md` is the same device at scale — a 2,554-word index into a 452 KB / 11,329-line `.d.ts`, 117 symbols each carrying an `L#`. Checked mechanically against the actual definition lines: **1 of 113 resolvable symbols is exact; 2 are within ±3; median absolute drift 16 lines, max 26, all positive.** The file's own header claims 11,327 lines against an actual 11,329.

The two rot identically. Only one is broken, and the difference is a single clause. The figma index says: *"Grep by symbol name to jump to definition. All `L#` line numbers refer to that file."* The primary key is a content anchor; the line number is an accelerator, so 16 lines of drift costs nothing. `versions.md` offers no content anchor, so the same drift makes the index unusable at exactly the moment it is consulted.

Why Stage 1 could not produce this: `reference/worker-brief.md` rule 4 says "anchor every edit by content, never by line number", and `without-measurement.md` §2 established that cached enumerations rot and should be deleted or repointed. Neither reaches the move actually used here — **ship both, with the content anchor named as primary** — which turns a rotting cache into a free accelerator whose failure mode is a slower grep rather than a wrong answer. That is a third option between "regenerable pointer" and "delete", and it is the one that makes a 62,000-word generated artifact usable at all.

### D6 — The "recap" section is the sole home of five rules

`figma-use/SKILL.md` §8 "Pre-Flight Checklist" is 21 checkboxes and reads as a summary of §1's 20 numbered Critical Rules. It is not. Five of its items appear nowhere else in SKILL.md **and nowhere in `gotchas.md`** (grep-verified): `resize()` resets sizing modes; IDs from previous calls passed as string literals; paint `color` must not include an `a` field; `FONT_FAMILY`-scoped variables must have every mode's value loaded before binding; `resize()` called before setting sizing modes. Thirteen of 21 restate a numbered rule; eight do not; five have no other home in the skill.

Why Stage 1 could not produce this: Stage 1's compression work (`attention-cost.md` §2) measures whether a general form re-derives its specifics. This is the opposite pathology and it is invisible to that test — a section whose *form* is redundant (a checklist) has become a rule store, so anyone who deletes it as a recap silently deletes five rules. It is the structural counterpart to `9a4e744` ("a file violating its own rule"), found in the wild: the section that exists to prevent omissions is the section from which omissions are hardest to notice.

### D7 — Two opposite, explicit policies for `scripts/` from the same vendor in the same release

`workflow-skills/video-interaction-mapper/SKILL.md:33-35`: *"Run the bundled files in `scripts/` as executable workflow helpers. **They are part of the skill's implementation, not reference material. Read or modify them only when debugging**, adapting to an unusual environment, or changing the skill itself."* — 5,111 words of Python that never enter context. The SKILL.md invokes them by CLI with flags.

`figma-generate-library/SKILL.md:140` rule 15: *"**Use the helper scripts** — **embed** scripts from `scripts/` into your `use_figma` calls. Don't write 200-line inline scripts from scratch."* — 3,322 words of JavaScript that must be read to be used.

Why Stage 1 could not produce this, and why it is the most useful item here: Stage 1 established "dissolve into structure" as strictly the best move when available (`attention-cost.md` D8, commit `a2ab0b4`) — the instruction stops needing to be followed. This corpus shows the move has **two forms with different economics**, and the vendor uses both without naming the distinction:

- **Executed** (`video-interaction-mapper`): the script is a *process boundary*. It costs zero context and the instruction genuinely dissolves — `extract_key_frames.py --mode scout` cannot be done wrong by an agent that never read it.
- **Embedded** (`figma-generate-library`): the script is a *snippet*. It costs full context on use, and the instruction does **not** dissolve — `cleanupOrphans.js` throws when handed no IDs, yet the prose rule it enforces is still written out twice (rule 11 "No destructive cleanup — cleanup scripts identify nodes by name convention or returned IDs, not by guessing", and the §11 table row "Remove only the exact node, variable, and collection IDs supplied from the state ledger").

The discriminator is whether the runtime can *call* the artifact or only *paste* it. `ocs`, hooks, and agent config are call-boundaries and dissolve. A code block in a reference file is a paste-boundary and does not — it is a reference with syntax highlighting, and its rule still has to be written in prose beside it. Stage 1's D5 ("could a mechanism hold this instead of the prose?") has no way to ask this, and would score both as "yes".

### D8 — Nobody in either corpus gives an attention or context reason for their own split

Grepped both corpora for `context window | token budget | token cost | do not load | don't load | progressive disclosure | keep short/lean`. Result: **zero instances where a skill justifies its own splitting on context or attention grounds.** Every hit is about the *artifact being built*, never about the skill file.

The sharpest instance is `build-mcp-server/SKILL.md:111,130`: *"tool schemas land directly in Claude's context window"* and *"listing every operation as a tool floods the context window and degrades model performance"*. That is the full attention-cost argument, stated by the author, as domain guidance about MCP tool catalogs — in a skill that ships 5,170 words of references and never applies the argument to itself.

The single corpus-wide exception is size-of-file, not attention: `figma-use/SKILL.md:19` — *"It is a large typings file, so do not load it all at once, grep for relevant sections as needed"* — about a 452 KB generated artifact, i.e. only the extreme case gets a stated reason.

Why Stage 1 could not produce this: Stage 1 established that *this project's* attention claim is unsupported by its own measurements. This establishes something stronger and independent — that eighteen shipped, heavily-structured procedural skills from two teams, one of which demonstrably holds the attention-cost model for a neighbouring artifact class, never invoke it to justify their own structure. The splitting is not argued from attention. If it were the reason, someone would have written it down once in 158,000 words.

---

## 3. The rule for what stays inline versus what is pushed out

**There is a real rule, it is not the one the structure suggests, and it has two named exceptions.**

The rule: **content goes out when a given run will not read it.** Not when it is long, not when it is detailed, not when it is code.

Evidence for:
- `figma-generate-design`: a single linear six-step workflow with no branch. 4,441 words inline (2nd largest SKILL.md in the corpus), 956 words of references, ratio **0.22**. Nothing to partition, so nothing goes out — including 165 lines of one step (Step 2, lines 63–228).
- `figma-code-connect`: one linear path, Steps 1–6. 3,569 words inline, ratio 1.11 — and it inlines a whole "Inline Quick Reference" API table (lines 332–400) *in addition to* shipping `references/api.md`.
- `figma-swiftui`: two mutually exclusive directions. 546 words inline — exactly the six numbered points that "hold regardless of direction" — and 8,034 words out. Ratio **14.71**.
- `figma-generate-diagram`, `playground`: strict partitions, one branch per run. Ratios 9.62 and 6.32; a run touches 23% and 28% of the skill.
- `figma-use-figjam`: 913 words inline, 13 node-type references out, ratio **21.64**, "load only the references your task needs".

The rule predicts SKILL.md length from **branch count**, not from domain size. One path → everything inline regardless of length. N exclusive paths → the shared preamble inline, the branches out.

**Exception 1 — size defeats it.** `figma-use/gotchas.md` is 7,364 words and is declared unconditional ("When to load: *Before any `use_figma`*"). By the rule it belongs inline; it is out because it is bigger than the largest SKILL.md in the corpus. There is no line cap (`figma-code-connect` 528 lines, `mcp-integration` 554), but there is an observed byte ceiling: the two largest SKILL.md files land at 34,164 B and 33,206 B, within 3% of each other, while reference files run to 37,632 B and 52,972 B. Nothing states the ceiling. Above roughly 34 KB, content goes out whether or not a run will read it.

**Exception 2 — the split can be pure cost.** `claude-automation-recommender` splits five ways where all five branches fire every run (the skill's own instruction is "Recommend 1-2 of each type"). `figma-generate-library` marks five of seven references **Required**, one per sequential phase, and every phase runs. Both pay the full structural cost — extra files, extra reads, extra link surface — and reduce nothing.

**What is *not* the rule.** Code density is not a discriminator in general. It looks like one in figma (SKILL.md 25.5% code vs references 54.7%, a 2.1× gap) and collapses in the Anthropic set (34.5% vs 42.6%, 1.2×), where `build-mcp-app/SKILL.md` is 51.1% code — more code-dense than its own references' mean — while shipping six references. Two teams, same file format, opposite convention. Anyone porting "put the code in references" out of the figma corpus is porting a house style, not a finding.

And within figma the apparent gap is an artefact of the branch rule, not an independent convention: the six router-shaped SKILL.md files carry 0.0–4.6% code (`figma-swiftui`, `figma-generate-diagram`, `figma-use-motion`, `figma-design-to-code` are all exactly **0.0%** — not one fenced line between them), while the two monolithic ones are the most code-dense files in the family (`figma-code-connect` 43.9%, `figma-generate-design` 41.5%). Code does not go out because it is code. It goes out when it belongs to a branch — and a router, by construction, contains no branch.

**Redundancy is not governed at all.** `gotchas.md`'s 44 topics against `figma-use/SKILL.md`, hand-classified: **20 restated in both, 24 only in gotchas.md**. I report the hand count because two mechanical proxies bracket it uselessly — a shared-key-term test says 91% duplicated, an exact-phrase test says 11% — which is itself worth recording: *automated overlap measures between a skill and its references are not trustworthy at either threshold*, so "is this reference redundant with the skill?" cannot currently be answered by grep.

---

## 4. Contradicting a Stage 1 conclusion

**`ratchet.md`'s framing of removal cost does not survive contact with a corpus whose rules describe someone else's surface.** Stage 1's ratchet is a story about an author who must generate their own warrant to delete. In this corpus the warrant arrives from outside on a schedule the author does not control (D2), the propagation is a grep (D1), and the observed direction over three releases is net down with zero additions. Stage 1 already corrected §1's stated *cause*; this corrects its stated *scope*. **The ratchet is a property of rules about your own preferred behaviour, not of standing prompts.** A prompt full of rules about an external, versioned surface has a deletion clock built in; a prompt full of rules about how you would like an agent to work has none, and no amount of instrumentation supplies one.

**`without-measurement.md` §1's "delete, not correct" is too strong for one of its three shapes.** Its policy for a claim that is neither regenerable nor anchored is deletion. The figma API index is a cached enumeration of the worst kind — 117 hand-copied line numbers, 99% of them wrong — and deleting it would be a mistake, because the same file names a content anchor as primary and the numbers as an accelerator (D5). The corrected form: **a cached value may stay if the retrieval instruction beside it does not depend on the cache being right.** `565a6b0`'s rule was derived from citations, where there is no such second key; it does not generalise to indexes that have one.

**`attention-cost.md` D8's ranking of "dissolve into structure" as always best needs the call/paste distinction (D7).** As stated, D8 would score `figma-generate-library`'s eight helper scripts as a dissolve. They are not: the rules they enforce are still written out in prose twice, and reading a script to paste it costs more context than the prose it was supposed to replace. Dissolve is strictly best only across a *call* boundary.

**One Stage 1 conclusion this corpus supports rather than contradicts, worth saying because it was uncertain:** `where-justification-lives.md` argued that provenance belongs outside and mechanism inline. Neither vendor writes dated incident provenance into any of the 18 skills — zero `Measured YYYY-MM-DD`-style clauses across 158,000 words — while mechanism is written out constantly ("the iframe's CSP blocks the transitive dependency fetches and the widget renders blank"; "failed scripts are atomic — if a script errors, it is not executed at all"). The convention Stage 1 derived from one rewrite is the universal convention in both external corpora.

---

## 5. Where this corpus speaks with one voice

Convergence is weak evidence here and the figma family's agreement is worth near-nothing (one vendor, one template — 7 of 12 carry the identical `skillNames` logging paragraph, 5 of 12 the identical "MANDATORY prerequisite" opener). Listed only where agreement crosses the vendor boundary:

1. **The `description` frontmatter is a trigger list, not a summary.** Both vendors write it as enumerated user phrasings ("Trigger for requests such as…", "This skill should be used when the user asks to…"), often longer than the first section of the skill body. 18/18.
2. **A reference is never named without a load condition beside it.** `mcp-server-dev`, `plugin-dev`, `claude-code-setup`, and 7/12 figma skills use a two- or three-column table whose second column is "When to load" / "Load when" / "Best For". Where a table is not used, the condition is inline in the sentence. I found no bare list of reference filenames anywhere.
3. **No dated provenance.** Zero incident narratives in 158,000 words, both vendors. Mechanism, yes, constantly; "we hit this on 2026-07-26", never.
4. **No stated attention or context justification for the skill's own structure.** 0/18 (D8).
5. **A front-loaded numbered rule block, before any procedure.** "Critical Rules" (figma-use, figma-generate-library, figma-use-slides, figma-implement-motion), "Rules and Pitfalls" (figma-code-connect), "Critical constraints"-shaped openers in `build-mcpb` and `build-mcp-app`.
6. **Errors are documented as verbatim strings.** Both vendors table the exact runtime message and its cause (`figma-use` §7; `build-mcp-app`'s CSP debugging note). Nobody paraphrases an error.

One thing that looks like convergence and is not: heavy `scripts/` use. Two of 20 skills have scripts at all, and those two disagree about whether scripts are read (D7).

---

## 6. What I read and found nothing in

- **`figma-design-to-code/SKILL.md`** (780 words) and **`figma-create-new-file/SKILL.md`** (580 words) — no references, no scripts, no conditional structure. Read in full looking for a stated reason to stay monolithic; there is none. Their only interesting property is a cross-skill deep link into another skill's reference (`../figma-use-slides/references/slide-grid.md`), which is the pattern that breaks in D4 — here it resolves, because it is written from SKILL.md.
- **`mcp-integration/SKILL.md`** (554 lines, the longest file in the corpus) — read for a length-pressure signature and found none. Its three references are equal-sized (548 / 535 / 538 words), which reads as a planned partition rather than accretion, and its `examples/` are three 15–26-line JSON files. No routing conditions beyond "Deep dive on each server type".
- **`playground` templates** — six near-identical 67–179-word scaffolds. A clean partition and nothing else; the split rule in §3 is the whole content.
- **`figma-generate-diagram/references/{architecture,flowchart,sequence,erd,gantt,state}.md`** — sampled three of six for divergence between branches of one partition. They are structurally identical (same section order, same "Universal constraints" restated per file). No disagreement to report.
- **Git history for either corpus** — neither cache nor marketplace tree is a repository (`.git` absent in both). The three figma release caches are the only diachronic evidence available, which is why D1 rests on `diff -rq` rather than on commit messages. No commit messages exist anywhere in this corpus, so `where-justification-lives.md`'s question — whether an argument attached to a deletion helps — is untestable here in either direction.
- **`plugin-api-standalone.d.ts`** (61,827 words) — inspected structurally to check the index (D5), not read. It is machine-generated typings, not authored instruction, and I excluded it from every word count except where explicitly noted.
- **The 8 `figma-generate-library/scripts/*.js`** — read two in full (`createComponentWithVariants.js`, `cleanupOrphans.js`) and skimmed the rest looking for instruction that had been absorbed out of the prose. Found the opposite (D7): the rules the scripts enforce are still stated in prose, twice.
