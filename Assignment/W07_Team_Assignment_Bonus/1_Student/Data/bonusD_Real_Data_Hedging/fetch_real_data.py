#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""(선택 과제) 실제 데이터로 2팀 패널 만들기 — 인터넷 연결이 필요하다.

만드는 파일: real_panel.csv (kh_panel_kic.csv와 같은 열)
  yield10        미국 10년 국채 금리(%)          FRED DGS10 월말
  infl_exp       10년 기대 인플레(BEI, %)        FRED T10YIE 월말
  vix            VIX                             FRED VIXCLS 월말
  *_ret          월 초과수익률(소수) = ETF 월 수익률 − 3개월 국채(FRED TB3MS ÷ 12)
                 장기 국채 TLT · 물가연동채 TIP · 주식 ACWI · 변동성 헤지 VIXY
주의
  - 기간이 짧다(VIXY 2011년~, ACWI 2008년~). 겹치지 않는 1년 구간이 15개 안팎이라 예측력 검정의 힘이 약하다.
  - ETF 수익률에는 보수가 이미 빠져 있다. 도구의 비용(cost_bp)과 이중 차감되는 점을 감안하라.
  - 필요한 패키지: pandas, yfinance  (pip install yfinance)

사용법
  python3 fetch_real_data.py                 # → real_panel.csv
  python3 hedging_tool.py --panel real_panel.csv
"""
import io, sys, urllib.request
import pandas as pd

FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
ETF = {"bond_long_ret": "TLT", "tips_ret": "TIP", "eq_ret": "ACWI", "vol_hedge_ret": "VIXY"}


def fred(code):
    raw = urllib.request.urlopen(FRED.format(code), timeout=30).read().decode()
    df = pd.read_csv(io.StringIO(raw)); df.columns = ["date", code]
    df["date"] = pd.to_datetime(df["date"]); df[code] = pd.to_numeric(df[code], errors="coerce")
    return df.set_index("date")[code].resample("ME").last()


def etf_prices(tickers):
    import yfinance as yf
    px = yf.download(list(tickers), start="2000-01-01", auto_adjust=True, progress=False)["Close"]
    return px.resample("ME").last()


def build(states, rf_annual_pct, prices):
    """states: DataFrame(yield10, infl_exp, vix) 월말 · rf_annual_pct: Series(%) · prices: DataFrame(티커별 월말 가격)"""
    ret = prices.pct_change()
    out = states.copy()
    for col, tk in ETF.items():
        out[col] = ret[tk] - rf_annual_pct / 100 / 12
    out = out.dropna()
    out.index = out.index.strftime("%Y-%m-%d"); out.index.name = "date"
    return out.round(5)


if __name__ == "__main__":
    try:
        st = pd.concat({"yield10": fred("DGS10"), "infl_exp": fred("T10YIE"), "vix": fred("VIXCLS")}, axis=1)
        rf = fred("TB3MS"); px = etf_prices(ETF.values())
    except Exception as e:
        sys.exit(f"데이터를 받지 못했다: {e}\n인터넷 연결과 yfinance 설치를 확인하라. 보너스 D는 실제 자료가 있어야 풀 수 있다. 인터넷이 되는 PC나 Google Colab에서 다시 실행하라.")
    panel = build(st, rf, px)
    panel.to_csv("real_panel.csv")
    print(f"real_panel.csv 저장 — {panel.index[0]} ~ {panel.index[-1]} · {len(panel)}개월")
