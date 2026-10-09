"""오케스트레이터 — 분기 말마다 에이전트를 정해진 순서로 부른다.

macro → cma → research → PC 6개 → ips-guardian → cro → 상호 검토 → 투표 → ic-agent → meta-reviewer → CIO → 변경 반영
"""
from __future__ import annotations
import json, os, shutil
import numpy as np
import pandas as pd
from . import data, ips as I, harness as H
from .agents_input import macro_agent, cma_builder, research_agent
from .agents_pc import run_all
from .agents_review import cro, metric_M, vote, reviews, ic_report
from .cio_meta import cio_step, meta_review, PendingDecision
from .data import ROOT, TICKERS


def quarters(first: str = "2022-08", include_last: bool = False) -> list[str]:
    """분기 말 결정 시점 목록. 기본은 다음 달 실현이 있는 시점까지(성과 평가용)."""
    last = data._month(data.last_month())
    out, q = [], data._month(first)
    while q + pd.DateOffset(months=0 if include_last else 1) <= last:
        out.append(q.strftime("%Y-%m"))
        q = q + pd.DateOffset(months=3)
    return out


def _dump(obj, path):
    json.dump(obj, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return path


def run_quarter(as_of: str, runs_dir: str | None = None, extra_proposal: dict | None = None, log=print) -> dict:
    runs_dir = runs_dir or os.path.join(ROOT, "runs")
    qs = quarters(include_last=True)
    i = qs.index(as_of) if as_of in qs else None
    prev = qs[i - 1] if i else None
    prev_dir = os.path.join(runs_dir, prev) if prev else None
    out = os.path.join(runs_dir, as_of)
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    h = H.Harness(as_of, out)
    params = H.load_params(as_of)
    ip = I.load()
    _dump({"as_of": as_of, "params": params, "ips_sha": H.sha(os.path.join(ROOT, "ips.md"))}, os.path.join(out, "config_used.json"))

    # 1. 입력
    m = h.call("macro-agent", "macro-regime", lambda: macro_agent(as_of, out), [os.path.join(ROOT, "data", "macro_monthly.csv")])
    regime = m["regime"]
    c = h.call("cma-builder", "cma-build", lambda: cma_builder(as_of, out, params), [os.path.join(ROOT, "data", "panel_monthly.csv")])["cma"]
    hist_reg = []
    for q in qs[: i or 0]:
        f = os.path.join(runs_dir, q, "macro.json")
        if os.path.exists(f):
            hist_reg.append(json.load(open(f)))
    prev_reg = hist_reg[-1] if hist_reg else None
    rs = h.call("research-agent", "research-memo", lambda: research_agent(as_of, out, regime, prev_reg, hist_reg), [os.path.join(out, "macro.json")])
    research_prop = rs["proposal"]
    if research_prop:
        os.makedirs(os.path.join(out, "proposals_change"), exist_ok=True)
        _dump(research_prop, os.path.join(out, "proposals_change", research_prop["id"] + ".json"))

    # 2. 구성
    cma_p = os.path.join(out, "cma.json")
    props = h.call("pc-agents(6)", "portfolio-construct", lambda: (lambda r: {"outputs": [os.path.join(out, "proposals", f"{k}.json") for k in r], "note": "6개 안 제출", "props": r})(run_all(c, ip, out, params)), [cma_p])["props"]
    if extra_proposal:  # 결함 주입 시험(T2·L3)용 — 외부에서 끼워 넣은 안
        props[extra_proposal["agent"]] = extra_proposal
        _dump({**extra_proposal, "weights": dict(zip(TICKERS, extra_proposal["w"]))}, os.path.join(out, "proposals", extra_proposal["agent"] + ".json"))
        h.log("harness", f"외부 주입 안 {extra_proposal['agent']} 을 후보에 추가(시험용)")

    # 3. 적격 심사
    cov = np.array(c["cov"])
    viol = {k: I.check(dict(zip(TICKERS, p["w"])), ip, cov) for k, p in props.items()}
    elig = [k for k in props if not viol[k]]
    el = {k: {"eligible": not viol[k], "violations": viol[k], "n_eff": round(I.n_eff(props[k]["w"]), 4)} for k in props}
    h.call("ips-guardian", "ips-check", lambda: {"outputs": [_dump(el, os.path.join(out, "eligibility.json"))],
           "note": f"적격 {len(elig)} / 기각 {len(props) - len(elig)}"}, [os.path.join(ROOT, "ips.md")] + [os.path.join(out, "proposals", f"{k}.json") for k in props],
           constraints=[f"{k}: {'; '.join(v)}" for k, v in viol.items() if v])

    # 4. 심의
    cr = h.call("cro-agent", "risk-report", lambda: (lambda r: {"outputs": [_dump(r, os.path.join(out, "cro_report.json"))], "note": "전 안에 같은 양식 보고서", "r": r})(cro(as_of, props, c, params)), [cma_p])["r"]
    rv = h.call("pc-agents(6)", "peer-review", lambda: (lambda r: {"outputs": [_dump(r, os.path.join(out, "reviews.json"))], "note": f"검토 {len(r)}건", "r": r})(reviews(props, elig, cr, ip, c)), [os.path.join(out, "cro_report.json")])["r"]
    Mres = metric_M(as_of, props, elig, c, ip, regime["label"], params)
    v = h.call("vote", "modified-borda", lambda: (lambda r: {"outputs": [_dump({**r, "metric": Mres}, os.path.join(out, "votes.json"))], "note": f"채택 후보 {r['winner']}", "r": r})(vote(props, elig, cr, Mres, params)),
               [os.path.join(out, "eligibility.json"), os.path.join(out, "cro_report.json"), os.path.join(out, "reviews.json")])["r"]

    # 5. 메타 리뷰 (직전 분기 사후 평가)
    meta_props = []
    if prev_dir and os.path.exists(os.path.join(prev_dir, "holdings.json")):
        hist = [json.load(open(os.path.join(runs_dir, q, "meta_review.json")))["mae"] for q in qs[1: i] if os.path.exists(os.path.join(runs_dir, q, "meta_review.json"))]
        last_meta = None
        for q in qs[1: i]:
            f = os.path.join(runs_dir, q, "meta_review.json")
            if os.path.exists(f) and json.load(open(f))["proposals"]:
                last_meta = qs.index(q)
        mr = h.call("meta-reviewer", "meta-review", lambda: meta_review(as_of, prev, prev_dir, out, params, hist, qs, last_meta), [os.path.join(prev_dir, "cma.json"), os.path.join(prev_dir, "holdings.json")])
        meta_props = mr["proposals"]

    holding = json.load(open(os.path.join(prev_dir, "holdings.json")))["weights"] if prev_dir and os.path.exists(os.path.join(prev_dir, "holdings.json")) else None
    icp = h.call("ic-agent", "ic-report", lambda: {"outputs": [ic_report(as_of, props, viol, cr, v, rv, regime, research_prop, meta_props, holding, out)], "note": f"권고 {v['winner']}"},
                 [os.path.join(out, "votes.json"), os.path.join(out, "reviews.json"), os.path.join(out, "cro_report.json")])

    # 6. CIO (사람) — 결정이 없으면 여기서 멈춘다
    cs = h.call("CIO(사람)", "-", lambda: cio_step(as_of, v["winner"], props, holding, out, ip, cov), [os.path.join(out, "ic_report.md"), os.path.join(ROOT, "data", "cio_decisions.csv")])

    # 7. 변경 제안 처리 — 킬스위치 통과 경로
    changes = []
    for pr in ([research_prop] if research_prop else []) + meta_props:
        st = H.apply_change(pr, as_of)
        changes.append(st)
        h.log("harness", f"변경 제안 {pr['id']} → {st['result']} ({st['why']})")
    _dump(changes, os.path.join(out, "changes.json"))
    log(f"  {as_of}  국면 {regime['label']:<8} 적격 {len(elig)}/6  권고 {str(v['winner']):<15} CIO {cs['decision']}" + (f"  변경 {[c['result'] for c in changes]}" if changes else ""))
    return {"as_of": as_of, "winner": v["winner"], "decision": cs["decision"]}


def run_all_quarters(runs_dir: str | None = None, log=print):
    runs_dir = runs_dir or os.path.join(ROOT, "runs")
    # 처음부터 다시 돌릴 때는 승격 기록도 처음부터 다시 쌓는다
    json.dump([], open(os.path.join(ROOT, "config", "param_changes.json"), "w"))
    res = []
    for q in quarters():
        try:
            res.append(run_quarter(q, runs_dir, log=log))
        except PendingDecision:
            log(f"  {q}  CIO 결정 대기 — 루프를 멈춘다")
            break
    return res
