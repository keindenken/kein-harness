# `fsd`: what has closed

Items moved out of `docs/skills/fsd/open.md` once closed, kept verbatim with a note on what closed them.

## What the `fsd` SKILL.md had to say (story U5)

Closed 2026-09-19: `2d94cb8` — the skill text states each of these, and the 2026-09-23 run corrected three of its sentences against the code.

Done in 2d94cb8: the skill text states each of these, and the 2026-09-23 run corrected three of its sentences against the code.

## Left open by the 2026-09-23 run

Closed 2026-09-26: the mid-stage Stop block's golden text (`hook.py`'s `_active_no_gap_reason`, mirrored in `check-fsd-hooks`'s `_expected_active_no_gap_closing`) now says a lead may end the turn after confirming a waited-on lane is alive, rather than only naming the check; `report` in `state.py` withholds the "Answer by re-invoking /kein:fsd" invitation once the run's own lifecycle is terminal (`TERMINAL_LIFECYCLES`), proven by a parked, unanswered whole-run question surviving a structural `halt` in `check-fsd-state`'s `scenario4-guard-scope-violations`; `claude -p --resume` was measured too and does not re-arm frontmatter hooks either, the same as `-c -p` (finding `260926-claude-resume-does-not-rearm-frontmatter-hooks.md`), and neither `fsd`'s `SKILL.md` nor its references claim or depend on hooks surviving a process continuation, so nothing there needed correcting; and `closeout.md` step 4 now names all three of `halt`'s refusal cases -- lifecycle not `active`, an empty `--reason`, and close would in fact succeed -- rather than only the third, the one this step ever reaches.

Carried in that run's receipt; the run record is `docs/skills/execute/260923-audit-stopping-rule.md`.

- **A waiting lead is not told it may wait.** The mid-stage Stop block tells a lead waiting on another lane to check the lane is alive, but not that it may then end the turn for the lane's notification. Nothing stalls — `stop_hook_active` lets the second stop through — but a literal reader may poll in-turn or read a healthy wait as a reason to exit. The fix moves the block's golden text in `check-fsd-hooks`.
- **A halted run's report invites an answer nothing can accept.** When a structural refusal ends a pause attempt in `halt`, `report` still lists the recorded question with "Answer by re-invoking /kein:fsd", and `answer` then refuses a terminal state.
- **Whether `claude --resume` re-arms frontmatter hooks is unmeasured.** The 2026-09-19 probe measured only a `-c -p` continuation, where they did not fire.
- **`closeout.md` step 4 states `halt`'s refusal as one case.** `halt` is also refused on a run that is not active and on an empty reason; neither is reachable from the step as written, so this is wording.

## A hand-authored checkpoint could open a span with a made-up hash

Closed 2026-09-29: 1d21b12 — `checkpoint` now refuses any appended `agents_md` span on any transition and any move into `paused`, so a span's hash always comes from `resume` or `respan`. The same commit added `respan`, which opens a span on an active run whose AGENTS.md reached the branch from another ref, so a rebase onto an owner commit no longer ends in `halt`.
