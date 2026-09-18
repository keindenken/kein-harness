# `kein-findings:findings` — 측정 발견을 필요할 때만 읽히는 별도 플러그인으로

Status: Draft — 잠정 실행 가능. 막는 질문은 없다. 이 설계가 기대는 사실 하나("정적 description이 관련 주제에서는 뜨고 무관한 주제에서는 조용하다")는 아직 측정하지 않았고, S3 안의 Gate G1이 이것을 판정한다. G1의 1차·2차 결과마다 갈 길은 S3의 판정표에 정해 두었다. 사용자 선호로 바뀔 수 있는 기본값(이 리포 `docs/skills/`와의 경계, Codex 노출, `kein-findings`의 버전 이동)은 Open Questions에 두고 기본값으로 진행한다.

## 출처와 범위

요구사항 출처는 세 가지다.

- 리서치 아티팩트: `.agents/kein/research/260919-llm-wiki-design.md` (sha256 `87533cacd9ab4baabf8f8a8c5d9ea71ef701ea21031a65ec6e50f802fb029fe2`). 특히 "미해결"의 D3-a/D3-b 사용자 답변을 따른다. 그 답변은 본문 설계 줄 "측정 발견은 그것을 낳은 리포에 둔다"를 뒤집는다. 이 계획은 답변 쪽을 따른다.
- 리서치 뒤 채팅에서 사용자가 동의한 여섯 가지다. 아래에서 R1–R6으로 부른다. 계획 초안 뒤 사용자가 내린 결정(U1–U4)으로 R2, R3, R4, R6이 개정되었고, 개정된 문장을 적는다.
  - R1: 측정 발견(예: `260808-subagent-capabilities-without-agent-teams`)은 리포 `docs/`가 아니라 wiki에 둔다. 에이전트는 필요할 때만 읽는다. 전역 CLAUDE.md에 "wiki를 참고하라"고 적는 방식은 실패했다. 항상 로드되는 메모리보다 필요할 때 읽는 방식을 선호한다. 채팅에서 제안한 메커니즘은 주제가 나오면 `description`으로 로드되는 스킬이다.
  - R2(U2로 개정): 사람용 기억 보조는 만들지 않는다. 사용자는 wiki를 직접 읽지 않는다. "언제 무엇을 봤고 어떤 느낌이었나"라는 발상은 남의 wiki-ingest를 보다가 나온 것이다. 사용자는 즉흥적인 주관 의견이 에이전트 컨텍스트에 들어가지 않게 하려 한다.
  - R3(U2로 개정): 외부 지식을 컴파일하는 wiki는 만들지 않는다. 행동을 바꾸는 외부 글은 규칙이나 스킬의 승격 후보가 된다. 그렇지 않은 글은 삭제한다.
  - R4(U2로 개정): `~/Documents/wiki`는 지금 갈 곳 없는 기록을 두는 inbox다. 항목마다 발견, 승격 후보, 삭제 중 하나로 보내는 drain 규칙이 필요하다.
  - R5: 장치 상한은 스킬 하나와 검사 스크립트 하나다(플러그인 manifest는 별도로 센다). 컴파일 층은 두지 않는다. 스킬 자체에 필요한 것 말고는 index도 유지하지 않는다. 옛 wiki는 쓰기의 76%를 자기 장치에 썼다(리서치 (2′)). 이런 장치 증식을 주 위험으로 다룬다.
  - R6(U1로 개정): wiki 스킬은 이 리포의 같은 marketplace에 있는 별도 플러그인 `kein-findings`에 둔다. `~/.claude/skills/wiki-collect`와 `~/.claude/skills/wiki-record`는 은퇴시킨다. `~/.agents/skills/handoff`는 범위 밖이다.
- 사용자 결정 U1–U4(이 개정의 입력):
  - U1: 발견 스킬은 `kein`과 다른 플러그인 `kein-findings`로 나누고 사용자 범위로 켠다. 사용자는 프로젝트마다 `kein`과 oh-my-claudecode 중 하나만 켜므로, `kein` 안의 스킬은 omc 프로젝트에 없다. 에이전트 런타임에 대한 발견은 어느 프로젝트에서나 필요하다. 나누는 기준은 주제가 아니라 "켜는 범위가 다르다"이다. 그래서 다른 스킬(dev, pm 등)은 지금 나누지 않는다.
  - U2: 인간 기억(옛 R2)을 전부 뺀다. `memory/`는 만들지 않는다. 사용자의 `무제*.md`는 제자리에 그대로 둔다.
  - U3: G1의 판정 경로 공백을 메운다. 1차와 2차에서 기대할 수 있는 결과가 모두 정해진 경로나 멈춤 경계로 가야 한다.
  - U4: oh-my-claudecode `wiki-query`에 관한 질문을 뺀다. omc와 kein은 함께 켜지지 않는다.

분류: 기능 추가와 이행이다. 같은 marketplace에 플러그인 하나(`kein-findings`: manifest, 스킬 하나, bin 명령 하나)를 더한다. eval 하네스는 arm에 넣을 플러그인을 케이스가 고르도록 조금 고치고, 케이스를 넷 더한다. 리포 밖의 개인 기록도 이행한다.

비목표:

- 컴파일된 주제 페이지, `index.md`, `log.md`, 임베딩이나 검색 계층은 만들지 않는다(R3, R5).
- 외부 글 수집 경로는 만들지 않는다. `wiki-collect`는 은퇴하고 대체하지 않는다(R3, R6).
- 사람이 읽을 기억 보조나 그 디렉터리는 만들지 않는다(R2, U2).
- 다른 kein 스킬을 별도 플러그인으로 나누지 않는다(U1: 기준은 켜는 범위).
- `plugin/`을 옮기거나 `plugins/` 아래로 재배치하지 않는다(결정 1).
- `~/.agents/skills/handoff`와 Codex용 스킬 사본은 범위 밖이다(R6).
- 이 리포 `docs/`, `.agents/`에 남은 옛 `~/Documents/wiki/...` 인용은 고쳐 쓰지 않는다. 그중 상당수(`_rules/`, `harness/`, `context-engineering/`)는 이미 존재하지 않는 경로를 가리키는 역사 기록이다. 이행에서 발견 파일의 이름(basename)은 그대로 두므로 note 인용은 이름으로 다시 찾을 수 있다.
- `~/Documents/wiki_deprecated/`는 보관본이다. 읽어서 복사하기만 하고 바꾸지 않는다.
- 사용자의 `~/Documents/wiki/무제*.md`와 `.obsidian/`은 건드리지 않는다(U2).
- 버전을 올리지 않는다. `kein`의 버전은 `bump-version` 스킬이 따로 올린다. `kein-findings`의 버전 이동은 Open Questions에 둔다.

표기: 아래에서 "확인"은 이 커밋(`f608c8c`, 작업 트리에 무관한 수정 있음)에서 직접 읽거나 돌려 본 사실이다. "추론"은 계획 단계의 추정이다.

## 이 계획이 기대는 사실

