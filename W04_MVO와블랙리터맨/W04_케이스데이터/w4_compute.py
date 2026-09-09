# -*- coding: utf-8 -*-
"""
W4 IC 케이스 판정 조건 계산 스크립트 (자체 완결)
  [M4 기금위]  K1 추정오차 검정 · K2 이행 실행 가능성 · K3 2031 정합성 · K4 시장 점유 상한
  [M5 BL IC]   V1 형식 · V2 Ω 정직성(Idzorek 역산) · V3 적중률 요건 · V4 스트레스 / N1 위험 예산 정합성
실행: python w4_build.py && python w4_compute.py
"""
import numpy as np, pandas as pd
from scipy.optimize import minimize
np.set_printoptions(suppress=True, precision=4)
pd.set_option("display.width", 160)

cma = pd.read_csv("fml_w4_cma.csv"); codes = list(cma.asset); names = list(cma.asset_kr)
corr = pd.read_csv("fml_w4_corr.csv", index_col=0).values
mu = cma.mu.values; sig = cma.sigma.values; box = cma.box_delta.values
Sigma = np.outer(sig, sig) * corr
P = pd.read_csv("fml_w4_path_params.csv").set_index("param").value
saa = pd.read_csv("fml_w4_saa.csv")
w27 = saa[saa.kind == "target_2027"].set_index("asset").weight.reindex(codes).values
R_STAR = float(mu @ w27)             # 요구수익 = 2027 목표 배분의 기대수익(CMA 기준)
RISKY = [0, 1, 2, 3, 4]              # 단기자금 제외 5자산

def min_var(mu_, S, r_req, caps=None):
    """min w'Σw  s.t. μ'w ≥ r_req, 합=1, 공매도 금지, (선택) 상한 — 요구수익이 불가능하면 도달 가능한 최대치로"""
    n = len(mu_); r_req = min(r_req, mu_.max() - 1e-6)
    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1}, {"type": "ineq", "fun": lambda w: mu_ @ w - r_req}]
    bnds = [(0, 1 if caps is None else caps[i]) for i in range(n)]
    res = minimize(lambda w: w @ S @ w, np.ones(n) / n, bounds=bnds, constraints=cons, method="SLSQP")
    return res.x

def util_max(mu_, S, gamma, caps=None):
    n = len(mu_); cons = [{"type": "eq", "fun": lambda w: w.sum() - 1}]
    bnds = [(0, 1 if caps is None else caps[i]) for i in range(n)]
    res = minimize(lambda w: -(mu_ @ w - gamma / 2 * w @ S @ w), np.ones(n) / n, bounds=bnds, constraints=cons, method="SLSQP")
    return res.x

def ledoit_wolf(R):
    """Ledoit-Wolf(2004) 상수상관 목표 수축 — 수축 강도 반환"""
    T, n = R.shape; X = R - R.mean(0); S = X.T @ X / T
    s = np.sqrt(np.diag(S)); rbar = ((S / np.outer(s, s)).sum() - n) / (n * (n - 1))
    F = rbar * np.outer(s, s); np.fill_diagonal(F, np.diag(S))
    pi_mat = ((X[:, :, None] * X[:, None, :]) ** 2).mean(0) - S ** 2 * 0  # 근사
    pi = ((X ** 2).T @ (X ** 2) / T - S ** 2).sum()
    gamma = ((F - S) ** 2).sum()
    kappa = pi / gamma if gamma > 0 else 0
    delta = max(0, min(1, kappa / T))
    return delta * F + (1 - delta) * S, delta

