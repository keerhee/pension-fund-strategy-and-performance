#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIC 헤징 수요 계산 도구 — W07 보너스 과제 D (간편 공식과 직접 최적화를 함께 계산)

[0] 간편 공식: 상태변수 → 그 수단의 이후 10년 연평균 수익 회귀(겹치는 구간, Newey–West t),
    헤징 수요 = (1 − 1/γ) × β × σ(상태변수) ÷ σ(수단) × 100  — 간편 공식(휴리스틱)
[1]~[4] 직접 최적화 (Campbell · Chan · Viceira 2003의 접근을 단순화)
  1) 데이터에서 VAR(1)을 추정한다 — 상태변수(10년 금리 · 기대 인플레 · VIX)는 전월 상태변수로,
     자산의 월 초과수익률(주식 · 장기 국채 · 물가연동채 · 변동성 헤지)도 전월 상태변수로 설명한다.
  2) 추정한 VAR로 미래 경로 4,000개를 만든다(출발점 = 상태변수의 표본 평균).
  3) 투자 기간 1년과 10년 각각에 대해, 매달 같은 비중을 유지할 때 기대효용(CRRA)이 가장 큰 비중을 찾는다.
  4) 헤징 수요 = 10년 최적 비중 − 1년 최적 비중. 1년 최적 비중이 '단기 최적(myopic)' 비중이다.
  5) 경제적 판정 = 그 수단을 뺀 최적 포트폴리오와 비교한 확실성등가(CE) 기여(비용 차감 후).

판정 기준은 교육용 가정이다(누가 정해도 이 값이어야 하는 것이 아니다). 옵션으로 바꿔 결론이 바뀌는지 확인하라.
  --t-min 2 (예측력)  --hd-min 3 (헤징 수요 %p)  --gain-min 1 (CE 기여 bp/년)

사용법
  python3 hedging_tool.py                         # 기본 (γ = 5, 판정 기준 t ≥ 2 · 헤징 수요 ≥ 3%p)
  python3 hedging_tool.py --gamma 2               # 위험회피 계수 변경
  python3 hedging_tool.py --t-min 3 --hd-min 10 --gain-min 10   # 판정 기준 변경
  python3 hedging_tool.py --panel kh_panel_nocov.csv      # 비교: 예측력은 있지만 공분산(헤지 메커니즘)이 없는 세계
  python3 hedging_tool.py --panel real_panel.csv  # 실제 데이터로 다시 (fetch_real_data.py로 만든 파일)
  python3 hedging_tool.py --horizon 5             # 장기 투자 기간을 5년으로
