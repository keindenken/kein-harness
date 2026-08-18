# Where the justification for a standing rule lives

Stage 1, angle: the §3 / §6 contradiction. Grounded only in this repo, `~/.claude/kein/prompts/`, and `~/Documents/wiki/`.

---

## 1. Measurement: how much of `kickoff.md` is justification

**Method.** `reference/kickoff.md` is 1,724 words; the `## Discipline` section is 16 bullets and 1,554 of them (90% of the file). I partitioned every bullet into contiguous spans and word-counted them, with three labels:

- **I — instruction**: what to do or not do, including scope and conditions.
- **M — mechanism**: why the rule is true, stated causally and without a date ("that snapshot is captured when the session starts and never updates").
- **E — dated evidence**: incident narrative, almost always opening `Measured 2026-…`.

Spans were exact substrings, asserted present in the file, so the partition is reproducible; 1,538 of 1,554 words were covered (99% — the remainder is list markers and inter-span punctuation).

| label | words | % of Discipline |
|---|---:|---:|
| I instruction | 552 | 36% |
| M mechanism | 421 | 27% |
| E dated evidence | 565 | 37% |
| **justification (M+E)** | **986** | **64%** |

Nine dated clauses (`Measured 2026-07-26` ×5, `2026-07-28` ×2, `2026-08-05` ×1, one lowercase parenthetical), plus one undated dated-fact (`retired 2026-08-04`). Mean 63 words per incident.

**Two controls.**

- `reference/worker-brief.md`, the file the same author wrote for workers: 633 words, **zero** dated clauses. Same author, same week, opposite convention.
- `~/.claude/kein/prompts/lead.md`, the 2026-08-08 successor that replaced `kickoff.md`: 755 words, 10 standing rules totalling 388 words, split **52% instruction / 48% mechanism, zero dated incidents**. Mechanism averages 18 words per rule versus `kickoff.md`'s 63 words per incident.

**A correction to the owner's own figure.** The wiki note `_raw/note/260809-rewriting-standing-agent-prompts-on-measurement.md` records: *"Roughly 60% of kickoff.md's bytes were dated incident narratives."* That number is right for justification **as a whole** (my 64%) and roughly 1.8× too high for the dated part alone (37%). It matters, because it misattributes the diet. `kickoff.md` → `lead.md` was a 56% word cut (1,724 → 755). Deleting every `Measured` clause accounts for about a third of it. The rest came from deleting three rules whose *premise* the 2026-08-08 measurement falsified, and from compressing mechanism. If you apply the same diet to a prompt with no falsified rules, you get a third, not 60%.

---

## 2. Recovery attempt: can git alone tell me why a line exists?

**Result for the central exhibit: total failure, for a boring reason.** `reference/` is **untracked**. `git ls-files reference/` → 0. `git log -- reference/kickoff.md` → 0 commits. Git carries nothing at all for the file this whole discussion is about. The same note records the consequence already paid: the pre-rewrite `worker-brief.md` "now exists nowhere."

**For the tracked prompts, three honest attempts**, all on lines in `plugin/skills/execute/SKILL.md` that carry no inline reason, run as a person about to delete them would run them:

| line | `git log -S` result | useful? |
|---|---|---|
| "Do not create another durable report by default." | `04206fa feat(execute): port the code-development convergence loop` | no |
| "…cannot be extracted to another worktree for concurrency" | same commit | no |
| "Exclude earlier findings, verdicts, identities…" | same commit | no |

`04206fa`'s 134-word message is entirely about renaming a worktree lock from `codex-orca-execute-<uid>` to `kein-execute-<uid>`. It explains nothing about any of the three rules. Adding a path filter to attempt 1 made it *worse*: it returned `df35a31 refactor(plugin): move loadable sources under plugin/`, a pure file move.

**This generalises.** I ran `git blame -w -C` over all 20 SKILL/reference/agent files (19,953 non-blank words) and tallied words per commit:

| commit | words | share |
|---|---:|---:|
| `a6b46a52` render the fourteen roles as Claude subagents | 12,027 | 60.3% |
| `b0ea8085` port the requirements-clarification workflow | 1,688 | 8.5% |
| `04206fa3` port the code-development convergence loop | 1,423 | 7.1% |
| `98df33c0` port the consensus planning workflow | 970 | 4.9% |
| `b3707fc0` port the cross-vendor lane roster | 552 | 2.8% |
| **five bulk port/render commits** | **16,660** | **83.6%** |

