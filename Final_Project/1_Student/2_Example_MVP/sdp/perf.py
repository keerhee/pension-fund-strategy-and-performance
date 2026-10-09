"""사후 성과 — 채택 경로 vs 각 PC 안을 계속 들었을 경우 vs 60/40 vs 동일가중. (평가 전용)"""
from __future__ import annotations
import csv, json, os
import numpy as np
import pandas as pd
from . import data
from .data import ROOT, TICKERS
from .pipeline import quarters


def _metrics(r: pd.Series, rf: float) -> dict:
    v = (1 + r).cumprod()
    ann = float(v.iloc[-1] ** (12 / len(r)) - 1)
    vol = float(r.std() * np.sqrt(12))
    mdd = float((v / v.cummax() - 1).min())
    return {"ann_ret": round(ann, 4), "vol": round(vol, 4), "sharpe": round((ann - rf) / vol, 3), "mdd": round(mdd, 4), "cum": round(float(v.iloc[-1] - 1), 4)}


def build(runs_dir: str | None = None) -> dict:
    runs_dir = runs_dir or os.path.join(ROOT, "runs")
    qs = [q for q in quarters() if os.path.exists(os.path.join(runs_dir, q, "holdings.json"))]
    last = data.last_month()
    paths = {"채택 경로(CIO)": [], "60/40 (SPY·IEF)": [], "동일가중 1/11": []}
    agents = sorted(f[:-5] for f in os.listdir(os.path.join(runs_dir, qs[0], "proposals")))
    for a in agents:
        paths[a] = []
    turnover, prevw = [], None
    for i, q in enumerate(qs):
        months = 3 if i < len(qs) - 1 else (data._month(last).to_period("M") - data._month(q).to_period("M")).n
        R = data.realized(q, months)
        hw = json.load(open(os.path.join(runs_dir, q, "holdings.json")))["weights"]
        w = np.array([hw[t] for t in TICKERS])
        if prevw is not None:
            turnover.append(0.5 * float(np.abs(w - prevw).sum()))
        prevw = w
        paths["채택 경로(CIO)"].append(pd.Series(R.values @ w, index=R.index))
        paths["60/40 (SPY·IEF)"].append(0.6 * R["SPY"] + 0.4 * R["IEF"])
        paths["동일가중 1/11"].append(R.mean(axis=1))
        for a in agents:
            pr = json.load(open(os.path.join(runs_dir, q, "proposals", a + ".json")))
            paths[a].append(pd.Series(R.values @ np.array(pr["w"]), index=R.index))
    series = {k: pd.concat(v) for k, v in paths.items()}
    rf = float(data.macro(last)["DGS3MO"].loc[series["채택 경로(CIO)"].index[0]:].mean()) / 100
    met = {k: _metrics(s, rf) for k, s in series.items()}
    rej = {}
    for q in qs:
        el = json.load(open(os.path.join(runs_dir, q, "eligibility.json")))
        for a, e in el.items():
            if not e["eligible"]:
                rej.setdefault(a, []).append(q)
    mae = [json.load(open(os.path.join(runs_dir, q, "meta_review.json")))["mae"] for q in qs if os.path.exists(os.path.join(runs_dir, q, "meta_review.json"))]
    return {"period": [series["채택 경로(CIO)"].index[0].strftime("%Y-%m"), series["채택 경로(CIO)"].index[-1].strftime("%Y-%m")], "rf": round(rf, 4),
            "metrics": met, "avg_turnover": round(float(np.mean(turnover)), 4), "rejected_quarters": rej,
            "mae_mean": round(float(np.mean(mae)), 4) if mae else None,
            "cum_paths": {k: [round(float(x), 5) for x in (1 + s).cumprod().values] for k, s in series.items()},
            "dates": [d.strftime("%Y-%m") for d in series["채택 경로(CIO)"].index]}


