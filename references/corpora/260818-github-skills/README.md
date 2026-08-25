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

At 550 repositories the totals are 550 of 550 parsed, no schema leaks, and $70. The first 450 were taken in descending order of how many of each one's skills were read; the last 100 are the sixteen remaining repositories with three or more read plus 84 drawn from the ≤2 pool, stratified by coverage, because that pool is the only place where coverage and the number read come apart — two of two is full coverage from two files.

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

The ≤2 pool confirmed the coverage relationship and found the floor underneath it. Coverage still separates there: 100% `one-field` and no `grab-bag` above 75% coverage, against 57% and 29% below 15%. But split by how many files were read rather than what fraction, **all 58 repositories where one skill was read came back `one-field`** — 100% of them at every coverage band but the lowest. That is not a finding. Asked what a collection's files share, a reader shown one file has no siblings to compare, and one skill has one subject. The model said so where it could — `house_style` came back "cannot be determined from a single file" and the sample warnings say there is no basis to judge — but `coherence` has no value meaning *unanswerable*, so it answered the only way the schema allowed.

Two files is different: 48% `one-field` against 62% for three or more, with the middle coverage bands landing at 43% `one-field` and 43% `grab-bag`. That is uncertainty rather than tautology, so those verdicts are kept. The viewer drops the 58, and the corpus-wide split moves from 65/14/22 to 62/15/23 when they go.

The viewer prints the coverage on the verdict chip, because a `grab-bag` reached from 18% of a repository and one reached from 90% are not the same claim. The Korean label for it is `모음` rather than `잡동사니`: of 82 such verdicts, 45% describe a personal toolbelt or one project's kit in so many words against 12% of `one-field` verdicts, so what holds them together is an owner rather than a subject — and `잡동사니` frames as junk what is mostly somebody's actual working set.

## One fabrication in 450 calls, and the check is what found it

`bioMate-AI/biomate-bioconductor-kb` produced a `best_claim` about bacterial genome counts overwhelming BioMart. It is in none of the three records the call was given and in none of the repository's fifteen skill directories. It reads exactly like real `biomaRt` documentation, which is the point: the model answered from what it knows about the subject rather than from what it was shown, and a scoring pass would have recorded that as a good result.

Three other claims failed to trace and none was invented, out of 550: 497 `best_claim` values are identical to a quote they were fed, 29 are a trimmed span of one, and 20 are null — 19 of those in repositories where no quote was fed at all, which is the only answer available. Two joined several lines of a list into one sentence with ` - ` separators, and one turned `scores 100` into `scores 10` while paraphrasing around it. `norm` was not extended to accept any of them: a bullet list flattened into a sentence is not a sentence in the source, and the guarantee is worth more than three rows.

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


## The nulls are real, and the one-sentence cap is expensive

`repo_pass.py` flags a record when its summary promises something specific and its quote is null — a testable prediction that a sentence is there and the first reader missed it. 91 of those went back through `extract.py` at `sonnet` on the unchanged prompt, blind to the earlier verdict, against two controls: 45 nulls the repository pass did *not* flag, and 45 records that already held a verified quote.

| arm | n | verified quote on re-read |
| :--- | ---: | ---: |
| flagged null | 91 | 15% |
| unflagged null | 44 | 14% |
| already had a quote | 44 | 70% |

**The flag carries no information.** A null the repository pass singled out yields no more than one drawn at random, so those 91 of 459 flags are noise, and the criterion that produced them should come out of the prompt. The 70% is what makes the other two readable: a second reader finds a quote in most files that hold one, so 14–15% is the residual rate at which a null hides something rather than evidence that `sonnet` reads harder. **Roughly one skill in seven that came back empty has a sentence in it; the other six do not.**

The control meant to check agreement found something else. Of the 31 files where `sonnet` reproduced a verified quote, only 13 were the sentence the first reader took. The other **18 were a different verified sentence in the same file**, and they are different claims rather than the same claim cut at another boundary — similarity between the pairs runs 0.16 to 0.32:

| | first reader | `sonnet` |
| :--- | :--- | :--- |
| `…/skills/ai/rag` | Fixed-size chunking splits a table in half and produces two useless chunks. | RETRIEVAL_FAILURE: 31 / 100 ← fix chunking and add a reranker |
| `…/deploy-linux-gpu` | A plain `cmd &` over SSH dies when the session closes | Heavy-KV models cost ~130 KB/token at Q8_0 → ~8.5 GB at 64K per slot |

So the 3,231 quotes are one draw, not the contents. A file that yields one qualifying sentence usually holds more, and the cap of one keeps whichever the reader happened to reach for. A second independent pass over the quote-bearing skills would be expected to add on the order of 1,300 distinct verified sentences, and over the nulls about 90 — and unlike asking for a list, which the fixture stage rejected for starting to paraphrase, it keeps one verbatim sentence per call as the unit.


## Pass 3: how far a claim travels

The guidebook/instruction split this corpus was started for does not cut where it was meant to. Only 9% of verified quotes name a tool at all, and **88% of quotes from skills that reach outside themselves name no tool in the sentence** — `reach` is a property of the skill and the question is a property of the claim, and the two are nearly orthogonal. Worse, the split puts *"`az graph query -o table` only renders summary columns and hides projected fields"* on the instruction side, where it is useless: the sentence is hard-won, verbatim, and dies with one Azure CLI release.

