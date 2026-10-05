#!/usr/bin/env python3
"""DORS 연작 덱 — 원문 예를 numpy로 다시 계산해 numbers.json · arrays.npz에 남긴다(약 5~8분).
실행: <python> compute.py     → 그다음 assets.py → build.js
원문 값과 나란히 적어 두고(paper_*), 덱의 각주는 이 파일의 대조에서 나온다.
"""
import json, time
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from gbwm_core import (MU3, SIG3, frontier, portfolios, grid_2020, grid_2022, solve, combine_goals,
                       forward_joint, proximity, min_wealth, _trans)

T0 = time.time()
N, ARR = {}, {}


def tick(msg):
    print(f"[{time.time() - T0:6.1f}s] {msg}", flush=True)


# =============================================================== A. 2018 JOIM
pts = np.array([(0.158, 0.0902), (0.424, 0.225), (0.291, 0.158), (0.249, 0.136), (0.0791, 0.0500),
                (0.119, 0.0704), (0.0108, 0.00829), (0.153, -0.0669)])      # 원문 그림 9–13의 (σ, μ)
s_, m_ = pts[:, 0], pts[:, 1]
(a18, b18, c18), *_ = np.linalg.lstsq(np.c_[m_ * m_, m_, np.ones_like(m_)], s_ * s_, rcond=None)
sig18 = lambda M: np.sqrt(a18 * M * M + b18 * M + c18)
t18, gr18, gl18 = 10, np.log(500 / 400) / 10, np.log(300 / 400) / 10
z18 = lambda S, M, g: (M - S * S / 2 - g) * np.sqrt(t18) / S


def cubic(a, b, c, g):
    """2018 식 (8): c3 μ³ + c2 μ² + c1 μ + c0 = 0."""
    co = [a * a, 1.5 * a * b, a * c + b * b / 2 - b - 2 * a * g, b * c / 2 - 2 * c - b * g]
    return co, np.sort(np.roots(co).real)[::-1]


co18, roots18 = cubic(a18, b18, c18, gr18)
mu_o = roots18[0]
f80 = lambda M: z18(sig18(M), M, gr18) - norm.ppf(0.8)
mu_u = brentq(f80, mu_o, 0.4); mu_l = brentq(f80, -b18 / 2 / a18 + 1e-6, mu_o)
mu_lt = brentq(lambda M: z18(sig18(M), M, gl18) - norm.ppf(0.95), mu_o, 0.4)
half_s = (sig18(mu_o) + sig18(mu_u)) / 2
mu_half = brentq(lambda M: sig18(M) - half_s, mu_o, mu_u)
N["y2018"] = dict(abc=[a18, b18, c18], vertex=[float(sig18(-b18 / 2 / a18)), -b18 / 2 / a18],
                  resid=list(np.round(sig18(m_) - s_, 5)), cubic=co18, roots=list(roots18),
                  ogpp=[float(sig18(mu_o)), mu_o, float(norm.cdf(z18(sig18(mu_o), mu_o, gr18)))],
                  other_tangent=[[float(sig18(r)), r] for r in roots18[1:]],
                  ugp=[float(sig18(mu_u)), mu_u], lgp=[float(sig18(mu_l)), mu_l],
                  ltp=[float(sig18(mu_lt)), mu_lt], half=[half_s, mu_half],
                  p_at_paper_ltp=float(norm.cdf(z18(0.249, 0.136, gl18))),
                  p_at_paper_ugp=float(norm.cdf(z18(0.424, 0.225, gr18))),
                  intercept=gr18,
                  paper=dict(ogpp=[0.158, 0.0902, 0.866], ugp=[0.424, 0.225], half=[0.291, 0.158],
                             ltp=[0.249, 0.136], tangents=[[0.0108, 0.00829], [0.153, -0.0669]]))
