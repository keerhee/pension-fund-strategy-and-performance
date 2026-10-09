# 자율주행 포트폴리오 — 예시 MVP (가상 기금 KFP)

BAF.60080 특강 XS 팀 프로젝트의 **제출물 예시**다. 이 폴더 그대로가 팀이 내는 zip의 모양이다.
Ang·Azimbayev·Kim(2026)의 에이전트 구조를 13개 에이전트로 줄여, 2022.9~2025.7을 분기마다 다시 결정했다.

## 채점자: 이것만 하면 된다

1. zip을 푼다.
2. **맥은 `start.command`, 윈도는 `start.bat`을 더블클릭한다.** 처음 한 번은 파이썬 패키지를 설치한다(1~2분, 파이썬 3.10 이상 필요).
3. 브라우저에 **채점 콘솔**(http://localhost:8765)이 열린다.

| 탭 | 하는 일 |
|---|---|
| 개요 | 성과·분기별 결정·기각안의 사후 성과 |
| 분기 보기 | IC 보고서·CIO 결정·감사 기록. **[이 분기 다시 계산]** → 제출본과 숫자 대조 |
| 공개 점검 T1~T8 | **[전체 실행]** — 약 10초 |
| 라이브 점검 L1~L3 | IPS 바꿔 실행 · 가상 충격 · 결함 주입 (발표 당일) |
| 문서 | IPS · 사전 등록 · CHANGELOG · CIO 개입 기록 · 의결문 |

파이썬이 없으면 `dashboard.html`을 브라우저로 열어 같은 화면을 읽기 전용으로 본다.
macOS가 "확인되지 않은 개발자" 경고를 띄우면 `start.command`를 우클릭 → 열기.

## 무엇이 다시 계산되고 무엇이 재생되는가

| 부분 | 채점 콘솔에서 |
|---|---|
| CMA · 최적화 · 위험 지표 · 적격 심사 · 투표 점수 · 성과 | **다시 계산** — 코드가 계산하므로 제출본과 소수 6자리까지 같아야 한다 |
| CIO 결정 · 변경 승인 | **입력으로 재생** — 사람이 적은 `data/cio_decisions.csv` · `data/approvals.csv` |
| 에이전트의 판단 문장(매크로 해석·리서치 메모·검토 의견·투표 순위) | **녹화본 재생** — 이 예시는 규칙 기반 대역이라 재현된다. LLM 에이전트를 쓰는 팀은 문장이 매번 달라질 수 있으므로 양식과 근거 기록만 본다 |

LLM 라이브 실행은 비용과 비결정성 때문에 채점자가 하지 않는다. 팀이 발표 때 Claude Code로 시연한다(`CLAUDE.md`).

## 결과 요약

| 경로 | 연율 수익 | 변동성 | 최대낙폭 |
|---|---|---|---|
| 채택 경로(CIO) | 7.90% | 9.61% | −7.3% |
| 60/40 (SPY·IEF) | 11.82% | 11.26% | −7.3% |
| MVO 계속 보유 (4개 분기 IPS 기각) | 11.57% | 8.61% | −5.3% |

- 자동 기각 8건(MVO 4 · 적대적 분산자 4) — 모두 유효 종목 수 4.0 미만
- CIO 개입 3회 — 조건부 승인 1, 반려 2 (`INTERVENTIONS.md`)
- 변경 제안 4건 — 반영 0, 롤백 1, 반려 3 (`CHANGELOG.md`)
- 공개 점검 T1~T8 전부 통과 (`reports/selfcheck.md`)
- 도입 의결: **조건부 승인** — 6개월 분석 전용 병행 운영 (`reports/resolution.md`)

## 구조

```
start.command / start.bat   채점 콘솔 실행 (더블클릭)
dashboard.html              정적 보기 (파이썬 없이)
ips.md                      정책 — 행동을 바꾸려면 코드가 아니라 이것을 고친다 (보호 파일)
PREREG.md                   사전 등록표
CHANGELOG.md                변경 제안 → 승인·반려 → 테스트 → 승격·롤백
INTERVENTIONS.md            CIO 결정 기록
CLAUDE.md                   Claude Code 라이브 모드 규칙
.claude/agents/             에이전트 13개 정의
.claude/skills/             스킬 7개 (보호 파일)
config/                     파라미터 (보호 파일)
data/                       ETF 월간 수익률 · FRED 매크로 · 사람의 결정(cio_decisions.csv, approvals.csv)
sdp/                        계산 코드 — 하네스·에이전트·오케스트레이터·점검·콘솔
runs/{YYYY-MM}/             분기별 실행 증거 — cma · 배분안 · 적격 · CRO · 검토 · 투표 · IC 보고서 · CIO 결정 · trace.jsonl
reports/                    성과 · 자가 점검 · 의결문
```

## 한 분기에 일어나는 일

```
macro-agent → cma-builder → research-agent
 → PC 6개(동일가중·역변동성·최소분산·최대 샤프·ERC·적대적 분산자)
 → ips-guardian(자동 기각) → cro-agent → 상호 검토 → 수정 보르다 투표
 → meta-reviewer(직전 분기 사후 평가) → ic-agent → CIO(사람) → 변경 처리(킬스위치)
```

## 터미널을 쓰는 경우 (팀원용)

```
python -m sdp serve        채점 콘솔
python -m sdp all          전 구간 다시 실행 (약 15초)
python -m sdp quarter 2024-11
python -m sdp check        공개 점검 T1~T8
python -m sdp report       성과 보고서·대시보드 갱신
```

## 팀 제출 때 README에 넣을 표 (견본)

| 구분 | 예시 MVP | 우리 팀 | 왜 바꿨나 |
|---|---|---|---|
| 기금 · IPS | 가상 기금 KFP (실질 4.5%, 변동성 10%) | (예) 대학 발전기금 — 지출률 5%, 실질 원금 보전 | |
| 유니버스 · 데이터 | ETF 11개 · FRED 6개 | | |
| 판단 부분 | 규칙 기반 대역 | (예) 리서치·검토·IC 보고서를 Claude Code 에이전트로, 녹화본 재생 | |
| PC 에이전트 | 6개 | (예) + LLM 뷰 블랙-리터만 | |
| 감독 장치 | 자동 기각 · 킬스위치 · 날짜 검사 | (예) + 국면 전환 시 학습 정지 | |

## 데이터

데이터 사전은 `data/DATA.md`, 내려받기는 `python data/fetch_data.py`. ETF 11개 월간 총수익률(과정 저장소 `self-driving-mvp/data/panel_monthly.csv`, yfinance)과 FRED 월평균(DGS3MO, DGS10, T10Y2Y, CPIAUCSL, UNRATE, BAA10Y). 물가·실업률은 발표 지연 1개월을 반영해 읽는다(`sdp/data.py`).
