# -*- coding: utf-8 -*-
"""목표 확률을 최대로 하는 동적 포트폴리오 — Das · Ostrov · Radhakrishnan · Srivastav (2020) 2절 재현.

13 덱 'Claude Code로 2020 DP 구현' 장의 프롬프트가 만들 법한 정답 스크립트(numpy만, 1초 안).
  ① 효율선: 2018 식 (4) σ = √(aμ² + bμ + c), μ를 0.0526 ~ 0.0886에서 등간격 m개(기본 15)
  ② 격자: 식 (3)–(4)로 Wmin · Wmax(Z = ±3), ln W를 σmin/ρ 간격으로 깔고 W(0)이 격자점이 되게 아래로 민다
  ③ 전이확률: 식 (6) φ((ln(Wj/(Wi + C)) − (μ − σ²/2))/σ)를 j에 대해 정규화
  ④ Bellman: 식 (5) V(T) = 1{W ≥ G}, 식 (7) V(Wi, t) = max_μ Σj V(Wj, t+1) p(j | i, μ) — t = T−1 … 0
  ⑤ 앞으로 전파: 식 (8)로 해마다 자산 분포, P[W(T) ≥ 150] · P[W(T) ≥ G]
  ⑥ 납입 · 인출 C(t): 3.2절 파산 처리(Wi + C ≤ 0이면 가치 0, Wmin은 1로)
실행: python3 gbwm_dp.py [--rho 3] [--m 15] [--G 200] [--W0 100] [--T 10]
"""
import argparse, time
import numpy as np

MU = np.array([0.0493, 0.0770, 0.0886])                 # 원문 표 1 — 미국 채권 · 해외 주식 · 미국 주식
SIG = np.array([[0.0017, -0.0017, -0.0021],
                [-0.0017, 0.0396, 0.0309],
                [-0.0021, 0.0309, 0.0392]])


def frontier(mu, S):
    """효율선 상수 a · b · c와 μ → 비중 함수 (2018 식 (4), 2020 2.2절)."""
    Si, o = np.linalg.inv(S), np.ones(len(mu))
    k, l, p = mu @ Si @ o, mu @ Si @ mu, o @ Si @ o
    g = (l * Si @ o - k * Si @ mu) / (l * p - k * k)
    h = (p * Si @ mu - k * Si @ o) / (l * p - k * k)
    return h @ S @ h, 2 * g @ S @ h, g @ S @ g, (lambda x: g + h * x)


def grid(W0, T, mus, sigs, C, rho):
    """식 (3)–(4) + 2.3절. 파산 가능(하한 ≤ 0)이면 하한을 1로 둔다(3.2절)."""
    mn, mx, smin, smax = mus.min(), mus.max(), sigs.min(), sigs.max()
    lo = lambda d: (mn - smax ** 2 / 2) * d - 3 * smax * np.sqrt(d)
    hi = lambda d: (mx - smax ** 2 / 2) * d + 3 * smax * np.sqrt(d)
    Wlo = min(W0 * np.exp(lo(tau)) + sum(C[t] * np.exp(lo(tau - t)) for t in range(1, tau + 1)) for tau in range(T + 1))
    Whi = max(W0 * np.exp(hi(tau)) + sum(C[t] * np.exp(hi(tau - t)) for t in range(1, tau + 1)) for tau in range(T + 1))
    Wlo = Wlo if Wlo > 0 else 1.0
    step = smin / rho
    n = int(np.ceil((np.log(Whi) - np.log(Wlo)) / step - 1e-12))
    lg = np.log(Wlo) + step * np.arange(n + 1)
    k0 = int(np.ceil((np.log(W0) - np.log(Wlo)) / step - 1e-12))
    lg -= lg[k0] - np.log(W0)                               # W(0)이 격자점이 되게 가장 적게 아래로
    return np.exp(lg), k0


def trans(X, W, mu, sg):
    """출발 금액 X(벡터)에서 격자 W로 가는 정규화 전이확률 행렬."""
    z = (np.log(W)[None, :] - np.log(X)[:, None] - (mu - sg ** 2 / 2)) / sg
    e = -0.5 * z * z
    q = np.exp(e - e.max(1, keepdims=True))                 # 행 최댓값을 빼고 지수 — 아주 작은 X에서도 0으로 나누지 않는다
    return q / q.sum(1, keepdims=True)


