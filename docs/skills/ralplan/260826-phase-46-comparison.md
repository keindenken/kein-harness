# phase-46 — 두 하네스를 같은 과제에 붙여보고 나온 것

descvi의 phase-46(v3.5 ring-furniture restyle)을 kein `ralplan`과 기존 하네스에 각각 붙였다. 2026-08-24~26에 관측했고, 아무것도 고치지 않았다 — 예외는 §5의 라벨 검증기 한 줄뿐이다.

여기 있는 항목은 전부 `docs/open-threads.md`에서 옮겨온 것이다. 그 파일에는 포인터만 남겼다.

## 0. 근거 자료

| 자료 | 위치 |
|---|---|
| 진입 트레이스 (기존) | `docs/260824-omc-plan-kickoff.md` |
| 진입 트레이스 (kein) | `docs/260824-kein-plan-kickoff.md` |
| 산출물 (기존) | `docs/260825-omc-v35-ralplan.md` |
| 산출물 (kein) | `docs/260826-kein-v35-ralplan.md` |
| 런 원장 (kein, 7라운드 전량) | `descvi/repo/phase-46-ring-furniture-restyle-in-kein/.agents/kein/runs/ralplan/260824-222055-…` |

**둘 다 승인본이 아니다.** kein 쪽은 `Status: Draft`, "TERMINAL UNAPPROVED" — 7라운드에서 owner의 정지 규칙으로 멈췄다. 기존 쪽은 그 텍스트에 2라운드를 돌고 "REVISION 5 — FINAL TEXT ROUND, NOT YET APPROVED"다. 아래의 모든 비교는 미승인 문서 두 개 사이의 것이다.

---

## 1. 아티팩트가 자기 리뷰 이력을 싣고 있고, 그건 분량 문제이자 블라인드 레인에 뚫린 구멍이다

범위가 완전히 같지는 않고, 그걸 감안해도 격차가 남는다.

|  | 기존 | kein |
|---|---|---|
| 줄 | 610 | 1069 |
| §3 룰링 하위절 | 8 | 22 |
| pre-mortem 시나리오 | 4 | 13 |
| 자기 이력 언급 | 20 (본문) | 149 |

분량은 증상이다. 원인은 RALPLAN이 아티팩트 하나를 라운드마다 제자리에서 고치고, **각 라운드의 수정이 "현재 상태"가 아니라 "이전 텍스트에 대한 diff"로 쓰인다**는 것이다. pre-mortem 13개의 순서가 S1–S8 다음 S13, S12, S11, S10, S9인 것도 같은 이유다 — 발견된 라운드 순이고, 플랜 독자에게는 의미 없는 정렬이다.

### 사실과 귀속이 섞여 있고, 하나만 남아야 한다

**사실** — 수정이 확립한 것. "pill의 바깥 도달은 밴드 전체다", "R42-D3 clause 4가 shipped build에서 깨져 있다", §2.11의 수정된 부등식. 실행자에게 필요하다.

**귀속** — 어느 리비전이 틀렸는지, 그게 뭐라고 주장했었는지, "P46-1's own class landing on P46-1's own section, twice". 필요 없다. **현재 룰링이 실행자가 행동할 수 있는 전부다.**

### 그리고 귀속은 소음이 아니라 계약 위반이다

`review-contract.md`:

> A fresh reviewer receives **no previous finding, verdict, reviewer identity, revision note, change summary, claimed fix, closure result**, or expected outcome.

그리고 `Status`/`Status reason`을 패키지에서 빼는 이유를 이렇게 쓴다 — 2라운드 이후의 `Status reason`은 "라운드와 그 verdict와 리비전이 바꾼 것"을 명명하게 되고 그건 **"four of the things in that list"** 라고.

**계약이 누수를 정확히 찾아 두 줄을 막았다. 그 네 가지가 본문 전체에 퍼져 있고, 패키지는 본문을 통째로 무삭제로 싣는다.** 블라인드라고 들은 레인이 이런 걸 읽는다:

```
⚠ Corrected at round 1. Revision 1 named two and omitted the one that matters.
### S13: (NEW, round 5) a row is green under one of the two invocations
```

`plan-gate.md`도 같은 목표를 자기 말로 적어놨다 — *"a reader who opens the plan cold gets that answer without reconstructing the round history"*. 그 줄 아래로는 아무것도 강제하지 않는다.

