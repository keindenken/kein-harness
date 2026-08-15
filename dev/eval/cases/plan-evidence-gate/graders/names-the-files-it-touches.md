---
type: llm
path: PLAN.md
weight: 1
---

Judge the `PLAN.md` reproduced below, not the assistant's reply. Its contents are supplied to you in full; do not look for it on disk, and do not fail it for not being in your working directory. If no artifact was supplied at all, fail.

The application is three modules in `marginalia/` beside the requirements document: `db.py`, `search.py`,
`notes.py`. They are on disk and readable. This grader asks whether the plan's implementation steps say which
of them each step changes, precisely enough that a reader opens the right file without guessing.

Pass if every step that changes existing code names the file it changes, and the name is rooted well enough to
locate — `marginalia/search.py`, or `fixture/marginalia/search.py`, or the same path with a leading `./`. A
step that creates a new file has to say where the new file goes, by the same standard. Naming a function or a
constant inside the file is better still, but the file is the bar.

Fail if the plan:

- describes the work as framework-agnostic, or as guidance an engineer maps onto the application later, when
  the application is right there;
- refers to what it changes only by role — "the search layer", "the save path", "the DB access code" — with
  no file behind it;
- names files for some steps and leaves others with nothing;
- gives an absolute filesystem path for a file in the repository, or one containing a home directory or a
  machine name. That is wrong even when it currently resolves, because the plan is read from another
  checkout.

The runtime data directory is not a repository path. The requirements ask the plan to name the index file
that sits beside `notes.db` in whatever directory `db.library_directory()` resolves to, and that directory is
machine-specific by construction. Naming the file — or describing the directory through the function that
resolves it — is right, and does not fail this grader. Writing out one machine's expansion of it as though it
were the location does.