"""
import argparse, os
import numpy as np, pandas as pd
from scipy.optimize import minimize

D = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--panel", default=f"{D}/kh_panel_kic.csv"); ap.add_argument("--gamma", type=float, default=5.0)
ap.add_argument("--horizon", type=int, default=10); ap.add_argument("--rf", type=float, default=3.0, help="무위험 금리 %/년")
ap.add_argument("--t-min", type=float, default=2.0); ap.add_argument("--hd-min", type=float, default=3.0)
ap.add_argument("--paths", type=int, default=4000); ap.add_argument("--gain-min", type=float, default=1.0, help="확실성등가 기여 기준 bp/년")
a = ap.parse_args()
G, H = a.gamma, a.horizon; RFM = a.rf / 100 / 12
pn = pd.read_csv(a.panel).dropna()
inst = pd.read_csv(f"{D}/kh_instruments.csv").set_index("instrument")
SV = ["yield10", "infl_exp", "vix"]; AS = ["eq", "bond_long", "tips", "vol_hedge"]
NAME = {"eq": "주식", "bond_long": "장기 국채", "tips": "물가연동채 · 실물", "vol_hedge": "변동성 헤지"}
S = pn[SV].values; R = pn[[f"{k}_ret" for k in AS]].values; T = len(pn)

# ── [1] 예측력 — 상태변수 → 이후 N년 연평균 초과수익 (Newey–West t) ───────────────
def predictive(x, ret, hz):
    m = 12 * hz
    if len(ret) - m < 24: return np.nan, np.nan, 0
    fwd = np.array([ret[i + 1:i + 1 + m].mean() * 12 for i in range(len(ret) - m)]); xs = x[: len(fwd)]
    X = np.c_[np.ones(len(xs)), xs]; b, *_ = np.linalg.lstsq(X, fwd, rcond=None); e = fwd - X @ b
    lag = m - 1; u = e[:, None] * X; Sm = u.T @ u
    for l in range(1, min(lag, len(u) - 1) + 1):
        Gm = u[l:].T @ u[:-l]; Sm += (1 - l / (lag + 1)) * (Gm + Gm.T)
    Xi = np.linalg.inv(X.T @ X); V = Xi @ Sm @ Xi
    return float(b[1]) * 100, float(b[1] / np.sqrt(V[1, 1])), len(ret) // m

# ── VAR 추정 ─────────────────────────────────────────────────────────────────
X = np.c_[np.ones(T - 1), S[:-1]]
Bs, *_ = np.linalg.lstsq(X, S[1:], rcond=None); Us = S[1:] - X @ Bs
Br, *_ = np.linalg.lstsq(X, R[1:], rcond=None); Ur = R[1:] - X @ Br
COV = np.cov(np.c_[Us, Ur].T)
L = np.linalg.cholesky(COV + 1e-12 * np.eye(COV.shape[0]))
rng = np.random.default_rng(7)
M = a.paths; NM = 12 * H
Z = rng.standard_normal((M, NM, COV.shape[0])) @ L.T
s = np.tile(S.mean(0), (M, 1)); RET = np.zeros((M, NM, len(AS)))
for t in range(NM):
    xt = np.c_[np.ones(M), s]
    RET[:, t] = xt @ Br + Z[:, t, 3:]
    s = xt @ Bs + Z[:, t, :3]

COST = np.array([0.0] + [inst.cost_bp[k] for k in AS[1:]]) / 1e4 / 12
BOUNDS = [(0, 1.0), (0, 1.0), (0, 1.0), (0, 0.3)]                                # 주식 0~100% · 오버레이 0~100% · 변동성 헤지 0~30%
def logce(w, months, cost=True):
    lw = np.log1p(np.clip(RFM + RET[:, :months] @ w - (COST @ np.abs(w) if cost else 0.0), -0.99, None)).sum(1)
    z = (1 - G) * lw; m = z.max()
    return (m + np.log(np.mean(np.exp(z - m)))) / (1 - G) * 12 / months      # 연율 로그 확실성등가
def ce(w, months, cost=True): return np.exp(logce(w, months, cost)) - 1
def optimize(months, free):
    def f(z):
        w = np.zeros(4); w[free] = z; return -logce(w, months)
    best = None
    for st in [0.3, 0.6]:
        z0 = np.full(len(free), 0.1); z0[0 if 0 in free else 0] = st if 0 in free else 0.1
        r = minimize(f, z0, bounds=[BOUNDS[j] for j in free], method="L-BFGS-B")
        if best is None or r.fun < best.fun: best = r
    w = np.zeros(4); w[free] = best.x; return w

print(f"=== 장기 투자자의 헤징 수요 — γ = {G:g} · 장기 투자 기간 {H}년 · 무위험 {a.rf:g}% · 데이터 {os.path.basename(a.panel)} ({T}개월) ===")
print(f"    판정 기준(교육용 가정 · 바꿔 볼 수 있음): ① 예측력 t ≥ {a.t_min:g} · ② 헤징 수요 ≥ {a.hd_min:g}%p · ③ 비용 차감 후 확실성등가 기여 > {a.gain_min:g}bp/년")
print(f"[0] 간편 공식 — 그 수단의 이후 {H}년 연평균 수익을 상태변수로 회귀 · 운용팀 기준(t ≥ 2 · |헤징 수요| ≥ 5%p · 비용 ≤ 30bp)")
for k in AS[1:]:
    sv = inst.state_var[k]; x = pn[sv].values; ret = pn[f"{k}_ret"].values * 100
    bH, tH, nind = predictive(x, ret / 100, H)
    s_x, s_r = np.std(x), np.std(ret) * 12 ** 0.5; hd0 = (1 - 1 / G) * bH * s_x / s_r * 100
    ok0 = [tH >= 2, abs(hd0) >= 5, inst.cost_bp[k] <= 30]
    print(f"    {NAME[k]:<9} β {bH:+.3f} · t {tH:+5.2f}(겹치지 않는 {H}년 구간 {nind}개) · 헤징 수요 (1−1/{G:g})×{bH:.3f}×{s_x:.2f}÷{s_r:.1f}×100 = {hd0:+5.1f}%p"
          f" · 비용 {inst.cost_bp[k]:.0f}bp → " + " · ".join(f"{s} {'통과' if o else '탈락'}" for s, o in zip("①②③", ok0)))
print("    ※ 이 공식은 '헤지 수단의 수익이 투자 기회 악화 충격과 함께 움직이는가'(공분산)를 보지 않는다. 아래 [1]~[4]가 그것을 직접 계산한다.")
print("[1] 예측력 — 상태변수가 1단위 높을 때 이후 1년 초과수익(%p) · Newey–West t값")
print("    (헤지 수단의 상태변수가 '투자 기회'를 예측하는가 — 예측 대상은 기금이 실제로 들고 있는 자산)")
LINK = {"bond_long": ("yield10", "bond_long"), "tips": ("infl_exp", "eq"), "vol_hedge": ("vix", "eq")}
tval = {}
for k, (sv, tgt) in LINK.items():
    b1, t1, nind = predictive(pn[sv].values, pn[f"{tgt}_ret"].values, 1); tval[k] = t1
    print(f"    {NAME[k]:<9} 상태변수 {sv:<9} → 예측 대상 {NAME[tgt]:<6} β {b1:+6.2f}%p · t {t1:+5.2f} (겹치지 않는 1년 구간 {nind}개)")
ALL = [0, 1, 2, 3]
w1 = optimize(12, ALL); wH = optimize(NM, ALL)
print(f"[2] 최적 비중 — 매달 같은 비중 유지 · 비용 차감 후 (오버레이 0~100%, 변동성 헤지 0~30%)")
print(f"    {'':<9} {'1년(단기 최적)':>12} {H:>4}년 최적   헤징 수요({H}년 − 1년)")
for i, k in enumerate(AS):
    print(f"    {NAME[k]:<9} {w1[i]:12.1%} {wH[i]:10.1%}   {100*(wH[i]-w1[i]):+6.1f}%p")
ceH = ce(wH, NM)
print(f"[3] 판정 — 수단을 뺀 최적 포트폴리오와 비교한 {H}년 확실성등가 기여(연율, 비용 차감 후)")
for i, k in enumerate(AS[1:], start=1):
    free = [j for j in ALL if j != i]; w_wo = optimize(NM, free); gain = (ceH - ce(w_wo, NM)) * 1e4
    wp = wH.copy(); wp[i] += 0.01; marg = (ce(wp, NM) - ceH) * 1e4
    hd = 100 * (wH[i] - w1[i]); ok = [abs(tval[k]) >= a.t_min, hd >= a.hd_min, gain > a.gain_min]
    mark = lambda b: "통과" if b else "탈락"
    print(f"    {NAME[k]:<9} 비용 {inst.cost_bp[k]:>3.0f}bp · 헤징 수요 {hd:+5.1f}%p · 기여 {gain:+6.1f}bp/년 (1%p 더 넣으면 {marg:+5.2f}bp) → ① {mark(ok[0])} · ② {mark(ok[1])} · ③ {mark(ok[2])}")
print(f"[4] 세 안의 {H}년 확실성등가 (연율, 비용 차감 후 · 각 안 안에서 비중 최적화, C는 변동성 헤지 5% 고정)")
wA = optimize(NM, [0]); wB = optimize(NM, [0, 1, 2])
def opt_fixed_vol():
    def f(z): return -logce(np.r_[z, 0.05], NM)
    r = minimize(f, wB[:3], bounds=BOUNDS[:3], method="L-BFGS-B"); return np.r_[r.x, 0.05]
wC = opt_fixed_vol(); ce1 = lambda w: ce(w, 12)
for nm, w in [("A 헤지 프로그램 없음", wA), ("B 장기 국채 + 물가연동채", wB), ("C B + 변동성 헤지 5%", wC)]:
    print(f"    {nm:<20} 주식 {w[0]:5.1%} · 장기 국채 {w[1]:5.1%} · 물가연동채 {w[2]:5.1%} · 변동성 헤지 {w[3]:4.1%}"
          f" → {H}년 CE {ce(w, NM)*100:5.2f}% (A 대비 {(ce(w, NM)-ce(wA, NM))*1e4:+5.0f}bp) · 1년 CE {ce1(w)*100:5.2f}%")
