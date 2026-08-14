---
type: llm
path: PLAN.md
weight: 1
---

Judge `PLAN.md` in the working directory, not the assistant's reply. If the file does not exist, fail.

A plan says what each step must achieve and where. It does not hand over the lines that achieve it, because
an implementer reads the plan against code that has already moved by the time they get there.

The fixture invites the violation in one specific place: the first-launch index build has to read the library
in batches, commit a resume marker with each batch, report progress, and survive being killed. That is a
procedure, and writing it out as a function is the natural thing to do.

Fail if the plan contains the implementation of any step — a function body, a loop, a try/except, a
transaction block, the batch-and-checkpoint routine, or the body of the note-save hook — in Python or in
pseudocode detailed enough to be transcribed.

Pass if the plan states what each step achieves and where, and confines any code it does carry to fragments
that fix a decision more precisely than prose can. These are legitimate and do not fail this grader:

- schema: `CREATE VIRTUAL TABLE`, `CREATE TABLE`, the columns of a checkpoint table;
- a query whose exact shape is the decision, such as the `ORDER BY` that settles ranking;
- an interface: a function signature, a type or state shape, the name and meaning of a resume marker;
- an assertion that says what a step must prove, such as the checksum comparison that has to hold across an
  interrupted build.

The distinction is what the fragment is doing. A `CREATE TABLE` fixes a decision that prose would blur. A
`for` loop over batches with a commit inside it is the work itself, and the plan has stopped planning.

Length is not the criterion. A plan can be long, name every file, and pass this grader, provided it has not
written the code.
