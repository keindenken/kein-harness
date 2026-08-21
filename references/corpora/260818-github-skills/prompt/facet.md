Each record below is one agent skill, already read by a model that saw the whole directory. `summary` says what the skill does, `quote` is a sentence copied verbatim from its source that its author could not have written without having done the thing, `quote_reason` says why that sentence qualified, and `drives`, `cli` and `mcp` name what the skill reaches for — `drives` in particular usually names tools the summary never mentions.

Two jobs per record.

**Say how far the knowledge travels.** A sentence can be hard-won and still be worth nothing once its tool is gone. Three levels, and the distinction is about the *knowledge*, not about whether a tool is named:

- `bound` — dies with a specific product, version or endpoint. *"`az graph query -o table` only renders summary columns and hides projected fields"* is a fact about one Azure CLI release; when it is fixed, the sentence is worthless.
- `tool-general` — the knowledge is tied to a tool, but that tool is one a practitioner keeps using across projects: a browser driver, a version control system, a package manager, a widely-used runtime or framework. Knowing it stays useful as long as the tool does.
- `transferable` — survives its tool entirely. *"Fixed-size chunking splits a table in half and produces two useless chunks"* is about retrieval, not about any library. *"A broken parser in one judge reduced the panel from 3 to 2 and prevented convergence"* is about judge panels, not about that harness.

Judge the record you were given, not the skill you imagine, and judge the *quote*. Where the quote and the summary point at different levels the quote decides, because the quote is the part that was checked against the source and the summary is another model's prose.

**Where `quote` is null, `transfer` is null.** Do not fall back to the summary. A summary is written in the abstract — *"reusable frontend patterns for React and Next.js"* — and abstraction reads as transferable no matter what the skill actually knows; asked to rate records with no quote, a pilot called 62% of them transferable against 43% of the quoted records in the same band. There is no claim to rate, so rate nothing. Still translate every field.

Set `needs_source` when the record genuinely does not let you decide and reading the skill's own text would. It costs a re-read, so set it only where the answer would change, not where you merely feel unsure.

**Translate into Korean.** For the reader, not for the record: the English stays beside your translation and remains the thing that was verified. Two rules and they are not negotiable.

- **Never translate what a machine reads.** Code, commands, flags, file paths, identifiers, error strings, product names, numbers and units stay exactly as written. `--no-verify` stays `--no-verify`; `Total_records` stays `Total_records`; `~130 KB/token` stays `~130 KB/token`.
- **Never repair the source.** If a sentence is fragmentary, a code comment, or ungrammatical, its Korean is fragmentary too. You are not improving it.

Write plain 해라체 — 평서문, no 존댓말, no honorifics.

Answer with a JSON array and nothing else: no preamble, no code fence. One object per input record, in the same order, each carrying the record's `id`:

[{"id": "<the id given>",
  "transfer": "bound" | "tool-general" | "transferable", or null where quote is null,
  "transfer_why": "one short clause naming what it is or is not tied to, or null",
  "needs_source": true | false,
  "ko_quote": "<Korean, or null where quote is null>",
  "ko_reason": "<Korean, or null where quote_reason is null>",
  "ko_summary": "<Korean>"}]

--- RECORDS ---
{{RECORDS}}
