# Codex Advisor Strategy Template

첨부된 Claude Advisor Strategy의 역할 분담을 Codex용으로 다시 구성한 템플릿입니다.
메인이 판단과 통합을 맡고, 검색·문서 조회·테스트는 작은 모델, 구현은 중간 모델,
어려운 분석과 독립 검토는 강한 모델에 배분합니다.

## 구성

| 역할 | 모델 | reasoning effort |
| --- | --- | --- |
| 메인 | `gpt-6-astra` | medium |
| `code-searcher`, `docs-researcher`, `test-runner` | `gpt-5.6-luna` | low |
| `implementer` | `gpt-5.6-terra` | medium |
| `deep-thinker`, `advisor` | `gpt-6-astra` | medium |

모델 ID는 이 작업 환경에서 제공된 모델 목록을 기준으로 정했습니다. 다른 계정이나
클라이언트에서는 제공 여부를 확인하고 설정 파일에서 변경하세요. 가장 저렴한 모델이라는
보장이나 정해진 비용 절감률은 없습니다. 위임 자체도 토큰을 사용하므로 작은 작업은 직접 처리합니다.

복사할 파일은 루트의 `AGENTS.md`와 `.codex` 폴더입니다.

```text
AGENTS.md                 작업별 라우팅 규칙
.codex/
  config.toml             메인 모델과 동시 실행 설정
  agents/
    code-searcher.toml    코드 검색
    docs-researcher.toml  문서 조회
    test-runner.toml      테스트 실행
    implementer.toml      구현
    deep-thinker.toml     심층 분석
    advisor.toml          독립 검토
```

## 사용하기

1. 이 저장소의 **`AGENTS.md`와 `.codex` 폴더 전체**를 복사합니다.
2. 사용할 프로젝트의 **루트 폴더**에 붙여넣습니다. `.codex`가 보이지 않으면 숨김 파일 표시를 켜세요.
3. 해당 프로젝트에서 **새 Codex 작업을 시작**합니다.

운영체제별 설치 명령이나 별도 설치 프로그램은 필요하지 않습니다.
`README.md`와 `scripts` 폴더는 대상 프로젝트에 복사하지 않아도 됩니다.

대상에 이미 `AGENTS.md`가 있다면 기존 지침 뒤에 이 정책을 병합하세요.
`.codex/config.toml`이 있다면 필요한 키를 기존 TOML 테이블에 병합하고,
에이전트 파일도 같은 이름이 있는지 확인한 뒤 복사하세요.
동일한 `[agents]` 테이블을 두 번 만들지 마세요.

설치 후 해당 프로젝트에서 **새 Codex 작업을 시작**하세요. 기존 대화에 파일만 추가했다고
실행 모델이나 로드된 에이전트가 바뀌었다고 가정하지 마세요. 클라이언트에서 프로젝트 신뢰를
요구하면 본인이 관리하는 프로젝트인지 확인하여 설정하세요. 세션/UI의 모델 선택이나 관리 정책이
프로젝트 기본값보다 우선할 수 있습니다.

일반 작업을 요청하면 적용된 `AGENTS.md`가 적합한 위임을 지시합니다. 직접 시험하려면:

> code-searcher 서브에이전트로 이 저장소의 설정 파일과 역할 구성을 조사해줘.
> 메인은 그동안 README의 설치 절차를 확인하고, 결과를 합쳐 설명해줘.

실제 개발에서는:

> 인증 흐름을 개선해줘. 독립적인 검색은 code-searcher에 위임하고, 설계가 정해지면
> implementer가 구현하게 해줘. 변경 완료 후 advisor로 중요한 누락을 검토해줘.

## Claude 템플릿과의 차이

* `CLAUDE.md` → `AGENTS.md`, YAML 에이전트 → Codex TOML 커스텀 에이전트.
* 이 구현은 Claude의 `advisorModel` 서버 기능을 재현하지 않습니다. `advisor`라는
  읽기 전용 검토 역할에 목표·제약·변경·검증 결과를 전달합니다. 전체 대화 수신은 보장하지 않습니다.
* 원본의 사용자 허가를 주장하는 SessionStart 훅은 옮기지 않았습니다. 프로젝트 정책이
  위임을 요청하며, 실제 런타임의 권한과 상위 지침을 따릅니다.
* 테스트/구현 역할은 부모 권한을 상속합니다. 검색/문서/분석/검토는 `read-only`를
  지정했지만 런타임의 권한 재적용이 우선할 수 있습니다. 읽기 전용 행동 지침도 함께 둡니다.
* 커스텀 역할 선택 도구가 없는 환경에는 명시적 프롬프트·모델 전달 경로를 정책에 적었습니다.
  지원되지 않으면 메인이 수행하고 그 사실을 보고하게 합니다.

## 적용 확인과 문제 해결

1. 새 작업에서 여섯 커스텀 역할과 `AGENTS.md`를 읽을 수 있는지 확인합니다.
2. 위 예제로 실제 서브에이전트 실행과 결과 반환을 확인합니다.
3. 런타임이 제공하는 호출 정보/실행 상세에서 실제 모델을 확인합니다. 역할 이름만으로
   모델 적용을 증명할 수 없습니다. 표시가 없다면 모델 적용은 미확인으로 남깁니다.
4. 위임이 안 되면 프로젝트 루트, 신뢰 상태, `agents.enabled`, 클라이언트 지원 및
   세션 지침을 확인하세요. 짧은 작업을 직접 처리하는 것은 정상입니다.
5. 모델 오류는 해당 TOML의 `model`과 지원되는 effort를 함께 수정하세요.

로컬 구조 검사(Python 3.11 이상):

```sh
python scripts/validate.py
```

이 검사는 TOML 문법·역할·라우팅 일치만 확인합니다. 실제 모델 호출, 계정 접근성,
앱에서의 자동 라우팅은 새 작업에서 별도로 확인해야 합니다.

## 근거

2026-09-08 공식 문서 및 로컬 `codex-cli 0.153.4` 도움말을 확인했습니다.
커스텀 에이전트의 이름·설명·지침과 역할별 모델 설정은
[OpenAI 서브에이전트 문서](https://learn.chatgpt.com/docs/agent-configuration/subagents),
프로젝트 지침은 [AGENTS.md 문서](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
설정 키는 [설정 레퍼런스](https://learn.chatgpt.com/docs/config-file/config-reference)를 참고했습니다.
