#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W7 M8 IC 케이스 — 판정 조건 계산 (w7m8_build.py 의 CSV → w7m8_results.json · compute_log.txt)

제1호 (기금운용위) 국민연금 기금의 LDI — 부채 벤치마크 도입 + 헤지 비율 목표·수단 (안 A·B·C)
  조건 ① 갭의 실재      국채 곡선 기준 적립비율 FR_g = F / PV_g(2026~2071 순유출) 와 자체 기준(5.5%) FR_h 를 층위로 구분하고,
                        금리 −100bp 시 ΔFR_g ≤ −5%p 이면 '헤지 대상 갭이 실재' → 부채 지표 없는 안은 탈락
  조건 ② 시장 수용      현물: 매입액 ≤ 프로그램 기간 장기물(20·30·50년) 신규 발행의 30%  /  IRS: 명목 ≤ 연간 원화 IRS 거래규모의 5%
  조건 ③ 유동성 버퍼    레버리지 헤지의 250bp 버퍼(TPR 2023.4) 와 3영업일 +200bp 변동증거금 ≤ 담보 적격 유동자산(단기자금 + 국고채)
  조건 ④ 허들           헤지 후 기대수익 μ ≥ 5.5% (연금개혁 전제 기금수익률)
  조건 ⑤ 거버넌스       국내채권 비중 ≤ 2027 목표 21.8% + SAA 허용범위 7.0%p (지침 별표 1) · IRS 오버레이는 지침에 파생 조항이 없어 개정 필요
