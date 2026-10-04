#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W7 IC 케이스 — 판정 조건 계산 (w7m9_build.py 의 CSV → w7m9_results.json · compute_log.txt)

제1호 (기금운용위) 기관형 글라이드패스 — 감축 시작 트리거와 종점 (안 A·B·C)
  조건 ① 인적자본 비율   H/F = 향후 30년 보험료 수입 PV / 기금.  H/F ≥ 0.625(총부 기준 위험자산 비중 40%) 인 동안은
                        감축 근거 없음 → 감축 시작은 H/F 가 0.625 아래로 내려가는 해부터(BMS 1992). 그보다 이르면 탈락
  조건 ② 허들            종점 비중의 μ ≥ 5.5%(연금개혁 전제 기금수익률) — 종점 w ≥ w_h
  조건 ③ 시간분산(금액)   정점 이후 1σ 연간 손실액 ≤ 그해 급여 지출 1년치 (Samuelson: 비율이 아니라 금액)
  조건 ④ 소진 시점       경로별 소진 연도 ≥ 2071 (개혁 후 5.5% 공식 전망)
  조건 ⑤ 유동성 버퍼     순유출 전환 이후(소진 5년 전까지) 매년 안전자산 ≥ 급여 1.5년치. 시퀀싱(2008형 충격 1회의 소진 앞당김)은 참고 산수 — 경로를 가르지 않는다
제2호 (KIC) 헤징 수요 프로그램 — 수단별 (Campbell · Chan · Viceira 2003 방식을 단순화)
  VAR(1) 추정(상태변수 3 · 자산 4의 월 초과수익을 전월 상태변수로) → 4,000개 경로 → 1년 · 10년 CRRA(γ=5) 최적 고정 비중
  조건 ① 예측력          상태변수 → 기금 자산의 이후 1년 초과수익 회귀 |t| ≥ 2 (Newey–West · 겹치지 않는 1년 구간 40개)
  조건 ② 헤징 수요       10년 최적 비중 − 1년 최적 비중 ≥ 3%p
  조건 ③ 순편익          그 수단을 뺀 최적 대비 10년 확실성등가 기여(비용 차감) > 1bp/년
  조건 ④ 거버넌스        다년 손실 허용 명문화 — 표결 조건(계산 대상 아님)
  임계값(①②③)은 교육용 가정이다. 참고로 간편 공식 (1−1/γ)·β·σx/σa(10년 회귀)의 값도 함께 남긴다 — 공분산을 보지 않는 근사.
