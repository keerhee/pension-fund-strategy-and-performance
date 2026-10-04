#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""국민연금 LDI 계산 도구 — W06 팀 과제 1·2팀용

사용법
  python3 nps_ldi_tool.py                         # 오늘(기준 곡선) 상태와 세 안 비교
  python3 nps_ldi_tool.py --shift -150 --kofr -125  # 국고채 곡선 1.5%p 하락 · KOFR 1.25%p 하락 상태에서
  python3 nps_ldi_tool.py --shift 150 --kofr 125 --team 2   # 2팀 세 안
  python3 nps_ldi_tool.py --bond 200 --irs 100    # 임의의 안 (30년 국채 매입액 · 금리스왑 계약금액, 조 원)

출력
  [1] 부채 — 부채 현재가치, 적립비율(국채 기준 · 자체 5.5% 기준), 부채 듀레이션, 부채 DV01
  [2] 자산 — 원화 금리 DV01, 헤지 비율 출발점
  [3] 안별 판정 — 헤지 비율, 기대수익, 시장 한도, 증거금 · 비상 담보, 판정 기준 ①~⑤
  [4] 실행 후 금리 이동 — 안을 실행한 뒤 곡선이 −150 · −100 · +100 · +150bp 움직이면 적립비율과 스왑 손익

