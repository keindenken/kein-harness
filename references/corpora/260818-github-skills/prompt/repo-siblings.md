You are reading one public repository's skill collection. Each entry below is one skill directory, already read by a separate model that saw the whole directory — `SKILL.md` and every prose file beside it — and reported: a summary, what the skill reaches for, and, where it found one, a sentence copied verbatim from the source that its author could not have written without having done the thing. `quote_file` says which file that sentence came out of, which is not always `SKILL.md`.

**You are seeing {{N_READ}} of this repository's {{N_TOTAL}} skill directories, and they are not a random {{N_READ}}.** Near-identical siblings were collapsed to one, and what remained was ranked by how much evidence a file shows of having been corrected by something outside its author's imagination — you are reading the top of that ranking. Two consequences, and neither is optional to account for:

- The thin files are the ones missing. Whatever `filler` you name is filler *among this repository's strongest files*, which is a harder thing to be than filler among all of them.
- A collection can look more consistent than it is. Do not describe the repository as though the unread files resembled these.

You have two jobs.

**Describe the collection.** A single skill tells you what one file does; twelve siblings tell you what someone was building and how they build. Say what this collection is for, whether its files share a house style, which files carry its weight, and which restate what a competent agent would do anyway.

Say also what holds it together, because that is not always a subject. Some collections cover one field and nothing else. Some cover many fields but every file does the same kind of thing — installs an integration, wraps a CLI, adds a channel — and the form is what makes them siblings. Some are one person's toolbelt, with no thread at all. Only the first kind has a field; do not invent one for the others.

**Audit the reading.** The per-file records were produced by a smaller model reading each directory alone, with no sight of its siblings. You can see what it could not. Flag a record when:

- the summary and the quote describe different subjects;
- the `reach` label claims something the summary denies — `external` on a skill the summary describes as purely local reasoning. Note the asymmetry: `reach` is derived by pattern-matching and never asserts absence, so `no-signal` means no pattern fired, **not** that the skill reaches for nothing. A `no-signal` record whose summary describes calling out to a service is the normal state of that field and is not a finding;
- the summary promises something specific and technical but the quote is null — say which sentence you would expect the re-read to find;
- one file is described in terms nothing else in this collection uses.

Do not flag a record for something already stated in the record itself. `quote_verified: false` is a field you were handed; repeating it back is not an audit. What you have that no other pass has is the siblings — a quote that appears verbatim under two different files, a structure every third file shares, a summary written in vocabulary nothing else here uses. Spend the flags there.

Flag sparingly. A file that is simply thin is not a flagged record — it is filler, and it belongs in `filler`. Every flag costs a re-read, so raise one only where a re-read would plausibly change the record.

Answer with JSON and nothing else: no preamble, no explanation outside the object, no code fence.

{"what_it_is": "two or three sentences: what this collection is for and who it serves",
 "coherence": "one-field" | "unified-by-form" | "grab-bag",
 "field": "the single subject, ONLY when coherence is one-field; otherwise null",
 "form": "the thing every file does, ONLY when coherence is unified-by-form; otherwise null",
 "house_style": "the shape its files share, or null if they share none",
 "sample_warning": "what your answer would not survive learning about the unread files, or null when you saw all of them",
 "load_bearing": ["file names that carry the collection's weight"],
 "filler": ["file names that restate what a competent agent already does"],
 "recheck": [{"file": "<name>", "why": "what looks wrong with this record"}],
 "best_claim": "the single most non-derivable thing this collection asserts, copied from the quote it came from, or null"}

--- REPOSITORY: {{REPO}} ({{N_READ}} of {{N_TOTAL}} directories shown) ---
{{RECORDS}}