# 자산이 줄면 최적점이 오른쪽으로 — W(0)을 바꿔 가며
w0s = np.linspace(300, 500, 21)
sens = []
for w0 in w0s:
    g = np.log(500 / w0) / 10
    _, rr = cubic(a18, b18, c18, g)
    M = rr[0]; sens.append([w0, float(sig18(M)), M, float(norm.cdf(z18(sig18(M), M, g)))])
N["y2018"]["w0_sens"] = sens
tick("2018 done")

# 2020 효율선 위에서 정적 해 (EGP 2절 · 2020 기본 예)
A20, B20, C20, wf20 = frontier()
EGPs = []
for W0, Wt, t in [(100, 125, 5), (100, 150, 6), (100, 200, 10)]:
    g = np.log(Wt / W0) / t
    _, rr = cubic(A20, B20, C20, g)
    M = rr[0]; S = np.sqrt(A20 * M * M + B20 * M + C20)
    EGPs.append([W0, Wt, t, M, S, float(norm.cdf((M - S * S / 2 - g) * np.sqrt(t) / S))])
N["static20"] = dict(cases=EGPs, paper=[[0.0580, 0.0471, 0.72], [0.0859, 0.1812, 0.51]])

# =============================================================== B. 2020 CMS
mus, sigs, wts = portfolios(mu_min=0.0526)
N["y2020"] = dict(abc=[A20, B20, C20], vertex=[float(np.sqrt(C20 - B20 ** 2 / 4 / A20)), -B20 / 2 / A20],
                  mus=list(mus), sigs=list(sigs), w=wts.tolist(),
                  paper=dict(w0=[0.9098, 0.0225, 0.0677], w14=[0.0731, -0.2470, 1.1738], sig_min=0.0374,
                             sig_max=0.1954, nodes=327, Wmin=21.72, Wmax=1269, P200=0.669, P150=0.777,
                             mu0=0.0835, sig0=0.1686))
T = 10
t1 = time.time()
W, i0 = grid_2020(100, T, mus, sigs)
r = solve(W, i0, T, mus, sigs, (W >= 200).astype(float))
rt = time.time() - t1
N["y2020"].update(nodes=len(W), Wmin=W[0], Wmax=W[-1], P200=r["V0"], P150=float(r["P"][-1][W >= 150].sum()),
                  l0=int(r["L"][0][i0]), mu0=mus[r["L"][0][i0]], sig0=sigs[r["L"][0][i0]], runtime=rt)
ARR.update(W20=W, V20=np.array(r["Vt"][:T]), L20=r["L"], P20=r["P"])


def evalpol(L, W, i0, T, mus, sigs):
    P = np.zeros(len(W)); P[i0] = 1
    for t in range(T):
        nxt = np.zeros(len(W))
        for l in np.unique(L[t]):
            idx = np.where((L[t] == l) & (P > 0))[0]
            if len(idx): nxt += P[idx] @ _trans(W[idx], W, mus[l], sigs[l], 1)
        P = nxt
    return P


fixed = [float(evalpol(np.full((T, len(W)), l), W, i0, T, mus, sigs)[W >= 200].sum()) for l in range(15)]
Ls = np.zeros((T, len(W)), int)
for t in range(T):
    tau = T - t
    zz = (mus[None, :] - sigs[None, :] ** 2 / 2 - np.log(200 / W)[:, None] / tau) * np.sqrt(tau) / sigs[None, :]
    Ls[t] = zz.argmax(1)
rep = float(evalpol(Ls, W, i0, T, mus, sigs)[W >= 200].sum())
N["y2020"].update(fixed=fixed, repeated_static=rep, oneshot_static=EGPs[2][5])
# 민감도 — 포트폴리오 수 m · 격자 밀도 ρ (원문 표 2–3)
sm, sr = [], []
for m in (5, 10, 15, 20, 40):
    mu_, sg_, _ = portfolios(n=m, mu_min=0.0526)
    t1 = time.time(); Wm, im = grid_2020(100, T, mu_, sg_)
    rm = solve(Wm, im, T, mu_, sg_, (Wm >= 200).astype(float))
    sm.append([m, time.time() - t1, float(rm["P"][-1][Wm >= 150].sum()), rm["V0"]])
