# -*- coding: utf-8 -*-
from nbhelp import M, C, build, badge
import m7data as d

F = "07_국민연금_LDI_케이스.ipynb"
YRS, CON, BEN, NET = d.cashflow()
MATS, YLDS = d.curve()
PR, MK = d.params(), d.market()
AS = {a["asset"]: a for a in d.assets()}
f = lambda k: float(PR[k])
END = int(f("liab_end_year"))

def asset_row(k):
    a = AS[k]
    tgt = a["target_pct_2027"] or "None"
    return (f'    "{k}": dict(name="{a["name"]}", amount={float(a["amount_trn_krw"])}, target={tgt}, D={float(a["mod_duration_y"])}, '
            f'krw={float(a["krw_rate_exposure"])}, mu={float(a["mu_pct"])}, gov={float(a["gov_bond_trn_krw"])}),')

ASSET_SRC = "ASSETS = {\n" + "\n".join(asset_row(k) for k in AS) + "\n}"

title = M(f"""
# 07 · 국민연금 LDI 케이스 — 모의 IC 제1호의 숫자 재현

{badge(F)}

**W06 M7 LDI 강의본 9 · 20 · 36 · 53 · 71~74장**(모의 IC)과 케이스 덱의 판정 숫자를 **케이스 데이터(교육용 추계)** 로 재현합니다.
계산 방식은 `W06_M7_케이스데이터/w6m7_compute.py`와 같고, 기대 결과는 `compute_log.txt` · 실습 덱 11장입니다. CSV 숫자는 노트북 안 상수로 옮겼습니다.

| 단계 | 강의 | 이 노트북에서 |
|---|---|---|
| 조건 ① 갭의 실재 | 9 · 20 · 36 · 73장 | 순부채 1,542 / 2,122조 · FR 95 / 69% · D_L 35.0년 · DV01 7.43조/bp · 원화 자산 D 0.85년 · 갭 −34.1년 · 헤지 2.1% → 3.0% · −100bp FR 69 → 49% |
| 수단 | 73장 · 케이스 | 30년 국고채 D 16.1 · IRS 30년 D 16.4 |
| 조건 ② 시장 수용 | 73장 | 장기물 87.3조 × 5년 × 30% = 131조 · IRS 5,986조 × 5% = 299조 |
| 조건 ③ 버퍼 | 53 · 73장 | 사흘 +200bp 증거금 401조 vs 유동자산 123조 · 250bp 버퍼 501조 |
| 조건 ④ 허들 · ⑤ 지침 | 73장 | μ ≥ 5.5% · 국내채권 ≤ 21.8 + 7.0%p · 파생 조항 없음 |
| 안 A · B · C | 9 · 72 · 74장 | 헤지 3 · 5(4.9) · 30% · 갭 · 필요 매입액 · 명목 · 판정 표 → 기본 답 안 B |

**모든 숫자는 '케이스 데이터(교육용 추계) 기준, 우리 계산'** 입니다. 공시 지표는 적립배율이며 적립비율이 아닙니다.
""")

