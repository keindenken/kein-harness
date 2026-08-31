# phase-47을 두 하네스가 실행했고, 결함을 서로의 트리에 대조했다

kein `execute`와 omc가 같은 base(`a7007ff`)에서 갈라져 descvi phase-47(드래그 재정렬)을 실행했다. 이 문서는 **양쪽이 기록한 결함을 상대 트리에서 찾아본** 결과다. 2026-08-31에 돌렸다.

루브릭도 리뷰어도 쓰지 않았다. 이 리포가 이미 값을 치른 이유에서다 — `260828-p47-draft-comparison.md` §4가 같은 문서를 두 레인이 15/19와 18/21로 센 것을 기록한다. **세는 계기는 못 믿는다.** 대신 양쪽이 커밋과 회고에 남긴 결함을 좌표로 삼고, 상대 브랜치에서 그 코드를 조회했다. 판정이 아니라 조회다.

## 0. 방법

| | |
|---|---|
| 표본 | `phase-47-drag-reorder-in-kein` (브랜치로 보존), omc는 `7441f3c` — descvi main에 08-31 fast-forward된 그 브랜치의 팁 |
| kein 결함 목록 | `docs/artifacts/260829-kein-p47-execute-claude.md` §3 표와 §4 |
| omc 결함 목록 | `cae2c91`(S47-4) · `f81ac91`(S47-5) · `7441f3c`(S47-6) 커밋 본문 |
| 대조 방법 | `git grep` / `git ls-tree` / `git show <ref>:<path>`. 워크트리는 정리됐으므로 전부 ref에서 읽었다 |
| 런 상태 | `docs/artifacts/ledgers/260829-p47-run-state/` (양쪽, tar, mtime 보존) |

**시각은 커밋 타임스탬프이고 작업 시간이 아니다** — 간격에 밤이 섞인다. kein의 S47-3만 회고가 리포트 mtime으로 실제 런을 11h10으로 재놨다.

## 1. 범위가 다르므로 전체 대 전체는 성립하지 않는다

| | 스토리 | 커밋 | diff |
|---|---|---|---|
| kein | S47-1 · S47-2 · S47-3 | 8 | 37파일 +5,957 / −519 |
| omc | S47-0 ~ S47-6 | 7 | 78파일 +10,315 / −411 |

omc가 페이즈를 끝냈고 kein은 셋에서 멈췄다. 브랜치 전체에 리뷰어를 붙이면 **범위를 재고 품질을 쟀다고 믿게 된다.** 겹치는 구간은 S47-1·2·3뿐이고, S47-3 커밋 규모는 비슷하다 — kein 13파일/2,133줄, omc 17파일/1,610줄.

## 2. 케이던스: 에이전트가 느린 게 아니라 패스가 많다

| | 단위 | 소요 |
|---|---|---|
| omc | **스토리** 하나 | S47-0→1+2 1h24 · **S47-3 1h16** · 3→4 1h18 |
| kein | **라운드** 하나 | R3 1h23 · R4 1h20 · R5 1h19 |

**omc의 스토리 단가와 kein의 라운드 단가가 같은 값이다.** 같은 크기의 일을 kein은 6번, omc는 1번 통과시켰다. S47-3의 12h14 대 1h16은 전부 패스 수다.

회고 §2는 이상치(R6의 2h05)를 설명했고 기준선은 설명하지 않았다. 비용의 몸통은 이상치가 아니라 **그 규칙성**이다.

## 3. 각자의 최악 결함은 자기 설계가 만들었고, 상대엔 그 표면이 없다

**kein이 찾은 것** — `stage.querySelector("#dsh-reorder-layer")`가 트리 순서상 앞선 작성자 프로토타입 페이지를 잡고, 거기 `replaceChildren()`이 걸려 매 스테이지 누름마다 작성자 서브트리를 비웠다. paint-only 계약의 스토리에서, 복구 없이. 라운드 5의 다섯 번째 블라인드 레인이 잡았다.

> omc 트리에 `#dsh-reorder-layer`가 **한 번도 안 나온다.** 헤드리스 모델(`reorder-model.ts`, `reorder-drag-machine.ts`)로 가서 전용 DOM 호스트를 안 만들었다. 고쳐서가 아니라 그 구조를 안 골라서다.

**omc가 찾은 것** — S47-3이 `#dsh-stage`에 press 시점 `setPointerCapture`를 걸었고, Chromium이 합성 클릭을 캡처 요소로 리타게팅해 shield의 컨테이너 스코프 클릭 해석이 null을 답했다. **모든 평범한 캔버스 클릭이 선택을 만드는 대신 해제했다.** S47-5에서 실험적으로 핀했다.

> kein 트리의 `setPointerCapture(` 호출은 `use-resize-drag.ts:405`와 `use-spacing-drag.ts:471` 둘뿐이고 **둘 다 phase-42/43 기존 코드**다. 리오더 경로는 캡처를 아예 안 잡는다.

**대칭이다.** "kein이 사고를 쳤다"는 읽기는 여기서 죽는다. 차이는 탐지가 아니라 **지연**이다 — kein은 결함이 태어난 스토리 안에서 잡았고, omc는 두 스토리 뒤에 잡았다. 그 사이 S47-3과 S47-4가 커밋됐고, `f81ac91`이 상태를 적는다: *"~52 e2e rows were failing on while every unit gate stayed green."*

## 4. 결함 계열은 양쪽이 같다 — 하네스가 아니라 코드베이스의 성질