for rho in (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6):
    t1 = time.time(); Wm, im = grid_2020(100, T, mus, sigs, rho=rho)
    rm = solve(Wm, im, T, mus, sigs, (Wm >= 200).astype(float))
    sr.append([rho, time.time() - t1, float(rm["P"][-1][Wm >= 150].sum()), rm["V0"], len(Wm)])
N["y2020"].update(sens_m=sm, sens_rho=sr,
                  paper_m=[[5, .775, .665], [10, .776, .668], [15, .777, .669], [20, .777, .669], [40, .777, .669]],
                  paper_rho=[[1, .777, .662], [1.5, .776, .673], [2, .780, .676], [2.5, .773, .666], [3, .777, .669],
                             [3.5, .780, .673], [4, .779, .674], [4.5, .778, .669], [5, .777, .670], [5.5, .779, .673],
                             [6, .778, .668]])
tick("2020 base + sens done")
# 납입 · 인출 (표 5 · 6)
cf = []
for Cv in (0, 1, 2, 3, 4, 5, -1, -5, -10, -15, -20):
    C = np.r_[0, np.full(T - 1, Cv), 0.0]
    Wc, ic = grid_2020(100, T, mus, sigs, C=C)
    rc = solve(Wc, ic, T, mus, sigs, (Wc >= 200).astype(float), cash=C)
    cf.append([Cv, max(0.0, 1 - rc["P"][-1].sum()), float(rc["P"][-1][Wc >= 150].sum()), rc["V0"]])
N["y2020"]["cashflow"] = cf
N["y2020"]["paper_cashflow"] = [[0, 0, .777, .669], [1, 0, .832, .730], [2, 0, .881, .789], [3, 0, .926, .848],
                                [4, 0, .961, .901], [5, 0, .984, .944], [-1, 0, .720, .609], [-5, .002, .491, .387],
                                [-10, .124, .246, .182], [-15, .492, .099, .072], [-20, .796, .034, .021]]
# 은퇴 예 · TDF (표 7 · 8)
T30, G30 = 30, 50 * 1.03 ** 30
glide = [(50, 54, [.27, .29, .44]), (55, 59, [.34, .26, .40]), (60, 64, [.42, .23, .35]),
         (65, 69, [.53, .19, .28]), (70, 74, [.67, .13, .20]), (75, 80, [.70, .12, .18])]
gw = lambda age: next(np.array(w) for lo, hi, w in glide if lo <= age <= hi)
Z = np.random.default_rng(2026).standard_normal((200_000, T30))
ret = []
for c in (0, 5, 10, 15, 20, 25, 30, 35, 40):
    C = np.zeros(T30 + 1)
    for t in range(1, 16): C[t] = c * 1.03 ** t
    for t in range(16, 30): C[t] = -50 * 1.03 ** t
    Wr, ir = grid_2020(100, T30, mus, sigs, C=C, wfloor=1.0)
    rr = solve(Wr, ir, T30, mus, sigs, (Wr >= G30).astype(float), cash=C)
    X = np.full(Z.shape[0], 100.0); alive = np.ones(Z.shape[0], bool)
    for t in range(T30):
        X = X + C[t]; alive &= X > 0; X = np.where(alive, X, 0)
        w = gw(50 + t); m = w @ MU3; s = np.sqrt(w @ SIG3 @ w)
        X = X * np.exp(m - s * s / 2 + s * Z[:, t])
    ret.append([c, rr["V0"], float(np.mean(alive & (X >= G30)))])
    if c == 15:
        ARR.update(Wret=Wr, Pret=rr["P"])
N["y2020"]["retire"] = ret
N["y2020"]["paper_retire"] = [[0, .128, .007], [5, .258, .039], [10, .420, .119], [15, .586, .266], [20, .735, .450],
                              [25, .854, .627], [30, .938, .770], [35, .984, .866], [40, .998, .928]]
