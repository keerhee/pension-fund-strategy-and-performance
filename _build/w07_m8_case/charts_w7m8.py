#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W07 M8 케이스 v3 그림 — w7m8_results.json · CSV 에서 그린다 (matplotlib, Noto Sans CJK KR). 출력 img/*.png + img/img_ratios.json 갱신"""
import json, os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(HERE)
D, IMG = f"{W}/data", f"{W}/img"; os.makedirs(IMG, exist_ok=True)
fm.fontManager.addfont(os.path.expanduser("~/Library/Fonts/NotoSansCJK.ttc"))
plt.rcParams.update({"font.family": "Noto Sans CJK KR", "font.size": 15, "axes.titlesize": 17, "axes.labelsize": 15,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#6B7280", "axes.unicode_minus": False})
NAVY, BLUE, GREEN, ORANGE, GRAY, BODY, MUTED, HAIR, RED = "#1B2C5E", "#2E5BAA", "#3FA36F", "#E65100", "#F4F5F9", "#3B4252", "#6B7280", "#D6D6DB", "#B23A48"
R = json.load(open(f"{D}/w7m8_results.json"))
cf = pd.read_csv(f"{D}/fml_w7m8_cashflow.csv"); P = pd.read_csv(f"{D}/fml_w7m8_params.csv").set_index("key").value
LI, AS, MK, IN = R["liability"], R["assets"], R["market"], R["instruments"]
OPT = {o["option"]: o for o in R["options"]}; grid = pd.DataFrame(R["grid"])


def save(fig, name):
    fig.savefig(f"{IMG}/{name}.png", dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig); print("→", name)


# 1. 현금흐름 — 급여 · 보험료 · 순유출 (2026~2071) ---------------------------------
w = cf[cf.year <= LI["window_end"]]
fig, ax = plt.subplots(figsize=(12.5, 5.4))
ax.bar(w.year, w.benefit_trn_krw, color=NAVY, width=0.8, label="급여 지출")
ax.bar(w.year, -w.contrib_trn_krw, color=BLUE, width=0.8, label="보험료 수입(−)")
ax.plot(w.year, w.net_outflow_trn_krw, color=ORANGE, lw=3, label="순유출 = 급여 − 보험료 (기금이 지는 부채의 현금흐름)")
net0 = int(w.year[w.net_outflow_trn_krw > 0].min())
ax.axvline(net0, color=HAIR, lw=1.5); ax.text(net0 + 0.4, ax.get_ylim()[1] * 0.02 + 900, f"순유출 전환 {net0}", color=MUTED, fontsize=13)
ax.axhline(0, color=MUTED, lw=0.8)
ax.set_xlim(2025.3, LI["window_end"] + 0.7); ax.set_ylabel("조원 / 년"); ax.set_xlabel("연도")
ax.set_title(f"기금이 지는 부채는 '급여'가 아니라 '순유출'이다 — 2026~{LI['window_end']}(개혁 후 5.5% 소진 연도)까지의 창, 교육용 추계", loc="left", color=NAVY)
ax.legend(loc="upper left", frameon=False, fontsize=13); ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_cashflow")

# 2. 두 할인율의 부채와 적립비율 ------------------------------------------------------
labels = ["자체 기준 5.5%\n(연금개혁 전제)", "국채 곡선\n(2026-09-18)", "국채 곡선 −100bp", "국채 곡선 +100bp"]
vals = [LI["L_hurdle_trn"], LI["L_gov_trn"], LI["L_gov_down100_trn"], LI["L_gov_up100_trn"]]
frs = [LI["FR_h"], LI["FR_g"], LI["FR_g_down100"], LI["FR_g_up100"]]
fig, ax = plt.subplots(figsize=(12.5, 5.4))
cols = [MUTED, NAVY, RED, GREEN]
ax.bar(labels, vals, color=cols, width=0.58)
F0 = float(P["fund_2025_trn"]); ax.axhline(F0, color=ORANGE, lw=2, ls="--", label=f"적립금 F = {F0:,.0f}조 (2025년 말) — 이 선 위가 미적립"); ax.legend(loc="upper left", frameon=False, fontsize=13)
for i, (v, fr) in enumerate(zip(vals, frs)):
    ax.text(i, v + 45, f"{v:,.0f}조", ha="center", fontsize=15, color=BODY, fontweight="bold")
    ax.text(i, v * 0.62, f"FR = {fr*100:.0f}%", ha="center", va="center", fontsize=17, color="white", fontweight="bold")
ax.set_ylim(0, max(vals) * 1.15); ax.set_ylabel("순부채 PV (조원)")
ax.set_title(f"같은 현금흐름, 다른 눈금 — 자체 기준 FR {LI['FR_h']*100:.0f}% 는 국채 기준 {LI['FR_g']*100:.0f}% 이고, −100bp 면 {LI['FR_g_down100']*100:.0f}% (D_L {LI['D_L']:.0f}년)", loc="left", color=NAVY)
ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_liability_fr")

# 3. 시장의 크기 — 부채 대 국고채 -------------------------------------------------------
items = [("순부채 PV (국채 기준)", LI["L_gov_trn"], NAVY), ("국고채 잔액 2025 말", MK["ktb_out_trn"], BLUE), ("30·50년물 잔액(추정)", MK["long_out_trn"], BLUE),
         ("장기물(20·30·50년) 발행 5년치", 5 * MK["long_issue_2025_trn"], GREEN), ("조건 ② 매입 상한(발행의 30%)", MK["cap_bond_trn"], ORANGE),
         ("담보 적격 유동자산", AS["liquid_trn"], MUTED)]
fig, ax = plt.subplots(figsize=(12.5, 5.2))
ax.barh([i[0] for i in items][::-1], [i[1] for i in items][::-1], color=[i[2] for i in items][::-1], height=0.6)
for i, (n, v, c) in enumerate(items[::-1]): ax.text(v + 25, i, f"{v:,.0f}조", va="center", fontsize=14, color=BODY)
ax.set_xlim(0, LI["L_gov_trn"] * 1.15); ax.set_xlabel("조원")
ax.set_title(f"부채는 국고채 시장의 {MK['liab_to_ktb']:.1f}배 — 영국(부채/길트 약 0.6)도 무너졌는데, 한국은 헤지 수단 자체가 부채보다 작다", loc="left", color=NAVY)
ax.grid(axis="x", color=HAIR, lw=0.8)
save(fig, "fig_market_scale")

# 4. 헤지 비율 격자 — 현물이면 얼마를, IRS 면 얼마를 ---------------------------------
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.5, 5.3)); fig.subplots_adjust(top=0.80, wspace=0.28)
grid = grid[grid.hedge_ratio <= 0.5].reset_index(drop=True)
x = grid.hedge_ratio * 100
ax.bar(x - 1.4, grid.bond_buy_trn, width=2.8, color=BLUE, label="현물 30년 국고채 매입액(조)")
ax.bar(x + 1.4, grid.irs_notional_trn, width=2.8, color=NAVY, label="IRS 30년 명목(조)")
ax.axhline(MK["cap_bond_trn"], color=BLUE, ls=":", lw=1.8); ax.text(40, MK["cap_bond_trn"] - 60, f"현물 상한 {MK['cap_bond_trn']}조", color=BLUE, fontsize=12, ha="center", va="top")
ax.axhline(MK["cap_irs_trn"], color=NAVY, ls=":", lw=1.8); ax.text(40, MK["cap_irs_trn"] + 40, f"IRS 상한 {MK['cap_irs_trn']}조", color=NAVY, fontsize=12, ha="center")
ax.set_xlabel("헤지 비율 목표 (%)"); ax.set_ylabel("조원"); ax.set_title("조건 ② 시장 수용 — 필요 매입액 · 명목", loc="left", color=NAVY)
ax.set_ylim(0, 3600); ax.set_xlim(0, 55); ax.legend(loc="upper left", frameon=False, fontsize=12); ax.grid(axis="y", color=HAIR, lw=0.8)
bx.bar(x - 1.4, grid.vm_3d_trn, width=2.8, color=RED, label=f"3영업일 +{int(float(P['shock_bp_3d']))}bp 변동증거금(조)")
bx.bar(x + 1.4, grid.buffer_trn, width=2.8, color=ORANGE, label="250bp 버퍼 요구액(조)")
bx.axhline(AS["liquid_trn"], color=MUTED, ls="--", lw=1.8); bx.text(40, AS["liquid_trn"] + 15, f"담보 적격 유동자산 {AS['liquid_trn']:.0f}조", color=MUTED, fontsize=12, ha="center")
bx.set_xlabel("헤지 비율 목표 (%)"); bx.set_title("조건 ③ 유동성 버퍼 — IRS 로 할 때", loc="left", color=NAVY)
bx.set_ylim(0, 1000); bx.set_xlim(0, 55); bx.legend(loc="upper left", frameon=False, fontsize=12); bx.grid(axis="y", color=HAIR, lw=0.8)
fig.suptitle(f"헤지 비율 5% 까지가 시장의 상한이다 — 30% 는 현물로 {grid.bond_buy_trn[3]:,.0f}조(장기물 발행 {grid.bond_years_of_long_issue[3]:.0f}년치), IRS 로 명목 {grid.irs_notional_trn[3]:,.0f}조 · 증거금 {grid.vm_3d_trn[3]:,.0f}조", x=0.01, y=0.97, ha="left", color=NAVY, fontsize=17)
save(fig, "fig_hedge_grid")

