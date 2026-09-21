#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W7 M9 케이스 v3 그림 — w7m9_results.json · CSV 에서 그린다 (matplotlib, Noto Sans CJK KR). 출력 img/*.png"""
import json, os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(HERE)
D, IMG = f"{W}/data", f"{W}/img"; os.makedirs(IMG, exist_ok=True)
fm.fontManager.addfont(os.path.expanduser("~/Library/Fonts/NotoSansCJK.ttc"))
plt.rcParams.update({"font.family": "Noto Sans CJK KR", "font.size": 15, "axes.titlesize": 17, "axes.labelsize": 15,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#6B7280", "axes.unicode_minus": False})
NAVY, BLUE, GREEN, ORANGE, GRAY, BODY, MUTED, HAIR, RED = "#1B2C5E", "#2E5BAA", "#3FA36F", "#E65100", "#F4F5F9", "#3B4252", "#6B7280", "#D6D6DB", "#B23A48"
R = json.load(open(f"{D}/w7m9_results.json"))
P = pd.read_csv(f"{D}/fml_w7m9_params.csv").set_index("key").value
G = pd.DataFrame(R["case1"]["grid"]); C1 = R["case1"]; C2 = R["case2"]
tdf = pd.read_csv(f"{D}/fml_w7m9_tdf_2022.csv"); alloc = pd.read_csv(f"{D}/fml_w7m9_endow_alloc.csv")
d1 = C1["default"]; d2 = C2["default"]


def save(fig, name):
    fig.savefig(f"{IMG}/{name}.png", dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig); print("→", name)


# ── 케이스 1 ──────────────────────────────────────────────────────────────────
# 1. 2022년 TDF 실적표
t = tdf[tdf.code != "TIAA_TRAD"].copy(); t = pd.concat([t, tdf[tdf.code == "TIAA_TRAD"]])
fig, ax = plt.subplots(figsize=(12.5, 5.2))
cols = [GREEN if v > 0 else (MUTED if c in ("KOSPI", "MSCI") else NAVY) for v, c in zip(t.ret_2022_pct, t.code)]
ax.barh(t.name, t.ret_2022_pct, color=cols, height=0.62)
for i, v in enumerate(t.ret_2022_pct): ax.text(v + (0.4 if v > 0 else -0.4), i, f"{v:+.1f}%", va="center", ha="left" if v > 0 else "right", fontsize=14, color=BODY)
ax.axvline(0, color=HAIR); ax.invert_yaxis(); ax.set_xlim(-28, 8); ax.set_xlabel("2022년 수익률 (%)")
ax.set_title("2022년 — Floor 가 없는 TDF 는 어디서나 −14~−17%, 보증형(TIAA)만 +3% (공시)", loc="left", color=NAVY)
ax.grid(axis="x", color=HAIR, lw=0.8)
save(fig, "fig_c1_tdf2022")

# 2. 조건 ①·② — Floor x 별 m 곡선 (수수료 0.5%)
fee0 = d1["fee_max"]
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.5, 5.2)); fig.subplots_adjust(top=0.82, wspace=0.25)
cx = {0.8: MUTED, 0.9: NAVY, 1.0: BLUE}
for x in [0.8, 0.9, 1.0]:
    g = G[(G.floor_x == x) & (G.fee_pct == fee0)].sort_values("m")
    ax.plot(g.m, g.p_safety_fail * 100, "-o", color=cx[x], lw=3 if x == 0.9 else 2, label=f"Floor x = {x:.2f}")
    bx.plot(g.m, g.p_cash_trap * 100, "-o", color=cx[x], lw=3 if x == 0.9 else 2, label=f"Floor x = {x:.2f}")
ax.axhline(5, color=ORANGE, ls=":", lw=1.5); ax.text(1, 5.6, "조건 ① 상한 5%", color=ORANGE, fontsize=13)
bx.axhline(10, color=ORANGE, ls=":", lw=1.5); bx.text(1, 10.8, "조건 ② 상한 10%", color=ORANGE, fontsize=13)
ax.set_title("조건 ① Safety 미달 확률 P(W_T < G_S) (%)", loc="left", color=NAVY); bx.set_title("조건 ② Cash Trap 확률 (%)", loc="left", color=NAVY)
for a in (ax, bx): a.set_xlabel("승수 m"); a.set_xticks(range(1, 7)); a.grid(axis="y", color=HAIR, lw=0.8); a.legend(frameon=False, fontsize=13)
fig.suptitle(f"승수 m 이 커질수록 ①·② 가 같이 나빠진다 — x = 0.90 은 m ≤ 2, x = 1.00 은 m ≤ 3 (수수료 {fee0}%)", x=0.01, y=0.97, ha="left", color=NAVY, fontsize=17)
save(fig, "fig_c1_cond12")

