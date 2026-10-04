#!/usr/bin/env python3
"""LDI 요약·기초 덱 — 수식 PNG · matplotlib 차트 · SVG→PNG 를 한 번에 만든다.
실행: (이 폴더에서) <python> assets.py   → eq/*.png, fig/*.png, eq/ratios.json, fig/ratios.json
수치는 W06 M7 강의본·도출 II 덱의 가상 기금(자산 100 · 부채 80)과 국민연금 케이스에서 온다."""
import json, math, os, glob
import numpy as np
import cairosvg
from PIL import Image
from render_eq import render, INK, PAPER, LIME, DARK
from zo_mpl import fig, save, C

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
os.makedirs("eq", exist_ok=True); os.makedirs("fig", exist_ok=True)
G, D = (INK, PAPER), (LIME, DARK)

# ---------------------------------------------------------------- 수식 ----
EQ = {
 "pv":     (r"L=\sum_{t=1}^{T}\frac{CF_t}{(1+r)^t}=\sum_{t=1}^{T}CF_t\,B(t)", G),
 "fr":     (r"\mathrm{FR}=\frac{A}{L},\qquad S=A-L", G),
 "dfr":    (r"\Delta\mathrm{FR}\approx\mathrm{FR}\cdot(r_A-r_L)", G),
 "rs":     (r"R_S=\frac{\Delta S}{A}=r_A-\frac{L}{A}\,r_L", D),
 "dur":    (r"D=\sum_t t\cdot\frac{PV_t}{V},\qquad \frac{\Delta V}{V}\approx-D\,\Delta y", G),
 "gap":    (r"\Delta S\approx-(D_A\,A-D_L\,L)\,\Delta y", D),
 "dv01":   (r"\mathrm{DV01}=D\times V\times 0.0001", G),
 "conv":   (r"\frac{\Delta V}{V}\approx-D\,\Delta y+\frac{1}{2}\,C\,(\Delta y)^2", G),
 "h":      (r"h=\frac{\mathrm{DV01}_A}{\mathrm{DV01}_L}=\frac{D_A\,A}{D_L\,L}", D),
 "red1":   (r"A\geq L", G),
 "red2":   (r"D_A\,A=D_L\,L", G),
 "red3":   (r"C_A\,A\geq C_L\,L", D),
 "cf":     (r"N_t=CF_t\quad(t\leq T_1)", G),
 "whedge": (r"w_{\mathrm{hedge}}=h\cdot\frac{D_L\,L}{D_H\,A}", G),
 "margin": (r"\mathrm{Margin}\approx\mathrm{DV01}_{\mathrm{swap}}\times\Delta y_{\mathrm{bp}}", G),
 "buffer": (r"\Delta y^{*}=\frac{K}{E\,D}=\frac{1}{\lambda D},\qquad \lambda\leq\frac{1}{0.025\,D}", D),
 "loop":   (r"\Delta y_{t+1}=\kappa\,E\,D\;\Delta y_t", D),
 "svb":    (r"\Delta E\approx-D_A\,A\,\Delta y", G),
 "obj":    (r"\max_{w}\ \mathbb{E}[R_S]-\frac{\gamma}{2}\,\mathrm{Var}(R_S)", G),
 "wstar":  (r"w_i^{*}=\frac{\mu_i}{\gamma\,\sigma_i^2}+\frac{1}{\mathrm{FR}}\cdot\frac{\mathrm{Cov}(r_i,R_L)}{\sigma_i^2}", D),
 "psp":    (r"\frac{\mu_i}{\gamma\,\sigma_i^2}", G),
 "lhp":    (r"\frac{1}{\mathrm{FR}}\cdot\frac{\mathrm{Cov}(r_i,R_L)}{\sigma_i^2}", G),
 "wb":     (r"w_B^{*}=\frac{1}{\mathrm{FR}}\cdot\frac{D_L}{D_B}\quad\Leftrightarrow\quad w_B^{*}\,A\,D_B=L\,D_L", G),
 "sigs":   (r"\sigma_S=\sqrt{(w_S\,\sigma_{eq})^2+\left(\frac{D_L}{\mathrm{FR}}\,(1-h)\,\sigma_y\right)^2}", D),
 "hnps":   (r"h=\frac{0.158}{7.43}\approx 2.1\%", G),
 "q30":    (r"Q_{30y}=\frac{\Delta\mathrm{DV01}}{(D_{30y}-D_{bond})\times 10^{-4}}", G),
}
for k in ("pv", "rs", "gap", "h", "red2", "buffer", "wstar", "sigs"):
    EQ["sm_" + k] = (EQ[k][0], G)
eq_ratio = {}
for k, (tex, (fg, bg)) in EQ.items():
    _, r = render(tex, f"{k}.png", fontsize=30, color=fg, bg=bg)
    eq_ratio[k] = round(r, 4)
json.dump(eq_ratio, open("eq/ratios.json", "w"), indent=1)

fig_ratio = {}
def keep(name, ratio): fig_ratio[name] = round(ratio, 4)

