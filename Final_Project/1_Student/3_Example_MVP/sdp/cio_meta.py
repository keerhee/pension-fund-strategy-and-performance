"""CIO 결정 반영 · meta-reviewer(BARREL 축소판)

CIO(사람)의 결정은 data/cio_decisions.csv, 변경 제안에 대한 승인은 data/approvals.csv 에 사람이 적는다.
코드는 그 결정을 읽어 반영할 뿐 대신 결정하지 않는다. 결정이 없으면 루프는 그 분기에서 멈춘다.
"""
from __future__ import annotations
import csv, json, os
import numpy as np
from . import data
from .data import TICKERS, ROOT
from .agents_input import cma


class PendingDecision(Exception):
    pass


def decisions() -> dict:
    p = os.path.join(ROOT, "data", "cio_decisions.csv")
    return {r["as_of"]: r for r in csv.DictReader(open(p, encoding="utf-8"))} if os.path.exists(p) else {}


def apply_condition(w: dict, cond: str) -> dict:
    """조건 형식: cap:GLD:0.10 — 상한을 씌우고 넘친 비중을 나머지 자산에 비례 배분."""
    if not cond:
        return dict(w)
    kind, t, val = cond.split(":")
    assert kind == "cap"
    w = dict(w); val = float(val)
    excess = max(0.0, w[t] - val)
    w[t] = min(w[t], val)
    rest = {k: v for k, v in w.items() if k != t and v > 0}
    tot = sum(rest.values())
    for k in rest:
        w[k] += excess * rest[k] / tot
    return {k: round(v, 6) for k, v in w.items()}


