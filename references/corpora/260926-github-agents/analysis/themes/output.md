# Output dimension: recurring themes

Source: `claims/output.jsonl`, 654 quotes from 505 distinct records, 413 repos, 398 owners (owner = the repo part before `/`).

## Method

- I read all 654 lines (quotes shown up to 300 characters, with full text pulled for every quote cited here). Nothing was sampled.
- I assigned each line to zero or more themes by hand, by line index. The assignment is in `analysis/themes/output.assign.json`: keys are theme codes, values are 0-based line indices into `output.jsonl`. A script computed every count from that assignment. 491 lines went into at least one theme and 163 went into none (mostly one-off content lists, tool quirks and domain templates).
- A line can belong to several themes. For example, "files changed + unverified + evidence" counts toward three.
- Counts are distinct records / distinct repos / distinct owners. Doc-type concentration names the most frequent types and their lift, which is the type's share inside the theme divided by its share across all 654 lines. Lift is shown only when the type has 3 or more lines in the theme.
- There was one coder and no second rater, so a theme's edges are judgment calls. The ordering by owner count holds up better than the exact numbers.

## 1. Top recurring themes (ordered by distinct owners)

### 1. Write to a fixed, prescribed path and filename pattern
The deliverable goes to a named location with a set naming convention (date prefix, kebab-case slug, sequence number).
- Counts: 112 records / 93 repos / 92 owners
- Doc types: project-docs 38, prd-spec 36, report-analysis 36. Relative concentration in fiction-narrative (1.9x) and prd-spec (1.7x).
- "Save the PRD to `docs/prds/<feature-name>.md` (kebab-case the feature name)" — c00294
- "Generate a markdown file with the naming format `YYYY-MM-DD-descriptive-name.md`" — c00900
- "Your sole deliverable is one Markdown file under `/specs/` (or, in delta-spec mode, `/specs/<NNNN>-<slug>.delta-<NN>.md`) that conforms to `docs/spec-format.md`." — c01262

### 2. Completion report lists the files changed, one line each
The final message lists every file created or edited, each with a one-line summary.
- Counts: 57 records / 55 repos / 53 owners
- Doc types: project-docs 49 (1.9x), api-reference 21, code-comments 12 (2.5x). prompt-instructions 6 lines (5.0x).
- "Report back briefly with the files you changed, one or two sentences about each, and any open questions or facts you could not verify. Do not repeat the prose in your report." — c01209
- "Return: per file, a one-line summary of what changed, plus any skipped brief items with the reason." — c00963
- "Report back: which sections you updated, one line each, plus anything you found stale but out of scope." — c01129

### 3. Report what remains open: unverified claims, gaps, skipped items, open questions
The return names what was not verified, not done, or still needs a human.
- Counts: 39 records / 39 repos / 38 owners
- Doc types: project-docs 27 (1.6x), api-reference 10, prd-spec 6
- "Report back: pages written or changed with a one-line summary each, any claims you could not verify, and every deviation with its reason." — c00651
- "a **"Verify — possibly inaccurate"** list of anything you left untouched because it needs a human/technical check." — c01028
- "Return: the drafted or regrounded document, the findings-note lines, the unknowns entries, and a coverage line stating what you checked and what you did not" — c01283

### 4. The file on disk is the deliverable, and the reply is only a pointer
The agent writes the file instead of describing it, and does not echo the content back to the caller. This merges two sub-patterns:
- "write, don't describe": 16 records / 16 owners
- "thin return (path, one line, or confirmation only)": 31 records / 23 repos / 23 owners

Merged counts and doc types:
- Counts: 42 records / 34 repos / 33 owners
- Doc types: report-analysis 23 (2.1x), project-docs 21, prd-spec 10
- "Write the file immediately — create it now; NEVER describe what you would write — why: a described entry is a lost entry" — c01601
- "Never return the drafted content in your reply." — c00710
- "Reply with just the path of the note you wrote or updated, and a one-line summary. The caller has the full context already - do not restate the work back to them." — c01201

