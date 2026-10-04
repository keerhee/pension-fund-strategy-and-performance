#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""국민연금 기관형 글라이드패스 계산 도구 — W07 팀 과제 1팀용

사용법
  python3 glidepath_tool.py                                  # 세 안(A 현행 유지 · B 트리거형 · C 즉시 감축) 비교
  python3 glidepath_tool.py --start 2042 --speed 1 --floor 50   # 임의의 경로: 감축 시작 연도 · 연 감축 %p · 종점 %
  python3 glidepath_tool.py --tw-target 35 --loss-max 1.2 --buffer 1.0   # 판정 기준 변경
  python3 glidepath_tool.py --mu-risk 7                       # 자본시장 가정(위험자산 기대수익) 변경

판정 기준(출처를 구분한다 — 공시: 바꿀 수 없는 사실 · 교육용: 위원회가 정할 값)
  ① 감축 시작: H/F < 0.65 ÷ (총자산 기준 목표 위험 비중) − 1. 목표 40%면 0.625 (교육용 · --tw-target)
  ② 종점 기대수익 ≥ 5.5% (공시: 2025 연금개혁이 전제한 기금수익률 · --hurdle로 민감도만)
  ③ 정점 이후 1σ 연간 손실액 ≤ 그해 급여 1년치 (교육용 · --loss-max)
  ④ 소진 ≥ 2071년 (공시: 2025 재정추계 수익률 5.5% 시나리오 · --deplete-min)
  ⑤ 순유출 이후 안전자산 ≥ 급여 1.5년치 (교육용 · --buffer)

출력
  [1] 인적자본 비율 H/F — 향후 30년 보험료 수입의 현재가치(H) ÷ 기금(F), 연도별 표와 감축 시작 임계 연도
  [2] 허들 — 기대수익 5.5% 이상이 되는 최소 위험자산 비중
  [3] 안별 판정 — 정점 · 소진 연도 · 1σ 손실액/급여 · 유동성 버퍼 · 위기 충격 1회의 소진 앞당김, 기준 ①~⑤