**그래서 라운드 수를 "루프가 수렴한다"는 증거로 단순하게 읽을 수 없다.** 각 라운드의 블라인드 중 일부는 이미 소진된 상태였다.

### 게이트로 막는 안은 철회했다

한때 `state.py`의 `review_text()`(= 아티팩트 − 두 줄, 레인이 읽는 바로 그 텍스트) 위에 검사를 거는 안을 올렸다. **함수가 이미 있으니 싸다**는 게 이유였고, 그건 설계 근거가 아니다.

무엇을 매칭해야 하는지 보면 성립하지 않는다. 같은 위반이 최소 네 모양으로 나온다 — `Corrected at round 1`, `revision 2's was circular`, `an earlier draft claimed`, `this was previously bounded at six`. 문법이 없다. 반대 방향은 더 나쁘다: 플랜은 `R42-D1 clause 4`, `phase-45`, `round-2 consensus`를 **정당하게** 인용한다. 단어에 걸면 남아야 할 인용이 걸린다. 안전할 만큼 느슨하면 아무것도 못 잡고, 뭘 잡을 만큼 엄격하면 맞는 글을 막는다.

### 규칙이 갈 곳

`prompts/planner.md`는 **아니다.** canonical이고 넷이 공유한다 — `plan`(단발), `ralplan`(매 라운드), `ocs ask`, `ocs team`. "어느 리비전이 틀렸는지 쓰지 마라"는 리비전이 없는 곳에서 의미가 없고, 그건 단발 사용 전부다.

맞는 집은 **`plan-gate.md`** — 첫 줄이 *"What RALPLAN adds to the artifact the `plan` skill produces … only the overlay is here"* 이고, `Status`에 대해 같은 원칙을 이미 담고 있다. 그리고 리비전 순간 Planner에게 실제로 도달하는 건 `review-contract.md`의 correction brief다.

### 밀도는 게이트가 아니라 그레이더로

본문 100줄당 이력 언급은 `dev/eval` 케이스 모드가 채점할 수 있는 숫자다. 문법 없는 것에 맞는 강도는 그것이다 — 보고하고 막지 않는다. 템플릿을 바꾸기 **전에** 갖고 있어야 변화를 입증할 수 있다.

### 기존 하네스에는 집이 있다

`## 10. Revision log` — 이력에 섹션 하나를 주고 본문은 놔둔다. `plan-template.md`가 이름 대는 건 Status, Status reason, Open Questions, Evidence Gates, Pre-mortem뿐이고 **라운드 이력에는 집이 없다.** 그래서 전부로 퍼진다.

---

## 2. 원장이 말해주는 것 — 루프가 자기 감사 기계를 키우고, 그걸 다시 감사한다

§1은 완성된 아티팩트 두 개만 보고 쓴 것이다. 그 중 하나를 만든 런이 라운드별 플랜 스냅샷·findings·레인별 리뷰어 파일을 전부 남겨놨다.

### 라운드 1은 깨끗하고, 나머지는 루프가 만든다

| 라운드 | 줄 | 이력 언급 | 100줄당 |
|---|---|---|---|
| 1 | 585 | 5 | 0.9 |
| 2 | 685 | 65 | 9.5 |
| 3 | 799 | 170 | 21.3 |
| 4 | 892 | 231 | 25.9 |
| 5 | 971 | 269 | 27.7 |
| 6 | 1008 | 313 | 31.1 |
| 7 | 1046 | 344 | 32.9 |
| 최종 | 1070 | 377 | 35.2 |

줄은 1.8배, 이력은 **75배**. 가장 큰 한 걸음은 라운드 1→2로, Planner가 처음 findings를 받는 지점이다.

이건 "Planner가 원래 장황하다"를 배제하지만 **루프의 어느 부분인지는 가르지 못한다.** Planner가 respawn이 아니라 resume되는 것이 원인이라는 앞선 주장은 근거가 얕다 — resume은 실재하고 문서화돼 있지만 correction brief의 내용도 똑같이 후보이고, 이 표로는 둘이 안 갈린다.

### 어느 라운드도 두 레인을 동시에 통과하지 못했다

