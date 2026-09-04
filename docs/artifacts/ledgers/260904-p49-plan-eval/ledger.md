# Task: build the execution ledger from one plan, and record what the plan did not give you

Read `common.md` first (same directory as this file).

You are the lead who has to execute the assigned plan with a team of workers, one story at a time. Read the kickoff document, then the whole assigned plan. Do not read the other plan.

For every story the plan defines, write a ledger entry:
- `id`, `title`
- `scope`: the files a worker may change, as the plan gives them or as you had to infer them (mark which)
- `completion_condition`: one paragraph, bounded and testable, in your words from the plan's text; cite the plan lines it comes from
- `verification_path`: the commands or checks that would show it done; cite lines
- `invented`: every material decision you had to make yourself because the plan did not — architecture, scope, acceptance semantics, safety, or which of two readings the plan meant. Quote the ambiguity with line numbers. An empty list is a legitimate answer; a padded list is not.
- `would_ask`: questions you would have to send back to the plan's owner before dispatching a worker; empty if none
- `one_round`: your judgment whether one worker could finish this story in one sitting and one review round. Support it with counts: files in scope, distinct acceptance claims in the completion condition, gates the story must implement and drive to a failing state, evidence gates it must run. Say `yes`, `no`, or `split` (and how you would split it).
- `reading_cost`: how many plan lines a worker must read to do this story alone (the story's section plus every section it points to), as a line count and a list of the sections.

Then a closing section:
- Which stories you could dispatch today without a question, which need one, which you could not dispatch.
- The plan's material decisions that are parked for the owner: list them with line numbers, and say for each whether a worker can proceed without the answer.
- Anything in the plan that would make a worker do wasted work: text addressed to reviewers rather than executors, repeated constraints, gates guarding things no story changes. Cite lines.

Use the ledger shape above as headed markdown per story, not JSON.