NAMES = {"pc-equal": "동일가중 (IPS 투영)", "pc-invvol": "역변동성 (IPS 투영)", "pc-minvar": "최소분산", "pc-maxsharpe": "최대 샤프 (MVO)",
         "pc-erc": "위험기여 균등 (ERC)", "pc-adversarial": "적대적 분산자"}


def write_reports(runs_dir: str | None = None):
    p = build(runs_dir)
    json.dump(p, open(os.path.join(ROOT, "reports", "performance.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    L = ["# 성과 보고서 (예시 MVP · 가상 기금 KFP)", "", f"평가 구간 {p['period'][0]} ~ {p['period'][1]} · 무위험 {p['rf']:.2%} · 분기 말 결정 12회", "",
         "| 경로 | 연율 수익 | 변동성 | 샤프 | 최대낙폭 | 누적 |", "|---|---|---|---|---|---|"]
    for k, m in p["metrics"].items():
        nm = NAMES.get(k, k) + (" — 계속 보유 가정" if k in NAMES else "")
        L.append(f"| {nm} | {m['ann_ret']:.2%} | {m['vol']:.2%} | {m['sharpe']:.2f} | {m['mdd']:.1%} | {m['cum']:.1%} |")
    L += ["", f"채택 경로 평균 분기 회전율 {p['avg_turnover']:.1%} · CMA 평균 절대 예측오차 {p['mae_mean']:.1%}", "",
          "## 기각된 안의 사후 성과", ""]
    for a, qs in p["rejected_quarters"].items():
        L.append(f"- {NAMES[a]}: {len(qs)}개 분기 기각 ({', '.join(qs)}) — 계속 보유했다면 연율 {p['metrics'][a]['ann_ret']:.2%}, 채택 경로 {p['metrics']['채택 경로(CIO)']['ann_ret']:.2%}")
    L += ["", "주의: 한 구간(35개월)의 결과다. 기각안이 사후에 더 좋았다는 사실만으로 규칙을 완화하지 않는다(사전 등록 원칙)."]
    open(os.path.join(ROOT, "reports", "performance.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    # CHANGELOG · INTERVENTIONS — 사람이 적은 결정 파일에서 자동 생성
    qs = [q for q in quarters() if os.path.exists(os.path.join(runs_dir or os.path.join(ROOT, "runs"), q, "changes.json"))]
    C = ["# CHANGELOG — 변경 제안과 처리 (킬스위치 기록)", "", "| 분기 | 제안 | 제안자 | 내용 | CIO | 결과 | 사유 |", "|---|---|---|---|---|---|---|"]
    ap = {r["proposal_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data", "approvals.csv"), encoding="utf-8"))}
    for q in qs:
        for ch in json.load(open(os.path.join(runs_dir or os.path.join(ROOT, "runs"), q, "changes.json"))):
            pid = ch["id"]
            C.append(f"| {q} | `{pid}` | {'research-agent' if 'research' in pid else 'meta-reviewer'} | {ch['change']} | {ap.get(pid, {}).get('decision', '—')} | **{ch['result']}** | {ch['why']} |")
    open(os.path.join(ROOT, "CHANGELOG.md"), "w", encoding="utf-8").write("\n".join(C) + "\n")
    D = ["# INTERVENTIONS — CIO 결정 기록 (예시: 사람 CIO가 IC 보고서를 읽고 적은 결정)", "", "| 분기 | IC 권고 | 결정 | 조건 | 사유 |", "|---|---|---|---|---|"]
    for r in csv.DictReader(open(os.path.join(ROOT, "data", "cio_decisions.csv"), encoding="utf-8")):
        f = os.path.join(runs_dir or os.path.join(ROOT, "runs"), r["as_of"], "votes.json")
        w = json.load(open(f))["winner"] if os.path.exists(f) else "-"
        D.append(f"| {r['as_of']} | {NAMES.get(w, w)} | {r['decision']} | {r['condition'] or '—'} | {r['reason']} |")
    open(os.path.join(ROOT, "INTERVENTIONS.md"), "w", encoding="utf-8").write("\n".join(D) + "\n")
    return p
