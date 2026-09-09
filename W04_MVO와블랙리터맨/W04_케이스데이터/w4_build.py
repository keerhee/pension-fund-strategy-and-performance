# -*- coding: utf-8 -*-
"""
W4 IC 케이스 교육용 데이터 생성 스크립트 (자체 완결)
생성물
  fml_w4_saa.csv         NPS 자산군별 목표·현재 비중 (공시 수치 + 교육용 가정 구분)
  fml_w4_cma.csv         6자산 5년 CMA (기대수익·변동성·Robust 박스 폭) — 교육용 가정
  fml_w4_corr.csv        6자산 상관 행렬 — 교육용 가정
  fml_w4_path_params.csv 이행 경로 판정(K2~K4)에 쓰는 파라미터 — 공시 수치 + 교육용 가정
  fml_w4_bl_inputs.csv   KIC 5자산 BL 입력 (시장 비중·변동성) — 교육용 가정
  fml_w4_bl_corr.csv     KIC 5자산 상관 행렬 — 교육용 가정
  fml_w4_views.csv       KIC CIO 뷰 시트 (P·Q·자신감) — 케이스 시나리오
  fml_w4_panel_sim.csv   CMA에서 생성한 120개월 모의 수익률 패널 (bootstrap 실험용, 교육용 가정)
실행: python w4_build.py
규약: 비중은 소수, 금액 열 이름에 단위, asof/source/is_assumed 열
"""
import numpy as np, pandas as pd
ASOF = "2026-09-09"

# 1) NPS 자산군 비중 -----------------------------------------------------
codes = ["eq_kr", "eq_gl", "bond_kr", "bond_gl", "alt", "cash"]
names = ["국내주식", "해외주식", "국내채권", "해외채권", "대체투자", "단기자금"]
rows = []
# 2027 목표 (기금운용위원회 2026-05-28 의결, 정책브리핑)
tgt27 = [0.208, 0.356, 0.218, 0.074, 0.143, 0.001]
for c, n, w in zip(codes, names, tgt27):
    rows.append(dict(institution="NPS", asset=c, asset_kr=n, kind="target_2027", weight=w,
                     asof="2026-05-28", source="기금운용위원회 의결(2026.5.28) · 정책브리핑", is_assumed=0))
# 2026.6 현재 (국내주식·대체는 공시, 나머지는 잔여 배분 가정)
cur = [0.291, 0.322, 0.190, 0.065, 0.140, -0.008]
cur_flag = [0, 1, 1, 1, 0, 1]
for c, n, w, f in zip(codes, names, cur, cur_flag):
    rows.append(dict(institution="NPS", asset=c, asset_kr=n, kind="actual_2026_06", weight=w,
                     asof="2026-06-30", source="기금운용본부 공시(2026.6)" if f == 0 else "교육용 가정(잔여 배분)", is_assumed=f))
# 2031 종점 (주식 55 · 채권 30 · 대체 15 — 국내·해외 분할 미공시)
for c, n, w in zip(["equity", "bond", "alt"], ["주식(국내+해외)", "채권(국내+해외)", "대체투자"], [0.55, 0.30, 0.15]):
    rows.append(dict(institution="NPS", asset=c, asset_kr=n, kind="target_2031", weight=w,
                     asof="2026-05-28", source="기금운용위원회 의결(2026.5.28)", is_assumed=0))
pd.DataFrame(rows).to_csv("fml_w4_saa.csv", index=False)

# 2) 6자산 CMA (강의 Part A 기준, 교육용 가정) -----------------------------
cma = pd.DataFrame({
    "asset": codes, "asset_kr": names,
    "mu": [0.075, 0.080, 0.035, 0.038, 0.070, 0.025],
    "sigma": [0.18, 0.16, 0.05, 0.06, 0.12, 0.005],
    "box_delta": [0.015, 0.010, 0.005, 0.005, 0.020, 0.0],
    "asof": ASOF, "source": "W4 강의 Part A 입력(교육용 가정)", "is_assumed": 1})
cma.to_csv("fml_w4_cma.csv", index=False)
corr = np.array([
    [1.00, 0.70, 0.10, 0.05, 0.55, 0.00],
    [0.70, 1.00, 0.05, 0.15, 0.60, 0.00],
    [0.10, 0.05, 1.00, 0.50, 0.10, 0.10],
    [0.05, 0.15, 0.50, 1.00, 0.15, 0.10],
    [0.55, 0.60, 0.10, 0.15, 1.00, 0.00],
    [0.00, 0.00, 0.10, 0.10, 0.00, 1.00]])
pd.DataFrame(corr, index=codes, columns=codes).to_csv("fml_w4_corr.csv")

