# Themes: doc-type-convention

Source: `claims/doc-type-convention.jsonl`, 904 quote lines from 608 distinct records, 502 repos, 478 owners. Every line was read. Counts below are computed from the file, not estimated.

Method. I did a first regex pass to find candidates, then assigned each theme by hand to an explicit list of line numbers after reading every line (one rater, no second coder). A line can belong to more than one theme. Counts are distinct records / distinct repos / distinct owners (the owner is the part of `repo` before `/`). "Concentration" gives the doc types that carry the most theme records, as the share of theme records carrying that type, with the lift over that type's share among all 608 records in this dimension in brackets (a record can carry several types). The baseline shares are project-docs 61%, api-reference 45%, changelog 16%, code-comments 15%, prd-spec 15%, report-analysis 11%, marketing-copy 7%, academic 4%, ux-microcopy 3%, social-media 2%. The appendix lists the record ids for each theme so the counts can be reproduced.

Coverage. All 33 candidate themes together cover 526 of the 904 lines (375 records, 317 owners). The other ~42% of lines are one-off domain conventions, such as game dialogue formats, marketing funnels, arc-kit report fields, Joomla specs, subtitle line breaks and KaTeX delimiters. Most of the dimension is long tail. The themes below are the part that recurs.

## 1. Top recurring themes (by distinct owners)

### T1. Code examples must be complete and runnable: every concept, command or endpoint gets one, with no pseudocode
Counts: 42 records / 38 repos / 38 owners. Concentration: project-docs 95% (1.6x), api-reference 76% (1.7x).
- "Working code, not pseudocode — agents will copy and modify, so it must compile/run" (c00088)
- "Code Examples: Include context (imports, setup). Show expected output. Test before publishing." (c00402)
- "Provide COMPLETE, RUNNABLE examples. Partial examples = LYING about functionality." (c00626)

### T2. Doc comments follow the language's standard format and its required tags
Examples of the formats: Google-style or numpydoc docstrings, JSDoc/TSDoc, `///` with `<summary>`/`<inheritdoc/>`, PHPDoc, kernel-doc, PodWeaver.
Counts: 39 records / 37 repos / 35 owners. Concentration: code-comments 92% (6.1x), api-reference 82% (1.8x).
- "All public methods need numpydoc-style docstrings with at minimum: Summary, Parameters, Returns, and Examples." (c00696)
- "Overrides, interface implementations, and documented members inheriting docs: `/// <inheritdoc />` (add a `<summary>` only when the inherited docs are insufficient)" (c00779)
- "For in-code docstrings you state the contract — pre-conditions, post-conditions, side effects, error modes — and skip what the language already encodes." (c01263)

### T3. Changelogs follow Keep a Changelog: an Unreleased section and Added/Changed/Deprecated/Removed/Fixed/Security categories
Counts: 32 records / 29 repos / 28 owners. Concentration: changelog 97% (6.1x), code-comments 38% (2.5x).
- "Changelogs must follow Keep a Changelog format with Unreleased, Added, Changed, Deprecated, Removed, Fixed, Security sections" (c00084)
- "CHANGELOG.md — Keep a Changelog 2.0.0, semver-aligned: breaking entries marked **Breaking:** with the migration step, Security entries lead with the CVE id" (c01447)
- "Follow the project's existing changelog format if one exists; otherwise use Keep a Changelog format." (c01350)

### T4. API reference covers error responses and request/response examples, not only the happy path
It often names curl plus several languages, and an error table per endpoint.
Counts: 23 records / 22 repos / 22 owners. Concentration: api-reference 96% (2.1x), changelog 35% (2.2x).
- "Every endpoint needs an error table. \"Returns 400 if invalid\" is not documentation." (c00717)
- "Include at least one \"happy path\" and one \"common failure\" example per critical endpoint." (c00077)
- "API docs must include error responses, not just happy path" (c01246)

### T5. Requirements take a fixed testable form: Given/When/Then, EARS, "As a … I want … so that", INVEST, RFC 2119 keywords
Counts: 21 records / 21 repos / 21 owners. Concentration: prd-spec 100% (6.7x).
- "Acceptance criteria are a contract - if it's not testable, it's not a criterion" (c00371)
- "KPIs are numbers with baselines and targets, not directions (\"reduce churn\" is not a KPI; \"churn 4.2% to 3.5% by Q3\" is)." (c01320)
- "ensure they use concrete data (not \"a valid input\"), describe business behaviour (not UI steps), and focus on one rule per scenario" (c01580)

