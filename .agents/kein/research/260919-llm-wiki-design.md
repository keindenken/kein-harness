# LLM wiki 설계 방향

Date: 2026-09-19

## 질문

LLM wiki(개인용 LLM 지식/기억 저장소) 설계 방향. 이전 시도는 'LLM이 모르는 지식을 수집하는 지식저장소'로 시작했다가 '기억저장소'로 바꾸려다 구조가 엉켜 폐기했다. (1) 공개된 LLM wiki 사례들(Karpathy의 LLM wiki 아이디어, GitHub 구현, YouTube 소개 등)은 어떤 목표와 구조를 택했나, (2) 지식저장소 vs 기억저장소를 섞으면 왜 엉키는지, 둘을 분리하거나 하나를 고르는 기준, (3) Claude Code 스킬/하네스 위에서 구현할 때 추천 설계(수집·정리·조회 흐름, 파일 구조, 에이전트가 쓰는 방식).

## 답

### (1) 공개 사례는 거의 전부 같은 뼈대를 쓴다

- Karpathy 원문은 **외부 소스로 만드는 지식저장소**다. 세 층(`raw/` 불변 원자료, LLM이 쓰는 `wiki/`, 규칙 문서 CLAUDE.md/AGENTS.md)과 `index.md`(목록), `log.md`(append-only 이력), 세 연산(ingest, query, lint)이 전부다. 사람은 소스를 고르고 질문하고, LLM은 "그 밖의 전부"를 한다. 대화 기억이나 사용자 선호를 담는 층은 원문 어디에도 없다. — 소스: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (원문 75줄 전체 확인, document-specialist 레인)
- 구현체도 이 뼈대를 그대로 따른다. 확인한 셋(`SamurAIGPT/llm-wiki-agent`, `Astro-Han/karpathy-llm-wiki`, `AgriciDaniel/claude-obsidian`) 모두 raw/wiki/index/log + ingest/query/lint이다. — 재생성: `gh api "repos/<repo>/git/trees/HEAD?recursive=1" --jq '.tree[].path'`, 스키마 파일은 각각 `CLAUDE.md`, `SKILL.md`, `WIKI.md`
- 차이는 뼈대 위에 얹은 것에서 난다. `Astro-Han`은 "load-bearing 사실(숫자·날짜·인용)은 링크된 raw에 글자 그대로 있어야 한다"는 grounding invariant를 두고 `scripts/check_evidence.py`로 기계 검사한다. `claude-obsidian`은 `wiki/hot.md`("bounded recent context")라는 세션 이월 층을 wiki 안에 넣었다. 기억을 wiki에 섞은 사례다. — 소스: 위 파일들
- **공개 구현의 대부분은 며칠 만에 멈춘다.** Karpathy 형식 로그 머리줄(`"] ingest |"`)로 GitHub 코드 검색을 한 랭킹 상위 100건(93개 리포, 포크 0)을 셌다. wiki 디렉터리 커밋 기준으로 보면, 커밋한 날짜 수의 중앙값은 2일, 첫 커밋부터 마지막 커밋까지의 기간 중앙값은 2일이다. 30일 넘게 이어진 곳은 31개, 마지막 커밋이 60일 넘게 지난 곳은 66개다. `log.md` 머리줄로만 세면 30일 넘게 이어진 곳은 21개로 더 적다. 로그 규율이 사용보다 먼저 무너진다는 뜻이다. — 재생성: `.agents/kein/research/260919-llm-wiki-design.survival.py` (파일 첫 줄에 실행법, 2026-09-19 실행)
- **생존과 "진행 중인 작업에 붙어 있음"의 연관은 약하다.** 코드 언어가 잡히는 리포의 비율은 30일 넘게 이어진 곳에서 26/31(84%), 멈춘 곳에서 43/62(69%)다. wiki가 리포 루트가 아닌 하위 경로에 든 비율은 14/31(45%) 대 20/62(32%)다. 방향은 맞지만 설계 근거로 삼을 만큼 크지 않다. — 재생성: 같은 스크립트. 코드 언어는 GitHub의 `language` 필드로 대신했다.
- 6개월 운영 후기(terryli.hm 등)는 **생존자 표본**이다. — 메커니즘: 계속 쓴 사람만 후기를 쓴다
- Karpathy 본인은 규모가 커지면 검색 계층(qmd: BM25+vector+rerank)을 붙이라고 했다. "files vs RAG"가 아니라 "개인 규모에서는 인프라를 미리 깔지 말라"는 입장이다. 원문은 index만으로 "~100 sources, ~hundreds of pages" 규모까지 버틴다고 적는다. — 재생성: `curl -sL https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw | grep -n -E "qmd|moderate scale"` (47행, 53행, 2026-09-19 확인)