- `.claude-plugin/marketplace.json`에는 플러그인이 하나(`kein`, source `./plugin`, version `0.0.2`) 있고, 최상위 `version`도 `0.0.2`다. `plugin/.claude-plugin/plugin.json`도 `0.0.2`다. (확인)
- `dev/libexec/bump-version`은 marketplace.json에서 `"version"` 필드를 `sed -n '1p'`(최상위)와 `sed -n '2p'`(첫 플러그인)로 읽는다. 쓸 때는 `"version": "<현재값>"` 문자열을 파일 전체에서 모두 바꾼다. 그래서 두 번째 플러그인 항목이 `kein` 앞에 오거나, 같은 버전 문자열을 가지면 이 명령이 잘못 읽거나 함께 올린다. (확인)
- `claude plugin validate <dir> --strict`는 plugin.json에 `version`이 없으면 경고를 내고 strict에서 실패한다. marketplace 항목에 `version`이 없는 것은, 그 항목의 plugin.json에 version이 있으면 통과한다. 두 항목을 가진 marketplace도 통과한다(스크래치 디렉터리에서 돌려 봄, Claude Code 2.1.276). (확인)
- `claude --help`(2.1.276): `--plugin-dir`는 반복할 수 있다(`--plugin-dir A --plugin-dir B`). (확인)
- 사용자 머신의 설치 방식: `~/.claude/skills/kein -> <repo>/plugin` symlink이고, `kein@skills-dir`로 로드된다. `~/.claude/settings.json`의 `enabledPlugins`에는 `"kein@skills-dir": false`가 있고, 프로젝트가 켠다. 스킬은 `skills/<name>/SKILL.md -> /kein:<name>` 형태로 네임스페이스가 붙는다(README Layout). 그래서 새 스킬 이름은 `kein-findings:findings`일 것이다. (확인, 새 이름은 추론이고 S2가 init inventory로 확인한다)
- 이 머신의 PATH에서 `command -v findings`와 `command -v kein-findings`는 아무것도 내지 않는다. (확인)
- `plugin/bin/ocs`는 `libexec/ocs-<name>`을 dispatch한다. `ocs`는 `kein`의 bin이므로 `kein`이 켜진 프로젝트에서만 PATH에 있다. `ocs-validate` 등의 주석에 따르면 `CLAUDE_PLUGIN_ROOT`는 Bash 도구 환경에 없다. 그래서 스킬 본문은 파일 경로 대신 PATH의 bin 명령을 부른다. (확인)
- `ocs-state-dir`은 `.agents/`를 프로젝트와 홈 양쪽에서 쓰는 벤더 중립 네임스페이스라고 적는다. 이 머신에는 `~/.agents/skills/`와 `~/.agents/disabled-skills/codex-orca-migration-20260730/`이 있다. 두 번째 것은 은퇴한 스킬을 날짜를 붙인 묶음으로 옮겨 둔 선례다. (확인)
- 플러그인 파이썬은 표준 라이브러리만 쓴다. `plugin/` 안에 `import yaml`이 없다. (확인)
- 모델이 부르지 못하게 할 스킬은 `disable-model-invocation: true`를 쓴다(`handoff`, `onboard`, `ping`). 나머지 kein 스킬은 description만으로 모델이 부를 수 있다. (확인)
- 규칙 링크(`~/.claude/rules/kein -> plugin/rules`)는 `onboard`가 config home에 만든다. eval arm은 config home을 인증 정보만 담아 새로 만든다(`dev/eval/run.py` `prepare_config_home`). 그래서 path-scoped rule은 arm에 닿지 않는다. 사용자의 `~/.claude/skills/` symlink와 `enabledPlugins`도 arm에 닿지 않는다(추론: 같은 이유. S3 G1의 Evidence method가 비교군 arm의 init inventory로 확인한다). (확인/추론)
- eval: 케이스는 `case.yaml`에 `execution.prompt`를 하나만 둔다. 워크트리에는 `fixture/`가 복사되고 git에 커밋된다(`graded.py` `prepare_case_worktree`). arm의 플러그인은 `resolve_arms`가 정한다. 기본 쌍에서 `with-skill`은 `prepare_plugin`이 `KEIN_ROOT`(`plugin/`)를 복사하고 에이전트를 렌더한 디렉터리를 받고, `without-skill`은 받지 않는다. `--variant` 모드에서는 각 arm이 `checkout / "plugin"`을 복사한다. `launch_command`는 `plugin_dir` 하나만 받아 `--plugin-dir`를 한 번 붙인다. arm의 환경은 `dict(os.environ, CLAUDE_CONFIG_DIR=…, KEIN_STATE_ROOT=…)`이다(`run.py` `launch`). 운영자의 환경 변수는 arm으로 새고, arm의 `HOME`은 운영자와 같다. (확인)
- 이벤트 요약의 `skills_invoked`에는 `Skill` 도구 입력의 `skill` 값이 이름 그대로 쌓인다. 반면 `tool_used` grader는 도구 종류로만 세고, `min`만 있고 `max`는 없다(`graded.py` `grade`). 그래서 "특정 스킬이 불렸다"와 "불리지 않았다"는 지금 grader로 표현할 수 없다. (확인)
- `--self-test`는 `selftest/should-pass|should-fail/_record.json`(예: `{"skills_invoked": [], "files_written": [...]}`)으로 결정적 grader를 arm 없이 검증한다. `dev/libexec/check-eval-launch`는 `run.py`를 모듈로 불러 `launch_command`의 명령줄을 세션 없이 단언한다. (확인)
- 이행 대상 원본(확인):
  - `~/Documents/wiki_deprecated/_raw/note/`에 18개 파일이 있다. 그중 `2026-08-06-a-red-gate-in-a-world-that-cannot-happen.md`와 `260806-a-red-gate-in-a-world-that-cannot-happen.md`는 바이트가 같다(`cmp`). 그래서 서로 다른 note는 17개다.
  - `~/Documents/wiki/_raw/note/`에는 `260819-orca-worktree-model.md`, `260912-ocs-team-codex-dispatch-dies-at-zero-seconds.md` 2개가 있다.
  - `~/Documents/wiki/_raw/`에는 외부 글 4개가 있다(`260815-llm-wiki.md`, OpenWiki 2개, `260819-Extend Claude with skills.md`).
  - 루트에는 사람이 쓴 `무제*.md` 4개가 있다. 그 밖에 빈 `_rules/`와 `.agent/`, 옛 장치인 `.claude/`(`commands/`, `skills/`, `settings.local.json`), `.obsidian/`, `.gitignore`가 있다.
  - vault git에는 remote가 없다. 커밋되지 않은 변경도 있다. `_rules/standing-prompt.md` 삭제, 그리고 untracked 외부 글, `260912` note, `무제 1.md`, `.claude/`, `.gitignore`, `.obsidian/`이다.
  - 모든 note는 옛 frontmatter(`source`, `source_type`, `date`, `captured`, `type`, `status: ingested|uningested`)를 쓴다.
- 옛 스킬: `wiki-record`는 `~/Documents/wiki/_raw/note/`에 쓰고 vault에 커밋한다. `wiki-collect`는 `_raw/<type>/`에 쓰고 `scripts/`와 `evals/`를 갖는다. 둘 다 git 밖의 `~/.claude/skills/`에 있다. `~/.agents/skills/`에는 wiki 스킬이 없다. (확인)
- 근거 계약(`plugin/rules/standing-prompt.md` 23행): 사실 주장은 자기 확인 수단을 달아야 한다. 받아들이는 형태 중 하나는 "a fact pinned to a version with the probe that re-checks it"(버전에 고정한 사실과 그것을 다시 확인하는 프로브)이다. (확인)
- `docs/open-threads.md`는 스킬에 묶이지 않는 보류 건을 두는 곳이다(AGENTS.md). (확인)

## 결정 1 — 배포 단위와 그 기계 장치

배포 단위 자체는 사용자가 정했다(U1). 별도 플러그인 `kein-findings`를 같은 marketplace에 두고 사용자 범위로 켠다. 여기서는 U1이 남긴 기계적 선택만 정한다.

- **소스 디렉터리: `plugin-findings/`(리포 루트, `plugin/`의 형제).** 대안은 `plugins/kein/`과 `plugins/kein-findings/`로 재배치하는 것이다. 이 대안은 기각한다. 사용자의 `~/.claude/skills/kein` symlink, `dev/kein-dev`의 `KEIN_ROOT`, eval `--variant`가 옛 커밋에서 복사하는 `checkout / "plugin"`, README가 모두 `plugin/` 경로에 묶여 있어서다. 이름 없는 `kein-findings/`도 기각한다. 루트의 `agents/`, `docs/`와 섞이면 배포되는 트리인지 드러나지 않는다. `plugin-` 접두어를 쓰면 목록에서 `plugin/` 옆에 오고 배포 트리라는 것이 보인다.
- **bin 명령: `plugin-findings/bin/findings` 하나(`where|list|check`).** `ocs`는 `kein`이 꺼진 곳에서 PATH에 없으므로 쓸 수 없다. 이 파일 하나가 R5의 "검사 스크립트 하나"다. libexec dispatch는 두지 않는다. `findings`는 지금 PATH에서 비어 있다(위 사실). 충돌 위험은 Pre-mortem S10에서 다룬다.
- **버전: `plugin-findings/.claude-plugin/plugin.json`에는 `version: 0.1.0`, marketplace 항목에는 `version`을 두지 않는다. 항목은 `kein` 뒤에 붙인다.** strict 검사는 plugin.json의 version을 요구하고 marketplace 항목의 version은 요구하지 않는다(위 사실). 항목에 version이 없으면 `bump-version`의 `sed -n '2p'` 읽기와 전체 치환이 `kein`에만 걸린다. `kein`과 다른 시작값을 쓰는 것은 두 plugin.json을 사람이 헷갈리지 않게 하려는 것이다. 이후 버전을 어떻게 옮길지는 Open Questions에 둔다.
- **켜는 방식: `~/.claude/skills/kein-findings -> <repo>/plugin-findings` symlink와, `~/.claude/settings.json`의 `"kein-findings@skills-dir": true`.** `kein`과 같은 skills-dir 방식이다. 사용자 범위에서 명시적으로 켠다. 켜는 일은 G1이 문안을 정한 뒤 S5에서 한다.
- **리포 규칙:** AGENTS.md의 "`plugin/`만 설치된다" 줄은 사실이 아니게 되므로 고친다. "`plugin-findings/bin/`에는 `findings` 하나만", "`plugin-findings/`는 `ocs`를 부르지 않는다" 같은 새 규칙 문장은 쓰지 않는다. 이 둘은 `dev/libexec/check-findings`가 검사로 붙잡는다(메모리 [[delete-rules-rather-than-reword]]). 그래도 문장이 필요한지는 `/kein:deliberate`가 판단할 일이다.