# 3. 조건 ③ — 수수료별 Market 달성 확률
fig, ax = plt.subplots(figsize=(12.5, 5.2))
for (x, m), col, ls in [((0.9, 2), NAVY, "-"), ((0.9, 3), BLUE, "--"), ((1.0, 2), GREEN, "-"), ((1.0, 3), GREEN, "--"), ((0.8, 1), MUTED, "-")]:
    g = G[(G.floor_x == x) & (G.m == m)].sort_values("fee_pct")
    ax.plot(g.fee_pct, g.p_market * 100, "-o", color=col, ls=ls, lw=3 if (x, m) == (0.9, 2) else 2, label=f"x = {x:.2f} · m = {m}")
ax.axhline(70, color=ORANGE, ls=":", lw=1.5); ax.text(0.52, 17.5, "점선 = 조건 ③ 하한 70% — Market 목표 = 원리금보장 3.09% 10년 복리", color=ORANGE, fontsize=13)
ax.axvline(0.59, color=HAIR, lw=1.5); ax.text(0.6, 79, "국내 TDF 총보수 평균 0.59% (2024년 말, 자본시장연구원)", color=MUTED, fontsize=12)
ax.set_xlabel("연 총보수 (%)"); ax.set_ylabel("P(W_T ≥ G_M) (%)"); ax.set_ylim(15, 82); ax.set_xticks([0.5, 0.8, 1.0, 1.2, 1.5])
ax.set_title("조건 ③ — 수수료가 Market 목표를 정한다: 0.5% 까지만 70% 를 넘고, GBI 예상 비용 0.8~1.5% 는 전부 미달", loc="left", color=NAVY)
ax.legend(frameon=False, fontsize=13, loc="upper right"); ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_c1_market")

# 4. 조건 ④ — 2022형 충격 Floor 위반율: GHP 연동 vs 고정 원금 / 갭 스트레스
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.5, 5.2), gridspec_kw={"width_ratios": [1.2, 1]}); fig.subplots_adjust(top=0.82, wspace=0.22)
g = G[(G.floor_x == 0.9) & (G.fee_pct == fee0)].sort_values("m")
xs = np.arange(1, 7)
ax.bar(xs - 0.2, g.shock_breach_ghp * 100, 0.4, color=NAVY, label="Floor = GHP 가격(금리 연동)")
ax.bar(xs + 0.2, g.shock_breach_fixed * 100, 0.4, color=RED, label="Floor = 고정 명목 원금")
for i, (a, b) in enumerate(zip(g.shock_breach_ghp, g.shock_breach_fixed)):
    ax.text(xs[i] - 0.2, a * 100 + 2, f"{a*100:.0f}", ha="center", fontsize=12, color=BODY); ax.text(xs[i] + 0.2, b * 100 + 2, f"{b*100:.0f}", ha="center", fontsize=12, color=BODY)
ax.axhline(1, color=ORANGE, ls=":", lw=1.5); ax.text(0.6, 3.5, "조건 ④ 상한 1%", color=ORANGE, fontsize=13)
ax.set_xlabel("승수 m"); ax.set_ylabel("Floor 위반율 (%)"); ax.set_ylim(0, 130); ax.set_xticks(xs)
ax.set_title("2022형(주식 −20% · 금리 +300bp), x = 0.90", loc="left", color=NAVY); ax.legend(frameon=False, fontsize=13, loc="upper left")
gp = pd.DataFrame(C1["gap_stress"])
bx.bar(gp.m, gp.breach * 100, 0.55, color=[GREEN if v <= 0.01 else (ORANGE if v < 0.5 else RED) for v in gp.breach])
for i, v in enumerate(gp.breach): bx.text(gp.m[i], v * 100 + 2, f"{v*100:.0f}", ha="center", fontsize=12, color=BODY)
bx.set_xlabel("승수 m (괄호 = 한 번에 깨지는 손실 1/m)"); bx.set_ylim(0, 130); bx.set_title("참고 — 한 달 −22% 갭(1987년 10월형), x = 1.00", loc="left", color=NAVY)
bx.set_xticks(list(gp.m)); bx.set_xticklabels([f"{m}\n({100/m:.0f}%)" for m in gp.m], fontsize=12)
for a in (ax, bx): a.grid(axis="y", color=HAIR, lw=0.8)
fig.suptitle("조건 ④ — 금리가 오르면 '고정 원금' Floor 는 예외 없이 깨진다 · 갭 위험은 1/m 에서 시작한다", x=0.01, y=0.97, ha="left", color=NAVY, fontsize=17)
save(fig, "fig_c1_shock")

