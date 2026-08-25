Each record below is one sentence copied verbatim from a public agent skill — a claim its author could not have written without having done the thing — together with a one-line summary of the skill it came from, for context only.

For each, say **what the claim is knowledge about**, in three to six words.

The subject of the claim, not the subject of the skill. A skill that builds slide decks can carry a claim about how a font renders; the claim is about font rendering. A skill for a research pipeline can carry a claim about how judges disagree; the claim is about judge panels. Where they differ, the quote decides.

Write the subject as a practitioner would name the thing they were dealing with when they learned it — `retrieval chunking`, `judge panel convergence`, `PDF text extraction`, `CI cache invalidation`, `screen-reader focus order`. Not a category and not a department: `engineering`, `documentation`, `best practices` name nothing. If two claims are about the same thing, they should come out with the same words; do not vary the phrasing for its own sake.

Where the claim is about a general practice rather than a specific mechanism, name the practice at the same grain — `writing failing tests first`, not `testing`.

Answer with a JSON array and nothing else: no preamble, no code fence. One object per input record, in the same order, each carrying the record's `id`:

[{"id": "<the id given>", "about": "<three to six words>"}]

--- RECORDS ---
{{RECORDS}}
