# -*- coding: utf-8 -*-
"""③ alloc-bl — 블랙리터맨 (W05).
   정책 중립 포트폴리오에서 균형수익률을 역산하고, 두 개의 뷰를 얹는다."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, common
from scipy.optimize import minimize

DELTA, TAU = 2.5, 0.05        # 위험회피계수 · 사전분포 신뢰도

def neutral_weights(tick, ips):
    """IPS 각 그룹의 중간값을 그룹 내 균등배분한 정책 중립 포트폴리오."""
    w = np.zeros(len(tick))
    for g, spec in ips["groups"].items():
        idx = [tick.index(t) for t in spec["members"] if t in tick]
        w[idx] = (spec["min"]+spec["max"])/2/len(idx)
    return w/w.sum()

def main(run):
    ips = common.load_ips(); cma = common.load(run=run, name="cma.json")
    tick = cma["tickers"]; S = np.array(cma["sigma"]); n = len(tick)
    w_eq = neutral_weights(tick, ips)
    pi = DELTA * S @ w_eq                                  # 균형수익률 역산

    # 뷰 — IC가 제시한 두 가지 판단
    i = {t:k for k,t in enumerate(tick)}
    P = np.zeros((2, n)); Q = np.zeros(2)
    P[0, i["EEM"]], P[0, i["EFA"]] = 1, -1; Q[0] = 0.02    # 신흥국이 선진국외를 연 2%p 상회
    P[1, i["TLT"]] = 1;                     Q[1] = 0.035   # 장기국채 절대 3.5%
    views = ["EEM − EFA = +2.0%p (상대)", "TLT = 3.5% (절대)"]
    Omega = np.diag(np.diag(P @ (TAU*S) @ P.T))            # 뷰 불확실성

    tS = TAU*S
    M = np.linalg.inv(np.linalg.inv(tS) + P.T@np.linalg.inv(Omega)@P)
    mu_bl = M @ (np.linalg.inv(tS)@pi + P.T@np.linalg.inv(Omega)@Q)

    bnds, cons = common.bounds_and_cons(tick, ips)
    neg = lambda w: -(w@mu_bl)/np.sqrt(w@S@w)
    best, bv = None, np.inf
    for seed in range(12):
        w0 = np.random.default_rng(200+seed).dirichlet(np.ones(n))
        r = minimize(neg, w0, method="SLSQP", bounds=bnds, constraints=cons,
                     options={"maxiter":400,"ftol":1e-10})
        if r.success and r.fun < bv: bv, best = r.fun, r.x
    w = np.clip(best,0,None); w /= w.sum()
    out = {"method":"Black-Litterman (2 views, IPS-constrained)", "agent":"alloc-bl", "week":"W05",
           "tickers":tick, "views":views, "delta":DELTA, "tau":TAU,
           "pi":dict(zip(tick, np.round(pi,5).tolist())),
           "mu_bl":dict(zip(tick, np.round(mu_bl,5).tolist())),
           "weights":dict(zip(tick, np.round(w,4).tolist())),
           "expected":{"ret":float(w@mu_bl), "vol":float(np.sqrt(w@S@w)),
                       "sharpe":float((w@mu_bl)/np.sqrt(w@S@w)), "effective_n":common.effective_n(w)},
           "ips_violations": common.check_ips(w, tick, ips)}
    p = common.save("alloc_bl.json", out, run)
    print("  뷰: " + " / ".join(views))
    print("  비중: " + ", ".join("%s %.1f%%" % (t, w[k]*100) for k,t in enumerate(tick) if w[k]>0.005))
    print("  기대 연수익 %.2f%% · 변동성 %.2f%% · 유효N %.2f"
          % (out["expected"]["ret"]*100, out["expected"]["vol"]*100, out["expected"]["effective_n"]))
    print("  IPS 위반: %s" % (out["ips_violations"] or "없음"))
    print("  → %s" % os.path.relpath(p, common.ROOT))

if __name__ == "__main__": main(sys.argv[1])