For 84% of the standing-prompt corpus, blame and `-S` both land on a commit whose message discusses porting mechanics — a lock rename, a generation pipeline, a `sandbox_mode` decision — and says nothing about any individual rule. The port commit is a horizon: the reasoning, if it exists, is in a different repository.

**The counter-case, and why it still fails.** `7b3a350 docs(execute): stop requiring records nothing reads` is a 338-word message that is *exactly* the reasoning one would want, and closes with the owner's own doctrine: *"Each deletion leaves its reason behind. An absence invites the next reader to fill it back in; an argument does not."* But `git log -S` on the current text of the lines it touched does not return it. You find it only by searching for `:advisory` — a string that no longer exists in the file. **`git log -S` searches present text, and the reasoning you most need at deletion time is attached to absent text.** A deletion's argument is structurally unreachable by the search a person would think to run.

And note what that commit actually did: it moved the reasoning **into** `plugin/skills/execute/references/lanes.md`. One table row was deleted; a three-sentence paragraph explaining the absence was added. The file got longer as the result of a cut. The author, on 2026-08-09, did not trust his own commit message to carry it — which is the strongest available evidence about whether commit messages work as a home. Commit messages here are unusually good and they are still not the answer.

**Verdict on git: it is a good archive and a bad index.** It survives, it is honest, it is where a long argument can live without costing attention. It has no retrieval path from the line to the argument.

---

## 3. The wiki as third home

**The delivery mechanism exists and I watched it fire.** `~/.claude/rules/wiki` is a directory symlink to `~/Documents/wiki/_rules`, and `_rules/authoring-claude-md.md` carries `paths: ["**/CLAUDE.md","**/CLAUDE.local.md","**/AGENTS.md","**/SKILL.md","**/.claude/rules/**"]`. During this task it injected itself, unasked, at the moment I read `plugin/skills/execute/SKILL.md`.

That is a live result for an open question the owner logged himself in `decisions/2026-08-03-vault-rules-via-symlink.md`: *"Whether a path-gated rule actually fires on a match was not tested directly."* It fires — on **read**, not just edit, and inside a **subagent**. Worth telling him regardless of what else comes out of this stage.

**But the content is not there.** The pointer names a general context-engineering note. It has nothing to do with any specific rule's provenance. And the material that *would* answer "why is this line here":

- `_raw/note/260809-rewriting-standing-agent-prompts-on-measurement.md` is `status: uningested` and appears nowhere in `index.md`.
- 8 of 18 `_raw/note/` files are uningested.
- `decisions/` contains exactly **one** page.
- Links run one way. Wiki notes name `kickoff`, `reference/kickoff.md`, `worker-brief.md` by name. The reverse does not exist: **0** of `kickoff.md`'s 16 rules link to a note, and the only wiki mention in the entire harness prompt corpus is `kickoff.md:31` telling you to *run* `/wiki-record` — a write pointer, not a read pointer.

So the vault today is the same failure as git wearing a nicer coat: the reasoning is genuinely there, in better prose than git has, and nothing at the deletion site points at it.

---

## 4. The criterion

**First, the finding that reframes the question.** §6 predicts that a rule carrying its own argument makes removal ordinary review. `kickoff.md` carries more argument than anything else measured here — 64% justification, 9 dated incidents — and §1 of the same note records that it *"still had no line anyone could argue for cutting."* **The inline-argument hypothesis is falsified by the note's own central exhibit.** When the deletions finally came, on 2026-08-08, they came from a *measurement that falsified the mechanism* (messages do not queue with teams off; a background subagent's final text does reach the lead), not from anyone reading the dated clauses and judging the rule spent. Three rules died because their causal premise was disproven from source. Zero died because their receipt looked stale.

That splits "justification" into three things that behave differently, and the split is the criterion:

**(a) Mechanism — inline, one clause, undated.** "Your edit vanishes with no conflict and no error when the lane next rewrites from its own context." This is not archive material; it is part of the instruction, because it is what lets an agent apply the rule to a case the rule did not name — the owner's own formatter example. It also does §6's job on its own and better than provenance does: a mechanism can be *checked from source and disproven*, which is what actually killed three rules. Cost is bounded: `lead.md` pays ~18 words per rule, once, forever.