N["y2020"]["G30"] = G30
tick("2020 cashflow + retire done")
# 한국 DC · IRP 위험자산 70% 한도 — 주식 비중(해외 + 미국) ≤ 70%로 μmax를 자른다(강의 재계산)
eq_share = lambda M: float(wf20(M)[1:].sum())
mu_cap = brentq(lambda M: eq_share(M) - 0.70, 0.0526, 0.0886)
mus_k, sigs_k, _ = portfolios(mu_min=0.0526, mu_max=mu_cap)
Wk, ik = grid_2020(100, T, mus_k, sigs_k)
rk = solve(Wk, ik, T, mus_k, sigs_k, (Wk >= 200).astype(float))
N["korea"] = dict(mu_cap=mu_cap, sig_cap=float(np.sqrt(A20 * mu_cap ** 2 + B20 * mu_cap + C20)),
                  w_cap=wf20(mu_cap).tolist(), P200_cap=rk["V0"], eq_at_max=eq_share(0.0886))
tick("korea done")

# =============================================================== C. 손계산 — 2기간 · 5칸 · 포트폴리오 둘
PH = [(0.0526, 0.0374), (0.0886, 0.1954)]                      # 원문 μmin · μmax 끝점(σ는 원문 값)
Wh = 100 * np.exp(0.15 * np.arange(-2, 3)); Gh = 110
V2 = (Wh >= Gh).astype(float)
Qh = [_trans(Wh, Wh, m, s, 1) for m, s in PH]
E1 = np.array([q @ V2 for q in Qh]); V1 = E1.max(0); c1 = E1.argmax(0)
E0 = np.array([q[2] @ V1 for q in Qh])
zB = (np.log(Wh / 100) - (PH[1][0] - PH[1][1] ** 2 / 2)) / PH[1][1]
fixedA = Qh[0][2] @ (Qh[0] @ V2); fixedB = Qh[1][2] @ (Qh[1] @ V2)
N["hand"] = dict(W=list(Wh), G=Gh, P=PH, E1=E1.tolist(), V1=list(V1), c1=list(map(int, c1)), E0=list(E0),
                 zB=list(zB), phiB=list(np.exp(-0.5 * zB * zB)), qB=list(Qh[1][2]), qA=list(Qh[0][2]),
                 fixedA=float(fixedA), fixedB=float(fixedB))
tick("hand done")

# =============================================================== D. 2022 JBF
T = 11
W22, i22 = grid_2022(100, T, mus, sigs, 475)
tab2 = []
for c5, c10 in [(100, 150), (150, 100)]:
    for u5, u10 in [(1000, 1000), (1000, 2000), (1000, 3000), (2000, 1000), (2000, 2000), (2000, 3000),
                    (3000, 1000), (3000, 2000), (3000, 3000)]:
        g = {5: (np.array([0., c5]), np.array([0., u5])), 10: (np.array([0., c10]), np.array([0., u10]))}
        rg = solve(W22, i22, T, mus, sigs, np.zeros(len(W22)), goals=g)
        tab2.append([c5, c10, u5, u10, rg["V0"], float(rg["P"][5][W22 >= c5].sum()), float(rg["pk"][5][1]),
                     float(rg["pk"][10][1])])
        if (c5, u5, u10) == (100, 2000, 3000):
            k5 = rg["K"][5]
            sw = [float(W22[i + 1]) for i in np.where(np.diff(k5) != 0)[0]]
            # 시점 5에서 산다 · 건너뛴다의 가치 차이 (자산 80 ~ 260)
            cst, utl = g[5]
            ev = {}
            for kk in (0, 1):
                X = W22 - cst[kk]; ok = X > 0
                best = np.full(len(W22), -np.inf)
                for mu_, sg_ in zip(mus, sigs):
                    best = np.maximum(best, _trans(np.where(ok, X, 1.0), W22, mu_, sg_, 1) @ rg["Vt"][6])
                ev[kk] = np.where(ok, best + utl[kk], -np.inf)
            ARR.update(W22=W22, take=ev[1], forgo=ev[0])
            N["y2022_switch"] = sw
