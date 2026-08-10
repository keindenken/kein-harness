# What a public skill corpus contains

Collected 2026-08-11 to answer a question `docs/prompt-revision.md` could not answer from inside this repository: what do people who write standing prompts know that is not derivable, and does the premise that prompts grow monotonically survive contact with a corpus.

## What was collected

`harvest.py` searched 13 repository queries, kept 579 repositories at 3 stars or more, read every path in each from the git trees API, and fetched 4,659 `SKILL.md` files. `triage.py` deduplicated and scored them. `dispatch.py` sent a 640-file stratified shortlist through `codex --model gpt-5.6-luna`, one record per file. `history.py` made blobless clones of the 244 shortlisted repositories, counted commits per path locally, and extracted 64 full revision histories. `growth.py` measures those histories.

Regenerate with `./harvest.py all && ./triage.py && ./dispatch.py select && ./dispatch.py run && ./dispatch.py collect && ./history.py clone && ./history.py rank && ./history.py diffs && ./growth.py`.

What is committed is what a claim below rests on. `classified.json` holds the model's reading of each shortlisted file, `growth.json` every commit's subject and added and removed line counts, `history.json` the revision depths, `shortlist.json` the sample frame, `repos.json` the search result, and `corpus-stats.json` the aggregates that would otherwise only exist inside the three large intermediates. Those three — `files.json`, `index.json`, `triage.json` — along with `corpus/`, `diffs/`, `results/` and `.cache/`, are gitignored: the scripts rebuild them, and 2.6 GB of blobless clones does not belong in this repository. The consequence is real and worth stating: re-running `harvest.py` later will not reproduce this corpus exactly, because the upstream repositories keep moving.

## The corpus is not what its size suggests

61,889 `SKILL.md` files exist across 434 repositories with any. The median repository holds 9; the largest holds 23,793. **Skill count per repository is an inverted quality signal** — a person writes the first number and a generator writes the second — so repositories at or under 50 were taken whole and larger ones sampled to 12.

Near-duplicate clustering removed only 7% (4,659 to 4,336), and the largest cluster is 11 files. The corpus is not people copying each other's text. It is people independently writing files that converge on the same structure, which is the same result an earlier reading of two vendor corpora reached from the other direction: unanimous on shape, silent on evidence.

## Prompts grow, and commit messages lie about it

Over 64 revision histories, 1,786 commits changed at least one line of a `SKILL.md`.

- 1,031 net positive, 215 net negative, 540 net zero. Median net per commit: +2.
- 57,462 lines added, 25,718 removed. **Removal happens at 45% the rate of addition and never enough to shrink a file.**
- **0 of 64 files ended smaller than they started.** Not one.

So the premise holds, and it holds despite deletion being routine. The failure is not that nobody deletes — it is that nobody deletes more than they add.

The sharper result is about recovery. 218 commits claim a cut or a simplification in their subject line; **90 of them (41%) are actually net negative, and 61 are net positive.** `garrytan/gstack`'s `v1.0.0.0 — simpler prompts` is **+163/−0** in `design-review/SKILL.md`. `docs/prompt-revision.md` already lists "commit messages are where the argument lives" as false because `git log -S` finds present text; this is worse than that. Searching commit messages for removals does not merely miss them, it returns additions more often than not.

The real cuts have three shapes and only one of them is a removal:

- **A budget enforced by a re-run process.** `refactor: trim oversized SKILL.md files to the <=520-line discipline` is −579 in one commit. This is the one dilution control in the corpus with a large effect behind it, and it matches what `docs/prompt-revision.md` says about budgets: it held because a line count is checkable, not because anyone argued.
- **Relocation, not deletion.** `extract content to reference files` (−142), `move check and health mode bodies into references` (−118). The obligation moves down a level; the run still reads it.
- **An external surface authorising the removal.** `remove ALL non-standard fields from SKILL.md - match Anthropic official format` (−111). Someone else's spec changed and made the deletion not the author's decision.