## 결정 2 — 개인 발견이 플러그인 밖에 있을 때 on-demand 트리거를 어떻게 걸까

긴장: 플러그인은 설치한 모든 사람에게 같은 파일로 배포되고 SKILL.md는 정적이다. 그런데 R1의 메커니즘은 "발견이 다루는 주제를 description이 이름으로 부른다"를 전제한다.

결정 요인(우선순위 순):

1. 트리거가 사람의 지시 문장이 아니라 로딩 메커니즘에 걸려야 한다. 산문 포인터는 이미 실패했다(R1).
2. 장치 상한(R5). 생성 단계, index, 두 번째 스킬은 모두 증식이다.
3. 개인 내용이 배포되는 플러그인 트리에 들어가지 않아야 한다. 스킬은 `kein`이 꺼진 프로젝트에서도 로드되는 `kein-findings` 안에 있어야 한다(R6, U1).

| 안 | 이득 | 비용 | 판정 |
| :-- | :-- | :-- | :-- |
| **A. 상황으로 쓴 정적 description과 목록 명령.** `plugin-findings/skills/findings/SKILL.md`의 description은 주제 목록이 아니라 상황("에이전트 런타임이 어떻게 동작하는지에 대한 믿음 위에서 답하거나 설계하려 할 때")을 적는다. 불리면 본문이 `findings list`로 claim 한 줄씩을 보고 맞는 파일만 읽는다. | 파일 둘(스킬과 bin)이면 끝난다(R5). 개인 내용은 런타임에 플러그인 밖에서 읽는다. 발견이 늘어도 description은 그대로다. | 개별 주제를 이름으로 부르지 못하므로 발화율이 낮을 수 있다. 영역 안의 무관한 질문에서도 뜬다. 다만 그때 드는 비용은 `list` 한 번이다. | **채택.** 발화율은 Gate G1이 판정한다. |
| B. 사용자별 스킬 디렉터리를 생성한다. `findings sync`가 `~/.claude/skills/findings-index/SKILL.md`에 발견 제목을 description으로 적는다. | description이 실제 주제를 부른다. 같은 파일을 `~/.agents/skills/`에도 두면 Codex도 읽을 수 있다. | 생성 단계와 두 번째 스킬이 생긴다. 이것은 옛 wiki가 쓰기의 76%를 쓴 index 유지와 같은 종류다. 발견이 늘면 description이 길이 예산에 걸려 잘린다. R6("플러그인 안에")과도 어긋난다. | G1이 멈춤 경계에 닿을 때 사용자에게 넘길 다음 후보다. 지금은 만들지 않는다. |
| C. SessionStart hook이 목록을 주입한다. | 발화율 문제가 없다. | 항상 로드되는 메모리다. R1의 선호에 정면으로 어긋난다. 사용자 범위로 켜므로 모든 프로젝트, 모든 세션에 비용이 든다. | 기각. |
| D. path-scoped rule(`plugin/rules/`에 `paths:`를 단 파일) | 파일을 열면 메커니즘이 로드한다. | 대화에서 나온 질문에는 뜨지 않는다. rule은 eval arm에 닿지 않아(위 사실) 측정할 수 없다. 산문 포인터와 같은 계열이다. 규칙 링크는 `kein`의 `onboard`가 만들므로 omc 프로젝트에는 없다(U1). | 기각. |

**위치와 탐지.** 발견 루트는 런타임에 `KEIN_FINDINGS_DIR`로 정하고, 없으면 `$HOME/.agents/findings`로 정한다. 둘 다 없으면 "발견 없음"으로 조용히 끝난다. 다른 설치자에게는 아무 일도 일어나지 않는다. 이 사용자는 실제 디렉터리를 `~/Documents/wiki/findings/`에 두고 `~/.agents/findings`를 그곳으로 가리키는 symlink를 하나 둔다. `~/Documents/wiki`는 git 저장소로 남기되, 에이전트가 쓰는 내용은 발견만으로 좁힌다. 발견을 저장소 루트에 flat하게 두지 않고 `findings/` 아래에 두는 이유는 하나다. 사용자의 `무제*.md`가 제자리 그대로 루트에 남는데(U2), `check`는 flat 루트에서 규칙에 맞지 않는 파일을 실패로 친다(S1 위반 1–3). 루트를 `findings/`로 한정하면 사용자 파일을 옮기지 않고도 검사를 엄격하게 유지할 수 있다. 저장소 경로를 `~/Documents/wiki`로 유지하는 것은 사용자의 기본 제안이다. git 이력(스냅샷 포함)과 기존 인용의 이름 검색도 그대로 이어진다. 설정 파일이나 toml은 두지 않는다. 옛 설계의 설정 증식(리서치 미해결 답변)을 반복하지 않기 위해서다.

**Codex.** 발견은 frontmatter를 단 평범한 markdown이고 고정 경로 `~/.agents/findings`에 있다. 그래서 어떤 에이전트든 경로만 알면 읽는다. Codex가 스스로 찾게 하는 장치는 이번에 만들지 않는다(Open Questions).

**뒤집을 증거.** init inventory에 스킬이 보이는데 G1이 멈춤 경계에 닿으면 A의 전제("상황 description으로 충분하다")가 무너진 것이다. 멈춤 경계는 1차 혼합 결과에서 direct ≤1/3이거나 quiet ≥4/6일 때, 또는 2차에서 두 문안 모두 부분 통과에 못 미칠 때다(S3 판정표). 그때 결정은 B로 넘어가고, 넘길지는 사용자가 정한다. 반대로 실제 세션에서 무관한 작업마다 `kein-findings:findings`가 뜬다는 관측이 있으면 description의 영역을 좁힌다.

## 발견 파일과 명령의 형태

이 fragment는 결정을 고정한다. 규칙은 주변 산문에 있다.

```text
<root>/YYMMDD-<slug>.md          # flat. 하위 디렉터리 없음. slug는 [a-z0-9-]+
---
claim: <측정 결과 한 문장, 한 줄, 200자 이하>
measured: YYYY-MM-DD             # 파일 이름의 YYMMDD와 같은 날
versions: <도구 버전; 도구 버전> | unrecorded
reproduce: <다시 돌릴 명령, 또는 이 파일 안 절차의 절 이름> | unrecorded
status: current | superseded | disputed
superseded_by: <root 안의 파일 이름>   # status: superseded일 때만, 그때는 필수
project: <발생 리포>              # 선택
---
# <제목 한 줄>
<본문: 무엇을 물었고, 무엇을 돌렸고, 무엇이 나왔나>
```

```text
findings where           # 루트 경로를 stdout에 출력. 루트가 없으면 아무것도 출력하지 않고 exit 3
findings list [--all]    # 한 줄에 발견 하나: <file>\t<measured>\t<status>\t<claim>. 기본은 current와 disputed만
findings check [<file>…] # 위반마다 한 줄 출력 후 exit 1. 깨끗하면 exit 0. unrecorded 개수는 참고로 알리고 실패로 치지 않는다
```

frontmatter는 한 줄짜리 `key: value`만 쓴다. YAML 리스트는 쓰지 않는다. 그래야 표준 라이브러리만으로 읽힌다. 허용 키 집합이 닫혀 있어 `check`가 모르는 키를 실패로 처리한다. 스키마 증식을 문장이 아니라 검사기가 막는다는 뜻이다. 이 방식은 리서치의 "규칙은 산문이 아니라 검사기로 강제한다" 줄과 메모리 [[delete-rules-rather-than-reword]]와 같은 방향이다. `unrecorded`는 이행한 옛 note를 받아들이기 위한 값이다. `list`는 이 값을 그대로 보여 주므로, 읽는 에이전트는 그 주장에 확인 수단이 없음을 안다.

## 실행 순서