### (2) 섞으면 엉키는 이유는 "무엇이 그것을 뒤집는가"가 다르기 때문이다

- 지식은 **새 근거에 의해 대체(supersede)**되지 잊히지 않는다. 기억은 경험에서 나오고 시간이 지나면 흐려져야 한다. 한 저장소에서 둘을 같은 연산으로 다루면 오래된 사실이 잊히거나, 반대로 낡은 기억이 사실처럼 남는다. — 소스: arXiv 2604.11364 (Roynard, 독립 연구자, 초록과 서론을 직접 확인). 이 논문은 층을 넷으로 나누고 층마다 지속 규칙을 다르게 준다. Knowledge는 "indefinite supersession", Memory는 "Ebbinghaus decay", Wisdom은 "evidence-gated revision", Intelligence는 "ephemeral inference"다. 동료 심사를 거치지 않은 한 사람의 제안이므로 무게는 의견에 가깝다.
- 분리 기준은 문헌마다 축이 다르다. CoALA는 **내용 유형**(semantic 사실 / episodic 사건 / procedural 방법)으로, Letta는 **접근 방식**(항상 컨텍스트에 있는 core vs 필요할 때 검색하는 archival)으로 나눈다. Claude Code는 **누가 쓰나**로 나눈다: CLAUDE.md는 사람이 쓰는 지시, auto memory는 Claude가 쓰는 관찰(`user`/`feedback`/`project`/`reference`). — 소스: arxiv.org/abs/2309.02427, docs.letta.com/concepts/memory-management, code.claude.com/docs/en/memory
- **의견:** 이전 시도가 엉킨 건 "지식 vs 기억"이라는 한 축으로 최소 세 축(내용 유형, 무효화 조건, 로딩 방식)을 한꺼번에 가르려 했기 때문일 가능성이 크다. 이전 위키를 읽지 않았으므로 검증하지 않은 추정이다.
- 이 리포 기록이 옛 위키의 **어느 부분을 실제로 인용했는지**는 셀 수 있다. `_raw/note/`(사용자가 직접 측정한 노트) 8회, 위키 전체 6회, `_rules/standing-prompt.md` 4회(지금은 `plugin/rules/`로 옮겨짐), `harness/`와 `context-engineering/` 요약 각 3회, `_rules/` 3회. 가장 많이 쓰인 것은 외부 지식도 사용자 선호도 아닌 **직접 측정한 발견**이었다. — 재생성: `grep -rhoE "~/Documents/wiki/[A-Za-z0-9_./-]*" docs .agents plugin agents | sed -E 's#(~/Documents/wiki/[^/]+/?[^/]*/?).*#\1#' | sort | uniq -c | sort -rn` (2026-09-19, df3f40c 기준)
- **의견:** 그래서 고를 축은 "지식이냐 기억이냐"보다 **무엇이 항목을 무효로 만드느냐**가 낫다. 이 리포의 근거 계약(`plugin/rules/standing-prompt.md`)과 같은 축이다.
  - 외부 지식 → 더 새로운 소스가 대체한다. wiki에 둔다.
  - 직접 측정한 발견 → 같은 측정을 다시 돌리면 뒤집힌다. wiki에 두되 버전과 재현 프로브를 단다. 위 논문의 Wisdom 층("evidence-gated revision")과 같은 자리다.
  - 선호와 교정 → 사용자가 다르게 말하면 뒤집힌다. Claude Code auto memory에 둔다. wiki에 두지 않는다.
  - 작업 절차 → 스킬이나 규칙 파일로 간다. 옛 `_rules/standing-prompt.md`가 실제로 그렇게 옮겨졌다.
  - 진행 중인 작업 상태 → `.agents/kein/`(plans, handoff)에 둔다. wiki에 두지 않는다.

