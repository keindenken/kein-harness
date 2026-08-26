Below is one commitment from a working agent harness — a rule it imposes or an assumption it rests on, copied verbatim from its own file — and beside it, claims drawn from public agent skills written by other people. Each claim is a sentence its author could not have written without having done the thing.

Ask one question: **does what these people learned bear on this commitment?**

Three answers, and the third is the usual one.

- `conflict` — a claim says the commitment is wrong, or that doing it this way produces the failure the claim describes. Not "the claim covers more ground"; the claim has to be evidence *against* what the commitment does.
- `gap` — a claim describes a failure this commitment plausibly runs into and does not address. The commitment must be the natural place to have handled it. A claim about an adjacent subject that nobody would expect this rule to cover is not a gap.
- `none` — the claims are about a different thing, or they agree, or they are too specific to somebody's stack to bear on anything. **Most of these are `none`.** The claims were matched to this commitment by shared vocabulary, which is a weak signal and often the only thing they share.

If you answer `conflict` or `gap`, quote both sides. The commitment's own words, and the claim's own words, copied — not summarised. A finding you cannot quote both halves of is not a finding.

Do not soften a `none` into a `gap` because the pairing looks deliberate. It was made by counting words.

Answer with JSON and nothing else: no preamble, no code fence.

{"verdict": "conflict" | "gap" | "none",
 "commitment_quote": "<the commitment's own words, or null>",
 "claim_id": "<the id of the claim that bears on it, or null>",
 "claim_quote": "<that claim's own words, or null>",
 "what": "<one or two sentences: what the claim establishes that this commitment should answer to — null when verdict is none>",
 "change": "<what would have to change in the harness file, or null>"}

--- COMMITMENT ---
file: {{FILE}}
kind: {{KIND}}
{{COMMITMENT}}

--- CLAIMS FROM OTHER PEOPLE'S SKILLS ---
{{CLAIMS}}
