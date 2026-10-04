#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W06 케이스 v3 그림 — w7m9_results.json · CSV 에서 그린다 (matplotlib, Noto Sans CJK KR). 출력 img/*.png"""
import json, os, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__)); W6 = os.path.dirname(HERE)
D, IMG = f"{W6}/data", f"{W6}/img"; os.makedirs(IMG, exist_ok=True)
for _fp in (os.path.expanduser("~/Library/Fonts/NotoSansCJK.ttc"), "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"):
    if os.path.exists(_fp): fm.fontManager.addfont(_fp); break
plt.rcParams.update({"font.family": "Noto Sans CJK KR", "font.size": 15, "axes.titlesize": 17, "axes.labelsize": 15,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#6B7280", "axes.unicode_minus": False})
NAVY, BLUE, GREEN, ORANGE, GRAY, BODY, MUTED, HAIR = "#1B2C5E", "#2E5BAA", "#3FA36F", "#E65100", "#F4F5F9", "#3B4252", "#6B7280", "#D6D6DB"
R = json.load(open(f"{D}/w7m9_results.json"))
cf = pd.read_csv(f"{D}/fml_w7m9_cashflow.csv"); gp = pd.read_csv(f"{D}/fml_w7m9_glidepaths.csv")
cma = pd.read_csv(f"{D}/fml_w7m9_cma.csv").set_index("asset"); P = pd.read_csv(f"{D}/fml_w7m9_params.csv").set_index("key").value
MU_R, MU_S, SG_R, SG_S, RHO = cma.mu_pct["risk"], cma.mu_pct["safe"], cma.sigma_pct["risk"], cma.sigma_pct["safe"], float(P["rho"])
F0 = float(P["fund_2025_trn"])
a1 = R["agenda1"]; paths = {p["path"]: p for p in a1["paths"]}
trig, netout, peakA = a1["cond1"]["trigger_year"], a1["cond1"]["net_outflow_year"], a1["cond1"]["peak_year_A"]


def mu(w): return w * MU_R + (1 - w) * MU_S
def project(w):
    F = F0; out = []
    for i, r in cf.iterrows():
        Fb = F; F = F * (1 + mu(w[i]) / 100) + r.contrib_trn_krw - r.benefit_trn_krw
        out.append((int(r.year), Fb, max(F, 0)))
        if F <= 0: break
    return pd.DataFrame(out, columns=["year", "Fb", "Fe"])


def save(fig, name):
    fig.savefig(f"{IMG}/{name}.png", dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig); print("→", name)


# 1. 기금 경로 A·B·C ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12.5, 5.6))
cols = {"A": MUTED, "B": NAVY, "C": BLUE}
for k in ["A", "B", "C"]:
    pr = project(gp[f"w_risk_{k}"].values)
    ax.plot(pr.year, pr.Fe / 1000, color=cols[k], lw=3 if k == "B" else 2.2, ls="-" if k != "A" else "--",
            label=f"안 {k} — 정점 {paths[k]['peak_year']}년 {paths[k]['peak_fund']/1000:.1f}천조 · 소진 {paths[k]['deplete_year']}")
ax.axvline(netout, color=HAIR, lw=1.5); ax.text(netout + 0.3, 0.3, f"순유출 전환 {netout}", color=MUTED, fontsize=13)
ax.axvline(trig, color=GREEN, lw=1.5, ls=":"); ax.text(trig + 0.3, 4.9, f"안 B 감축 시작 {trig}\n(H/F < 0.625)", color=GREEN, fontsize=13)
ax.axvline(2071, color=ORANGE, lw=1.5, ls=":"); ax.text(2071 + 0.3, 3.9, "조건 ④\n소진 ≥ 2071\n(개혁 후 5.5% 전망)", color=ORANGE, fontsize=13)
ax.set_xlim(2026, 2080); ax.set_ylim(0, 7.8); ax.set_ylabel("적립금 (천조 원)"); ax.set_xlabel("연도")
ax.set_title("기금 경로 — 감축을 늦출수록 정점은 높고, 일찍 하면 소진이 당겨진다 (교육용 CMA 8.0 / 3.0)", loc="left", color=NAVY)
ax.legend(loc="upper left", frameon=False, fontsize=13); ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_fund_paths")

# 2. H/F 비율과 총부 기준 위험자산 비중 ----------------------------------------------
tab = pd.DataFrame(a1["cond1"]["table"]); tab = tab[tab.year <= 2070]
fig, ax = plt.subplots(figsize=(12.5, 5.4)); ax2 = ax.twinx(); ax2.spines["right"].set_visible(True)
ax.plot(tab.year, tab.HF, color=NAVY, lw=3, label="H/F = 향후 30년 보험료 PV ÷ 기금 (좌)")
ax2.plot(tab.year, tab.risk_share_total_wealth * 100, color=GREEN, lw=2.5, ls="--", label="총부 기준 위험자산 비중 65·F/(F+H) (우, %)")
ax.axhline(0.625, color=ORANGE, lw=1.5, ls=":"); ax.text(2027, 0.66, "조건 ① 임계 H/F = 0.625 ⇔ 총부 위험비중 40%", color=ORANGE, fontsize=13)
ax.axvline(trig, color=GREEN, lw=1.5, ls=":"); ax.text(trig + 0.3, 1.05, f"{trig}년 도달\n→ 감축 시작 하한", color=GREEN, fontsize=13)
ax.set_ylim(0, 1.3); ax2.set_ylim(20, 50); ax.set_ylabel("H/F"); ax2.set_ylabel("총부 위험자산 비중 (%)"); ax.set_xlabel("연도")
ax.set_title("인적자본 유사물 — 2026년 H/F 1.16, 총부 기준 위험자산은 30%뿐이다 (BMS 1992의 기관판)", loc="left", color=NAVY)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, loc="upper right", frameon=False, fontsize=13)
ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_hf_ratio")

# 3. 글라이드패스 세 안 --------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12.5, 5.0))
for k in ["A", "B", "C"]:
    ax.plot(gp.year, gp[f"w_risk_{k}"] * 100, color=cols[k], lw=3 if k == "B" else 2.2, ls="-" if k != "A" else "--", label=f"안 {k}")
ax.axhline(a1["hurdle_min_w"] * 100, color=ORANGE, lw=1.5, ls=":"); ax.text(2027, a1["hurdle_min_w"] * 100 + 0.8, "조건 ② 허들 하한 w_h = 50% (μ = 5.5%)", color=ORANGE, fontsize=13)
ax.axvline(trig, color=GREEN, lw=1.5, ls=":"); ax.text(trig + 0.4, 66.5, f"조건 ① 트리거 {trig}", color=GREEN, fontsize=13)
ax.set_xlim(2026, 2080); ax.set_ylim(40, 70); ax.set_ylabel("위험자산 비중 (%)"); ax.set_xlabel("연도")
ax.set_title("세 안의 글라이드패스 — 언제 시작해, 어디서 멈추는가", loc="left", color=NAVY)
ax.legend(loc="lower left", frameon=False, fontsize=13); ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_glidepaths")

# 4. 시간분산 — 비율 vs 금액 -------------------------------------------------------
td = pd.DataFrame(a1["time_div"])
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.5, 5.2)); fig.subplots_adjust(top=0.8)
ax.bar(td["T"].astype(str), td.annualized, color=BLUE, width=0.6); ax.set_title("연환산 σ/√T (%) — 줄어든다", loc="left", color=NAVY); ax.set_xlabel("지평 T (년)")
for i, v in enumerate(td.annualized): ax.text(i, v + 0.2, f"{v:.1f}", ha="center", fontsize=13, color=BODY)
bx.bar(td["T"].astype(str), td.cumulative, color=NAVY, width=0.6); bx.set_title("누적 σ√T (%) — 커진다 (Samuelson의 반격)", loc="left", color=NAVY); bx.set_xlabel("지평 T (년)")
for i, v in enumerate(td.cumulative): bx.text(i, v + 1, f"{v:.0f}", ha="center", fontsize=13, color=BODY)
for a in (ax, bx): a.grid(axis="y", color=HAIR, lw=0.8)
fig.suptitle("같은 65:35(σ 10%)를 두 자로 재면 정반대 — 기금이 커질수록 '금액'이 급여를 넘는다", x=0.01, y=0.97, ha="left", color=NAVY, fontsize=17)
save(fig, "fig_time_div")