# ---------------------------------------------------------------- 차트 ----
# c_pv — 만기별 100의 오늘 값 (3% vs 5%), 20년 표시
t = np.arange(0, 41)
f, ax = fig("panel")
ax.plot(t, 100 / 1.03 ** t, color=C["teal"], label="할인율 3%")
ax.plot(t, 100 / 1.05 ** t, color=C["blue"], label="할인율 5%")
for r, col, dx, dy in ((0.03, C["teal"], 8, 6), (0.05, C["blue"], -52, -26)):
    v = 100 / (1 + r) ** 20
    ax.plot([20], [v], "o", color=col)
    ax.annotate(f"{v:.1f}", (20, v), xytext=(dx, dy), textcoords="offset points",
                color=col, fontsize=15, fontweight="bold")
ax.axvline(20, color=C["hair"], lw=1.2, ls="--")
ax.set_xlabel("지급 시점 (년)"); ax.set_ylabel("100의 오늘 값")
ax.set_ylim(0, 105); ax.legend(loc="upper right")
keep("c_pv", save(f, "fig/c_pv.png"))

# c_gap — 금리 1%p 하락 전후 자산·부채·잉여금
f, ax = fig("panel")
lab = ["자산", "부채", "잉여금"]
before, after = [100, 80, 20], [103, 96, 7]
x = np.arange(3); wd = 0.36
b1 = ax.bar(x - wd / 2, before, wd, color=C["muted"], label="지금")
b2 = ax.bar(x + wd / 2, after, wd, color=[C["teal"], C["teal"], C["red"]], label="금리 1%p 하락 후")
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 2, f"{b.get_height():g}",
                ha="center", fontsize=15, fontweight="bold", color=C["body"])
ax.set_xticks(x, lab); ax.set_ylim(0, 138); ax.set_ylabel("금액")
ax.legend(loc="upper center", ncol=2, handles=[b1, b2[0]], labels=["지금", "금리 1%p 하락 후"])
keep("c_gap", save(f, "fig/c_gap.png"))

# c_conv — 10년 뒤 100 (V 60.65, D 10, C 100): 정확 vs 1차 vs 1차+2차
dy = np.linspace(-0.04, 0.04, 161)
V0 = 100 * math.exp(-0.5)
exact = 100 * np.exp(-10 * (0.05 + dy)) - V0
first = -10 * V0 * dy
second = first + 0.5 * 100 * V0 * dy ** 2
f, ax = fig("panel")
ax.plot(dy * 100, exact, color=C["teal"], label="정확한 값")
ax.plot(dy * 100, first, color=C["muted"], ls="--", label="듀레이션만 (1차)")
ax.plot(dy * 100, second, color=C["amber"], ls=":", lw=3, label="볼록성 추가 (2차)")
ax.axhline(0, color=C["hair"], lw=1)
ax.annotate("+2%p: 정확 −11.0\n1차만 −12.1", (2, -12.13), xytext=(-150, -38), textcoords="offset points",
            fontsize=14, color=C["body"], arrowprops=dict(arrowstyle="->", color=C["muted"]))
ax.set_xlabel(r"금리 변화 $\Delta y$ (%p)"); ax.set_ylabel(r"가격 변화 $\Delta V$")
ax.legend(loc="upper right")
keep("c_conv", save(f, "fig/c_conv.png"))

# c_hedge — 금리 1%p 하락 후 잉여금 (h 19 · 72 · 100%)
f, ax = fig("panel")
names = ["지금\nh = 19%", "50을 30년물로\nh = 72%", "80을 30년물로\nh = 100%"]
vals = [7, 15.5, 20]
bars = ax.bar(names, vals, color=[C["red"], C["teal"], C["lime"]], width=0.58,
              edgecolor=[C["red"], C["teal"], C["lime_dk"]])
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v:g}", ha="center",
            fontsize=16, fontweight="bold", color=C["body"])
ax.axhline(20, color=C["muted"], lw=1.2, ls="--")
ax.text(-0.29, 20.6, "출발 잉여금 20", ha="left", fontsize=14, color=C["muted"])
ax.set_ylim(0, 24); ax.set_ylabel("금리 1%p 하락 후 잉여금")
keep("c_hedge", save(f, "fig/c_hedge.png"))

# c_red — 바벨 vs 불일치: 금리 변화별 잉여금
dy = np.linspace(-0.025, 0.025, 101)
y = 0.05 + dy
L = 100 * np.exp(-10 * y)
Ab = 38.94 * np.exp(-5 * y) + 64.20 * np.exp(-15 * y)
Am = 77.88 * np.exp(-5 * y)
f, ax = fig("panel")
ax.plot(dy * 100, Ab - L, color=C["lime_dk"], label="바벨 5년 + 15년 (D 10 · C 125)")
ax.plot(dy * 100, Am - L, color=C["red"], label="5년물 하나 (D 5)")
ax.axhline(0, color=C["muted"], lw=1)
for d, v, col in ((-2, -7.05, C["red"]), (-2, 0.37, C["lime_dk"])):
    ax.plot([d], [v], "o", color=col)
    ax.annotate(f"{v:+.2f}", (d, v), xytext=(10, -4 if v < 0 else 8), textcoords="offset points",
                fontsize=15, fontweight="bold", color=col)
