You are reading every skill in one public repository's skill collection. Each entry below is one skill file, already read by a separate model that saw the whole file and reported: a summary, which kinds of thing the skill calls out to, and — where it found one — a sentence copied verbatim from the file that its author could not have written without having done the thing.

You have two jobs.

**Describe the collection.** A single skill tells you what one file does; twelve siblings tell you what someone was building and how they build. Say what this collection is for, whether its files share a house style, which files carry its weight, and which restate what a competent agent would do anyway.

Say also what holds it together, because that is not always a subject. Some collections cover one field and nothing else. Some cover many fields but every file does the same kind of thing — installs an integration, wraps a CLI, adds a channel — and the form is what makes them siblings. Some are one person's toolbelt, with no thread at all. Only the first kind has a field; do not invent one for the others.

**Audit the reading.** The per-file records were produced by a smaller model reading each file alone, with no sight of its siblings. You can see what it could not. Flag a record when:

- the summary and the quote describe different subjects;
- the `calls` label contradicts the summary;
- the summary promises something specific and technical but the quote is null;
- one file is described in terms nothing else in this collection uses.

Flag sparingly. A file that is simply thin is not a flagged record — it is filler, and it belongs in `filler`. Every flag costs a re-read, so raise one only where a re-read would plausibly change the record.

Answer with JSON and nothing else: no preamble, no explanation outside the object, no code fence.

{"repo": "<the repository name>",
 "what_it_is": "two or three sentences: what this collection is for and who it serves",
 "coherence": "one-field" | "unified-by-form" | "grab-bag",
 "field": "the single subject, ONLY when coherence is one-field; otherwise null",
 "form": "the thing every file does, ONLY when coherence is unified-by-form; otherwise null",
 "house_style": "the shape its files share, or null if they share none",
 "load_bearing": ["file names that carry the collection's weight"],
 "filler": ["file names that restate what a competent agent already does"],
 "recheck": [{"file": "<name>", "why": "what looks wrong with this record"}],
 "best_claim": "the single most non-derivable thing this collection asserts, copied from the quote it came from, or null"}

--- REPOSITORY: {{REPO}} ---
{{RECORDS}}
