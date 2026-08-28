# phase-47 v1 초안 두 개를 블라인드로 평가했다

phase-47(드래그 재정렬)의 라운드 1 초안을 kein `ralplan`과 omc `2plan`이 각각 냈고, 그 둘을 서브에이전트에 붙여 비교했다. 2026-08-28에 돌렸다.

원래 목적은 대체 표본이었다. phase-46 원장이 삭제되면서 `4·5b`(감사 장치 173줄)를 물어볼 데가 없어졌고, 완성 초안 두 개는 `docs/artifacts/`에 남아 있었다. **그 사이 phase-47 원장이 보존되면서 원본이 생겼으므로, 이 문서는 대체가 아니라 별개 축의 관측으로 남는다.**

## 0. 방법

| | |
|---|---|
| 표본 | `docs/artifacts/260827-kein-p47-ralplan-v1.md` (445줄), `260827-omc-p47-ralplan-v1.md` (380줄) |
| 레인 | 6 — 기준 3개 × A/B 배치 2벌 |
| 에이전트 | `general-purpose`. `kein:critic`을 안 쓴 이유는 그 프롬프트의 자체 우선순위가 여기 세운 기준과 경쟁하기 때문 |

**독자를 먼저 고정했다** — *"계획에 참여하지 않았고, 문서를 처음 열고, 페이즈를 출하해야 하는 구현자."* `plan-gate.md`가 스스로 적은 목표이고, 이걸 고정하지 않으면 "완결성"이 높은 점수를 받으면서 §1이 잡은 팽창을 정확히 보상하게 된다.

기준 셋:

- **Executable without invention** — 구현자가 문서가 안 내린 물질적 결정(architecture / scope / acceptance semantics / safety)을 몇 번 발명해야 하나. `plan`의 실행가능성 게이트가 쓰는 정의 그대로.
- **Verification that can fail** — 각 게이트가 무엇이 RED로 만드는지를 이름 대나. do-nothing 빌드에서 green인 게이트를 겨냥.
- **Surplus for the builder** — 심판을 향한 내용이 몇 %인가. §1의 재측정.

편향 통제: `-in-kein` 식별자 제거, 파일명 `draft-A`/`draft-B`, **배치를 뒤집은 두 벌**(`pairA`는 A=kein, `pairB`는 A=omc). 같은 기준의 두 레인이 서로 다른 라벨을 이기면 그건 위치 편향이지 품질 신호가 아니다. 레포 접근은 막았다 — 워크트리 이름이 `-in-kein`/`-in-omc`라 읽는 순간 블라인드가 깨진다.

## 1. 결과 — 한쪽이 낫다는 결론은 안 나온다

| 기준 | `pairA` | `pairB` | 판정 |
|---|---|---|---|
| Executable without invention | kein 4 / omc 3 | kein 4 / omc 3 | **kein** — 복제, 편향 0 |
| Surplus for the builder | omc lean (17% vs 14%) | omc lean (25% vs 22%) | **omc** — 복제, 격차 3pp |
| Gates that can fail | 5 = 5, kein쪽 (low) | 4 = 4, 차이 없음 (medium) | **무승부** |

### kein의 승리가 제일 단단하다

두 레인이 같은 점수(4 vs 3)를, 반대 배치에서, 독립적으로 냈다. 그리고 **같은 두 줄**을 결정적 결함으로 지목했다 — omc가 자기 산출물 둘을 구현자가 얻을 수 없는 룰링에 되돌려준 지점:

```
L35   (a) recommended, (b) recorded — routed to the lead/owner (§8)
L328  Needs: a lead ruling … Blocking: S47-2's shape.
```

전자는 드래그 리드아웃의 내용 자체가 미결이라 그 스토리를 못 짓고, 후자는 와이어 계약과 기능 상한이 미결이다. 한 레인의 표현: *"the phase's central write design and one named deliverable both stall at the desk."*

**kein의 최악 결함은 한 레인만 찾았다** — 포인터→슬롯 매핑이 정의되지 않음(주력 제스처의 핵심), 그리고 `flex-row-reverse`가 단조 감소라 `no-flow-axis`로 오분류되어 **이미 flex인 부모에게 "flex를 먼저 적용하라"** 는 문구가 나가는 것. 후자는 그 문서 자신이 금지한 실패 양식이다.

### omc의 승리는 작고, 한 레인이 스스로 오차범위 안이라고 했다

절대 추정치는 레인마다 크게 달랐고(14% vs 22%) 차이는 두 번 다 3pp였다. 그리고 두 잉여 레인이 **둘 다** 이렇게 적었다:

> Some of B's extra length is bought scope, not surplus.

**445 대 380줄의 상당 부분이 팽창이 아니라 구현 범위다.** 범위는 셋 갈린다 — 와이어(kein `steps: N` / omc `expectDestination`), 라이더(kein이 KI-47·KI-54를 IN, omc는 미라우팅·제외), non-flex 부모(kein은 block flow 허용, omc는 전부 거부). 레인들에게 점수에 넣지 말라고 했지만 줄 수에는 들어간다.

## 2. §1이 재현됐다 — 그런데 kein 병이 아니다

두 잉여 레인이 독립적으로 **양쪽 문서의 ADR을 최대 잉여로** 꼽았다. kein 13~15줄, omc 25~27줄. `Alternatives considered`가 **§0에서 losers를 builder-facing으로 만들었던 근거를 벗겨낸 채** 호명만 한다.

**§1은 이걸 kein 아티팩트의 문제로 적었다. 이 표본은 플랜 형식 자체의 문제라고 말한다.** 정정으로 기록한다.