```
r1  arch MUST_FIX  critic MUST_FIX   findings  8
r2  arch MUST_FIX  critic MUST_FIX            10
r3  arch MUST_FIX  critic MUST_FIX             6
r4  arch MUST_FIX  critic MUST_FIX            10
r5  arch MUST_FIX  critic MUST_FIX             8
r6  arch MUST_FIX  critic PASS                 4
r7  arch PASS      critic MUST_FIX             3
```

끝에서 통과 레인이 번갈아 바뀐다. 한 독자를 만족시킨 개정이 다른 독자에게 뭔가를 노출시키는 모양이다.

### 리뷰어들이 "이건 재발"이라고 두 번 말했다

> **round 3, critic** — "This is the identical defect the plan diagnosed for requirement item 7 and repaired with DR46-8/G46-17, left standing for requirement item 10."

> **round 7, critic** — "This is the THIRD instance of the shape §3.2 and §3.18 each corrected elsewhere, un-applied here."

그 shape — 테스트 row를 한 단위로 취급하지만 실제로는 여러 주체 여러 leg인 것 — 는 라운드 2, 3, 5, 6, 7에 같은 계약에 대해 나타난다.

`SKILL.md:53`이 정확히 이걸 위한 문장이다:

> When the same defect class recurs against the same contract, **revisit the contract or underlying design instead of polishing the same prose again.**

**규칙이 있고, 리뷰어가 재발을 소리내어 말했고, 루프는 계속 산문을 다듬었다.**

### 수리로 주조된 절이 다음 라운드의 결함이 됐다 — 3전 3승

| 절 | 주조 | 반증 |
|---|---|---|
| §3.20 anchor citation 인벤토리 | r3 | r4 — "omits S46-0 entirely" |
| §3.21 test-home 정책 | r4 | r5 — "measured against ONE jsdom", 이 리포는 둘로 돌린다 |
| §3.22 sweeps, fixed point까지 | r5 | r6 — 자기 pass-6 문장이 자기 read-form 규칙을 깬다 |

**플랜이 4라운드에 자기 실패 양식을 예측했고 두 번 더 했다.** pre-mortem에 그대로 있다:

> `S12: (NEW, round 4) a repair mints a gate row, and the row is the next round's defect`

### 그 findings는 취향이 아니고, 그 장치는 아무 계약에도 없다

결과절이 구체적이다:

- r4 §3.20 누락 → "the FIRST story of the phase lands with CI's citation gate RED"
- r5 fixed point 반증 → requirement item 6이 UNGATED, "both catchers sweep 1 credits it to are **green on a do-nothing build**"

**do-nothing 빌드에서 green인 게이트**는 이 하네스가 도처에서 거부하는 실패다. 취향이 아니다.

그런데 §3.20·§3.21·§3.22 중 어느 것도 `plan-template.md`가 이름 대지 않는다. Planner가 **리뷰어에게 완결성을 입증하려고** 만든 것이고, 최종본 1069줄 중 **173줄(16%)** 이며, 실행자는 하나도 필요 없다 — 죽는 인용의 인벤토리, 테스트가 어디 사는지의 정책, 4패스 sweep 기록은 **리뷰어를 향한 증거**지 구현 지시가 아니다.

findings를 주체별로 거칠게 나누면 (작업 / 플랜 자신의 검증 장치) 라운드별로 6/2, 4/6, 2/4, 3/7, 3/5, 3/1, 2/1이다. **라운드 1은 리스타일 얘기고, 2~5는 대체로 플랜이 라운드 1에 답하려고 만든 것을 감사한다.**

### 그래서 §1의 두 불만이 한 뿌리다

```
149건 이력 귀속  =  "당신 지적을 반영했다"
173줄 감사 장치  =  "나는 완결하다"
```

**둘 다 리뷰어를 향한 내용이고, 둘 다 구현자를 향한 문서 안에 있다.** 라운드 1 플랜은 앞의 것이 5건, 뒤의 것이 0줄이었다. 리뷰어용 산출물을 놓을 곳이 어디에도 없어서 전부 아티팩트 본문으로 들어간다.

### 5라운드 트리거가 한쪽만 담은 질문으로 발화했다

`SKILL.md:51`이 5라운드 근처를 진단 트리거로 만들고, `:53`이 재발 시 계약을 다시 보라고 한다. 그 지점에서 런은 owner에게 계속할지 물었고, "closing 추세라 계속"이 `(권장)`을 달고 있었으며 계약을 지목하는 선택지는 없었다.

