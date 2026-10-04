#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""퇴직연금 디폴트옵션 계산 도구 — W06 팀 과제 4팀용

사용법
  python3 default_option_tool.py                         # 금리 3.0% · 원리금보장 3.09%에서 세 상품 비교
  python3 default_option_tool.py --rate 1.5 --guar 1.59  # 저금리
  python3 default_option_tool.py --rate 4.5 --guar 4.59  # 고금리
  python3 default_option_tool.py --cppi 0.9 2 0.5        # 임의의 CPPI (보장선 x, 승수 m, 총보수 %)
  python3 default_option_tool.py --tdf 0.6 0.6           # 임의의 혼합형 (주식 비중, 총보수 %)

가입자: 55세 · 적립금 1 · 65세 은퇴(10년). 안전 목표 G_S = 1.10, 원리금보장 목표 G_M = (1 + 원리금보장 수익률)^10.
모의실험 4,000개 경로 — 주식 수익률은 40년 모의 수익률 패널(교육용)에서 12개월 단위로 다시 뽑고, 채권 금리는 출발 금리 주변을 움직인다.

판정 기준
  ① 목표 미달     P(10년 뒤 적립금 < 1.10) ≤ 5%
  ② 원리금보장 이기기  P(10년 뒤 적립금 ≥ G_M) ≥ 70% (총보수 차감 후)
  ③ 위기 첫해      첫해에 2022형 위기(주식 −20% · 금리 +3%p)가 와도 P(10년 뒤 < 1.10) ≤ 10%
  ④ 안전자산 고착   CPPI가 한 번이라도 여유분 1% 미만으로 떨어져 주식을 못 사게 될 확률 ≤ 10% (CPPI만 해당)