### T6. Classify each page as one Diátaxis/Divio type (tutorial, how-to, reference, explanation) and never mix types on one page
Counts: 21 records / 21 repos / 21 owners, or 18 independent voices once the template family is collapsed (see Lineage). Concentration: project-docs 95% (1.6x), api-reference 86% (1.9x).
- "Diátaxis: every page is exactly one of tutorial (learning) / how-to (task) / reference (facts) / explanation (why). Mixed page → split." (c01447)
- "cada página/documento es uno solo de los cuatro tipos. Si necesitas cubrir varios, son varios documentos enlazados entre sí." (c00201) (each page is exactly one of the four types; to cover several, write several linked pages)
- "Migration guides are strictly for breaking changes. Do not include new features or non-breaking additions -- those belong in the feature pages or release notes, not in migration guides." (c00927)

### T7. ADRs use a standard format (Nygard or MADR: Status/Context/Decision/Consequences), are numbered, and are superseded rather than edited
Counts: 22 records / 22 repos / 21 owners. The immutability sub-rule has 4 records / 4 owners. Concentration: project-docs 91% (1.5x), prd-spec 50% (3.3x).
- "For ADRs you follow the standard sections (Status, Context, Decision, Consequences) and number them sequentially." (c01263)
- "You never edit an accepted ADR — you supersede it with a new one and update the old Status line." (c01263)
- "Never rewrite a published ADR — supersede it with a new one" (c00369)

### T8. One source of truth: link to or generate from the owner of a fact (code, spec, canonical doc) instead of restating it
Counts: 20 records / 20 repos / 20 owners. Concentration: project-docs 90% (1.5x), api-reference 55% (1.2x).
- "Never re-describe implementation behavior in prose. Point to the owning source, test, schema, manifest, or workflow." (c00389)
- "Reference is GENERATED from the spec ... never hand-maintained - hand-written reference drifts from reality within weeks." (c00885)
- "OpenAPI-derived API reference: when an OpenAPI spec exists, generate the API reference from it (endpoints, params, schemas, errors) — never hand-write contracts from memory." (c00397)

### T9. Keep terminology consistent: reuse the codebase's or glossary's terms and define terms on first use
Counts: 19 records / 19 repos / 19 owners. Concentration: project-docs 79% (1.3x), prd-spec 32% (2.1x).
- "Reuse existing terms. If the codebase calls it `primResID`, the doc calls it `primResID`, not `primitive_id`." (c01106)
- "a glossary entry must exist for every domain-specific term" (c00042)
- "the architectural nouns and verbs come straight from [LANGUAGE.md](LANGUAGE.md). Concision is not an excuse to drift." (c00101)

### T10. Start from the repo's own template for the doc type and fill every placeholder
Counts: 19 records / 18 repos / 18 owners. Concentration: prd-spec 42% (2.8x), report-analysis 21% (1.9x).
- "Treat `tools/azsdk-cli/docs/specs/README.md` and `tools/azsdk-cli/docs/specs/spec-template.md` as the source of truth for structure and required sections." (c00830)
- "Load templates: Read the appropriate template from `context/templates/` — use `prd-template.md` for PRDs. Replace every bracketed placeholder." (c00955)
- "RELEASE_NOTES.md (repo root) follows a **fixed template** — only the content rotates, never the structure." (c01023)

### T11. Comments and design docs explain why, not what
Counts: 17 records / 17 repos / 17 owners. Concentration: code-comments 82% (5.4x), api-reference 82% (1.8x).
- "Explain the \"why\", not the \"what\" — `// abort stale request before starting a new one` not `// call abort()`" (c01192)
- "Use code comments for intent, invariants, and non-obvious tradeoffs rather than narrating syntax." (c00946)
- "Architecture decisions: WHY a design was chosen (not what it is — the code shows that)." (c00655)