S1 → S2 → S3(G1) → S5. S4는 S1이 끝나면 S2·S3과 따로 진행할 수 있다. S5는 G1과 S4를 모두 기다린다.

### S1 — `kein-findings` 플러그인 골격과 `findings` 명령

목적: U1의 배포 단위를 세우고, R5의 "검사 스크립트 하나"를 만든다. 이 명령은 스킬이 경로를 부르지 않고 발견에 닿는 유일한 입구이기도 하다.

위치: `plugin-findings/.claude-plugin/plugin.json`(새 파일), `plugin-findings/bin/findings`(새 파일, 실행 가능), `.claude-plugin/marketplace.json`(`plugins`에 항목 추가), `dev/libexec/check-findings`(새 파일, 배포되지 않는 회귀 검사), `AGENTS.md`(무엇이 배포되는가 절과 명령 블록).

요구 동작:

- manifest: `name: kein-findings`, `version: 0.1.0`, `description`, `author`. 컴포넌트 경로는 적지 않는다. `kein`의 manifest처럼 기본 디렉터리를 자동으로 찾게 한다.
- marketplace: `kein` 항목 뒤에 `{name: kein-findings, description, source: ./plugin-findings, category}`를 붙이고 `version`은 두지 않는다(결정 1). 최상위 `version`과 `kein` 항목은 바꾸지 않는다.
- `findings`는 위 인터페이스를 그대로 구현한다. 루트는 `KEIN_FINDINGS_DIR`, 없으면 `$HOME/.agents/findings` 순으로 정한다. symlink를 따라간다. 파이썬을 쓴다면 표준 라이브러리만 쓴다. `ocs`, `plugin/`, `CLAUDE_PLUGIN_ROOT`에 기대지 않는다. `kein`이 꺼진 프로젝트에서도 혼자 돌아야 하기 때문이다(U1).
- `check`가 실패로 치는 것:
  1. 루트 최상위에 `.md`가 아닌 일반 파일이나 하위 디렉터리가 있다. dot 항목(`.git` 등)은 무시한다.
  2. 파일 이름이 `^\d{6}-[a-z0-9-]+\.md$`와 맞지 않는다.
  3. frontmatter가 없거나 한 줄 `key: value` 형식이 아니다.
  4. 허용 집합 밖의 키가 있거나 필수 키(`claim`, `measured`, `versions`, `reproduce`, `status`)가 빠졌다.
  5. `measured`가 유효한 날짜가 아니거나 파일 이름의 날짜와 다르다.
  6. `claim`이 비었거나 200자를 넘는다.
  7. `status`가 enum 밖이다.
  8. `superseded_by`가 있어야 할 때 없거나, 있으면 안 될 때 있다. 또는 존재하지 않는 파일이나 자기 자신을 가리킨다.
  9. 본문 H1이 정확히 하나가 아니다.
  10. 두 파일의 본문이 바이트 단위로 같다.
- 스크립트 안에 개인 경로(`Documents/wiki`)를 쓰지 않는다. 기본값은 `$HOME/.agents/findings` 하나다.
- `dev/libexec/check-findings`(첫 줄 `#:`은 `kein-dev help` 요약)는 `$KEIN_REPO_ROOT/plugin-findings/bin/findings`를 부른다. 임시 디렉터리에 발견 파일을 합성한다. 그리고 위반 1–10을 하나씩 넣은 경우가 exit 1과 해당 위반 줄을 내는지, 깨끗한 경우가 exit 0인지, 루트가 없을 때 `where`가 exit 3에 빈 stdout인지 확인한다. 선례는 `dev/libexec/check-git-guard`의 합성 입력 방식이다. 여기에 트리 단언 세 가지를 더한다. `plugin-findings/bin/`에 `findings` 말고 다른 항목이 없어야 한다. `plugin-findings/` 아래에서 단어 `ocs`, `Documents/wiki`, `CLAUDE_PLUGIN_ROOT`가 나오지 않아야 한다. marketplace.json의 `"version"` 필드는 정확히 둘(최상위와 `kein`)이어야 한다. 이 단언들이 결정 1의 "규칙 문장 대신 검사"다.
- AGENTS.md: "`plugin/`만 설치된다" 줄을 "`plugin/`(kein)과 `plugin-findings/`(kein-findings)만 설치된다"는 사실로 고친다. 명령 블록에는 `claude plugin validate plugin-findings --strict`와 `dev/kein-dev check-findings`를 더한다. 그 밖의 규칙 문장은 더하지 않는다(결정 1).

수용 기준:

- `dev/kein-dev check-findings`가 exit 0으로 끝나야 한다. 위반 10종 각각이 자기 줄을 내야 하고, 트리 단언 셋이 모두 통과해야 한다.
- `claude plugin validate plugin-findings --strict`, `claude plugin validate . --strict`(marketplace), `claude plugin validate plugin --strict`가 모두 통과해야 한다.
- `KEIN_FINDINGS_DIR=/nonexistent plugin-findings/bin/findings where; echo $?`가 빈 출력과 `3`을 내야 한다.
- `git diff --stat <S1 시작 커밋> -- plugin/`가 비어 있어야 한다. S1은 `kein` 트리를 건드리지 않는다.

실패 시: 위반 하나라도 잡히지 않거나 strict 검사가 실패하면 S2로 넘어가지 않는다. S4의 이행 검증이 이 검사에 기대기 때문이다.

### S2 — `kein-findings:findings` 스킬: 조회와 기록

목적: R1의 on-demand 트리거와 기록 경로다. R5의 "스킬 하나"다.

위치: `plugin-findings/skills/findings/SKILL.md`(새 파일, 참조 파일은 두지 않음).

요구 동작:

- frontmatter에 `name: findings`를 둔다. `disable-model-invocation`은 쓰지 않는다. description은 결정 2 A안의 상황을 적는다. 조회와 기록 두 용도를 모두 부르고, 앞 250자 안에 트리거가 들어가야 한다. G1이 측정할 시작 문안은 다음과 같다. 문구 조정은 G1 판정표의 수정 경로에서만 한다.

  ```text
  Use before answering, deciding, or designing on a belief about how an agent runtime behaves — Claude Code, Codex, Orca, subagents, skills, hooks, sandboxes, headless runs — because it may already have been measured. Also use to record a new measurement.
  ```

- 본문 조회 절차:
  1. `findings list`를 돌린다. 명령이 없거나, exit 3이거나, 출력이 비었으면 발견을 언급하지 않고 원래 작업을 계속한다.
  2. claim 줄로 관련 파일을 고르고, 고른 파일만 읽는다.
  3. 인용할 때는 파일 이름과 `versions`를 함께 적는다.
  4. 지금 환경의 버전이 `versions`와 다르거나 값이 `unrecorded`이면 그 주장을 확인되지 않은 것으로 다룬다. 결론이 그 주장에 걸려 있으면 `reproduce`를 다시 돌릴지 말한다.
  5. 루트 밖(같은 git 저장소의 다른 파일 포함)은 읽지 않는다. 사용자의 `무제*.md`는 에이전트 컨텍스트에 넣지 않으려는 주관 메모이기 때문이다(R2, U2).
- 본문 기록 절차:
  1. 측정이 있었을 때만 쓴다. 선호, 교정, 작업 상태는 여기에 쓰지 않는다. 각각의 자리는 auto memory와 작업 리포의 상태 디렉터리다(리서치 (2)의 무효화 축).
  2. `$(findings where)/YYMMDD-<slug>.md`에 위 스키마로 쓴다. 루트가 없으면 만들지 말고 사용자에게 알린다.
  3. 새 발견이 옛 발견을 뒤집으면 옛 파일의 `status`를 `superseded`로 바꾸고 `superseded_by`를 단다. 옛 파일은 지우지 않는다.
  4. `findings check`를 통과시킨다.
  5. 루트가 git 작업 트리 안이면 거기서 커밋한다. 옛 `wiki-record`가 하던 대로다.
  6. 보고는 경로와, 재구성한 부분이 어디인지로 한다. 파일 내용을 다시 출력하지 않는다.
- 본문은 개인 경로와 `ocs`를 부르지 않고 `findings`만 부른다.
- 쓰는 규칙은 `plugin/rules/standing-prompt.md`를 따른다. 새 규칙 문장은 `/kein:deliberate`의 판정을 거친다. 이것은 리포 AGENTS.md가 요구하는 일이다.

수용 기준:

- `claude plugin validate plugin-findings --strict`가 통과해야 한다. `dev/kein-dev check-findings`도 여전히 통과해야 한다(트리 단언이 SKILL.md까지 본다).
- description 길이가 250자 이하여야 한다. 확인은 frontmatter를 추출해 문자 수를 세는 한 줄 명령으로 한다.
- 새 헤드리스 세션의 init inventory에 이 스킬이 보여야 한다. 확인은 S3의 첫 케이스를 `--arm with-skill --runs 1`로 한 번 돌린 이벤트 스트림의 `system/init.skills`로 한다. 거기 찍힌 정확한 이름(기대값 `kein-findings:findings`)을 S3 grader의 `skill:` 값으로 쓴다. 이름이 다르면 계획의 나머지 부분에서도 그 이름으로 읽는다.

실패 시: inventory에 스킬이 없으면 플러그인 로딩 문제다. G1을 돌리기 전에 고친다.

### S3 — 트리거 측정과 Gate G1

목적: 이 설계에서 검증되지 않은 채 하중을 받는 주장("정적 description이 관련 주제에서는 뜨고 무관한 주제에서는 조용하다")을 측정한다.

위치: `dev/eval/graded.py`, `dev/eval/run.py`, `dev/libexec/check-eval-launch`, 새 케이스 `dev/eval/cases/findings-trigger-{direct,implicit,quiet-unrelated,quiet-near}/`.

요구 동작:

- **arm에 넣을 플러그인을 케이스가 고른다.** `case.yaml`의 선택 필드 `execution.plugins`(플러그인 이름 목록, 기본 `[kein]`)를 받는다. 이름은 run.py 안의 고정 대응(`kein -> plugin/`, `kein-findings -> plugin-findings/`)으로 소스 디렉터리를 찾는다. 모르는 이름이면 run을 시작하기 전에 거부한다. treatment arm은 목록의 플러그인마다 run 내부 복사본을 받는다. `kein`은 지금처럼 `prepare_plugin`으로 에이전트를 렌더하고, `kein-findings`는 복사만 한다. control arm은 아무것도 받지 않는다. `--variant` 모드에서는 각 arm이 자기 checkout의 같은 소스 디렉터리(`checkout/plugin-findings` 등)를 복사한다. fixture 모드와 `plan-*` 케이스는 기본값 `[kein]`으로 지금과 같은 명령줄을 받아야 한다. `launch_command`는 플러그인 디렉터리 목록을 받아 항목마다 `--plugin-dir`를 하나씩 붙인다(반복 가능, 위 사실). 빈 목록이면 아무것도 붙이지 않는다. 케이스 이름에서 소스 디렉터리를 찾는 부분은 복사 없이 부를 수 있는 순수 함수로 둔다. 그래야 `check-eval-launch`가 세션도 복사도 없이 단언할 수 있다.
- `tool_used` grader에 선택 필드 둘을 더한다. `skill:`은 `skills_invoked`에서 정확히 이 이름만 센다. S2에서 확인한 이름(기대값 `kein-findings:findings`)과, 네임스페이스 없는 `findings` 두 형태를 모두 받는다. `max:`는 상한이다. 기존 케이스의 판정은 바뀌지 않아야 한다.
- arm마다 `KEIN_FINDINGS_DIR`를 항상 명시적으로 설정한다. 케이스의 `execution.findings_dir: <케이스 디렉터리 기준 상대 경로>`가 있으면 그 디렉터리를 워크트리 밖의 replicate별 경로(`<run_dir>/findings/<arm>-<index>`)로 복사하고 그곳을 가리킨다. 없으면 존재하지 않는 replicate별 경로를 가리킨다. fixture 모드 실행도 같다. 이것이 없으면 모든 arm이 운영자의 실제 `~/.agents/findings`를 본다(Pre-mortem S3). 발견을 워크트리 밖에 두는 이유도 있다. arm이 cwd를 `ls`해서 발견을 찾는 경로를 막아야 스킬 발화만 측정할 수 있다.
- `check-eval-launch`에 단언을 더한다. (1) `plugins`를 선언하지 않은 케이스: treatment 명령줄에 `--plugin-dir`가 정확히 하나이고 `kein` 복사본을 가리킨다. control에는 없다. 지금 단언과 같은 결과다. (2) `plugins: [kein-findings]`인 케이스: treatment에 `--plugin-dir`가 정확히 하나이고 `kein-findings` 복사본을 가리킨다. `kein`은 들어가지 않는다. control에는 없다. (3) 모르는 플러그인 이름은 거부한다. (4) 케이스가 `findings_dir`를 선언하지 않아도 arm 환경의 `KEIN_FINDINGS_DIR`는 운영자 값이 아니라 존재하지 않는 run 내부 경로여야 한다. 선언하면 워크트리 밖의 복사본을 가리켜야 한다.
- 케이스 넷. 모두 `execution.plugins: [kein-findings]`를 선언한다. 모두 entry를 고정하지 않는다(슬래시 접두어 없음). 발견 fixture는 합성한다. 실제 개인 note를 리포에 복사하지 않는다. 합성 발견 하나에는 모델이 사전 지식으로 댈 수 없는 표지(예: 가짜 측정값과 `versions: claude-code 0.0.0-fixture`)를 심는다.
  - `findings-trigger-direct`: 한국어로 런타임 동작을 직접 묻는다. 예: agent teams 없이 서브에이전트끼리 메시지를 주고받을 수 있는지 묻고, 답을 `ANSWER.md`에 쓰게 한다.
  - `findings-trigger-implicit`: 동작을 묻지 않는 설계 작업이다. 예: fixture의 `SKILL.md`에 워커 간 메시지 전달 절차를 더한다. 발견이 관련은 있지만 질문으로 드러나지 않는다.
  - `findings-trigger-quiet-unrelated`: 에이전트 영역 밖의 코딩 작업이다.
  - `findings-trigger-quiet-near`: 에이전트 영역 어휘는 있지만 런타임 믿음이 필요 없는 작업이다. 예: fixture `SKILL.md`의 오탈자를 고친다.
- grader: hit 케이스에는 `tool_used` `skill: <S2에서 확인한 이름>` `min: 1`과, 결과 파일에 심은 표지가 나오는지 보는 `regex`를 둔다. quiet 케이스에는 같은 `skill:`에 `max: 0`과 결과 파일의 `file_exists`를 둔다. 각 케이스에 `selftest/should-pass|should-fail/_record.json`을 둔다.
- 1차 측정은 기본 arm 쌍(`with-skill`/`without-skill`)으로 케이스마다 3회 돌린다. 스킬 grader는 control에서 구조적으로 실패하므로 판정은 with-skill arm의 횟수로 읽는다. 표지 grader의 arm 간 차이는 발견이 답을 바꿨는지 보여 준다.

수용 기준:

- `dev/kein-dev check-eval-launch`가 통과해야 한다.
- `dev/kein-dev eval --case <each> --self-test`가 네 케이스 모두 통과해야 한다.
- 기존 두 케이스(`plan-evidence-gate`, `plan-no-unknown`)의 `--self-test`도 그대로 통과해야 한다.
- 네 케이스의 1차 실측이 모든 replicate에서 끝나야 한다(timeout과 비정상 exit 없음). 그 뒤 G1이 판정한다.

G1 판정표. 표기: D는 direct 발화 수(/3), I는 implicit(/3), Q는 quiet 두 케이스 합산(/6)이다. 모두 with-skill arm(2차에서는 각 variant arm)의 `skills_invoked` 기준이다. "통과 기준"은 D=3, I≥2, Q≤1이다. "부분 기준"은 D≥2, Q≤3이다. "모자람"은 D<3 또는 I<2이고, "넘침"은 Q≥2다.

| 차수 | 결과 | 조건 | 경로 |
| :-- | :-- | :-- | :-- |
| 1차 | 통과 | 통과 기준 | S5로 간다. 시작 문안을 둔다. |
| 1차 | 모자람 | 모자람이고 넘침 아님 | description을 한 번 넓힌 뒤 2차 |
| 1차 | 넘침 | 넘침이고 모자람 아님 | description을 한 번 좁힌 뒤 2차 |
| 1차 | 혼합, 부분 | 모자람이면서 넘침, 그리고 부분 기준 | 한 방향 수정으로 둘 다 고칠 수 없다. 수정하지 않고 S5로 간다. 시작 문안을 두고, B안을 `docs/skills/findings/open.md`에 후보로 올린다. |
| 1차 | 혼합, 실패 | 모자람이면서 넘침, 그리고 부분 기준 미달(D≤1 또는 Q≥4) | 멈춤 경계(Unexpected result) |
| 2차 | 통과 | before나 after 중 하나 이상이 통과 기준 | S5로 간다. 통과한 문안을 두고, 둘 다 통과하면 after를 둔다. |
| 2차 | 부분 | 통과한 문안은 없지만 하나 이상이 부분 기준 | S5로 간다. 부분 기준을 만족한 문안 중 D+I가 큰 쪽을 둔다. 같으면 Q가 작은 쪽, 그래도 같으면 before를 둔다. B안을 `docs/skills/findings/open.md`에 후보로 올린다. |
| 2차 | 실패 | 두 문안 모두 부분 기준 미달 | 멈춤 경계(Unexpected result) |