print("=" * 70); print("[M4] K1 추정오차 검정 — 국내주식(eq_kr) 비중이 후보 수치를 구분하는가")
mu5, box5, S5 = mu[RISKY], box[RISKY], Sigma[np.ix_(RISKY, RISKY)]; n5 = [names[i] for i in RISKY]
print(f"  요구수익 r* = {R_STAR:.2%} (2027 목표 배분의 CMA 기대수익) · 5자산(단기자금 제외) · 공매도 금지")
caps = np.array([1, 0.40, 1, 1, 0.15])
w_pure = min_var(mu5, S5, R_STAR)
w_cap = min_var(mu5, S5, R_STAR, caps)
w_rob = min_var(mu5 - box5, S5, R_STAR - 0.01)      # 박스 최악 μ(μ − δ_box), 요구수익 1%p 완화
panel = pd.read_csv("fml_w4_panel_sim.csv"); R = panel[[f"{c}_ret" for c in codes]].values[:, RISKY]
S_lw, dlt = ledoit_wolf(R); S_lw *= 12
w_lw = min_var(mu5, S_lw, R_STAR)
rng = np.random.default_rng(1); B = 300; W = []; T = len(R)
for b in range(B):
    mub = rng.multivariate_normal(mu5, S5 / T)           # μ 추정오차: N(μ, Σ/T)
    idx = rng.integers(0, T, T); Sb, _ = ledoit_wolf(R[idx]); Sb *= 12
    W.append(min_var(mub, Sb, R_STAR))
W = np.array(W); w_mich = W.mean(0)
tab = pd.DataFrame({"순수 MVO": w_pure, "제약 MVO(해외주식≤40·대체≤15)": w_cap, "Robust(박스)": w_rob, "Ledoit-Wolf": w_lw, "Michaud(LW+재표본)": w_mich}, index=n5).T
print((tab * 100).round(1))
q = np.percentile(W[:, 0], [5, 50, 95]) * 100
print(f"  국내주식 부트스트랩 분포(B={B}, T={T}) 5%·50%·95% = {q[0]:.1f} / {q[1]:.1f} / {q[2]:.1f} %  | LW 수축 강도 {dlt:.2f}")
print("  γ 민감도(효용 최대화·제약 동일, 국내주식 %):", {g: round(util_max(mu5, S5, g, caps)[0]*100, 1) for g in [1.5, 2.5, 4.0, 6.0]})
print(f"  현재 29.1% · 2027 목표 20.8% · 후보 14.9 / 18.0 / 20.8 — 강건 해(Robust·LW·Michaud) 국내주식 최대 {tab.iloc[2:,0].max()*100:.1f}% < 20.8% → 상향·동결의 MVO 근거 없음")
print(f"  후보가 분포 구간 안에 있는가: 14.9 {'안' if q[0]<=14.9<=q[2] else '밖'} · 18.0 {'안' if q[0]<=18<=q[2] else '밖'} · 20.8 {'안' if q[0]<=20.8<=q[2] else '밖'} → 구간 안이면 MVO만으로 수치 확정 불가")

print("=" * 70); print("[M4] K2 이행 실행 가능성 — 무매도 표류 경로와 연 순매도 한도")
A0 = P.aum_trn_krw; g = P.aum_growth; pr = P.eq_kr_price_return; H = int(P.horizon_years)
w0 = P.w_eq_kr_now
drift = [w0 * ((1 + pr) / (1 + g)) ** t for t in range(H + 1)]
A_H = A0 * (1 + g) ** H
limit = P.adv_trn_krw * P.participation_cap * P.trading_days
print(f"  표류 경로(신규 자금 배제·배당 비재투자): " + " → ".join(f"{d*100:.1f}" for d in drift) + " %  (2026→2031)")
print(f"  2031 총자산 {A_H:,.0f}조 · 연 순매도 한도 = ADV {P.adv_trn_krw}조 × 참여율 {P.participation_cap:.0%} × {int(P.trading_days)}일 = {limit:.0f}조/년")
cands = {"안 A 14.9%": 0.149, "안 C 17.5%": 0.175, "안 C 18.0%": 0.18, "안 B 20.8%": 0.208}
for k, x in cands.items():
    need = (drift[-1] - x) * A_H / H
    print(f"  {k}: 필요 순매도 {need:5.0f}조/년 → {'한도 이내 ✓' if need <= limit else '한도 초과 ✗'} (비율 {need/limit:.2f})")
x_star = drift[-1] - limit * H / A_H
print(f"  한도를 꽉 채웠을 때 도달 가능한 2031 종점 = {x_star*100:.1f}% → 기본 답의 하한")