### T12. Match the toolchain's exact syntax, or the doc breaks when rendered
Examples: link form, required frontmatter keys, code-fence language, math delimiters, component usage.
Counts: 17 records / 17 repos / 17 owners. Concentration: project-docs 88% (1.4x), api-reference 71% (1.6x).
- "Always include `.md` extension** in internal links: ... ❌ `[Setup Guide](./setup)` (WRONG - causes dead link error)" (c00109)
- "The katex-header in this project configures **only** `$...$` and `$$...$$` as delimiters. `\\(...\\)` and `\\[...\\]` are NOT configured and will render as raw escaped text." (c00325)
- "**README.md** must use absolute URLs for all links because its content is synced verbatim to docs.pact.io" (c00624)

### T13. API specs follow OpenAPI 3.x strictly, with `$ref` for shared components and auth/security schemes
Counts: 19 records / 17 repos / 17 owners, or 16 independent voices (see Lineage). Concentration: api-reference 100% (2.2x).
- "Ensure all specifications strictly adhere to OpenAPI 3.0.x schema requirements, including proper structure, required fields, and valid syntax." (c00288)
- "Single source of truth: The OpenAPI spec is THE contract" (c01208)
- "Follow OpenAPI 3.0 specification strictly" (c00027)

### T14. Match the existing documentation's style, structure, format and tone before inventing anything
Counts: 17 records / 17 repos / 17 owners. Concentration: project-docs 100% (1.6x), changelog 29% (1.8x).
- "search 3+ existing doc/section patterns and evaluate fit before writing — match the local doc convention, don't invent a new section shape" (c01600)
- "Mirror the structure, frontmatter, heading order, and link conventions of neighboring documentation pages." (c00738)
- "Add or verify an entry (what changed, why, impact) if maintenance-engineer didn't already write one for a fix; match the tone and format of existing entries." (c00078)

### T15. Breaking changes get a migration path with before/after examples
Counts: 15 records / 15 repos / 15 owners. Concentration: changelog 60% (3.8x), api-reference 80% (1.8x).
- "Breaking changes → write **Migration Guide** with before/after snippets." (c00363)
- "Deprecated endpoints must be marked with the deprecated flag and include a description pointing to the replacement endpoint and migration steps." (c00118)
- "Breaking changes: Must include \"BREAKING CHANGE:\" in footer with migration guide" (c01599)

Just below the cut, by owners:
- Version marking: which release introduced or deprecated a feature, and version-locked examples. 14 records / 14 owners, 12 independent voices.
- Mandatory updates when code changes, for example "When `Makefile` changes, sync …" (c01469) or "Every new sysfs attribute needs a corresponding ABI doc entry" (c01563). 13 records / 13 owners.
- Platform-native social and marketing copy, with the hook in the first N characters or seconds. 14 records / 12 owners.
- Changelog entries written for users, describing behaviour rather than commits. 11 records / 11 owners.
- Mermaid for diagrams. 12 records / 11 owners.
- Named external style guide. 11 owners.
- Repo style-guide file. 11 owners.
- Accessibility (WCAG, alt text). 9 owners.
- Academic citation form. 7 owners.
- Last-updated dates. 7 owners.
- Current-state-only docs. 7 owners.
- README as a fast orientation page. 6 owners.
- i18n placeholders preserved exactly. 6 owners.

Unions that matter for the proposal:
- Defer to the repo's own convention source (T10 + T14 + repo style-guide file): 46 records / 44 owners.
- Changelog, format or user-facing: 38 records / 34 owners.
- API reference, OpenAPI or errors/examples: 38 records / 35 owners.
- Versions or dates: 21 owners.
- Any named style guide, external or repo: 22 records / 21 owners.

## 2. Lineage warnings

