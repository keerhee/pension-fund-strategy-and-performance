# -*- coding: utf-8 -*-
"""GBI 방법 3 — 몬테카를로로 필요 자본 K와 목표 달성 확률을 센다 (W06 M8 강의본 단원 ③).

가정(강의본 방법 1과 같음): 55세 · 금융자산 10억 · T = 10년 · 연 단위
  GHP: 실질 r = 2%(연 수익률 e^0.02 − 1 = 2.02%), 변동성 0
  주식: 연 로그수익 = r + λ − ½σ² + σ·ε, λ = 6%, σ = 20%  → 연 수익률 R = e^(로그수익) − 1
  목표: Safety 6억 · 95%(주식 0%) · Market 3억 · 70%(주식 67.08%) · Aspirational 5억 · 30%(주식 100%)

규칙(경로 하나에 해마다 적용):
  고정 비중 w — 연초에 주식 w · GHP 1 − w로 되돌리고, 한 해 수익을 반영한다
      W(t+1) = W(t) × [ w × (1 + R) + (1 − w) × (1 + r_GHP) ]
  CPPI(F, m) — ① floor F(t) = 목표 G의 현재가치 = G × e^(−r(T − t)) ② 쿠션 C = W − F
      ③ 위험 노출 E = m × C (0과 W 사이로 자름) ④ 나머지 W − E는 GHP ⑤ 한 해 수익 반영
  (Flexicure = floor를 매년 자산의 일정 비율로 다시 잡는 CPPI)

필요 자본 K: 후보 K마다 같은 경로 전체에 규칙을 적용해 W_T ≥ G인 경로의 비율(달성 확률)을 세고,
  비율 ≥ p인 가장 작은 K를 고른다(이분법 = 후보 구간을 반씩 좁힌다).
  ※ 경로마다 '가장 좋은 K'를 골라 다수결하는 것은 틀린 방법(미래를 안 뒤 고르는 사후 최적).
목표가 여럿이면 (i) 계좌를 나눠 목표별로 K를 구해 더하거나 (ii) 한 계좌의 후보(총자본 K, 주식 비중 w) 격자를 만들어
  후보마다 세 목표의 성공 비율을 같은 경로로 동시에 세고, 조건을 모두 만족하는 후보 중 K가 가장 작은 것을 고른다.

실행: python3 gbi_mc.py          # 본 계산 → gbi_mc_results.json
      python3 gbi_mc.py --demo   # 학습용: 경로 하나 3년 표 · 경로 10개 장난감 예 · 격자 예 (gbi_mc_demo.json)
numpy만 사용, 1초 안팎."""
import json, math, os, sys, time
import numpy as np

SEED, N, T = 2026, 100_000, 10
r, lam, sig = 0.02, 0.06, 0.20
RG = math.exp(r) - 1                                   # GHP 연 수익률 2.02%
GOALS = [("Safety", 6.0, 0.95, 1.645, 0.0), ("Market", 3.0, 0.70, 0.524, 0.6708), ("Aspirational", 5.0, 0.30, -0.524, 1.0)]
HERE = os.path.dirname(os.path.abspath(__file__))


def stock_returns(rng, n, kind="normal"):
    """연 주식 수익률 R (n 경로 × T년). kind='t5'면 연 충격을 자유도 5의 t분포(분산 1로 스케일)로."""
    if kind == "normal":
        e = rng.standard_normal((n, T))
    else:
        e = rng.standard_t(5, (n, T)) * math.sqrt(3 / 5)
    return np.exp(r + lam - 0.5 * sig * sig + sig * e) - 1


def run_fixed(W0, w, R, years=T):
    """고정 비중 규칙 — 반환: 해마다의 자산 (n × (years+1))."""
    W = np.empty((R.shape[0], years + 1)); W[:, 0] = W0
    for t in range(years):
        W[:, t + 1] = W[:, t] * (w * (1 + R[:, t]) + (1 - w) * (1 + RG))
    return W


def run_cppi(W0, G, m, R, years=T):
    """CPPI 규칙 — floor = 목표 G의 현재가치. 반환: 자산 경로와 해마다의 (F, C, E)."""
    n = R.shape[0]; W = np.empty((n, years + 1)); W[:, 0] = W0; rec = []
    for t in range(years):
        F = G * math.exp(-r * (T - t))
        C = W[:, t] - F
        E = np.clip(m * C, 0, W[:, t])
        W[:, t + 1] = E * (1 + R[:, t]) + (W[:, t] - E) * (1 + RG)
        rec.append((F, C, E))
    return W, rec


