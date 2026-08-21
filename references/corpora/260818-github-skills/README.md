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

`gpt-5.6-luna` is cheap and now measured. Starting from a freshly reset weekly window, 2,274 calls moved `rate_limits.used_percent` from 2% to 10% — 0.0035 points each, and steady across five chunks of roughly 490. Reading 3,975 skill directories costs a tenth of one week.

That also settles a reading this file used to carry. A day earlier the number appeared to step 76 → 77 after about 113 calls, which suggested a rate thirty times higher. It was a residue: `gpt-5.6-sol` had left the counter somewhere above 76.5 and one call tipped it. The gauge has no decimals, so the only way to read it is from a floor you own.

Claude's side is measured too, and differently. 398 Haiku calls through `claude -p` cost $18.90 — $0.0475 each, 15.0M input tokens in twenty minutes. The weight is not the skill document: 23,145 tokens per call are Claude Code's own system prefix, against roughly 6k of content, because `-p` is a fresh session every time. Output is 94% thinking. `--allowed-tools ""` removes 490 tokens of that, `--system-prompt` leaves 15,852 still arriving, and `DISABLE_PROMPT_CACHING` costs *more* — the 25% write premium on 12k is cheaper than paying list price for the 22k prefix.

Luna is also faster: 29 calls a minute on six workers, against 16 on twelve.

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

Over 3,227 verified quotes it is **17%** — and getting there took throwing out a wrong version of the same number. Counting every quote whose `quote_file` is not `SKILL.md` gives 27%, but 410 of those records have no `SKILL.md` at all: they are anchored on a root `AGENTS.md` or `CLAUDE.md`, which is the whole skill rather than a level above one. A claim cannot have moved down from a level that was never there. Among the 2,825 skills that do have a `SKILL.md`, 480 quotes came from a file beside it; among the 1,399 that have a `SKILL.md` *and* prose siblings, it is **34%**. The pilot's 5-of-5 was drawn from repositories chosen for having deep reference trees, and it overstated the rate by a factor of two.

## Pass 1 reads a collection, and it reads the top of one

`repo_pass.py` gives one call every pass-2 record from one repository. Fifty repositories — the eight the pilot used, plus fourteen each from three coverage bands — cost $5.96 and five minutes at `sonnet`, and the two halves of the prompt did not do equally well.

The describing half holds up. No schema leaks in fifty: `field` appears only under `one-field` and `form` only under `unified-by-form`. Every `best_claim` traces back — 46 identical to a quote it was fed, 4 a trimmed span of one, none matching nothing, and none resting on a quote that had failed pass 2's own verbatim check. That closes the chain: a sentence in a source file, located there by `extract.py`, located again in the record by this pass. And seven of the pilot's eight `coherence` verdicts reproduced across a change of corpus *and* a change of prompt. The eighth is `trailofbits/skills` moving `grab-bag` to `one-field`, which was one of the two verdicts the pilot had already flagged as arguable; a security firm's fuzzing and static-analysis skills are one field.

The auditing half mostly restated its input. Of fifty flags over 513 records, **twenty were raised against a `no-signal` record** — and `no-signal` means no grep pattern fired, not that the skill reaches for nothing, which is the one thing `labels.py` is built never to claim. Nine more repeated `quote_verified: false` back at a reader that had handed it over. Six were new: four cross-file observations no other pass can make, including a quote appearing verbatim under two different files in `NeoLabHQ/context-engineering-kit`, and two null quotes under summaries specific enough to expect one. The prompt caused this by listing "the `reach` label contradicts the summary" as a flagging criterion without saying which direction of that comparison is meaningful. `prompt/repo-siblings.md` says which direction, and says outright that a field handed to the model is not something to hand back; `prompt/repo.md` is kept as run. Re-running the same fifty against it cost $7.06 and moved the flags where the wording aimed them:

| | run 1 | run 2 |
| :--- | ---: | ---: |
| flags on a `no-signal` record | 20 | 9 |
| restating `quote_verified` | 9 | 5 |
| cross-file, or a null under a specific summary | 6 | 17 |

`coherence` agreed on 46 of 50 across the change. Both runs kept a clean schema and a fully traceable `best_claim`.

At 450 repositories — taken in descending order of how many of each one's skills were read, so a run stopped early loses its least useful tail — the totals are 450 of 450 parsed, no schema leaks, 132 flags of 426 that no cheaper pass produces, and $60.

## `grab-bag` measures how much of the repository was read

Coverage moves the verdict monotonically across its whole range, and nothing else measured does:

| coverage | repos | `one-field` | `grab-bag` | median repo size |
| :--- | ---: | ---: | ---: | ---: |
| <20% | 54 | 48% | 37% | 30 |
| 20–30% | 108 | 56% | 29% | 24 |
| 30–40% | 73 | 59% | 23% | 23 |
| 40–55% | 110 | 68% | 18% | 17 |
| 55–75% | 76 | 67% | 14% | 15 |
| 75%+ | 29 | **86%** | **3%** | 10 |

At three-quarters of a repository read, `grab-bag` almost disappears. Held at a fixed coverage of 20–40%, repository size produces nothing monotone — 56%, 66% and 48% `one-field` across ≤25, 26–45 and 46+ files — while held at a fixed size of 16–25 files, coverage still separates 65%/20% from 52%/33%. **Coverage matters within size; size does not matter within coverage.**

