"""시점 잠금(as_of) 공통 로더 — 모든 에이전트는 이 함수로만 데이터를 읽는다.

규칙
- 수익률 패널: 행 날짜 m 은 'm월 한 달의 수익률'이다. as_of=YYYY-MM 이면 그 달까지 읽을 수 있다.
- 매크로: 금리·스프레드는 그 달 평균이 월말에 알려진다(지연 0개월).
  물가(CPI)·실업률은 다음 달 중순 발표이므로 1개월 늦게 쓴다.
- as_of 이후 행을 요청하면 AsOfViolation 을 던지고 하네스가 trace 에 남긴다.
"""
from __future__ import annotations
import os
import pandas as pd

ROOT = os.environ.get("SDP_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TICKERS = ["SPY", "EFA", "EEM", "IEF", "TLT", "LQD", "HYG", "TIP", "VNQ", "GLD", "DBC"]
PUB_LAG = {"DGS3MO": 0, "DGS10": 0, "T10Y2Y": 0, "BAA10Y": 0, "CPIAUCSL": 1, "UNRATE": 1}


class AsOfViolation(Exception):
    pass


def _month(x) -> pd.Timestamp:
    return pd.Timestamp(str(x)[:7] + "-01")


def _read_panel() -> pd.DataFrame:
    p = pd.read_csv(os.path.join(ROOT, "data", "panel_monthly.csv"), parse_dates=["date"]).set_index("date")
    p.columns = [c.replace("ret_", "") for c in p.columns]
    return p[TICKERS] / 100.0


def _read_macro() -> pd.DataFrame:
    return pd.read_csv(os.path.join(ROOT, "data", "macro_monthly.csv"), parse_dates=["date"]).set_index("date")


def returns(as_of: str, start: str | None = None, end: str | None = None) -> pd.DataFrame:
    """as_of 달까지의 월간 수익률. end 가 as_of 를 넘으면 거부한다."""
    a = _month(as_of)
    if end is not None and _month(end) > a:
        raise AsOfViolation(f"as_of={as_of} 인데 {end} 까지 요청함")
    p = _read_panel()
    p = p.loc[: a]
    if start is not None:
        p = p.loc[_month(start):]
    return p


def macro(as_of: str) -> pd.DataFrame:
    """발표 지연을 반영해, as_of 시점에 실제로 알 수 있었던 값만 돌려준다."""
    a = _month(as_of)
    m = _read_macro()
    out = {}
    for col, lag in PUB_LAG.items():
        s = m[col].copy()
        s.index = s.index + pd.DateOffset(months=lag)  # 발표된 달로 옮긴다
        out[col] = s.loc[: a]
    return pd.DataFrame(out)


def realized(after: str, months: int) -> pd.DataFrame:
    """사후 평가 전용 — meta-reviewer 와 성과 계산만 부른다. 결정 단계에서 부르면 안 된다."""
    a = _month(after)
    p = _read_panel()
    return p.loc[a + pd.DateOffset(months=1): a + pd.DateOffset(months=months)]


def last_month() -> str:
    return _read_panel().index[-1].strftime("%Y-%m")
