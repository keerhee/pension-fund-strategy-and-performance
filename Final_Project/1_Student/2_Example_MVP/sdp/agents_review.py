"""심의 층 — cro-agent · 상호 검토 · 투표(수정 보르다) · ic-agent

숫자(위험 지표, 점수, 득표)는 전부 코드가 계산한다.
예시 MVP의 검토 의견·투표 순위는 '각 에이전트의 평가 렌즈'로 정하는 규칙 기반 대역이다.
라이브 모드에서는 Claude Code 에이전트가 같은 숫자를 읽고 검토 문장과 순위를 직접 쓴다.
"""
from __future__ import annotations
import json, os
import numpy as np
import pandas as pd
from . import data, ips as I
from .data import TICKERS
from .agents_pc import AGENTS

ORDER = [a[0] for a in AGENTS]


# ---------------- cro-agent ----------------
def _path_ret(w, R: pd.DataFrame) -> pd.Series:
    return R[TICKERS].values @ np.asarray(w) if len(R) else pd.Series(dtype=float)


def cro(as_of: str, props: dict, c: dict, params: dict) -> dict:
    cov = np.array(c["cov"])
    R = data.returns(as_of).iloc[-params["cma"]["window_months"]:]
    out = {}
    for aid, p in props.items():
        w = np.array(p["w"])
        pr = R.values @ w
        q = np.quantile(pr, 0.05)
        cvar = float(pr[pr <= q].mean())
        rc = w * (cov @ w) / (w @ cov @ w)
        stress = {}
        for k, (a, b) in params["stress"].items():
            Rs = data.returns(as_of, start=a, end=b).loc[:b]
            stress[k] = round(float(np.prod(1 + Rs.values @ w) - 1), 6)
        v = np.cumprod(1 + pr)
        mdd = float((v / np.maximum.accumulate(v) - 1).min())
        top = np.argsort(-rc)[:3]
        out[aid] = {"exp_vol": round(float(np.sqrt(w @ cov @ w)), 6), "cvar95_m": round(cvar, 6),
                    "rc": [round(float(x), 6) for x in rc], "rc_std": round(float(np.std(rc)), 6),
                    "rc_top3": [[TICKERS[i], round(float(rc[i]), 4)] for i in top],
                    "stress": stress, "hist_mdd": round(mdd, 6)}
    return out


# ---------------- 정량 점수 M ----------------
REGIME_PENALTY = {"물가 가속": {"TLT": 1.0, "IEF": 0.5, "LQD": 0.5},
                  "곡선 역전": {"HYG": 1.0, "EEM": 0.5}}


def _minmax(x: dict) -> dict:
    v = np.array(list(x.values()), float)
    lo, hi = v.min(), v.max()
    return {k: (0.5 if hi - lo < 1e-12 else float((x[k] - lo) / (hi - lo))) for k in x}


def metric_M(as_of: str, props: dict, elig: list, c: dict, ip: dict, regime: str, params: dict) -> dict:
    if not elig:
        return {"M": {}, "components": {}}
    cov, se, rf = np.array(c["cov"]), np.array(c["se_mu"]), c["rf"]
    R = data.returns(as_of).iloc[-params["metric_window_months"]:]
    comp = {k: {} for k in ["bt_sharpe", "slack", "n_eff", "regime_fit", "est_risk"]}
    for aid in elig:
        w = np.array(props[aid]["w"])
        pr = R.values @ w
        comp["bt_sharpe"][aid] = float((pr.mean() * 12 - rf) / (pr.std() * np.sqrt(12)))
        comp["slack"][aid] = I.slack(dict(zip(TICKERS, w)), ip, cov)
        comp["n_eff"][aid] = I.n_eff(w)
        pen = REGIME_PENALTY.get(regime, {})
        comp["regime_fit"][aid] = -sum(pen.get(t, 0) * w[i] for i, t in enumerate(TICKERS))
        comp["est_risk"][aid] = -float(w @ se)
    norm = {k: _minmax(v) for k, v in comp.items()}
    M = {aid: float(np.mean([norm[k][aid] for k in norm])) for aid in elig}
    return {"M": {k: round(v, 6) for k, v in M.items()},
            "components": {k: {a: round(x, 6) for a, x in v.items()} for k, v in comp.items()}}