def k_min(G, p, growth):
    """같은 경로의 성장 배수 growth(= W_T / K)에서 달성 비율 ≥ p인 최소 K — 이분법."""
    lo, hi = 0.0, G * 10
    for _ in range(60):
        mid = (lo + hi) / 2
        if np.mean(mid * growth >= G) >= p: hi = mid
        else: lo = mid
    return hi


def k_closed(G, z, w):
    m = r + w * lam - 0.5 * w * w * sig * sig; s = w * sig
    return G * math.exp(-T * (m - z * s / math.sqrt(T)))


def main():
    t0 = time.time()
    out = {"seed": SEED, "N": N, "T": T, "rule": "고정 비중, 매년 되돌림", "goals": []}
    rng = np.random.default_rng(SEED)
    R = {"normal": stock_returns(rng, N, "normal"), "t5": stock_returns(rng, N, "t5")}
    for name, G, p, z, w in GOALS:
        row = {"goal": name, "G": G, "p": p, "w": w, "K_closed": k_closed(G, z, w)}
        for kind, Rk in R.items():
            g = run_fixed(1.0, w, Rk)[:, -1]
            pr = float(np.mean(row["K_closed"] * g >= G))
            row[kind] = {"K_mc": k_min(G, p, g), "p_at_K_closed": pr, "se": math.sqrt(pr * (1 - pr) / N)}
        out["goals"].append(row)
    cp = {}
    for kind, Rk in R.items():
        W, _ = run_cppi(10.0, 6.0, 3.0, Rk)
        F_path = np.array([6.0 * math.exp(-r * (T - t - 1)) for t in range(T)])
        breach = (W[:, 1:] < F_path - 1e-12).any(axis=1)
        A = W[:, -1]
        cp[kind] = {"P_W_ge_6": float(np.mean(A >= 6)), "P_W_ge_9": float(np.mean(A >= 9)),
                    "P_W_ge_14": float(np.mean(A >= 14)), "P_floor_breach": float(breach.mean()), "median_W": float(np.median(A))}
    out["cppi"] = {"A0": 10.0, "floor": "Safety 6억의 현재가치", "m": 3.0, **cp}
    out["seconds"] = round(time.time() - t0, 2)
    json.dump(out, open(os.path.join(HERE, "gbi_mc_results.json"), "w"), ensure_ascii=False, indent=1)
    for g in out["goals"]:
        print(f'{g["goal"]:12s} 닫힌 해 {g["K_closed"]:.3f} | MC {g["normal"]["K_mc"]:.3f} '
              f'(닫힌 해 K의 확률 {g["normal"]["p_at_K_closed"]:.4f} ± {g["normal"]["se"]:.4f}) | t5 {g["t5"]["K_mc"]:.3f}')
    print("CPPI", out["cppi"]); print("초", out["seconds"])