"""
import json, os
import numpy as np, pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
P = pd.read_csv(f"{D}/fml_w7m8_params.csv").set_index("key").value
f = lambda k: float(P[k])
cf = pd.read_csv(f"{D}/fml_w7m8_cashflow.csv")
curve = pd.read_csv(f"{D}/fml_w7m8_curve.csv")
assets = pd.read_csv(f"{D}/fml_w7m8_assets.csv").set_index("asset")
mkt = pd.read_csv(f"{D}/fml_w7m8_market.csv").set_index("key").value
opts = pd.read_csv(f"{D}/fml_w7m8_options.csv")
log = []
def L(s): log.append(s); print(s)

F0 = f("fund_2025_trn"); HURDLE = f("hurdle_pct"); END = int(f("liab_end_year"))
A_TOT = assets.amount_trn_krw.sum()

# ── 곡선 · 할인 ─────────────────────────────────────────────────────────────
mats, ylds = curve.maturity_y.values.astype(float), curve.yield_pct.values
def z(t, shift_bp=0.0):
    """만기 t년의 (교육용) 제로금리 % — 공시 4점 + 보간점을 선형 보간, 50년 이후 평탄"""
    return float(np.interp(t, mats, ylds)) + shift_bp / 100
def pv_flows(flows, years, rate=None, shift_bp=0.0):
    """연말 현금흐름의 2025년 말 기준 현재가치. rate 가 있으면 평탄 할인, 없으면 곡선."""
    t = np.array(years) - 2025
    r = np.array([rate if rate is not None else z(tt, shift_bp) for tt in t])
    return float(np.sum(flows / (1 + r / 100) ** t))

w = cf[cf.year <= END]
net, ben, con, yrs = w.net_outflow_trn_krw.values, w.benefit_trn_krw.values, w.contrib_trn_krw.values, w.year.values
L_h = pv_flows(net, yrs, rate=HURDLE)
L_g = pv_flows(net, yrs)
L_g_dn = pv_flows(net, yrs, shift_bp=-100); L_g_up = pv_flows(net, yrs, shift_bp=100)
PVben_g, PVcon_g = pv_flows(ben, yrs), pv_flows(con, yrs)
D_L = -(pv_flows(net, yrs, shift_bp=10) - pv_flows(net, yrs, shift_bp=-10)) / (2 * L_g * 0.001)   # 수정 듀레이션(년)
D_ben = -(pv_flows(ben, yrs, shift_bp=10) - pv_flows(ben, yrs, shift_bp=-10)) / (2 * PVben_g * 0.001)
DV01_L = D_L * L_g * 1e-4            # 조원/bp
FR_h, FR_g = F0 / L_h, F0 / L_g
FR_g_dn, FR_g_up = F0 / L_g_dn, F0 / L_g_up

L("=== 제1호 — 국민연금 기금의 LDI: 부채 벤치마크와 헤지 비율 ===")
L(f"[부채] 창 2026~{END} 순유출(급여−보험료) PV — 자체 기준 {HURDLE}% : {L_h:,.0f}조 · 국채 곡선(3y {z(3):.2f} · 10y {z(10):.2f} · 30y {z(30):.2f}%) : {L_g:,.0f}조")
L(f"       (급여 PV {PVben_g:,.0f}조 − 보험료 PV {PVcon_g:,.0f}조 = {L_g:,.0f}조 · 수정 듀레이션 D_L = {D_L:.1f}년 · 급여만의 D = {D_ben:.1f}년 · DV01_L = {DV01_L:.2f}조/bp)")
L(f"[조건 ①] 적립비율 — 자체 기준 FR_h = {FR_h*100:.0f}% · 국채 기준 FR_g = {FR_g*100:.0f}% (참고: 2026.6 자산 {f('fund_2026h1_trn'):,.1f}조면 FR_g {f('fund_2026h1_trn')/L_g*100:.0f}%)")

# ── 자산 측 원화 금리 민감도 ────────────────────────────────────────────────
assets["dv01_trn"] = assets.amount_trn_krw * assets.mod_duration_y * assets.krw_rate_exposure * 1e-4
DV01_A = float(assets.dv01_trn.sum())
D_A_krw = DV01_A / (A_TOT * 1e-4)                    # 총자산 대비 원화 금리 듀레이션(년)
D_A_all = float((assets.amount_trn_krw * assets.mod_duration_y).sum() / A_TOT)   # 외화 채권까지 세면
h0 = DV01_A / DV01_L
gap0 = D_A_krw - D_L
def fr_after(dv01_hedge_extra, shift_bp):
    """평행 이동 shift_bp 후 국채 기준 적립비율 — 자산은 DV01(기존+헤지)로, 부채는 곡선 재할인으로"""
    A1 = F0 - (DV01_A + dv01_hedge_extra) * shift_bp * (F0 / A_TOT)      # 2026.6 DV01 을 2025 말 F 규모로 환산
    return A1 / pv_flows(net, yrs, shift_bp=shift_bp)
dFR_A = (fr_after(0, -100) - FR_g) * 100
L(f"[조건 ①] 자산 원화 DV01 = {DV01_A:.3f}조/bp (국내채권 {assets.amount_trn_krw['bond_dom']:.1f}조 × D {assets.mod_duration_y['bond_dom']}) → 원화 금리 듀레이션 D_A = {D_A_krw:.2f}년 (외화 채권까지 세면 {D_A_all:.2f}년)")
L(f"[조건 ①] 듀레이션 갭 = D_A − D_L = {gap0:.1f}년 · 현행 헤지 비율 h0 = DV01_A / DV01_L = {h0*100:.1f}%")
L(f"[조건 ①] 금리 −100bp → 부채 {L_g_dn:,.0f}조(+{(L_g_dn/L_g-1)*100:.0f}%) · FR_g {FR_g*100:.0f}% → {fr_after(0,-100)*100:.0f}% (ΔFR {dFR_A:+.1f}%p, 임계 {f('dfr_material_pp'):+.0f}%p → {'갭 실재' if dFR_A <= f('dfr_material_pp') else '갭 비실재'})")
cond1_gap_exists = bool(dFR_A <= f("dfr_material_pp"))

# 소진 연도 — 수익률 1%p 의 값 (재정추계와 같은 방식: 고정 수익률로 기금 경로)
def deplete(rate):
    F = F0
    for _, r in cf.iterrows():
        F = F * (1 + rate / 100) + r.contrib_trn_krw - r.benefit_trn_krw
        if F <= 0: return int(r.year)
    return None
dep55, dep45 = deplete(5.5), deplete(4.5)
L(f"[조건 ①] 소진 연도(교육용 추계) — 5.5%: {dep55} · 4.5%: {dep45} (공식 2071 · 2064) → 수익률 1%p = 소진 {dep55-dep45}년")

# ── 헤지 수단의 DV01 ───────────────────────────────────────────────────────
def par_mod_duration(T, y):
    """만기 T년, 연 이표 = 수익률 y% 인 액면가 채권의 수정 듀레이션"""
    c = y / 100; t = np.arange(1, T + 1); pv = c / (1 + c) ** t; pv[-1] += 1 / (1 + c) ** T
    return float(np.sum(t * pv) / (1 + c))
T = int(f("hedge_tenor_y")); y30 = z(T)
D_bond30 = par_mod_duration(T, y30); D_irs30 = par_mod_duration(T, y30 + f("swap_spread_30y_pp"))
dv01_per_trn_bond, dv01_per_trn_irs = D_bond30 * 1e-4, D_irs30 * 1e-4
L(f"[수단] 30년 국고채(수익률 {y30:.2f}%) 수정 듀레이션 {D_bond30:.1f}년 → 1조당 DV01 {dv01_per_trn_bond*1e4:.4f}조/bp… 즉 매입 100조 = {100*dv01_per_trn_bond:.3f}조/bp · IRS 30년(고정 {y30+f('swap_spread_30y_pp'):.2f}%) {D_irs30:.1f}년")

# ── 시장 수용 · 유동자산 ────────────────────────────────────────────────────
long_issue = float(mkt["ktb_issue_long_2025_trn"]); irs_turn = float(mkt["irs_turnover_2025_trn"])
cap_bond_trn = f("cap_issue_share") * f("program_years") * long_issue
cap_irs_trn = f("cap_irs_turnover_share") * irs_turn
liquid = float(assets.amount_trn_krw["cash"] + assets.gov_bond_trn_krw["bond_dom"])
long_out = float(mkt["ktb_30y_out_2025_trn_est"] + mkt["ktb_50y_out_2025_trn_est"])
L(f"[조건 ②] 장기물(20·30·50년) 연 발행 {long_issue:.1f}조 → {f('program_years'):.0f}년 × {f('cap_issue_share'):.0%} = 현물 매입 상한 {cap_bond_trn:.0f}조 · IRS 명목 상한 = 연 거래 {irs_turn:,.0f}조 × {f('cap_irs_turnover_share'):.0%} = {cap_irs_trn:.0f}조")
L(f"[조건 ②] 초장기(30·50년) 잔액 추정 {long_out:.0f}조 · 국고채 잔액 {float(mkt['ktb_outstanding_trn']):,.1f}조 vs 부채 {L_g:,.0f}조 (부채 ÷ 국고채 잔액 = {L_g/float(mkt['ktb_outstanding_trn']):.2f}배)")
L(f"[조건 ③] 담보 적격 유동자산 = 단기자금 {assets.amount_trn_krw['cash']:.1f} + 국고채 보유 {assets.gov_bond_trn_krw['bond_dom']:.1f} = {liquid:.1f}조")

# ── 기대수익 ────────────────────────────────────────────────────────────────
mu0 = float((assets.amount_trn_krw * assets.mu_pct).sum() / A_TOT)
tw = assets.target_pct_2027.fillna(0.0); tw["cash"] = max(0.0, 100 - tw.sum())            # 2027 목표 비중(단기자금은 잔여)
mu_saa = float((tw * assets.mu_pct).sum() / 100)
BD_TARGET_AMT = f("target_bond_dom_2027_pct") / 100 * A_TOT                                 # 목표 국내채권 금액(조) — 안 A·B 의 공통 출발점
D_BD = float(assets.mod_duration_y["bond_dom"])
def dv01_assets(bond30_trn):
    """SAA 목표 국내채권(D 5.5) 중 bond30_trn 을 30년물(D 16.1)로 배정했을 때의 원화 DV01"""
    return (BD_TARGET_AMT - bond30_trn) * D_BD * 1e-4 + bond30_trn * dv01_per_trn_bond
def mu_after_bond(buy_trn):
    """SAA 목표 국내채권 안에서는 30년물이 벤치마크 채권(4.2)을 대체(+0.4%p), 목표를 넘는 분은 위험자산(8.0)에서 뺀다"""
    inside = min(buy_trn, BD_TARGET_AMT); beyond = max(0.0, buy_trn - BD_TARGET_AMT)
    return mu_saa + inside / A_TOT * (y30 - float(assets.mu_pct["bond_dom"])) + beyond / A_TOT * (y30 - 8.0)
def mu_after_irs(notional_trn):
    """IRS 오버레이 캐리 = (고정 수취 − 변동 지급) × 명목 / 자산"""
    return mu_saa + notional_trn / A_TOT * ((y30 + f("swap_spread_30y_pp")) - f("kofr_pct"))
DV01_A_SAA = dv01_assets(0.0); h_saa = DV01_A_SAA / DV01_L
L(f"[조건 ④] 기대수익 — 2026.6 현행 구성 μ {mu0:.2f}% · 2027 SAA 목표 구성(국내채권 21.8%) μ_SAA = {mu_saa:.2f}% (위험자산 8.0 · 국내채권 4.2 · 해외채권 4.5, 교육용) · 허들 {HURDLE}%")
L(f"[출발점] SAA 목표 이행 후 국내채권 {BD_TARGET_AMT:.0f}조 × D {D_BD} → DV01 {DV01_A_SAA:.3f}조/bp · 헤지 비율 {h_saa*100:.1f}% (오늘 보유 기준 {h0*100:.1f}%) — 안 A·B 는 여기서 출발한다")

# ── 안 A·B·C 판정 ───────────────────────────────────────────────────────────
tgt_bond_dom = f("target_bond_dom_2027_pct"); rng = f("saa_range_bond_dom_pp")
def judge(option, buy_trn=0.0, irs_trn=0.0, lbp=1):
    dv01_total = dv01_assets(buy_trn) + irs_trn * dv01_per_trn_irs
    dv01_extra = dv01_total - DV01_A
    h = dv01_total / DV01_L
    gap = dv01_total / (A_TOT * 1e-4) - D_L
    fr_dn = fr_after(dv01_extra, -100); dfr = (fr_dn - FR_g) * 100
    vm_3d = irs_trn * dv01_per_trn_irs * f("shock_bp_3d")        # 3일 +200bp 변동증거금(조)
    buffer_req = irs_trn * dv01_per_trn_irs * f("buffer_bp")     # 250bp 버퍼(조)
    mu = mu_after_bond(buy_trn) if buy_trn else mu_after_irs(irs_trn) if irs_trn else mu_saa
    bond_dom_pct = max(BD_TARGET_AMT, buy_trn) / A_TOT * 100 if buy_trn <= BD_TARGET_AMT else (buy_trn) / A_TOT * 100
    c1 = bool(lbp == 1) if cond1_gap_exists else True              # 갭이 실재하면 부채 지표(LBP) 없는 안은 탈락
    c2 = bool(buy_trn <= cap_bond_trn + 1e-9 and irs_trn <= cap_irs_trn + 1e-9)
    c3 = bool(buffer_req <= liquid and vm_3d <= liquid)
    c4 = bool(mu >= HURDLE)
    c5_range = bool(bond_dom_pct <= tgt_bond_dom + rng + 1e-9)
    c5 = bool(c5_range and irs_trn == 0)                            # IRS 는 지침에 파생 조항이 없어 개정 전에는 불가
    return {"option": option, "buy_bond_trn": round(buy_trn, 1), "irs_notional_trn": round(irs_trn, 1), "dv01_extra_trn": round(dv01_extra, 3),
            "hedge_ratio": round(h, 4), "gap_years": round(gap, 1), "fr_g_down100": round(fr_dn, 3), "dfr_down100_pp": round(dfr, 1),
            "vm_3d_trn": round(vm_3d, 1), "buffer_req_trn": round(buffer_req, 1), "liquid_trn": round(liquid, 1),
            "mu_after_pct": round(mu, 2), "bond_dom_pct_after": round(bond_dom_pct, 1),
            "buy_vs_cap": round(buy_trn / cap_bond_trn, 2) if buy_trn else 0.0, "irs_vs_cap": round(irs_trn / cap_irs_trn, 2) if irs_trn else 0.0,
            "buy_vs_long_out": round(buy_trn / long_out, 2) if buy_trn else 0.0,
            "cond1_ok": c1, "cond2_ok": c2, "cond3_ok": c3, "cond4_ok": c4, "cond5_ok": c5, "cond5_range_ok": c5_range, "lbp": lbp}

buy_B = cap_bond_trn                                                     # 안 B — 시장 상한까지 현물
irs_C = max(0.0, (f("hedge_target_C") * DV01_L - DV01_A_SAA) / dv01_per_trn_irs)   # 안 C — SAA 출발점에서 30% 를 IRS 로
res_opts = [judge("A", 0, 0, lbp=0), judge("B", buy_B, 0, lbp=1), judge("C", 0, irs_C, lbp=1)]
ok = lambda b: "통과" if b else "탈락"
for r in res_opts:
    L(f"[안 {r['option']}] 30년물 배정 {r['buy_bond_trn']:.0f}조 · IRS 명목 {r['irs_notional_trn']:,.0f}조 → 헤지 비율 {r['hedge_ratio']*100:.1f}% · 갭 {r['gap_years']:.1f}년 · −100bp 시 FR_g {r['fr_g_down100']*100:.0f}% (Δ {r['dfr_down100_pp']:+.1f}%p)")
    L(f"       매입/상한 {r['buy_vs_cap']:.2f} · IRS/상한 {r['irs_vs_cap']:.2f} · 3일 +{f('shock_bp_3d'):.0f}bp 증거금 {r['vm_3d_trn']:.0f}조 · 250bp 버퍼 {r['buffer_req_trn']:.0f}조 vs 유동자산 {liquid:.0f}조 · μ {r['mu_after_pct']:.2f}% · 국내채권 {r['bond_dom_pct_after']:.1f}%")
    L(f"       조건① {ok(r['cond1_ok'])} · ② {ok(r['cond2_ok'])} · ③ {ok(r['cond3_ok'])} · ④ {ok(r['cond4_ok'])} · ⑤ {ok(r['cond5_ok'])}{'' if r['cond5_range_ok'] else '(허용범위 초과)'}{' (IRS — 지침 파생 조항 없음)' if r['irs_notional_trn'] > 0 else ''}")

# ── 헤지 비율 격자 — 현물로 / IRS 로 각각 얼마가 드는가 ─────────────────────────
grid = []
for ht in [0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 1.00]:
    need = max(0.0, ht * DV01_L - DV01_A_SAA)
    bond = need / (dv01_per_trn_bond - D_BD * 1e-4); irs = need / dv01_per_trn_irs   # 현물은 D 5.5 채권을 D 16.1 로 바꾸는 순증분
    grid.append({"hedge_ratio": ht, "dv01_need_trn": round(need, 3), "bond_buy_trn": round(bond), "bond_vs_cap": round(bond / cap_bond_trn, 1), "bond_vs_long_out": round(bond / long_out, 2),
                 "bond_years_of_long_issue": round(bond / long_issue, 1), "irs_notional_trn": round(irs), "irs_vs_turnover": round(irs / irs_turn, 3),
                 "vm_3d_trn": round(irs * dv01_per_trn_irs * f("shock_bp_3d")), "buffer_trn": round(irs * dv01_per_trn_irs * f("buffer_bp")),
                 "mu_bond_pct": round(mu_after_bond(bond), 2), "mu_irs_pct": round(mu_after_irs(irs), 2), "gap_years": round(ht * D_L - D_L + 0, 1)})
L("[격자] 헤지 비율 → 현물 30년 국고채 매입액(조) / 장기물 연 발행 대비 년수 / IRS 명목(조) / 3일 증거금(조) / 250bp 버퍼(조)")
for g in grid:
    L(f"       {g['hedge_ratio']*100:>4.0f}% : 현물 {g['bond_buy_trn']:>6,.0f}조 = 장기물 발행 {g['bond_years_of_long_issue']:>5.1f}년치 · 초장기 잔액의 {g['bond_vs_long_out']*100:>5.0f}% | IRS {g['irs_notional_trn']:>6,.0f}조 = 연 거래의 {g['irs_vs_turnover']*100:>4.0f}% · 증거금 {g['vm_3d_trn']:>4,.0f}조 · 버퍼 {g['buffer_trn']:>4,.0f}조 | μ 현물 {g['mu_bond_pct']:.2f} · IRS {g['mu_irs_pct']:.2f}%")

# ── 민감도 — 조건 ② 임계 · 프로그램 기간이 바뀌면 안 B 의 헤지 비율은 ───────────
sens = []
for share in [0.2, 0.3, 0.5]:
    for yrs_ in [5, 10]:
        buy = share * yrs_ * long_issue
        sens.append({"cap_issue_share": share, "program_years": yrs_, "buy_trn": round(buy), "hedge_ratio": round(dv01_assets(buy) / DV01_L, 3),
                     "gap_years": round(dv01_assets(buy) / (A_TOT * 1e-4) - D_L, 1), "mu_pct": round(mu_after_bond(buy), 2),
                     "bond_dom_pct": round(max(BD_TARGET_AMT, buy) / A_TOT * 100, 1)})
L("[민감도 B] " + " · ".join(f"발행 {s['cap_issue_share']:.0%}×{s['program_years']}년 → {s['buy_trn']}조, 헤지 {s['hedge_ratio']*100:.1f}%, 갭 {s['gap_years']}년, μ {s['mu_pct']}" for s in sens))

# ── 해외 비교 ───────────────────────────────────────────────────────────────
uk_ratio = f("uk_ldi_exposure_bn_gbp") / 2200; kr_ratio = L_g / float(mkt["ktb_outstanding_trn"])
L(f"[비교] 영국 DB 부채 약 1.4조 파운드 · 길트 시장 약 2.2조(부채/시장 {1400/2200:.2f}) · LDI 익스포저 1.5조 — 그래도 2022년에 무너졌다 / 한국 부채 {L_g:,.0f}조 · 국고채 {float(mkt['ktb_outstanding_trn']):,.0f}조(부채/시장 {kr_ratio:.2f}) · 초장기 {long_out:.0f}조")

res = {"asof": P["asof"], "liability": {"window_end": END, "L_hurdle_trn": round(L_h), "L_gov_trn": round(L_g), "L_gov_down100_trn": round(L_g_dn), "L_gov_up100_trn": round(L_g_up),
        "PV_benefit_trn": round(PVben_g), "PV_contrib_trn": round(PVcon_g), "D_L": round(D_L, 1), "D_benefit": round(D_ben, 1), "DV01_L_trn": round(DV01_L, 3),
        "FR_h": round(FR_h, 3), "FR_g": round(FR_g, 3), "FR_g_down100": round(FR_g_dn, 3), "FR_g_up100": round(FR_g_up, 3), "FR_g_2026h1": round(f("fund_2026h1_trn") / L_g, 3),
        "curve": {int(m): round(z(m), 2) for m in [1, 2, 3, 5, 10, 20, 30, 50]}, "deplete_55": dep55, "deplete_45": dep45},
       "assets": {"total_trn": round(A_TOT, 1), "DV01_A_trn": round(DV01_A, 4), "D_A_krw": round(D_A_krw, 2), "D_A_all": round(D_A_all, 2), "hedge_ratio_0": round(h0, 4), "gap0_years": round(gap0, 1),
                  "mu0_pct": round(mu0, 2), "mu_saa_pct": round(mu_saa, 2), "DV01_A_saa_trn": round(DV01_A_SAA, 4), "hedge_ratio_saa": round(h_saa, 4), "bond_dom_target_trn": round(BD_TARGET_AMT), "liquid_trn": round(liquid, 1), "dFR_A_down100_pp": round(dFR_A, 1), "cond1_gap_exists": cond1_gap_exists},
       "instruments": {"bond30_yield": round(y30, 2), "D_bond30": round(D_bond30, 1), "D_irs30": round(D_irs30, 1), "dv01_per_100trn_bond": round(100 * dv01_per_trn_bond, 3)},
       "market": {"long_issue_2025_trn": long_issue, "cap_bond_trn": round(cap_bond_trn), "cap_irs_trn": round(cap_irs_trn), "long_out_trn": round(long_out), "ktb_out_trn": float(mkt["ktb_outstanding_trn"]),
                  "irs_turnover_trn": irs_turn, "liab_to_ktb": round(kr_ratio, 2)},
       "options": res_opts, "grid": grid, "sensitivity_B": sens}
json.dump(res, open(f"{D}/w7m8_results.json", "w"), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
open(f"{D}/compute_log.txt", "w").write("\n".join(log) + "\n")
print("→ w7m8_results.json · compute_log.txt")
