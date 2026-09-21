# W6 특별세션 SS2 IC 케이스 데이터 사전 (기준일 2026-09-21)

케이스 문서·덱·이 데이터만으로 심의가 끝나도록 만든 교육용 데이터셋이다. 공시 수치와 교육용 가정은 모든 표에서 `is_assumed` 열(0 = 공시·의결·통계 수치, 1 = 교육용 가정)로 구분한다. 교육용 가정은 학생이 `w6ss2_build.py` 상단 상수에서 바꾸어 판정 결과가 어떻게 달라지는지 확인하는 것이 실습의 일부다.

## 실행 순서

```
python w6ss2_build.py      # CSV 6개 생성 (7자산 일간 모의 패널 · 국민연금 2026 스냅샷 · 4기관 프로파일)
python w6ss2_compute.py    # 제1호 조건 ①~④ · 제2호 기관별 지표 계산 → w6ss2_results.json, compute_log.txt
```

필요 패키지: numpy, pandas. 실제 시계열로 다시 돌리려면 아래처럼 받아 `fml_w6ss2_panel_daily_sim.csv`와 같은 열 이름(`<자산코드>_ret`, 일간 단순수익률, `month_id`)으로 넣는다. 국고채는 KOSEF 국고채10년(148070.KS), 국내주식은 KOSPI 지수(^KS11) 또는 EWY, 해외 자산은 ETF 프록시다. 코스피 일평균 거래대금은 KRX 정보데이터시스템에서 월별로 받는다.

```
import yfinance as yf
tick = {"eq_kr": "^KS11", "eq_dm": "URTH", "eq_em": "EEM", "bond_ktb": "148070.KS", "bond_gl": "BNDX", "reit": "VNQ", "cmdty": "DBC"}
px = yf.download(list(tick.values()), start="2012-01-01")["Close"].rename(columns={v: k for k, v in tick.items()})
ret = px.pct_change().dropna(); ret.columns = [f"{c}_ret" for c in ret.columns]
ret["month_id"] = (ret.index.year - ret.index.year[0]) * 12 + ret.index.month - ret.index.month[0]
ret.reset_index().rename(columns={"Date": "date"}).to_csv("fml_w6ss2_panel_daily_sim.csv", index=False)
```

## 파일과 열

### fml_w6ss2_params.csv — 파라미터 (공시/가정 구분)

| 열 | 정의 |
|---|---|
| key | 파라미터 이름 (`cvar_limit_pct`, `saa_band_eq_kr`, `rebal_cap_new_bp`, `part_cash`, `max_days` …) |
| value | 값 |
| meaning | 뜻 |
| is_assumed | 0 공시 · 1 교육용 가정 |

공시 값: 2025년 말 적립금 1,458조 · 2026년 6월 말 1,866조(상반기 수익률 27.22%, 국내주식 107.37%), 위험한도 CVaR(α=0.05) ≥ −15%(기금운용지침 제6조의2), 기준포트폴리오 위험자산 65%, SAA 허용범위 국내주식 ±3.0 · 국내채권 ±7.0 · 해외주식 ±4.0 · 해외채권 ±0.5%p(별표 1, 2024.5.31), TAA 국내주식 ±2.0, 2026.5.28 국내주식 SAA 한시 확대(언론 추정 ±6%p), 리밸런싱 실행 한도 월 50bp·10영업일(2026.1~6) → 월 25bp·20영업일(2026.7~), 코스피 일평균 거래대금 2025년 16.9조 · 2026년 2월 32.2조 · 5월 48.0조, 코스피200 야간선물 일평균 16.7조(2026.5).

교육용 가정: 시장충격 계수 η 0.5, 현물 참여율 5%, 선물 참여율 20%, 코스피200 선물 정규장 일평균 30조, 임계(20 거래일 · 순 프리미엄 > 0 · |t| ≥ 2), 안 B 총 위험자산 밴드 ±2%p, 두 자산 CMA(위험 8.0/15.0 · 안전 3.0/4.5 · ρ 0.1 — W6 케이스와 동일), NPS 연간 순현금흐름 +0.75%.

### fml_w6ss2_panel_daily_sim.csv — 7자산 일간 모의 패널 (교육용, 20년 5,040일)

| 열 | 정의 | 단위 |
|---|---|---|
| date | 거래일(달력은 편의상 붙인 것) | YYYY-MM-DD |
| eq_kr_ret · eq_dm_ret · eq_em_ret · bond_ktb_ret · bond_gl_ret · reit_ret · cmdty_ret | 국내주식 · 선진주식 · 신흥주식 · 국고채 · 글로벌채권 · 상장 부동산 · 원자재의 일간 단순수익률 | 소수 |
| month_id | 월 번호(0~239) — 21거래일 = 1개월 | — |

