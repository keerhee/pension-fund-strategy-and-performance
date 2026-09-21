#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W7 M9 IC 케이스 교육용 데이터 생성 (기준일 2026-09-21).

케이스 1  퇴직연금 디폴트옵션 'Flexicure형(Floor + Cushion)' 상품 — Floor 수준 x · 승수 m 상한 · 수수료 상한 c 를 표결
케이스 2  H대학교 발전기금(5,000억, 가상) 'Yale 모델' — 비유동 대체 상한 x · 안전 유동자산 하한 y · 지출률 z 를 표결

공시 수치(is_assumed=0)와 교육용 가정(is_assumed=1)을 열로 구분한다. 교육용 가정은 이 파일 상단 상수를
바꾸면 되고, 바꾸면 w7m9_compute.py 의 판정 결과가 달라진다 — 그것이 실습의 일부다.

생성 파일
  fml_w7m9_params.csv          판정 임계·프로필·시뮬레이션 파라미터(공시/가정 구분)
  fml_w7m9_public_facts.csv    공시 수치 횡단면 — 퇴직연금·디폴트옵션·TDF·GPFG·Yale·사립대 적립금 (asof·source)
  fml_w7m9_tdf_2022.csv        2022년 TDF 실적표(공시) — 미국 3사 2025 빈티지 · 국내 TDF2025/2045 평균 · 지수
  fml_w7m9_panel_sim.csv       교육용 월간 모의 시장 패널 480개월 — 주식·국채·10년 금리·비유동 대체·현금·물가
  fml_w7m9_cppi_grid.csv       케이스 1 표결 격자 — Floor x · 승수 m · 수수료 c 조합
  fml_w7m9_cma.csv             케이스 2 자산군 CMA(교육용)
  fml_w7m9_endow_alloc.csv     케이스 2 비유동 대체 상한별 배분안(교육용)
  fml_w7m9_endow_cashflow.csv  케이스 2 지출·인출·캐피탈콜 시나리오(교육용)
  fml_w7m9_scenarios.csv       충격 시나리오 — 2022형·2008형 자산군 수익률(교육용)
