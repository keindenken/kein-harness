# Anti-Autoresearch — 리뷰어를 판사에서 증거 추출자로 강등시키는 설계

Date: 2026-08-29

`research` 스킬의 첫 런. 이 문서는 답이자 그 스킬의 첫 실행 기록이다.

## 질문

`docs/project/research-skill/notes.md`가 다음으로 지목한 것: `wanshuiyin/Anti-Autoresearch`가 가장 가까운 선행 사례이고, 그 구조와 그들이 겪어서 알게 된 것 중 우리 설계에 걸리는 것이 무엇인가.

## 답

### 핵심 장치는 하나다 — 제안과 판정의 분리

리뷰어가 findings를 **제안**하고, 판정은 **규칙만으로 코드가** 낸다. 워크플로 문서가 그것을 자기 말로 적는다:

> **Auditors propose; the adjudicator decides.** No auditor (and not this orchestrator) ever computes `overall_verdict`; only `tools/adjudicate_findings.py` does, by fixed rules.
> (감사자는 제안하고 판정자가 결정한다. 어떤 감사자도, 이 오케스트레이터도 `overall_verdict`를 계산하지 않는다.)

> **Reviewer ≠ adjudicator.** The reviewer *proposes* findings; only `tools/adjudicate_findings.py` *decides* the verdict. **The model is demoted from judge to evidence-extractor.**
> (모델은 판사에서 증거 추출자로 강등된다.)

**근거 형태: 검증 가능한 메커니즘.** 명세만이 아니라 구현을 확인했다 — `tools/adjudicate_findings.py`는 893줄 순수 표준 라이브러리이고, 판정 규칙이 파일 상단 주석에 그대로 있다:

```
any critical                 -> HARD_FLAGS
else any major/minor         -> SOFT_FLAGS
else                         -> CLEAN_GIVEN_EVIDENCE   (NOT "the paper is honest")
```

재확인 프로브: `gh api repos/wanshuiyin/Anti-Autoresearch/contents/tools/adjudicate_findings.py --jq .content | base64 -d`

### 우리에게 없는 것 셋

**1. 커버리지 게이트 — 깨끗함과 안 돌았음을 구분한다.**

`adjudicate.py:542`가 `CLEAN_GIVEN_EVIDENCE`를 조건부로 `REVIEW_UNAVAILABLE`로 바꾼다. 배지 텍스트가 그 의미를 못박는다:

> `REVIEW_UNAVAILABLE (incomplete sweep — not an acquittal)`
> (불완전한 스윕 — 무죄 방면이 아니다)

워크플로 문서의 대응 규칙:

> a dead reviewer must never become a fabricated finding, and an empty file must never masquerade as a completed review
> (죽은 리뷰어가 조작된 finding이 돼서는 안 되고, 빈 파일이 완료된 리뷰인 척해서는 안 된다)

**우리 정지 규칙에 이 구분이 없다.** "감사가 맹점을 지목하지 않으면 라운드가 안 열린다"는 감사가 *맹점이 없다고 판단한 경우*와 *감사가 못 돌았거나 실패한 경우*를 같게 읽는다. 후자는 종료가 아니라 미완이다.

**2. 관측 가능성 등급이 주장의 강도를 상한한다.**

L0(PDF만) / L1(소스) / L2(리포+결과). 감사자는 finding마다 `observability_level_required`를 신고하고, 런의 등급을 넘으면 판정자가 **강등한다** — 구현에서 `observability-exceeds-run(req=L2>run=L1)`으로 사유가 붙는다(`adjudicate.py:409`).

> **Observability caps everything.** L0 / L1 **cannot** assert code/result-level fraud.

이것이 우리가 이번 세션에 만든 **맹점 대 도달 실패** 구분과 같은 문제인데, 우리는 산문으로 감사자에게 정직하라고 요구하고 저쪽은 **기계가 강등한다.** 우리 쪽은 감사자가 규칙을 안 지키면 아무 일도 안 일어난다.

**3. 앵커 규칙 — 모든 finding이 원장의 축자 스팬을 달아야 한다.**

`span in claim`이지 `claim in span`이 아니라고 방향까지 못박혀 있다. 이것은 우리 코퍼스 프로그램이 독립적으로 도달한 규율과 같다 — `verify.py`가 인용을 원문에서 찾고, `norm`이 네 번 틀렸던 것이 전부 정규화 구멍이었지 조작이 아니었다는 그 기록(`references/corpora/260818-github-skills/README.md`).

**수렴 신호로 읽을 만하다** *(의견)*. 서로 모르는 두 프로젝트가 "모델의 출력은 원문에 위치가 확인되기 전까지 기록하지 않는다"에 도달했다.

### 겪어서 알게 된 것 — 우리 런에 바로 걸리는 둘

**직렬로 돌려라, 병렬은 매달린다.**

> Keep the calls **serial** — concurrent codex threads can hang; fan-out buys *breadth of dimensions*, not parallelism.
> (호출은 직렬로 유지하라 — 동시에 도는 codex 스레드는 멈출 수 있다. 팬아웃은 차원의 폭을 사는 것이지 병렬성을 사는 것이 아니다.)

우리 `SKILL.md`는 레인을 병렬로 돌라고 적는다. 네이티브 서브에이전트에는 해당 없지만, **감사를 `ocs ask codex`로 보낼 때는 걸린다.**