N["y2022_tab2"] = tab2
N["y2022_tab2_paper"] = [[100, 150, 1000, 1000, 1168, .893, .893, .275], [100, 150, 1000, 2000, 1855, .917, .123, .866],
                         [100, 150, 1000, 3000, 2757, .969, .009, .916], [100, 150, 2000, 1000, 2110, .969, .969, .171],
                         [100, 150, 2000, 2000, 2336, .893, .893, .275], [100, 150, 2000, 3000, 2886, .849, .298, .764],
                         [100, 150, 3000, 1000, 3087, .984, .984, .134], [100, 150, 3000, 2000, 3259, .950, .950, .205],
                         [100, 150, 3000, 3000, 3504, .893, .893, .275],
                         [150, 100, 1000, 1000, 1185, .398, .398, .787], [150, 100, 1000, 2000, 2137, .358, .186, .976],
                         [150, 100, 1000, 3000, 3120, .340, .163, .986], [150, 100, 2000, 1000, 1631, .493, .493, .644],
                         [150, 100, 2000, 2000, 2370, .398, .398, .787], [150, 100, 2000, 3000, 3306, .373, .210, .962],
                         [150, 100, 3000, 1000, 2155, .544, .544, .524], [150, 100, 3000, 2000, 2792, .449, .449, .723],
                         [150, 100, 3000, 3000, 3555, .398, .398, .787]]
N["y2022_grid"] = dict(nodes=len(W22), Wmin=W22[0], Wmax=W22[-1], paper_Wmax=1834)
tick("2022 tab2 done")
# 일곱 목표 (표 3 · 표 4 Run 1 · 7)
G7 = [(5, 25), (8, 17), (10, 15), (11, 80), (17, 50), (22, 60), (24, 130)]
U1 = [1000, 2500, 500, 1500, 300, 3000, 2000]
U7 = [1200, 760, 425, 2700, 700, 2900, 2070]
T = 25


def seven(W0, U, inf=None):
    I = np.zeros(T + 1) if inf is None else inf
    Wg, ig = grid_2022(W0, T, mus, sigs, 556, I=I)
    g = {t: (np.array([0., c]), np.array([0., u])) for (t, c), u in zip(G7, U)}
    rg = solve(Wg, ig, T, mus, sigs, np.zeros(len(Wg)), cash=I, goals=g)
    return rg["V0"], [float(rg["pk"][t][1]) for t, _ in G7], Wg


v1, p1, Wg = seven(30, U1)
I7 = np.zeros(T + 1); I7[1:7] = 3; I7[7:T] = 2
v7, p7, _ = seven(50, U7, I7)
N["y2022_seven"] = dict(V=v1, p=p1, frac=v1 / sum(U1), Wmax=Wg[-1], V7=v7, p7=p7,
                        paper=dict(V=5415, p=[.0446, .9871, .2077, .0316, .0192, .7569, .2373],
                                   p7=[.6237, .9914, .3150, .6046, .3072, .9902, .6027], Wmax=5026))
# 같은 해 목표 셋 + 10년 목표 (표 5)
c5, u5, map5 = combine_goals([[(0, 0), (7, 100)], [(0, 0), (9, 90), (20, 300)],
                              [(0, 0), (10, 40), (20, 250), (30, 400), (40, 500)]])
c10, u10, _ = combine_goals([[(0, 0), (50, 500), (90, 1000)]])
T = 11
Wc, ic = grid_2022(50, T, mus, sigs, 419)
rc = solve(Wc, ic, T, mus, sigs, np.zeros(len(Wc)), goals={5: (c5, u5), 10: (c10, u10)})
N["y2022_conc"] = dict(cost=list(c5), util=list(u5), V=rc["V0"], pk5=list(rc["pk"][5]), pk10=list(rc["pk"][10]),
                       paper=dict(V=1013, pk10=[.4187, .2137, .3676],
                                  pk5=[.0198, .0554, .0012, .1547, .2240, .0109, .0267, .0672, .0073, .0394, .1162,
                                       .1938, .0834]))