"""
import argparse, os
import numpy as np, pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
P = pd.read_csv(f"{D}/do_params.csv").set_index("key").value
f = lambda k: float(P[k])
panel = pd.read_csv(f"{D}/do_panel_sim.csv")
ap = argparse.ArgumentParser()
ap.add_argument("--rate", type=float, default=f("ghp_y0"), help="10년 채권 금리 출발값 %")
ap.add_argument("--guar", type=float, default=f("market_alt_ret_pct"), help="원리금보장 수익률 %")
ap.add_argument("--cppi", type=float, nargs=3, default=None, metavar=("X", "M", "FEE"))
ap.add_argument("--tdf", type=float, nargs=2, default=None, metavar=("W_EQ", "FEE"))
a = ap.parse_args()

T = 120; NP = 4000; GS = 1.10; GM = (1 + a.guar / 100) ** 10; Y0 = a.rate
eq_m = panel.eq_ret.values; dy_m = np.r_[0, np.diff(panel.yield10.values)]
nb = len(eq_m) // 12
eqB = eq_m[: nb * 12].reshape(nb, 12); dyB = dy_m[: nb * 12].reshape(nb, 12)
rng = np.random.default_rng(int(f("panel_seed")))

def draw(shock):
    idx = rng.integers(0, nb, size=(NP, T // 12)); eq = eqB[idx].reshape(NP, T); dy = dyB[idx].reshape(NP, T)
    if shock:
        eq[:, :12] = np.array([-0.03, -0.02, -0.08, -0.04, 0.02, -0.06, 0.01, -0.03, 0.03, -0.02, 0.02, 0.005]); dy[:, :12] = 0.25
    return eq, dy
def zc(dy):
    y = np.zeros((dy.shape[0], T + 1)); y[:, 0] = Y0
    for t in range(T): y[:, t + 1] = np.clip(y[:, t] + dy[:, t] + 0.012 * (Y0 - y[:, t]), 0.3, None)
    return np.exp(-y / 100 * (T - np.arange(T + 1)) / 12)
def mixed(eq, dy, w, fee):
    Pz = zc(dy); W = np.ones(eq.shape[0])
    for t in range(T): W = W * (1 + w * eq[:, t] + (1 - w) * (Pz[:, t + 1] / Pz[:, t] - 1)) * (1 - fee / 1200)
    return W, np.zeros(eq.shape[0], bool), np.nan
def cppi(eq, dy, x, m, fee):
    Pz = zc(dy); W = np.ones(eq.shape[0]); trap = np.zeros(eq.shape[0], bool); Hp = Gp = None
    fg = (1 - fee / 1200) ** (-(T - np.arange(T + 1)))
    for t in range(T):
        F = x * GS * Pz[:, t] * fg[t]
        if t % 3 == 0:
            wgt = np.clip(m * (W - F) / W, 0, 1); Hp = wgt * W; Gp = W - Hp
            if t == 0: w0 = float(wgt.mean())
        Hp = Hp * (1 + eq[:, t]) * (1 - fee / 1200); Gp = Gp * (Pz[:, t + 1] / Pz[:, t]) * (1 - fee / 1200); W = Hp + Gp
        trap |= (W - x * GS * Pz[:, t + 1] * fg[t + 1]) / W < 0.01
    return W, trap, w0

eqN, dyN = draw(False); eqS, dyS = draw(True)
PRODUCTS = [("A 혼합형(TDF형) 주식 60%", "tdf", (0.6, 0.6)), ("B CPPI 보장형", "cppi", (0.9, 2, 0.5)), ("C CPPI 공격형", "cppi", (0.8, 4, 0.5))]
if a.cppi: PRODUCTS = [("사용자 CPPI", "cppi", tuple(a.cppi))]
if a.tdf: PRODUCTS = [("사용자 혼합형", "tdf", tuple(a.tdf))]

P0 = np.exp(-Y0 / 100 * 10)
print(f"=== 디폴트옵션 비교 — 채권 금리 {Y0}% · 원리금보장 {a.guar}% → G_M = {GM:.3f} · 10년 무이표채 가격 P(0,10) = e^(-10y) = {P0:.3f} ===")
print("기준: ① 목표 미달 ≤ 5% · ② 원리금보장 이기기 ≥ 70% · ③ 위기 첫해 목표 미달 ≤ 10% · ④ 안전자산 고착 ≤ 10%")
for name, kind, prm in PRODUCTS:
    if kind == "tdf":
        W, trap, w0 = mixed(eqN, dyN, *prm); Ws, _, _ = mixed(eqS, dyS, *prm); desc = f"주식 {prm[0]:.0%} 고정 · 총보수 {prm[1]}%"
    else:
        W, trap, w0 = cppi(eqN, dyN, *prm); Ws, _, _ = cppi(eqS, dyS, *prm)
        cushion = 1 - prm[0] * GS * P0 / (1 - prm[2] / 1200) ** 120   # 총보수만큼 보장선을 높여 둔다
        desc = f"보장선 {prm[0]:.0%} · 승수 {prm[1]:.0f} · 총보수 {prm[2]}% | 여유분 {cushion:.1%} → 첫 주식 비중 {w0:.0%}"
    c1, c2, c3 = (W < GS).mean(), (W >= GM).mean(), (Ws < GS).mean(); c4 = trap.mean() if kind == "cppi" else None
    ok = [c1 <= .05, c2 >= .70, c3 <= .10, (c4 <= .10) if c4 is not None else True]
    print(f"\n◆ {name}: {desc}")
    print(f"  10년 뒤 적립금 — 중앙값 {np.median(W):.2f} · 하위 10% {np.quantile(W, .1):.2f}")
    print(f"  ① 목표 미달 {c1:.1%} · ② 원리금보장 이기기 {c2:.0%} · ③ 위기 첫해 목표 미달 {c3:.1%} · ④ 안전자산 고착 " + (f"{c4:.1%}" if c4 is not None else "해당 없음"))
    print("  판정 " + " · ".join(f"{s} {'통과' if o else '탈락'}" for s, o in zip("①②③④", ok)) + f" → {'모두 통과' if all(ok) else '탈락 있음'}")
