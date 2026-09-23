# fsd test run — descvi remaining-KI batch (2026-09-22)

Run: descvi `.agents/kein/runs/fsd/260922-010759-ki-remaining/state.json`. Requirements: `.agents/kein/requirements/260922-ki-remaining.md` (7 KIs, one plan with per-KI sections, execute with codex executor and reviewer). Issues and inefficiencies are appended as they happen.

## 1. Interview stage not linked when the ledger validation shares a Bash call

- What happened: I ran `ocs validate interview ledger <path>` chained with `&&` after the heredoc that wrote the ledger, and later chained it again with the ledger collapse. The hook never linked the interview stage (`status` → `association: none`). After the collapse, `ocs state fsd attach <state> interview <ledger>` refused (`must be a live run of this flow`), and `gap` answered `no gap` rather than naming the missing link — a silent dead end.
- Workaround: rewrote the ledger as active, ran the validation as its own Bash call (linked: `association: kept`), then restored the completed receipt.
- Suggestions: (a) have `gap` report "interview entered but unlinked" instead of `no gap`; (b) let `attach` accept a completed ledger whose `requirements_path` resolves inside the worktree; (c) the skill text says "each as its own Bash call", but the reason (the hook reads only single-command calls) is easy to miss — say it next to the interview's own validate step.

## 2. ralplan over a 7-KI batch: one story keeps generating the blocking findings

- Rounds 1–3 all ended BLOCK. Of the blocking grounds, KI-49's story (S5, pull the baseline at gesture arm) produced one in every round, each a new facet of the same design: round 1 the three generation comparisons and the spacing path, round 3 the dirty-draft settlement re-key and the `preview.select(` choke-point invariant. The other six KIs converged by round 2–3 with REVISE-level findings only.
- Cost: each round is two fresh ~200k-token native lanes plus a ~200k planner revision, and the whole plan (400–500 lines) is re-reviewed each time because one story moved.
- Inefficiency: the gate has no way to approve the converged stories while one story iterates. Splitting the story out means editing the plan (new review hash, new round) or a second ralplan run, which fsd's single linear ralplan stage does not model.
- Lead decision (logged here, applied if round 4 blocks S5 again): move KI-49 to its own plan and approve the rest, rather than letting one contested story hold six settled ones.
- Suggestion: let ralplan approve per story (per-section review hashes), or let fsd queue a follow-up ralplan/execute pair for a split-out story instead of forcing it into the same linear run.

## 3. ralplan hit the round-5 exit; the fsd deferral path worked but the plan still carried a real evidence gap

- Round 4: critic BLOCK (S3's restore helper would reload the page mid-row and erase S5's stale condition). Round 5: architect BLOCK on S7 (the heartbeat false-positive count had no collector, no planted verdict, no ping exposure), critic REVISE. Five rounds, each ~600k tokens across planner + two lanes.
- fsd's decision policy handled it cleanly: `fsd assume` (A1) + a deferral with `caught_by: fsd assumption A1; execute final audit` + `ralplan approve --findings`. The approving Status line carries the deferral and the carried REVISE list.
- Observation: blocking grounds migrated across stories (S5 → S3/S5 seam → S7) as each was fixed; a 7-KI plan offers a large surface, so "about five rounds" arrived mostly because of breadth, not because one design was contested. Per-story approval (see item 2) would have cut this.

## 4. `gap` treats the lead's own earlier execute run as "another operator's"

- After ralplan approved, `gap` refused to name execute: an execute run from this same lead's session three days earlier (`260919-103258-ki-49-stale-baseline-batch`, lifecycle active because one task had been split off and `park` had refused it) still claimed the worktree. The printed action was the abort command, framed as "decisions for whoever owns that occupant".
- decision-policy says never abort another operator's run; there is no notion of "same operator, earlier session". I verified its tasks had landed and its split task was preserved on a pushed branch, recorded fsd assumption A2, and aborted it.
- Root cause upstream: `ocs state execute park` refuses a `correcting` task whose scope changed since dispatch (a rebase legitimately changes it), so a split-off task leaves its run permanently active. Suggestions: let `park` accept a task whose scope diverged because of an upstream rebase (with a reason), and let fsd show the occupant's owner/session so the lead can tell "mine, stale" from "someone else's".

## 5. The session went silent for ~8 hours: a turn ended with no tool call while a background lane was "waiting"