### (2′) 이 사용자의 옛 wiki는 어떻게 쓰였나 — 라운드 3

**관측 구간이 좁다.** `wiki_deprecated`의 git 커밋 45개는 모두 2026-08-03~08-09에 있다. Claude 세션 기록도 08-03 이후 것만 남아 있다. 파일 수정 시각으로 보면 내용의 상당수는 5~6월에 쓰였는데(5월 18개, 6월 25개), 그 시기의 사용은 보이지 않는다. 아래 수치는 wiki가 살아 있던 마지막 일주일과 그 뒤를 본 것이다. — 재생성: `git -C ~/Documents/wiki_deprecated log --format=%ad --date=short | sort | uniq -c`

- **그 일주일의 쓰기는 대부분 운영 장치로 갔다.** 실제 프로젝트 세션 66개(19개 디렉터리. `/private/tmp` 아래 eval·스크래치 세션 2,125개는 뺐다)에서 `~/Documents/wiki*`에 대한 Write/Edit는 446회다. 그중 `_system/`, `.claude/`, `CLAUDE.md`, `log.md`, `build-wiki.prompt.md`, `index.md`, `GEMINI.md`가 340회(76%)다. 구축 단계만 본 수치일 수 있다. git에서도 같은 모양이다: 커밋이 건드린 파일 중 `_raw` 200, 루트 파일 79, `.claude` 25, `_system` 17에 비해 주제 디렉터리는 `harness` 36, `llm-techniques` 31 등이다. — 재생성: jsonl의 `tool_use` 중 `file_path`에 `/Documents/wiki`가 들어간 것을 최상위 디렉터리별로 센다. `git -C ~/Documents/wiki_deprecated log --name-only --format= | awk -F/ '{print $1}' | sort | uniq -c`
- **에이전트가 밖에서 꺼내 쓴 경로는 kein-harness 하나였다.** `wiki-query` 호출은 0회다. wiki 폴더 밖에서 wiki 경로를 건드린 세션은 kein-harness(본 리포와 워크트리) 9개와 그 밖 4개다. Codex 세션 4,127개 중 wiki 경로가 나오는 것은 9월의 `wiki-record` 언급 5개다. 모두 wiki가 멈춘 뒤의 구간이다.
- **사람은 읽었다.** `~/Documents/wiki/.obsidian/workspace.json`의 `lastOpenFiles`에 `_raw/note/` 10개, `context-engineering/` 4개, `harness/agent-harness-comparison.md`, `_rules/` 3개가 있다. 에이전트 기록만으로 "꺼내 쓰지 않았다"고 말할 수 없다. — 재생성: `python3 -c "import json;print(json.load(open('$HOME/Documents/wiki/.obsidian/workspace.json'))['lastOpenFiles'])"`
- **옛 wiki는 폐기된 게 아니라 줄어든 채로 남아 있다.** `~/Documents/wiki`는 같은 vault가 이어진 것으로 보인다. 컴파일된 주제 페이지는 없고 `_raw`(외부 소스와 `note/`)와 `_rules`만 남았다. 8월 18~19일에 "note: …", "rules: …" 커밋이 있다. 사람이 직접 쓰는 `무제*.md`는 8월 26일과 9월 6일에 수정됐다. — 재생성: `git -C ~/Documents/wiki log --format='%ad %s' --date=short`, `ls -la ~/Documents/wiki`
- **쌓인 내용:** `_raw/`는 youtube 23, note 18, article 13, repo 4, docs 1이다. note 18개는 제목상 전부 에이전트 하네스를 만들며 측정한 발견이다.
- **범위가 넓어진 시점이 로그에 남아 있다.** `log.md` 머리줄 35개 중 `decision` 10개가 2026-08-03~04에 몰려 있다. 그중 "Vault becomes the default home for homeless knowledge", "`/record` skill and the `decisions/` area"가 있다. — 재생성: `grep -E '^## \[[0-9-]+\] decision' ~/Documents/wiki_deprecated/log.md`
- **의견:** 사용자가 실제로 남긴 형태(원자료 + 측정 노트 + 규칙, 컴파일본은 없음)는 공개 사례의 "raw는 쌓고 wiki는 LLM이 컴파일한다"와 다르다. 살아남은 것은 raw 층뿐이다. 컴파일 층이 가치를 냈는지는 이 자료로 판정되지 않는다.

