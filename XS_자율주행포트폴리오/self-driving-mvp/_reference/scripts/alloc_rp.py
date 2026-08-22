# -*- coding: utf-8 -*-
"""④ alloc-riskparity — 위험기여도 균등 (W06). IPS 제약 하 ERC."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, common
from scipy.optimize import minimize

def main(run):
    ips = common.load_ips(); cma = common.load(run=run, name="cma.json")
    tick = cma["tickers"]; S = np.array(cma["sigma"]); n = len(tick)
    mu = np.array([cma["mu"][t] for t in tick])
    bnds, cons = common.bounds_and_cons(tick, ips)
    def obj(w):
        pv = np.sqrt(w@S@w)
        rc = w*(S@w)/pv                      # 각 자산의 위험기여
        return ((rc - pv/n)**2).sum()*1e4
    best, bv = None, np.inf
    for seed in range(12):
        rng = np.random.default_rng(100+seed)
        w0 = rng.dirichlet(np.ones(n))
        r = minimize(obj, w0, method="SLSQP", bounds=bnds, constraints=cons,
                     options={"maxiter":600, "ftol":1e-12})
        if r.success and r.fun < bv: bv, best = r.fun, r.x
    w = np.clip(best, 0, None); w /= w.sum()
    pv = np.sqrt(w@S@w); rc = w*(S@w)/pv
    out = {"method":"Risk Parity (ERC, IPS-constrained)", "agent":"alloc-riskparity", "week":"W06",
           "tickers":tick, "weights":dict(zip(tick, np.round(w,4).tolist())),
           "risk_contrib":dict(zip(tick, np.round(rc/pv,4).tolist())),
           "expected":{"ret":float(w@mu), "vol":float(pv),
                       "sharpe":float((w@mu)/pv), "effective_n":common.effective_n(w)},
           "ips_violations": common.check_ips(w, tick, ips)}
    p = common.save("alloc_rp.json", out, run)
    print("  비중: " + ", ".join("%s %.1f%%" % (t, w[i]*100) for i,t in enumerate(tick) if w[i]>0.005))
    print("  위험기여 편차(최대-최소): %.1f%%p" % (np.ptp(rc/pv)*100))
    print("  기대 연수익 %.2f%% · 변동성 %.2f%% · 유효N %.2f"
          % (out["expected"]["ret"]*100, pv*100, out["expected"]["effective_n"]))
    print("  IPS 위반: %s" % (out["ips_violations"] or "없음"))
    print("  → %s" % os.path.relpath(p, common.ROOT))

if __name__ == "__main__": main(sys.argv[1])
