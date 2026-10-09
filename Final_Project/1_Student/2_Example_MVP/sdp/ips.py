"""ips-guardian — IPS 를 읽어 제약을 만들고, 배분안의 위반 여부를 판정한다."""
from __future__ import annotations
import os, re
import numpy as np
import yaml
from .data import ROOT, TICKERS


def load(path: str | None = None) -> dict:
    txt = open(path or os.path.join(ROOT, "ips.md"), encoding="utf-8").read()
    m = re.search(r"```yaml\n(.*?)```", txt, re.S)
    if not m:
        raise ValueError("ips.md 에 기계가 읽는 yaml 블록이 없다")
    return yaml.safe_load(m.group(1))


def n_eff(w) -> float:
    w = np.asarray(w, float)
    return float(1.0 / np.sum(w ** 2))


def check(w: dict, ips: dict, cov: np.ndarray | None = None) -> list[str]:
    """위반 사유 목록. 빈 목록이면 적격."""
    c = ips["constraints"]
    v = []
    x = np.array([w.get(t, 0.0) for t in TICKERS])
    extra = [k for k in w if k not in TICKERS]
    if extra:
        v.append(f"허용되지 않은 자산 {extra}")
    if abs(x.sum() - c["weight_sum"]) > 1e-4:
        v.append(f"비중 합 {x.sum():.4f} ≠ {c['weight_sum']}")
    if c.get("long_only") and (x < -1e-6).any():
        v.append("공매도(음의 비중)")
    if (x > c["asset_max"] + 1e-6).any():
        i = int(np.argmax(x))
        v.append(f"{TICKERS[i]} {x[i]:.1%} > 종목 상한 {c['asset_max']:.0%}")
    for g, spec in c["groups"].items():
        s = sum(w.get(t, 0.0) for t in spec["members"])
        if s < spec["min"] - 1e-6 or s > spec["max"] + 1e-6:
            v.append(f"{g} {s:.1%} 범위 [{spec['min']:.0%}, {spec['max']:.0%}] 밖")
    ne = n_eff(x) if x.sum() > 0 else 0
    if ne < c["effective_n_min"] - 1e-6:
        v.append(f"유효 종목 수 {ne:.2f} < {c['effective_n_min']}")
    if cov is not None and "vol_cap" in c:
        vol = float(np.sqrt(x @ cov @ x))
        if vol > c["vol_cap"] + 1e-6:
            v.append(f"사전 변동성 {vol:.1%} > 한도 {c['vol_cap']:.0%}")
    return v


def slack(w: dict, ips: dict, cov: np.ndarray) -> float:
    """제약까지 남은 여유 중 가장 작은 값 (0 이면 경계에 붙어 있음)."""
    c = ips["constraints"]
    x = np.array([w.get(t, 0.0) for t in TICKERS])
    s = [c["asset_max"] - x.max(), n_eff(x) / c["effective_n_min"] - 1, c["vol_cap"] - float(np.sqrt(x @ cov @ x))]
    for spec in c["groups"].values():
        g = sum(w.get(t, 0.0) for t in spec["members"])
        s += [g - spec["min"], spec["max"] - g]
    return float(min(s))