print("=" * 70); print("[M4] K3 2031 정합성 — 주식 55% 안에서 해외주식이 2027 목표(35.6%) 아래로 내려가지 않는 국내주식 상한")
x_max = P.w_equity_target_2031 - P.w_eq_gl_target_2027
print(f"  국내주식 상한 = 55.0 − 35.6 = {x_max*100:.1f}% → 20.8% 동결은 해외주식 축소(35.6→34.2)를 뜻해 정합성 위반")

print("=" * 70); print("[M4] K4 시장 점유 상한 — 2031 보유액 / 국내주식 시가총액")
cap31 = P.mktcap_kr_trn_krw * (1 + pr) ** H
for k, x in cands.items():
    sh = x * A_H / cap31
    print(f"  {k}: 보유 {x*A_H:,.0f}조 / 시총 {cap31:,.0f}조 = {sh:.1%} → {'상한 이내' if sh <= P.share_cap else '상한 초과'}")
print(f"  현재 점유(2026.2) 7.7% · 2026.6 추정 {w0*A0/P.mktcap_kr_trn_krw:.1%} — K4는 어느 후보도 배제하지 않는다(구분력 없음, 기록만)")

# ---------------------------------------------------------------- BL
print("=" * 70); print("[M5] KIC 5자산 Black-Litterman")
bl = pd.read_csv("fml_w4_bl_inputs.csv"); kc = list(bl.asset); kn = list(bl.asset_kr)
kcorr = pd.read_csv("fml_w4_bl_corr.csv", index_col=0).values
ks = bl.sigma.values; KS = np.outer(ks, ks) * kcorr; wm = bl.w_mkt.values
delta, tau = 2.5, 0.025
pi = delta * KS @ wm
print("  균형 초과수익 π(δ=2.5):", dict(zip(kn, (pi * 100).round(2))))
V = pd.read_csv("fml_w4_views.csv")
Pm = V[[f"p_{c}" for c in kc]].values.astype(float); Q = V.q.values.copy(); conf = V.confidence.values.copy()
print("  V1 형식 — P 행합:", Pm.sum(1), "(절대=1 · 상대=0 ✓)", "| Q 단위: 초과수익(π와 동일) ✓ | Ω 대각·양수 ✓")

def bl_post(Om):
    tS = tau * KS
    M = np.linalg.inv(np.linalg.inv(tS) + Pm.T @ np.linalg.inv(Om) @ Pm)
    mu_bl = M @ (np.linalg.inv(tS) @ pi + Pm.T @ np.linalg.inv(Om) @ Q)
    w = np.linalg.inv(delta * KS) @ mu_bl
    return mu_bl, w

def idzorek_omega():
    """Idzorek(2005): 자신감 c → 100% 확신 시 비중 이동의 c배가 되도록 Ω_k 역산(뷰별 1차원 탐색)"""
    om = np.zeros(len(Q))
    for k in range(len(Q)):
        pk = Pm[k:k + 1]; qk = Q[k:k + 1]
        tS = tau * KS
        mu100 = pi + tS @ pk.T @ np.linalg.inv(pk @ tS @ pk.T) @ (qk - pk @ pi)
        w100 = np.linalg.inv(delta * KS) @ mu100
        target = wm + conf[k] * (w100 - wm)
        best, bo = 1e9, None
        for o in np.logspace(-6, 0, 600):
            M = np.linalg.inv(np.linalg.inv(tS) + pk.T @ pk / o)
            mu_k = M @ (np.linalg.inv(tS) @ pi + pk.T @ qk / o)
            wk = np.linalg.inv(delta * KS) @ mu_k
            err = np.sum((wk - target) ** 2)
            if err < best: best, bo = err, o
        om[k] = bo
    return np.diag(om)

Om_case = np.diag(V.omega_case.values); Om_idz = idzorek_omega()
mu_c, w_c = bl_post(Om_case); mu_i, w_i = bl_post(Om_idz)
def constrained(mu_bl, S, cash_max=0.0):
    n = len(mu_bl); cons = [{"type": "eq", "fun": lambda w: w.sum() - 1}]
    res = minimize(lambda w: -(mu_bl @ w - delta / 2 * w @ S @ w), wm if len(wm)==n else np.ones(n)/n, bounds=[(0, 1)] * n, constraints=cons, method="SLSQP")
    return res.x