Those last two are exactly the two escapes from "testing whether a rule is needed means violating it", and both now have live instances rather than being reasoned about.

## The off-switch exists, unmeasured, three layers deep

`gstack`'s `v1` release added a Writing Style section and shipped it with a config key (`gstack-config get explain_level`), a one-time migration flag file, and this:

> **User-turn override.** If the user's current message says "be terse" / "no explanations" / "brutally honest, just the answer" / similar, skip this entire Writing Style block for your next response, regardless of config.

`docs/prompt-revision.md` says the off-switch affordance exists elsewhere and that none of them connects it to measurement. Confirmed, with a stronger instance than expected: the third layer hands the switch to the population the rule is imposed on, per turn, and nothing anywhere counts how often it is pulled.

## One repository measures its own prompts

Of 4,659 skills, 58 mention an eval or benchmark artifact, 43 mention a repeat count, and 14 make a first-person measurement claim. Of those 14, one measures the skill rather than the skill's subject matter.

**`trailofbits/skills`** carries per-plugin `evals/<case>/{case.yaml, fixture/, graders/*.md}` and a runner at `plugins/variant-analysis/tests/eval.sh` with `workflow` and `baseline` arms. Its `spec-to-code-compliance/SKILL.md` states its own result inline:

> Measured on the `routes-not-inline` eval: with this plugin installed the work is dispatched every run, without it never — Δ +1.00. Deleting this section while leaving the workflow in place changes nothing, because the workflow is a real commitment.

That second sentence is a removal warrant written by the author, in place, addressed to whoever later considers the deletion. It is `docs/prompt-revision.md`'s "unnecessary by construction, because a mechanism now holds it" as a standing annotation rather than as an argument.

Four things from it bear directly on `.agents/kein/requirements/260810-skill-measurement-program.md`:

- **A turn budget is not neutral between arms.** From `audit-context-building/evals/dispatches-not-inlines/case.yaml`: *"The skill reads three reference files before it starts, so it needs roughly twice the turns a bare agent does on this prompt. At max_turns 20 the plugin arm was truncated before it answered, which scored as a routing failure."* The 2026-08-04 program recorded `with-skill` killed at a 2400-second timeout after 238 turns and read it as cost. It may have been this confound. A cap calibrated on the control scores the treatment as a failure, and the failure looks like the skill not working.
- **A grader fixes its target defect and rules out other true findings.** `name-is-not-evidence/graders/senior-branch-unenforced.md` enumerates four near-miss responses as failures, then: *"Other true findings — the operator zeroing a balance in `reassign` against §4, the external call to `feeSink.record` before the event … — are fine but do not by themselves satisfy this grader."* This is the answer to the constraint recorded in `kein-open-threads`: variance in *which* defect a run happens to find measures the model, so a grader that admits any true finding measures the model too. Fixing the target removes that variance from the score without scoring severity.
- **A grader pre-authorises the reasonable objection.** The same file allows a specific competing reading of the spec and states it does not fail the grader provided the divergence is still reported. An assertion that has not decided this in advance gets it decided per run.
- **An expensive eval is named to escape the CI glob on purpose,** and a failing run keeps its work directory while a passing one deletes it. Retention keyed to outcome, because a failure is when the transcript is worth reading.

`evals/` sits inside the plugin there, which independently arrives at the placement decision `260810-skill-measurement-program.md` argued for and expected to be argued against.

## What the deeply-revised files answer

Revision depth and the specificity score agree — files with 20 or more commits have median specificity 73 against 49 for files with 2 or fewer — but they rank differently. Specificity surfaces domain API facts. Revision depth surfaces process skills. The nine most relevant, with commit counts:

- **`understand` (56)** — when the project is in a git worktree, output must redirect to the main repository, because worktree data is ephemeral. `ocs team` resolved *where a lane runs*; this is the adjacent decision about *where its artifacts land*.
- **`academic-paper` (48)** — writer and evaluator calls are physically separated so each pre-commitment is paper-blind. The UNPRIMED instruction enforced by process rather than by prose.
- **`openloomi-loop` (47)** — classifier rules are enforced twice, once in the prompt and again server-side after decisions are written. "Prompt or mechanism" answered with both, deliberately.
- **`design-review` (79)** — filesystem paths in a plan are classified DONE or NOT DONE by checking existence; UNVERIFIABLE is reserved for genuinely abstract claims. A reviewer default that rations its own escape hatch.
- **`review` (104)** — the cross-vendor structured review runs only for diffs of 200 lines or more, the adversarial review always runs, and adversarial findings never block shipping. Three separate decisions this repository has open.
- **`academic-paper-reviewer` (37)** — a CRITICAL finding cannot be silently ignored: unresolved blocks Accept, and rejecting one requires visible rationale. A third answer to whether a PASS carries an artifact — asymmetric, requiring the record only on dismissal.
- **`planning-with-files` (80)** — after every two view, browser, or search operations, save findings to files. A context-preservation cadence keyed to operation count rather than to token count.
- **`writing-skills` (24)** — *"Testing found that workflow summaries in descriptions can cause agents to perform one review when the full skill requires more."* A measured effect of description text on behaviour, which is the trigger-text question with an observation attached.
- **`ship` (117)** — if code changes after the test run, prior output is explicitly stale evidence and the suite must be rerun.

One convergence worth recording because it is the same defect: `fix: resolve codex exec -C repo root eagerly to prevent wrong-project reviews`. A cross-vendor call whose working directory resolved late, and therefore reviewed a different project. `ocs team` shipped `--worktree current` reading Orca's focused worktree while the state root came from `$PWD`, fixed in `be6f216`. Late working-directory resolution in a cross-vendor launch is a defect class, not an accident.

## Where the non-derivable content actually is

Overwhelmingly in domain API behaviour, not in prompt craft: Unity's multi-hit physics queries are not distance-sorted; Search Console totals are a separate aggregate because query rows omit anonymised traffic; Stata treats numeric missing as greater than every number, so `income > 50000` silently includes it. Rich, real, and mostly irrelevant to how a prompt should be written.

The exception is a technique rather than a fact. `rossmann-voice` derives a style specification by **measuring a corpus instead of asserting rules**: 513,683 words, 28,005 sentences, a contraction rate of 83.6% reported with its across-year range of 77–89%, and drift detection stated against those numbers. A voice specified this way is falsifiable against its own source. That generalises past writing.

For the domains this harness has no skill in, the corpus offers shapes worth stealing rather than content: `define-prioritization-framework` refuses to run a method when its inputs are absent (Kano without customer research, RICE without quantitative inputs) rather than running it badly; `site-visit-report` requires "Not observed" and forbids "no issue observed" for any area that could not be reached, which is `docs/prompt-revision.md`'s "absence of failure is not a warrant" arrived at independently and enforced as vocabulary; `systematic-literature-review` caps retries at one search and pre-empts the rationalisation — *"do not retry with modified queries, even if results seem imperfect."*

## What this does not establish

- **The model's `worth` score does not discriminate.** The top band scored 2+ at 91% and the control band at 85%, which is not a difference. Ranking here comes from the specificity heuristic and from revision depth, both computed locally; the model's contribution is the `claim` field and nothing else. Do not reuse `worth`.
- **The growth measurement covers 64 files, all of them selected for being heavily revised.** It says prompts that get maintained grow. It says nothing about the ones that were written once, which are the majority.
- **41% of simplification claims being honest is a property of these 64 histories**, and the classifier is a keyword match on subject lines that counts `refactor` as a simplification claim. Re-derive from `growth.json` before quoting it elsewhere.
- **`trailofbits/skills` was not read in full.** Four files were. Whether its eval harness works is not established here; what is established is that it exists and what shape it has.
- The search reached what GitHub's repository index surfaces for 13 queries, sorted by stars. A skill nobody starred is invisible to it.