- **T6 Diátaxis.** One template family carries 4 of the 21 owners: the widely copied "engineering-technical-writer" (msitarzewski/agency-agents style). Its members are c00004 (monoes, merged across 54 repos), c00131 (imMamdouhaboammar, same English wording), c00068 (liaoxinjie666, a Chinese translation: "应用Divio文档系统…绝不混合它们", "apply the Divio documentation system… never mix them") and c00909 (xuanbingbingo, a Chinese variant, which also carries the README "5 秒测试" / five-second test that counts in the README theme). In the corpus, the words "Divio" and "5-second test" occur mostly in files named `engineering-technical-writer`. As independent voices that is 18, not 21. The same family adds 2 of the 14 owners in version marking ("Version everything — docs must match the software version they describe; deprecate old docs, never delete", c00131, and its translation in c00068).
- **T13 OpenAPI.** ruvnet has 3 records (c00027, c00148, c00149) and Ashhad1200 (c00106) repeats the same four lines: "Follow OpenAPI 3.0 specification strictly", "Use $ref for reusable components", and so on. This is the claude-flow `docs-api-openapi` agent, which appears under many owners in the corpus. The theme has 16 independent voices, and 4 of its 19 records are one text.
- **T1 runnable examples.** affaan-m has 4 records (c00470, c00473, c00476, c00478) that are the same line in Spanish, Japanese, Korean and Portuguese; they count as 1 owner but 4 records. c00002 (darrenhinde, "every concept needs a working code example") is merged across 84 repos, and the phrase "concept needs a" appears in 90 corpus files. c01054 (llcoolblaze, "Every concept needs a code example") is probably a variant of it, but I did not confirm that. The owner count holds up; the reach is template-driven.
- **i18n placeholders.** c01376 and c01377 (bullish0x/GameStudio) repeat c00000 (Donchitos/Claude-Code-Game-Studios, merged across 130 repos) word for word: "All variable insertions use named placeholders". The theme has 5 independent voices, not 6.
- **Platform-native.** caioimori (sinapse-ai) has 2 of the 14 records, and within this dimension its records are near-duplicates (c01452 and c01458 match; so do c01450 and c01456). c00007 (mrgoonie, "First 140 characters are critical (preview text)") is merged across 38 repos, so the rule's reach comes mainly from one file.
- **T3 Keep a Changelog.** borghei has 3 records and isac322 has 3 (c01024, c01144, c01145). Exact-phrase repeats across owners, such as "Follow [Keep a Changelog](https://keepachangelog.com) format" in c00278 and c00464, are more likely independent citations of the same external standard than shared lineage. The theme is a real standard, not an artefact of copying.
- **High-reach single records.** Owner counts are unaffected, but readers should know these records are really copies of one file: c00003 (github/awesome-copilot, "Follow the [Michael Nygard ADR format]", 72 repos), c00016 (TaxCore terminology, 20 repos), c00011 (SuperClaude WCAG, 27 repos) and c00018 (davila7 WCAG, 18 repos).
- **Within-repo multiplicity** does not inflate owner counts but does inflate record counts. prmichaelsen (7 lines), tiny-flowlab (8, all fiction examples), tractorjuice/arc-kit (8, all report-specific) and microsoft/hve-core (several) are single voices with many roles.

## 3. Sharp but rare (1–2 owners, precise, adoptable by a general writer)

1. "Never guess citation keys. A `MISSING:` placeholder is always better than a fabricated key that might resolve to the wrong paper." (c00390, MichaelsEngineering, academic) This is a concrete rule for missing evidence: an explicit marker instead of a plausible invention.
2. "Where a service has no published price, render `[NO PUBLISHED PRICE]` and `[QUOTE REQUIRED]` rather than a number." (c00605, tractorjuice, report) The same move applied to numbers in reports.
3. "illustrative 必须明确为示例，不能伪装成真实案例" ("an illustrative case must be marked as an example and must not pass as a real one") (c00715, dongbeixiaohuo, blog/marketing)
4. "对于标记为\"需后端验证\"的漏洞，在报告中单独归类，提示审计人员需进一步手工测试确认" ("put vulnerabilities marked 'needs backend verification' in their own category, telling auditors to confirm them by manual testing") (c00719, sssmmmwww, report) Unverified findings are kept apart from verified ones.
5. "Preserve historical scope. A claim written about 4.1.1 stays a 4.1.1 claim. Do not retroactively update a statement that was true when written — add a note." (c01317, JuanLunaIA, project-docs)
6. "Treat the opening `In this lesson, you will:` list as authoritative. Make the summary list a one-for-one, past-tense reflection of those objectives without adding new claims." (c00104, 01fe25bca308-stack, project-docs) The summary may not introduce claims the body lacks.
7. "Keep ADRs track-independent and do not cite transient local files as durable references." (c00365, Flip451, prd-spec) A durable document must not cite sources that will disappear.
8. "If risk_level = LOW and no anomalies: the executive summary should be one sentence: \"Log analysis complete — no threats detected.\"" (c00938, FlorianBruniaux, report) The length of the summary follows how much was found.
9. "Prose worth keeping does not just get deleted — move it to a help topic" (c00265, CircleCI-Public, ux-microcopy/project-docs) When cutting, relocate what is worth keeping instead of discarding it.
10. "每个计算单元格必须是公式字符串，绝不能是在 Python 中计算后粘贴的数值。" ("every computed cell must be a formula string, never a value computed in Python and pasted in") (c00406, Zeus-Center, report) The number stays traceable to its derivation inside the deliverable.