So `facet.py` asks how far the knowledge travels, in three levels — `bound` to a product or version, `tool-general` where the tool itself is one a practitioner keeps, and `transferable` where the claim survives its tool. A pilot of 200 splits 47/23/30, so the middle level is real and not a hedge.

Nothing new is read. Everything the judgement needs was written by pass 2 — and `drives` in particular, which names tools the summary never mentions in 85% of cases and is the *only* place they are named in half of all records. Feeding forty records with their summary, quote, quote_reason and `drives` costs a hundred calls; re-reading the directories would cost 3,957 to recover context already on disk. The escape hatch for records the context cannot settle fired twice in 200.

Translation rides the same call. It is additive: the English stays, because a located quote is the guarantee this corpus makes and a translation cannot carry it. `check()` enforces the mechanical half — code, flags, paths and numbers must survive into the Korean unaltered — and after two rounds of tightening its own false positives (`access/deletion` is not a path, `5s` becoming `5초` is not a loss) it reports **0 violations in 170 quotes**.

Two things had to be corrected before scaling:

- **A summary reads as transferable no matter what.** Asked to rate records with no quote, the pilot called 62% of them `transferable` against 43% of quoted records in the same `reach` band. Abstraction has no tool in it. `transfer` is now null where the quote is null — there is no checked claim to rate — while translation still covers every record.
- **A batch dies whole.** One record trips a cyber safeguard and its twenty-nine neighbours go with it; `facet.py` counted every written line as done on resume, which would have buried them as already-read. Only successful records count now. 2.7% of the corpus carries security vocabulary, spread across 64 of 132 batches, but one batch in eleven actually failed — most of that vocabulary is defensive. Those records get re-run in batches of five, and any that still trip it stay unprocessed and are marked as such rather than filed with the 637 that simply hold no quote.


## Reading the corpus: a few repeated problems and a very long tail

The corpus is an index, not a replacement — anyone writing a skill will open the original — so the question is which originals, and about what. Three stages, about seventy calls, over the 882 claims rated `transferable`.

**`topic.py` names what each claim is about, with no list to choose from.** 260811 handed a model seven `DOMAINS` regexes and assigned by first alphabetical match; `meta` fired on 66% of files and every bucket after `code` held leftovers. A category list is a hypothesis, and offering one gets it confirmed rather than tested. Asked instead to name the thing the author was dealing with — `retrieval chunking`, `judge panel convergence`, `crt.sh subdomain discovery gaps` — 881 claims produce **867 distinct subjects, 853 of them used once.**

That is the shape of the thing, and it matches every other distribution here: 1,648 identifiers named in quotes with 81% appearing once, 1,713 words across the subjects with 63% appearing once. This corpus is not a few topics. It is a handful of problems people keep hitting and an enormous tail of things one person hit once.

**The subjects were checked before they were used.** Re-running the naming with the claims regrouped into different batches — so no claim sees the same neighbours — 881 claims land on subjects that agree at **81%** by shared-word similarity, against **0.3%** for the same claims randomly paired. Median similarity 0.65 against 0.00. 18% are byte-identical. Most of what does not match is one subject said twice: `mock vs real API divergence` against `mocked tests masking integration failures`, `vacuous tests over empty loops` against `empty-array loop test assertions`. The subjects are in the corpus, not in the call.

**`cluster.py` groups them without a model,** because a model given 881 subjects would invent a taxonomy for them. Words are weighted by rarity — the commonest, `file`, appears in 31 subjects that share nothing else — and linkage is average rather than single. Single linkage is what a union-find gives and it chains: `concurrent plan file writes` to `file read context size` to `subagent dispatch context size`, and a cluster of fourteen forms that is about nothing. Average linkage leaves 121 clusters of two or more covering **281 claims, 32%**, the largest holding seven.

**`cluster_read.py` reads each cluster's claims and is allowed to reject it.** Lexical grouping puts five claims together because every subject ended in "false positives" — A/B testing, HLA typing, cloud storage exposure, subdomain takeover — and calling that a subject buries five real claims under a heading that fits none. Of 23 clusters with three or more claims, **6 came back "not a subject"**, each naming the word it had been grouped on. That is the same permission the repository pass has to say a collection has no thread, and it caught 26%.

The 17 that survived are what the corpus knows more than once:

| | what more than one source independently establishes |
| :--- | :--- |
| context window overflow | failures are silent — a legal memo drops 60% of a contract with no error, and degradation starts well before the limit |
| LLM-as-judge reliability | verdict-before-reasoning ordering and minor wording both move scores materially; a single run is unsafe, and a panel that loses one judge stops converging |
| automated a11y gates | passing axe does not mean the UI works; scanners catch 30–40% and miss focus order, alt-text quality, and visible render defects |
| premature completion | prose, a passing test, an opened PR are not evidence of done; agents default to declaring finished unless checked against a durable artifact |
| minimum sample size | naive N runs low by orders of magnitude, and below threshold the right move is to withhold the statistic rather than report it |

**No cluster contained a contradiction.** Zero across all 17, which is worth stating rather than passing over: it may be that three to seven claims are too few to disagree, or that the prompt saying `null` is the ordinary case discouraged looking. It is not evidence that these questions are settled.
