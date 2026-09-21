#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W6 IC 케이스 — 판정 조건 계산 (w6_build.py 의 CSV → w6_results.json · compute_log.txt)

제1호 (기금운용위) 기관형 글라이드패스 — 감축 시작 트리거와 종점 (안 A·B·C)
  조건 ① 인적자본 비율   H/F = 향후 30년 보험료 수입 PV / 기금.  H/F ≥ 0.625(총부 기준 위험자산 비중 40%) 인 동안은
                        감축 근거 없음 → 감축 시작은 H/F 가 0.625 아래로 내려가는 해부터(BMS 1992). 그보다 이르면 탈락
  조건 ② 허들            종점 비중의 μ ≥ 5.5%(연금개혁 전제 기금수익률) — 종점 w ≥ w_h
  조건 ③ 시간분산(금액)   정점 이후 1σ 연간 손실액 ≤ 그해 급여 지출 1년치 (Samuelson: 비율이 아니라 금액)
  조건 ④ 소진 시점       경로별 소진 연도 ≥ 2071 (개혁 후 5.5% 공식 전망)
  조건 ⑤ 유동성 버퍼     순유출 전환 이후(소진 5년 전까지) 매년 안전자산 ≥ 급여 2년치. 시퀀싱(2008형 충격 1회의 소진 앞당김)은 참고 산수 — 경로를 가르지 않는다
제2호 (KIC) 헤징 수요 프로그램 — 수단별
  조건 ① 예측력          상태변수 → 이후 10년 연환산 초과수익 회귀의 t값 ≥ 2 (Newey–West)
  조건 ② 크기            헤징 수요(%p) = (1 − 1/γ) × β × σ_state / σ_asset ≥ 5%p
  조건 ③ 비용            연 캐리 비용 ≤ 30bp
  조건 ④ 거버넌스        다년 손실 허용 명문화 — 표결 조건(계산 대상 아님)
"""
import json, os
import numpy as np, pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
P = pd.read_csv(f"{D}/fml_w6_params.csv").set_index("key").value
f = lambda k: float(P[k])
cf = pd.read_csv(f"{D}/fml_w6_cashflow.csv")
gp = pd.read_csv(f"{D}/fml_w6_glidepaths.csv")
cma = pd.read_csv(f"{D}/fml_w6_cma.csv").set_index("asset")
sc = pd.read_csv(f"{D}/fml_w6_scenarios.csv").set_index("scenario")
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
L("\n=== 제2호 — KIC 헤징 수요 프로그램 ===")
pn = pd.read_csv(f"{D}/fml_w6_kic_panel_sim.csv")
hedge = pd.read_csv(f"{D}/fml_w6_kic_hedge.csv").set_index("instrument")
gamma, Hz = f("gamma_kic"), int(f("horizon_kic"))


def predictive(x, ret, hz):
    """상태변수 x(t) → 이후 hz년 연환산 수익(%) 회귀. Newey–West(lag 12hz−1) t값."""
    fwd = np.array([ret[i + 1:i + 1 + 12 * hz].mean() * 12 for i in range(len(ret) - 12 * hz)]); xs = x[: len(fwd)]
    X = np.c_[np.ones(len(xs)), xs]; beta, *_ = np.linalg.lstsq(X, fwd, rcond=None); resid = fwd - X @ beta
    lag = 12 * hz - 1; u = resid[:, None] * X; S = u.T @ u
    for l in range(1, lag + 1):
        wgt = 1 - l / (lag + 1); G = u[l:].T @ u[:-l]; S += wgt * (G + G.T)
    XtX_inv = np.linalg.inv(X.T @ X); V = XtX_inv @ S @ XtX_inv
    return float(beta[1]), float(beta[1] / np.sqrt(V[1, 1]))


a2 = []
for inst, r in hedge.iterrows():
    x = pn[r.state_var].values; ret = pn[f"{inst}_ret"].values * 100
    beta, t = predictive(x, ret, Hz)
    sig_state = np.std(x); sig_asset = np.std(ret) * 12 ** 0.5
    hedge_pp = (1 - 1 / gamma) * beta * sig_state / sig_asset * 100
    cost = r.carry_cost_bp
    ok1, ok2, ok3 = t >= f("t_min"), abs(hedge_pp) >= f("hedge_min_pp"), cost <= f("cost_max_bp")
    verdict = "채택" if ok1 and ok2 and ok3 else ("조건부" if (ok1 and ok3) or (ok2 and ok3 and t >= 1.5) else "기각")
    a2.append({"instrument": inst, "name": r["name"], "state_var": r.state_var, "beta": round(beta, 3), "t": round(t, 2),
               "sig_state": round(float(sig_state), 3), "sig_asset": round(float(sig_asset), 2),
               "hedge_pp": round(float(hedge_pp), 1), "carry_cost_bp": int(cost), "cond1_ok": bool(ok1), "cond2_ok": bool(ok2), "cond3_ok": bool(ok3), "verdict": verdict})
    L(f"[{r['name']}] {r.state_var} → 10년 수익: β {beta:.3f} · t {t:.2f} ({'통과' if ok1 else '탈락'}) · 헤징 수요 {hedge_pp:+.1f}%p ({'통과' if ok2 else '탈락'}) "
      f"· 비용 {cost:.0f}bp ({'통과' if ok3 else '탈락'}) → {verdict}")
res["agenda2"]["instruments"] = a2
res["agenda2"]["gamma"] = gamma; res["agenda2"]["horizon"] = Hz
hz_tab = []
for hz in [1, 5, 10]:
    beta, t = predictive(pn["yield10"].values, pn["bond_long_ret"].values * 100, hz)
    hz_tab.append({"horizon": hz, "beta": round(beta, 3), "t": round(t, 2)})
res["agenda2"]["bond_horizon"] = hz_tab
L("[지평] 장기채 예측 t값: " + " · ".join(f"{h['horizon']}년 {h['t']:.2f}" for h in hz_tab))
# γ 민감도 — 헤징 수요는 (1−1/γ) 에 비례
res["agenda2"]["gamma_sens"] = [{"gamma": g, "bond_pp": round((1 - 1 / g) / (1 - 1 / gamma) * a2[0]["hedge_pp"], 1)} for g in [1, 2, 5, 10]]
L("[γ 민감도] 장기채 헤징 수요: " + " · ".join(f"γ={s['gamma']} {s['bond_pp']:+.1f}%p" for s in res["agenda2"]["gamma_sens"]))

json.dump(res, open(f"{D}/w6_results.json", "w"), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
open(f"{D}/compute_log.txt", "w").write("\n".join(log) + "\n")
print("→ w6_results.json · compute_log.txt")