### 5. Output only the deliverable: no preamble, narration, commentary or internal notes
This includes a sub-pattern: working notes, annotations, provenance ids and reasoning must stay out of the deliverable text (8 records / 7 owners).
- Counts: 28 records / 26 repos / 25 owners
- Doc types: project-docs 10, prd-spec 9 (1.8x), other 7 (2.4x), fiction-narrative 4 (2.6x)
- "Return only the requested markdown. No preamble, no postscript, no "I'll now..." narration." — c00112
- "Emit the report body only — no preamble about yourself, no notes about these instructions, no metadata block." — c00707
- "初稿写入 draft_v1.md 与 draft_v1_notes.md，不得把内部备注混入正文" (write the first draft to draft_v1.md and draft_v1_notes.md; internal notes must not be mixed into the body) — c00715

### 6. No silent gaps: either finish the content or mark the unknown with an explicit marker
There are two poles:
- Never leave TBD/TODO or template residue: 15 records / 14 owners.
- Mark missing data with a named, often greppable marker instead of inventing it: 12 records / 11 owners.

They do not conflict. Several quotes allow markers and forbid only generic filler.
- Counts: 26 records / 25 repos / 25 owners
- Doc types: project-docs 13, marketing-copy 7 (2.3x), prd-spec 6
- "Every doc ends in a definite state — no "TODO: fill this in" placeholders unless explicitly requested as a template." — c00298
- "Placeholders for content you cannot author (real testimonials, metrics, customer names) marked with `<<PLACEHOLDER: …>>` so the requester can grep them" — c01260
- "write `NEEDS HUMAN INPUT: <what>` so the human fills it before submitting" — c01073

### 7. Report the verification done and the evidence used
The return names the commands run, the build result, and the sources or files the claims were checked against.
- Counts: 24 records / 23 repos / 22 owners
- Doc types: project-docs 19 (1.8x), api-reference 8, code-comments 4. prompt-instructions 3 lines (6.3x).
- "In author mode, make the edits and end with a list of files touched plus, for each concrete claim you introduced, the thing you opened to verify it." — c00936
- "Return the changed paths, the claims verified against source, and any remaining gap." — c01025
- "Include concrete evidence in completion outputs: changed files and validation commands." — c01092

### 8. End with a fixed status token from a closed vocabulary
The token usually includes a blocked or failed state.
- Counts: 21 records / 21 repos / 21 owners
- Doc types: project-docs 21 (2.0x), api-reference 9, changelog 5
- "Return status: COMPLETE | BLOCKED | PARTIAL" — c00082
- "Finish: `Docs ready` or `Blocked — need human`" — c00899
- "Never overwrite an occupied path; return `REPORT_WRITE_FAILED`" — c00086

### 9. Give several labelled variants, ranked or with a recommended pick
- Counts: 20 records / 20 repos / 20 owners
- Doc types: marketing-copy 20 (every line), blog-article 12 (7.0x), social-media 11 (11.5x), ux-microcopy 11 (9.5x). This theme is genre-specific, not general.
- "For each request, return 3 options labeled A, B, and C." — c00169
- "Produce the contenders and rank them: 2–4 candidate hooks + 2–4 candidate punchlines, each one line, ordered best-first with one line on why the top one leads." — c00825
- "Write 2-3 headline variants — the founder picks the winner" — c01273

### 10. Markdown format constraints (valid, lint-clean, converts cleanly, no HTML)
- Counts: 19 records / 19 repos / 18 owners
- Doc types: spread evenly (project-docs 4, api-reference 4, report-analysis 4), with no concentration
- "Clean Markdown output. Reports should convert cleanly to PDF via standard Markdown-to-PDF tools." — c00246
- "Produced PRDs must be valid Markdown and pass markdownlint validation." — c00629
- "Markdown only. No HTML, no CSS, no `<div>` wrappers, no class names." — c01260

### 11. Update the index, registry or navigation when a doc is added
The agent also updates the index, registry or nav (README tables, sidebar config, docs.json, coverage registry).
- Counts: 15 records / 15 repos / 15 owners
- Doc types: project-docs 12 (1.9x), api-reference 9 (2.5x), changelog 4 (2.3x)
- "Update the registry atomically. After writing any doc file, immediately update the corresponding registry row in `docs/coverage.md`." — c00449
- "Register in `docs/docs.json` (critical — forget this and the page 404s)" — c00249
- "When creating feature documentation, always add an entry to `docs/features/README.md`. The index is a markdown table with columns: Feature (link), Description (one line), Status." — c01228

