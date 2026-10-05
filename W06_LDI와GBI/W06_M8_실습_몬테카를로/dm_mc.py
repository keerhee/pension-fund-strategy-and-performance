# -*- coding: utf-8 -*-
"""방법 2(Das–Markowitz) 문제를 몬테카를로로 푼다 — 식 대신 '센다' (W06 M8 강의본 단원 ③ 방법 3).

문제(계좌마다): 미달 확률 P(R < H) ≤ α 안에서 기대수익이 가장 큰 비중 w (비중 합 1)
자산(원 논문 예): 채권 · 저위험 주식 · 고위험 주식 — 기대수익 5 · 10 · 25%, 표준편차 5 · 20 · 50%, 두 주식 상관 0.2
절차: ① 1년 수익률 표본 N = 200,000을 한 번만 만든다(공통 난수)
      ② 후보 비중을 정한다 — (a) 격자: 공매도 허용 −100~200%(2%p 간격 → 근처 0.25%p로 다시) · 롱온리 0~100%
                             (b) 변수 묶기: 효율선 위 w(γ) = g + v/γ 한 축만(γ 400개)
      ③ 후보마다 기대수익(입력 μ로 바로 계산)과 미달 비율(표본 중 R < H인 비율)을 센다 — 확률은 정규식으로 계산하지 않는다
      ④ 미달 비율 ≤ α인 후보 중 기대수익 최대가 답
두꺼운 꼬리: 같은 평균 · 공분산의 다변량 t(자유도 5)로 표본을 바꿔 같은 일을 한다(닫힌 해가 못 하는 일).
실행: python3 dm_mc.py   (numpy만 · 결과 dm_mc_results.json · 수십 초)"""
import json, math, os, time
import numpy as np

SEED, N = 2026, 200_000
MU = np.array([0.05, 0.10, 0.25])
S = np.array([[0.0025, 0, 0], [0, 0.04, 0.02], [0, 0.02, 0.25]])
ACCTS = [("은퇴", -0.10, 0.05), ("교육", -0.05, 0.15), ("상속", -0.15, 0.20)]
CLOSED = {"은퇴": [53.9, 26.6, 19.5], "교육": [37.9, 35.0, 27.1], "상속": [-78.9, 96.2, 82.7]}
LONG_ONLY_CLOSED = {"상속": [0.0, 8.9, 91.1]}
HERE = os.path.dirname(os.path.abspath(__file__))


def samples(rng, kind):
    L = np.linalg.cholesky(S)
    z = rng.standard_normal((N, 3))
    if kind == "t5":                                   # 다변량 t(자유도 5), 분산을 맞추려고 √(3/5)를 곱한다
        w = rng.chisquare(5, N) / 5
        z = z / np.sqrt(w)[:, None] * math.sqrt(3 / 5)
    return MU + z @ L.T


def evaluate(X, W, H, chunk=400):
    """후보 W(k × 3)마다 기대수익(입력 μ로 바로)과 미달 비율(표본에서 센다)."""
    m = W @ MU; miss = np.empty(len(W))
    for i in range(0, len(W), chunk):
        Rp = X @ W[i:i + chunk].T                      # N × 후보 묶음
        miss[i:i + chunk] = (Rp < H).mean(axis=0)
    return m, miss


def best(W, m, miss, a):
    ok = miss <= a
    if not ok.any(): return None
    i = np.argmax(np.where(ok, m, -np.inf))
    return W[i], float(m[i]), float(miss[i])


def grid(lo, hi, step):
    v = np.round(np.arange(lo, hi + 1e-9, step), 6)
    a, b = np.meshgrid(v, v, indexing="ij")
    W = np.stack([a.ravel(), b.ravel(), 1 - a.ravel() - b.ravel()], 1)
    return W[(W[:, 2] >= lo - 1e-9) & (W[:, 2] <= hi + 1e-9)]


def solve_grid(X, H, a, lo, hi):
    W = grid(lo, hi, 0.02); n1 = len(W)
    m, miss = evaluate(X, W, H); w0 = best(W, m, miss, a)[0]
    v = np.arange(-0.04, 0.0401, 0.0025)
    a2, b2 = np.meshgrid(w0[0] + v, w0[1] + v, indexing="ij")
    W2 = np.stack([a2.ravel(), b2.ravel(), 1 - a2.ravel() - b2.ravel()], 1)
    W2 = W2[(W2.min(1) >= lo - 1e-9) & (W2.max(1) <= hi + 1e-9)]
    m2, miss2 = evaluate(X, W2, H); w, mm, ms = best(W2, m2, miss2, a)
    return {"w": [round(x * 100, 1) for x in w], "mean": mm, "miss": ms, "candidates": n1 + len(W2)}


def solve_gamma(X, H, a):
    o = np.ones(3); Si = np.linalg.inv(S); A = o @ Si @ MU; C = o @ Si @ o
    g = Si @ o / C; v = Si @ (MU - A / C * o)
    gam = np.geomspace(0.3, 30, 400)
    W = g[None, :] + v[None, :] / gam[:, None]
    m, miss = evaluate(X, W, H); w, mm, ms = best(W, m, miss, a)
    i = int(np.argmin(np.abs(W - w).sum(1)))
    return {"w": [round(x * 100, 1) for x in w], "gamma": float(gam[i]), "mean": mm, "miss": ms, "candidates": len(W)}


def main():
    t0 = time.time()
    out = {"seed": SEED, "N": N, "accounts": {}}
    for kind in ("normal", "t5"):
        X = samples(np.random.default_rng(SEED), kind)
        for name, H, a in ACCTS:
            row = out["accounts"].setdefault(name, {"H": H, "alpha": a, "closed": CLOSED[name]})
            r = {"gamma_line": solve_gamma(X, H, a), "long_only": solve_grid(X, H, a, 0.0, 1.0)}
            if kind == "normal": r["grid"] = solve_grid(X, H, a, -1.0, 2.0)
            r["se_miss"] = math.sqrt(a * (1 - a) / N)
            row[kind] = r
        print(kind, "done", round(time.time() - t0, 1), "s")
    # 꼬리 점검 — α가 작을 때(1%) 정규 대 t5: 같은 분산의 t는 5%보다 바깥(1%)에서 더 두껍다
    tail = {}
    for kind in ("normal", "t5"):
        X = samples(np.random.default_rng(SEED), kind)
        tail[kind] = solve_gamma(X, -0.20, 0.01)
    out["tail_check"] = {"H": -0.20, "alpha": 0.01, **tail}
    out["long_only_closed"] = LONG_ONLY_CLOSED
    out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(HERE, "dm_mc_results.json"), "w"), ensure_ascii=False, indent=1)
    for name, row in out["accounts"].items():
        n, t = row["normal"], row["t5"]
        print(f'{name} (H {row["H"]:.0%}, α {row["alpha"]:.0%}) 닫힌 해 {row["closed"]} | 격자 {n["grid"]["w"]} ({n["grid"]["candidates"]:,}개)'
              f' | γ 한 축 {n["gamma_line"]["w"]} γ {n["gamma_line"]["gamma"]:.2f} ({n["gamma_line"]["candidates"]}개)'
              f' | 롱온리 {n["long_only"]["w"]} | t5 γ 한 축 {t["gamma_line"]["w"]} · 롱온리 {t["long_only"]["w"]}')
    print("꼬리 점검 (−20%, 1%): 정규", out["tail_check"]["normal"]["w"], "· t5", out["tail_check"]["t5"]["w"])
    print("초", out["seconds"])


if __name__ == "__main__":
    main()
