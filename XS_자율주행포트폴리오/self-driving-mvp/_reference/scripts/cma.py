# -*- coding: utf-8 -*-
"""① cma-builder — 자본시장 가정을 만든다 (W03).
   기대수익률은 역사적 평균을 전체 평균 쪽으로 축소하고,
   공분산은 Ledoit-Wolf 축소를 적용한다."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, common

SPLIT = "2022-07-31"          # 학습/평가 분리 — 이 시점 이후는 보지 않는다
SHRINK_MU = 0.5               # 역사적 평균을 그랜드 평균으로 당기는 비율

def ledoit_wolf(X):
    """상수상관 목표로 축소한 공분산. sklearn 없이 구현."""
    T, N = X.shape
    S = np.cov(X, rowvar=False, ddof=1)
    d = np.sqrt(np.diag(S)); C = S/np.outer(d, d)
    rbar = (C.sum()-N)/(N*(N-1))
    F = rbar*np.outer(d, d); np.fill_diagonal(F, np.diag(S))
    Xc = X - X.mean(0)
    phi = sum(((Xc[t:t+1].T@Xc[t:t+1] - S)**2).sum() for t in range(T))/T
    gamma = ((F-S)**2).sum()
    shrink = max(0.0, min(1.0, (phi/T)/gamma)) if gamma > 0 else 0.0
    return shrink*F + (1-shrink)*S, shrink

def main(run):
    R = common.load_panel()
    train = R.loc[:SPLIT]
    tick = list(train.columns); X = train.values
    mu_h = X.mean(0)*12
    mu = mu_h.mean() + SHRINK_MU*(mu_h - mu_h.mean())      # 기대수익률 축소
    S_m, shrink = ledoit_wolf(X)
    Sigma = S_m*12
    out = {"as_of": SPLIT, "train_months": len(train), "tickers": tick,
           "mu": dict(zip(tick, np.round(mu, 5).tolist())),
           "sigma": np.round(Sigma, 6).tolist(),
           "shrink_intensity": round(float(shrink), 4),
           "method": "historical mean shrunk %.0f%% to grand mean; Ledoit-Wolf covariance" % (SHRINK_MU*100)}
    p = common.save("cma.json", out, run)
    print("  학습구간 %s ~ %s (%d개월), 평가구간은 보지 않았다."
          % (train.index[0].date(), train.index[-1].date(), len(train)))
    print("  Ledoit-Wolf 축소강도 %.3f" % shrink)
    print("  기대수익률(연율 %): " + ", ".join("%s %.1f" % (t, mu[i]*100) for i, t in enumerate(tick)))
    print("  → %s" % os.path.relpath(p, common.ROOT))

if __name__ == "__main__": main(sys.argv[1])