# 5. 산수 — x=0.90 의 m 별 최종자산 분포(중위 · 하위 10% · 상위 10%)와 두 목표
fig, ax = plt.subplots(figsize=(12.5, 5.2))
for x, col, off in [(0.9, NAVY, -0.15), (1.0, BLUE, 0.15)]:
    g = G[(G.floor_x == x) & (G.fee_pct == fee0)].sort_values("m")
    ax.errorbar(g.m + off, g.median_W, yerr=[g.median_W - g.p10_W, g.p90_W - g.median_W], fmt="o", color=col, capsize=6, lw=2, ms=9, label=f"x = {x:.2f} — 중위(점) · 하위 10% ~ 상위 10%(막대)")
ax.axhline(C1["G_S"], color=ORANGE, ls=":", lw=1.5); ax.text(0.55, C1["G_S"] + 0.03, f"Safety 목표 G_S = {C1['G_S']:.2f}", color=ORANGE, fontsize=13)
ax.axhline(C1["G_M"], color=GREEN, ls=":", lw=1.5); ax.text(0.55, C1["G_M"] + 0.03, f"Market 목표 G_M = {C1['G_M']:.3f} (원리금보장 3.09%)", color=GREEN, fontsize=13)
bh = [b for b in C1["buyhold"] if b["w_eq"] == 0.6 and b["fee_pct"] == 0.8][0]
ax.axhline(bh["median_W"], color=MUTED, ls="--", lw=1.2); ax.text(3.35, bh["median_W"] + 0.04, f"참고 — 고정 60/40(TDF형, 0.8%) 중위 {bh['median_W']:.2f} · Safety 미달 {bh['p_safety_fail']*100:.1f}%", color=MUTED, fontsize=12, bbox=dict(facecolor="white", edgecolor="none", alpha=0.9))
ax.set_xlabel("승수 m"); ax.set_ylabel("10년 후 자산 (초기 = 1)"); ax.set_xticks(range(1, 7)); ax.set_ylim(0.8, 3.0)
ax.set_title(f"산수 — m 을 키우면 중위는 오르지만 하위 10% 는 Floor 로 내려앉는다 (수수료 {fee0}%, 4,000 경로)", loc="left", color=NAVY)
ax.legend(frameon=False, fontsize=13, loc="upper left"); ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_c1_dist")

# 6. 한국 퇴직연금·디폴트옵션 공시 — 쏠림
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.5, 5.0), gridspec_kw={"width_ratios": [1, 1]}); fig.subplots_adjust(top=0.82, wspace=0.3)
cats = ["퇴직연금 전체\n501.4조", "디폴트옵션\n53.3조"]; guar = [75.4, 85.4]; perf = [100 - 75.4, 100 - 85.4]
ax.bar(cats, guar, color=MUTED, width=0.55, label="원리금보장(안정형)"); ax.bar(cats, perf, bottom=guar, color=NAVY, width=0.55, label="실적배당(투자형)")
for i, v in enumerate(guar): ax.text(i, v / 2, f"{v:.1f}%", ha="center", va="center", color="white", fontsize=15, fontweight="bold")
for i, v in enumerate(perf): ax.text(i, guar[i] + v / 2, f"{v:.1f}%", ha="center", va="center", color="white", fontsize=14)
ax.set_ylim(0, 100); ax.set_title("적립금 구성 (2025년 말, 금감원·고용노동부 공시)", loc="left", color=NAVY); ax.legend(frameon=False, fontsize=12, loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.14))
rets = [("원리금보장 평균", 3.09, MUTED), ("퇴직연금 전체", 6.47, BLUE), ("실적배당 평균", 16.80, NAVY)]
bx.bar([r[0] for r in rets], [r[1] for r in rets], color=[r[2] for r in rets], width=0.55)
for i, r in enumerate(rets): bx.text(i, r[1] + 0.4, f"{r[1]:.2f}%", ha="center", fontsize=14, color=BODY)
bx.set_ylim(0, 20); bx.set_title("2025년 운용수익률 (%)", loc="left", color=NAVY)
for a in (ax, bx): a.grid(axis="y", color=HAIR, lw=0.8)
fig.suptitle("디폴트옵션 지정 가입자 734만 명 중 583만 명(79.4%)이 안정형 — 3.09% 가 Market 목표의 기준이 되는 이유", x=0.01, y=0.97, ha="left", color=NAVY, fontsize=17)
save(fig, "fig_c1_market_facts")