cells = [
M(f"""
## 1. 케이스 데이터 — 노트북 안 상수
출처: `W06_M7_케이스데이터/` `fml_w6m7_cashflow.csv`(교육용 추계, W07과 같은 가정) · `fml_w6m7_curve.csv`(3 · 10 · 30 · 50년 공시 + 보간) ·
`fml_w6m7_assets.csv`(금액 · 비중 공시, 듀레이션 · μ는 교육용 가정) · `fml_w6m7_market.csv` · `fml_w6m7_params.csv`. 기준일 {PR['asof']}.
"""),
C(f"""
YEARS = np.arange({YRS[0]}, {YRS[-1] + 1})                       # 2026~2095
CONTRIB = np.array({d.fmt_list(CON)})                              # 보험료(조)
BENEFIT = np.array({d.fmt_list(BEN)})                              # 급여(조)
NET = np.array({d.fmt_list(NET)})                                  # 순유출 = 급여 − 보험료(조)
MATS = np.array({MATS}); YLDS = np.array({YLDS})    # 국고채 곡선(만기 · %)
{ASSET_SRC}
P = dict(fund_2025={f('fund_2025_trn')}, fund_2026h1={f('fund_2026h1_trn')}, hurdle={f('hurdle_pct')}, end={END},
         dfr_material={f('dfr_material_pp')}, target_bd={f('target_bond_dom_2027_pct')}, range_bd={f('saa_range_bond_dom_pp')},
         kofr={f('kofr_pct')}, swap_spread={f('swap_spread_30y_pp')}, tenor={int(f('hedge_tenor_y'))}, program_years={f('program_years')},
         cap_issue={f('cap_issue_share')}, cap_irs={f('cap_irs_turnover_share')}, buffer_bp={f('buffer_bp')}, shock_3d={f('shock_bp_3d')},
         hedge_C={f('hedge_target_C')}, official_dep45={int(f('deplete_45_official'))}, official_dep55={int(f('deplete_55_official'))})
MKT = dict(long_issue={float(MK['ktb_issue_long_2025_trn'])}, irs_turnover={float(MK['irs_turnover_2025_trn'])}, ktb_out={float(MK['ktb_outstanding_trn'])},
           out30={float(MK['ktb_30y_out_2025_trn_est'])}, out50={float(MK['ktb_50y_out_2025_trn_est'])})
A_TOT = sum(a["amount"] for a in ASSETS.values())
F0 = P["fund_2025"]
win = YEARS <= P["end"]
print(f"자산 합계 {{A_TOT:,.1f}}조(2026.6) · 2025년 말 적립금 {{F0:,.0f}}조 · 부채 창 2026~{{P['end']}} ({{win.sum()}}년)")
"""),
M("""
## 2. 조건 ① 갭의 실재 — 순부채 두 눈금 · 듀레이션 · DV01
순부채 = 2026~2071 순유출의 현재가치(2025년 말 기준, 연말 현금흐름). 부채의 수정 듀레이션은 곡선을 ±10bp 평행 이동해 수치로 잽니다.
"""),
C("""
def z(t, shift_bp=0.0):
    return np.interp(t, MATS, YLDS) + shift_bp / 100

def pv_flows(flows, years, rate=None, shift_bp=0.0):
    t = np.asarray(years) - 2025
    r = np.full(t.shape, rate, dtype=float) if rate is not None else z(t, shift_bp)
    return float(np.sum(flows / (1 + r / 100) ** t))

net, yrs = NET[win], YEARS[win]
L_h = pv_flows(net, yrs, rate=P["hurdle"])
L_g = pv_flows(net, yrs)
PVben, PVcon = pv_flows(BENEFIT[win], yrs), pv_flows(CONTRIB[win], yrs)
D_L = -(pv_flows(net, yrs, shift_bp=10) - pv_flows(net, yrs, shift_bp=-10)) / (2 * L_g * 0.001)
DV01_L = D_L * L_g * 1e-4
FR_h, FR_g = F0 / L_h, F0 / L_g
print(f"순부채 — 자체 5.5%: {L_h:,.0f}조 · 국채 곡선: {L_g:,.0f}조 (급여 PV {PVben:,.0f} − 보험료 PV {PVcon:,.0f})")
print(f"FR_h = {FR_h:.0%} · FR_g = {FR_g:.0%} · (참고: 2026.6 자산 1,865.6조면 FR_g {P['fund_2026h1'] / L_g:.0%})")
print(f"부채 수정 듀레이션 D_L = {D_L:.1f}년 · DV01_L = {DV01_L:.2f}조/bp")
check("순부채 자체 5.5% (조)", L_h, 1542, 0.5, ",.0f")
check("순부채 국채 곡선 (조)", L_g, 2122, 0.5, ",.0f")
check("급여 PV (조)", PVben, 4659, 0.5, ",.0f")
check("보험료 PV (조)", PVcon, 2537, 0.5, ",.0f")
check("FR_h (%)", 100 * FR_h, 95, 0.5, ".1f")
check("FR_g (%)", 100 * FR_g, 69, 0.5, ".1f")
check("D_L (년)", D_L, 35.0, 0.05, ".2f")
check("DV01_L (조/bp)", DV01_L, 7.43, 0.005, ".3f")
"""),
M("""
**자산 쪽 원화 금리 민감도.** 해외채권 110조는 외화 금리 노출이라 원화 부채의 헤지가 아닙니다 — 국내채권 287.8조 × D 5.5(+ 단기자금)만 셉니다.
헤지비율 h = 자산 DV01 ÷ 부채 DV01(03 노트북의 식).
"""),
C("""
DV01_A = sum(a["amount"] * a["D"] * a["krw"] * 1e-4 for a in ASSETS.values())
D_A_krw = DV01_A / (A_TOT * 1e-4)
D_A_all = sum(a["amount"] * a["D"] for a in ASSETS.values()) / A_TOT
h0 = DV01_A / DV01_L
gap0 = D_A_krw - D_L
def fr_after(dv01_extra, shift_bp):
    \"\"\"평행 이동 뒤 국채 기준 FR — 자산은 DV01로(2026.6 DV01을 2025 말 규모로 환산), 부채는 곡선 재할인\"\"\"
    A1 = F0 - (DV01_A + dv01_extra) * shift_bp * (F0 / A_TOT)
    return A1 / pv_flows(net, yrs, shift_bp=shift_bp)
L_dn = pv_flows(net, yrs, shift_bp=-100)
dFR_A = 100 * (fr_after(0, -100) - FR_g)
print(f"자산 원화 DV01 {DV01_A:.3f}조/bp → 원화 금리 듀레이션 D_A = {D_A_krw:.2f}년 (외화 채권까지 세면 {D_A_all:.2f}년)")
print(f"듀레이션 갭 = {gap0:.1f}년 · 현 보유 헤지비율 h0 = {h0:.1%}")
print(f"금리 −100bp → 부채 {L_dn:,.0f}조 ({L_dn / L_g - 1:+.0%}) · FR_g {FR_g:.0%} → {fr_after(0, -100):.0%} (ΔFR {dFR_A:+.1f}%p, 임계 {P['dfr_material']:+.0f}%p → {'갭 실재' if dFR_A <= P['dfr_material'] else '갭 비실재'})")
check("자산 원화 DV01 (조/bp)", DV01_A, 0.158, 0.0005, ".4f")
check("원화 자산 D (년)", D_A_krw, 0.85, 0.005, ".3f")
check("외화 채권 포함 D (년)", D_A_all, 1.23, 0.005, ".3f")
check("듀레이션 갭 (년)", gap0, -34.1, 0.05, ".2f")
check("현 보유 헤지비율 (%)", 100 * h0, 2.1, 0.05, ".2f")
check("−100bp 부채 (조)", L_dn, 3019, 0.5, ",.0f")
check("−100bp FR_g (%)", 100 * fr_after(0, -100), 49, 0.5, ".1f")
check("−100bp ΔFR_g (%p)", dFR_A, -20.0, 0.05, ".2f")
"""),
M("""
**소진 연도(강의 22장 각주).** 고정 수익률로 기금 경로를 굴리는 재정추계 방식. 공식 추계는 5.5% → 2071 · 4.5% → 2064이고,
교육용 추계는 5.5% → 2070 · 4.5% → 2065로 1년씩 어긋납니다(현금흐름을 정점 · 소진에 맞춘 근사라서 — 수익률 1%p = 소진 5~7년이라는 메시지는 같음).
"""),
C("""
def deplete(rate):
    F = F0
    for y, c, b in zip(YEARS, CONTRIB, BENEFIT):
        F = F * (1 + rate / 100) + c - b
        if F <= 0: return int(y)
dep55, dep45 = deplete(5.5), deplete(4.5)
print(f"교육용 추계 소진 — 5.5%: {dep55} · 4.5%: {dep45} (공식 {P['official_dep55']} · {P['official_dep45']}) → 수익률 1%p = 소진 {dep55 - dep45}년")
check("교육용 소진 5.5% (compute_log)", dep55, 2070, 0, ".0f")
check("교육용 소진 4.5% (compute_log)", dep45, 2065, 0, ".0f")
"""),
M("""
## 3. 수단 · 시장 수용 · 유동자산 · 허들 (조건 ②~⑤의 입력)
- 30년 국고채(수익률 4.60%) · 30년 IRS(고정 4.45%)의 수정 듀레이션
- 조건 ②: 현물 매입 ≤ 장기물(20 · 30 · 50년) 연 발행 × 5년 × 30% · IRS 명목 ≤ 연간 원화 IRS 거래 × 5%
- 조건 ③: 담보 적격 유동자산 = 단기자금 + 국고채 보유
- 조건 ④: 2027 SAA 목표 구성의 기대수익 μ_SAA(위험자산 8.0 · 국내채권 4.2 · 해외채권 4.5, 교육용)
"""),
C("""
def par_mod_duration(T, y):
    c = y / 100; t = np.arange(1, T + 1); pv = c / (1 + c) ** t; pv[-1] += 1 / (1 + c) ** T
    return float(np.sum(t * pv) / (1 + c))
y30 = z(P["tenor"])
D_bond30 = par_mod_duration(P["tenor"], y30); D_irs30 = par_mod_duration(P["tenor"], y30 + P["swap_spread"])
dv01_bond, dv01_irs = D_bond30 * 1e-4, D_irs30 * 1e-4          # 1조당 DV01(조/bp)
cap_bond = P["cap_issue"] * P["program_years"] * MKT["long_issue"]
cap_irs = P["cap_irs"] * MKT["irs_turnover"]
liquid = ASSETS["cash"]["amount"] + ASSETS["bond_dom"]["gov"]
long_out = MKT["out30"] + MKT["out50"]
tw = {k: (a["target"] or 0.0) for k, a in ASSETS.items()}; tw["cash"] = max(0.0, 100 - sum(tw.values()))
mu_saa = sum(tw[k] * ASSETS[k]["mu"] for k in ASSETS) / 100
BD_TARGET = P["target_bd"] / 100 * A_TOT
D_BD = ASSETS["bond_dom"]["D"]
def dv01_assets(bond30):
    \"\"\"SAA 목표 국내채권(D 5.5) 중 bond30조를 30년물로 바꿔 든 경우의 원화 DV01\"\"\"
    return (BD_TARGET - bond30) * D_BD * 1e-4 + bond30 * dv01_bond
DV01_SAA = dv01_assets(0.0); h_saa = DV01_SAA / DV01_L
print(f"30년 국고채 D {D_bond30:.1f}년(100조 = {100 * dv01_bond:.3f}조/bp) · IRS 30년 D {D_irs30:.1f}년")
print(f"조건 ② 현물 상한 {MKT['long_issue']}조 × 5년 × 30% = {cap_bond:.0f}조 · IRS 상한 {MKT['irs_turnover']:,.0f}조 × 5% = {cap_irs:.0f}조 · 초장기 잔액 {long_out:.0f}조")
print(f"조건 ③ 유동자산 = {ASSETS['cash']['amount']} + {ASSETS['bond_dom']['gov']} = {liquid:.1f}조 · 조건 ④ μ_SAA = {mu_saa:.2f}% vs 허들 {P['hurdle']}%")
print(f"출발점 — 2027 목표 비중 이행 후 국내채권 {BD_TARGET:.0f}조 × D 5.5 → DV01 {DV01_SAA:.3f}조/bp · 헤지 {h_saa:.1%}")
check("30년 국고채 수정 D (년)", D_bond30, 16.1, 0.05, ".2f")
check("IRS 30년 수정 D (년)", D_irs30, 16.4, 0.05, ".2f")
check("조건 ② 현물 상한 (조)", cap_bond, 131, 0.5, ".1f")
check("조건 ② IRS 상한 (조)", cap_irs, 299, 0.5, ".1f")
check("초장기 국고채 잔액 (조)", long_out, 437, 0.5, ".1f")
check("유동자산 (조)", liquid, 123.2, 0.05, ".2f")
check("μ_SAA (%)", mu_saa, 6.91, 0.005, ".3f")
check("2027 목표 이행 시 헤지 (%)", 100 * h_saa, 3.0, 0.05, ".2f")
"""),
M("""
## 4. 안 A · B · C 판정 (강의 9 · 72 · 74장)
- **안 A · 현행 유지** — LDI 조치 없음, 2027 목표 비중만 채운다(헤지 3%), 부채 벤치마크 없음
- **안 B · 30년 국고채 교체** — 보유 채권 131조(시장 상한)를 5년간 30년 국고채로 바꿔 든다, 부채 벤치마크 공시, 증거금 없음
- **안 C · IRS 오버레이** — 30년 고정금리 수취 스왑을 명목 1,223조 맺어 헤지 30%, 부채 벤치마크 공시

판정: ① 갭이 실재하면 부채 지표(LBP) 없는 안 탈락 · ② 매입 ≤ 131조 · IRS ≤ 299조 · ③ 사흘 +200bp 증거금 · 250bp 버퍼 ≤ 유동자산 ·
④ 헤지 후 μ ≥ 5.5% · ⑤ 국내채권 ≤ 21.8 + 7.0%p, IRS는 지침에 파생 조항이 없어 개정 전 불가.
"""),
C("""
cond1_gap = dFR_A <= P["dfr_material"]
def mu_after_bond(buy):
    inside = min(buy, BD_TARGET); beyond = max(0.0, buy - BD_TARGET)
    return mu_saa + inside / A_TOT * (y30 - ASSETS["bond_dom"]["mu"]) + beyond / A_TOT * (y30 - 8.0)
def mu_after_irs(notional):
    return mu_saa + notional / A_TOT * ((y30 + P["swap_spread"]) - P["kofr"])

def judge(name, buy=0.0, irs=0.0, lbp=1):
    dv01_tot = dv01_assets(buy) + irs * dv01_irs
    h = dv01_tot / DV01_L
    gap = dv01_tot / (A_TOT * 1e-4) - D_L
    fr_dn = fr_after(dv01_tot - DV01_A, -100)
    vm3 = irs * dv01_irs * P["shock_3d"]; buf = irs * dv01_irs * P["buffer_bp"]
    mu = mu_after_bond(buy) if buy else (mu_after_irs(irs) if irs else mu_saa)
    bd_pct = max(BD_TARGET, buy) / A_TOT * 100
    c = [bool(lbp) if cond1_gap else True,
         buy <= cap_bond + 1e-9 and irs <= cap_irs + 1e-9,
         buf <= liquid and vm3 <= liquid,
         mu >= P["hurdle"],
         bd_pct <= P["target_bd"] + P["range_bd"] + 1e-9 and irs == 0]
    return dict(안=name, 매입=buy, 명목=irs, 헤지=h, 갭=gap, FR_dn=fr_dn, dFR=100 * (fr_dn - FR_g), 증거금=vm3, 버퍼=buf, mu=mu,
                국내채권=bd_pct, 상한대비=(irs / cap_irs if irs else buy / cap_bond), 조건=c)

irs_C = (P["hedge_C"] * DV01_L - DV01_SAA) / dv01_irs
OPTS = [judge("A", lbp=0), judge("B", buy=cap_bond), judge("C", irs=irs_C)]
ok = lambda b: "통과" if b else "탈락"
print(f"{'안':2s} {'30년물':>7s} {'IRS 명목':>9s} {'헤지':>6s} {'갭':>7s} {'−100bp FR':>10s} {'증거금':>7s} {'버퍼':>6s} {'μ':>6s}   조건 ①~⑤")
for o in OPTS:
    print(f"{o['안']:2s} {o['매입']:6.0f}조 {o['명목']:8,.0f}조 {o['헤지']:6.1%} {o['갭']:6.1f}년 {o['FR_dn']:5.0%}({o['dFR']:+.1f}) {o['증거금']:6.0f}조 {o['버퍼']:5.0f}조 {o['mu']:5.2f}%   "
          + " · ".join(ok(x) for x in o["조건"]))
A_, B_, C_ = OPTS
check("안 A 헤지 (%)", 100 * A_["헤지"], 3.0, 0.05, ".2f")
check("안 A 갭 (년)", A_["갭"], -33.8, 0.05, ".2f")
check("안 A −100bp ΔFR (%p)", A_["dFR"], -19.8, 0.05, ".2f")
check("안 B 매입 (조)", B_["매입"], 131, 0.5, ".1f")
check("안 B 헤지 (%)", 100 * B_["헤지"], 4.9, 0.05, ".2f")
check("안 B 갭 (년)", B_["갭"], -33.1, 0.05, ".2f")
check("안 B μ (%)", B_["mu"], 6.94, 0.005, ".3f")
check("안 C IRS 명목 (조)", C_["명목"], 1223, 0.5, ",.1f")
check("안 C 헤지 (%)", 100 * C_["헤지"], 30.0, 0.05, ".2f")
check("안 C 갭 (년)", C_["갭"], -23.1, 0.05, ".2f")
check("안 C −100bp FR (%)", 100 * C_["FR_dn"], 54, 0.5, ".1f")
check("안 C 사흘 +200bp 증거금 (조)", C_["증거금"], 401, 0.5, ".1f")
check("안 C 250bp 버퍼 (조)", C_["버퍼"], 501, 0.5, ".1f")
check("안 C IRS ÷ 시장 상한 (배)", C_["상한대비"], 4.1, 0.05, ".2f")
check("안 C μ (%)", C_["mu"], 7.37, 0.005, ".3f")
"""),
M("""
**판정 조건 ①~⑤ 표.** 안 B만 다섯 조건을 모두 통과합니다 → **기본 답: 안 B 조건부 승인**(부채 벤치마크 도입 + 시장 상한 131조까지 30년 국고채 교체).
헤지 후에도 남는 갭(−33년)의 부담자를 의결문에 반드시 적습니다.
"""),
C("""
NAMES = ["① 갭 실재 (LBP)", "② 시장 수용", "③ 버퍼", "④ 허들 5.5%", "⑤ 지침"]
fig, ax = plt.subplots(figsize=(8.5, 2.6))
ax.set_xlim(0, 5); ax.set_ylim(0, 3); ax.axis("off")
for j, n in enumerate(NAMES):
    ax.text(j + 0.5, 3.05, n, ha="center", va="bottom", fontsize=9, fontweight="bold", color=INK)
for i, o in enumerate(OPTS):
    yy = 2 - i
    ax.text(-0.08, yy + 0.5, f"안 {o['안']} · 헤지 {o['헤지']:.0%}", ha="right", va="center", fontsize=10, fontweight="bold")
    for j, c in enumerate(o["조건"]):
        ax.add_patch(plt.Rectangle((j + 0.04, yy + 0.06), 0.92, 0.88, color=TEAL if c else RED, alpha=0.9))
        ax.text(j + 0.5, yy + 0.5, "통과" if c else "탈락", ha="center", va="center", color="white", fontweight="bold")
ax.set_title("판정 조건 ①~⑤ — 다섯 조건을 모두 통과하는 안은 B뿐 (교육용 추계, 우리 계산)", pad=28)
plt.show()
for o in OPTS:
    check(f"안 {o['안']} 판정 (통과 조건 수)", sum(o["조건"]), {"A": 4, "B": 5, "C": 2}[o["안"]], 0, ".0f")
"""),
M("""
## 5. 그래프 — 금리 이동에 따른 적립비율(두 눈금)
국채 눈금(FR_g)은 곡선을 평행 이동해 부채를 다시 할인하고, 자산은 안별 DV01로 움직입니다. 자체 눈금(FR_h)은 할인율이 5.5%로 고정이라
부채가 움직이지 않고 자산 DV01만큼만 흔들립니다 — **두 눈금은 금리 위험을 전혀 다르게 보여 줍니다.**
"""),
C("""
shifts = np.arange(-200, 201, 10)
fig, ax = plt.subplots(figsize=(9, 4.6))
for o, c in zip(OPTS, [RED, TEAL, INK]):
    extra = dv01_assets(o["매입"]) + o["명목"] * dv01_irs - DV01_A
    ax.plot(shifts, [100 * fr_after(extra, s) for s in shifts], color=c, lw=2.2, label=f"국채 눈금 FR_g — 안 {o['안']} (헤지 {o['헤지']:.0%})")
FRh_line = [100 * (F0 - DV01_A * s * (F0 / A_TOT)) / L_h for s in shifts]
ax.plot(shifts, FRh_line, color=OLIVE, lw=1.8, ls="--", label="자체 눈금 FR_h (5.5% 고정 — 부채 불변)")
ax.axhline(100, color=GRAY, lw=0.8, ls=":"); ax.axvline(0, color=GRAY, lw=0.6)
ax.annotate(f"−100bp: {FR_g:.0%} → {fr_after(0, -100):.0%}", (-100, 100 * fr_after(0, -100)), textcoords="offset points", xytext=(10, -22), color=RED, fontsize=9)
ax.scatter([-100], [100 * fr_after(0, -100)], color=LIME, edgecolor=RED, zorder=5, s=70)
ax.set_xlabel("국채 곡선 평행 이동 (bp)"); ax.set_ylabel("적립비율 (%)")
ax.set_title("금리 −100bp에 FR_g 69 → 49% — 안 C(헤지 30%)도 54%에 그친다")
ax.legend(fontsize=8.5, loc="lower right")
plt.show()
"""),
M("""
## 6. 그래프 — 안별 헤지비율 · 증거금 vs 유동자산 · 시장 상한
"""),
C("""
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.3))
bars = ax1.bar([f"안 {o['안']}" for o in OPTS], [100 * o["헤지"] for o in OPTS], color=[GRAY, TEAL, INK], edgecolor=INK)
for b, o in zip(bars, OPTS):
    ax1.text(b.get_x() + b.get_width() / 2, 100 * o["헤지"] + 0.8, f"{o['헤지']:.1%}\\n갭 {o['갭']:.1f}년", ha="center", fontsize=9)
ax1.axhline(100 * h0, color=RED, ls="--", lw=1, label=f"현 보유 헤지 {h0:.1%}"); ax1.legend(loc="upper left")
ax1.set_ylim(0, 40); ax1.set_ylabel("헤지비율 (%)"); ax1.set_title("헤지비율 = 자산 DV01 ÷ 부채 DV01")
labels = ["안 C 사흘\\n+200bp 증거금", "안 C 250bp\\n버퍼", "유동자산\\n(단기 + 국고채)", "IRS 시장\\n상한", "안 C\\n명목"]
vals = [C_["증거금"], C_["버퍼"], liquid, cap_irs, C_["명목"]]
cols = [RED, RED, TEAL, OLIVE, INK]
bars = ax2.bar(labels, vals, color=cols, edgecolor=INK)
for b, v in zip(bars, vals):
    ax2.text(b.get_x() + b.get_width() / 2, v + 20, f"{v:,.0f}조", ha="center", fontsize=9, fontweight="bold")
ax2.set_ylabel("조원"); ax2.set_ylim(0, 1400)
ax2.set_title("안 C — 증거금 401조 > 유동자산 123조 · 명목은 시장 상한의 4.1배")
fig.tight_layout(); plt.show()
"""),
M("""
## 7. 헤지 비율 격자 — 현물로 / IRS로 각각 얼마가 드나 (compute_log '격자')
목표 헤지비율 h\\*에서 필요한 추가 DV01 = h\\*·DV01_L − DV01_SAA. 현물은 D 5.5 채권을 D 16.1로 바꾸는 순증분으로, IRS는 명목 × D 16.4로 채웁니다.
"""),
C("""
print(f"{'h*':>5s} {'현물 매입':>9s} {'= 장기물 발행':>12s} {'IRS 명목':>9s} {'사흘 증거금':>10s} {'μ 현물':>7s} {'μ IRS':>7s}")
GRID = []
for ht in [0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 1.00]:
    need = max(0.0, ht * DV01_L - DV01_SAA)
    bond = need / (dv01_bond - D_BD * 1e-4); irs = need / dv01_irs
    GRID.append((ht, bond, irs))
    print(f"{ht:5.0%} {bond:8,.0f}조 {bond / MKT['long_issue']:10.1f}년치 {irs:8,.0f}조 {irs * dv01_irs * 200:9,.0f}조 {mu_after_bond(bond):6.2f}% {mu_after_irs(irs):6.2f}%")
check("격자 h 30% IRS 명목 (조)", GRID[3][2], 1223, 0.5, ",.0f")
check("격자 h 100% 현물 매입 (조)", GRID[6][1], 6796, 0.5, ",.0f")
print("→ 현물만으로 헤지 30%를 하려면 장기물 발행 20년치 이상이 필요하다 — 조건 ②가 현물 헤지의 천장을 정한다")
"""),
M("""
## 8. 정리 — IC 발언으로
- "조건 ①: 국채 눈금 FR 69%, −100bp에 49%(−20%p) — 갭은 실재한다. 부채 벤치마크 없는 안 A는 탈락."
- "조건 ②: 시장이 받아 줄 현물은 131조 — 헤지는 3 → 4.9%까지. 안 C의 스왑 1,223조는 IRS 상한 299조의 4.1배."
- "조건 ③: 안 C는 사흘 +200bp에 증거금 401조, 유동자산은 123조 — 2022 영국의 조건이 그대로 재현된다."
- **기본 답: 안 B 조건부 승인** — 그리고 헤지 후에도 남는 갭 −33년의 부담자를 의결문에 적는다.
"""),
]

ex = [
    "조건 ②의 임계를 '장기물 발행의 50% × 10년'으로 완화하면 안 B의 매입액 · 헤지비율 · 갭은? (`judge('B2', buy=0.5 * 10 * MKT['long_issue'])`)",
    "안 C를 헤지 10%로 줄이면 IRS 명목 · 사흘 증거금은? 조건 ② · ③을 통과하나? (`irs = (0.10 * DV01_L - DV01_SAA) / dv01_irs`)",
    "국채 곡선이 전체적으로 +100bp 오른 상태에서 출발하면 FR_g와 D_L은 어떻게 바뀌나? (`pv_flows(net, yrs, shift_bp=100)`)",
]

if __name__ == "__main__":
    build(F, title, cells, ex)
