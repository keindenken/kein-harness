Read the skill file below and answer in JSON on one line, no prose around it.

**The quote is a copy, not a sentence you write.** Find one contiguous span of the file and reproduce it character for character — every backtick, every number, every piece of punctuation. Do not join two spans. Do not start from the file and finish in your own words. Do not tidy anything. If no span qualifies, the answer is null.

You are looking for evidence that this file was corrected by reality rather than composed from the idea of its subject. A sentence qualifies when the author could only have written it after the thing went wrong, or after they measured something, or after they hit a limit nobody documents.

Sentences that QUALIFY, for the shape of them:
- "In practice the API answers with an empty body when the token has expired, so check the body and not the status."
- "Past a certain length the loader truncates this file with no warning, so keep it short."
- "`--paginate` stops early even though `total_count` reports more."
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
 "quote": "one contiguous span copied verbatim from the file, or null",
 "quote_reason": "what the author had to have done to know it, or null"}

--- FILE: {{FILE}} ---
{{BODY}}
