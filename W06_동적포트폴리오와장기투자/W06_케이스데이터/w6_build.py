#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W6 IC 케이스 교육용 데이터 생성 (기준일 2026-09-20).

제1호  국민연금 기금의 '기관형 글라이드패스' — 위험자산 비중을 언제부터, 얼마나 줄이는가
제2호  KIC 헤징 수요 프로그램 — 어느 상태변수에, 얼마나

공시 수치(is_assumed=0)와 교육용 가정(is_assumed=1)을 열로 구분한다. 교육용 가정은 이 파일의
상단 상수를 바꾸면 되고, 바꾸면 w6_compute.py 의 판정 결과가 달라진다 — 그것이 실습의 일부다.

생성 파일
  fml_w6_params.csv        판정 임계·CMA·기준일 등 파라미터(공시/가정 구분)
  fml_w6_fund_history.csv  기금 적립금·누적 조성·지출(공시)
  fml_w6_cashflow.csv      2026~2095 연도별 보험료 수입·급여 지출·보험료율 (교육용 추계, 2025 재정추계 정점·소진에 맞춤)
  fml_w6_glidepaths.csv    안 A·B·C 의 연도별 위험자산 비중
  fml_w6_cma.csv           위험자산·안전자산 CMA (교육용)
  fml_w6_scenarios.csv     충격 시나리오(2022형·2008형) 자산군 수익률
  fml_w6_kic_panel_sim.csv KIC 제2호 — 월간 모의 패널(상태변수 · 자산 수익률), 480개월
  fml_w6_kic_hedge.csv     KIC 제2호 — 헤지 수단별 비용·유동성(교육용)
