#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W6 특별세션 SS2 IC 케이스 교육용 데이터 생성 (기준일 2026-09-21).

제1호  국민연금 기금의 리밸런싱 규칙 — 밴드 폭 · 점검 주기 · 실행 한도 · 실행 수단 (안 A·B·C)
제2호  빈도·밴드의 기관별 차등 — 규모 · 유동성 · 현금흐름 · 부채 구조가 다른 4기관에 같은 규칙을 쓸 것인가

공시 수치(is_assumed=0)와 교육용 가정(is_assumed=1)을 열로 구분한다. 교육용 가정은 이 파일의
상단 상수를 바꾸면 되고, 바꾸면 w6ss2_compute.py 의 판정 결과가 달라진다 — 그것이 실습의 일부다.

생성 파일
  fml_w6ss2_params.csv          판정 임계 · CMA · 참여율 · 기준일 (공시/가정 구분)
  fml_w6ss2_panel_daily_sim.csv 7자산 일간 모의 패널 20년(5,040일) — 월간 AR(1) φ · 상관 · σ 를 설계해 만든 교육용 패널
  fml_w6ss2_assets.csv          자산코드 · 이름 · 설계 μ·σ·φ · 거래비용(스프레드) · 시장 일평균 거래대금 · NPS 자산군 매핑
  fml_w6ss2_nps_snapshot.csv    국민연금 2026 — 목표비중 · 실제비중 · 허용범위 · 실행 한도 · 거래대금 (공시)
  fml_w6ss2_kospi_2026.csv      코스피 주요 시점 종가와 국민연금 국내주식 비중 (공시)
  fml_w6ss2_institutions.csv    제2호 4기관 프로파일 — 규모 · 배분 · 거래대금 · 현금흐름 · 비유동 비중 · 위험한도

