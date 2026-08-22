# -*- coding: utf-8 -*-
"""② alloc-mvo — 평균분산 최적화 (W04). IPS 제약 하 최대 샤프."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, common
from scipy.optimize import minimize

def main(run):
    ips = common.load_ips(); cma = common.load(run=run, name="cma.json")
    tick = cma["tickers"]; mu = np.array([cma["mu"][t] for t in tick])
    S = np.array(cma["sigma"])
    bnds, cons = common.bounds_and_cons(tick, ips)
    neg_sharpe = lambda w: -(w@mu)/np.sqrt(w@S@w)
    best, bv = None, np.inf
    for seed in range(12):                       # 다중 시작점 — 국소해 회피
        rng = np.random.default_rng(seed)
        w0 = rng.dirichlet(np.ones(len(tick)))
        r = minimize(neg_sharpe, w0, method="SLSQP", bounds=bnds,
                     constraints=cons, options={"maxiter":400, "ftol":1e-10})
        if r.success and r.fun < bv: bv, best = r.fun, r.x
    w = np.clip(best, 0, None); w /= w.sum()
    out = {"method":"MVO (max Sharpe, IPS-constrained)", "agent":"alloc-mvo", "week":"W04",
           "tickers":tick, "weights":dict(zip(tick, np.round(w,4).tolist())),
           "expected":{"ret":float(w@mu), "vol":float(np.sqrt(w@S@w)),
                       "sharpe":float((w@mu)/np.sqrt(w@S@w)), "effective_n":common.effective_n(w)},
           "ips_violations": common.check_ips(w, tick, ips)}
    p = common.save("alloc_mvo.json", out, run)
    print("  비중: " + ", ".join("%s %.1f%%" % (t, w[i]*100) for i,t in enumerate(tick) if w[i]>0.005))
    print("  기대 연수익 %.2f%% · 변동성 %.2f%% · 유효N %.2f"
          % (out["expected"]["ret"]*100, out["expected"]["vol"]*100, out["expected"]["effective_n"]))
    print("  IPS 위반: %s" % (out["ips_violations"] or "없음"))
    print("  → %s" % os.path.relpath(p, common.ROOT))

if __name__ == "__main__": main(sys.argv[1])
