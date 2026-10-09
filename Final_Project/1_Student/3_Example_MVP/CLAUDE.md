# 자율주행 포트폴리오 — 예시 MVP (Claude Code 라이브 모드 안내)

## 하네스 규칙 (반드시 지킨다)
1. **숫자는 코드로만.** 기대수익률·공분산·최적화·위험 지표·투표 점수는 `python -m sdp …`가 만든다. 에이전트가 숫자를 계산하거나 json의 숫자를 고치지 않는다.
2. **보호 파일.** `ips.md`, `config/*.json`, `.claude/skills/**`는 직접 고치지 않는다. 수정은 `runs/{as_of}/proposals_change/`에 제안서로만 남긴다. 반영은 CIO 승인(`data/approvals.csv`)과 테스트 통과 뒤 하네스가 한다.
3. **시점 잠금.** `as_of` 이후 데이터·사건을 쓰지 않는다. 하네스가 에이전트 문서의 날짜를 검사해 멈춘다.
4. **CIO는 사람이다.** IC 보고서까지만 만들고 멈춘다. 결정은 사람이 `data/cio_decisions.csv`에 적는다.

## 라이브 모드에서 에이전트가 하는 일
예시 MVP의 판단 문장은 규칙 기반 대역이다. 라이브 모드에서는 아래 파일을 에이전트가 다시 쓴다.

| 에이전트 | 읽는 것 | 다시 쓰는 것 |
|---|---|---|
| macro-agent | `macro.json` | `macro.md` 해석 3줄 |
| research-agent | `macro.json`, as_of 이전 자료 | `research_memo.md`, 필요하면 제안서 |
| PC 에이전트 6개 | `cro_report.json`, 다른 안 | `reviews.json`의 검토 의견, 투표 순위 |
| ic-agent | `votes.json`, `reviews.json`, `cro_report.json` | `ic_report.md` |

## 자주 쓰는 프롬프트
- "2024-11 분기를 다시 돌리고 IC 보고서를 요약해줘"
- "공개 점검 T1~T8을 돌려줘" (= `python -m sdp check`)
- "ips.md의 유효 종목 수 하한을 3.5로 바꾸면 2024-02 결론이 어떻게 되는지 임시 복사본에서 보여줘"