**두 규칙이 그 질문에서 만나는데 하나만 질문에 실렸다.** 재발 규칙이 결과를 바꿀 수 있었던 유일한 지점이라 여기 같이 적는다.

---

## 3. 진입 비용 — 그리고 대부분은 프로세스 탓이 아니다

플래너 디스패치까지: 기존 약 4단계, kein 약 12단계(그중 7개가 Bash).

### 차이가 없는 곳

기존 MCP 서버는 도구 67개를 노출한다 — state, notepad, project memory, shared memory, wiki, LSP 브리지, Python REPL, trace 리더. **영속화 표면이고, 그 트레이스에서 한 번 호출됐고, 진입을 싸게 만든 게 아니다.**

훅은 11개 이벤트에 22개고, `SessionStart` 셋이 최대 6000자를 우선순위대로 주입한다 — project memory, notepad priority, pending tasks, restored modes. 사용자가 타이핑하기 전에 끝난다. **그게 온보딩이고 트레이스의 시계에 안 잡힌다.**

이건 양보해도 된다. 다른 아키텍처지 이쪽의 결함이 아니다. 양보 못 할 건 **이쪽에서 최적화 가능한 걸 안 한 채로 두는 것**이다.

그리고 그마저 과장이다. `descvi/repo`가 `OMC_SKIP_HOOKS`로 `skill-injector`와 `keyword-detector`를 끈다. **인젝터를 끈 상태로도 4단계에 진입했다.**

### 차이가 실제로 있는 곳

`2plan`은 한 파일 62줄, references 없음. `ralplan`은 73줄 + references 4개 + `plan`의 SKILL.md와 템플릿 — **6파일 약 330줄**이고, `cd … && cat` 한 번에 하나씩 읽었다.

### `stage`는 이 문서에 정의가 없다

`## Required Files`가 "Read these when their stage begins"라고 쓰는데, 런의 위치를 가리키는 어휘가 셋 있고 그중 정의 없는 것으로 쓰고 있다:

| 어휘 | 정의된 곳 | 값 |
|---|---|---|
| Workflow 단계 | `SKILL.md ## Workflow` | 1..7 |
| transition | `ocs state ralplan --help` | start / open / block / revised / approve / complete / abort |
| phase | `state.json` | initializing / drafting / drafted / reviewing / revising / gathering_evidence / blocked / interrupted |
| round | `state.json` | 정수 |
| **stage** | **없음** | — |

정렬하면:

```
step 1–2   (start 이전)          phase 없음
step 3     start          →      drafted,   round 0
step 4     open           →      reviewing, round +1   ┐
step 5     (레인 디스패치)         reviewing            │ 반복
step 6     block → revised →     revising → drafted    │
step 7     approve/complete →    (receipt)             ┘
```

step 4~7이 루프이므로 읽기를 단계 번호에 거는 것도 틀린 앵커다.

### 실제 필요 시점

| 파일 | 필요한 지점 |
|---|---|
| `state-schema.md` | `start` 이전 |
| `plan-gate.md` | 첫 `open` 이전 (Status·해시) |
| `review-contract.md` | 초안 이후, 레인 디스패치 이전 |
| `lanes.md` | 호출이 벤더를 지정할 때만 |

`review-contract.md`만 유예가 실재한다 — 그 사이에 Planner 디스패치 하나가 통째로 들어간다. 나머지 둘은 진입에 필요하다. 즉 **지금 문장은 존재하지 않는 유예를 제안하고 있고**, 리드가 셋을 킥오프에 읽은 건 그 유예가 없다는 걸 알아본 것에 가깝다.

앵커는 **transition 이름**으로 쓰는 게 맞다. 리드가 실제로 `ocs state ralplan open`을 타이핑하고, 그 단어는 CLI에도 `state.py`에도 있으며 `round`·`phase`와 겹치지 않는다. `SKILL.md:27`의 `stage-specific package`도 `lane-specific`이다 — `review-contract.md`가 *"a separate package for each **lane**"* 이라고 쓴다.