An earlier draft of this section claimed the opposite about size, from a comparison that held the *number* of files read at twelve rather than the fraction. Twelve of a 20-file repository and twelve of a 60-file one are 60% and 20% coverage, so that comparison varied coverage while appearing to control for it. Reading fewer files does not by itself push the verdict: repositories where three or four were read land at 62% `one-field`, indistinguishable from those where twelve were, because a small repository read three deep can be better covered than a large one read twelve deep.

What survives as an independent signal is the flag rate, which falls from 17% of records to 10% as `n_read` rises — less evidence, more suspicion — and that is a fact about the auditor rather than about the repositories.

The viewer prints the coverage on the verdict chip, because a `grab-bag` reached from 18% of a repository and one reached from 90% are not the same claim. The Korean label for it is `모음` rather than `잡동사니`: of 82 such verdicts, 45% describe a personal toolbelt or one project's kit in so many words against 12% of `one-field` verdicts, so what holds them together is an owner rather than a subject — and `잡동사니` frames as junk what is mostly somebody's actual working set.

## One fabrication in 450 calls, and the check is what found it

`bioMate-AI/biomate-bioconductor-kb` produced a `best_claim` about bacterial genome counts overwhelming BioMart. It is in none of the three records the call was given and in none of the repository's fifteen skill directories. It reads exactly like real `biomaRt` documentation, which is the point: the model answered from what it knows about the subject rather than from what it was shown, and a scoring pass would have recorded that as a good result.

Three other claims failed to trace and none was invented. Two joined several lines of a list into one sentence with ` - ` separators, and one turned `scores 100` into `scores 10` while paraphrasing around it. `norm` was not extended to accept any of them: a bullet list flattened into a sentence is not a sentence in the source, and the guarantee is worth more than three rows.

## The verbatim checker has now been wrong four times

Every one was a normalisation gap, and none was a fabrication:

| what it missed | found by |
| :--- | :--- |
| a quote lifted out of a wrapped `# ` comment | first fixture run |
| a quote lifted out of `- **bold:**` | first fixture run |
| curly quotes against straight ones | pass 1, on a Chinese legal skill scoring 0.98 similar and 0 matching |
| `[text](url)` against its rendered text | pass 1, on `microsoft/skills-for-fabric` |
| whitespace between CJK characters, and fullwidth punctuation | pass 1, on three CJK repositories |

`norm` now folds typographic and fullwidth punctuation to ASCII, reduces links to their text, and drops whitespace adjacent to CJK — the last narrowly, because collapsing space everywhere would let an English paraphrase match by accident. Rechecking pass 2's 93 rejected quotes recovers six; **87 remain, and they are drift.** So the check was never too strict. It was wrong in five specific ways, all of them about writing systems and markup it had not been shown.

Two `best_claim` values still do not trace, and both are real drift: `agentscope-ai/OpenJudge` turned `scores 100` into `scores 10` while paraphrasing around it, and `obra/superpowers-skills` dropped the clause that dated the observation.

One reply was accepted as a record with no verdict in it. `parse` took the first balanced object it found, and that was an element of `recheck`; it now requires the object to carry the key the caller names.

## What pass 1 found that the pass it audits could not

Three of run 2's flags said a `cli` label had no business being there — a rubric-text generator credited with the Go toolchain, a Firebase-messaging skill credited with `make`. They were right, and about `labels.py` rather than about the skills.

The comment over `BINS` said matches were "counted only at the head of a line inside a fence". The regex was `(?:^|[\s|&;(])`, which under `re.M` means line start **or any preceding whitespace**, and that is where English lives: `go through` inside a fenced ASCII diagram scored `go`; `make FCM messaging work` scored `make`. The comment described an intent the code did not implement, and nothing downstream could notice, because a grep that over-fires looks exactly like a corpus that uses more tools.

Restricting the match to command position — line start, a shell prompt or list marker at one, or the point after `|`, `&&`, `;`, `$(` — over all 3,964 records:

| | before | after |
| :--- | ---: | ---: |
| `make` | 222 | 44 |
| `go` | 208 | 63 |
| `node` | 346 | 196 |
| `claude` | 120 | 67 |
| all `cli` labels | 5,451 | 4,139 |

216 records — 5% — lose a claim to reach outside themselves, 184 of them all the way to `no-signal`. The prompt markers are worth their extra alternation: 1% of a 1,200-record sample writes its only invocation as `$ uv run …`, which a strict line-start rule would have thrown away. Corrected labels are in `runs/labels-v2.jsonl`, keyed by skill.

A second defect surfaced while measuring the first. `extract.py` keyed a skill as `repo/dir`, and `dir` is empty for a repository anchored on a root `AGENTS.md` or `CLAUDE.md` — so a repository holding both produced two manifest entries under one key. 442 keys cover 447 entries, 25 of them shortlisted: read twice in a fresh run, and the second silently skipped as already-done in a resumed one. The key now carries the loose file, and the record carries it as a field.

**What this pass sees is not the collection.** 745 of 846 repositories arrive partly read, and the missing files are not a random sample: dedupe accounts for 386 of 4,671 unread directories in the large repositories and the specificity cut for the other 4,285. So a `filler` list here names filler among a repository's strongest files. The prompt says so and the record carries `n_read`/`n_total`, but no wording repairs the sample — only reading more of it would.

A byproduct worth keeping: the flags include eighteen records whose quote was null, chosen because their summaries promised something a quote should have carried. That is a better place to test whether pass 2's nulls are real than an equal number drawn at random.