# 5. 1σ 손실액 / 급여 (조건 ③) ------------------------------------------------------
fig, ax = plt.subplots(figsize=(12.5, 5.0))
for k in ["A", "B", "C"]:
    pr = project(gp[f"w_risk_{k}"].values); w = gp[f"w_risk_{k}"].values[: len(pr)]
    ben = cf.benefit_trn_krw.values[: len(pr)]
    lr = w * SG_R / 100 * pr.Fb.values / ben
    m = (pr.year >= 2040) & (pr.year <= 2074)
    ax.plot(pr.year[m], lr[m], color=cols[k], lw=3 if k == "B" else 2.2, ls="-" if k != "A" else "--", label=f"안 {k} — 최대 {paths[k]['loss_ratio_max']:.2f}년치")
ax.axhline(1.0, color=ORANGE, lw=1.5, ls=":"); ax.text(2040.5, 1.03, "조건 ③ 상한 — 1σ 연간 손실액 ≤ 그해 급여 1년치", color=ORANGE, fontsize=13)
ax.axvline(peakA, color=HAIR, lw=1.5); ax.text(peakA + 0.3, 0.25, f"안 A 정점 {peakA}", color=MUTED, fontsize=13)
ax.set_ylim(0, 1.3); ax.set_ylabel("1σ 손실액 ÷ 급여 (년치)"); ax.set_xlabel("연도")
ax.set_title("정점 이후 '한 해 나쁜 해'가 급여 한 해분을 넘는가 — 비율이 아니라 금액의 위험", loc="left", color=NAVY)
ax.legend(loc="upper right", frameon=False, fontsize=13); ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_loss_ratio")