실제 자료로 바꾸려면 data_dictionary.md 의 yfinance · FRED 코드로 같은 열 이름의 일간 패널을 만들어 넣는다.
"""
import os
import numpy as np, pandas as pd

ASOF = "2026-09-21"
OUT = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# 0. 공시 수치 (is_assumed = 0)
# ─────────────────────────────────────────────────────────────────────────────
FUND_2025 = 1458.0            # 조원, 2025년 말 적립금 (국민연금 통계) — W6 케이스와 같은 값
FUND_2026H1 = 1866.0          # 조원, 2026년 6월 말 적립금 (기금운용본부 · 2026.8.28)
RET_2025, RET_2026H1 = 18.82, 27.22            # 기금 수익률 % (2025 연간 · 2026 상반기)
RET_KR_EQ_2025, RET_KR_EQ_2026H1 = 82.44, 107.37
KR_EQ_2025 = (264.0, 18.1)    # 2025년 말 국내주식 (조원, 비중 %) — KB 리서치 인용 공시 재구성
KR_EQ_2026_03 = (320.9, 21.0) # 2026.3 말
KR_EQ_2026_05 = (543.6, 29.4) # 2026.5 말 (1,848.7조 중)
KR_EQ_2026_06 = (543.2, 29.1) # 2026.6 말
FX_EQ_2026_06 = (661.1, 35.4); ALT_2026_06 = (260.9, 14.0)
TARGET_2026 = {"eq_kr": 20.8, "eq_fx": 34.7, "bond_kr": 23.1, "bond_fx": 7.4, "alt": 14.0}   # 2026년 말 목표(2026.5.28 조정)
TARGET_2026_OLD = {"eq_kr": 14.9}                                                            # 2026.1 확정 → 5.28 상향
TARGET_2027 = {"eq_kr": 20.8, "eq_fx": 35.6, "bond_kr": 21.8, "bond_fx": 7.4, "alt": 14.3}
MID_2031 = {"stock": 55, "bond": 30, "alt": 15}
SAA_BAND = {"eq_kr": 3.0, "bond_kr": 7.0, "eq_fx": 4.0, "bond_fx": 0.5}      # 기금운용지침 별표 1 (2024.5.31) ±%p
TAA_BAND = {"eq_kr": 2.0, "bond_kr": 5.0, "eq_fx": 3.0, "bond_fx": "+2.0/-4.0"}
SAA_BAND_KR_TEMP = 6.0        # 2026.5.28 한시 확대(연말 재점검) — 공식 수치 비공개, 언론 추정 ±6%p
REBAL_CAP_OLD = (50, 10)      # 월 최대 조정 bp · 영업일 (2026.1~6)
REBAL_CAP_NEW = (25, 20)      # 2026.7.1 부터 — 일 매도 약 0.225조
MORATORIUM = ("2026-01-26", "2026-06-30")
CVAR_LIMIT = -15.0            # 지침 제6조의2 CVaR(α=0.05) ≥ −15%
REF_PORT = (0.65, 0.35)       # 기준포트폴리오 위험자산 65 : 안전자산 35 (2024.5 의결)
KOSPI = [("2024-12-30", 2399.49), ("2025-12-30", 4214.17), ("2026-03-31", 5052.46), ("2026-05-22", 7847.71),
         ("2026-05-29", 8476.15), ("2026-06-19", 9385.59), ("2026-07-07", 6258.77), ("2026-09-18", 6894.23)]  # 6.19 는 장중 고점
ADV_KOSPI_2025, ADV_KOSPI_2026_02, ADV_KOSPI_2026_05 = 16.9, 32.2, 48.0   # 조원, 유가증권시장 일평균 거래대금
ADV_K200_NIGHT_2026_05 = 16.7                                             # 조원, 코스피200 야간선물 일평균 (2026.5)
KIC_AUM_BN_USD, KIC_TRAD, KIC_ALT = 2320, 78.1, 21.9                     # 2025년 말
KIC_RET_2025, KIC_RET_10Y = 13.91, 7.07
SWF = {"name": "한국판 전략형 국부펀드(KIC 전략투자계정)", "capital_trn": 20.0, "launch": "2027(계획)",
       "public_shares_trn": 16.0, "inkind_tax_shares_trn": 4.0}        # 2026.7.31 정부 발표 — 20조+α

# ─────────────────────────────────────────────────────────────────────────────
# 1. 교육용 가정 (is_assumed = 1) — 바꿔 보라
# ─────────────────────────────────────────────────────────────────────────────
SEED_BASE = 6602
N_YEARS = 20                  # 모의 패널 길이(년) — 월간 AR(1) t값이 보이려면 240개월은 있어야 한다
DAYS_PER_MONTH = 21
# 7자산 설계값 — μ·σ 는 연 %, φ 는 월간 수익률 AR(1) 계수(음수 = 평균회귀)
ASSETS = pd.DataFrame([
    # code       name                 mu   sig   phi    spread_bp  dvol_bp  adv_trn_krw   nps_class  yf_ticker
    ("eq_kr",   "국내주식(KOSPI)",     8.0, 20.0, -0.10,   10,      150,     48.0,        "eq_kr",   "^KS11 (EWY)"),
    ("eq_dm",   "선진주식(MSCI World)", 8.0, 15.0,  0.02,    8,      100,   1200.0,        "eq_fx",   "URTH"),
    ("eq_em",   "신흥주식(MSCI EM)",   9.0, 20.0, -0.15,   25,      130,    150.0,        "eq_fx",   "EEM"),
    ("bond_ktb","국고채(10년)",         3.0,  5.0,  0.12,    3,       30,     20.0,        "bond_kr", "148070.KS"),
    ("bond_gl", "글로벌채권(헤지)",     3.5,  6.0,  0.08,    8,       35,    400.0,        "bond_fx", "BNDX"),
    ("reit",    "상장 부동산(REIT)",    7.0, 18.0, -0.13,   15,      120,     30.0,        "alt",     "VNQ"),
    ("cmdty",   "원자재(선물)",         4.0, 16.0,  0.05,   10,      110,     60.0,        "alt",     "DBC"),
], columns=["code", "name", "mu_pct", "sigma_pct", "phi", "spread_bp", "dvol_bp", "adv_trn_krw", "nps_class", "yf_ticker"])
CORR = np.array([   # 충격 상관(교육용) — 순서 eq_kr eq_dm eq_em bond_ktb bond_gl reit cmdty
    [1.00, 0.60, 0.65, -0.10, 0.05, 0.50, 0.30],
    [0.60, 1.00, 0.75, -0.15, 0.10, 0.60, 0.30],
    [0.65, 0.75, 1.00, -0.10, 0.05, 0.55, 0.40],
    [-0.10, -0.15, -0.10, 1.00, 0.50, 0.10, -0.10],
    [0.05, 0.10, 0.05, 0.50, 1.00, 0.20, 0.00],
    [0.50, 0.60, 0.55, 0.10, 0.20, 1.00, 0.25],
    [0.30, 0.30, 0.40, -0.10, 0.00, 0.25, 1.00]])
# NPS 유동 7자산 비중(교육용 매핑) — 2026년 말 목표: 국내주식 20.8 · 해외주식 34.7(선진 30.0 + 신흥 4.7) · 국내채권 23.1 · 해외채권 7.4 · 대체 14.0(REIT 7 + 원자재 7)
W_NPS = {"eq_kr": 0.208, "eq_dm": 0.300, "eq_em": 0.047, "bond_ktb": 0.231, "bond_gl": 0.074, "reit": 0.070, "cmdty": 0.070}
RISK_ASSETS = ["eq_kr", "eq_dm", "eq_em", "reit", "cmdty"]      # 위험자산 비중 = 이 다섯의 합 (교육용 정의: 목표에서 69.5%)
MU_RISK, MU_SAFE, SIG_RISK, SIG_SAFE, RHO = 8.0, 3.0, 15.0, 4.5, 0.10   # 두 자산 CMA — W6 케이스와 동일(기준포트폴리오 65:35 판정용)
IMPACT_ETA = 0.5              # 시장충격 계수 — 충격(bp) = η · 일변동성(bp) · sqrt(주문/일평균 거래대금)
PART_CASH = 0.05              # 현물 참여율(일평균 거래대금 대비) — 조건 ③
PART_FUT = 0.20               # 선물 참여율(선물 일평균 거래대금 대비)
ADV_K200_FUT_TOTAL = 30.0     # 조원, 코스피200 선물 정규장 일평균 거래대금(교육용 가정 — 야간선물만 16.7조 공시)
MAX_DAYS = 20                 # 조건 ③ 임계 — 밴드 복원 거래를 20 거래일(한 달) 안에 끝내야 한다
NET_MIN_BP = 0.0              # 조건 ② 임계 — 순 프리미엄(DR − 비용) > 0
NET_TOL_BP = 5.0              # 최적 규칙과의 허용 격차(bp) — 이 안에 들면 동등
T_MIN = 2.0                   # 조건 ① 임계 — AR(1) φ의 |t| ≥ 2
RISK_BAND_TOTAL = 2.0         # 안 B 의 총 위험자산 밴드 ±%p (오버레이로 복원)
NPS_NET_FLOW_PCT = 0.75       # NPS 연간 순현금흐름 / 적립금 % (2026 보험료 70조 − 급여 56조 ≈ +14조, W6 교육용 추계)
# 제2호 4기관 (교육용 가정은 is_assumed 열에 표시)
INSTITUTIONS = [
    # code  name  aum_trn_krw  liquid_market  adv_trn_krw  w_eq  w_bond  w_alt  illiquid_share  net_flow_pct  risk_limit  deriv_access  is_assumed(프로파일 층위)
    ("NPS", "국민연금기금", FUND_2026H1, "코스피(국내주식)", ADV_KOSPI_2026_05, 0.641, 0.215, 0.140, 0.14, NPS_NET_FLOW_PCT, "CVaR95 −15%(지침)", 1, 0),
    ("KIC", "한국투자공사(외환보유액 위탁)", round(KIC_AUM_BN_USD * 0.1435, 0), "글로벌 주식(미국)", 1200.0, 0.45, 0.33, 0.22, 0.22, 0.0, "기준포트폴리오 위험예산(교육용)", 1, 1),
    ("SWF", SWF["name"], SWF["capital_trn"], "비상장 정책지분 + 국내 첨단산업 지분", 0.0, 0.95, 0.00, 0.05, 0.95, 0.0, "미정(출범 전 설계)", 0, 1),
    ("UNIV", "H대학교 발전기금(가상 · W7 케이스)", 0.5, "글로벌 ETF", 1200.0, 0.60, 0.30, 0.10, 0.10, -3.0, "유동성 하한 30% · 지출 Floor 250억", 0, 1),
]

# ─────────────────────────────────────────────────────────────────────────────
# 2. 월간 VAR(1)(대각 φ) → 일간 분해 모의 패널
# ─────────────────────────────────────────────────────────────────────────────
N_M = N_YEARS * 12
codes = ASSETS.code.tolist()
mu_m = ASSETS.mu_pct.values / 100 / 12
sig_m = ASSETS.sigma_pct.values / 100 / np.sqrt(12)
phi = ASSETS.phi.values
sig_eps = sig_m * np.sqrt(1 - phi ** 2)          # 정상 분산이 설계 σ² 이 되도록 충격 분산을 줄인다
L = np.linalg.cholesky(CORR)


def ar1_t(x):
    """월간 수익률 AR(1) 회귀 r_t = a + φ r_{t-1} 의 (φ̂, t)"""
    y, x1 = x[1:], x[:-1]
    X = np.c_[np.ones(len(x1)), x1]
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b; s2 = e @ e / (len(y) - 2)
    V = s2 * np.linalg.inv(X.T @ X)
    return float(b[1]), float(b[1] / np.sqrt(V[1, 1]))


def simulate_monthly(seed):
    r = np.random.default_rng(seed)
    R = np.zeros((N_M, 7)); prev = np.zeros(7)
    for t in range(N_M):
        eps = (L @ r.standard_normal(7)) * sig_eps
        R[t] = mu_m + phi * prev + eps
        prev = R[t] - mu_m
    return R


# 시드 탐색 — 설계 범위: EM t ≤ −2.3 · REIT t ≤ −2.0 · 국내주식 t ∈ [−2.0, −1.2] · 선진주식 |t| < 0.8 · 국고채 t ≥ 1.5
def in_design(R):
    T = {c: ar1_t(R[:, i])[1] for i, c in enumerate(codes)}
    return (T["eq_em"] <= -2.3 and T["reit"] <= -2.0 and -2.0 <= T["eq_kr"] <= -1.2 and abs(T["eq_dm"]) < 0.8 and T["bond_ktb"] >= 1.5), T


seed = None
for s in range(SEED_BASE, SEED_BASE + 4000):
    R = simulate_monthly(s); ok, T = in_design(R)
    if ok:
        seed = s; break
assert seed is not None, "설계 범위에 드는 시드를 못 찾았다 — 범위를 넓히거나 φ 를 키워라"
print(f"[패널] 시드 {seed} · 월간 AR(1) t: " + " · ".join(f"{c} {T[c]:.2f}" for c in codes))

# 일간 분해 — 월 수익률을 21일로 나누고, 합이 0 인 일간 잡음을 더한다(월간 합은 설계값 그대로)
rng = np.random.default_rng(seed + 1)
dates = pd.bdate_range(end="2026-09-18", periods=N_M * DAYS_PER_MONTH)
D = np.zeros((N_M * DAYS_PER_MONTH, 7))
for t in range(N_M):
    noise = (L @ rng.standard_normal((7, DAYS_PER_MONTH))).T * (sig_m / np.sqrt(DAYS_PER_MONTH))
    noise -= noise.mean(axis=0, keepdims=True)
    D[t * DAYS_PER_MONTH:(t + 1) * DAYS_PER_MONTH] = R[t] / DAYS_PER_MONTH + noise
panel = pd.DataFrame(D, columns=[f"{c}_ret" for c in codes]); panel.insert(0, "date", dates.strftime("%Y-%m-%d"))
panel["month_id"] = np.repeat(np.arange(N_M), DAYS_PER_MONTH)
panel.round(7).to_csv(f"{OUT}/fml_w6ss2_panel_daily_sim.csv", index=False)

A = ASSETS.copy(); A["w_nps"] = A.code.map(W_NPS); A["is_risk"] = A.code.isin(RISK_ASSETS).astype(int)
A["is_assumed"] = 1; A["asof"] = ASOF; A["source"] = "교육용 설계값(μ·σ·φ·스프레드·일변동성) · 거래대금은 2026.5 코스피 48조 공시 외 교육용 가정"
A.to_csv(f"{OUT}/fml_w6ss2_assets.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 3. 파라미터 · 공시 스냅샷 · 코스피 · 기관
# ─────────────────────────────────────────────────────────────────────────────
params = [
    ("asof", ASOF, "기준일", 0), ("fund_2025_trn", FUND_2025, "2025년 말 적립금(조원)", 0), ("fund_2026h1_trn", FUND_2026H1, "2026.6 말 적립금(조원)", 0),
    ("ret_2025_pct", RET_2025, "2025 기금 수익률 %", 0), ("ret_2026h1_pct", RET_2026H1, "2026 상반기 기금 수익률 %", 0),
    ("ret_kr_eq_2025_pct", RET_KR_EQ_2025, "2025 국내주식 수익률 %", 0), ("ret_kr_eq_2026h1_pct", RET_KR_EQ_2026H1, "2026 상반기 국내주식 수익률 %", 0),
    ("cvar_limit_pct", CVAR_LIMIT, "위험한도 CVaR(α=0.05) ≥ −15% (지침 제6조의2)", 0), ("ref_risk_share", REF_PORT[0], "기준포트폴리오 위험자산 비중", 0),
    ("saa_band_eq_kr", SAA_BAND["eq_kr"], "SAA 허용범위 국내주식 ±%p (별표 1, 2024.5.31)", 0), ("saa_band_bond_kr", SAA_BAND["bond_kr"], "국내채권 ±%p", 0),
    ("saa_band_eq_fx", SAA_BAND["eq_fx"], "해외주식 ±%p", 0), ("saa_band_bond_fx", SAA_BAND["bond_fx"], "해외채권 ±%p", 0),
    ("taa_band_eq_kr", TAA_BAND["eq_kr"], "TAA 허용범위 국내주식 ±%p", 0), ("saa_band_eq_kr_temp", SAA_BAND_KR_TEMP, "2026.5.28 한시 확대(언론 추정) ±%p", 0),
    ("rebal_cap_new_bp", REBAL_CAP_NEW[0], "월 최대 조정 bp (2026.7~)", 0), ("rebal_cap_new_days", REBAL_CAP_NEW[1], "월 영업일", 0),
    ("rebal_cap_old_bp", REBAL_CAP_OLD[0], "월 최대 조정 bp (2026.1~6)", 0), ("rebal_cap_old_days", REBAL_CAP_OLD[1], "월 영업일", 0),
    ("adv_kospi_2025", ADV_KOSPI_2025, "코스피 일평균 거래대금 2025 (조원)", 0), ("adv_kospi_2026_05", ADV_KOSPI_2026_05, "2026.5 (조원)", 0),
    ("adv_k200_night_2026_05", ADV_K200_NIGHT_2026_05, "코스피200 야간선물 일평균 2026.5 (조원)", 0),
    ("adv_k200_fut_total", ADV_K200_FUT_TOTAL, "코스피200 선물 정규장 일평균(교육용 가정, 조원)", 1),
    ("impact_eta", IMPACT_ETA, "시장충격 계수 η", 1), ("part_cash", PART_CASH, "현물 참여율", 1), ("part_fut", PART_FUT, "선물 참여율", 1),
    ("max_days", MAX_DAYS, "조건 ③ 임계 — 복원 거래 완료 거래일", 1), ("net_min_bp", NET_MIN_BP, "조건 ② 임계 — 순 프리미엄 > 0 bp", 1),
    ("net_tol_bp", NET_TOL_BP, "최적 규칙과의 허용 격차 bp", 1), ("t_min", T_MIN, "조건 ① 임계 — |t| ≥ 2", 1),
    ("risk_band_total", RISK_BAND_TOTAL, "안 B 총 위험자산 밴드 ±%p", 1),
    ("mu_risk", MU_RISK, "두 자산 CMA 위험자산 μ %", 1), ("mu_safe", MU_SAFE, "안전자산 μ %", 1), ("sig_risk", SIG_RISK, "위험자산 σ %", 1), ("sig_safe", SIG_SAFE, "안전자산 σ %", 1), ("rho", RHO, "상관", 1),
    ("n_years", N_YEARS, "모의 패널 길이(년)", 1), ("seed", seed, "패널 난수 시드(설계 범위에 드는 첫 시드)", 1),
    ("nps_net_flow_pct", NPS_NET_FLOW_PCT, "NPS 연간 순현금흐름/적립금 % (W6 교육용 추계)", 1),
]
pd.DataFrame(params, columns=["key", "value", "meaning", "is_assumed"]).to_csv(f"{OUT}/fml_w6ss2_params.csv", index=False)

snap = [
    ("eq_kr", "국내주식", TARGET_2026_OLD["eq_kr"], TARGET_2026["eq_kr"], KR_EQ_2025[1], KR_EQ_2026_03[1], KR_EQ_2026_05[1], KR_EQ_2026_06[1], KR_EQ_2026_06[0], SAA_BAND["eq_kr"], SAA_BAND_KR_TEMP, TAA_BAND["eq_kr"], TARGET_2027["eq_kr"]),
    ("eq_fx", "해외주식", None, TARGET_2026["eq_fx"], None, None, None, FX_EQ_2026_06[1], FX_EQ_2026_06[0], SAA_BAND["eq_fx"], None, TAA_BAND["eq_fx"], TARGET_2027["eq_fx"]),
    ("bond_kr", "국내채권", None, TARGET_2026["bond_kr"], None, None, None, None, None, SAA_BAND["bond_kr"], None, TAA_BAND["bond_kr"], TARGET_2027["bond_kr"]),
    ("bond_fx", "해외채권", None, TARGET_2026["bond_fx"], None, None, None, None, None, SAA_BAND["bond_fx"], None, TAA_BAND["bond_fx"], TARGET_2027["bond_fx"]),
    ("alt", "대체투자", None, TARGET_2026["alt"], None, None, None, ALT_2026_06[1], ALT_2026_06[0], None, None, None, TARGET_2027["alt"]),
]
pd.DataFrame(snap, columns=["nps_class", "name", "target_2026_jan_pct", "target_2026_pct", "actual_2025_12_pct", "actual_2026_03_pct", "actual_2026_05_pct",
                            "actual_2026_06_pct", "actual_2026_06_trn", "saa_band_pp", "saa_band_temp_pp", "taa_band_pp", "target_2027_pct"]).assign(
    is_assumed=0, asof=ASOF, source="기금운용위 2026.1.26 · 5.28 의결 · 기금운용본부 월별 포트폴리오 · 기금운용지침 별표 1(2024.5.31)").to_csv(f"{OUT}/fml_w6ss2_nps_snapshot.csv", index=False)

kospi = pd.DataFrame(KOSPI, columns=["date", "kospi_close"])
kospi["note"] = ["2024 말", "2025 말(+75.6%)", "2026.3 말 · NPS 국내주식 21.0%", "거래대금 48조 기록", "5월 말 종가 · NPS 29.4%",
                 "장중 고점 · 유예 종료 직전", "고점 대비 −33% · NPS 약 23.5%(추정)", "기준일 직전 종가"]
kospi["nps_kr_eq_pct"] = [None, KR_EQ_2025[1], KR_EQ_2026_03[1], None, KR_EQ_2026_05[1], None, 23.5, None]
kospi["is_assumed"] = [0, 0, 0, 0, 0, 0, 1, 0]   # 7.7 비중은 언론 추정
kospi["asof"] = ASOF; kospi["source"] = "KRX · 기금운용본부 · 언론(2026.6~8)"
kospi.to_csv(f"{OUT}/fml_w6ss2_kospi_2026.csv", index=False)

inst = pd.DataFrame(INSTITUTIONS, columns=["code", "name", "aum_trn_krw", "liquid_market", "adv_trn_krw", "w_eq", "w_bond", "w_alt", "illiquid_share",
                                           "net_flow_pct", "risk_limit", "deriv_access", "is_assumed"])
inst["asof"] = ASOF
inst["source"] = ["기금운용본부 2026.6 말(국내주식 29.1 + 해외주식 35.4 = 64.1 · 대체 14.0 · 잔여 채권) · 순현금흐름은 교육용 추계",
                  "KIC 2025년 말 2,320억 달러(전통 78.1 · 대체 21.9 공시) — 주식/채권 분할과 거래대금은 교육용 가정 · 환율 1,435원",
                  "2026.7.31 정부 발표(20조+α · 공공기관 주식 16조 · 물납주식 4조 · 2027 가동 계획) — 배분·비유동 비중은 교육용 가정",
                  "W7 M9 케이스 2 의 가상 기관(5,000억) — 배분 · 지출률 5% · 기부 2% 는 교육용 가정"]
inst.to_csv(f"{OUT}/fml_w6ss2_institutions.csv", index=False)
print("→ CSV 6개 생성:", ", ".join(sorted(f for f in os.listdir(OUT) if f.startswith("fml_w6ss2_"))))