# ── 케이스 2 ──────────────────────────────────────────────────────────────────
# 7. 조건 ① — 락업 생존 연수
lk = pd.DataFrame(C2["lockup"])
fig, ax = plt.subplots(figsize=(12.5, 5.0))
ax.bar(lk.illiq_cap_pct.astype(str) + "%", lk.survival_years, color=[GREEN if c else RED for c in lk.c1], width=0.55)
for i, (v, c) in enumerate(zip(lk.survival_years, lk.c1)): ax.text(i, v + 0.4, f"{v}년", ha="center", fontsize=14, color=BODY)
ax.axhline(float(P["lockup_years"]), color=ORANGE, ls=":", lw=1.5); ax.text(2.45, float(P["lockup_years"]) + 1.6, f"조건 ① 락업 {int(float(P['lockup_years']))}년 — 짧으면 '팔 수 없는 자산'을 팔아야 한다", color=ORANGE, fontsize=13)
ax.set_xlabel("비유동 대체 상한 x"); ax.set_ylabel("매도 없이 버티는 연수"); ax.set_ylim(0, 25)
ax.set_title("조건 ① 실질 지평 — 2022형 충격 + 3년차 목돈 600억 + 캐피탈콜 아래 안전·상장 자산만으로 버티는 연수", loc="left", color=NAVY)
ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_c2_lockup")

# 8. 조건 ② — 실질가치 유지 확률
mc = pd.DataFrame(C2["mc"])
fig, ax = plt.subplots(figsize=(12.5, 5.2))
cx2 = {0: MUTED, 10: HAIR, 20: NAVY, 30: BLUE, 40: "#7FA6D9", 60: RED}
for x in sorted(mc.illiq_cap_pct.unique()):
    g = mc[mc.illiq_cap_pct == x].sort_values("z_pct")
    ax.plot(g.z_pct, g.p_real_keep * 100, "-o", color=cx2[x], lw=3.2 if x == d2["x"] else 1.8, ms=8 if x == d2["x"] else 6, label=f"x = {x}%" + (" (기본 답)" if x == d2["x"] else ""))
ax.axhline(50, color=ORANGE, ls=":", lw=1.5); ax.text(3.52, 51, "조건 ② 하한 50% — 세대 간 중립(30년 후 실질가치 ≥ 지금)", color=ORANGE, fontsize=13)
ax.axvline(5.25, color=HAIR, lw=1.5); ax.text(5.27, 88, "Yale 5.25%", color=MUTED, fontsize=12)
ax.set_xlabel("지출률 z (%)"); ax.set_ylabel("P(실질가치 유지) (%)"); ax.set_xticks([3.5, 4.0, 4.5, 5.25]); ax.set_ylim(20, 95)
ax.set_title("조건 ② — x = 20% 는 z 4.5% 까지, x = 0%(GPFG 형) 는 4.0% 까지 · Yale 의 5.25% 는 x ≥ 30% 에서만 (4,000 경로 · 30년)", loc="left", color=NAVY)
ax.legend(frameon=False, fontsize=12, loc="lower left", ncol=2); ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_c2_realkeep")

