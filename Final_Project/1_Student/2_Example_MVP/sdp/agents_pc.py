"""포트폴리오 구성(PC) 에이전트 6개 — 같은 cma.json 을 받아 각자 배분안을 낸다.

모든 최적화는 IPS의 종목 상한·자산군 범위·사전 변동성 한도를 제약으로 넣는다.
분산 요건(N_eff)만은 넣지 않는다 — 코너해가 나오면 ips-guardian 이 걸러야 한다(MVP와 같은 설계).
"""
from __future__ import annotations
import json, os
import numpy as np
from scipy.optimize import minimize
from .data import TICKERS

N = len(TICKERS)


def _cons(ips: dict, cov: np.ndarray | None):
    c = ips["constraints"]
    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1.0}]
    for spec in c["groups"].values():
        idx = [TICKERS.index(t) for t in spec["members"]]
        cons.append({"type": "ineq", "fun": lambda w, idx=idx, lo=spec["min"]: w[idx].sum() - lo})
        cons.append({"type": "ineq", "fun": lambda w, idx=idx, hi=spec["max"]: hi - w[idx].sum()})
    if cov is not None:
        cons.append({"type": "ineq", "fun": lambda w: c["vol_cap"] ** 2 - w @ cov @ w})
    return cons, [(0.0, c["asset_max"])] * N


def _solve(obj, ips, cov, x0=None, vol=True):
    cons, bnds = _cons(ips, cov if vol else None)
    x0 = np.full(N, 1.0 / N) if x0 is None else x0
    r = minimize(obj, x0, method="SLSQP", bounds=bnds, constraints=cons, options={"maxiter": 500, "ftol": 1e-12})
    w = np.clip(r.x, 0, None)
    return w / w.sum(), bool(r.success)


def _project(target, ips, cov):
    return _solve(lambda w: np.sum((w - target) ** 2), ips, cov)


def equal_weight(mu, cov, rf, ips, others=None):
    return _project(np.full(N, 1 / N), ips, cov)


def inverse_vol(mu, cov, rf, ips, others=None):
    iv = 1 / np.sqrt(np.diag(cov))
    return _project(iv / iv.sum(), ips, cov)


def min_variance(mu, cov, rf, ips, others=None):
    return _solve(lambda w: w @ cov @ w * 100, ips, cov)


def max_sharpe(mu, cov, rf, ips, others=None):
    return _solve(lambda w: -(w @ mu - rf) / np.sqrt(w @ cov @ w), ips, cov)


def erc(mu, cov, rf, ips, others=None):
    def obj(w):
        rc = w * (cov @ w)
        return np.sum((rc - rc.sum() / N) ** 2) * 1e4
    return _solve(obj, ips, cov)


def sharpe(w, mu, cov, rf):
    return float((w @ mu - rf) / np.sqrt(w @ cov @ w))


def adversarial(mu, cov, rf, ips, others, starts=8):
    """다른 안들과의 평균 추적오차 제곱을 최대화, 샤프 비율 ≥ 다른 안들의 중앙값."""
    W = np.array(others)
    sr_min = float(np.median([sharpe(w, mu, cov, rf) for w in W]))
    cons, bnds = _cons(ips, cov)
    cons = cons + [{"type": "ineq", "fun": lambda w: (w @ mu - rf) - sr_min * np.sqrt(w @ cov @ w)}]
    obj = lambda w: -np.mean([(w - k) @ cov @ (w - k) for k in W]) * 1e4
    best, bw = None, None
    rng = np.random.default_rng(20260402)  # 고정 시드 — 같은 입력이면 같은 답
    x0s = [np.full(N, 1 / N)] + [rng.dirichlet(np.ones(N)) for _ in range(starts - 1)]
    for x0 in x0s:
        r = minimize(obj, x0, method="SLSQP", bounds=bnds, constraints=cons, options={"maxiter": 500, "ftol": 1e-12})
        w = np.clip(r.x, 0, None); w = w / w.sum()
        ok = all(c["fun"](w) >= -1e-6 if c["type"] == "ineq" else abs(c["fun"](w)) < 1e-6 for c in cons)
        if ok and (best is None or r.fun < best):
            best, bw = r.fun, w
    if bw is None:
        bw = W.mean(0)
    return bw, True, sr_min


AGENTS = [
    ("pc-equal", "동일가중 (IPS 투영)", "휴리스틱", equal_weight, "유효 종목 수가 클수록 좋다"),
    ("pc-invvol", "역변동성 (IPS 투영)", "휴리스틱", inverse_vol, "사전 변동성이 낮을수록 좋다"),
    ("pc-minvar", "최소분산", "위험 구조", min_variance, "꼬리 손실(CVaR)이 작을수록 좋다"),
    ("pc-maxsharpe", "최대 샤프 (MVO)", "수익 최적화", max_sharpe, "CMA 기대 샤프가 높을수록 좋다"),
    ("pc-erc", "위험기여 균등 (ERC)", "위험 구조", erc, "위험기여가 고를수록 좋다"),
    ("pc-adversarial", "적대적 분산자", "에이전트형", adversarial, "다른 안들과 다를수록 좋다"),
]


def run_all(c: dict, ips: dict, out_dir: str, params: dict) -> dict:
    mu, cov, rf = np.array(c["mu"]), np.array(c["cov"]), c["rf"]
    os.makedirs(os.path.join(out_dir, "proposals"), exist_ok=True)
    res = {}
    for aid, name, fam, fn, lens in AGENTS:
        extra = {}
        if aid == "pc-adversarial":
            others = [np.array(res[k]["w"]) for k in res]
            w, ok, srmin = fn(mu, cov, rf, ips, others, starts=params["adversarial"]["starts"])
            extra["sr_min"] = round(srmin, 6)
        else:
            w, ok = fn(mu, cov, rf, ips)
        w = np.round(w, 6); w = w / w.sum()
        res[aid] = {"agent": aid, "method": name, "family": fam, "lens": lens, "solver_ok": ok,
                    "w": [round(float(x), 6) for x in w], "exp_ret": round(float(w @ mu), 6),
                    "exp_vol": round(float(np.sqrt(w @ cov @ w)), 6), "exp_sharpe": round(sharpe(w, mu, cov, rf), 6), **extra}
    for aid, r in res.items():
        p = os.path.join(out_dir, "proposals", f"{aid}.json")
        json.dump({**r, "weights": dict(zip(TICKERS, r["w"]))}, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return res
