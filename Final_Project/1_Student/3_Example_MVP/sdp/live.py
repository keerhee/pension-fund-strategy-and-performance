"""라이브 점검 L1~L3 — 발표 당일 교수가 주는 과제. 코드는 고치지 않고 IPS·입력만 바꾼다. 모두 임시 복사본에서 돈다."""
from __future__ import annotations
import json, os, re
import pandas as pd
import yaml
from .data import ROOT
from .selfcheck import copy_repo, py, _numbers


def _read(p):
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def _quarter_view(d: str, q: str) -> dict:
    qd = os.path.join(d, "runs", q)
    out = {"ic_report": _read(os.path.join(qd, "ic_report.md")), "cio": _read(os.path.join(qd, "cio_decision.md"))}
    for k in ("eligibility", "votes", "holdings"):
        f = os.path.join(qd, k + ".json")
        out[k] = json.load(open(f)) if os.path.exists(f) else None
    tr = os.path.join(qd, "trace.jsonl")
    out["trace"] = [json.loads(l) for l in open(tr, encoding="utf-8")] if os.path.exists(tr) else []
    return out


def l1(q: str, overrides: dict) -> dict:
    """IPS 조항 변경. overrides 예: {"vol_cap": 0.07, "asset_max": 0.25, "effective_n_min": 4.0, "groups.alternative.max": 0.15}"""
    d = copy_repo()
    p = os.path.join(d, "ips.md")
    txt = open(p, encoding="utf-8").read()
    m = re.search(r"```yaml\n(.*?)```", txt, re.S)
    y = yaml.safe_load(m.group(1))
    for k, v in overrides.items():
        node, keys = y["constraints"], k.split(".")
        for kk in keys[:-1]:
            node = node[kk]
        node[keys[-1]] = float(v)
    new = yaml.safe_dump(y, allow_unicode=True, sort_keys=False)
    open(p, "w", encoding="utf-8").write(txt[: m.start(1)] + new + txt[m.end(1):])
    r = py(d, f"from sdp import pipeline; pipeline.run_quarter('{q}')")
    after = _quarter_view(d, q)
    before = _quarter_view(ROOT, q)
    return {"ok": r.returncode == 0, "log": (r.stdout + r.stderr)[-1500:], "overrides": overrides,
            "before": {"winner": before["votes"]["winner"], "eligible": {k: v["eligible"] for k, v in before["eligibility"].items()}},
            "after": {"winner": after["votes"]["winner"] if after["votes"] else None,
                      "eligible": {k: v["eligible"] for k, v in (after["eligibility"] or {}).items()},
                      "violations": {k: v["violations"] for k, v in (after["eligibility"] or {}).items() if v["violations"]}},
            "ic_report": after["ic_report"]}


DUR = {"IEF": 7.5, "TLT": 16.5, "LQD": 8.5, "HYG": 3.5, "TIP": 7.0}


def l2(equity: float, rate_bp: float, gold: float, commodity: float) -> dict:
    """가상의 다음 달 충격을 붙이고 다음 분기를 진행한다. CIO 결정은 비어 있으므로 IC 보고서에서 멈춘다."""
    d = copy_repo()
    pp = os.path.join(d, "data", "panel_monthly.csv")
    P = pd.read_csv(pp)
    last = pd.Timestamp(P["date"].iloc[-1])
    nxt = (last + pd.DateOffset(months=1)).strftime("%Y-%m-01")
    dy = rate_bp / 100.0
    row = {"date": nxt, "ret_SPY": equity, "ret_EFA": equity * 1.0, "ret_EEM": equity * 1.2, "ret_VNQ": equity * 1.1,
           "ret_GLD": gold, "ret_DBC": commodity}
    for t, D in DUR.items():
        row[f"ret_{t}"] = -D * dy + (0.4 * equity if t == "HYG" else 0.0)
    P = pd.concat([P, pd.DataFrame([row])[P.columns]], ignore_index=True)
    P.round(4).to_csv(pp, index=False)
    mp = os.path.join(d, "data", "macro_monthly.csv")
    M = pd.read_csv(mp)
    mr = M.iloc[-1].copy(); mr["date"] = nxt
    mr["DGS10"] += dy; mr["T10Y2Y"] += dy * 0.5; mr["CPIAUCSL"] *= 1.002
    mr["BAA10Y"] += 0.5 if equity <= -10 else 0.0
    pd.concat([M, pd.DataFrame([mr])], ignore_index=True).round(4).to_csv(mp, index=False)
    q = nxt[:7]
    r = py(d, f"from sdp import pipeline; pipeline.run_quarter('{q}')")
    v = _quarter_view(d, q)
    return {"ok": "PendingDecision" in r.stderr or r.returncode == 0, "as_of": q, "shock_row": row,
            "log": (r.stdout + r.stderr)[-800:], "ic_report": v["ic_report"], "cio": v["cio"],
            "note": "IC 보고서까지 생성. CIO 결정이 없어 루프가 멈췄다 — 팀의 CIO가 이 자리에서 결정한다."}


def l3(kind: str, q: str = "2024-11") -> dict:
    """숨은 결함 주입. kind: 'sum103' (비중 합 1.03 안) | 'future_memo' (리서치 메모에 결정 시점 이후 사건)"""
    d = copy_repo()
    if kind == "sum103":
        code = ("from sdp import pipeline; w=[0.11,0.1,0.1,0.1,0.1,0.1,0.08,0.1,0.08,0.08,0.08]; "
                f"pipeline.run_quarter('{q}', extra_proposal={{'agent':'pc-buggy','method':'결함 주입안','family':'시험','lens':'-','w':w,'exp_ret':0,'exp_vol':0,'exp_sharpe':0}})")
        r = py(d, code)
        v = _quarter_view(d, q)
        el = (v["eligibility"] or {}).get("pc-buggy", {})
        caught = el and not el.get("eligible", True)
        return {"ok": r.returncode == 0, "caught": bool(caught), "where": "ips-guardian (eligibility.json)",
                "evidence": el.get("violations"), "ic_report": v["ic_report"], "log": (r.stdout + r.stderr)[-800:]}
    if kind == "future_memo":
        inj = "2025-03 연준이 금리를 0.5%p 내린 뒤 장기채가 강세를 보였다."
        r = py(d, f"from sdp import pipeline; pipeline.run_quarter('{q}')", env_extra={"SDP_INJECT_MEMO": inj})
        v = _quarter_view(d, q)
        hit = [t for t in v["trace"] if t.get("lookahead")]
        return {"ok": True, "caught": bool(hit) and "LookaheadError" in r.stderr, "where": "harness (research-agent 산출물 날짜 검사)",
                "evidence": hit[-1] if hit else None, "injected": inj, "log": r.stderr[-500:]}
    raise ValueError(kind)


def recompute(q: str) -> dict:
    """채점자가 고른 분기를 다시 계산해 제출본과 대조한다(T8의 단일 분기판)."""
    d = copy_repo()
    r = py(d, f"from sdp import pipeline; pipeline.run_quarter('{q}')")
    if r.returncode != 0:
        return {"ok": False, "log": r.stderr[-800:]}
    a, b = _numbers(os.path.join(ROOT, "runs", q)), _numbers(os.path.join(d, "runs", q))
    return {"ok": True, "q": q, "items": [{"item": k, "match": a[k] == b.get(k)} for k in a], "all_match": a == b,
            "log": r.stdout[-300:]}
