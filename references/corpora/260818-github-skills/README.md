# Second skill corpus — extraction prompt, validated before the harvest

The 260811 corpus asked a model to *score* each skill, and 90% of files scored 2 or 3 out of 3. The control band — drawn from below the median on the structural proxy, median specificity 5 against 54 — scored 85% against the top band's 91%. A six-point gap across a tenfold difference in the proxy is not a measurement. This round replaces the score with an extraction whose answer can be checked against the file it came from.

Nothing here has been harvested yet. What is settled is the prompt and the way it is scored.

## The prompt

`prompt/extract.md`. It asks for a summary, a dependency label, and **one sentence copied verbatim** that the author could not have written without having done the thing — or null. `prompt/extract-v0-superseded.md` is the version that asked the same question without worked examples.

Verbatim is the point. A quote is checked by locating it in the source; a score cannot be checked at all. `verify.py` does the locating, after stripping per-line comment and list markers and inline emphasis from both sides — two of the first three apparent fabrications turned out to be a quote lifted correctly out of a wrapped `# ` comment and out of `- **bold:**`, so a checker that misses those throws away good rows.

## What was measured

Model is `gpt-5.6-luna` at `model_reasoning_effort=medium`, whole file, one call per file.

| | positives (8) | negatives (8) | unlabelled (15) |
| :--- | ---: | ---: | ---: |
| v0, no examples | 3/8 | 0/8 | 0/15 |
| **v1, worked examples** | **8/8** | **1/8** | **9/15** |
| v1 + list of quotes | 8/8 | 1/8 | 8/15, **9 unverifiable** |

v0's zero on the unlabelled set was a floor effect, not a finding about the corpus: the same files yield nine verified quotes once the prompt shows what qualifies. Asking for a list instead of one sentence raises recall and starts paraphrasing, which is the one thing the design cannot tolerate.

Reliability, two independent runs of v1 over all 31 files:

- yes/no agreement **90%**, chance 52%, **kappa 0.80**
- identical sentence when both yielded one: 9/17

The second number reads worse than it is. Several disagreements are the same claim quoted at different boundaries, and the rest are two different real claims in a file that holds several — which is the cost of the one-sentence cap, not model instability.

## The fixture

`fixture/positive.txt` — eight files that 260811's `findings.md` named as carrying a claim someone had to do the work to write. `fixture/negative.txt` — eight control-band files that scored zero on every specificity marker. `fixture/unlabelled.txt` — fifteen median-sized files drawn at random, no ground truth, used to read the base rate.

Run a variant against them with `./run_variant.py prompt/extract.md --effort medium --workers 4`.

**The positive half is the weak part.** Eight files is small, and their labels are one reading of `findings.md` rather than an established fact. A variant scoring 8/8 on them has cleared a low bar. Growing this half is worth more than any further prompt wording.

Positives were first run against the first 8,000 bytes of each file, which invalidated that run: the claim `findings.md` cites in `garrytan/gstack` sits at byte 38,288. Feed whole files. Note also that feeding the whole file is not uniformly better — gstack returned a good quote from its first 8 KB and null from all 105 KB.

## Cost

`gpt-5.6-luna` costs at least two orders of magnitude less ChatGPT plan quota than the paid tiers, and whether it costs anything is unresolved. Over the rollout history `gpt-5.6-sol` accumulates +1,552 points of `rate_limits.used_percent`, `gpt-5.5` +1,221, `gpt-5.6-terra` +429, `gpt-5.4-mini` +240, and luna +0 across 20 sessions. The instrument responds — 34 sol turns move it four points.

Then it moved. Roughly 113 luna calls into one day the reading stepped 76 to 77, with no session crossing it internally and nothing else running; 60 further calls left it at 77. This does not settle the question and cannot: the reading has no decimals, so a step could be one luna call tipping a residue left at 76.9 by the sol session before it, or luna costing about 1% per hundred calls. Do not plan around either. Read the number between batches and stop if it climbs.

6–14 seconds per call at 18k tokens. Run it in small batches rather than all at once.

