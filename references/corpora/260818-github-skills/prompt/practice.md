Below is one file from an agent harness — a prompt, a skill, or an agent definition. It is instruction: it tells a model how to work.

Pull out **what this file actually commits to**. Each commitment is a rule the file imposes or an assumption it rests on, quoted verbatim so it can be checked against the file it came from.

What counts:

- an instruction with a *mechanism* — an order to follow, a threshold, a required artifact, a gate that must pass, a thing that must never happen;
- an assumption the instruction only makes sense under — a step that presumes an earlier one produced something, a check that presumes a particular failure is the one worth catching.

What does not count: a description of the file's purpose, a definition of a term, an example, boilerplate about tone or formatting. If removing the sentence would change nothing about what the model does, it is not a commitment.

For each, also say what it is **about** — three to six words naming the thing being decided, as a practitioner would name it: `judge output ordering`, `plan gate evidence`, `subagent context isolation`, `test-first enforcement`. Not a department and not the file's own name. If two commitments decide the same thing, give them the same words.

Answer with JSON and nothing else: no preamble, no code fence.

{"commitments": [
  {"quote": "<copied verbatim from the file, one sentence or one bullet>",
   "about": "<three to six words>",
   "kind": "rule" | "assumption"}
]}

Ten is plenty for a large file and two is fine for a small one. A file that commits to nothing gets an empty list.

--- FILE: {{PATH}} ---
{{BODY}}