모든 숫자는 교육용 단순화다: 보험료 · 급여 흐름은 금리와 무관하게 고정, 곡선은 평행 이동.
"""
import argparse, json, os
import numpy as np, pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--shift", type=float, default=0.0, help="국고채 곡선 평행 이동(bp). 예: -150")
ap.add_argument("--kofr", type=float, default=None, help="단기금리(KOFR) 이동(bp). 기본값 = shift")
ap.add_argument("--team", type=int, default=1, help="1 또는 2 — 비교할 세 안")
ap.add_argument("--bond", type=float, default=None, help="임의 안: 30년 국채 매입액(조)")
ap.add_argument("--irs", type=float, default=0.0, help="임의 안: 금리스왑(고정 수취) 계약금액(조)")
ap.add_argument("--json", default=None, help="결과를 저장할 json 파일명")
a = ap.parse_args()
SHIFT = a.shift; KS = a.shift if a.kofr is None else a.kofr

P = pd.read_csv(f"{D}/nps_params.csv").set_index("key").value
f = lambda k: float(P[k])
cf = pd.read_csv(f"{D}/nps_cashflow.csv")
curve = pd.read_csv(f"{D}/nps_curve.csv")
assets = pd.read_csv(f"{D}/nps_assets.csv").set_index("asset")
mkt = pd.read_csv(f"{D}/nps_market.csv").set_index("key").value

F0 = f("fund_2025_trn"); HURDLE = f("hurdle_pct"); END = int(f("liab_end_year"))
A_TOT = assets.amount_trn_krw.sum(); KOFR = f("kofr_pct") + KS / 100
mats, ylds = curve.maturity_y.values.astype(float), curve.yield_pct.values + SHIFT / 100

def z(t, s=0.0): return float(np.interp(t, mats, ylds)) + s / 100
def pv(flows, years, rate=None, s=0.0):
    t = np.array(years) - 2025
    r = np.array([rate if rate is not None else z(tt, s) for tt in t])
    return float(np.sum(flows / (1 + r / 100) ** t))

w = cf[cf.year <= END]; net, yrs = w.net_outflow_trn_krw.values, w.year.values
L_h = pv(net, yrs, rate=HURDLE); L_g = pv(net, yrs)
D_L = -(pv(net, yrs, s=10) - pv(net, yrs, s=-10)) / (2 * L_g * 0.001)
DV01_L = D_L * L_g * 1e-4
FR_h, FR_g = F0 / L_h, F0 / L_g

def par_md(T, y):
    c = y / 100; t = np.arange(1, T + 1); v = c / (1 + c) ** t; v[-1] += 1 / (1 + c) ** T
    return float(np.sum(t * v) / (1 + c))
def par_px(T, c, y):
    t = np.arange(1, T + 1); return float(np.sum(c / (1 + y / 100) ** t) + 100 / (1 + y / 100) ** T) / 100
y30 = z(30); s30 = y30 + f("swap_spread_30y_pp")
D_B, D_S = par_md(30, y30), par_md(30, s30)
dB, dS = D_B * 1e-4, D_S * 1e-4                      # 1조당 DV01 (조/bp)

assets["dv01"] = assets.amount_trn_krw * assets.mod_duration_y * assets.krw_rate_exposure * 1e-4
DV01_A = float(assets.dv01.sum())
tw = assets.target_pct_2027.fillna(0.0); tw["cash"] = max(0.0, 100 - tw.sum())
mu_saa = float((tw * assets.mu_pct).sum() / 100)
BD = f("target_bond_dom_2027_pct") / 100 * A_TOT; D_BD = float(assets.mod_duration_y["bond_dom"])
liquid = float(assets.amount_trn_krw["cash"] + assets.gov_bond_trn_krw["bond_dom"])
long_issue = float(mkt["ktb_issue_long_2025_trn"]); irs_turn = float(mkt["irs_turnover_2025_trn"])
cap_bond = f("cap_issue_share") * f("program_years") * long_issue
cap_irs = f("cap_irs_turnover_share") * irs_turn
DV01_SAA = BD * D_BD * 1e-4

def dv01_hedge(bond, irs): return (BD - bond) * D_BD * 1e-4 + bond * dB + irs * dS
def mu_of(bond, irs):
    inside = min(bond, BD); beyond = max(0.0, bond - BD)
    return mu_saa + inside / A_TOT * (y30 - float(assets.mu_pct["bond_dom"])) + beyond / A_TOT * (y30 - 8.0) + irs / A_TOT * (s30 - KOFR)
def fr_after_move(bond, irs, move):
    """안을 실행한 뒤 곡선이 move(bp) 더 움직이면 — 국채 기준 적립비율 · 스왑 손익(풀 재평가)"""
    base_bd = (BD - bond) * (-D_BD * move * 1e-4)
    b30 = bond * (par_px(30, y30, y30 + move / 100) - 1)
    sw = irs * (par_px(30, s30, s30 + move / 100) - 1)
    A1 = F0 + (base_bd + b30 + sw) * (F0 / A_TOT)
    return A1 / pv(net, yrs, s=move), sw

def judge(name, bond, irs, lbp):
    dv = dv01_hedge(bond, irs); h = dv / DV01_L
    fr_dn, _ = fr_after_move(bond, irs, -100); dfr = (fr_dn - FR_g) * 100
    vm3 = irs * dS * f("shock_bp_3d"); buf = irs * dS * f("buffer_bp"); mu = mu_of(bond, irs)
    gap_real = dfr <= f("dfr_material_pp")
    c = {"①": (lbp == 1) if gap_real else True,
         "②": bond <= cap_bond + 0.5 and irs <= cap_irs + 0.5,
         "③": max(vm3, buf) <= liquid,
         "④": mu >= HURDLE,
         "⑤": irs == 0}
    moves = {m: fr_after_move(bond, irs, m) for m in (-150, -100, 100, 150)}
    return {"안": name, "30년국채_조": round(bond), "스왑_조": round(irs), "부채지표(LBP)": "도입" if lbp else "없음",
            "헤지비율_%": round(h * 100, 1), "기대수익_%": round(mu, 2), "-100bp시_적립비율변화_%p": round(dfr, 1),
            "국채매입÷한도": round(bond / cap_bond, 2), "스왑÷한도": round(irs / cap_irs, 2),
            "3일+200bp_증거금_조": round(vm3), "250bp_비상담보_조": round(buf), "담보가능자산_조": round(liquid, 1),
            "판정": {k: ("통과" if v else "탈락") for k, v in c.items()},
            "실행후_금리이동": {f"{m:+d}bp": {"적립비율_%": round(v[0] * 100, 1), "스왑손익_조": round(v[1]), "스왑손실÷담보": round(-v[1] / liquid, 2) if v[1] < 0 else 0.0} for m, v in moves.items()}}

# ── 안 정의 ──────────────────────────────────────────────────────────────────
irs30 = max(0.0, (0.30 * DV01_L - DV01_SAA) / dS)          # 스왑만으로 헤지 비율 30%
OPTIONS = {1: [("A 현행 유지", 0, 0, 0), ("B 30년 국채 5년 분할", cap_bond, 0, 1), ("C 금리스왑 헤지 30%", 0, irs30, 1)],
           2: [("A 현행 유지", 0, 0, 0), ("B 30년 국채 5년 분할", cap_bond, 0, 1), ("C 국채 + 금리스왑(한도 내)", cap_bond, cap_irs, 1)]}
opts = [("사용자 안", a.bond, a.irs, 1)] if a.bond is not None else OPTIONS[a.team]

print(f"=== 국민연금 LDI 계산 — 곡선 {SHIFT:+.0f}bp · KOFR {KOFR:.2f}% ===")
print(f"[1] 국고채 3년 {z(3):.2f} · 10년 {z(10):.2f} · 30년 {y30:.2f}%")
print(f"    부채(2026~{END} 순지급의 현재가치) — 국채 기준 {L_g:,.0f}조 · 자체 5.5% 기준 {L_h:,.0f}조")
print(f"    적립비율 = 적립금 {F0:,.0f}조 ÷ 부채 → 국채 기준 {FR_g*100:.1f}% · 자체 기준 {FR_h*100:.1f}%")
print(f"    부채 듀레이션 {D_L:.1f}년 · 부채 DV01 {DV01_L:.2f}조/bp (금리 1bp 하락 시 부채 증가액)")
print(f"[2] 자산 원화 DV01 오늘 {DV01_A:.3f}조/bp (헤지 비율 {DV01_A/DV01_L*100:.1f}%) · 2027 목표 비중 이행 후 {DV01_SAA:.3f}조/bp (헤지 비율 {DV01_SAA/DV01_L*100:.1f}%)")
print(f"    30년 국채 듀레이션 {D_B:.1f}년(100조 매입 = {100*dB:.3f}조/bp) · 30년 스왑 {D_S:.1f}년 · 스왑 고정금리 {s30:.2f}% vs KOFR {KOFR:.2f}%")
print(f"    시장 한도 — 국채 {cap_bond:.0f}조(장기물 연 발행 {long_issue}조 × 30% × 5년) · 스왑 {cap_irs:.0f}조(연 거래 {irs_turn:,.0f}조 × 5%) · 담보 가능 자산 {liquid:.1f}조 · 기대수익 출발점 {mu_saa:.2f}%")
out = []
print("[3] 안별 판정")
for name, b, i, l in opts:
    r = judge(name, b, i, l); out.append(r)
    print(f"  ◆ {name}: 국채 {r['30년국채_조']}조 · 스왑 {r['스왑_조']:,}조 · 부채지표 {r['부채지표(LBP)']}")
    print(f"    헤지 비율 {r['헤지비율_%']}% · 기대수익 {r['기대수익_%']}% · 금리 −1%p 시 적립비율 {r['-100bp시_적립비율변화_%p']:+.1f}%p")
    print(f"    국채÷한도 {r['국채매입÷한도']} · 스왑÷한도 {r['스왑÷한도']} · 3일 급등 증거금 {r['3일+200bp_증거금_조']}조 · 비상 담보 {r['250bp_비상담보_조']}조 (담보 가능 {liquid:.0f}조)")
    print("    판정 " + " · ".join(f"{k} {v}" for k, v in r["판정"].items()))
print("[4] 안을 오늘 실행한 뒤 곡선이 더 움직이면 — 국채 기준 적립비율(%) / 스왑 손익(조)")
for r in out:
    print(f"  {r['안']:<22}" + " | ".join(f"{k}: {v['적립비율_%']}% / {v['스왑손익_조']:+,}" + (f" (담보의 {v['스왑손실÷담보']}배)" if v['스왑손실÷담보'] else "") for k, v in r["실행후_금리이동"].items()))
if a.json:
    json.dump({"shift_bp": SHIFT, "L_gov": round(L_g), "L_self": round(L_h), "FR_gov": round(FR_g, 4), "FR_self": round(FR_h, 4), "D_L": round(D_L, 1),
               "DV01_L": round(DV01_L, 3), "y30": round(y30, 2), "options": out}, open(a.json, "w"), ensure_ascii=False, indent=1)