설계: 월간 수익률을 대각 VAR(1)로 만들고(자산별 AR(1) φ — 국내주식 −0.10 · 선진 +0.02 · 신흥 −0.15 · 국고채 +0.12 · 글로벌채권 +0.08 · REIT −0.13 · 원자재 +0.05, 충격 상관은 `CORR`), 각 달을 21일로 나눠 합이 0인 일간 잡음을 더했다(월간 합은 설계값 그대로). 난수 시드는 설계 범위(신흥 t ≤ −2.3 · REIT t ≤ −2.0 · 국내주식 t ∈ [−2.0, −1.2] · 선진 |t| < 0.8 · 국고채 t ≥ 1.5)에 드는 첫 시드로 고정한다(`seed`). 240개월로도 φ −0.10의 t가 −1.6에 그친다는 사실 자체가 질문 ①의 소재다.

### fml_w6ss2_assets.csv — 자산 설계값과 비용 (교육용)

| 열 | 정의 |
|---|---|
| code · name | 자산코드 · 이름 |
| mu_pct · sigma_pct · phi | 설계 연 기대수익 · 연 변동성 · 월간 AR(1) φ |
| spread_bp · dvol_bp | 왕복 스프레드·수수료(bp) · 일 변동성(bp) — 시장충격 계산용 |
| adv_trn_krw | 해당 시장 일평균 거래대금(조원) — 국내주식만 공시(2026.5 48조), 나머지는 교육용 가정 |
| nps_class · w_nps · is_risk | 국민연금 자산군 매핑 · 2026년 말 목표비중의 7자산 분할(교육용) · 위험자산 여부 |
| yf_ticker | 실제 자료 프록시 티커 |

### fml_w6ss2_nps_snapshot.csv — 국민연금 2026 (공시)

| 열 | 정의 |
|---|---|
| nps_class · name | 자산군 |
| target_2026_jan_pct · target_2026_pct · target_2027_pct | 2026년 말 목표(1월 확정 · 5.28 조정) · 2027년 말 목표 |
| actual_2025_12_pct · actual_2026_03_pct · actual_2026_05_pct · actual_2026_06_pct · actual_2026_06_trn | 실제 비중(%) · 6월 말 금액(조원) |
| saa_band_pp · saa_band_temp_pp · taa_band_pp | 지침 별표 1 SAA 허용범위 · 2026.5.28 한시 확대(언론 추정) · TAA 허용범위 |

### fml_w6ss2_kospi_2026.csv — 코스피와 국민연금 국내주식 비중 (공시)

| 열 | 정의 |
|---|---|
| date · kospi_close | 주요 시점 종가(6.19는 장중 고점) |
| nps_kr_eq_pct | 그 시점의 국민연금 국내주식 비중(7.7 값은 언론 추정, is_assumed = 1) |

### fml_w6ss2_institutions.csv — 제2호 4기관 프로파일

| 열 | 정의 |
|---|---|
| code · name | NPS · KIC · SWF(한국판 전략형 국부펀드, KIC 전략투자계정) · UNIV(H대 발전기금, 가상) |
| aum_trn_krw | 자산(조원) — NPS 2026.6 말 1,866 · KIC 2025년 말 2,320억 달러(환율 1,435원) · SWF 초기 자본금 20조(2027 가동 계획) · UNIV 0.5 |
| liquid_market · adv_trn_krw | 리밸런싱이 닿는 시장과 그 일평균 거래대금(조원) — SWF는 비상장 지분이라 0 |
| w_eq · w_bond · w_alt · illiquid_share | 배분과 비유동 비중 — NPS는 공시, 나머지는 교육용 가정 |
| net_flow_pct | 연간 순현금흐름 ÷ 자산(%) — NPS +0.75(교육용 추계) · KIC 0 · SWF 0 · UNIV −3(지출 5% − 기부 2%) |
| risk_limit · deriv_access | 위험한도의 존재 · 지수선물 오버레이 접근(1/0) |

## w6ss2_compute.py 가 계산하는 것

- 제1호 조건 ① 자산군별 월간 AR(1) φ·t와 분산비 VR(12); 조건 ② 규칙별(B&H · 캘린더 일/주/월/분기/반기/연 · 밴드 ±2/3/5/6 · 안 A/B/C) 분산수익 DR = g_port − Σw·g_i, 회전율, 비용(NPS 규모 = 스프레드 + 제곱근 시장충격, 소형 = 스프레드만), 순 프리미엄, 위험자산 드리프트, CVaR 한도 초과일; 조건 ③ 2026.6 공시 갭 시나리오별 복원 거래일(월 25bp 한도 · 현물 5% 참여 · 선물 20% 참여); 조건 ④ 두 자산 CMA 의 CVaR95 곡선과 위험자산 상한 w_max, 2026.6 실제 드리프트의 CVaR, 패널 B&H 드리프트 분포. 안 B의 밴드 폭 민감도.
- 제2호 기관별 실행일수(1%p · 3%p), 현금흐름 용량(½σ 임계), 비유동 비중, 자기 규모에서의 후보 규칙(NPS 규칙 · 월 복원 · 분기 복원 · 밴드 ±3 월 · 밴드 ±5 분기) 순 프리미엄과 실행 가능성 → 규칙표와 안 A(단일 규칙) 성립 여부.

결과는 `w6ss2_results.json`(구조화)과 `compute_log.txt`(읽는 용)에 남는다.