ax.set_xlabel(r"금리 변화 $\Delta y$ (%p)"); ax.set_ylabel(r"잉여금 $S$")
ax.legend(loc="lower right")
keep("c_red", save(f, "fig/c_red.png"))

# c_buffer — 남은 헤지 자본 vs 금리 상승폭 (E 80, D 20)
bp = np.linspace(0, 400, 201)
f, ax = fig("panel")
for lam, col in ((1.6, C["teal"]), (2.0, C["amber"]), (3.0, C["red"])):
    K = 80 / lam
    ax.plot(bp, np.maximum(K - 80 * 20 * bp / 1e4, 0), color=col,
            label=rf"$\lambda$ = {lam:g}  (K {K:.0f})")
ax.axvline(250, color=C["body"], ls="--", lw=1.4)
ax.text(255, 46, "규제 기준 250bp", fontsize=14, color=C["body"])
ax.set_xlabel("금리 상승 (bp)"); ax.set_ylabel("남은 헤지 자본")
ax.set_ylim(0, 52); ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.86))
keep("c_buffer", save(f, "fig/c_buffer.png"))

# c_budget — 잉여금 변동성과 9% 예산 아래 주식 한도
h = np.linspace(0, 1, 201)
rate = 16 * (1 - h) * 0.8
sig = np.sqrt(7.5 ** 2 + rate ** 2)
cap = np.where(rate < 9, np.sqrt(np.maximum(81 - rate ** 2, 0)) / 15 * 100, 0)
f, (a1, a2) = fig("panel", 2, 1)
a1.plot(h * 100, sig, color=C["teal"])
a1.text(52, 11.0, "잉여금 변동성", fontsize=14, color=C["teal"], fontweight="bold")
a1.plot(h * 100, rate, color=C["blue"], ls="--")
a1.text(30, 2.0, "헤지 안 된 금리 위험", fontsize=14, color=C["blue"])
a1.axhline(7.5, color=C["muted"], lw=1, ls=":")
for hh, v in ((19, 12.8), (100, 7.5)):
    a1.plot([hh], [v], "o", color=C["teal"])
    a1.annotate(f"{v}%", (hh, v), xytext=(-12, 9), textcoords="offset points",
                fontsize=15, fontweight="bold", color=C["teal"])
a1.set_ylabel("변동성 (%)")
a1.set_ylim(0, 16)
a2.plot(h * 100, cap, color=C["lime_dk"])
for hh, v in ((44, 36), (60, 49), (100, 60)):
    a2.plot([hh], [v], "o", color=C["lime_dk"])
    a2.annotate(f"{v}%", (hh, v), xytext=(-30, 8), textcoords="offset points",
                fontsize=15, fontweight="bold", color=C["body"])
a2.set_xlabel("헤지 비율 h (%)"); a2.set_ylabel("주식 한도 (%)")
a2.set_ylim(0, 72)
keep("c_budget", save(f, "fig/c_budget.png"))

# c_trigger — 적립비율 트리거 계단 (도출 II 7-1)
fr = [90, 110, 110, 120, 120, 135, 135, 145]
hh = [50, 50, 70, 70, 90, 90, 100, 100]
eqw = [60, 60, 55, 55, 50, 50, 35, 35]
f, ax = fig("panel")
ax.plot(fr, hh, color=C["teal"], label="헤지 비율 h")
ax.plot(fr, eqw, color=C["amber"], label="주식 비중")
ax.axvline(125, color=C["red"], ls="--", lw=1.4)
ax.text(126, 8, "지금 125%", color=C["red"], fontsize=14, fontweight="bold")
ax.set_xlabel("적립비율 (%)"); ax.set_ylabel("비중 (%)")
ax.set_ylim(0, 110); ax.legend(loc="upper left")
keep("c_trigger", save(f, "fig/c_trigger.png"))

# c_nps — 국민연금 적립비율의 두 눈금
f, ax = fig("panel")
names = ["자체 5.5%\n순부채 1,542조", "국채 곡선\n순부채 2,122조", "국채 곡선\n금리 −100bp"]
vals = [95, 69, 49]
bars = ax.bar(names, vals, color=[C["muted"], C["teal"], C["red"]], width=0.58)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v}%", ha="center",
            fontsize=16, fontweight="bold", color=C["body"])
ax.axhline(100, color=C["hair"], lw=1.2, ls="--")
ax.set_ylim(0, 112); ax.set_ylabel("적립비율 (%)")
keep("c_nps", save(f, "fig/c_nps.png"))

# ---------------------------------------------------------------- SVG ----
for svg in sorted(glob.glob("svg/*.svg")):
    name = os.path.splitext(os.path.basename(svg))[0]
    out = f"fig/{name}.png"
    cairosvg.svg2png(url=svg, write_to=out, output_width=None)
    im = Image.open(out).convert("RGB"); im.save(out)
    keep(name, im.width / im.height)
    print(f"[svg] {out} {im.width}x{im.height}")

json.dump(fig_ratio, open("fig/ratios.json", "w"), indent=1)
print("eq", len(eq_ratio), "fig", len(fig_ratio))