w_c = constrained(mu_c, KS); w_i = constrained(mu_i, KS)
tS = tau * KS
wt_case = [(Pm[k] @ tS @ Pm[k]) / (Pm[k] @ tS @ Pm[k] + Om_case[k, k]) for k in range(3)]
wt_idz = [(Pm[k] @ tS @ Pm[k]) / (Pm[k] @ tS @ Pm[k] + Om_idz[k, k]) for k in range(3)]
print("  V2 Ω 정직성 — 케이스 Ω:", np.diag(Om_case), "→ 뷰 반영률", np.round(wt_case, 2))
print("               Idzorek 역산 Ω(70·60·50%):", np.array2string(np.diag(Om_idz), formatter={"float_kind": lambda x: f"{x:.2e}"}), "→ 뷰 반영률", np.round(wt_idz, 2))
res = pd.DataFrame({"시장 비중": wm, "π": pi, "사후 μ(케이스 Ω)": mu_c, "비중(케이스 Ω)": w_c, "사후 μ(Idzorek)": mu_i, "비중(Idzorek)": w_i}, index=kn)
print((res * 100).round(1))
print(f"  (비중은 공매도 금지·합=1 제약 하의 사후 최적화) 케이스 덱 표기 '미 국채 20→26 · IG 15→11 · PE 10→8' 대조: 케이스 Ω 결과 {np.round(w_c[[1,2,3]]*100,1)} · Idzorek 결과 {np.round(w_i[[1,2,3]]*100,1)}")
# V4 스트레스: 세 뷰가 동시에 반대(뷰 크기만큼 반대 방향) 실현
dw = w_i - wm
shock = np.zeros(len(kc))
for k in range(3):
    shock += Pm[k] * (-(Q[k] - Pm[k] @ pi))       # 뷰가 예상한 편차가 같은 크기로 반대 실현
loss = dw @ shock
te = np.sqrt(dw @ KS @ dw)
print(f"  V4 스트레스 — 활성 비중 Δw = {np.round(dw*100,1)} · TE {te:.2%} · 세 뷰 동시 반대 시 손실 {loss:.2%} → 예산 −0.50% {'이내' if loss >= -0.005 else '초과'}")

print("  V3 자신감 상한 탐색 — 뷰 적중 이력이 없을 때 TE 예산(1.0%) 안에 드는 최대 균일 자신감 c")
conf0 = conf.copy(); rows = []
for c in [0.10, 0.20, 0.25, 0.30, 0.40, 0.50, 0.70]:
    conf[:] = c; Om_c = idzorek_omega(); mu_cc, _ = bl_post(Om_c); w_cc = constrained(mu_cc, KS)
    d = w_cc - wm; te_c = np.sqrt(d @ KS @ d); loss_c = d @ shock
    rows.append((c, te_c, w_cc[1], w_cc[2], loss_c))
conf[:] = conf0
for c, te_c, wu, wi_, l in rows:
    print(f"    c={c:.2f}: TE {te_c:.2%} · 미 국채 {wu:.1%} · IG {wi_:.1%} · 동시 반대 손실 {l:.2%} {'✓' if te_c <= 0.01 else '✗'}")
c_star = max(c for c, te_c, *_ in rows if te_c <= 0.01)
print(f"  → TE ≤ 1.0%를 만족하는 최대 자신감 c* = {c_star:.0%} : 이력 없는 뷰의 자신감 상한(조건부 승인 조건 1)")