# ---------------- 렌즈와 투표 ----------------
def lens_values(voter: str, props: dict, cro_r: dict) -> dict:
    """voter 가 다른 안을 보는 잣대 (클수록 좋다)."""
    cov_te = {}
    if voter == "pc-adversarial":
        W = {k: np.array(v["w"]) for k, v in props.items()}
        for k in W:
            cov_te[k] = float(np.mean([np.sum((W[k] - W[j]) ** 2) for j in W if j != k]))
    f = {"pc-equal": lambda k: I.n_eff(props[k]["w"]),
         "pc-invvol": lambda k: -props[k]["exp_vol"],
         "pc-minvar": lambda k: cro_r[k]["cvar95_m"],
         "pc-maxsharpe": lambda k: props[k]["exp_sharpe"],
         "pc-erc": lambda k: -cro_r[k]["rc_std"],
         "pc-adversarial": lambda k: cov_te[k]}[voter]
    return {k: f(k) for k in props}


def tally(ballots: dict, cands: list, top_points: list, bottom: float):
    """ballots: 투표자 → 순위 목록(좋은 순, 자기 제외). 최하위 1개는 bottom 점, 나머지 상위에 top_points."""
    S = {c: 0.0 for c in cands}
    flags = {c: [] for c in cands}
    for voter, ranking in ballots.items():
        if not ranking:
            continue
        if len(ranking) == 1:
            S[ranking[0]] += top_points[0]
            continue
        body, last = ranking[:-1], ranking[-1]
        for pts, c in zip(top_points, body):
            S[c] += pts
        S[last] += bottom
        flags[last].append(voter)
    return S, flags


def blend(S: dict, M: dict, lam: float) -> dict:
    if not S:
        return {}
    Sh = _minmax(S)
    return {k: {"S": S[k], "S_hat": round(Sh[k], 6), "M": round(M[k], 6), "score": round(lam * Sh[k] + (1 - lam) * M[k], 6)} for k in S}


def borda_example() -> dict:
    """과제 문서 §5 M8 검산 예제 — 정답 Score = (0.473, 0.850, 0.900, 0.450), 채택 C."""
    ballots = {"A": ["B", "C", "D"], "B": ["C", "A", "D"], "C": ["B", "A", "D"], "D": ["C", "B", "A"]}
    S, _ = tally(ballots, ["A", "B", "C", "D"], [2, 1], -2)
    res = blend(S, {"A": 0.40, "B": 0.70, "C": 0.80, "D": 0.90}, 0.5)
    win = max(res, key=lambda k: (res[k]["score"], -"ABCD".index(k)))
    return {"S": S, "score": {k: round(v["score"], 3) for k, v in res.items()}, "winner": win}


def vote(props: dict, elig: list, cro_r: dict, Mres: dict, params: dict) -> dict:
    ballots = {}
    for voter in ORDER:
        lv = lens_values(voter, props, cro_r)
        cand = [k for k in elig if k != voter]
        ballots[voter] = sorted(cand, key=lambda k: (-lv[k], ORDER.index(k)))
    vp = params["vote"]
    S, flags = tally(ballots, elig, vp["top_points"], vp["bottom_points"])
    res = blend(S, Mres["M"], vp["lambda"])
    ranking = sorted(elig, key=lambda k: (-res[k]["score"], ORDER.index(k)))
    return {"ballots": ballots, "rule": f"자기 제외 상위 {len(vp['top_points'])}개 {vp['top_points']}점 · 최하위 {vp['bottom_points']}점 · λ={vp['lambda']}",
            "result": res, "bottom_flags": flags, "ranking": ranking, "winner": ranking[0] if ranking else None}


# ---------------- 상호 검토 ----------------
def reviews(props: dict, elig: list, cro_r: dict, ip: dict, c: dict) -> list:
    cov = np.array(c["cov"])
    out = []
    for j, rv in enumerate(ORDER):
        for d in (1, 3):
            tg = ORDER[(j + d) % len(ORDER)]
            p = props[tg]
            w = dict(zip(TICKERS, p["w"]))
            if tg not in elig:
                out.append({"reviewer": rv, "target": tg, "verdict": "해당 없음", "items": ["IPS 위반으로 기각된 안"]})
                continue
            warn, items = 0, []
            s = I.slack(w, ip, cov)
            items.append(f"IPS 여유 {s:.3f}" + (" — 경계에 붙어 있음" if s < 0.01 else ""))
            warn += s < 0.01
            mx = max(p["w"]); ne = I.n_eff(p["w"])
            items.append(f"최대 비중 {mx:.1%}, 유효 종목 수 {ne:.2f}" + (" — 집중" if ne < 5 else ""))
            warn += ne < 5
            st = cro_r[tg]["stress"]["rate_shock_2022"]
            items.append(f"2022 금리 충격 재현 손실 {st:.1%}" + (" — 큼" if st < -0.15 else ""))
            warn += st < -0.15
            lv = lens_values(tg, props, cro_r)
            rank = sorted(elig, key=lambda k: -lv[k]).index(tg) + 1 if tg in lv else None
            items.append(f"근거 일관성: 자기 목적('{p['lens']}')에서 적격안 중 {rank}위" + ("" if rank == 1 else " — 목적과 결과 불일치"))
            warn += (rank != 1) and tg not in ("pc-equal", "pc-invvol")
            out.append({"reviewer": rv, "target": tg, "verdict": ["지지", "조건부 지지", "반대"][min(int(warn), 2)], "items": items})
    return out