"""
import os
import numpy as np, pandas as pd

ASOF = "2026-09-21"
OUT = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# 0. 공시 수치 (is_assumed = 0) — 출처는 fml_w7m9_public_facts.csv 의 source 열
# ─────────────────────────────────────────────────────────────────────────────
DC_TOTAL_TRN = 501.4          # 퇴직연금 적립금 2025년 말(조 원) — 금감원 2025 퇴직연금 투자백서
DC_GUAR_SHARE = 0.754         # 원리금보장 비중 75.4% (378.1조)
DC_GUAR_RET = 3.09            # 원리금보장 상품 평균 수익률 % (2025)
DC_TOTAL_RET_2025 = 6.47      # 전체 운용수익률 % (2025, 제도 도입 후 최고)
DEFAULT_TRN = 53.3            # 디폴트옵션 적립금 2025년 말(조 원) — 한국금융신문 2026.9.10
DEFAULT_STABLE_SHARE = 0.854  # 그중 안정형(원리금보장) 45.5조 = 85.4%
DEFAULT_MEMBERS_MN = 7.34     # 디폴트옵션 지정 가입자 734만 명(안정형 583만 = 79.4%)
TDF_NAV_2024_TRN = 16.6       # TDF 순자산 2024년 말(조 원) — 자본시장연구원 이슈보고서 26-08(제로인)
TDF_SET_2026_07_TRN = 20.2    # TDF 설정액 2026.7 말(조 원) — 금융투자협회·KG제로인(파이낸셜뉴스 2026.8.17)
TDF_FEE_AVG = 0.59            # TDF 총보수율 평균 % (2024년 말, 2025 빈티지 0.48)
TDF2025_2022 = -14.0          # 2022년 국내 TDF2025 1년 평균 수익률 % (자본시장연구원)
TDF2045_2022 = -16.8
GPFG_NOK_BN = 21268           # GPFG 2025년 말 시장가치(10억 NOK) — NBIM 연차보고서 2025
GPFG_USD_TRN = 2.39           # 2026.6 말 약 2.39조 달러(22,683 십억 NOK)
GPFG_EQ = 0.713               # 주식 71.3% · 채권 26.5 · 비상장 부동산 1.7 · 인프라 0.4 (2025 말)
GPFG_REL_PP = 0.24            # 1998~2025 벤치마크 대비 연 +0.24%p(비용 전) · 2025년 −0.28%p
GPFG_COST_BP = 4              # 운용비용 4bp
GPFG_RET_SINCE_1998 = 6.6     # 연평균 수익률 % (1998~2025)
YALE_BN_USD = 44.1            # Yale 기금 2025.6 말(10억 달러) · FY2025 수익률 11.1% · 10년 9.4%
YALE_SPEND_TARGET = 5.25      # 목표 지출률 % (80/20 평활) · FY2025 지출 21억 달러
YALE_ILLIQ_CAP = 0.50         # 정책 — 비유동 자산 ≤ 50%, 시장 비민감 자산(현금·채권·절대수익) ≥ 30%
YALE_SECONDARY_BN = 2.5       # 2025.6 PE 세컨더리 매각 약 25억 달러(탐색 규모 60억)
PRIV_UNIV_RESERVE_TRN = 11.5644  # 사립대 274교 적립금 2024년(조 원) — 교육부·대학교육연구소
PRIV_UNIV_SEC_CAP = 0.5       # 사립학교법 32조의2 — 적립금의 1/2 한도에서 증권 취득

# ─────────────────────────────────────────────────────────────────────────────
# 1. 교육용 가정 (is_assumed = 1) — 바꿔 보라
# ─────────────────────────────────────────────────────────────────────────────
SEED = 7009
N_PANEL = 480                       # 모의 패널 개월 수(40년)
# 케이스 1 — 표준 가입자 프로필(교육용)
AGE0, RETIRE_AGE = 55, 65           # 지평 10년
A0 = 1.0                            # 초기 적립금(단위: 초기 자산 = 1)
G_S_MULT = 1.10                     # Safety 목표 = 은퇴 시점 초기 자산의 1.10배(명목 원금 + 연 1%) — 원리금보장의 하한선 수준
GHP_Y0 = 3.0                        # 10년 국고채 금리 출발값 % (GHP = 만기 매칭 무이표채)
MARKET_ALT_RET = DC_GUAR_RET        # Market 목표 = 원리금보장 상품(3.09%) 10년 복리 — 공시 수익률을 목표로 쓴다
FLOOR_X = [0.80, 0.90, 1.00]        # 표결 후보 — Floor = x × Safety 목표의 현재가치(GHP 가격)
M_LIST = [1, 2, 3, 4, 5, 6]         # 표결 후보 — 승수 m
FEE_LIST = [0.5, 0.8, 1.0, 1.2, 1.5]  # 표결 후보 — 연 총보수 %
SAFETY_FAIL_MAX = 0.05              # 조건 ① P(W_T < G_S) ≤ 5%
CASH_TRAP_MAX = 0.10                # 조건 ② Cash Trap(락인 상태로 만기 도달) 확률 ≤ 10%
MARKET_MIN = 0.70                   # 조건 ③ 수수료 차감 후 P(W_T ≥ G_M) ≥ 70%
BREACH_MAX = 0.01                   # 조건 ④ 2022형 충격에서 Floor 위반율 ≤ 1%
CASH_TRAP_CUSHION = 0.01            # Cash Trap 정의 — 쿠션(W−F)/W 가 1% 아래로 떨어진 적이 있음(Floor 에 붙어 회복 불가)
REBAL_MONTHS = 3                    # 리밸런싱 주기(개월) — 실무는 이산시간: 분기. 1로 바꾸면 Cash Trap 은 줄고 거래비용이 는다
N_PATH_CPPI = 4000
MONTH_LOSS_CAP = -0.15              # 패널 월간 손실 절단(2008.10 −16.9% 참고). 1987.10 −21.8% 형 갭은 GAP_SHOCK 으로 따로 잰다
GAP_SHOCK = -0.22                   # 갭 스트레스 — 한 달 −22%(1987년 10월) 가 리밸런싱 직후에 오면 m 별로 Floor 가 깨지는가
SHOCK_2022_EQ = [-0.03, -0.02, -0.08, -0.04, 0.02, -0.06, 0.01, -0.03, 0.03, -0.02, 0.02, 0.005]  # 12개월 ≈ −19.6%
SHOCK_2022_DY = 0.25                # 금리 매월 +25bp × 12 = +300bp
# 케이스 2 — H대학교(가상) 프로필
ENDOW_KRW_BN = 5000.0               # 기금 5,000억(억 원)
FIXED_SPEND_BN = 175.0              # 장학·연구 고정 지출 175억(3.5%) — 삭감 불가(교육용 가정)
CURRENT_SPEND_BN = 200.0            # 현행 지출 200억(4.0%) = 고정 175 + 운영 전입 25 — 이사회 '지출 유지' 결의(교육용)
LUMP_BN, LUMP_YEAR = 600.0, 3       # 3년차 건축 목돈 600억 인출(교육용 시나리오)
Z_LIST = [3.5, 4.0, 4.5, 5.25]      # 표결 후보 — 지출률 % (5.25 = Yale 목표 지출률)
Y_LIST = [15, 20, 25, 30, 40]       # 표결 후보 — 안전 유동자산(현금·국채) 하한 %
X_ILLIQ = [0, 10, 20, 30, 40, 60]   # 표결 후보 — 비유동 대체(PE·VC·사모부동산) 상한 %
LOCKUP_YEARS = 10                   # 조건 ① 비유동 자산 락업(년, PE 펀드 존속기간) — 이 기간 유동자산으로 버텨야 한다
REAL_KEEP_MIN = 0.50                # 조건 ② 세대 간 중립 — 30년 후 실질가치 ≥ 현재 확률 ≥ 50% (기대 실질수익 ≥ 지출률)
SPEND_MARGIN = 0.5                  # 조건 ② z ≤ μ_real − 0.5%p
INFL = 2.0                          # 물가 % (교육용)
STAFF_H = 1                         # H대 대체투자 전담 인력(명) — 가상
STAFF_MIN, MGR_MIN, MIN_COMMIT_BN = 3, 15, 100.0   # 조건 ③ 직접 PE·VC 요건 — 전담 ≥3명 · 매니저 15개 분산 · 최소 출자 100억
UNFUNDED_SHARE, CALL_YEARS, DIST_START = 0.40, 4, 6  # 미납 약정 = 목표의 40%, 4년에 걸쳐 납입, 분배는 6년차부터(스트레스 시 0)
SMOOTH_W = 0.80                     # 지출 평활 — S_t = 0.8·S_{t−1}(1+π) + 0.2·z·W_{t−1} (Yale 규칙)
SPEND_KEEP_MIN = 0.95               # 조건 ④ 충격 후 3년 고정 지출 유지 확률 ≥ 95%
NO_SELL_YEARS = 3                   # 충격 후 3년간 주식·대체 매도 없이 안전 유동자산으로만 지출·목돈을 댄다
N_PATH_ENDOW, HORIZON_ENDOW = 4000, 30
CMA = {  # asset: (name, mu %, sigma %, liquid, is_direct)
    "eq":       ("주식(상장 대체 포함)", 8.0, 15.0, 1),
    "bond_gov": ("국채·우량채", 3.5, 5.0, 1),
    "cash":     ("현금·MMF", 2.5, 0.5, 1),
    "alt_pe":   ("비유동 대체 — 펀드오브펀드·세컨더리 경유(순)", 10.0, 20.0, 0),
    "alt_pe_direct": ("비유동 대체 — 일류 PE·VC 직접(접근권 충족 시)", 12.0, 22.0, 0),
}
ALLOC = {  # 비유동 x% → (eq, bond_gov, cash, alt_pe)
    0: (65, 30, 5, 0), 10: (60, 25, 5, 10), 20: (50, 25, 5, 20),
    30: (45, 20, 5, 30), 40: (40, 15, 5, 40), 60: (25, 10, 5, 60),
}
SHOCK = {  # scenario: (eq, bond_gov, cash, alt_pe 보고 기준(평가 지연), alt_pe 실제, 10년 금리 변화 bp)
    "2022형": (-20.0, -15.0, 2.0, -5.0, -20.0, 300),
    "2008형": (-40.0, 8.0, 3.0, -10.0, -35.0, -150),
}

rng = np.random.default_rng(SEED)

# ─────────────────────────────────────────────────────────────────────────────
# 2. 교육용 월간 모의 시장 패널 — 국면 전환(평시/위기) + 두꺼운 꼬리, 금리 AR(1), 대체는 평가 지연
# ─────────────────────────────────────────────────────────────────────────────
def simulate_panel(seed):
    r = np.random.default_rng(seed)
    n = N_PANEL
    regime = np.zeros(n, dtype=int); eq = np.zeros(n); y = np.zeros(n); y[0] = GHP_Y0
    for t in range(n):
        if t > 0:
            regime[t] = (1 if r.random() < 0.025 else 0) if regime[t-1] == 0 else (1 if r.random() < 0.65 else 0)
        mu, sg = (0.0080, 0.030) if regime[t] == 0 else (-0.025, 0.055)
        eq[t] = max(MONTH_LOSS_CAP, mu + sg * r.standard_t(5) / np.sqrt(5 / 3))   # 월간 손실 절단 — 1987년 10월형 갭(−22%)은 별도 스트레스로 다룬다
        if t > 0:
            y[t] = max(0.3, y[t-1] + 0.012 * (GHP_Y0 - y[t-1]) + r.normal(0, 0.17) + (0.12 if regime[t] == 0 and eq[t] > 0.03 else 0) - (0.15 if regime[t] == 1 else 0))
    dy = np.r_[0, np.diff(y)]
    bond = y / 100 / 12 - 7.0 * dy / 100                         # 듀레이션 7 국채 지수
    cash = np.clip(y - 0.5, 0.2, None) / 100 / 12
    pe_true = 0.0015 + 1.10 * eq + r.normal(0, 0.02, n)         # 비유동 대체 실제 수익(순, 펀드오브펀드 경유) — 주식 β 1.10 + 프리미엄
    pe_rep = np.zeros(n)
    for t in range(n):
        pe_rep[t] = 0.35 * pe_true[t] + 0.65 * (pe_rep[t-1] if t else pe_true[t])   # 평가 지연(스무딩)
    cpi = INFL / 100 / 12 + r.normal(0, 0.002, n)
    return regime, eq, y, bond, cash, pe_true, pe_rep, cpi


def annual_stats(eq):
    a = (1 + eq).reshape(-1, 12).prod(1) - 1
    return a.mean() * 100, a.std() * 100, a.min() * 100


# 설계 범위 — 주식 연 μ 8~9% · σ 13.5~16.5% · 최악 연 −25~−40%(2022형·2008형이 표본에 들어 있어야 한다)
seed = SEED
for s in range(SEED, SEED + 3000):
    reg, eq, y10, bond, cash, pe_t, pe_r, cpi = simulate_panel(s)
    m, sg, mn = annual_stats(eq)
    if 8.0 <= m <= 9.0 and 13.5 <= sg <= 16.5 and -40 <= mn <= -25 and 1.5 <= y10.min() and y10.max() <= 6.5:
        seed = s; break
else:
    raise SystemExit("설계 범위의 시드를 찾지 못함")
m, sg, mn = annual_stats(eq)
print(f"패널 시드 {seed} — 주식 연 μ {m:.1f}% σ {sg:.1f}% 최악 {mn:.1f}% · 금리 {y10.min():.1f}~{y10.max():.1f}% · 위기 개월 {reg.sum()}")
dates = pd.date_range("1986-12-31", periods=N_PANEL, freq="ME")
panel = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "regime": reg, "eq_ret": eq.round(5), "yield10": y10.round(3),
                      "bond_gov_ret": bond.round(5), "rf": cash.round(5), "alt_pe_ret": pe_t.round(5),
                      "alt_pe_rep_ret": pe_r.round(5), "cpi": cpi.round(5)})
panel.to_csv(f"{OUT}/fml_w7m9_panel_sim.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 3. 케이스 1 표결 격자 · 케이스 2 배분안·현금흐름·CMA·충격
# ─────────────────────────────────────────────────────────────────────────────
grid = [(x, mm, c) for x in FLOOR_X for mm in M_LIST for c in FEE_LIST]
pd.DataFrame(grid, columns=["floor_x", "m", "fee_pct"]).assign(is_assumed=1, asof=ASOF).to_csv(f"{OUT}/fml_w7m9_cppi_grid.csv", index=False)

def _ann(x): a = (1 + x[: (len(x)//12)*12].reshape(-1, 12)).prod(1) - 1; return round(a.mean()*100, 2), round(a.std()*100, 2)
_st = {"eq": _ann(eq), "bond_gov": _ann(bond), "cash": _ann(cash), "alt_pe": _ann(pe_t)}
_st["alt_pe_direct"] = (round(_st["alt_pe"][0] + 2.0, 2), _st["alt_pe"][1])   # 일류 접근 프리미엄 +2%p(교육용 가정)
CMA = {k: (v[0], _st[k][0], _st[k][1], v[3]) for k, v in CMA.items()}          # μ·σ 는 패널의 연 실현치로 맞춘다(산수와 MC 의 정합)
print("CMA(패널 연 실현치) — " + " · ".join(f"{k} {v[1]:.1f}/{v[2]:.1f}" for k, v in CMA.items()))
pd.DataFrame([(k, v[0], v[1], v[2], v[3], 1, ASOF) for k, v in CMA.items()],
             columns=["asset", "name", "mu_pct", "sigma_pct", "is_liquid", "is_assumed", "asof"]).to_csv(f"{OUT}/fml_w7m9_cma.csv", index=False)
pd.DataFrame([(x, *v, 1, ASOF) for x, v in ALLOC.items()],
             columns=["illiq_cap_pct", "w_eq", "w_bond_gov", "w_cash", "w_alt_pe", "is_assumed", "asof"]).to_csv(f"{OUT}/fml_w7m9_endow_alloc.csv", index=False)
rows = []
for t in range(1, HORIZON_ENDOW + 1):
    rows.append((t, FIXED_SPEND_BN * (1 + INFL / 100) ** (t - 1), CURRENT_SPEND_BN * (1 + INFL / 100) ** (t - 1),
                 LUMP_BN if t == LUMP_YEAR else 0.0))
pd.DataFrame(rows, columns=["year", "fixed_spend_bn_krw", "current_spend_bn_krw", "lump_withdrawal_bn_krw"]).assign(is_assumed=1, asof=ASOF).round(1).to_csv(f"{OUT}/fml_w7m9_endow_cashflow.csv", index=False)
pd.DataFrame([(k, *v, 1, ASOF) for k, v in SHOCK.items()],
             columns=["scenario", "eq_ret_pct", "bond_gov_ret_pct", "cash_ret_pct", "alt_pe_rep_ret_pct", "alt_pe_true_ret_pct", "yield10_chg_bp", "is_assumed", "asof"]).to_csv(f"{OUT}/fml_w7m9_scenarios.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 4. 공시 수치 횡단면 · 2022 TDF 실적표
# ─────────────────────────────────────────────────────────────────────────────
facts = [
    ("KR_DC", "dc_total_trn_krw", DC_TOTAL_TRN, "퇴직연금 적립금(조)", "2025-12-31", "금융감독원 2025 퇴직연금 투자백서(2026.5)"),
    ("KR_DC", "dc_guar_share", DC_GUAR_SHARE, "원리금보장 비중(378.1조)", "2025-12-31", "금융감독원 2025 퇴직연금 투자백서"),
    ("KR_DC", "dc_guar_ret_pct", DC_GUAR_RET, "원리금보장 평균 수익률 %", "2025-12-31", "금융감독원 2025 퇴직연금 투자백서"),
    ("KR_DC", "dc_total_ret_pct", DC_TOTAL_RET_2025, "전체 운용수익률 % (실적배당 16.80)", "2025-12-31", "금융감독원 2025 퇴직연금 투자백서"),
    ("KR_DEFAULT", "default_trn_krw", DEFAULT_TRN, "디폴트옵션 적립금(조) — 2023.7 시행", "2025-12-31", "한국금융신문 2026.9.10(고용노동부·금감원 공시 집계)"),
    ("KR_DEFAULT", "default_stable_share", DEFAULT_STABLE_SHARE, "안정형(원리금보장) 비중 45.5조", "2025-12-31", "한국금융신문 2026.9.10"),
    ("KR_DEFAULT", "default_members_mn", DEFAULT_MEMBERS_MN, "지정 가입자(백만 명), 안정형 583만 = 79.4%", "2025-12-31", "한국금융신문 2026.9.10"),
    ("KR_TDF", "tdf_nav_trn_krw", TDF_NAV_2024_TRN, "TDF 순자산(조) — 설정액 11.9조 · 운용사 22", "2024-12-31", "자본시장연구원 이슈보고서 26-08(제로인)"),
    ("KR_TDF", "tdf_set_trn_krw", TDF_SET_2026_07_TRN, "TDF 설정액(조) — 2026년 유입 3.7조", "2026-07-31", "금융투자협회·KG제로인(파이낸셜뉴스 2026.8.17)"),
    ("KR_TDF", "tdf_fee_avg_pct", TDF_FEE_AVG, "TDF 총보수율 평균 % (2025 빈티지 0.48 · 2050 0.71)", "2024-12-31", "자본시장연구원 이슈보고서 26-08"),
    ("KR_TDF", "tdf_share_of_dc_funds", 0.303, "퇴직연금 공모펀드 중 TDF 비중", "2026-08-03", "파이낸셜뉴스 2026.8.17"),
    ("GPFG", "aum_bn_nok", GPFG_NOK_BN, "시장가치(10억 NOK) — 2026.6 말 22,683", "2025-12-31", "NBIM 연차보고서 2025"),
    ("GPFG", "aum_trn_usd", GPFG_USD_TRN, "약 2.39조 달러", "2026-06-30", "NBIM 반기보고서 2026"),
    ("GPFG", "eq_share", GPFG_EQ, "주식 비중(채권 26.5 · 비상장 부동산 1.7 · 인프라 0.4)", "2025-12-31", "NBIM 연차보고서 2025"),
    ("GPFG", "rel_ret_pp", GPFG_REL_PP, "1998~2025 벤치마크 대비 연 %p(비용 전) · 2025년 −0.28", "2025-12-31", "NBIM 연차보고서 2025"),
    ("GPFG", "cost_bp", GPFG_COST_BP, "운용비용 bp", "2025-12-31", "NBIM 연차보고서 2025"),
    ("GPFG", "ret_since_1998_pct", GPFG_RET_SINCE_1998, "연평균 수익률 % (2025년 15.1%)", "2025-12-31", "NBIM 연차보고서 2025"),
    ("YALE", "aum_bn_usd", YALE_BN_USD, "기금 규모 — FY2025 수익률 11.1% · 10년 연 9.4% · 지출 21억 달러", "2025-06-30", "Yale News 2025.10.24"),
    ("YALE", "spend_target_pct", YALE_SPEND_TARGET, "목표 지출률 % — 80/20 평활, 예산의 약 1/3", "2025-06-30", "Yale Provost 기금 지출정책 안내"),
    ("YALE", "illiq_cap", YALE_ILLIQ_CAP, "정책 — 비유동 ≤ 50% · 시장 비민감 자산 ≥ 30%", "2025-06-30", "Yale Investments Office 기금 보고서"),
    ("YALE", "secondary_sale_bn_usd", YALE_SECONDARY_BN, "PE 세컨더리 매각(탐색 60억) — 연방 지원 축소·유동성", "2025-06-30", "Yale Daily News 2025.6.11 · Bloomberg"),
    ("YALE", "swensen_era_ret_pct", 13.7, "Swensen 재임 36년(1985~2021) 연평균 % — 과거 기록", "2021-06-30", "Yale News 2021.10.14"),
    ("KR_UNIV", "private_univ_reserve_trn_krw", PRIV_UNIV_RESERVE_TRN, "사립대 274교 적립금(조) — 예금·채권 중심", "2024-12-31", "교육부 대학알리미 · 대학교육연구소(2025.9)"),
    ("KR_UNIV", "reserve_securities_cap", PRIV_UNIV_SEC_CAP, "사립학교법 32조의2 — 적립금의 1/2 한도 증권 취득(벤처 1/10)", "2026-02-15", "국가법령정보센터"),
    ("KR_UNIV", "univ_fin_invest_loss_2021_bn", 183, "2021년 사립대 금융상품 투자 손실(억) — 교육부 국정감사 자료", "2021-12-31", "연합뉴스 2022.9.26"),
]
pd.DataFrame(facts, columns=["entity", "key", "value", "meaning", "asof", "source"]).assign(is_assumed=0).to_csv(f"{OUT}/fml_w7m9_public_facts.csv", index=False)

tdf = [
    ("VTTVX", "Vanguard Target Retirement 2025", "US", -15.55, 0.08, "없음 — 정적 글라이드패스", "Vanguard 팩트시트 2026.6"),
    ("FFTWX", "Fidelity Freedom 2025", "US", -16.6, 0.58, "없음 — 능동 배분", "AAII 펀드 데이터(Morningstar)"),
    ("TRRHX", "T. Rowe Price Retirement 2025", "US", -15.7, 0.53, "없음 — 주식 55% 유지", "AAII 펀드 데이터 · T. Rowe 팩트시트 2026.6"),
    ("KR_TDF2025", "국내 TDF2025 1년 평균", "KR", TDF2025_2022, 0.48, "펀드별 상이 — 편차 큼", "자본시장연구원 이슈보고서 26-08"),
    ("KR_TDF2045", "국내 TDF2045 1년 평균", "KR", TDF2045_2022, 0.68, "펀드별 상이", "자본시장연구원 이슈보고서 26-08"),
    ("KOSPI", "KOSPI 2022", "KR", -24.1, None, "지수", "자본시장연구원 이슈보고서 26-08"),
    ("MSCI", "MSCI 지수 2022", "US", -19.8, None, "지수", "자본시장연구원 이슈보고서 26-08"),
    ("TIAA_TRAD", "TIAA Traditional(RA 계약) 보증 최저", "US", 3.0, None, "보증 3% + 추가 적립이율", "TIAA 계약 안내"),
]
pd.DataFrame(tdf, columns=["code", "name", "market", "ret_2022_pct", "fee_pct", "floor_device", "source"]).assign(asof="2022-12-31", is_assumed=0).to_csv(f"{OUT}/fml_w7m9_tdf_2022.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 5. 파라미터 표
# ─────────────────────────────────────────────────────────────────────────────
params = [
    ("asof", ASOF, "기준일", 0), ("dc_guar_ret_pct", DC_GUAR_RET, "원리금보장 평균 수익률(Market 목표의 기준)", 0),
    ("panel_seed", seed, "모의 패널 난수 시드(설계 범위 탐색 결과)", 1), ("n_panel", N_PANEL, "패널 개월 수", 1),
    ("age0", AGE0, "케이스 1 표준 가입자 나이", 1), ("retire_age", RETIRE_AGE, "은퇴 나이(지평 10년)", 1),
    ("a0", A0, "초기 적립금(=1)", 1), ("g_s_mult", G_S_MULT, "Safety 목표 G_S = 초기 자산 × 배수(명목, T=10)", 1),
    ("ghp_y0", GHP_Y0, "10년 금리 출발값 %", 1), ("market_alt_ret_pct", MARKET_ALT_RET, "Market 목표 G_M = (1+r)^10, r = 원리금보장 수익률", 0),
    ("safety_fail_max", SAFETY_FAIL_MAX, "조건 ① P(W_T<G_S) 상한", 1), ("cash_trap_max", CASH_TRAP_MAX, "조건 ② Cash Trap 확률 상한", 1),
    ("market_min", MARKET_MIN, "조건 ③ P(W_T≥G_M) 하한", 1), ("breach_max", BREACH_MAX, "조건 ④ 2022형 Floor 위반율 상한", 1),
    ("cash_trap_cushion", CASH_TRAP_CUSHION, "Cash Trap — 쿠션/W 임계", 1), ("rebal_months", REBAL_MONTHS, "리밸런싱 주기(개월)", 1), ("n_path_cppi", N_PATH_CPPI, "CPPI 경로 수", 1),
    ("shock_2022_dy_bp", SHOCK_2022_DY * 100, "2022형 월 금리 상승 bp(×12)", 1), ("month_loss_cap", MONTH_LOSS_CAP, "패널 월간 손실 절단", 1), ("gap_shock", GAP_SHOCK, "갭 스트레스 — 한 달 수익률(1987년 10월형)", 1),
    ("endow_bn_krw", ENDOW_KRW_BN, "H대 기금(억)", 1), ("fixed_spend_bn", FIXED_SPEND_BN, "고정 지출(억) 3.5%", 1),
    ("current_spend_bn", CURRENT_SPEND_BN, "현행 지출(억) 4.0% — 이사회 유지 결의", 1), ("lump_bn", LUMP_BN, "목돈 인출(억)", 1), ("lump_year", LUMP_YEAR, "목돈 인출 연차", 1),
    ("lockup_years", LOCKUP_YEARS, "조건 ① 락업(년)", 1), ("real_keep_min", REAL_KEEP_MIN, "조건 ② 실질가치 유지 확률 하한", 1), ("spend_margin_pp", SPEND_MARGIN, "조건 ② 안전마진 %p", 1), ("infl_pct", INFL, "물가 %", 1),
    ("staff_h", STAFF_H, "H대 대체 전담 인력(명)", 1), ("staff_min", STAFF_MIN, "조건 ③ 전담 인력 하한", 1), ("mgr_min", MGR_MIN, "조건 ③ 매니저 분산 하한(개)", 1), ("min_commit_bn", MIN_COMMIT_BN, "최소 출자(억)", 1),
    ("unfunded_share", UNFUNDED_SHARE, "미납 약정 = 목표 × 비율", 1), ("call_years", CALL_YEARS, "납입 연수", 1), ("dist_start", DIST_START, "분배 개시 연차", 1),
    ("smooth_w", SMOOTH_W, "지출 평활 가중(전년 지출)", 1), ("spend_keep_min", SPEND_KEEP_MIN, "조건 ④ 고정 지출 유지 확률 하한", 1), ("no_sell_years", NO_SELL_YEARS, "충격 후 매도 금지 연수", 1),
    ("n_path_endow", N_PATH_ENDOW, "기금 경로 수", 1), ("z_list", "|".join(str(z) for z in Z_LIST), "지출률 후보", 1), ("y_list", "|".join(str(y) for y in Y_LIST), "안전 유동자산 하한 후보", 1), ("horizon_endow", HORIZON_ENDOW, "기금 지평(년)", 1),
    ("yale_illiq_cap", YALE_ILLIQ_CAP, "Yale 정책 비유동 상한(참고)", 0), ("yale_spend_target", YALE_SPEND_TARGET, "Yale 목표 지출률(참고)", 0),
]
pd.DataFrame(params, columns=["key", "value", "meaning", "is_assumed"]).to_csv(f"{OUT}/fml_w7m9_params.csv", index=False)
print("CSV 9개 생성")