### 12. Machine-readable return only (a single JSON or YAML object, no prose)
- Counts: 14 records / 14 repos / 14 owners
- Doc types: prd-spec 6 (2.3x), project-docs 6, marketing-copy 3
- "Produce a single JSON object as your final message. No prose outside it." — c00401
- "The output is one JSON object — no surrounding prose, no concatenated RST outside the JSON." — c01483
- "JSON is structured-only: array of findings, plus metadata. No prose." — c01116

### 13. Name the concrete next step or next owner
- Counts: 14 records / 14 repos / 14 owners
- Doc types: project-docs 8, changelog 4 (2.4x), report-analysis 4
- "Propose the exact next revision task instead of vague "let me know" endings" — c00012
- "End every deliverable with `Handoff:` naming the next responsible agent or the Principal Author." — c00932
- "Report changed files, evidence, risks, and next owner." — c01020

### 14. Present revisions as original, then change, then reason
- Counts: 15 records / 14 repos / 14 owners
- Doc types: project-docs 8, other 4 (3.3x), blog-article 3 (3.0x), code-comments 3 (2.5x)
- "每一处实质性修改，我都给「原句 → 改后 → 为什么」。" (for every substantive change I give "original sentence → revised → why") — c01627
- "Its description names each page, the sentence that was wrong, the core change that made it wrong (commit or pull request), and the sentence it says now." — c00976
- "Present the draft or diff to the operator as a proposal. State plainly what changed, what it derives from, and what it now claims as canon." — c00745

### 15. AI or agent attribution markers (contested)
Some agents require a generated-by marker, AI notice or co-author line. Others forbid any AI attribution.
- Counts: 15 records / 14 repos / 14 owners
- Doc types: project-docs 8, report-analysis 5, api-reference 4
- "Never include AI attribution lines anywhere in documentation" — c00094
- "Include a warning that the security audit was performed by AI and the report was written by AI, and that bugs may have been missed." — c00284
- "Add `Co-Authored-By: Claude` line ONLY if Claude contributed a significant amount of code in this revision, not if Claude only drafted the commit message." — c01599

### Just below the cutoff
- Draft status and human sign-off before shipping: 17 records / 13 repos / 13 owners
- Commit/PR mechanics: 13 records / 12 owners
- Bilingual or language-matching output: 11 records / 6 owners
- Never overwrite an existing file, or version each draft: 8 records / 7 owners
- Don't invent numbers; render verbatim: 8 records / 7 owners (report-analysis 2.8x)
- Confidence labels: 6 records / 6 owners

## 2. Lineage warnings

- **Theme 4 (thin return):** tractorjuice/arc-kit supplies 9 of the 31 thin-return records (c00248, c00605–c00612), nearly all "Return a one-line summary to the orchestrator" or "Return a one-line summary, no markdown". Without it the sub-pattern is 22 records / 22 owners. It still recurs, but the record count exaggerates it by about 40%.
  - akiselev (c00132) and alfieprojectsdev (c00139) share the identical line "After editing files, respond with ONLY:", so one template counts as two owners.
- **Theme 1 (path):**
  - tiny-flowlab contributes 6 records, all from one fiction pipeline (chapter_XX.md, setting_world.md, ...).
  - UitbreidenOS contributes 5 records. Four of them are one outreach agent translated into DE/ES/EN/NL (c01416–c01419), same path `/outreach/reviews/sarah-chen-email-1.md`.
  - vinnie357 has 4 near-identical "Save X to `<project_path>/.claudio/docs/...`" lines, and kcenon has several.
  - One template, "Your task: read code from `<dir>` and generate or update documentation in `docs/`", appears under three owners: fugazi c00336, PowerGenome c00751, abdes c01321.
  - iannuttall c00160 and NicholasSpisak c00756 share "Save as Markdown in specified folder (default: .content/{slug}.md)".
  - Removing the four heaviest owners still leaves 88 owners, so the theme is robust. It is also the least transferable, since every instance is project-specific.
