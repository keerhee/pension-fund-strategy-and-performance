# -*- coding: utf-8 -*-
"""우선순위 순서로 목표 셋의 필요 자본을 몬테카를로로 찾는다 — W06 M8 강의본 54장 재현(실습 A · 55장)(정답 스크립트).

가정(gbi_mc.py와 같다)
  자산 10억 · 기간 T = 10년 · 연 단위 · 매년 비중을 되돌린다(이산 재조정)
  GHP: 실질 r = 2% → 연 수익률 e^0.02 − 1 = 2.02%, 변동성 0
  주식: 연 로그수익 = r + λ − ½σ² + σ·ε (λ = 6%, σ = 20%, ε ~ 표준정규) → 연 수익률 = e^(로그수익) − 1
  목표: Safety 6억 · 95%(GHP로 확정) → Market 3억 · 70%(주식 67.08%) → Aspirational 5억 · 30%(주식 100%)
절차
  ① Safety는 식으로 확정: K = G × e^(−rT)
  ② 남은 자금 안에서 Market K를 이분법으로 10번 — 시도마다 후보 K와 성공 비율(10년 뒤 자산 ≥ 3억인 경로 비율)
  ③ 남은 자금으로 Aspirational 달성 확률, 그리고 필요한 몫(이분법)
  ④ 합계 · 걸린 시간
  ⑤ 공통 난수 효과: 1만 경로 묶음을 바꿔 셀 때 vs 같은 경로
모든 후보에 같은 경로를 쓴다(공통 난수). 경로마다 최적 K를 골라 다수결하지 않는다.
실행: python3 priority_mc.py [--seed 2026] [--n 100000] [--p 0.95 0.70 0.30]   (numpy만)"""
import argparse, math, time
import numpy as np

T, R_GHP_LOG, LAM, SIG = 10, 0.02, 0.06, 0.20
RG = math.exp(R_GHP_LOG) - 1


def growth(R, w):
    """경로마다 10년 성장 배수 — 해마다 주식 w · GHP 1 − w로 되돌리고 한 해 수익을 반영한다."""
    g = np.ones(R.shape[0])
    for t in range(R.shape[1]):
        g *= w * (1 + R[:, t]) + (1 - w) * (1 + RG)
    return g


def bisect(G, p, g, lo, hi, n_iter, log=None):
    """성공 비율(K × g ≥ G) ≥ p인 가장 작은 K — 구간을 반씩 좁힌다."""
    for i in range(n_iter):
        mid = (lo + hi) / 2
        pr = float(np.mean(mid * g >= G))
        if log is not None: log.append((i + 1, mid, pr))
        if pr >= p: hi = mid
        else: lo = mid
    return hi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--n", type=int, default=100_000)
    ap.add_argument("--p", type=float, nargs=3, default=[0.95, 0.70, 0.30])
    a = ap.parse_args()
    pS, pM, pA = a.p
    t0 = time.time()
    rng = np.random.default_rng(a.seed)
    eps = rng.standard_normal((a.n, T))                              # 경로는 한 번만 만든다
    R = np.exp(R_GHP_LOG + LAM - 0.5 * SIG ** 2 + SIG * eps) - 1      # 연 주식 수익률(단순 수익률)

    # ① Safety — GHP는 변동성이 0이라 식으로 끝난다
    KS = 6.0 * math.exp(-R_GHP_LOG * T)
    left = 10.0 - KS
    print(f"1단계 Safety 6억 · {pS:.0%}: K = 6 × e^(−0.2) = {KS:.2f}억 (탐색 0회) → 남은 자금 {left:.2f}억")

    # ② Market — 남은 자금 [0, left] 안에서 이분법 10번
    gM = growth(R, 0.6708)
    log = []
    KM = bisect(3.0, pM, gM, 0.0, left, 10, log)
    print(f"2단계 Market 3억 · {pM:.0%}: 이분법 10회")
    for i, k, pr in log:
        print(f"   시도 {i:2d}  K = {k:.3f}억 → {pr:6.2%} {'≥' if pr >= pM else '<'} {pM:.0%}")
    left2 = left - KM
    print(f"   → K = {KM:.2f}억 · 남은 자금 {left2:.2f}억")

    # ③ Aspirational — 남은 자금의 달성 확률과 필요한 몫
    gA = growth(R, 1.0)
    pr_left = float(np.mean(left2 * gA >= 5.0))
    KA = bisect(5.0, pA, gA, 0.0, 50.0, 60)
    print(f"3단계 Aspirational 5억 · {pA:.0%}: 남은 {left2:.2f}억이면 달성 {pr_left:.1%} · 필요 K = {KA:.2f}억 → 여유 {left2 - KA:.2f}억")

    # ④ 합계
    print(f"합계 {KS:.2f} + {KM:.2f} + {KA:.2f} = {KS + KM + KA:.2f}억 · 걸린 시간 {time.time() - t0:.2f}초")

    # ⑤ 공통 난수 — 같은 후보를 다른 1만 경로 묶음으로 세면 흔들린다
    m = min(10_000, a.n // 2)
    for K in (2.26, 2.24):
        print(f"공통 난수 확인 K {K:.2f}억: 묶음 A {np.mean(K * gM[:m] >= 3):.2%} · 묶음 B {np.mean(K * gM[m:2 * m] >= 3):.2%}")
    se = math.sqrt(pM * (1 - pM) / a.n)
    print(f"표준오차(p {pM:.0%}, N {a.n:,}) = ±{se:.2%}")


if __name__ == "__main__":
    main()