## Most surface proxies failed, and one was wrongly convicted

Each of these stood in for a judgement, was cheaper than a model reading the file, and measured something else:

| proxy | meant to measure | actually measured |
| :--- | :--- | :--- |
| seven `DOMAINS` regexes (260811) | subject | `meta` fires on 66% and `process` on 67%; assignment was alphabetical first-match, so every bucket after `code` is a leftover |
| `shape` regex (260811) | instruction / reference / guidebook | `instruction` on 2.7% of files, the one class most wanted |
| description word overlap | within-repo subject coherence | template reuse — top score 1.000 is five byte-identical descriptions, and `marketingskills` (all marketing) scores 0.060 against `makerskills` (a toolbelt) at 0.042 |
| the model's own `calls` field | what a skill reaches for | reported `none` for a file that says `uv run` forty-seven times |

`specificity` belongs on a different list. It looked like another failure — its control band, drawn from below the median, scored 85% against the top band's 91% — but that was the *score* failing to discriminate, not the proxy. Asked for a quote instead, a stratified 500 yields 24%, 40%, 64% and 74% across its quartiles: monotonic, and a threefold spread. The control band did exactly what a control band is for, and the conclusion drawn from it was the wrong one.

What has worked instead is a model reading the file and quoting it, with the quote located in the source before the record is kept. Over 498 stratified files, 250 quotes verified and 9 did not; two of those nine are the checker's own normalisation missing a match and the rest read as paraphrase. None of them entered the count.

The one proxy that survives is narrow and admits its blind spot. `labels.py` reports a pattern it found and never reports absence — `no-signal` means no pattern fired, not that the skill reaches for nothing. A quarter of the pilot disagreed with the model, and each side was right about a different thing: grep caught the binaries in fenced commands, the model caught n8n calling MCP tools by bare name with no `mcp__` prefix anywhere.

## A repository is not one subject

The repo pass reports `coherence` before it reports a field, because assigning a field per repository assumes a homogeneity most repositories do not have.

- `one-field` — `coreyhaines31/marketingskills` (49 files, all marketing), `czlonkowski/n8n-skills`, `huggingface/skills`
- `unified-by-form` — `nanocoai/nanoclaw`: 50 files spanning Discord, Signal, Ollama, Vercel and a Karpathy wiki, every one of them the same procedure. The form is recoverable and the per-file view cannot show it.
- `grab-bag` — `coreyhaines31/makerskills` (19 files, one maker's toolbelt), `zhayujie/CowAgent` (3 unrelated)

The same author holds one of each. Two of eight pilot verdicts are arguable, both landing on `grab-bag` while their own `what_it_is` names a thread, so `grab-bag` may be where the model goes when undecided.

## What the harvest changed, and the first thing it showed

`harvest.py` treats a skill as a directory. A survey of 2,239 skill directories found 51% hold something besides `SKILL.md`, and only 47% of those siblings are Markdown — `.py` is 32%, and there are fonts, spreadsheets and images. So the tree is mirrored rather than flattened, every file carries its blob SHA, and binaries are recorded by path and size and left upstream.

`assemble.py` then builds the document a call reads: prose inlined under a `<file path="...">` tag, everything else listed by name, size and type. Merging the scripts in as well would answer no question this pass asks — it asks for a sentence — while a merged prose document has a median of 9 KB against 11 KB for all text and a maximum of 2 MB against 15 MB.

The path on the tag is not decoration. `czlonkowski/n8n-skills/skills/n8n-agents` is 23 KB as a file and 122 KB as a directory, and in the first eight directories run this way, **all five quotes came from a reference file rather than from `SKILL.md`** — `AGENT_TOOL_BINARY.md`, `DATA_ACCESS.md`, `ERROR_PATTERNS.md`, `references/vector-f-subshell-expansion.md`, `resources/VULNERABILITY_PATTERNS.md`. 260811 concluded that prompts shrink because obligations move down a level, from a corpus containing only the level they move from. `quote_file` is where that finally becomes measurable, and eight directories is not yet a measurement.