**새 스레드, 절대 이어받기 금지.**

> **Fresh thread per dimension, serial.** … **never** `codex-reply` carrying one dimension's conclusions into another (the bias guard). On a stall, re-invoke the *identical* prompt in a fresh thread.

코퍼스가 그 계열에서 뽑은 검증된 인용이 그 이유를 수치로 준다:

> 동일한 논문에 대해 연속 답장과 "지난 라운드 이후 우리는 X를 했다" 같은 프롬프트로 실행하면 점수가 실제 3/10에서 가짜 8/10으로 여러 라운드에 걸쳐 부풀려졌다. 새 스레드로 전환하자 진짜 3/10 평가가 회복되었다.

**근거 형태: 소스 포인터.** `references/corpora/260818-github-skills/runs/facet.jsonl`, 키 `wanshuiyin/Auto-claude-code-research-in-sleep/skills/skills-codex-claude-review/auto-paper-improvement-loop`.

## 분해와 배정

**이 분해는 자료를 보기 전에 세운 가정이다.** 세 단위로 나눴다: (Q1) 역할 분리의 구현, (Q2) 우리에게 없거나 충돌하는 장치, (Q3) 겪어서 알게 된 것.

배정: Q1에 규정된 것 + 일어난 것, Q2에 일어난 것, Q3에 일어난 것 + 말해진 것.

## 라운드

### 라운드 1

- **물은 것** — Q1·Q2·Q3 전부
- **레인** — 규정된 것(`workflows/anti-autoresearch/SKILL.md` 70,765바이트를 blob SHA로 되받아 구조 절만 판독) · 일어난 것(코퍼스 `facet.jsonl`의 `wanshuiyin/*` 21행, 전부 검증된 인용 보유) · 말해진 것(`WebSearch`)
- **돌아온 것** — 위 답의 전부. 말해진 것 레인은 **독립적인 목소리를 하나도 주지 않았다** — 저자의 README 프레이밍과 그 미러 사이트, 그리고 자매 리포뿐이다.
- **감사** — 두 개를 지목했고 둘 다 라운드를 열었다:
  - **소스 맹점:** 읽은 것이 스크립트가 아니라 **스크립트의 명세**다. "규정된 것"의 구조적 맹점이 정확히 "실제로 무슨 일이 일어나는지"인데 안 메워졌다. → 메울 레인: 일어난 것
  - **분해 맹점:** 세 질문이 전부 *그들의* 설계를 묻는다. **어느 것도** 그 설계의 전제가 우리 문제에 성립하는지 묻지 않는다 — 저쪽은 고정된 아티팩트(논문)를 원장에 대조하고, 우리는 열린 소스에서 문서를 만든다. → 메울 레인: 규정된 것/일어난 것을 다른 질문으로 재개

### 라운드 2

- **물은 것** — 명세가 말하는 것을 구현이 실제로 하는가
- **레인** — 일어난 것 (`gh api`로 트리와 `tools/adjudicate_findings.py` 직접 판독)
- **돌아온 것** — 세 장치 전부 명세와 구현이 일치. 판정 규칙, `REVIEW_UNAVAILABLE` 전환(`:542`), 관측 강등(`:409`), 앵커 검사(`_anchored`).
- **감사** — 소스 맹점 없음. 분해 맹점은 **남았다**(아래 미해결).

## 한계

- **모집단.** 전수가 아니다. 규정된 것 레인은 그 리포 65파일 중 2개를 읽었고, 일어난 것 레인은 판정기 1개를 읽었다. 말해진 것 레인은 랭킹된 상위 결과 8건이다.
- **코퍼스는 이 리포에 대해 "일어난 것" 소스가 아니었다.** `provenance.tsv`가 이 리포에서 받은 것은 **65파일 중 12개, 전부 `SKILL.md`**다. 46KB 판정기와 35KB 판정기 테스트가 통째로 없다. 코퍼스가 담은 것은 행위가 아니라 **행위의 명세**다.
- **남은 맹점.** 분해 맹점이 미해결로 남았다 — 아래.
- **도달 실패.** 없음. `gh`가 인증돼 있어 blob SHA와 경로 양쪽으로 원문이 열렸다. 웹 검색은 로그인 벽에 막힌 것이 아니라 **독립적인 논의가 존재하지 않아서** 비었다. 이 둘은 다른 결과이고, 후자는 도달 실패가 아니다.

## 미해결

- **저쪽 전제가 우리 문제에 성립하는가.** 저쪽은 고정된 아티팩트를 스팬 고정 원장에 대조한다 — 판정할 대상이 이미 존재하고 유한하다. 우리는 열린 소스에서 문서를 *만든다*. 원장에 해당하는 것이 우리에게 무엇인지, 애초에 있는지가 안 물어졌다.
- **커버리지 게이트를 우리 정지 규칙에 넣을지.** 넣으면 "감사가 못 돌았다"가 종료로 읽히는 구멍이 닫힌다. 안 넣으면 첫 실전 런에서 그 구멍으로 조용히 끝날 수 있다.
- **관측 등급의 우리 판(版).** 우리는 산문으로 감사자에게 맹점과 도달 실패를 구분하라고 요구한다. 저쪽은 기계가 강등한다. 우리 쪽에 강등할 기계가 있을 수 있는지는 안 물어봤다.