# 5. 평행 이동에 따른 국채 기준 적립비율 — 세 안 -------------------------------------------
shifts = np.arange(-200, 201, 25)
mats = pd.read_csv(f"{D}/fml_w7m8_curve.csv"); m_, y_ = mats.maturity_y.values.astype(float), mats.yield_pct.values
net, yrs = w.net_outflow_trn_krw.values, w.year.values
def pv(shift):
    t = yrs - 2025; r = np.interp(t, m_, y_) + shift / 100; return float(np.sum(net / (1 + r / 100) ** t))
A_TOT = AS["total_trn"]
fig, ax = plt.subplots(figsize=(12.5, 5.2))
for k, c, ls in [("A", MUTED, "--"), ("B", NAVY, "-"), ("C", BLUE, "-")]:
    dv = AS["DV01_A_saa_trn"] + OPT[k]["dv01_extra_trn"] + (AS["DV01_A_trn"] - AS["DV01_A_saa_trn"]) * 0  # 안별 총 DV01 (SAA 출발점)
    dv = AS["DV01_A_trn"] + OPT[k]["dv01_extra_trn"]
    fr = [(F0 - dv * s * (F0 / A_TOT)) / pv(s) * 100 for s in shifts]
    ax.plot(shifts, fr, color=c, lw=3 if k == "B" else 2.2, ls=ls, label=f"안 {k} — 헤지 비율 {OPT[k]['hedge_ratio']*100:.0f}% · −100bp 시 FR {OPT[k]['fr_g_down100']*100:.0f}%")
