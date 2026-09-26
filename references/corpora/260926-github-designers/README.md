# UI/UX designer agents and design skills on GitHub — evidence for the `designer` role

A sibling of `../260926-github-agents/`, which surveyed writing roles for the `writer` role. This one asks what a `designer` role should carry, given that the owner expects its output to vary: an HTML mockup, a light prototype, components, design tokens, a redesign of existing UI, or a written opinion.

The answer is in `analysis/synthesis.md`; read its scorecard first. The short version:
- Nobody writes one designer role across all those forms.
- Craft and taste live in skills more than in agents.
- Starting from the existing product is common. Rendering the result and looking at it is a minority practice, and half the roles that ask for it say nothing about a missing tool.
- The corpus does most of its quality judging inside the maker, which runs against a designer that does not judge its own work.

Nothing here measures outcomes.

## Why agents and skills both

Harvesting agents alone missed where the craft is. The earlier skill corpus (`../260818-github-skills/provenance.tsv`) lists 430 SKILL.md files whose directory names read as UI work, including Anthropic's `frontend-design`, `taste-skill`, `web-design-guidelines` and `emil-design-eng`. So the extraction reads both, and every count in the analysis is split by kind.

## Pipeline

| Step | Tool | Output |
| :--- | :--- | :--- |
| Harvest agents: the writer harvest's 778 repositories plus design-oriented repo queries, repo trees, code search, raw fetch, exact dedupe | `harvest.py repos trees code raw dedupe` | `repos.json`, `files-*.json`, `index.json`, `unique.json`, `harvest.log`, `corpus/` (ignored) |
| Near-duplicate clusters (same rule as the writer corpus: MinHash, 5-word shingles, Jaccard 0.6) | `cluster.py` | `clusters.json`, 4,350 clusters |
| Design skills from the skill corpus: select by directory name, fetch at HEAD | `skills.py select fetch` | `skills-selected.json`, `skills-index.json`, `corpus-skills/` (ignored) |
| Narrow both, merge near-duplicate skills, cut batches of ten | `pick.py` | `selection.json`, `batches/NNNN.json` |
| Extraction, one model agent per batch, one file at a time | `workflows/extract.js` | `results/<batch>/<id>.json` (ignored) |
| Shape, id and verbatim-quote check | `check_results.py` | — |
| Records, counts, quotes by dimension | `merge.py`, `aggregate.py`, `export_claims.py` | `records.json`, `stats.txt`, `claims/<dimension>.jsonl` |
| Ten theme readers, seven deep readers over 31 files, synthesis, three skeptics, revision | `workflows/analysis.js` with `analysis/deep-read-selection.json` | `analysis/` |

## What was read

The harvest kept 6,613 agent files from 4,632 repositories: 5,233 distinct texts in 4,350 clusters. Code search dominated, and many of its queries hit the 300-result cap, so the agent side is a large sample rather than a census.

`pick.py` keeps what the writer corpus showed was worth reading, and drops noise by name:
- **Agent clusters.** Kept only if copied into two or more repositories, or at 100 stars and up. The writer corpus's low-star tail read as domain content rather than craft.
- **Agent names.** An allowlist of design terms minus a denylist of the other things "design" names: APIs, games, systems, experiments, curricula.
- **Excluded on purpose.** Accessibility-only auditors, frontend implementers, UX researchers, Figma API operators and UI-library usage guides. Each is its own specialist. Designer roles that cover those concerns say so in their own text.
- **Skills.** Narrowed the same way. Anything whose name meant something else was dropped by reading names and descriptions: prototype pollution, TypeScript interfaces, image colour grading, poster art. Then near-duplicates were merged; twelve copies of one `frontend-design` became one.

That left 355 agents and 121 skills, 476 files and about 520k words, some 39% of the writer run. The extraction marked 405 of them as design roles: 308 agents and 97 skills, from 314 owners.

## Extraction

Per file, `workflows/extract.js` returns:
- `design_role`
- outputs, modes (create, revise-existing, review) and surfaces
- sixteen flags, each requiring a supporting quote. Among them: inspects the existing UI, follows the design system, renders and looks, anti-generic guidance, commits to a direction, variants, states, accessibility, and a boundary with the implementer.
- up to ten verbatim instructions, each with a dimension
- `external_files`, which is true when substance is deferred to files not included (57% of design roles; 75% of skills)
- a 1–5 specificity, and a note

A two-batch pilot preceded the run. 90 of about 3,700 quotes (2.6%) did not locate verbatim in their source and are dropped by `export_claims.py`, leaving 3,261 in `claims/`. As in the writer corpus, specificity runs high (174 of 405 at 5) and is for relative comparison only.

## Limits

- Instructions, not behaviour. No rendered output was collected or judged.
- Skills were fetched at each repository's current HEAD, because the provenance records blob hashes rather than commits. Only SKILL.md was taken. The `references/` directories and sibling skills, where several of the best files keep their substance, are unread.
- Role-split counts are low by construction, because the specialist roles a designer would sit beside were excluded.
- Several runtime beliefs stated inside prompts are unverified: MCP tools under a `tools:` allowlist, `allowed-tools` in agent files, `@path` expansion in a subagent body, and nested spawning. `analysis/synthesis.md` Q6 lists them as eval 12.
- Flags were set by one model, and themes were coded by one reader each. The cross-dimension unions in the synthesis are the synthesiser's construction and are not deflated for template families.
