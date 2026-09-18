# Recording a finding

Record only what was run and observed. A preference, a correction, or the state of ongoing work is not a finding and belongs in memory or the project's own state.

Write `$(findings where)/YYMMDD-<slug>.md`. If `where` exits 3 there is no root; tell the user rather than creating one.

```markdown
---
claim: <what was measured, one sentence, at most 200 characters>
measured: YYYY-MM-DD
versions: <tool version; tool version> | unrecorded
reproduce: <the command to rerun, or the section of this file that describes it> | unrecorded
status: current
---
# <title>

<what was asked, what was run, what came back>
```

`measured` matches the date in the file name. `project: <repository>` may be added. No other keys: `findings check` rejects them, and that refusal is what keeps the store from growing an index or a taxonomy.

When a new finding overturns an old one, set the old file's `status: superseded` and `superseded_by: <new file name>`; never delete it. `disputed` marks a claim that two measurements disagree on.

Run `findings check <file>` until it exits 0. If the root is inside a git work tree, commit the new file there. Report the path, not the content.