| 계열 | kein | omc |
|---|---|---|
| 다른 이유로 통과하는 게이트 | 4 | 2 |
| 리드 룰링이 소스/측정에 뒤집힘 | 5라운드 5/5 | *"THE LEAD'S REPAIR RULING WAS REVERSED BY MEASUREMENT, twice over"* (S47-6) |
| 늦게 발견된 선택 상태 결함 | 라운드 5의 파괴적 드레인 | S47-6 랜딩 감사, *"NOT ON ANY LIST"* |

omc의 게이트 둘: **G47-6**은 밴드가 `[a.bottom, b.top]` 안에 있다고 단언했는데, 오답 변이가 한쪽 4px 오프셋으로 떨어져도 수치가 여전히 구간 안이라 초록으로 남았다. **G47-7b**는 코드가 아니라 **러너를 쟀다**.

세 계열이 양쪽에 독립적으로 나타났다는 것이 이 관측의 강한 부분이다. **같은 코드베이스와 같은 과제가 만드는 것이지 하네스가 만드는 것이 아니다.**

## 5. 공유 조건 셋을 확인했고, 한 칸만 비대칭이다

세 조건 모두 양쪽 브랜치에 동일하게 존재한다:

- `src/app/globals.css:131` — `@layer base { * { @apply border-border outline-ring/50; } }`
- jsdom이 둘로 갈린다 — `packages/descvi`가 `^25.0.0`, 루트가 `^29.1.1`
- ring layer 자식들의 `pointerEvents`

**jsdom 분기가 유일하게 한쪽이 명확히 나은 칸이다.** omc의 G47-7b가 거기 빠졌다 — `cssText`를 통째로 비교해 descvi 러너에선 통과하고 루트 러너에선 같은 코드로 실패했고, S47-4에서 속성별 비교로 고쳤다. kein은 **플랜에서 미리 쟀다**: `round-8-plan.md` §(c)가 두 버전을 적고 프로브가 `packages/descvi` 자체 해석으로 jsdom을 로드하게 했다. kein의 `cssText` 사용은 두 파일뿐이고 둘 다 phase-47 이전이다.

단서를 같이 적는다: **kein은 jsdom 게이트를 적게 썼으므로 노출도 적었다.** 예견의 공과 노출의 차이를 이 관측은 못 가른다.

## 6. 게이트가 어느 층에 사는가 — 이게 나머지를 설명한다

| | e2e | vitest |
|---|---|---|
| kein | `reorder-gesture.spec.ts` | 3 |
| omc | `reorder-drag.spec.ts` | **6** (`reorder-model`, `reorder-drag-machine`, `reorder-paint-geometry`, `reorder-refusal-messages`, `reorder-drag-wiring`, `reorder-paint`) |

**omc는 헤드리스로 게이트 가능한 구조를 골랐다.** 순수 모델과 상태 기계라 유닛 여섯이 로직을 덮고 `pnpm gates`가 실제로 본다.

**kein은 산출물이 DOM 페인트인 구조를 골랐고, 그것을 자기 소스에 적었다** (`use-reorder-affordances.ts:44`, correction round 5):

> ⚠ **NO UNIT TEST COVERS THIS FILE, AND THAT IS STATED HERE RATHER THAN LEFT TO BE DISCOVERED.** … a `pnpm gates` run on its own sees none of it.

`pnpm gates`는 양쪽 브랜치에서 바이트 동일(`node scripts/gates.mjs`)이다. **도구 차이가 아니라 무엇을 어디서 게이트할지의 선택이다.**

그래서 같은 함정 — 유닛 게이트는 브라우저 동작에 눈이 멀다 — 이 정반대 결과를 냈다. kein은 브라우저를 몰아 **브라우저에서 변이시켜야만 보이는 게이트 결함 넷**을 찾았고 값은 라운드였다. omc는 13/13 초록을 유지하며 빨랐고, 값은 두 커밋짜리 회귀였다. `f81ac91`이 이유를 적는다 — vitest 스위트 다섯이 `setPointerCapture`를 스텁으로 지우고, jsdom은 포인터 캡처도 클릭 리타게팅도 구현하지 않으며, **e2e는 설계상 `pnpm gates` 밖이다.** 그 커밋에서 리드가 *"pnpm test:e2e now runs for every remaining phase-47 commit"*을 룰링했다.

## 7. 무엇을 말할 수 있고 무엇을 못 하나

**말할 수 있는 것.** 품질 프리미엄은 있고 **라운드 수가 아니라 게이트 층에서 나온다.** 그리고 각 하네스의 최악 결함은 자기 설계가 만들었으며, 상대 트리에는 그 표면이 없다.

**말할 수 없는 것.** 어느 쪽이 나은지. 브라우저 게이트의 값은 중간 커밋이 소비되는지에 달렸고, 이 프로젝트에서 그 답은 관측되지 않았다.

**이 비교의 가장 큰 편향**은 성숙도다. 이것은 `execute`의 **첫 실전 런**이었다 — 입력 동일성 충돌로 런 셋이 폐기됐고, 브리프가 런 도중 강화됐고, 리드가 하네스를 배우며 돌렸다. 회고의 개선 일곱 개는 전부 **다음 런에서 처음 적용된다.** 첫 런과 성숙한 런을 비교하면 성숙도를 재는 것이다.

n은 런 하나가 아니라 결함 여덟이다. 그래도 페이즈 하나·과제 하나이므로 **이것은 발견이 아니라 다음 페이즈가 반증할 수 있는 가설이다.**