- **Theme 2 (files changed):** vijaythecoder c00033 (copies_in_repos 11) and AJCastello c01368 are the same sentence: "Return a brief changelog listing files created/updated and a one‑line summary of each." Otherwise wording varies widely across owners, which suggests real independent convergence.
- **Theme 6 (no silent gaps):** melnikov1512 c00098 ("NEVER use TBD/TODO as final.") and paodealho404 c00223 ("No TBD / TODO in final.") are near-identical wording, probably one template.
- **Theme 15 (attribution):** the count merges opposite instructions (forbid vs require). It shows the topic recurs, not that anyone agrees on it. kesslernity (2 records, same AI-assistance disclaimer) and defuse (2 lines in one record) each count once.
- **Below-cutoff themes:**
  - Human review: UitbreidenOS supplies 4 of the 17 records (the same translated file).
  - Language: kcenon supplies 5 of the 11 claims (the same "both languages" rule across PRD, SDS and DBS agents).
- **Counter-signal from one popular template:** davila7 c00005 (copies_in_repos 53) and jtgsystems c00780 carry the identical sample completion message "Documentation completed. Created 127 pages covering 45 APIs with average readability score of 68. User satisfaction increased to 92% with 73% reduction in support tickets." davila7 c00018 is similar ("Reduced support tickets by 60%..."). These are fabricated metrics used as example output. That one template family spread across many repos gives agents a model of invented numbers. The explicit "never estimate or invent numbers" rules (7 owners) are fewer than the copies of this template.
- **One record, many repos:** gsd-build c00006 (copies_in_repos 43) carries both "Returns confirmation only — do not return doc content to the orchestrator." and a generated-by marker. It counts once here, but a copy-weighted tally would make it look dominant.

## 3. Sharp but rare (1–2 owners, precise, adoptable by a writer)

1. A bounded return file with a fixed field set: "Write that file with STATUS / DID / VERIFIED / NOT-CHECKED / FLAGS / NEXT (≤12 lines) as your last Write, then stop." — c01447
2. Per-claim evidence in the return: "for each concrete claim you introduced, the thing you opened to verify it." — c00936
3. A coverage line that names what was not checked: "a coverage line stating what you checked and what you did not" — c01283
4. A correction record that ties each fix to its cause: "names each page, the sentence that was wrong, the core change that made it wrong (commit or pull request), and the sentence it says now." — c00976
5. No paraphrasing of an upstream verdict: "render `recommendation.verdict` and `recommendation.basis` verbatim. Do not restate it in your own words and do not add a verdict where the payload has none." — c00248
6. Greppable unknowns: "marked with `<<PLACEHOLDER: …>>` so the requester can grep them" — c01260
7. A physical split between notes and deliverable, plus honest status: "初稿写入 draft_v1.md 与 draft_v1_notes.md，不得把内部备注混入正文" (draft to draft_v1.md, notes to draft_v1_notes.md, never mixed into the body). The same record also says tentative titles "不得称为用户已确认" (must not be called user-confirmed). — c00715
8. Provenance kept out of the text: "a source_fact id (or any fact id) MUST appear ONLY in the PROVENANCE JSON after the marker, never in the main.tex itself (not in text, not in a comment)" — c00708
9. A reader-based cutting criterion: "Keep what readers need to trust/decide/act: required findings, uncertainty, citations, QA evidence, safety warnings, blockers, next actions." — c01442
10. A reproducibility bar for reports: "Keep the report reproducible: another engineer should be able to replay each SUBMIT finding from what you wrote." — c00212

## 4. Bearing on the PROPOSED WRITER

### Carrying doc-type differences outside the role (path rules / brief)
**Supported strongly.**
- The largest theme, fixed path and naming (92 owners), is entirely project-specific.
- Variants (20 owners) sit almost entirely in marketing, social and UX copy (lift 7–11x).
- Index/registry sync (15 owners) is literally "when you touch docs/X, also update Y". A path-scoped rule is the natural carrier for that.
- Markdown constraints, bilingual output and attribution policy are also project settings, and attribution is contradictory across projects.