# 3) 이행 경로 파라미터 --------------------------------------------------
pp = [
    ("aum_trn_krw", 1865.6, "2026-06-30", "기금운용본부 공시(2026.6 총자산)", 0),
    ("w_eq_kr_now", 0.291, "2026-06-30", "기금운용본부 공시(2026.6 국내주식 비중)", 0),
    ("w_eq_kr_target_2027", 0.208, "2026-05-28", "기금운용위원회 의결", 0),
    ("w_eq_gl_target_2027", 0.356, "2026-05-28", "기금운용위원회 의결", 0),
    ("w_equity_target_2031", 0.55, "2026-05-28", "기금운용위원회 의결", 0),
    ("band_saa_taa_pp", 0.05, "2026-05-28", "SAA·TAA 허용범위 합계(기존 상단 19.9% = 14.9 + 5.0)", 0),
    ("mktcap_kr_trn_krw", 7000.0, "2026-06-30", "교육용 가정(2026.2말 5,146조에 이후 지수 상승 반영) — KRX에서 확인", 1),
    ("nps_share_of_mktcap_2026_02", 0.077, "2026-02-28", "언론 보도(395.1조 / 5,146.4조)", 0),
    ("adv_trn_krw", 20.0, "2026-06-30", "교육용 가정(국내주식 일평균 거래대금) — KRX에서 확인", 1),
    ("participation_cap", 0.01, ASOF, "교육용 가정(연기금 순매도 참여율 상한)", 1),
    ("trading_days", 240, ASOF, "교육용 가정", 1),
    ("aum_growth", 0.07, ASOF, "교육용 가정(순유입 + 운용수익)", 1),
    ("eq_kr_price_return", 0.055, ASOF, "교육용 가정(국내주식 가격수익 = μ 7.5% − 배당 2.0%)", 1),
    ("eq_kr_div_yield", 0.020, ASOF, "교육용 가정", 1),
    ("share_cap", 0.10, ASOF, "교육용 가정(시장 점유 상한)", 1),
    ("horizon_years", 5, ASOF, "2026 → 2031", 0),
]
pd.DataFrame(pp, columns=["param", "value", "asof", "source", "is_assumed"]).to_csv("fml_w4_path_params.csv", index=False)

# 4) KIC BL 입력 ----------------------------------------------------------
kc = ["eq_gl", "ust", "ig", "alt_pe", "alt_infra"]
kn = ["글로벌 주식", "미 국채", "IG 채권", "PE", "인프라"]
bl = pd.DataFrame({"institution": "KIC", "asset": kc, "asset_kr": kn,
                   "w_mkt": [0.50, 0.20, 0.15, 0.10, 0.05],
                   "sigma": [0.15, 0.06, 0.05, 0.20, 0.12],
                   "asof": ASOF, "source": "W4 강의 심층·KIC(교육용 가정)", "is_assumed": 1})
bl.to_csv("fml_w4_bl_inputs.csv", index=False)
kcorr = np.array([
    [1.00, -0.10, 0.20, 0.70, 0.50],
    [-0.10, 1.00, 0.60, -0.10, 0.10],
    [0.20, 0.60, 1.00, 0.10, 0.20],
    [0.70, -0.10, 0.10, 1.00, 0.45],
    [0.50, 0.10, 0.20, 0.45, 1.00]])
pd.DataFrame(kcorr, index=kc, columns=kc).to_csv("fml_w4_bl_corr.csv")
views = pd.DataFrame({
    "view_id": [1, 2, 3],
    "view_kr": ["미 국채 초과수익 0.5%로 상승", "미 국채가 IG 채권을 0.2%p 상회", "PE 초과수익 2.5%에 그침"],
    "view_type": ["absolute", "relative", "absolute"],
    "p_eq_gl": [0, 0, 0], "p_ust": [1, 1, 0], "p_ig": [0, -1, 0], "p_alt_pe": [0, 0, 1], "p_alt_infra": [0, 0, 0],
    "q": [0.005, 0.002, 0.025],
    "confidence": [0.70, 0.60, 0.50],
    "omega_case": [0.0015, 0.0015, 0.003],
    "asof": ASOF, "source": "케이스 시나리오(교육용 가정)", "is_assumed": 1})
views.to_csv("fml_w4_views.csv", index=False)

# 5) 모의 월간 수익률 패널 (bootstrap 실험용) ------------------------------
rng = np.random.default_rng(60080)
T = 120
Sig = np.outer(cma.sigma, cma.sigma) * corr
L = np.linalg.cholesky(Sig / 12)
Z = rng.standard_normal((T, len(codes)))
R = (cma.mu.values / 12) + Z @ L.T
dates = pd.date_range("2016-09-30", periods=T, freq="ME")
panel = pd.DataFrame(R, columns=[f"{c}_ret" for c in codes])
panel.insert(0, "date", dates.strftime("%Y-%m-%d"))
panel["rf"] = 0.025 / 12
panel.to_csv("fml_w4_panel_sim.csv", index=False)
print("built:", [f for f in ["fml_w4_saa.csv", "fml_w4_cma.csv", "fml_w4_corr.csv", "fml_w4_path_params.csv",
      "fml_w4_bl_inputs.csv", "fml_w4_bl_corr.csv", "fml_w4_views.csv", "fml_w4_panel_sim.csv"]])