# 9. 조건 ④ — 안전 유동자산 하한
bf = pd.DataFrame(C2["buffer"])
fig, ax = plt.subplots(figsize=(12.5, 4.8))
ax.bar(bf.y_pct.astype(str) + "%", bf.p_no_forced_and_spend * 100, color=[GREEN if v >= 0.95 else RED for v in bf.p_no_forced_and_spend], width=0.55)
for i, v in enumerate(bf.p_no_forced_and_spend): ax.text(i, v * 100 + 2, f"{v*100:.0f}%", ha="center", fontsize=14, color=BODY)
ax.axhline(95, color=ORANGE, ls=":", lw=1.5); ax.text(-0.4, 97, "조건 ④ 하한 95%", color=ORANGE, fontsize=13)
ax.set_xlabel("안전 유동자산(현금 · 국채) 하한 y"); ax.set_ylabel("강제매도 없이 3년 지출 유지 (%)"); ax.set_ylim(0, 112)
ax.set_title(f"조건 ④ — 산수로는 22.7%(고정 지출 3년 + 목돈)지만 국채도 −15% 맞는 해가 있어 y = {d2['y']}% 가 하한 (x = 20 · z = 4.5)", loc="left", color=NAVY)
ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_c2_buffer")

# 10. 배분안 — 비유동 상한별 (GPFG 참고)
fig, ax = plt.subplots(figsize=(12.5, 5.0))
labels = [f"x = {x}%" for x in alloc.illiq_cap_pct] + ["GPFG\n(2025 말)"]
w_eq = list(alloc.w_eq) + [71.3]; w_bd = list(alloc.w_bond_gov) + [26.5]; w_cs = list(alloc.w_cash) + [0]; w_pe = list(alloc.w_alt_pe) + [2.1]
bot = np.zeros(len(labels))
for vals, col, name in [(w_pe, RED, "비유동 대체(PE·VC·사모부동산)"), (w_eq, NAVY, "주식(상장 대체 포함)"), (w_bd, BLUE, "국채·우량채"), (w_cs, MUTED, "현금")]:
    ax.bar(labels, vals, bottom=bot, color=col, width=0.6, label=name)
    for i, v in enumerate(vals):
        if v >= 8: ax.text(i, bot[i] + v / 2, f"{v:.0f}", ha="center", va="center", color="white", fontsize=13)
    bot += np.array(vals)
ax.set_ylim(0, 100); ax.set_ylabel("%"); ax.legend(frameon=False, fontsize=12, loc="upper center", ncol=4, bbox_to_anchor=(0.5, -0.12))
ax.set_title("H대 배분안(교육용) — 비유동 상한 x 마다 주식·채권을 줄여 채운다 · GPFG 는 비상장 2.1%(부동산 1.7 · 인프라 0.4)", loc="left", color=NAVY)
save(fig, "fig_c2_alloc")

# 11. Spending Rule 예시 — 80/20 평활 vs 즉시 반영, 2022형 충격
z = d2["z"] / 100; W0 = 5000.0; S = 200.0; mu = [m for m in C2["spend_rule"] if m["illiq_cap_pct"] == d2["x"]][0]["mu_nominal"] / 100
Ws = [W0]; Ss = [S]; Sn = [S]; Fx = [175.0]
for t in range(1, 11):
    r = -0.153 if t == 1 else mu
    Wt = Ws[-1] * (1 + r) - Ss[-1] - (600 if t == 3 else 0)
    Ws.append(Wt); Ss.append(0.8 * Ss[-1] * 1.02 + 0.2 * z * Ws[-2]); Sn.append(z * Ws[-2]); Fx.append(175 * 1.02 ** t)
fig, ax = plt.subplots(figsize=(12.5, 5.0))
yrs = list(range(0, 11))
ax.plot(yrs, Ss, "-o", color=NAVY, lw=3, label="80/20 평활 지출 S_t (z = 4.5%)")
ax.plot(yrs, Sn, "--o", color=MUTED, lw=2, label="평활 없이 z·W_{t−1}")
ax.plot(yrs, Fx, ":", color=ORANGE, lw=2, label="고정 지출 Floor(장학·연구 175억, 물가 연동)")
ax.axvspan(0.5, 1.5, color="#FBEAEA", alpha=0.6); ax.text(1, 262, "1년차 2022형\n(포트폴리오 −15%)", ha="center", color=RED, fontsize=12)
ax.axvline(3, color=HAIR); ax.text(3.05, 262, "3년차 목돈 600억", color=MUTED, fontsize=12)
ax.set_xlabel("연차"); ax.set_ylabel("억 원"); ax.set_ylim(150, 280); ax.set_xticks(yrs)
ax.set_title("Spending Rule — 평활이 있으면 충격의 해에도 지출은 4% 만 줄고 Floor 위에 남는다 (결정론 예시, μ = 기대수익)", loc="left", color=NAVY)
ax.legend(frameon=False, fontsize=13, loc="lower right"); ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_c2_spendrule")
print("charts done")
