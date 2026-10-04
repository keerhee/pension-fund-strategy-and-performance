# -*- coding: utf-8 -*-
"""2팀 교육용 모의 패널 생성기 — 데이터 생성 과정(DGP)을 공개한다.
이 자료는 '증거'가 아니라 이론의 작동 방식을 보여 주도록 설계한 교육용 데이터다.
python3 build_panel.py            # 기본 시드 71 → kh_panel_kic.csv (배포 자료와 같다)
python3 build_panel.py --seed 5   # 다른 시드 → kh_panel_seed5.csv (결론이 시드에 따라 바뀌는지 확인)
"""
import argparse, numpy as np, pandas as pd
ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, default=71); ap.add_argument("--months", type=int, default=480)
a = ap.parse_args(); N = a.months
r = np.random.default_rng(a.seed)
e_y = r.normal(0, 0.12, N); e_p = r.normal(0, 0.08, N); e_v = r.normal(0, 2.4, N)
y = np.zeros(N); p = np.zeros(N); v = np.zeros(N); y[0], p[0], v[0] = 3.5, 2.2, 18.0
for t in range(1, N):
    y[t] = y[t-1] + 0.04 * (3.5 - y[t-1]) + e_y[t]          # 10년 금리(%): 평균 회귀
    p[t] = p[t-1] + 0.03 * (2.2 - p[t-1]) + e_p[t]          # 기대 인플레(%)
    v[t] = max(9.0, v[t-1] + 0.10 * (18 - v[t-1]) + e_v[t])  # VIX
lag = lambda x: np.r_[x[0], x[:-1]]
dv = np.diff(np.r_[v[0], v])
# 월 초과수익률(%) — 상태변수 '수준'이 다음 달 기대수익을, 상태변수 '충격'이 이번 달 실현수익을 움직인다
bond = 0.04 + 0.45 * (lag(y) - 3.5) - 15.0 * e_y + r.normal(0, 0.3, N)            # 금리 하락 → 지금 이익, 이후 기대수익 하락
eq   = 0.45 - 1.20 * (lag(p) - 2.2) + 0.04 * (lag(v) - 18) - 2.0 * e_p - 0.5 * dv + r.normal(0, 3.6, N)  # 인플레가 높으면 이후 주식 기대수익 하락
tips = 0.02 + 6.0 * e_p - 6.0 * e_y + r.normal(0, 1.0, N)                         # 인플레 상승 충격에 이익
vol  = -0.5 + 0.9 * dv + r.normal(0, 4.0, N)                                       # 평시 보유 비용, 변동성 급등 시 이익
out = "kh_panel_kic.csv" if a.seed == 71 and N == 480 else f"kh_panel_seed{a.seed}.csv"
pd.DataFrame({"date": pd.date_range("1986-12-31", periods=N, freq="ME").strftime("%Y-%m-%d"),
              "yield10": y.round(3), "infl_exp": p.round(3), "vix": v.round(2),
              "bond_long_ret": (bond/100).round(5), "tips_ret": (tips/100).round(5),
              "eq_ret": (eq/100).round(5), "vol_hedge_ret": (vol/100).round(5)}).to_csv(out, index=False)
print(out, " ".join(f"{n} 연평균 {x.mean()*12:+.1f}% · 연변동성 {x.std()*np.sqrt(12):.1f}%" for n, x in [("bond", bond), ("tips", tips), ("eq", eq), ("vol", vol)]))