**(b) Provenance — outside, always.** Which incident, what date, what it cost. It is the only term that grows without bound: one narrative per occurrence, ~63 words each, forever, and §2 of the note already establishes that it cannot settle removal anyway (a past cost does not predict a current one, and absence of recurrence proves nothing). Worse than useless at the deletion site: a dated receipt makes a rule *harder* to delete by making it look adjudicated. Its one real job — confirming the rule was empirical rather than invented — is a one-time audit question, not a per-read one, and can afford a lookup.

**(c) Environment facts — inline but quarantined, dated as a block.** `lead.md` already invented this and it is the sharpest move in the rewrite: a `## Harness facts` section, one collective date, a tool version, and *"These are the lines most likely to rot; check them before trusting them."* The date attaches to the **fact**, which perishes, not to the **rule**, which does not. This is why the owner's instinct that dates made the prompt heavy is right in general and wrong in one place: the date on a harness fact is load-bearing.

**Reconciliation of §3 and §6:** §6 is satisfied by (a) and does not require (b). §3's attention cost is paid almost entirely by (b). The criterion cuts exactly the unbounded term and keeps the one that both explains and enables deletion. Applied to `kickoff.md` it predicts a 37% cut with no loss of deletability — and `lead.md`, which the owner built independently, sits exactly where the criterion says it should (52/48, zero incidents, facts quarantined and dated).

**Where (b) then lives, so it is found at the moment of deletion.** Not a new mechanism — the one that already fires. `~/.claude/rules/wiki/authoring-claude-md.md` triggers on `**/SKILL.md`, `**/CLAUDE.md`, `**/AGENTS.md`. Adding one sentence to that rule naming where this project's rule provenance lives costs **zero words in any standing prompt**, because a path-gated rule file is not a standing prompt: it loads only when someone opens a prompt file, which is precisely the moment of deletion. It is the only candidate in evidence that is *pushed* rather than pulled, and pushed is the whole requirement — a commit message needs someone to think of `git log -S`, a document needs someone to think of the document, and this needs nothing.

Two things it does not do, stated plainly: it is **per-file, not per-line** — it can say "provenance for this file's rules is at X", never "this line came from the 2026-07-28 `dryRun` incident"; and it fires on **opening the file**, so a deletion decided in conversation, or from `git log`, or from a grep hit, never sees it. Per-line attribution has no mechanism in any evidence I found.

---

## 5. What I could not ground

- **Whether anyone has ever run `git log -S` on a prompt line while considering a deletion.** No evidence either way. My three attempts are the only data, and they are mine, not the owner's. The whole case against git rests on a retrieval path that may be hypothetical in both directions.
- **Whether mechanism-only actually preserves deletability.** `lead.md` is two days old and no line has been deleted from it. The criterion is derived from a revision, not tested by one. It could turn out that a reader says "I can see why it's true, but I have no idea whether it still matters" and has to go looking anyway — in which case (b) has to come back inline and §3's cost has to simply be paid.
- **Whether dropping the dated clauses changes compliance at all.** No `ocs eval` comparison of `kickoff.md` vs `lead.md` exists; the note records that nothing loads the new prompts except two shell commands, and §5 of the source note argues this cannot be measured at n=1 regardless.
- **The `paths:` firing is n=1.** One observation, in a subagent, on read. I did not test Edit, a non-matching path, cross-session reliability, or whether it fires when several rules match.
- **The port horizon.** 84% of the prompt corpus was written in another repository I did not open. Its history may contain per-rule reasoning that would change the git verdict for that material — though not the retrieval problem, since `-S` cannot cross the port commit either way.
- Per the boundary: no external prompt-writing material, no `~/.claude/plugins/`, no web. `lead-omc.md` was counted but not read closely.

**What would change my mind**

- A case in this repo where `git log -S` on a current prompt line returns a commit that explains it, for a line *not* touched by a later reasoned edit. That would undercut the 84% blame finding and put git back in contention.
- A deletion round on `lead.md` that stalls on "I can't tell if this still matters" — that shows mechanism alone does not discharge §6 and provenance belongs inline after all.
- A path-gated rule failing to fire in one of the owner's real editing sessions. The push mechanism is the entire load-bearing element of the recommendation; if it is unreliable, the answer collapses back to "inline, and pay the weight," and the honest form of that is (a) inline plus (b) as one dated parenthetical, which is roughly where `kickoff.md` already was.
- Evidence that the three rules deleted on 2026-08-08 were found *because* their dated clauses made them auditable, rather than because a separate measurement falsified them. That would rescue §6's original claim, and I inferred the causation from the note's narrative rather than observing it.