None of these belong in a general role's core. The corpus holds no evidence that a per-type role does better. It shows only that type-specific output rules exist and are local.

### Point 1: start from the reader
**Weak support from this dimension.**
- Only 6 records / 6 owners frame output around the document's reader, for example "audience / goal" (c00285), "Audience: who this update helps" (c00995), "what a reviewer should open in the browser to check" (c00923) and c01442.
- The reader this dimension cares about is overwhelmingly the caller or orchestrator: themes 2, 3, 4, 7, 8, 12 and 13.

**Addition:** the proposal names one reader, but the corpus shows the writer always has two: the document's reader and the caller who consumes the return. The role should name both.

### Point 2: every factual sentence traceable; interpretation marked
**Supported, but the corpus places traceability mostly in the return rather than in the document.**
- Verification reporting has 22 owners and open-gap reporting has 38 owners.
- Claim-level checking is rarer: 7 records / 7 owners (c00936, c01025, c01283, c00934, c00651, c01209, and c00632 "unresolved claims").
- "Don't invent numbers / render verbatim" has only 7 owners and concentrates in reports.
- Confidence labels (6 owners) are the corpus's closest analogue to marking interpretation, e.g. "high (grounded in sources), medium (inferred), low (speculative)" (c00342).

**Additions:**
- The proposal says to mark interpretation but says nothing about unknowns. Theme 6 (25 owners) says an unknown in the deliverable gets a named, greppable marker, never generic TBD and never invented filler.
- The davila7 template family shows why example outputs given to a writer must pass the same evidence bar. A popular template teaches fabricated metrics.

### Point 3: cutting by default; working notes to a separate output, never into the deliverable
**Supported most strongly of the three.**
- "Only the deliverable, no preamble or notes" has 25 owners.
- "File is the deliverable, reply is a pointer" has 33 owners.
- c00715 and c00708 even physically separate notes and provenance from the text.

**Addition:** the proposal says there is a separate output for the caller but does not say what goes in it. The corpus converges on a return contract:
- files changed, one line each (53 owners)
- what was not verified or remains open (38)
- what was verified and with what evidence (22)
- a closed status token that includes a blocked or failed state (21)
- next step or next owner (14)
- a size bound on the reply itself (c01447 ≤12 lines, c00971 ≤60 words, c01442 ~100 tokens)

The claim ledger in the proposal fits naturally as the "verified / unverified" part of this contract.

### Combining drafts by claim with an evidence-tier ledger
**Neither supported nor contradicted: no output-dimension quote combines several drafts or tiers evidence.**
- Per-claim return fields (the 7 owners above) show that a claim-level unit is already used.
- The tier ordering (measured > vendor doc > recurring > single) is the proposal's own addition, with no corpus precedent in this dimension.

### "Does not judge the quality of its own output"
**Mildly contradicted by practice.** 5 records / 5 owners require self-scoring or self-review in the output:
- "composite = (humanity × 0.30) + ..." (c00081)
- "end with one line: "voice match check: pass"" (c00350)
- "Your final output MUST include the completed Self-Critique Results table" (c00626)
- c00956 "the self-review"
- c01427 "AI Detection Score"

These are rare and unmeasured, so they do not outweigh the proposal's rationale. They show that the proposal departs from some existing practice.

### What this dimension has and the proposal lacks
1. **The caller-return contract** described under Point 3 (fields, status vocabulary including BLOCKED or no-op, size bound).
2. **Write, don't describe; don't echo the content** (33 owners), plus **never overwrite an existing file** (7 owners, e.g. c00086 "Never overwrite an occupied path; return `REPORT_WRITE_FAILED`", and c00127, which appends a timestamp suffix instead).
3. **Revision format:** when editing an existing text, report original → change → reason (14 owners).
4. **Draft status honesty:** do not present a draft as approved or confirmed (13 owners, e.g. c00715, c01232 "stating which sections are COMPLETE and which are DRAFT").
5. **Companion updates** (index, registry, nav) when a doc is added. Mechanically this belongs in path rules, but the role needs to expect that such rules exist.