"""
import json, os
import numpy as np, pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
P = pd.read_csv(f"{D}/fml_w7m9_params.csv").set_index("key").value
f = lambda k: float(P[k])
cf = pd.read_csv(f"{D}/fml_w7m9_cashflow.csv")
gp = pd.read_csv(f"{D}/fml_w7m9_glidepaths.csv")
cma = pd.read_csv(f"{D}/fml_w7m9_cma.csv").set_index("asset")
sc = pd.read_csv(f"{D}/fml_w7m9_scenarios.csv").set_index("scenario")
MU_R, MU_S, SG_R, SG_S, RHO = cma.mu_pct["risk"], cma.mu_pct["safe"], cma.sigma_pct["risk"], cma.sigma_pct["safe"], f("rho")
F0 = f("fund_2025_trn"); HURDLE = f("hurdle_pct"); DISC = f("disc"); DEP_MIN = f("deplete_55_official")
log = []
def L(s): log.append(s); print(s)


def mu_sig(w):
    mu = w * MU_R + (1 - w) * MU_S
    var = (w * SG_R) ** 2 + ((1 - w) * SG_S) ** 2 + 2 * w * (1 - w) * SG_R * SG_S * RHO
    return mu, var ** 0.5


def project(w, shock=None):
    """w: 연도별 위험자산 비중. shock=(연도 집합, (risk, safe) 수익률 %) 이면 그 해만 충격 수익률."""
    F = F0; rows = []
    for i, r in cf.iterrows():
        y = int(r.year)
        ret = (w[i] * shock[1][0] + (1 - w[i]) * shock[1][1]) if (shock and y in shock[0]) else mu_sig(w[i])[0]
        Fb = F
        F = F * (1 + ret / 100) + r.contrib_trn_krw - r.benefit_trn_krw
        rows.append((y, Fb, ret, max(F, 0.0), w[i]))
        if F <= 0: break
    return pd.DataFrame(rows, columns=["year", "fund_begin", "ret", "fund_end", "w_risk"])


def deplete_year(path):
    d = path[path.fund_end <= 0].year
    return int(d.min()) if len(d) else None


res = {"asof": P["asof"], "agenda1": {}, "agenda2": {}}
L("=== 제1호 — 기관형 글라이드패스 ===")
# ── 조건 ① H/F ──────────────────────────────────────────────────────────────
c = cf.contrib_trn_krw.values
HW = int(f("h_window"))
H = np.array([sum(c[j] / (1 + DISC) ** (j - i + 1) for j in range(i, min(i + HW, len(c)))) for i in range(len(c))])
baseA = project(gp.w_risk_A.values)
n = len(baseA)
hf = H[:n] / baseA.fund_begin.values
hf_tab = pd.DataFrame({"year": baseA.year, "H_trn": H[:n].round(0), "F_trn": baseA.fund_begin.round(0), "HF": hf.round(3),
                       "risk_share_total_wealth": (0.65 * baseA.fund_begin.values / (baseA.fund_begin.values + H[:n])).round(3)})
trig = int(hf_tab.year[np.argmax(hf < f("hf_trigger"))])
net_out_year = int(cf.year[np.argmax(cf.benefit_trn_krw > cf.contrib_trn_krw)])
peakA = int(baseA.loc[baseA.fund_end.idxmax()].year)
L(f"[조건 ①] 2026 H/F = {hf[0]:.2f} (H {H[0]:,.0f}조 · F {F0:,.0f}조) → 총부 기준 위험자산 비중 {0.65*F0/(F0+H[0])*100:.1f}%")
L(f"[조건 ①] H/F < {f('hf_trigger'):.2f} 최초 연도 = {trig} · 순유출(급여 > 보험료) 전환 = {net_out_year} · 안 A 정점 = {peakA}")
for y in [2026, 2030, 2035, 2040, 2045, 2050, 2055, 2060]:
    if (hf_tab.year == y).any():
        r = hf_tab[hf_tab.year == y].iloc[0]
        L(f"        {y}: H {r.H_trn:,.0f} · F {r.F_trn:,.0f} · H/F {r.HF:.2f} · 총부 위험비중 {r.risk_share_total_wealth*100:.1f}%")
res["agenda1"]["cond1"] = {"HF_2026": round(float(hf[0]), 3), "trigger_year": trig, "net_outflow_year": net_out_year, "peak_year_A": peakA,
                           "table": hf_tab.to_dict("records")}
w_h = (HURDLE - MU_S) / (MU_R - MU_S)
res["agenda1"]["hurdle_min_w"] = round(w_h, 4)
L(f"[조건 ②] μ(w) ≥ {HURDLE}% 인 최소 위험자산 비중 w_h = {w_h*100:.1f}% (μ_risk {MU_R} · μ_safe {MU_S})")

# ── 조건 ②~⑤ 경로별 ────────────────────────────────────────────────────────
summary = []
for k in ["A", "B", "C"]:
    w = gp[f"w_risk_{k}"].values
    start = int(gp.year[np.argmax(w < 0.649)]) if (w < 0.649).any() else None
    base = project(w); dep = deplete_year(base)
    pk = base.loc[base.fund_end.idxmax()]
    mu_end = mu_sig(w[-1])[0]
    # 조건 ③ 시간분산(금액): 정점 이후 1σ 손실액 / 급여
    loss_ratio = []
    for i, r in base.iterrows():
        if r.year >= peakA and r.fund_begin > 0:
            ben = cf.benefit_trn_krw[cf.year == r.year].iloc[0]
            loss_ratio.append((int(r.year), r.w_risk * SG_R / 100 * r.fund_begin / ben))
    lr_max = max(v for _, v in loss_ratio) if loss_ratio else 0
    lr_2060 = next((v for y, v in loss_ratio if y == 2060), None)
    # 조건 ⑤ 시퀀싱: 2008형 충격 1회 — 순유출 전환 해 / 비교용 2027 · 2050
    seq = {}
    for sy in [2027, net_out_year, 2050]:
        d_s = deplete_year(project(w, ({sy}, (sc.risk_ret_pct["2008형"], sc.safe_ret_pct["2008형"]))))
        seq[sy] = (dep - d_s) if (dep and d_s) else None
    d22 = deplete_year(project(w, ({net_out_year}, (sc.risk_ret_pct["2022형"], sc.safe_ret_pct["2022형"]))))
    seq22 = (dep - d22) if (dep and d22) else None
    # 버퍼: 순유출 이후, 소진 5년 전까지 안전자산/급여
    buf = [((1 - r.w_risk) * r.fund_begin / cf.benefit_trn_krw[cf.year == r.year].iloc[0], int(r.year))
           for _, r in base.iterrows() if net_out_year <= r.year <= (dep or 2095) - 5 and r.fund_begin > 0]
    buf_min = min(buf) if buf else (0, None)
    row = {"path": k, "start_year": start, "w_end": float(w[-1]), "mu_2026": round(mu_sig(w[0])[0], 2), "mu_end": round(mu_end, 2),
           "peak_year": int(pk.year), "peak_fund": round(float(pk.fund_end)), "deplete_year": dep,
           "loss_ratio_max": round(lr_max, 2), "loss_ratio_2060": (round(lr_2060, 2) if lr_2060 else None),
           "seq_2008_at_netout": seq[net_out_year], "seq_2008_at_2027": seq[2027], "seq_2008_at_2050": seq[2050], "seq_2022_at_netout": seq22,
           "buffer_min_years": round(buf_min[0], 1), "buffer_min_year": buf_min[1],
           "cond1_ok": bool(start is None or start >= trig),
           "cond2_ok": bool(w[-1] >= w_h - 1e-9),
           "cond3_ok": bool(lr_max <= f("loss_ratio_max")),
           "cond4_ok": bool(dep and dep >= DEP_MIN),
           "cond5_ok": bool(buf_min[0] >= f("buffer_years"))}
    summary.append(row)
    ok = lambda b: "통과" if b else "탈락"
    L(f"[안 {k}] 시작 {start} · 종점 w {w[-1]*100:.0f}% · μ {row['mu_2026']}→{row['mu_end']}% · 정점 {int(pk.year)}년 {pk.fund_end:,.0f}조 · 소진 {dep}")
    L(f"       1σ손실/급여 최대 {lr_max:.2f}년치(2060 {lr_2060 if lr_2060 is None else round(lr_2060,2)}) · 2008형 충격 앞당김: {net_out_year}년 {seq[net_out_year]}년 / 2027년 {seq[2027]}년 / 2050년 {seq[2050]}년 · 2022형 {seq22}년 · 버퍼 최소 {buf_min[0]:.1f}년치({buf_min[1]})")
    L(f"       조건① {ok(row['cond1_ok'])} · ② {ok(row['cond2_ok'])} · ③ {ok(row['cond3_ok'])} · ④ {ok(row['cond4_ok'])} · ⑤ {ok(row['cond5_ok'])}")
res["agenda1"]["paths"] = summary

# 민감도 — 안 B 트리거 연도에서 속도·종점 바꿔 소진 연도와 조건 ③
sens = []
for spd in [0.5, 1.0, 2.0]:
    for floor in [60, 55, 50, 45, 40]:
        w = np.array([0.65 if y < trig else max(floor, 65 - spd * (y - trig + 1)) / 100 for y in cf.year])
        base = project(w); dep = deplete_year(base)
        lr = max((r.w_risk * SG_R / 100 * r.fund_begin / cf.benefit_trn_krw[cf.year == r.year].iloc[0]) for _, r in base.iterrows() if r.year >= peakA and r.fund_begin > 0)
        sens.append({"speed": spd, "floor": floor, "deplete": dep, "loss_ratio_max": round(lr, 2), "mu_end": round(mu_sig(w[-1])[0], 2),
                     "cond2_ok": bool(floor / 100 >= w_h - 1e-9), "cond3_ok": bool(lr <= f("loss_ratio_max")), "cond4_ok": bool(dep and dep >= DEP_MIN)})
res["agenda1"]["sensitivity_B"] = sens
L("[민감도 B, 1%p/년] " + " · ".join(f"종점 {s['floor']}%→소진 {s['deplete']}, 손실비 {s['loss_ratio_max']}, μ {s['mu_end']}" for s in sens if s["speed"] == 1.0))
sig65 = mu_sig(0.65)[1]
res["agenda1"]["time_div"] = [{"T": T, "annualized": round(sig65 / T ** 0.5, 2), "cumulative": round(sig65 * T ** 0.5, 1)} for T in [1, 5, 10, 20, 30]]
L("[시간분산] 65:35 σ {:.1f}% → T=30 연환산 {:.1f}% · 누적 {:.0f}%".format(sig65, sig65 / 30 ** 0.5, sig65 * 30 ** 0.5))

# ── 제2호 KIC ──────────────────────────────────────────────────────────────
from scipy.optimize import minimize
L("\n=== 제2호 — KIC 헤징 수요 프로그램 ===")
hedge = pd.read_csv(f"{D}/fml_w7m9_kic_hedge.csv").set_index("instrument")
gamma, Hz, RF = f("gamma_kic"), int(f("horizon_kic")), f("rf_kic") / 100 / 12
AS = ["eq", "bond_long", "tips", "vol_hedge"]; SV = ["yield10", "infl_exp", "vix"]
LINK = {"bond_long": ("yield10", "bond_long"), "tips": ("infl_exp", "eq"), "vol_hedge": ("vix", "eq")}
COST = np.array([0.0] + [hedge.cost_bp[k] for k in AS[1:]]) / 1e4 / 12
BOUNDS = [(0, 1.0), (0, 1.0), (0, 1.0), (0, 0.3)]


def predictive(x, ret, hz):
    """상태변수 x(t) → 이후 hz년 연환산 수익(%) 회귀. Newey–West(lag 12hz−1) t값."""
    fwd = np.array([ret[i + 1:i + 1 + 12 * hz].mean() * 12 for i in range(len(ret) - 12 * hz)]); xs = x[: len(fwd)]
    X = np.c_[np.ones(len(xs)), xs]; beta, *_ = np.linalg.lstsq(X, fwd, rcond=None); resid = fwd - X @ beta
    lag = 12 * hz - 1; u = resid[:, None] * X; S = u.T @ u
    for l in range(1, min(lag, len(u) - 1) + 1):
        wgt = 1 - l / (lag + 1); G = u[l:].T @ u[:-l]; S += wgt * (G + G.T)
    XtX_inv = np.linalg.inv(X.T @ X); V = XtX_inv @ S @ XtX_inv
    return float(beta[1]), float(beta[1] / np.sqrt(V[1, 1]))


def kic_engine(pn, paths=4000, seed=7):
    S = pn[SV].values; R = pn[[f"{k}_ret" for k in AS]].values; T = len(pn)
    X = np.c_[np.ones(T - 1), S[:-1]]
    Bs, *_ = np.linalg.lstsq(X, S[1:], rcond=None); Br, *_ = np.linalg.lstsq(X, R[1:], rcond=None)
    U = np.c_[S[1:] - X @ Bs, R[1:] - X @ Br]; Lc = np.linalg.cholesky(np.cov(U.T) + 1e-12 * np.eye(U.shape[1]))
    NM = 12 * Hz; Z = np.random.default_rng(seed).standard_normal((paths, NM, U.shape[1])) @ Lc.T
    s = np.tile(S.mean(0), (paths, 1)); RET = np.zeros((paths, NM, 4))
    for t in range(NM):
        xt = np.c_[np.ones(paths), s]; RET[:, t] = xt @ Br + Z[:, t, 3:]; s = xt @ Bs + Z[:, t, :3]
    def logce(w, m):
        lw = np.log1p(np.clip(RF + RET[:, :m] @ w - COST @ np.abs(w), -0.99, None)).sum(1)
        z = (1 - gamma) * lw; mx = z.max(); return (mx + np.log(np.mean(np.exp(z - mx)))) / (1 - gamma) * 12 / m
    ce = lambda w, m: (np.exp(logce(w, m)) - 1) * 100
    def opt(m, free, fixed=None):
        fixed = fixed or {}
        def fn(z):
            w = np.zeros(4); w[free] = z
            for k, v in fixed.items(): w[k] = v
            return -logce(w, m)
        best = None
        for st in (0.3, 0.6):
            z0 = np.full(len(free), 0.1); z0[0] = st if free[0] == 0 else 0.1
            r = minimize(fn, z0, bounds=[BOUNDS[j] for j in free], method="L-BFGS-B")
            if best is None or r.fun < best.fun: best = r
        w = np.zeros(4); w[free] = best.x
        for k, v in fixed.items(): w[k] = v
        return w
    return logce, ce, opt, NM


pn = pd.read_csv(f"{D}/fml_w7m9_kic_panel_sim.csv")
logce, ce, opt, NM = kic_engine(pn)
ALL = [0, 1, 2, 3]; w1 = opt(12, ALL); wH = opt(NM, ALL); ceH = ce(wH, NM)
a2 = []
for i, k in enumerate(AS[1:], start=1):
    sv, tgt = LINK[k]; r = hedge.loc[k]
    b1, t1 = predictive(pn[sv].values, pn[f"{tgt}_ret"].values * 100, 1)
    bF, tF = predictive(pn[sv].values, pn[f"{k}_ret"].values * 100, Hz)
    s_x, s_a = float(np.std(pn[sv].values)), float(np.std(pn[f"{k}_ret"].values * 100) * 12 ** 0.5)
    formula_pp = (1 - 1 / gamma) * bF * s_x / s_a * 100
    w_wo = opt(NM, [j for j in ALL if j != i]); gain = (ceH - ce(w_wo, NM)) * 100
    hd = (wH[i] - w1[i]) * 100
    ok1, ok2, ok3 = abs(t1) >= f("t_min"), hd >= f("hedge_min_pp"), gain > f("gain_min_bp")
    verdict = "채택" if ok1 and ok2 and ok3 else "기각"
    a2.append({"instrument": k, "name": r["name"], "state_var": sv, "target": tgt, "beta_1y": round(b1, 2), "t": round(t1, 2),
               "w_1y_pct": round(w1[i] * 100, 1), "w_10y_pct": round(wH[i] * 100, 1), "hedge_pp": round(hd, 1), "gain_bp": round(gain, 1),
               "cost_bp": int(r.cost_bp), "formula_t10": round(tF, 2), "formula_pp": round(formula_pp, 1),
               "cond1_ok": bool(ok1), "cond2_ok": bool(ok2), "cond3_ok": bool(ok3), "verdict": verdict})
    L(f"[{r['name']}] {sv} → {tgt} 1년: β {b1:+.2f} · t {t1:+.2f} ({'통과' if ok1 else '탈락'}) · 최적 비중 1년 {w1[i]*100:.1f}% → 10년 {wH[i]*100:.1f}% · "
      f"헤징 수요 {hd:+.1f}%p ({'통과' if ok2 else '탈락'}) · CE 기여 {gain:+.1f}bp ({'통과' if ok3 else '탈락'}) → {verdict}"
      f" | 참고 간편 공식: 10년 t {tF:.2f} · {formula_pp:+.1f}%p")
res["agenda2"]["instruments"] = a2
res["agenda2"]["gamma"] = gamma; res["agenda2"]["horizon"] = Hz
res["agenda2"]["equity"] = {"w_1y_pct": round(w1[0] * 100, 1), "w_10y_pct": round(wH[0] * 100, 1)}
L(f"[주식] 1년 {w1[0]*100:.1f}% → 10년 {wH[0]*100:.1f}%")
wA = opt(NM, [0]); wB = opt(NM, [0, 1, 2]); wC = opt(NM, [0, 1, 2], {3: 0.05})
opts = []; ceA = ce(wA, NM)
for nm, w in [("A", wA), ("B", wB), ("C", wC)]:
    opts.append({"vs_A_bp": int(round((ce(w, NM) - ceA) * 100)), "option": nm, "w_eq": round(w[0] * 100, 1), "w_bond": round(w[1] * 100, 1), "w_tips": round(w[2] * 100, 1), "w_vol": round(w[3] * 100, 1),
                 "ce_10y_pct": round(ce(w, NM), 2), "ce_1y_pct": round(ce(w, 12), 2)})
res["agenda2"]["options"] = opts
L("[세 안] " + " · ".join(f"{o['option']} 주식 {o['w_eq']} · 장기채 {o['w_bond']} · 물가연동 {o['w_tips']} · 변동성 {o['w_vol']} → 10년 CE {o['ce_10y_pct']:.2f}% (A 대비 {o['vs_A_bp']:+d}bp)" for o in opts))
# γ 민감도 — 직접 계산
gs = []
for g in [2, 5, 10]:
    g0 = gamma; gamma = g; lc, cc, oo, nm_ = kic_engine(pn); a1_, aH_ = oo(12, ALL), oo(nm_, ALL); gamma = g0
    gs.append({"gamma": g, "bond_pp": round((aH_[1] - a1_[1]) * 100, 1), "tips_pp": round((aH_[2] - a1_[2]) * 100, 1)})
res["agenda2"]["gamma_sens"] = gs
L("[γ 민감도] 헤징 수요(장기채 · 물가연동채): " + " · ".join(f"γ={x['gamma']} {x['bond_pp']:+.1f} · {x['tips_pp']:+.1f}%p" for x in gs))
# 강건성 — 같은 생성 과정, 다른 40년(시드 1~5)
import importlib.util
rob = []
spec = importlib.util.spec_from_file_location("bld", f"{D}/w7m9_build.py")
src = open(f"{D}/w7m9_build.py").read()
ns = {"np": np, "pd": pd}; exec(src[src.index("def simulate_kic"):src.index("yld, inf, vix, bond_long, tips, eq, vol_hedge = simulate_kic(KIC_SEED)")], {**ns, "N": 480}, ns)
for sd in range(1, 6):
    y_, p_, v_, b_, t_, e_, h_ = ns["simulate_kic"](sd)
    pq = pd.DataFrame({"yield10": y_, "infl_exp": p_, "vix": v_, "bond_long_ret": b_ / 100, "tips_ret": t_ / 100, "eq_ret": e_ / 100, "vol_hedge_ret": h_ / 100})
    lc, cc, oo, nm_ = kic_engine(pq)
    A_, B_, C_ = oo(nm_, [0]), oo(nm_, [0, 1, 2]), oo(nm_, [0, 1, 2], {3: 0.05})
    rob.append({"seed": sd, "B_vs_A_bp": round((cc(B_, nm_) - cc(A_, nm_)) * 100), "C_vs_B_bp": round((cc(C_, nm_) - cc(B_, nm_)) * 100), "w_tips_B": round(B_[2] * 100, 1)})
res["agenda2"]["robustness"] = rob
L("[강건성 · 시드 1~5] " + " · ".join(f"시드 {x['seed']}: B−A {x['B_vs_A_bp']:+d} · C−B {x['C_vs_B_bp']:+d}bp · 물가연동 {x['w_tips_B']}%" for x in rob))

json.dump(res, open(f"{D}/w7m9_results.json", "w"), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
open(f"{D}/compute_log.txt", "w").write("\n".join(log) + "\n")
print("→ w7m9_results.json · compute_log.txt")
