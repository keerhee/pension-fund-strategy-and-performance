# 보너스 D — 데이터와 도구

| 파일 | 내용 |
|---|---|
| `fetch_real_data.py` | 인터넷이 되는 PC에서 실행한다. FRED(DGS10 · T10YIE · VIXCLS · TB3MS)와 ETF(TLT · TIP · ACWI · VIXY) 월말 자료로 `real_panel.csv`를 만든다. 필요한 패키지: pandas, yfinance |
| `hedging_tool.py` | [0] 간편 공식 · [1]~[4] VAR(1) → 1년 · 10년 CRRA 최적 비중 → 헤징 수요 · CE 기여. `--panel real_panel.csv`로 실제 자료를 넣는다 |
| `kh_instruments.csv` | 수단별 상태변수와 연 비용(5 · 15 · 40bp) |
| `kh_panel_kic.csv` | 비교 기준 — 본 과제 2팀이 쓴 40년 교육용 모의 자료 |

주의
- 실제 자료는 기간이 짧다(VIXY 2011년~, ACWI 2008년~ → 약 15년). 겹치지 않는 1년 구간이 15개 안팎이다.
- ETF 수익률에는 운용 보수가 이미 빠져 있다. 도구의 비용(cost_bp)과 이중으로 빠지는 점을 감안한다.
- 데이터 출처 사이트가 바뀌어 스크립트가 실패하면 같은 열(date · yield10 · infl_exp · vix · bond_long_ret · tips_ret · eq_ret · vol_hedge_ret, 월 초과수익률은 소수)로 CSV를 직접 만들어도 된다.