def demo():
    rng = np.random.default_rng(SEED)
    R = stock_returns(rng, N, "normal")          # 본 계산과 같은 난수 — 앞의 경로를 그대로 보여 준다
    d = {"seed": SEED}
    # A) 경로 1의 3년 — 고정 비중(Market 몫 2.24억, w 67.08%)과 CPPI(10억, floor = Safety + Market 9억의 현가, m = 3 — 설명용)
    path = R[:1, :3]
    Wf = run_fixed(2.24, 0.6708, path, 3)[0]
    d["A_fixed"] = [{"year": t + 1, "R": float(path[0, t]), "W0": float(Wf[t]), "stock": float(0.6708 * Wf[t]),
                     "ghp": float(0.3292 * Wf[t]), "W1": float(Wf[t + 1])} for t in range(3)]
    Wc, rec = run_cppi(10.0, 9.0, 3.0, path, 3)
    d["A_cppi"] = [{"year": t + 1, "R": float(path[0, t]), "W0": float(Wc[0, t]), "F": rec[t][0], "C": float(rec[t][1][0]),
                    "E": float(rec[t][2][0]), "ghp": float(Wc[0, t] - rec[t][2][0]), "W1": float(Wc[0, t + 1])} for t in range(3)]
    # B) 장난감 — 경로 10개 · Market(G 3억, p 70%) · 후보 K 2.0 · 2.2 · 2.4
    g10 = run_fixed(1.0, 0.6708, R[:10])[:, -1]
    d["B_paths"] = [float(x) for x in g10]
    d["B_hits"] = {str(K): int(np.sum(K * g10 >= 3.0)) for K in (2.0, 2.2, 2.4)}
    gN = run_fixed(1.0, 0.6708, R)[:, -1]
    d["B_full"] = {"K_mc": k_min(3.0, 0.70, gN), "K_closed": k_closed(3.0, 0.524, 0.6708)}
    # D) 격자 — 한 계좌(총자본 K, 주식 비중 w), 세 목표는 같은 날 우선순위대로 쌓는다(6 · 9 · 14억)
    grid = []
    for w in (0.2, 0.4, 0.6):
        g = run_fixed(1.0, w, R)[:, -1]
        for K in (7.5, 8.5):
            W = K * g
            ps = [float(np.mean(W >= 6)), float(np.mean(W >= 9)), float(np.mean(W >= 14))]
            grid.append({"w": w, "K": K, "pS": ps[0], "pM": ps[1], "pA": ps[2], "left": 10 - K,
                         "pass": ps[0] >= 0.95 and ps[1] >= 0.70 and ps[2] >= 0.30})
    d["D_grid"] = grid
    best = None
    for w in np.round(np.arange(0.0, 1.0001, 0.05), 2):
        g = run_fixed(1.0, float(w), R)[:, -1]
        for K in np.round(np.arange(6.0, 10.001, 0.1), 2):
            W = K * g
            if np.mean(W >= 6) >= 0.95 and np.mean(W >= 9) >= 0.70 and np.mean(W >= 14) >= 0.30:
                if best is None or K < best["K"]: best = {"w": float(w), "K": float(K)}
                break
    d["D_best"] = best
    gE = run_fixed(1.0, 0.6, R)[:, -1]
    d["D_edge"] = []
    for K in (7.1, 7.0):
        W = K * gE; ps = [float(np.mean(W >= 6)), float(np.mean(W >= 9)), float(np.mean(W >= 14))]
        d["D_edge"].append({"w": 0.6, "K": K, "pS": ps[0], "pM": ps[1], "pA": ps[2], "left": 10 - K,
                            "pass": ps[0] >= 0.95 and ps[1] >= 0.70 and ps[2] >= 0.30})
    d["D_grid_size"] = {"w": 21, "K": 41, "candidates": 21 * 41}
    # E) 우선순위 순서 — Safety는 GHP로 확정 → 남은 자금에서 Market K 이분법 → 남은 자금으로 Aspirational
    t0 = time.time()
    KS = k_closed(6.0, 1.645, 0.0); left = 10 - KS
    gM = run_fixed(1.0, 0.6708, R)[:, -1]; lo, hi, trials = 0.0, left, []
    while hi - lo > 0.005:
        mid = (lo + hi) / 2; pr = float(np.mean(mid * gM >= 3.0)); trials.append({"K": mid, "p": pr})
        if pr >= 0.70: hi = mid
        else: lo = mid
    KM = hi; left2 = left - KM
    gA = run_fixed(1.0, 1.0, R)[:, -1]
    pA_left = float(np.mean(left2 * gA >= 5.0)); KA = k_min(5.0, 0.30, gA)
    d["E_priority"] = {"K_S": KS, "left_after_S": left, "trials": trials, "K_M": KM, "left_after_M": left2,
                       "pA_with_left": pA_left, "K_A": KA, "total": KS + KM + KA, "spare": 10 - KS - KM - KA,
                       "searches": len(trials), "seconds": round(time.time() - t0, 3)}
    # F) 공통 난수 — 같은 후보(Market K 2.26억)를 다른 난수 1만 경로 두 묶음으로 세면 vs 같은 경로로 두 번 세면
    a1 = float(np.mean(2.26 * gM[:10000] >= 3)); a2 = float(np.mean(2.26 * gM[10000:20000] >= 3))
    b1 = float(np.mean(2.24 * gM[:10000] >= 3)); b2 = float(np.mean(2.24 * gM[10000:20000] >= 3))
    d["F_crn"] = {"K226_setA": a1, "K226_setB": a2, "K224_setA": b1, "K224_setB": b2}
    json.dump(d, open(os.path.join(HERE, "gbi_mc_demo.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(d, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else main()