**이 두 문장은 `6368b16`이 반증했다.** 불릿 넷이 이미 각자 시점을 달고 있어서(*"before creating or resuming a run"*, *"before setting a status or computing a hash"*) transition 이름을 끌어올 자리가 없었다 — 앞엣것은 resume까지 덮고 뒤엣것은 첫 `open`을 정확히 가리키니 transition 이름보다 낫다. 리드 문장만 지웠고 어휘는 늘지 않았다. `lane-specific`도 틀렸다: `:27`이 Planner도 같이 디스패치하는데 Planner는 레인이 아니고 계약에 Planner 절이 없다. 그래서 계약 자체를 가리키게 했고, `c360041`이 Planner를 그 줄에서 빼면서 남은 게 실제로 레인 둘이 됐다. **위 표의 `stage` 행은 이제 리포에 없다** — §6이 그 자리에서 나온 후속을 잇는다.

### 구체적인 것 둘, 하나는 결함이고 하나는 아니다

**`ls -R`은 결함이 아니다.** 싼 오리엔테이션이고, 이걸 낭비로 읽으면 비용에 관한 규칙이 아니라 정돈에 관한 규칙이 된다.

**`plan`의 계약을 `cat`으로 가져온 건 결함이다.** `ralplan/SKILL.md:14`가 "the only skill it runs is `plan`"이라 하고 Required Files 줄이 계약은 "arrives with the `plan` invocation"이라 하는데, 리드가 둘 다의 반대를 했다. 두 문장 다 틀리지 않았고, **이미 열려 있는 디렉터리 목록을 이기기엔 너무 조용하다.** 서술이 아니라 거부로 강화해야 한다.

### 측정 자체에 대한 주의

"플래너까지의 단계 수"는 **세션 시작에 선불하는 쪽에 구조적으로 유리하다.** 기존 하네스는 플랜을 안 짜는 세션에서도 매번 낸다. 스킬 호출 시점부터 재면 그 비용이 정의상 안 보인다. **6파일 대 1파일은 실재하고, 4단계 대 12단계는 부풀려져 있다.**

---

## 4. 리드가 requirements를 저술했다 — 계약은 요약을 요구했는데

`ralplan/SKILL.md:35`:

> preserve the original requirements **by path and hash** when possible; otherwise store a **prompt-safe summary** and its hash

`state.py`의 `start --input`도 requirements 경로를 받는다. 대체안은 *요약*이다.

phase-46 킥오프는 대신 132줄짜리 `requirements.md`를 런 디렉터리에 썼고 250줄을 넘겼다. 출처 문서들은 리포에 이미 있고 그 안에 경로로 인용까지 돼 있다. **계약의 어느 쪽도 이걸 요구하지 않는다** — 경로가 있으니 첫 번째 갈래가 적용되고, 만들어진 것은 어느 모로 보나 요약이 아니다.

무해하지 않다. **리드는 루프에서 독립 리뷰를 안 받는 유일한 에이전트다.** 리드가 혼자 쓴 requirements가 아래 모든 레인의 지배 텍스트가 되는데, 그게 원본을 제대로 옮겼는지 아무것도 확인하지 않는다.

**계약 쪽 잘못일 가능성이 열려 있다.** "preserve by path and hash"는 requirements 파일이 하나 있다고 가정한다. tracker + 스펙 한 절 + known-issues + owner 룰링 셋으로 조립된 페이즈에는 보존할 단일 경로가 없고, 요약 갈래는 실제로 발생하는 케이스에 비해 구멍이 너무 작을 수 있다. 그렇다면 고칠 것은 **자기가 뭔지 정직하게 말하는 세 번째 선택지 + 분량 상한**이지, requirements인 척하는 리드 저술 문서가 아니다.

---

## 5. 20분짜리 라운드가 문장부호에 쓰였다 — 검증기를 리드만 돌릴 수 있어서

`validate-plan`이 phase-46 플랜의 Evidence Gate 넷을 거절했다. 내용은 맞았고, 라벨이 `- Pass path (조건): …`인데 `_evidence_gate_errors`가 `^- Pass path:`를 요구했다.

### 비용 구조

플래너가 20분 15초 돌고 반환했고, 리드가 검증했고, 1초면 스스로 잡을 수 있었던 형식 수정을 위해 resume됐다. **`validate-plan`은 정확히 한 곳에만 문서화돼 있다** — `state-schema.md`, 리드용 레퍼런스다. `prompts/planner.md`는 이 명령의 존재를 모른다. **아티팩트를 쓰는 에이전트가 아티팩트의 형식을 확인할 방법이 없다.**

