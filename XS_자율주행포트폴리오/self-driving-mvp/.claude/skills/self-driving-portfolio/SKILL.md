---
name: self-driving-portfolio
description: "자율주행 포트폴리오 파이프라인을 실행한다. (1) '자산배분 돌려줘', '포트폴리오 만들어줘' 요청 시, (2) CMA부터 IC 표결까지 한 사이클을 수행할 때, (3) '메타 리뷰', '지시문 점검' 등 사이클 사후 검토 요청 시 사용."
---

# self-driving-portfolio — 오케스트레이터

7개 에이전트를 한 사이클로 엮는다. **누가 언제 어떤 순서로 협업하는가**를 정의한다.

## 전제

- `ips.md`가 이 파이프라인의 헌법이다. 실행 전 반드시 읽는다.
- `data/panel_monthly.csv`가 있어야 한다. 없으면 `fetch_data.py`를 먼저 돌린다.
- 산출물은 `runs/{YYYY-MM-DD}/`에 쌓인다. 사이클마다 폴더가 하나 생긴다.

## 실행 순서

실행 모드는 **하이브리드**다. 2단계는 팬아웃(병렬), 나머지는 파이프라인(순차).

| 단계 | 에이전트 | 패턴 | 산출 |
|---|---|---|---|
| 0 | `ips-guardian` | — | 제약 로드 (다른 단계가 호출) |
| 1 | `cma-builder` | 파이프라인 | `cma.json` |
| 2 | `alloc-mvo` · `alloc-bl` · `alloc-riskparity` | **팬아웃** | `alloc_*.json` |
| 3 | `ic-critic` | **팬인** + 생성-검증 | `ic_vote.json` |
| 4 | `meta-reviewer` | 파이프라인 | `meta_review.json` |

```bash
RUN=$(date +%Y-%m-%d)
.venv/bin/python scripts/cma.py         "$RUN"
.venv/bin/python scripts/alloc_mvo.py   "$RUN"
.venv/bin/python scripts/alloc_bl.py    "$RUN"
.venv/bin/python scripts/alloc_rp.py    "$RUN"
.venv/bin/python scripts/ic_critic.py   "$RUN"
.venv/bin/python scripts/meta_review.py "$RUN"
```

## 데이터 전달 프로토콜

에이전트는 서로에게 값을 넘기지 않는다. **모두 `runs/{날짜}/`의 JSON을 통해서만** 주고받는다.
이유는 감사 가능성이다 — 어느 단계의 무엇이 다음 단계에 들어갔는지 파일로 남는다.
IPS 7.2항("근거를 남기지 않은 안은 무효")이 이 설계를 요구한다.

## 에러 핸들링

| 상황 | 처리 |
|---|---|
| 배분 에이전트 1개 실패 | 나머지로 표결을 진행하고, 실패 사실을 `ic_vote.json`에 남긴다 |
| 배분 에이전트 전부 실패 | 사이클을 중단한다. 직전 사이클 결과를 재사용하지 않는다 |
| 모든 후보가 IPS 위반 | `winner: null`로 두고 사람에게 escalate |
| CMA 예측오차가 과대 | 중단하지 않는다. `meta-reviewer`가 다음 사이클 제안으로 남긴다 |

## 사람의 개입 지점

1. **집행 승인** — 이 파이프라인의 산출은 권고안이다(IPS 7.1항).
2. **지시문 개정** — `meta-reviewer`의 제안은 사람이 검토한 뒤에만 반영한다(IPS 7.4항).
3. **정책 변경** — `ips.md` 수정은 에이전트의 권한이 아니다.
