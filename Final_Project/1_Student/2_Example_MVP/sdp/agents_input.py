"""입력 층 — macro-agent · cma-builder · research-agent

예시 MVP에서는 세 에이전트의 '판단 문장'을 규칙 기반 대역(stand-in)이 쓴다.
라이브 모드에서는 Claude Code 에이전트가 같은 숫자(json)를 읽고 문장(md)만 새로 쓴다 — 숫자는 언제나 코드가 만든다.
"""
from __future__ import annotations
import json, os
import numpy as np
import pandas as pd
from . import data


# ---------------- macro-agent ----------------
def regime_of(m: pd.DataFrame) -> dict:
    cpi = m["CPIAUCSL"].dropna()
    infl = float(cpi.iloc[-1] / cpi.iloc[-13] - 1)
    infl_6m_ago = float(cpi.iloc[-7] / cpi.iloc[-19] - 1)
    d10 = float(m["DGS10"].dropna().iloc[-1] - m["DGS10"].dropna().iloc[-7])
    curve = float(m["T10Y2Y"].dropna().iloc[-1])
    spread = float(m["BAA10Y"].dropna().iloc[-1])
    if infl >= 0.04 and infl - infl_6m_ago >= 0:
        label = "물가 가속"
    elif infl >= 0.03 and infl - infl_6m_ago < 0:
        label = "디스인플레이션"
    elif curve < 0:
        label = "곡선 역전"
    else:
        label = "안정"
    return {"label": label, "cpi_yoy": round(infl, 4), "cpi_yoy_6m_ago": round(infl_6m_ago, 4),
            "dgs10_chg_6m": round(d10, 3), "t10y2y": round(curve, 3), "baa10y": round(spread, 3),
            "dgs3mo": round(float(m["DGS3MO"].dropna().iloc[-1]), 3)}


def macro_agent(as_of: str, out_dir: str) -> dict:
    r = regime_of(data.macro(as_of))
    json.dump(r, open(os.path.join(out_dir, "macro.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = (f"# 매크로 국면 — {as_of}\n\n**국면: {r['label']}** (규칙 판정)\n\n"
          f"- 물가 상승률(전년 대비, 1개월 지연 반영) {r['cpi_yoy']:.1%}, 6개월 전 {r['cpi_yoy_6m_ago']:.1%}\n"
          f"- 10년 금리 6개월 변화 {r['dgs10_chg_6m']:+.2f}%p, 장단기 금리차 {r['t10y2y']:+.2f}%p, 신용 스프레드 {r['baa10y']:.2f}%p\n"
          f"- 해석(대역): 국면 '{r['label']}'에서는 "
          + {"물가 가속": "듀레이션이 긴 채권의 손실 위험이 크다.",
             "디스인플레이션": "금리 정점 이후 채권의 회복 가능성이 있으나 변동성이 크다.",
             "곡선 역전": "경기 둔화 신호 — 하이일드·신흥국 신용 위험에 유의한다.",
             "안정": "특정 자산을 피할 국면 신호는 없다."}[r["label"]] + "\n")
    p = os.path.join(out_dir, "macro.md")
    open(p, "w", encoding="utf-8").write(md)
    return {"outputs": [os.path.join(out_dir, "macro.json"), p], "note": f"국면 {r['label']}", "regime": r}


# ---------------- cma-builder ----------------
def ledoit_wolf(X: np.ndarray) -> tuple[np.ndarray, float]:
    """Ledoit–Wolf(2004) 수축 — 목표는 평균 분산 × 단위행렬."""
    T, N = X.shape
    Xc = X - X.mean(0)
    S = Xc.T @ Xc / T
    mu = np.trace(S) / N
    F = mu * np.eye(N)
    d2 = np.sum((S - F) ** 2)
    b2 = sum(np.sum((np.outer(x, x) - S) ** 2) for x in Xc) / T ** 2
    b2 = min(b2, d2)
    a = b2 / d2 if d2 > 0 else 1.0
    return a * F + (1 - a) * S, float(a)


def cma(as_of: str, params: dict) -> dict:
    w = params["cma"]["window_months"]
    R = data.returns(as_of).iloc[-w:]
    mu_hist = R.mean().values * 12
    delta = params["cma"]["shrink_delta"]
    mu = (1 - delta) * mu_hist + delta * mu_hist.mean()
    S, a = ledoit_wolf(R.values)
    cov = S * 12
    se = R.std().values * 12 / np.sqrt(len(R))
    rf = float(data.macro(as_of)["DGS3MO"].dropna().iloc[-1]) / 100
    return {"as_of": as_of, "window": [R.index[0].strftime("%Y-%m"), R.index[-1].strftime("%Y-%m")], "T": len(R),
            "shrink_delta": delta, "lw_shrinkage": round(a, 6), "rf": round(rf, 6),
            "tickers": data.TICKERS, "mu": np.round(mu, 6).tolist(), "mu_hist": np.round(mu_hist, 6).tolist(),
            "se_mu": np.round(se, 6).tolist(), "cov": np.round(cov, 8).tolist()}


def cma_builder(as_of: str, out_dir: str, params: dict) -> dict:
    c = cma(as_of, params)
    p = os.path.join(out_dir, "cma.json")
    json.dump(c, open(p, "w", encoding="utf-8"), indent=1)
    return {"outputs": [p], "note": f"μ 수축 δ={c['shrink_delta']}, LW 수축 {c['lw_shrinkage']:.3f}, 표본 {c['window'][0]}~{c['window'][1]}", "cma": c}


# ---------------- research-agent ----------------
def research_agent(as_of: str, out_dir: str, regime: dict, prev_regime: dict | None, history: list) -> dict:
    """대역 규칙: 국면이 바뀌면 메모를 쓰고, 처음 보는 '물가 가속' 국면이면 IPS 변경을 제안한다."""
    changed = prev_regime is not None and prev_regime["label"] != regime["label"]
    seen = {h["label"] for h in history}
    lines = [f"# 리서치 메모 — {as_of}", "", f"자료: {as_of} 이전 공개 자료만 사용 (시점 잠금)", ""]
    proposal = None
    if regime["label"] == "물가 가속" and "물가 가속" not in seen:
        proposal = {"id": f"P-{as_of}-research-ips", "kind": "ips", "by": "research-agent", "target": "ips.md 4항",
                    "change": "채권군 하한 25% → 15% 한시 완화 (물가 가속 국면 동안)",
                    "why": f"물가 {regime['cpi_yoy']:.1%} 가속 국면에서 듀레이션 손실 위험이 크다",
                    "test": {"improved": None, "summary": "정책 변경은 백테스트로 검증하지 않음 — CIO 판단"}}
        lines += ["결론: **IPS 변경 제안** — " + proposal["change"], "", "근거: " + proposal["why"]]
    elif changed:
        lines += [f"결론: 현행 유지 — 국면 전환 감지 ({prev_regime['label']} → {regime['label']}). 다음 분기 재점검."]
    else:
        lines += [f"결론: 현행 유지 — 국면 '{regime['label']}' 지속."]
    inj = os.environ.get("SDP_INJECT_MEMO")  # 결함 주입 시험(L3)용 — 채점 콘솔만 쓴다
    if inj:
        lines += ["", "참고 자료: " + inj]
    p = os.path.join(out_dir, "research_memo.md")
    open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return {"outputs": [p], "note": "변경 제안 1건" if proposal else "현행 유지", "proposal": proposal}
