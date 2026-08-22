"""W04 실습데이터 덱의 명세대로 월간 총수익률 패널을 만든다.
   자산 11개 x 10년(월말). 배당 포함 총수익률(auto_adjust=True)."""
import sys, time
import yfinance as yf, pandas as pd

TICKERS = ["SPY","EFA","EEM",          # 주식: 미국·선진국·신흥국
           "IEF","TLT","LQD","HYG","TIP",  # 채권: 중기국채·장기국채·IG·HY·물가연동
           "VNQ","GLD","DBC"]          # 대체: 리츠·금·원자재
START, END = "2015-07-01", "2025-07-31"

def main():
    for attempt in range(1, 6):
        try:
            px = yf.download(TICKERS, start=START, end=END, interval="1mo",
                             auto_adjust=True, progress=False, threads=False)["Close"]
            if px.dropna(how="all").empty: raise RuntimeError("빈 응답")
            break
        except Exception as e:
            print("  시도 %d 실패: %s" % (attempt, e)); time.sleep(6*attempt)
    else:
        sys.exit("데이터를 받지 못했다.")

    px = px[TICKERS].dropna()
    ret = px.pct_change().dropna() * 100          # 월간 총수익률 %
    ret.index.name = "date"
    ret.columns = ["ret_" + c for c in ret.columns]
    ret.round(4).to_csv("data/panel_monthly.csv")
    print("  저장: data/panel_monthly.csv")
    print("  기간: %s ~ %s  ·  T=%d개월  ·  N=%d자산"
          % (ret.index[0].date(), ret.index[-1].date(), len(ret), ret.shape[1]))
    print("  연율 수익률(%%): " + ", ".join(
        "%s %.1f" % (c[4:], ret[c].mean()*12) for c in ret.columns))

if __name__ == "__main__":
    main()
