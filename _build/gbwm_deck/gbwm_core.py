#!/usr/bin/env python3
"""DORS(Das · Ostrov · Radhakrishnan · Srivastav) GBWM 연작 — 재계산용 공용 코어 (numpy만).

  frontier()        2018 식 (4)·(6) — σ² = aμ² + bμ + c 의 a · b · c (2020 · 2022 · EGP도 같은 식)
  grid_2020()       2020 2.3절 — ln W를 σmin/ρ 간격으로, W(0)이 격자점이 되게 아래로 민다
  grid_2022()       2022 2.4절 — imax개를 Wmin(파산 대용)~Wmax 로그 등간격, W(0)에 맞춰 민다
  solve()           Bellman 역산 + 앞으로 확률 전파(2020 식 (5)–(8) · 2022 식 (4)–(5))
  combine_goals()   2022 2.3절 — 같은 해 목표들의 비용 · 효용 벡터(조합 → 정렬 → 지배 제거)
"""
import itertools
import numpy as np

# 2020 표 1 · EGP 식 (4)–(5) — 미국 채권 · 해외 주식 · 미국 주식 (1998–2017)
MU3 = np.array([0.0493, 0.0770, 0.0886])
SIG3 = np.array([[0.0017, -0.0017, -0.0021],
                 [-0.0017, 0.0396, 0.0309],
                 [-0.0021, 0.0309, 0.0392]])     # 원문 표 1의 0.03086 은 대칭 0.0309 로 둔다(EGP 식 (5))


def frontier(mu=MU3, S=SIG3):
    """2018 식 (4): σ = √(aμ² + bμ + c). 반환 (a, b, c, 비중함수 w(μ))."""
    Si = np.linalg.inv(S)
    o = np.ones(len(mu))
    k, l, m = mu @ Si @ o, mu @ Si @ mu, o @ Si @ o
    g = (l * Si @ o - k * Si @ mu) / (l * m - k * k)
    h = (m * Si @ mu - k * Si @ o) / (l * m - k * k)
    a, b, c = h @ S @ h, 2 * g @ S @ h, g @ S @ g
    return a, b, c, (lambda x: g + h * x)


def sig_of(mu_, abc):
    a, b, c = abc[:3]
    return np.sqrt(a * mu_ ** 2 + b * mu_ + c)


def portfolios(n=15, mu_min=None, mu_max=0.0886, mu=MU3, S=SIG3):
    """효율선 위 μ 등간격 n개 (2020 · 2022 기본: 꼭짓점 μ ~ 0.0886)."""
    abc = frontier(mu, S)
    a, b, c, wf = abc
    if mu_min is None:
        mu_min = -b / (2 * a)                       # 꼭짓점(최소분산)
    mus = np.linspace(mu_min, mu_max, n)
    return mus, sig_of(mus, abc), np.array([wf(x) for x in mus])


def _snap(lo, hi, W0, step=None, n=None):
    """ln 등간격 격자를 만들고, W0가 격자점이 되도록 가장 적게 아래로 민다."""
    L0, L1, l0 = np.log(lo), np.log(hi), np.log(W0)
    if step is not None:
        K = int(np.ceil((L1 - L0) / step - 1e-12))
        lg = L0 + step * np.arange(K + 1)
    else:
        lg = np.linspace(L0, L1, n)
        step = lg[1] - lg[0]
    kk = int(np.ceil((l0 - L0) / step - 1e-12))
    shift = L0 + kk * step - l0
    lg = lg - shift
    i0 = kk
    return np.exp(lg), i0


def grid_2020(W0, T, mus, sigs, C=None, rho=3.0, h=1.0, wfloor=None):
    """2020 식 (3)–(4) + 2.3절. C[t] (t=0..T-1, C[0]=0) 는 미리 정한 납입(+) · 인출(−)."""
    C = np.zeros(T + 1) if C is None else np.asarray(C, float)
    mn, mx, smin, smax = mus.min(), mus.max(), sigs.min(), sigs.max()
    lo, hi = [], []
    for tau in range(T + 1):
        dlo = lambda d: (mn - smax ** 2 / 2) * h * d - 3 * smax * np.sqrt(h * d)
        dhi = lambda d: (mx - smax ** 2 / 2) * h * d + 3 * smax * np.sqrt(h * d)
        lo.append(W0 * np.exp(dlo(tau)) + sum(C[t] * np.exp(dlo(tau - t)) for t in range(1, tau + 1)))
        hi.append(W0 * np.exp(dhi(tau)) + sum(C[t] * np.exp(dhi(tau - t)) for t in range(1, tau + 1)))
    Wlo, Whi = min(lo), max(hi)
    if Wlo <= 0 or wfloor is not None:               # 3.2절 — 파산 가능하면 작은 양수로
        Wlo = wfloor if wfloor is not None else 1.0
    return _snap(Wlo, Whi, W0, step=smin * np.sqrt(h) / rho)