kein 고유 잉여는 따로 있고, 양쪽 레인이 같은 것을 꼽았다:

- **§6 Pre-mortem** 37~39줄 — 모든 `Caught by`가 §5의 이미 명세된 게이트를, 모든 `Prevented by`가 §3의 이미 진술된 룰링을 가리킨다. 한 시나리오의 residual은 문자 그대로 `"None."`
- **§8 out-of-scope 표** 18~20줄 — 14행, 표제가 *"because silence is what let three items go missing"*. 대부분이 구현자가 근처도 안 갈 작업. 누락방지 인벤토리 그 자체.

## 3. 새 구분 — 뭉친 잉여 vs 꿴 잉여

> A threads its surplus through the ruling sections as inline asides the builder rereads on every pass … whereas B's surplus is concentrated where a builder can skip it whole.

kein에서 뽑힌 실제 문장: `"this clause exists because a reviewer will ask"`, `"the one a reviewer will cut"`, `"stated rather than skipped"`, `"said here rather than discovered live"`.

**퍼센트가 같아도 비용이 다르다.** 뭉친 잉여는 건너뛸 수 있고 꿴 잉여는 못 건너뛴다. §1은 섹션 단위로 셌는데 이건 문장 단위이고, 이쪽이 더 나은 지표다.

## 4. 세는 계기는 못 믿는다 — 규격화 A/B에 직접 물린다

같은 문서에 대한 두 게이트 레인의 집계:

| | 레인 1 | 레인 2 |
|---|---|---|
| kein | 15/19 | 18/21 |
| omc | 16/20 | 14/21 |

한 레인은 두 문서를 동률로, 다른 레인은 kein 우세로 셌다. 차이는 스토리 레벨의 `Verification: unit, jsdom-free.` 같은 줄을 분모에 넣느냐뿐이다.

**"RED-when 있는 게이트 수를 센다"는 그레이더는 노이즈다.** 이 실험에서 실제로 분별한 것은 전부 질적 판독이었고, 남은 작업의 규격화 A/B 메모가 *"llm 그레이더로 판정하고, vocabulary 그레이더는 조작 검사로"* 라고 적어둔 것이 여기서 지지를 받는다.

## 5. 서로에게서 가져올 것

**kein이 갖고 omc가 못 가진 것 — 계기 검증(positive control).** 게이트가 0을 보고하기 전에 1을 낼 수 있는지 먼저 확인한다.

> plant a sniff, see the enumeration name it, remove it (the instrument is shown able to produce a non-zero result before its zero is believed)

> the instrument is validated by confirming the `steps` = 32 timing is not equal to the `steps` = 1 timing … a harness that cannot see 32× work is not measuring the loop

**"게이트가 실패할 수 있나"보다 한 층 위다 — "게이트가 성공을 볼 수 있나".** §5의 라벨 검증기 사건(여섯 필드를 읽는다는 검사가 다섯 개와 줄바꿈 하나를 읽고 있던 것)이 정확히 이게 없어서 생긴 결함이다.

**omc가 갖고 kein이 못 가진 것 둘.**

설계 결정을 반증하는 게이트:

> Replace `expectDestination` with a `steps: number` → the stale-chain row lands the element in the wrong position and returns 200. **This gate is the entire argument for (d) over (b), made executable.**

코드가 아니라 기각된 대안을 RED로 만든다. kein의 DR 테이블은 같은 논증을 산문으로만 갖고 있어서, 리비전 때 누가 뒤집으면 아무것도 안 걸린다.

그리고 상설 의무 한 줄 — *"every one of these is shown RED under its named mutation **before** it is believed green"*. 게이트가 아니라 규칙이고, kein엔 대응물이 없다.

**kein의 누락:** arming 술어와 거부 문구에 게이트 행이 없다. 후자는 그 문서가 내세우는 주장인데 위반돼도 RED가 되는 검사가 없다. 한 레인이 `unfalsifiable-by-omission`으로 분류했다.

## 6. 반전 서술이 리뷰 라운드 이전에 이미 있다

kein이 자기 킥오프 브리프에 대한 반박을 **네 번** 돌린다. 이건 v1, 리뷰 라운드 0회다.

§2의 표는 라운드 1이 깨끗했다고 기록했다. 대상이 리뷰 findings가 아니라 킥오프 브리프일 뿐 **모양은 같다 — 앞선 문서가 틀린 것을 독자에게 알리기.** §2가 "루프가 만든다"고 본 것의 씨앗이 더 이른 데 있을 가능성이 열린다. phase-47 원장의 라운드별 스냅샷이 이걸 직접 답할 수 있다.

## 7. 얼마나 믿을지

**믿을 만한 것:** executable 차원의 복제(같은 점수 2/2, 같은 결함 줄 지목), 잉여 방향의 복제(3pp 2/2), 게이트 무승부.

**믿으면 안 되는 것:**

- **표본 1쌍.** 방향이지 결론이 아니다.
- **kein 쪽은 이 세션의 15커밋이 안 들어간 버전이다.** 특히 `## Quick Reference`/`## Common Mistakes` 삭제와 `Required Files` 재편 이전.
- **범위가 셋 갈린다.** 점수에는 안 넣게 했지만 줄 수에는 들어간다.
- **레포 대조를 안 했다.** "인용된 사실이 참인가"는 안 물었다. 블라인드를 지키려고 포기한 것이고 이게 제일 큰 구멍이다 — §2가 기록한 phase-21 실패("아티팩트에 대해 검증하고 러닝 앱에 대해 안 한 사실 둘")가 정확히 이 축이다.
