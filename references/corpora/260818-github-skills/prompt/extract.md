Read the skill file below and answer in JSON on one line, no prose around it.

You are looking for evidence that this file was corrected by reality rather than composed from the idea of its subject. A sentence qualifies when the author could only have written it after the thing went wrong, or after they measured something, or after they hit a limit nobody documents.

Sentences that QUALIFY, for the shape of them:
- "In practice the API returns 200 with an empty body when the token has expired, so check the body and not the status."
- "Keep this file under 520 lines; past that the loader truncates it with no warning."
- "`--paginate` stops at 1000 results even though `total_count` reports more."
- "Claude reliably ignores this instruction when it appears after the examples, so it goes first."

Sentences that DO NOT qualify, however well written:
- "Always write clear, maintainable code."
- "Use TypeScript for type safety."
- "Run the tests before committing."
- "This skill helps you write better PRDs."
- Any step of a procedure that follows from knowing the tool exists.

Answer:

{"summary": "two or three sentences: what this skill does and how it operates",
 "drives": ["each external system, service, or tool this skill operates, by name; empty if it operates nothing outside itself"],
 "quote": "the single strongest qualifying sentence, copied VERBATIM from the file, or null",
 "quote_reason": "what the author had to have done to know it, or null"}

Copy the quote character for character, including backticks and punctuation. Most files contain nothing that qualifies, and null is the right answer for those. Never write a sentence that is not in the file.

--- FILE: {{FILE}} ---
{{BODY}}