2차는 네 케이스를 `--variant before=<S2 커밋> --variant after=HEAD`로 케이스마다 3회 돈다. 두 variant arm 모두 자기 checkout의 `plugin-findings/`를 받는다. description 수정은 이 계획에서 한 번뿐이다. 부분 경로에서도 스킬을 slash 전용으로 바꾸지 않는다. 부분적으로라도 뜨는 트리거가 R1의 선호에 더 가깝기 때문이다.

**Gate — G1 트리거 발화.**

- Claim: 상황으로 쓴 정적 description만으로도 헤드리스 세션에서 `kein-findings:findings`가 관련 작업에서는 불리고 무관한 작업에서는 불리지 않는다. 기준은 판정표의 통과 기준이다(direct 3/3, implicit ≥2/3, quiet 합산 ≤1/6).
- Evidence method: `dev/kein-dev eval --case findings-trigger-<name>`을 네 케이스에 돌리고 with-skill arm에서 스킬 grader가 통과한 횟수를 센다. 같은 run의 `system/init.skills`를 두 가지로 확인한다. with-skill arm에는 스킬이 있어야 하고, control arm에는 없어야 한다. control arm을 보는 이유는 사용자 범위로 켠 플러그인이 새 config home을 뚫고 섞이지 않았는지 확인하려는 것이다.
- Alternate path: 판정표의 1차 모자람과 넘침 행(한 번 고친 뒤 2차)과, 1차 혼합-부분 행과 2차 통과·부분 행(S5로 가고, 부분 경로에서는 B안을 `open.md`에 올림)이다. 1차 결과는 통과가 아니면 모자람, 넘침, 혼합 중 하나에 반드시 들어간다. 2차 결과는 통과, 부분, 실패 중 하나에 반드시 들어간다.
- Unexpected result: 다음 가운데 하나면 S5를 시작하지 않고 멈춘다. (a) 판정표의 1차 혼합-실패나 2차 실패: 측정 run 경로와 D/I/Q 수치를 붙여 B안, C안 중 무엇으로 갈지 사용자에게 넘긴다. (b) with-skill arm의 init inventory에 스킬이 없다: S2의 로딩 실패로 돌아간다. 고친 뒤 1차부터 다시 재고, 한 번뿐인 수정은 쓰지 않은 것으로 친다. (c) control arm의 init inventory에 스킬이 있다: 그 run의 수치를 버리고 `run.py`의 격리부터 고친 뒤 다시 잰다. (d) replicate가 timeout이나 비정상 exit로 끝났다: 그 케이스만 다시 돈다. 다시 돈 뒤에도 끝나지 않으면 판정하지 않고 멈춘다.

### S4 — 옛 스킬 은퇴, 이행, inbox drain

목적: R4와 R6이다. inbox를 비우고, 옛 스킬이 다시 inbox를 채우는 경로를 끊는다.

위치: 리포 밖의 개인 파일은 `~/.claude/skills/wiki-collect`, `~/.claude/skills/wiki-record`, `~/.agents/disabled-skills/`, `~/Documents/wiki/`, `~/.agents/findings`(symlink)다. 리포 안에서는 `docs/open-threads.md`(승격 후보가 있을 때만)가 바뀐다.

순서와 요구 동작. 순서가 중요하다.

1. **은퇴를 먼저 한다.** 두 스킬 디렉터리를 `~/.agents/disabled-skills/wiki-retire-<YYMMDD>/`로 옮긴다(삭제하지 않음). 기존 `codex-orca-migration-20260730` 선례를 따른다. 은퇴가 drain보다 먼저여야 하는 이유가 있다. drain 중이나 뒤에 다른 세션의 `wiki-record`가 `_raw/note/`를 다시 만들지 못하게 하려는 것이다.
2. **스냅샷을 커밋한다.** `~/Documents/wiki`의 커밋되지 않은 현재 상태 전체를 먼저 한 커밋으로 남긴다(`.gitignore`가 거르는 것은 제외). 이후 모든 이동과 삭제를 `git mv`나 `git rm` 커밋으로 하고, 이 스냅샷으로 되돌릴 수 있게 하려는 것이다. 저장소에 remote가 없으므로, 이 스냅샷 이후로는 이력을 다시 쓰는 명령(amend, rebase, gc prune)을 쓰지 않는다.
3. **drain 규칙을 적용한다.** 대상은 note 20개(`wiki_deprecated` 18개와 `wiki` 2개)와 외부 글 4개, 합쳐 24개다. 항목마다 목적지는 셋 중 하나다. 판정은 에이전트가 한다. 모든 삭제는 스냅샷 커밋 뒤의 `git rm`이다. `wiki_deprecated` 쪽 항목은 원본이 거기 그대로 남는다. 그래서 되찾을 수 없는 손실이 없고, 실행 중에 사람 승인이 필요하지 않다(메모리 [[unattended-runs-no-mid-run-approval]]).
   - **발견**: 무언가를 돌리거나 관측한 결과를 담은 note. 예상 대상은 `wiki_deprecated/_raw/note/`의 서로 다른 17개 가운데 측정인 것과 `wiki/_raw/note/` 2개다. 각 파일은 같은 basename으로 `~/Documents/wiki/findings/`에 둔다(`wiki` 쪽은 `git mv`, `wiki_deprecated` 쪽은 복사). 옛 frontmatter는 새 스키마로 바꾼다. `measured`는 옛 `date`에서 가져온다. `claim`은 본문에서 한 문장을 뽑는다. `versions`와 `reproduce`는 본문에 버전 줄이나 재현 명령이 있을 때만 채우고, 없으면 `unrecorded`로 둔다. `project`는 옛 값을 유지한다. 본문은 바꾸지 않는다. `2026-08-06-…` 형식의 이름은 `YYMMDD-`로 맞춘다.
   - **승격 후보**: 외부 글이나 note 중 규칙이나 스킬의 행동을 바꿀 내용이 있는 것(예: `260819-Extend Claude with skills.md`). `docs/open-threads.md`에 한 항목을 적는다. 항목에는 무엇을 바꿀 후보인지 한 줄, 그리고 되찾을 위치(`~/Documents/wiki` 스냅샷 커밋 해시와 원래 경로, `wiki_deprecated`에서 온 것이면 그 경로)를 적는다. 이 항목은 `/kein:deliberate`에 넘길 대상이다. 파일 자체는 삭제한다. 이번에 규칙을 편집하지는 않는다.
   - **삭제**: 나머지 전부. 측정이 아닌 note(판정 기준: 돌린 명령이나 관측값이 없고 질문 목록이나 메모인 것. 예상 후보는 `260718-open-questions-to-discuss.md`), 행동을 바꾸지 않는 외부 글, 바이트가 같은 중복(`2026-08-06-a-red-gate-…`)이 여기 들어간다. 빈 `_rules/`와 `.agent/`, 옛 장치 `~/Documents/wiki/.claude/`도 지운다. `.claude/`는 이 저장소에서 작업하는 에이전트에게 옛 wiki 명령과 스킬을 로드한다.
   - **건드리지 않음**: `무제*.md` 4개, `.obsidian/`, `.gitignore`(U2). 이것들은 24개 집계에 넣지 않는다.
   - 분류표(파일, 목적지, 한 줄 사유)는 drain 커밋 메시지 본문에 적는다. 별도 파일은 만들지 않는다.
4. **inbox 자체를 없앤다.** 비워진 `~/Documents/wiki/_raw/`를 제거한다. 새로 생기는 기록의 목적지는 이제 발견 루트 하나다. 그래서 drain 규칙을 상시 문장으로 남기지 않는다. inbox가 없으면 비울 대상도 없다.
5. **탐지 경로를 연결한다.** `~/.agents/findings -> ~/Documents/wiki/findings` symlink를 만든다.

수용 기준(플러그인을 켜기 전이므로 bin은 리포 경로로 부른다):