def solve(W0, G, T, mus, sigs, C, rho):
    W, i0 = grid(W0, T, mus, sigs, C, rho)
    n = len(W)
    V = (W >= G).astype(float)                              # 식 (5)
    pol = np.zeros((T, n), int)
    Q = {}                                                  # 시점별 (포트폴리오 → 전이행렬) — 앞으로 전파에 재사용
    for t in range(T - 1, -1, -1):                           # 거꾸로 — 식 (7)
        X = W + C[t]
        ok = X > 0                                          # 3.2절: 인출 뒤 0 이하면 파산
        Qt = [trans(np.where(ok, X, 1.0), W, m, s) for m, s in zip(mus, sigs)]
        EV = np.array([q @ V for q in Qt])                  # (m, n)
        pol[t] = EV.argmax(0)
        V = np.where(ok, EV.max(0), 0.0)
        Q[t] = (Qt, ok)
    P = np.zeros(n); P[i0] = 1.0                            # 앞으로 — 식 (8)
    dist = [P.copy()]
    for t in range(T):
        Qt, ok = Q[t]
        nxt = np.zeros(n)
        for l in np.unique(pol[t]):
            idx = np.where(ok & (pol[t] == l))[0]
            nxt += P[idx] @ Qt[l][idx]
        P = nxt; dist.append(P.copy())
    return dict(W=W, i0=i0, V0=V[i0], pol=pol, P=P, dist=dist)


def fixed(W0, G, T, mus, sigs, rho):
    """15개 중 하나를 T년 고정했을 때의 목표 확률 — 비교용."""
    C = np.zeros(T + 1)
    W, i0 = grid(W0, T, mus, sigs, C, rho)
    out = []
    for m, s in zip(mus, sigs):
        q = trans(W, W, m, s)
        P = np.zeros(len(W)); P[i0] = 1.0
        for _ in range(T):
            P = P @ q
        out.append(P[W >= G].sum())
    return np.array(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rho", type=float, default=3.0)
    ap.add_argument("--m", type=int, default=15)
    ap.add_argument("--G", type=float, default=200.0)
    ap.add_argument("--W0", type=float, default=100.0)
    ap.add_argument("--T", type=int, default=10)
    a = ap.parse_args()
    t0 = time.time()
    A, B, Cc, wf = frontier(MU, SIG)
    mus = np.linspace(0.0526, 0.0886, a.m)
    sigs = np.sqrt(A * mus ** 2 + B * mus + Cc)
    print(f"효율선 a = {A:.4f} · b = {B:.4f} · c = {Cc:.5f} → 포트폴리오 {a.m}개, "
          f"σ {sigs[0]:.4f} ~ {sigs[-1]:.4f}")
    print(f"  0번 비중 {np.round(wf(mus[0]), 4)} · {a.m - 1}번 비중 {np.round(wf(mus[-1]), 4)}")
    T = a.T
    r = solve(a.W0, a.G, T, mus, sigs, np.zeros(T + 1), a.rho)
    W = r["W"]
    l0 = r["pol"][0][r["i0"]]
    print(f"격자 {len(W)}칸 · Wmin {W[0]:.2f} · Wmax {W[-1]:.0f}")
    print(f"기본 예: P[W(T) ≥ {a.G:.0f}] = {r['V0']:.3f} · P[W(T) ≥ 150] = {r['P'][W >= 150].sum():.3f} "
          f"· 시작 포트폴리오 {l0}번 (μ {mus[l0]:.4f}, σ {sigs[l0]:.4f})")
    fx = fixed(a.W0, a.G, T, mus, sigs, a.rho)
    print(f"비교: 한 포트폴리오 고정 최고 = {fx.max():.3f} ({fx.argmax()}번) → DP가 {100 * (r['V0'] - fx.max()):.1f}%p 높다")
    print("최적 포트폴리오 번호 — 자산이 적으면 공격적(14번), 많으면 보수적(0번):")
    for t in (0, 3, 6, 9):
        pl = r["pol"][t]
        j1 = np.argmax(pl < a.m - 1)                           # 가장 공격적인 번호를 처음 벗어나는 칸
        j0 = j1 + np.argmax(pl[j1:] == 0)                      # 그 위에서 처음 0번이 되는 칸
        print(f"  t = {t}: 자산 {W[j1]:.0f} 미만이면 {a.m - 1}번 · {W[j0]:.0f} 이상이면 0번(목표가 거의 확실한 구간)")
    print("납입 · 인출 C(t) (t = 1 … 9):")
    for c in (1, 3, 5, -1, -5, -10):
        C = np.r_[0.0, np.full(T - 1, c), 0.0]
        rc = solve(a.W0, a.G, T, mus, sigs, C, a.rho)
        Wc = rc["W"]
        print(f"  C = {c:+d}: P[≥ 150] = {rc['P'][Wc >= 150].sum():.3f} · P[≥ {a.G:.0f}] = {rc['V0']:.3f} "
              f"· 파산 {max(0.0, 1 - rc['P'].sum()):.3f}")
    print(f"걸린 시간 {time.time() - t0:.2f}초")


if __name__ == "__main__":
    main()
