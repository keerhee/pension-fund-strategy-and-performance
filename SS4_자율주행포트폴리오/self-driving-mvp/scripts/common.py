# -*- coding: utf-8 -*-
"""IPS 파싱 · 데이터 적재 · 제약 검사 — 모든 에이전트가 공유한다."""
import json, os, re
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "runs")

def load_ips(path=None):
    """IPS 본문의 부록 A(YAML 블록)를 읽는다. PyYAML 없이 최소 파싱."""
    path = path or os.path.join(ROOT, "ips.md")
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"```yaml\n(.*?)```", txt, re.S)
    if not m: raise SystemExit("IPS에서 부록 A(yaml 블록)를 찾지 못했다.")
    y = m.group(1)
    def num(k, d=None):
        mm = re.search(r"%s:\s*([-\d.]+)" % k, y)
        return float(mm.group(1)) if mm else d
    groups = {}
    for g, mem, lo, hi in re.findall(
            r"(\w+):\s*\{members:\s*\[([^\]]+)\],\s*min:\s*([\d.]+),\s*max:\s*([\d.]+)\}", y):
        groups[g] = {"members": [s.strip() for s in mem.split(",")],
                     "min": float(lo), "max": float(hi)}
    return {"asset_max": num("asset_max", .30), "asset_min": num("asset_min", 0.),
            "effective_n_min": num("effective_n_min", 4.), "groups": groups,
            "long_only": "long_only: true" in y,
            "real_return_target": num("real_return_target", .045),
            "vol_cap": num("vol_cap", .10), "mdd_limit": num("mdd_limit", -.20)}

def load_panel():
    df = pd.read_csv(os.path.join(ROOT, "data", "panel_monthly.csv"),
                     index_col="date", parse_dates=True)
    df.columns = [c.replace("ret_", "") for c in df.columns]
    return df / 100.0                      # % → 소수

def effective_n(w):
    w = np.asarray(w, float); s = (w**2).sum()
    return float(1.0/s) if s > 0 else 0.0

def check_ips(w, tickers, ips):
    """IPS 위반 목록을 돌려준다. 빈 리스트면 적격."""
    w = np.asarray(w, float); v = []
    if abs(w.sum()-1) > 1e-4:      v.append("비중 합 %.4f ≠ 1" % w.sum())
    if ips["long_only"] and w.min() < -1e-6: v.append("공매도 발생 (최소 %.3f)" % w.min())
    if w.max() > ips["asset_max"]+1e-6:
        v.append("개별 상한 초과: %s %.1f%% > %.0f%%"
                 % (tickers[int(w.argmax())], w.max()*100, ips["asset_max"]*100))
    for g, spec in ips["groups"].items():
        idx = [tickers.index(t) for t in spec["members"] if t in tickers]
        tot = w[idx].sum()
        if tot < spec["min"]-1e-6: v.append("%s 하한 미달: %.1f%% < %.0f%%" % (g, tot*100, spec["min"]*100))
        if tot > spec["max"]+1e-6: v.append("%s 상한 초과: %.1f%% > %.0f%%" % (g, tot*100, spec["max"]*100))
    en = effective_n(w)
    if en < ips["effective_n_min"]-1e-6:
        v.append("유효 종목 수 %.2f < %.1f" % (en, ips["effective_n_min"]))
    return v

def perf(w, R):
    """월간 수익률 행렬 R로 연율 성과를 낸다."""
    w = np.asarray(w, float); r = R.values @ w
    ann_ret = float((1+r).prod()**(12/len(r)) - 1)
    ann_vol = float(r.std(ddof=1)*np.sqrt(12))
    cum = (1+r).cumprod(); mdd = float((cum/np.maximum.accumulate(cum) - 1).min())
    return {"ann_return": ann_ret, "ann_vol": ann_vol, "mdd": mdd,
            "sharpe": float(ann_ret/ann_vol) if ann_vol > 0 else 0.0,
            "effective_n": effective_n(w)}

def save(name, obj, run):
    d = os.path.join(RUNS, run); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name)
    json.dump(obj, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return p

def load(name, run):
    return json.load(open(os.path.join(RUNS, run, name), encoding="utf-8"))

def bounds_and_cons(tickers, ips):
    """scipy 최적화용 제약을 IPS에서 만든다."""
    n = len(tickers)
    bnds = [(ips["asset_min"], ips["asset_max"])]*n
    cons = [{"type":"eq", "fun": lambda w: w.sum()-1}]
    for g, spec in ips["groups"].items():
        idx = [tickers.index(t) for t in spec["members"] if t in tickers]
        cons.append({"type":"ineq","fun":(lambda i,lo: (lambda w: w[i].sum()-lo))(idx, spec["min"])})
        cons.append({"type":"ineq","fun":(lambda i,hi: (lambda w: hi-w[i].sum()))(idx, spec["max"])})
    return bnds, cons