새 메커니즘은 필요 없다. 검증기가 있고, 명령 한 줄이고, 플래너는 이미 정식 플랜 경로를 받는다. 빠진 건 "반환 전에 돌려라" 한 줄인데 canonical 프롬프트 수정이라 조용히 할 일이 아니다.

### 검사가 자기 목적보다 엄격했다 — 수리 완료 (`8bedb2e`)

존재 이유는 게이트가 여섯 개 개념을 담았는지, 특히 정지 경계가 있는지다(`plan-template.md`: *"a gate whose unexpected result has no stop boundary is not a gate"*). 실제로 테스트한 건 리터럴 `^- Pass path:`였다.

**그리고 이 리포가 같은 판정을 이미 내렸는데 절반만 통보받았다.** `dev/eval/cases/plan-evidence-gate/case.yaml:41`이 `vocabulary-gate-shape`를 "the label, not the label plus a colon"으로 완화한 기록을 갖고 있다. 이유는 `- Alternate path (all shipped targets report FTS5_AVAILABLE=0):`에 0점을 준 것이고, 그 플랜에 대한 판정은 *"had used the template's vocabulary more thoroughly than the template asks, and the control read it as absent"* 다.

같은 구성, 같은 결론, 먼저 적혀 있었다. **완화는 제안이 아니라 정합성 수리였다.**

### 커버리지를 쓰다가 두 번째 결함이 나왔다

값을 `\s*\S`로 매칭했고 `\s`는 개행을 포함한다. `re.MULTILINE`이라 `- Pass path:`(값 없음)가 **다음 줄의 첫 글자를 값으로 먹었다.** 하네스 역사상 모든 빈 라벨이 통과했다.

**여섯 필드를 읽는다는 검사가 다섯 개와 줄바꿈 하나를 읽고 있었고, 여섯 개를 다 채운 플랜엔 RED, 다섯 개만 채운 플랜엔 GREEN이었다.** 정확히 뒤집혀 있었다.

```python
# before
rf"^- {label}:\s*\S"
# after
rf"^- {label}\b[^:\n]*:[^\S\n]*\S"
```

`validate-plan`에는 테스트가 하나도 없었고, 그게 둘 다 살아남은 이유다. 지금은 `check-ralplan-state`에 양방향으로 있다 — 한정어 통과 / 정지 경계 누락·다른 라벨·빈 값 거부.

### 아예 뺄지는 아직 열려 있다

유지 논거를 처음 낸 건 나였고 약했다. "`plan-gate.md`가 승인을 게이트의 열거 가능성에 걸어놨다"는 것이었는데, 확인해보니 **`_evidence_gate_errors`가 하네스에서 Evidence Gate를 파싱하는 유일한 코드다.** downstream 소비자가 없다. 기계 독자를 보호하는 게 아니라 **저자가 여섯 개를 적었는지 확인**하는 것이고, 형식 검사의 옷을 입은 내용 완결성 검사다.

그 완결성은 이미 레인이 소유한다. `review-contract.md`가 Critic에게 *"missing failure behavior"* 와 *"whether the supplied gate could genuinely fail"* 을 준다. 정지 경계 없는 게이트가 정확히 그 둘이다.

**지금까지의 장부: 20분 라운드 하나 지출, 기록된 캐치 0.**

지우기 전에 모르는 것 둘 — Critic이 라벨 부재를 파서만큼 안정적으로 잡는가, 그리고 저 검사가 한 번이라도 뭘 잡았는가. 둘 다 런 원장에서 답이 나온다.

### "정형화" 느낌은 실제보다 좁다

`validate_plan_text`가 무조건 강제하는 건 셋뿐이다 — 레벨1 제목, 유효한 `Status` 하나, 비어있지 않은 `Status reason`. `_evidence_gate_errors`는 `## Evidence Gates` 헤딩이 없으면 에러를 아예 반환하지 않고, 템플릿은 그 shape와 pre-mortem을 둘 다 optional이라 부른다.

