#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W7 M8 IC 케이스 교육용 데이터 생성 (기준일 2026-09-21).

제1호  국민연금 기금의 부채연계투자(LDI) — 부채 벤치마크를 도입하고, 부채 헤지 비율을 몇 %까지, 어떤 수단으로 올리는가
      안 A 현행(헤지 추가 없음 · 부채 지표 없음) · 안 B 시장 상한형(현물 초장기 국채, 5년) · 안 C 오버레이형(IRS 레버리지, 헤지 비율 30%)

공시 수치(is_assumed=0)와 교육용 가정(is_assumed=1)을 열로 구분한다. 교육용 가정은 이 파일 상단 상수를
바꾸면 되고, 바꾸면 w7m8_compute.py 의 판정 결과가 달라진다 — 그것이 실습의 일부다.
급여·보험료 현금흐름 추계는 W06 케이스데이터(fml_w6_cashflow.csv)와 같은 가정을 쓴다(주차 간 정합).

생성 파일
  fml_w7m8_params.csv     판정 임계 · 기준일 · 공시/가정 파라미터
  fml_w7m8_cashflow.csv   2026~2095 연도별 보험료 수입 · 급여 지출 · 순유출 (교육용 추계, 2025 재정추계 정점·소진에 맞춤)
  fml_w7m8_curve.csv      원화 국고채 수익률 곡선(2026-09-18 공시 4점 + 교육용 보간)과 충격 시나리오
  fml_w7m8_assets.csv     기금 자산 구성(2026.6 말 공시)과 원화 금리 듀레이션(교육용 가정)
  fml_w7m8_market.csv     시장 수용 규모 — 국고채 잔액·2025 만기별 발행·초장기물 잔액 추정·원화 IRS 거래규모
  fml_w7m8_options.csv    안 A·B·C 의 설계 변수(헤지 비율 목표 · 수단 · 프로그램 기간 · 버퍼)
  fml_w7m8_scenarios.csv  금리 충격 시나리오(평행 −100bp · 3일 +200bp · 2022 영국형)
  fml_w7m8_peers.csv      영국 · 네덜란드 · 한국의 부채 대 시장 규모 비교(공시 + 추정)