print("=" * 70); print("[M5] 제2호 N1 — NPS 6자산 BL 가상 시나리오(교육용): 사후 비중과 기준포트폴리오 위험 예산")
wm6 = w27; Sig6 = Sigma; pi6 = delta * Sig6 @ wm6
P6 = np.array([[-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 1, -1, 0, 0]], float)   # 해외>국내 +0.5%p · 대체 초과 3% · 국내채권 > 해외채권 +0.2%p
Q6 = np.array([0.005, 0.030, 0.002]); c6 = np.array([0.5, 0.5, 0.5])
tS6 = tau * Sig6
def idz6():
    om = []
    for k in range(3):
        pk = P6[k:k+1]; qk = Q6[k:k+1]
        mu100 = pi6 + tS6 @ pk.T @ np.linalg.inv(pk @ tS6 @ pk.T) @ (qk - pk @ pi6)
        w100 = np.linalg.inv(delta * Sig6) @ mu100; target = wm6 + c6[k] * (w100 - wm6)
        best, bo = 1e9, None
        for o in np.logspace(-6, 0, 600):
            M = np.linalg.inv(np.linalg.inv(tS6) + pk.T @ pk / o)
            wk = np.linalg.inv(delta * Sig6) @ (M @ (np.linalg.inv(tS6) @ pi6 + pk.T @ qk / o))
            e = np.sum((wk - target) ** 2)
            if e < best: best, bo = e, o
        om.append(bo)
    return np.diag(om)
Om6 = idz6()
M6 = np.linalg.inv(np.linalg.inv(tS6) + P6.T @ np.linalg.inv(Om6) @ P6)
mu6 = M6 @ (np.linalg.inv(tS6) @ pi6 + P6.T @ np.linalg.inv(Om6) @ Q6)
def constrained6(mu_bl):
    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1}]
    res = minimize(lambda w: -(mu_bl @ w - delta / 2 * w @ Sig6 @ w), wm6, bounds=[(0, 1)] * 5 + [(0, 0.02)], constraints=cons, method="SLSQP")
    return res.x
w6 = constrained6(mu6)
print("  π(2027 목표 비중 역산):", dict(zip(names, (pi6*100).round(2))))
print("  사후 비중:", dict(zip(names, (w6*100).round(1))), f"| 합 {w6.sum():.3f}")
s_ref = np.sqrt(wm6 @ Sig6 @ wm6); s_post = np.sqrt(w6 @ Sig6 @ w6)
print(f"  N1 위험 예산 — 기준(2027 목표) σ {s_ref:.2%} · 사후 σ {s_post:.2%} → {'예산 이내(σ 비율 %.2f)' % (s_post/s_ref) if s_post <= s_ref*1.05 else '예산 초과'}")
print("  주의: 국내주식 사후 비중은 뷰 선택에 따라 달라진다 — '17.5% 일치'는 검증이 아니라 가정의 산물(교육용)")

# ---------------------------------------------------------------- 결과 저장 (덱 그림용)
import json
out = {
    "methods": {k: [float(v) for v in tab.loc[k].values] for k in tab.index}, "assets5": n5,
    "boot_eq_kr": [float(v) for v in W[:, 0]], "boot_q": [float(v) for v in q],
    "gamma_sens": {str(g): float(util_max(mu5, S5, g, caps)[0]) for g in [1.5, 2.0, 2.5, 3.0, 4.0, 6.0]},
    "drift": [float(d) for d in drift], "A_H": float(A_H), "limit": float(limit),
    "need": {k: float((drift[-1] - x) * A_H / H) for k, x in cands.items()}, "x_star": float(x_star), "x_max": float(x_max),
    "share31": {k: float(x * A_H / cap31) for k, x in cands.items()},
    "pi": [float(v) for v in pi], "kn": kn, "wm": [float(v) for v in wm],
    "w_case": [float(v) for v in w_c], "w_idz": [float(v) for v in w_i], "wt_case": [float(v) for v in wt_case], "wt_idz": [float(v) for v in wt_idz],
    "om_case": [float(v) for v in np.diag(Om_case)], "om_idz": [float(v) for v in np.diag(Om_idz)],
    "conf_table": [[float(v) for v in r] for r in rows], "c_star": float(c_star),
    "te_idz": float(te), "loss_idz": float(loss),
    "nps_pi": [float(v) for v in pi6], "nps_w": [float(v) for v in w6], "nps_sig": [float(s_ref), float(s_post)], "names6": names,
}
json.dump(out, open("w4_results.json", "w"), ensure_ascii=False, indent=1)
print("saved w4_results.json")