- `<repo>/plugin-findings/bin/findings check`가 exit 0으로 끝나야 한다. 이때 `<repo>/plugin-findings/bin/findings where`는 `~/.agents/findings`를 내야 한다. `unrecorded` 개수는 보고에 싣는다.
- 개수가 맞아야 한다: 24 = 발견 n + 승격 후보 k + 삭제 m. 커밋 메시지의 분류표와 `docs/open-threads.md`의 새 항목 k개로 대조한다. 삭제 m에는 중복 1이 들어 있다.
- `ls ~/.claude/skills`에 `wiki-collect`와 `wiki-record`가 없어야 한다. `grep -rln "Documents/wiki/_raw" ~/.claude/skills ~/.agents/skills ~/.codex/AGENTS.md 2>/dev/null`가 아무것도 내지 않아야 한다.
- `~/Documents/wiki/_raw`, `.claude`, `_rules`, `.agent`, `memory`가 없어야 한다. `무제*.md` 4개는 스냅샷 커밋과 바이트가 같아야 한다(`git -C ~/Documents/wiki diff <snapshot> -- '무제*.md'`가 비어 있음). `git -C ~/Documents/wiki status --short`가 비어 있어야 한다.
- `<repo>/plugin-findings/bin/findings list`가 `260808-subagent-capabilities-without-agent-teams.md`의 claim 줄을 보여야 한다.

실패 시: 개수가 맞지 않거나 `check`를 통과시킬 수 없는 note가 있으면 그 파일을 옮기지 않고 원래 자리에 둔다. 그리고 `_raw/` 제거(4번)를 하지 않는다. 남은 파일 목록을 보고한다. 되돌리기는 스냅샷 커밋으로 `git -C ~/Documents/wiki reset --hard <snapshot>` 하고, 은퇴한 스킬 디렉터리를 원래 자리로 옮기고, `docs/open-threads.md`의 새 항목을 되돌리는 것이다.

### S5 — 사용자 범위로 켜기, 측정 기록과 설명

목적: G1이 정한 문안으로 `kein-findings`를 모든 프로젝트에서 켜고(U1), G1의 결과를 이 리포의 규칙이 정한 자리에 남기고, 사람이 읽을 설치·사용 설명을 더한다.

S5는 G1과 S4를 기다린다. G1이 멈춤 경계에서 끝났으면 S5는 시작하지 않는다. 사용자 범위로 켜는 일은 모든 프로젝트, 모든 세션에 비용이 드는 변경이므로, 트리거가 판정표상 쓸 만하다고 나온 뒤에만 한다.

위치: 개인 설정 `~/.claude/skills/kein-findings`(symlink), `~/.claude/settings.json`(`enabledPlugins`에 한 줄). 리포 안에서는 `docs/skills/findings/YYMMDD-trigger.md`(새 파일), `docs/skills/findings/open.md`(판정표가 부분 경로로 끝났을 때만), `README.md`.

요구 동작:

- `~/.claude/skills/kein-findings -> <repo>/plugin-findings` symlink를 만든다. `~/.claude/settings.json`의 `enabledPlugins`에 `"kein-findings@skills-dir": true`를 더한다. 다른 항목은 바꾸지 않는다.
- 측정 문서에는 다음을 적는다. G1 판정표에서 어느 행으로 끝났는지, 차수별·케이스별 발화 수(D/I/Q), 표지 grader의 arm 간 결과, 둔 문안, run 디렉터리 경로, 측정한 Claude Code 버전, 다시 돌리는 명령.
- README에는 다음을 적는다. Layout에 `plugin-findings/`, 두 번째 플러그인을 두는 이유(켜는 범위가 다르다, U1), `kein-findings@skills-dir` symlink와 사용자 범위로 켜는 설정, 발견 루트 탐지 순서, `~/.agents/findings` symlink 관례, `findings check`, `claude plugin validate plugin-findings --strict`. 개인 경로는 예시로만 적는다. 첫 줄의 "Five skills" 같은 집계가 `kein`에 대한 것임이 흐려지지 않게 한다.
- 장치 상한을 확인한다. 이 계획 전체의 리포 diff에서 `plugin-findings/` 아래 새 파일은 `.claude-plugin/plugin.json`, `bin/findings`, `skills/findings/SKILL.md` 셋뿐이어야 하고, `plugin/` 아래 변경은 없어야 한다.

수용 기준:

- `git diff --stat <plan 시작 커밋>..HEAD -- plugin-findings/`는 위의 세 파일만 보여야 한다. `git diff --stat <plan 시작 커밋>..HEAD -- plugin/`은 비어 있어야 한다.
- `claude plugin validate plugin-findings --strict`와 `claude plugin validate plugin --strict`가 통과해야 한다.
- `claude plugin list`가 `kein-findings@skills-dir`를 로드되고 켜진 상태로 보여야 한다.
- `kein`이 켜지지 않은 새 임시 디렉터리(`mktemp -d`)에서 헤드리스 `claude -p … --output-format stream-json --verbose`를 돌린다. 이벤트의 `system/init.skills`에 `kein-findings:findings`가 있고 `kein:` 스킬은 없어야 한다. 같은 세션의 Bash에서 `command -v findings`가 `plugin-findings/bin/findings`를 가리켜야 한다.
- 측정 문서의 재현 명령이 복사해 붙이면 그대로 도는 형태여야 한다.

실패 시: 임시 디렉터리 확인에서 스킬이 없으면 symlink나 `enabledPlugins` 문제다. 문서를 쓰기 전에 고친다. 되돌리기는 symlink와 설정 한 줄을 지우는 것이다.

## Pre-mortem