"""
import os
import numpy as np, pandas as pd

ASOF = "2026-09-21"
OUT = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# 0. 공시 수치 (is_assumed = 0)
# ─────────────────────────────────────────────────────────────────────────────
FUND_2025 = 1458.0            # 조원, 2025년 말 적립금 (국민연금 통계 · 2025 수익률 18.82%)
FUND_2026H1 = 1865.6          # 조원, 2026년 6월 말 (기금운용본부 포트폴리오 현황, 잠정)
ASSETS_2026H1 = {             # 조원, 2026.6 말 자산군별 금액 (기금운용본부 공시)
    "eq_dom": 543.2, "eq_for": 661.1, "bond_dom": 287.8, "bond_for": 110.2, "alt": 260.9, "cash": 4.6}
BOND_DOM_GOV_SHARE = 0.412    # 국내채권 중 국채 비중 (2026 2분기 말 공시)
TARGET_2027 = {"eq_dom": 20.8, "eq_for": 35.6, "bond_dom": 21.8, "bond_for": 7.4, "alt": 14.3}   # 2026.5.28 기금위 의결, 2027년 말 목표 %
SAA_RANGE_BOND_DOM = 7.0      # 국내채권 SAA 허용범위 ±%p (기금운용지침 별표 1, 2024.5.31)
PEAK_YEAR, PEAK_FUND = 2053, 3659.0     # 2025 재정추계(개혁 반영) 최대 적립 시점·규모
DEPLETE_45, DEPLETE_55 = 2064, 2071     # 소진 시점 — 기금수익률 4.5% / 5.5%
HURDLE = 5.5                  # 연금개혁 전제 기금수익률 (%) — 과정 표준 '허들'
CVAR_LIMIT = -15.0            # 기준포트폴리오 위험한도 CVaR95 (지침 제6조의2)
RATE_PATH = {y: min(13.0, 9.0 + 0.5 * (y - 2025)) for y in range(2025, 2096)}   # 보험료율 %, 2026~2033 +0.5%p/년
BENEFIT_2025_OFFICIAL, BENEFIT_2026_OFFICIAL = 50.1, 56.7   # 조원, 국민연금 중기재정전망(2025~2029) 급여 지출
UNFUNDED_NABO, UNFUNDED_NPSRI = 1820.0, 1735.0               # 조원, 미적립부채 추정 — 국회예산정책처(70년 기준) · 국민연금연구원(2021)
CURVE_OFFICIAL = {3: 4.06, 10: 4.47, 30: 4.60, 50: 4.55}      # %, 국고채 수익률 2026-09-18 (금융투자협회 최종호가 기준 집계치)
KTB_OUTSTANDING_2025 = 1159.4                               # 조원, 국고채 잔액 2025.12 말 (재정경제부 국채시장 통계)
KTB_ISSUE_2025 = {"2y": 26.1, "3y": 45.4, "5y": 37.0, "10y": 29.6, "20y": 7.6, "30y": 71.3, "50y": 8.4, "cpi": 0.5}   # 조원, 2025 만기물별 발행
KTB_ISSUE_TOTAL_2025, KTB_PLAN_2026 = 226.2, 225.7          # 조원 · 2026 계획(장기물 35±5%)
KTB_30Y_INCREASE_2014_2024 = 291.0                          # 조원, 30년물 잔액 증가(2014→2024, 자본시장연구원)
KTB_AVG_MATURITY_2024 = 13.2                                # 년, 평균 잔존만기 2024 (자본시장연구원)
LONG_BUYERS_2013_2024 = {"insurer": 229.4, "fund_mutual": 53.5, "foreign": 51.1, "asset_mgr": 14.1}   # 조원, 잔존만기 20년 초과 순매수
IRS_TURNOVER_2025, IRD_TURNOVER_2025 = 5986.0, 6215.0       # 조원, 2025 이자율스왑 · 이자율 관련 장외파생 거래규모(금융감독원)
UK = {"ldi_exposure_bn_gbp": 1500, "boe_envelope_bn": 65, "boe_bought_bn": 19.3, "gilt30_from": 3.7, "gilt30_to": 5.1,
      "buffer_bp": 250, "replenish_days": 5, "gilt_market_bn_gbp": 2200, "db_liab_bn_gbp": 1400}
NL = {"hedge_ratio_pre_wtp": 0.72, "wtp_deadline": "2028-01-01", "assets_bn_eur": 1700}

# ─────────────────────────────────────────────────────────────────────────────
# 1. 교육용 가정 (is_assumed = 1) — 바꿔 보라
# ─────────────────────────────────────────────────────────────────────────────
CONTRIB_2026, BENEFIT_2026 = 70.0, 56.0     # 2026 보험료 수입 · 급여 지출(조) — W06 과 동일
WAGE_G, INSURED_G = 0.030, -0.008           # 임금 상승률 · 가입자 증가율
G_B_EARLY, G_B_LATE, G_B_TAIL = 0.075, 0.0675, 0.035   # 급여 증가율 ~2050 · 2051~2070 · 이후 (W06 격자 탐색값)
LIAB_END_YEAR = DEPLETE_55                  # 부채 창 — 개혁 후 5.5% 공식 소진 연도(2071)까지의 순유출을 기금이 지는 부채로 본다
CURVE_INTERP = {1: 3.95, 2: 4.00, 5: 4.25, 20: 4.58}     # %, 교육용 보간점
DUR = {"bond_dom": 5.5, "bond_for": 6.5, "cash": 0.2, "eq_dom": 0.0, "eq_for": 0.0, "alt": 0.0}   # 수정 듀레이션(년)
KRW_RATE_EXPOSURE = {"bond_dom": 1.0, "bond_for": 0.0, "cash": 1.0, "eq_dom": 0.0, "eq_for": 0.0, "alt": 0.0}  # 원화 금리 노출 — 해외채권은 외화 금리
MU = {"eq_dom": 8.0, "eq_for": 8.0, "alt": 8.0, "bond_dom": 4.2, "bond_for": 4.5, "cash": 3.75}   # 기대수익 % (위험자산 8.0은 W06 과 동일)
KOFR = 3.75                                  # 단기 변동금리(교육용)
SWAP_SPREAD_30Y = -0.15                      # IRS 30년 고정금리 − 국고채 30년 (%p, 교육용)
HEDGE_TENOR = 30                             # 헤지 수단 만기(년) — 현물 국고채 · IRS 모두 30년
PROGRAM_YEARS = 5                            # 안 B 현물 매입 프로그램 기간(년)
CAP_ISSUE_SHARE = 0.30                       # 조건 ② 임계 — 매입액 ≤ 프로그램 기간 장기물(20·30·50년) 신규 발행의 30%
CAP_IRS_TURNOVER_SHARE = 0.05                # 조건 ② 임계 — IRS 명목 ≤ 연간 원화 IRS 거래규모의 5%
LONG_BOND_SHARE_2026PLAN = 0.35              # 2026 발행계획 장기물 비중(공시, 계획)
BUFFER_BP, REPLENISH_DAYS = 250, 5           # 조건 ③ — 영국 TPR 2023.4 최소 회복력 버퍼 · 재충전 기한
SHOCK_BP_3D = 200                            # 조건 ③ 스트레스 — 3영업일 +200bp (2022 영국 30년 길트 4일 +140bp 를 반올림)
DFR_MATERIAL_PP = -5.0                       # 조건 ① 임계 — 금리 −100bp 시 국채 기준 적립비율 변화 ≤ −5%p 면 '갭 실재'
HEDGE_TARGET_C = 0.30                        # 안 C 헤지 비율 목표
LIQUID_COLLATERAL = ["cash", "gov_bond"]     # 담보 적격 유동자산 — 단기자금 + 국고채 보유분
KTB_30Y_OUT_2014 = 30.0                      # 조원, 2014 말 30년물 잔액(교육용 추정; 2012 발행 개시)
KTB_50Y_OUT_2025 = 45.0                      # 조원, 2025 말 50년물 잔액(교육용 추정; 2016 발행 개시, 연 3~8조)
IRS_LONG_TENOR_SHARE = 0.10                  # 원화 IRS 거래 중 20년 이상 장기물 비중(교육용 가정)

YEARS = list(range(2026, 2096))


def cashflows():
    rows = []
    for y in YEARS:
        k = y - 2026
        contrib = CONTRIB_2026 * ((1 + WAGE_G) * (1 + INSURED_G)) ** k * (RATE_PATH[y] / RATE_PATH[2026])
        ben = BENEFIT_2026 * (1 + G_B_EARLY) ** min(k, 2050 - 2026) * (1 + G_B_LATE) ** max(0, min(y, 2070) - 2050) * (1 + G_B_TAIL) ** max(0, y - 2070)
        rows.append((y, RATE_PATH[y], contrib, ben, ben - contrib))
    return pd.DataFrame(rows, columns=["year", "contrib_rate_pct", "contrib_trn_krw", "benefit_trn_krw", "net_outflow_trn_krw"])


cf = cashflows()
cf["in_liability_window"] = (cf.year <= LIAB_END_YEAR).astype(int)
cf["is_assumed"] = 1; cf["asof"] = ASOF
cf["source"] = "교육용 추계 — W06 케이스데이터와 동일 가정(2025 재정추계 정점 2053·3,659조 · 소진 2064에 맞춤)"
cf.round(2).to_csv(f"{OUT}/fml_w7m8_cashflow.csv", index=False)

# ── 곡선 ────────────────────────────────────────────────────────────────────
curve = [(m, r, 0, "국고채 최종호가 수익률 2026-09-18") for m, r in CURVE_OFFICIAL.items()] + \
        [(m, r, 1, "교육용 보간") for m, r in CURVE_INTERP.items()]
curve = pd.DataFrame(sorted(curve), columns=["maturity_y", "yield_pct", "is_assumed", "source"]); curve["asof"] = ASOF
curve.to_csv(f"{OUT}/fml_w7m8_curve.csv", index=False)

# ── 자산 ────────────────────────────────────────────────────────────────────
names = {"eq_dom": "국내주식", "eq_for": "해외주식", "bond_dom": "국내채권", "bond_for": "해외채권", "alt": "대체투자", "cash": "단기자금"}
rows = []
for k, v in ASSETS_2026H1.items():
    rows.append((k, names[k], v, round(v / FUND_2026H1 * 100, 1), TARGET_2027.get(k, np.nan), DUR[k], KRW_RATE_EXPOSURE[k], MU[k]))
assets = pd.DataFrame(rows, columns=["asset", "name", "amount_trn_krw", "weight_pct_2026h1", "target_pct_2027", "mod_duration_y", "krw_rate_exposure", "mu_pct"])
assets["gov_bond_trn_krw"] = np.where(assets.asset == "bond_dom", round(ASSETS_2026H1["bond_dom"] * BOND_DOM_GOV_SHARE, 1), 0.0)
assets["asof"] = "2026-06-30"; assets["source"] = "기금운용본부 포트폴리오 현황(금액·비중, 공시) · 듀레이션·μ 는 교육용 가정"
assets["is_assumed_duration_mu"] = 1
assets.to_csv(f"{OUT}/fml_w7m8_assets.csv", index=False)

# ── 시장 규모 ───────────────────────────────────────────────────────────────
long_issue_2025 = KTB_ISSUE_2025["20y"] + KTB_ISSUE_2025["30y"] + KTB_ISSUE_2025["50y"]
ktb30_out_2025 = KTB_30Y_OUT_2014 + KTB_30Y_INCREASE_2014_2024 + KTB_ISSUE_2025["30y"]
market = pd.DataFrame([
    ("ktb_outstanding_trn", KTB_OUTSTANDING_2025, "국고채 잔액 2025.12 말", 0, "재정경제부 국채시장 통계"),
    ("ktb_issue_total_2025_trn", KTB_ISSUE_TOTAL_2025, "2025 국고채 발행 총액", 0, "재정경제부 국채시장 통계"),
    ("ktb_issue_30y_2025_trn", KTB_ISSUE_2025["30y"], "2025 30년물 발행", 0, "재정경제부 국채시장 통계"),
    ("ktb_issue_50y_2025_trn", KTB_ISSUE_2025["50y"], "2025 50년물 발행", 0, "재정경제부 국채시장 통계"),
    ("ktb_issue_20y_2025_trn", KTB_ISSUE_2025["20y"], "2025 20년물 발행", 0, "재정경제부 국채시장 통계"),
    ("ktb_issue_long_2025_trn", round(long_issue_2025, 1), "2025 장기물(20·30·50년) 발행 합계", 0, "재정경제부 국채시장 통계(합산)"),
    ("ktb_plan_2026_trn", KTB_PLAN_2026, "2026 국고채 발행 계획(장기물 35±5%)", 0, "재정경제부 2026 발행계획"),
    ("ktb_30y_out_2025_trn_est", round(ktb30_out_2025, 1), "30년물 잔액 2025 말 추정 = 2014 말 30조 + 2014→24 증가 291조 + 2025 발행 71.3조", 1, "자본시장연구원(증가분) + 교육용 추정"),
    ("ktb_50y_out_2025_trn_est", KTB_50Y_OUT_2025, "50년물 잔액 2025 말 추정", 1, "교육용 추정"),
    ("ktb_avg_maturity_2024_y", KTB_AVG_MATURITY_2024, "국고채 평균 잔존만기 2024", 0, "자본시장연구원"),
    ("long_buyer_insurer_trn", LONG_BUYERS_2013_2024["insurer"], "잔존만기 20년 초과 순매수 2013~2024 — 보험사", 0, "자본시장연구원"),
    ("long_buyer_fund_trn", LONG_BUYERS_2013_2024["fund_mutual"], "잔존만기 20년 초과 순매수 2013~2024 — 기금·공제", 0, "자본시장연구원"),
    ("long_buyer_foreign_trn", LONG_BUYERS_2013_2024["foreign"], "잔존만기 20년 초과 순매수 2013~2024 — 외국인", 0, "자본시장연구원"),
    ("irs_turnover_2025_trn", IRS_TURNOVER_2025, "2025 원화 이자율스왑 거래규모(연간 명목)", 0, "금융감독원 장외파생상품 거래 현황"),
    ("ird_turnover_2025_trn", IRD_TURNOVER_2025, "2025 이자율 관련 장외파생 거래규모", 0, "금융감독원"),
    ("irs_long_tenor_share", IRS_LONG_TENOR_SHARE, "IRS 거래 중 20년 이상 장기물 비중", 1, "교육용 가정"),
    ("unfunded_nabo_trn", UNFUNDED_NABO, "미적립부채 추정(70년 기준)", 0, "국회예산정책처"),
    ("unfunded_npsri_2021_trn", UNFUNDED_NPSRI, "미적립부채 추정(2021)", 0, "국민연금연구원"),
], columns=["key", "value", "meaning", "is_assumed", "source"]); market["asof"] = ASOF
market.to_csv(f"{OUT}/fml_w7m8_market.csv", index=False)

# ── 안 A·B·C ───────────────────────────────────────────────────────────────
options = pd.DataFrame([
    ("A", "현행 — 헤지 추가 없음 · 부채 벤치마크 없음", "none", 0.0, 0, 0, 0),
    ("B", f"시장 상한형 — 현물 30년 국고채, {PROGRAM_YEARS}년 프로그램, 매입 ≤ 장기물 발행의 {CAP_ISSUE_SHARE:.0%} · 부채 벤치마크(LBP) 공시", "cash_bond_30y", np.nan, PROGRAM_YEARS, 0, 1),
    ("C", f"오버레이형 — IRS 30년 오버레이로 헤지 비율 {HEDGE_TARGET_C:.0%}, 버퍼 {BUFFER_BP}bp · 부채 벤치마크 공시", "irs_30y", HEDGE_TARGET_C, 1, BUFFER_BP, 1),
], columns=["option", "description", "instrument", "hedge_ratio_target", "program_years", "buffer_bp", "lbp_disclosure"])
options["is_assumed"] = 1; options["asof"] = ASOF
options.to_csv(f"{OUT}/fml_w7m8_options.csv", index=False)

# ── 시나리오 ────────────────────────────────────────────────────────────────
pd.DataFrame([
    ("parallel_down_100", -100, 250, "평행 −100bp 영구 — 조건 ① 갭의 크기(적립비율 · 소진 연도)", 1),
    ("parallel_up_100", 100, 250, "평행 +100bp 영구 — 대칭 확인", 1),
    ("spike_up_200_3d", SHOCK_BP_3D, 3, "3영업일 +200bp 급등 — 조건 ③ 증거금(2022 영국 30년 길트 4일 +140bp 참고)", 1),
    ("uk_2022", 140, 4, "2022.9 영국 — 30년 길트 3.7 → 5.1%, BoE 650억 파운드 한도 · 실매입 193억", 0),
], columns=["scenario", "shock_bp", "horizon_days", "meaning", "is_assumed"]).assign(asof=ASOF).to_csv(f"{OUT}/fml_w7m8_scenarios.csv", index=False)

# ── 해외 비교 ────────────────────────────────────────────────────────────────
pd.DataFrame([
    ("UK", "영국 DB(2022)", UK["db_liab_bn_gbp"], UK["gilt_market_bn_gbp"], UK["ldi_exposure_bn_gbp"], 0.65, "십억 파운드", 0, "PPF · DMO · BoE — 부채·길트 잔액은 근사(±10%)"),
    ("NL", "네덜란드 DB(전환 전)", NL["assets_bn_eur"], np.nan, np.nan, NL["hedge_ratio_pre_wtp"], "십억 유로", 0, "DNB · 업계 추정(유로 스왑 시장이 헤지 수단이라 국채 잔액 비교 생략)"),
    ("KR", "국민연금(2026)", np.nan, KTB_OUTSTANDING_2025, round(ktb30_out_2025 + KTB_50Y_OUT_2025, 1), np.nan, "조원", 1, "부채·헤지 비율은 w7m8_compute.py 가 채운다(교육용)"),
], columns=["code", "name", "liability", "gov_bond_market", "long_market_or_ldi", "hedge_ratio", "unit", "is_assumed", "note"]).assign(asof=ASOF).to_csv(f"{OUT}/fml_w7m8_peers.csv", index=False)

# ── 파라미터 ────────────────────────────────────────────────────────────────
params = [
    ("asof", ASOF, "기준일", 0), ("fund_2025_trn", FUND_2025, "2025년 말 적립금(조)", 0), ("fund_2026h1_trn", FUND_2026H1, "2026년 6월 말 적립금(조, 잠정)", 0),
    ("peak_year_official", PEAK_YEAR, "2025 재정추계 최대 적립 시점", 0), ("peak_fund_official", PEAK_FUND, "최대 적립 규모(조)", 0),
    ("deplete_45_official", DEPLETE_45, "소진 — 수익률 4.5%", 0), ("deplete_55_official", DEPLETE_55, "소진 — 수익률 5.5%", 0),
    ("hurdle_pct", HURDLE, "허들 — 연금개혁 전제 기금수익률", 0), ("cvar_limit_pct", CVAR_LIMIT, "기준포트폴리오 위험한도 CVaR95(지침 제6조의2)", 0),
    ("saa_range_bond_dom_pp", SAA_RANGE_BOND_DOM, "국내채권 SAA 허용범위 ±%p(지침 별표 1)", 0), ("target_bond_dom_2027_pct", TARGET_2027["bond_dom"], "2027년 말 국내채권 목표 비중", 0),
    ("bond_dom_gov_share", BOND_DOM_GOV_SHARE, "국내채권 중 국채 비중(2026 2분기)", 0),
    ("benefit_2025_official", BENEFIT_2025_OFFICIAL, "2025 급여 지출(조, 중기재정전망)", 0), ("benefit_2026_official", BENEFIT_2026_OFFICIAL, "2026 급여 지출(조, 중기재정전망)", 0),
    ("contrib_2026", CONTRIB_2026, "2026 보험료 수입(조)", 1), ("benefit_2026", BENEFIT_2026, "2026 급여 지출(조)", 1),
    ("wage_g", WAGE_G, "임금 상승률", 1), ("insured_g", INSURED_G, "가입자 증가율", 1),
    ("benefit_g_early", G_B_EARLY, "급여 증가율 ~2050", 1), ("benefit_g_late", G_B_LATE, "급여 증가율 2051~2070", 1), ("benefit_g_tail", G_B_TAIL, "급여 증가율 2071~", 1),
    ("liab_end_year", LIAB_END_YEAR, "부채 창 종료 연도(순유출 PV 의 마지막 해)", 1),
    ("kofr_pct", KOFR, "단기 변동금리", 1), ("swap_spread_30y_pp", SWAP_SPREAD_30Y, "IRS 30년 − 국고채 30년", 1), ("hedge_tenor_y", HEDGE_TENOR, "헤지 수단 만기", 1),
    ("program_years", PROGRAM_YEARS, "안 B 프로그램 기간", 1), ("cap_issue_share", CAP_ISSUE_SHARE, "조건 ② 매입 ≤ 장기물 발행의 비율", 1),
    ("cap_irs_turnover_share", CAP_IRS_TURNOVER_SHARE, "조건 ② IRS 명목 ≤ 연간 거래규모의 비율", 1),
    ("buffer_bp", BUFFER_BP, "조건 ③ 버퍼(영국 TPR 최소 회복력)", 0), ("replenish_days", REPLENISH_DAYS, "버퍼 재충전 기한(영업일)", 0),
    ("shock_bp_3d", SHOCK_BP_3D, "조건 ③ 스트레스 — 3영업일 급등 bp", 1), ("dfr_material_pp", DFR_MATERIAL_PP, "조건 ① 임계 — −100bp 시 ΔFR_g", 1),
    ("hedge_target_C", HEDGE_TARGET_C, "안 C 헤지 비율 목표", 1), ("irs_turnover_2025_trn", IRS_TURNOVER_2025, "2025 원화 IRS 거래규모(조)", 0),
    ("uk_ldi_exposure_bn_gbp", UK["ldi_exposure_bn_gbp"], "영국 LDI 레버리지 익스포저(2021, 십억 파운드)", 0), ("uk_boe_envelope_bn", UK["boe_envelope_bn"], "BoE 매입 한도", 0), ("uk_boe_bought_bn", UK["boe_bought_bn"], "BoE 실매입", 0),
    ("nl_hedge_ratio", NL["hedge_ratio_pre_wtp"], "네덜란드 부채 헤지 비율(전환 전, 업계 추정)", 0), ("nl_wtp_deadline", NL["wtp_deadline"], "네덜란드 새 연금계약 전환 기한", 0),
    ("unfunded_nabo_trn", UNFUNDED_NABO, "미적립부채(국회예산정책처, 70년)", 0),
]
pd.DataFrame(params, columns=["key", "value", "meaning", "is_assumed"]).to_csv(f"{OUT}/fml_w7m8_params.csv", index=False)
print("→ fml_w7m8_*.csv 8개 생성 (", OUT, ")")
