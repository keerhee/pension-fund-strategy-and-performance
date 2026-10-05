#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H대학교 발전기금 계산 도구 — W06 팀 과제 4팀용

사용법
  python3 h_univ_tool.py                 # 세 안(A 보수형 · B 균형형 · C Yale 추종형) 비교
  python3 h_univ_tool.py --eq 50 --bond 25 --cash 5 --alt 20 --z 4.5 --lump-year 3 --staff 1   # 임의의 안

비중은 % (합계 100). z = 목표 지출률 %. lump-year = 공사비 600억 인출 연차. staff = 사모투자 전담 인력(명).

출력
  [1] 기대수익 — 안의 명목 · 실질 기대수익과 지출률 상한(실질 기대수익 − 0.5%p)
  [2] 기준 ① 충격 직후 버틸 수 있는 기간 — 2022형 · 2008형 충격 뒤 사모투자를 팔지 않고
      유동자산(주식 · 국채 · 현금)만으로 지출 · 출자 요청 · 공사비를 감당하는 연수
      (유동자산은 물가만큼만 불어난다고 보수적으로 가정)
  [3] 기준 ② 30년 실질가치 유지 확률 — 4,000개 경로 모의실험 (평시 / 첫해 2022형 충격)
  [4] 기준 ③ 운용 역량 — 직접 사모투자 요건(전담 인력 ≥ 3명 · 펀드 15개 × 100억)
  [5] 기준 ④ 위기 3년 — 충격 직후 현금 · 국채만으로 3년 지출 + 공사비 600억을 낼 수 있는가