**진짜 함정은 하나다: 선택 섹션이 한 번 쓰이는 순간 엄격 형식이 된다.** 헤딩 한 줄이 리터럴 라벨 여섯 개를 물고 온다. 이건 문장부호 바운스와 같은 결함이지 별개가 아니다.

"개발 전용 같다"는 느낌은 다른 데서 온다. `plan`의 description이 스스로 "implementation plan"이라 하고, 템플릿 예시가 dev 모양이다. 라벨 검사를 풀든 지우든 그건 안 움직인다.

---

---

## 6. ①②를 고치다 나온 것 — 셋 다 아직 안 정했다

`8bedb2e`·`6368b16`·`c360041`로 A·①·②가 닫혔고, 그 과정에서 표에 없던 스레드 셋이 나왔다. 셋 다 근거는 여기 있고 판정은 없다.

### closure audit이 재량으로만 존재했고, 7라운드 내내 한 번도 안 켜졌다

§2가 "루프가 재발을 못 잡았다"고 쓴 것의 한 단계 아래다. 잡을 계기가 있었는데 재량이었다.

`review-contract.md:48` — *"A previous live reviewer **may** perform a primed closure check for a subtle, high-risk, partial, or reworded correction."* 조건 넷을 리드가 판정하고, 판정 어휘는 없고, positive는 승인 못 한다.

descvi의 `2plan`은 같은 것을 상설 계기로 쓴다. `:25-28`:

> - **CLOSURE AUDIT (primed).** Hand it the required-changes list; require a per-item verdict — CLOSED / PARTIAL / NOT CLOSED / **REWORDED-ONLY**
> - **UNPRIMED re-review.** A FRESH agent, current text plus the quality bar
>
> Running only the first rubber-stamps a list; **running only the second never notices a reworded fix.**

**phase-46은 7라운드 전부 두 번째만 돌았다.** 원장의 verdict 표에 closure check가 없다. 그리고 §2가 기록한 재발이 정확히 첫 번째 계기가 보는 모양이다 — 라운드 7 critic의 *"the THIRD instance of the shape §3.2 and §3.18 each corrected elsewhere, **un-applied here**"*. 다른 데서 고쳐놓고 여기엔 적용 안 한 것은 이전 텍스트를 본 레인만 볼 수 있다.

정해지지 않은 것 셋:

- **재량 → 상설이 맞는 값인가.** 매 라운드 레인 하나가 순증이고, 그건 이 하네스가 다른 곳에서 계속 묻는 상시 비용 질문이다. 발화할 때만 무는 비용이 아니라 매 라운드 무는 비용이다.
- **`2plan`은 later round의 레인을 "무엇이 바뀌었는지"로 고른다**(`:23`). ralplan의 레인 집합은 고정이고, 그 고정이 블라인드 대칭성을 사고 있다. 두 설계가 다른 것을 사고 있어서 한쪽을 그대로 옮길 수 없다.
- **판정 어휘가 진짜 산출물일 수 있다.** REWORDED-ONLY는 프레시 레인이 원리적으로 못 내는 판정이고, 어휘가 없으면 primed 레인을 켜도 "고쳐졌다"로 수렴한다. 어휘만 `review-contract.md`에 넣고 재량은 그대로 두는 중간 수도 있다.

### `## Workflow`의 번호는 앵커가 아니다

`stage`와 같은 병이고, `6368b16`이 그 단어를 지우면서 이쪽이 드러났다.

step 4~7은 루프다(§3의 정렬표). 번호는 순차를 암시하고, 루프에는 없는 것을 암시한다. 그리고 이미 살아있는 의존이 하나 있다 — step 3이 *"Revisions … happen in **step 6**"*이라고 안에서 자기를 참조한다. 밖에서의 참조는 더 나쁘다: ②의 초안이 "step 3 gives … step 6 asks"였고 그게 철회된 이유가 이것이다.

`2plan`은 번호를 안 쓴다 — "Round 1", "Then: ONE consolidated revision brief", "Later rounds". 이름은 편집을 견딘다.

값이 붙는 지점: §3의 어휘표가 5개였고 `stage`가 빠져 4개(Workflow 단계 / transition / phase / round)다. **Workflow가 번호 대신 `state.py`의 이름을 쓰면 "Workflow 단계"가 흡수돼 3개로 떨어지고, 남는 셋은 전부 기계가 정의하는 것이 된다.** 어휘를 새로 만들지 않고 줄어드는 유일한 경로다.