Honourable mentions, left out for length:
- "Do not invent telemetry names; do not paraphrase OpenTelemetry semantic conventions." (c00629)
- "record user-visible changes … without inventing release dates or versions" (c00946)
- "Captions explain data, methods, units, uncertainty and the observed finding, not just the chart type." (c00733)
- "Impact in numbers, root cause as a mechanism, and an honest **Detection** section" (c01193)
- "If a previous report exists for a device, compute a delta and label items **Resolved / Still open / New**." (c01577)

## 4. Bearing on the PROPOSED WRITER

**Differences between doc types live outside the role.** Supported, with a caveat.
- The large themes are sharply type-bound: Keep a Changelog runs at 6.1x in changelog, requirements formats at 6.7x in prd-spec, doc-comment formats at 6.1x in code-comments, and OpenAPI is 100% api-reference.
- Most of them are pointers to a named external standard (Keep a Changelog, Diátaxis, Nygard/MADR, OpenAPI, EARS/GWT, Google/numpydoc, WCAG, OWASP) or to a repo file. That fits short path-scoped rule files well: `CHANGELOG.md`, `docs/adr/**`, `*.py`, `openapi.yaml`, `specs/**`.
- The strongest combined signal, defer to the repo's own convention source (neighbouring docs, the repo template, the repo style-guide file), has 44 owners. It says the convention should come from the repo at write time, which is what the proposal's rule files and caller briefs do.
- Caveat: this corpus puts these rules inside single-type roles. It shows where authors put conventions, not that a general role fails without them, so it neither confirms nor refutes the "split only on failure" rule.

**Point 1, start from the reader.** Supported in form, rarely stated as a reader question.
- Diátaxis (T6, 18 to 21 owners) is a reader-intent classification: learning, task, lookup, understanding. It can be read as point 1 turned into a structure rule, and arguably belongs in the core as the first question rather than in a rule file.
- User-facing changelog entries (11 owners, for example "Changelogs should be written for humans, not generated from commit messages", c01246) and README orientation (6 owners) are also reader-first rules specialised to a type.

**Point 2, facts traceable to evidence.** Strongly supported, and the corpus adds mechanisms the proposal lacks.
- T8 single source of truth (20 owners) and T1 runnable examples (38 owners, "Test before publishing", c00402) are the project-docs form of traceability. T1 goes further than "traceable to code": the example must have been run, which is the "measured" tier applied to documentation.
- Missing from the proposal: what to write when the evidence is absent. The rare rules converge on an explicit marker in the deliverable rather than an omission or an invention: `MISSING:` (c00390), `[NO PUBLISHED PRICE]` (c00605), "must be marked as an example" (c00715), and a separate category for unverified findings (c00719). This is a small, adoptable addition to point 2.
- Missing: the time scope of claims. Two positions conflict here. Current-state-only (7 owners: "Docs are present-tense", c01103; "No meta-log in AI-facing docs", c01600) and ADR immutability or historical scope (4 owners plus c01317: "A claim written about 4.1.1 stays a 4.1.1 claim") disagree about whether an old statement is corrected or kept and annotated. They are type-dependent: living docs are current-state, decision records are historical. That makes this a good candidate for rule files, but the core should at least say that a claim carries the version or date it was true for. The version-marking (14 owners) and last-updated (7 owners) themes point the same way.
- Evidence the proposal does not list: the document builds or renders. T12 (17 owners) consists entirely of failures that only show when the doc is rendered (dead links, raw KaTeX, a missing frontmatter key). For project docs, "it renders in the target toolchain" is a checkable fact alongside "matches the code".