### (3) Claude Code 위에서의 설계 — 의견, 근거는 각 줄에

- **먼저 판정할 것 — 컴파일 층이 필요한가:** **의견.** (2′)에서 살아남은 것은 raw 층(외부 소스, 측정 노트)과 규칙뿐이다. 에이전트가 wiki를 꺼내 쓴 경로는 kein-harness 하나였다. 사람이 Obsidian으로 읽은 흔적은 있다. 그래서 먼저 raw 층만 운영하고, 컴파일(`wiki/` 페이지 생성)은 "같은 주제를 여러 번 다시 찾는다"는 수요가 보일 때 붙이는 편이 낫다. 이 판정은 왜 멈췄는지(미해결 D3-a)에 따라 뒤집힐 수 있다.
- **범위:** wiki는 지식저장소 하나로 좁힌다. 기억은 새로 만들지 않고 이미 있는 저장소를 쓴다(auto memory, `.agents/kein/`). `claude-obsidian`의 `hot.md` 같은 세션 이월 층은 넣지 않는다. — 근거: 위 (2), 그리고 Karpathy 원문에 그 층이 없다는 점
- **측정 발견은 wiki가 아니라 그것을 낳은 리포에 둔다:** 하네스 측정은 `docs/skills/...`에, 다른 프로젝트의 측정은 그 프로젝트에 둔다. wiki는 외부 소스만 받는다. — 근거: (2′). 옛 note 18개가 모두 한 리포의 작업에서 나왔고, 소비도 그 리포에서 일어났다. 라운드 1의 "소스 두 종류" 안을 이것으로 대체한다.
- **규칙은 산문이 아니라 검사기로 강제한다:** 링크, frontmatter, index 동기화, "숫자·인용은 raw에 그대로 있어야 한다"는 검사를 스크립트로 둔다. — 근거: 6개월 운영 후기(terryli.hm, 2026-04-09) "Convention doesn't survive context loss ... The fix isn't a better schema — it's enforcement", `Astro-Han`의 check_evidence.py. 메모리 [[delete-rules-rather-than-reword]]와도 같은 방향이다.
- **lint는 다른 모델이 돈다:** 의미 점검(모순, 낡은 주장)은 `ocs ask codex`처럼 다른 벤더에 맡긴다. — 근거: proudfrog.com 글 "Claude on Wednesday is likely to read it, find it internally consistent, and certify it", ranjankumar.in 사례(요약이 원문을 대체한 뒤 lint 세 번이 서로 일관된 오류를 통과시킴)
- **감쇠 대신 대체:** 지식 페이지에는 망각 곡선을 넣지 않는다. 새 소스가 낡은 주장을 뒤집으면 `Status: Outdated`나 `Disputed`로 표시하고 지우지 않는다(`Astro-Han` 방식). 대신 `index.md`에 줄 수 상한을 둬서 정리를 강제한다. — 근거: arXiv 2604.11364, terryli.hm "Set budgets (max 80 lines for the index)"
- **조회는 agentic search로 한다:** `index.md`를 읽고 grep으로 찾는다. 임베딩은 수백 페이지를 넘겨 느려질 때만 붙인다. — 근거: Anthropic Agent SDK 블로그 "we suggest starting with agentic search, and only adding semantic search if you need faster results"
- **수요에서 출발:** **의견.** 진행 중인 작업이 부산물을 쏟아 넣는 형태가 따로 떨어진 "second brain"보다 오래 갈 것이다. 이 사용자에게 그 부산물은 이미 있다: `/research` 아티팩트, 측정 노트, handoff. 공개 데이터의 연관은 약하다(위 (1)). 이 사용자가 wiki에 실제로 무엇을 물었는지는 아직 세지 않았다(미해결 참고).
- **배치:** wiki는 별도 git 리포(경로는 새로 정한다. 아래 "이행" 참고)로 두고, 스키마는 그 리포의 AGENTS.md에 둔다. kein 플러그인에는 넣지 않는다. 다른 프로젝트에서 조회할 때만 쓰는 얇은 스킬 하나(`disable-model-invocation`)면 충분하다. — 근거: Karpathy 원문에서 스키마는 wiki와 함께 진화하는 문서다. 이 리포 CLAUDE.md에 따르면 `plugin/`은 켜진 모든 프로젝트에 올라간다.
- **대안 — 스테이징과 승격:** 고범수 영상(https://www.youtube.com/watch?v=sQSFeqeLKtU, 자동 자막이 매우 흐려 요지만 확인)은 에이전트가 자유롭게 쌓는 "agent vault"와 사람이 의도적으로 승격시키는 메인 vault를 분리한다. 위 설계는 LLM이 wiki에 직접 쓰는 것을 전제하므로 이 대안과 갈린다. **의견:** 생존 데이터(대부분 며칠 만에 멈춤)와 자기 검증의 한계를 보면, `raw/`는 자동으로 쌓더라도 `wiki/` 컴파일은 사람이 고른 것만 하는 편이 유지 비용과 오염을 둘 다 줄인다. 이 선택은 아직 근거로 판정되지 않았다.
- **이행:** `~/Documents/wiki`는 아직 있고 `_raw`(8월 19일 수정), `_rules`(8월 29일 수정), `무제*.md`를 담고 있다. `wiki_deprecated`와 따로 남은 것인지 언제 생겼는지는 확인하지 않았다. 설치된 `~/.claude/skills/wiki-collect`는 `~/Documents/wiki/_raw/...`에 저장한다. 그래서 새 wiki를 그 경로에서 시작하면 옛 스킬이 계속 거기에 쓴다. 옛 스킬을 먼저 걷어내거나 새 경로를 쓴다. — 재생성: `ls -la ~/Documents/wiki`, `grep -n "Documents/wiki" ~/.claude/skills/wiki-collect/SKILL.md` (11행, 92행, 라운드 2 감사자가 확인. 리드는 그 파일을 읽지 않음)
- **`/research`와의 연결:** `/research` 아티팩트는 이미 인용이 붙은 소스이므로 `raw/`로 들어가는 ingest 경로의 1순위 후보다. — 의견

## 분해와 배정

자료 없이 세운 가정이다.

| 단위 | 레인 |
|---|---|
| U1 공개 사례의 목표·구조 | 규정된 것(Karpathy 원문, `kein:document-specialist`) · 일어난 것(GitHub 구현체 트리·스키마·이슈) · 말해진 것(후기 블로그, YouTube) |
| U2 지식 vs 기억 | 규정된 것(CoALA, Letta, Anthropic memory 문서) · 말해진 것(분리 논의 글, 논문 하이라이트) · 일어난 것(이 리포가 옛 위키의 어느 부분을 인용했는지 셈) |
| U3 Claude Code 구현 | 규정된 것(Claude Code skills/memory 문서, Agent SDK 블로그) · 일어난 것(Claude Code용 구현체 3개) |

옛 스킬(`wiki-collect`, `wiki-record`, `wiki-query`)과 `~/Documents/wiki_deprecated`는 사용자 요청에 따라 일부러 읽지 않았다.

## 라운드

### 라운드 1
- **물은 것** — U1–U3 전부
- **레인** — 규정된 것: `kein:document-specialist` 1회(1차 소스 9개 읽음). 일어난 것: `gh search repos "llm wiki"` 상위 30개, 트리 6개, 스키마 파일 3개, 이슈 목록 5개 리포(각 최대 100건 제목 필터). 말해진 것: exa 검색 3회(후기, 분리 논의, YouTube), 결과 24건 하이라이트.
- **돌아온 것** — 위 답 절
- **감사** — 새 `kein:critic`. 인용: "라운드 하나를 더 열 근거가 있다. 이름 붙은 맹점 둘이 모두 '일어난 것' 레인으로 메워진다." S1: "'일어난 것' 레인에는 쓰이면서 자란 위키가 없었다 … 열어 본 스키마 파일 3개는 행위가 아니라 행위의 명세다." S2: 옛 위키 사용 증거가 이 리포의 인용뿐이다. 이 리포는 하네스를 만드는 곳이라 측정 노트 인용이 많은 것은 구조적으로 예상된다. D1: "위키가 어떤 질문에 답해야 하는지 … 아무도 묻지 않았다". D2: 새 위키가 기존 스킬·경로와 어떻게 공존하고 옮겨 갈지 묻지 않았다. 라운드 없이 할 일: X와 gist를 브라우저로 재시도, arXiv 원문 확인, 스테이징 대안 합성, 경로 충돌 확인.

### 라운드 2
- **물은 것** — S1과 D1: 실제로 쓰인 LLM wiki는 얼마나 오래 쓰이고, 살아남는 것은 어떤 종류인가. D2: 지금 경로와 스킬 상태.
- **레인** — 일어난 것. GitHub 코드 검색으로 `log.md` 93개를 모아 기록 날짜를 셈. 로컬에서 `ls`만.
- **돌아온 것** — 답 절의 "대부분 며칠 만에 멈춘다", "진행 중인 작업에 붙어 있다", "이행" 항목. 라운드 밖 수정으로 arXiv 초록 확인과 스테이징 대안 합성을 했다.
- **감사** — 새 `kein:critic`. 인용: "다음 라운드를 열 근거는 조건부로 하나 있다 … 사용자 허락 없이 열 수 있는 라운드는 없음이다." D-a: "라운드 2는 이것을 '공개 위키 중 무엇이 살아남나'로 바꿔 물었고, 둘은 다른 질문이다." 이것을 메울 레인은 보류 중인 S2다. D-b(생존 위키와 멈춘 위키의 스키마 비교)는 약한 근거로 D-a보다 뒤에 둔다. 과장 지적 세 건(생존 연관, 모집단 제약 누락, 이행 날짜)은 라운드 없이 고쳤다. 커밋 기준 보정(S-b)도 했다.
- **보류(해제됨)** — S2(옛 위키 git log의 디렉터리별 커밋 수, 세션 기록의 `wiki-query`·`wiki-record` 호출 수)는 옛 위키 메타데이터를 봐야 하므로 사용자 허락을 기다린다. 내용은 읽지 않는 조회다.

### 라운드 3
- **물은 것** — D-a/S2: 이 사용자가 옛 wiki를 실제로 어떻게 썼나. 무엇을 썼고, 누가 어디서 꺼내 썼고, 범위는 언제 넓어졌나.
- **레인** — 일어난 것. 사용자가 읽기를 허락했다("이제 읽어도 될듯"). `wiki_deprecated`의 파일 수, 디렉터리 이름, 로그 머리줄, note 제목을 봤다. Claude 세션 기록 2,191개와 Codex 세션 기록 4,127개의 tool_use를 셌다. 페이지 본문은 읽지 않았다.
- **돌아온 것** — 답 절 (2′). 설계의 "소스 두 종류"를 "측정 발견은 그 리포에"로 바꿨고, "먼저 판정할 것"을 더했다.
- **감사** — 새 `kein:critic`. 인용: "새 라운드를 열 근거는 없습니다." 지적 사항: 세션 표본 2,191개 중 2,125개가 `/private/tmp`(과장), 측정 구간이 wiki가 멈춘 뒤와 겹침, `~/Documents/wiki`를 사용 분석에서 뺌, 사람의 읽기를 세지 않음(S3-a, `lastOpenFiles`가 반대 증거), 계획한 `git log --name-only` 집계를 싣지 않음. 모두 라운드 없이 고쳤다. D3-a "왜 멈췄나"와 D3-b "지금 손으로 쓰는 vault는 무엇을 위한 것인가"는 사용자 본인만 답할 수 있어 미해결에 올렸다.

## 한계

- **모집단** — GitHub 리포 검색 "llm wiki" 6,874개 중 별 순 상위 30개를 목록으로 봤다. 생존 분석은 특정 로그 형식 문자열로 코드 검색한 랭킹 상위 100건(93개 리포)이다. 둘 다 전수가 아니다. 다른 로그 형식을 쓰는 wiki, 공개 리포의 기본 브랜치에 없는 것은 보이지 않는다. 후기 글은 exa 검색 상위 24건이다.
- **남은 맹점** — 로컬 전용이나 비공개 wiki(push하지 않은 Obsidian vault 등). 개인 wiki가 가장 흔히 머무는 곳인데, 메울 레인이 없다. 공개 생존율이 개인 사용 전체를 대표한다고 볼 수 없다.
- **하지 않은 일** — X/Twitter(HTTP 402)와 gist 작성 날짜(GitHub Gists API 서버 오류)는 이 세션에 붙은 브라우저로 다시 시도하지 않았다. 둘 다 결론을 바꾸지 않는 보조 근거라서 남겨 뒀다. 고범수 영상은 자동 자막이 흐려 요지만 확인했다.
- **읽지 않은 것** — 옛 wiki 페이지 본문과 옛 wiki 스킬 본문. 라운드 3은 이름, 개수, 로그 머리줄만 봤다.
- **세션 기록의 보존 구간** — Claude 세션 기록은 2026-08-03 이후 것만 남아 있고, `wiki_deprecated`의 git 기록도 08-03에 시작한다. 5~7월의 사용은 어느 소스에도 없다. 메울 레인이 없는 모집단 한계다.
- **사람의 읽기** — Obsidian `lastOpenFiles`는 최근 연 파일 목록일 뿐 횟수가 아니다.

## 미해결

- **D3-a/D3-b 사용자 답변 (2026-09-19, 요지):** 처음에는 "LLM이 모르는 지식을 더한다(스킬처럼)"로 접근해 글을 모았다. 그런데 context-engineering 글 몇 개 말고는 의미가 없었다. 이후 "언제 무엇을 봤고 어떤 느낌을 받았나"를 돕는 기억 보조 저장소로 쓰려 했다. 매번 로드되는 메모리보다 필요할 때 꺼내 읽는 방식을 선호한다. 바꾸는 과정에서 설정(toml)이 늘었다. 전역 CLAUDE.md에 지침을 적어도 에이전트가 자연스럽게 읽는 흐름이 생기지 않았다. `wiki-query`는 충분히 쌓이기 전이라 쓸 일이 없었다. 발견은 wiki에 두고 싶다. 리포 `docs/`는 사람이 읽는 문서용으로 남기고 싶다. 지금 `~/Documents/wiki`는 옛 wiki를 버린 뒤 갈 곳 없는 기록을 잠깐 두는 곳이다.
  - 이 답으로 설계 줄 "측정 발견은 그것을 낳은 리포에 둔다"는 사용자 선호와 충돌한다. 채팅에서 대안을 제시했다: 발견을 스킬 형태의 디렉터리로 두고 description으로 필요할 때 로드되게 한다.
- ~~D3-a, 사용자에게 묻는다: 옛 wiki는 왜 멈췄나.~~ 위 답변으로 닫음. 구조가 엉켜서인지, 유지 비용 때문인지, 쓸 일이 없어서인지. "컴파일 층이 필요한가"의 판정이 이 답에 달려 있다.
- **D3-b, 사용자에게 묻는다: 지금 `~/Documents/wiki`(raw, note, rules, 손으로 쓴 `무제*.md`)는 무엇을 위해 쓰고 있나.** 새 설계가 이것을 대체하는지, 이것 위에 얹히는지가 달라진다.
- ~~S2~~ 라운드 3에서 처리했다.
- **(참고용으로 남긴 옛 S2 설명)** 이 사용자가 옛 wiki를 실제로 어떻게 썼는지를 내용 없이 세는 조회다. 예: `git -C ~/Documents/wiki_deprecated log --name-only --format=`를 최상위 디렉터리별로 센 수, `~/.claude/projects/*/*.jsonl`에서 `wiki-query`·`wiki-record`·`wiki-collect` 호출 횟수. 이 조회가 설계 줄 "수요에서 출발"과 "소스 두 종류"를 판정한다.
- **D-b.** 30일 넘게 이어진 31곳과 멈춘 62곳의 스키마 파일을 비교한다. 검사기 강제, 세션 이월 층, 스테이징이 생존과 관련 있는지 보는 것이다. 표본이 작고 스키마는 명세라서 우선순위가 낮다.
- **스테이징 대안.** 에이전트가 쓰는 곳과 사람이 승격시키는 곳을 나눌지는 근거로 판정되지 않았다.