def cio_step(as_of: str, winner: str | None, props: dict, holding: dict | None, out_dir: str, ip: dict, cov) -> dict:
    from .ips import check
    d = decisions().get(as_of)
    p = os.path.join(out_dir, "cio_decision.md")
    if d is None:
        open(p, "w", encoding="utf-8").write(f"# CIO 결정 — {as_of}\n\n**결정 대기** — IC 보고서를 읽고 data/cio_decisions.csv 에 결정을 적은 뒤 다시 실행한다.\n")
        raise PendingDecision(as_of)
    dec, cond, why = d["decision"], d.get("condition", ""), d["reason"]
    note = ""
    if winner is None:
        note = "IC 권고안 없음(전 안 기각) — CIO 결정과 무관하게 현 보유 유지. 사람 개입이 필요한 분기"
    if dec in ("승인", "조건부 승인") and winner:
        w = dict(zip(TICKERS, props[winner]["w"]))
        if dec == "조건부 승인":
            w = apply_condition(w, cond)
            v = check(w, ip, cov)
            if v:
                note = f"조건 적용 후 IPS 위반({'; '.join(v)}) — 조건부 승인 무효, 현 보유 유지"
                w = holding
        new = w
    else:
        new = holding
        if new is None:
            raise ValueError("첫 분기에 채택안이 없거나 반려되면 보유 포트폴리오가 없다 — IPS를 점검하라")
    hp = os.path.join(out_dir, "holdings.json")
    json.dump({"as_of": as_of, "decision": dec, "condition": cond, "weights": new}, open(hp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    shown = dec if winner else "현 보유 유지(권고안 없음)"
    L = [f"# CIO 결정 — {as_of}", "", f"**{shown}**" + (f" (조건: `{cond}`)" if cond and winner else ""), "", f"사유: {why}"]
    if winner:
        L.append(f"\nIC 권고안: `{winner}`")
    if note:
        L.append(f"\n하네스 메모: {note}")
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    return {"outputs": [p, hp], "note": f"{shown} {cond}".strip(), "holding": new, "decision": shown}


# ---------------- meta-reviewer ----------------
def _ann3(R) -> np.ndarray:
    return np.prod(1 + R.values, axis=0) ** 4 - 1


def mae_for(q: str, delta: float, params: dict) -> float:
    prm = json.loads(json.dumps(params)); prm["cma"]["shrink_delta"] = delta
    mu = np.array(cma(q, prm)["mu"])
    real = _ann3(data.realized(q, 3))
    return float(np.mean(np.abs(mu - real)))


def meta_review(as_of: str, prev: str, prev_dir: str, out_dir: str, params: dict, hist: list, quarters: list, last_meta_idx: int | None) -> dict:
    pc = json.load(open(os.path.join(prev_dir, "cma.json")))
    R = data.realized(prev, 3)
    assert R.index[-1].strftime("%Y-%m") <= as_of, "평가 구간을 넘어 읽음"
    real = _ann3(R)
    mu = np.array(pc["mu"])
    err = real - mu
    mae = float(np.mean(np.abs(err)))
    ports = {}
    for f in sorted(os.listdir(os.path.join(prev_dir, "proposals"))):
        pr = json.load(open(os.path.join(prev_dir, "proposals", f)))
        ports[pr["agent"]] = round(float(np.prod(1 + R.values @ np.array(pr["w"])) - 1), 6)
    el = json.load(open(os.path.join(prev_dir, "eligibility.json")))
    hold = json.load(open(os.path.join(prev_dir, "holdings.json")))["weights"]
    adopted = round(float(np.prod(1 + R.values @ np.array([hold[t] for t in TICKERS])) - 1), 6)
    maes = [h for h in hist] + [mae]
    m = params["meta"]
    roll = float(np.mean(maes[-m["lookback_quarters"]:]))
    props = []
    d0 = params["cma"]["shrink_delta"]
    i = quarters.index(as_of)
    if len(maes) >= 2 and roll > m["mae_trigger"] and d0 < 0.9 - 1e-9 and (last_meta_idx is None or i - last_meta_idx >= 4):
        d1 = round(min(0.9, d0 + m["delta_step"]), 2)
        import pandas as pd
        # 테스트 구간: 결정 시점 이전의 분기 말 8개 — 각 시점의 μ를 그 시점 데이터로 다시 추정하고, 실현은 as_of 이전 것만 쓴다
        tq = [(data._month(as_of) - pd.DateOffset(months=3 * k)).strftime("%Y-%m") for k in range(m["test_quarters"], 0, -1)]
        a = float(np.mean([mae_for(q, d0, params) for q in tq])); b = float(np.mean([mae_for(q, d1, params) for q in tq]))
        props.append({"id": f"P-{as_of}-meta-delta", "kind": "param", "by": "meta-reviewer", "target": "cma-builder 스킬 파라미터",
                      "path": ["cma", "shrink_delta"], "old": d0, "new": d1,
                      "change": f"기대수익률 수축 강도 δ {d0} → {d1}",
                      "why": f"최근 {len(maes[-m['lookback_quarters']:])}분기 평균 예측오차 {roll:.1%} > 기준 {m['mae_trigger']:.0%}",
                      "test": {"quarters": tq, "mae_current": round(a, 6), "mae_new": round(b, 6), "improved": b < a,
                               "summary": f"과거 {len(tq)}분기 재추정 MAE {a:.2%} → {b:.2%}"}})
    res = {"as_of": as_of, "evaluated": prev, "months": [R.index[0].strftime("%Y-%m"), R.index[-1].strftime("%Y-%m")],
           "asset_error_ann": dict(zip(TICKERS, np.round(err, 6).tolist())), "mae": round(mae, 6), "rolling_mae": round(roll, 6),
           "quarter_return": ports, "adopted_quarter_return": adopted,
           "rejected_but_better": [k for k, ok in el.items() if not ok["eligible"] and ports.get(k, -9) > adopted],
           "proposals": [p["id"] for p in props], "auto_applied": False}
    p = os.path.join(out_dir, "meta_review.json")
    json.dump(res, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    outs = [p]
    for pr in props:
        q = os.path.join(out_dir, "proposals_change", pr["id"] + ".json")
        os.makedirs(os.path.dirname(q), exist_ok=True)
        json.dump(pr, open(q, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        outs.append(q)
    return {"outputs": outs, "note": f"MAE {mae:.1%}, 4분기 평균 {roll:.1%}, 제안 {len(props)}건 (자동 반영 없음)", "res": res, "proposals": props}