"""
import argparse, os
import numpy as np, pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
P = pd.read_csv(f"{D}/hu_params.csv").set_index("key").value
f = lambda k: float(P[k])
panel = pd.read_csv(f"{D}/hu_panel_sim.csv")
cma = pd.read_csv(f"{D}/hu_cma.csv").set_index("asset")
sc = pd.read_csv(f"{D}/hu_scenarios.csv").set_index("scenario")
cfl = pd.read_csv(f"{D}/hu_spend_cashflow.csv")

ap = argparse.ArgumentParser()
for k, d in [("eq", None), ("bond", None), ("cash", None), ("alt", None), ("z", None)]:
    ap.add_argument(f"--{k}", type=float, default=d)
ap.add_argument("--lump-year", type=int, default=3); ap.add_argument("--staff", type=int, default=1)
a = ap.parse_args()

W0 = f("endow_bn_krw"); SPEND0 = f("current_spend_bn"); LUMP = f("lump_bn"); INF = f("infl_pct") / 100
CALL_SHARE, CALL_Y = f("unfunded_share"), int(f("call_years")); LOCK = f("lockup_years"); H = 30
OPTS = [("A 보수형", 65, 30, 5, 0, 4.0, 3, 1), ("B 균형형", 50, 25, 5, 20, 4.5, 3, 1), ("C Yale 추종형", 55, 10, 5, 30, 5.25, 8, 3)]
if a.eq is not None:
    OPTS = [("사용자 안", a.eq, a.bond, a.cash, a.alt, a.z, a.lump_year, a.staff)]

# 연 수익률 블록(40년 모의 수익률 패널(교육용), 연 단위로 묶음)
nb = len(panel) // 12
ann = lambda s: (1 + s.values[: nb * 12].reshape(nb, 12)).prod(1) - 1
A_eq, A_bd, A_cs, A_pe, A_pi = ann(panel.eq_ret), ann(panel.bond_gov_ret), ann(panel.rf), ann(panel.alt_pe_ret), ann(panel.cpi)
rng = np.random.default_rng(int(f("panel_seed")) + 1); idx = rng.integers(0, nb, size=(4000, H))

def survival(we, wb, wc, x, shock, lump_year):
    s = sc.loc[shock]
    liq = W0 * (we / 100 * (1 + s.eq_ret_pct / 100) + wb / 100 * (1 + s.bond_gov_ret_pct / 100) + wc / 100 * (1 + s.cash_ret_pct / 100))
    calls = CALL_SHARE * x / 100 * W0 / CALL_Y; years = 0
    for t in range(1, H + 1):
        out = SPEND0 + (LUMP if t == lump_year else 0) + (calls if t <= CALL_Y else 0)
        liq = liq * (1 + INF) - out
        if liq <= 0: break
        years = t
    return years, calls

def mc(we, wb, wc, x, z, lump_year, shock):
    w = np.array([we, wb, wc, x]) / 100
    R = np.stack([A_eq[idx], A_bd[idx], A_cs[idx], A_pe[idx]], -1); PI = A_pi[idx].copy()
    if shock:
        s = sc.loc["2022형"]; R[:, 0, :] = np.array([s.eq_ret_pct, s.bond_gov_ret_pct, s.cash_ret_pct, s.alt_pe_true_ret_pct]) / 100; PI[:, 0] = INF
    W = np.full(4000, W0); S = np.full(4000, SPEND0); defl = np.ones(4000)
    for t in range(H):
        S = f("smooth_w") * S * (1 + PI[:, t]) + (1 - f("smooth_w")) * z / 100 * W
        W = W * (1 + (R[:, t, :] * w).sum(1)) - S - (LUMP if t + 1 == lump_year else 0.0)
        defl *= (1 + PI[:, t])
    Wr = W / defl
    return float((Wr >= W0).mean()), float(np.median(Wr))

print("=== H대학교 발전기금 5,000억 — 안별 판정 (기준: ① ≥ 10년 · ② ≥ 50% · ③ 역량 · ④ 3년 지출+공사비) ===")
mu = {k: float(cma.mu_pct[k]) for k in cma.index}
print(f"기대수익(교육용) — 주식 {mu['eq']:.1f} · 국채 {mu['bond_gov']:.1f} · 현금 {mu['cash']:.1f} · 사모투자(재간접) {mu['alt_pe']:.1f} · 사모투자(직접) {mu['alt_pe_direct']:.1f}% · 물가 {f('infl_pct'):.1f}%")
for name, we, wb, wc, x, z, ly, staff in OPTS:
    assert abs(we + wb + wc + x - 100) < 1e-6, "비중 합계는 100이어야 한다"
    direct = staff >= f("staff_min") and x / 100 * W0 >= f("mgr_min") * f("min_commit_bn")
    mu_n = (we * mu["eq"] + wb * mu["bond_gov"] + wc * mu["cash"] + x * (mu["alt_pe_direct"] if direct else mu["alt_pe"])) / 100
    z_max = mu_n - f("infl_pct") - f("spend_margin_pp")
    s22, calls = survival(we, wb, wc, x, "2022형", ly); s08, _ = survival(we, wb, wc, x, "2008형", ly)
    pk, med = mc(we, wb, wc, x, z, ly, False); pks, _ = mc(we, wb, wc, x, z, ly, True)
    safe_after = W0 * (wb / 100 * (1 + sc.loc["2022형"].bond_gov_ret_pct / 100) + wc / 100 * (1 + sc.loc["2022형"].cash_ret_pct / 100))
    need3 = float(cfl.fixed_spend_bn_krw[:3].sum()) + LUMP
    print(f"\n◆ {name}: 주식 {we:.0f} · 국채 {wb:.0f} · 현금 {wc:.0f} · 사모투자 {x:.0f}% | 현금성 자산(국채+현금) {wb+wc:.0f}% | 지출률 {z}% | 공사비 {ly}년차 | 전담 인력 {staff}명")
    print(f"  [1] 명목 기대수익 {mu_n:.2f}% · 실질 {mu_n-f('infl_pct'):.2f}% → 지출률 상한 {z_max:.2f}% ({'지출률 ' + str(z) + '% 이내' if z <= z_max else '지출률 ' + str(z) + '% 초과'})")
    print(f"  [2] ① 버틸 수 있는 기간 — 2022형 {s22}년 · 2008형 {s08}년 (출자 요청 연 {calls:.0f}억 × {CALL_Y}년) → {'통과' if min(s22, s08) >= LOCK else '탈락'}")
    print(f"  [3] ② 30년 실질가치 유지 확률 — 평시 {pk:.0%} · 첫해 2022형 충격 {pks:.0%} (실질 기금 중앙값 {med:,.0f}억) → {'통과' if pk >= f('real_keep_min') else '탈락'}")
    print(f"  [4] ③ 운용 역량 — 사모투자 {x/100*W0:,.0f}억 · 전담 {staff}명 → {'직접 투자 가능' if direct else ('재간접펀드 · 세컨더리만 가능' if x > 0 else '해당 없음')}")
    print(f"  [5] ④ 충격 직후 현금 · 국채 {safe_after:,.0f}억 vs 3년 지출 {need3-LUMP:,.0f}억 + 공사비 {LUMP:,.0f}억 = {need3:,.0f}억 → {'통과' if safe_after >= need3 else '탈락'}")