안 정한 것: 이름을 transition 이름(`start`/`open`/`block`/`revised`/`approve`/`complete`)으로 할지, 아니면 setup / round / close 같은 상위 이름으로 하고 그 안에 번호를 둘지. 앞은 기계와 1:1이지만 step 1~2가 `start` 이전이라 덮이지 않고, 뒤는 새 어휘를 셋 만든다.

### sizing이 선언된 적이 없다

`plan/SKILL.md:26-30`이 리드에게 **브리프에 어느 크기를 골랐는지 말하라**고 하고, 이렇게 쓴다: *"A plan that comes back carrying several unresolved material decisions was sized too small … The size was the lead's call and correcting it is too."*

7라운드 원장 전체에 sizing 선언이 없다. `plan`을 안 돌렸으니 그 문장에 도달한 적이 없다.

§2는 분량 폭증의 원인을 resume이냐 correction brief냐로 못 갈랐다. **선언되지 않은 sizing은 둘 다보다 상류에 있는 세 번째 후보이고, 라운드 1(585줄)에 이미 작용한다** — 라운드 1은 이력 5건·감사 장치 0줄로 깨끗했지만 585줄이었고, 그 585줄이 이후 모든 라운드의 감사 대상이다.

`c360041`이 `plan` 미호출 쪽을 고쳤지만 **그건 아직 런으로 확인된 게 아니다.** 확인은 싸다: 다음 런이 `plan`을 거치면 브리프에 크기가 적히거나 안 적히거나 둘 중 하나고, 적힌 런의 라운드 1 줄 수가 585와 비교된다.

---

## 남은 작업

| # | 항목 | 상태 |
|---|---|---|
| A | 라벨 완화 + 개행 버그 | **완료** `8bedb2e` |
| 1 | `stage` → transition 앵커, `stage-specific` → `lane-specific` | **완료** `6368b16` — 앵커를 도입하는 대신 단어가 나갔다 |
| 2 | `plan` 호출 강제 — 서술을 거부로 | **완료** `c360041` — 거부가 아니라 경쟁하던 허가를 옮겼다 |
| 3 | requirements 계약에 모순이 있는지부터 | 논의 필요 |
| 6a | closure audit — 재량을 상설로, 판정 어휘 포함 (§6) | 논의 필요, 값 제일 큼 |
| 6b | Workflow 번호 → 이름, 어휘 4→3 (§6) | 안 정함 |
| 6c | sizing 미선언 — 다음 런이 확인 (§6) | 관측 대기 |
| 4·5 | 이력 규칙 → `plan-gate.md` + correction brief | 논의 필요 |
| — | `prompts/planner.md`에 `validate-plan` 추가 | canonical 수정, 별건 |
| — | 규격화 A/B — `--variant` + `plan-evidence-gate`, **llm 그레이더로 판정** | 리그는 이미 있음 |
| — | 타 플러그인 arm | 훅·MCP 인정 여부가 선결 |

### 규격화 A/B에 대한 메모

`plan-evidence-gate` 케이스의 그레이더 11개가 이미 두 종류로 갈라져 있다:

- **llm** — `gate-decides-both-paths`(weight 2), `records-the-open-question`, `sequences-the-irreversible-step` 등. 어휘 무관, 개념만 본다. `gate-decides-both-paths`는 `- Pass path:` 같은 라벨을 한 번도 언급하지 않는다.
- **regex** — `vocabulary-gate-shape`, `vocabulary-open-questions`, `vocabulary-status-metadata`. 템플릿 어휘가 나타나는지.

실험은 `--variant strict=<sha> loose=<sha>`로 그대로 떨어진다. llm 그레이더로 판정하고, vocabulary 그레이더는 조작 검사로 쓴다. **어휘를 지우고 어휘 그레이더로 채점하면 자기 조작을 측정한 게 된다.**

그리고 "게이트가 불필요한 데서 뜨는가"는 `plan-no-unknown`이 이미 물었고(`tags: [plan, gate-optionality, ablation]`) 5런 30 replicate에서 `no-evidence-gate` 29/30, `no-manufactured-unknown` 30/30으로 답이 나왔다. **안 넘친다.** 안 물어본 건 6라벨 규격이 품질을 사는가다.