tick("2022 seven + conc done")
# 은퇴 세 목표 · TDF (표 8) — '앞 목표를 모두 내고도 지급 능력 유지' 확률
T = 61
I = np.zeros(T + 1)
for t in range(1, 35): I[t] = 10 * 1.03 ** t
for t in range(35, T): I[t] = 80 * 1.03 ** (t - 35)
g3 = {35: (np.array([0., 2500]), np.array([0., 4.])), 50: (np.array([0., 3000]), np.array([0., 2.])),
      60: (np.array([0., 4000]), np.array([0., 1.]))}
Wt, it = grid_2022(100, T, mus, sigs, 1000, I=I)
rt8 = solve(Wt, it, T, mus, sigs, np.zeros(len(Wt)), cash=I, goals=g3)
dpj = forward_joint(rt8, Wt, it, T, mus, sigs, cash=I, goals=g3)
glide8 = [(35, 44, [.10, .27, .63]), (45, 49, [.15, .25, .60]), (50, 54, [.22, .23, .55]), (55, 59, [.30, .20, .50]),
          (60, 64, [.37, .18, .45]), (65, 69, [.46, .16, .38]), (70, 74, [.59, .12, .29]), (75, 96, [.70, .09, .21])]
gw8 = lambda age: next(np.array(w) for lo, hi, w in glide8 if lo <= age <= hi)
rng = np.random.default_rng(2026); n = 200_000
X = np.full(n, 100.0); allp = np.ones(n, bool); tdf = {}
for t in range(T):
    X = X + I[t]
    if t in g3:
        ok = X >= g3[t][0][1]; X = np.where(ok, X - g3[t][0][1], X); allp &= ok; tdf[t] = float(allp.mean())
    w = gw8(35 + t); m = w @ MU3; s = np.sqrt(w @ SIG3 @ w)
    X = X * np.exp(m - s * s / 2 + s * rng.standard_normal(n))
N["y2022_retire"] = dict(dp=[dpj[t] for t in (35, 50, 60)], tdf=[tdf[t] for t in (35, 50, 60)],
                         paper_dp=[.782, .746, .713], paper_tdf=[.639, .559, .449])
tick("2022 retire done")
# 목표 수에 따른 계산 시간 — 해마다 목표 하나씩(25년 · 556칸)
T = 25
scal = []
for ng in (1, 3, 6, 12, 24):
    ts = np.linspace(1, 24, ng).round().astype(int)
    g = {int(t): (np.array([0., 10.]), np.array([0., 100.])) for t in ts}
    Wg, ig = grid_2022(100, T, mus, sigs, 556)
    t1 = time.time(); solve(Wg, ig, T, mus, sigs, np.zeros(len(Wg)), goals=g); scal.append([ng, time.time() - t1])
N["scaling"] = scal
tick("scaling done")

# =============================================================== E. EGP — 두 목표 프런티어 · 근접점 · 최소 초기 자금
T = 21


def imax_for(W0):
    return int(round(63 * np.log(W0 * np.exp((0.0886 - 0.0374 ** 2 / 2) * T + 3 * 0.1954 * np.sqrt(T)))))


cache = {}


def p2(W0, U):
    key = (round(W0, 5), round(float(U[0]), 6), round(float(U[1]), 6))
    if key not in cache:
        Wg, ig = grid_2022(W0, T, mus, sigs, imax_for(W0))
        g = {10: (np.array([0., 100]), np.array([0., U[0]])), 20: (np.array([0., 150]), np.array([0., U[1]]))}
        rg = solve(Wg, ig, T, mus, sigs, np.zeros(len(Wg)), goals=g)
        cache[key] = (np.array([rg["pk"][10][1], rg["pk"][20][1]]), int(rg["L"][0][ig]))
    return cache[key]