# 6. KIC 헤징 수요 — 1년 · 10년 최적 비중과 세 안 -----------------------------------------
a2 = R["agenda2"]; ins = a2["instruments"]
short = lambda t: t.split("(")[0].replace(" · 실물자산", "").strip()
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.5, 5.2), gridspec_kw={"width_ratios": [1.3, 1]}); fig.subplots_adjust(top=0.80, wspace=0.28)
names = ["주식"] + [short(i["name"]) for i in ins]
w1 = [a2["equity"]["w_1y_pct"]] + [i["w_1y_pct"] for i in ins]; wH = [a2["equity"]["w_10y_pct"]] + [i["w_10y_pct"] for i in ins]
yy = np.arange(len(names))
ax.barh(yy - 0.2, w1, height=0.38, color=MUTED, label="1년 최적(단기)"); ax.barh(yy + 0.2, wH, height=0.38, color=GREEN, label=f"{a2['horizon']}년 최적")
ax.set_yticks(yy); ax.set_yticklabels(names); ax.invert_yaxis(); ax.set_xlim(0, 80)
for k in range(len(names)):
    ax.text(w1[k] + 1, k - 0.2, f"{w1[k]:.1f}", va="center", fontsize=12, color=BODY); ax.text(wH[k] + 1, k + 0.2, f"{wH[k]:.1f}", va="center", fontsize=12, color=BODY)
ax.set_title("최적 비중(%) — 두 막대의 차이가 헤징 수요", loc="left", color=NAVY); ax.legend(loc="lower right", frameon=False, fontsize=12)
op = a2["options"]; lab = {"A": "A 헤지 없음", "B": "B 장기채+물가연동", "C": "C B+변동성 5%"}
bx.bar([lab[o["option"]] for o in op], [o["ce_10y_pct"] for o in op], color=[MUTED, GREEN, MUTED], width=0.55)
for k, o in enumerate(op): bx.text(k, o["ce_10y_pct"] + 0.02, f"{o['ce_10y_pct']:.2f}%\n({o['vs_A_bp']:+d}bp)", ha="center", fontsize=12, color=BODY)
bx.set_ylim(3.5, 4.45); bx.set_title("세 안의 10년 확실성등가(비용 차감)", loc="left", color=NAVY); bx.tick_params(axis="x", labelsize=11)
ax.grid(axis="x", color=HAIR, lw=0.8); bx.grid(axis="y", color=HAIR, lw=0.8)
fig.suptitle("장기 투자자는 장기채 · 물가연동채를 더 담는다 — 변동성 헤지는 두 지평 모두 0", x=0.01, y=0.97, ha="left", color=NAVY, fontsize=17)
save(fig, "fig_kic_hedge")

# 7. 간편 공식 vs 직접 계산 ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.6))
nm = [short(i["name"]) for i in ins]; xx = np.arange(len(nm))
f_ = [i["formula_pp"] for i in ins]; d_ = [i["hedge_pp"] for i in ins]
ax.bar(xx - 0.2, f_, width=0.38, color=MUTED, label="간편 공식 (1−1/γ)·β·σx/σa"); ax.bar(xx + 0.2, d_, width=0.38, color=GREEN, label="직접 계산 (10년 − 1년)")
for k in range(len(nm)):
    ax.text(k - 0.2, f_[k] + (1 if f_[k] >= 0 else -4), f"{f_[k]:+.1f}", ha="center", fontsize=12, color=BODY); ax.text(k + 0.2, d_[k] + 1, f"{d_[k]:+.1f}", ha="center", fontsize=12, color=BODY)
ax.axhline(3, color=ORANGE, ls=":", lw=1.5); ax.axhline(0, color=HAIR, lw=1); ax.set_ylim(-8, 50)
ax.set_xticks(xx); ax.set_xticklabels(nm); ax.set_ylabel("헤징 수요 (%p)"); ax.legend(frameon=False, fontsize=11, loc="upper left")
ax.set_title("공식은 공분산을 보지 않는다 — 크기를 놓친다", loc="left", color=NAVY); ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_kic_horizon")
print("charts done")
