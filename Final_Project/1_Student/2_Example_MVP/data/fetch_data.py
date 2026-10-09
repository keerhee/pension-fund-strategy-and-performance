"""데이터 내려받기 — 팀은 자기 유니버스·지표로 바꿔 쓴다. 실행: python data/fetch_data.py"""
import io, urllib.request
import pandas as pd

TICKERS = ["SPY", "EFA", "EEM", "IEF", "TLT", "LQD", "HYG", "TIP", "VNQ", "GLD", "DBC"]
FRED = ["DGS3MO", "DGS10", "T10Y2Y", "CPIAUCSL", "UNRATE", "BAA10Y"]
START, END = "2015-07-01", "2025-07-31"


def etf():
    import yfinance as yf
    px = yf.download(TICKERS, start=START, end=END, interval="1mo", auto_adjust=True, progress=False)["Close"][TICKERS].dropna()
    r = px.pct_change().dropna() * 100
    r.index.name = "date"; r.columns = ["ret_" + c for c in r.columns]
    r.round(4).to_csv("data/panel_monthly.csv")


def fred():
    out = []
    for s in FRED:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}&cosd=2014-01-01&coed={END}&fq=Monthly&fam=avg"
        df = pd.read_csv(io.BytesIO(urllib.request.urlopen(url, timeout=30).read()))
        df.columns = ["date", s]; df["date"] = pd.to_datetime(df["date"])
        out.append(df.set_index("date"))
    m = pd.concat(out, axis=1)
    m.index = m.index.strftime("%Y-%m-01"); m.index.name = "date"
    m.round(4).to_csv("data/macro_monthly.csv")


if __name__ == "__main__":
    etf(); fred(); print("data/ 갱신 — DATA.md 의 '내려받은 날짜'를 고친다")