모든 현금흐름은 교육용 추계(2025 재정추계의 정점 · 소진에 맞춘 가정)이며 수익률은 기대수익으로 굴린다.
"""
import argparse, os
import numpy as np, pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--start", type=int, default=None); ap.add_argument("--speed", type=float, default=1.0); ap.add_argument("--floor", type=float, default=None)
ap.add_argument("--tw-target", type=float, default=40.0, help="총자산(F+H) 기준 목표 위험자산 비중 %%")
ap.add_argument("--hurdle", type=float, default=None); ap.add_argument("--loss-max", type=float, default=None)
ap.add_argument("--buffer", type=float, default=None); ap.add_argument("--deplete-min", type=int, default=None)
ap.add_argument("--mu-risk", type=float, default=None, help="위험자산 기대수익 %%"); ap.add_argument("--sig-risk", type=float, default=None)
a = ap.parse_args()

P = pd.read_csv(f"{D}/gp_params.csv").set_index("key").value
f = lambda k: float(P[k])
cf = pd.read_csv(f"{D}/gp_cashflow.csv"); gp = pd.read_csv(f"{D}/gp_glidepaths.csv")
cma = pd.read_csv(f"{D}/gp_cma.csv").set_index("asset"); sc = pd.read_csv(f"{D}/gp_scenarios.csv").set_index("scenario")
MU_R, MU_S, SG_R, SG_S, RHO = cma.mu_pct["risk"], cma.mu_pct["safe"], cma.sigma_pct["risk"], cma.sigma_pct["safe"], f("rho")
if a.mu_risk is not None: MU_R = a.mu_risk
if a.sig_risk is not None: SG_R = a.sig_risk
F0 = f("fund_2025_trn"); HURDLE = a.hurdle if a.hurdle is not None else f("hurdle_pct"); DISC = f("disc")
DEP_MIN = a.deplete_min if a.deplete_min is not None else int(f("deplete_55_official"))
HF_TRIG = round(f("ref_port_risk") / (a.tw_target / 100) - 1, 3)
LOSS_MAX = a.loss_max if a.loss_max is not None else f("loss_ratio_max"); BUF = a.buffer if a.buffer is not None else f("buffer_years")

def mu_sig(w):
    mu = w * MU_R + (1 - w) * MU_S
    return mu, ((w * SG_R) ** 2 + ((1 - w) * SG_S) ** 2 + 2 * w * (1 - w) * SG_R * SG_S * RHO) ** 0.5
def project(w, shock=None):
    F = F0; rows = []
    for i, r in cf.iterrows():
        y = int(r.year)
        ret = (w[i] * shock[1][0] + (1 - w[i]) * shock[1][1]) if (shock and y in shock[0]) else mu_sig(w[i])[0]
        Fb = F; F = F * (1 + ret / 100) + r.contrib_trn_krw - r.benefit_trn_krw
        rows.append((y, Fb, max(F, 0.0), w[i]))
        if F <= 0: break
    return pd.DataFrame(rows, columns=["year", "fund_begin", "fund_end", "w_risk"])
def deplete(p):
    d = p[p.fund_end <= 0].year; return int(d.min()) if len(d) else None

# [1] H/F
c = cf.contrib_trn_krw.values; HW = int(f("h_window"))
H = np.array([sum(c[j] / (1 + DISC) ** (j - i + 1) for j in range(i, min(i + HW, len(c)))) for i in range(len(c))])
baseA = project(gp.w_risk_A.values); n = len(baseA); hf = H[:n] / baseA.fund_begin.values
trig = int(baseA.year[np.argmax(hf < HF_TRIG)])
net_out = int(cf.year[np.argmax(cf.benefit_trn_krw > cf.contrib_trn_krw)])
peakA = int(baseA.loc[baseA.fund_end.idxmax()].year)
print(f"=== 국민연금 기관형 글라이드패스 — 위험자산 {MU_R}%/{SG_R}% · 안전자산 {MU_S}%/{SG_S}% ===")
print(f"    판정 기준: ① H/F < {HF_TRIG}(총자산 기준 목표 {a.tw_target:g}%, 교육용) · ② 종점 기대수익 ≥ {HURDLE}%(공시) · ③ 1σ 손실/급여 ≤ {LOSS_MAX:g}년치(교육용) · ④ 소진 ≥ {DEP_MIN}년(공시) · ⑤ 버퍼 ≥ {BUF:g}년치(교육용)")
print(f"[1] 인적자본 비율 H/F (H = 향후 {HW}년 보험료 수입의 현재가치, 할인율 {DISC*100:.1f}%)")
for y in [2026, 2030, 2035, 2040, 2042, 2045, 2050, 2055, 2060]:
    i = int(np.where(baseA.year == y)[0][0])
    tot = baseA.fund_begin[i] + H[i]
    print(f"    {y}: H {H[i]:>6,.0f}조 · F {baseA.fund_begin[i]:>6,.0f}조 · H/F {hf[i]:.2f} · 총자산(F+H) 기준 위험자산 비중 {0.65*baseA.fund_begin[i]/tot*100:.1f}%")
print(f"    → H/F가 {HF_TRIG} 아래로 내려가는 첫해 = {trig}년 · 순유출(급여 > 보험료) 전환 = {net_out}년 · 현행(65%) 유지 시 기금 정점 = {peakA}년")
w_h = (HURDLE - MU_S) / (MU_R - MU_S)
print(f"[2] 허들 — 기대수익 μ(w) = w×{MU_R} + (1−w)×{MU_S} ≥ {HURDLE}% → 최소 위험자산 비중 {w_h*100:.0f}%")

paths = {"A 현행 유지(65% 고정)": gp.w_risk_A.values, "B 트리거형(2042년부터, 종점 50%)": gp.w_risk_B.values, "C 즉시 감축(2027년부터, 종점 45%)": gp.w_risk_C.values}
if a.start:
    fl = a.floor if a.floor is not None else 50
    paths = {f"사용자 경로({a.start}년부터 연 {a.speed}%p, 종점 {fl:.0f}%)": np.array([0.65 if y < a.start else max(fl, 65 - a.speed * (y - a.start + 1)) / 100 for y in cf.year])}
print(f"[3] 안별 판정 — ① 감축 시작 ≥ {trig}년 · ② 종점 ≥ {w_h*100:.0f}% · ③ 1σ 손실/급여 ≤ {LOSS_MAX:g}년치 · ④ 소진 ≥ {DEP_MIN:.0f}년 · ⑤ 버퍼 ≥ {BUF}년치")
for name, w in paths.items():
    start = int(cf.year[np.argmax(w < 0.649)]) if (w < 0.649).any() else None
    base = project(w); dep = deplete(base); pk = base.loc[base.fund_end.idxmax()]
    lr = [(int(r.year), r.w_risk * SG_R / 100 * r.fund_begin / cf.benefit_trn_krw[cf.year == r.year].iloc[0]) for _, r in base.iterrows() if r.year >= peakA and r.fund_begin > 0]
    lr_max = max(v for _, v in lr)
    buf = [((1 - r.w_risk) * r.fund_begin / cf.benefit_trn_krw[cf.year == r.year].iloc[0], int(r.year)) for _, r in base.iterrows() if net_out <= r.year <= (dep or 2095) - 5 and r.fund_begin > 0]
    bmin = min(buf)
    seq = {}
    for sy in [2027, net_out, 2050]:
        ds = deplete(project(w, ({sy}, (sc.risk_ret_pct["2008형"], sc.safe_ret_pct["2008형"]))))
        seq[sy] = (dep - ds) if (dep and ds) else None
    ok = [start is None or start >= trig, w[-1] >= w_h - 1e-9, lr_max <= LOSS_MAX, bool(dep and dep >= DEP_MIN), bmin[0] >= BUF]
    print(f"\n  ◆ {name}")
    print(f"    감축 시작 {start or '없음'} · 종점 {w[-1]*100:.0f}% · 기대수익 {mu_sig(w[0])[0]:.2f}% → {mu_sig(w[-1])[0]:.2f}%")
    print(f"    기금 정점 {int(pk.year)}년 {pk.fund_end:,.0f}조 · 소진 {dep}년")
    print(f"    정점 이후 1σ 연간 손실액 ÷ 그해 급여 최대 {lr_max:.2f}년치 · 순유출 이후 안전자산 ÷ 급여 최소 {bmin[0]:.1f}년치({bmin[1]}년)")
    print(f"    2008형 충격(위험 −22% · 안전 +4%) 1회의 소진 앞당김 — 2027년 {seq[2027]}년 · {net_out}년 {seq[net_out]}년 · 2050년 {seq[2050]}년")
    print("    판정 " + " · ".join(f"{s} {'통과' if o else '탈락'}" for s, o in zip("①②③④⑤", ok)))
