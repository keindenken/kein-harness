# Common rules for every evaluator

You are evaluating an implementation plan for a repository. Two plans exist for the same phase, written by different teams from the same starting point. They are named only `plan-A.md` and `plan-B.md`. **Do not try to infer which team wrote which, and do not mention any guess.** Judge only what is on the page.

Paths (all absolute):
- Plans: `/private/tmp/claude-501/-Users-kein-Documents-workspace-dev-worktree-kein-harness-instrument/6fde1749-c119-492f-9599-adfa17248f3d/scratchpad/p49-eval/plan-A.md` and `.../plan-B.md`
- The repository exactly as it stood when both plans started: `.../p49-eval/base/` (a plain tree, not a git checkout; read and grep it freely; never modify it)
- The owner's kickoff document both plans answer: `.../p49-eval/base/docs/handoff/260903-phase-49-kickoff.md`
- Write your output to the file named in your task. Also return it as your final message.

Every judgment must cite a line number in the plan (`plan-A.md:123`) or a path in `base/`. A judgment with no citation is invalid and will be discarded. Prefer fewer, cited findings over many uncited ones. Do not summarize the plans back; the reader has them.

Write plain prose and tables. No praise, no hedging paragraphs. English.
