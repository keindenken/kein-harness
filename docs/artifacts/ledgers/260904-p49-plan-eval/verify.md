# Task: verify a plan's claims about the repository

Read `common.md` first (same directory as this file).

Read your assigned line range of the assigned plan. Extract every claim the plan makes about the repository that can be checked against `base/` by reading: a file or path exists; a symbol, constant, function, test title or CI step exists; a quoted line or anchor (`path#exact text`) is present verbatim; a stated count (N files, N rows, N mentions) is right; a described current behavior is what the code does. Skip claims about the future, opinions, and anything not checkable from the tree.

Cap at 40 claims. Prefer claims the plan builds a decision, a gate, or a story's scope on over incidental ones. Spread them across the range rather than taking the first 40.

For each claim, check it against `base/` yourself (grep, read). Verdict: `TRUE`, `FALSE`, `PARTLY` (true in substance, wrong in a detail — say which), or `UNCHECKABLE` (say why). For FALSE and PARTLY, state what the tree actually says, with the path.

Output, in this order:
1. A table: `#` | plan line | claim (quoted or tightly paraphrased) | verdict | evidence (path, and the actual text where it differs).
2. Totals: TRUE / PARTLY / FALSE / UNCHECKABLE.
3. The three FALSE or PARTLY claims that would do the most damage if an executor believed them, and why (one sentence each).