- **S1: eval은 통과했는데 실제 세션에서는 스킬이 뜨지 않는다.** 헤드리스 `-p`와 대화형 세션이 다르거나, 실제 세션에는 `kein`이나 omc의 스킬이 함께 있어 listing 예산이 description을 자르거나 트리거를 가져간다. G1 arm에는 `kein-findings`만 있다. Caught by: G1(헤드리스, 단독 플러그인 한정), S5 측정 문서에 적힌 한계 · Prevented by: S2가 description 앞 250자 안에 트리거를 두게 한 것 · Acts on: `plugin-findings/skills/findings/SKILL.md` frontmatter의 `description` 필드. S2 수용 기준의 문자 수 확인이 이것을 읽는다 · Residual: 대화형 세션과 다른 플러그인이 함께 있을 때의 발화율은 측정하지 않는다. 사후 관측은 Open Questions의 대화형 발화율 항목에 남긴다.
- **S2: 개인 발견이나 개인 경로가 배포되는 트리(`plugin/`, `plugin-findings/`)에 들어간다.** Caught by: S1의 `check-findings` 트리 단언(`Documents/wiki` 금지), S5의 두 트리 diff 확인 · Prevented by: 루트를 런타임에 플러그인 밖에서 정하는 것(결정 2), 그리고 합성 eval fixture · Acts on: `findings`의 루트 탐지(`KEIN_FINDINGS_DIR`, 다음 `$HOME/.agents/findings`)와 `dev/eval/cases/findings-trigger-*/`의 fixture 파일 · Residual: 개인 발견을 인용한 문장을 누군가 스킬 본문에 직접 쓰는 경우는 grep으로 못 잡는다. 이것은 리뷰가 맡는다.
- **S3: eval arm이 운영자의 실제 발견이나 사용자 범위 플러그인을 본다.** 그러면 G1이 합성 fixture가 아닌 것으로 통과하고, 기존 `plan-*` 케이스의 arm에도 개인 발견이 섞인다. 사용자 범위로 켠 `kein-findings`가 control arm에 들어가면 control이 control이 아니게 된다. Caught by: S3 수용 기준의 `check-eval-launch` 단언 (1)–(4), G1 Evidence method의 control arm init inventory 확인과 Unexpected result (c) · Prevented by: `run.py`가 모든 arm에 `KEIN_FINDINGS_DIR`를 명시적으로 설정하는 것, 새로 만드는 config home, 케이스가 고른 플러그인만 `--plugin-dir`로 넣는 것 · Acts on: `run.py` `launch`가 만드는 `environment` dict(운영자 `os.environ`의 값을 덮어씀)와 `launch_command`가 붙이는 `--plugin-dir` 목록 · Residual: arm의 `HOME`은 운영자와 같다. 스킬을 거치지 않고 `~/.agents/findings`를 직접 여는 arm은 막지 못한다. 합성 fixture의 표지가 이 경우를 드러낸다(실제 발견에는 표지가 없다).
- **S4: 장치가 다시 자란다.** index 파일, 설정, frontmatter 필드, 하위 디렉터리, 두 번째 bin이 조금씩 붙어 옛 wiki의 76% 패턴을 반복한다. Caught by: S5의 `plugin-findings/` diff 확인(파일 셋), S1 `check`의 1·4번 위반, `check-findings`의 bin 단일 단언 · Prevented by: `check`의 닫힌 키 집합과 flat 루트 규칙, `bin/`에 `findings` 하나 · Acts on: 발견 루트 최상위의 항목 목록과 각 파일의 frontmatter 키(`check`가 매 기록 뒤 읽음), `plugin-findings/bin/`의 항목 목록(`check-findings`가 읽음) · Residual: `check` 자체를 넓히는 변경은 막지 못한다. 그런 변경은 `/kein:deliberate`를 거치게 되어 있다.
- **S5: 이행이 note를 잃거나 바꾸거나, 사용자 파일을 건드린다.** Caught by: S4 수용 기준의 24개 대조, `findings check`, `무제*.md`의 스냅샷 대비 무변경, 빈 `git status` · Prevented by: 스냅샷 커밋을 먼저 하는 것, 모든 삭제를 스냅샷 뒤의 `git rm`으로 하는 것, 스냅샷 뒤 이력을 다시 쓰지 않는 것, 본문 무변경 · Acts on: `~/Documents/wiki` git 저장소의 커밋과 `git mv`/`git rm`. 원본 경로는 basename으로 맞추고, 승격 후보는 `docs/open-threads.md`에 스냅샷 해시와 경로로 남긴다 · Residual: `claim` 한 줄 요약이 note의 주장을 잘못 옮길 수 있다. 사람이 읽지 않으므로(U2) 이것은 에이전트가 claim으로 파일을 골라 본문을 읽을 때만 드러난다. 잘못 고르지 않은 파일은 드러나지 않는다.
- **S6: 은퇴가 불완전해 옛 경로로 계속 쓰인다.** 다른 곳에 사본이 있거나, 이미 열린 세션에 옛 스킬이 로드돼 있는 경우다. Caught by: S4 수용 기준의 `ls`와 `grep -rln "Documents/wiki/_raw"`, 그리고 `_raw/` 부재 확인 · Prevented by: 은퇴를 drain보다 먼저 하는 순서 · Acts on: `~/.claude/skills/wiki-{collect,record}` 디렉터리 이동 · Residual: S4 실행 중에 이미 열려 있던 세션은 옛 스킬을 계속 가진다. 그 세션이 쓰면 `_raw/`가 다시 생긴다. 그러면 다음 `git status`에 보인다.
- **S7: description이 너무 넓어 에이전트 관련 작업마다 뜬다.** 사용자 범위로 켜므로 모든 프로젝트에 비용이 든다. Caught by: G1의 quiet 케이스 두 개와 판정표의 넘침 행 · Prevented by: 조회 절차 1단계. 목록 한 번으로 끝나고 무관하면 본문을 읽지 않는다 · Acts on: 스킬 본문의 조회 절차. 에이전트가 `findings list` 출력의 claim 줄로 파일을 고른다 · Residual: 영역 안의 무관한 작업에서 뜨는 목록 호출 한 번은 받아들인다.
- **S8: `kein-findings`는 켜져 있는데 이 리포의 도구가 그것을 보지 않는다.** `claude plugin validate plugin --strict`와 `check-agents`는 `kein`만 본다. 누군가 `plugin-findings/`를 고친 뒤 kein 쪽 검사만 돌리면 깨진 manifest나 `ocs`를 부르는 bin이 그대로 배포된다. Caught by: S1·S2 수용 기준의 `claude plugin validate plugin-findings --strict`와 `dev/kein-dev check-findings`, S3의 `check-eval-launch` 단언 (2) · Prevented by: AGENTS.md 명령 블록에 두 명령을 더한 것, `check-findings`의 트리 단언(`ocs` 금지, bin 단일) · Acts on: `dev/libexec/check-findings`가 `$KEIN_REPO_ROOT/plugin-findings/` 트리를 grep하고 bin을 실행하는 것 · Residual: 두 플러그인을 한 번에 검사하는 단일 명령은 없다. AGENTS.md 명령 블록을 읽고 둘 다 돌리는지에 기댄다.
- **S9: 두 플러그인의 버전이 어긋나거나 `bump-version`이 `kein-findings`를 잘못 건드린다.** marketplace에서 `kein-findings` 항목이 `kein` 앞에 들어가거나 `version`을 가지면, `bump-version`이 두 번째 `"version"`을 `kein`으로 잘못 읽거나 같은 문자열을 함께 올린다. Caught by: `check-findings`의 "marketplace.json의 `version` 필드는 정확히 둘" 단언 · Prevented by: 항목을 `kein` 뒤에 붙이고 `version`을 두지 않는 것(결정 1), 시작값을 `kein`과 다른 `0.1.0`으로 두는 것 · Acts on: `.claude-plugin/marketplace.json`의 `plugins[1]`에 `version` 키가 없다는 사실. `bump-version`의 `sed -n '2p'`와 전체 치환은 이 사실을 전제로 `kein`만 읽고 쓴다 · Residual: `plugin-findings/.claude-plugin/plugin.json`의 버전은 아무것도 옮기지 않는다. skills-dir 방식에서는 로드에 영향이 없지만, marketplace 설치자는 옛 캐시를 계속 쓸 수 있다(Open Questions).
- **S10: `findings`라는 이름이 PATH의 다른 명령과 부딪친다.** 사용자 범위로 켜므로 모든 프로젝트의 PATH에 올라간다. 어떤 프로젝트가 같은 이름의 도구를 PATH에 두면, 스킬이 엉뚱한 프로그램을 부른다. 그 프로그램의 exit code는 `where`의 exit 3 약속과 다르다. Caught by: 계획 시점의 `command -v findings`(비어 있음, 위 사실), S5 수용 기준의 `command -v findings`가 `plugin-findings/bin/findings`를 가리키는지 확인 · Prevented by: None · Residual: 이후 프로젝트별로 생기는 충돌은 잡지 못한다. 플러그인 bin과 프로젝트 PATH의 순서는 측정하지 않았다. 충돌이 관측되면 bin 이름을 `kein-findings`로 바꾸고, 스킬 본문과 `check-findings`를 함께 고친다.

## Open Questions

- 이 리포 AGENTS.md의 "스킬별 측정 결과는 `docs/skills/<skill>/`" 줄과 R1의 관계. 기본값(추론): `docs/skills/`는 이 리포 스킬의 eval 보고로 남긴다. 외부 런타임(Claude Code, Codex, Orca)의 동작 측정은 발견 루트로 보낸다. S5의 G1 기록도 이 기본값을 따라 `docs/skills/findings/`에 둔다. 사용자가 skill eval 보고까지 발견 루트로 옮기길 원하면 AGENTS.md 한 줄과 기존 `docs/skills/*` 파일의 처리가 새 범위로 생긴다.
- Codex 노출. 지금은 발견이 고정 경로의 평범한 파일이라서 경로를 들은 Codex만 읽는다. `~/.agents/skills/`에 조회 스킬을 둘지는 Codex 쪽에서 `findings`가 PATH에 있는지에 달려 있다. `findings`는 Claude Code 플러그인의 bin이라 Codex의 PATH에는 없다. 그리고 R6가 Codex용 스킬을 범위 밖으로 두었으므로 이번에는 하지 않는다.
- 대화형 세션의 실제 발화율. G1은 헤드리스, 단독 플러그인만 잰다. 몇 주 뒤 세션 기록(`~/.claude/projects/*/*.jsonl`)에서 `kein-findings:findings` 호출과 그 세션의 주제를 세 보는 사후 관측을 할지, 한다면 언제 할지 정해야 한다. 이 관측이 결정 2의 "뒤집을 증거"의 실제 공급원이다.
- `kein-findings`의 버전 이동. 기본값: plugin.json의 `0.1.0`은 사람이 필요할 때 손으로 올린다. `bump-version`은 `kein`만 다룬다. skills-dir 방식으로 쓰는 동안에는 버전이 로드에 영향이 없다(README의 version trap). marketplace로 설치하는 사람이 생기면 선택지가 생긴다. `bump-version`이 두 플러그인을 함께 올리게 하거나, 플러그인별 인자를 받게 하거나, `kein-findings` plugin.json에서 version을 빼고 커밋 SHA를 쓰는 것이다. 마지막 안은 strict 검사와 충돌한다(위 사실). 어느 쪽이든 `bump-version` 스킬과 `dev/libexec/bump-version`을 바꾸는 별도 작업이다.
