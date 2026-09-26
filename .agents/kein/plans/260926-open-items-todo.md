# Open items: working list

Requirements: `.agents/kein/requirements/260926-open-items.md` (R1–R8). This file is only the order and the state of each piece.

## 0. Probes (lead) — gate R5, R6, R8, R7.5

- [x] codex resume keeps history, not model/effort/sandbox (findings 260926-codex-resume-keeps-history-not-launch-config.md)
- [x] SessionStart hook sees ORCA_TERMINAL_HANDLE (findings 260926-sessionstart-hook-sees-orca-terminal-handle.md)
- [x] `claude -p --resume` does not re-arm frontmatter hooks (findings 260926-claude-resume-does-not-rearm-frontmatter-hooks.md)

## 1. `check-execute-state` under two minutes (executor) — R7.6

- [x] 283 s → 46 s, assertions kept (1297143)

## 2. ralplan review model (lead, one review lane at the end) — R1, R2, R3 ralplan side, R1.5 fsd, R2.4 wording

- [x] state.py: Status rules, `fix`, `--primed`, `--max-rounds`; check-ralplan-state cases with mutation proof; check-fsd-state fixture helper
- [x] SKILL.md, review-contract, plan-gate, state-schema, fsd decision-policy, execute REVISE sentence
- [x] review lane REVISE (5), all corrected → 8f3593c

## 3. execute state (execute) — R4, R3 execute side, R7.1, R7.2

- [x] 4a41c57, then three review rounds corrected in the kein-open-items worktree → 9f2e508, merged 85ab5e2

## 4. codex resume and `--planner codex` — R5, R6

- [x] `ocs team --resume`, session capture, `--keep` removed; live lane + resume verified
- [x] plan / ralplan `--planner codex` docs; execute lanes.md worktree lifetime
- [x] review lane REVISE (9), all corrected; live chain new-worktree → resume → close verified → eeda04d

## 5. The rest — R7.3, R7.4, R7.5, R8

- [x] R7.3/R7.4 eval + arm PATH scrub → d06aa8d
- [x] R7.5 fsd → 06b3577
- [x] R8.3 `ocs` refuses two harness trees on PATH
- [x] R8.1/R8.2 `ocs home-run`, SessionStart hook, `ocs team` rebinding → eeda04d (R8.3 amended to PATH)

## After all

- [x] closed items moved → 60b834c
- [x] full gate run on merged main 85ab5e2: every dev/kein-dev check and both plugin validations pass; both live descvi runs validate and reconcile