ax.axhline(100, color=ORANGE, ls=":", lw=1.5); ax.text(-198, 101.5, "완전 적립 100%", color=ORANGE, fontsize=12)
ax.axvline(0, color=HAIR, lw=1.2); ax.set_xlabel("국채 곡선 평행 이동 (bp)"); ax.set_ylabel("국채 기준 적립비율 FR_g (%)")
ax.set_title("금리가 내리면 세 안 모두 적립비율이 떨어진다 — 시장이 허용하는 헤지(안 B)는 기울기를 거의 바꾸지 못한다", loc="left", color=NAVY)
ax.legend(loc="upper left", frameon=False, fontsize=13); ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_fr_shift")

# 6. 안 C 의 증거금 — 영국 2022 와 나란히 ------------------------------------------------
fig, ax = plt.subplots(figsize=(12.5, 5.0))
names = ["안 C 3일 +200bp\n변동증거금", "안 C 250bp 버퍼\n(TPR 최소 회복력)", "담보 적격\n유동자산(단기+국고채)", "국고채 보유 전체\n(국내채권의 41%)", "안 B 증거금\n(현물 — 없음)"]
vals = [OPT["C"]["vm_3d_trn"], OPT["C"]["buffer_req_trn"], AS["liquid_trn"], AS["liquid_trn"] - 4.6, 0]
ax.bar(names, vals, color=[RED, ORANGE, MUTED, MUTED, GREEN], width=0.58)
for i, v in enumerate(vals): ax.text(i, v + 12, f"{v:,.0f}조", ha="center", fontsize=15, color=BODY, fontweight="bold")
ax.set_ylim(0, max(vals) * 1.2); ax.set_ylabel("조원")
ax.set_title(f"안 C — 하루 {OPT['C']['vm_3d_trn']/3:,.0f}조씩 사흘 — 증거금이 유동자산의 {OPT['C']['vm_3d_trn']/AS['liquid_trn']:.1f}배: 2022년 영국의 Doom Loop 가 여기서 시작된다", loc="left", color=NAVY)
ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_margin")

# ratios ---------------------------------------------------------------------------
rp = f"{IMG}/img_ratios.json"; ratios = json.load(open(rp)) if os.path.exists(rp) else {}
for fn in os.listdir(IMG):
    if fn.endswith(".png"):
        im = Image.open(f"{IMG}/{fn}"); ratios[fn[:-4]] = round(im.width / im.height, 4)
json.dump(ratios, open(rp, "w"), indent=1)
print("charts done · ratios:", len(ratios))