- After S1's acceptance I ended a turn with a status message and no tool call, expecting the M53 measurement agent's completion notification. The agent had itself parked on a Monitor after run 2 and stopped; no notification ever arrived. The run sat idle from ~03:01 to ~10:42 KST until the owner noticed ("중간에 툴 호출 없이 턴이 종료돼서 또 끊긴 것 같은데 이런 실수하면 조용히 루프가 끊김").
- Two failures compound: (a) a lead turn that ends without a tool call in an unattended fsd run ends the run; (b) a native measurement subagent that delegates its own waiting to a Monitor can return an "interim" result and never resume.
- Fix applied: the lead drove M53's remaining runs itself in the foreground, one `pnpm test:e2e:record` per call.
- Suggestions: fsd hooks could refuse (or warn on) an end-of-turn with no tool call while the flow is active and not in `report`; measurement briefs should forbid Monitor-parking and require the lane to run its runs in the foreground to completion; a returned "interim" subagent result should be treated as a failure to finish, not as progress.

## 6. M53 took four verifier rounds on a measurement document

- Round 0: REVISE-shaped findings that actually cited the completion condition (the codex verifier writes `VERDICT: REVISE` while its findings name a clause, which the state refuses as REVISE; the lead must re-classify it as BLOCK), and one cited clause was not verbatim, so the correction checkpoint was refused silently because the lead piped the checkpoint through `tail`. Cause of the underlying finding: the first 12 runs had no per-run process attestation. Fix: a full re-run (~75 min) with an attesting wrapper.
- Round 1: the lead's own generated table mislabelled `signal` as `exit` (a column-index slip). Round 2: missing sha256 for some cited records, wrong run-dependent ordinals, and "idle" not qualified as edge-attested. Round 3: PASS.
- Inefficiency: most rounds were spent on record-keeping details, not the measurement. Suggestions: have the measurement brief ship a record manifest generator and an attestation wrapper from the start; have `ocs ask` reject a response whose verdict word contradicts its `Blocks` fields instead of passing it to the lead; never pipe `ocs state execute checkpoint` output (a lesson this lead already had in memory and still slipped on through a helper's `| tail`).

## 7. A handoff snapshot inside the run directory turns the repository's citation gate RED

- The plan's Playwright-handoff protocol (§2.6) put partial-tree copies of source files under the gitignored run directory (`.agents/kein/runs/<run>/handoff/<story>-<k>/…/OverlayShell.tsx`). descvi's `scripts/check-citation-anchors.mjs` resolves anchor basenames over the whole working tree, gitignored files included, so the copy made `OverlayShell.tsx` ambiguous and the gate went RED.
- Fix applied: snapshots now live outside the repository (`/Users/kein/Documents/workspace/dev/worktree/repo/ki-batch-handoff/`).
- Suggestion for kein: when a skill or a plan asks for source snapshots, put them in a scratch directory outside the worktree by default; a gitignored path is still inside every tool that walks the tree.

## 8. S4 (KI-10) review ran five rounds; each blind round surfaced the next layer of missing proof

- Round 0: missing vitest row groups (critical), snapshot identity, the live multi-select check, stale comments. Round 1 (lead): closure text. Round 2: a missing index-shift row, stale expected-failure docs, two branches with only missing-export REDs. Round 3: the pre-op capture's only RED attempt had stayed green (the executor had said so in its own report, and no later brief picked it up), plus two comment slips. Round 4: pending.
- Causes: (a) the plan's row list was long, and the codex executor twice ended a dispatch "partial" (ocs team `status=failed`), leaving items the lead had to re-brief; (b) a codex report that says "this RED is not valid evidence" is easy to lose between rounds unless the lead re-reads every report line; (c) blind reviewers sample different parts of a large diff each round, so a complete row-to-RED map is only achieved incrementally.
- Suggestions: have the executor report emit a machine-readable row→RED-log table the lead can diff against the plan's row list before review; have execute track "known-invalid evidence" items across rounds so a reviewer does not have to rediscover them; for stories with >10 required rows, split the story (plan-time) so each review surface is small.

## 9. S5 (KI-49): codex team lanes time out on large stories, and the story's own verification path missed two regressions only the commit gate caught

- The codex executor (`ocs team`) ended four of the first five S5 dispatches with `status=failed` after 430–600 s, each self-reporting "partial". The first one wrote production code before any regression row, against the brief's rows-first instruction. The lead split the story into steps (rows+RED, implementation, e2e port, corrections), which worked but cost many dispatches.
- The codex lane cannot run Playwright or the full vitest runners (sandbox EMFILE). Two e2e-dependent corrections were moved to native executors, which lanes.md allows but which the owner's "codex for implementation" instruction had not anticipated.
- The story's verification path named six vitest files and two e2e specs. The commit gate's full runners then found (a) four mounted-shell vitest rows stuck in `armed-pending` (a real product bug: a none→element selection never wrote its baseline snapshot, so every real arm would have taken the slow path) and (b) `panel-focus` gate 4 losing a chip draft. Six review rounds had passed without either, because neither lane runs the full suite.
- Suggestions: for a story that changes a shared session hook, have the plan's verification path include the full package runner (it takes ~1 min here) rather than a hand-picked file list; give `ocs team` a configurable timeout, or have it checkpoint partial work in a structured way the next dispatch can resume from; make the executor refuse to edit product files before the brief's RED log exists when the brief says rows-first.

## 10. S6 (KI-19): the codex executor lane could not run the real browser, and the jsdom-green fix was wrong in the browser

- **What happened:** the codex team executor delivered S6's fix and its e2e row but, per the codex-cannot-run-Playwright constraint, did not run the row. The lead ran it: 3 of 3 failed on the fixed tree. A native `kein:executor` found why (Vite HMR reaches the page before the POST response, so the hold armed in the response handler was too late) and moved the arm point. Its report also said "report exists and the dispatch has not settled" — the codex team lane wrote its report without signalling completion, so the lead had to read the report file rather than trust the lane's exit.
- **Cost:** one extra native executor dispatch and one extra lead e2e cycle, plus a lead pass to unwrap hard-wrapped comments that the native executor's correction reintroduced (the codex lane had passed its own no-wrap proof).
- **Suggestion:** for a story whose completion condition names an e2e row, `execute` could route the executor lane to a runtime that can run it (native) by default, or require the brief to split "write the row" (codex) from "run the row and fix what it finds" (native) as two steps. The no-wrap proof belongs in every executor's report, including correction-round executors.

## 11. The whole-set audit needed four passes, and three of them found only convention breaches

- **What happened:** S8's final audit over a 13-commit stack ran four times. Pass 1 found three claims the code did not support (a comment promising no stale node, a comment calling an event proof of a dead channel, a file header saying "zero timers" above a timer). Pass 2 found a hard-wrapped comment block inside an injected browser-script string literal and a line-number citation in a research file that the citation gate's own line-pin leg does not scan. Pass 3 found that the lead's unwrap script had missed the numbered list items inside that same string, and that the commit message claimed otherwise. Pass 4 finally found a substantive defect — a second post-navigation bare click in the row KI-53's fix was about — plus one more comment overstatement.
- **Cost:** four audit lanes plus four commit-gate cycles, for what was substantively one finding class (claims outstripping code) and one real defect.
- **Suggestion:** the lead sweep before pass 1 should be mechanical and exhaustive rather than eyeballed: decode string literals, diff every added comment for sentence continuations, and re-derive every claim sentence in a comment or register entry against the symbol it names. Passes that find only convention breaches are passes the lead could have spent. Worth noting the ordering effect too: the cheap breaches crowded out the real defect until pass 4, so an audit brief that says "report the substantive findings first, and the convention sweep as an appendix" would surface the expensive item earlier.

## 12. The whole-set audit did not converge: twelve passes, and the last four each raised a NEW claim

- **What happened:** S8's final audit ran twelve times. Passes 1–3 found claims the code did not support and convention breaches. Pass 4 found a real defect (KI-53's second bare click). Pass 5 found two more (the ring-hold token stolen by a non-insert op; the missing KI-53 witness). Pass 6 found the heartbeat's uncorrelated pong. Pass 7 found the edit-map writers unordered. Pass 8 found the ordering rule did not cover the bridge's own fetch. Pass 9 broadened that claim. Pass 10 falsified pass 9's broadening (the commit serializer rules it out) — and the lead had already applied pass 9's prescription without re-deriving it. Pass 11 found two register texts that lagged the corrections. Pass 12 found a new defect in the KI-19 hold (an unrelated selection loses its ring while an insert POST is pending).
- **Cost:** roughly half this run. Each pass was one lane plus a commit-gate cycle; several also cost an executor dispatch and 2–6 review rounds.
- **What worked:** the defects found from pass 4 on were real, and three of them were shipped bugs no row could see. The audit is earning its keep on substance.
- **What did not:** there is no stopping rule, and no distinction between "this pass confirms the last one's fixes" and "this pass opens a new line". A fresh blind lane over a growing diff will keep finding new claims indefinitely, because the diff keeps growing with the fixes. Two compounding failures: a lane's prescription was applied without re-derivation (pass 9 → pass 10 had to falsify it), and the lead kept opening new tasks at the tail of the run rather than registering findings for a later one.
- **Suggestion:** give the final audit a contract with a stop: pass N+1 sees the PREVIOUS pass's findings and their dispositions and is asked only (a) are these dispositions sound and (b) is there a defect of a class not yet raised — and anything new after the second pass is REGISTERED as a known issue by default rather than fixed in the same run, unless it is a regression the run itself introduced. That is what the lead ended up doing by hand at passes 9–12, several thousand tokens late.