**Point 3, cutting is the default and working notes stay out.** Partly supported, partly in tension.
- Support: why-not-what (17 owners), "No commit dump as a release note" (c00397), current-state-only with "history goes to git / `CHANGELOG.md` / `docs/adr/**`" (c01600), and "keep the design doc body to the latest snapshot, no history" ("本文は最新スナップショットのみに保ち、経緯は書かない", c01399). The last two are the doc-type version of keeping process out of the deliverable.
- Tension: several of the largest themes are completeness mandates rather than cuts. Examples are "every concept needs a working code example" (T1), "every endpoint needs an error table" (T4), `<summary>` "on **every public member**" (T2), the required Keep a Changelog categories (T3), and required ADR sections (T7). A writer that cuts by default will cut these unless the rule file marks them as required elements. So the rule files the proposal relies on need a "required elements" form, not just style advice.
- The rare rule "move it, don't delete it" (c00265) shows that cutting from the deliverable can mean relocating. The proposal's separate caller output covers reasoning, but not content that belongs in a different document (Diátaxis split, migration guide versus release notes, c00927).

**Point 4, claim-level merge, evidence-tier ledger, no self-judging.** Not addressed by this dimension, with little support or contradiction.
- The closest material concerns precedence between sources: "This document is canonical: A prototype is an attachment, and a difference resolves in favor of this document." (c00684); English as the source of truth for translations (c01097); the Japanese docs as canonical (c01151); and "Prefer one portable canonical rule over independent platform-specific policy copies" (c01030).
- One conflict for the tier ordering: "If the rule and the example contradict each other, follow the example" ("Если правило и пример противоречат друг другу, ориентируйся на пример", c01281). This is a single source, but it is exactly the kind of claim the ledger should record at the lowest tier.
- In the ledger, the named standards behind the big themes (Keep a Changelog, OpenAPI, Diátaxis, Nygard, EARS) sit at "vendor or standard documentation". Recurrence across independent owners (T1 to T15) is the third tier, and the lineage section above is needed before that tier can be credited.

**Present in this dimension but absent from the proposal:**
- **Code-change-triggered doc duties** (13 owners): "When `Makefile` changes, sync: `DEVELOPMENT.md`…" (c01469); "For every new component added, add a row to the Components Used table" (c01583). These fire on touching code, not a doc file. A path-scoped rule keyed only on doc paths will not load for them. The rule needs to match source paths, or the caller's brief has to carry the duty.
- **Scope rules for when not to write** (4 owners): "Bug fix | No documentation required unless the bug revealed incorrect documentation" (c01202); "Do not add anything if nothing changes on the main sections" (c01422). This is cutting at the level of the whole document, which the proposal does not cover.
- **Localization invariants**: preserve placeholders byte for byte, never concatenate strings (c00885), and know which language is canonical. These are hard constraints rather than style, and they fit rule files.

## Appendix: record ids per theme (for reproducing counts)