def sweep(W0, n=23):
    out = []
    for th in np.linspace(0, np.pi / 2, n):
        U = np.array([np.cos(th), np.sin(th)]) * 100
        p, l0 = p2(W0, np.maximum(U, 1e-6))
        out.append([float(th), float(p[0]), float(p[1]), l0])
    return out


d = np.array([0.7, 0.8])
fr50 = sweep(50)
tick("EGP sweep 50")
pp, Upp, sd, kk = proximity(lambda U: p2(50, U)[0], d)
tick("EGP prox 50")
log = []
xm, sm_, pm, Um = min_wealth(lambda W0, U: p2(W0, U)[0], d, 50.0, 100.0, log=log)
tick("EGP min W0")
fr_min = sweep(xm); fr100 = sweep(100)
N["egp"] = dict(fr50=fr50, fr_min=fr_min, fr100=fr100, prox50=list(pp), U50=list(Upp / Upp[0] * 100), dist50=sd,
                minW=xm, p_min=list(pm), U_min=list(Um / Um[0] * 100),
                secant=[[float(x), float(s)] for x, s, *_ in log],
                single=[], paper=dict(p2max=.875, p1max=.709, p2_at_p1max=.197, l0=[6, 14, 11], prox50=[.4894, .5828],
                                      dist50=.3025, prox100=[.814, .922], minW=79.9, U_min=[100, 108.47]))
# 한 목표만 — 10년 두 배 · 20년 세 배 (2020 단일 목표 DP, 목표 시점 관례 점검)
for G, TT in [(100, 10), (150, 20), (100, 11), (150, 21)]:
    Wg, ig = grid_2020(50, TT, mus, sigs)
    rg = solve(Wg, ig, TT, mus, sigs, (Wg >= G).astype(float))
    N["egp"]["single"].append([G, TT, rg["V0"], int(rg["L"][0][ig])])
tick("EGP done")

# =============================================================== F. M8 대입 — 55세 · 세 목표 6 · 9 · 14억 · 10년
wq = np.linspace(0, 1, 21); mu8 = 0.02 + 0.06 * wq; sg8 = np.maximum(0.2 * wq, 0.004)
T = 10; tgt = np.array([0.95, 0.70, 0.30])


def p8(W0, U, wcap=1.0):
    m = wq <= wcap + 1e-9
    Wg, ig = grid_2022(W0, T, mu8[m], sg8[m], 400, wb=0.5)
    VT = U[0] * (Wg >= 6) + U[1] * (Wg >= 9) + U[2] * (Wg >= 14)
    rg = solve(Wg, ig, T, mu8[m], sg8[m], VT)
    PT = rg["P"][-1]
    return np.array([PT[Wg >= 6 - 1e-9].sum(), PT[Wg >= 9 - 1e-9].sum(), PT[Wg >= 14 - 1e-9].sum()]), rg, Wg, ig


log8 = []
x8, s8, pr8, U8 = min_wealth(lambda W0, U: p8(W0, U)[0], tgt, 6.0, 8.0, log=log8)
_, r8, W8, i8 = p8(x8, U8)
pc, Uc, sc, _ = proximity(lambda U: p8(x8, U, 0.7)[0], tgt, U0=U8)
p71, *_ = p8(7.1, U8)
N["m8"] = dict(minW=x8, p=list(pr8), U=list(U8 / U8[0]), secant=[[float(x), float(s)] for x, s, *_ in log8],
               w0_choice=float(wq[r8["L"][0][i8]]), cap70_at_minW=list(pc), p_at_71=list(p71),
               paper=dict(sep=9.13, one_account=7.1))
ARR.update(W8=W8, L8=r8["L"])
tick("M8 done")

json.dump(N, open("numbers.json", "w"), indent=1, ensure_ascii=False, default=float)
np.savez_compressed("arrays.npz", **ARR)
tick("saved numbers.json · arrays.npz")
