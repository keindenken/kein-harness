# Writing-role agents on GitHub — evidence for the `writer` role

The two skill corpora (260811, 260818) looked at `SKILL.md`. This one looks at agent definitions whose job is to write: writer, author, editor, technical writer, documenter, copywriter, report and PRD writers. It was built to answer one question before the harness's `writer` role is written: is there evidence for one general writer with doc-type rules outside it, and what should its core say?

The answer is in `analysis/synthesis.md`. Read its "How to read this" and "Bottom line" first. The short version: popular authors write one writer per repository, scoped to what that repository needs; almost nobody writes a writer as broad as the proposal; nothing in the corpus compares architectures or wordings; and the corpus is best used as a catalogue of instructions to test, not as proof that any of them works.

## Pipeline

| Step | Tool | Output |
| :--- | :--- | :--- |
| Harvest: repo search, repo trees, code search, raw fetch, exact dedupe | `harvest.py repos trees code raw dedupe` | `repos.json`, `files-tree.json`, `files-code.json`, `index.json`, `unique.json`, `corpus/` (ignored) |
| Near-duplicate clusters (MinHash, 5-word shingles, 128 permutations, 32 bands, Jaccard 0.6, 40 words minimum) | `cluster.py` | `clusters.json`, 5,264 clusters ordered by copy count, then stars |
| Batches of ten clusters | — | `batches/NNNN.json`, 527 manifests |
| Extraction, one model agent per batch, one file at a time, one JSON per file | `workflows/extract.js` | `results-sonnet/<batch>/<id>.json` (ignored) |
| Shape, id and verbatim-quote check | `check_results.py` (`RESULTS=<dir>`) | `quote-problem-ids.json` |
| Fold into records | `merge.py` | `records.json` |
| Counts | `aggregate.py` | `stats.txt` |
| Quotes by dimension | `export_claims.py` | `claims/<dimension>.jsonl` |
| Theme analysis, deep reads, synthesis, three skeptics, revision | `workflows/analysis.js` with `analysis/deep-read-selection.json` | `analysis/` |

`corpus/` and every `results*/` directory are ignored: they are other people's files and per-file model output. `records.json` is the kept form of the main run.

## What was read, and what was not

The harvest kept 7,746 files. Exact dedupe and clustering left 5,264 texts. Extraction covered batches 0000–0162, the first 1,630 clusters: every cluster copied into more than one repository, plus single-repository clusters down to 9 stars. 1,089 of them are writing roles, from 820 repositories and 776 owners.

The filename filter drops anything named for review, test, lint, debug, security, deploy, infra, sql, database, frontend or backend, and the repository queries target coding-agent collections. So reviewer roles are missing by construction, and the lean toward code documentation (project docs on 610 records, prompt instructions on 28) is partly the search's doing.

**The unread tail was sampled and left unread.** The remaining 3,634 clusters are single-repository files at 0 to 9 stars. Eight batches spread across them (0185, 0230, 0276, 0321, 0367, 0412, 0458, 0503; 80 clusters) went through the same extraction, and their records are in `records-tail-sample.json`, not in `records.json`.

| | main slice | tail sample |
| :--- | ---: | ---: |
| writing roles | 1,089 / 1,630 (67%) | 57 / 80 (71%) |
| general-purpose share | 15% | 18% |
| audience_first | 44% | 33% |
| verify_against_source | 63% | 74% |
| cite_sources | 21% | 35% |
| separate_fact_from_opinion | 9% | 18% |
| cut_or_concise | 52% | 47% |
| reasoning_kept_out | 5% | 2% |
| output_contract | 79% | 81% |

57 records is too few to read those differences as more than direction. Of the sample's 425 quotes the model rated specific, 236 have a maximum word-set Jaccard below 0.25 against every main-slice quote, so the wording is mostly new. Read one by one, the new material is domain content rather than writing craft: CRM risk flags, Spanish copy tone, legal citation forms, ad scoring rubrics, LinkedIn phrase bans, an electrical-inspection report, a quiz-item checklist. None of it adds a principle a general writer would carry. That, and the cost of 356 more batches, is why the rest was not extracted. `analysis/synthesis.md` Q6 E12 describes the larger sample that would settle it.

## Extraction

`workflows/extract.js` holds the prompt. Per file it returns `writing_role`, `doc_types`, `scope` (single-type, few-types, general-purpose), fourteen boolean flags that each require a supporting quote, up to ten verbatim instructions each with a dimension and a specific-or-boilerplate mark, a 1–5 specificity for the whole file, and a note.

Model choice was measured on pilots of the same ten files. The first cheaper-model pilot, which read a whole batch before writing, attributed 18 quotes to the neighbouring file and paraphrased 5 more. Reading and writing one file at a time brought both to zero on the re-pilot, and that is the shape the main run used. The specificity rating runs high (502 of 1,089 records at 5) and is used for relative comparison only.

`check_results.py` locates every quote in its source file after normalising whitespace and markdown markers, and lists the files whose quotes fail in `quote-problem-ids.json`. `export_claims.py` repeats the check per quote and drops any that fail, leaving 8,923 specific, verbatim quotes in `claims/`.

## Analysis

`workflows/analysis.js` ran eleven theme readers (evidence, style, structure, process, scope-boundary, doc-type convention, self-check, output, audience, length, collaboration) over `claims/`, seven deep readers over the 32 files in `analysis/deep-read-selection.json`, one synthesis against six questions about the proposed design, three skeptics (numbers, quotes, reasoning), and a revision that answered all 66 skeptic issues. `analysis/revision-log.md` records each one. The verdicts that changed under review: "misframed" became "narrower than practice", "the carrier works" became "delivered once", the missing-input policies moved from adopt to test, and the list of unaddressed instructions was reframed from gaps to candidates.

Four themes (evidence, scope-boundary, self-check, style) saved no id lists, so their counts cannot be reproduced; the others can, from `analysis/themes/*.assign.json` or the id appendices.

## Limits

- Instructions, not behaviour. Nothing here shows what an agent did with a prompt, and a third of the roles that ask for examples to be run, and declare tools, have no tool that runs anything.
- Owner is the independence unit, and it is a proxy. Catalogues such as `github/awesome-copilot` re-host many authors, and template families make one text look like many voices.
- Files a prompt depends on (conventions, register cards, skills) were not collected, so thin-looking roles may be thin only here.
- Flags and doc types were set by one model; themes were coded by one reader each.