- `runnable_examples`: c00002, c00009, c00055, c00075, c00082, c00088, c00173, c00210, c00221, c00254, c00255, c00282, c00383, c00402, c00460, c00470, c00473, c00476, c00478, c00499, c00626, c00636, c00741, c00922, c01001, c01052, c01054, c01064, c01197, c01225, c01271, c01272, c01313, c01314, c01318, c01335, c01423, c01431, c01467, c01468, c01555, c01586
- `doc_comment_format`: c00047, c00099, c00177, c00188, c00206, c00310, c00329, c00391, c00407, c00425, c00426, c00463, c00671, c00696, c00743, c00753, c00779, c00866, c00890, c00952, c00953, c01064, c01096, c01101, c01186, c01188, c01222, c01243, c01251, c01263, c01303, c01353, c01395, c01446, c01558, c01563, c01566, c01579, c01624
- `keep_a_changelog_format`: c00063, c00084, c00113, c00254, c00278, c00314, c00321, c00345, c00352, c00374, c00383, c00393, c00459, c00464, c00514, c00663, c00664, c00878, c00946, c00972, c01024, c01127, c01144, c01145, c01243, c01246, c01350, c01356, c01383, c01431, c01447, c01576
- `api_errors_and_examples`: c00038, c00052, c00055, c00077, c00106, c00118, c00140, c00306, c00324, c00345, c00497, c00717, c00718, c00752, c00762, c01048, c01065, c01150, c01246, c01257, c01579, c01586, c01592
- `requirements_format`: c00054, c00093, c00137, c00217, c00371, c00387, c00436, c00504, c00588, c00941, c00955, c01057, c01082, c01242, c01320, c01385, c01425, c01434, c01501, c01580, c01625
- `diataxis_split`: c00004, c00068, c00084, c00131, c00201, c00216, c00259, c00278, c00296, c00360, c00374, c00624, c00909, c00927, c00929, c01090, c01202, c01228, c01442, c01447, c01471
- `adr_format`: c00003, c00084, c00092, c00184, c00259, c00317, c00365, c00369, c00379, c00391, c00407, c00547, c00549, c00721, c00789, c00887, c01263, c01348, c01410, c01605, c01607, c01609 (immutability subset: c00259, c00369, c01263, c01605)
- `single_source_link_or_generate`: c00193, c00239, c00335, c00389, c00397, c00523, c00698, c00730, c00752, c00854, c00885, c00892, c00917, c01019, c01038, c01097, c01151, c01208, c01566, c01624
- `terminology`: c00016, c00034, c00042, c00101, c00185, c00191, c00343, c00762, c00943, c00980, c01001, c01106, c01159, c01280, c01304, c01314, c01550, c01588, c01617
- `use_repo_template`: c00120, c00172, c00266, c00284, c00378, c00581, c00629, c00784, c00789, c00790, c00830, c00839, c00862, c00955, c01023, c01114, c01169, c01380, c01578
- `why_not_what`: c00219, c00240, c00374, c00463, c00626, c00637, c00655, c00780, c00946, c01055, c01192, c01263, c01315, c01349, c01395, c01586, c01616
- `toolchain_syntax`: c00048, c00109, c00158, c00249, c00325, c00464, c00601, c00624, c00648, c00802, c00994, c01038, c01085, c01302, c01396, c01540, c01610
- `openapi_standard`: c00027, c00033, c00091, c00106, c00117, c00148, c00149, c00211, c00288, c00335, c00374, c00397, c00513, c00717, c00885, c01048, c01065, c01148, c01208
- `match_existing_docs`: c00078, c00180, c00183, c00185, c00264, c00271, c00300, c00343, c00441, c00738, c00834, c00887, c01056, c01314, c01350, c01551, c01600
- `breaking_migration`: c00037, c00067, c00118, c00213, c00289, c00335, c00363, c00844, c00922, c00927, c01053, c01208, c01447, c01589, c01599
- `version_marking`: c00068, c00118, c00123, c00131, c00210, c00255, c00323, c00337, c00597, c00671, c00717, c01100, c01243, c01467
- `code_change_triggers_doc_update`: c00184, c00213, c00363, c00375, c00636, c01166, c01323, c01329, c01368, c01469, c01563, c01579, c01583
- `platform_native`: c00007, c00032, c00163, c00178, c00234, c00419, c00794, c00825, c01039, c01062, c01441, c01449, c01453, c01462
- `changelog_user_facing`: c00314, c00397, c00785, c00878, c00946, c01056, c01127, c01198, c01227, c01246, c01329
- `mermaid_diagrams`: c00101, c00113, c00259, c00268, c00710, c00750, c00961, c00985, c01212, c01251, c01372, c01576
- `named_style_guide_external`: c00158, c00159, c00200, c00452, c00717, c00823, c00839, c01070, c01137, c01197, c01340
- `repo_style_guide_file`: c00097, c00111, c00115, c00192, c00787, c00815, c00886, c01056, c01175, c01306, c01310
- `accessibility`: c00011, c00018, c00146, c00211, c00253, c00324, c00982, c00985, c01334
- `academic_citation`: c00041, c00390, c00412, c00428, c00494, c00763, c01213, c01316
- `last_updated_dates`: c00079, c00254, c00259, c00877, c01150, c01158, c01587
- `current_state_only`: c00050, c00184, c00213, c01103, c01349, c01399, c01600
- `i18n_placeholders`: c00000, c00170, c00377, c00815, c00885, c01376, c01377
- `readme_orientation`: c00077, c00374, c00375, c00909, c01188, c01321
- `docs_scope_when_not`: c00927, c01198, c01202, c01422