# ---------------- ic-agent ----------------
def ic_report(as_of, props, viol, cro_r, v, revs, regime, research_prop, meta_props, holding, out_dir) -> str:
    L = [f"# IC 보고서 — {as_of}", "", f"국면: **{regime['label']}** · 투표 규칙: {v['rule']}", ""]
    if v["winner"] is None:
        L += ["**권고안 없음** — 모든 안이 IPS 위반으로 기각됐다. CIO의 개입이 필요하다.", ""]
    else:
        w0 = v["winner"]; ru = v["ranking"][1] if len(v["ranking"]) > 1 else None
        L += [f"## 권고: {props[w0]['method']} (`{w0}`)", ""]
        if ru:
            L += [f"차점: {props[ru]['method']} (`{ru}`) — 점수 차 {v['result'][w0]['score'] - v['result'][ru]['score']:.3f}", ""]
        wr = dict(zip(TICKERS, props[w0]["w"]))
        L += ["| " + " | ".join(TICKERS) + " |", "|" + "---|" * len(TICKERS),
              "| " + " | ".join(f"{wr[t]:.1%}" for t in TICKERS) + " |", ""]
        if holding:
            to = 0.5 * sum(abs(wr[t] - holding.get(t, 0)) for t in TICKERS)
            L += [f"현재 보유 대비 회전율 {to:.1%}", ""]
    L += ["## 후보 비교", "", "| 안 | 점수 | 득표 S | 정량 M | 최하위 지목 | 기대수익 | 사전 변동성 | N_eff | 2022 충격 |", "|---|---|---|---|---|---|---|---|---|"]
    for k in v["ranking"]:
        r = v["result"][k]
        L.append(f"| {props[k]['method']} | {r['score']:.3f} | {r['S']:.0f} | {r['M']:.3f} | {len(v['bottom_flags'][k])} | "
                 f"{props[k]['exp_ret']:.2%} | {props[k]['exp_vol']:.2%} | {I.n_eff(props[k]['w']):.2f} | {cro_r[k]['stress']['rate_shock_2022']:.1%} |")
    L += [""]
    rej = [k for k in props if viol[k]]
    L += ["## 기각된 안", ""] + ([f"- {props[k]['method']}: " + "; ".join(viol[k]) for k in rej] or ["- 없음"]) + [""]
    if v["ranking"]:
        most = max(v["ranking"], key=lambda k: (len(v["bottom_flags"][k]), -v["ranking"].index(k)))
        if v["bottom_flags"][most]:
            L += ["## 반대 의견", "", f"- 최하위 지목 최다: {props[most]['method']} ({len(v['bottom_flags'][most])}표 — {', '.join(v['bottom_flags'][most])})"]
        if v["winner"]:
            rv = [r for r in revs if r["target"] == v["winner"]]
            for r in rv:
                L.append(f"- {r['reviewer']}의 검토: **{r['verdict']}** — " + " / ".join(r["items"]))
        L += [""]
    L += ["## CIO가 판단할 것", ""]
    L.append("- 권고안을 승인 / 조건부 승인(조건 명시) / 반려(현 보유 유지) 중 하나로 결정")
    if research_prop:
        L.append(f"- 리서치 에이전트의 IPS 변경 제안 `{research_prop['id']}`: {research_prop['change']}")
    for mp in meta_props:
        L.append(f"- 메타 리뷰 변경 제안 `{mp['id']}`: {mp['change']} (테스트: {mp['test']['summary']})")
    p = os.path.join(out_dir, "ic_report.md")
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    return p
