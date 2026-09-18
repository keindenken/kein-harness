# kein-harness

Claude Code용 `kein` 하네스를 만드는 리포다. 설치 방법, 로딩 방식, 설계 이유처럼 사람이 읽을 설명은 README.md에 있고, 이 파일에는 여기서 작업할 때 지켜야 하는 것만 둔다.

## 무엇이 배포되는가

- `plugin/`만 설치된다. `agents/`, `dev/`, `docs/`, `.agents/`는 배포되지 않는다. 하네스가 실행 중에 쓰는 것은 `plugin/` 안에, 하네스를 만들고 검사하는 도구는 `dev/`에 둔다.
- `plugin/bin/`에는 `ocs` 하나만 둔다. 여기 있는 파일은 플러그인이 켜진 모든 프로젝트에서 Bash PATH에 올라간다. 서브커맨드는 `plugin/libexec/ocs-<name>`으로 만들고, 첫 `#:` 주석 줄이 `ocs help`의 요약이 된다.
- 개발용 명령은 `dev/libexec/<name>`에 두고 `dev/kein-dev <name>`으로 부른다. `ocs`에서 `dev/`를 참조하지 않는다.

## 에이전트 역할

- 역할 본문은 `agents/`, tier와 sandbox_mode는 `agents.json`에서 고친다. `plugin/agents/`는 렌더 결과이므로 직접 고치지 않는다.
- 고친 뒤에는 `dev/kein-dev render-agents`로 다시 렌더하고 `dev/kein-dev check-agents`로 드리프트가 없는지 확인한다.
- 프롬프트 산문에 모델 이름을 쓰지 않는다. 모델은 `agents.json`의 `tier`가 정한다.

## 상태와 기록

- 런 상태와 작업 산출물은 `ocs state-dir`이 가리키는 `.agents/kein/` 아래에 둔다. `runs/`는 임시이고, `requirements/`, `plans/`, `handoff/`는 남기는 기록이다.
- `docs/`는 참고 문서용이다. 스킬별 측정 결과는 `docs/skills/<skill>/YYMMDD-<주제>.md`, 보류한 일은 같은 폴더의 `open.md`, 스킬에 묶이지 않는 보류 건은 `docs/open-threads.md`에 둔다.

## 스킬과 프롬프트 개선

- 규칙을 더하거나 뺄지는 `/kein:deliberate`로 판단하고, 문구를 런 결과로 바꿀지는 `/sharpen`으로 판정한다. 둘 다 편집은 하지 않는다.
- eval은 `dev/kein-dev eval --case <name>`으로 돌리고, 케이스는 `dev/eval/cases/`에 있다.
- eval 실행 디렉터리는 허브의 `../eval/`에 생긴다. 리포 밖이어야 이 파일이 arm에 들어가지 않기 때문이다. 허브나 그 상위에 CLAUDE.md가 생기면 eval이 실행을 거부한다.

## 명령

```sh
ocs help                                         # 에이전트가 작업 중에 쓰는 CLI
dev/kein-dev help                                # 하네스 개발용 명령
claude plugin validate plugin --strict           # 플러그인 매니페스트 검사
```

버전을 올릴 때는 `bump-version` 스킬로 `plugin/.claude-plugin/plugin.json`과 `.claude-plugin/marketplace.json`을 함께 올린다.

## 커밋

`feat(execute): ...`처럼 conventional prefix 뒤에 무엇이 달라졌는지를 문장으로 쓴다.

커밋은 요청을 기다리지 않는다. 한 작업 단위가 검증까지 끝나면 에이전트가 판단해 커밋하고, 이 리포에서는 이 줄이 "요청이 있을 때만 커밋한다"는 기본 지침보다 우선한다. push는 하지 않는다. push는 버전을 올릴 때 `bump-version` 스킬 안에서만 한다.