def grid_2022(W0, T, mus, sigs, imax, I=None, cmax=None, wb=1.0, h=1.0):
    """2022 식 (1)–(2) + 2.4절 — Wmin은 파산 대용 wb, Wmax는 식 (2)."""
    I = np.zeros(T + 1) if I is None else np.asarray(I, float)
    mx, smin, smax = mus.max(), sigs.min(), sigs.max()
    hi = []
    for t in range(T + 1):
        d = lambda x: (mx - smin ** 2 / 2) * h * x + 3 * smax * np.sqrt(h * x)
        hi.append(W0 * np.exp(d(t)) + sum(I[s] * np.exp(d(t - s)) for s in range(t + 1)))
    return _snap(wb, max(hi), W0, n=imax)


def combine_goals(goals):
    """2022 2.3절. goals = [[(cost, util), ...], ...] (각 목표의 선택지, (0,0) 포함).
    반환 cost · util 벡터와 각 칸이 어떤 선택 조합인지."""
    combos = []
    for pick in itertools.product(*[range(len(g)) for g in goals]):
        c = sum(goals[j][p][0] for j, p in enumerate(pick))
        u = sum(goals[j][p][1] for j, p in enumerate(pick))
        combos.append((c, u, pick))
    combos.sort(key=lambda z: (z[0], -z[1]))
    best = {}
    for c, u, pk in combos:                          # 같은 비용이면 효용이 큰 것만
        if c not in best or u > best[c][1]:
            best[c] = (c, u, pk)
    out, top = [], -np.inf
    for c in sorted(best):                           # 앞 칸보다 효용이 크지 않으면 버린다
        if best[c][1] > top:
            out.append(best[c]); top = best[c][1]
    return (np.array([o[0] for o in out], float), np.array([o[1] for o in out], float),
            [o[2] for o in out])


def _trans(X, W, mu, sg, h):
    """X(…)에서 한 기간 뒤 격자 W로 가는 정규화 전이확률 — 2020 식 (6) · 2022 3.1절."""
    lw = np.log(W)
    with np.errstate(divide="ignore", invalid="ignore"):
        z = (lw[None, :] - np.log(X)[:, None] - (mu - sg ** 2 / 2) * h) / (sg * np.sqrt(h))
    e = -0.5 * z * z
    q = np.exp(e - e.max(1, keepdims=True))         # 행 최댓값을 빼고 지수 — 아주 작은 X도 가장 가까운 칸으로
    return q / q.sum(1, keepdims=True)


def solve(W, i0, T, mus, sigs, VT, h=1.0, cash=None, goals=None, tdist=None):
    """Bellman 역산(식 (7) · 2022 식 (4))과 앞으로 전파(식 (8) · 2022 식 (5)).

    W      : 격자(imax), i0: W(0)의 위치, T: 마지막 시점, VT: 시점 T의 가치(격자 위)
    cash   : 길이 T+1 — 해마다 미리 정한 납입(+) · 인출(−) (2020 C(t) · 2022 I(t))
    goals  : {t: (cost 벡터, util 벡터)} — 2022 비용 · 효용 벡터(첫 칸 0, 0)
    반환    : dict(V0, Vt, L(포트폴리오 선택), K(목표 칸 선택), P(분포), pk{t: 칸별 확률}, bankrupt)
    """
    n = len(W)
    cash = np.zeros(T + 1) if cash is None else np.asarray(cash, float)
    goals = goals or {}
    V = np.asarray(VT, float).copy()
    Vt, L, K = [None] * (T + 1), np.zeros((T, n), int), np.zeros((T, n), int)
    Vt[T] = V.copy()
    for t in range(T - 1, -1, -1):
        cst, utl = goals.get(t, (np.zeros(1), np.zeros(1)))
        X = W[:, None] + cash[t] - cst[None, :]                     # (n, k) 투자 원금
        ok = X > 0
        Xc = np.where(ok, X, 1.0).ravel()
        best = np.full(X.shape, -np.inf); arg = np.zeros(X.shape, int)
        for l, (mu, sg) in enumerate(zip(mus, sigs)):              # 먼저 포트폴리오로 최적화(분할 최적화)
            ev = (_trans(Xc, W, mu, sg, h) @ V).reshape(X.shape)
            upd = ev > best + 1e-15
            best = np.where(upd, ev, best); arg = np.where(upd, l, arg)
        best = np.where(ok, best, 0.0)                              # 파산 → 이후 가치 0
        # 목표 칸: 낼 수 있는 비용만 (W + 현금흐름 ≥ 비용), 그다음 칸으로 최적화
        afford = (W[:, None] + cash[t] - cst[None, :]) >= -1e-12
        tot = np.where(afford, utl[None, :] + best, -np.inf)
        nk = tot.shape[1]
        kk = nk - 1 - np.argmax(tot[:, ::-1] >= tot.max(1, keepdims=True) - 1e-9, 1)   # 동률이면 지금 목표를 산다
        V = tot[np.arange(n), kk]
        V = np.where(np.isfinite(V), V, 0.0)
        K[t], L[t] = kk, arg[np.arange(n), kk]
        Vt[t] = V.copy()
    # 앞으로 전파
    P = np.zeros((T + 1, n)); P[0, i0] = 1.0
    pk, bankrupt = {}, np.zeros(T + 1)
    for t in range(T):
        cst, _ = goals.get(t, (np.zeros(1), np.zeros(1)))
        if t in goals:
            pk[t] = np.array([P[t][K[t] == k].sum() for k in range(len(cst))])
        X = W + cash[t] - cst[K[t]]
        alive = (X > 0) & (P[t] > 0)
        bankrupt[t] = P[t][(X <= 0) & (P[t] > 0)].sum()
        nxt = np.zeros(n)
        for l in np.unique(L[t][alive]):
            idx = np.where(alive & (L[t] == l))[0]
            q = _trans(X[idx], W, mus[l], sigs[l], h)
            nxt += P[t][idx] @ q
        P[t + 1] = nxt
    return dict(V0=Vt[0][i0], Vt=Vt, L=L, K=K, P=P, pk=pk, bankrupt=bankrupt)