"""
import json, os
import numpy as np, pandas as pd

ASOF = "2026-09-20"
OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(606)

# ─────────────────────────────────────────────────────────────────────────────
# 0. 공시 수치 (is_assumed = 0)
# ─────────────────────────────────────────────────────────────────────────────
FUND_2025 = 1458.0          # 조원, 2025년 말 적립금 (국민연금 통계)
FUND_2024 = 1212.9          # 조원, 2024년 말 (보건복지부)
CUM_CONTRIB_2024 = 859.0    # 누적 연금보험료 등, 2024년 말 (보건복지부)
CUM_BENEFIT_2024 = 371.3    # 누적 연금급여, 2024년 말
CUM_OUT_2026_04 = 452.8     # 누적 지출(연금급여 등), 2026.4 말 (기금운용본부)
CUM_OUT_2024 = 383.9        # 누적 지출, 2024 말
PEAK_YEAR, PEAK_FUND = 2053, 3659.0     # 2025 재정추계(개혁 반영) — 최대 적립 시점·규모
DEPLETE_45, DEPLETE_55 = 2064, 2071     # 소진 시점 — 기금수익률 4.5% / 5.5% 가정
RATE_PATH = {y: min(13.0, 9.0 + 0.5 * (y - 2025)) for y in range(2025, 2096)}   # 보험료율 %, 2026~2033 +0.5%p/년
HURDLE = 5.5                # 연금개혁 전제 기금수익률 (%)
REF_PORT = (0.65, 0.35)     # 기준포트폴리오 위험자산 65 : 안전자산 35 (2024.5 의결)
CVAR_LIMIT = -15.0          # 기준포트폴리오 위험한도 CVaR95 (%)
BENEFIT_2025 = (CUM_OUT_2026_04 - CUM_OUT_2024) / (16 / 12)   # 연 환산 지출 ≈ 51.7조 (2025~26.4 평균)

# ─────────────────────────────────────────────────────────────────────────────
# 1. 교육용 가정 (is_assumed = 1) — 바꿔 보라
# ─────────────────────────────────────────────────────────────────────────────
CONTRIB_2026 = 70.0         # 2026 보험료 수입(조), 보험료율 9.5% 기준 — 교육용 가정
BENEFIT_2026 = 56.0         # 2026 급여 지출(조) — 교육용 가정(2025 실적 약 52조에서 증가)
WAGE_G = 0.030              # 임금 상승률 (명목)
INSURED_G = -0.008          # 가입자 수 증가율 (감소)
DISC = 0.055                # 인적자본 유사물(미래 보험료 PV) 할인율 = 허들
H_WINDOW = 30               # 인적자본 유사물의 창(년) — 근로자의 남은 경력처럼 향후 30년 보험료만 센다
MU_RISK, MU_SAFE = 8.0, 3.0         # 위험자산·안전자산 기대수익 % (교육용 CMA)
SIG_RISK, SIG_SAFE, RHO = 15.0, 4.5, 0.10
SHOCK = {"2022형": (-9.4, -5.0),     # (위험자산, 안전자산) 연 수익률 % — 2022 기금 실적 기반 재구성
         "2008형": (-22.0, 4.0)}
BUFFER_YEARS = 1.5          # 조건 ⑤ 안전자산 ≥ 급여 n년치 (순유출 이후, 소진 5년 전까지 매년)
HF_TRIGGER = 0.625          # 조건 ① 인적자본 비율(H/F) 임계 ⇔ 총부(기금+H) 기준 위험자산 비중 40% (0.65/(1+0.625))
SEQ_LIMIT_YEARS = 5.0       # 참고 산수 — 2008형 충격 1회가 앞당기는 소진 연수(경로를 가르지 않는다 → 버퍼로 다룬다)
GLIDE_SPEED = 1.0           # 안 B·C 감축 속도 %p/년
GLIDE_FLOOR_B, GLIDE_FLOOR_C = 50.0, 45.0    # 종점 위험자산 비중 % — B 는 허들 하한(μ ≥ 5.5%)과 같다
LOSS_RATIO_MAX = 1.0        # 조건 ③ 시간분산: 1σ 연간 손실액 ≤ 그해 급여 n년치
GAMMA_KIC, HORIZON_KIC = 5.0, 10             # 제2호 위험회피도·지평(년)


def mu_sig(w):
    """위험자산 비중 w(0~1) 포트폴리오의 (μ, σ) %"""
    mu = w * MU_RISK + (1 - w) * MU_SAFE
    var = (w * SIG_RISK) ** 2 + ((1 - w) * SIG_SAFE) ** 2 + 2 * w * (1 - w) * SIG_RISK * SIG_SAFE * RHO
    return mu, var ** 0.5


# ─────────────────────────────────────────────────────────────────────────────
# 2. 현금흐름 추계 — 정점 2053 · 3,659조, 소진 2064(4.5%)에 맞춰 급여 증가율을 맞춘다
# ─────────────────────────────────────────────────────────────────────────────
YEARS = list(range(2026, 2096))


def cashflows(g_b_early, g_b_late, switch=2050, g_b_tail=0.035, switch2=2070):
    rows = []
    for y in YEARS:
        k = y - 2026
        contrib = CONTRIB_2026 * ((1 + WAGE_G) * (1 + INSURED_G)) ** k * (RATE_PATH[y] / RATE_PATH[2026])
        ben = BENEFIT_2026 * (1 + g_b_early) ** min(k, switch - 2026) * (1 + g_b_late) ** max(0, min(y, switch2) - switch) * (1 + g_b_tail) ** max(0, y - switch2)
        rows.append((y, RATE_PATH[y], contrib, ben))
    return pd.DataFrame(rows, columns=["year", "contrib_rate_pct", "contrib_trn_krw", "benefit_trn_krw"])


def project(cf, r_pct, w_path=None):
    """기금 경로. r_pct: 고정 수익률(%) 또는 None(w_path 로 μ 계산). 반환 DataFrame(year, fund_begin, ret, fund_end)"""
    F = FUND_2025; out = []
    for i, row in cf.iterrows():
        r = r_pct if r_pct is not None else mu_sig(w_path[i])[0]
        Fb = F
        F = F * (1 + r / 100) + row.contrib_trn_krw - row.benefit_trn_krw
        out.append((int(row.year), Fb, r, F))
        if F < 0:
            out[-1] = (int(row.year), Fb, r, 0.0)
            break
    return pd.DataFrame(out, columns=["year", "fund_begin_trn", "ret_pct", "fund_end_trn"])


def peak_and_deplete(path):
    pk = path.loc[path.fund_end_trn.idxmax()]
    dep = path[path.fund_end_trn <= 0].year.min()
    return int(pk.year), float(pk.fund_end_trn), (int(dep) if pd.notna(dep) else None)


# 급여 증가율 2개(2050 이전·이후)를 격자 탐색해 공시 정점·소진에 가장 가깝게
best = None
for g1 in np.arange(0.050, 0.081, 0.0025):
    for g2 in np.arange(0.030, 0.071, 0.0025):
        cf = cashflows(g1, g2)
        pk_y, pk_f, dep = peak_and_deplete(project(cf, 4.5))
        if dep is None: continue
        err = abs(pk_y - PEAK_YEAR) * 40 + abs(pk_f - PEAK_FUND) / 10 + abs(dep - DEPLETE_45) * 40
        if best is None or err < best[0]:
            best = (err, g1, g2, pk_y, pk_f, dep)
_, G_B_EARLY, G_B_LATE, pk_y, pk_f, dep45 = best
cf = cashflows(G_B_EARLY, G_B_LATE)
pk55 = peak_and_deplete(project(cf, 5.5))
cf["is_assumed"] = 1; cf["asof"] = ASOF; cf["source"] = "교육용 추계 — 2025 재정추계 정점(2053·3,659조)·소진(2064)에 맞춤"
cf.round(2).to_csv(f"{OUT}/fml_w6_cashflow.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 3. 글라이드패스 안 A·B·C
# ─────────────────────────────────────────────────────────────────────────────
# 인적자본 유사물 H(t) = 미래 보험료 수입의 현재가치(할인 5.5%) — 각 연도 초 기준
def human_capital(cf, disc=DISC):
    H = []
    c = cf.contrib_trn_krw.values
    for i in range(len(c)):
        H.append(sum(c[j] / (1 + disc) ** (j - i + 1) for j in range(i, min(i + H_WINDOW, len(c)))))
    return np.array(H)


H = human_capital(cf)
base = project(cf, None, np.full(len(cf), REF_PORT[0]))      # 안 A 로 기금 경로 → H/F 비율
F_begin = base.fund_begin_trn.values
hf = H[: len(F_begin)] / F_begin
trigger_year = int(cf.year[np.argmax(hf < HF_TRIGGER)]) if (hf < HF_TRIGGER).any() else None

def glide(start_year, floor):
    w = []
    for y in YEARS:
        if y < start_year: w.append(REF_PORT[0] * 100)
        else: w.append(max(floor, REF_PORT[0] * 100 - GLIDE_SPEED * (y - start_year + 1)))
    return np.array(w) / 100

paths = {
    "A": ("감축 없음 — 65:35 유지 · 유동성 버퍼로 대응", glide(9999, 65.0)),
    "B": (f"트리거형 — H/F < {HF_TRIGGER:.2f} 되는 해({trigger_year})부터 연 {GLIDE_SPEED:.0f}%p, 종점 {GLIDE_FLOOR_B:.0f}%", glide(trigger_year, GLIDE_FLOOR_B)),
    "C": (f"즉시 감축 — 2027년부터 연 {GLIDE_SPEED:.0f}%p, 종점 {GLIDE_FLOOR_C:.0f}%", glide(2027, GLIDE_FLOOR_C)),
}
gp = pd.DataFrame({"year": YEARS, **{f"w_risk_{k}": v[1] for k, v in paths.items()}})
gp["is_assumed"] = 1; gp["asof"] = ASOF
gp.round(4).to_csv(f"{OUT}/fml_w6_glidepaths.csv", index=False)

pd.DataFrame([
    ("risk", "위험자산(주식+대체)", MU_RISK, SIG_RISK, 1, ASOF),
    ("safe", "안전자산(채권)", MU_SAFE, SIG_SAFE, 1, ASOF),
], columns=["asset", "name", "mu_pct", "sigma_pct", "is_assumed", "asof"]).to_csv(f"{OUT}/fml_w6_cma.csv", index=False)
pd.DataFrame([(k, v[0], v[1], 1, ASOF) for k, v in SHOCK.items()],
             columns=["scenario", "risk_ret_pct", "safe_ret_pct", "is_assumed", "asof"]).to_csv(f"{OUT}/fml_w6_scenarios.csv", index=False)

pd.DataFrame([
    (2023, 1035.8, None, None, 0), (2024, FUND_2024, CUM_CONTRIB_2024, CUM_BENEFIT_2024, 0),
    (2025, FUND_2025, None, None, 0), (2026.5, 1865.6, None, None, 0),
], columns=["year", "fund_trn_krw", "cum_contrib_trn", "cum_benefit_trn", "is_assumed"]).assign(
    asof=ASOF, source="보건복지부 기금적립금 현황 · 국민연금 통계(2026.6)").to_csv(f"{OUT}/fml_w6_fund_history.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 4. KIC 제2호 — 상태변수 모의 패널 (교육용, 파라미터를 알고 만든 데이터)
#    자산: 장기 국채(bond_long) · 물가연동채(tips) · 주식(eq) · 변동성 헤지(vol_hedge, 롱 VIX 선물 유사)
#    상태변수: 10년 금리(yield10), 기대 인플레(infl_exp), 변동성 지수(vix)
#    "예측력"은 상태변수 → 이후 10년 연환산 초과수익 회귀의 t값으로 잰다.
# ─────────────────────────────────────────────────────────────────────────────
N = 480
GAMMA_KIC_, HZ_ = 5.0, 10


def predictive(x, ret, hz):
    """상태변수 x(t) → 이후 hz년 연환산 수익(%) 회귀의 (β, Newey–West t) — w6_compute.py 와 같은 정의"""
    fwd = np.array([ret[i + 1:i + 1 + 12 * hz].mean() * 12 for i in range(len(ret) - 12 * hz)]); xs = x[: len(fwd)]
    X = np.c_[np.ones(len(xs)), xs]; beta, *_ = np.linalg.lstsq(X, fwd, rcond=None); resid = fwd - X @ beta
    lag = 12 * hz - 1; u = resid[:, None] * X; S = u.T @ u
    for l in range(1, lag + 1):
        wgt = 1 - l / (lag + 1); G = u[l:].T @ u[:-l]; S += wgt * (G + G.T)
    XtX_inv = np.linalg.inv(X.T @ X); V = XtX_inv @ S @ XtX_inv
    return float(beta[1]), float(beta[1] / np.sqrt(V[1, 1]))


def simulate(seed):
    r = np.random.default_rng(seed)
    yld = np.zeros(N); inf = np.zeros(N); vix = np.zeros(N)
    yld[0], inf[0], vix[0] = 3.5, 2.2, 18.0
    for t in range(1, N):
        yld[t] = yld[t-1] + 0.006 * (3.5 - yld[t-1]) + r.normal(0, 0.10)     # 매우 지속적(반감기 약 10년) — 장기 예측력의 원천
        inf[t] = inf[t-1] + 0.008 * (2.2 - inf[t-1]) + r.normal(0, 0.08)
        vix[t] = max(9, vix[t-1] + 0.10 * (18 - vix[t-1]) + r.normal(0, 2.4))    # 빠르게 되돌아감(반감기 7개월) — 장기 예측력 없음
    e_b = r.normal(0, 1.2, N); e_t = r.normal(0, 1.0, N); e_e = r.normal(0, 4.2, N); e_v = r.normal(0, 7.0, N)
    lag = lambda a: np.r_[a[0], a[:-1]]           # 전월 상태변수가 이달 수익을 예측
    bond_long = 0.10 + 1.00 * (lag(yld) - 3.5) / 12 + e_b                  # 금리 1%p 높으면 이후 장기채 연 +1.0%p (강한 예측, β≈1)
    tips = 0.06 + 0.60 * (lag(inf) - 2.2) / 12 + 0.25 * (lag(yld) - 3.5) / 12 + e_t   # 기대 인플레 1%p → 연 +0.6%p (중간)
    eq = 0.50 + 0.05 * (lag(vix) - 18) / 12 + e_e                          # VIX 1pt → 연 +0.05%p (약함)
    vol_hedge = -1.2 + 0.9 * np.diff(np.r_[vix[0], vix]) + e_v            # 변동성 헤지: 평시 캐리 −1.2%/월, VIX 급등 시 +
    return yld, inf, vix, bond_long, tips, eq, vol_hedge


# 교육용 패널은 "설계된 예측력"을 가져야 한다 — 한 번의 난수 경로는 40년 표본으로도 t값이 크게 흔들리므로
# (장기 지평 회귀의 표본 문제 자체가 강의 소재다) 설계 범위에 드는 시드를 골라 기록한다.
def in_design(seed):
    yld, inf, vix, bl, tp, eq, vh = simulate(seed)
    tb = predictive(yld, bl, HZ_)[1]; tt = predictive(inf, tp, HZ_)[1]; tv = predictive(vix, eq, HZ_)[1]
    return (3.0 <= tb <= 6.0) and (2.0 <= tt <= 3.0) and (abs(tv) < 1.2), (tb, tt, tv)

SEED = None
for s in range(1, 3000):
    ok, ts = in_design(s)
    if ok: SEED = s; break
assert SEED is not None, "설계 범위의 시드를 찾지 못함"
yld, inf, vix, bond_long, tips, eq, vol_hedge = simulate(SEED)
print(f"KIC 패널 시드 {SEED} — t값 장기채 {ts[0]:.2f} · TIPS {ts[1]:.2f} · VIX {ts[2]:.2f}")
dates = pd.date_range("1986-12-31", periods=N, freq="ME")
panel = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "yield10": yld.round(3), "infl_exp": inf.round(3), "vix": vix.round(2),
                      "bond_long_ret": (bond_long / 100).round(5), "tips_ret": (tips / 100).round(5),
                      "eq_ret": (eq / 100).round(5), "vol_hedge_ret": (vol_hedge / 100).round(5)})
panel.to_csv(f"{OUT}/fml_w6_kic_panel_sim.csv", index=False)

pd.DataFrame([
    ("bond_long", "장기 국채 오버레이", "yield10", "금리 하락(재투자 수익 악화)", 5, 90, 1),
    ("tips", "물가연동채 · 실물자산", "infl_exp", "인플레 상승(실질가치 하락)", 15, 60, 1),
    ("vol_hedge", "변동성 헤지(옵션 · VIX 상품)", "vix", "변동성 상승(투자 기회 악화)", 140, 40, 1),
], columns=["instrument", "name", "state_var", "bad_state", "carry_cost_bp", "liquidity_score", "is_assumed"]).assign(asof=ASOF).to_csv(f"{OUT}/fml_w6_kic_hedge.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# 5. 파라미터 표
# ─────────────────────────────────────────────────────────────────────────────
params = [
    ("asof", ASOF, "기준일", 0), ("fund_2025_trn", FUND_2025, "2025년 말 적립금(조)", 0),
    ("peak_year_official", PEAK_YEAR, "2025 재정추계 최대 적립 시점", 0), ("peak_fund_official", PEAK_FUND, "최대 적립 규모(조)", 0),
    ("deplete_45_official", DEPLETE_45, "소진 시점 — 수익률 4.5%", 0), ("deplete_55_official", DEPLETE_55, "소진 시점 — 수익률 5.5%", 0),
    ("hurdle_pct", HURDLE, "연금개혁 전제 기금수익률", 0), ("ref_port_risk", REF_PORT[0], "기준포트폴리오 위험자산 비중", 0),
    ("cvar_limit_pct", CVAR_LIMIT, "기준포트폴리오 위험한도 CVaR95", 0), ("benefit_2025_est", round(BENEFIT_2025, 1), "2025~26.4 연환산 지출(조), 누적 지출 차분", 0),
    ("contrib_2026", CONTRIB_2026, "2026 보험료 수입(조)", 1), ("benefit_2026", BENEFIT_2026, "2026 급여 지출(조)", 1),
    ("wage_g", WAGE_G, "임금 상승률", 1), ("insured_g", INSURED_G, "가입자 증가율", 1),
    ("benefit_g_early", round(G_B_EARLY, 4), "급여 증가율 ~2050 (정점·소진에 맞춘 값)", 1), ("benefit_g_late", round(G_B_LATE, 4), "급여 증가율 2051~", 1),
    ("disc", DISC, "인적자본 유사물 할인율", 1), ("h_window", H_WINDOW, "인적자본 유사물 창(년)", 1), ("mu_risk", MU_RISK, "위험자산 μ", 1), ("mu_safe", MU_SAFE, "안전자산 μ", 1),
    ("sig_risk", SIG_RISK, "위험자산 σ", 1), ("sig_safe", SIG_SAFE, "안전자산 σ", 1), ("rho", RHO, "상관", 1),
    ("hf_trigger", HF_TRIGGER, "조건 ① H/F 임계(총부 위험비중 40%)", 1), ("seq_limit_years", SEQ_LIMIT_YEARS, "참고 — 충격 1회 소진 앞당김(년)", 1), ("loss_ratio_max", LOSS_RATIO_MAX, "조건 ③ 1σ 손실액/급여 상한(년치)", 1),
    ("buffer_years", BUFFER_YEARS, "조건 ⑤ 안전자산 ≥ 급여 n년치", 1), ("glide_speed", GLIDE_SPEED, "감축 속도 %p/년", 1),
    ("floor_B", GLIDE_FLOOR_B, "안 B 종점", 1), ("floor_C", GLIDE_FLOOR_C, "안 C 종점", 1),
    ("gamma_kic", GAMMA_KIC, "KIC 위험회피도", 1), ("kic_panel_seed", SEED, "KIC 모의 패널 난수 시드(설계 범위 탐색 결과)", 1), ("horizon_kic", HORIZON_KIC, "KIC 지평(년)", 1),
    ("t_min", 2.0, "제2호 조건 ① 예측력 t값 하한", 1), ("hedge_min_pp", 5.0, "제2호 조건 ② 헤징 수요 하한(%p)", 1),
    ("cost_max_bp", 30.0, "제2호 조건 ③ 연 캐리 비용 상한(bp)", 1),
]
pd.DataFrame(params, columns=["key", "value", "meaning", "is_assumed"]).to_csv(f"{OUT}/fml_w6_params.csv", index=False)

print(f"급여 증가율 맞춤: ~2050 {G_B_EARLY:.4f} · 2051~ {G_B_LATE:.4f} → 4.5% 정점 {pk_y}년 {pk_f:,.0f}조 · 소진 {dep45} / 5.5% 정점 {pk55[0]}년 {pk55[1]:,.0f}조 · 소진 {pk55[2]}")
print(f"H/F 트리거({HF_TRIGGER}) 도달 연도: {trigger_year}")
print("CSV 9개 생성")