def forward_joint(r, W, i0, T, mus, sigs, h=1.0, cash=None, goals=None):
    """최적 전략 아래 '지금까지 모든 목표를 샀다'의 확률(2022 표 8의 '목표를 내고도 지급 능력 유지')."""
    n = len(W)
    cash = np.zeros(T + 1) if cash is None else np.asarray(cash, float)
    goals = goals or {}
    A = np.zeros(n); A[i0] = 1.0                       # 지금까지 전부 산 경로의 질량
    B = np.zeros(n)                                    # 하나라도 못 산 경로
    out = {}
    for t in range(T):
        cst, _ = goals.get(t, (np.zeros(1), np.zeros(1)))
        kk = r["K"][t]
        if t in goals:
            took = kk > 0
            B = B + np.where(took, 0, A); A = np.where(took, A, 0)
            out[t] = A.sum()
        X = W + cash[t] - cst[kk]
        alive = X > 0
        nA, nB = np.zeros(n), np.zeros(n)
        for l in np.unique(r["L"][t][alive]):
            idx = np.where(alive & (r["L"][t] == l))[0]
            q = _trans(X[idx], W, mus[l], sigs[l], h)
            nA += A[idx] @ q; nB += B[idx] @ q
        A, B = nA, nB
    return out


def proximity(pfun, d, U0=None, it=80, tol=2e-3, dU0=None):
    """EGP 4.1절 근접점 알고리즘 — U_new = U_old + ΔU (d − p_old), 거리가 늘면 ΔU를 70%로.
    pfun(U) → 목표 확률 벡터 p. 반환 (p, U, 부호 거리(+ 부족 · − 초과), 반복 수)."""
    d = np.asarray(d, float)
    U = np.full(len(d), 100.0) if U0 is None else np.asarray(U0, float)
    p = pfun(U)
    dU = 0.99 * U.mean() if dU0 is None else dU0
    k = 0
    for k in range(it):
        while True:
            Un = np.maximum(U + dU * (d - p), 1e-3 * U.mean())
            pn = pfun(Un)
            if np.linalg.norm(d - pn) <= np.linalg.norm(d - p) + 1e-12 or dU < 1e-3:
                break
            dU *= 0.7
        U, p = Un, pn
        e = d - p
        if np.linalg.norm(e) < 1e-4:
            break
        sgn = 1.0 if e.sum() >= 0 else -1.0          # 부족이면 U ∥ (d − p), 초과면 U ∥ (p − d)
        if np.linalg.norm(U / np.linalg.norm(U) - sgn * e / np.linalg.norm(e)) < tol:
            break
    e = d - p
    dist = np.linalg.norm(e)
    return p, U, (dist if np.all(e >= -1e-9) or e.sum() > 0 else -dist), k + 1


def min_wealth(pfun_w, d, w_lo, w_hi, tol=2e-3, it=10, log=None):
    """EGP 4.2절 — 초기 자금을 입력, 근접점의 부호 거리를 출력으로 할선법."""
    U = None
    pts = []
    for x in (w_lo, w_hi):
        p, U, s, _ = proximity(lambda u: pfun_w(x, u), d, U0=U)
        pts.append((x, s, p, U))
        if log is not None: log.append((x, s, p, U))
    for _ in range(it):
        (x0, f0, *_), (x1, f1, *_) = pts[-2], pts[-1]
        if f1 == f0: break
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        p, U, s, _ = proximity(lambda u: pfun_w(x2, u), d, U0=pts[-1][3])
        pts.append((x2, s, p, U))
        if log is not None: log.append((x2, s, p, U))
        if abs(s) < tol: break
    return pts[-1]
